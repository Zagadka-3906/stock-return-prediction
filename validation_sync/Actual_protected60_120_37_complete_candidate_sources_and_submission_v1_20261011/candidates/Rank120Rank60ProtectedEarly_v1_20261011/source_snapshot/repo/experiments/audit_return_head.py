"""One fixed return-amplitude auxiliary, with protected official turnover.

The existing baseline state is unchanged. Original Float64 labels are loaded
only after predictions and prediction-causality checks have been completed.
"""
from __future__ import annotations

import argparse
import gc
import hashlib
import json
import tempfile
from pathlib import Path

import numpy as np
import pandas as pd
import polars as pl

from experiments import return_head_models as models
from experiments.audit_top_weight import baseline_reload, production_integrity
from experiments.audit_top_internal import paired_intervals, synthetic_panel
from experiments.cached_recheck import make_prediction
from experiments.official_seed_development import official_score, original_labels
from src.research_stats import quantile_stats
from run import FEATURE_FILE, ROOT
from src.scoring import Panel, add_top_persistence, make_scores

OUT = ROOT / "experiments/return_head_eval"
KEYS = ["ts_code", "trade_date"]
CANDIDATE = "protected_return_w0p25"
file_hash = models.file_hash


def read(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def predict(panel: Panel, raw: np.ndarray | None, candidate: bool) -> np.ndarray:
    return make_prediction(panel, raw, "top_only" if candidate else "baseline", .25 if candidate else 0.)


def protected_checks(panel: Panel, raw: np.ndarray, baseline: np.ndarray, candidate: np.ndarray) -> dict:
    """Rebuild protection and verify no edits outside permitted blocks/days."""
    base_raw = panel.frame["pred_raw"].to_numpy().reshape(panel.valid_price.shape)
    auxiliary = np.asarray(raw).reshape(panel.valid_price.shape)
    stable = add_top_persistence(panel, make_scores(panel, base_raw, .9), .3).reshape(panel.valid_price.shape)
    base, pred = baseline.reshape(panel.valid_price.shape), candidate.reshape(panel.valid_price.shape)
    skipped, changed = 0, []
    for day in range(len(panel.dates)):
        valid = panel.valid_price[day] & np.isfinite(base_raw[day])
        indices = np.flatnonzero(panel.up[day] == 0)
        n_top = max(len(indices) // 10, 1)
        allowed = np.zeros(panel.rows_per_day, dtype=bool)
        if len(indices) and valid.any():
            top = indices[np.argsort(-stable[day, indices], kind="stable")[:n_top]]
            if valid[top].all():
                protected = valid & (stable[day] >= stable[day, top].min())
                if (np.count_nonzero(protected & (panel.up[day] == 0)) == n_top
                        and np.isfinite(auxiliary[day, protected]).all()):
                    allowed = protected
        assert np.array_equal(base[day, ~allowed], pred[day, ~allowed])
        skipped += int(not allowed.any())
        changed.append(int(np.count_nonzero(base[day] != pred[day])))
    return {"baseline_state_not_modified": True, "outside_allowed_protected_block_exact": True,
            "fallback_days": skipped, "days_with_changed_prediction": int(np.count_nonzero(changed)),
            "mean_changed_rows_per_day": float(np.mean(changed))}


def official_top_identity_check(panel: Panel, baseline: np.ndarray, candidate: np.ndarray) -> dict:
    """Read prediction CSV exactly as the evaluator, without any return labels."""
    tops = {}
    with tempfile.TemporaryDirectory(prefix="return-head-top-identity-") as temporary:
        folder = Path(temporary)
        for name, pred in (("baseline", baseline), ("candidate", candidate)):
            path = folder / f"{name}.csv"
            panel.frame.select(KEYS).with_columns(pl.Series("pred", pred)).write_csv(path, float_precision=17)
            parsed = pd.read_csv(path)
            assert np.array_equal(parsed["ts_code"].to_numpy(), panel.frame["ts_code"].to_numpy())
            assert np.array_equal(parsed["trade_date"].to_numpy(), panel.frame["trade_date"].to_numpy())
            parsed["flag_limit_up"] = panel.frame["flag_limit_up"].to_numpy()
            tops[name] = []
            for _, group in parsed.groupby("trade_date", sort=True):
                eligible = group[group["flag_limit_up"] == 0].copy()
                # No kind argument: preserve the actual evaluator's default tie sorting.
                ordered = eligible.sort_values("pred", ascending=False)
                tops[name].append(set(ordered["ts_code"].iloc[:max(len(ordered) // 10, 1)]))
    assert len(tops["baseline"]) == len(panel.dates)
    assert all(a == b for a, b in zip(tops["baseline"], tops["candidate"], strict=True))
    return {"same_csv_float17_and_pandas_default_sort": True, "labels_not_used": True,
            "daily_top_identities_exact": True, "days_checked": len(panel.dates)}


def synthetic_checks() -> dict:
    rng = np.random.default_rng(260925)
    days, stocks = 6, 128
    cases = {}
    for name in ("ordinary", "tied_boundary", "all_invalid", "sparse_valid",
                 "all_limit_up", "nonfinite_auxiliary"):
        valid = np.ones((days, stocks), dtype=bool)
        up = np.zeros((days, stocks), dtype=np.int8)
        base_raw = rng.normal(size=(days, stocks))
        raw = rng.normal(size=(days, stocks))
        if name == "tied_boundary":
            base_raw[:] = 1.
        if name == "all_invalid":
            valid[2] = False
        if name == "sparse_valid":
            valid[2, :124] = False
        if name == "all_limit_up":
            up[2] = 1
        if name == "nonfinite_auxiliary":
            raw[2] = np.nan
        fixture = synthetic_panel(valid, up)
        panel = Panel.from_frame(fixture.frame.with_columns(
            pl.Series("pred_raw", base_raw.reshape(-1)), pl.lit(None, dtype=pl.Float64).alias("y_ret_1d")))
        baseline, candidate = predict(panel, None, False), predict(panel, raw.reshape(-1), True)
        assert np.isfinite(candidate).all()
        rows = 4 * stocks
        prefix = Panel.from_frame(panel.frame.head(rows))
        assert np.array_equal(candidate[:rows], predict(prefix, raw.reshape(-1)[:rows], True))
        changed = Panel.from_frame(panel.frame.with_columns(pl.Series("y_ret_1d", rng.normal(size=days * stocks))))
        assert np.array_equal(candidate, predict(changed, raw.reshape(-1), True))
        block = protected_checks(panel, raw.reshape(-1), baseline, candidate)
        identity = official_top_identity_check(panel, baseline, candidate)
        if name == "tied_boundary":
            # Only the cold-start day has an ambiguous Top boundary. Later days
            # gain the baseline retention bonus and may validly reorder inside.
            assert np.array_equal(baseline[:stocks], candidate[:stocks])
        cases[name] = {"finite": True, "prefix_and_label_invariance": True,
                       "protected_checks": block, "official_top_identity": identity}
    return {"status": "passed", "cases": cases,
            "source_sha256": file_hash(Path(__file__)), "protocol_sha256": file_hash(OUT / "protocol.json")}


def independent_target_checks(year: int) -> dict:
    """Independent Polars daily quantiles/clipping/moments, versus NumPy trainer."""
    fold = models.read_protocol()["folds"][str(year)]
    frame = (pl.scan_parquet(FEATURE_FILE)
             .filter(pl.col("is_train") & (pl.col("trade_date") < fold["training_cutoff_exclusive"])
                     & pl.col("y_rank").is_not_null() & pl.col("price_valid"))
             .select("trade_date", pl.col("y_ret_1d").cast(pl.Float64).alias("ret"))
             .collect().with_row_index("_row"))
    bounds = frame.group_by("trade_date").agg(pl.col("ret").quantile(.01, interpolation="linear").alias("lo"),
                                              pl.col("ret").quantile(.99, interpolation="linear").alias("hi"))
    assert len(frame) == fold["training_rows"] and len(bounds) == fold["training_days"]
    joined = frame.join(bounds, on="trade_date", how="left", validate="m:1", maintain_order="left")
    assert joined.select(frame.columns).equals(frame)
    joined = joined.with_columns(pl.when(pl.col("ret") < pl.col("lo")).then(pl.col("lo"))
        .when(pl.col("ret") > pl.col("hi")).then(pl.col("hi")).otherwise(pl.col("ret")).alias("clipped"))
    joined = joined.with_columns(pl.col("clipped").mean().over("trade_date").alias("mu"),
                                  pl.col("clipped").std(ddof=0).over("trade_date").alias("sd"))
    expected = joined.select(pl.when(pl.col("sd") <= 1e-12).then(0.)
        .otherwise((pl.col("clipped") - pl.col("mu")) / pl.col("sd")).cast(pl.Float32)).to_series().to_numpy()
    actual = models.training_target(frame["trade_date"].to_numpy(), frame["ret"].to_numpy())
    assert actual.dtype == np.float32 and np.isfinite(actual).all()
    maximum_error = float(np.max(np.abs(actual.astype(float) - expected.astype(float))))
    # Different reduction algorithms may round moments differently; never demand fake bit equality.
    assert np.allclose(actual, expected, rtol=1e-6, atol=1e-7) and maximum_error <= 1e-6
    digest = hashlib.sha256(actual.tobytes()).hexdigest()
    metadata = read(OUT / f"{models.MODEL_KEY}_{year}.json")
    assert digest == metadata["target_stats"]["target_array_sha256"]
    assert int(frame["trade_date"].max()) == fold["training_last_date"]
    return {"training_only_independent_polars_reconstruction_passed": True,
            "target_array_sha256": digest, "target_hash_matches_metadata": True,
            "max_abs_float32_target_difference": maximum_error, "tolerance": "rtol=1e-6, atol=1e-7, max_abs<=1e-6",
            "training_rows": len(frame), "training_days": len(bounds),
            "input_precision": "cached Float32 promoted to Float64; original lost precision is not restored"}


def predictions(year: int):
    panel = models.load_panel(year)
    assert not np.isfinite(panel.y).any()
    raw = models.load_raw(year, panel)
    baseline = predict(panel, None, False)
    candidate = predict(panel, raw, True)
    assert np.isfinite(baseline).all() and np.isfinite(candidate).all()
    changed = Panel.from_frame(panel.frame.with_columns(pl.Series(
        "y_ret_1d", np.random.default_rng(260925).normal(size=len(panel.frame)))))
    rows = 50 * panel.rows_per_day
    prefix = Panel.from_frame(panel.frame.head(rows))
    for name, auxiliary, is_candidate, prediction in (("baseline", None, False, baseline), ("candidate", raw, True, candidate)):
        assert np.array_equal(prediction, predict(changed, auxiliary, is_candidate))
        prefix_aux = auxiliary[:rows] if auxiliary is not None else None
        assert np.array_equal(prediction[:rows], predict(prefix, prefix_aux, is_candidate))
    checks = {"prediction_labels_all_missing": True, "label_perturbation_invariant": True,
              "prefix_50_days_exact": True, "finite_all_rows": True,
              "protected_block": protected_checks(panel, raw, baseline, candidate),
              "official_top_identity": official_top_identity_check(panel, baseline, candidate)}
    return panel, {"baseline": baseline, "candidate": candidate}, checks


def dependencies(years: tuple[int, ...]) -> dict:
    sources = {}
    for year in years:
        sources.update(models.fingerprint(year)["source_sha256"])
        for extension in ("txt", "parquet", "json"):
            path = OUT / f"{models.MODEL_KEY}_{year}.{extension}"
            sources[str(path.relative_to(ROOT))] = file_hash(path)
    for path in (Path(__file__), OUT / "prediction_tests.json", OUT / "target_tests.json",
                 ROOT / "experiments/audit_top_weight.py", ROOT / "experiments/top_weight_models.py",
                 ROOT / "experiments/audit_top_internal.py", ROOT / "experiments/official_seed_development.py",
                 ROOT / "experiments/cached_recheck.py", ROOT / "report_analytics.py"):
        sources[str(path.relative_to(ROOT))] = file_hash(path)
    return dict(sorted(sources.items()))


def evaluate_year(year: int) -> dict:
    target_checks = independent_target_checks(year)
    panel, predicted, checks = predictions(year)
    record = {"rows": len(panel.frame), "days": len(panel.dates), "target_checks": target_checks,
              "prediction_checks": checks, "baseline_reload": baseline_reload(year, panel), "deciles": {}}
    labelled = Panel.from_frame(panel.frame.drop("y_ret_1d").join(original_labels(year), on=KEYS, how="left", validate="1:1"))
    assert labelled.frame.select(KEYS).equals(panel.frame.select(KEYS))
    daily = {}
    for name, pred in predicted.items():
        metrics, daily[name] = official_score(panel, pred, year)
        record[name] = metrics
        record["deciles"][name] = quantile_stats(labelled, pred)
        daily[name].write_csv(OUT / f"official_{name}_{year}_daily.csv")
        panel.frame.select(KEYS).with_columns(pl.Series("pred", pred)).write_parquet(OUT / f"{name}_processed_{year}.parquet")
        print(f"OFFICIAL {year}/{name}: score={metrics['final_score']:.12f}; IC={metrics['ic_mean']:.9f}; "
              f"excess={metrics['annual_excess']:.9f}; turnover={metrics['mean_turnover']:.9f}", flush=True)
    previous = read(ROOT / ("experiments/day_balance_eval/development.json" if year in (2022, 2023)
                            else "experiments/day_balance_eval/diagnostic_2024.json"))
    expected = previous["years"][str(year)]["baseline"]
    assert set(expected) == set(record["baseline"])
    assert all(abs(record["baseline"][key] - value) <= 1e-12 for key, value in expected.items())
    assert np.array_equal(daily["baseline"]["turnover"].to_numpy(), daily["candidate"]["turnover"].to_numpy(), equal_nan=True)
    record["official_turnover_top_identities_equal"] = checks["official_top_identity"]["daily_top_identities_exact"]
    record["official_daily_turnover_exact"] = True
    record["baseline_official_metrics_match_frozen"] = True
    record["delta"] = {key: record["candidate"][key] - record["baseline"][key] for key in record["baseline"]}
    record["paired_uncertainty"] = paired_intervals(daily["candidate"], daily["baseline"], record["delta"]["final_score"])
    record["score_components"] = {"ic": .4 * record["delta"]["ic_mean"],
                                   "annual_excess": .3 * record["delta"]["annual_excess"],
                                   "turnover": -.3 * record["delta"]["mean_turnover"]}
    assert abs(sum(record["score_components"].values()) - record["delta"]["final_score"]) < 1e-12
    first = {name: frame.row(0, named=True) for name, frame in daily.items()}
    n_ic = int(np.isfinite(daily["baseline"]["rank_ic"].to_numpy()).sum())
    n_excess = int(np.isfinite(daily["baseline"]["excess"].to_numpy()).sum())
    record["first_day_score_contribution"] = (.4 * (first["candidate"]["rank_ic"] - first["baseline"]["rank_ic"]) / n_ic
        + 75.6 * (first["candidate"]["excess"] - first["baseline"]["excess"]) / n_excess)
    record["cold_start_note"] = "Full-year official score retained; t2-onward keeps original prediction state, not a restarted strategy."
    record["passes_primary_pair"] = (all(record["delta"][key] > 0 for key in ("ic_mean", "annual_excess", "final_score"))
        and record["official_daily_turnover_exact"] and record["official_turnover_top_identities_equal"])
    record["decile_note"] = "Auxiliary stable-tie ex-post quantiles; not the official default-sort metrics or executable net returns."
    return record


def run(stage: str) -> dict:
    if stage not in ("develop", "diagnose"):
        raise ValueError("Only fixed development or gated diagnosis is permitted")
    protocol = models.read_protocol()
    years = (2022, 2023) if stage == "develop" else (2024,)
    if stage == "diagnose":
        models.diagnostic_gate()
        development = read(OUT / "development.json")
        assert development["audit_source_sha256"] == file_hash(Path(__file__))
    destination = OUT / ("development.json" if stage == "develop" else "diagnostic_2024.json")
    paths = [OUT / f"{name}_{year}{extension}" for year in years
             for name, extension in (("official_baseline", "_daily.csv"), ("official_candidate", "_daily.csv"),
                                     ("baseline_processed", ".parquet"), ("candidate_processed", ".parquet"))]
    if destination.exists() or any(path.exists() for path in paths):
        raise FileExistsError("Preserve existing completed or partial audit evidence")
    tests = synthetic_checks()
    assert read(OUT / "prediction_tests.json") == tests
    initial = dependencies(years)
    production_before = production_integrity()
    result = {"candidate_key": CANDIDATE, "primary_years": [2022, 2023], "years": {}, "candidate_count": 1,
              "blend": protocol["blend"], "postprocess": protocol["postprocess"],
              "protocol_sha256": file_hash(OUT / "protocol.json"), "audit_source_sha256": file_hash(Path(__file__)),
              "model_fingerprints": {str(year): models.fingerprint(year)["fingerprint_sha256"] for year in years},
              "no_automatic_promotion": True, "limitations": protocol["limitations"],
              "official_daily_reconstruction_tolerance": 1e-12, "production_before": production_before}
    for year in years:
        result["years"][str(year)] = evaluate_year(year)
        gc.collect()
    assert dependencies(years) == initial
    result["artifacts_sha256"] = {**initial, **{str(path.relative_to(ROOT)): file_hash(path) for path in paths}}
    if stage == "develop":
        result["primary_gate_passed"] = all(item["passes_primary_pair"] for item in result["years"].values())
        result["next_action"] = "fixed_2024_diagnostic_permitted" if result["primary_gate_passed"] else "stop_keep_production_no_retuning_or_more_years"
    else:
        result["development_sha256"] = file_hash(OUT / "development.json")
        result["fixed_historical_diagnostic_only"] = True
    result["production_after"] = production_integrity()
    assert result["production_after"] == production_before
    destination.write_text(json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False), encoding="utf-8")
    print(f"COMPLETED {stage}: {result.get('next_action', 'diagnostic_only')}", flush=True)
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("stage", choices=("test", "develop", "diagnose"))
    args = parser.parse_args()
    if args.stage == "test":
        result = synthetic_checks()
        path = OUT / "prediction_tests.json"
        if path.exists():
            assert read(path) == result, "Saved tests changed; preserve for inspection"
        else:
            path.write_text(json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False), encoding="utf-8")
        print("Synthetic protected-block and official Top identity tests passed", flush=True)
    else:
        run(args.stage)
