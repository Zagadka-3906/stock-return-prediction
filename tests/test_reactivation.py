"""Regression test for a stock resuming trading after a missing price."""

import sys
from pathlib import Path

import numpy as np
import polars as pl

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from src.scoring import Panel, make_scores  # noqa: E402


frame = pl.DataFrame({
    "ts_code": ["A", "B", "A", "B"],
    "trade_date": [20240102, 20240102, 20240103, 20240103],
    "y_ret_1d": [0.0, None, 0.0, 0.0],
    "flag_limit_up": [0, 0, 0, 0],
    "price_valid": [True, False, True, True],
})
panel = Panel.from_frame(frame)
scores = make_scores(panel, np.array([0.2, -1e6, 0.1, 0.3]), alpha=0.95)
assert scores[1] == -10.0
assert scores[3] == 1.0, "The resumed stock must start from its current-day rank"
print("Reactivation smoothing test passed")
