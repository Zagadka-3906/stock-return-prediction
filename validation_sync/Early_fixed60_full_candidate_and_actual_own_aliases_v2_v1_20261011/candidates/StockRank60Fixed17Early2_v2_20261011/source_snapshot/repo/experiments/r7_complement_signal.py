"""Fixed 10% neural complement to the corrected R4 raw ranking signal.

The caller supplies an already key-aligned neural raw array. Both raw signals
are ranked in the same current valid-price pool, before R4's unchanged EMA,
persistence, protected ordering and 25% pooled auxiliary ordering. Limit-up
stocks remain in this ranking pool; the original postprocessor handles them.
This weight is a rank-signal weight, not a portfolio allocation.

Only weight=.10 is the real candidate. Endpoints are supported for synthetic
invariants: zero bypasses re-ranking and reconstructs R4 exactly; one uses the
neural percentile. No labels or label availability enter either API. Calls
start a fresh historical state, as in the existing per-year R4 replay.

This module never loads caches, scores candidates, trains models or writes
artifacts. Run ``python -B experiments/r7_complement_signal.py --test``.
"""

from __future__ import annotations

import argparse
import json
from numbers import Real
from pathlib import Path
import sys

sys.dont_write_bytecode = True
if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import numpy as np
import polars as pl
from scipy.stats import rankdata

from experiments.cached_recheck import BASE_CONFIG, make_prediction
from src.scoring import Panel


CANDIDATE_WEIGHT = 0.10
POOLED_WEIGHT = 0.25
EXPECTED_POST = {"alpha": 0.9, "bonus": 0.3,
                 "restore_lower": True, "top_current_weight": 1.0}


def _inputs(frame: pl.DataFrame, neural_raw: np.ndarray,
            weight: float) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Validate alignment without sorting, filtering or using label columns."""
    if not isinstance(frame, pl.DataFrame) or frame.is_empty():
        raise ValueError("frame must be a nonempty Polars DataFrame")
    required = {"trade_date", "ts_code", "price_valid", "pred_raw"}
    if not required.issubset(frame.columns):
        raise ValueError(f"Missing columns: {sorted(required - set(frame.columns))}")
    if not isinstance(weight, Real):
        raise ValueError("weight must be a finite scalar in [0, 1]")
    if not np.isfinite(weight) or not 0 <= weight <= 1:
        raise ValueError("weight must be a finite scalar in [0, 1]")
    keys = frame.select("trade_date", "ts_code")
    if any(keys.null_count().row(0)):
        raise ValueError("Keys must not contain nulls")
    if not keys.equals(keys.sort("trade_date", "ts_code")):
        raise ValueError("Keys must already be sorted by trade_date, ts_code")
    n_days = frame["trade_date"].n_unique()
    if frame.height % n_days:
        raise ValueError("Keys must form a rectangular panel")
    n_codes = frame.height // n_days
    dates = frame["trade_date"].to_numpy().reshape(n_days, n_codes)
    codes = frame["ts_code"].to_numpy().reshape(n_days, n_codes)
    if not np.all(dates == dates[:, :1]) or not np.all(codes == codes[:1]):
        raise ValueError("Each date must contain the same ordered stock codes")
    if np.unique(codes[0]).size != n_codes:
        raise ValueError("Keys must be unique")
    valid_series = frame["price_valid"]
    if valid_series.dtype != pl.Boolean or valid_series.null_count():
        raise ValueError("price_valid must be non-null Boolean")
    valid = valid_series.to_numpy().reshape(n_days, n_codes)
    try:
        base = frame["pred_raw"].cast(pl.Float64).to_numpy()
        neural = np.asarray(neural_raw, dtype=np.float64)
    except (TypeError, ValueError, pl.exceptions.PolarsError) as exc:
        raise ValueError("Both raw signals must be numeric") from exc
    if neural.shape != (frame.height,):
        raise ValueError("neural_raw must be a one-dimensional aligned array")
    base = base.reshape(valid.shape)
    neural = neural.reshape(valid.shape)
    if not np.isfinite(base[valid]).all() or not np.isfinite(neural[valid]).all():
        raise ValueError("Every valid-price row must have two finite raw signals")
    return base, neural, valid


def blend_raw(frame: pl.DataFrame, neural_raw: np.ndarray,
              weight: float = CANDIDATE_WEIGHT) -> np.ndarray:
    """Return aligned Float64 ranks; invalid-price rows are exactly -10.

    For a daily valid-price set S of size n, the actual candidate is
    .90 * average_rank(R4_raw[S])/n + .10 * average_rank(neural_raw[S])/n.
    Valid rows are never dropped because one signal is nonfinite: that is an
    input error, including at weight=0. Keys must already be sorted/rectangular.
    """
    base, neural, valid = _inputs(frame, neural_raw, weight)
    out = np.full(base.shape, -10.0, dtype=np.float64)
    if weight == 0:
        out[valid] = base[valid]
        return out.reshape(-1)
    for day, mask in enumerate(valid):
        count = int(mask.sum())
        if count:
            left = rankdata(base[day, mask], method="average") / count
            right = rankdata(neural[day, mask], method="average") / count
            out[day, mask] = (1 - weight) * left + weight * right
    return out.reshape(-1)


def prediction(frame: pl.DataFrame, neural_raw: np.ndarray,
               weight: float = CANDIDATE_WEIGHT) -> np.ndarray:
    """Apply R4's complete fixed postprocessor to the complemented raw signal.

    The original aux_raw values, protected-group percentile calculation and
    nonfinite-aux fallback are unchanged. Dummy labels satisfy Panel's schema;
    user labels and future_available are deliberately never read. As in R4,
    invalid-price final scores are below -1 (persistence can add .3 to -10).
    """
    mixed = blend_raw(frame, neural_raw, weight)
    if BASE_CONFIG != EXPECTED_POST:
        raise RuntimeError("The fixed R4 postprocessing configuration changed")
    if not {"aux_raw", "flag_limit_up"}.issubset(frame.columns):
        raise ValueError("prediction requires aux_raw and flag_limit_up")
    up = frame["flag_limit_up"]
    if up.null_count() or not up.is_in([0, 1]).all():
        raise ValueError("flag_limit_up must contain only non-null 0/1 values")
    auxiliary = frame["aux_raw"].cast(pl.Float64).to_numpy()
    sanitized = frame.select("trade_date", "ts_code", "price_valid", "flag_limit_up").with_columns(
        pl.Series("pred_raw", mixed), pl.lit(None, dtype=pl.Float64).alias("y_ret_1d"))
    panel = Panel.from_frame(sanitized)
    return make_prediction(panel, auxiliary, "top_only", POOLED_WEIGHT)


def tests() -> dict:
    """Run only generated synthetic inputs; no historical data or scoring."""
    checks = {}

    def equal(name: str, actual: np.ndarray, expected: np.ndarray) -> None:
        np.testing.assert_array_equal(actual, expected, err_msg=name)
        checks[name] = True

    def rejects(name: str, action) -> None:
        try:
            action()
        except ValueError:
            checks[name] = True
        else:
            raise AssertionError(f"{name}: expected ValueError")

    tiny = pl.DataFrame({"trade_date": [1] * 4, "ts_code": list("abcd"),
                         "price_valid": [True, True, True, False],
                         "pred_raw": [2.0, 2.0, 5.0, float("nan")],
                         "flag_limit_up": [0, 1, 0, 0],
                         "aux_raw": [4.0, 3.0, 2.0, float("nan")]})
    nn = np.array([9.0, 3.0, 3.0, np.inf])
    equal("hand_calculated_ties_common_pool", blend_raw(tiny, nn),
          np.array([0.9 * 0.5 + 0.1, 0.9 * 0.5 + 0.1 * 0.5,
                    0.9 + 0.1 * 0.5, -10.0]))
    equal("one_endpoint_neural_rank", blend_raw(tiny, nn, 1), np.array([1., .5, .5, -10.]))
    equal("zero_endpoint_keeps_raw", blend_raw(tiny, nn, 0), np.array([2., 2., 5., -10.]))
    assert blend_raw(tiny, nn).dtype == np.float64
    checks["float64_output"] = True
    all_invalid = tiny.with_columns(pl.lit(False).alias("price_valid"))
    equal("empty_daily_valid_pool", blend_raw(all_invalid, nn), np.full(4, -10.))
    equal("all_invalid_post", prediction(all_invalid, nn), np.full(4, -10.))
    equal("singleton_pool", blend_raw(tiny.head(1), nn[:1]), np.ones(1))
    assert np.isfinite(prediction(tiny, nn)).all() and prediction(tiny, nn)[-1] < -1
    checks["small_pool_post"] = True
    for value in (np.nan, np.inf, -np.inf):
        bad_nn = nn.copy()
        bad_nn[0] = value
        rejects(f"neural_nonfinite_{value}", lambda x=bad_nn: blend_raw(tiny, x))
        rejects(f"neural_nonfinite_even_zero_{value}", lambda x=bad_nn: blend_raw(tiny, x, 0))
        bad_raw = tiny.with_columns(pl.Series("pred_raw", [value, 2., 5., np.nan]))
        rejects(f"r4_nonfinite_{value}", lambda f=bad_raw: blend_raw(f, nn))
    rejects("neural_bad_shape", lambda: blend_raw(tiny, nn.reshape(1, 4)))
    rejects("neural_bad_length", lambda: blend_raw(tiny, nn[:3]))
    for value in (-.1, 1.1, np.nan, np.inf, "0.1", [.1], None, .1 + .2j):
        rejects(f"bad_weight_{value}", lambda w=value: blend_raw(tiny, nn, w))
    rejects("empty_frame", lambda: blend_raw(tiny.head(0), nn[:0]))
    rejects("missing_required", lambda: blend_raw(tiny.drop("pred_raw"), nn))
    rejects("unsorted_keys", lambda: blend_raw(tiny.reverse(), nn))
    duplicate = tiny.with_columns(pl.Series("ts_code", ["a", "a", "c", "d"]))
    rejects("duplicate_keys", lambda: blend_raw(duplicate, nn))
    null_key = tiny.with_columns(pl.Series("ts_code", [None, "b", "c", "d"]))
    rejects("null_keys", lambda: blend_raw(null_key, nn))
    for valid in ([True, None, True, False], [1, 1, 1, 0]):
        bad = tiny.with_columns(pl.Series("price_valid", valid))
        rejects(f"bad_valid_dtype_or_null_{valid}", lambda f=bad: blend_raw(f, nn))

    # Six dates and 120 codes exercise the original >=100-stock retention state,
    # invalid-price gaps and resumption, limit-up eligibility, and pooled ranks.
    n, days = 120, 6
    stock = np.tile(np.arange(n), days)
    day = np.repeat(np.arange(days), n)
    valid = ~(((day == 2) | (day == 3)) & (stock < 3))
    raw = ((stock * 17 + day * 11) % n).astype(np.float64)
    neural = ((stock * 13 - day * 7) % n).astype(np.float64)
    raw[~valid] = -10
    frame = pl.DataFrame({"trade_date": day + 1,
                          "ts_code": [f"S{i:03d}" for i in stock],
                          "price_valid": valid, "pred_raw": raw,
                          "flag_limit_up": ((stock + day) % 17 == 0).astype(int),
                          "aux_raw": ((stock * 19 + day * 3) % n).astype(float),
                          "y_ret_1d": (stock - 60) / 1000,
                          "future_available": day < 5})
    before = frame.clone()
    nn_before = neural.copy()
    direct = make_prediction(Panel.from_frame(frame), frame["aux_raw"].to_numpy(), "top_only", .25)
    equal("weight_zero_exact_r4_post", prediction(frame, neural, 0), direct)
    pred = prediction(frame, neural)
    assert pred.dtype == np.float64 and np.isfinite(pred).all() and (pred[~valid] < -1).all()
    checks["post_finite_and_invalid_excluded"] = True
    # Replay the unchanged original API with exactly the generated mixed raw.
    mixed = blend_raw(frame, neural)
    original_api = make_prediction(Panel.from_frame(frame.with_columns(pl.Series("pred_raw", mixed))),
                                   frame["aux_raw"].to_numpy(), "top_only", .25)
    equal("complete_original_post_and_aux", pred, original_api)
    altered_labels = frame.with_columns(pl.lit(float("nan")).alias("y_ret_1d"),
                                        (~pl.col("future_available")).alias("future_available"))
    equal("labels_and_future_availability_ignored", prediction(altered_labels, neural), pred)
    equal("label_columns_unnecessary", prediction(frame.drop("y_ret_1d", "future_available"), neural), pred)
    cutoff = 4 * n
    equal("prefix_raw", blend_raw(frame.head(cutoff), neural[:cutoff]), mixed[:cutoff])
    equal("prefix_post", prediction(frame.head(cutoff), neural[:cutoff]), pred[:cutoff])
    future_raw, future_neural = raw.copy(), neural.copy()
    future_raw[cutoff:] *= -7
    future_neural[cutoff:] *= -11
    future = frame.with_columns(pl.Series("pred_raw", future_raw),
                               pl.when(pl.col("trade_date") > 4).then(-pl.col("aux_raw"))
                               .otherwise(pl.col("aux_raw")).alias("aux_raw"))
    equal("future_signals_do_not_change_past_raw", blend_raw(future, future_neural)[:cutoff], mixed[:cutoff])
    equal("future_signals_do_not_change_past_post", prediction(future, future_neural)[:cutoff], pred[:cutoff])
    transformed = frame.with_columns((3 * pl.col("pred_raw") + 7).alias("pred_raw"))
    equal("monotone_transform_raw", blend_raw(transformed, 2 * neural - 13), mixed)
    equal("monotone_transform_post", prediction(transformed, 2 * neural - 13), pred)
    equal("monotone_transform_preserves_ties", blend_raw(tiny.with_columns(
        (3 * pl.col("pred_raw") + 7).alias("pred_raw")), 2 * nn - 13), blend_raw(tiny, nn))
    assert frame.equals(before)
    equal("neural_input_not_mutated", neural, nn_before)
    checks["frame_not_mutated"] = True
    rejects("nonrectangular_keys", lambda: blend_raw(frame.head(frame.height - 1), neural[:-1]))
    changed_code = frame.with_columns(pl.when((pl.col("trade_date") == days) & (pl.col("ts_code") == "S119"))
                                     .then(pl.lit("S120")).otherwise(pl.col("ts_code")).alias("ts_code"))
    rejects("different_daily_code_set", lambda: blend_raw(changed_code, neural))
    unequal_days = frame.with_columns(pl.when((pl.col("trade_date") == 2) & (pl.col("ts_code") == "S000"))
                                     .then(pl.lit(1)).otherwise(pl.col("trade_date")).alias("trade_date"))
    rejects("unequal_daily_counts", lambda: blend_raw(unequal_days.sort("trade_date", "ts_code"), neural))
    rejects("missing_aux", lambda: prediction(frame.drop("aux_raw"), neural))
    rejects("bad_limit_flag", lambda: prediction(frame.with_columns(pl.lit(None).alias("flag_limit_up")), neural))
    # Retain the existing whole-day fallback when pooled raw is nonfinite.
    missing_aux = frame.with_columns(pl.lit(float("nan")).alias("aux_raw"))
    reference_missing_aux = make_prediction(Panel.from_frame(missing_aux.with_columns(pl.Series("pred_raw", mixed))),
                                           missing_aux["aux_raw"].to_numpy(), "top_only", .25)
    equal("unchanged_nonfinite_aux_fallback", prediction(missing_aux, neural), reference_missing_aux)
    return {"status": "passed", "candidate_weight": CANDIDATE_WEIGHT,
            "pooled_weight": POOLED_WEIGHT, "check_count": len(checks), "checks": checks,
            "historical_data_read": False, "historical_candidates_scored": False}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--test", action="store_true", required=True,
                        help="Run synthetic invariants and print JSON only")
    parser.parse_args()
    print(json.dumps(tests(), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
