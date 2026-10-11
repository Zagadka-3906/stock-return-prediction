"""Development-only choice of current-signal weight within protected Top ranks."""
from __future__ import annotations

import argparse
import json

from experiments.protected_top import load_panel
from run import ROOT
from src.scoring import Panel, postprocess_scores, score

OUT = ROOT / "experiments" / "top_internal_eval"
WEIGHTS = (0.0, 0.5, 1.0)


def predictions(panel: Panel, weight: float):
    raw = panel.frame["pred_raw"].to_numpy()
    return postprocess_scores(panel, raw, .9, .3, True, weight)


def develop() -> None:
    results = {str(weight): {"weight": weight, "years": {}} for weight in WEIGHTS}
    for year in (2022, 2023):
        panel = load_panel(year)
        for weight in WEIGHTS:
            metrics, _ = score(panel, predictions(panel, weight))
            results[str(weight)]["years"][str(year)] = metrics
            print(f"{year} weight={weight}: {json.dumps(metrics)}", flush=True)
    for result in results.values():
        result["minimum_annual_score"] = min(m["final_score"] for m in result["years"].values())
    key = max(results, key=lambda k: results[k]["minimum_annual_score"])
    output = {"selection_years": [2022, 2023], "selection_rule": "maximize_minimum_annual_score",
              "fixed_alpha": .9, "fixed_bonus": .3, "selected_weight": results[key]["weight"],
              "candidates": results,
              "caveat": "Sequential exploratory selection; 2024 is historical diagnosis, not an untouched holdout."}
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "development.json").write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"SELECTED weight={output['selected_weight']}", flush=True)


def diagnose() -> None:
    dev = json.loads((OUT / "development.json").read_text(encoding="utf-8"))
    panel = load_panel(2024)
    pred = predictions(panel, dev["selected_weight"])
    metrics, daily = score(panel, pred)
    baseline, _ = score(panel, predictions(panel, 0.0))
    result = {"selected_weight": dev["selected_weight"], "metrics": metrics, "baseline": baseline,
              "delta": metrics["final_score"] - baseline["final_score"]}
    (OUT / "diagnostic_2024.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    daily.write_csv(OUT / "selected_2024_daily.csv")
    print(json.dumps(result, ensure_ascii=False, indent=2), flush=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("stage", choices=("develop", "diagnose"))
    args = parser.parse_args()
    develop() if args.stage == "develop" else diagnose()
