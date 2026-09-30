"""Final sweep, wave 2: four mechanisms not covered by any earlier suite.

Each candidate attacks a different measured weakness:

  W2a  smoothed-label backbone. The released alpha=0.9 EMA costs about 7% of raw
       IC to buy a 20x turnover reduction. If the backbone is trained on a
       causally smoothed label, persistence is learned instead of imposed, so
       less post-hoc smoothing should be needed. Two variants: released alpha
       and a deliberately lower alpha that exploits the built-in persistence.
  W2b  post-processing ensemble. 2022 prefers less smoothing and 2023 more, so
       rank-averaging the finished pipelines at alpha 0.85/0.90/0.95 hedges the
       regime dependence that killed every single-alpha candidate.
  W2c  two-day-horizon backbone. Averaging the 1-day and 2-day rank targets
       smooths the signal at the label level without touching the postprocessor.
  W2d  pruned-feature backbone. Drop the twenty lowest split-gain features to
       reduce noise dimensions; pruning was never ablated, only additions were.

All candidates run through the released post-processing and pooled blend
unchanged unless the candidate definition states otherwise. Standing three-year
strict gate; mean and maximin reported for every candidate.
"""
from __future__ import annotations

import argparse
import json
import time
from pathlib import Path

import lightgbm as lgb
import numpy as np
import polars as pl

from run import FEATURE_FILE, ROOT, feature_names, fold_cutoff, to_matrix
from experiments.bonus_extension import (BASE_BONUS, BLEND_WEIGHT, file_hash, load_auxiliary,
                                         load_panel, release_scores)
from experiments.final_sweep import blend_top_only, retention_scores, RELEASED
from experiments.official_seed_development import official_score
from experiments.sequence_model import load_panel as load_seq_panel

OUT = ROOT / "experiments" / "final_sweep_eval"
KEYS = ["ts_code", "trade_date"]
ROUNDS, SEED = 180, 2026
BASE_PARAMS = {"objective": "regression", "metric": "l2", "learning_rate": 0.05, "num_leaves": 31,
               "min_data_in_leaf": 300, "feature_fraction": 0.85, "bagging_fraction": 0.85,
               "bagging_freq": 1, "lambda_l2": 5.0, "max_bin": 127, "num_threads": 16,
               "seed": SEED, "verbosity": -1}
SMOOTH_ALPHA = 0.9
PRUNE_COUNT = 20
ENSEMBLE_ALPHAS = (0.85, 0.90, 0.95)
DEVELOPMENT_YEARS = (2022, 2023)
NUMERIC_TOLERANCE = 1e-12

CANDIDATES = [
    {"key": "W2a_smoothed_label_alpha0.90", "variant": "smoothed", "alpha": 0.90},
    {"key": "W2a_smoothed_label_alpha0.70", "variant": "smoothed", "alpha": 0.70},
    {"key": "W2b_postprocess_ensemble", "variant": "pp_ensemble", "alpha": None},
    {"key": "W2c_two_day_horizon", "variant": "two_day", "alpha": 0.90},
    {"key": "W2d_pruned_features", "variant": "pruned", "alpha": 0.90},
]

PROTOCOL = {
    "experiment": "final_sweep_wave2_mechanisms",
    "candidates": CANDIDATES,
    "postprocess": "released stack (alpha per candidate, bonus 0.3, protected restoration with "
                   "top_current_weight 1.0) then the 25% top-only pooled blend",
    "scorer": "Unmodified evaluate.py via official_score",
    "development_years": list(DEVELOPMENT_YEARS),
    "diagnostic_year": 2024,
    "adoption_gate": "strict improvement over the released composite in 2022 AND 2023, then 2024",
    "baseline_anchor": "released backbone raw through the same code path reproduces the released "
                       "composite to 1e-12 in every scored year",
    "smoothed_label": "per stock, s_t = y_rank_t when s is unset or y_rank_t missing, else "
                      "(1-0.9)*y_rank_t + 0.9*s_{t-1}; strictly causal, no future label enters",
    "two_day_label": "0.5*rank(y_ret_1d) + 0.5*rank(close(t+2)/close(t+1)-1); the final two "
                     "training days are purged because the 2-day label touches t+2",
    "pruned_features": "the twenty lowest total split-gain features from "
                       "validation/feature_importance.csv of the released full model",
    "prohibited_after_results": [
        "Retuning alpha beyond the two pre-declared smoothed variants",
        "Adding ensemble members or weights",
        "Changing the prune count or the horizon mix",
        "Re-scoring years or modifying the release",
    ],
    "limitations": [
        "2022-2024 are repeatedly examined historical years.",
        "Wave-2 candidates reuse the released pooled auxiliary, which was fitted against the old "
        "backbone; a genuinely better backbone would deserve a refitted auxiliary, but refitting is "
        "out of scope for a sweep.",
    ],
}


def log(message: str) -> None:
    print(f"[{time.strftime('%H:%M:%S')}] {message}", flush=True)


def flat_indices(frame: pl.DataFrame, dates_arr: np.ndarray, codes_arr: np.ndarray,
                 n_codes: int) -> np.ndarray:
    """Vectorized map from frame rows onto the rectangular (day, stock) panel."""
    d = frame["trade_date"].to_numpy()
    c = frame["ts_code"].to_numpy()
    row = np.searchsorted(dates_arr, d)
    col = np.searchsorted(codes_arr, c)
    if not (np.all(dates_arr[row] == d) and np.all(codes_arr[col] == c)):
        raise AssertionError("Frame rows do not map onto the rectangular panel")
    return row * n_codes + col


def smoothed_labels(y: np.ndarray) -> np.ndarray:
    """Causal per-stock EMA of the daily rank label; missing days carry the state."""
    out = np.full_like(y, np.nan)
    state = np.full(y.shape[1], np.nan)
    for row in range(y.shape[0]):
        current = y[row]
        finite = np.isfinite(current)
        has_state = np.isfinite(state)
        state = np.where(finite & has_state,
                         (1 - SMOOTH_ALPHA) * current + SMOOTH_ALPHA * state, state)
        state = np.where(finite & ~has_state, current, state)
        out[row] = state
    return out


def write_protocol() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / "protocol_wave2.json"
    if path.exists():
        raise SystemExit("Wave-2 protocol already frozen")
    payload = {**PROTOCOL, "frozen_at_local": time.strftime("%Y-%m-%dT%H:%M:%S"),
               "source_sha256": file_hash(Path(__file__))}
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    log("Froze wave-2 protocol before any training")


def verify_protocol() -> dict:
    path = OUT / "protocol_extra.json"
    protocol = json.loads((OUT / "protocol_wave2.json").read_text(encoding="utf-8"))
    if protocol["source_sha256"] != file_hash(Path(__file__)):
        raise SystemExit("final_sweep_wave2.py changed after its protocol was frozen; stop")
    return protocol


def train() -> None:
    protocol = verify_protocol()
    result_path = OUT / "training_wave2.json"
    if result_path.exists():
        raise SystemExit("Wave-2 training already recorded; preserving it")
    features = feature_names()
    importance = pl.read_csv(ROOT / "validation/feature_importance.csv")
    dropped = set(importance.sort("gain").head(PRUNE_COUNT)["feature"].to_list())
    pruned_features = [f for f in features if f not in dropped]
    log(f"Pruning {len(dropped)} features: {sorted(dropped)[:6]}...")
    dates, codes, x_panel, y_panel, valid_panel, _ = load_seq_panel(features, 2024)
    smooth = smoothed_labels(y_panel)
    dates_arr, codes_arr = np.asarray(dates), np.asarray(codes)
    n_codes = len(codes)
    flat = y_panel.reshape(-1)
    lazy = pl.scan_parquet(FEATURE_FILE)
    record = {"generated_at_local": time.strftime("%Y-%m-%dT%H:%M:%S"),
              "protocol_sha256": file_hash(OUT / "protocol_wave2.json"),
              "pruned_features": sorted(dropped), "candidates": {}}
    for candidate in CANDIDATES:
        variant = candidate["variant"]
        if variant == "pp_ensemble":
            record["candidates"][candidate["key"]] = {"note": "no retraining; reuses released "
                                                               "backbone caches at three alphas"}
            continue
        record["candidates"][candidate["key"]] = {}
        use_features = pruned_features if variant == "pruned" else features
        for year in DEVELOPMENT_YEARS + (2024,):
            cutoff = fold_cutoff(year)
            frame = (lazy.filter(pl.col("is_train") & (pl.col("trade_date") < cutoff)
                                 & pl.col("price_valid"))
                     .select(KEYS + use_features + ["y_rank"])
                     .sort("trade_date", "ts_code").collect())
            label = flat[flat_indices(frame, dates_arr, codes_arr, n_codes)].astype(np.float32)
            if variant == "smoothed":
                idx = flat_indices(frame, dates_arr, codes_arr, n_codes)
                label = smooth.reshape(-1)[idx].astype(np.float32)
                label[np.isnan(flat[idx])] = np.nan
            if variant == "two_day":
                idx = flat_indices(frame, dates_arr, codes_arr, n_codes)
                row_idx = idx // n_codes
                y_next = np.where(row_idx + 1 < len(dates),
                                  flat[np.minimum(idx + n_codes, flat.size - 1)], np.nan)
                label = (0.5 * flat[idx] + 0.5 * y_next).astype(np.float32)
                last_two = sorted(frame["trade_date"].unique().to_list())[-2:]
                keep_days = ~frame["trade_date"].is_in(last_two).to_numpy()
                frame = frame.filter(~pl.col("trade_date").is_in(last_two))
                label = label[keep_days]
            keep = np.isfinite(label)
            matrix = to_matrix(frame, use_features)[keep]
            label = label[keep]
            model = lgb.train(BASE_PARAMS, lgb.Dataset(matrix, label=label,
                                                       feature_name=use_features, free_raw_data=True),
                              num_boost_round=ROUNDS)
            valid_frame = (lazy.filter(pl.col("trade_date").is_between(
                year * 10000 + 101, year * 10000 + 1231))
                .select(KEYS + use_features + ["price_valid"]).sort("trade_date", "ts_code").collect())
            raw = model.predict(to_matrix(valid_frame, use_features)).astype(np.float64)
            raw[~valid_frame["price_valid"].to_numpy()] = -1e6
            cache = OUT / f"{candidate['key']}_{year}.parquet"
            valid_frame.select(KEYS).with_columns(pl.Series("pred_raw", raw)).write_parquet(
                cache, compression="zstd")
            record["candidates"][candidate["key"]][str(year)] = {
                "rows": int(len(label)), "cache": cache.relative_to(ROOT).as_posix(),
                "cache_sha256": file_hash(cache)}
            log(f"{candidate['key']} {year}: rows={len(label):,}")
            del frame, valid_frame, matrix, label, model
    result_path.write_text(json.dumps(record, ensure_ascii=False, indent=2), encoding="utf-8")
    log(f"Wrote {result_path}")


def develop() -> None:
    verify_protocol()
    result_path = OUT / "development_wave2.json"
    if result_path.exists():
        raise SystemExit("Wave-2 development already recorded; preserving it")
    released = release_scores()
    started = time.monotonic()
    candidates = {}
    for year in DEVELOPMENT_YEARS:
        panel = load_panel(year)
        auxiliary = load_auxiliary(year, panel)
        backbone = panel.frame["pred_raw"].to_numpy().astype(np.float64)
        baseline = blend_top_only(panel, retention_scores(panel, backbone, RELEASED["alpha"],
                                                          BASE_BONUS, "standard"),
                                  backbone, auxiliary, BLEND_WEIGHT)
        baseline_metrics, _ = official_score(panel, baseline, year)
        if abs(baseline_metrics["final_score"] - released[year]) > NUMERIC_TOLERANCE:
            raise AssertionError(f"{year} wave-2 baseline anchor off")
        log(f"{year} baseline anchor reproduced exactly")
        for candidate in CANDIDATES:
            key, variant = candidate["key"], candidate["variant"]
            if variant == "pp_ensemble":
                members = []
                for alpha in ENSEMBLE_ALPHAS:
                    stable = retention_scores(panel, backbone, alpha, BASE_BONUS, "standard")
                    members.append(blend_top_only(panel, stable, backbone, auxiliary, BLEND_WEIGHT))
                shape = panel.valid_price.shape
                mixed = np.zeros(shape)
                for member in members:
                    m = member.reshape(shape)
                    for day in range(shape[0]):
                        keep = panel.valid_price[day]
                        from scipy.stats import rankdata as _rd
                        mixed[day][keep] += _rd(m[day][keep], method="average") / keep.sum()
                prediction = mixed.reshape(-1) / len(members)
            else:
                frame = pl.read_parquet(OUT / f"{key}_{year}.parquet").sort("trade_date", "ts_code")
                raw = frame["pred_raw"].to_numpy().astype(np.float64)
                stable = retention_scores(panel, raw, candidate["alpha"], BASE_BONUS, "standard")
                prediction = blend_top_only(panel, stable, raw, auxiliary, BLEND_WEIGHT)
            metrics, daily = official_score(panel, prediction, year)
            item = candidates.setdefault(key, {"years": {}})
            item["years"][str(year)] = {k: float(v) for k, v in metrics.items()}
            daily.write_csv(OUT / f"{key}_{year}_daily.csv")
            log(f"{year} {key}: score={metrics['final_score']:.9f} ic={metrics['ic_mean']:.6f} "
                f"excess={metrics['annual_excess']:.6f} turn={metrics['mean_turnover']:.6f}")
        del panel, auxiliary
    for key, item in candidates.items():
        deltas = {y: item["years"][y]["final_score"] - released[y] for y in map(str, DEVELOPMENT_YEARS)}
        item["score_delta"] = deltas
        item["passes_development_gate"] = all(v > NUMERIC_TOLERANCE for v in deltas.values())
        item["two_year_mean_delta"] = sum(deltas.values()) / len(deltas)
        item["two_year_minimax_delta"] = min(deltas.values())
    passing = [k for k, v in candidates.items() if v["passes_development_gate"]]
    output = {"stage": "develop_wave2", "generated_at_local": time.strftime("%Y-%m-%dT%H:%M:%S"),
              "elapsed_seconds": time.monotonic() - started,
              "protocol_sha256": file_hash(OUT / "protocol_wave2.json"),
              "candidates": candidates, "candidates_passing_development_gate": passing,
              "caveat": PROTOCOL["limitations"]}
    result_path.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")
    log(f"WAVE-2 DEVELOPMENT: {len(passing)} of {len(candidates)} pass: {passing}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("stage", choices=("protocol", "train", "develop"))
    arguments = parser.parse_args()
    if arguments.stage == "protocol":
        write_protocol()
    elif arguments.stage == "train":
        train()
    else:
        develop()
