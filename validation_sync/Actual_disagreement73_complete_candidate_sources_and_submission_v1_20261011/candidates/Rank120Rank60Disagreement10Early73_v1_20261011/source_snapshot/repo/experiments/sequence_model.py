"""Sequence-model feasibility probe against the frozen LightGBM backbone.

Nothing here retrains or touches the release. The question is narrow and was
chosen after measuring the real bar: the released 2022 Rank IC of 0.118468 is
measured after EMA smoothing, the persistence bonus, protected-block restoration
and the 25% blend, and that stack *costs* IC relative to the raw backbone
(0.127848). A new model family must therefore be judged on raw IC first.

Nested split, so the outer year is scored exactly once:

    inner train  2018-2020   (cutoff exclusive 20201231, which is purged because
                              its label uses the first 2021 close)
    inner val    2021        early stopping and architecture selection
    outer test   2022        scored once, against the frozen reference bars

Three architectures are pre-declared. The MLP control matters most: if a plain
feed-forward net on the same 63 daily features matches the GRU, then the
sequence structure is not earning its keep and the backbone is already
extracting what is there.

Loss is negative mean daily cross-sectional Pearson correlation, the
differentiable proxy for the competition's Spearman Rank IC. Reported metrics
always come from the unmodified evaluate.py through official_score.
"""
from __future__ import annotations

import argparse
import json
import time
from pathlib import Path

import numpy as np
import polars as pl

from run import FEATURE_FILE, ROOT, feature_names, fold_cutoff, to_matrix

OUT = ROOT / "experiments" / "sequence_model_eval"
KEYS = ["ts_code", "trade_date"]

INNER_CUTOFF_EXCLUSIVE = 20201231     # purge 20201231: its label uses a 2021 close
INNER_VAL_YEAR = 2021
OUTER_YEAR = 2022
SEED = 2026
CLIP_STD = 5.0
BATCH_DAYS = 4
LEARNING_RATE = 1e-3
WEIGHT_DECAY = 1e-6
MAX_EPOCHS = 60
PATIENCE = 10
MIN_VALID_PER_DAY = 100

# Pre-declared grid. Window applies only to the recurrent variants; the MLP
# control sees the single current day.
ARCHITECTURES = ("mlp", "gru", "gru_cat")
HIDDEN = (64, 128)
WINDOWS = (10, 20)

PROTOCOL = {
    "experiment": "sequence_model_feasibility_probe",
    "question": "Can a recurrent sequence model over the frozen 63 daily features beat the raw "
                "LightGBM backbone's cross-sectional Rank IC, alone or in a rank-average ensemble?",
    "primary_bar": "backbone_raw_no_postprocess ic_mean for 2022 from reference_bars.json",
    "nested_split": {
        "inner_train": "2018-2020, cutoff exclusive 20201231 (purged: its label uses a 2021 close)",
        "inner_val": "2021, used for early stopping and architecture selection only",
        "outer_test": "2022, scored exactly once after the architecture is frozen",
    },
    "features": "the frozen original 63, unchanged; no new or market-level features",
    "target": "y_rank, the same daily centered cross-sectional percentile the backbone regresses",
    "normalization": {
        "rule": "per-feature mean and standard deviation fitted only on price-valid rows dated "
                "strictly before the relevant cutoff, using nonfinite-aware two-pass statistics, "
                "then clip to +/-5 standard deviations and set any remaining nonfinite value to zero",
        "search_phase_cutoff": INNER_CUTOFF_EXCLUSIVE,
        "final_fold_cutoff": "fold_cutoff(2022), matching the released backbone fold",
        "std_floor": "only a non-finite or exactly-zero standard deviation is replaced by 1.0",
        "nonfinite_handling": "49 of the 63 features contain missing values (up to 10.04% of "
                              "price-valid rows for VMA60/VSTD60), so naive column means are NaN; "
                              "statistics must ignore nonfinite entries rather than propagate them",
    },
    "window": "L trailing trading days ending at and including day t; days with an incomplete "
              "window are masked out of both loss and evaluation",
    "loss": "negative mean daily cross-sectional Pearson correlation over valid rows; days with "
            "fewer than 100 valid rows are excluded",
    "optimizer": {"type": "Adam", "lr": LEARNING_RATE, "weight_decay": WEIGHT_DECAY,
                  "schedule": "none", "precision": "float32, TF32 disabled"},
    "batch_days": BATCH_DAYS,
    "max_epochs": MAX_EPOCHS,
    "early_stopping": f"best inner-val daily IC, patience {PATIENCE} epochs",
    "seed": SEED,
    "grid": {"architectures": list(ARCHITECTURES), "hidden": list(HIDDEN), "windows": list(WINDOWS),
             "note": "mlp ignores the window dimension"},
    "selection_rule": "highest inner-val (2021) mean daily IC; exact ties prefer the smaller "
                      "hidden size then the shorter window then ARCHITECTURES order",
    "gate": {
        "strong_pass": "sequence model raw 2022 IC >= backbone raw 2022 IC",
        "pass": "rank-average ensemble of backbone raw and sequence model raw achieves 2022 IC "
                "strictly greater than backbone raw 2022 IC",
        "fail": "neither; stop, adopt nothing, try no further architecture, window, seed or epoch",
    },
    "ensemble_rule": "per-day cross-sectional percentile rank of each raw signal, averaged with "
                     "equal weight, then scored by the unmodified evaluator; no post-processing "
                     "stack is applied at this stage",
    "scorer": "Unmodified evaluate.py via official_score: float17 CSV round trip, original Float64 "
              "labels, pandas default descending tie order",
    "prohibited_after_results": [
        "Adding or substituting architectures, windows, hidden sizes, seeds or epoch counts",
        "Re-scoring 2022, or scoring 2023/2024 before the 2022 gate is decided",
        "Tuning on 2022 in any way, including choosing epochs by outer-year IC",
        "Applying the released post-processing stack to rescue a failing raw IC",
        "Modifying the release, its manifest, or any frozen source or prior experiment directory",
    ],
    "amendments_before_any_scoring": [
        {
            "at_local": "2026-09-26T02:58",
            "change": "Normalization statistics changed from naive per-column mean/std to "
                      "nonfinite-aware two-pass statistics, and the standard-deviation floor "
                      "changed from 1e-8 to only non-finite or exactly zero.",
            "reason": "49 of the 63 features contain missing values, so a naive column mean is NaN "
                      "and the subsequent (x-mean)/std turned the entire column nonfinite, which "
                      "the zero-fill then silently discarded. A throwaway smoke test caught this "
                      "before any search or outer-year scoring. Separately, ILLIQ has a true "
                      "standard deviation of 8.15e-09 with a mean of 5.90e-10, so a 1e-8 floor "
                      "would have destroyed a genuine feature rather than guarding a constant one.",
            "evidence": "The superseded protocol is preserved at "
                        "protocol_superseded_before_scoring.json. No search, fold, gate or score "
                        "existed at the time of this amendment.",
        },
    ],
    "limitations": [
        "cuDNN recurrent backward is not bitwise deterministic, so repeated runs of an identical "
        "configuration can differ slightly; the selected configuration is rerun to bound that "
        "variance rather than to pick a better number.",
        "2022 has been examined many times across roughly twenty prior rounds and is not a blind "
        "holdout.",
        "A single outer year cannot separate a real model improvement from regime luck.",
        "Raw IC is the bar at this stage; a pass here does not by itself imply a higher released "
        "composite score, because the post-processing stack was tuned on the backbone's signal.",
    ],
}


def log(message: str) -> None:
    print(f"[{time.strftime('%H:%M:%S')}] {message}", flush=True)


def file_hash(path: Path) -> str:
    import hashlib
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_panel(features: list[str], end_year: int):
    """Rectangular (day, stock) arrays over 2018 through end_year."""
    frame = (pl.scan_parquet(FEATURE_FILE)
             .filter(pl.col("trade_date") <= end_year * 10000 + 1231)
             .select(KEYS + features + ["y_rank", "price_valid", "is_train"])
             .sort("trade_date", "ts_code")
             .collect())
    dates = frame["trade_date"].unique(maintain_order=True).to_list()
    codes = frame["ts_code"].to_numpy()
    n = len(codes) // len(dates)
    if len(codes) != len(dates) * n:
        raise AssertionError("Sequence panel is not rectangular")
    codes = codes.reshape(len(dates), n)
    if not np.all(codes == codes[0]):
        raise AssertionError("Stock order differs across dates in the sequence panel")
    x = to_matrix(frame, features).reshape(len(dates), n, len(features))
    y = frame["y_rank"].to_numpy().astype(np.float32).reshape(len(dates), n)
    valid = frame["price_valid"].to_numpy().reshape(len(dates), n)
    is_train = frame["is_train"].to_numpy().reshape(len(dates), n)
    log(f"Panel {len(dates)} days x {n} stocks x {len(features)} features "
        f"({x.nbytes / 2**30:.2f} GiB float32)")
    return [int(d) for d in dates], [str(c) for c in codes[0]], x, y, valid, is_train


def fit_scaler(x: np.ndarray, valid: np.ndarray, dates: list[int], cutoff: int,
               blocks: int = 8) -> tuple:
    """Nonfinite-aware two-pass column statistics over price-valid training rows.

    49 of the 63 features carry missing values, so a naive column mean is NaN and
    would propagate through (x - mean)/std into a wholly discarded column. Both
    passes are chunked to bound peak memory. Only a non-finite or exactly-zero
    standard deviation is replaced; a genuinely small one (ILLIQ has 8.15e-09) is
    real scale, not a degenerate column.
    """
    days = np.asarray([d < cutoff for d in dates])
    if not days.any():
        raise AssertionError("No training days before the normalization cutoff")
    flat = x[days][valid[days]]
    rows, n_features = flat.shape
    if rows < 1000:
        raise AssertionError(f"Only {rows} rows before the normalization cutoff")
    splits = np.array_split(np.arange(rows), blocks)

    count = np.zeros(n_features, dtype=np.float64)
    total = np.zeros(n_features, dtype=np.float64)
    for block in splits:
        sub = flat[block]
        finite = np.isfinite(sub)
        count += finite.sum(axis=0)
        total += np.where(finite, sub, 0.0).astype(np.float64).sum(axis=0)
    if not np.all(count > 0):
        empty = int(np.count_nonzero(count <= 0))
        raise AssertionError(f"{empty} features have no finite training value")
    mean = total / count

    squares = np.zeros(n_features, dtype=np.float64)
    for block in splits:
        sub = flat[block]
        finite = np.isfinite(sub)
        centered = np.where(finite, sub.astype(np.float64) - mean, 0.0)
        squares += (centered * centered).sum(axis=0)
    std = np.sqrt(np.maximum(squares / count, 0.0))

    degenerate = int(np.count_nonzero(~np.isfinite(std) | (std <= 0)))
    std[~np.isfinite(std)] = 1.0
    std[std <= 0] = 1.0
    mean[~np.isfinite(mean)] = 0.0
    mean32 = np.ascontiguousarray(mean, dtype=np.float32)
    std32 = np.ascontiguousarray(std, dtype=np.float32)

    missing_per_column = (~np.isfinite(flat)).sum(axis=0)
    stats = {
        "cutoff_exclusive": cutoff,
        "rows": int(rows),
        "days": int(days.sum()),
        "features": int(n_features),
        "nonfinite_input_cells": int(missing_per_column.sum()),
        "nonfinite_fraction_max": float((missing_per_column / rows).max()),
        "columns_with_any_missing": int(np.count_nonzero(missing_per_column > 0)),
        "degenerate_std_columns_replaced": degenerate,
        "std_min": float(std32.min()), "std_max": float(std32.max()),
        "mean_min": float(mean32.min()), "mean_max": float(mean32.max()),
        "mean_sha256": file_hash_of_array(mean32),
        "std_sha256": file_hash_of_array(std32),
    }
    del flat
    return mean32, std32, stats


def file_hash_of_array(array: np.ndarray) -> str:
    import hashlib
    return hashlib.sha256(np.ascontiguousarray(array, dtype=np.float32).tobytes()).hexdigest()


def apply_scaler(x: np.ndarray, mean: np.ndarray, std: np.ndarray) -> np.ndarray:
    z = (x - mean) / std
    z = np.clip(z, -CLIP_STD, CLIP_STD)
    z[~np.isfinite(z)] = 0.0
    return np.ascontiguousarray(z, dtype=np.float32)


def write_protocol() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / "protocol.json"
    features = feature_names()
    if len(features) != 63:
        raise AssertionError("Expected exactly the frozen 63 features")
    payload = {**PROTOCOL, "feature_names": features,
               "frozen_at_local": time.strftime("%Y-%m-%dT%H:%M:%S"),
               "source_sha256": file_hash(Path(__file__)),
               "feature_file_sha256": file_hash(FEATURE_FILE),
               "outer_fold_cutoff_exclusive": fold_cutoff(OUTER_YEAR),
               "reference_bars_sha256": file_hash(OUT / "reference_bars.json")}
    if path.exists():
        existing = json.loads(path.read_text(encoding="utf-8"))
        drift = {k: (existing.get(k), v) for k, v in PROTOCOL.items() if existing.get(k) != v}
        if drift:
            raise SystemExit(f"Protocol already frozen and differs; do not rewrite it after results: {drift}")
        log("Protocol already frozen and unchanged")
        return
    if not (OUT / "reference_bars.json").exists():
        raise SystemExit("Run experiments.reference_bars first; the bar must exist before freezing")
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    log(f"Froze protocol before any training: {len(ARCHITECTURES)} architectures x "
        f"{len(HIDDEN)} hidden x {len(WINDOWS)} windows")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("stage", choices=("protocol", "search", "fold"))
    arguments = parser.parse_args()
    if arguments.stage == "protocol":
        write_protocol()
    else:
        from experiments.sequence_training import run_stage
        run_stage(arguments.stage)
