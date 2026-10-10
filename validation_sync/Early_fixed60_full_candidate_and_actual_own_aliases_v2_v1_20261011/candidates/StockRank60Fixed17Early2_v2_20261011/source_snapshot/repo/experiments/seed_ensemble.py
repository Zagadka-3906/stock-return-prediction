"""Fixed equal-weight three-seed experiment; no production files are changed.

Selection uses only 2022/2023. The optional diagnose command is deliberately
separate and evaluates only the already selected mode in historical 2024.
"""
from __future__ import annotations

import argparse
import ast
import gc
import hashlib
import inspect
import json
import time
from functools import lru_cache
from pathlib import Path

import lightgbm as lgb
import numpy as np
import polars as pl
from scipy.stats import rankdata

from run import FEATURE_FILE, ROOT, feature_names, fit_model, fold_cutoff, to_matrix
from src.scoring import Panel, add_top_persistence, make_scores, postprocess_scores, score

OUT = ROOT / "experiments" / "seed_ensemble_eval"
SEEDS = (2026, 17, 43)
MODES = ("baseline", "full_signal", "top_only")
YEARS = (2022, 2023)
ROUNDS = 180
THREADS = 16
POSTPROCESS = {"alpha": .9, "bonus": .3, "restore_lower": True, "top_current_weight": 1.0}


def log(message: str) -> None:
    print(f"[{time.strftime('%H:%M:%S')}] {message}", flush=True)


@lru_cache(maxsize=64)
def _file_hash(path: str, size: int, mtime_ns: int) -> str:
    del size, mtime_ns
    digest = hashlib.sha256()
    with open(path, "rb") as stream:
        for block in iter(lambda: stream.read(8 * 1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def file_hash(path: Path) -> str:
    stat = path.stat()
    return _file_hash(str(path.resolve()), stat.st_size, stat.st_mtime_ns)


def params_for_seed(seed: int, threads: int = THREADS) -> dict:
    """Read production parameters, replacing only seed and requested threads."""
    tree = ast.parse(inspect.getsource(fit_model))
    assignment = next(node for node in ast.walk(tree) if isinstance(node, ast.Assign)
                      and any(isinstance(target, ast.Name) and target.id == "params" for target in node.targets))
    values = assignment.value
    for node in ast.walk(values):
        if isinstance(node, ast.Dict):
            node.values = [ast.Constant(threads) if isinstance(value, ast.Name) and value.id == "threads" else value
                           for value in node.values]
    result = ast.literal_eval(values)
    result["seed"] = seed
    return result


def fingerprint(year: int, seed: int, threads: int = THREADS) -> dict:
    paths = [FEATURE_FILE, ROOT / "data/feature_manifest.json", ROOT / "run.py",
             ROOT / "src/features.py", ROOT / "src/scoring.py", Path(__file__),
             ROOT / f"validation/fold_{year}.parquet", ROOT / f"models/fold_{year}.txt"]
    payload = {"year": year, "seed": seed, "rounds": ROUNDS,
               "training_cutoff_exclusive": fold_cutoff(year),
               "training_filter": "is_train & trade_date < cutoff & y_rank.not_null & price_valid",
               "params": params_for_seed(seed, threads), "features": feature_names(),
               "lightgbm_version": lgb.__version__,
               "source_sha256": {str(path.relative_to(ROOT)): file_hash(path) for path in paths}}
    payload["fingerprint_sha256"] = hashlib.sha256(json.dumps(payload, sort_keys=True).encode()).hexdigest()
    return payload


def load_panel(year: int) -> Panel:
    return Panel.from_frame(pl.read_parquet(ROOT / f"validation/fold_{year}.parquet"))


def _paths(year: int, seed: int) -> tuple[Path, Path, Path]:
    stem = f"seed_{seed}_{year}"
    return OUT / f"{stem}.txt", OUT / f"{stem}.parquet", OUT / f"{stem}.json"


def load_seed_raw(year: int, seed: int, panel: Panel) -> np.ndarray:
    if seed == 2026:
        return panel.frame.get_column("pred_raw").to_numpy()
    if seed not in SEEDS:
        raise ValueError(f"Seed {seed} was not predeclared")
    model_path, cache_path, meta_path = _paths(year, seed)
    metadata = json.loads(meta_path.read_text(encoding="utf-8"))
    expected = fingerprint(year, seed, int(metadata["params"]["num_threads"]))
    if metadata["fingerprint_sha256"] != expected["fingerprint_sha256"]:
        raise ValueError(f"Stale cache fingerprint for year={year}, seed={seed}")
    if metadata["model_sha256"] != file_hash(model_path) or metadata["cache_sha256"] != file_hash(cache_path):
        raise ValueError("Saved model or prediction cache hash mismatch")
    frame = pl.read_parquet(cache_path)
    if not frame.select("ts_code", "trade_date").equals(panel.frame.select("ts_code", "trade_date")):
        raise ValueError("Prediction keys/order differ from baseline panel")
    raw = frame.get_column("pred_raw").to_numpy()
    if raw.dtype != np.float32 or not np.isfinite(raw).all():
        raise ValueError("Seed prediction cache must be finite float32")
    return raw


def train(year: int, seed: int, threads: int = THREADS) -> None:
    if seed not in (17, 43):
        raise ValueError("Only the two predeclared new seeds may be trained")
    if threads != THREADS:
        raise ValueError("This fixed experiment requires 16 threads")
    OUT.mkdir(exist_ok=True)
    model_path, cache_path, meta_path = _paths(year, seed)
    expected = fingerprint(year, seed, threads)
    if all(path.exists() for path in (model_path, cache_path, meta_path)):
        try:
            load_seed_raw(year, seed, load_panel(year))
            log(f"Validated cache: year={year}, seed={seed}")
            return
        except (ValueError, KeyError, json.JSONDecodeError) as exc:
            log(f"Cache rejected ({exc}); rebuilding experimental outputs")
    features = expected["features"]
    if len(features) != 63:
        raise ValueError("The predeclared experiment requires the existing 63 features")
    cutoff = expected["training_cutoff_exclusive"]
    lazy = pl.scan_parquet(FEATURE_FILE)
    training_filter = pl.col("is_train") & (pl.col("trade_date") < cutoff) & pl.col("y_rank").is_not_null() & pl.col("price_valid")
    frame = lazy.filter(training_filter).select(features + ["y_rank", "trade_date"]).collect()
    x = to_matrix(frame, features)
    y = frame.get_column("y_rank").to_numpy().astype(np.float32)
    row_count = len(y)
    dates = frame.get_column("trade_date")
    first_date, last_date = int(dates.min()), int(dates.max())
    del frame, dates
    gc.collect()
    log(f"Training year={year}, seed={seed}, rows={row_count:,}, dates={first_date}..{last_date}, purge={cutoff}")
    start = time.monotonic()
    dataset = lgb.Dataset(x, label=y, feature_name=features, free_raw_data=True)
    model = lgb.train(expected["params"], dataset, num_boost_round=ROUNDS,
                      callbacks=[lgb.log_evaluation(period=60)])
    model_path.write_text(model.model_to_string(), encoding="utf-8")
    del dataset, x, y
    gc.collect()
    valid = lazy.filter(pl.col("is_train") & pl.col("trade_date").is_between(year * 10000 + 101, year * 10000 + 1231)).sort("trade_date", "ts_code").select(features + ["ts_code", "trade_date", "price_valid"]).collect()
    matrix = to_matrix(valid, features)
    raw = model.predict(matrix, num_threads=threads).astype(np.float32)
    raw[~valid.get_column("price_valid").to_numpy()] = -1e6
    reloaded = lgb.Booster(model_str=model_path.read_text(encoding="utf-8"))
    if reloaded.feature_name() != features:
        raise AssertionError("Saved model feature order mismatch")
    indices = np.linspace(0, len(raw) - 1, min(4096, len(raw)), dtype=int)
    checked = reloaded.predict(matrix[indices], num_threads=threads).astype(np.float32)
    checked[~valid.get_column("price_valid").to_numpy()[indices]] = -1e6
    error = float(np.max(np.abs(checked.astype(float) - raw[indices].astype(float))))
    if error != 0:
        raise AssertionError(f"Reloaded model differs: {error}")
    result = valid.select("ts_code", "trade_date").with_columns(pl.Series("pred_raw", raw))
    result.write_parquet(cache_path, compression="zstd")
    metadata = {**expected, "training_rows": row_count, "training_first_date": first_date,
                "training_last_date": last_date, "validation_rows": len(raw),
                "validation_first_date": int(valid.get_column("trade_date").min()),
                "validation_last_date": int(valid.get_column("trade_date").max()),
                "model_sha256": file_hash(model_path), "cache_sha256": file_hash(cache_path),
                "reload_check_rows": len(indices), "reload_max_abs_error": error,
                "elapsed_seconds": time.monotonic() - start}
    meta_path.write_text(json.dumps(metadata, indent=2, ensure_ascii=False), encoding="utf-8")
    log(f"Saved year={year}, seed={seed}; elapsed={metadata['elapsed_seconds']:.1f}s, reload error={error}")
    del model, reloaded, valid, matrix, raw, result
    gc.collect()


def make_prediction(panel: Panel, raw_by_seed: dict[int, np.ndarray], mode: str) -> np.ndarray:
    if mode not in MODES:
        raise ValueError(f"Unknown predeclared mode {mode}")
    baseline_raw = raw_by_seed[2026]
    base = postprocess_scores(panel, baseline_raw, **POSTPROCESS)
    if mode == "baseline":
        return base
    if set(raw_by_seed) != set(SEEDS):
        raise ValueError("Exactly seeds 2026, 17, 43 are required; individual seed selection is forbidden")
    if mode == "full_signal":
        ranked = [make_scores(panel, raw_by_seed[seed], 0.0) for seed in SEEDS]
        return postprocess_scores(panel, np.mean(ranked, axis=0), **POSTPROCESS)
    stable = add_top_persistence(panel, make_scores(panel, baseline_raw, .9), .3).reshape(panel.valid_price.shape)
    raws = {seed: np.asarray(raw_by_seed[seed], dtype=float).reshape(panel.valid_price.shape) for seed in SEEDS}
    out = base.reshape(panel.valid_price.shape).copy()
    for day in range(len(panel.dates)):
        valid = panel.valid_price[day] & np.isfinite(raws[2026][day])
        indices = np.flatnonzero(panel.up[day] == 0)
        if not len(indices) or not valid.any():
            continue
        n_top = max(len(indices) // 10, 1)
        top = indices[np.argsort(-stable[day, indices], kind="stable")[:n_top]]
        if not valid[top].all():
            continue
        protected = valid & (stable[day] >= stable[day, top].min())
        if np.count_nonzero(protected & (panel.up[day] == 0)) != n_top:
            continue
        if any(not np.isfinite(raws[seed][day, protected]).all() for seed in SEEDS):
            continue
        n_protected, n_valid = int(protected.sum()), int(valid.sum())
        average = np.mean([rankdata(raws[seed][day, protected], method="average") / n_protected for seed in SEEDS], axis=0)
        out[day, protected] = (n_valid - n_protected + rankdata(average, method="average")) / n_valid
    return out.reshape(-1)


def develop() -> dict:
    OUT.mkdir(exist_ok=True)
    result = {"selection_years": list(YEARS), "seeds": list(SEEDS), "rounds": ROUNDS,
              "weights": [1 / 3] * 3, "postprocess": POSTPROCESS,
              "selection_rule": "maximize_minimum_annual_score_2022_2023",
              "candidate_count": 3, "candidates": {mode: {"years": {}} for mode in MODES},
              "note": "No individual seed selection, no weight tuning; 2024 labels not used in development."}
    for year in YEARS:
        for seed in (17, 43):
            train(year, seed)
        panel = load_panel(year)
        raws = {seed: load_seed_raw(year, seed, panel) for seed in SEEDS}
        for mode in MODES:
            metrics, daily = score(panel, make_prediction(panel, raws, mode))
            result["candidates"][mode]["years"][str(year)] = metrics
            daily.write_csv(OUT / f"{mode}_{year}_daily.csv")
            log(f"year={year}, mode={mode}, score={metrics['final_score']:.9f}")
        del panel, raws
        gc.collect()
    for item in result["candidates"].values():
        item["minimum_annual_score"] = min(item["years"][str(year)]["final_score"] for year in YEARS)
    result["selected_mode"] = max(MODES, key=lambda mode: result["candidates"][mode]["minimum_annual_score"])
    result["artifacts_sha256"] = {str(path.relative_to(ROOT)): file_hash(path)
                                  for path in sorted(OUT.glob("seed_*")) if path.is_file()}
    result["experiment_source_sha256"] = file_hash(Path(__file__))
    (OUT / "development.json").write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    log(f"Selected mode on development years only: {result['selected_mode']}")
    return result


def diagnose() -> None:
    development_path = OUT / "development.json"
    selection_hash = file_hash(development_path)
    development = json.loads(development_path.read_text(encoding="utf-8"))
    mode = development["selected_mode"]
    if mode == "baseline":
        raise ValueError("Baseline selected; there is no new candidate to diagnose")
    for seed in (17, 43):
        train(2024, seed)
    panel = load_panel(2024)
    raws = {seed: load_seed_raw(2024, seed, panel) for seed in SEEDS}
    prediction = make_prediction(panel, raws, mode)
    metrics, daily = score(panel, prediction)
    baseline_metrics, _ = score(panel, make_prediction(panel, raws, "baseline"))
    daily.write_csv(OUT / "selected_2024_daily.csv")
    panel.frame.select("ts_code", "trade_date").with_columns(pl.Series("pred", prediction)).write_parquet(OUT / "selected_2024.parquet")
    result = {"selected_mode": mode, "development_sha256": selection_hash,
              "selected_metrics": metrics, "baseline_metrics": baseline_metrics,
              "historical_diagnostic_only": True, "no_candidate_reselection": True}
    (OUT / "diagnostic_2024.json").write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    log(f"Historical 2024 diagnostic, fixed mode={mode}: score={metrics['final_score']:.9f}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("step", choices=("develop", "diagnose"))
    args = parser.parse_args()
    if args.step == "develop":
        develop()
    else:
        diagnose()
