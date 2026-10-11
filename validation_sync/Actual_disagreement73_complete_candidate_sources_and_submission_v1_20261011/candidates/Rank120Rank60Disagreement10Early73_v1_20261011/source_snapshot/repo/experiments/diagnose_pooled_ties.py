"""Ex-post attribution of the frozen pooled-vs-daily-z 2024 return Top.

No fitting, forecast changes, tie-break choices, or adoption-rule changes.
The new output directory is created once; old or partial outputs are not reused.
"""
from __future__ import annotations

import argparse
import io
import json
import time
from pathlib import Path

import numpy as np
import pandas as pd
import polars as pl
from scipy.stats import spearmanr

from experiments.day_balance_models import file_hash
from experiments.official_seed_development import original_labels

ROOT = Path(__file__).resolve().parents[1]
PRIOR = ROOT / "experiments/return_pooled_eval"
OUT = ROOT / "experiments/pooled_tie_diagnosis"
KEYS = ["ts_code", "trade_date"]
MODELS = ("reference", "candidate")
STATES = ("raw_stable", "raw_default", "parsed_stable", "parsed_default")
N_DAYS = 242
YEAR = 2024
TOL = 1e-12


def read(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_new(path: Path, record: dict) -> None:
    with path.open("x", encoding="utf-8") as stream:
        json.dump(record, stream, ensure_ascii=False, indent=2, allow_nan=False)


def frozen_sources() -> dict:
    diagnostic, development, decision = (read(PRIOR / name) for name in
                                        ("diagnostic_2024.json", "development.json", "decision.json"))
    assert decision["diagnostic_2024_sha256"] == file_hash(PRIOR / "diagnostic_2024.json")
    assert decision["development_sha256"] == file_hash(PRIOR / "development.json")
    assert diagnostic["protocol_sha256"] == file_hash(PRIOR / "protocol.json")
    locks = {}
    for mapping in (read(PRIOR / "prior_artifacts_sha256.json"), diagnostic["artifacts_sha256"],
                    development["artifacts_sha256"], diagnostic["production_after"]):
        for relative, expected in mapping.items():
            path = ROOT / relative
            normalized = path.relative_to(ROOT).as_posix()
            if normalized in locks and locks[normalized] != expected:
                raise ValueError(f"Contradictory frozen hashes: {relative}")
            if file_hash(path) != expected:
                raise ValueError(f"Frozen artifact changed: {relative}")
            locks[normalized] = expected
    for path in list(PRIOR.iterdir()) + [Path(__file__), ROOT / "evaluate.py",
                                       ROOT / "experiments/official_seed_development.py",
                                       ROOT / "experiments/day_balance_models.py"]:
        if path.is_file():
            locks[path.relative_to(ROOT).as_posix()] = file_hash(path)
    return dict(sorted(locks.items()))


def csv_parse(frame: pl.DataFrame) -> pd.DataFrame:
    # Same Polars fixed-decimal serialization and pandas default parser as the
    # frozen official_score helper. No round_trip parser or artificial tie key.
    return pd.read_csv(io.StringIO(frame.write_csv(float_precision=17)))


def selections(group: pd.DataFrame) -> dict:
    eligible = group[(group.flag_limit_up == 0) & group.y_original.notna()].copy()
    if len(eligible) < 100:
        raise ValueError("This frozen 242-day diagnostic requires >=100 return-eligible rows per date")
    k = max(len(eligible) // 10, 1)
    result = {}
    for state in STATES:
        column = "pred_raw" if state.startswith("raw") else "pred_parsed"
        options = {"kind": "stable"} if state.endswith("stable") else {}
        ordered = eligible.sort_values(column, ascending=False, **options)
        top = ordered.iloc[:k]
        cutoff = float(ordered[column].iloc[k-1])
        tie = eligible[eligible[column] == cutoff]
        above = int((eligible[column] > cutoff).sum())
        result[state] = {"ordered": ordered, "top": top, "ids": set(top.index), "k": k,
                         "cutoff": cutoff, "tie_ids": set(tie.index), "tie_count": len(tie),
                         "above": above, "straddling_tie": bool(above < k < above+len(tie)),
                         "excess_original": float(top.y_original.mean()-ordered.y_original.mean()),
                         "excess_parsed": float(top.y_parsed.mean()-ordered.y_parsed.mean()),
                         "top_original": float(top.y_original.mean()),
                         "top_parsed": float(top.y_parsed.mean()),
                         "market_original": float(ordered.y_original.mean()),
                         "market_parsed": float(ordered.y_parsed.mean())}
    return result


def classification(group: pd.DataFrame, before: set, after: set) -> dict:
    entrants, exits = sorted(after-before), sorted(before-after)
    combinations = [(i, j) for i in entrants for j in exits]
    counts = {"csv_created_tie_pairs": 0, "csv_broken_tie_pairs": 0,
              "precision_reversal_pairs": 0, "preexisting_exact_tie_pairs": 0}
    for i, j in combinations:
        a, b = group.loc[i], group.loc[j]
        raw, parsed = np.sign(a.pred_raw-b.pred_raw), np.sign(a.pred_parsed-b.pred_parsed)
        counts["csv_created_tie_pairs"] += int(raw != 0 and parsed == 0)
        counts["csv_broken_tie_pairs"] += int(raw == 0 and parsed != 0)
        counts["precision_reversal_pairs"] += int(raw*parsed < 0)
        counts["preexisting_exact_tie_pairs"] += int(raw == 0 and parsed == 0)
    return {**counts, "entered": len(entrants), "exited": len(exits),
            "pair_definition": "Cartesian entrant/exiter comparisons, not a causal pairing"}


def self_test() -> dict:
    n = 130
    g = pd.DataFrame({"ts_code": [f"S{i}" for i in range(n)], "trade_date": 20240102,
                      "pred_raw": np.repeat(np.arange(13, dtype=float), 10),
                      "pred_parsed": np.repeat(np.arange(13, dtype=float), 10),
                      "flag_limit_up": 0, "y_original": np.linspace(-.02, .03, n),
                      "y_parsed": np.linspace(-.02, .03, n)})
    states = selections(g)
    assert states["raw_stable"]["straddling_tie"]
    for state in STATES:
        assert states[state]["k"] == 13
    a, b = states["raw_stable"], states["raw_default"]
    contribution = sum(g.loc[i, "y_original"]/13 for i in b["ids"]-a["ids"])
    contribution -= sum(g.loc[i, "y_original"]/13 for i in a["ids"]-b["ids"])
    assert abs(contribution-(b["excess_original"]-a["excess_original"])) < 1e-15
    g.loc[0, "y_original"] = np.nan
    g.loc[0, "y_parsed"] = np.nan
    g.loc[1, "flag_limit_up"] = 1
    assert all(0 not in s["ids"] and 1 not in s["ids"] for s in selections(g).values())
    pair = pd.DataFrame({"pred_raw": [1.0, np.nextafter(1.0, 0.0)], "pred_parsed": [1.0, 1.0]})
    assert classification(pair, {0}, {1})["csv_created_tie_pairs"] == 1
    pair["pred_parsed"] = [0.0, 2.0]
    assert classification(pair, {0}, {1})["precision_reversal_pairs"] == 1
    return {"status": "passed", "synthetic_boundary_tie": True,
            "stock_sum_matches_top_difference": True, "missing_and_limitup_exclusion": True,
            "new_tie_and_reversal_detection": True}


def _event(date: int, component: str, path: str, model: str, action: str, index: int,
           coefficient: float, data: dict, states: dict, use_label_delta: bool = False) -> dict:
    row = data[model].loc[index]
    raw, parsed = states[model]["raw_stable"], states[model]["parsed_stable"]
    value = float(row.y_parsed-row.y_original) if use_label_delta else float(row.y_original)
    daily = coefficient*value
    return {"trade_date": date, "path": path, "component": component, "model": model,
            "action": action, "ts_code": row.ts_code, "source_row_index": index,
            "portfolio_coefficient": coefficient, "n_top": raw["k"],
            "pred_raw": float(row.pred_raw), "pred_parsed": float(row.pred_parsed),
            "pred_raw_hex": float(row.pred_raw).hex(), "pred_parsed_hex": float(row.pred_parsed).hex(),
            "raw_boundary_score": raw["cutoff"], "parsed_boundary_score": parsed["cutoff"],
            "raw_boundary_tie_group_size": raw["tie_count"], "parsed_boundary_tie_group_size": parsed["tie_count"],
            "is_raw_boundary_group": index in raw["tie_ids"], "is_parsed_boundary_group": index in parsed["tie_ids"],
            "y_original": float(row.y_original), "y_parsed": float(row.y_parsed),
            "y_original_hex": float(row.y_original).hex(), "y_parsed_hex": float(row.y_parsed).hex(),
            "y_missing": bool(pd.isna(row.y_original)), "flag_limit_up": int(row.flag_limit_up),
            "daily_excess_contribution": daily,
            "annual_excess_contribution": daily*252/N_DAYS,
            "composite_top_component_contribution": daily*252/N_DAYS*.3}


def diagnose(resume_input_validation: bool = False) -> dict:
    started = time.monotonic()
    recovery = None
    if OUT.exists() and resume_input_validation:
        if {path.name for path in OUT.iterdir()} != {"protocol.json"}:
            raise FileExistsError("Recovery requires exactly the initial protocol and no outputs")
        recovery = {"prior_protocol_sha256": file_hash(OUT/"protocol.json"),
                    "reason": "The first run stopped before the daily loop: dict(DataFrameGroupBy) invoked pandas' string keys attribute. Replace with an explicit iteration comprehension; preserve all analysis rules.",
                    "prior_statistics_or_outputs_created": False}
    elif OUT.exists():
        raise FileExistsError("Refusing to overwrite an existing or partial diagnosis directory")
    tests = self_test()
    locks = frozen_sources()
    OUT.mkdir(exist_ok=resume_input_validation)
    protocol = {"diagnostic_only": True, "year": YEAR, "models": list(MODELS), "days": N_DAYS,
                "source_artifacts_sha256": locks, "script_sha256": file_hash(Path(__file__)),
                "predictions_frozen": True, "no_training_or_tuning": True,
                "no_adoption_rule_changes": True, "labels_for_ex_post_attribution_only": True,
                "eligibility": "flag_limit_up==0 and y_ret_1d.notna; n_top=max(n//10,1)",
                "serialization": "Polars write_csv(float_precision=17), pandas.read_csv default",
                "main_path": ["raw_stable original labels", "parsed_stable original labels",
                              "parsed_default original labels", "parsed_default parsed labels"],
                "alternative_path": ["raw_stable original labels", "raw_default original labels",
                                     "parsed_default original labels", "parsed_default parsed labels"],
                "components": "Candidate minus reference at each state; retain label serialization and mean-reduction residuals separately. Per-stock composite contribution is the 30% Top-excess component only; report the official IC and turnover contributions separately.",
                "attribution_tolerance": 1e-12, "self_tests": tests,
                "runtime": {"pandas": pd.__version__, "numpy": np.__version__, "polars": pl.__version__}}
    protocol_name = "protocol_recovery.json" if recovery else "protocol.json"
    if recovery:
        protocol["recovery"] = recovery
    write_new(OUT/protocol_name, protocol)
    diagnostic = read(PRIOR/"diagnostic_2024.json")["years"]["2024"]
    predictions = {name: pl.read_parquet(PRIOR/f"{name}_processed_2024.parquet") for name in MODELS}
    keys = predictions["reference"].select(KEYS)
    assert len(keys) == 1125300 and keys.equals(keys.sort("trade_date", "ts_code"))
    assert keys.select(pl.struct(KEYS).n_unique()).item() == len(keys)
    assert predictions["candidate"].select(KEYS).equals(keys)
    labels = keys.join(original_labels(2024), on=KEYS, how="left", validate="1:1", maintain_order="left")
    flags = pl.read_parquet(ROOT/"validation/fold_2024.parquet", columns=KEYS+["flag_limit_up"])
    assert flags.select(KEYS).equals(keys)
    parsed_labels, parsed_flags = csv_parse(labels), csv_parse(flags)
    frames = {}
    serialization = {}
    for model in MODELS:
        raw = predictions[model].to_pandas().merge(labels.to_pandas(), on=KEYS, how="inner")
        raw = raw.merge(flags.to_pandas(), on=KEYS, how="inner")
        parsed = csv_parse(predictions[model]).merge(parsed_labels, on=KEYS, how="inner")
        parsed = parsed.merge(parsed_flags, on=KEYS, how="inner")
        assert np.array_equal(raw.ts_code.to_numpy(), parsed.ts_code.to_numpy())
        assert np.array_equal(raw.trade_date.to_numpy(), parsed.trade_date.to_numpy())
        assert np.array_equal(raw.y_ret_1d.isna(), parsed.y_ret_1d.isna())
        assert np.array_equal(raw.flag_limit_up, parsed.flag_limit_up)
        frames[model] = raw.rename(columns={"pred": "pred_raw", "y_ret_1d": "y_original"})
        frames[model]["pred_parsed"] = parsed.pred
        frames[model]["y_parsed"] = parsed.y_ret_1d
        serialization[model] = {"prediction_nonexact_values": int(np.count_nonzero(raw.pred.to_numpy()!=parsed.pred.to_numpy())),
                                "prediction_max_abs_difference": float(np.max(np.abs(raw.pred.to_numpy()-parsed.pred.to_numpy()))),
                                "labels_nonexact_values": int(np.count_nonzero((raw.y_ret_1d.to_numpy()!=parsed.y_ret_1d.to_numpy()) & raw.y_ret_1d.notna().to_numpy())),
                                "labels_max_abs_difference": float(np.nanmax(np.abs(raw.y_ret_1d.to_numpy()-parsed.y_ret_1d.to_numpy()))),
                                "keys_order_flags_missing_masks_exact": True}
    official = {name: pl.read_csv(PRIOR/f"official_{name}_2024_daily.csv").to_pandas().set_index("trade_date") for name in MODELS}
    grouped = {name: {date:group for date, group in frame.groupby("trade_date", sort=True)}
               for name, frame in frames.items()}
    dates = sorted(grouped["reference"])
    assert len(dates) == N_DAYS and dates == sorted(grouped["candidate"])
    days, events, boundaries, transitions = [], [], [], []
    previous = {name: None for name in MODELS}
    for date in dates:
        data = {name: grouped[name][date] for name in MODELS}
        state = {name: selections(data[name]) for name in MODELS}
        delta = {key: state["candidate"][key]["excess_original"]-state["reference"][key]["excess_original"] for key in STATES}
        parsed_delta = state["candidate"]["parsed_default"]["excess_parsed"]-state["reference"]["parsed_default"]["excess_parsed"]
        components = {"raw_stable_signal": delta["raw_stable"],
                      "prediction_serialization_stable": delta["parsed_stable"]-delta["raw_stable"],
                      "default_sort_parsed": delta["parsed_default"]-delta["parsed_stable"],
                      "label_serialization": parsed_delta-delta["parsed_default"],
                      "default_sort_raw": delta["raw_default"]-delta["raw_stable"],
                      "prediction_serialization_default": delta["parsed_default"]-delta["raw_default"]}
        day = {"trade_date": int(date), "official_delta_excess": parsed_delta,
               **{f"delta_{key}_original_labels": value for key, value in delta.items()}, **components,
               "interaction": components["prediction_serialization_default"]-components["prediction_serialization_stable"]}
        day["interaction_crosscheck_residual"] = day["interaction"]-(components["default_sort_parsed"]-components["default_sort_raw"])
        day_events_start = len(events)
        for model in MODELS:
            sign = 1 if model == "candidate" else -1
            g, s = data[model], state[model]
            assert all(s[key]["k"] == state["reference"]["raw_stable"]["k"] for key in STATES)
            # Underlying candidate/reference membership difference, not an inferred trade.
            other = "reference" if model == "candidate" else "candidate"
            for index in sorted(s["raw_stable"]["ids"]-state[other]["raw_stable"]["ids"]):
                events.append(_event(int(date), "raw_stable_signal", "main", model,
                                     "candidate_in" if sign==1 else "reference_out", index,
                                     sign/s["raw_stable"]["k"], data, state))
            for component, path, before, after in (
                ("prediction_serialization_stable", "main", "raw_stable", "parsed_stable"),
                ("default_sort_parsed", "main", "parsed_stable", "parsed_default"),
                ("default_sort_raw", "alternative", "raw_stable", "raw_default"),
                ("prediction_serialization_default", "alternative", "raw_default", "parsed_default")):
                old_ids, new_ids = s[before]["ids"], s[after]["ids"]
                changes = classification(g, old_ids, new_ids)
                same_repr = before.split("_")[0] == after.split("_")[0]
                score_column = "pred_raw" if before.startswith("raw") else "pred_parsed"
                if same_repr and old_ids != new_ids:
                    changed_ids = old_ids^new_ids
                    assert all(g.loc[index, score_column] == s[before]["cutoff"] for index in changed_ids)
                transitions.append({"trade_date": int(date), "model": model, "component": component,
                                    "path": path, "from_state": before, "to_state": after,
                                    "same_representation_changes_are_exact_boundary_ties": same_repr,
                                    **changes})
                for action, indices, direction in (("in", new_ids-old_ids, 1), ("out", old_ids-new_ids, -1)):
                    for index in sorted(indices):
                        events.append(_event(int(date), component, path, model, action, index,
                                             sign*direction/s[before]["k"], data, state))
            # Label rounding affects values, not membership. Common holdings cancel
            # across candidate/reference; retain only the nonzero coefficient rows.
            for index in sorted(s["parsed_default"]["ids"]-state[other]["parsed_default"]["ids"]):
                events.append(_event(int(date), "label_serialization", "main", model, "label_value_change", index,
                                     sign/s["parsed_default"]["k"], data, state, use_label_delta=True))
            for representation in ("raw", "parsed"):
                ss, dd = s[f"{representation}_stable"], s[f"{representation}_default"]
                day[f"{model}_{representation}_tie_group_size"] = ss["tie_count"]
                day[f"{model}_{representation}_straddling_tie"] = ss["straddling_tie"]
                day[f"{model}_{representation}_default_vs_stable_members_changed"] = len(ss["ids"]^dd["ids"])//2
                day[f"{model}_{representation}_n_top"] = ss["k"]
                column = f"pred_{representation}"
                if ss["straddling_tie"]:
                    # Also expose equal-score rows excluded by missing labels or limit-up.
                    matching = g[g[column] == ss["cutoff"]]
                    for index, row in matching.iterrows():
                        y = None if pd.isna(row.y_original) else float(row.y_original)
                        yp = None if pd.isna(row.y_parsed) else float(row.y_parsed)
                        boundaries.append({"trade_date": int(date), "model": model, "representation": representation,
                                           "ts_code": row.ts_code, "source_row_index": int(index),
                                           "pred_raw": float(row.pred_raw), "pred_parsed": float(row.pred_parsed),
                                           "pred_raw_hex": float(row.pred_raw).hex(), "pred_parsed_hex": float(row.pred_parsed).hex(),
                                           "cutoff": ss["cutoff"], "cutoff_hex": float(ss["cutoff"]).hex(),
                                           "eligible_tie_group_size": ss["tie_count"], "slots_in_group": ss["k"]-ss["above"],
                                           "y_original": y, "y_parsed": yp, "y_missing": y is None,
                                           "flag_limit_up": int(row.flag_limit_up),
                                           "return_eligible": bool(row.flag_limit_up==0 and y is not None),
                                           "selected_stable": index in ss["ids"], "selected_default": index in dd["ids"]})
            final = s["parsed_default"]
            expected = official[model].loc[date]
            assert abs(final["excess_parsed"]-expected.excess) <= TOL
            assert abs(final["top_parsed"]-expected.top1_return) <= TOL
            valid = g[g.y_parsed.notna()]
            ic = float(spearmanr(valid.pred_parsed, valid.y_parsed).statistic)
            assert abs(ic-expected.rank_ic) <= TOL
            turnover_universe = g[g.flag_limit_up==0].sort_values("pred_parsed", ascending=False)
            current = set(turnover_universe.ts_code.iloc[:max(len(turnover_universe)//10,1)])
            turnover = np.nan if previous[model] is None else 1-len(current & previous[model])/len(current | previous[model])
            assert (np.isnan(turnover) and pd.isna(expected.turnover)) or abs(turnover-expected.turnover) <= TOL
            previous[model] = current
            day[f"{model}_official_rank_ic"] = ic
            day[f"{model}_official_turnover"] = turnover
            for key in STATES:
                day[f"{model}_{key}_excess_original"] = s[key]["excess_original"]
                day[f"{model}_{key}_excess_parsed"] = s[key]["excess_parsed"]
        assert previous["reference"] == previous["candidate"]
        day["official_ic_score_contribution"] = .4*(day["candidate_official_rank_ic"]-day["reference_official_rank_ic"])/N_DAYS
        day["official_top_score_contribution"] = .3*252*parsed_delta/N_DAYS
        day["official_turnover_score_contribution"] = 0.0
        day["official_total_score_contribution"] = day["official_ic_score_contribution"]+day["official_top_score_contribution"]
        for component, value in components.items():
            event_sum = sum(event["daily_excess_contribution"] for event in events[day_events_start:] if event["component"] == component)
            day[f"{component}_stock_sum"] = event_sum
            day[f"{component}_mean_reduction_residual"] = value-event_sum
            assert abs(value-event_sum) < 1e-12
        main_sum = sum(components[key] for key in ("raw_stable_signal", "prediction_serialization_stable", "default_sort_parsed", "label_serialization"))
        alt_sum = sum(components[key] for key in ("raw_stable_signal", "default_sort_raw", "prediction_serialization_default", "label_serialization"))
        day["main_reconciliation_residual"] = parsed_delta-main_sum
        day["alternative_reconciliation_residual"] = parsed_delta-alt_sum
        assert abs(parsed_delta-main_sum) < TOL and abs(parsed_delta-alt_sum) < TOL
        assert abs(day["interaction_crosscheck_residual"]) < TOL
        days.append(day)
    daily = pl.DataFrame(days)
    event_frame = pl.DataFrame(events)
    transition_frame = pl.DataFrame(transitions)
    boundary_frame = pl.DataFrame(boundaries)
    annual = {name: float(daily[name].sum()*252/N_DAYS) for name in
              ("official_delta_excess", "raw_stable_signal", "prediction_serialization_stable",
               "default_sort_parsed", "label_serialization", "default_sort_raw",
               "prediction_serialization_default", "interaction")}
    assert abs(annual["official_delta_excess"]-diagnostic["delta"]["annual_excess"]) < TOL
    assert abs(daily["official_total_score_contribution"].sum()-diagnostic["delta"]["final_score"]) < TOL
    for name in MODELS:
        for state_name in STATES:
            for labels_kind in ("original", "parsed"):
                annual[f"{name}_{state_name}_{labels_kind}"] = float(daily[f"{name}_{state_name}_excess_{labels_kind}"].mean()*252)
    counts = {}
    for model in MODELS:
        counts[model] = {f"{rep}_boundary_tie_days": int(daily[f"{model}_{rep}_straddling_tie"].sum()) for rep in ("raw", "parsed")}
        counts[model].update({f"{rep}_default_vs_stable_member_difference_days": int((daily[f"{model}_{rep}_default_vs_stable_members_changed"]>0).sum()) for rep in ("raw", "parsed")})
        st = transition_frame.filter((pl.col("model")==model) & (pl.col("component")=="prediction_serialization_stable"))
        counts[model]["raw_stable_vs_parsed_stable_member_difference_days"] = int((st["entered"]>0).sum())
    assert counts["reference"]["parsed_boundary_tie_days"] == 17
    assert counts["reference"]["parsed_default_vs_stable_member_difference_days"] == 11
    assert counts["candidate"]["parsed_boundary_tie_days"] == 15
    assert counts["candidate"]["parsed_default_vs_stable_member_difference_days"] == 5
    # Keep the frozen report's independently computed raw-stable auxiliary as a check.
    decile_delta = (diagnostic["deciles"]["candidate"]["top_minus_market"]["mean"]-
                   diagnostic["deciles"]["reference"]["top_minus_market"]["mean"])*252
    assert abs(annual["raw_stable_signal"]-decile_delta) < TOL
    for component in ("raw_stable_signal", "prediction_serialization_stable", "default_sort_parsed", "label_serialization", "default_sort_raw", "prediction_serialization_default"):
        stock_sum = event_frame.filter(pl.col("component")==component)["annual_excess_contribution"].sum()
        residual = daily[f"{component}_mean_reduction_residual"].sum()*252/N_DAYS
        assert abs(stock_sum+residual-annual[component]) < TOL
    if frozen_sources() != locks:
        raise AssertionError("A frozen artifact changed during attribution")
    daily.write_csv(OUT/"daily_decomposition.csv", float_precision=17)
    event_frame.write_csv(OUT/"stock_contribution_events.csv", float_precision=17)
    event_frame.write_parquet(OUT/"stock_contribution_events.parquet")
    transition_frame.write_csv(OUT/"membership_transitions.csv")
    boundary_frame.write_csv(OUT/"boundary_tie_members.csv", float_precision=17)
    boundary_frame.write_parquet(OUT/"boundary_tie_members.parquet")
    components = ["raw_stable_signal", "prediction_serialization_stable", "default_sort_parsed", "label_serialization"]
    main_events = event_frame.filter(pl.col("path")=="main")
    per_stock = main_events.group_by("ts_code").agg(pl.col("annual_excess_contribution").sum(),
                            pl.col("composite_top_component_contribution").sum(), pl.len().alias("event_count"))
    per_stock.sort("annual_excess_contribution", descending=True).write_csv(OUT/"stock_annual_contributions.csv", float_precision=17)
    tie_stock = main_events.filter(pl.col("component")=="default_sort_parsed").group_by("ts_code").agg(
        pl.col("annual_excess_contribution").sum(), pl.col("composite_top_component_contribution").sum())
    summary = {"status": "passed", "active_protocol": protocol_name, "protocol_sha256": file_hash(OUT/protocol_name),
               "prior_files_verified_before_and_after": len(locks), "rows": len(keys), "days": N_DAYS,
               "annual_excess_decomposition": annual,
               "main_composite_top_component_decomposition": {name: annual[name]*.3 for name in components},
               "official_ic_score_contribution": float(daily["official_ic_score_contribution"].sum()),
               "official_turnover_score_contribution": 0.0,
               "official_composite_delta": float(daily["official_total_score_contribution"].sum()),
               "frozen_official_delta": diagnostic["delta"], "tie_counts": counts,
               "serialization_numeric_changes": serialization,
               "precision_transition_totals": transition_frame.group_by("component").agg(
                   pl.col("entered").sum(), pl.col("csv_created_tie_pairs").sum(), pl.col("csv_broken_tie_pairs").sum(),
                   pl.col("precision_reversal_pairs").sum(), pl.col("preexisting_exact_tie_pairs").sum()).to_dicts(),
               "changed_sort_dates": sorted(set(transition_frame.filter((pl.col("component")=="default_sort_parsed") & (pl.col("entered")>0))["trade_date"].to_list())),
               "top_tie_stock_contributors": tie_stock.sort("annual_excess_contribution", descending=True).head(10).to_dicts(),
               "bottom_tie_stock_contributors": tie_stock.sort("annual_excess_contribution").head(10).to_dicts(),
               "event_rows": len(events), "boundary_rows": len(boundaries),
               "max_daily_reconciliation_residual": float(daily["main_reconciliation_residual"].abs().max()),
               "max_daily_component_mean_reduction_residual": max(float(daily[f"{name}_mean_reduction_residual"].abs().max()) for name in components),
               "annual_main_event_sum_plus_reduction_residual": float(main_events["annual_excess_contribution"].sum()+sum(daily[f"{name}_mean_reduction_residual"].sum()*252/N_DAYS for name in components)),
               "all_official_daily_top_returns_excess_ic_turnover_reproduced": True,
               "all_same_representation_sort_swaps_are_exact_boundary_ties": True,
               "labels_used_for_prediction": False, "training_performed": False,
               "tie_break_changed": False, "adoption_rule_changed": False,
               "production_submission_report_modified": False, "seconds": time.monotonic()-started,
               "notes": ["This decomposes an already observed 2024 historical result, not an independent validation or a new candidate.",
                         "Raw and parsed stable/default are diagnostic paths, not selectable tie-breaking hyperparameters.",
                         "Events marked alternative must not be added to the main path. Per-stock composite contributions include only the 30% Top-excess score term.",
                         "Labels and label-missingness are used only as required for ex-post official return attribution. Their CSV numerical changes and floating-point mean-reduction residuals are explicitly separate.",
                         "A same-score default/stable Top swap is an exact tie; serialization can create ties or change quicksort's equal-value ordering elsewhere. Pair classifications are descriptive Cartesian comparisons, not unique causal matchings."]}
    summary["output_artifacts_sha256"] = {p.name:file_hash(p) for p in OUT.iterdir() if p.is_file() and p.name != "summary.json"}
    write_new(OUT/"summary.json", summary)
    text = f"""# 2024 年边界同分对 pooled 结果的贡献诊断

本次只拆解已冻结的两组预测，未重训、未改变同分排序或上轮采用规则。收益标签仅用于事后归因。

## 主要结果

固定官方口径下，候选相对逐日标准化参考方案的年化 Top 超额增加 {annual['official_delta_excess']:.12f}，综合分增加 {summary['official_composite_delta']:.12f}。

| 主路径项目 | 年化超额贡献 | 综合分中的 Top 项贡献 |
| --- | ---: | ---: |
| 原始内存预测、稳定排序 | {annual['raw_stable_signal']:.12f} | {annual['raw_stable_signal']*.3:.12f} |
| 预测值 CSV 序列化增量，稳定排序 | {annual['prediction_serialization_stable']:.12f} | {annual['prediction_serialization_stable']*.3:.12f} |
| 解析预测上的默认排序相对稳定排序 | {annual['default_sort_parsed']:.12f} | {annual['default_sort_parsed']*.3:.12f} |
| 原始收益标签到 CSV 解析标签的数值变化 | {annual['label_serialization']:.17g} | {annual['label_serialization']*.3:.17g} |

IC 项另贡献 {summary['official_ic_score_contribution']:.12f}，换手项贡献为 0。逐股表中的综合分贡献仅指 Top 收益项，不能与主路径重复相加。

候选与参考方案的 parsed-default/stable 名单差异分别出现于 {counts['candidate']['parsed_default_vs_stable_member_difference_days']} 日和 {counts['reference']['parsed_default_vs_stable_member_difference_days']} 日。检查证明，同一数值表示下的名单变化均发生在精确同分的截断组内。原始预测与 CSV 解析预测在稳定排序下的名单差异分别为 {counts['candidate']['raw_stable_vs_parsed_stable_member_difference_days']} 日和 {counts['reference']['raw_stable_vs_parsed_stable_member_difference_days']} 日。

因此，内存稳定排序下的候选 Top 收益差是负数，而官方默认排序下为正数。该段增益对边界同分取舍敏感，不宜全部解释为更强的预测能力。这个事后诊断不撤销或改写先前约定的官方评分采用规则，也不选择对收益更有利的排序方式。

## 另一条路径与核对

先在原始内存预测上改用默认排序，年化增量为 {annual['default_sort_raw']:.12f}；再进行预测 CSV 序列化，增量为 {annual['prediction_serialization_default']:.12f}。两条路径的交互项为 {annual['interaction']:.12f}，两条路径均回到同一个官方结果。

逐日主分解最大残差为 {summary['max_daily_reconciliation_residual']:.4g}；逐日单项股票贡献与直接求均值的最大浮点残差为 {summary['max_daily_component_mean_reduction_residual']:.4g}。标签数值变化与求均值顺序残差单列，没有预先归到同分影响中。所有逐日官方收益、超额、IC 与换手均复现，逐股、逐日与年度合计按 1e-12 容差核对。

## 文件说明

- daily_decomposition.csv：242 日四种预测/排序口径、两种标签值、主路径和交互分解。
- stock_contribution_events.csv / .parquet：逐股入出及标签数值事件、原值与解析值、精确十六进制表示、收益、缺失/涨停标记和年化/综合分贡献。
- membership_transitions.csv：逐日名单变化、CSV 新同分/打破同分/次序反转诊断。
- boundary_tie_members.csv / .parquet：截断同分组及同分但因缺失标签或涨停而未入选的股票。
- stock_annual_contributions.csv：仅主路径的逐股年贡献汇总。
- summary.json / {protocol_name}：完整数值、公式口径、来源 SHA 与核验记录；初次输入分组异常前的协议原件保留，未覆盖。

这不是可执行组合收益评估。官方收益 Top 排除缺失收益标签，而换手 Top 不排除，不能据此推断交易成本或实盘收益。
"""
    with (OUT/"诊断说明.md").open("x", encoding="utf-8") as stream:
        stream.write(text)
    print(json.dumps({"annual_main": {name:annual[name] for name in components},
                      "official_delta": annual["official_delta_excess"], "tie_counts":counts,
                      "events":len(events), "seconds":summary["seconds"]}, ensure_ascii=False, indent=2), flush=True)
    return summary


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("stage", choices=("test", "run"))
    parser.add_argument("--resume-input-validation", action="store_true")
    args = parser.parse_args()
    if args.stage == "test":
        print(json.dumps(self_test(), indent=2))
    else:
        diagnose(resume_input_validation=args.resume_input_validation)


if __name__ == "__main__":
    main()
