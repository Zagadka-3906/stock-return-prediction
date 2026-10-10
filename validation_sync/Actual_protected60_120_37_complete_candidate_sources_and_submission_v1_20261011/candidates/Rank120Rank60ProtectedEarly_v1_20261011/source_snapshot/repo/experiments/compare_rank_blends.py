"""Compare predeclared model blends on 2022–2023 only."""

from __future__ import annotations

import json

import numpy as np
import polars as pl

from run import ROOT
from src.scoring import Panel, add_top_persistence, make_scores, score


OUT = ROOT / "experiments" / "ranking_eval"
ALPHA = 0.95
BONUS = 0.15
WEIGHTS = (0.0, 0.1, 0.25, 0.5, 0.75, 1.0)
CANDIDATES = {
    "xgboost": "xgboost_linear_ndcg_{year}_80round.parquet",
    "lambdarank": "lightgbm_lambdarank_{year}_80round.parquet",
}


def main() -> None:
    results: dict[str, dict] = {}
    for name, pattern in CANDIDATES.items():
        by_year = {}
        for year in (2022, 2023):
            base = pl.read_parquet(ROOT / "validation" / f"fold_{year}.parquet").sort("trade_date", "ts_code")
            other = pl.read_parquet(OUT / pattern.format(year=year)).sort("trade_date", "ts_code")
            if not base.select("ts_code", "trade_date").equals(other.select("ts_code", "trade_date")):
                raise AssertionError(f"{name} {year}: key mismatch")
            panel = Panel.from_frame(base)
            model = make_scores(panel, base["pred_raw"].to_numpy(), ALPHA)
            candidate = make_scores(panel, other["pred_raw"].to_numpy(), ALPHA)
            by_year[str(year)] = {}
            for weight in WEIGHTS:
                blended = (1.0 - weight) * model + weight * candidate
                metrics, _ = score(panel, add_top_persistence(panel, blended, BONUS))
                by_year[str(year)][str(weight)] = metrics
                print(f"{name} {year} weight={weight:.2f} score={metrics['final_score']:.6f}", flush=True)
        summary = {}
        for weight in WEIGHTS:
            scores = [by_year[str(year)][str(weight)]["final_score"] for year in (2022, 2023)]
            summary[str(weight)] = {"worst": min(scores), "mean": float(np.mean(scores))}
        selected = max(WEIGHTS, key=lambda w: summary[str(w)]["worst"])
        results[name] = {"years": by_year, "summary": summary, "selected_weight": selected}
        print(f"SELECTED {name} weight={selected:.2f} worst={summary[str(selected)]['worst']:.6f}", flush=True)
    (OUT / "blend_development_2022_2023.json").write_text(
        json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
