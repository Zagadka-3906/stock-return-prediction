"""Exact, retrospective attribution of a frozen blend, never candidate selection."""
from __future__ import annotations

import gc
import json
import tempfile
from pathlib import Path

import numpy as np
import pandas as pd
import polars as pl
from scipy.stats import spearmanr

from experiments import audit_early_years as prior
from experiments import early_year_models as models
from experiments.feature_expansion_features import ADDED_FEATURE_FILE
from experiments.seed_ensemble import file_hash
from src.research_stats import hac_stats
from run import FEATURE_FILE, ROOT

OUT = ROOT / "experiments/top_loss_diagnosis"
GROUPS = {0: "neither_turnover_top", 1: "baseline_turnover_top_only",
          2: "blend_turnover_top_only", 3: "both_turnover_tops"}
KEYS = ["ts_code", "trade_date"]


def sources() -> tuple[dict, dict, dict]:
    protocol = prior.read_json(OUT / "protocol.json")
    results = prior.read_json(models.OUT / "results.json")
    decision = prior.read_json(models.OUT / "decision.json")
    assert protocol["previous_results_sha256"] == decision["results_sha256"] == file_hash(models.OUT / "results.json")
    assert protocol["fixed_key"] == results["fixed_key"] == "full_signal_w0.5"
    assert (protocol["primary_year"], protocol["comparison_year"]) == (2021, 2020)
    assert results["fixed_config"] == {"mode": "full_signal", "weight": .5}
    assert decision["production_promoted"] is False
    fingerprints = dict(results["source_and_artifacts_sha256"])
    for relative, expected in fingerprints.items():
        assert file_hash(ROOT / relative) == expected, relative
    for path in (Path(__file__), OUT / "protocol.json", models.OUT / "results.json",
                 models.OUT / "decision.json", Path(prior.__file__)):
        fingerprints[str(path.relative_to(ROOT))] = file_hash(path)
    prior.verify_protocol()
    prior.production_integrity()
    return protocol, results, fingerprints


def load_exposures(year: int, keys: pl.DataFrame, columns: list[str]) -> pd.DataFrame:
    # Reuse existing after-close features, without constructing new signals.
    base_columns = [c for c in columns if c.startswith("CS_")]
    other_columns = [c for c in columns if c not in base_columns]
    mask = pl.col("trade_date").is_between(year * 10000 + 101, year * 10000 + 1231)
    base = pl.scan_parquet(FEATURE_FILE).filter(mask).select(*KEYS, *base_columns).collect()
    added = pl.scan_parquet(ADDED_FEATURE_FILE).filter(mask).select(*KEYS, *other_columns).collect()
    frame = base.join(added, on=KEYS, how="left", validate="1:1").sort("trade_date", "ts_code")
    assert frame.select(KEYS).equals(keys)
    return frame.select(columns).to_pandas()


def csv_roundtrip(labelled, predictions: dict) -> dict[str, pd.DataFrame]:
    """Identical file precision, readers, merge order and sorts as the prior audit."""
    with tempfile.TemporaryDirectory(prefix="fixed-top-attribution-") as temporary:
        folder = Path(temporary)
        labelled.frame.select(*KEYS, "y_ret_1d").write_csv(folder / "labels.csv", float_precision=17)
        labelled.frame.select(*KEYS, "flag_limit_up").write_csv(folder / "flags.csv")
        labels = pd.read_csv(folder / "labels.csv")
        assert np.isfinite(labels.y_ret_1d.dropna()).all()
        flags = pd.read_csv(folder / "flags.csv", usecols=KEYS + ["flag_limit_up"])
        frames = {}
        for name, prediction in predictions.items():
            path = folder / f"{name}.csv"
            labelled.frame.select(KEYS).with_columns(pl.Series("pred", prediction)).write_csv(path, float_precision=17)
            frame = pd.read_csv(path).merge(labels, on=KEYS, how="inner").merge(flags, on=KEYS, how="inner")
            assert frame[KEYS].equals(labelled.frame.select(KEYS).to_pandas().astype({"trade_date": "int64"}))
            frames[name] = frame
    return frames


def jaccard(a: set, b: set) -> float:
    return 1 - len(a & b) / len(a | b) if a or b else 0.


def membership(group: pd.DataFrame) -> tuple[set, set, dict]:
    return_eligible = group[(group.flag_limit_up == 0) & group.y_ret_1d.notna()].copy()
    holding_eligible = group[group.flag_limit_up == 0].copy()
    assert len(return_eligible) >= 100 and len(holding_eligible) >= 100
    ordered_return = return_eligible.sort_values("pred", ascending=False).reset_index()
    ordered_holding = holding_eligible.sort_values("pred", ascending=False)
    k, h = max(len(return_eligible) // 10, 1), max(len(holding_eligible) // 10, 1)
    rt = set(ordered_return["index"].iloc[:k].tolist())
    ht = set(ordered_holding.index[:h].tolist())
    valid = group.dropna(subset=["y_ret_1d"])
    metrics = {"rank_ic": float(spearmanr(valid.pred, valid.y_ret_1d).statistic),
               "top1_return": float(ordered_return.y_ret_1d.iloc[:k].mean()),
               "market_return": float(return_eligible.y_ret_1d.mean()),
               "return_top_size": k, "turnover_top_size": h,
               "return_eligible": len(return_eligible), "turnover_eligible": len(holding_eligible),
               "turnover_top_missing_labels": int(group.loc[list(ht), "y_ret_1d"].isna().sum()),
               "return_top_outside_turnover_top": len(rt - ht),
               "turnover_top_outside_return_top": len(ht - rt),
               "return_vs_turnover_jaccard": jaccard(rt, ht)}
    metrics["excess"] = metrics["top1_return"] - metrics["market_return"]
    return rt, ht, metrics


def scalar_stats(values) -> dict:
    values = np.asarray(values, dtype=float)
    finite = values[np.isfinite(values)]
    return {"stock_days": len(values), "finite_stock_days": len(finite),
            "missing_fraction": float(1 - len(finite) / len(values)) if len(values) else None,
            "mean": float(finite.mean()) if len(finite) else None,
            "median": float(np.median(finite)) if len(finite) else None}


def period_table(daily: pd.DataFrame, period: str) -> list[dict]:
    frame = daily.copy()
    dates = pd.to_datetime(frame.trade_date.astype(str))
    frame["period"] = dates.dt.to_period(period).astype(str)
    columns = ["annual_excess_contribution", "score_ic_contribution",
               "score_excess_contribution", "score_turnover_contribution", "score_contribution"]
    rows = []
    for name, group in frame.groupby("period"):
        rows.append({"period": name, "days": len(group),
                     "negative_excess_days": int((group.excess_delta < 0).sum()),
                     **{col: float(group[col].sum()) for col in columns}})
    assert abs(sum(row["score_contribution"] for row in rows) - daily.score_contribution.sum()) < 1e-12
    return rows


def analyse(year: int, protocol: dict, frozen: dict) -> dict:
    panel = models.load_panel(year)
    raw = models.load_market_raw(year, panel)
    predictions, checks = prior.prediction_checks(panel, raw, frozen["fixed_config"])
    saved = pl.read_parquet(models.OUT / f"fixed_blend_{year}.parquet")
    assert saved.select(KEYS).equals(panel.frame.select(KEYS))
    assert np.array_equal(saved["pred"].to_numpy(), predictions["fixed_blend"])
    exposures = load_exposures(year, panel.frame.select(KEYS), protocol["exposure_columns"])
    labelled = prior.labelled_panel(panel, year)  # labels enter only after predictions are frozen
    frames = csv_roundtrip(labelled, predictions)
    daily_frozen = {name: pd.read_csv(models.OUT / f"official_{name}_{year}_daily.csv").set_index("trade_date")
                    for name in predictions}
    daily_rows, event_frames, universes = [], [], {name: [] for name in predictions}
    previous_holdings = {name: None for name in predictions}
    base_groups = frames["baseline"].groupby("trade_date")
    blend_groups = frames["fixed_blend"].groupby("trade_date")
    for (date, base_group), (date2, blend_group) in zip(base_groups, blend_groups):
        assert date == date2 and np.array_equal(base_group.index, blend_group.index)
        assert base_group.ts_code.equals(blend_group.ts_code)
        tops, holds, metrics = {}, {}, {}
        for name, group in (("baseline", base_group), ("fixed_blend", blend_group)):
            tops[name], holds[name], metrics[name] = membership(group)
            codes = set(group.loc[list(holds[name]), "ts_code"])
            metrics[name]["turnover"] = (jaccard(codes, previous_holdings[name])
                                          if previous_holdings[name] is not None else np.nan)
            previous_holdings[name] = codes
            expected = daily_frozen[name].loc[date]
            for key in ("rank_ic", "top1_return", "excess", "turnover"):
                assert np.isclose(metrics[name][key], expected[key], rtol=0, atol=1e-12, equal_nan=True), (year, date, name, key)
            universes[name].append({"trade_date": int(date), **metrics[name]})
        b, c = metrics["baseline"], metrics["fixed_blend"]
        assert b["return_top_size"] == c["return_top_size"]
        assert b["market_return"] == c["market_return"]
        added = tops["fixed_blend"] - tops["baseline"]
        removed = tops["baseline"] - tops["fixed_blend"]
        assert len(added) == len(removed)
        k = b["return_top_size"]
        row = {"trade_date": int(date), "return_top_size": k,
               "added_count": len(added), "removed_count": len(removed),
               "shared_return_count": len(tops["baseline"] & tops["fixed_blend"]),
               "return_top_between_models_jaccard": jaccard(tops["baseline"], tops["fixed_blend"]),
               "turnover_top_between_models_jaccard": jaccard(holds["baseline"], holds["fixed_blend"]),
               "rank_ic_delta": c["rank_ic"] - b["rank_ic"],
               "excess_delta": c["excess"] - b["excess"],
               "turnover_delta": c["turnover"] - b["turnover"]}
        event_indices = sorted(added | removed)
        events = base_group.loc[event_indices, KEYS + ["y_ret_1d"]].copy()
        events["sign"] = [1 if idx in added else -1 for idx in event_indices]
        events["side"] = np.where(events.sign == 1, "added", "removed")
        events["membership_group"] = [GROUPS[int(idx in holds["baseline"]) + 2 * int(idx in holds["fixed_blend"])] for idx in event_indices]
        events["daily_top_delta_contribution"] = events.sign * events.y_ret_1d / k
        events["annual_excess_contribution"] = events.daily_top_delta_contribution * 252 / len(panel.dates)
        for column in protocol["exposure_columns"]:
            events[column] = exposures.loc[event_indices, column].to_numpy()
        assert abs(events.daily_top_delta_contribution.sum() - row["excess_delta"]) < 1e-12
        for group_name in GROUPS.values():
            grouped = events[events.membership_group == group_name]
            row[f"delta_{group_name}"] = float(grouped.daily_top_delta_contribution.sum())
            row[f"added_{group_name}"] = int((grouped.sign == 1).sum())
            row[f"removed_{group_name}"] = int((grouped.sign == -1).sum())
        event_frames.append(events)
        daily_rows.append(row)
    daily = pd.DataFrame(daily_rows)
    events = pd.concat(event_frames, ignore_index=True)
    expected = frozen["years"][str(year)]
    denominators = {key: int(np.isfinite(daily_frozen["baseline"][key]).sum())
                    for key in ("rank_ic", "excess", "turnover")}
    assert denominators == {"rank_ic": 243, "excess": 243, "turnover": 242}
    daily["annual_excess_contribution"] = 252 * daily.excess_delta / denominators["excess"]
    daily["score_ic_contribution"] = .4 * daily.rank_ic_delta / denominators["rank_ic"]
    daily["score_excess_contribution"] = .3 * daily.annual_excess_contribution
    daily["score_turnover_contribution"] = -.3 * daily.turnover_delta.fillna(0) / denominators["turnover"]
    daily["score_contribution"] = daily[["score_ic_contribution", "score_excess_contribution", "score_turnover_contribution"]].sum(axis=1)
    expected_excess = expected["metrics"]["fixed_blend"]["annual_excess"] - expected["metrics"]["baseline"]["annual_excess"]
    assert abs(daily.annual_excess_contribution.sum() - expected_excess) < 1e-12
    assert abs(events.annual_excess_contribution.sum() - expected_excess) < 1e-12
    assert abs(daily.score_contribution.sum() - expected["official_score_delta"]) < 1e-12
    stock = events.groupby("ts_code").agg(annual_excess_contribution=("annual_excess_contribution", "sum"),
                                          changed_stock_days=("sign", "size"), added_days=("sign", lambda s: int((s == 1).sum())),
                                          removed_days=("sign", lambda s: int((s == -1).sum())))
    stock = stock.sort_values("annual_excess_contribution").reset_index()
    assert abs(stock.annual_excess_contribution.sum() - expected_excess) < 1e-12
    outfiles = {f"daily_{year}.csv": daily, f"stock_contributions_{year}.csv": stock}
    for name, frame in outfiles.items():
        frame.to_csv(OUT / name, index=False, float_format="%.17g")
    pl.from_pandas(events).write_parquet(OUT / f"replacement_events_{year}.parquet")
    universe_summary = {}
    for name, rows in universes.items():
        frame = pd.DataFrame(rows)
        frame.to_csv(OUT / f"universes_{name}_{year}.csv", index=False, float_format="%.17g")
        universe_summary[name] = {column: float(frame[column].mean()) for column in (
            "return_top_size", "turnover_top_size", "return_eligible", "turnover_eligible",
            "turnover_top_missing_labels", "return_top_outside_turnover_top", "turnover_top_outside_return_top", "return_vs_turnover_jaccard")}
    groups = {}
    for name in GROUPS.values():
        subset = events[events.membership_group == name]
        groups[name] = {"added_stock_days": int((subset.sign == 1).sum()),
                        "removed_stock_days": int((subset.sign == -1).sum()),
                        "annual_excess_contribution": float(subset.annual_excess_contribution.sum()),
                        "annualized_contribution_hac": hac_stats(252 * daily[f"delta_{name}"].to_numpy())}
    columns = ["trade_date", "excess_delta", "annual_excess_contribution", "score_contribution"]
    sorted_days = daily.sort_values("annual_excess_contribution")
    monthly = period_table(daily, "M")
    return {"year": year, "official_score_delta": expected["official_score_delta"],
            "annual_excess_delta": expected_excess,
            "score_components": {col: float(daily[col].sum()) for col in (
                "score_ic_contribution", "score_excess_contribution", "score_turnover_contribution")},
            "months": monthly, "quarters": period_table(daily, "Q"),
            "negative_excess_months": sum(x["annual_excess_contribution"] < 0 for x in monthly),
            "negative_score_months": sum(x["score_contribution"] < 0 for x in monthly),
            "negative_excess_days": int((daily.excess_delta < 0).sum()),
            "best_five_days": sorted_days.tail(5)[columns].to_dict("records"),
            "worst_five_days": sorted_days.head(5)[columns].to_dict("records"),
            "best_five_stocks": stock.tail(5).to_dict("records"),
            "worst_five_stocks": stock.head(5).to_dict("records"),
            "gross_negative_day_contributions": float(daily.loc[daily.annual_excess_contribution < 0, "annual_excess_contribution"].sum()),
            "gross_positive_day_contributions": float(daily.loc[daily.annual_excess_contribution > 0, "annual_excess_contribution"].sum()),
            "turnover_membership_partition": groups,
            "universe_means": universe_summary,
            "replacement_daily_means": {column: float(daily[column].mean()) for column in (
                "added_count", "shared_return_count", "return_top_between_models_jaccard", "turnover_top_between_models_jaccard")},
            "exposures": {side: {col: scalar_stats(events.loc[events.side == side, col])
                                  for col in protocol["exposure_columns"]}
                          for side in ("added", "removed")},
            "prediction_checks": checks, "saved_prediction_exactly_reproduced": True,
            "official_daily_all_metrics_reproduced": True,
            "return_replacement_identity_all_days": True,
            "all_attribution_totals_reconcile": True,
            "hac_annual_excess_delta": hac_stats(252 * daily.excess_delta.to_numpy()),
            "first_day_score_contribution": float(daily.score_contribution.iloc[0]),
            "remaining_days_score_contribution_sum": float(daily.score_contribution.iloc[1:].sum()),
            "exposure_weighting": "Equal stock-day observations among changed return constituents; finite values only with missingness reported. No causal feature attribution."}


def run() -> dict:
    protocol, frozen, initial = sources()
    result = {"fixed_key": protocol["fixed_key"], "primary_year": 2021, "comparison_year": 2020,
              "no_training_or_reselection": True, "production_updated": False,
              "limitations": protocol["limitations"], "years": {},
              "versions": {"pandas": pd.__version__, "numpy": np.__version__, "polars": pl.__version__}}
    for year in (2020, 2021):
        result["years"][str(year)] = analyse(year, protocol, frozen)
        models.log(f"ATTRIBUTION {year}: " + json.dumps({key: result["years"][str(year)][key]
                   for key in ("annual_excess_delta", "score_components", "negative_excess_months", "replacement_daily_means")}, ensure_ascii=True))
        gc.collect()
    assert sources()[2] == initial
    result["sources_sha256"] = initial
    result["artifacts_sha256"] = {str(path.relative_to(ROOT)): file_hash(path)
                                 for path in sorted(OUT.iterdir()) if path.suffix in (".csv", ".parquet")}
    result["production_integrity"] = prior.production_integrity()
    (OUT / "results.json").write_text(json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False), encoding="utf-8")
    return result


if __name__ == "__main__":
    run()
