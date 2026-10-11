"""Fixed 71-feature return-amplitude auxiliary; no validation labels loaded.

Only eight frozen market-relative predictors are added to the recommended
63-feature auxiliary. Target, rows, parameters and protected 25% blend are fixed.
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

from experiments import feature_expansion as expansion
from experiments import feature_expansion_features as added
from experiments import return_head_models as frozen
from experiments.seed_ensemble import params_for_seed
from run import FEATURE_FILE, MANIFEST, ROOT, feature_names, fold_cutoff, to_matrix
from src.scoring import Panel


OUT = ROOT / "experiments" / "return_market_eval"
PRIMARY_YEARS = (2022, 2023)
MODEL_KEY = "return_market_z1_99"
CANDIDATE_KEY = "protected_return_market_w0p25"
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
training_target = frozen.training_target


def log(message: str) -> None:
    print(f"[{time.strftime('%H:%M:%S')}] {message}", flush=True)


def features_for_model() -> list[str]:
    features = expansion.features_for_variant("market")
    if (len(features) != 71 or features[:63] != feature_names()
            or features[63:] != list(added.GROUPS["market_relative"])):
        raise ValueError("The original 63 + fixed eight market predictors changed")
    return features


def read_protocol() -> dict:
    protocol = json.loads((OUT / "protocol.json").read_text(encoding="utf-8"))
    fixed = {"experiment": "fixed_market_features_return_head_protected_top_score_first",
             "declared_before_training_and_scoring": True, "candidate_key": CANDIDATE_KEY,
             "model_key": MODEL_KEY, "baseline_key": BASELINE_KEY,
             "primary_years": list(PRIMARY_YEARS), "conditional_diagnostic_year": 2024,
             "candidate_count": 1, "feature_count": 71, "feature_variant": "market",
             "added_features": features_for_model()[63:],
             "rounds": ROUNDS, "seed": SEED, "threads": THREADS,
             "blend": BLEND, "postprocess": POSTPROCESS,
             "training_filter": "is_train & trade_date < fold_cutoff(year) & y_rank.not_null & price_valid"}
    if any(protocol.get(key) != value for key, value in fixed.items()):
        raise ValueError("Market-return-head protocol differs from its single fixed design")
    if (protocol.get("target") != frozen.read_protocol()["target"]
            or protocol.get("folds") != {str(year): values for year, values in EXPECTED.items()}):
        raise ValueError("The original return target or training boundaries changed")
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
    if len(manifest) != 42:
        raise ValueError("The predeclared 42-file prior manifest changed")
    for relative, expected_hash in manifest.items():
        if file_hash(ROOT / relative) != expected_hash:
            raise ValueError(f"Frozen prior evidence changed: {relative}")
    for directory in (frozen.OUT, ROOT / "experiments/return_head_scorefirst_eval"):
        prefix = directory.relative_to(ROOT).as_posix() + "/"
        declared = {name: value for name, value in manifest.items() if name.startswith(prefix)}
        actual = {path.relative_to(ROOT).as_posix(): file_hash(path)
                  for path in directory.rglob("*") if path.is_file()}
        if actual != declared:
            raise ValueError("A frozen prior directory file set or content changed")
    sources = dict(manifest)
    for path in (frozen.OUT / "development.json",
                 ROOT / "experiments/return_head_scorefirst_eval/diagnostic_2024.json"):
        record = json.loads(path.read_text(encoding="utf-8"))
        sources.update(record["artifacts_sha256"])
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
    expansion.verify_feature_inputs()
    paths = [FEATURE_FILE, MANIFEST, added.ADDED_FEATURE_FILE, ROOT / "data" / "raw" / "训练集.csv",
             ROOT / "run.py", ROOT / "src/features.py", ROOT / "src/scoring.py",
             ROOT / "evaluate.py", ROOT / "experiments/seed_ensemble.py",
             ROOT / "experiments/day_balance_models.py", ROOT / "experiments/cached_recheck.py",
             Path(frozen.__file__), Path(expansion.__file__), Path(added.__file__),
             ROOT / "experiments/feature_expansion_eval/protocol.json",
             Path(__file__), ROOT / "experiments/audit_return_market.py",
             ROOT / "experiments/check_return_market_prefix.py",
             ROOT / "experiments/check_feature_expansion_prefix.py",
             OUT / "protocol.json", model_tests_path, prior_manifest_path, audit_path]
    sources.update({str(path.relative_to(ROOT)): file_hash(path) for path in paths})
    return dict(sorted(sources.items()))


def test_model() -> dict:
    """Pure checks before training; no validation returns or model fitting."""
    read_protocol()
    original_target = frozen.test_target()
    features = features_for_model()
    base = pl.DataFrame({"ts_code": ["B", "A", "A"], "trade_date": [2, 1, 2],
                         "base": [1., 2., 3.]}).with_row_index("_left_order")
    extra = pl.DataFrame({"ts_code": ["A", "B", "A"], "trade_date": [2, 2, 1],
                          "market": [None, 4., 5.]}).with_columns(pl.lit(True).alias("_matched"))
    joined = base.join(extra, on=KEYS, how="left", validate="1:1", maintain_order="left")
    assert joined.select(KEYS).equals(base.select(KEYS))
    assert joined["_left_order"].equals(base["_left_order"])
    assert joined["market"].to_list() == [4., 5., None]
    assert joined["_matched"].null_count() == 0
    missing = base.join(extra.head(2), on=KEYS, how="left", validate="1:1", maintain_order="left")
    assert missing["_matched"].null_count() == 1
    try:
        base.join(pl.concat([extra, extra.head(1)]), on=KEYS, how="left", validate="1:1", maintain_order="left")
    except pl.exceptions.ComputeError:
        duplicate_rejected = True
    else:
        raise AssertionError("A duplicate added-feature key was accepted")
    return {"status": "passed", "feature_count": len(features), "features": features,
            "same_frozen_target_tests": original_target,
            "left_join_original_order_and_nullable_values": True,
            "missing_key_detected_separately_from_nullable_feature": True,
            "duplicate_added_key_rejected": duplicate_rejected,
            "source_sha256": file_hash(Path(__file__)),
            "protocol_sha256": file_hash(OUT / "protocol.json")}


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
    audit_source = ROOT / "experiments/audit_return_market.py"
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
               "reference_target_array_sha256": reference["target_stats"]["target_array_sha256"],
               "sample_weight": None, "blend": BLEND, "postprocess": POSTPROCESS,
               "validation_labels_loaded": False,
               "lightgbm_version": lgb.__version__, "numpy_version": np.__version__,
               "polars_version": pl.__version__, "source_sha256": dict(sorted(sources.items()))}
    if gate is not None:
        payload["diagnostic_gate"] = gate
    payload["fingerprint_sha256"] = hashlib.sha256(
        json.dumps(payload, sort_keys=True).encode("utf-8")).hexdigest()
    return payload


def joined_frame(mask: pl.Expr, columns: list[str], sort: bool = False) -> pl.DataFrame:
    """Exact base keys retained with a checked 1:1 left join; no imputation."""
    return expansion._joined_frame(mask, columns, features_for_model()[63:], sort=sort)


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
        raise ValueError("Stale return-market model fingerprint/metadata")
    if (metadata["model_sha256"] != file_hash(model_path)
            or metadata["cache_sha256"] != file_hash(cache_path)):
        raise ValueError("Return-market model or raw cache hash changed")
    base = load_panel(year) if panel is None else panel
    frame = pl.read_parquet(cache_path)
    if (frame.columns != KEYS + ["pred_raw"]
            or not frame.select(KEYS).equals(base.frame.select(KEYS))
            or frame.select(pl.struct(KEYS).n_unique()).item() != len(frame)):
        raise ValueError("Market auxiliary keys/order/coverage differ from baseline")
    for field in ("training_first_date", "training_last_date", "training_rows"):
        if metadata[field] != EXPECTED[year][field]:
            raise ValueError(f"Saved training {field} changed")
    stats = metadata["target_stats"]
    if (stats["training_days"] != EXPECTED[year]["training_days"]
            or stats["training_rows"] != EXPECTED[year]["training_rows"]
            or stats["target_array_sha256"] != expected["reference_target_array_sha256"]
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
            raise ValueError("Incomplete market auxiliary cache exists; preserve for inspection")
        load_raw(year)
        log(f"Validated frozen return-market cache: {year}")
        return
    features, cutoff = expected["features"], expected["training_cutoff_exclusive"]
    mask = (pl.col("is_train") & (pl.col("trade_date") < cutoff)
            & pl.col("y_rank").is_not_null() & pl.col("price_valid"))
    frame = joined_frame(mask, features + ["trade_date", "y_ret_1d"])
    if frame["y_ret_1d"].dtype != pl.Float32:
        raise AssertionError("Training target input must retain the original Float32 cache")
    x = to_matrix(frame, features)
    dates, returns = frame["trade_date"].to_numpy(), frame["y_ret_1d"].to_numpy()
    rows, first_date, last_date = len(frame), int(dates.min()), int(dates.max())
    if (rows != EXPECTED[year]["training_rows"] or first_date != EXPECTED[year]["training_first_date"]
            or last_date != EXPECTED[year]["training_last_date"] or last_date >= cutoff
            or not np.isfinite(returns).all()):
        raise AssertionError("Training mask rows, date boundaries or targets differ")
    y, target_stats = frozen._target_with_stats(dates, returns)
    if (target_stats["training_days"] != EXPECTED[year]["training_days"]
            or target_stats["target_array_sha256"] != expected["reference_target_array_sha256"]):
        raise AssertionError("Training target bytes/order differ from the frozen 63-feature reference")
    train_missingness = feature_missingness(frame)
    del frame, dates, returns
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
    valid = joined_frame(valid_mask, features + KEYS + ["price_valid"], sort=True)
    valid_missingness = feature_missingness(valid)
    matrix = to_matrix(valid, features)
    raw = model.predict(matrix, num_threads=THREADS).astype(np.float32)
    valid_price = valid["price_valid"].to_numpy()
    raw[~valid_price] = -1e6
    if not np.isfinite(raw).all():
        raise AssertionError("Market auxiliary emitted nonfinite raw predictions")
    reloaded = lgb.Booster(model_str=model_path.read_text(encoding="utf-8"))
    if reloaded.feature_name() != features or reloaded.current_iteration() != ROUNDS:
        raise AssertionError("Saved market auxiliary feature order or rounds differ")
    indices = np.linspace(0, len(raw) - 1, min(4096, len(raw)), dtype=int)
    checked = reloaded.predict(matrix[indices], num_threads=THREADS).astype(np.float32)
    checked[~valid_price[indices]] = -1e6
    reload_error = float(np.max(np.abs(checked.astype(float) - raw[indices].astype(float))))
    if reload_error != 0:
        raise AssertionError(f"Reloaded market auxiliary differs: {reload_error}")
    result = valid.select(KEYS).with_columns(pl.Series("pred_raw", raw))
    if not result.select(KEYS).equals(load_panel(year).frame.select(KEYS)):
        raise AssertionError("Market auxiliary cache coverage/order differs from baseline")
    result.write_parquet(cache_path, compression="zstd")
    if fingerprint(year) != expected:
        raise AssertionError("Frozen source/input changed during return-market training")
    metadata = {**expected, "training_rows": rows, "training_first_date": first_date,
                "training_last_date": last_date, "validation_rows": len(raw),
                "validation_days": valid["trade_date"].n_unique(),
                "validation_first_date": int(valid["trade_date"].min()),
                "validation_last_date": int(valid["trade_date"].max()),
                "target_stats": target_stats,
                "training_feature_missingness": train_missingness,
                "validation_feature_missingness": valid_missingness,
                "feature_alignment": expansion.verify_feature_inputs(),
                "training_target_matches_63_feature_reference_exact": True,
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
        log("Frozen 71-feature return-head model tests passed")
    elif args.step == "check":
        if args.year is None:
            log(f"Verified {len(_locked_sources())} frozen prior/model sources")
        else:
            log(f"Verified {args.year} fingerprint {fingerprint(args.year)['fingerprint_sha256']}")
    else:
        if args.year is None:
            parser.error("train requires --year; 2024 is independently gated")
        train(args.year)
