"""Portable training and prediction for the 67-feature XGBoost rank ensemble."""
from __future__ import annotations

import gc
import json
from pathlib import Path

import lightgbm as lgb
import numpy as np
import polars as pl
import xgboost as xgb
from scipy.stats import rankdata

from src.peer_features import add_columns
from src.pooled_target import _target_with_stats
from src.postprocessing import make_prediction
from src.scoring import Panel

ROOT = Path(__file__).resolve().parents[1]
KEYS = ["ts_code", "trade_date"]


def configuration(path: Path | None = None) -> dict:
    config = json.loads((path or ROOT / "config/ensemble.json").read_text(encoding="utf-8"))
    schema = json.loads((ROOT / "config/features.json").read_text(encoding="utf-8"))
    config["base_features"] = schema["features"]
    config["features"] = schema["features"] + config["peer_features"]
    if len(config["features"]) != 67 or len(set(config["seeds"])) != len(config["seeds"]):
        raise ValueError("Expected 67 ordered features and unique ensemble seeds")
    expected = {"alpha": 0.9, "bonus": 0.3, "restore_lower": True, "top_current_weight": 1.0}
    if config["postprocess"] != expected:
        raise ValueError("The extracted postprocessor implements the recorded fixed configuration")
    return config


def ensure_peer_cache(config: dict) -> Path:
    destination = ROOT / config["feature_cache"]
    if not destination.is_file():
        base = ROOT / "data/features.parquet"
        if not base.is_file():
            raise FileNotFoundError("Build base features first: python run.py features")
        print("正在从基础面板生成同伴特征", flush=True)
        frame = pl.read_parquet(base).sort("ts_code", "trade_date")
        destination.parent.mkdir(parents=True, exist_ok=True)
        add_columns(frame).write_parquet(destination, compression="zstd")
    columns = pl.scan_parquet(destination).collect_schema().names()
    needed = config["features"] + KEYS + ["row_id", "is_train", "price_valid", "flag_limit_up"]
    if missing := set(needed) - set(columns):
        raise ValueError(f"Feature cache is missing columns: {sorted(missing)}")
    return destination


def rank_average(raws: list[np.ndarray], valid: np.ndarray, days: int, codes: int) -> np.ndarray:
    if not raws or valid.size != days * codes or any(raw.size != valid.size for raw in raws):
        raise ValueError("Member predictions must align with the rectangular daily panel")
    combined = np.full(valid.size, -10.0, dtype=np.float64)
    for day in range(days):
        low, high = day * codes, (day + 1) * codes
        keep = valid[low:high]
        for raw in raws:
            keep = keep & np.isfinite(raw[low:high])
        rows = low + np.flatnonzero(keep)
        if rows.size:
            accumulated = np.zeros(rows.size, dtype=np.float64)
            for raw in raws:
                accumulated += rankdata(raw[rows], method="average") / rows.size
            combined[rows] = accumulated / len(raws)
    return combined


def predict(config: dict, output: Path, threads: int = 16, model_dir: Path | None = None) -> dict:
    directory = model_dir or ROOT / config["model_directory"]
    members = [directory / f"xgboost_seed{seed}.ubj" for seed in config["seeds"]]
    auxiliary_path = directory / config["auxiliary"]["file"]
    if missing := [str(path) for path in members + [auxiliary_path] if not path.is_file()]:
        raise FileNotFoundError(f"Train or supply the model files first: {missing[:3]}")
    # Prediction selects no return labels, including retrospectively available labels.
    names = list(dict.fromkeys(KEYS + ["row_id", "flag_limit_up", "price_valid"] + config["features"]))
    frame = (pl.scan_parquet(ensure_peer_cache(config)).filter(~pl.col("is_train"))
             .select(names).sort("trade_date", "ts_code").collect())
    days, codes = frame["trade_date"].n_unique(), frame["ts_code"].n_unique()
    if len(frame) != days * codes:
        raise ValueError("Prediction requires a complete rectangular daily panel")
    valid = frame["price_valid"].to_numpy()
    matrix = np.ascontiguousarray(frame.select(config["features"]).to_numpy(), dtype=np.float32)
    raws = []
    for seed, path in zip(config["seeds"], members, strict=True):
        model = xgb.XGBRegressor(n_jobs=threads)
        model.load_model(path)
        if model.get_booster().num_features() != len(config["features"]):
            raise ValueError(f"Model feature count differs: {path.name}")
        raw = model.predict(matrix).astype(np.float64)
        if not np.isfinite(raw).all():
            raise ValueError(f"Nonfinite predictions: seed {seed}")
        raw[~valid] = -1e6
        raws.append(raw)
    averaged = rank_average(raws, valid, days, codes)
    auxiliary = lgb.Booster(model_str=auxiliary_path.read_text(encoding="utf-8"))
    aux_matrix = np.ascontiguousarray(frame.select(config["base_features"]).to_numpy(), dtype=np.float32)
    aux_raw = auxiliary.predict(aux_matrix, num_threads=threads).astype(np.float32)
    aux_raw[~valid] = -1e6
    panel_frame = frame.select(KEYS + ["row_id", "flag_limit_up", "price_valid"]).with_columns(
        pl.lit(None, dtype=pl.Float64).alias("y_ret_1d"), pl.Series("pred_raw", averaged))
    panel = Panel.from_frame(panel_frame)
    ranked = make_prediction(panel, aux_raw, config["auxiliary"]["mode"], config["auxiliary"]["weight"])
    transform = config["prediction"]
    values = np.where(ranked < -1, transform["invalid_value"],
                      transform["rank_affine_scale"] * (ranked - transform["rank_center"]))
    result = panel.frame.with_columns(pl.Series("pred", values)).sort("row_id").select(KEYS + ["pred"])
    from run import verify_submission
    output.parent.mkdir(parents=True, exist_ok=True)
    result.write_csv(output, float_precision=transform["float_precision"])
    verify_submission(output)
    return {"rows": len(result), "days": days, "stocks": codes, "members": len(members), "output": str(output)}


def train(config: dict, threads: int = 16, device: str = "cpu", retrain: bool = False) -> None:
    directory = ROOT / config["model_directory"]
    directory.mkdir(parents=True, exist_ok=True)
    missing_seeds = [seed for seed in config["seeds"]
                     if retrain or not (directory / f"xgboost_seed{seed}.ubj").is_file()]
    if missing_seeds:
        frame = (pl.scan_parquet(ensure_peer_cache(config))
                 .filter(pl.col("is_train") & pl.col("y_rank").is_not_null() & pl.col("price_valid"))
                 .select(KEYS + config["features"] + ["y_rank"]).sort("trade_date", "ts_code").collect())
        matrix = np.ascontiguousarray(frame.select(config["features"]).to_numpy(), dtype=np.float32)
        labels = frame["y_rank"].to_numpy().astype(np.float32)
        del frame
        gc.collect()
        for seed in missing_seeds:
            params = dict(config["xgboost_params"], n_jobs=threads)
            model = xgb.XGBRegressor(seed=seed, device=device, **params)
            print(f"正在训练随机种子 {seed}，训练样本 {len(labels):,} 行", flush=True)
            model.fit(matrix, labels)
            model.save_model(directory / f"xgboost_seed{seed}.ubj")
            del model
            gc.collect()
        del matrix, labels
        gc.collect()
    auxiliary_path = directory / config["auxiliary"]["file"]
    if retrain or not auxiliary_path.is_file():
        from run import fit_model
        frame = (pl.scan_parquet(ROOT / "data/features.parquet")
                 .filter(pl.col("is_train") & pl.col("y_rank").is_not_null() & pl.col("price_valid"))
                 .select(KEYS + config["base_features"] + ["y_ret_1d"]).collect())
        target, _ = _target_with_stats(frame["trade_date"].to_numpy(), frame["y_ret_1d"].to_numpy())
        matrix = np.ascontiguousarray(frame.select(config["base_features"]).to_numpy(), dtype=np.float32)
        print("正在训练 pooled RMS 收益辅助模型", flush=True)
        model = fit_model(matrix, target, config["base_features"], config["auxiliary"]["rounds"], threads)
        auxiliary_path.write_text(model.model_to_string(), encoding="utf-8")
    print(f"模型已就绪：{directory}", flush=True)
