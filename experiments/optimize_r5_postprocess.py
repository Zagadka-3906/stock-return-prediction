"""Two fixed r5 postprocessing candidates; synthetic tests only in this module.

No labels are accessed when constructing predictions. This file does not score
historical data, select parameters, write a protocol, or modify any release.
"""
from __future__ import annotations

import os
for _thread_var in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "POLARS_MAX_THREADS"):
    os.environ[_thread_var] = str(min(int(os.environ.get(_thread_var, "8")), 8))

import json
from pathlib import Path
import sys

import numpy as np
import polars as pl

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.scoring import Panel, add_top_persistence, make_scores  # noqa: E402
from experiments.final_sweep import blend_top_only  # noqa: E402


CANDIDATES = {
    "stale_decay": {
        "key": "stale_decay", "alpha": 0.9, "bonus": 0.3,
        "support_percentile": 0.8, "grace_days": 3, "half_life_days": 10,
        "pooled_weight": 0.25,
        "formula": "streak_t = streak_(t-1)+1 iff valid_t and r_t<0.8, else 0; "
                   "b_t=0.3*2**(-max(streak_t-3,0)/10); s_t=EMA0.9(r)_t+b_t*prior_top_t",
    },
    "downside_ema": {
        "key": "downside_ema", "alpha": 0.9, "downside_alpha": 0.7,
        "gap": 0.2, "confirmation_days": 2, "bonus": 0.3, "pooled_weight": 0.25,
        "formula": "weak_t = valid_t and valid_(t-1) and r_t<=EMA_(t-1)-0.2; "
                   "streak_t=streak_(t-1)+1 iff weak_t else 0; "
                   "alpha_t=0.7 iff streak_t>=2 else 0.9; "
                   "EMA_t=(1-alpha_t)*r_t+alpha_t*EMA_(t-1)",
    },
}


def retention_bonus(streak: np.ndarray) -> np.ndarray:
    """Streak includes today; days 1-3 keep .3, day 13 is the first half."""
    return 0.3 * np.exp2(-np.maximum(np.asarray(streak, dtype=float) - 3, 0) / 10)


def stale_stable(panel: Panel, raw: np.ndarray) -> tuple[np.ndarray, dict]:
    shape = panel.valid_price.shape
    ranked = make_scores(panel, raw, 0.0).reshape(shape)
    smoothed = make_scores(panel, raw, 0.9).reshape(shape)
    valid = panel.valid_price & np.isfinite(np.asarray(raw).reshape(shape))
    out = smoothed.copy()
    streaks = np.zeros(shape, dtype=np.int32)
    bonuses = np.zeros(shape, dtype=float)
    streak = np.zeros(panel.rows_per_day, dtype=np.int32)
    previous_top = np.zeros(panel.rows_per_day, dtype=bool)
    for day in range(len(panel.dates)):
        streak = np.where(valid[day] & (ranked[day] < .8), streak + 1, 0)
        bonus = retention_bonus(streak)
        applied = previous_top & valid[day]
        out[day, applied] += bonus[applied]
        out[day, ~valid[day]] = -10.0
        streaks[day] = streak
        bonuses[day, applied] = bonus[applied]
        tradeable = panel.up[day] == 0
        previous_top[:] = False
        count = int(tradeable.sum())
        if count >= 100:
            indices = np.flatnonzero(tradeable)
            selected = np.argsort(-out[day, indices], kind="stable")[:max(count // 10, 1)]
            previous_top[indices[selected]] = True
    return out.reshape(-1), {"streak": streaks, "applied_bonus": bonuses}


def downside_smoothing(panel: Panel, raw: np.ndarray) -> tuple[np.ndarray, dict]:
    shape = panel.valid_price.shape
    ranked = make_scores(panel, raw, 0.0).reshape(shape)
    valid = panel.valid_price & np.isfinite(np.asarray(raw).reshape(shape))
    out = np.full(shape, -10.0, dtype=float)
    alphas = np.full(shape, .9, dtype=float)
    streaks = np.zeros(shape, dtype=np.int32)
    streak = np.zeros(panel.rows_per_day, dtype=np.int32)
    for day in range(len(panel.dates)):
        if day == 0:
            out[day] = ranked[day]
            continue
        previous = out[day - 1]
        continuing = valid[day] & valid[day - 1]
        weak = continuing & (ranked[day] <= previous - .2)
        streak = np.where(weak, streak + 1, 0)
        alpha = np.where(streak >= 2, .7, .9)
        score = np.where(continuing, (1 - alpha) * ranked[day] + alpha * previous, ranked[day])
        score[~valid[day]] = -10.0
        out[day], alphas[day], streaks[day] = score, alpha, streak
    return out.reshape(-1), {"streak": streaks, "alpha": alphas}


def candidate_prediction(panel: Panel, raw: np.ndarray, aux: np.ndarray, key: str) -> np.ndarray:
    """Return the same unscaled rank-score format as cached_recheck.make_prediction.

    The released protected-block restoration and pooled .25 blend are reused
    exactly. Only the EMA rule or the prior-Top bonus changes, never both.
    State uses each candidate's own previous tradable Top, before restoration.
    """
    if key not in CANDIDATES:
        raise ValueError(f"Unknown r5 postprocess candidate: {key}")
    raw = np.asarray(raw, dtype=float).reshape(-1)
    aux = np.asarray(aux, dtype=float).reshape(-1)
    if len(raw) != len(panel.frame) or len(aux) != len(panel.frame):
        raise ValueError("Prediction arrays must align with every panel row")
    if key == "stale_decay":
        stable, _ = stale_stable(panel, raw)
    else:
        smoothed, _ = downside_smoothing(panel, raw)
        stable = add_top_persistence(panel, smoothed, .3)
    return blend_top_only(panel, stable, raw, aux, .25)


def synthetic_tests() -> dict:
    days, stocks = 18, 200
    raw = np.tile(np.arange(stocks, dtype=float), (days, 1))
    # A former leader weakens for two consecutive days; B pauses and resumes.
    raw[1:15, -1] = -1
    valid = np.ones((days, stocks), dtype=bool)
    valid[4:6, -2] = False
    up = np.zeros((days, stocks), dtype=np.int8)
    up[3, -3] = 1
    # One day has fewer than 100 tradeable names, exercising the state reset.
    up[10, :120] = 1
    aux = np.random.default_rng(260926).normal(size=raw.shape)
    frame = pl.DataFrame({
        "ts_code": [f"S{s:03d}" for _ in range(days) for s in range(stocks)],
        "trade_date": np.repeat(np.arange(20240101, 20240101 + days), stocks),
        "flag_limit_up": up.ravel(), "price_valid": valid.ravel(),
        "y_ret_1d": np.zeros(days * stocks), "pred_raw": raw.ravel(),
    })
    panel = Panel.from_frame(frame)
    changed = Panel.from_frame(frame.with_columns(pl.Series("y_ret_1d", np.full(days * stocks, np.nan))))
    shortened = Panel.from_frame(frame.head(stocks * 12))
    outcomes = {}
    for key in CANDIDATES:
        pred = candidate_prediction(panel, raw.ravel(), aux.ravel(), key)
        assert np.isfinite(pred).all()
        assert (pred.reshape(raw.shape)[~valid] < -1).all()
        assert np.array_equal(pred, candidate_prediction(changed, raw.ravel(), aux.ravel(), key))
        prefix = candidate_prediction(shortened, raw[:12].ravel(), aux[:12].ravel(), key)
        assert np.array_equal(prefix, pred[:stocks * 12])
        outcomes[key] = {"finite": True, "invalid_below_minus_one": True,
                         "label_perturbation_exact": True, "prefix_12_days_exact": True}
    b = retention_bonus(np.array([0, 1, 2, 3, 4, 13, 23]))
    assert np.array_equal(b[:4], np.full(4, .3))
    assert b[4] < .3 and b[5] == .15 and b[6] == .075
    stable, stale = stale_stable(panel, raw.ravel())
    assert np.array_equal(stale["streak"][:5, -1], np.array([0, 1, 2, 3, 4]))
    assert stale["streak"][4, -2] == stale["streak"][5, -2] == 0
    # Invalid state resets and full-strength support resets only from current rank.
    assert stale["streak"][15, -1] == 0
    assert not stale["applied_bonus"][11].any()
    smooth, downside = downside_smoothing(panel, raw.ravel())
    smooth = smooth.reshape(raw.shape)
    rank = make_scores(panel, raw.ravel(), 0).reshape(raw.shape)
    assert downside["streak"][1, -1] == 1 and downside["alpha"][1, -1] == .9
    assert downside["streak"][2, -1] == 2 and downside["alpha"][2, -1] == .7
    assert np.isclose(smooth[2, -1], .3 * rank[2, -1] + .7 * smooth[1, -1])
    assert smooth[6, -2] == rank[6, -2] and downside["streak"][6, -2] == 0
    assert downside["streak"][15, -1] == 0 and downside["alpha"][15, -1] == .9
    assert np.array_equal(smooth[:, 30], make_scores(panel, raw.ravel(), .9).reshape(raw.shape)[:, 30])
    try:
        candidate_prediction(panel, raw.ravel(), aux.ravel(), "unknown")
    except ValueError:
        pass
    else:
        raise AssertionError("Unknown candidate accepted")
    return {"status": "passed", "candidates": outcomes,
            "stale_three_day_grace_and_ten_day_halflife": True,
            "stale_today_updated_before_bonus": True, "below100_tradeable_resets_top_state": True,
            "downside_two_day_confirmation": True, "downside_uses_previous_candidate_ema": True,
            "failed_condition_resets_streak": True, "invalid_and_resumption_reset": True,
            "untriggered_ema_matches_released": True, "historical_labels_scored": False}


if __name__ == "__main__":
    print(json.dumps(synthetic_tests(), indent=2))
