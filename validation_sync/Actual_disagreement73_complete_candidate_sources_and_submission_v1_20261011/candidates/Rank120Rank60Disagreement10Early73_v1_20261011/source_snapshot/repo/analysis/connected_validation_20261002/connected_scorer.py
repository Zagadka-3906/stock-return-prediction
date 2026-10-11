"""The connected 2020-2024 official scorer required by 后续选模标准.md §3.

The standard's primary score is the official composite computed ONCE over the connected out-of-sample
series: each year's walk-forward predictions are concatenated in date order and the unmodified
evaluate.py is run over the whole interval, so turnover at a year boundary is measured against the
previous year's last day instead of being silently dropped.

This project has never computed that number. Every ranking it ever produced used the equal-weight mean
of five separate annual composites, which (a) is not the aggregation the brief implies and (b) drops
four boundary turnover observations - one per year transition - because the evaluator starts turnover
on the second day of whatever frame it is given. Under the new standard the five-year mean survives
only as a diagnostic.

Nothing here reads test labels or any 2025-2026 data. Import and call score_candidate().
"""
from __future__ import annotations

import hashlib
import json
import sys
import time
from pathlib import Path

import numpy as np
import polars as pl

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT))
from experiments.revalidate_fold_local import score_official  # noqa: E402

ARCHIVE = ROOT.parent / "赛题五_历史归档_20261001"
R4 = ARCHIVE / "experiments/revalidation_20260926/validation"
YEARS = (2020, 2021, 2022, 2023, 2024)
KEYS = ["ts_code", "trade_date"]
KEEP = KEYS + ["flag_limit_up", "y_ret_1d", "price_valid", "aux_raw"]
FRAME_CACHE = HERE / "combined_fold_frame.parquet"


def sha(path: Path) -> str:
    value = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for chunk in iter(lambda: stream.read(8 * 1024 * 1024), b""):
            value.update(chunk)
    return value.hexdigest()


def log(message: str) -> None:
    print(f"[{time.strftime('%H:%M:%S')}] {message}", flush=True)


def combined_frame(rebuild: bool = False) -> pl.DataFrame:
    """Concatenate the five fold frames in date order; cached because every candidate reuses it."""
    if FRAME_CACHE.exists() and not rebuild:
        return pl.read_parquet(FRAME_CACHE)
    parts = []
    for year in YEARS:
        path = R4 / f"predictions_ensemble4_{year}.parquet"
        part = pl.read_parquet(path).select(KEEP)
        if part["trade_date"].min() // 10000 != year or part["trade_date"].max() // 10000 != year:
            raise AssertionError(f"{year}: fold frame does not sit inside its own year")
        parts.append(part)
    frame = pl.concat(parts).sort("trade_date", "ts_code")
    dates = frame["trade_date"].unique().sort()
    gaps = [(int(a), int(b)) for a, b in zip(dates[:-1], dates[1:]) if b - a > 100]
    frame.write_parquet(FRAME_CACHE, compression="zstd")
    log(f"combined frame: {len(frame):,} rows, {len(dates)} days, "
        f"{dates.min()}..{dates.max()}; large date gaps (year ends) = {len(gaps)}")
    return pl.read_parquet(FRAME_CACHE)


def score(frame: pl.DataFrame, pred: np.ndarray) -> dict:
    metrics, daily = score_official(frame, pred)
    return {"metrics": metrics, "daily": daily}


def score_candidate(frame: pl.DataFrame, pred: np.ndarray, name: str) -> dict:
    """Connected composite (primary) plus the five annual composites (diagnostic only)."""
    if not np.isfinite(pred).all():
        raise ValueError(f"{name}: non-finite predictions")
    if len(pred) != len(frame):
        raise ValueError(f"{name}: {len(pred)} predictions for {len(frame)} rows")
    started = time.monotonic()
    connected = score(frame, pred)["metrics"]
    annual = {}
    dates = frame["trade_date"].to_numpy()
    for year in YEARS:
        mask = (dates >= year * 10000 + 101) & (dates <= year * 10000 + 1231)
        annual[year] = score(frame.filter(pl.Series(mask)), pred[mask])["metrics"]
    five_year_mean = float(np.mean([annual[y]["final_score"] for y in YEARS]))
    return {
        "name": name,
        "connected_final_score": connected["final_score"],
        "connected_metrics": connected,
        "annual_final_scores": {str(y): annual[y]["final_score"] for y in YEARS},
        "five_year_equal_weight_mean_diagnostic_only": five_year_mean,
        "connected_minus_five_year_mean": connected["final_score"] - five_year_mean,
        "seconds": round(time.monotonic() - started, 1),
    }


def score_arm_dict(frame: pl.DataFrame, preds_by_year: dict[int, np.ndarray], name: str,
                   frozen_annual: dict[int, float] | None = None,
                   tolerance: float = 2e-9, save: bool = True) -> dict:
    """Score one candidate given its five per-fold FINAL prediction columns.

    The per-year frames are the same slices the combined frame is built from, in the same
    (trade_date, ts_code) order, so concatenating in year order yields the connected column. Annual
    composites are computed on the slices and asserted against the frozen record when one exists, so
    a reconstruction error can never be mistaken for a result.
    """
    dates = frame["trade_date"].to_numpy()
    parts, annual = [], {}
    for year in YEARS:
        path = R4 / f"predictions_ensemble4_{year}.parquet"
        yf = pl.read_parquet(path).sort("trade_date", "ts_code")
        pred = np.asarray(preds_by_year[year], dtype=np.float64)
        if len(pred) != len(yf):
            raise ValueError(f"{name}/{year}: {len(pred)} predictions for {len(yf)} rows")
        if not np.isfinite(pred).all():
            raise ValueError(f"{name}/{year}: non-finite predictions")
        mask = (dates >= year * 10000 + 101) & (dates <= year * 10000 + 1231)
        if not yf.select(KEYS).equals(frame.filter(pl.Series(mask)).select(KEYS)):
            raise AssertionError(f"{name}/{year}: keys do not match the combined frame slice")
        metrics, _ = score_official(yf, pred)
        annual[year] = metrics
        if frozen_annual is not None and year in frozen_annual:
            diff = abs(metrics["final_score"] - frozen_annual[year])
            if diff > tolerance:
                raise AssertionError(f"{name}/{year}: {metrics['final_score']!r} vs frozen "
                                     f"{frozen_annual[year]!r} (diff {diff:.3e} > {tolerance:.0e})")
        parts.append(pred)
        del yf
    connected_pred = np.concatenate(parts)
    if len(connected_pred) != len(frame):
        raise ValueError(f"{name}: connected column is {len(connected_pred)} of {len(frame)} rows")
    started = time.monotonic()
    connected, _ = score_official(frame, connected_pred)
    five_year_mean = float(np.mean([annual[y]["final_score"] for y in YEARS]))
    if save:
        np.save(HERE / f"connected_pred_{name}.npy", connected_pred)
    log(f"{name}: CONNECTED {connected['final_score']:.9f} | five-year mean {five_year_mean:.9f} "
        f"| delta {connected['final_score'] - five_year_mean:+.9f}")
    return {"name": name, "connected_final_score": connected["final_score"],
            "connected_metrics": connected,
            "annual_final_scores": {str(y): annual[y]["final_score"] for y in YEARS},
            "annual_metrics": {str(y): annual[y] for y in YEARS},
            "five_year_equal_weight_mean_diagnostic_only": five_year_mean,
            "connected_minus_five_year_mean": connected["final_score"] - five_year_mean,
            "annual_calibration": ({str(y): {"recomputed": annual[y]["final_score"],
                                             "frozen": frozen_annual[y],
                                             "abs_diff": abs(annual[y]["final_score"] - frozen_annual[y])}
                                     for y in frozen_annual} if frozen_annual else {}),
            "connected_seconds": round(time.monotonic() - started, 1)}


def turnover_accounting(frame: pl.DataFrame) -> dict:
    """How many turnover observations the annual caliber drops relative to the connected one."""
    dates = frame["trade_date"].unique().sort().to_list()
    per_year = {y: int(sum(1 for d in dates if d // 10000 == y)) for y in YEARS}
    annual_observations = sum(max(n - 1, 0) for n in per_year.values())
    connected_observations = len(dates) - 1
    return {"days_total": len(dates), "days_per_year": per_year,
            "turnover_observations_annual_caliber": annual_observations,
            "turnover_observations_connected_caliber": connected_observations,
            "boundary_observations_recovered":
                connected_observations - annual_observations}


def calibrate(frame: pl.DataFrame, expected_annual: dict[int, float], pred: np.ndarray,
              name: str, tolerance: float = 2e-9) -> dict:
    """Prove the combined frame is faithful: each year slice must reproduce its frozen composite."""
    dates = frame["trade_date"].to_numpy()
    record = {}
    for year, expected in expected_annual.items():
        mask = (dates >= year * 10000 + 101) & (dates <= year * 10000 + 1231)
        got = score(frame.filter(pl.Series(mask)), pred[mask])["metrics"]["final_score"]
        record[str(year)] = {"recomputed": got, "frozen": expected, "abs_diff": abs(got - expected)}
        if abs(got - expected) > tolerance:
            raise AssertionError(f"{name}/{year}: slice composite {got!r} vs frozen {expected!r}")
    log(f"{name}: all five year slices of the combined frame reproduce their frozen composites "
        f"(max diff {max(v['abs_diff'] for v in record.values()):.1e})")
    return record


if __name__ == "__main__":
    frame = combined_frame()
    accounting = turnover_accounting(frame)
    log(json.dumps(accounting, ensure_ascii=False))
    (HERE / "frame_accounting.json").write_text(
        json.dumps({"accounting": accounting, "frame_rows": len(frame),
                    "frame_sha256": sha(FRAME_CACHE),
                    "sources": {str(y): sha(R4 / f"predictions_ensemble4_{y}.parquet")
                                for y in YEARS},
                    "built_at_local": time.strftime("%Y-%m-%dT%H:%M:%S")},
                   ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
