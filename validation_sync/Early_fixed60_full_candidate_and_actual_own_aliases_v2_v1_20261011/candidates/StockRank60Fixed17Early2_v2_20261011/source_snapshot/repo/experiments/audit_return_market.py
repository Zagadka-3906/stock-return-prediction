"""One market-feature return head, compared against the recommended 25% head."""
from __future__ import annotations

import argparse
import gc
import json
from pathlib import Path

import lightgbm as lgb
import numpy as np
import polars as pl

from experiments import return_market_models as models
from experiments import return_head_models as reference_models
from experiments import return_head_scorefirst as reference_2024
from experiments import audit_return_head as protected
from experiments import audit_return_head_scorefirst as audit_reference_2024
from experiments import feature_expansion as expanded
from experiments import feature_expansion_features as features_added
from experiments.check_return_market_prefix import check_model_prefix
from experiments.audit_top_weight import baseline_reload, production_integrity
from experiments.audit_top_internal import paired_intervals
from experiments.official_seed_development import official_score, original_labels
from src.research_stats import quantile_stats
from run import FEATURE_FILE, ROOT, feature_names, to_matrix
from src.scoring import Panel

OUT = ROOT / "experiments/return_market_eval"
KEYS = ["ts_code", "trade_date"]
file_hash = models.file_hash


def read(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def prior_integrity() -> dict:
    path = ROOT / models.read_protocol()["prior_manifest"]
    expected = read(path)
    for relative, digest in expected.items():
        assert file_hash(ROOT / relative) == digest, f"Prior evidence changed: {relative}"
    counts = {}
    for folder in (reference_models.OUT, reference_2024.OUT):
        prefix = folder.relative_to(ROOT).as_posix() + "/"
        actual = {p.relative_to(ROOT).as_posix() for p in folder.rglob("*") if p.is_file()}
        assert actual == {key for key in expected if key.startswith(prefix)}
        counts[prefix] = len(actual)
    assert read(reference_models.OUT / "development.json")["primary_gate_passed"] is False
    decision = read(reference_2024.OUT / "decision.json")
    assert decision["recommended_for_next_version"] is True and decision["deployed_to_production"] is False
    return {"unchanged": True, "prior_files_checked": len(expected), "directory_file_counts": counts,
            "manifest_sha256": file_hash(path), "old_failed_rule_preserved": True,
            "previous_score_first_recommendation_preserved": True}


def tests() -> dict:
    protocol = models.read_protocol()
    assert models.training_target is reference_models.training_target
    assert protocol["target"] == reference_models.read_protocol()["target"]
    assert expanded.features_for_variant("market") == feature_names() + protocol["added_features"]
    assert len(protocol["added_features"]) == 8 and protocol["feature_count"] == 71
    assert reference_models.test_target() == read(reference_models.OUT / "target_tests.json")
    assert protected.synthetic_checks() == read(reference_models.OUT / "prediction_tests.json")
    return {"status": "passed", "training_target_unchanged": True,
            "exact_63_plus_8_market_feature_order": True,
            "frozen_target_and_protected_prediction_synthetic_tests_reproduced": True,
            "prior_integrity": prior_integrity(), "protocol_sha256": file_hash(OUT / "protocol.json"),
            "audit_source_sha256": file_hash(Path(__file__))}


def reference_artifacts(year: int) -> tuple[Path, dict, Path]:
    if year in (2022, 2023):
        folder = reference_models.OUT
        record = read(folder / "development.json")["years"][str(year)]
    elif year == 2024:
        folder = reference_2024.OUT
        record = read(folder / "diagnostic_2024.json")
    else:
        raise ValueError("Only predeclared years are permitted")
    return folder, record["candidate"], folder / f"candidate_processed_{year}.parquet"


def target_checks(year: int) -> dict:
    # Reuse the independently coded Polars reconstruction, not training NumPy statistics.
    result = (protected.independent_target_checks(year) if year in (2022, 2023)
              else audit_reference_2024.independent_target_checks())
    meta = read(OUT / f"{models.MODEL_KEY}_{year}.json")
    folder, _, _ = reference_artifacts(year)
    previous = read(folder / f"return_z1_99_{year}.json")
    digest = result["target_array_sha256"]
    assert digest == meta["target_stats"]["target_array_sha256"] == previous["target_stats"]["target_array_sha256"]
    return {**result, "new_and_reference_target_sha256_exact": True}


def reload_checks(year: int, panel: Panel, ref_raw: np.ndarray, new_raw: np.ndarray) -> dict:
    original = feature_names()
    features = expanded.features_for_variant("market")
    indices = np.linspace(0, len(panel.frame) - 1, 4096, dtype=int)
    sample = (pl.scan_parquet(FEATURE_FILE)
              .filter(pl.col("is_train") & pl.col("trade_date").is_between(year * 10000 + 101, year * 10000 + 1231))
              .select(*KEYS, *original).sort("trade_date", "ts_code").with_row_index("_index")
              .filter(pl.col("_index").is_in(indices.tolist())).collect())
    assert sample.select(KEYS).equals(panel.frame.with_row_index("_index")
        .filter(pl.col("_index").is_in(indices.tolist())).select(KEYS))
    additions = pl.scan_parquet(features_added.ADDED_FEATURE_FILE).select(KEYS + features[63:]).collect()
    joined = sample.join(additions, on=KEYS, how="left", validate="1:1", maintain_order="left")
    assert joined.select(sample.columns).equals(sample)
    folder, _, _ = reference_artifacts(year)
    result = {"original_rank_backbone": baseline_reload(year, panel)}
    for name, names, path, raw in (
        ("reference_63_return_head", original, folder / f"return_z1_99_{year}.txt", ref_raw),
        ("candidate_71_return_head", features, OUT / f"{models.MODEL_KEY}_{year}.txt", new_raw),
    ):
        model = lgb.Booster(model_str=path.read_text(encoding="utf-8"))
        assert model.feature_name() == names and model.num_trees() == 180
        pred = model.predict(to_matrix(joined, names), num_threads=16).astype(np.float32)
        pred[~panel.frame["price_valid"].to_numpy()[indices]] = -1e6
        assert np.array_equal(pred, raw[indices])
        result[name] = {"rows": len(indices), "max_abs_error": 0.0,
                        "feature_order_and_180_trees_verified": True}
    return result


def predictions(year: int):
    panel = models.load_panel(year)
    assert not np.isfinite(panel.y).any()
    reference_raw = (reference_models.load_raw(year, panel) if year in (2022, 2023)
                     else reference_2024.load_raw(panel))
    candidate_raw = models.load_raw(year, panel)
    reloads = reload_checks(year, panel, reference_raw, candidate_raw)
    # BOTH heads use the same original rank backbone, never recursively blended.
    backbone = protected.predict(panel, None, False)
    predictions = {"reference": protected.predict(panel, reference_raw, True),
                   "candidate": protected.predict(panel, candidate_raw, True)}
    changed = Panel.from_frame(panel.frame.with_columns(pl.Series(
        "y_ret_1d", np.random.default_rng(260926).normal(size=len(panel.frame)))))
    rows = 50 * panel.rows_per_day
    prefix = Panel.from_frame(panel.frame.head(rows))
    block_checks = {}
    for name, raw in (("reference", reference_raw), ("candidate", candidate_raw)):
        pred = predictions[name]
        assert np.isfinite(pred).all()
        assert np.array_equal(pred, protected.predict(changed, raw, True))
        assert np.array_equal(pred[:rows], protected.predict(prefix, raw[:rows], True))
        block_checks[name] = protected.protected_checks(panel, raw, backbone, pred)
    _, _, frozen_path = reference_artifacts(year)
    frozen = pl.read_parquet(frozen_path)
    assert frozen.select(KEYS).equals(panel.frame.select(KEYS))
    assert np.array_equal(frozen["pred"].to_numpy(), predictions["reference"])
    identity = protected.official_top_identity_check(panel, predictions["reference"], predictions["candidate"])
    checks = {"prediction_labels_all_missing": True, "label_perturbation_invariant": True,
              "prefix_50_days_exact": True, "finite_all_rows": True,
              "reference_processed_predictions_match_frozen_exact": True,
              "both_heads_use_original_rank_state_no_recursive_blend": True,
              "protected_blocks": block_checks, "official_top_identity": identity}
    return panel, predictions, checks, reloads


def dependencies(years: tuple[int, ...]) -> dict:
    sources = {}
    for year in years:
        sources.update(models.fingerprint(year)["source_sha256"])
        for extension in ("txt", "parquet", "json"):
            path = OUT / f"{models.MODEL_KEY}_{year}.{extension}"
            sources[path.relative_to(ROOT).as_posix()] = file_hash(path)
    sources.update(read(ROOT / models.read_protocol()["prior_manifest"]))
    for path in (Path(__file__), OUT / "tests.json", ROOT / "experiments/check_return_market_prefix.py",
                 ROOT / "experiments/audit_return_head.py", ROOT / "experiments/audit_return_head_scorefirst.py",
                 ROOT / "experiments/check_feature_expansion_prefix.py",
                 ROOT / "experiments/audit_top_weight.py", ROOT / "experiments/audit_top_internal.py",
                 ROOT / "experiments/official_seed_development.py", ROOT / "experiments/cached_recheck.py",
                 ROOT / "report_analytics.py"):
        sources[path.relative_to(ROOT).as_posix()] = file_hash(path)
    return dict(sorted(sources.items()))


def evaluate_year(year: int) -> dict:
    target = target_checks(year)
    panel, predicted, checks, reloads = predictions(year)
    feature_prefix = check_model_prefix(year)
    assert feature_prefix["status"] == "passed"
    assert feature_prefix["production_float32_with_sentinel_nonexact_count"] == 0
    assert feature_prefix["model_output_float64_nonexact_count"] == 0
    # Load evaluation labels only after all predictions/causality checks.
    labelled = Panel.from_frame(panel.frame.drop("y_ret_1d").join(original_labels(year),
        on=KEYS, how="left", validate="1:1", maintain_order="left"))
    assert labelled.frame.select(KEYS).equals(panel.frame.select(KEYS))
    record = {"rows": len(panel.frame), "days": len(panel.dates), "target_checks": target,
              "prediction_checks": checks, "model_reload_checks": reloads,
              "feature_prefix_checks": feature_prefix, "deciles": {}}
    daily = {}
    for name, pred in predicted.items():
        metrics, daily[name] = official_score(panel, pred, year)
        record[name] = metrics
        record["deciles"][name] = quantile_stats(labelled, pred)
        daily[name].write_csv(OUT / f"official_{name}_{year}_daily.csv")
        panel.frame.select(KEYS).with_columns(pl.Series("pred", pred)).write_parquet(OUT / f"{name}_processed_{year}.parquet")
        print(f"OFFICIAL {year}/{name}: score={metrics['final_score']:.12f}; IC={metrics['ic_mean']:.9f}; "
              f"excess={metrics['annual_excess']:.9f}; turnover={metrics['mean_turnover']:.9f}", flush=True)
    folder, expected, _ = reference_artifacts(year)
    assert set(expected) == set(record["reference"])
    assert all(abs(record["reference"][key] - value) <= 1e-12 for key, value in expected.items())
    frozen_daily = pl.read_csv(folder / f"official_candidate_{year}_daily.csv")
    assert frozen_daily.columns == daily["reference"].columns
    for column in frozen_daily.columns:
        assert np.allclose(frozen_daily[column].to_numpy(), daily["reference"][column].to_numpy(),
                           rtol=0, atol=1e-12, equal_nan=True)
    assert np.array_equal(daily["reference"]["turnover"].to_numpy(), daily["candidate"]["turnover"].to_numpy(), equal_nan=True)
    record["reference_official_metrics_and_daily_match_frozen"] = True
    record["official_turnover_top_identities_equal"] = checks["official_top_identity"]["daily_top_identities_exact"]
    record["official_daily_turnover_exact"] = True
    record["delta"] = {key: record["candidate"][key] - record["reference"][key] for key in record["reference"]}
    record["paired_uncertainty"] = paired_intervals(daily["candidate"], daily["reference"], record["delta"]["final_score"])
    record["score_components"] = {"ic": .4 * record["delta"]["ic_mean"],
                                   "annual_excess": .3 * record["delta"]["annual_excess"],
                                   "turnover": -.3 * record["delta"]["mean_turnover"]}
    assert abs(sum(record["score_components"].values()) - record["delta"]["final_score"]) < 1e-12
    first = {name: frame.row(0, named=True) for name, frame in daily.items()}
    n_ic = int(np.isfinite(daily["reference"]["rank_ic"].to_numpy()).sum())
    n_excess = int(np.isfinite(daily["reference"]["excess"].to_numpy()).sum())
    record["first_day_score_contribution"] = (
        .4 * (first["candidate"]["rank_ic"] - first["reference"]["rank_ic"]) / n_ic
        + 75.6 * (first["candidate"]["excess"] - first["reference"]["excess"]) / n_excess)
    record["all_integrity_and_causality_checks_passed"] = True
    record["passes_score_first_rule"] = record["delta"]["final_score"] > models.read_protocol()["rule"]["numerical_score_tolerance"]
    record["cold_start_note"] = "Full-year score retained; t2 sensitivity preserves original prediction state, not a restarted strategy."
    record["decile_note"] = "Auxiliary stable-tie ex-post quantiles; not official default sorting or executable net returns."
    return record


def run(stage: str) -> dict:
    protocol = models.read_protocol()
    if stage not in ("develop", "diagnose"):
        raise ValueError("Only predeclared development or gated diagnosis")
    years = (2022, 2023) if stage == "develop" else (2024,)
    if stage == "diagnose":
        models.diagnostic_gate()
    destination = OUT / ("development.json" if stage == "develop" else "diagnostic_2024.json")
    paths = [OUT / f"{name}_{year}{suffix}" for year in years for name, suffix in (
        ("official_reference", "_daily.csv"), ("official_candidate", "_daily.csv"),
        ("reference_processed", ".parquet"), ("candidate_processed", ".parquet"))]
    if destination.exists() or any(path.exists() for path in paths):
        raise FileExistsError("Preserve existing complete or partial audit evidence")
    assert read(OUT / "tests.json") == tests()
    before = dependencies(years)
    production_before, prior_before = production_integrity(), prior_integrity()
    result = {"experiment": protocol["experiment"], "candidate_key": models.CANDIDATE_KEY,
              "baseline_key": protocol["baseline_key"], "candidate_count": 1, "primary_years": [2022, 2023],
              "protocol_sha256": file_hash(OUT / "protocol.json"), "audit_source_sha256": file_hash(Path(__file__)),
              "model_fingerprints": {str(y): models.fingerprint(y)["fingerprint_sha256"] for y in years},
              "blend": protocol["blend"], "postprocess": protocol["postprocess"], "decision_rule": protocol["rule"],
              "production_before": production_before, "prior_before": prior_before,
              "limitations": protocol["limitations"], "official_daily_reconstruction_tolerance": 1e-12, "years": {}}
    for year in years:
        result["years"][str(year)] = evaluate_year(year)
        gc.collect()
    assert dependencies(years) == before
    result["artifacts_sha256"] = {**before, **{p.relative_to(ROOT).as_posix(): file_hash(p) for p in paths}}
    result["production_after"], result["prior_after"] = production_integrity(), prior_integrity()
    assert result["production_after"] == production_before and result["prior_after"] == prior_before
    result["all_integrity_and_causality_checks_passed"] = True
    if stage == "develop":
        result["primary_gate_passed"] = all(r["passes_score_first_rule"] for r in result["years"].values())
        result["next_action"] = ("fixed_2024_diagnostic_permitted" if result["primary_gate_passed"]
                                 else "stop_retain_recommended_63_feature_25_percent_scheme")
    else:
        result["development_sha256"] = file_hash(OUT / "development.json")
        result["passes_score_first_rule"] = result["years"]["2024"]["passes_score_first_rule"]
    result["deployed_to_production"] = False
    result["official_submission_or_report_changed"] = False
    destination.write_text(json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False), encoding="utf-8")
    print(f"COMPLETED {stage}: {result.get('next_action', result.get('passes_score_first_rule'))}", flush=True)
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("step", choices=("test", "develop", "diagnose"))
    args = parser.parse_args()
    if args.step == "test":
        result = tests()
        path = OUT / "tests.json"
        if path.exists():
            assert read(path) == result, "Frozen tests changed"
        else:
            path.write_text(json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False), encoding="utf-8")
        print("Target, feature order, protected Top and prior-preservation tests passed", flush=True)
    else:
        run(args.step)
