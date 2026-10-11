"""Summarize predeclared candidate comparisons and paired daily uncertainty."""

from __future__ import annotations

import json

import numpy as np
import polars as pl

from src.research_stats import hac_stats
from run import ROOT
from src.scoring import Panel, add_top_persistence, make_scores, score


OUT = ROOT / "experiments" / "next_steps_eval"
VARIANTS = ("top2", "huber", "recent2x", "rolling3")
YEARS = (2022, 2023, 2024)
ALPHA = 0.95
BONUS = 0.15


def baseline(year: int) -> tuple[dict, pl.DataFrame]:
    fold = pl.read_parquet(ROOT / "validation" / f"fold_{year}.parquet")
    panel = Panel.from_frame(fold)
    pred = add_top_persistence(panel, make_scores(panel, panel.frame["pred_raw"].to_numpy(), ALPHA), BONUS)
    return score(panel, pred)


def paired_hac(base: pl.DataFrame, candidate: pl.DataFrame) -> dict:
    if not base["trade_date"].equals(candidate["trade_date"]):
        raise AssertionError("Daily date mismatch")
    ic = candidate["rank_ic"].to_numpy() - base["rank_ic"].to_numpy()
    excess = candidate["excess"].to_numpy() - base["excess"].to_numpy()
    turnover = candidate["turnover"].to_numpy() - base["turnover"].to_numpy()
    daily_score_delta = 0.4 * ic + 0.3 * 252 * excess - 0.3 * turnover
    return {
        "rank_ic_delta": hac_stats(ic),
        "annual_excess_delta": hac_stats(252 * excess),
        "turnover_delta": hac_stats(turnover),
        "daily_score_delta_t2_onward": hac_stats(daily_score_delta),
        "note": "The composite daily series omits the first day because turnover is undefined. "
                "Intervals are descriptive and not corrected for candidate selection.",
    }


def main() -> None:
    result = {"alpha": ALPHA, "bonus": BONUS, "development_years": [2022, 2023],
              "diagnostic_year": 2024, "baseline": {}, "variants": {}}
    base_daily = {}
    for year in YEARS:
        metrics, daily = baseline(year)
        result["baseline"][str(year)] = metrics
        base_daily[year] = daily
    for variant in VARIANTS:
        by_year = {}
        for year in YEARS:
            path = OUT / f"{variant}_{year}.json"
            if not path.exists():
                continue
            candidate = json.loads(path.read_text(encoding="utf-8"))
            daily = pl.read_csv(OUT / f"{variant}_{year}_daily.csv")
            metrics = candidate["metrics"]
            by_year[str(year)] = {
                "metrics": metrics,
                "score_delta": metrics["final_score"] - result["baseline"][str(year)]["final_score"],
                "paired_hac": paired_hac(base_daily[year], daily),
            }
            print(f"{variant} {year}: score={metrics['final_score']:.6f} "
                  f"delta={by_year[str(year)]['score_delta']:+.6f}", flush=True)
        if all(str(y) in by_year for y in (2022, 2023)):
            by_year["development_min_score"] = min(by_year[str(y)]["metrics"]["final_score"] for y in (2022, 2023))
        result["variants"][variant] = by_year
    selected = max(
        ("baseline", *VARIANTS),
        key=lambda name: min(
            result["baseline"][str(y)]["final_score"] if name == "baseline"
            else result["variants"][name][str(y)]["metrics"]["final_score"]
            for y in (2022, 2023)
        ),
    )
    result["selected_on_development"] = selected
    result["promotion_decision"] = "keep_baseline" if selected == "baseline" or (
        str(2024) in result["variants"].get(selected, {})
        and result["variants"][selected]["2024"]["score_delta"] <= 0
    ) else "requires_further_review"
    target = OUT / "summary.json"
    target.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"selected={selected}, decision={result['promotion_decision']}, saved={target}", flush=True)


if __name__ == "__main__":
    main()
