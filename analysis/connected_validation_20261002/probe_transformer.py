"""Direction 3 probe: can the tabular transformer be reproduced, and what does a fold cost?

The orderer ensemble W5a has five members: four gradient-boosted tree families on the same Alpha158
features plus one GRU-cat sequence model. The GRU's history is the reason to look at the transformer: it
was **rejected standalone** in final_sweep_wave5 ("the released post-processing stack is tuned for daily
cross-sectional tree ranks, and the sequence ensemble failed its own gate"), yet as a minority member of
a rank average it became the single most valuable component of the wave-12 winning orderer. The tabular
transformer is the other structurally different signal in the project - an FT-Transformer-lite with one
learned token per feature - and it was rejected by the same suite, so the same argument applies to it and
has never been tested.

The blocker is coverage, not code. `final_sweep_eval/T2g_tabular_transformer_{2022,2023,2024}.parquet`
exist, but the connected caliber needs all five fold years and 2020/2021 were never trained. The
`r6_transformer_20260926` checkpoints cover 2020-2022 but are a DIFFERENT experiment with its own
config, so they cannot be assumed interchangeable with final_sweep_extra's TR_* constants.

This probe answers the two questions that decide whether direction 3 is worth its cost:
  1. does final_sweep_extra's own train_transformer / predict_transformer reproduce the frozen
     T2g_tabular_transformer_2022.parquet? If not, the recipe is not recoverable and the direction dies.
  2. how long does one fold take, and how much memory? training_extra.json records 3.578 s for both 2022
     and 2023 with bit-identical digits, but that timer wraps ONLY predict_transformer -
     train_transformer sits outside it - so the recorded number says nothing about the cost that matters.

Stage `prove` runs question 1 and 2 for 2022. Stage `extend` trains 2020 and 2021 and writes their raw
columns, and is only meaningful once `prove` has passed. Nothing is written to the archive; output goes
to wave26_transformer/. No test-period data is read.
"""
from __future__ import annotations

import argparse
import ctypes
import gc
import hashlib
import json
import sys
import time
from pathlib import Path

import numpy as np
import polars as pl

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
ARCHIVE = ROOT.parent / "赛题五_历史归档_20261001"
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(ARCHIVE))

OUT = HERE / "wave26_transformer"
RAW = OUT / "raw"
FROZEN = ARCHIVE / "experiments/final_sweep_eval"
PROOF_YEAR = 2022
EXTEND_YEARS = (2020, 2021)
KEYS = ["ts_code", "trade_date"]


def sha(path) -> str:
    value = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for chunk in iter(lambda: stream.read(8 * 1024 * 1024), b""):
            value.update(chunk)
    return value.hexdigest()


def log(message: str) -> None:
    print(f"[{time.strftime('%H:%M:%S')}] {message}", flush=True)


def memory_gib() -> dict:
    class MEMORYSTATUSEX(ctypes.Structure):
        _fields_ = [("dwLength", ctypes.c_ulong), ("dwMemoryLoad", ctypes.c_ulong),
                    ("ullTotalPhys", ctypes.c_ulonglong), ("ullAvailPhys", ctypes.c_ulonglong),
                    ("ullTotalPageFile", ctypes.c_ulonglong), ("ullAvailPageFile", ctypes.c_ulonglong),
                    ("ullTotalVirtual", ctypes.c_ulonglong), ("ullAvailVirtual", ctypes.c_ulonglong),
                    ("ullAvailExtendedVirtual", ctypes.c_ulonglong)]
    stat = MEMORYSTATUSEX()
    stat.dwLength = ctypes.sizeof(MEMORYSTATUSEX)
    ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(stat))
    gib = 1024 ** 3
    return {"total_gib": round(stat.ullTotalPhys / gib, 2),
            "available_gib": round(stat.ullAvailPhys / gib, 2),
            "load_percent": int(stat.dwMemoryLoad)}


def run_year(fse, load_seq_panel, fit_scaler, apply_scaler, feature_names, fold_cutoff, to_matrix,
             FEATURE_FILE, R4, year: int, keep_model: bool):
    """Train and predict one fold exactly as final_sweep_extra.train() does for the transformer."""
    features = feature_names()
    timings: dict = {}
    t0 = time.monotonic()
    dates, codes, x, y, valid, _ = load_seq_panel(features, 2024)
    timings["load_panel_seconds"] = round(time.monotonic() - t0, 1)
    timings["panel_shape"] = list(np.shape(x))
    timings["panel_gib"] = round(x.nbytes / 1024 ** 3, 3)
    timings["memory_after_panel"] = memory_gib()
    log(f"panel {np.shape(x)} = {x.nbytes / 1024 ** 3:.2f} GiB, "
        f"{timings['load_panel_seconds']}s; RAM {timings['memory_after_panel']}")

    cutoff = fold_cutoff(year)
    t0 = time.monotonic()
    mean, std, stats = fit_scaler(x, valid, dates, cutoff)
    z = apply_scaler(x, mean, std)
    timings["scale_seconds"] = round(time.monotonic() - t0, 1)
    timings["memory_after_scale"] = memory_gib()

    import torch
    t0 = time.monotonic()
    model = fse.train_transformer(z, y, valid, dates, cutoff)
    timings["TRAIN_transformer_seconds"] = round(time.monotonic() - t0, 1)
    timings["memory_after_train"] = memory_gib()
    timings["cuda_available"] = bool(torch.cuda.is_available())
    log(f"TRAIN took {timings['TRAIN_transformer_seconds']}s (the frozen record's 3.578 s covers "
        f"predict only); RAM {timings['memory_after_train']}")

    outer_days = [t for t, d in enumerate(dates) if year * 10000 + 101 <= d <= year * 10000 + 1231]
    t0 = time.monotonic()
    raw_days = fse.predict_transformer(model, z, outer_days, z.shape[1], z.shape[2])
    timings["predict_seconds"] = round(time.monotonic() - t0, 1)
    raw = raw_days.reshape(-1).astype(np.float64)
    raw[~valid[np.asarray(outer_days)].reshape(-1)] = -1e6
    raw[~np.isfinite(raw)] = -1e6

    lazy = pl.scan_parquet(FEATURE_FILE)
    valid_frame = (lazy.filter(pl.col("trade_date").is_between(year * 10000 + 101, year * 10000 + 1231))
                   .select(KEYS + ["price_valid"]).sort("trade_date", "ts_code").collect())
    if len(raw) != len(valid_frame):
        raise AssertionError(f"{year}: raw has {len(raw)} rows, feature frame has {len(valid_frame)}")
    frame = pl.read_parquet(R4 / f"predictions_ensemble4_{year}.parquet").sort("trade_date", "ts_code")
    if not frame.select(KEYS).equals(valid_frame.select(KEYS)):
        raise AssertionError(f"{year}: feature frame keys do not match the fold frame")

    if not keep_model:
        del model
    del x, y, valid, z, mean, std
    gc.collect()
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
    return valid_frame, raw, timings


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("stage", choices=("prove", "extend"))
    args = parser.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    RAW.mkdir(parents=True, exist_ok=True)

    import torch
    import experiments.final_sweep_extra as fse
    from experiments.sequence_model import load_panel as load_seq_panel, fit_scaler, apply_scaler
    from run import FEATURE_FILE, feature_names, fold_cutoff, to_matrix
    from experiments.r6_topk import R4

    log(f"torch {torch.__version__}, cuda {torch.cuda.is_available()}, "
        f"TR config dim={fse.TR_DIM} layers={fse.TR_LAYERS} heads={fse.TR_HEADS} "
        f"epochs={fse.TR_EPOCHS} batch_days={fse.TR_BATCH_DAYS} seed={fse.SEED}")

    if args.stage == "prove":
        frame, raw, timings = run_year(fse, load_seq_panel, fit_scaler, apply_scaler, feature_names,
                                       fold_cutoff, to_matrix, FEATURE_FILE, R4, PROOF_YEAR, False)
        frozen_path = FROZEN / f"T2g_tabular_transformer_{PROOF_YEAR}.parquet"
        frozen = pl.read_parquet(frozen_path).sort("trade_date", "ts_code")
        if not frozen.select(KEYS).equals(frame.select(KEYS)):
            raise AssertionError("the frozen transformer cache's keys do not match the fold frame")
        target = frozen["pred_raw"].to_numpy().astype(np.float64)
        both_finite = np.isfinite(target) & (target > -1e5) & np.isfinite(raw) & (raw > -1e5)
        diff_all = float(np.abs(raw - target).max())
        diff_finite = float(np.abs(raw[both_finite] - target[both_finite]).max()) if both_finite.any() \
            else None
        identical = bool(np.array_equal(raw, target))
        # rank agreement on the usable subset is what actually matters for an orderer role
        ranks_equal = None
        if both_finite.any():
            from scipy.stats import spearmanr
            ranks_equal = float(spearmanr(raw[both_finite], target[both_finite]).statistic)
        log(f"PROVE {PROOF_YEAR}: bit-identical={identical}, max|diff| all={diff_all:.6e}, "
            f"finite subset={diff_finite}, finite rows={int(both_finite.sum())}/{len(raw)}, "
            f"spearman={ranks_equal}")
        record = {"stage": "prove", "year": PROOF_YEAR, "frozen_cache": str(frozen_path),
                  "frozen_sha256": sha(frozen_path), "bit_identical": identical,
                  "max_abs_diff_all": diff_all, "max_abs_diff_finite_subset": diff_finite,
                  "finite_rows": int(both_finite.sum()), "rows": int(len(raw)),
                  "spearman_on_finite_subset": ranks_equal,
                  "sentinel_convention_note": "both writers set price-invalid rows to -1e6, but the "
                                              "frozen cache was written by a run whose panel came from "
                                              "the same loader; compare the usable subset, not the "
                                              "sentinels, for rank purposes",
                  "timings": timings, "transformer_config": {
                      "dim": fse.TR_DIM, "layers": fse.TR_LAYERS, "heads": fse.TR_HEADS,
                      "epochs": fse.TR_EPOCHS, "batch_days": fse.TR_BATCH_DAYS, "seed": fse.SEED},
                  "recorded_elapsed_in_training_extra_json": 3.578,
                  "why_the_recorded_number_is_misleading": "final_sweep_extra.train() starts its timer "
                                                           "after train_transformer returns, so 3.578 s "
                                                           "is predict-only",
                  "proved_at_local": time.strftime("%Y-%m-%dT%H:%M:%S"),
                  "source_sha256": sha(Path(__file__))}
        (OUT / f"prove_{PROOF_YEAR}.json").write_text(
            json.dumps(record, ensure_ascii=False, indent=2, default=str) + "\n", encoding="utf-8")
        np.save(RAW / f"transformer_raw_{PROOF_YEAR}.npy", raw)
        log(f"wrote {OUT / f'prove_{PROOF_YEAR}.json'}")
        return

    for year in EXTEND_YEARS:
        target = RAW / f"transformer_raw_{year}.npy"
        if target.exists():
            log(f"{year}: already trained, skipping")
            continue
        frame, raw, timings = run_year(fse, load_seq_panel, fit_scaler, apply_scaler, feature_names,
                                       fold_cutoff, to_matrix, FEATURE_FILE, R4, year, False)
        frame.select(KEYS).with_columns(pl.Series("pred_raw", raw)).write_parquet(
            RAW / f"transformer_{year}.parquet", compression="zstd")
        np.save(target, raw)
        (OUT / f"extend_{year}.json").write_text(
            json.dumps({"stage": "extend", "year": year, "rows": int(len(raw)),
                        "sentinel_rows": int((raw <= -1e5).sum()), "timings": timings,
                        "trained_at_local": time.strftime("%Y-%m-%dT%H:%M:%S")},
                       ensure_ascii=False, indent=2, default=str) + "\n", encoding="utf-8")
        log(f"{year}: trained in {timings['TRAIN_transformer_seconds']}s, "
            f"{int((raw <= -1e5).sum()):,} sentinel rows")


if __name__ == "__main__":
    main()
