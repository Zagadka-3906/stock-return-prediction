"""Audit the frozen equal-day model on two additional historical years.

No candidate selection or production promotion. Both years are always reported.
Predictions and their causality checks precede loading evaluation labels.
"""
from __future__ import annotations

import gc
import hashlib
import json
from pathlib import Path

import lightgbm as lgb
import numpy as np
import polars as pl

from experiments import day_balance_early_models as models
# Pure read-only helpers: no previous blend is generated or selected here.
from experiments.audit_early_years import labelled_panel, official_score
from experiments.audit_top_internal import paired_intervals
from experiments.audit_top_weight import production_integrity
from src.research_stats import quantile_stats
from run import FEATURE_FILE, ROOT, feature_names, to_matrix
from src.scoring import Panel, postprocess_scores

OUT = ROOT / "experiments/day_balance_early_eval"
KEYS = ["ts_code", "trade_date"]
CANDIDATE = "equal_day"
file_hash = models.file_hash


def read(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def dependencies() -> dict:
    sources = {}
    for year in models.YEARS:
        sources.update(models.fingerprint(year)["source_sha256"])
        for extension in ("txt", "parquet", "json"):
            for folder, stem in ((OUT, CANDIDATE),
                                 (ROOT / "experiments/early_year_eval", "early_baseline")):
                path = folder / f"{stem}_{year}.{extension}"
                sources[str(path.relative_to(ROOT))] = file_hash(path)
    for relative in (
            "experiments/audit_day_balance_early.py", "experiments/audit_early_years.py",
            "experiments/audit_top_internal.py", "experiments/audit_top_weight.py",
            "experiments/top_weight_models.py", "experiments/market_blend.py",
            "experiments/official_seed_development.py", "report_analytics.py",
            "evaluate.py", "validation/prediction_audit.json",
            "output/docx/赛题五量价收益预测分析报告_优化版.docx"):
        sources[relative] = file_hash(ROOT / relative)
    return dict(sorted(sources.items()))


def independent_weight_checks(year: int) -> dict:
    """Independently rebuild all weights by group-by plus an order-preserving join."""
    fold = models.read_protocol()["folds"][str(year)]
    frame = (pl.scan_parquet(FEATURE_FILE)
             .filter(pl.col("is_train") & (pl.col("trade_date") < fold["training_cutoff_exclusive"])
                     & pl.col("y_rank").is_not_null() & pl.col("price_valid"))
             .select("trade_date").collect().with_row_index("_row"))
    counts = frame.group_by("trade_date").len(name="n_date")
    joined = frame.join(counts, on="trade_date", how="left", validate="m:1", maintain_order="left")
    assert joined.select("_row", "trade_date").equals(frame)
    rows, days = len(frame), len(counts)
    assert rows == fold["training_rows"] and days == fold["training_days"]
    assert int(frame["trade_date"].min()) == fold["training_first_date"]
    assert int(frame["trade_date"].max()) == fold["training_last_date"]
    expected = (rows / (days * joined["n_date"].to_numpy().astype(np.float64))).astype(np.float32)
    observed = models.training_weights(frame["trade_date"].to_numpy())
    assert observed.dtype == np.float32 and np.array_equal(observed, expected)
    weight_hash = hashlib.sha256(observed.tobytes()).hexdigest()
    stats = read(OUT / f"{CANDIDATE}_{year}.json")["weight_statistics"]
    assert weight_hash == stats["weight_array_sha256"] and days == stats["training_days"]
    per_date = (frame.with_columns(pl.Series("weight", observed.astype(np.float64)))
                .group_by("trade_date").agg(pl.col("weight").sum().alias("total"),
                                            pl.col("weight").min().alias("min"),
                                            pl.col("weight").max().alias("max")))
    assert np.array_equal(per_date["min"].to_numpy(), per_date["max"].to_numpy())
    error = float(np.max(np.abs(per_date["total"].to_numpy() / (rows / days) - 1)))
    assert error <= 1e-7 and abs(observed.mean(dtype=np.float64) - 1) <= 1e-7
    return {"training_only_groupby_reconstruction_exact": True,
            "training_weight_hash_matches_metadata": True, "weight_array_sha256": weight_hash,
            "rows": rows, "days": days, "within_date_weights_identical": True,
            "daily_rows_min": int(counts["n_date"].min()), "daily_rows_max": int(counts["n_date"].max()),
            "min_weight": float(observed.min()), "max_weight": float(observed.max()),
            "actual_mean_float64": float(observed.mean(dtype=np.float64)),
            "max_relative_day_total_error": error}


def model_reload_checks(year: int, panel: Panel, candidate_raw: np.ndarray) -> dict:
    """Check both saved model files against independently selected feature rows."""
    features = feature_names()
    indices = np.linspace(0, len(panel.frame) - 1, min(4096, len(panel.frame)), dtype=int)
    sample = (pl.scan_parquet(FEATURE_FILE)
              .filter(pl.col("is_train") & pl.col("trade_date").is_between(year * 10000 + 101, year * 10000 + 1231))
              .select(*KEYS, *features).sort("trade_date", "ts_code").with_row_index("_index")
              .filter(pl.col("_index").is_in(indices.tolist())).collect())
    expected_keys = panel.frame.with_row_index("_index").filter(pl.col("_index").is_in(indices.tolist())).select(KEYS)
    assert sample.select(KEYS).equals(expected_keys)
    x = to_matrix(sample, features)
    cases = {"baseline": (ROOT / f"experiments/early_year_eval/early_baseline_{year}.txt",
                           panel.frame["pred_raw"].to_numpy()),
             "candidate": (OUT / f"{CANDIDATE}_{year}.txt", candidate_raw)}
    result = {}
    for name, (path, raw) in cases.items():
        model = lgb.Booster(model_str=path.read_text(encoding="utf-8"))
        assert model.feature_name() == features and model.num_trees() == 180
        pred = model.predict(x, num_threads=16).astype(np.float32)
        pred[~panel.frame["price_valid"].to_numpy()[indices]] = -1e6
        assert np.array_equal(pred, raw[indices])
        result[name] = {"rows": len(indices), "max_abs_error": 0.0,
                        "feature_order_and_180_trees_verified": True}
    return result


def predictions(year: int):
    panel = models.load_panel(year)
    assert not np.isfinite(panel.y).any()
    candidate_raw = models.load_raw(year, panel)
    reload_checks = model_reload_checks(year, panel, candidate_raw)
    raws = {"baseline": panel.frame["pred_raw"].to_numpy(), "candidate": candidate_raw}
    changed = Panel.from_frame(panel.frame.with_columns(pl.Series(
        "y_ret_1d", np.random.default_rng(260925).normal(size=len(panel.frame)))))
    prefix_rows = 50 * panel.rows_per_day
    prefix = Panel.from_frame(panel.frame.head(prefix_rows))
    predicted, checks = {}, {}
    for name, raw in raws.items():
        pred = postprocess_scores(panel, raw, **models.POSTPROCESS)
        assert len(pred) == len(panel.frame) and np.isfinite(pred).all()
        assert np.array_equal(pred, postprocess_scores(changed, raw, **models.POSTPROCESS))
        assert np.array_equal(pred[:prefix_rows], postprocess_scores(prefix, raw[:prefix_rows], **models.POSTPROCESS))
        predicted[name] = pred
        checks[name] = {"prediction_labels_all_missing": True, "label_perturbation_invariant": True,
                        "prefix_50_days_exact": True, "finite_all_rows": True}
    return panel, predicted, checks, reload_checks


def evaluate_year(year: int) -> dict:
    weights = independent_weight_checks(year)
    panel, predicted, checks, reloads = predictions(year)
    fold = models.read_protocol()["folds"][str(year)]
    assert fold["training_last_date"] < fold["training_cutoff_exclusive"] < panel.dates[0]
    record = {"rows": len(panel.frame), "days": len(panel.dates),
              "first_date": int(panel.dates[0]), "last_date": int(panel.dates[-1]),
              "training": fold, "weight_checks": weights,
              "prediction_checks": checks, "model_reload_checks": reloads, "deciles": {}}
    # Both predictions and prediction-only tests are complete BEFORE labels enter.
    labelled = labelled_panel(panel, year)
    daily = {}
    for name, pred in predicted.items():
        metrics, daily[name] = official_score(labelled, pred)
        record[name] = metrics
        record["deciles"][name] = quantile_stats(labelled, pred)
        daily[name].write_csv(OUT / f"official_{name}_{year}_daily.csv")
        panel.frame.select(KEYS).with_columns(pl.Series("pred", pred)).write_parquet(
            OUT / f"{name}_processed_{year}.parquet")
        print(f"OFFICIAL {year}/{name}: score={metrics['final_score']:.12f}; IC={metrics['ic_mean']:.9f}; "
              f"excess={metrics['annual_excess']:.9f}; turnover={metrics['mean_turnover']:.9f}", flush=True)
    expected = read(ROOT / "experiments/early_year_eval/results.json")["years"][str(year)]["metrics"]["baseline"]
    assert set(record["baseline"]) == set(expected)
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
    record["cold_start_note"] = "Full-year official score retained; t2-onward keeps original prediction state, not a restarted strategy."
    record["passes_non_deterioration"] = record["delta"]["final_score"] >= 0
    record["decile_note"] = "Auxiliary stable-tie ex-post label-available quantiles, not official default-sort metrics or executable net returns."
    return record


def run() -> dict:
    protocol = models.read_protocol()
    # Preserve completed or partial audit evidence rather than silently overwrite.
    destinations = [OUT / "results.json"] + [OUT / f"{name}_{year}{extension}" for year in models.YEARS
        for name, extension in (("official_baseline", "_daily.csv"), ("official_candidate", "_daily.csv"),
                                ("baseline_processed", ".parquet"), ("candidate_processed", ".parquet"))]
    if any(path.exists() for path in destinations):
        raise FileExistsError("Audit evidence already exists; preserve it for inspection")
    initial = dependencies()
    production_before = production_integrity()
    result = {"experiment": protocol["experiment"], "candidate_key": CANDIDATE,
              "additional_years": list(models.YEARS), "years": {}, "candidate_count": 1,
              "postprocess": models.POSTPROCESS, "no_candidate_reselection": True,
              "historical_stress_test_not_blind": True,
              "protocol_sha256": file_hash(OUT / "protocol.json"),
              "previous_development_sha256": protocol["previous_development_sha256"],
              "previous_diagnostic_2024_sha256": protocol["previous_diagnostic_2024_sha256"],
              "previous_decision_sha256": protocol["previous_decision_sha256"],
              "audit_source_sha256": file_hash(Path(__file__)),
              "model_fingerprints": {str(year): models.fingerprint(year)["fingerprint_sha256"] for year in models.YEARS},
              "robustness_guardrail": protocol["robustness_guardrail"],
              "no_automatic_promotion": True, "limitations": protocol["limitations"],
              "official_daily_reconstruction_tolerance": 1e-12, "production_before": production_before}
    for year in models.YEARS:
        result["years"][str(year)] = evaluate_year(year)
        gc.collect()
    assert dependencies() == initial, "A frozen dependency changed during scoring"
    result["artifacts_sha256"] = {**initial,
        **{str(path.relative_to(ROOT)): file_hash(path) for path in destinations[1:]}}
    result["both_additional_years_non_decreasing"] = all(
        value["passes_non_deterioration"] for value in result["years"].values())
    result["both_additional_years_excess_non_decreasing"] = all(
        value["delta"]["annual_excess"] >= 0 for value in result["years"].values())
    result["production_after"] = production_integrity()
    assert result["production_after"] == production_before
    (OUT / "results.json").write_text(json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False), encoding="utf-8")
    print(f"COMPLETED: both additional years non-decreasing={result['both_additional_years_non_decreasing']}; no promotion", flush=True)
    return result


if __name__ == "__main__":
    run()
