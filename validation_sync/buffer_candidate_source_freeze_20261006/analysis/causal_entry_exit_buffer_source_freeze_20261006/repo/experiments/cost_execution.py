"""Application validation: realized turnover, transaction costs and execution timing.

The competition metric credits y_ret_1d = close(t+1)/close(t) - 1 to a Top set
formed from a signal that is only computable at close(t), and it deducts no
cost. This module quantifies both gaps for the released pooled_rms25 prediction
without modifying any frozen artifact.

Two questions:
  A. What one-way turnover does the official Jaccard distance actually imply,
     and what round-trip cost makes the strategy break even?
  B. Under A-share cost assumptions, what is the net annualized excess?

Top sets and daily excess are taken from a frame built by replaying the exact
CSV round trip and merge order of the unmodified evaluate.py. Because that
evaluator sorts with pandas' default non-stable descending quicksort, any
change to row order reshuffles exact ties and changes the Top membership; the
aggregate excess and Jaccard reproduced here are therefore asserted against the
real evaluator's own output before use. Returns and label availability are never
used to form a portfolio.
"""
from __future__ import annotations

import argparse
import json
import tempfile
import time
from pathlib import Path

import numpy as np
import pandas as pd
import polars as pl

from run import ROOT
from src.scoring import Panel
from experiments.bonus_extension import (AUXILIARY, BASE_BONUS, BLEND_WEIGHT, FOLD,
                                         blend_top_only, file_hash, load_auxiliary,
                                         load_panel, release_scores)
from experiments.official_seed_development import official_score, original_labels

OUT = ROOT / "experiments" / "cost_execution_eval"
YEARS = (2022, 2023, 2024)

# Round-trip cost grid, as a fraction of traded notional. Components for A-shares:
# commission about 0.025% each way, stamp duty 0.05% on the sell side only
# (halved from 0.1% on 2023-08-28), transfer fee negligible, plus slippage and
# price impact. 0.30% round trip is the central assumption; the grid brackets it.
COST_GRID = (0.0010, 0.0015, 0.0020, 0.0025, 0.0030, 0.0040, 0.0050)
CENTRAL_COST = 0.0030
TRADING_DAYS = 252
# Day one buys the whole book, incurring only the entry leg of a round trip.
INITIAL_BUILD_LEGS = 0.5


def evaluator_frame(panel: Panel, prediction: np.ndarray, year: int) -> pd.DataFrame:
    """Replay evaluate.py's CSV round trip and merge order byte for byte."""
    labels = original_labels(year)
    keys = panel.frame.select("ts_code", "trade_date")
    joined = (panel.frame.drop("y_ret_1d")
              .join(labels, on=["ts_code", "trade_date"], how="left", validate="1:1")
              .sort("trade_date", "ts_code"))
    if not joined.select("ts_code", "trade_date").equals(keys):
        raise AssertionError("Label join changed prediction row order")
    with tempfile.TemporaryDirectory(prefix="cost-exec-") as temporary:
        folder = Path(temporary)
        keys.with_columns(pl.Series("pred", np.asarray(prediction, dtype=float))).write_csv(
            folder / "submission.csv", float_precision=17)
        joined.select("ts_code", "trade_date", "flag_limit_up").write_csv(folder / "测试集_X.csv")
        joined.select("ts_code", "trade_date", "y_ret_1d").write_csv(folder / "测试集_Y.csv",
                                                                    float_precision=17)
        prediction_frame = pd.read_csv(folder / "submission.csv")
        label_frame = pd.read_csv(folder / "测试集_Y.csv")
        flag_frame = pd.read_csv(folder / "测试集_X.csv",
                                 usecols=["ts_code", "trade_date", "flag_limit_up"])
    merged = prediction_frame.merge(label_frame, on=["ts_code", "trade_date"], how="inner")
    return merged.merge(flag_frame, on=["ts_code", "trade_date"], how="inner")


def daily_excess(merged: pd.DataFrame) -> dict[int, float]:
    """Official Top 10% excess per day, using the evaluator's own groupby and sort."""
    out = {}
    for date, group in merged.groupby("trade_date"):
        valid = group[(group["flag_limit_up"] == 0) & group["y_ret_1d"].notna()].copy()
        if len(valid) < 100:
            continue
        # Deliberately no kind= argument: the official evaluator uses the default.
        valid = valid.sort_values("pred", ascending=False).reset_index(drop=True)
        n_top = max(len(valid) // 10, 1)
        returns = valid["y_ret_1d"]
        out[int(date)] = float(returns.iloc[:n_top].mean() - returns.mean())
    return out


def turnover_top_sets(merged: pd.DataFrame) -> dict[int, list[str]]:
    """Official turnover Top sets per day, using the evaluator's boolean-filter path."""
    sets = {}
    for date in sorted(merged["trade_date"].unique()):
        group = merged[merged["trade_date"] == date]
        valid = group[group["flag_limit_up"] == 0].copy()
        if len(valid) < 100:
            continue
        valid = valid.sort_values("pred", ascending=False)
        sets[int(date)] = list(valid["ts_code"].iloc[:max(len(valid) // 10, 1)])
    return sets


def turnover_series(sets: dict[int, list[str]]) -> dict:
    """Jaccard distance and realized one-way turnover between consecutive Top sets."""
    dates = sorted(sets)
    jaccard, one_way, sizes = {}, {}, {}
    for index in range(1, len(dates)):
        today, yesterday = set(sets[dates[index]]), set(sets[dates[index - 1]])
        union = len(today | yesterday)
        if not union:
            continue
        jaccard[dates[index]] = 1 - len(today & yesterday) / union
        one_way[dates[index]] = len(today - yesterday) / len(today)
        sizes[dates[index]] = len(today)
    return {"jaccard": jaccard, "one_way": one_way, "size": sizes}


def cost_analysis(year: int) -> dict:
    panel = load_panel(year)
    auxiliary = load_auxiliary(year, panel)
    prediction = blend_top_only(panel, auxiliary, BASE_BONUS, BLEND_WEIGHT)

    official, official_daily = official_score(panel, prediction, year)
    merged = evaluator_frame(panel, prediction, year)
    excess = daily_excess(merged)
    series = turnover_series(turnover_top_sets(merged))

    # The official excess averages every eligible day, but turnover is only
    # defined from day two onward. Keep the two denominators separate: costs are
    # charged on rebalance days, excess is averaged over all scoring days.
    all_dates = sorted(excess)
    turn_dates = sorted(series["jaccard"])
    if all_dates[1:] != turn_dates:
        raise AssertionError(f"{year}: excess days and turnover days are not the same window")
    gross = np.asarray([excess[d] for d in all_dates], dtype=float)
    jaccard = np.asarray([series["jaccard"][d] for d in turn_dates], dtype=float)
    one_way = np.asarray([series["one_way"][d] for d in turn_dates], dtype=float)
    if not (np.isfinite(gross).all() and np.isfinite(one_way).all() and np.isfinite(jaccard).all()):
        raise AssertionError(f"{year}: nonfinite excess or turnover series")

    mean_gross = float(gross.mean())
    mean_one_way = float(one_way.mean())
    annual_gross = mean_gross * TRADING_DAYS

    # Anchor every derived quantity to the unmodified evaluator before use.
    if abs(official["final_score"] - release_scores()[year]) > 1e-12:
        raise AssertionError(f"{year}: baseline does not reproduce the released composite score")
    if abs(float(jaccard.mean()) - official["mean_turnover"]) > 1e-12:
        raise AssertionError(f"{year}: reproduced Jaccard {jaccard.mean():.12f} differs from "
                             f"the official {official['mean_turnover']:.12f}")
    if abs(annual_gross - official["annual_excess"]) > 1e-12:
        raise AssertionError(f"{year}: reproduced gross excess {annual_gross:.12f} differs from "
                             f"the official {official['annual_excess']:.12f}")
    if not np.allclose([excess[d] for d in all_dates],
                       official_daily["excess"].to_numpy().astype(float), rtol=0, atol=1e-15):
        raise AssertionError(f"{year}: daily excess series differs from the official daily evidence")

    nets = {}
    for cost in COST_GRID:
        # Day one buys the whole book and pays only the entry leg; later days pay
        # the round trip on the fraction of the book actually replaced.
        daily_cost = np.empty(len(all_dates), dtype=float)
        daily_cost[0] = INITIAL_BUILD_LEGS * cost
        daily_cost[1:] = one_way * cost
        annual_net = float((gross - daily_cost).mean()) * TRADING_DAYS
        nets[f"{cost:.4f}"] = {
            "round_trip_cost": cost,
            "annual_net_excess": annual_net,
            "annual_cost_drag": annual_gross - annual_net,
            "retained_fraction_of_gross": annual_net / annual_gross if annual_gross else None,
        }
    breakeven = mean_gross / mean_one_way if mean_one_way > 0 else float("inf")

    result = {
        "year": year,
        "official_metrics": {k: float(v) for k, v in official.items()},
        "anchored_to_unmodified_evaluator": True,
        "excess_days": len(all_dates),
        "turnover_days": len(turn_dates),
        "mean_top_size": float(np.mean([series["size"][d] for d in turn_dates])),
        "official_mean_jaccard": float(jaccard.mean()),
        "mean_one_way_turnover": mean_one_way,
        "annualized_one_way_turnover": mean_one_way * TRADING_DAYS,
        "jaccard_to_one_way_ratio": float(jaccard.mean() / mean_one_way) if mean_one_way else None,
        "mean_daily_gross_excess": mean_gross,
        "annual_gross_excess": annual_gross,
        "breakeven_round_trip_cost": float(breakeven),
        "breakeven_multiple_of_central_cost": float(breakeven / CENTRAL_COST),
        "net_by_cost": nets,
        "central_assumption": {"round_trip_cost": CENTRAL_COST, **nets[f"{CENTRAL_COST:.4f}"]},
        "conventions": {
            "top_set_rule": "flag_limit_up == 0, pandas default descending pred sort, first "
                            "floor(n/10); replayed through the evaluator's own CSV round trip and "
                            "merge order so exact ties break identically",
            "excess_rule": "flag_limit_up == 0 and finite y_ret_1d; Top mean minus eligible mean",
            "excess_denominator": "all eligible scoring days, including day one",
            "turnover_denominator": "day two onward only, matching the official metric",
            "one_way_turnover": "|S_t \\ S_{t-1}| / |S_t|, the fraction of the book actually replaced",
            "jaccard_relation": "for equal-size sets J = 2u/(1+u), so u = J/(2-J); the measured "
                                "one-way rate is used directly rather than this approximation",
            "cost_charging": "one_way_turnover(t) x round_trip_cost on rebalance days; day one pays "
                             "0.5 x round trip for the initial full-book entry",
            "annualization": "daily mean x 252, simple sum, not compounded net value",
            "execution_timing": "still the competition's close(t) to close(t+1) convention",
            "not_modeled": "position-level liquidity limits, partial fills, borrowing, the strategy's "
                           "own market impact, and next-open rather than same-close execution",
        },
    }
    del panel, auxiliary, prediction, merged
    return result


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    result_path = OUT / "cost_analysis.json"
    if result_path.exists():
        raise SystemExit("Cost analysis already recorded; preserving it instead of recomputing")
    started = time.monotonic()
    years = {}
    for year in YEARS:
        item = years[str(year)] = cost_analysis(year)
        print(f"{year}: gross={item['annual_gross_excess']:.4%} "
              f"net@{CENTRAL_COST:.2%}={item['central_assumption']['annual_net_excess']:.4%} "
              f"one_way_turn={item['mean_one_way_turnover']:.4%} "
              f"jaccard={item['official_mean_jaccard']:.4%} "
              f"breakeven={item['breakeven_round_trip_cost']:.4%} "
              f"({item['breakeven_multiple_of_central_cost']:.1f}x central)", flush=True)

    mean = lambda key: float(np.mean([years[str(y)][key] for y in YEARS]))
    net_mean = float(np.mean([years[str(y)]["central_assumption"]["annual_net_excess"] for y in YEARS]))
    output = {
        "generated_at_local": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "elapsed_seconds": time.monotonic() - started,
        "years": years,
        "three_year_mean_annual_gross_excess": mean("annual_gross_excess"),
        "three_year_mean_annual_net_excess_at_central_cost": net_mean,
        "three_year_mean_cost_drag": mean("annual_gross_excess") - net_mean,
        "three_year_mean_one_way_turnover": mean("mean_one_way_turnover"),
        "three_year_mean_breakeven_round_trip_cost": mean("breakeven_round_trip_cost"),
        "cost_grid": list(COST_GRID),
        "central_cost": CENTRAL_COST,
        "source_and_input_sha256": {
            str(Path(__file__).relative_to(ROOT)).replace("\\", "/"): file_hash(Path(__file__)),
            "experiments/bonus_extension.py": file_hash(ROOT / "experiments/bonus_extension.py"),
            "experiments/official_seed_development.py": file_hash(ROOT / "experiments/official_seed_development.py"),
            "evaluate.py": file_hash(ROOT / "evaluate.py"),
            "src/scoring.py": file_hash(ROOT / "src/scoring.py"),
            **{FOLD.format(year=y): file_hash(ROOT / FOLD.format(year=y)) for y in YEARS},
            **{AUXILIARY.format(year=y): file_hash(ROOT / AUXILIARY.format(year=y)) for y in YEARS},
        },
        "caveats": [
            "Simple sum of daily net excess annualized by 252; not a compounded net value curve.",
            "Execution is still modeled at the close that forms the signal, which is the "
            "competition's own convention and the more favorable of the two; a next-open variant "
            "would forgo part of the overnight move.",
            "Slippage and impact are assumptions, not measurements. The grid brackets them and the "
            "break-even round-trip rate is the defensible summary statistic.",
            "Official turnover Top and return Top use different missing-label filters, so cost is "
            "charged on the traded book while excess is earned on the label-eligible book.",
            "2022-2024 are historical diagnosis years examined many times, not a blind holdout "
            "or an official 2025-2026 test result.",
        ],
    }
    result_path.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\n3-year mean gross={output['three_year_mean_annual_gross_excess']:.4%} "
          f"net@{CENTRAL_COST:.2%}={net_mean:.4%} "
          f"drag={output['three_year_mean_cost_drag']:.4%} "
          f"breakeven={output['three_year_mean_breakeven_round_trip_cost']:.4%}", flush=True)
    print(f"Wrote {result_path}", flush=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("stage", nargs="?", choices=("analyze",), default="analyze")
    parser.parse_args()
    main()
