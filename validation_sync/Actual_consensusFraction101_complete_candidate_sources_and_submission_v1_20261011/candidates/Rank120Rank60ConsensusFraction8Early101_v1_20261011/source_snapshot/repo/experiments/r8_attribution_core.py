"""Exact retrospective attribution of two already-frozen final score columns.

attribute_year(frame) -> (daily pandas frame, stock pandas frame, summary dict).
No candidate generation, fitting, reweighting or historical I/O. Caller provides
one canonically sorted year. Label-free turnover lists are fixed in a first pass;
the second pass reproduces the official ex-post label-filtered return lists.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import sys
import tempfile
import warnings

import numpy as np
import pandas as pd
from scipy.stats import spearmanr

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

KEYS = ["trade_date", "ts_code"]
PREDICTIONS = {"base": "pred_base", "candidate": "pred_candidate"}
STOCK_COLUMNS = ["trade_date", "ts_code", "side", "sign", "y_ret_1d", "return_k",
                 "signed_return_contribution", "annual_excess_delta_contribution",
                 "annual_score_return_contribution"]


def _sha_members(codes) -> str:
    return hashlib.sha256(json.dumps(sorted(map(str, codes)), ensure_ascii=False,
                                    separators=(",", ":")).encode("utf-8")).hexdigest()


def _safe(value):
    if isinstance(value, dict):
        return {str(k): _safe(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [_safe(v) for v in value]
    if isinstance(value, (np.bool_, bool)):
        return bool(value)
    if isinstance(value, (np.integer, int)):
        return int(value)
    if isinstance(value, (np.floating, float)):
        return float(value) if np.isfinite(value) else None
    return value


def _mean(values) -> float:
    return float(np.mean(values)) if len(values) else float("nan")


def _close(a, b, context: str, tolerance=1e-12) -> float:
    if np.isnan(a) and np.isnan(b):
        return 0.
    difference = abs(float(a) - float(b))
    if not np.isfinite(difference) or difference > tolerance:
        raise AssertionError(f"Attribution identity failed {context}: {a} != {b}")
    return difference


def _validate(frame: pd.DataFrame) -> int:
    required = set(KEYS + ["flag_limit_up", "y_ret_1d", *PREDICTIONS.values()])
    if not isinstance(frame, pd.DataFrame) or frame.empty or not required <= set(frame.columns):
        raise ValueError("Nonempty frame with both predictions, keys, flag and original labels required")
    if frame[KEYS].isna().any().any() or frame.duplicated(KEYS).any():
        raise ValueError("Keys must be nonnull and unique")
    if not pd.api.types.is_integer_dtype(frame["trade_date"]):
        raise ValueError("trade_date must be integer YYYYMMDD")
    if not frame["ts_code"].map(lambda x: isinstance(x, str)).all():
        raise ValueError("ts_code must be a string")
    if not frame[KEYS].reset_index(drop=True).equals(frame.sort_values(KEYS)[KEYS].reset_index(drop=True)):
        raise ValueError("Caller must provide canonical trade_date, ts_code order")
    dates = pd.to_datetime(frame["trade_date"].astype(str), format="%Y%m%d", errors="raise")
    years = dates.dt.year.unique()
    if len(years) != 1:
        raise ValueError("Annual attribution accepts exactly one year; annual weights must not be pooled")
    if frame["y_ret_1d"].dtype != np.dtype("float64") or np.isinf(frame["y_ret_1d"].to_numpy()).any():
        raise ValueError("Original labels must be Float64; NaN is allowed, infinity is not")
    if frame["flag_limit_up"].isna().any() or not frame["flag_limit_up"].isin([0, 1]).all():
        raise ValueError("flag_limit_up must be nonnull 0/1")
    if not np.isfinite(frame[list(PREDICTIONS.values())].to_numpy(dtype=np.float64)).all():
        raise ValueError("Saved final predictions must be finite")
    return int(years[0])


def _ranked_top(pool: pd.DataFrame, column: str) -> tuple[pd.DataFrame, int, pd.DataFrame]:
    # Intentionally identical to evaluate.py. Do not replace pandas' default
    # sort with stable sorting: filtering changes tied rows and quicksort order.
    ranked = pool.sort_values(column, ascending=False)
    k = max(len(pool) // 10, 1)
    return ranked.iloc[:k], int((ranked[column] == ranked.iloc[k - 1][column]).sum()), ranked


def _label_free_pass(frame: pd.DataFrame) -> dict[int, dict]:
    """Complete this pass before touching labels; turnover never reads Y."""
    signal = frame[KEYS + ["flag_limit_up", *PREDICTIONS.values()]]
    previous = {name: None for name in PREDICTIONS}
    result = {}
    for date, group in signal.groupby("trade_date", sort=True):
        pool = group[group["flag_limit_up"] == 0].copy()
        row = {"pool_n": len(pool), "k": max(len(pool) // 10, 1) if len(pool) >= 100 else 0,
               "top": {}, "turnover": {}, "ties": {}}
        for name, column in PREDICTIONS.items():
            if len(pool) < 100:
                top, tie_count, turnover = set(), 0, np.nan
                previous[name] = None
            else:
                selected, tie_count, _ = _ranked_top(pool, column)
                top = set(selected["ts_code"])
                old = previous[name]
                turnover = 1 - len(top & old) / len(top | old) if old is not None and old else np.nan
                previous[name] = top
            row["top"][name], row["turnover"][name], row["ties"][name] = top, turnover, tie_count
        result[int(date)] = row
    return result


def attribute_year(frame: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, dict]:
    """Attribute candidate-minus-base official metrics for one fixed year.

    signed_return_contribution is +y/K for additions and -y/K for deletions
    relative to the base OFFICIAL RETURN Top on the same date. No arbitrary
    matching of an added stock with a deleted stock is performed. Missing-label
    filtering is ex-post official scoring, never an inference or order rule.
    """
    year = _validate(frame)
    frozen = _label_free_pass(frame)
    rows, stocks = [], []
    errors = {"daily_swap_return": 0., "daily_market_cancellation": 0., "annual_score_components": 0.,
              "annual_stock_return": 0., "monthly_score_components": 0.}
    for date, group in frame.groupby("trade_date", sort=True):
        date = int(date)
        prior = frozen[date]
        labeled = group.dropna(subset=["y_ret_1d"])
        eligible = group[(group["flag_limit_up"] == 0) & group["y_ret_1d"].notna()].copy()
        usable_ic, usable_return = len(labeled) >= 30, len(eligible) >= 100
        k = max(len(eligible) // 10, 1) if usable_return else 0
        market = float(eligible["y_ret_1d"].mean()) if usable_return else np.nan
        row = {"trade_date": date, "year": year, "month": date // 100,
               "ic_observed_n": len(labeled), "ic_eligible": usable_ic, "return_eligible": usable_return,
               "turnover_eligible": bool(np.isfinite(prior["turnover"]["base"])),
               "return_pool_n": len(eligible), "return_k": k,
               "turnover_pool_n": prior["pool_n"], "turnover_k": prior["k"],
               "label_missing_nonlimit_n": prior["pool_n"] - len(eligible), "market_return": market}
        return_top = {}
        for name, column in PREDICTIONS.items():
            with warnings.catch_warnings():
                warnings.simplefilter("ignore", category=RuntimeWarning)
                ic = float(spearmanr(labeled[column], labeled["y_ret_1d"]).statistic) if usable_ic else np.nan
            top, tied, ranked_pool = _ranked_top(eligible, column) if usable_return else (eligible.iloc[:0], 0, eligible)
            members = set(top["ts_code"])
            return_top[name] = members
            turnover_top = prior["top"][name]
            top_return = float(top["y_ret_1d"].mean()) if usable_return else np.nan
            # Official evaluate.py computes the market mean AFTER each signal's
            # sort. Identical mathematical pools can have tiny order-roundoff.
            ordered_market = float(ranked_pool["y_ret_1d"].mean()) if usable_return else np.nan
            missing_top = group[group["ts_code"].isin(turnover_top)]["y_ret_1d"].isna().sum()
            row.update({f"ic_{name}": ic, f"top_return_{name}": top_return,
                        f"market_return_{name}": ordered_market,
                        f"excess_{name}": top_return - ordered_market,
                        f"turnover_{name}": prior["turnover"][name],
                        f"return_top_sha256_{name}": _sha_members(members),
                        f"turnover_top_sha256_{name}": _sha_members(turnover_top),
                        f"return_cutoff_tie_n_{name}": tied,
                        f"turnover_cutoff_tie_n_{name}": prior["ties"][name],
                        f"missing_labels_in_turnover_top_{name}": int(missing_top),
                        f"return_not_turnover_top_n_{name}": len(members - turnover_top),
                        f"turnover_not_return_top_n_{name}": len(turnover_top - members)})
        added, removed = return_top["candidate"] - return_top["base"], return_top["base"] - return_top["candidate"]
        if len(added) != len(removed):
            raise AssertionError("Identical official eligibility must give equal addition/removal counts")
        labels = group.set_index("ts_code")["y_ret_1d"]
        added_sum = float(labels.loc[sorted(added)].sum()) if added else 0.
        removed_sum = float(labels.loc[sorted(removed)].sum()) if removed else 0.
        addition = added_sum / k if usable_return else np.nan
        deletion = -removed_sum / k if usable_return else np.nan
        delta_return = row["top_return_candidate"] - row["top_return_base"]
        delta_excess = row["excess_candidate"] - row["excess_base"]
        errors["daily_swap_return"] = max(errors["daily_swap_return"], _close(addition + deletion, delta_return, f"swap/{date}"))
        errors["daily_market_cancellation"] = max(errors["daily_market_cancellation"], _close(delta_return, delta_excess, f"market/{date}"))
        row.update({"added_n": len(added), "removed_n": len(removed),
                    "common_return_top_n": len(return_top["base"] & return_top["candidate"]),
                    "added_return_sum": added_sum, "removed_return_sum": removed_sum,
                    "added_return_contribution": addition, "removed_return_contribution": deletion,
                    "swap_return_delta": addition + deletion, "delta_excess": delta_excess,
                    "delta_market_mean_rounding": row["market_return_candidate"] - row["market_return_base"],
                    "group_attribution_rounding_residual": delta_excess - (addition + deletion),
                    "delta_ic": row["ic_candidate"] - row["ic_base"],
                    "delta_turnover": row["turnover_candidate"] - row["turnover_base"]})
        for side, codes, sign in (("added", added, 1), ("removed", removed, -1)):
            for code in sorted(codes):
                value = float(labels.loc[code])
                stocks.append({"trade_date": date, "ts_code": code, "side": side, "sign": sign,
                               "y_ret_1d": value, "return_k": k,
                               "signed_return_contribution": sign * value / k})
        rows.append(row)
    daily = pd.DataFrame(rows)
    stock = pd.DataFrame(stocks, columns=STOCK_COLUMNS)
    counts = {"ic_days": int(daily["ic_eligible"].sum()), "return_days": int(daily["return_eligible"].sum()),
              "turnover_pairs": int(daily["turnover_eligible"].sum())}
    ni, nr, nt = counts["ic_days"], counts["return_days"], counts["turnover_pairs"]
    metrics = {}
    for name in PREDICTIONS:
        ic = daily.loc[daily["ic_eligible"], f"ic_{name}"].to_numpy()
        ic_mean = _mean(ic)
        ic_std = float(np.std(ic, ddof=1)) if len(ic) > 1 else np.nan
        annual = 252 * _mean(daily.loc[daily["return_eligible"], f"excess_{name}"].to_numpy())
        turn = _mean(daily.loc[daily["turnover_eligible"], f"turnover_{name}"].to_numpy())
        metrics[name] = {"ic_mean": ic_mean, "ic_std": ic_std, "icir": ic_mean / ic_std if ic_std > 0 else 0.,
                         "ic_positive_ratio": _mean(ic > 0), "annual_excess": annual,
                         "top1_annual_ret": 252 * _mean(daily.loc[daily["return_eligible"], f"top_return_{name}"].to_numpy()),
                         "mean_turnover": turn, "final_score": .4 * ic_mean + .3 * annual + .3 * (1 - turn)}
    # Different component denominators are retained. Undefined daily entries
    # contribute zero only outside that component's official eligible set.
    daily["annual_score_ic_contribution"] = np.where(daily["ic_eligible"], .4 * daily["delta_ic"] / max(ni, 1), 0.)
    daily["annual_excess_delta_contribution"] = np.where(daily["return_eligible"], 252 * daily["delta_excess"] / max(nr, 1), 0.)
    daily["annual_score_return_contribution"] = .3 * daily["annual_excess_delta_contribution"]
    daily["annual_score_turnover_contribution"] = np.where(daily["turnover_eligible"], -.3 * daily["delta_turnover"] / max(nt, 1), 0.)
    daily["annual_score_delta_contribution"] = (daily["annual_score_ic_contribution"]
        + daily["annual_score_return_contribution"] + daily["annual_score_turnover_contribution"])
    stock["annual_excess_delta_contribution"] = stock["signed_return_contribution"] * 252 / max(nr, 1)
    stock["annual_score_return_contribution"] = .3 * stock["annual_excess_delta_contribution"]
    # Every stock/date cohort sum must reproduce the official daily change.
    stock_daily = stock.groupby("trade_date")["signed_return_contribution"].sum() if len(stock) else pd.Series(dtype=float)
    daily["stock_return_contribution_sum"] = np.where(daily["return_eligible"],
        daily["trade_date"].map(stock_daily).fillna(0.), np.nan)
    daily["stock_attribution_rounding_residual"] = daily["delta_excess"] - daily["stock_return_contribution_sum"]
    for row in daily[daily["return_eligible"]].itertuples():
        errors["daily_swap_return"] = max(errors["daily_swap_return"],
            _close(stock_daily.get(row.trade_date, 0.), row.delta_excess, f"stock-sum/{row.trade_date}"))
    delta = {key: metrics["candidate"][key] - metrics["base"][key] for key in metrics["base"]}
    contributions = {"ic": .4 * delta["ic_mean"], "return": .3 * delta["annual_excess"],
                     "turnover": -.3 * delta["mean_turnover"]}
    component_columns = ["annual_score_ic_contribution", "annual_score_return_contribution",
                         "annual_score_turnover_contribution", "annual_score_delta_contribution"]
    complete = bool(ni and nr and nt and np.isfinite(delta["final_score"]))
    if complete:
        errors["annual_score_components"] = _close(sum(contributions.values()), delta["final_score"], "annual/components")
        errors["annual_score_components"] = max(errors["annual_score_components"],
            _close(np.sum(daily["annual_score_delta_contribution"].to_numpy()), delta["final_score"], "annual/daily"))
    if nr:
        errors["annual_stock_return"] = _close(stock["annual_excess_delta_contribution"].sum(), delta["annual_excess"], "annual/stock")
    monthly = []
    for month, group in daily.groupby("month", sort=True):
        item = {"month": int(month), "ic_days": int(group["ic_eligible"].sum()),
                "return_days": int(group["return_eligible"].sum()), "turnover_pairs": int(group["turnover_eligible"].sum())}
        item.update({key: float(np.sum(group[key].to_numpy())) for key in component_columns})
        monthly.append(item)
    if complete:
        errors["monthly_score_components"] = _close(sum(x["annual_score_delta_contribution"] for x in monthly),
                                                     delta["final_score"], "monthly/annual")
    by_stock = (stock.groupby("ts_code", sort=True).agg(
        stock_days=("trade_date", "size"), signed_return_sum=("signed_return_contribution", "sum"),
        annual_excess_delta_contribution=("annual_excess_delta_contribution", "sum"),
        annual_score_return_contribution=("annual_score_return_contribution", "sum")).reset_index()
        if len(stock) else pd.DataFrame(columns=["ts_code", "stock_days", "signed_return_sum",
            "annual_excess_delta_contribution", "annual_score_return_contribution"]))

    def removal(table, identifier):
        column = "annual_score_return_contribution"
        positive = table[table[column] > 0].sort_values([column, identifier], ascending=[False, True])
        chosen = positive.head(5)
        removed = float(chosen[column].sum())
        positive_total = float(positive[column].sum())
        return {"selected": chosen[[identifier, column]].to_dict("records"), "count": len(chosen),
                "removed_annual_score_return_contribution": removed,
                "share_of_positive_return_contributions": removed / positive_total if positive_total > 0 else None,
                "score_delta_after_subtracting_these_attribution_terms": delta["final_score"] - removed,
                "annual_excess_delta_after_subtracting_these_attribution_terms": delta["annual_excess"] - removed / .3,
                "operation": "Subtract at most five largest positive realized return attribution terms. Keep original annual denominators, all memberships, IC and turnover unchanged. No new candidate or rescore."}

    summary = {"status": "descriptive_attribution_only", "year": year, "days": len(daily),
               "counts": counts, "metrics": metrics, "candidate_minus_base": delta,
               "score_contributions": contributions, "monthly_contributions_using_full_year_denominators": monthly,
               "annual_excess_minus_stock_sum_rounding_residual": delta["annual_excess"] - stock["annual_excess_delta_contribution"].sum(),
               "by_stock": by_stock.to_dict("records"),
               "remove_up_to_five_positive_return_days_attribution_only": removal(daily, "trade_date"),
               "remove_up_to_five_positive_return_stocks_attribution_only": removal(by_stock, "ts_code"),
               "max_identity_error": errors, "complete_official_score_defined": complete,
               "definitions": {
                   "return_top": "Official ex-post set: flag_limit_up==0 and y_ret_1d.notna(), >=100 rows, K=floor(N/10); identical pandas default sort_values ties. No extra price-valid mask.",
                   "turnover_top": "First pass uses only keys, flag and frozen final predictions: flag_limit_up==0, >=100, K=floor(N/10); reset after small pool; first pair undefined; no label filter.",
                   "stock_contribution": "Same-date candidate-only +y/K, base-only -y/K; common members cancel, equal add/drop counts. Identical benchmark pools mathematically cancel; each official sorted market mean and floating summation residual are retained explicitly (identity tolerance 1e-12).",
                   "annualization": "252 times equal-day arithmetic mean, not compounded account return. Annual component denominators remain separate; months sum to full-year contributions.",
                   "labels": "Labels influence outcomes and the official RETURN set only. They never alter final predictions or label-free turnover memberships. Missing labels are neither filled nor guessed.",
                   "missing_label_diagnostics": "Report missing Y in label-free Top, both K values, and return/turnover set differences. These are different definitions, not evidence of a causal trading fill.",
                   "sensitivity": "Post-hoc concentration diagnostics on fixed realized attribution terms; at most five positive days/stocks, deterministic ascending date/code ties. Not a new selection/gate or a performance estimate for a revised strategy.",
                   "undefined": "Nonexistent official components or degenerate IC stay null in JSON; no fabricated full score. Daily/stock files retain NaN where appropriate.",
               }, "new_candidate_created": False, "new_model_fitted": False, "selection_rule_changed": False}
    # Public aliases match the existing official daily evidence vocabulary.
    for name in PREDICTIONS:
        for target, source in (("rank_ic", "ic"), ("excess", "excess"),
                               ("top1_return", "top_return"), ("turnover", "turnover")):
            daily[f"{name}_{target}"] = daily[f"{source}_{name}"]
    return daily, stock[STOCK_COLUMNS], _safe(summary)


def synthetic_tests() -> dict:
    """Only generated data and temporary official-evaluator CSV fixtures."""
    rows = []
    for day in (20200102, 20200103, 20200203):
        for i in range(120):
            value = (i % 11 - 5) / 128
            rows.append({"trade_date": day, "ts_code": f"s{i:03}", "flag_limit_up": 0,
                         "y_ret_1d": value, "pred_base": float(i // 3),
                         "pred_candidate": float(i // 3 + (5 if (i + day) % 13 == 0 else 0))})
    frame = pd.DataFrame(rows)
    frame.loc[(frame.trade_date == 20200103) & (frame.ts_code == "s119"), "y_ret_1d"] = np.nan
    frame.loc[(frame.trade_date == 20200203) & (frame.ts_code == "s115"), "flag_limit_up"] = 1
    daily, stock, summary = attribute_year(frame)
    assert all(value <= 1e-12 for value in summary["max_identity_error"].values())
    assert (daily["added_n"] == daily["removed_n"]).all()
    checks = {"daily_stock_monthly_and_annual_additive_identities": True}
    # Direct original evaluate.py check exercises default tie ordering and its
    # different return/turnover eligibility and denominators, on synthetic CSVs.
    from evaluate import evaluate
    with tempfile.TemporaryDirectory(prefix="r8-attribution-synthetic-") as temporary:
        folder = Path(temporary)
        frame[["ts_code", "trade_date", "y_ret_1d"]].to_csv(folder / "测试集_Y.csv", index=False, float_format="%.17g")
        frame[["ts_code", "trade_date", "flag_limit_up"]].to_csv(folder / "测试集_X.csv", index=False)
        for name, column in PREDICTIONS.items():
            frame[["ts_code", "trade_date", column]].rename(columns={column: "pred"}).to_csv(
                folder / "submission.csv", index=False, float_format="%.17g")
            official = evaluate(str(folder / "submission.csv"), str(folder))
            for key, value in official.items():
                _close(summary["metrics"][name][key], value, f"synthetic official/{name}/{key}")
    checks["original_official_evaluator_default_ties_and_three_denominators"] = True
    frozen_columns = [c for c in daily if c.startswith("turnover_top_sha256") or c in ("turnover_base", "turnover_candidate", "delta_turnover")]
    poisoned = frame.copy()
    poisoned["y_ret_1d"] = np.nan
    missing_daily, missing_stock, missing_summary = attribute_year(poisoned)
    pd.testing.assert_frame_equal(daily[frozen_columns], missing_daily[frozen_columns])
    assert missing_stock.empty and missing_summary["metrics"]["base"]["final_score"] is None
    checks["labels_and_missingness_cannot_change_turnover_top"] = True
    for column in ("pred_candidate", "y_ret_1d"):
        constant = frame.copy()
        constant.loc[constant.trade_date == 20200102, column] = 0.
        constant_daily, _, constant_summary = attribute_year(constant)
        candidate_metrics = constant_summary["metrics"]["candidate"]
        assert candidate_metrics["ic_mean"] is None and candidate_metrics["ic_std"] is None
        assert candidate_metrics["final_score"] is None and candidate_metrics["icir"] == 0.
        assert constant_summary["counts"]["ic_days"] == 3
        assert np.isnan(constant_daily.iloc[0]["candidate_rank_ic"])
        _close(candidate_metrics["ic_positive_ratio"],
               np.mean(constant_daily["candidate_rank_ic"].to_numpy() > 0), "constant IC counted false")
    checks["constant_prediction_or_label_day_propagates_official_nan_ic"] = True
    prefix, prefix_stock, _ = attribute_year(frame[frame.trade_date <= 20200103].copy())
    unscaled = [c for c in daily if not c.startswith("annual_")]
    pd.testing.assert_frame_equal(prefix[unscaled].reset_index(drop=True), daily.head(2)[unscaled].reset_index(drop=True))
    pd.testing.assert_frame_equal(prefix_stock[[c for c in STOCK_COLUMNS if not c.startswith("annual_")]].reset_index(drop=True),
        stock[stock.trade_date <= 20200103][[c for c in STOCK_COLUMNS if not c.startswith("annual_")]].reset_index(drop=True))
    checks["future_append_keeps_unscaled_daily_and_stock_prefix"] = True
    identical = frame.copy()
    identical["pred_candidate"] = identical["pred_base"]
    same_daily, same_stock, same_summary = attribute_year(identical)
    assert same_stock.empty and same_summary["candidate_minus_base"]["final_score"] == 0.
    assert same_summary["remove_up_to_five_positive_return_stocks_attribution_only"]["count"] == 0
    checks["identical_candidates_empty_stock_attribution"] = True
    # One explicit replacement: 89 joins instead of 90, then returns to base.
    hand = []
    for date in (20200102, 20200103):
        for i in range(100):
            hand.append({"trade_date": date, "ts_code": f"s{i:03}", "flag_limit_up": 0,
                         "y_ret_1d": 1. if i == 89 else i / 1000,
                         "pred_base": float(i), "pred_candidate": float(101 if date == 20200102 and i == 89 else i)})
    h, s, j = attribute_year(pd.DataFrame(hand))
    _close(h.iloc[0]["delta_excess"], (1. - .090) / 10, "hand swap")
    _close(h.iloc[1]["turnover_candidate"], 2 / 11, "hand Jaccard")
    assert h.iloc[1]["turnover_base"] == 0. and h.iloc[0]["added_n"] == 1
    assert j["remove_up_to_five_positive_return_days_attribution_only"]["count"] == 1
    expected_removed = .3 * 252 / 2 * (1. - .090) / 10
    _close(j["remove_up_to_five_positive_return_days_attribution_only"]["removed_annual_score_return_contribution"],
           expected_removed, "sensitivity frozen denominator")
    checks["hand_swap_jaccard_and_sensitivity_without_reselection"] = True
    small = frame.copy()
    small.loc[(small.trade_date == 20200103) & (small.ts_code < "s030"), "flag_limit_up"] = 1
    reset, _, reset_summary = attribute_year(small)
    assert reset["turnover_eligible"].sum() == 0 and reset_summary["counts"]["turnover_pairs"] == 0
    assert reset_summary["metrics"]["base"]["final_score"] is None
    checks["small_pool_resets_turnover_history"] = True
    for bad in (frame.iloc[::-1], pd.concat([frame, frame.iloc[:1]], ignore_index=True),
                frame.assign(y_ret_1d=frame.y_ret_1d.astype("float32")),
                pd.concat([frame, frame.assign(trade_date=frame.trade_date + 10000)], ignore_index=True)):
        try:
            attribute_year(bad)
        except ValueError:
            pass
        else:
            raise AssertionError("Malformed input was accepted")
    checks["reject_unsorted_duplicate_float32_and_mixed_years"] = True
    json.dumps(summary, allow_nan=False)
    json.dumps(missing_summary, allow_nan=False)
    json.dumps(reset_summary, allow_nan=False)
    checks["strict_json_handles_undefined_components"] = True
    return {"status": "passed", "synthetic_only": True, "historical_data_read": False, "checks": checks}


if __name__ == "__main__":
    print(json.dumps(synthetic_tests(), ensure_ascii=False, indent=2, allow_nan=False))
