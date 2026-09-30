"""Descriptive complementarity of two existing raw signals; never a blend.

The caller freezes this source and inputs before evaluating historical data.
No model fitting, weight choice, official scoring, or artifact writing occurs
here. Labels affect outcome diagnostics only, never signal ranks or Top sets.
"""
from __future__ import annotations

import hashlib
import json

import numpy as np
import polars as pl
from scipy.stats import rankdata

KEYS = ["ts_code", "trade_date"]
MIN_CORRELATION_ROWS = 3
RESIDUAL_RELATIVE_TOLERANCE = 1e-12
GROUPS = ("top_r4", "top_neural", "top_common", "top_r4_only", "top_neural_only")


def _pearson(x: np.ndarray, y: np.ndarray) -> float | None:
    if len(x) < MIN_CORRELATION_ROWS:
        return None
    a, b = x - x.mean(), y - y.mean()
    aa, bb = float(a @ a), float(b @ b)
    if aa <= 0.0 or bb <= 0.0:
        return None
    value = float((a @ b) / np.sqrt(aa * bb))
    return float(np.clip(value, -1.0, 1.0)) if np.isfinite(value) else None


def _spearman(x: np.ndarray, y: np.ndarray) -> float | None:
    if len(x) < MIN_CORRELATION_ROWS:
        return None
    return _pearson(rankdata(x, method="average"), rankdata(y, method="average"))


def _partial_rank_ic(base: np.ndarray, neural: np.ndarray, y: np.ndarray) -> float | None:
    """OLS residual correlation of ranks on the SAME labeled sample.

    This is an outcome diagnostic, not an inference-time residual signal.
    An intercept and base ranks are removed from both neural and label ranks.
    Constant conditioning ranks or near-zero residual variance return null.
    """
    if len(y) < MIN_CORRELATION_ROWS:
        return None
    b, t, target = [rankdata(a, method="average") for a in (base, neural, y)]
    b, t, target = b - b.mean(), t - t.mean(), target - target.mean()
    bb = float(b @ b)
    if bb <= 0.0:
        return None
    residual_t = t - b * float((b @ t) / bb)
    residual_y = target - b * float((b @ target) / bb)
    for residual, original in ((residual_t, t), (residual_y, target)):
        original_norm = float(np.linalg.norm(original))
        if (original_norm <= 0.0 or float(np.linalg.norm(residual))
                <= RESIDUAL_RELATIVE_TOLERANCE * original_norm):
            return None
    return _pearson(residual_t, residual_y)


def _member_sha(codes: np.ndarray, indices: np.ndarray) -> str:
    members = sorted(str(code) for code in codes[indices])
    encoded = json.dumps(members, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _top_indices(pool: np.ndarray, values: np.ndarray, k: int) -> np.ndarray:
    # Frame rows have already been sorted by code; stable ties use that order.
    return pool[np.argsort(-values[pool], kind="stable")[:k]]


def diagnose(frame: pl.DataFrame, neural_raw: np.ndarray) -> tuple[pl.DataFrame, dict]:
    """Diagnose existing r4 raw and neural raw, without constructing a mixture.

    neural_raw must align positionally with the supplied frame BEFORE sorting.
    Required columns: ts_code, trade_date, pred_raw, price_valid, flag_limit_up,
    and original Float64 y_ret_1d. The function never modifies its inputs.
    Returns one scalar-only wide row per market date plus date-equal summaries.
    """
    required = KEYS + ["pred_raw", "price_valid", "flag_limit_up", "y_ret_1d"]
    if not set(required).issubset(frame.columns) or not len(frame):
        raise ValueError("A nonempty frame with keys, both state flags and raw Float64 labels is required")
    if frame["y_ret_1d"].dtype != pl.Float64:
        raise TypeError("Original y_ret_1d must remain Float64")
    if frame["price_valid"].dtype != pl.Boolean or frame["price_valid"].null_count():
        raise TypeError("price_valid must be nonnull Boolean")
    if any(frame[column].null_count() for column in KEYS + ["flag_limit_up"]):
        raise ValueError("Keys and flag_limit_up must be nonnull")
    if frame.select(KEYS).n_unique() != len(frame):
        raise ValueError("Duplicate date/code keys")
    neural = np.asarray(neural_raw, dtype=np.float64)
    if neural.ndim != 1 or len(neural) != len(frame):
        raise ValueError("neural_raw must be one flat vector aligned with frame rows")
    joined = frame.select(required).with_columns(pl.Series("_neural", neural)).sort("trade_date", "ts_code")
    rows = []
    for day in joined.partition_by("trade_date", maintain_order=True):
        date = int(day["trade_date"][0])
        codes = day["ts_code"].to_numpy()
        base = day["pred_raw"].cast(pl.Float64).to_numpy()
        neural = day["_neural"].to_numpy()
        labels = day["y_ret_1d"].to_numpy()
        price = day["price_valid"].to_numpy()
        up = day["flag_limit_up"].to_numpy()
        common = price & np.isfinite(base) & np.isfinite(neural)
        indices = np.flatnonzero(common)
        percentiles = np.full(len(day), np.nan)
        if len(indices):
            percentiles[indices] = rankdata(base[indices], method="average") / len(indices)
        # The percentile bins are defined before looking at any label. A tie
        # shares its midrank bin; bins need not have equal numbers of stocks.
        bins = np.full(len(day), -1, dtype=np.int8)
        bins[indices] = np.clip(np.ceil(percentiles[indices] * 10).astype(int) - 1, 0, 9)
        pool = np.flatnonzero(common & (up == 0))
        k = max(len(pool) // 10, 1) if len(pool) else 0
        top_b = _top_indices(pool, base, k)
        top_t = _top_indices(pool, neural, k)
        groups = {"top_r4": top_b, "top_neural": top_t,
                  "top_common": np.intersect1d(top_b, top_t),
                  "top_r4_only": np.setdiff1d(top_b, top_t),
                  "top_neural_only": np.setdiff1d(top_t, top_b)}
        # All group membership and signal-only correlation above are fixed
        # without return availability. From here on labels are measurement.
        labeled = common & np.isfinite(labels)
        union_n = len(np.union1d(top_b, top_t))
        row = {"trade_date": date, "panel_n": len(day), "price_valid_n": int(price.sum()),
               "common_n": int(common.sum()), "common_y_n": int(labeled.sum()),
               "price_valid_nonfinite_signal_n": int((price & ~common).sum()),
               "common_y_coverage": float(labeled.sum() / common.sum()) if common.any() else None,
               "raw_rank_correlation": _spearman(base[common], neural[common]),
               "r4_rank_ic": _spearman(base[labeled], labels[labeled]),
               "neural_rank_ic": _spearman(neural[labeled], labels[labeled]),
               "neural_partial_rank_ic_given_r4": _partial_rank_ic(base[labeled], neural[labeled], labels[labeled]),
               "top_pool_n": len(pool), "top_k": k,
               "top_jaccard": float(len(groups["top_common"]) / union_n) if union_n else None}
        for decile in range(10):
            mask = bins == decile
            known = mask & np.isfinite(labels)
            prefix = f"r4_decile_{decile + 1:02d}"
            row[prefix + "_n"] = int(mask.sum())
            row[prefix + "_y_n"] = int(known.sum())
            row[prefix + "_y_coverage"] = float(known.sum() / mask.sum()) if mask.any() else None
            row[prefix + "_neural_ic"] = _spearman(neural[known], labels[known])
        for name, members in groups.items():
            outcomes = labels[members]
            finite = np.isfinite(outcomes)
            row[name + "_n"] = len(members)
            row[name + "_members_sha256"] = _member_sha(codes, members)
            row[name + "_y_n"] = int(finite.sum())
            row[name + "_y_coverage"] = float(finite.mean()) if len(members) else None
            row[name + "_mean_y1"] = float(outcomes[finite].mean()) if finite.any() else None
        rows.append(row)

    # Preserve Float64 even when every value of a degenerate metric is null.
    float_columns = [key for key in rows[0] if key not in ("trade_date", "top_k")
                     and not key.endswith("_n") and not key.endswith("_sha256")]
    daily = pl.DataFrame(rows, schema_overrides={key: pl.Float64 for key in float_columns})
    means, valid_days = {}, {}
    for column in daily.columns:
        if column == "trade_date" or column.endswith("_sha256"):
            continue
        values = daily[column].cast(pl.Float64).to_numpy()
        finite = np.isfinite(values)
        means[column] = float(values[finite].mean()) if finite.any() else None
        valid_days[column] = int(finite.sum())
    summary = {
        "status": "descriptive_diagnostics_only", "days": len(daily),
        "first_date": int(daily["trade_date"].min()), "last_date": int(daily["trade_date"].max()),
        "date_equal_mean": means, "valid_days": valid_days,
        "minimum_correlation_rows": MIN_CORRELATION_ROWS,
        "residual_relative_tolerance": RESIDUAL_RELATIVE_TOLERANCE,
        "definitions": {
            "common_pool": "Current price_valid AND finite r4 raw AND finite neural raw; includes limit-up stocks; independent of labels.",
            "rank_ic_pool": "Common pool intersect finite original Float64 one-day labels, identical for both signals and partial IC.",
            "partial_rank_ic": "Average-tie rank all three variables within the same labeled sample; remove intercept and r4 rank from neural rank and label rank; Pearson correlation of residuals. Degenerate conditioning or residual variance is null.",
            "r4_deciles": "Daily r4 average-tie percentile over the common pool, fixed bins (0,.1],(.1,.2],...,(.9,1]; ties stay together. Neural IC is measured only afterwards on observed labels within each bin.",
            "top_pool": "Current common pool AND flag_limit_up==0; K=max(floor(pool_n/10),1) if nonempty, else0. Stable code-order ties. No minimum100 rule because this is a descriptive membership diagnostic.",
            "top_outcomes": "Members fixed before labels; group mean of observed original one-day returns in decimal units, plus observed/selected coverage. No missing-label backfill, zero fill, excess benchmark, annualization, or costs.",
            "aggregation": "Each reported metric equally weights dates on which that metric is finite. Empty groups/degenerate correlations are null; valid_days is explicit. Means of counts are mean daily counts, not pooled performance.",
            "membership_hashes": "SHA256 of each day's sorted code list in canonical UTF-8 JSON; enables label/missingness-invariance checks without nested CSV columns.",
        },
        "limitations": [
            "Official IC uses all nonmissing-label rows, including limit-up and price-invalid rows; this diagnostic uses a common price-valid pool.",
            "Official return Top filters nonlimit and observed-label rows BEFORE selection; official turnover Top filters nonlimit rows WITHOUT a label mask. Neither equals this diagnostic Top pool in general.",
            "Partial or conditional IC and low rank correlation do not establish better official score, an optimal weight, causal attribution, or executable returns.",
            "Any outcome residualization is retrospective measurement only, never an inference-time signal. All historical years have already been viewed.",
            "No naive t statistics, selection-adjusted inference, win rate, or trading claim is produced.",
        ],
        "mixed_predictions_created": False, "weights_selected": False,
        "official_score_computed": False, "new_model_fitted": False,
    }
    return daily, summary


def synthetic_tests() -> dict:
    """No historical files read, no scores/blends generated, no artifacts written."""
    base = np.repeat(np.array([-1., 0., 1.]), 3)
    neural = np.tile(np.array([-1., 0., 1.]), 3)
    frame = pl.DataFrame({"trade_date": [20200102] * 9,
        "ts_code": [f"s{i:02d}" for i in range(9)], "pred_raw": base,
        "price_valid": [True] * 9, "flag_limit_up": [0] * 9,
        "y_ret_1d": neural * .01})
    daily, summary = diagnose(frame, neural)
    r = daily.row(0, named=True)
    assert abs(r["raw_rank_correlation"]) < 1e-14
    assert abs(r["r4_rank_ic"]) < 1e-14 and abs(r["neural_rank_ic"] - 1.) < 1e-14
    assert abs(r["neural_partial_rank_ic_given_r4"] - 1.) < 1e-14
    assert [r[f"r4_decile_{i:02d}_n"] for i in (3, 6, 9)] == [3, 3, 3]
    assert sum(r[f"r4_decile_{i:02d}_n"] for i in range(1, 11)) == 9
    assert all(r[f"r4_decile_{i:02d}_neural_ic"] == 1. for i in (3, 6, 9))
    collinear, _ = diagnose(frame, 2 * base + 7)
    assert collinear["neural_partial_rank_ic_given_r4"][0] is None
    constant, _ = diagnose(frame.with_columns(pl.lit(.03, dtype=pl.Float64).alias("y_ret_1d")), neural)
    assert constant["neural_partial_rank_ic_given_r4"][0] is None

    poisoned, _ = diagnose(frame.with_columns((-pl.col("y_ret_1d")).alias("y_ret_1d")), neural)
    label_independent = ["raw_rank_correlation", "common_n", "top_pool_n", "top_k", "top_jaccard"]
    label_independent += [name + suffix for name in GROUPS for suffix in ("_n", "_members_sha256")]
    label_independent += [f"r4_decile_{i:02d}_n" for i in range(1, 11)]
    assert daily.select(label_independent).equals(poisoned.select(label_independent))
    assert poisoned["neural_rank_ic"][0] == -1.
    # Neural Top is s02 under stable code-order ties. Removing its future label
    # must not replace it with equally ranked but observed s05/s08.
    missing = frame.with_columns(pl.when(pl.col("ts_code") == "s02")
        .then(pl.lit(None, dtype=pl.Float64)).otherwise(pl.col("y_ret_1d")).alias("y_ret_1d"))
    absent, _ = diagnose(missing, neural)
    assert daily.select(label_independent).equals(absent.select(label_independent))
    assert absent["top_neural_n"][0] == 1 and absent["top_neural_y_n"][0] == 0
    assert absent["top_neural_y_coverage"][0] == 0. and absent["top_neural_mean_y1"][0] is None

    invalid = pl.concat([frame, pl.DataFrame({"trade_date": [20200102], "ts_code": ["invalid"],
        "pred_raw": [1e20], "price_valid": [False], "flag_limit_up": [0], "y_ret_1d": [123.]})])
    invalid_daily, _ = diagnose(invalid, np.r_[neural, 1e30])
    assert daily.select(label_independent).equals(invalid_daily.select(label_independent))
    limited = frame.with_columns(pl.when(pl.col("ts_code") == "s02").then(1).otherwise(0).alias("flag_limit_up"))
    limited_daily, _ = diagnose(limited, neural)
    assert limited_daily["common_n"][0] == 9 and limited_daily["top_pool_n"][0] == 8
    assert limited_daily["top_neural_members_sha256"][0] != daily["top_neural_members_sha256"][0]

    reverse, _ = diagnose(frame.reverse(), neural[::-1])
    assert daily.equals(reverse)
    later = frame.with_columns(pl.lit(20200103, dtype=pl.Int64).alias("trade_date"), (-pl.col("pred_raw")).alias("pred_raw"))
    both, _ = diagnose(pl.concat([frame, later]), np.r_[neural, -neural])
    assert daily.equals(both.head(1))
    empty, empty_summary = diagnose(frame.with_columns(pl.lit(False).alias("price_valid")), neural)
    assert empty["top_k"][0] == 0 and empty["raw_rank_correlation"][0] is None
    assert empty_summary["valid_days"]["raw_rank_correlation"] == 0
    nonfinite, _ = diagnose(frame, np.where(np.arange(9) == 0, np.inf, neural))
    assert nonfinite["common_n"][0] == 8 and nonfinite["price_valid_nonfinite_signal_n"][0] == 1
    # Different pool sizes still receive one unit of weight per date.
    small = frame.head(3).with_columns(pl.lit(20200104, dtype=pl.Int64).alias("trade_date"))
    _, unequal_summary = diagnose(pl.concat([frame, small]), np.r_[neural, neural[:3]])
    assert unequal_summary["date_equal_mean"]["common_n"] == 6.
    assert unequal_summary["valid_days"]["r4_rank_ic"] == 1
    for result in (summary, empty_summary, unequal_summary):
        json.dumps(result, allow_nan=False)
    errors = 0
    for bad in (frame.with_columns(pl.col("y_ret_1d").cast(pl.Float32)), pl.concat([frame, frame.head(1)])):
        try:
            diagnose(bad, np.resize(neural, len(bad)))
        except (ValueError, TypeError):
            errors += 1
    assert errors == 2
    return {"status": "passed", "independent_rank_signal_partial_ic": True,
        "collinear_and_constant_outcome_return_null": True, "tie_preserving_fixed_deciles": True,
        "labels_do_not_change_top_members_or_signal_correlation": True,
        "missing_top_label_does_not_backfill": True, "price_invalid_and_nonfinite_excluded": True,
        "limit_flag_changes_top_pool_only": True, "row_permutation_and_date_prefix_exact": True,
        "empty_pool_nulls_and_date_equal_aggregation": True, "float64_labels_and_unique_keys_required": True,
        "historical_data_read": False, "mixed_predictions_or_official_scores_created": False}


if __name__ == "__main__":
    print(json.dumps(synthetic_tests(), ensure_ascii=False, indent=2, allow_nan=False))
