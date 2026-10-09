"""Independent official evaluation of one fixed training-label weighting rule."""
from __future__ import annotations

import argparse
import gc
import hashlib
import json
from pathlib import Path

import lightgbm as lgb
import numpy as np
import polars as pl

from experiments import top_weight_models as models
from experiments.audit_top_internal import paired_intervals
from experiments.official_seed_development import official_score, original_labels
from experiments.seed_ensemble import file_hash
from src.research_stats import quantile_stats
from run import FEATURE_FILE, ROOT, feature_names, to_matrix
from src.scoring import Panel, postprocess_scores

OUT = ROOT / "experiments/top_weight_eval"
KEYS = ["ts_code", "trade_date"]
REPORT = "output/docx/赛题五量价收益预测分析报告_优化版.docx"
REPORT_SHA = "55e9019d4c8f0f6028b02f3356062b824fe5279f948e11aee223501a391f0d26"
CANDIDATE = "top10_weight1p5"


def read(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def production_integrity() -> dict:
    expected = {**read(ROOT / "validation/prediction_audit.json")["input_sha256"], REPORT: REPORT_SHA}
    for relative, value in expected.items():
        assert file_hash(ROOT / relative) == value, f"Production artifact changed: {relative}"
    return expected


def dependencies(years: tuple[int, ...]) -> dict:
    sources = {}
    for year in years:
        sources.update(models.fingerprint(year)["source_sha256"])
        for extension in ("txt", "parquet", "json"):
            path = OUT / f"{CANDIDATE}_{year}.{extension}"
            sources[str(path.relative_to(ROOT))] = file_hash(path)
    for relative in (
            "experiments/audit_top_weight.py", "experiments/audit_top_internal.py",
            "experiments/official_seed_development.py", "report_analytics.py",
            "experiments/top_weight_eval/weight_tests.json",
            "experiments/market_blend_eval/development.json",
            "experiments/market_blend_eval/diagnostic_2024.json", REPORT):
        sources[relative] = file_hash(ROOT / relative)
    return dict(sorted(sources.items()))


def independent_weight_checks(year: int) -> dict:
    """Use a separate formula and explicit training-only scan to check actual weights."""
    protocol = models.read_protocol()
    cutoff = protocol["folds"][str(year)]["training_cutoff_exclusive"]
    frame = (pl.scan_parquet(FEATURE_FILE)
             .filter(pl.col("is_train") & (pl.col("trade_date") < cutoff)
                     & pl.col("y_rank").is_not_null() & pl.col("price_valid"))
             .select("y_rank", "trade_date").collect())
    y = frame["y_rank"].to_numpy().astype(np.float32)
    mask = y > np.float32(.4)
    denominator = 1 + .5 * int(mask.sum()) / len(mask)
    expected = np.full(len(y), 1 / denominator, dtype=np.float32)
    expected[mask] = np.float32(1.5 / denominator)
    observed = models.training_weights(y)
    assert observed.dtype == np.float32 and np.array_equal(observed, expected)
    actual_hash = hashlib.sha256(observed.tobytes()).hexdigest()
    meta = read(OUT / f"{CANDIDATE}_{year}.json")
    assert actual_hash == meta["weight_statistics"]["weight_array_sha256"]
    assert int(mask.sum()) == meta["weight_statistics"]["upper_count"]
    assert int((y == np.float32(.4)).sum()) == meta["weight_statistics"]["threshold_tie_count"]
    assert abs(float(observed.mean(dtype=np.float64)) - 1) < 1e-7
    assert len(y) == protocol["folds"][str(year)]["training_rows"]
    assert int(frame["trade_date"].max()) == protocol["folds"][str(year)]["training_last_date"]
    # Boundary points, including a tie at Float32(.4), are checked independently.
    threshold = np.float32(.4)
    fixture = np.array([-.5, 0, np.nextafter(threshold, -np.inf, dtype=np.float32),
                        threshold, threshold, np.nextafter(threshold, np.inf, dtype=np.float32), .5], dtype=np.float32)
    test = models.training_weights(fixture)
    assert np.all(test[:5] == test[0]) and np.all(test[5:] == test[-1])
    assert abs(float(test[-1] / test[0]) - 1.5) < 1e-6
    return {"training_only_reconstruction_exact": True, "float32_boundary_ties_checked": True,
            "training_weight_hash_matches_metadata": True, "weight_array_sha256": actual_hash,
            "rows": len(y), "upper_rows": int(mask.sum()), "upper_fraction": float(mask.mean()),
            "threshold_equal_rows": int((y == threshold).sum()),
            "weight_mean_float64": float(observed.mean(dtype=np.float64)),
            "lower_weight": float(expected[~mask][0]), "upper_weight": float(expected[mask][0])}


def baseline_reload(year: int, panel: Panel) -> dict:
    features = feature_names()
    model = lgb.Booster(model_str=(ROOT / f"models/fold_{year}.txt").read_text(encoding="utf-8"))
    assert model.feature_name() == features and model.num_trees() == 180
    indices = np.linspace(0, len(panel.frame) - 1, 4096, dtype=int)
    sample = (pl.scan_parquet(FEATURE_FILE)
              .filter(pl.col("is_train") & pl.col("trade_date").is_between(year * 10000 + 101, year * 10000 + 1231))
              .select(*KEYS, *features).sort("trade_date", "ts_code").with_row_index("_index")
              .filter(pl.col("_index").is_in(indices.tolist())).collect())
    expected_keys = panel.frame.with_row_index("_index").filter(pl.col("_index").is_in(indices.tolist())).select(KEYS)
    assert sample.select(KEYS).equals(expected_keys)
    pred = model.predict(to_matrix(sample, features), num_threads=16).astype(np.float32)
    pred[~panel.frame["price_valid"].to_numpy()[indices]] = -1e6
    baseline = panel.frame["pred_raw"].to_numpy()[indices]
    assert np.array_equal(pred, baseline)
    return {"rows": len(indices), "max_abs_error": 0.0, "baseline_feature_order_and_180_trees_verified": True}


def predictions(year: int):
    panel = models.load_panel(year)
    assert not np.isfinite(panel.y).any()
    raw = models.load_raw(year, panel)
    raws = {"baseline": panel.frame["pred_raw"].to_numpy(), "candidate": raw}
    predicted, checks = {}, {}
    changed = Panel.from_frame(panel.frame.with_columns(
        pl.Series("y_ret_1d", np.random.default_rng(251026).normal(size=len(panel.frame)))))
    n = 50 * panel.rows_per_day
    prefix = Panel.from_frame(panel.frame.head(n))
    for name, values in raws.items():
        pred = postprocess_scores(panel, values, **models.POSTPROCESS)
        assert np.isfinite(pred).all()
        assert np.array_equal(pred, postprocess_scores(changed, values, **models.POSTPROCESS))
        assert np.array_equal(pred[:n], postprocess_scores(prefix, values[:n], **models.POSTPROCESS))
        predicted[name] = pred
        checks[name] = {"labels_absent_at_prediction": True, "label_perturbation_invariant": True,
                        "prefix_50_days_exact": True, "finite_all_rows": True}
    return panel, predicted, checks


def evaluate_year(year: int) -> dict:
    weight_checks = independent_weight_checks(year)
    panel, predicted, checks = predictions(year)
    reload_check = baseline_reload(year, panel)
    record = {"rows": len(panel.frame), "days": len(panel.dates), "prediction_checks": checks,
              "weight_checks": weight_checks, "baseline_reload": reload_check, "deciles": {}}
    daily = {}
    # Original labels become available only after both predictions are fixed.
    labelled = Panel.from_frame(panel.frame.drop("y_ret_1d").join(
        original_labels(year), on=KEYS, how="left", validate="1:1"))
    assert labelled.frame.select(KEYS).equals(panel.frame.select(KEYS))
    for name, pred in predicted.items():
        metrics, daily[name] = official_score(panel, pred, year)
        record[name] = metrics
        record["deciles"][name] = quantile_stats(labelled, pred)
        daily[name].write_csv(OUT / f"official_{name}_{year}_daily.csv")
        panel.frame.select(KEYS).with_columns(pl.Series("pred", pred)).write_parquet(OUT / f"{name}_processed_{year}.parquet")
        print(f"OFFICIAL {year}/{name}: score={metrics['final_score']:.12f}; "
              f"IC={metrics['ic_mean']:.9f}; excess={metrics['annual_excess']:.9f}; "
              f"turnover={metrics['mean_turnover']:.9f}", flush=True)
    if year in (2022, 2023):
        expected = read(ROOT / "experiments/market_blend_eval/development.json")["candidates"]["baseline"]["years"][str(year)]
    else:
        expected = read(ROOT / "experiments/market_blend_eval/diagnostic_2024.json")["official_baseline"]
    assert all(abs(record["baseline"][key] - value) <= 1e-12 for key, value in expected.items())
    record["baseline_official_metrics_match_frozen"] = True
    record["delta"] = {key: record["candidate"][key] - record["baseline"][key] for key in record["baseline"]}
    record["paired_uncertainty"] = paired_intervals(daily["candidate"], daily["baseline"], record["delta"]["final_score"])
    first = {name: frame.row(0, named=True) for name, frame in daily.items()}
    n_ic = int(np.isfinite(daily["baseline"]["rank_ic"].to_numpy()).sum())
    n_excess = int(np.isfinite(daily["baseline"]["excess"].to_numpy()).sum())
    record["first_day_score_contribution"] = (
        .4 * (first["candidate"]["rank_ic"] - first["baseline"]["rank_ic"]) / n_ic
        + 75.6 * (first["candidate"]["excess"] - first["baseline"]["excess"]) / n_excess)
    record["cold_start_note"] = "Full-year official difference retained. t2-onward HAC omits the first day but keeps original prediction state; it is not a restarted strategy."
    record["score_components"] = {"ic": .4 * record["delta"]["ic_mean"],
                                   "annual_excess": .3 * record["delta"]["annual_excess"],
                                   "turnover": -.3 * record["delta"]["mean_turnover"]}
    assert abs(sum(record["score_components"].values()) - record["delta"]["final_score"]) < 1e-12
    record["passes_primary_pair"] = record["delta"]["final_score"] > 0 and record["delta"]["annual_excess"] > 0
    record["decile_note"] = "Auxiliary stable-tie, ex-post label-available quantiles; not official tie sort or executable net returns."
    return record


def run(stage: str) -> dict:
    if stage not in ("develop", "diagnose"):
        raise ValueError("Only the fixed development or gated diagnosis stages are supported")
    protocol = models.read_protocol()
    years = (2022, 2023) if stage == "develop" else (2024,)
    development = None
    if stage == "diagnose":
        development = read(OUT / "development.json")
        assert development["primary_gate_passed"] is True
        assert development["protocol_sha256"] == file_hash(OUT / "protocol.json")
        assert development["audit_source_sha256"] == file_hash(Path(__file__))
        for relative, sha in development["artifacts_sha256"].items():
            assert file_hash(ROOT / relative) == sha
        for value in development["years"].values():
            assert value["candidate"]["final_score"] > value["baseline"]["final_score"]
            assert value["candidate"]["annual_excess"] > value["baseline"]["annual_excess"]
    initial = dependencies(years)
    production_before = production_integrity()
    result = {"candidate_key": CANDIDATE, "primary_years": [2022, 2023], "years": {},
              "protocol_sha256": file_hash(OUT / "protocol.json"),
              "audit_source_sha256": file_hash(Path(__file__)),
              "model_fingerprints": {str(year): models.fingerprint(year)["fingerprint_sha256"] for year in years},
              "postprocess": models.POSTPROCESS, "candidate_count": 1,
              "limitations": protocol["limitations"], "no_automatic_promotion": True,
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
        result["primary_gate_passed"] = all(value["passes_primary_pair"] for value in result["years"].values())
        result["next_action"] = ("fixed_2024_diagnostic_permitted" if result["primary_gate_passed"]
                                 else "stop_no_more_weights_or_years_keep_production")
        destination = OUT / "development.json"
    else:
        result["development_sha256"] = file_hash(OUT / "development.json")
        result["fixed_historical_diagnostic_only"] = True
        destination = OUT / "diagnostic_2024.json"
    result["production_after"] = production_integrity()
    assert result["production_after"] == production_before
    destination.write_text(json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False), encoding="utf-8")
    print(f"COMPLETED {stage}: {result.get('next_action', 'diagnosis_only')}", flush=True)
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("stage", choices=("develop", "diagnose"))
    arguments = parser.parse_args()
    run(arguments.stage)
