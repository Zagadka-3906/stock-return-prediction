"""User-authorized score-first 2024 diagnostic, separate from the failed IC gate.

The original return-head experiment and its failed primary gate remain frozen.
This module copies no target algorithm and never invokes the old 2024 entrypoints.
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


OUT = ROOT / "experiments" / "return_head_scorefirst_eval"
YEAR = 2024
CANDIDATE_KEY = "protected_return_w0p25"
MODEL_KEY = "return_z1_99"
ROUNDS, SEED, THREADS = 180, 2026, 16
BLEND = {"mode": "top_only", "weight": .25}
POSTPROCESS = {"alpha": .9, "bonus": .3, "restore_lower": True, "top_current_weight": 1.0}
KEYS = ["ts_code", "trade_date"]
EXPECTED = {"training_cutoff_exclusive": 20231229, "training_first_date": 20180102,
            "training_last_date": 20231228, "training_rows": 5659954, "training_days": 1456}
file_hash = frozen.file_hash
training_target = frozen.training_target


def log(message: str) -> None:
    print(f"[{time.strftime('%H:%M:%S')}] {message}", flush=True)


def read_protocol() -> dict:
    protocol = json.loads((OUT / "protocol.json").read_text(encoding="utf-8"))
    fixed = {"experiment": "fixed_return_head_2024_score_first_reconsideration",
             "declared_before_2024_candidate_training_and_scoring": True,
             "user_authorized_rule_change": True,
             "rule_change_after_2022_2023_results_known": True,
             "old_protocol_and_failure_record_preserved": True,
             "old_primary_gate_passed": False, "candidate_count": 1,
             "year": YEAR, "candidate_key": CANDIDATE_KEY, "model_key": MODEL_KEY,
             "feature_count": 63, "rounds": ROUNDS, "seed": SEED, "threads": THREADS,
             "blend": BLEND, "postprocess": POSTPROCESS,
             "training_filter": "is_train & trade_date < fold_cutoff(year) & y_rank.not_null & price_valid"}
    if any(protocol.get(key) != value for key, value in fixed.items()):
        raise ValueError("Score-first protocol differs from the single user-authorized diagnostic")
    original = frozen.read_protocol()
    if protocol.get("target") != original["target"] or protocol.get("fold") != EXPECTED:
        raise ValueError("The original auxiliary target or 2024 training boundary changed")
    fixed_rule = {
        "development_prerequisite": "Frozen 2022 and 2023 official composite scores both improve, with exact daily official Top identities and turnover preserved; their original per-component gate remains recorded as failed.",
        "diagnostic_acceptance": "2024 official candidate final_score minus baseline final_score > 1e-12, and all implementation, provenance, causality, complete coverage, same-CSV official scoring and exact daily turnover Top identity/series checks pass.",
        "numerical_score_tolerance": 1e-12,
        "component_metrics": "Report IC, annual excess and turnover separately. IC or another component need not independently improve if the official composite improves and the protected-turnover invariant passes.",
        "uncertainty": "Report paired HAC intervals, first-day and t2-onward sensitivity. Confidence intervals containing zero are disclosed as weak evidence, not an automatic rejection threshold.",
        "if_passed": "Recommend the fixed 25% scheme for the next version under the score-first preference, with exploratory-history and uncertainty caveats. Record recommendation separately from actual deployment.",
        "if_failed": "Do not adopt; retain production baseline. Do not change the blend, target, year or acceptance threshold after seeing this result.",
    }
    if protocol.get("new_rule") != fixed_rule:
        raise ValueError("The separately authorized score-first rule changed")
    return protocol


def preflight() -> dict:
    """Verify new score-first permission while explicitly preserving old failure."""
    protocol = read_protocol()
    expected_previous = {
        "experiments/return_head_eval/protocol.json", "experiments/return_head_eval/development.json",
        "experiments/return_head_eval/decision.json", "experiments/return_head_models.py",
        "experiments/audit_return_head.py", "experiments/return_head_eval/target_tests.json",
        "experiments/return_head_eval/prediction_tests.json",
    }
    prior_hashes = protocol["prior_files_sha256"]
    if set(prior_hashes) != expected_previous:
        raise ValueError("The seven directly locked prior evidence files changed")
    for relative, expected_hash in prior_hashes.items():
        path = ROOT / relative
        if file_hash(path) != expected_hash:
            raise ValueError(f"Prior return-head evidence changed: {path.name}")
    manifest_path = ROOT / protocol["prior_directory_manifest"]
    if file_hash(manifest_path) != protocol["prior_directory_manifest_sha256"]:
        raise ValueError("The original-directory manifest changed")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    present = {path.relative_to(ROOT).as_posix(): file_hash(path)
               for path in frozen.OUT.rglob("*") if path.is_file()}
    if present != manifest:
        raise ValueError("The original return-head directory file set or contents changed")
    development = json.loads((frozen.OUT / "development.json").read_text(encoding="utf-8"))
    decision = json.loads((frozen.OUT / "decision.json").read_text(encoding="utf-8"))
    if (development.get("candidate_key") != CANDIDATE_KEY
            or development.get("primary_years") != [2022, 2023]
            or development.get("candidate_count") != 1
            or development.get("blend") != BLEND or development.get("postprocess") != POSTPROCESS
            or development.get("primary_gate_passed") is not False
            or decision.get("primary_gate_passed") is not False
            or decision.get("candidate_key") != CANDIDATE_KEY
            or decision.get("development_sha256") != prior_hashes["experiments/return_head_eval/development.json"]
            or development.get("protocol_sha256") != prior_hashes["experiments/return_head_eval/protocol.json"]
            or development.get("audit_source_sha256") != prior_hashes["experiments/audit_return_head.py"]):
        raise ValueError("Original candidate or failed IC gate evidence is inconsistent")
    if json.loads((frozen.OUT / "target_tests.json").read_text(encoding="utf-8")) != frozen.test_target():
        raise ValueError("Original target algorithm/tests changed")
    sources = dict(development["artifacts_sha256"])
    if len(sources) != 222:
        raise ValueError("The original complete 222-artifact development manifest changed")
    years = {}
    original_gate_parts = []
    for year in (2022, 2023):
        yearly = development["years"][str(year)]
        baseline, candidate = yearly["baseline"], yearly["candidate"]
        for metric in ("ic_mean", "annual_excess", "final_score", "mean_turnover"):
            if not np.isfinite(baseline[metric]) or not np.isfinite(candidate[metric]):
                raise ValueError("Development metrics must be finite")
        top_exact = (yearly.get("official_turnover_top_identities_equal") is True
                     and yearly.get("official_daily_turnover_exact") is True
                     and yearly.get("prediction_checks", {}).get("official_top_identity", {}).get(
                         "daily_top_identities_exact") is True
                     and baseline["mean_turnover"] == candidate["mean_turnover"])
        improved_score = candidate["final_score"] - baseline["final_score"] > 1e-12
        if not improved_score or not top_exact:
            raise ValueError("The separate score-first development gate did not pass in both years")
        original_gate_parts.append(top_exact and all(candidate[key] > baseline[key]
            for key in ("ic_mean", "annual_excess", "final_score")))
        # Only the old 2022/2023 APIs are allowed: their original gate is irrelevant.
        old_payload = frozen.fingerprint(year)
        if development["model_fingerprints"][str(year)] != old_payload["fingerprint_sha256"]:
            raise ValueError("Original primary auxiliary fingerprint changed")
        frozen.load_raw(year)
        if not set(old_payload["source_sha256"]).issubset(sources):
            raise ValueError("Original development omits source fingerprint artifacts")
        years[str(year)] = {"score_delta": candidate["final_score"] - baseline["final_score"],
                            "ic_delta": candidate["ic_mean"] - baseline["ic_mean"],
                            "annual_excess_delta": candidate["annual_excess"] - baseline["annual_excess"],
                            "official_top_and_turnover_exact": top_exact,
                            "score_first_passed": improved_score and top_exact,
                            "model_fingerprint_sha256": old_payload["fingerprint_sha256"]}
    if all(original_gate_parts):
        raise ValueError("Original simultaneous-improvement gate no longer matches its recorded failure")
    for relative, expected_hash in sources.items():
        if file_hash(ROOT / relative) != expected_hash:
            raise ValueError(f"Original development artifact/source changed: {relative}")
    sources.update(manifest)
    sources.update(prior_hashes)
    audit_path = ROOT / "validation/prediction_audit.json"
    production = json.loads(audit_path.read_text(encoding="utf-8"))["input_sha256"]
    for relative, expected_hash in production.items():
        if file_hash(ROOT / relative) != expected_hash:
            raise ValueError(f"Production source/artifact changed: {relative}")
    sources.update(production)
    paths = [FEATURE_FILE, MANIFEST, ROOT / "data" / "raw" / "训练集.csv", ROOT / "run.py",
             ROOT / "src/features.py", ROOT / "src/scoring.py", ROOT / "evaluate.py",
             ROOT / "experiments/seed_ensemble.py", ROOT / "experiments/day_balance_models.py",
             ROOT / "experiments/cached_recheck.py", ROOT / "experiments/official_seed_development.py",
             Path(__file__), OUT / "protocol.json", audit_path, ROOT / "validation/metrics.json",
             ROOT / f"models/fold_{YEAR}.txt", ROOT / f"validation/fold_{YEAR}.parquet",
             manifest_path, *(ROOT / relative for relative in prior_hashes)]
    sources.update({str(path.relative_to(ROOT)): file_hash(path) for path in paths})
    return {"old_primary_gate_passed": False, "new_score_first_development_gate_passed": True,
            "original_artifacts_verified": 222, "previous_years": years,
            "original_directory_files_verified": len(manifest),
            "source_sha256": dict(sorted(sources.items()))}


def fingerprint() -> dict:
    cutoff = fold_cutoff(YEAR)
    if cutoff != EXPECTED["training_cutoff_exclusive"]:
        raise ValueError("The original 2024 one-day purge date changed")
    features = feature_names()
    if len(features) != 63:
        raise ValueError("Exactly the original 63 features must be retained")
    previous = preflight()
    payload = {"year": YEAR, "candidate_key": CANDIDATE_KEY, "model_key": MODEL_KEY,
               "rounds": ROUNDS, "seed": SEED, "threads": THREADS,
               "params": params_for_seed(SEED, THREADS), "features": features,
               "training_cutoff_exclusive": cutoff,
               "training_filter": read_protocol()["training_filter"],
               "target": read_protocol()["target"], "sample_weight": None,
               "blend": BLEND, "postprocess": POSTPROCESS,
               "validation_labels_loaded": False, "old_primary_gate_passed": False,
               "new_score_first_development_gate_passed": True,
               "previous_years": previous["previous_years"],
               "lightgbm_version": lgb.__version__, "numpy_version": np.__version__,
               "polars_version": pl.__version__, "source_sha256": previous["source_sha256"]}
    payload["fingerprint_sha256"] = hashlib.sha256(
        json.dumps(payload, sort_keys=True).encode("utf-8")).hexdigest()
    return payload


def _paths() -> tuple[Path, Path, Path]:
    stem = f"{MODEL_KEY}_{YEAR}"
    return OUT / f"{stem}.txt", OUT / f"{stem}.parquet", OUT / f"{stem}.json"


def load_panel() -> Panel:
    """Read only baseline observables and raw predictions, never 2024 labels."""
    frame = pl.read_parquet(ROOT / f"validation/fold_{YEAR}.parquet",
                            columns=KEYS + ["flag_limit_up", "price_valid", "pred_raw"])
    if (frame.select(pl.struct(KEYS).n_unique()).item() != len(frame)
            or not frame.select(KEYS).equals(frame.sort("trade_date", "ts_code").select(KEYS))
            or not frame["trade_date"].is_between(YEAR * 10000 + 101, YEAR * 10000 + 1231).all()):
        raise ValueError("2024 baseline keys/order/year differ")
    panel = Panel.from_frame(frame.with_columns(pl.lit(None, dtype=pl.Float64).alias("y_ret_1d")))
    if np.isfinite(panel.y).any():
        raise AssertionError("Prediction panel must contain no validation labels")
    return panel


def load_raw(panel: Panel | None = None) -> np.ndarray:
    model_path, cache_path, meta_path = _paths()
    metadata = json.loads(meta_path.read_text(encoding="utf-8"))
    expected = fingerprint()
    if any(metadata.get(key) != value for key, value in expected.items()):
        raise ValueError("Stale score-first 2024 auxiliary fingerprint/metadata")
    if (metadata["model_sha256"] != file_hash(model_path)
            or metadata["cache_sha256"] != file_hash(cache_path)):
        raise ValueError("Score-first auxiliary model/cache hash changed")
    base = load_panel() if panel is None else panel
    frame = pl.read_parquet(cache_path)
    if (frame.columns != KEYS + ["pred_raw"]
            or not frame.select(KEYS).equals(base.frame.select(KEYS))
            or frame.select(pl.struct(KEYS).n_unique()).item() != len(frame)):
        raise ValueError("Score-first auxiliary keys/order/coverage differ from baseline")
    for field in ("training_first_date", "training_last_date", "training_rows"):
        if metadata[field] != EXPECTED[field]:
            raise ValueError(f"Saved training {field} changed")
    stats = metadata["target_stats"]
    if (stats["training_days"] != EXPECTED["training_days"]
            or stats["training_rows"] != EXPECTED["training_rows"]
            or metadata["validation_rows"] != len(frame)
            or metadata["reload_check_rows"] != min(4096, len(frame))
            or metadata["reload_max_abs_error"] != 0):
        raise ValueError("Saved target, coverage or reload checks differ")
    raw = frame["pred_raw"].to_numpy()
    if (raw.dtype != np.float32 or not np.isfinite(raw).all()
            or np.any(raw[~base.valid_price.reshape(-1)] != np.float32(-1e6))):
        raise ValueError("Raw predictions must be finite Float32 with invalid-price sentinel")
    return raw


def train() -> None:
    expected = fingerprint()
    model_path, cache_path, meta_path = _paths()
    if any(path.exists() for path in (model_path, cache_path, meta_path)):
        if not all(path.exists() for path in (model_path, cache_path, meta_path)):
            raise ValueError("Incomplete score-first cache exists; preserve for inspection")
        load_raw()
        log("Validated frozen score-first 2024 auxiliary cache")
        return
    features, cutoff = expected["features"], expected["training_cutoff_exclusive"]
    lazy = pl.scan_parquet(FEATURE_FILE)
    mask = (pl.col("is_train") & (pl.col("trade_date") < cutoff)
            & pl.col("y_rank").is_not_null() & pl.col("price_valid"))
    frame = lazy.filter(mask).select(features + ["trade_date", "y_ret_1d"]).collect()
    if frame["y_ret_1d"].dtype != pl.Float32:
        raise AssertionError("Training labels must be the original Float32 cache")
    x = to_matrix(frame, features)
    dates, returns = frame["trade_date"].to_numpy(), frame["y_ret_1d"].to_numpy()
    rows, first_date, last_date = len(frame), int(dates.min()), int(dates.max())
    if (rows != EXPECTED["training_rows"] or first_date != EXPECTED["training_first_date"]
            or last_date != EXPECTED["training_last_date"] or last_date >= cutoff
            or not np.isfinite(returns).all()):
        raise AssertionError("2024 training mask, rows, boundaries or returns differ")
    y, target_stats = frozen._target_with_stats(dates, returns)
    if target_stats["training_days"] != EXPECTED["training_days"]:
        raise AssertionError("2024 target training-day count changed")
    del frame, dates, returns
    gc.collect()
    log(f"Training {YEAR}/{MODEL_KEY}: rows={rows:,}, days={target_stats['training_days']}, "
        f"features={len(features)}, dates={first_date}..{last_date}, purge={cutoff}")
    started = time.monotonic()
    dataset = lgb.Dataset(x, label=y, feature_name=features, free_raw_data=True)
    model = lgb.train(expected["params"], dataset, num_boost_round=ROUNDS)
    model_path.write_text(model.model_to_string(), encoding="utf-8")
    del dataset, x, y
    gc.collect()
    valid = (lazy.filter(pl.col("is_train") & pl.col("trade_date").is_between(
        YEAR * 10000 + 101, YEAR * 10000 + 1231)).sort("trade_date", "ts_code")
        .select(features + KEYS + ["price_valid"]).collect())
    matrix = to_matrix(valid, features)
    raw = model.predict(matrix, num_threads=THREADS).astype(np.float32)
    valid_price = valid["price_valid"].to_numpy()
    raw[~valid_price] = -1e6
    if not np.isfinite(raw).all():
        raise AssertionError("Score-first 2024 auxiliary emitted nonfinite raw predictions")
    reloaded = lgb.Booster(model_str=model_path.read_text(encoding="utf-8"))
    if reloaded.feature_name() != features or reloaded.current_iteration() != ROUNDS:
        raise AssertionError("Saved auxiliary feature order or rounds differ")
    indices = np.linspace(0, len(raw) - 1, min(4096, len(raw)), dtype=int)
    checked = reloaded.predict(matrix[indices], num_threads=THREADS).astype(np.float32)
    checked[~valid_price[indices]] = -1e6
    reload_error = float(np.max(np.abs(checked.astype(float) - raw[indices].astype(float))))
    if reload_error != 0:
        raise AssertionError(f"Reloaded score-first auxiliary differs: {reload_error}")
    result = valid.select(KEYS).with_columns(pl.Series("pred_raw", raw))
    if not result.select(KEYS).equals(load_panel().frame.select(KEYS)):
        raise AssertionError("Auxiliary cache coverage/order differs from 2024 baseline")
    result.write_parquet(cache_path, compression="zstd")
    if fingerprint() != expected:
        raise AssertionError("A frozen source/input changed during score-first auxiliary training")
    metadata = {**expected, "training_rows": rows, "training_first_date": first_date,
                "training_last_date": last_date, "validation_rows": len(raw),
                "validation_days": valid["trade_date"].n_unique(),
                "validation_first_date": int(valid["trade_date"].min()),
                "validation_last_date": int(valid["trade_date"].max()),
                "target_stats": target_stats,
                "model_sha256": file_hash(model_path), "cache_sha256": file_hash(cache_path),
                "reload_check_rows": len(indices), "reload_max_abs_error": reload_error,
                "elapsed_seconds": time.monotonic() - started}
    meta_path.write_text(json.dumps(metadata, ensure_ascii=False, indent=2), encoding="utf-8")
    log(f"Saved {YEAR}: rows={len(raw):,}, elapsed={metadata['elapsed_seconds']:.1f}s, reload={reload_error}")
    del model, reloaded, matrix, valid, raw, result
    gc.collect()
    load_raw()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("step", choices=("check", "train"))
    args = parser.parse_args()
    if args.step == "check":
        result = preflight()
        log(f"Prior artifacts={result['original_artifacts_verified']}; old_gate=False; score_first_gate=True")
    else:
        train()
