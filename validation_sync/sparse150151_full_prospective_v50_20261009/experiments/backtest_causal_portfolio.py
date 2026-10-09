"""Self-financing next-open execution on frozen fold-local signals.

This new diagnostic never imports an official label-based return evaluator and
never modifies a released model, prediction, or report. See execution/protocol.json
for the predeclared trading and mark-to-market assumptions.
"""
from __future__ import annotations

import os

# Set before importing numerical libraries; do not compete with model fitting.
os.environ["POLARS_MAX_THREADS"] = "4"
os.environ["OMP_NUM_THREADS"] = "4"
os.environ["OPENBLAS_NUM_THREADS"] = "4"
os.environ["MKL_NUM_THREADS"] = "4"

import argparse
from dataclasses import dataclass
import hashlib
import json
from pathlib import Path
import time

import numpy as np
import polars as pl


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "experiments/revalidation_20260926/execution"
PREDICTIONS = ROOT / "experiments/revalidation_20260926/validation"
YEARS = (2022, 2023, 2024)
COSTS = (0.0, 0.001, 0.003, 0.005)
PORTFOLIOS = ("baseline", "ensemble4", "market")
KEYS = ["trade_date", "ts_code"]
BAR_COLUMNS = KEYS + ["open", "close", "vol", "flag_limit_up", "flag_limit_down"]


def sha(path: Path) -> str:
    with path.open("rb") as handle:
        return hashlib.file_digest(handle, "sha256").hexdigest()


def write_json(path: Path, value: dict) -> None:
    with path.open("x", encoding="utf-8") as handle:
        json.dump(value, handle, ensure_ascii=False, indent=2, allow_nan=False)


def log(message: str) -> None:
    print(f"[{time.strftime('%H:%M:%S')}] {message}", flush=True)


@dataclass
class Market:
    dates: np.ndarray
    codes: np.ndarray
    opens: np.ndarray
    closes: np.ndarray
    volumes: np.ndarray
    up: np.ndarray
    down: np.ndarray
    scores: dict[str, np.ndarray]

    def prefix(self, days: int) -> "Market":
        return Market(self.dates[:days], self.codes, self.opens[:days],
                      self.closes[:days], self.volumes[:days], self.up[:days],
                      self.down[:days], {k: v[:days] for k, v in self.scores.items()})


def market_from_frames(bars: pl.DataFrame, predictions: dict[str, pl.DataFrame]) -> Market:
    """Projection makes labels and any other future fields inaccessible downstream."""
    bars = bars.select(BAR_COLUMNS).sort(KEYS)
    if bars.select(pl.struct(KEYS).n_unique()).item() != len(bars):
        raise ValueError("Duplicate daily quote keys")
    dates = bars["trade_date"].unique(maintain_order=True).to_numpy()
    codes = bars.filter(pl.col("trade_date") == int(dates[0]))["ts_code"].to_numpy()
    shape = (len(dates), len(codes))
    if len(bars) != shape[0] * shape[1]:
        raise ValueError("Expected organizer's complete rectangular symbol/date grid")
    if not np.all(bars["ts_code"].to_numpy().reshape(shape) == codes):
        raise ValueError("Daily symbol order is not constant")
    matrices = {}
    for name, frame in predictions.items():
        frame = frame.select(KEYS + ["pred"]).sort(KEYS)
        if not frame.select(KEYS).equals(bars.select(KEYS)):
            raise ValueError(f"Prediction/raw quote keys do not match: {name}")
        score = frame["pred"].cast(pl.Float64).to_numpy().reshape(shape)
        if not np.isfinite(score).all():
            raise ValueError(f"Nonfinite prediction: {name}")
        matrices[name] = score
    array = lambda column: bars[column].cast(pl.Float64).to_numpy().reshape(shape)
    return Market(dates, codes, array("open"), array("close"), array("vol"),
                  array("flag_limit_up"), array("flag_limit_down"), matrices)


def load_market() -> tuple[Market, dict]:
    source = ROOT / "data" / "raw" / "训练集.csv"
    # Never load y_ret_1d: select is pushed into the lazy CSV scan.
    bars = (pl.scan_csv(source, schema_overrides={"ts_code": pl.String,
                "trade_date": pl.Int32}, null_values=["NaN", "nan", ""])
            .filter(pl.col("trade_date").is_between(20220101, 20241231))
            .select(BAR_COLUMNS).collect())
    frames, inputs = {}, {"训练集.csv": sha(source)}
    for name in PORTFOLIOS[:2]:
        parts = []
        for year in YEARS:
            path = PREDICTIONS / f"predictions_{name}_{year}.parquet"
            inputs[path.relative_to(ROOT).as_posix()] = sha(path)
            parts.append(pl.read_parquet(path, columns=KEYS + ["pred"]))
        frames[name] = pl.concat(parts)
    market = market_from_frames(bars, frames)
    if len(market.dates) != 726 or len(market.codes) != 4650:
        raise ValueError("Expected the 726-day / 4650-symbol 2022-2024 panel")
    return market, inputs


def target_indices(market: Market, day: int, portfolio: str) -> np.ndarray:
    """The only signal-selection routine: all array accesses are at signal date t."""
    eligible = (np.isfinite(market.closes[day]) & (market.closes[day] > 0)
                & (market.up[day] == 0))
    index = np.flatnonzero(eligible)
    if portfolio == "market" or not len(index):
        return index
    # codes were sorted ascending; stable sorting fixes ties without future labels.
    ranked = index[np.argsort(-market.scores[portfolio][day, index], kind="stable")]
    return ranked[:max(len(index) // 10, 1)]


def event_hash(codes: np.ndarray, bought: np.ndarray, sold: np.ndarray) -> str:
    selected = np.flatnonzero((bought > 0) | (sold > 0))
    digest = hashlib.sha256()
    for i in selected:
        digest.update(str(codes[i]).encode("utf-8") + b"\0")
        digest.update(np.asarray([bought[i], sold[i]], dtype="<f8").tobytes())
    return digest.hexdigest()


def simulate(market: Market, portfolio: str, round_trip_cost: float) -> tuple[pl.DataFrame, dict]:
    """Fractional adjusted-price units, no leverage, sells before proportional buys."""
    side_cost = round_trip_cost / 2.0
    n = len(market.codes)
    quantity = np.zeros(n, dtype=np.float64)
    marks = np.zeros(n, dtype=np.float64)
    mark_age = np.zeros(n, dtype=np.int32)
    cash, previous_nav, gross_nav = 1.0, 1.0, 1.0
    target = np.array([], dtype=np.int64)
    records = []
    max_cash_residual = 0.0
    max_asset_residual = 0.0
    orders = hashlib.sha256()
    for day, date in enumerate(market.dates):
        opening, closing = market.opens[day], market.closes[day]
        open_valid = np.isfinite(opening) & (opening > 0)
        close_valid = np.isfinite(closing) & (closing > 0)
        # Only a same-day open quote can price a fill. Missing quotes keep holdings.
        marks = np.where(open_valid, opening, marks)
        nav_before = cash + float(np.dot(quantity, marks))
        if nav_before <= 0 or not np.isfinite(nav_before):
            raise AssertionError("Nonpositive or nonfinite portfolio equity")
        cash_before = cash
        current_value = quantity * marks
        desired_value = np.zeros(n, dtype=np.float64)
        if len(target):
            desired_value[target] = nav_before / len(target)
        desired_delta = desired_value - current_value
        desired_buy = np.maximum(desired_delta, 0.0)
        desired_sell = np.minimum(np.maximum(-desired_delta, 0.0), current_value)
        material_buy = desired_buy > 1e-14 * nav_before
        material_sell = desired_sell > 1e-14 * nav_before
        volume_ok = np.isfinite(market.volumes[day]) & (market.volumes[day] > 0)
        quote_ok = open_valid & volume_ok
        # The daily flags/volume are explicit conservative execution proxies, not
        # inputs to yesterday's candidate set and not claims about auction prints.
        buy_allowed = quote_ok & (market.up[day] == 0)
        sell_allowed = quote_ok & (market.down[day] == 0)
        sell_value = np.where(sell_allowed & material_sell, desired_sell, 0.0)
        sold = np.divide(sell_value, opening, out=np.zeros(n), where=open_valid)
        sold = np.minimum(sold, quantity)
        sell_value = sold * np.where(open_valid, opening, 0.0)
        total_sold = float(sell_value.sum())
        quantity -= sold
        cash += total_sold * (1.0 - side_cost)
        buy_request = np.where(buy_allowed & material_buy, desired_buy, 0.0)
        requested = float(buy_request.sum())
        # Reserve both the stock purchase and its actual one-way transaction fee.
        buy_scale = min(1.0, max(cash, 0.0) / (requested * (1 + side_cost))) if requested else 1.0
        buy_value = buy_request * buy_scale
        bought = np.divide(buy_value, opening, out=np.zeros(n), where=open_valid)
        total_bought = float(buy_value.sum())
        quantity += bought
        fee = side_cost * (total_bought + total_sold)
        cash -= total_bought * (1.0 + side_cost)
        cash_residual = cash - (cash_before + total_sold - total_bought - fee)
        asset_residual = cash + float(np.dot(quantity, marks)) - (nav_before - fee)
        max_cash_residual = max(max_cash_residual, abs(cash_residual))
        max_asset_residual = max(max_asset_residual, abs(asset_residual))
        if cash < -1e-12 * nav_before or np.any(quantity < -1e-12):
            raise AssertionError("Self-financing portfolio borrowed cash or shorted stock")
        if max(abs(cash_residual), abs(asset_residual)) > 2e-12 * nav_before:
            raise AssertionError("Cash/asset conservation failed during execution")
        # Price movements alter weights; no implicit rebalancing or cash injection.
        marks = np.where(close_valid, closing, marks)
        mark_age = np.where(close_valid | open_valid, 0, mark_age + 1)
        positions_value = quantity * marks
        nav = cash + float(positions_value.sum())
        net_return = nav / previous_nav - 1.0
        # Cost add-back uses THIS fee-paid account's actual held shares. This
        # diagnostic gross curve is distinct from a separately simulated zero-fee
        # account, whose cash-constrained holdings may differ.
        gross_return = net_return + fee / previous_nav
        gross_nav *= 1.0 + gross_return
        held = quantity > 1e-14
        missing_open = ~open_valid
        suspended = open_valid & ~volume_ok
        limit_buy = quote_ok & (market.up[day] != 0)
        limit_sell = quote_ok & (market.down[day] != 0)
        daily_order_hash = event_hash(market.codes, bought, sold)
        orders.update(daily_order_hash.encode("ascii"))
        records.append({
            "trade_date": int(date), "signal_date": int(market.dates[day - 1]) if day else None,
            "portfolio": portfolio, "round_trip_cost": round_trip_cost,
            "target_count": int(len(target)), "held_count": int(held.sum()),
            "nav_before_open_trades": nav_before, "net_nav": nav,
            "gross_nav_same_actual_holdings": gross_nav, "net_return": net_return,
            "gross_return_same_actual_holdings": gross_return,
            "cash_before_trades": cash_before, "cash": cash,
            "cash_weight": cash / nav, "stock_value": float(positions_value.sum()),
            "buy_notional": total_bought, "sell_notional": total_sold, "fees": fee,
            "turnover_actual_two_sided": (total_bought + total_sold) / nav_before,
            "turnover_actual_half_two_sided": .5 * (total_bought + total_sold) / nav_before,
            "buy_scaling_for_cash": buy_scale,
            "unfilled_buy_cash_notional": requested * (1.0 - buy_scale),
            "blocked_buy_missing_open_count": int((material_buy & missing_open).sum()),
            "blocked_sell_missing_open_count": int((material_sell & missing_open).sum()),
            "blocked_buy_suspended_count": int((material_buy & suspended).sum()),
            "blocked_sell_suspended_count": int((material_sell & suspended).sum()),
            "blocked_buy_limit_count": int((material_buy & limit_buy).sum()),
            "blocked_sell_limit_count": int((material_sell & limit_sell).sum()),
            "blocked_buy_notional": float(desired_buy[~buy_allowed].sum()),
            "blocked_sell_notional": float(desired_sell[~sell_allowed].sum()),
            "missing_close_held_count": int((held & ~close_valid).sum()),
            "stale_mark_held_count": int((held & (mark_age > 0)).sum()),
            "stale_mark_weight": float(positions_value[held & (mark_age > 0)].sum() / nav),
            "max_held_stale_sessions": int(mark_age[held].max()) if held.any() else 0,
            "cash_conservation_residual": cash_residual,
            "asset_conservation_residual": asset_residual,
            "filled_buy_names": int(np.count_nonzero(bought)),
            "filled_sell_names": int(np.count_nonzero(sold)),
            "order_sha256": daily_order_hash,
        })
        previous_nav = nav
        # Form tomorrow's orders only after today's execution and closing marks.
        target = target_indices(market, day, portfolio)
    final = {
        "portfolio": portfolio, "round_trip_cost": round_trip_cost,
        "all_orders_sha256": orders.hexdigest(), "final_cash": cash,
        "final_nav": previous_nav, "max_cash_conservation_error": max_cash_residual,
        "max_asset_conservation_error": max_asset_residual,
        "final_positions": [{"ts_code": str(market.codes[i]), "fractional_units": float(quantity[i]),
                             "last_mark": float(marks[i]), "weight": float(quantity[i] * marks[i] / previous_nav),
                             "mark_stale_sessions": int(mark_age[i])}
                            for i in np.flatnonzero(quantity > 1e-14)],
    }
    return pl.DataFrame(records), final


def drawdown(returns: np.ndarray) -> float:
    wealth = np.r_[1.0, np.cumprod(1.0 + returns)]
    return float(np.min(wealth / np.maximum.accumulate(wealth) - 1.0))


def stats(frame: pl.DataFrame, benchmark: pl.DataFrame) -> dict:
    if not frame["trade_date"].equals(benchmark["trade_date"]):
        raise AssertionError("Strategy and benchmark execution calendars differ")
    r = frame["net_return"].to_numpy()
    g = frame["gross_return_same_actual_holdings"].to_numpy()
    b = benchmark["net_return"].to_numpy()
    bg = benchmark["gross_return_same_actual_holdings"].to_numpy()
    growth = float(np.prod(1.0 + r))
    gross = float(np.prod(1.0 + g))
    market = float(np.prod(1.0 + b))
    market_gross = float(np.prod(1.0 + bg))
    result = {
        "days": len(r), "first_date": int(frame["trade_date"].min()),
        "last_date": int(frame["trade_date"].max()),
        "net_compound_return": growth - 1, "gross_same_holdings_compound_return": gross - 1,
        "benchmark_net_compound_return": market - 1,
        "benchmark_gross_same_holdings_compound_return": market_gross - 1,
        "net_compound_excess_percentage_points": growth - market,
        "gross_compound_excess_percentage_points": gross - market_gross,
        "net_relative_wealth_return": growth / market - 1,
        "net_annualized_compound_return_252": growth ** (252 / len(r)) - 1,
        "benchmark_net_annualized_compound_return_252": market ** (252 / len(r)) - 1,
        "net_max_drawdown": drawdown(r), "gross_same_holdings_max_drawdown": drawdown(g),
        "benchmark_net_max_drawdown": drawdown(b),
        "actual_two_sided_turnover_sum": float(frame["turnover_actual_two_sided"].sum()),
        "actual_half_two_sided_turnover_daily_mean": float(frame["turnover_actual_half_two_sided"].mean()),
        "buy_notional_in_initial_equity_units": float(frame["buy_notional"].sum()),
        "sell_notional_in_initial_equity_units": float(frame["sell_notional"].sum()),
        "paid_fees_in_initial_equity_units": float(frame["fees"].sum()),
        "mean_cash_weight": float(frame["cash_weight"].mean()),
        "max_stale_mark_weight": float(frame["stale_mark_weight"].max()),
        "max_held_stale_sessions": int(frame["max_held_stale_sessions"].max()),
        "stale_mark_position_days": int(frame["stale_mark_held_count"].sum()),
        "missing_close_position_days": int(frame["missing_close_held_count"].sum()),
        "days_with_stale_held_marks": int((frame["stale_mark_held_count"] > 0).sum()),
        "blocked_buy_notional_sum": float(frame["blocked_buy_notional"].sum()),
        "blocked_sell_notional_sum": float(frame["blocked_sell_notional"].sum()),
        "blocked_requests_are_repeated_daily_attempts": True,
    }
    for column in frame.columns:
        if column.startswith("blocked_") and column.endswith("_count"):
            result[column + "_sum"] = int(frame[column].sum())
    return result


def fixture() -> tuple[pl.DataFrame, dict[str, pl.DataFrame]]:
    records = []
    score_records = []
    # A is initially selected; later B takes over. A is suspension/limit trapped,
    # and B cannot be bought at the same-day conservative limit-up barrier.
    for day in range(7):
        for stock in range(20):
            opening = 10.0 + stock * .1 + day * .05
            closing = opening * (1.002 if stock % 2 else .999)
            up = int(stock == 2 and day == 2)
            down = int(stock == 0 and day == 2)
            volume = 0.0 if stock == 1 and day == 2 else 1000.0
            if stock == 0 and day == 3:
                opening = closing = None
            score = (10.0 if stock < 2 else 0.0) if day == 0 else (10.0 if stock in (2, 3) else 0.0)
            key = {"trade_date": 20220103 + day, "ts_code": f"S{stock:02d}"}
            records.append({**key, "open": opening, "close": closing, "vol": volume,
                            "flag_limit_up": up, "flag_limit_down": down,
                            "y_ret_1d": stock * 100.0 + day})
            score_records.append({**key, "pred": score, "y_ret_1d": -stock - day})
    pred = pl.DataFrame(score_records)
    return pl.DataFrame(records), {"baseline": pred, "ensemble4": pred}


def tests() -> dict:
    bars, predictions = fixture()
    market = market_from_frames(bars, predictions)
    central, state = simulate(market, "ensemble4", .003)
    # Projection must make arbitrary labels, deleted labels, and an added future
    # availability mask irrelevant to BOTH orders and price-accounting returns.
    perturbed_bars = bars.with_columns(pl.lit(float("nan")).alias("y_ret_1d"),
                                      pl.lit(False).alias("future_label_available"))
    perturbed_predictions = {k: v.with_columns(pl.lit(1e99).alias("y_ret_1d"))
                             for k, v in predictions.items()}
    changed, _ = simulate(market_from_frames(perturbed_bars, perturbed_predictions), "ensemble4", .003)
    deleted, _ = simulate(market_from_frames(bars.drop("y_ret_1d"),
                    {k: v.drop("y_ret_1d") for k, v in predictions.items()}), "ensemble4", .003)
    assert central.equals(changed) and central.equals(deleted)
    short, _ = simulate(market.prefix(4), "ensemble4", .003)
    assert short.equals(central.head(4)), "Future append altered completed execution days"
    day2 = central.row(2, named=True)
    assert day2["blocked_sell_limit_count"] == 1
    assert day2["blocked_sell_suspended_count"] == 1
    assert day2["blocked_buy_limit_count"] == 1
    assert central.row(3, named=True)["stale_mark_held_count"] >= 1
    assert central.row(0, named=True)["filled_buy_names"] == 0
    assert central.row(1, named=True)["filled_buy_names"] == 2
    assert float(central["cash"].min()) >= -1e-12
    assert state["max_cash_conservation_error"] < 1e-12
    assert state["max_asset_conservation_error"] < 1e-12
    # With constant prices, fees alone explain any loss, not a selected return array.
    flat_bars = bars.with_columns(pl.lit(10.).alias("open"), pl.lit(10.).alias("close"),
                                 pl.lit(1000.).alias("vol"), pl.lit(0).alias("flag_limit_up"),
                                 pl.lit(0).alias("flag_limit_down"))
    flat, _ = simulate(market_from_frames(flat_bars, predictions), "ensemble4", .003)
    assert abs(float(flat["net_nav"][-1]) + float(flat["fees"].sum()) - 1) < 1e-12
    assert np.max(np.abs(flat["gross_return_same_actual_holdings"].to_numpy())) < 1e-12
    return {"status": "passed", "label_perturbation_exact_orders_and_returns": True,
            "deleted_labels_exact_orders_and_returns": True,
            "future_availability_mask_ignored": True, "future_append_prefix_exact": True,
            "signal_at_close_first_execution_next_open": True,
            "suspension_and_missing_quote_holdings_preserved": True,
            "directional_limit_constraints_enforced": True,
            "cash_and_assets_conserved_without_borrowing": True,
            "flat_price_loss_equals_actual_paid_fees": True,
            "max_fixture_cash_conservation_error": state["max_cash_conservation_error"],
            "max_fixture_asset_conservation_error": state["max_asset_conservation_error"]}


def protocol() -> dict:
    return {
        "experiment": "causal_unified_holdings_next_open_2022_2024",
        "declared_before_backtest": True, "years": list(YEARS),
        "prediction_directory": PREDICTIONS.relative_to(ROOT).as_posix(),
        "prediction_files": [f"predictions_{p}_{y}.parquet" for p in PORTFOLIOS[:2] for y in YEARS],
        "prediction_contract": "Corrected fold-local scores from the separate revalidation; no old full-fit auxiliary or future-training label is read by this engine.",
        "raw_columns_loaded": BAR_COLUMNS,
        "source_and_raw_sha256": {Path(__file__).relative_to(ROOT).as_posix(): sha(Path(__file__)),
                                   "训练集.csv": sha(ROOT / "data" / "raw" / "训练集.csv")},
        "selection": "At close(t), eligible iff close(t) finite positive and flag_limit_up(t)==0. Top floor(eligible/10), at least 1; descending pred(t), ties ts_code ascending. No y or future availability filter.",
        "benchmark": "Equal-weight every member of exactly the same t-known eligible universe; same execution dates, cash/holdings accounting, constraints and fee grid.",
        "execution": "t+1 opening price; target equal monetary weights from pretrade opening marked equity. Sell excess positions first; feasible buys are proportionally scaled to cash after reserving their fees. No label enters sizing.",
        "constraints": "Predeclared conservative scenario: invalid/missing open or nonpositive/missing execution-day volume blocks both directions; execution-day flag_limit_up!=0 blocks buys, flag_limit_down!=0 blocks sells. These daily flags/volume are execution proxies, not known opening-auction limit states and never signal inputs for the previous date.",
        "failed_fills": "Retain unsold shares and residual cash. Unfilled requests expire that day and are replaced by next day's target. Mark missing prices at last available same/past open or close; do not drop the asset or assign zero return to a separate selected universe.",
        "account": "Initial cash 1, fractional adjusted-price units, long only, no leverage, no deposits/withdrawals, zero cash interest. Shares and cash persist across calendar years; model prediction state may cold-start per fold.",
        "calendar": "Use all 2022-2024 quote days. First day stays cash until its close signal; first fill next trading day's open. End at 2024 final close with no terminal forced liquidation and no terminal exit fee; last close signal remains unexecuted.",
        "mark_to_market": "Use current valid close, else current valid open, else last available quote. Missing-quote holdings are kept and stale age/weight reported. No delisting payout or corporate-action model; organizer-adjusted prices are assumed internally consistent.",
        "cost_grid_round_trip": list(COSTS), "central_round_trip": .003,
        "cost_meaning": "Hypothetical all-in scenarios, not legal fee rates. Charge round_trip/2 on EACH actual buy/sell notional including initial entry. No separate slippage or market-impact model.",
        "gross_net": "Net NAV is the self-financing marked account. For the identical actual fee-paid holdings, daily gross return=net return+paid fees/previous NAV, compounded separately. The zero-fee account is also rerun independently; cash-constrained holdings can differ across fee scenarios.",
        "turnover": "Actual (buy notional+sell notional)/opening pretrade NAV, also report half this value. Not a Jaccard-distance proxy; includes drift rebalancing and initial entry.",
        "returns": "Calendar-year and whole-period compounded NAV returns; excess is strategy return minus same-cost benchmark return plus relative wealth ratio. 252-day CAGR explicitly separate. Drawdown includes initial equity.",
        "limitations": ["Historical diagnostic on repeatedly examined years, not an untouched holdout.",
            "Daily execution proxies cannot establish actual auction liquidity or fillability.",
            "Unlimited capacity, fractional shares, no lot size/minimum fee, no borrow or liquidity-impact model.",
            "No corporate-action/delisting recovery model; stale marks may hide losses.",
            "Organizer point-in-time universe and adjusted-price provenance remain unverified."],
    }


def prepare() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    checks = tests()
    declared = protocol()
    path = OUT / "protocol.json"
    if path.exists():
        if json.loads(path.read_text(encoding="utf-8")) != declared:
            raise ValueError("Existing predeclared execution protocol differs; preserve evidence")
    else:
        write_json(path, declared)
    test_path = OUT / "tests.json"
    if test_path.exists():
        if json.loads(test_path.read_text(encoding="utf-8")) != checks:
            raise ValueError("Existing execution tests differ")
    else:
        write_json(test_path, checks)
    log("Execution protocol pinned and meaningful causal/cash/constraint tests passed")


def run() -> None:
    prepare()
    if (OUT / "summary.json").exists():
        raise FileExistsError("Preserve completed execution evidence; do not overwrite")
    started = time.monotonic()
    market, inputs = load_market()
    log(f"Loaded label-free quotes/scores: {len(market.dates)} days x {len(market.codes)} symbols")
    write_json(OUT / "input_manifest.json", {"protocol_sha256": sha(OUT / "protocol.json"),
                                            "files_sha256": inputs})
    frames, accounts, aggregates = {}, {}, {}
    for cost in COSTS:
        key = f"{cost:.4f}"
        frames[key], accounts[key], aggregates[key] = {}, {}, {}
        for name in PORTFOLIOS:
            frame, final = simulate(market, name, cost)
            # Test real prices/scores against the full run, including orders and cash.
            short, _ = simulate(market.prefix(60), name, cost)
            if not short.equals(frame.head(60)):
                raise AssertionError(f"Real-data causal prefix differs: {name}/{cost}")
            frames[key][name], accounts[key][name] = frame, final
            positions = final.pop("final_positions")
            pl.DataFrame(positions).write_csv(OUT / f"final_positions_{name}_rt{key}.csv", float_precision=17)
            log(f"{name} roundtrip={cost:.1%}: final NAV={final['final_nav']:.6f}")
        benchmark = frames[key]["market"]
        for name in PORTFOLIOS:
            frame = frames[key][name]
            frame = frame.with_columns(
                pl.Series("benchmark_net_return", benchmark["net_return"]),
                pl.Series("benchmark_net_nav", benchmark["net_nav"]),
                (frame["net_nav"] / benchmark["net_nav"] - 1).alias("net_relative_wealth_return"))
            frame.write_csv(OUT / f"daily_{name}_rt{key}.csv", float_precision=17)
            aggregates[key][name] = {"whole_period": stats(frame, benchmark), "by_year": {}}
            for year in YEARS:
                year_mask = (pl.col("trade_date") // 10000) == year
                aggregates[key][name]["by_year"][str(year)] = stats(frame.filter(year_mask), benchmark.filter(year_mask))
    contrasts = {}
    for key, values in aggregates.items():
        contrasts[key] = {}
        for year in ["whole_period", *map(str, YEARS)]:
            extract = lambda model: values[model]["whole_period"] if year == "whole_period" else values[model]["by_year"][year]
            a, b = extract("ensemble4"), extract("baseline")
            contrasts[key][year] = {
                "ensemble_minus_baseline_net_return": a["net_compound_return"] - b["net_compound_return"],
                "ensemble_minus_baseline_net_excess": a["net_compound_excess_percentage_points"] - b["net_compound_excess_percentage_points"],
                "ensemble_minus_baseline_max_drawdown": a["net_max_drawdown"] - b["net_max_drawdown"],
                "ensemble_minus_baseline_turnover_half_daily_mean": a["actual_half_two_sided_turnover_daily_mean"] - b["actual_half_two_sided_turnover_daily_mean"],
            }
    result = {"status": "passed", "generated_at_local": time.strftime("%Y-%m-%dT%H:%M:%S"),
              "elapsed_seconds": time.monotonic() - started,
              "protocol_sha256": sha(OUT / "protocol.json"), "source_sha256": sha(Path(__file__)),
              "input_manifest_sha256": sha(OUT / "input_manifest.json"),
              "tests_sha256": sha(OUT / "tests.json"),
              "real_data_prefix_60_days_exact_all_12_accounts": True,
              "label_columns_loaded_for_backtest": [],
              "years": list(YEARS), "trading_dates": len(market.dates), "stocks": len(market.codes),
              "round_trip_cost_grid": list(COSTS), "central_round_trip_cost": .003,
              "all_cost_scenarios": aggregates, "ensemble_minus_baseline": contrasts,
              "account_reconciliation": accounts,
              "artifacts_sha256": {p.name: sha(p) for p in sorted(OUT.glob("*.csv"))}}
    if any(sha(ROOT / path) != expected for path, expected in inputs.items()):
        raise AssertionError("Execution input changed while running")
    if sha(Path(__file__)) != json.loads((OUT / "protocol.json").read_text(encoding="utf-8"))["source_and_raw_sha256"][Path(__file__).relative_to(ROOT).as_posix()]:
        raise AssertionError("Predeclared execution source changed during run")
    result["inputs_and_source_unchanged_during_run"] = True
    write_json(OUT / "summary.json", result)
    write_conclusion(result)
    log(f"Completed unified execution diagnostic in {result['elapsed_seconds']:.1f}s")


def write_conclusion(result: dict) -> None:
    central = result["all_cost_scenarios"]["0.0030"]
    lines = ["# 同一持仓、次日开盘、自融资执行复核", "",
             "本结果是预声明日频执行约束下的历史诊断，不是官方收益打分，也不表示真实开盘成交得到验证。仅加载行情和折内预测，不读取收益标签。",
             "", "- t 日收盘选股，t+1 开盘先卖后买；资金不足按比例缩单。分数持仓、无杠杆、现金守恒，跨年延续持仓。",
             "- 策略与等权市场基准使用相同可知股票池、入场日期、成交约束和费用。缺行情保留持仓，以最后可得价格估值。",
             "- 执行日全天涨跌停标志与零成交量仅是保守成交约束代理，无法证明开盘时的真实限价状态；没有退市回收或公司行动模型。",
             "- 往返 0、0.10%、0.30%、0.50% 为费用情景，每次买卖按实际单边成交额收取一半；不是法律费率。",
             "- 毛收益由同一实际持仓加回实际费用获得；同时独立重跑零费账户。净收益为账户复合收益，不以官方 Jaccard 换手近似交易成本。",
             "", "## 中心费用：往返 0.30%", "",
             "| 区间 | pooled 基线净收益 | ensemble4 净收益 | 市场基准净收益 | ensemble4 净超额 | 新版较基线净收益变化 |",
             "|---|---:|---:|---:|---:|---:|"]
    for label in [*map(str, YEARS), "whole_period"]:
        take = lambda model: central[model]["whole_period"] if label == "whole_period" else central[model]["by_year"][label]
        a, b, market = take("ensemble4"), take("baseline"), take("market")
        name = "2022—2024 累计" if label == "whole_period" else label
        lines.append(f"| {name} | {b['net_compound_return']:.2%} | {a['net_compound_return']:.2%} | {market['net_compound_return']:.2%} | {a['net_compound_excess_percentage_points']:.2%} | {a['net_compound_return']-b['net_compound_return']:+.2%} |")
    lines += ["", "## 全期费用敏感度", "", "| 往返费用 | pooled 基线净收益 | ensemble4 净收益 | ensemble4 相对市场净超额 | ensemble4 最大回撤 |",
              "|---|---:|---:|---:|---:|"]
    for key, values in result["all_cost_scenarios"].items():
        a, b = values["ensemble4"]["whole_period"], values["baseline"]["whole_period"]
        lines.append(f"| {float(key):.2%} | {b['net_compound_return']:.2%} | {a['net_compound_return']:.2%} | {a['net_compound_excess_percentage_points']:.2%} | {a['net_max_drawdown']:.2%} |")
    a = central["ensemble4"]["whole_period"]
    delta = result["ensemble_minus_baseline"]["0.0030"]["whole_period"]["ensemble_minus_baseline_net_return"]
    lines += ["", "## 解释与核验", "",
              f"在本中心情景下，新版较 pooled 基线三年累计净收益变化为 {delta:+.2%}。这个数回答统一真实持仓口径下的执行差异，不能替代测试期无标签的真实样本外评价。",
              f"新版日均实际半双边换手 {a['actual_half_two_sided_turnover_daily_mean']:.2%}，平均现金权重 {a['mean_cash_weight']:.2%}；缺行情持仓最大陈旧估值权重 {a['max_stale_mark_weight']:.2%}，最长 {a['max_held_stale_sessions']} 个交易日。",
              "标签扰动、删除标签、追加未来前缀、停牌/缺行情持仓保留、方向限价、现金守恒和常价成本恒等式测试均通过；12 个实际账户的前 60 日前缀与完整运行逐项一致。",
              "每日文件披露实际买卖金额、费用、现金、净值、失败订单计数/金额、缺价估值、现金约束缩单和订单摘要哈希；失败金额可能包括逐日重复尝试，不能解释为独立订单总额。",
              "尚未建模：真实开盘集合竞价深度、市场冲击、最低佣金/整手、退市清算与调整因子来源。终点保留持仓，不强制清算，因此未扣终端退出费用。",
              "当前实验不修改既有 active_release.json、提交物、模型或报告。"]
    path = OUT / "结论.md"
    with path.open("x", encoding="utf-8") as handle:
        handle.write("\n".join(lines) + "\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("stage", choices=("test", "prepare", "run"), default="run", nargs="?")
    args = parser.parse_args()
    if args.stage == "test":
        print(json.dumps(tests(), ensure_ascii=False, indent=2))
    elif args.stage == "prepare":
        prepare()
    else:
        run()
