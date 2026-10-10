"""Application validation: does the alpha survive realistic next-open execution?

The competition credits y_ret_1d(t) = close(t+1)/close(t) - 1 to a Top set
formed from a signal that uses day t's OHLCV and is therefore only computable at
close(t). Buying at that same close is not executable. This module decomposes
the official one-day return into the leg a real trader cannot capture and the
leg they can, using only OPEN0 = open/close from the frozen feature panel.

Exact multiplicative identity, with o = OPEN0(t+1) and y = y_ret_1d(t):

    close(t) -> open(t+1)   overnight, NOT capturable   o*(1+y) - 1
    open(t+1) -> close(t+1) intraday, capturable        1/o - 1
    product                                             (1+y) - 1

The realistic daily-rebalanced return is instead open(t+1) -> open(t+2):

    [OPEN0(t+2)/OPEN0(t+1)] * (1 + y_ret_1d(t+1)) - 1

which needs the following year's label for the final fold day, so that day is
dropped from the open-to-open series and the reduced coverage is disclosed.

Top sets are the released ones, taken from the evaluator-faithful replay in
cost_execution. Portfolio membership never depends on returns or on whether a
label happens to be missing.
"""
from __future__ import annotations

import argparse
import json
import time
from pathlib import Path

import numpy as np
import polars as pl

from run import ROOT
from experiments.bonus_extension import (AUXILIARY, BASE_BONUS, BLEND_WEIGHT, FOLD,
                                         blend_top_only, file_hash, load_auxiliary, load_panel)
from experiments.cost_execution import TRADING_DAYS, daily_excess, evaluator_frame
from experiments.official_seed_development import official_score

OUT = ROOT / "experiments" / "cost_execution_eval"
FEATURE_FILE = ROOT / "data" / "features.parquet"
YEARS = (2022, 2023, 2024)
MIN_ELIGIBLE = 100


def open0_calendar(year: int, panel_codes: np.ndarray) -> tuple[np.ndarray, np.ndarray, list[int]]:
    """OPEN0 and price_valid over the fold year plus the following January.

    Column order is asserted identical to the fold panel's stock order, so the
    two panels can be indexed positionally without any sorting assumption.
    """
    frame = (pl.scan_parquet(FEATURE_FILE)
             .filter(pl.col("trade_date").is_between(year * 10000 + 101, (year + 1) * 10000 + 131))
             .select(["ts_code", "trade_date", "OPEN0", "price_valid"])
             .sort("trade_date", "ts_code")
             .collect())
    dates = frame["trade_date"].unique(maintain_order=True).to_list()
    codes = frame["ts_code"].to_numpy()
    n = len(codes) // len(dates)
    if len(codes) != len(dates) * n:
        raise AssertionError(f"{year}: OPEN0 panel is not rectangular")
    codes = codes.reshape(len(dates), n)
    if not np.all(codes == codes[0]):
        raise AssertionError(f"{year}: stock order differs across dates in the OPEN0 panel")
    if not np.array_equal(codes[0], panel_codes):
        raise AssertionError(f"{year}: OPEN0 panel stock order differs from the fold panel")
    if len(dates) < 244:
        raise AssertionError(f"{year}: extended calendar is too short for an open-to-open leg")
    return (frame["OPEN0"].to_numpy().astype(np.float64).reshape(len(dates), n),
            frame["price_valid"].to_numpy().reshape(len(dates), n),
            [int(d) for d in dates])


def selection_sets(merged, panel_codes: np.ndarray) -> tuple[dict[int, np.ndarray], dict[int, np.ndarray]]:
    """Return Top and eligible-market column positions per day, in evaluator order.

    Positions index the panel's rectangular (day, stock) grid; the caller has
    already asserted that the replayed frame preserves the panel's row order.
    """
    positions = {str(code): index for index, code in enumerate(panel_codes)}
    top, market = {}, {}
    for date, group in merged.groupby("trade_date"):
        eligible = group[(group["flag_limit_up"] == 0) & group["y_ret_1d"].notna()]
        if len(eligible) < MIN_ELIGIBLE:
            continue
        ordered = eligible.sort_values("pred", ascending=False).reset_index(drop=True)
        n_top = max(len(ordered) // 10, 1)
        codes = ordered["ts_code"].to_numpy()
        top[int(date)] = np.asarray([positions[str(c)] for c in codes[:n_top]], dtype=int)
        market[int(date)] = np.asarray([positions[str(c)] for c in codes], dtype=int)
    return top, market


def execution_analysis(year: int) -> dict:
    panel = load_panel(year)
    auxiliary = load_auxiliary(year, panel)
    prediction = blend_top_only(panel, auxiliary, BASE_BONUS, BLEND_WEIGHT)
    shape = panel.valid_price.shape

    official, official_daily = official_score(panel, prediction, year)
    merged = evaluator_frame(panel, prediction, year)
    if not np.array_equal(merged["ts_code"].to_numpy(), panel.frame["ts_code"].to_numpy()):
        raise AssertionError(f"{year}: evaluator replay changed row order")
    official_excess = daily_excess(merged)

    # Float64 original labels, aligned to the panel's rectangular (day, stock) grid.
    y64 = merged["y_ret_1d"].to_numpy().astype(np.float64).reshape(shape)
    open0, open_valid, calendar = open0_calendar(year, panel.codes)
    index_of = {date: position for position, date in enumerate(calendar)}
    fold_dates = [int(d) for d in panel.dates]
    for position, date in enumerate(fold_dates[:-1]):
        if calendar[index_of[date] + 1] != fold_dates[position + 1]:
            raise AssertionError(f"{year}: the extended calendar is not contiguous with the fold")

    top_sets, market_sets = selection_sets(merged, panel.codes)
    legs = {key: [] for key in ("cc_top", "cc_market", "ccok_top", "ccok_market",
                                "on_top", "on_market", "id_top", "id_market",
                                "cross_top", "cross_market", "oo_top", "oo_market")}
    counts = {"scored_days": 0, "open_to_open_days": 0,
              "top_observations": 0, "top_observations_open_to_open": 0}
    identity_residual = 0.0

    def part(values: np.ndarray, mask: np.ndarray) -> float:
        return float(values[mask].mean()) if mask.any() else np.nan

    for position, date in enumerate(fold_dates):
        if date not in top_sets:
            continue
        i = index_of[date]
        top, market = top_sets[date], market_sets[date]
        o1, o2 = open0[i + 1], open0[i + 2]
        v1, v2 = open_valid[i + 1], open_valid[i + 2]
        y = y64[position]
        y_next = y64[position + 1] if position + 1 < shape[0] else None

        y_top, o1_top, o2_top = y[top], o1[top], o2[top]
        y_mkt, o1_mkt, o2_mkt = y[market], o1[market], o2[market]
        ok_top = np.isfinite(y_top) & np.isfinite(o1_top) & (o1_top > 0) & v1[top]
        ok_mkt = np.isfinite(y_mkt) & np.isfinite(o1_mkt) & (o1_mkt > 0) & v1[market]

        # Per-observation legs. The multiplicative identity is exact for each
        # stock; cross-sectional means decompose additively through the
        # overnight x intraday cross term, which is carried explicitly.
        on_top, id_top = o1_top * (1 + y_top) - 1, 1 / o1_top - 1
        on_mkt, id_mkt = o1_mkt * (1 + y_mkt) - 1, 1 / o1_mkt - 1
        if ok_top.any():
            identity_residual = max(identity_residual, float(np.max(np.abs(
                (1 + on_top[ok_top]) * (1 + id_top[ok_top]) - (1 + y_top[ok_top])))))
        if ok_mkt.any():
            identity_residual = max(identity_residual, float(np.max(np.abs(
                (1 + on_mkt[ok_mkt]) * (1 + id_mkt[ok_mkt]) - (1 + y_mkt[ok_mkt])))))

        legs["cc_top"].append(part(y_top, np.isfinite(y_top)))
        legs["cc_market"].append(part(y_mkt, np.isfinite(y_mkt)))
        legs["ccok_top"].append(part(y_top, ok_top))
        legs["ccok_market"].append(part(y_mkt, ok_mkt))
        legs["on_top"].append(part(on_top, ok_top))
        legs["on_market"].append(part(on_mkt, ok_mkt))
        legs["id_top"].append(part(id_top, ok_top))
        legs["id_market"].append(part(id_mkt, ok_mkt))
        legs["cross_top"].append(part(on_top * id_top, ok_top))
        legs["cross_market"].append(part(on_mkt * id_mkt, ok_mkt))
        counts["scored_days"] += 1
        counts["top_observations"] += int(ok_top.sum())

        if y_next is not None:
            yn_top, yn_mkt = y_next[top], y_next[market]
            ok_top_oo = ok_top & np.isfinite(o2_top) & (o2_top > 0) & v2[top] & np.isfinite(yn_top)
            ok_mkt_oo = ok_mkt & np.isfinite(o2_mkt) & (o2_mkt > 0) & v2[market] & np.isfinite(yn_mkt)
            legs["oo_top"].append(part((o2_top / o1_top) * (1 + yn_top) - 1, ok_top_oo))
            legs["oo_market"].append(part((o2_mkt / o1_mkt) * (1 + yn_mkt) - 1, ok_mkt_oo))
            counts["open_to_open_days"] += 1
            counts["top_observations_open_to_open"] += int(ok_top_oo.sum())
        else:
            # Final fold day: the open-to-open leg needs the next year's label.
            for key in ("oo_top", "oo_market"):
                legs[key].append(np.nan)

    if counts["scored_days"] < 240:
        raise AssertionError(f"{year}: only {counts['scored_days']} scored execution days")
    arrays = {}
    for key, values in legs.items():
        array = np.asarray(values, dtype=float)
        if len(array) != counts["scored_days"]:
            raise AssertionError(f"{year}: {key} series length {len(array)} != {counts['scored_days']}")
        arrays[key] = array
    open_to_open_days = np.isfinite(arrays["oo_top"]) & np.isfinite(arrays["oo_market"])
    if int(open_to_open_days.sum()) != counts["open_to_open_days"]:
        raise AssertionError(f"{year}: open-to-open day count disagrees with the coverage counter")
    for key, array in arrays.items():
        check = array[open_to_open_days] if key.startswith("oo") else array
        if not np.isfinite(check).all():
            raise AssertionError(f"{year}: nonfinite execution leg {key}")
    if identity_residual > 1e-12:
        raise AssertionError(f"{year}: per-observation overnight x intraday identity failed "
                             f"(residual {identity_residual:.3e})")

    def annual(top_key: str, market_key: str, mask: np.ndarray | None = None) -> dict:
        if mask is None:
            top_values, market_values = arrays[top_key], arrays[market_key]
        else:
            top_values, market_values = arrays[top_key][mask], arrays[market_key][mask]
        excess = top_values - market_values
        return {"mean_daily_excess": float(excess.mean()),
                "annual_excess": float(excess.mean() * TRADING_DAYS),
                "mean_daily_top": float(top_values.mean()),
                "annual_top": float(top_values.mean() * TRADING_DAYS),
                "days": int(len(excess))}

    close_to_close = annual("cc_top", "cc_market")
    if abs(close_to_close["annual_excess"] - official["annual_excess"]) > 1e-9:
        raise AssertionError(f"{year}: close-to-close replay {close_to_close['annual_excess']:.12f} "
                             f"differs from the official {official['annual_excess']:.12f}")
    official_mean = float(np.mean([official_excess[d] for d in sorted(official_excess)]))
    if abs(close_to_close["mean_daily_excess"] - official_mean) > 1e-12:
        raise AssertionError(f"{year}: close-to-close daily mean differs from the official series")
    if close_to_close["days"] != len(official_excess):
        raise AssertionError(f"{year}: scored day count differs from the official excess series")

    overnight = annual("on_top", "on_market")
    intraday = annual("id_top", "id_market")
    cross = annual("cross_top", "cross_market")
    close_to_close_same_mask = annual("ccok_top", "ccok_market")
    open_to_open = annual("oo_top", "oo_market", open_to_open_days)

    additive_residual = abs(overnight["annual_excess"] + intraday["annual_excess"]
                            + cross["annual_excess"] - close_to_close_same_mask["annual_excess"])
    if additive_residual > 1e-9:
        raise AssertionError(f"{year}: additive leg decomposition failed (residual {additive_residual:.3e})")

    result = {
        "year": year,
        "official_composite_score": float(official["final_score"]),
        "official_annual_excess_close_to_close": float(official["annual_excess"]),
        "replay_close_to_close": close_to_close,
        "decomposition": {
            "basis": "identical eligibility mask for all four legs, so they sum exactly",
            "close_to_close_same_mask": close_to_close_same_mask,
            "overnight_close_to_next_open": overnight,
            "intraday_next_open_to_next_close": intraday,
            "overnight_x_intraday_cross_term": cross,
            "per_observation_identity_max_residual": identity_residual,
            "additive_decomposition_residual": additive_residual,
            "overnight_share_of_gross_excess": overnight["annual_excess"] / close_to_close["annual_excess"],
            "intraday_share_of_gross_excess": intraday["annual_excess"] / close_to_close["annual_excess"],
        },
        "executable_open_to_open": open_to_open,
        "executable_retained_fraction": open_to_open["annual_excess"] / close_to_close["annual_excess"],
        "coverage": {**counts,
                     "top_observation_retention_open_to_close": counts["top_observations"] / max(
                         counts["scored_days"], 1),
                     "open_to_top_observation_retention": (counts["top_observations_open_to_open"]
                                                           / max(counts["top_observations"], 1))},
        "conventions": {
            "signal_time": "close(t), using day t OHLCV; the official metric assumes a close(t) fill",
            "overnight": "close(t) -> open(t+1) = OPEN0(t+1)*(1+y_ret_1d(t)) - 1, not capturable",
            "intraday": "open(t+1) -> close(t+1) = 1/OPEN0(t+1) - 1, capturable at the next open",
            "cross_term": "overnight x intraday product; required because the multiplicative "
                          "identity is per observation, not between cross-sectional means",
            "open_to_open": "open(t+1) -> open(t+2), the true daily-rebalanced holding return",
            "numerator": "the released label-eligible return Top set, evaluator tie order",
            "denominator": "the same label-eligible market over the identical window",
            "dropped_day": "the final fold day needs the following year's label and is excluded "
                           "from the open-to-open series only; the close-to-close anchor keeps all days",
            "costs": "not applied here; see cost_analysis.json for the cost grid",
        },
    }
    del panel, auxiliary, prediction, merged
    return result


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    result_path = OUT / "execution_timing.json"
    if result_path.exists():
        raise SystemExit("Execution timing analysis already recorded; preserving it")
    started = time.monotonic()
    years = {}
    for year in YEARS:
        item = years[str(year)] = execution_analysis(year)
        decomposition = item["decomposition"]
        executable = item["executable_open_to_open"]
        print(f"{year}: official c->c={item['official_annual_excess_close_to_close']:.4%} | "
              f"overnight={decomposition['overnight_close_to_next_open']['annual_excess']:.4%} "
              f"({decomposition['overnight_share_of_gross_excess']:.1%}) | "
              f"intraday={decomposition['intraday_next_open_to_next_close']['annual_excess']:.4%} "
              f"({decomposition['intraday_share_of_gross_excess']:.1%}) | "
              f"cross={decomposition['overnight_x_intraday_cross_term']['annual_excess']:.4%} | "
              f"executable o->o={executable['annual_excess']:.4%} "
              f"(retained {item['executable_retained_fraction']:.1%}, "
              f"{item['coverage']['open_to_open_days']}d)", flush=True)

    average = lambda path: float(np.mean([
        path(years[str(y)]) for y in YEARS]))
    means = {
        "official_close_to_close": average(lambda v: v["official_annual_excess_close_to_close"]),
        "overnight": average(lambda v: v["decomposition"]["overnight_close_to_next_open"]["annual_excess"]),
        "intraday": average(lambda v: v["decomposition"]["intraday_next_open_to_next_close"]["annual_excess"]),
        "cross": average(lambda v: v["decomposition"]["overnight_x_intraday_cross_term"]["annual_excess"]),
        "executable_open_to_open": average(lambda v: v["executable_open_to_open"]["annual_excess"]),
    }
    means["overnight_share_of_gross"] = means["overnight"] / means["official_close_to_close"]
    means["executable_retained_fraction"] = (means["executable_open_to_open"]
                                             / means["official_close_to_close"])
    output = {
        "generated_at_local": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "elapsed_seconds": time.monotonic() - started,
        "years": years,
        "three_year_mean": means,
        "source_and_input_sha256": {
            str(Path(__file__).relative_to(ROOT)).replace("\\", "/"): file_hash(Path(__file__)),
            "experiments/cost_execution.py": file_hash(ROOT / "experiments/cost_execution.py"),
            "experiments/bonus_extension.py": file_hash(ROOT / "experiments/bonus_extension.py"),
            "evaluate.py": file_hash(ROOT / "evaluate.py"),
            "data/features.parquet": file_hash(FEATURE_FILE),
            **{FOLD.format(year=y): file_hash(ROOT / FOLD.format(year=y)) for y in YEARS},
            **{AUXILIARY.format(year=y): file_hash(ROOT / AUXILIARY.format(year=y)) for y in YEARS},
        },
        "caveats": [
            "Open-to-open assumes a fill at the official open with no auction impact; a large order "
            "would move the open itself, so this is an upper bound on the executable leg.",
            "The final fold day is excluded from the open-to-open series because it needs the "
            "following year's label; the close-to-close anchor keeps every scored day.",
            "Each window recomputes eligibility from that window's price validity, so the market "
            "denominator differs slightly between the three legs.",
            "Costs are not applied here; combine with cost_analysis.json for a net figure.",
            "2022-2024 are repeatedly examined historical years, not a blind holdout or an official "
            "2025-2026 test result.",
        ],
    }
    result_path.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\n3-year mean: official c->c={means['official_close_to_close']:.4%} "
          f"overnight={means['overnight']:.4%} ({means['overnight_share_of_gross']:.1%}) "
          f"executable o->o={means['executable_open_to_open']:.4%} "
          f"(retained {means['executable_retained_fraction']:.1%})", flush=True)
    print(f"Wrote {result_path}", flush=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("stage", nargs="?", choices=("analyze",), default="analyze")
    parser.parse_args()
    main()
