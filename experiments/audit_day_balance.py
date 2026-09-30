"""Official, independent audit of a single equal-training-day candidate."""
from __future__ import annotations

import argparse
import gc
import hashlib
import json
from pathlib import Path

import numpy as np
import polars as pl

from experiments import day_balance_models as models
# These two read-only helpers are independent of the former candidate's weights/gate.
from experiments.audit_top_weight import baseline_reload, production_integrity
from experiments.audit_top_internal import paired_intervals
from experiments.official_seed_development import official_score, original_labels
from experiments.seed_ensemble import file_hash
from src.research_stats import quantile_stats
from run import FEATURE_FILE, ROOT
from src.scoring import Panel, postprocess_scores

OUT = ROOT / "experiments/day_balance_eval"
KEYS = ["ts_code", "trade_date"]
CANDIDATE = "equal_day"


def read(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def dependencies(years: tuple[int, ...]) -> dict:
    sources = {}
    for year in years:
        sources.update(models.fingerprint(year)["source_sha256"])
        for extension in ("txt", "parquet", "json"):
            path = OUT / f"{CANDIDATE}_{year}.{extension}"
            sources[str(path.relative_to(ROOT))] = file_hash(path)
    for relative in (
            "experiments/audit_day_balance.py", "experiments/audit_top_weight.py",
            "experiments/top_weight_models.py", "experiments/audit_top_internal.py",
            "experiments/official_seed_development.py", "report_analytics.py",
            "experiments/day_balance_eval/weight_tests.json",
            "experiments/market_blend_eval/development.json",
            "experiments/market_blend_eval/diagnostic_2024.json"):
        sources[relative] = file_hash(ROOT / relative)
    return dict(sorted(sources.items()))


def independent_weight_checks(year: int) -> dict:
    """Reconstruct weights with a group-by and order-verified join, not numpy.unique."""
    fold = models.read_protocol()["folds"][str(year)]
    frame = (pl.scan_parquet(FEATURE_FILE)
             .filter(pl.col("is_train") & (pl.col("trade_date") < fold["training_cutoff_exclusive"])
                     & pl.col("y_rank").is_not_null() & pl.col("price_valid"))
             .select("trade_date").collect().with_row_index("_row"))
    counts = frame.group_by("trade_date").len(name="n_date")
    joined = frame.join(counts, on="trade_date", how="left", validate="m:1", maintain_order="left")
    assert joined.select("_row", "trade_date").equals(frame)
    n_rows, n_days = len(frame), len(counts)
    assert n_rows == fold["training_rows"] and n_days == fold["training_days"]
    assert int(frame["trade_date"].max()) == fold["training_last_date"]
    expected = (n_rows / (n_days * joined["n_date"].to_numpy().astype(np.float64))).astype(np.float32)
    observed = models.training_weights(frame["trade_date"].to_numpy())
    assert observed.dtype == np.float32 and np.array_equal(observed, expected)
    weight_hash = hashlib.sha256(observed.tobytes()).hexdigest()
    stats = read(OUT / f"{CANDIDATE}_{year}.json")["weight_statistics"]
    assert weight_hash == stats["weight_array_sha256"]
    assert n_days == stats["training_days"]
    per_date = (frame.with_columns(pl.Series("weight", observed.astype(np.float64)))
                .group_by("trade_date").agg(pl.col("weight").sum().alias("total"),
                                            pl.col("weight").min().alias("min"),
                                            pl.col("weight").max().alias("max")))
    assert np.array_equal(per_date["min"].to_numpy(), per_date["max"].to_numpy())
    maximum_error = float(np.max(np.abs(per_date["total"].to_numpy() / (n_rows / n_days) - 1)))
    assert maximum_error <= 1e-7 and abs(observed.mean(dtype=np.float64) - 1) <= 1e-7
    fixture = np.array([20200102, 20200102, 20200103, 20200106, 20200106, 20200106], dtype=np.int32)
    fixture_expected = np.array([1., 1., 2., 2 / 3, 2 / 3, 2 / 3], dtype=np.float32)
    assert np.array_equal(models.training_weights(fixture), fixture_expected)
    permutation = np.array([5, 2, 0, 4, 1, 3])
    assert np.array_equal(models.training_weights(fixture[permutation]), fixture_expected[permutation])
    return {"training_only_groupby_reconstruction_exact": True,
            "training_weight_hash_matches_metadata": True, "weight_array_sha256": weight_hash,
            "fixture_and_permutation_passed": True, "rows": n_rows, "days": n_days,
            "daily_rows_min": int(counts["n_date"].min()), "daily_rows_max": int(counts["n_date"].max()),
            "min_weight": float(observed.min()), "max_weight": float(observed.max()),
            "actual_mean_float64": float(observed.mean(dtype=np.float64)),
            "within_date_weights_identical": True, "max_relative_day_total_error": maximum_error}


def predictions(year: int):
    panel = models.load_panel(year)
    assert not np.isfinite(panel.y).any()
    raws = {"baseline": panel.frame["pred_raw"].to_numpy(), "candidate": models.load_raw(year, panel)}
    changed = Panel.from_frame(panel.frame.with_columns(pl.Series(
        "y_ret_1d", np.random.default_rng(260924).normal(size=len(panel.frame)))))
    prefix_rows = 50 * panel.rows_per_day
    prefix = Panel.from_frame(panel.frame.head(prefix_rows))
    predictions, checks = {}, {}
    for name, raw in raws.items():
        pred = postprocess_scores(panel, raw, **models.POSTPROCESS)
        assert len(pred) == len(panel.frame) and np.isfinite(pred).all()
        assert np.array_equal(pred, postprocess_scores(changed, raw, **models.POSTPROCESS))
        assert np.array_equal(pred[:prefix_rows], postprocess_scores(prefix, raw[:prefix_rows], **models.POSTPROCESS))
        predictions[name] = pred
        checks[name] = {"prediction_labels_all_missing": True, "label_perturbation_invariant": True,
                        "prefix_50_days_exact": True, "finite_all_rows": True}
    return panel, predictions, checks


def evaluate_year(year: int) -> dict:
    weights = independent_weight_checks(year)
    panel, predicted, checks = predictions(year)
    record = {"rows": len(panel.frame), "days": len(panel.dates), "weight_checks": weights,
              "prediction_checks": checks, "baseline_reload": baseline_reload(year, panel), "deciles": {}}
    daily = {}
    # Both sets of predictions already exist; only now load evaluation returns.
    labelled = Panel.from_frame(panel.frame.drop("y_ret_1d").join(
        original_labels(year), on=KEYS, how="left", validate="1:1"))
    assert labelled.frame.select(KEYS).equals(panel.frame.select(KEYS))
    for name, pred in predicted.items():
        metrics, daily[name] = official_score(panel, pred, year)
        record[name] = metrics
        record["deciles"][name] = quantile_stats(labelled, pred)
        daily[name].write_csv(OUT / f"official_{name}_{year}_daily.csv")
        panel.frame.select(KEYS).with_columns(pl.Series("pred", pred)).write_parquet(OUT / f"{name}_processed_{year}.parquet")
        print(f"OFFICIAL {year}/{name}: score={metrics['final_score']:.12f}; IC={metrics['ic_mean']:.9f}; "
              f"excess={metrics['annual_excess']:.9f}; turnover={metrics['mean_turnover']:.9f}", flush=True)
    expected = (read(ROOT / "experiments/market_blend_eval/development.json")["candidates"]["baseline"]["years"][str(year)]
                if year in (2022, 2023) else read(ROOT / "experiments/market_blend_eval/diagnostic_2024.json")["official_baseline"])
    assert all(abs(record["baseline"][key] - value) <= 1e-12 for key, value in expected.items())
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
    record["first_day_score_contribution"] = (
        .4 * (first["candidate"]["rank_ic"] - first["baseline"]["rank_ic"]) / n_ic
        + 75.6 * (first["candidate"]["excess"] - first["baseline"]["excess"]) / n_excess)
    record["cold_start_note"] = "Official full-year scores retained; t2-onward diagnostic keeps original prediction state and is not a restarted strategy."
    record["passes_primary_pair"] = record["delta"]["final_score"] > 0 and record["delta"]["annual_excess"] > 0
    record["decile_note"] = "Auxiliary stable-tie ex-post label-available quantiles, not official default-sort metrics or executable net returns."
    return record


def run(stage: str) -> dict:
    if stage not in ("develop", "diagnose"):
        raise ValueError("Only the fixed development or gated diagnosis is permitted")
    protocol = models.read_protocol()
    years = (2022, 2023) if stage == "develop" else (2024,)
    if stage == "diagnose":
        development = read(OUT / "development.json")
        assert development["candidate_key"] == CANDIDATE and development["primary_years"] == [2022, 2023]
        assert development["primary_gate_passed"] is True
        assert development["protocol_sha256"] == file_hash(OUT / "protocol.json")
        assert development["audit_source_sha256"] == file_hash(Path(__file__))
        for relative, sha in development["artifacts_sha256"].items():
            assert file_hash(ROOT / relative) == sha
        for year in (2022, 2023):
            item = development["years"][str(year)]
            assert item["candidate"]["final_score"] > item["baseline"]["final_score"]
            assert item["candidate"]["annual_excess"] > item["baseline"]["annual_excess"]
    initial = dependencies(years)
    production_before = production_integrity()
    result = {"candidate_key": CANDIDATE, "primary_years": [2022, 2023], "years": {},
              "candidate_count": 1, "postprocess": models.POSTPROCESS,
              "protocol_sha256": file_hash(OUT / "protocol.json"), "audit_source_sha256": file_hash(Path(__file__)),
              "model_fingerprints": {str(year): models.fingerprint(year)["fingerprint_sha256"] for year in years},
              "no_automatic_promotion": True, "limitations": protocol["limitations"],
              "production_before": production_before}
    for year in years:
        result["years"][str(year)] = evaluate_year(year)
        gc.collect()
    assert dependencies(years) == initial
    paths = [OUT / f"{name}_{year}{extension}" for year in years
             for name, extension in (("official_baseline", "_daily.csv"), ("official_candidate", "_daily.csv"),
                                     ("baseline_processed", ".parquet"), ("candidate_processed", ".parquet"))]
    result["artifacts_sha256"] = {**initial, **{str(path.relative_to(ROOT)): file_hash(path) for path in paths}}
    if stage == "develop":
        result["primary_gate_passed"] = all(item["passes_primary_pair"] for item in result["years"].values())
        result["next_action"] = ("fixed_2024_diagnostic_permitted" if result["primary_gate_passed"]
                                 else "stop_no_formula_changes_or_extra_years_keep_production")
        destination = OUT / "development.json"
    else:
        result["development_sha256"] = file_hash(OUT / "development.json")
        result["fixed_historical_diagnostic_only"] = True
        destination = OUT / "diagnostic_2024.json"
    result["production_after"] = production_integrity()
    assert result["production_after"] == production_before
    destination.write_text(json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False), encoding="utf-8")
    print(f"COMPLETED {stage}: {result.get('next_action', 'diagnostic_only')}", flush=True)
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("stage", choices=("develop", "diagnose"))
    args = parser.parse_args()
    run(args.stage)
