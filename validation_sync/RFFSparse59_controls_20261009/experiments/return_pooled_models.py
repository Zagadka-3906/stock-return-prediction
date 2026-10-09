"""One pooled training-fold scale for the original 63-feature return head.

Daily clipping and centering remain unchanged. Only the scale changes from
each date's standard deviation to RMS over every filtered training row.
No validation/test observations enter the scale or target.
"""
from __future__ import annotations

import argparse
import gc
import hashlib
import json
import time
from pathlib import Path

import lightgbm as lgb
import numpy as np
import polars as pl

from experiments import return_head_models as frozen
from experiments.seed_ensemble import params_for_seed
from run import FEATURE_FILE, MANIFEST, ROOT, feature_names, fold_cutoff, to_matrix
from src.scoring import Panel


OUT = ROOT / "experiments" / "return_pooled_eval"
PRIMARY_YEARS = (2022, 2023)
MODEL_KEY = "return_pooled1_99"
CANDIDATE_KEY = "protected_return_pooled_w0p25"
BASELINE_KEY = "protected_return_w0p25"
ROUNDS, SEED, THREADS = 180, 2026, 16
BLEND = {"mode": "top_only", "weight": .25}
POSTPROCESS = {"alpha": .9, "bonus": .3, "restore_lower": True, "top_current_weight": 1.0}
KEYS = ["ts_code", "trade_date"]
EXPECTED = {
    2022: {"training_cutoff_exclusive": 20211231, "training_first_date": 20180102,
           "training_last_date": 20211230, "training_rows": 3568878, "training_days": 972},
    2023: {"training_cutoff_exclusive": 20221230, "training_first_date": 20180102,
           "training_last_date": 20221229, "training_rows": 4597785, "training_days": 1214},
    2024: {"training_cutoff_exclusive": 20231229, "training_first_date": 20180102,
           "training_last_date": 20231228, "training_rows": 5659954, "training_days": 1456},
}
file_hash = frozen.file_hash


def log(message: str) -> None:
    print(f"[{time.strftime('%H:%M:%S')}] {message}", flush=True)


def features_for_model() -> list[str]:
    features = feature_names()
    if len(features) != 63:
        raise ValueError("Exactly the frozen original 63 features are required")
    return features


def _target_with_stats(dates: np.ndarray, returns: np.ndarray) -> tuple[np.ndarray, dict]:
    """Caller supplies only the final purged and filtered training fold.

    New training rows may legitimately rescale all targets through pooled RMS.
    This is not a prediction transform and must never receive held-out labels.
    """
    dates = np.asarray(dates)
    values = np.asarray(returns)
    if (dates.ndim != 1 or not len(dates) or dates.dtype.kind not in "iuf"
            or not np.isfinite(dates).all() or not np.equal(dates, np.floor(dates)).all()
            or np.any(dates < 0) or np.any(dates >= 2**63)):
        raise ValueError("Dates must be a nonempty vector of nonnegative finite Int64-compatible integers")
    if (values.ndim != 1 or len(values) != len(dates) or values.dtype.kind not in "iuf"
            or not np.isfinite(values).all()):
        raise ValueError("Training returns must be finite numeric values aligned to dates")
    with np.errstate(over="ignore", invalid="ignore"):
        cached = values.astype(np.float32)
    if not np.isfinite(cached).all():
        raise ValueError("Training returns must remain finite in the original Float32 cache")
    dates_int64 = dates.astype(np.int64)
    values = cached.astype(np.float64)
    order = np.argsort(dates_int64, kind="stable")
    ordered_dates = dates_int64[order]
    bounds = np.r_[0, np.flatnonzero(ordered_dates[1:] != ordered_dates[:-1]) + 1, len(dates)]
    centered = np.empty(len(values), dtype=np.float64)
    daily_clipped_std = []
    daily_centered_mean = []
    nearconstant = 0
    for left, right in zip(bounds[:-1], bounds[1:]):
        indices = order[left:right]
        daily = values[indices]
        low, high = np.quantile(daily, [.01, .99], method="linear")
        clipped = np.clip(daily, low, high)
        center = float(clipped.mean(dtype=np.float64))
        scale = float(clipped.std(ddof=0, dtype=np.float64))
        daily_clipped_std.append(scale)
        if scale <= 1e-12:
            residual = np.zeros(len(indices), dtype=np.float64)
            nearconstant += 1
        else:
            residual = clipped - center
        centered[indices] = residual
        daily_centered_mean.append(abs(float(residual.mean(dtype=np.float64))))
    # All training rows count in N, including zero/near-constant dates.
    pooled_rms = float(np.sqrt(np.mean(centered * centered, dtype=np.float64)))
    if not np.isfinite(pooled_rms):
        raise AssertionError("Training-fold RMS unexpectedly became nonfinite")
    pooled_nearconstant = pooled_rms <= 1e-12
    target = (np.zeros(len(centered), dtype=np.float32) if pooled_nearconstant
              else (centered / pooled_rms).astype(np.float32))
    if not np.isfinite(target).all():
        raise AssertionError("Pooled-scale target contains nonfinite values")
    target_means, target_stds = [], []
    for left, right in zip(bounds[:-1], bounds[1:]):
        daily_target = target[order[left:right]].astype(np.float64)
        target_means.append(abs(float(daily_target.mean())))
        target_stds.append(float(daily_target.std(ddof=0)))
    stats = {
        "target_array_sha256": hashlib.sha256(target.tobytes()).hexdigest(),
        "raw_return_float32_sha256": hashlib.sha256(cached.tobytes()).hexdigest(),
        "training_dates_int64_sha256": hashlib.sha256(dates_int64.tobytes()).hexdigest(),
        "centered_float64_sha256": hashlib.sha256(centered.tobytes()).hexdigest(),
        "pooled_rms_float64": pooled_rms,
        "training_days": len(bounds) - 1, "training_rows": len(target),
        "nearconstant_days": nearconstant, "pooled_nearconstant": pooled_nearconstant,
        "max_abs_daily_centered_mean": float(max(daily_centered_mean)),
        "max_abs_daily_target_mean": float(max(target_means)),
        "daily_target_std_min": float(min(target_stds)),
        "daily_target_std_max": float(max(target_stds)),
        "global_target_rms_float64": float(np.sqrt(np.mean(target.astype(np.float64)**2))),
        "target_min": float(target.min()), "target_max": float(target.max()),
        "clipped_std_min": float(min(daily_clipped_std)),
        "clipped_std_max": float(max(daily_clipped_std)),
        "input_dtype": "Float32_promoted_to_Float64", "output_dtype": "Float32",
        "array_hash_encoding": "C-contiguous native-endian bytes; returns Float32, dates Int64, centered Float64, target Float32",
        "scope": "Entire final purged training fold only; all retained rows including nearconstant-day zeros enter pooled RMS; no validation/test labels or counts",
    }
    return target, stats


def training_target(dates: np.ndarray, returns: np.ndarray) -> np.ndarray:
    return _target_with_stats(dates, returns)[0]


def test_model() -> dict:
    """Hand-derived heteroscedastic fixture and training-scope tests."""
    read_protocol()
    # Date A clips to +/-1.96 and +/-1; B is exactly 10*A; C is zero after centering.
    dates = np.array([1]*5 + [2]*5 + [3]*2, dtype=np.int32)
    values = np.array([-2, -1, 0, 1, 2, -20, -10, 0, 10, 20, 5, 5], dtype=np.float32)
    expected_centered = np.array([-1.96, -1, 0, 1, 1.96, -19.6, -10, 0, 10, 19.6, 0, 0], np.float64)
    expected_rms = np.sqrt(978.0032 / 12)
    target, stats = _target_with_stats(dates, values)
    expected_target = (expected_centered / expected_rms).astype(np.float32)
    assert np.allclose(target, expected_target, rtol=0, atol=1e-7)
    assert abs(stats["pooled_rms_float64"] - expected_rms) < 1e-12
    assert abs(float(target[6]) / float(target[1]) - 10) < 1e-6
    assert stats["nearconstant_days"] == 1 and not stats["pooled_nearconstant"]
    assert target.dtype == np.float32 and len(target) == len(values)
    assert not np.array_equal(target, frozen.training_target(dates, values))
    assert np.all(target[-2:] == 0)
    assert abs(stats["global_target_rms_float64"] - 1) < 1e-7
    assert stats["daily_target_std_max"] > stats["daily_target_std_min"]
    permutation = np.array([11, 4, 8, 2, 0, 9, 5, 7, 3, 6, 10, 1])
    assert np.allclose(training_target(dates[permutation], values[permutation]), target[permutation],
                       rtol=0, atol=1e-7)
    assert np.array_equal(training_target([1], [9]), np.zeros(1, np.float32))
    assert np.array_equal(training_target([1, 1, 2, 2], [5, 5, -8, -8]), np.zeros(4, np.float32))
    tiny, tiny_stats = _target_with_stats([1, 1, 2, 2], [-1e-14, 1e-14, -1, 1])
    assert np.all(tiny[:2] == 0) and tiny_stats["nearconstant_days"] == 1
    diluted, diluted_stats = _target_with_stats([1, 1]+[2]*100, [-2e-12, 2e-12]+[0]*100)
    assert diluted_stats["nearconstant_days"] == 1 and diluted_stats["pooled_nearconstant"]
    assert np.all(diluted == 0)
    outlier_returns = np.array([-100, 0, 0, 1, 100], np.float32)
    outlier, _ = _target_with_stats(np.ones(5, np.int32), outlier_returns)
    manual_clipped = np.array([-96, 0, 0, 1, 96.04], np.float64)
    manual_centered = manual_clipped - manual_clipped.mean()
    assert np.allclose(outlier, (manual_centered / np.sqrt(np.mean(manual_centered**2))).astype(np.float32),
                       rtol=0, atol=1e-7)
    assert outlier[1] == outlier[2]
    rounded = values.astype(np.float64)
    rounded[-1] += 1e-10
    assert np.array_equal(training_target(dates, rounded), target)
    invalid = (("empty", [], []), ("non_vector_date", [[1, 2]], [1, 2]),
               ("non_vector_return", [1, 2], [[1, 2]]), ("length_mismatch", [1], [1, 2]),
               ("fractional_date", [1, 2.5], [1, 2]), ("nan_date", [1, np.nan], [1, 2]),
               ("infinite_date", [1, np.inf], [1, 2]), ("string_date", ["1"], [1]),
               ("negative_date", [-1], [1]), ("int64_overflow_date", [1e30], [1]),
               ("nan_return", [1, 1], [0, np.nan]), ("infinite_return", [1], [np.inf]),
               ("string_return", [1], ["1"]), ("float32_overflow", [1], [1e100]),
               ("boolean_date", [True], [1]), ("boolean_return", [1], [True]))
    rejected = []
    for name, bad_dates, bad_returns in invalid:
        try:
            training_target(bad_dates, bad_returns)
        except ValueError:
            rejected.append(name)
        else:
            raise AssertionError(f"Invalid pooled-target input accepted: {name}")
    dates_suffix = np.r_[dates, [20250102, 20250102]]
    values_suffix = np.r_[values, [np.nan, np.inf]]
    mask = np.arange(len(dates_suffix)) < len(dates)
    assert np.array_equal(training_target(dates_suffix[mask], values_suffix[mask]), target)
    values_suffix[~mask] = [-1000, 1000]
    assert np.array_equal(training_target(dates_suffix[mask], values_suffix[mask]), target)
    appended = training_target(dates_suffix, values_suffix)
    assert not np.array_equal(appended[:len(target)], target)
    # Legal added zero rows lower RMS because the denominator includes every row.
    zero_appended, zero_stats = _target_with_stats(np.r_[dates, [4, 4]], np.r_[values, [0, 0]])
    assert zero_stats["pooled_rms_float64"] < stats["pooled_rms_float64"]
    assert not np.array_equal(zero_appended[:len(target)], target)
    return {"status": "passed", "manual_heteroscedastic_fixture": True,
            "expected_centered_sum_of_squares": 978.0032, "all_rows_including_zero_days_in_denominator": True,
            "different_from_daily_zscore": True, "tenfold_amplitude_ratio_retained": True,
            "constant_single_row_nearconstant_and_global_threshold": True,
            "outlier_linear_clipping_and_ties": True, "row_order_and_permutation": True,
            "cached_float32_before_float64_statistics": True, "invalid_inputs_rejected": rejected,
            "validation_suffix_filtered_before_target_construction": True,
            "legitimate_training_append_changes_global_scale": True,
            "fixture_stats": stats, "features": features_for_model(),
            "source_sha256": file_hash(Path(__file__)), "protocol_sha256": file_hash(OUT / "protocol.json")}


def read_protocol() -> dict:
    protocol = json.loads((OUT / "protocol.json").read_text(encoding="utf-8"))
    fixed = {"experiment": "fixed_pooled_scale_return_head",
             "declared_before_training_and_scoring": True, "candidate_key": CANDIDATE_KEY,
             "model_key": MODEL_KEY, "baseline_key": BASELINE_KEY,
             "primary_years": list(PRIMARY_YEARS), "conditional_diagnostic_year": 2024,
             "candidate_count": 1, "feature_count": 63, "feature_variant": "original_63",
             "added_features": [],
             "rounds": ROUNDS, "seed": SEED, "threads": THREADS,
             "blend": BLEND, "postprocess": POSTPROCESS,
             "training_filter": "is_train & trade_date < fold_cutoff(year) & y_rank.not_null & price_valid"}
    if any(protocol.get(key) != value for key, value in fixed.items()):
        raise ValueError("Pooled-return-head protocol differs from its single fixed design")
    fixed_target = {
        "input": "cached Float32 y_ret_1d for final filtered training rows only, promoted to Float64 before all statistics",
        "quantiles": [.01, .99], "quantile_method": "linear",
        "formula": "For each filtered training date: clipped=clip(return,q01,q99); centered=clipped-mean(clipped), except dates with std(clipped,ddof=0)<=1e-12 are set to zero exactly as the reference. Across ALL final filtered training rows including those zero rows: pooled_rms=sqrt(mean(centered**2)); target=centered/pooled_rms, or all zero if pooled_rms<=1e-12.",
        "standard_deviation_ddof": 0, "near_constant_std_threshold": 1e-12,
        "near_constant_action": "Set every centered value on that date to zero; do not delete rows; include zero rows in pooled RMS denominator",
        "scale_scope": "One RMS fitted only on the current purged historical training fold, sample-weighted over all rows; never daily scales, equal-day weights or full train-plus-validation/test data",
        "pooled_near_constant_rms_threshold": 1e-12,
        "pooled_near_constant_action": "Set every target in the fold to zero",
        "output": "Float32 target in original training row order",
        "weights": "None; no equal-day, top-label or recency weights", "tuning": "None",
    }
    if (protocol.get("target") != fixed_target
            or protocol.get("folds") != {str(year): values for year, values in EXPECTED.items()}):
        raise ValueError("The pooled target or original training boundaries changed")
    if protocol.get("target_audit_tolerance") != {
            "rtol": 1e-6, "atol": 1e-7, "max_abs_float32": 1e-6,
            "pooled_rms_rtol": 1e-12, "pooled_rms_atol": 1e-15}:
        raise ValueError("Predeclared independent target audit tolerances changed")
    if (protocol.get("prior_manifest") != "experiments/return_pooled_eval/prior_artifacts_sha256.json"
            or protocol.get("prior_directories") != ["experiments/return_head_eval",
                "experiments/return_head_scorefirst_eval", "experiments/return_market_eval",
                "experiments/return_market_stable_eval"]):
        raise ValueError("Frozen prior evidence scope changed")
    fixed_rule = {
        "numerical_score_tolerance": 1e-12,
        "development": "Both 2022 and 2023 candidate official final_score minus fixed 63-feature 25% reference final_score > 1e-12, and all integrity, complete-coverage, causality, same-CSV original scoring, exact official daily Top identities and turnover checks pass. Only then permit one fixed 2024 train/diagnosis.",
        "diagnostic": "The unchanged 2024 candidate must also improve official composite score over the fixed 63-feature 25% reference by >1e-12 and pass all checks to recommend adoption.",
        "components": "Report IC, excess and turnover; IC or excess need not individually increase. Exact protected daily turnover/Top identity is an implementation invariant, not a new component-score gate.",
        "uncertainty": "Report paired HAC confidence intervals and first-day/t2 diagnostics. CI including zero is not an automatic veto.",
        "failure": "Stop, retain the previously recommended 63-feature 25% candidate. Do not tune target, weight, seed, feature group, postprocess or test additional years after failure.",
        "promotion": "Recommendation only. No production, official submission or DOCX changes.",
    }
    if protocol.get("rule") != fixed_rule:
        raise ValueError("The frozen score-first acceptance rule changed")
    return protocol


def _reference_metadata(year: int) -> dict:
    directory = (frozen.OUT if year in PRIMARY_YEARS
                 else ROOT / "experiments/return_head_scorefirst_eval")
    stem = f"return_z1_99_{year}"
    metadata = json.loads((directory / f"{stem}.json").read_text(encoding="utf-8"))
    if (metadata["model_sha256"] != file_hash(directory / f"{stem}.txt")
            or metadata["cache_sha256"] != file_hash(directory / f"{stem}.parquet")
            or metadata["features"] != feature_names()
            or metadata["target"] != frozen.read_protocol()["target"]
            or metadata["params"] != params_for_seed(SEED, THREADS)
            or metadata["rounds"] != ROUNDS or metadata["sample_weight"] is not None
            or metadata["reload_check_rows"] != 4096 or metadata["reload_max_abs_error"] != 0):
        raise ValueError("Frozen 63-feature reference model or metadata changed")
    return metadata


def _locked_sources() -> dict[str, str]:
    protocol = read_protocol()
    prior_manifest_path = ROOT / protocol["prior_manifest"]
    manifest = json.loads(prior_manifest_path.read_text(encoding="utf-8"))
    for relative, expected_hash in manifest.items():
        if file_hash(ROOT / relative) != expected_hash:
            raise ValueError(f"Frozen prior evidence changed: {relative}")
    for relative_directory in protocol["prior_directories"]:
        directory = ROOT / relative_directory
        prefix = directory.relative_to(ROOT).as_posix() + "/"
        declared = {name: value for name, value in manifest.items() if name.startswith(prefix)}
        actual = {path.relative_to(ROOT).as_posix(): file_hash(path)
                  for path in directory.rglob("*") if path.is_file()}
        if actual != declared:
            raise ValueError("A frozen prior directory file set or content changed")
    sources = dict(manifest)
    v1_out = ROOT / "experiments/return_market_eval"
    failed = json.loads((v1_out / "decision.json").read_text(encoding="utf-8"))
    if (failed.get("status") != "stopped_before_official_scoring_due_to_prefix_prediction_invariance_failure"
            or failed.get("candidate_key") != "protected_return_market_w0p25"
            or failed.get("official_scores") is not None
            or failed.get("development_score_gate_evaluated") is not False
            or failed.get("diagnostic_2024_run") is not False
            or failed.get("failure_audit_sha256") != file_hash(v1_out / "failure_audit.json")):
        raise ValueError("The unscored failed v1 evidence must remain intact")
    for year in PRIMARY_YEARS:
        v1_model = json.loads((v1_out / f"return_market_z1_99_{year}.json").read_text(encoding="utf-8"))
        sources.update(v1_model["source_sha256"])
    for path in (frozen.OUT / "development.json",
                 ROOT / "experiments/return_head_scorefirst_eval/diagnostic_2024.json",
                 ROOT / "experiments/return_market_stable_eval/development.json",
                 ROOT / "experiments/return_market_stable_eval/diagnostic_2024.json"):
        record = json.loads(path.read_text(encoding="utf-8"))
        sources.update(record["artifacts_sha256"])
    stable_out = ROOT / "experiments/return_market_stable_eval"
    stable_decision = json.loads((stable_out / "decision.json").read_text(encoding="utf-8"))
    if (stable_decision.get("recommended_for_next_version") is not False
            or stable_decision.get("retained_recommended_scheme") != BASELINE_KEY
            or stable_decision.get("diagnostic_2024_score_gate_passed") is not False
            or stable_decision.get("all_integrity_and_causality_checks_passed") is not True
            or stable_decision.get("development_sha256") != file_hash(stable_out / "development.json")
            or stable_decision.get("diagnostic_2024_sha256") != file_hash(stable_out / "diagnostic_2024.json")):
        raise ValueError("The previous market-feature negative result must remain intact")
    decision_path = ROOT / "experiments/return_head_scorefirst_eval/decision.json"
    decision = json.loads(decision_path.read_text(encoding="utf-8"))
    if (decision.get("candidate_key") != BASELINE_KEY
            or decision.get("recommended_for_next_version") is not True
            or decision.get("new_score_first_rule_passed") is not True
            or decision.get("diagnostic_2024_sha256") != file_hash(
                ROOT / "experiments/return_head_scorefirst_eval/diagnostic_2024.json")):
        raise ValueError("The comparison must remain the recommended 63-feature 25% head")
    if json.loads((frozen.OUT / "target_tests.json").read_text(encoding="utf-8")) != frozen.test_target():
        raise ValueError("Frozen target algorithm or unit tests changed")
    model_tests_path = OUT / "model_tests.json"
    if json.loads(model_tests_path.read_text(encoding="utf-8")) != test_model():
        raise ValueError("New model tests do not match frozen source/protocol")
    audit_path = ROOT / "validation/prediction_audit.json"
    sources.update(json.loads(audit_path.read_text(encoding="utf-8"))["input_sha256"])
    for relative, expected_hash in sources.items():
        if file_hash(ROOT / relative) != expected_hash:
            raise ValueError(f"Transitive evidence or production source changed: {relative}")
    paths = [FEATURE_FILE, MANIFEST, ROOT / "data" / "raw" / "训练集.csv",
             ROOT / "run.py", ROOT / "src/features.py", ROOT / "src/scoring.py",
             ROOT / "evaluate.py", ROOT / "experiments/seed_ensemble.py",
             ROOT / "experiments/day_balance_models.py", ROOT / "experiments/cached_recheck.py",
             Path(frozen.__file__),
             Path(__file__), ROOT / "experiments/audit_return_pooled.py",
             OUT / "protocol.json", model_tests_path, prior_manifest_path, audit_path]
    sources.update({str(path.relative_to(ROOT)): file_hash(path) for path in paths})
    return dict(sorted(sources.items()))


def _check_year(year: int) -> None:
    if year not in (*PRIMARY_YEARS, 2024):
        raise ValueError("Only primary 2022/2023 and conditionally permitted 2024 are supported")


def _paths(year: int) -> tuple[Path, Path, Path]:
    _check_year(year)
    stem = f"{MODEL_KEY}_{year}"
    return OUT / f"{stem}.txt", OUT / f"{stem}.parquet", OUT / f"{stem}.json"


def diagnostic_gate() -> dict:
    path = OUT / "development.json"
    if not path.exists():
        raise ValueError("2024 forbidden until both new development folds pass")
    record = json.loads(path.read_text(encoding="utf-8"))
    audit_source = ROOT / "experiments/audit_return_pooled.py"
    if (record.get("primary_gate_passed") is not True
            or record.get("all_integrity_and_causality_checks_passed") is not True
            or record.get("candidate_key") != CANDIDATE_KEY
            or record.get("baseline_key") != BASELINE_KEY
            or record.get("primary_years") != list(PRIMARY_YEARS)
            or record.get("protocol_sha256") != file_hash(OUT / "protocol.json")
            or record.get("audit_source_sha256") != file_hash(audit_source)):
        raise ValueError("2024 development gate is failed, mismatched or unaudited")
    required = {str(path.relative_to(ROOT)) for path in (
        audit_source, OUT / "protocol.json", OUT / "model_tests.json")}
    for year in PRIMARY_YEARS:
        yearly = record.get("years", {}).get(str(year), {})
        reference, candidate = yearly.get("reference", {}), yearly.get("candidate", {})
        old, new = reference.get("final_score", np.nan), candidate.get("final_score", np.nan)
        if not np.isfinite(old) or not np.isfinite(new) or new - old <= 1e-12:
            raise ValueError("2024 requires positive score gain over the recommended reference in BOTH years")
        if (yearly.get("passes_score_first_rule") is not True
                or yearly.get("all_integrity_and_causality_checks_passed") is not True
                or yearly.get("official_turnover_top_identities_equal") is not True
                or yearly.get("official_daily_turnover_exact") is not True
                or reference.get("mean_turnover") != candidate.get("mean_turnover")):
            raise ValueError("2024 requires all audits and actual daily Top/turnover checks")
        current = fingerprint(year)
        if record.get("model_fingerprints", {}).get(str(year)) != current["fingerprint_sha256"]:
            raise ValueError("New primary model fingerprints changed after evaluation")
        load_raw(year)
        required.update(current["source_sha256"])
        required.update(str(path.relative_to(ROOT)) for path in _paths(year))
        for name in ("reference", "candidate"):
            required.add(str((OUT / f"official_{name}_{year}_daily.csv").relative_to(ROOT)))
            required.add(str((OUT / f"{name}_processed_{year}.parquet").relative_to(ROOT)))
    artifacts = record.get("artifacts_sha256", {})
    normalized_required = {name.replace("\\", "/") for name in required}
    normalized_artifacts = {name.replace("\\", "/") for name in artifacts}
    if not normalized_required.issubset(normalized_artifacts):
        raise ValueError("Development gate omits required source/model/daily evidence")
    for relative, expected_hash in artifacts.items():
        if file_hash(ROOT / relative) != expected_hash:
            raise ValueError(f"New development artifact changed: {relative}")
    return {"development_sha256": file_hash(path), "primary_gate_passed": True}


def fingerprint(year: int) -> dict:
    _check_year(year)
    gate = diagnostic_gate() if year == 2024 else None
    cutoff = fold_cutoff(year)
    if cutoff != EXPECTED[year]["training_cutoff_exclusive"]:
        raise ValueError("One-day purge boundary changed")
    sources = _locked_sources()
    for path in (ROOT / f"models/fold_{year}.txt", ROOT / f"validation/fold_{year}.parquet"):
        sources[str(path.relative_to(ROOT))] = file_hash(path)
    reference = _reference_metadata(year)
    payload = {"year": year, "candidate_key": CANDIDATE_KEY, "baseline_key": BASELINE_KEY,
               "model_key": MODEL_KEY, "rounds": ROUNDS, "seed": SEED, "threads": THREADS,
               "params": params_for_seed(SEED, THREADS), "features": features_for_model(),
               "training_cutoff_exclusive": cutoff,
               "training_filter": read_protocol()["training_filter"], "target": read_protocol()["target"],
               "reference_daily_z_target_array_sha256": reference["target_stats"]["target_array_sha256"],
               "sample_weight": None, "blend": BLEND, "postprocess": POSTPROCESS,
               "validation_labels_loaded": False,
               "lightgbm_version": lgb.__version__, "numpy_version": np.__version__,
               "polars_version": pl.__version__, "source_sha256": dict(sorted(sources.items()))}
    if gate is not None:
        payload["diagnostic_gate"] = gate
    payload["fingerprint_sha256"] = hashlib.sha256(
        json.dumps(payload, sort_keys=True).encode("utf-8")).hexdigest()
    return payload


def feature_missingness(frame: pl.DataFrame) -> dict:
    features = features_for_model()
    nulls = frame.select(pl.col(features).null_count()).row(0, named=True)
    nans = frame.select(pl.col(features).is_nan().sum()).row(0, named=True)
    infinities = frame.select(pl.col(features).is_infinite().sum()).row(0, named=True)
    if any(infinities.values()):
        raise AssertionError("Frozen predictor cache contains unexpected infinity")
    return {"rows": len(frame), "feature_count": len(features),
            "null_count": nulls, "nan_count": nans, "infinite_count": infinities,
            "missing_features_retained_without_imputation": True}


def load_panel(year: int) -> Panel:
    _check_year(year)
    if year == 2024:
        diagnostic_gate()
    frame = pl.read_parquet(ROOT / f"validation/fold_{year}.parquet",
                            columns=KEYS + ["flag_limit_up", "price_valid", "pred_raw"])
    if (frame.select(pl.struct(KEYS).n_unique()).item() != len(frame)
            or not frame.select(KEYS).equals(frame.sort("trade_date", "ts_code").select(KEYS))
            or not frame["trade_date"].is_between(year * 10000 + 101, year * 10000 + 1231).all()):
        raise ValueError("Panel keys/order/year differ from original baseline")
    panel = Panel.from_frame(frame.with_columns(pl.lit(None, dtype=pl.Float64).alias("y_ret_1d")))
    if np.isfinite(panel.y).any():
        raise AssertionError("Prediction panel must contain no validation labels")
    return panel


def load_raw(year: int, panel: Panel | None = None) -> np.ndarray:
    model_path, cache_path, meta_path = _paths(year)
    metadata = json.loads(meta_path.read_text(encoding="utf-8"))
    expected = fingerprint(year)
    if any(metadata.get(key) != value for key, value in expected.items()):
        raise ValueError("Stale pooled-return model fingerprint/metadata")
    if (metadata["model_sha256"] != file_hash(model_path)
            or metadata["cache_sha256"] != file_hash(cache_path)):
        raise ValueError("Pooled-return model or raw cache hash changed")
    base = load_panel(year) if panel is None else panel
    frame = pl.read_parquet(cache_path)
    if (frame.columns != KEYS + ["pred_raw"]
            or not frame.select(KEYS).equals(base.frame.select(KEYS))
            or frame.select(pl.struct(KEYS).n_unique()).item() != len(frame)):
        raise ValueError("Pooled auxiliary keys/order/coverage differ from baseline")
    for field in ("training_first_date", "training_last_date", "training_rows"):
        if metadata[field] != EXPECTED[year][field]:
            raise ValueError(f"Saved training {field} changed")
    stats = metadata["target_stats"]
    if (stats["training_days"] != EXPECTED[year]["training_days"]
            or stats["training_rows"] != EXPECTED[year]["training_rows"]
            or not np.isfinite(stats["pooled_rms_float64"])
            or stats["pooled_rms_float64"] <= 1e-12
            or stats["pooled_nearconstant"] is not False
            or metadata.get("reference_daily_z_target_reconstructed_exact") is not True
            or metadata.get("target_differs_from_reference_daily_z") is not True
            or stats["target_array_sha256"] == expected["reference_daily_z_target_array_sha256"]
            or len(metadata.get("training_keys_sha256", "")) != 64
            or metadata["validation_rows"] != len(frame)
            or metadata["reload_check_rows"] != min(4096, len(frame))
            or metadata["reload_max_abs_error"] != 0):
        raise ValueError("Saved target, coverage or reload assertions differ")
    raw = frame["pred_raw"].to_numpy()
    if (raw.dtype != np.float32 or not np.isfinite(raw).all()
            or np.any(raw[~base.valid_price.reshape(-1)] != np.float32(-1e6))):
        raise ValueError("Raw predictions must be finite Float32 with invalid-price sentinel")
    return raw


def train(year: int) -> None:
    expected = fingerprint(year)
    model_path, cache_path, meta_path = _paths(year)
    if any(path.exists() for path in (model_path, cache_path, meta_path)):
        if not all(path.exists() for path in (model_path, cache_path, meta_path)):
            raise ValueError("Incomplete pooled auxiliary cache exists; preserve for inspection")
        load_raw(year)
        log(f"Validated frozen pooled-return cache: {year}")
        return
    features, cutoff = expected["features"], expected["training_cutoff_exclusive"]
    mask = (pl.col("is_train") & (pl.col("trade_date") < cutoff)
            & pl.col("y_rank").is_not_null() & pl.col("price_valid"))
    frame = pl.scan_parquet(FEATURE_FILE).filter(mask).select(KEYS + features + ["y_ret_1d"]).collect()
    if frame["y_ret_1d"].dtype != pl.Float32:
        raise AssertionError("Training target input must retain the original Float32 cache")
    x = to_matrix(frame, features)
    dates, returns = frame["trade_date"].to_numpy(), frame["y_ret_1d"].to_numpy()
    rows, first_date, last_date = len(frame), int(dates.min()), int(dates.max())
    if (rows != EXPECTED[year]["training_rows"] or first_date != EXPECTED[year]["training_first_date"]
            or last_date != EXPECTED[year]["training_last_date"] or last_date >= cutoff
            or not np.isfinite(returns).all()
            or frame.select(pl.struct(KEYS).n_unique()).item() != rows):
        raise AssertionError("Training mask rows, date boundaries or targets differ")
    y, target_stats = _target_with_stats(dates, returns)
    if (target_stats["training_days"] != EXPECTED[year]["training_days"]
            or target_stats["training_rows"] != rows
            or target_stats["pooled_nearconstant"]
            or target_stats["target_array_sha256"] == expected["reference_daily_z_target_array_sha256"]):
        raise AssertionError("Pooled target count, scale or intended difference from daily-z target failed")
    reference_target, reference_stats = frozen._target_with_stats(dates, returns)
    if reference_stats != _reference_metadata(year)["target_stats"]:
        raise AssertionError("Original training labels or row order differ from the frozen reference")
    training_keys_sha256 = hashlib.sha256(frame.select(KEYS).write_csv().encode("utf-8")).hexdigest()
    train_missingness = feature_missingness(frame)
    del frame, dates, returns, reference_target
    gc.collect()
    log(f"Training {year}/{MODEL_KEY}: rows={rows:,}, days={target_stats['training_days']}, "
        f"features={len(features)}, dates={first_date}..{last_date}, purge={cutoff}")
    started = time.monotonic()
    dataset = lgb.Dataset(x, label=y, feature_name=features, free_raw_data=True)
    model = lgb.train(expected["params"], dataset, num_boost_round=ROUNDS)
    model_path.write_text(model.model_to_string(), encoding="utf-8")
    del dataset, x, y
    gc.collect()
    valid_mask = pl.col("is_train") & pl.col("trade_date").is_between(
        year * 10000 + 101, year * 10000 + 1231)
    valid = (pl.scan_parquet(FEATURE_FILE).filter(valid_mask).sort("trade_date", "ts_code")
             .select(features + KEYS + ["price_valid"]).collect())
    valid_missingness = feature_missingness(valid)
    matrix = to_matrix(valid, features)
    raw = model.predict(matrix, num_threads=THREADS).astype(np.float32)
    valid_price = valid["price_valid"].to_numpy()
    raw[~valid_price] = -1e6
    if not np.isfinite(raw).all():
        raise AssertionError("Pooled auxiliary emitted nonfinite raw predictions")
    reloaded = lgb.Booster(model_str=model_path.read_text(encoding="utf-8"))
    if reloaded.feature_name() != features or reloaded.current_iteration() != ROUNDS:
        raise AssertionError("Saved pooled auxiliary feature order or rounds differ")
    indices = np.linspace(0, len(raw) - 1, min(4096, len(raw)), dtype=int)
    checked = reloaded.predict(matrix[indices], num_threads=THREADS).astype(np.float32)
    checked[~valid_price[indices]] = -1e6
    reload_error = float(np.max(np.abs(checked.astype(float) - raw[indices].astype(float))))
    if reload_error != 0:
        raise AssertionError(f"Reloaded pooled auxiliary differs: {reload_error}")
    result = valid.select(KEYS).with_columns(pl.Series("pred_raw", raw))
    if not result.select(KEYS).equals(load_panel(year).frame.select(KEYS)):
        raise AssertionError("Pooled auxiliary cache coverage/order differs from baseline")
    result.write_parquet(cache_path, compression="zstd")
    if fingerprint(year) != expected:
        raise AssertionError("Frozen source/input changed during pooled-return training")
    metadata = {**expected, "training_rows": rows, "training_first_date": first_date,
                "training_last_date": last_date, "validation_rows": len(raw),
                "validation_days": valid["trade_date"].n_unique(),
                "validation_first_date": int(valid["trade_date"].min()),
                "validation_last_date": int(valid["trade_date"].max()),
                "target_stats": target_stats,
                "training_keys_sha256": training_keys_sha256,
                "training_keys_hash_encoding": "frame.select(KEYS).write_csv().encode('utf-8'); original training row order",
                "reference_daily_z_target_reconstructed_exact": True,
                "target_differs_from_reference_daily_z": True,
                "training_feature_missingness": train_missingness,
                "validation_feature_missingness": valid_missingness,
                "model_sha256": file_hash(model_path), "cache_sha256": file_hash(cache_path),
                "reload_check_rows": len(indices), "reload_max_abs_error": reload_error,
                "elapsed_seconds": time.monotonic() - started}
    meta_path.write_text(json.dumps(metadata, ensure_ascii=False, indent=2), encoding="utf-8")
    log(f"Saved {year}: rows={len(raw):,}, elapsed={metadata['elapsed_seconds']:.1f}s, reload={reload_error}")
    del model, reloaded, matrix, valid, raw, result
    gc.collect()
    load_raw(year)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("step", choices=("check", "test", "train"))
    parser.add_argument("--year", type=int, choices=(*PRIMARY_YEARS, 2024))
    args = parser.parse_args()
    if args.step == "test":
        result = test_model()
        path = OUT / "model_tests.json"
        if path.exists() and json.loads(path.read_text(encoding="utf-8")) != result:
            raise ValueError("Preserve previous model tests: source or protocol changed")
        if not path.exists():
            path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
        log("Frozen 63-feature pooled-return-head model tests passed")
    elif args.step == "check":
        if args.year is None:
            log(f"Verified {len(_locked_sources())} frozen prior/model sources")
        else:
            log(f"Verified {args.year} fingerprint {fingerprint(args.year)['fingerprint_sha256']}")
    else:
        if args.year is None:
            parser.error("train requires --year; 2024 is independently gated")
        train(args.year)
