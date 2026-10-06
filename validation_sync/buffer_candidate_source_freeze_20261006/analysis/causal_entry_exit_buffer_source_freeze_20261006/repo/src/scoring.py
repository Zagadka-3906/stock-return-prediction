"""Validation scorer matching the supplied evaluate.py on complete daily panels."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import polars as pl
from scipy.stats import rankdata, spearmanr


@dataclass
class Panel:
    frame: pl.DataFrame
    dates: np.ndarray
    codes: np.ndarray
    y: np.ndarray
    up: np.ndarray
    valid_price: np.ndarray
    rows_per_day: int

    @classmethod
    def from_frame(cls, frame: pl.DataFrame) -> "Panel":
        frame = frame.sort("trade_date", "ts_code")
        dates = frame.get_column("trade_date").unique(maintain_order=True).to_numpy()
        codes = frame.get_column("ts_code").to_numpy()
        n = len(codes) // len(dates)
        if len(codes) != len(dates) * n:
            raise ValueError("Panel is not rectangular")
        if not np.all(codes.reshape(len(dates), n) == codes[:n]):
            raise ValueError("Stock order differs across dates")
        return cls(
            frame=frame,
            dates=dates,
            codes=codes[:n],
            y=frame.get_column("y_ret_1d").to_numpy().reshape(len(dates), n),
            up=frame.get_column("flag_limit_up").to_numpy().reshape(len(dates), n),
            valid_price=frame.get_column("price_valid").to_numpy().reshape(len(dates), n),
            rows_per_day=n,
        )


def make_scores(panel: Panel, raw: np.ndarray, alpha: float) -> np.ndarray:
    """Rank each day, then smooth each symbol using information through day t."""
    if not 0 <= alpha < 1:
        raise ValueError("alpha must be in [0, 1)")
    p = np.asarray(raw, dtype=np.float64).reshape(len(panel.dates), panel.rows_per_day)
    out = np.empty_like(p)
    previous = None
    previous_valid = None
    for i in range(len(panel.dates)):
        valid = panel.valid_price[i] & np.isfinite(p[i])
        rank = np.full(panel.rows_per_day, -10.0)
        count = int(valid.sum())
        if count:
            rank[valid] = rankdata(p[i, valid], method="average") / count
        if previous is None:
            score = rank
        else:
            score = np.where(previous_valid, (1 - alpha) * rank + alpha * previous, rank)
        score[~valid] = -10.0
        out[i] = score
        previous = score
        previous_valid = valid
    return out.reshape(-1)


def add_top_persistence(panel: Panel, smoothed: np.ndarray, bonus: float) -> np.ndarray:
    """Add a causal retention bonus to yesterday's tradeable Top 10%.

    The prior Top list is formed using only prior-day scores and the prior-day
    limit-up flag, exactly as in the competition's turnover rule. No labels
    or future observations enter this transform.
    """
    if not np.isfinite(bonus) or bonus < 0:
        raise ValueError("bonus must be finite and non-negative")
    base = np.asarray(smoothed, dtype=np.float64).reshape(len(panel.dates), panel.rows_per_day)
    out = base.copy()
    prior_top = np.zeros(panel.rows_per_day, dtype=bool)
    for day in range(len(panel.dates)):
        out[day, prior_top] += bonus
        tradeable = panel.up[day] == 0
        count = int(tradeable.sum())
        if count < 100:
            prior_top[:] = False
            continue
        eligible_indices = np.flatnonzero(tradeable)
        selected = np.argsort(-out[day, tradeable], kind="stable")[: max(count // 10, 1)]
        prior_top[:] = False
        prior_top[eligible_indices[selected]] = True
    return out.reshape(-1)


def restore_lower_ranks(panel: Panel, stable: np.ndarray, raw: np.ndarray,
                        top_current_weight: float = 0.0) -> np.ndarray:
    """Protect the stable tradable Top set; use current ranks below its cutoff.

    The transform reads only current/past features, predictions and limit flags.
    It never reads returns or their availability. A positive top_current_weight
    blends current ranks into the protected block's internal ordering, without
    feeding that ordering back into the historical persistence state. At a tied
    Top boundary the internal reorder is skipped to preserve Top membership.
    """
    if not np.isfinite(top_current_weight) or not 0 <= top_current_weight <= 1:
        raise ValueError("top_current_weight must be in [0, 1]")
    stable = np.asarray(stable, dtype=float).reshape(panel.valid_price.shape)
    raw = np.asarray(raw, dtype=float).reshape(panel.valid_price.shape)
    out = np.full_like(stable, -10.0)
    for day in range(len(panel.dates)):
        valid = panel.valid_price[day] & np.isfinite(raw[day])
        indices = np.flatnonzero(panel.up[day] == 0)
        n_top = max(len(indices) // 10, 1)
        if not len(indices) or not valid.any():
            out[day] = stable[day]
            continue
        top = indices[np.argsort(-stable[day, indices], kind="stable")[:n_top]]
        if not valid[top].all():
            out[day] = stable[day]
            continue
        protected = valid & (stable[day] >= stable[day, top].min())
        lower = valid & ~protected
        n_valid, n_lower = int(valid.sum()), int(lower.sum())
        out[day, lower] = rankdata(raw[day, lower], method="average") / n_valid
        upper_rank = rankdata(stable[day, protected], method="average")
        if top_current_weight and np.count_nonzero(protected & (panel.up[day] == 0)) == n_top:
            current_rank = rankdata(raw[day, protected], method="average")
            mixed = (1 - top_current_weight) * upper_rank + top_current_weight * current_rank
            upper_rank = rankdata(mixed, method="average")
        out[day, protected] = (n_lower + upper_rank) / n_valid
    return out.reshape(-1)


def postprocess_scores(panel: Panel, raw: np.ndarray, alpha: float, bonus: float,
                       restore_lower: bool = False, top_current_weight: float = 0.0) -> np.ndarray:
    if not np.isfinite(top_current_weight) or not 0 <= top_current_weight <= 1:
        raise ValueError("top_current_weight must be in [0, 1]")
    if top_current_weight and not restore_lower:
        raise ValueError("Top reordering requires protected rank restoration")
    stable = add_top_persistence(panel, make_scores(panel, raw, alpha), bonus)
    return restore_lower_ranks(panel, stable, raw, top_current_weight) if restore_lower else stable


def score(panel: Panel, predictions: np.ndarray) -> tuple[dict, pl.DataFrame]:
    """Replicate the official IC, Top 10% excess, and Jaccard turnover."""
    p = np.asarray(predictions, dtype=np.float64).reshape(len(panel.dates), panel.rows_per_day)
    if not np.isfinite(p).all():
        raise ValueError("Predictions contain NaN or infinity")
    ic_values, excess_values, top_values, turnovers, details = [], [], [], [], []
    prev_top = None
    for i, date in enumerate(panel.dates):
        y = panel.y[i]
        pred = p[i]
        valid_y = np.isfinite(y)
        ic = np.nan
        if valid_y.sum() >= 30:
            ic = float(spearmanr(pred[valid_y], y[valid_y]).statistic)
            ic_values.append(ic)
        eligible = (panel.up[i] == 0) & valid_y
        excess = top_return = np.nan
        if eligible.sum() >= 100:
            order = np.argsort(-pred[eligible], kind="stable")
            returns = y[eligible]
            n_top = max(len(returns) // 10, 1)
            top_return = float(returns[order[:n_top]].mean())
            excess = top_return - float(returns.mean())
            excess_values.append(excess)
            top_values.append(top_return)
        # The official turnover code does not remove rows whose label is null.
        tradeable = panel.up[i] == 0
        turnover = np.nan
        if tradeable.sum() < 100:
            prev_top = None
        else:
            codes = panel.codes[tradeable]
            order = np.argsort(-pred[tradeable], kind="stable")
            curr_top = set(codes[order[:max(len(codes) // 10, 1)]])
            if prev_top:
                turnover = 1 - len(curr_top & prev_top) / len(curr_top | prev_top)
                turnovers.append(turnover)
            prev_top = curr_top
        details.append((int(date), ic, excess, top_return, turnover))
    ic_arr = np.asarray(ic_values)
    mean_ic = float(ic_arr.mean())
    ic_std = float(ic_arr.std(ddof=1))
    annual_excess = float(np.mean(excess_values) * 252)
    mean_turnover = float(np.mean(turnovers))
    metrics = {
        "ic_mean": mean_ic,
        "ic_std": ic_std,
        "icir": mean_ic / ic_std if ic_std > 0 else 0.0,
        "ic_positive_ratio": float((ic_arr > 0).mean()),
        "annual_excess": annual_excess,
        "top1_annual_ret": float(np.mean(top_values) * 252),
        "mean_turnover": mean_turnover,
        "final_score": mean_ic * 0.4 + annual_excess * 0.3 + (1 - mean_turnover) * 0.3,
        "ic_days": len(ic_values),
        "excess_days": len(excess_values),
        "turnover_days": len(turnovers),
    }
    daily = pl.DataFrame(details, schema=["trade_date", "rank_ic", "excess", "top1_return", "turnover"], orient="row")
    return metrics, daily
