"""Daily contributions whose mean reproduces the official composite difference."""
from __future__ import annotations

import numpy as np
import pandas as pd

WEIGHTS = {"rank_ic": 0.4, "excess": 0.3 * 252, "turnover": -0.3}


def metric_denominators(frame: pd.DataFrame) -> dict[str, int]:
    counts = {}
    for name in WEIGHTS:
        values = frame[name].to_numpy(dtype=np.float64)
        if np.isinf(values).any():
            raise ValueError(f"Infinite official metric: {name}")
        counts[name] = int(np.isfinite(values).sum())
        if not counts[name]:
            raise ValueError(f"No valid days for official metric: {name}")
    return counts


def composite(frame: pd.DataFrame) -> float:
    metric_denominators(frame)
    return float(0.3 + sum(weight * frame[name].mean() for name, weight in WEIGHTS.items()))


def daily_contribution(frame: pd.DataFrame) -> np.ndarray:
    """N-scaled shares; average over N rows retains each metric's valid-day denominator.

    The common constant 0.3 cancels between arms. A missing metric contributes
    zero to its sum, while its denominator excludes that row (normally day one
    of turnover). Each arm retains its own denominators if missingness differs.
    """
    counts = metric_denominators(frame)
    result = np.zeros(len(frame), dtype=np.float64)
    for name, weight in WEIGHTS.items():
        values = frame[name].to_numpy(dtype=np.float64)
        result += weight * np.nan_to_num(values, nan=0.0) * len(frame) / counts[name]
    if not np.isclose(result.mean(), composite(frame) - 0.3, rtol=0, atol=1e-12):
        raise AssertionError("Daily contributions do not reproduce the official composite")
    return result


def paired_difference(left: pd.DataFrame, right: pd.DataFrame) -> np.ndarray:
    if left["trade_date"].duplicated().any() or right["trade_date"].duplicated().any():
        raise AssertionError("Duplicate daily trade dates")
    if not np.array_equal(left["trade_date"].to_numpy(), right["trade_date"].to_numpy()):
        raise AssertionError("Daily frames are not aligned on trade_date")
    diff = daily_contribution(left) - daily_contribution(right)
    if not np.isclose(diff.mean(), composite(left) - composite(right), rtol=0, atol=1e-12):
        raise AssertionError("Paired contributions do not reproduce the official score difference")
    return diff
