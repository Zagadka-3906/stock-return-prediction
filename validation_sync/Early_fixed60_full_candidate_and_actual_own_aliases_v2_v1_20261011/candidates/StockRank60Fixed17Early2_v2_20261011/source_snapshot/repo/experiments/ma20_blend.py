"""Select a small MA20/model rank blend on 2022–2023, without touching 2024."""

from __future__ import annotations

import json

import numpy as np
import polars as pl

from run import ROOT
from src.scoring import Panel, add_top_persistence, make_scores, score


OUT = ROOT / "experiments" / "next_steps_eval"
WEIGHTS = (0.0, 0.02, 0.05, 0.10, 0.20, 0.25, 0.50, 0.75, 1.0)
ALPHA = 0.95
BONUS = 0.15


def main() -> None:
    yearly = {}
    for year in (2022, 2023):
        frame = pl.read_parquet(ROOT / "validation" / f"fold_{year}.parquet")
        panel = Panel.from_frame(frame)
        model = make_scores(panel, panel.frame["pred_raw"].to_numpy(), ALPHA)
        ma20 = make_scores(panel, panel.frame["MA20"].fill_null(-1e6).to_numpy(), ALPHA)
        yearly[str(year)] = {}
        for weight in WEIGHTS:
            candidate = add_top_persistence(panel, (1 - weight) * model + weight * ma20, BONUS)
            metrics, _ = score(panel, candidate)
            yearly[str(year)][str(weight)] = metrics
            print(f"{year} MA20={weight:.2f} score={metrics['final_score']:.6f}", flush=True)
    summary = {
        str(weight): {
            "worst": min(yearly[str(year)][str(weight)]["final_score"] for year in (2022, 2023)),
            "mean": float(np.mean([yearly[str(year)][str(weight)]["final_score"] for year in (2022, 2023)])),
        }
        for weight in WEIGHTS
    }
    selected = max(WEIGHTS, key=lambda weight: summary[str(weight)]["worst"])
    result = {"alpha": ALPHA, "bonus": BONUS, "selection_years": [2022, 2023],
              "years": yearly, "summary": summary, "selected_weight": selected}
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "ma20_blend_2022_2023.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(f"SELECTED MA20={selected:.2f} worst={summary[str(selected)]['worst']:.6f}", flush=True)


if __name__ == "__main__":
    main()
