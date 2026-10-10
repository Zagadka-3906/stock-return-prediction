"""Check the preselected 25% XGBoost blend on inspected 2024 data."""

from __future__ import annotations

import json

import polars as pl

from run import ROOT
from src.scoring import Panel, add_top_persistence, make_scores, score


def main() -> None:
    year = 2024
    weight = 0.25
    alpha = 0.95
    bonus = 0.15
    base = pl.read_parquet(ROOT / "validation" / f"fold_{year}.parquet").sort("trade_date", "ts_code")
    alt = pl.read_parquet(ROOT / "experiments" / "ranking_eval" /
                          "xgboost_linear_ndcg_2024_80round.parquet").sort("trade_date", "ts_code")
    if not base.select("ts_code", "trade_date").equals(alt.select("ts_code", "trade_date")):
        raise AssertionError("Validation keys differ")
    panel = Panel.from_frame(base)
    base_smoothed = make_scores(panel, base["pred_raw"].to_numpy(), alpha)
    alt_smoothed = make_scores(panel, alt["pred_raw"].to_numpy(), alpha)
    blend = (1.0 - weight) * base_smoothed + weight * alt_smoothed
    metrics, _ = score(panel, add_top_persistence(panel, blend, bonus))
    out = {"year": year, "weight_selected_on": [2022, 2023], "weight": weight,
           "alpha": alpha, "bonus": bonus, "metrics": metrics}
    path = ROOT / "experiments" / "ranking_eval" / "xgb_blend_2024.json"
    path.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(out, ensure_ascii=False, indent=2), flush=True)


if __name__ == "__main__":
    main()
