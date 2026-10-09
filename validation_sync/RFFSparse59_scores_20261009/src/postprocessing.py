"""Label-independent persistence, rank restoration and auxiliary blending."""
from __future__ import annotations
import numpy as np
from scipy.stats import rankdata
from src.scoring import Panel, add_top_persistence, make_scores, postprocess_scores
BASE_CONFIG = {"alpha": 0.9, "bonus": 0.3, "restore_lower": True, "top_current_weight": 1.0}

def daily_percentiles(panel: Panel, raw: np.ndarray) -> np.ndarray:
    values = np.asarray(raw, dtype=np.float64).reshape(panel.valid_price.shape)
    out = np.full_like(values, -10.0)
    for day in range(len(panel.dates)):
        valid = panel.valid_price[day] & np.isfinite(values[day])
        if valid.any():
            out[day, valid] = rankdata(values[day, valid], method="average") / int(valid.sum())
    return out.reshape(-1)

def make_prediction(panel: Panel, auxiliary_raw: np.ndarray | None, mode: str, weight: float) -> np.ndarray:
    """Construct predictions without reading returns or label availability.

    full_signal blends daily valid-price percentile ranks, then applies the
    production postprocessor. top_only retains the baseline's entire state,
    lower ordering and protected membership, mixing percentile ranks computed
    *within* the protected upper block. Ambiguous boundaries or invalid Top
    observations fall back to the production output for that complete day.
    """
    if not np.isfinite(weight) or not 0 <= weight <= 1:
        raise ValueError("weight must be in [0, 1]")
    base_raw = panel.frame["pred_raw"].to_numpy().astype(np.float64)
    if mode == "baseline":
        return postprocess_scores(panel, base_raw, **BASE_CONFIG)
    if mode not in {"pure", "full_signal", "top_only"}:
        raise ValueError(f"Unknown mode: {mode}")
    if auxiliary_raw is None:
        raise ValueError(f"Auxiliary predictions are required for {mode}")
    auxiliary_raw = np.asarray(auxiliary_raw, dtype=np.float64)
    if auxiliary_raw.size != base_raw.size:
        raise ValueError("Auxiliary prediction size does not match baseline")
    if mode == "pure":
        return postprocess_scores(panel, auxiliary_raw, **BASE_CONFIG)
    if mode == "full_signal":
        mixed = ((1 - weight) * daily_percentiles(panel, base_raw)
                 + weight * daily_percentiles(panel, auxiliary_raw))
        return postprocess_scores(panel, mixed, **BASE_CONFIG)

    out = postprocess_scores(panel, base_raw, **BASE_CONFIG).reshape(panel.valid_price.shape)
    stable = add_top_persistence(panel, make_scores(panel, base_raw, BASE_CONFIG["alpha"]),
                                 BASE_CONFIG["bonus"]).reshape(panel.valid_price.shape)
    base_raw = base_raw.reshape(panel.valid_price.shape)
    auxiliary_raw = auxiliary_raw.reshape(panel.valid_price.shape)
    for day in range(len(panel.dates)):
        valid = panel.valid_price[day] & np.isfinite(base_raw[day])
        indices = np.flatnonzero(panel.up[day] == 0)
        n_top = max(len(indices) // 10, 1)
        if not len(indices) or not valid.any():
            continue
        top = indices[np.argsort(-stable[day, indices], kind="stable")[:n_top]]
        if not valid[top].all():
            continue
        protected = valid & (stable[day] >= stable[day, top].min())
        if np.count_nonzero(protected & (panel.up[day] == 0)) != n_top:
            continue
        if not np.isfinite(auxiliary_raw[day, protected]).all():
            continue
        n_upper = int(protected.sum())
        base_rank = rankdata(base_raw[day, protected], method="average") / n_upper
        auxiliary_rank = rankdata(auxiliary_raw[day, protected], method="average") / n_upper
        blended_rank = rankdata((1 - weight) * base_rank + weight * auxiliary_rank, method="average")
        n_valid = int(valid.sum())
        out[day, protected] = (n_valid - n_upper + blended_rank) / n_valid
    return out.reshape(-1)
