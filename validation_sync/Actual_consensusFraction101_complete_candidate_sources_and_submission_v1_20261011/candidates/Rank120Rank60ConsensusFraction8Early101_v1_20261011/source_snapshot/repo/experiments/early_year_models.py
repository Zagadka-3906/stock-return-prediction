"""Train four frozen historical-check models without reading evaluation labels.

The 2020/2021 folds extend evidence for an already locked 50/50 rank blend.
They are not candidate-selection folds. Only experimental outputs are written.
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

from experiments import feature_expansion, feature_expansion_features as added
from experiments.seed_ensemble import file_hash, params_for_seed
from run import FEATURE_FILE, MANIFEST, ROOT, feature_names, fold_cutoff, to_matrix
from src.scoring import Panel


OUT = ROOT / "experiments" / "early_year_eval"
YEARS = (2020, 2021)
VARIANTS = ("baseline", "market")
ROUNDS, SEED, THREADS = 180, 2026, 16
LOCKED_CONFIG = {"mode": "full_signal", "weight": 0.5}
KEYS = ["ts_code", "trade_date"]
EXPECTED = {2020: {"rows": 1694259, "cutoff": 20191231, "last_date": 20191230},
            2021: {"rows": 2594048, "cutoff": 20201231, "last_date": 20201230}}


def log(message: str) -> None:
    print(f"[{time.strftime('%H:%M:%S')}] {message}", flush=True)


def check_protocol() -> dict:
    protocol = json.loads((OUT / "protocol.json").read_text(encoding="utf-8"))
    if (protocol.get("years") != list(YEARS)
            or protocol.get("variants") != list(VARIANTS)
            or protocol.get("locked_config") != LOCKED_CONFIG
            or protocol.get("rounds") != ROUNDS
            or protocol.get("seed") != SEED
            or protocol.get("threads") != THREADS
            or protocol.get("declared_before_model_training") is not True):
        raise ValueError("Historical-check protocol differs from the frozen design")
    for relative, expected_hash in protocol.get("source_sha256", {}).items():
        if file_hash(ROOT / relative) != expected_hash:
            raise ValueError(f"Protocol-locked source changed: {relative}")
    return protocol


def features_for_variant(variant: str) -> list[str]:
    if variant not in VARIANTS:
        raise ValueError("Only baseline and market models are predeclared")
    original = feature_names()
    market = list(added.GROUPS["market_relative"])
    if len(original) != 63 or len(market) != 8 or set(original) & set(market):
        raise ValueError("Frozen 63 + 8 feature definitions changed")
    return original + (market if variant == "market" else [])


def _locked_sources() -> dict[str, str]:
    """Verify the prior choice and retain its complete artifact provenance."""
    protocol = check_protocol()
    previous_out = ROOT / "experiments" / "market_blend_eval"
    development_path = previous_out / "development.json"
    development = json.loads(development_path.read_text(encoding="utf-8"))
    if (development["selection_years"] != [2022, 2023]
            or development["selected_key"] != "full_signal_w0.5"
            or development["selected_config"] != LOCKED_CONFIG
            or development["experiment_source_sha256"]
            != file_hash(ROOT / "experiments" / "market_blend.py")):
        raise ValueError("The previous development choice/source is not the locked 50/50 blend")
    sources = dict(development["artifacts_sha256"])
    for filename in ("development_audit.json", "diagnostic_2024.json", "decision.json"):
        record = json.loads((previous_out / filename).read_text(encoding="utf-8"))
        if (record["development_sha256"] != file_hash(development_path)
                or record["selected_key"] != "full_signal_w0.5"
                or record["selected_config"] != LOCKED_CONFIG):
            raise ValueError(f"Prior locked evidence changed: {filename}")
        if "audit_source_sha256" in record:
            audit_path = ROOT / "experiments" / "audit_market_blend.py"
            if file_hash(audit_path) != record["audit_source_sha256"]:
                raise ValueError("Prior market-blend audit source changed")
            sources[str(audit_path.relative_to(ROOT))] = record["audit_source_sha256"]
            sources.update(record["audit_dependencies_sha256"])
    for relative, expected_hash in sources.items():
        if file_hash(ROOT / relative) != expected_hash:
            raise ValueError(f"Prior locked source/artifact changed: {relative}")
    paths = [FEATURE_FILE, MANIFEST, added.ADDED_FEATURE_FILE,
             added.OUT / "feature_manifest.json", added.OUT / "feature_tests.json",
             added.OUT / "real_prefix_audit.json", added.OUT / "real_prefix_model_audit.json",
             feature_expansion.OUT / "protocol.json", ROOT / "data" / "raw" / "训练集.csv",
             ROOT / "run.py", ROOT / "src/features.py", ROOT / "src/scoring.py",
             Path(__file__), Path(added.__file__), Path(feature_expansion.__file__),
             ROOT / "experiments/seed_ensemble.py", ROOT / "experiments/market_blend.py",
             ROOT / "experiments/cached_recheck.py",
             ROOT / "experiments/official_seed_development.py", ROOT / "evaluate.py",
             OUT / "protocol.json", development_path,
             *(previous_out / name for name in
               ("development_audit.json", "diagnostic_2024.json", "decision.json"))]
    paths.extend(ROOT / relative for relative in protocol.get("source_sha256", {}))
    sources.update({str(path.relative_to(ROOT)): file_hash(path) for path in paths})
    return dict(sorted(sources.items()))


def fingerprint(year: int, variant: str) -> dict:
    if year not in YEARS or variant not in VARIANTS:
        raise ValueError("Only the four predeclared historical models are supported")
    cutoff = fold_cutoff(year)
    if cutoff != EXPECTED[year]["cutoff"]:
        raise ValueError("Historical training purge date changed")
    payload = {"year": year, "variant": variant, "rounds": ROUNDS,
               "seed": SEED, "params": params_for_seed(SEED, THREADS),
               "features": features_for_variant(variant), "locked_config": LOCKED_CONFIG,
               "training_cutoff_exclusive": cutoff,
               "training_filter": "is_train & trade_date < cutoff & y_rank.not_null & price_valid",
               "purge_rule": "exclude last trading date before validation; no future training",
               "validation_labels_loaded": False, "candidate_selection_performed": False,
               "lightgbm_version": lgb.__version__, "numpy_version": np.__version__,
               "polars_version": pl.__version__, "source_sha256": _locked_sources()}
    payload["fingerprint_sha256"] = hashlib.sha256(
        json.dumps(payload, sort_keys=True).encode("utf-8")).hexdigest()
    return payload


def _paths(year: int, variant: str) -> tuple[Path, Path, Path]:
    stem = f"early_{variant}_{year}"
    return OUT / f"{stem}.txt", OUT / f"{stem}.parquet", OUT / f"{stem}.json"


def _panel_base(year: int) -> pl.DataFrame:
    if year not in YEARS:
        raise ValueError("Only the two fixed historical years are supported")
    return (pl.scan_parquet(FEATURE_FILE)
            .filter(pl.col("is_train") & pl.col("trade_date").is_between(
                year * 10000 + 101, year * 10000 + 1231))
            .select(*KEYS, "flag_limit_up", "price_valid")
            .sort("trade_date", "ts_code").collect()
            .with_columns(pl.lit(None, dtype=pl.Float64).alias("y_ret_1d")))


def load_raw(year: int, variant: str, panel: Panel | None = None) -> np.ndarray:
    model_path, cache_path, meta_path = _paths(year, variant)
    metadata = json.loads(meta_path.read_text(encoding="utf-8"))
    expected = fingerprint(year, variant)
    if metadata["fingerprint_sha256"] != expected["fingerprint_sha256"]:
        raise ValueError(f"Stale historical-model fingerprint: {year}/{variant}")
    if any(metadata.get(key) != value for key, value in expected.items()):
        raise ValueError("Historical-model metadata differs from its signed payload")
    if (metadata["model_sha256"] != file_hash(model_path)
            or metadata["cache_sha256"] != file_hash(cache_path)):
        raise ValueError("Saved historical model or prediction cache was changed")
    frame = pl.read_parquet(cache_path)
    base = _panel_base(year) if panel is None else panel.frame
    if (frame.columns != KEYS + ["pred_raw"]
            or not frame.select(KEYS).equals(base.select(KEYS))
            or not frame.select(KEYS).equals(frame.sort("trade_date", "ts_code").select(KEYS))
            or frame.select(pl.struct(KEYS).n_unique()).item() != len(frame)):
        raise ValueError("Historical prediction keys, uniqueness or ordering differ")
    if (metadata["training_rows"] != EXPECTED[year]["rows"]
            or metadata["training_last_date"] != EXPECTED[year]["last_date"]
            or metadata["validation_rows"] != len(frame)
            or metadata["reload_max_abs_error"] != 0
            or metadata["reload_check_rows"] != min(4096, len(frame))):
        raise ValueError("Saved historical training-boundary or reload checks differ")
    raw = frame.get_column("pred_raw").to_numpy()
    valid = base.get_column("price_valid").to_numpy()
    if (raw.dtype != np.float32 or not np.isfinite(raw).all()
            or np.any(raw[~valid] != np.float32(-1e6))):
        raise ValueError("Historical raw predictions must be finite Float32 with invalid-price sentinel")
    return raw


def load_panel(year: int) -> Panel:
    base = _panel_base(year)
    raw = load_raw(year, "baseline")
    return Panel.from_frame(base.with_columns(pl.Series("pred_raw", raw)))


def load_market_raw(year: int, panel: Panel) -> np.ndarray:
    return load_raw(year, "market", panel)


def train(year: int, variant: str) -> None:
    alignment = feature_expansion.verify_feature_inputs()
    expected = fingerprint(year, variant)
    OUT.mkdir(parents=True, exist_ok=True)
    model_path, cache_path, meta_path = _paths(year, variant)
    if any(path.exists() for path in (model_path, cache_path, meta_path)):
        if not all(path.exists() for path in (model_path, cache_path, meta_path)):
            raise ValueError("Incomplete historical cache exists; preserve it for manual inspection")
        load_raw(year, variant)
        log(f"Validated frozen cache {year}/{variant}")
        return
    features = expected["features"]
    added_columns = features[63:]
    cutoff = expected["training_cutoff_exclusive"]
    mask = (pl.col("is_train") & (pl.col("trade_date") < cutoff)
            & pl.col("y_rank").is_not_null() & pl.col("price_valid"))
    frame = feature_expansion._joined_frame(mask, features + ["y_rank", "trade_date"], added_columns)
    x = to_matrix(frame, features)
    y = frame.get_column("y_rank").to_numpy().astype(np.float32)
    rows = len(y)
    first_date, last_date = int(frame["trade_date"].min()), int(frame["trade_date"].max())
    if (rows != EXPECTED[year]["rows"] or last_date != EXPECTED[year]["last_date"]
            or last_date >= cutoff or not np.isfinite(y).all()):
        raise AssertionError("Historical training rows, date boundary or finite targets differ")
    del frame
    gc.collect()
    log(f"Training {year}/{variant}: rows={rows:,}, features={len(features)}, "
        f"dates={first_date}..{last_date}, excluded={cutoff}")
    start = time.monotonic()
    dataset = lgb.Dataset(x, label=y, feature_name=features, free_raw_data=True)
    model = lgb.train(expected["params"], dataset, num_boost_round=ROUNDS)
    model_path.write_text(model.model_to_string(), encoding="utf-8")
    del dataset, x, y
    gc.collect()
    validation_mask = pl.col("is_train") & pl.col("trade_date").is_between(
        year * 10000 + 101, year * 10000 + 1231)
    valid = feature_expansion._joined_frame(validation_mask, features + KEYS + ["price_valid"],
                                            added_columns, sort=True)
    matrix = to_matrix(valid, features)
    raw = model.predict(matrix, num_threads=THREADS).astype(np.float32)
    valid_price = valid["price_valid"].to_numpy()
    raw[~valid_price] = -1e6
    if not np.isfinite(raw).all():
        raise AssertionError("Historical model emitted nonfinite predictions")
    reloaded = lgb.Booster(model_str=model_path.read_text(encoding="utf-8"))
    if reloaded.feature_name() != features:
        raise AssertionError("Historical model feature order changed on reload")
    indices = np.linspace(0, len(raw) - 1, min(4096, len(raw)), dtype=int)
    checked = reloaded.predict(matrix[indices], num_threads=THREADS).astype(np.float32)
    checked[~valid_price[indices]] = -1e6
    error = float(np.max(np.abs(checked.astype(float) - raw[indices].astype(float))))
    if error != 0:
        raise AssertionError(f"Reloaded historical model differs by {error}")
    result = valid.select(KEYS).with_columns(pl.Series("pred_raw", raw))
    if (result.select(pl.struct(KEYS).n_unique()).item() != len(result)
            or not result.select(KEYS).equals(_panel_base(year).select(KEYS))):
        raise AssertionError("Historical validation cache changed row coverage or keys")
    result.write_parquet(cache_path, compression="zstd")
    if fingerprint(year, variant) != expected:
        raise AssertionError("A frozen source changed during historical model training")
    metadata = {**expected, "training_rows": rows, "training_first_date": first_date,
                "training_last_date": last_date, "validation_rows": len(raw),
                "validation_first_date": int(valid["trade_date"].min()),
                "validation_last_date": int(valid["trade_date"].max()),
                "validation_days": valid["trade_date"].n_unique(),
                "feature_input_alignment": alignment,
                "model_sha256": file_hash(model_path), "cache_sha256": file_hash(cache_path),
                "reload_check_rows": len(indices), "reload_max_abs_error": error,
                "elapsed_seconds": time.monotonic() - start}
    meta_path.write_text(json.dumps(metadata, ensure_ascii=False, indent=2), encoding="utf-8")
    log(f"Saved {year}/{variant}: rows={len(raw):,}, elapsed={metadata['elapsed_seconds']:.1f}s, reload={error}")
    del model, reloaded, matrix, valid, raw, result
    gc.collect()
    load_raw(year, variant)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("step", choices=("train",))
    parser.parse_args()
    for requested_year in YEARS:
        for requested_variant in VARIANTS:
            train(requested_year, requested_variant)
