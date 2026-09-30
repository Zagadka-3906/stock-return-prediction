"""Fixed anchor plus Float64 MSE / sampled average-tie RankIC correction heads.

No historical I/O, OOF generation, scoring, early stopping or model selection.
The caller supplies a rectangular, sorted panel of past, mature OOF rows.
All training groups and WLS calibration are shared. Booster predictions are
increments only: no init_score, boost_from_average=False, zero initial f.

RankIC uses frozen-weight logistic pseudo-gradients, not a gradient of hard
Spearman. A full-pair normalizer is computed exactly in O(n log n); uniform
unordered sampling has replacement and uses M/Q importance correction. Twice
the pair Hessian diagonal majorizes the sampled full Hessian. No row h floor.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
import tempfile
import time

sys.dont_write_bytecode = True
if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import lightgbm as lgb
import llvmlite
import numba
from numba import njit
import numpy as np
import polars as pl
from scipy.special import expit
from scipy.stats import rankdata, spearmanr

from experiments import r9_residual_core as r9

ROUNDS = 80
PAIRS_PER_ROW = 8
SIGMA = 1.
SEED = 2026
BASE_FEATURE_NAME = r9.BASE_FEATURE_NAME
PARAMS = {key: value for key, value in r9.PARAMS.items() if key not in {"objective", "metric"}}
PARAMS.update({"metric": "None", "boost_from_average": False,
               "min_sum_hessian_in_leaf": .001})


def versions() -> dict:
    return {"python": sys.version.split()[0], "numpy": np.__version__,
            "lightgbm": lgb.__version__, "numba": numba.__version__,
            "llvmlite": llvmlite.__version__}


def prepare(frame: pl.DataFrame, features: np.ndarray, feature_names: list[str]) -> dict:
    """Build one shared date-filtered training slice and positive-slope WLS.

    Returned matrix/target/anchor/weights/dates have selected rows only. mask,
    b, target_full and anchor_full align with every input panel row. Date
    exclusion uses b and u before WLS; positive affine calibration must then
    preserve ranks on ALL price-valid rows, including unlabelled ones.
    """
    if (len(feature_names) != 63 or len(set(feature_names)) != 63
            or BASE_FEATURE_NAME in feature_names):
        raise ValueError("Expected 63 distinct original feature names")
    values = np.asarray(features)
    if values.shape != (len(frame), 63):
        raise ValueError("X63 must align with every full-panel row")
    b, target_full = r9.base_percentile(frame), r9.target_percentile(frame)
    dates_full = frame["trade_date"].to_numpy()
    mask = np.isfinite(target_full)
    date_values, starts, counts = np.unique(dates_full, return_index=True, return_counts=True)
    excluded = []
    for date, start, count in zip(date_values, starts, counts):
        ix = np.flatnonzero(mask[start:start+count]) + start
        reasons = []
        if len(ix) < 2:
            reasons.append("fewer_than_two_finite_targets")
        else:
            if np.ptp(b[ix]) == 0:
                reasons.append("constant_base_in_target_pool")
            if np.ptp(target_full[ix]) == 0:
                reasons.append("constant_target")
        if reasons:
            mask[start:start+count] = False
            excluded.append({"trade_date": int(date), "finite_target_rows": int(len(ix)),
                             "reasons": reasons})
    if not mask.any():
        raise ValueError("Every date is degenerate; no common training slice")
    weights = r9.date_weights(frame, mask)[mask]
    normalized = r9.date_weights(frame, mask, normalize=True)[mask]
    normalized = normalized / normalized.sum()
    x, target = b[mask], target_full[mask]
    mean_x, mean_y = np.dot(normalized, x), np.dot(normalized, target)
    centered_x, centered_y = x - mean_x, target - mean_y
    variance = float(np.dot(normalized, centered_x * centered_x))
    if not np.isfinite(variance) or variance <= 0:
        raise ValueError("WLS base variance is not positive")
    slope = float(np.dot(normalized, centered_x * centered_y) / variance)
    intercept = float(mean_y - slope * mean_x)
    if not np.isfinite(slope) or slope <= 0 or not np.isfinite(intercept):
        raise ValueError("WLS requires a finite strictly positive slope; no fallback anchor")
    dates = np.asarray(dates_full[mask], dtype=np.int64)
    retained_dates = np.unique(dates)
    calibration = {"intercept": intercept, "slope": slope,
        "training_rows": int(mask.sum()), "training_dates": int(len(retained_dates)),
        "training_date_values": retained_dates.tolist(),
        "weight_sum": float(weights.sum()), "weight_mean": float(weights.mean()),
        "calibration_weight_sum": float(normalized.sum()),
        "feature_names": list(feature_names),
        "model_feature_names": list(feature_names) + [BASE_FEATURE_NAME],
        "params": dict(PARAMS), "rounds": ROUNDS,
        "target": "Average rank/n of original Float64 y in price_valid AND finite-y pool; includes limit-up",
        "base": "Average rank/n of raw R4 in complete current price_valid pool, independent of Y",
        "weights": "Common retained dates: tree N/(D*n_day), WLS normalized sum1",
        "precision": "Float64 targets, WLS, anchor and objective derivative construction; Float32 C-order X63+b; LGB casts returned g/h to Float32 before native update; labels are unused dummy zeros",
        "lightgbm_version": lgb.__version__}
    anchor_full = r9.calibrated_base(frame, b, calibration)
    anchor = anchor_full[mask]
    calibration["weighted_mse"] = float(np.dot(normalized, (anchor-target)**2))
    metadata = {"retained_training_rows": int(mask.sum()),
        "retained_training_dates": int(len(retained_dates)),
        "retained_date_values": retained_dates.tolist(),
        "excluded_degenerate_dates": excluded, "input_rows": len(frame),
        "finite_target_rows_before_group_filter": int(np.isfinite(target_full).sum()),
        "input_dates": int(len(date_values)), "feature_names": calibration["model_feature_names"],
        "matrix_dtype": "float32", "matrix_order": "C", "target_anchor_weight_dtype": "float64",
        "initial_increment": 0., "init_score": None, "boost_from_average": False,
        "versions": versions()}
    result = {"matrix": r9.make_matrix(values[mask], b[mask]),
        "target": np.ascontiguousarray(target, dtype=np.float64),
        "anchor": np.ascontiguousarray(anchor, dtype=np.float64),
        "weights": np.ascontiguousarray(weights, dtype=np.float64), "dates": dates,
        "mask": mask, "b": b, "target_full": target_full, "anchor_full": anchor_full,
        "calibration": calibration, "metadata": metadata}
    for value in result.values():
        if isinstance(value, np.ndarray):
            value.setflags(write=False)
    return result


@njit(cache=False)
def _average_ranks(values, order):
    result = np.empty(len(values), dtype=np.float64)
    first = 0
    while first < len(values):
        stop = first + 1
        while stop < len(values) and values[order[stop]] == values[order[first]]:
            stop += 1
        average = (first + 1 + stop) / 2.
        for cursor in range(first, stop):
            result[order[cursor]] = average
        first = stop
    return result


@njit(cache=False)
def _fenwick_sum(p, q, coordinates, order):
    """Exact sum |dp*dq| with four Fenwick moments and half-integer ranks."""
    tree = np.zeros((2 * len(p) + 1, 4), dtype=np.float64)
    total_count = total_p = total_q = total_pq = answer = 0.
    for at in order:
        x, y, index = p[at], q[at], coordinates[at]
        count = sum_p = sum_q = sum_pq = 0.
        cursor = index
        while cursor:
            count += tree[cursor, 0]
            sum_p += tree[cursor, 1]
            sum_q += tree[cursor, 2]
            sum_pq += tree[cursor, 3]
            cursor -= cursor & -cursor
        answer += x*y*count - y*sum_p - x*sum_q + sum_pq
        answer += x*(total_q-sum_q) - x*y*(total_count-count) - (total_pq-sum_pq) + y*(total_p-sum_p)
        total_count += 1.
        total_p += x
        total_q += y
        total_pq += x*y
        cursor = index
        while cursor < len(tree):
            tree[cursor, 0] += 1.
            tree[cursor, 1] += x
            tree[cursor, 2] += y
            tree[cursor, 3] += x*y
            cursor += cursor & -cursor
    return answer


def full_pair_normalizer(scores: np.ndarray, targets: np.ndarray) -> dict:
    """Diagnostic public helper; no O(n^2) storage and average ties throughout."""
    s, y = np.asarray(scores, dtype=np.float64), np.asarray(targets, dtype=np.float64)
    if s.ndim != 1 or y.shape != s.shape or len(s) < 2 or not np.isfinite(s).all() or not np.isfinite(y).all():
        raise ValueError("Two aligned finite one-dimensional groups with n>=2 are required")
    order = np.argsort(s, kind="stable")
    p, q = _average_ranks(s, order), rankdata(y, method="average")
    denominator = float(np.linalg.norm(p-p.mean()) * np.linalg.norm(q-q.mean()))
    absolute_sum = float(_fenwick_sum(p, q, (2*q).astype(np.int64), order))
    return {"p": p, "q": q, "C": denominator, "absolute_product_sum": absolute_sum,
            "sum_a": absolute_sum/denominator if denominator > 0 else 0.}


def sample_pairs(n: int, iteration: int, trade_date: int, draws: int | None = None) -> tuple[np.ndarray, np.ndarray]:
    """Uniform unordered pairs, with replacement; zero-weight ties stay sampled."""
    if n < 2 or iteration < 0 or trade_date < 0:
        raise ValueError("Invalid group size, zero-based iteration or date")
    draws = PAIRS_PER_ROW * n if draws is None else int(draws)
    if draws <= 0:
        raise ValueError("At least one draw is required")
    rng = np.random.default_rng(np.random.SeedSequence([SEED, iteration, int(trade_date)]))
    left = rng.integers(0, n, size=draws)
    right = rng.integers(0, n-1, size=draws)
    right += right >= left
    return np.minimum(left, right), np.maximum(left, right)


def frozen_pair_terms(scores, p, q, left, right, absolute_sum, mass, importance=1.) -> tuple[np.ndarray, np.ndarray, float, int]:
    """Frozen rank weights. Return g, twice diagonal Hessian, surrogate loss.

    a/sum(a) equals |dp*dq|/sum|dp*dq| because C cancels exactly. This
    cancellation avoids needless rescaling; the normalizer remains FULL-pair.
    mass=N/D and importance=M/Q for sampled calls, 1 for enumerated calls.
    """
    scores, p, q = map(lambda x: np.asarray(x, dtype=np.float64), (scores, p, q))
    n = len(scores)
    if absolute_sum <= 0 or mass <= 0 or importance <= 0:
        raise ValueError("Nonpositive pair normalization")
    raw_weight = np.abs((p[left]-p[right]) * (q[left]-q[right]))
    active = raw_weight > 0
    left, right, raw_weight = left[active], right[active], raw_weight[active]
    coefficient = (mass * importance / absolute_sum) * raw_weight
    direction = np.sign(q[left]-q[right])
    margin = SIGMA * direction * (scores[left]-scores[right])
    wrong = expit(-margin)
    pair_gradient = -SIGMA * coefficient * direction * wrong
    pair_hessian = SIGMA**2 * coefficient * wrong * (1-wrong)
    gradient = (np.bincount(left, weights=pair_gradient, minlength=n)
                - np.bincount(right, weights=pair_gradient, minlength=n))
    diagonal = (np.bincount(left, weights=pair_hessian, minlength=n)
                + np.bincount(right, weights=pair_hessian, minlength=n))
    loss = float(np.dot(coefficient, np.logaddexp(0., -margin)))
    return gradient, 2 * diagonal, loss, int(active.sum())


def _validate_prepared(prepared):
    matrix, target, anchor, weights, dates = (prepared[key] for key in ("matrix", "target", "anchor", "weights", "dates"))
    n = len(target)
    if matrix.shape != (n, 64) or matrix.dtype != np.float32 or not matrix.flags.c_contiguous:
        raise ValueError("Prepared matrix must be selected-row Float32 C-order X63+b")
    for key, array in (("target", target), ("anchor", anchor), ("weights", weights)):
        if array.shape != (n,) or array.dtype != np.float64 or not np.isfinite(array).all():
            raise ValueError(f"Prepared {key} must be finite aligned Float64")
    if dates.shape != (n,) or not np.issubdtype(dates.dtype, np.integer) or not np.all(dates[:-1] <= dates[1:]):
        raise ValueError("Prepared dates must be aligned sorted integers")
    if n == 0 or (weights <= 0).any():
        raise ValueError("Empty or nonpositive-weight training slice")
    unique, starts, counts = np.unique(dates, return_index=True, return_counts=True)
    if np.any(counts < 2):
        raise ValueError("Prepared group has fewer than two rows")
    for start, count in zip(starts, counts):
        sl = slice(start, start+count)
        if np.ptp(target[sl]) == 0 or np.ptp(anchor[sl]) == 0:
            raise ValueError("Prepared group remains degenerate")
        np.testing.assert_allclose(weights[sl], n/(len(unique)*count), rtol=1e-13, atol=0)
    return unique, starts, counts


def make_objective(prepared: dict, kind: str):
    """Return custom callable plus its JSON trace; callable reads Float64 arrays."""
    if kind not in {"mse", "rankic"}:
        raise ValueError("kind must be mse or rankic")
    unique, starts, counts = _validate_prepared(prepared)
    target, anchor, weights = (prepared[key] for key in ("target", "anchor", "weights"))
    n, days, history = len(target), len(unique), []
    q_groups = [rankdata(target[start:start+count], method="average") for start, count in zip(starts, counts)]
    q_coords = [(2*q).astype(np.int64) for q in q_groups]
    q_norms = [float(np.linalg.norm(q-q.mean())) for q in q_groups]

    def objective(increments, dataset):
        del dataset  # Native labels/weights/init_score never enter either loss.
        started, iteration = time.perf_counter(), len(history)
        increment = np.asarray(increments, dtype=np.float64)
        if increment.shape != anchor.shape or not np.isfinite(increment).all():
            raise ValueError("Increment predictions must be finite aligned Float64")
        scores = anchor + increment
        if not np.isfinite(scores).all():
            raise ValueError("Anchor plus increment overflow")
        if kind == "mse":
            residual = scores-target
            gradient, hessian = weights*residual, weights.copy()
            loss = float(.5*np.dot(weights, residual*residual)/n)
            record = {"iteration": iteration, "training_loss": loss,
                      "date_equal_mse": 2*loss, "active_days": days,
                      "degenerate_dates": [], "sampled_pairs": 0, "positive_weight_pairs": 0}
        else:
            gradient, hessian = np.zeros(n), np.zeros(n)
            loss, inactive, sampled, positive, normalizers = 0., [], 0, 0, []
            for day_index, (date, start, count) in enumerate(zip(unique, starts, counts)):
                stop = start+count
                s, q = scores[start:stop], q_groups[day_index]
                order = np.argsort(s, kind="stable")
                p = _average_ranks(s, order)
                p_norm = float(np.linalg.norm(p-p.mean()))
                absolute_sum = float(_fenwick_sum(p, q, q_coords[day_index], order))
                if p_norm == 0 or q_norms[day_index] == 0 or absolute_sum <= 0:
                    inactive.append(int(date))
                    continue
                normalizers.append(absolute_sum/(p_norm*q_norms[day_index]))
                left, right = sample_pairs(int(count), iteration, int(date))
                importance = (int(count)*(int(count)-1)/2) / len(left)
                g, h, current_loss, active_pairs = frozen_pair_terms(s, p, q, left, right, absolute_sum, n/days, importance)
                gradient[start:stop], hessian[start:stop] = g, h
                loss += current_loss
                sampled += len(left)
                positive += active_pairs
            record = {"iteration": iteration, "training_loss": loss/n,
                "active_days": days-len(inactive), "degenerate_dates": inactive,
                "sampled_pairs": int(sampled), "positive_weight_pairs": int(positive),
                "minimum_full_sum_a": min(normalizers) if normalizers else None,
                "maximum_full_sum_a": max(normalizers) if normalizers else None}
            if len(inactive) == days:
                record["error"] = "all_runtime_groups_degenerate"
                record["seconds"] = time.perf_counter()-started
                history.append(record)
                raise ValueError("All RankIC date groups became degenerate; no fallback or tie breaking")
        if not np.isfinite(gradient).all() or not np.isfinite(hessian).all() or (hessian < 0).any() or not np.isfinite(record["training_loss"]):
            raise ValueError("Nonfinite loss/derivative or negative Hessian")
        if iteration == 0:
            record["initial_increment_zero"] = bool(np.all(increment == 0))
        record["seconds"] = time.perf_counter()-started
        history.append(record)
        return gradient, hessian

    return objective, history


def fit(prepared: dict, kind: str) -> tuple[lgb.Booster, dict]:
    """Fit exactly the fixed requested rounds; natural no-split stops are recorded."""
    objective, history = make_objective(prepared, kind)
    dataset = lgb.Dataset(prepared["matrix"], label=np.zeros(len(prepared["target"]), dtype=np.float32),
                          feature_name=prepared["calibration"]["model_feature_names"], free_raw_data=True)
    params = dict(PARAMS)

    def from_zero_objective(increments, data):
        if not history and np.any(np.asarray(increments) != 0):
            raise ValueError("LightGBM did not start from an exactly zero increment")
        return objective(increments, data)

    params["objective"] = from_zero_objective
    booster = lgb.train(params, dataset, num_boost_round=ROUNDS)
    metadata = {"kind": kind, "params": dict(PARAMS), "requested_rounds": ROUNDS,
        "objective_calls": len(history), "actual_booster_iterations": booster.current_iteration(),
        "actual_trees": booster.num_trees(), "initial_increment": 0., "init_score": None,
        "initial_increment_verified": bool(history and history[0]["initial_increment_zero"]),
        "native_dataset_labels": "unused Float32 zero placeholders; no dataset weights",
        "objective_arrays": "Float64 target/anchor/weights captured from the common prepared slice",
        "native_derivative_boundary": "LightGBM 4.7.0 Python Booster.__boost casts custom gradients/Hessians to Float32 before the native call",
        "training_rows": len(prepared["target"]), "training_dates": len(np.unique(prepared["dates"])),
        "mse_formula": "g=w*(f+anchor-u), h=w; w=N/(D*n_day), loss=0.5*sum(w*residual^2)",
        "rankic_formula": "a=abs(dp*dq)/C; coefficient=(N/D)*(M/Q)*a/sum_full(a); sigma=1; g of frozen-weight logistic; h=2*pair diagonal majorizer",
        "sampling": {"draws_per_row": PAIRS_PER_ROW, "replacement": True, "unordered": True,
                     "seed": "SeedSequence([2026, zero_based_objective_call, integer_trade_date])",
                     "zero_weight_ties": "retained in draw denominator, never resampled"},
        "runtime_degenerate_policy": "g=h=0 for that date; retain original N,D; all dates degenerate raises",
        "row_hessian_floor": None, "leaf_min_sum_hessian": PARAMS["min_sum_hessian_in_leaf"],
        "trace_usage": "training diagnostics only, never used for early stopping/checkpoint/model selection",
        "trace": history, "versions": versions()}
    return booster, metadata


def predict_raw(frame, features, booster, calibration):
    return r9.predict_raw(frame, features, booster, calibration)


def prediction(frame, features, booster, calibration):
    return r9.prediction(frame, features, booster, calibration)


def synthetic_tests() -> dict:
    """Mathematical, pool, initialization and real save/reload tests; no history."""
    checks, detail = {}, {}

    def checked(name, condition):
        if not condition:
            raise AssertionError(name)
        checks[name] = True

    def rejected(name, operation):
        try:
            operation()
        except ValueError:
            checks[name] = True
        else:
            raise AssertionError(f"Expected rejection: {name}")

    rng = np.random.default_rng(SEED)
    worst_swap = 0.
    for size in (2, 5, 17, 61, 199):
        s = rng.integers(0, 7, size).astype(float)
        y = rng.integers(0, 9, size).astype(float)
        item = full_pair_normalizer(s, y)
        p, q = item["p"], item["q"]
        left, right = np.triu_indices(size, 1)
        expected = np.abs((p[left]-p[right])*(q[left]-q[right])).sum()
        np.testing.assert_equal(item["absolute_product_sum"], expected)
        np.testing.assert_array_equal(p, rankdata(s, method="average"))
        if item["C"] > 0 and size <= 17:
            original = spearmanr(s, y).statistic
            for i, j in zip(left, right):
                change = s.copy()
                change[i], change[j] = change[j], change[i]
                expected_swap = (p[j]-p[i])*(q[i]-q[j])/item["C"]
                worst_swap = max(worst_swap, abs((spearmanr(change, y).statistic-original)-expected_swap))
    checked("fenwick_matches_all_pairs_and_average_ties", True)
    checked("average_rank_swap_identity", worst_swap < 1e-12)
    detail["maximum_swap_error"] = float(worst_swap)

    s, y = np.array([.1, .1, .3, .8, .9]), np.array([2., 1., 1., 4., 3.])
    item = full_pair_normalizer(s, y)
    p, q, total = item["p"], item["q"], item["absolute_product_sum"]
    left, right = np.triu_indices(len(s), 1)
    mass = 7.5
    g, h, loss, _ = frozen_pair_terms(s, p, q, left, right, total, mass)
    step, finite_g, finite_h = 1e-5, np.zeros(len(s)), np.zeros((len(s), len(s)))
    for i in range(len(s)):
        up, down = s.copy(), s.copy()
        up[i] += step
        down[i] -= step
        gu, _, lu, _ = frozen_pair_terms(up, p, q, left, right, total, mass)
        gd, _, ld, _ = frozen_pair_terms(down, p, q, left, right, total, mass)
        finite_g[i], finite_h[:, i] = (lu-ld)/(2*step), (gu-gd)/(2*step)
    np.testing.assert_allclose(g, finite_g, rtol=0, atol=1e-9)
    np.testing.assert_allclose(h, 2*np.diag(finite_h), rtol=0, atol=1e-9)
    checked("frozen_gradient_and_twice_diagonal_finite_difference", True)
    checked("twice_diagonal_majorizes_full_hessian", np.linalg.eigvalsh(np.diag(h)-finite_h).min() >= -1e-9)
    checked("zero_sum_gradient_and_descent_direction", abs(g.sum()) < 1e-12 and frozen_pair_terms(s-.01*g, p, q, left, right, total, mass)[2] < loss)
    expected_g, expected_h = np.zeros(len(s)), np.zeros(len(s))
    for i in range(len(left)):
        gi, hi, _, _ = frozen_pair_terms(s, p, q, left[i:i+1], right[i:i+1], total, mass, len(left))
        expected_g += gi/len(left)
        expected_h += hi/len(left)
    np.testing.assert_allclose(expected_g, g, rtol=0, atol=1e-12)
    np.testing.assert_allclose(expected_h, h, rtol=0, atol=1e-12)
    checked("enumerated_sampling_gradient_and_majorizer_expectation", True)
    tally = np.zeros((len(s), len(s)), dtype=int)
    for i in range(len(s)):
        for slot in range(len(s)-1):
            j = slot + int(slot >= i)
            tally[min(i, j), max(i, j)] += 1
    checked("uniform_unordered_pair_probability", np.all(tally[left, right] == 2))
    a, b = sample_pairs(61, 0, 20200102)
    aa, bb = sample_pairs(61, 0, 20200102)
    checked("deterministic_8n_sampling_without_self_pairs", len(a) == 488 and np.array_equal(a, aa) and np.array_equal(b, bb) and np.all(a < b))
    checked("iteration_and_date_seeds_differ", not np.array_equal(a, sample_pairs(61, 1, 20200102)[0]) and not np.array_equal(a, sample_pairs(61, 0, 20200103)[0]))
    constant = full_pair_normalizer(np.zeros(5), y)
    checked("constant_start_not_broken_by_stock_order", constant["C"] == 0 and constant["sum_a"] == 0)

    names = [f"f{i:02}" for i in range(63)]
    tiny = pl.DataFrame({"trade_date": np.repeat([20200102, 20200103, 20200106, 20200107], 4),
        "ts_code": list("abcd")*4, "price_valid": [True]*3+[False]+[True]*12,
        "pred_raw": [1., 1., 3., np.nan, 1., 2., 3., 4., 1., 1., 1., 1., 1., 2., 3., 4.],
        "y_ret_1d": [1., 2., 3., 999., 1., 2., np.nan, np.nan, 1., 2., 3., 4., 1., 1., 1., 1.],
        "flag_limit_up": [0, 1, 0, 0]*4, "aux_raw": [1., 2., 3., 4.]*4})
    prep = prepare(tiny, np.zeros((len(tiny), 63)), names)
    checked("common_whole_date_filter_no_minimum_beyond_two", prep["metadata"]["retained_training_rows"] == 5 and prep["metadata"]["retained_training_dates"] == 2 and len(prep["metadata"]["excluded_degenerate_dates"]) == 2)
    np.testing.assert_array_equal(prep["b"][:8], [.5, .5, 1., np.nan, .25, .5, .75, 1.])
    np.testing.assert_array_equal(prep["target"], [1/3, 2/3, 1., .5, 1.])
    checked("base_full_pool_target_label_pool_and_limitup_included", True)
    np.testing.assert_allclose([prep["weights"][:3].sum(), prep["weights"][3:].sum(), prep["weights"].mean()], [2.5, 2.5, 1.], rtol=0, atol=1e-14)
    checked("unequal_groups_equal_day_mass_and_mean1_weights", True)
    design = np.column_stack([np.ones(len(prep["target"])), prep["b"][prep["mask"]]])
    wls = np.linalg.solve(design.T@(prep["weights"][:, None]*design), design.T@(prep["weights"]*prep["target"]))
    np.testing.assert_allclose(wls, [prep["calibration"]["intercept"], prep["calibration"]["slope"]], rtol=0, atol=1e-12)
    checked("WLS_on_common_slice_equals_normal_equations", True)
    mse, mse_history = make_objective(prep, "mse")
    increment = np.linspace(-.1, .1, len(prep["target"]))
    mg, mh = mse(increment, object())
    np.testing.assert_array_equal(mg, prep["weights"]*(increment+prep["anchor"]-prep["target"]))
    np.testing.assert_array_equal(mh, prep["weights"])
    checked("MSE_uses_closed_Float64_arrays_and_single_weights", mg.dtype == np.float64 and mh.dtype == np.float64)
    rank_objective, runtime_history = make_objective(prep, "rankic")
    cancel = np.zeros(len(prep["anchor"]))
    cancel[:3] = -prep["anchor"][:3]
    rg, rh = rank_objective(cancel, None)
    checked("runtime_constant_date_zero_without_renormalizing_N_D", np.all(rg[:3] == 0) and np.all(rh[:3] == 0) and runtime_history[-1]["degenerate_dates"] == [20200102])
    q2 = full_pair_normalizer(prep["anchor"][3:], prep["target"][3:])
    eleft, eright = sample_pairs(2, 0, 20200103)
    eg, eh, _, _ = frozen_pair_terms(prep["anchor"][3:], q2["p"], q2["q"], eleft, eright, q2["absolute_product_sum"], 2.5, 1/len(eleft))
    np.testing.assert_array_equal(rg[3:], eg)
    np.testing.assert_array_equal(rh[3:], eh)
    rejected("all_runtime_dates_degenerate_fail_closed", lambda: make_objective(prep, "rankic")[0](-prep["anchor"], None))
    rejected("constant_initial_groups_fail_closed", lambda: prepare(tiny.with_columns(pl.lit(1.).alias("pred_raw")), np.zeros((len(tiny), 63)), names))
    rejected("Float32_source_targets_rejected", lambda: prepare(tiny.with_columns(pl.col("y_ret_1d").cast(pl.Float32)), np.zeros((len(tiny), 63)), names))
    rejected("nonpositive_WLS_no_anchor_fallback", lambda: prepare(tiny.with_columns((-pl.col("pred_raw")).alias("y_ret_1d")), np.zeros((len(tiny), 63)), names))
    missing_groups = pl.concat([tiny, tiny.head(4).with_columns(
        pl.lit(20200108, dtype=pl.Int64).alias("trade_date"), pl.lit(float("nan")).alias("y_ret_1d")),
        tiny.head(4).with_columns(pl.lit(20200109, dtype=pl.Int64).alias("trade_date"),
            pl.when(pl.col("ts_code") == "a").then(1.).otherwise(float("nan")).alias("y_ret_1d"))])
    missing_prep = prepare(missing_groups, np.zeros((len(missing_groups), 63)), names)
    np.testing.assert_array_equal(missing_prep["target"], prep["target"])
    np.testing.assert_array_equal(missing_prep["weights"], prep["weights"])
    checked("zero_and_singleton_target_dates_excluded_without_dilution", [row["finite_target_rows"] for row in missing_prep["metadata"]["excluded_degenerate_dates"][-2:]] == [0, 1])

    stocks, days = 2200, 3
    stock, day = np.tile(np.arange(stocks), days), np.repeat(np.arange(days), stocks)
    features = rng.normal(size=(stocks*days, 63)).astype(np.float32)
    features[:, 0] = (stock % 2)*2-1
    raw = ((stock*17+day*31) % stocks).astype(float)
    labels = raw/stocks + .35*features[:, 0]
    labels[(day == 0) & (stock % 7 == 0)] = np.nan
    valid = ~((day == 1) & (stock < 5))
    frame = pl.DataFrame({"trade_date": 20200203+day, "ts_code": [f"S{i:04}" for i in stock],
        "price_valid": valid, "pred_raw": raw, "y_ret_1d": labels,
        "flag_limit_up": (stock % 17 == 0).astype(int), "aux_raw": np.sin(stock/17),
        "future_available": day < 2})
    prepared = prepare(frame, features, names)
    calibration = prepared["calibration"]
    clean = frame.select(r9.KEYS+["price_valid", "flag_limit_up", "pred_raw"]).with_columns(pl.lit(None, dtype=pl.Float64).alias("y_ret_1d"))
    original = r9.make_prediction(r9.Panel.from_frame(clean), frame["aux_raw"].to_numpy(), "top_only", .25)
    zero = prediction(frame, features, None, calibration)
    np.testing.assert_array_equal(zero, original)
    checked("actual_affine_zero_exact_R4_post_no_raw_bypass", True)
    for kind in ("mse", "rankic"):
        booster, metadata = fit(prepared, kind)
        raw_prediction = predict_raw(frame, features, booster, calibration)
        post = prediction(frame, features, booster, calibration)
        checked(f"{kind}_real_fixed_budget_fit_from_zero", metadata["objective_calls"] == ROUNDS and booster.num_feature() == 64 and metadata["params"]["boost_from_average"] is False and metadata["initial_increment_verified"])
        corrected_selected = raw_prediction[prepared["mask"]]
        np.testing.assert_array_equal(corrected_selected, prepared["anchor"] + booster.predict(prepared["matrix"], num_threads=8))
        checked(f"{kind}_model_output_increment_only", np.max(np.abs(corrected_selected-prepared["anchor"])) > 0)
        poisoned = frame.with_columns(pl.lit(float("nan")).alias("y_ret_1d"), (~pl.col("future_available")).alias("future_available"))
        np.testing.assert_array_equal(prediction(poisoned, features, booster, calibration), post)
        np.testing.assert_array_equal(prediction(frame.drop("y_ret_1d", "future_available"), features, booster, calibration), post)
        checked(f"{kind}_inference_labels_and_future_availability_ignored", True)
        cut = 2*stocks
        np.testing.assert_array_equal(prediction(frame.head(cut), features[:cut], booster, calibration), post[:cut])
        changed_features = features.copy()
        changed_features[cut:] *= -99
        future = frame.with_columns(pl.when(pl.col("trade_date") > 20200204).then(-pl.col("pred_raw")).otherwise(pl.col("pred_raw")).alias("pred_raw"))
        np.testing.assert_array_equal(prediction(future, changed_features, booster, calibration)[:cut], post[:cut])
        checked(f"{kind}_prefix_and_future_feature_poison", True)
        checked(f"{kind}_invalid_sentinels", np.all(raw_prediction[~valid] == -10) and np.all(post[~valid] < -1))
        with tempfile.TemporaryDirectory(prefix="r10-synthetic-") as temporary:
            path = Path(temporary)/"model.txt"
            booster.save_model(str(path))
            reloaded = lgb.Booster(model_str=path.read_text(encoding="utf-8"))
            saved_calibration = json.loads(json.dumps(calibration, allow_nan=False))
            np.testing.assert_array_equal(predict_raw(frame, features, reloaded, saved_calibration), raw_prediction)
            np.testing.assert_array_equal(prediction(frame, features, reloaded, saved_calibration), post)
        checked(f"{kind}_model_and_calibration_save_reload_exact", True)
        detail[kind] = {"objective_calls": metadata["objective_calls"], "actual_trees": metadata["actual_trees"],
                        "total_objective_seconds": float(sum(row["seconds"] for row in metadata["trace"]))}
    # Warm synthetic objective timing only: no actual 4650-stock data are read.
    fake_scores = rng.normal(size=4650)
    fake_targets = rng.integers(0, 300, size=4650).astype(float)
    started = time.perf_counter()
    for _ in range(5):
        full_pair_normalizer(fake_scores, fake_targets)
    detail["4650_row_normalizer_mean_seconds"] = (time.perf_counter()-started)/5
    detail["synthetic_selected_rows"] = len(prepared["target"])
    return {"status": "passed", "checks": checks, "check_count": len(checks), "details": detail,
            "params": dict(PARAMS), "rounds": ROUNDS, "pairs_per_row": PAIRS_PER_ROW,
            "versions": versions(), "historical_io_training_scoring": False,
            "limitations": "Synthetic math/engineering checks only; no evidence of historical performance"}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--test", required=True, action="store_true")
    parser.parse_args()
    print(json.dumps(synthetic_tests(), ensure_ascii=False, indent=2, allow_nan=False))
