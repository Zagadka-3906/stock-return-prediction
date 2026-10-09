"""User-authorized score-first 2024 diagnosis; old failed protocol stays intact."""
from __future__ import annotations

import argparse
import gc
import hashlib
import json
from pathlib import Path

import lightgbm as lgb
import numpy as np
import polars as pl

from experiments import return_head_scorefirst as models
from experiments import audit_return_head as original_audit
from experiments import return_head_models as original_models
from experiments.audit_top_weight import production_integrity
from experiments.audit_top_internal import paired_intervals
from experiments.official_seed_development import official_score, original_labels
from src.research_stats import quantile_stats
from run import FEATURE_FILE, ROOT, feature_names, to_matrix
from src.scoring import Panel

OUT = ROOT / "experiments/return_head_scorefirst_eval"
KEYS = ["ts_code", "trade_date"]
YEAR = 2024
file_hash = models.file_hash


def read(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def old_directory_integrity() -> dict:
    protocol = models.read_protocol()
    manifest_path = ROOT / protocol["prior_directory_manifest"]
    assert file_hash(manifest_path) == protocol["prior_directory_manifest_sha256"]
    expected = read(manifest_path)
    actual = {path.relative_to(ROOT).as_posix(): file_hash(path)
              for path in sorted(original_models.OUT.rglob("*")) if path.is_file()}
    assert actual == expected, "Old experiment file set or content was changed"
    assert read(original_models.OUT / "development.json")["primary_gate_passed"] is False
    assert read(original_models.OUT / "decision.json")["diagnostic_2024_run"] is False
    return {"unchanged": True, "files_checked": len(actual),
            "manifest_sha256": file_hash(manifest_path), "old_primary_gate_passed": False}


def tests() -> dict:
    protocol = models.read_protocol()
    assert models.training_target is original_models.training_target
    assert protocol["target"] == original_models.read_protocol()["target"]
    assert protocol["blend"] == {"mode": "top_only", "weight": .25}
    target_tests = original_models.test_target()
    prediction_tests = original_audit.synthetic_checks()
    assert target_tests == read(original_models.OUT / "target_tests.json")
    assert prediction_tests == read(original_models.OUT / "prediction_tests.json")
    blocked = False
    try:
        original_models.diagnostic_gate()
    except ValueError:
        blocked = True
    assert blocked, "The old three-metric gate must remain failed, not overridden"
    return {"status": "passed", "target_implementation_identical": True,
            "old_target_tests_reproduced": True, "old_prediction_synthetic_tests_reproduced": True,
            "old_2024_gate_still_rejects": True, "old_directory": old_directory_integrity(),
            "audit_source_sha256": file_hash(Path(__file__)), "protocol_sha256": file_hash(OUT / "protocol.json")}


def independent_target_checks() -> dict:
    fold = models.read_protocol()["fold"]
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
    assert np.allclose(actual, expected, rtol=1e-6, atol=1e-7) and maximum_error <= 1e-6
    digest = hashlib.sha256(actual.tobytes()).hexdigest()
    metadata = read(OUT / f"{models.MODEL_KEY}_{YEAR}.json")
    assert digest == metadata["target_stats"]["target_array_sha256"]
    assert int(frame["trade_date"].min()) == fold["training_first_date"]
    assert int(frame["trade_date"].max()) == fold["training_last_date"]
    return {"training_only_independent_polars_reconstruction_passed": True,
            "target_array_sha256": digest, "target_hash_matches_metadata": True,
            "max_abs_float32_target_difference": maximum_error, "tolerance": "rtol=1e-6, atol=1e-7, max_abs<=1e-6",
            "training_rows": len(frame), "training_days": len(bounds),
            "input_precision": "cached Float32 promoted to Float64; original lost precision is not restored"}


def model_reload_checks(panel: Panel, candidate_raw: np.ndarray) -> dict:
    features = feature_names()
    indices = np.linspace(0, len(panel.frame) - 1, min(4096, len(panel.frame)), dtype=int)
    sample = (pl.scan_parquet(FEATURE_FILE)
              .filter(pl.col("is_train") & pl.col("trade_date").is_between(20240101, 20241231))
              .select(*KEYS, *features).sort("trade_date", "ts_code").with_row_index("_index")
              .filter(pl.col("_index").is_in(indices.tolist())).collect())
    expected_keys = panel.frame.with_row_index("_index").filter(pl.col("_index").is_in(indices.tolist())).select(KEYS)
    assert sample.select(KEYS).equals(expected_keys)
    matrix = to_matrix(sample, features)
    result = {}
    cases = {"baseline": (ROOT / "models/fold_2024.txt", panel.frame["pred_raw"].to_numpy()),
             "auxiliary": (OUT / f"{models.MODEL_KEY}_{YEAR}.txt", candidate_raw)}
    for name, (path, raw) in cases.items():
        model = lgb.Booster(model_str=path.read_text(encoding="utf-8"))
        assert model.feature_name() == features and model.num_trees() == 180
        prediction = model.predict(matrix, num_threads=16).astype(np.float32)
        prediction[~panel.frame["price_valid"].to_numpy()[indices]] = -1e6
        assert np.array_equal(prediction, raw[indices])
        result[name] = {"rows": len(indices), "max_abs_error": 0.0, "feature_order_and_180_trees_verified": True}
    return result


def predictions():
    panel = models.load_panel()
    assert not np.isfinite(panel.y).any()
    raw = models.load_raw(panel)
    reloads = model_reload_checks(panel, raw)
    baseline = original_audit.predict(panel, None, False)
    candidate = original_audit.predict(panel, raw, True)
    assert np.isfinite(baseline).all() and np.isfinite(candidate).all()
    changed = Panel.from_frame(panel.frame.with_columns(pl.Series(
        "y_ret_1d", np.random.default_rng(260925).normal(size=len(panel.frame)))))
    rows = 50 * panel.rows_per_day
    prefix = Panel.from_frame(panel.frame.head(rows))
    for auxiliary, is_candidate, pred in ((None, False, baseline), (raw, True, candidate)):
        assert np.array_equal(pred, original_audit.predict(changed, auxiliary, is_candidate))
        prefix_raw = auxiliary[:rows] if auxiliary is not None else None
        assert np.array_equal(pred[:rows], original_audit.predict(prefix, prefix_raw, is_candidate))
    checks = {"prediction_labels_all_missing": True, "label_perturbation_invariant": True,
              "prefix_50_days_exact": True, "finite_all_rows": True,
              "protected_block": original_audit.protected_checks(panel, raw, baseline, candidate),
              "official_top_identity": original_audit.official_top_identity_check(panel, baseline, candidate)}
    return panel, {"baseline": baseline, "candidate": candidate}, checks, reloads


def dependencies() -> dict:
    sources = dict(models.fingerprint()["source_sha256"])
    paths = [Path(__file__), OUT / "tests.json", ROOT / "experiments/audit_return_head.py",
             ROOT / "experiments/audit_top_weight.py", ROOT / "experiments/top_weight_models.py",
             ROOT / "experiments/audit_top_internal.py", ROOT / "experiments/official_seed_development.py",
             ROOT / "experiments/cached_recheck.py", ROOT / "report_analytics.py"]
    paths.extend(OUT / f"{models.MODEL_KEY}_{YEAR}.{extension}" for extension in ("txt", "parquet", "json"))
    sources.update({str(path.relative_to(ROOT)): file_hash(path) for path in paths})
    return dict(sorted(sources.items()))


def run() -> dict:
    protocol = models.read_protocol()
    preflight = models.preflight()
    assert preflight["old_primary_gate_passed"] is False
    assert preflight["new_score_first_development_gate_passed"] is True
    destination = OUT / "diagnostic_2024.json"
    paths = [OUT / f"{name}_{YEAR}{extension}" for name, extension in (
        ("official_baseline", "_daily.csv"), ("official_candidate", "_daily.csv"),
        ("baseline_processed", ".parquet"), ("candidate_processed", ".parquet"))]
    if destination.exists() or any(path.exists() for path in paths):
        raise FileExistsError("Preserve existing completed or partial audit evidence")
    assert read(OUT / "tests.json") == tests()
    before = dependencies()
    production_before, old_before = production_integrity(), old_directory_integrity()
    target_checks = independent_target_checks()
    panel, predicted, checks, reloads = predictions()
    # Both prediction arrays and all prediction-only checks precede return loading.
    labelled = Panel.from_frame(panel.frame.drop("y_ret_1d").join(
        original_labels(YEAR), on=KEYS, how="left", validate="1:1"))
    assert labelled.frame.select(KEYS).equals(panel.frame.select(KEYS))
    result = {"experiment": protocol["experiment"], "candidate_key": models.CANDIDATE_KEY,
              "year": YEAR, "candidate_count": 1, "blend": protocol["blend"],
              "postprocess": protocol["postprocess"], "protocol_sha256": file_hash(OUT / "protocol.json"),
              "audit_source_sha256": file_hash(Path(__file__)), "model_fingerprint": models.fingerprint()["fingerprint_sha256"],
              "previous_development_sha256": file_hash(original_models.OUT / "development.json"),
              "previous_decision_sha256": file_hash(original_models.OUT / "decision.json"),
              "old_primary_gate_passed": False, "new_score_first_development_gate_passed": True,
              "rule_changed_after_development_results_known": True,
              "no_candidate_reselection": True, "rows": len(panel.frame), "days": len(panel.dates),
              "training": protocol["fold"], "target_checks": target_checks, "model_reload_checks": reloads,
              "prediction_checks": checks, "deciles": {}, "decision_rule": protocol["new_rule"],
              "production_before": production_before, "old_directory_before": old_before,
              "limitations": protocol["limitations"], "official_daily_reconstruction_tolerance": 1e-12}
    daily = {}
    for name, prediction in predicted.items():
        metrics, daily[name] = official_score(panel, prediction, YEAR)
        result[name] = metrics
        result["deciles"][name] = quantile_stats(labelled, prediction)
        daily[name].write_csv(OUT / f"official_{name}_{YEAR}_daily.csv")
        panel.frame.select(KEYS).with_columns(pl.Series("pred", prediction)).write_parquet(
            OUT / f"{name}_processed_{YEAR}.parquet")
        print(f"OFFICIAL {YEAR}/{name}: score={metrics['final_score']:.12f}; IC={metrics['ic_mean']:.9f}; "
              f"excess={metrics['annual_excess']:.9f}; turnover={metrics['mean_turnover']:.9f}", flush=True)
    expected = read(ROOT / "experiments/day_balance_eval/diagnostic_2024.json")["years"][str(YEAR)]["baseline"]
    assert set(expected) == set(result["baseline"])
    assert all(abs(result["baseline"][key] - value) <= 1e-12 for key, value in expected.items())
    assert np.array_equal(daily["baseline"]["turnover"].to_numpy(), daily["candidate"]["turnover"].to_numpy(), equal_nan=True)
    result["baseline_official_metrics_match_frozen"] = True
    result["official_turnover_top_identities_equal"] = checks["official_top_identity"]["daily_top_identities_exact"]
    result["official_daily_turnover_exact"] = True
    result["delta"] = {key: result["candidate"][key] - result["baseline"][key] for key in result["baseline"]}
    result["paired_uncertainty"] = paired_intervals(daily["candidate"], daily["baseline"], result["delta"]["final_score"])
    result["score_components"] = {"ic": .4 * result["delta"]["ic_mean"],
                                   "annual_excess": .3 * result["delta"]["annual_excess"],
                                   "turnover": -.3 * result["delta"]["mean_turnover"]}
    assert abs(sum(result["score_components"].values()) - result["delta"]["final_score"]) < 1e-12
    first = {name: frame.row(0, named=True) for name, frame in daily.items()}
    n_ic = int(np.isfinite(daily["baseline"]["rank_ic"].to_numpy()).sum())
    n_excess = int(np.isfinite(daily["baseline"]["excess"].to_numpy()).sum())
    result["first_day_score_contribution"] = (.4 * (first["candidate"]["rank_ic"] - first["baseline"]["rank_ic"]) / n_ic
        + 75.6 * (first["candidate"]["excess"] - first["baseline"]["excess"]) / n_excess)
    result["cold_start_note"] = "Full-year official score retained; t2-onward keeps original prediction state, not a restarted strategy."
    result["decile_note"] = "Auxiliary stable-tie ex-post quantiles, not official default-sort metrics or executable net returns."
    assert dependencies() == before
    result["artifacts_sha256"] = {**before, **{str(path.relative_to(ROOT)): file_hash(path) for path in paths}}
    result["production_after"], result["old_directory_after"] = production_integrity(), old_directory_integrity()
    assert result["production_after"] == production_before and result["old_directory_after"] == old_before
    result["all_integrity_and_causality_checks_passed"] = True
    result["passes_score_first_rule"] = (result["delta"]["final_score"] > protocol["new_rule"]["numerical_score_tolerance"]
        and result["official_turnover_top_identities_equal"] and result["official_daily_turnover_exact"])
    result["recommendation"] = "adopt_fixed_scheme_for_next_version" if result["passes_score_first_rule"] else "do_not_adopt_keep_baseline"
    result["deployed_to_production"] = False
    result["official_submission_or_report_changed"] = False
    destination.write_text(json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False), encoding="utf-8")
    print(f"COMPLETED 2024 score-first diagnosis: {result['recommendation']}; production unchanged", flush=True)
    gc.collect()
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("step", choices=("test", "diagnose"))
    args = parser.parse_args()
    if args.step == "test":
        result = tests()
        path = OUT / "tests.json"
        if path.exists():
            assert read(path) == result, "Prior tests differ; preserve evidence"
        else:
            path.write_text(json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False), encoding="utf-8")
        print("Score-first target, protected-Top and old-gate preservation tests passed", flush=True)
    else:
        run()
