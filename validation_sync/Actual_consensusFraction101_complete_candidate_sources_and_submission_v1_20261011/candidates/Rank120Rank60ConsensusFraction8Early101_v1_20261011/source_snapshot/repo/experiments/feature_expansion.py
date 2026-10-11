"""Predeclared feature-group ablation with frozen training and postprocessing.

Development is confined to 2022/2023 and uses the unmodified official evaluator.
The explicit ``train`` command can train the locked candidate in 2024; this
module deliberately has no command that scores or selects against 2024 labels.
No production model, prediction, report, or feature file is overwritten.
"""
from __future__ import annotations

import argparse
import gc
import hashlib
import json
import time
from functools import lru_cache
from pathlib import Path

import lightgbm as lgb
import numpy as np
import polars as pl

from experiments import feature_expansion_features as added
from experiments.official_seed_development import official_score
from experiments.seed_ensemble import file_hash, params_for_seed
from run import FEATURE_FILE, MANIFEST, ROOT, feature_names, fold_cutoff, to_matrix
from src.scoring import Panel, postprocess_scores, score


OUT = ROOT / "experiments" / "feature_expansion_eval"
VARIANTS = {
    "baseline": (),
    "pv": ("price_volume",),
    "market": ("market_relative",),
    "both": ("price_volume", "market_relative"),
}
YEARS = (2022, 2023)
ROUNDS = 180
THREADS = 16
SEED = 2026
POSTPROCESS = {"alpha": .9, "bonus": .3, "restore_lower": True,
               "top_current_weight": 1.0}
KEYS = ["ts_code", "trade_date"]


def log(message: str) -> None:
    print(f"[{time.strftime('%H:%M:%S')}] {message}", flush=True)


def feature_artifacts() -> tuple[Path, Path]:
    """The builder and its checks are required, never created by training."""
    return added.OUT / "feature_manifest.json", added.OUT / "feature_tests.json"


def features_for_variant(variant: str) -> list[str]:
    if variant not in VARIANTS:
        raise ValueError(f"Unknown predeclared variant: {variant}")
    original = feature_names()
    if len(original) != 63 or set(added.GROUPS) != {"price_volume", "market_relative"}:
        raise ValueError("The fixed experiment expects 63 base features and two named groups")
    if any(len(added.GROUPS[group]) != 8 for group in added.GROUPS):
        raise ValueError("The fixed groups must each contain exactly eight features")
    declared = [name for group in ("price_volume", "market_relative")
                for name in added.GROUPS[group]]
    if declared != list(added.FEATURE_NAMES) or len(set(declared)) != 16:
        raise ValueError("Added feature declarations differ or are duplicated")
    if set(original) & set(declared):
        raise ValueError("Added features overlap production names")
    return original + [name for group in VARIANTS[variant] for name in added.GROUPS[group]]


@lru_cache(maxsize=4)
def _verify_added_keys(base_hash: str, added_hash: str, tests_hash: str) -> dict:
    del base_hash, added_hash, tests_hash
    base_keys = pl.scan_parquet(FEATURE_FILE).filter(pl.col("is_train")).select(KEYS).collect()
    extra = pl.scan_parquet(added.ADDED_FEATURE_FILE)
    schema = extra.collect_schema()
    if set(schema.names()) != set(KEYS + list(added.FEATURE_NAMES)):
        raise ValueError("Added parquet must contain only keys and the declared sixteen features")
    extra_keys = extra.select(KEYS).collect()
    for label, keys in (("production", base_keys), ("added", extra_keys)):
        if keys.select(pl.struct(KEYS).n_unique()).item() != len(keys):
            raise ValueError(f"Duplicate {label} feature keys")
        if any(keys.null_count().row(0)):
            raise ValueError(f"Null {label} feature keys")
    if len(base_keys) != len(extra_keys):
        raise ValueError("Added features do not cover the full training-period key set")
    matched = base_keys.with_row_index("_left_order").join(
        extra_keys.with_columns(pl.lit(True).alias("_matched")),
        on=KEYS, how="left", validate="1:1", maintain_order="left",
    )
    if (matched.get_column("_matched").null_count()
            or not matched.select(KEYS).equals(base_keys)
            or not np.array_equal(matched.get_column("_left_order").to_numpy(),
                                  np.arange(len(base_keys)))):
        raise AssertionError("Added-key 1:1 left join did not preserve original row alignment")
    result = {"training_period_key_rows": len(base_keys), "unique_keys": True,
              "complete_coverage": True, "left_join_row_order_verified": True}
    del base_keys, extra_keys, matched
    gc.collect()
    return result


def verify_feature_inputs() -> dict:
    manifest_path, tests_path = feature_artifacts()
    tests = json.loads(tests_path.read_text(encoding="utf-8"))
    if tests.get("status") != "passed" or tests.get("passed") is not True:
        raise ValueError("Feature-builder tests must have status='passed' before training")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    source_hash = file_hash(Path(added.__file__))
    if (tests["feature_module_sha256"] != source_hash
            or manifest["feature_module_sha256"] != source_hash):
        raise ValueError("Feature builder source differs from its tests or manifest")
    if manifest["features_sha256"] != file_hash(added.ADDED_FEATURE_FILE):
        raise ValueError("Added feature parquet differs from its manifest")
    source_path = Path(manifest["source_file"])
    if not source_path.is_absolute():
        source_path = ROOT / source_path
    if source_path.resolve() != (ROOT / "data" / "raw" / "训练集.csv").resolve():
        raise ValueError("The predeclared feature source must be the original training CSV")
    if manifest["source_sha256"] != file_hash(source_path):
        raise ValueError("Original training CSV changed since added-feature generation")
    if manifest["features"] != list(added.FEATURE_NAMES) or manifest["groups"] != added.GROUPS:
        raise ValueError("Manifest feature declarations differ from the executable builder")
    if (manifest.get("feature_count") != 16 or tests.get("feature_count") != 16
            or manifest.get("labels_used") is not False
            or manifest.get("test_file_read") is not False):
        raise ValueError("Manifest must attest sixteen label-free, training-only features")
    protocol = json.loads((OUT / "protocol.json").read_text(encoding="utf-8"))
    if (protocol["candidate_order"] != list(VARIANTS)
            or protocol["development_years"] != list(YEARS)
            or protocol["postprocess"] != POSTPROCESS
            or protocol.get("declared_before_model_training") is not True):
        raise ValueError("Predeclared experiment protocol differs from this runner")
    features_for_variant("both")
    return _verify_added_keys(file_hash(FEATURE_FILE), file_hash(added.ADDED_FEATURE_FILE),
                              file_hash(tests_path))


def fingerprint(year: int, variant: str) -> dict:
    if year not in (2022, 2023, 2024) or variant not in VARIANTS:
        raise ValueError("Only the predefined annual folds and variants are permitted")
    manifest_path, tests_path = feature_artifacts()
    paths = [FEATURE_FILE, MANIFEST, added.ADDED_FEATURE_FILE, manifest_path, tests_path,
             OUT / "protocol.json", ROOT / "data" / "raw" / "训练集.csv",
             ROOT / "run.py", ROOT / "src/features.py", ROOT / "src/scoring.py",
             Path(__file__), Path(added.__file__), ROOT / "experiments/seed_ensemble.py",
             ROOT / "experiments/official_seed_development.py", ROOT / "evaluate.py",
             ROOT / f"validation/fold_{year}.parquet", ROOT / f"models/fold_{year}.txt"]
    payload = {
        "year": year, "variant": variant, "groups": list(VARIANTS[variant]),
        "rounds": ROUNDS, "seed": SEED, "params": params_for_seed(SEED, THREADS),
        "features": features_for_variant(variant), "postprocess": POSTPROCESS,
        "training_cutoff_exclusive": fold_cutoff(year),
        "training_filter": "is_train & trade_date < cutoff & y_rank.not_null & price_valid",
        "purge_rule": "exclude the last trading date before the validation year; next-day target",
        "lightgbm_version": lgb.__version__,
        "source_sha256": {str(path.relative_to(ROOT)): file_hash(path) for path in paths},
    }
    payload["fingerprint_sha256"] = hashlib.sha256(
        json.dumps(payload, sort_keys=True).encode("utf-8")
    ).hexdigest()
    return payload


def load_panel(year: int) -> Panel:
    if year not in (2022, 2023, 2024):
        raise ValueError("Only the established annual folds are supported")
    return Panel.from_frame(pl.read_parquet(ROOT / f"validation/fold_{year}.parquet"))


def _paths(year: int, variant: str) -> tuple[Path, Path, Path]:
    stem = f"feature_{variant}_{year}"
    return OUT / f"{stem}.txt", OUT / f"{stem}.parquet", OUT / f"{stem}.json"


def load_raw(year: int, variant: str, panel: Panel) -> np.ndarray:
    if variant not in VARIANTS:
        raise ValueError(f"Unknown predeclared variant: {variant}")
    if not np.all((panel.dates >= year * 10000 + 101)
                  & (panel.dates <= year * 10000 + 1231)):
        raise ValueError("Panel dates do not match requested prediction year")
    if variant == "baseline":
        raw = panel.frame.get_column("pred_raw").to_numpy()
    else:
        model_path, cache_path, metadata_path = _paths(year, variant)
        metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
        if metadata["fingerprint_sha256"] != fingerprint(year, variant)["fingerprint_sha256"]:
            raise ValueError(f"Stale {variant}/{year} training-cache fingerprint")
        if (metadata["model_sha256"] != file_hash(model_path)
                or metadata["cache_sha256"] != file_hash(cache_path)):
            raise ValueError("Saved model or prediction cache was changed")
        frame = pl.read_parquet(cache_path)
        if frame.columns != KEYS + ["pred_raw"]:
            raise ValueError("Prediction cache has unexpected columns")
        if not frame.select(KEYS).equals(panel.frame.select(KEYS)):
            raise ValueError("Prediction keys/order differ from baseline panel")
        raw = frame.get_column("pred_raw").to_numpy()
    if raw.dtype != np.float32 or len(raw) != len(panel.frame) or not np.isfinite(raw).all():
        raise ValueError("Raw predictions must be finite aligned float32 values")
    if np.any(raw[~panel.valid_price.reshape(-1)] != np.float32(-1e6)):
        raise ValueError("Invalid-price rows must retain the production -1e6 sentinel")
    return raw


def _joined_frame(filter_expression: pl.Expr, columns: list[str],
                  added_columns: list[str], sort: bool = False) -> pl.DataFrame:
    base_columns = list(dict.fromkeys(KEYS + [name for name in columns if name not in added_columns]))
    base = pl.scan_parquet(FEATURE_FILE).filter(filter_expression).select(base_columns).collect()
    if sort:
        base = base.sort("trade_date", "ts_code")
    base = base.with_row_index("_left_order")
    # The 1:1 left join selects the exact base keys. Keep structural missing
    # features as null; no y-based imputation or row dropping is performed.
    extra = pl.scan_parquet(added.ADDED_FEATURE_FILE).select(KEYS + added_columns).collect()
    joined = base.join(extra.with_columns(pl.lit(True).alias("_matched")),
                       on=KEYS, how="left", validate="1:1", maintain_order="left")
    if (len(joined) != len(base) or joined.get_column("_matched").null_count()
            or not joined.select(KEYS).equals(base.select(KEYS))
            or not joined.get_column("_left_order").equals(base.get_column("_left_order"))):
        raise AssertionError("Model-frame feature join changed keys, row count, or order")
    return joined.drop("_left_order", "_matched")


def train(year: int, variant: str) -> None:
    if variant == "baseline" or variant not in VARIANTS:
        raise ValueError("The baseline is reused; train only pv, market, or both")
    if year not in (2022, 2023, 2024):
        raise ValueError("Only predeclared annual folds may be trained")
    if year == 2024:
        development = json.loads((OUT / "development.json").read_text(encoding="utf-8"))
        chosen = max(VARIANTS, key=lambda name: min(
            development["candidates"][name]["years"][str(y)]["final_score"] for y in YEARS))
        if (development["selection_years"] != list(YEARS)
                or development["selected_variant"] != chosen or variant != chosen):
            raise ValueError("2024 training is restricted to the already locked development winner")
        if development["experiment_source_sha256"] != file_hash(Path(__file__)):
            raise ValueError("Runner changed after development selection")
        for relative, expected_hash in development["artifacts_sha256"].items():
            if file_hash(ROOT / relative) != expected_hash:
                raise ValueError(f"Locked development artifact changed: {relative}")
    alignment = verify_feature_inputs()
    OUT.mkdir(exist_ok=True)
    expected = fingerprint(year, variant)
    model_path, cache_path, metadata_path = _paths(year, variant)
    if all(path.exists() for path in (model_path, cache_path, metadata_path)):
        try:
            load_raw(year, variant, load_panel(year))
            log(f"Validated cache: year={year}, variant={variant}")
            return
        except (ValueError, KeyError, json.JSONDecodeError) as exc:
            log(f"Experimental cache rejected ({exc}); rebuilding")
    features = expected["features"]
    added_columns = features[len(feature_names()):]
    cutoff = expected["training_cutoff_exclusive"]
    training_filter = (pl.col("is_train") & (pl.col("trade_date") < cutoff)
                       & pl.col("y_rank").is_not_null() & pl.col("price_valid"))
    frame = _joined_frame(training_filter, features + ["y_rank", "trade_date"], added_columns)
    x, y = to_matrix(frame, features), frame.get_column("y_rank").to_numpy().astype(np.float32)
    row_count = len(y)
    first_date = int(frame.get_column("trade_date").min())
    last_date = int(frame.get_column("trade_date").max())
    if last_date >= cutoff or not np.isfinite(y).all():
        raise AssertionError("Training purge or finite-target condition failed")
    del frame
    gc.collect()
    log(f"Training {year}/{variant}: {row_count:,} rows, {len(features)} features, "
        f"dates {first_date}..{last_date}, purge={cutoff}")
    start = time.monotonic()
    dataset = lgb.Dataset(x, label=y, feature_name=features, free_raw_data=True)
    model = lgb.train(expected["params"], dataset, num_boost_round=ROUNDS,
                      callbacks=[lgb.log_evaluation(period=60)])
    model_path.write_text(model.model_to_string(), encoding="utf-8")
    del dataset, x, y
    gc.collect()
    validation_filter = pl.col("is_train") & pl.col("trade_date").is_between(
        year * 10000 + 101, year * 10000 + 1231)
    valid = _joined_frame(validation_filter, features + KEYS + ["price_valid"],
                          added_columns, sort=True)
    matrix = to_matrix(valid, features)
    raw = model.predict(matrix, num_threads=THREADS).astype(np.float32)
    valid_price = valid.get_column("price_valid").to_numpy()
    raw[~valid_price] = -1e6
    if not np.isfinite(raw).all():
        raise AssertionError("Model emitted a nonfinite prediction")
    reloaded = lgb.Booster(model_str=model_path.read_text(encoding="utf-8"))
    if reloaded.feature_name() != features:
        raise AssertionError("Reloaded model changed the feature order")
    indices = np.linspace(0, len(raw) - 1, min(4096, len(raw)), dtype=int)
    checked = reloaded.predict(matrix[indices], num_threads=THREADS).astype(np.float32)
    checked[~valid_price[indices]] = -1e6
    error = float(np.max(np.abs(checked.astype(float) - raw[indices].astype(float))))
    if error != 0:
        raise AssertionError(f"Reloaded model prediction error: {error}")
    result = valid.select(KEYS).with_columns(pl.Series("pred_raw", raw))
    result.write_parquet(cache_path, compression="zstd")
    if fingerprint(year, variant)["fingerprint_sha256"] != expected["fingerprint_sha256"]:
        raise AssertionError("Experiment sources changed during training; cache is not valid")
    metadata = {
        **expected, "feature_alignment": alignment,
        "training_rows": row_count, "training_first_date": first_date,
        "training_last_date": last_date, "validation_rows": len(raw),
        "validation_first_date": int(valid.get_column("trade_date").min()),
        "validation_last_date": int(valid.get_column("trade_date").max()),
        "model_sha256": file_hash(model_path), "cache_sha256": file_hash(cache_path),
        "reload_check_rows": len(indices), "reload_max_abs_error": error,
        "feature_importance_gain": dict(zip(features, model.feature_importance("gain").tolist(), strict=True)),
        "elapsed_seconds": time.monotonic() - start,
    }
    metadata_path.write_text(json.dumps(metadata, ensure_ascii=False, indent=2), encoding="utf-8")
    log(f"Saved {year}/{variant}: elapsed {metadata['elapsed_seconds']:.1f}s, reload error={error}")
    del model, reloaded, valid, matrix, raw, result
    gc.collect()


def make_prediction(panel: Panel, raw: np.ndarray) -> np.ndarray:
    raw = np.asarray(raw)
    if raw.size != len(panel.frame) or not np.isfinite(raw).all():
        raise ValueError("Postprocessing requires one finite prediction per panel row")
    return postprocess_scores(panel, raw, **POSTPROCESS)


def develop() -> dict:
    alignment = verify_feature_inputs()
    OUT.mkdir(exist_ok=True)
    initial = fingerprint(YEARS[0], "baseline")
    result = {
        "selection_years": list(YEARS), "variants": {key: list(value) for key, value in VARIANTS.items()},
        "candidate_count": len(VARIANTS), "seed": SEED, "rounds": ROUNDS,
        "params": params_for_seed(SEED, THREADS), "postprocess": POSTPROCESS,
        "feature_alignment": alignment,
        "selection_rule": "maximize_minimum_official_annual_score_2022_2023; exact ties prefer baseline then declaration order",
        "tie_policy_note": "Unmodified evaluate.py; pandas default descending sort_values; daily evidence rebuilt from identical CSV bytes.",
        "candidates": {variant: {"groups": list(groups), "features": features_for_variant(variant),
                                  "years": {}} for variant, groups in VARIANTS.items()},
        "project_metrics": {variant: {} for variant in VARIANTS},
        "official_minus_project_score": {variant: {} for variant in VARIANTS},
        "note": "2024 labels are not read or scored in development. No model parameter or postprocessing search.",
    }
    for year in YEARS:
        panel = load_panel(year)
        for variant in VARIANTS:
            if variant != "baseline":
                train(year, variant)
            raw = load_raw(year, variant, panel)
            prediction = make_prediction(panel, raw)
            project_metrics, project_daily = score(panel, prediction)
            official_metrics, official_daily = official_score(panel, prediction, year)
            result["candidates"][variant]["years"][str(year)] = official_metrics
            result["project_metrics"][variant][str(year)] = project_metrics
            result["official_minus_project_score"][variant][str(year)] = (
                official_metrics["final_score"] - project_metrics["final_score"])
            official_daily.write_csv(OUT / f"official_{variant}_{year}_daily.csv")
            project_daily.write_csv(OUT / f"project_{variant}_{year}_daily.csv")
            log(f"OFFICIAL {year}/{variant}: {official_metrics['final_score']:.12f}")
            del raw, prediction, project_daily, official_daily
            gc.collect()
        del panel
        gc.collect()
    for candidate in result["candidates"].values():
        candidate["minimum_annual_score"] = min(
            candidate["years"][str(year)]["final_score"] for year in YEARS)
    result["selected_variant"] = max(
        VARIANTS, key=lambda variant: result["candidates"][variant]["minimum_annual_score"])
    if fingerprint(YEARS[0], "baseline")["fingerprint_sha256"] != initial["fingerprint_sha256"]:
        raise AssertionError("Experiment sources changed during development")
    artifacts = set()
    for year in YEARS:
        artifacts.add(ROOT / f"validation/fold_{year}.parquet")
        artifacts.add(ROOT / f"models/fold_{year}.txt")
        for variant in VARIANTS:
            if variant != "baseline":
                artifacts.update(_paths(year, variant))
            artifacts.add(OUT / f"official_{variant}_{year}_daily.csv")
            artifacts.add(OUT / f"project_{variant}_{year}_daily.csv")
    artifacts.update(ROOT / relative for relative in initial["source_sha256"])
    result["artifacts_sha256"] = {str(path.relative_to(ROOT)): file_hash(path)
                                  for path in sorted(artifacts)}
    result["experiment_source_sha256"] = file_hash(Path(__file__))
    (OUT / "development.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    log(f"Locked selection using 2022/2023 only: {result['selected_variant']}")
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("step", choices=("develop", "train"))
    parser.add_argument("--year", type=int, choices=(2022, 2023, 2024))
    parser.add_argument("--variant", choices=tuple(variant for variant in VARIANTS if variant != "baseline"))
    args = parser.parse_args()
    if args.step == "develop":
        if args.year is not None or args.variant is not None:
            parser.error("Development always evaluates the fixed full 2022/2023 protocol")
        develop()
    else:
        if args.year is None or args.variant is None:
            parser.error("train requires --year and --variant")
        train(args.year, args.variant)
