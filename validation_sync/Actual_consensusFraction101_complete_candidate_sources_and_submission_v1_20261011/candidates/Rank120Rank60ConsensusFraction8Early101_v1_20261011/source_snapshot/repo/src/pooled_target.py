"""Daily clipped/centered returns scaled by the training-only pooled RMS."""
from __future__ import annotations
import hashlib
import numpy as np

def _target_with_stats(dates: np.ndarray, returns: np.ndarray) -> tuple[np.ndarray, dict]:
    """Caller supplies only the final purged and filtered training fold.

    New training rows may legitimately rescale all targets through pooled RMS.
    This is not a prediction transform and must never receive held-out labels.
    """
    dates = np.asarray(dates)
    values = np.asarray(returns)
    if (dates.ndim != 1 or not len(dates) or dates.dtype.kind not in "iuf"
            or not np.isfinite(dates).all() or not np.equal(dates, np.floor(dates)).all()
            or np.any(dates < 0) or np.any(dates >= 2**63)):
        raise ValueError("Dates must be a nonempty vector of nonnegative finite Int64-compatible integers")
    if (values.ndim != 1 or len(values) != len(dates) or values.dtype.kind not in "iuf"
            or not np.isfinite(values).all()):
        raise ValueError("Training returns must be finite numeric values aligned to dates")
    with np.errstate(over="ignore", invalid="ignore"):
        cached = values.astype(np.float32)
    if not np.isfinite(cached).all():
        raise ValueError("Training returns must remain finite in the original Float32 cache")
    dates_int64 = dates.astype(np.int64)
    values = cached.astype(np.float64)
    order = np.argsort(dates_int64, kind="stable")
    ordered_dates = dates_int64[order]
    bounds = np.r_[0, np.flatnonzero(ordered_dates[1:] != ordered_dates[:-1]) + 1, len(dates)]
    centered = np.empty(len(values), dtype=np.float64)
    daily_clipped_std = []
    daily_centered_mean = []
    nearconstant = 0
    for left, right in zip(bounds[:-1], bounds[1:]):
        indices = order[left:right]
        daily = values[indices]
        low, high = np.quantile(daily, [.01, .99], method="linear")
        clipped = np.clip(daily, low, high)
        center = float(clipped.mean(dtype=np.float64))
        scale = float(clipped.std(ddof=0, dtype=np.float64))
        daily_clipped_std.append(scale)
        if scale <= 1e-12:
            residual = np.zeros(len(indices), dtype=np.float64)
            nearconstant += 1
        else:
            residual = clipped - center
        centered[indices] = residual
        daily_centered_mean.append(abs(float(residual.mean(dtype=np.float64))))
    # All training rows count in N, including zero/near-constant dates.
    pooled_rms = float(np.sqrt(np.mean(centered * centered, dtype=np.float64)))
    if not np.isfinite(pooled_rms):
        raise AssertionError("Training-fold RMS unexpectedly became nonfinite")
    pooled_nearconstant = pooled_rms <= 1e-12
    target = (np.zeros(len(centered), dtype=np.float32) if pooled_nearconstant
              else (centered / pooled_rms).astype(np.float32))
    if not np.isfinite(target).all():
        raise AssertionError("Pooled-scale target contains nonfinite values")
    target_means, target_stds = [], []
    for left, right in zip(bounds[:-1], bounds[1:]):
        daily_target = target[order[left:right]].astype(np.float64)
        target_means.append(abs(float(daily_target.mean())))
        target_stds.append(float(daily_target.std(ddof=0)))
    stats = {
        "target_array_sha256": hashlib.sha256(target.tobytes()).hexdigest(),
        "raw_return_float32_sha256": hashlib.sha256(cached.tobytes()).hexdigest(),
        "training_dates_int64_sha256": hashlib.sha256(dates_int64.tobytes()).hexdigest(),
        "centered_float64_sha256": hashlib.sha256(centered.tobytes()).hexdigest(),
        "pooled_rms_float64": pooled_rms,
        "training_days": len(bounds) - 1, "training_rows": len(target),
        "nearconstant_days": nearconstant, "pooled_nearconstant": pooled_nearconstant,
        "max_abs_daily_centered_mean": float(max(daily_centered_mean)),
        "max_abs_daily_target_mean": float(max(target_means)),
        "daily_target_std_min": float(min(target_stds)),
        "daily_target_std_max": float(max(target_stds)),
        "global_target_rms_float64": float(np.sqrt(np.mean(target.astype(np.float64)**2))),
        "target_min": float(target.min()), "target_max": float(target.max()),
        "clipped_std_min": float(min(daily_clipped_std)),
        "clipped_std_max": float(max(daily_clipped_std)),
        "input_dtype": "Float32_promoted_to_Float64", "output_dtype": "Float32",
        "array_hash_encoding": "C-contiguous native-endian bytes; returns Float32, dates Int64, centered Float64, target Float32",
        "scope": "Entire final purged training fold only; all retained rows including nearconstant-day zeros enter pooled RMS; no validation/test labels or counts",
    }
    return target, stats
