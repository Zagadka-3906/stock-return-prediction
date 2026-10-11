"""Historical quantile diagnostics and Newey-West mean uncertainty."""
from __future__ import annotations
import math
import numpy as np
from scipy.stats import spearmanr
from src.scoring import Panel

def hac_stats(values: np.ndarray, lags: int | None = None) -> dict:
    """Newey-West mean SE, Bartlett weights, denominator T for autocovariance.

    Lag default floor(4*(T/100)^(2/9)); normal-approximation intervals.
    This tests the unconditional mean and does not correct model selection.
    """
    x = np.asarray(values, dtype=float)
    x = x[np.isfinite(x)]
    n = len(x)
    if n < 2:
        return {"n": n, "mean": float(x.mean()) if n else None}
    lag = min(n - 1, max(0, int(math.floor(4 * (n / 100) ** (2 / 9))) if lags is None else lags))
    mean = float(x.mean())
    centered = x - mean
    lrv = float(centered @ centered) / n
    for k in range(1, lag + 1):
        gamma = float(centered[k:] @ centered[:-k]) / n
        lrv += 2 * (1 - k / (lag + 1)) * gamma
    se = math.sqrt(max(0, lrv) / n)
    return {
        "n": n, "lags": lag, "mean": mean, "hac_se": se,
        "hac_t": mean / se if se > 0 else None,
        "normal_95_ci": [mean - 1.96 * se, mean + 1.96 * se],
    }

def quantile_stats(panel: Panel, predictions: np.ndarray) -> dict:
    pred = predictions.reshape(len(panel.dates), panel.rows_per_day)
    quantiles, markets = [], []
    for i in range(len(panel.dates)):
        eligible = np.isfinite(panel.y[i]) & (panel.up[i] == 0)
        returns = panel.y[i, eligible]
        if len(returns) < 100:
            continue
        descending = np.argsort(-pred[i, eligible], kind="stable")
        ordered = returns[descending]
        # The first group is exactly floor(n/10), matching the official Top 10%.
        edges = np.floor(np.linspace(0, len(ordered), 11)).astype(int)
        high_to_low = [float(ordered[edges[k]:edges[k + 1]].mean()) for k in range(10)]
        quantiles.append(high_to_low[::-1])
        markets.append(float(returns.mean()))
    q = np.asarray(quantiles)
    market = np.asarray(markets)
    means = q.mean(axis=0)
    excess = q[:, -1] - market
    return {
        "eligible_rule": "flag_limit_up == 0 and finite y_ret_1d; split within each date; equal-weight days",
        "days": len(q), "mean_daily_returns": means.tolist(),
        "market_mean_daily_return": float(market.mean()),
        "quantile_mean_spearman": float(spearmanr(np.arange(1, 11), means).statistic),
        "positive_adjacent_differences": int((np.diff(means) > 0).sum()),
        "top_minus_market": hac_stats(excess),
        "top_minus_bottom": hac_stats(q[:, -1] - q[:, 0]),
        "top_minus_market_lag_sensitivity": {str(l): hac_stats(excess, l) for l in (5, 10, 20)},
    }
