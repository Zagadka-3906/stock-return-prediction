"""Compare our validation scorer against the organizer's original script."""

from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path

import numpy as np
import polars as pl

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from evaluate import evaluate  # noqa: E402
from src.scoring import Panel, make_scores, score  # noqa: E402


def main() -> None:
    fold = pl.read_parquet(ROOT / "validation" / "fold_2024.parquet")
    dates = fold.get_column("trade_date").unique().sort().head(10).to_list()
    fold = fold.filter(pl.col("trade_date").is_in(dates)).sort("trade_date", "ts_code")
    panel = Panel.from_frame(fold)
    alpha = json.loads((ROOT / "validation" / "metrics.json").read_text(encoding="utf-8"))["selected_alpha"]
    predictions = make_scores(panel, panel.frame.get_column("pred_raw").to_numpy(), alpha)
    ours, _ = score(panel, predictions)
    keys = panel.frame.select("ts_code", "trade_date")
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp)
        keys.with_columns(pl.Series("pred", predictions)).write_csv(path / "submission.csv", float_precision=14)
        keys.with_columns(panel.frame.get_column("y_ret_1d")).write_csv(path / "测试集_Y.csv", float_precision=14)
        keys.with_columns(panel.frame.get_column("flag_limit_up")).write_csv(path / "测试集_X.csv")
        official = evaluate(str(path / "submission.csv"), str(path))
    differences = {}
    for name in ("ic_mean", "ic_std", "icir", "ic_positive_ratio", "annual_excess", "top1_annual_ret", "mean_turnover", "final_score"):
        differences[name] = abs(ours[name] - official[name])
        print(f"{name}: ours={ours[name]:.12f}; official={official[name]:.12f}; abs_diff={differences[name]:.12g}")
    if differences["final_score"] > 1e-5 or differences["mean_turnover"] > 1e-10:
        raise AssertionError("Competition scorer differs materially from official evaluate.py")
    print("The organizer's evaluate.py agrees within CSV rounding tolerance on ten full trading days.")


if __name__ == "__main__":
    main()
