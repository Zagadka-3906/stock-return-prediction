"""Check the preselected recent-weighted 2024 candidate with organizer evaluate.py."""

from __future__ import annotations

import json
from pathlib import Path
import tempfile

import polars as pl

from evaluate import evaluate
from run import ROOT
from src.scoring import Panel, add_top_persistence, make_scores, score


def main() -> None:
    fold = pl.read_parquet(ROOT / "validation" / "fold_2024.parquet").sort("trade_date", "ts_code")
    candidate = pl.read_parquet(ROOT / "experiments" / "next_steps_eval" / "recent2x_2024.parquet").sort("trade_date", "ts_code")
    if not fold.select("ts_code", "trade_date").equals(candidate.select("ts_code", "trade_date")):
        raise AssertionError("Candidate keys do not match the baseline validation fold")
    panel = Panel.from_frame(fold)
    pred = add_top_persistence(panel, make_scores(panel, candidate["pred_raw"].to_numpy(), 0.95), 0.15)
    ours, _ = score(panel, pred)
    original_y = (
        pl.scan_csv(ROOT / "data" / "raw" / "训练集.csv", schema_overrides={
            "ts_code": pl.String, "trade_date": pl.Int32, "y_ret_1d": pl.Float64,
        }, null_values=["NaN", "nan", ""])
        .filter(pl.col("trade_date").is_between(20240101, 20241231))
        .select("ts_code", "trade_date", "y_ret_1d")
        .collect()
    )
    keys = panel.frame.select("ts_code", "trade_date")
    exact_y = keys.join(original_y, on=["ts_code", "trade_date"], how="left", validate="1:1").sort("trade_date", "ts_code")
    if exact_y["y_ret_1d"].null_count() != panel.frame["y_ret_1d"].null_count():
        raise AssertionError("Original and cached labels have different missing counts")
    with tempfile.TemporaryDirectory(prefix="next-steps-official-") as tmp:
        directory = Path(tmp)
        keys.with_columns(pl.Series("pred", pred)).write_csv(directory / "submission.csv", float_precision=17)
        keys.with_columns(exact_y["y_ret_1d"]).write_csv(directory / "测试集_Y.csv", float_precision=17)
        keys.with_columns(panel.frame["flag_limit_up"]).write_csv(directory / "测试集_X.csv")
        official = {key: float(value) for key, value in evaluate(str(directory / "submission.csv"), str(directory)).items()}
    differences = {name: abs(ours[name] - official[name]) for name in official}
    if differences["final_score"] > 1e-5 or differences["mean_turnover"] > 1e-10:
        raise AssertionError(f"Candidate scoring diverges from organizer: {differences}")
    result = {"project_scorer": ours, "organizer_scorer": official, "absolute_differences": differences,
              "uses_original_float64_labels": True}
    target = ROOT / "experiments" / "next_steps_eval" / "recent2x_2024_official.json"
    target.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Official score={official['final_score']:.9f}; project score={ours['final_score']:.9f}; "
          f"delta={differences['final_score']:.9g}", flush=True)


if __name__ == "__main__":
    main()
