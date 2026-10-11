"""One fixed five-market-day value calibration mechanism; never a release builder.

Only r4 fold-local OOF predictions from 2020/2021 fit the calibrators. 2022 is
the mechanism screen. Frozen coefficients may see 2023/2024 only if that screen
passes. All years were previously viewed; none is an independent holdout.
"""
from __future__ import annotations

import os
for _key in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "POLARS_MAX_THREADS"):
    os.environ[_key] = "4"
import argparse
import gc
import hashlib
import json
from pathlib import Path
import sys
import time

import numpy as np
import polars as pl
from scipy.stats import rankdata

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "experiments/r6_value5_20260926"
R4 = ROOT / "experiments/revalidation_20260926/validation"
R4_MANIFEST = ROOT / "releases/ensemble4_r4/release_manifest.json"
R4_MANIFEST_SHA256 = "ecfbe0dd84e04115f7c1736813ba05ded840c6982ed66c791b483d4bded8a4cf"
KEYS = ["ts_code", "trade_date"]
FEATURES = ["raw_rank", "ema09", "raw_rank_squared", "ema09_squared", "raw_x_ema",
            "prior_r4_top", "prior_top_age_log60", "raw_rank_change1", "raw_rank_mean5"]
MODELS = {"candidate": list(range(9)), "joint_rank_ema": list(range(5)),
          "raw_only": [0, 2], "ema_only": [1, 3]}
HORIZON, RIDGE_LAMBDA, SENTINEL = 5, .01, -1e6
GATES = {"relative_daily_mse_improvement_min": .001, "rank_ic5_delta_min": .002,
         "top5_return_delta_min": .0001, "bootstrap_positive_share_min": .8,
         "confirmation_each_year": {"relative_daily_mse_improvement_min": 0.,
             "rank_ic5_delta_min": 0., "top5_return_delta_min": 0.}}


def sha(path):
    h = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for block in iter(lambda: stream.read(8 * 1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def read(path):
    return json.loads(Path(path).read_text(encoding="utf-8-sig"))


def write_new(path, obj):
    with Path(path).open("x", encoding="utf-8") as stream:
        json.dump(obj, stream, ensure_ascii=False, indent=2, allow_nan=False)


def log(message):
    print(f"[{time.strftime('%H:%M:%S')}] {message}", flush=True)


def cache_path(year):
    return R4 / f"predictions_ensemble4_{year}.parquet"


def panel_arrays(frame):
    ordered = frame.sort("trade_date", "ts_code")
    if not ordered.select(KEYS).equals(frame.select(KEYS)):
        raise ValueError("Expected date/code-sorted rows")
    if frame.select(KEYS).n_unique() != len(frame):
        raise ValueError("Duplicate prediction keys")
    dates = frame["trade_date"].unique(maintain_order=True).to_numpy()
    codes = frame["ts_code"].to_numpy()
    n = len(frame) // len(dates)
    if n * len(dates) != len(frame) or not np.all(codes.reshape(-1, n) == codes[:n]):
        raise ValueError("Full market-date rectangular panel required")
    return dates, n


def load_year(year):
    frame = pl.read_parquet(cache_path(year)).sort("trade_date", "ts_code")
    if frame["y_ret_1d"].dtype != pl.Float64:
        raise TypeError("Five-day labels require original Float64 returns")
    if not np.all(frame["trade_date"].to_numpy() // 10000 == year):
        raise ValueError("Unexpected fold date")
    panel_arrays(frame)
    return frame


def make_features(frame):
    """Current/past predictions only; reset state at each annual OOF boundary.

    The prior Top is the previous date's r4 cached final score Top among all
    flag_limit_up==0 rows, with no return/label-availability condition. Its K
    uses that entire current flag-only pool. Invalid prices get low scores.
    """
    dates, n = panel_arrays(frame)
    shape = (len(dates), n)
    raw = frame["pred_raw"].to_numpy().reshape(shape)
    valid = frame["price_valid"].to_numpy().reshape(shape) & np.isfinite(raw)
    final = frame["pred"].to_numpy().reshape(shape)
    up = frame["flag_limit_up"].to_numpy().reshape(shape)
    ranks = np.full(shape, .5)
    ema = np.full(shape, .5)
    change = np.zeros(shape)
    average5 = np.full(shape, .5)
    prior = np.zeros(shape, dtype=bool)
    ages = np.zeros(shape, dtype=np.int32)
    top = np.zeros(n, dtype=bool)
    age = np.zeros(n, dtype=np.int32)
    for day in range(len(dates)):
        keep = valid[day]
        if keep.any():
            ranks[day, keep] = rankdata(raw[day, keep], method="average") / keep.sum()
        ema[day] = ranks[day]
        if day:
            continuing = keep & valid[day - 1]
            ema[day, continuing] = .1 * ranks[day, continuing] + .9 * ema[day - 1, continuing]
            change[day, continuing] = ranks[day, continuing] - ranks[day - 1, continuing]
        average5[day] = ranks[day]
        if day >= 4:
            complete = valid[day - 4:day + 1].all(axis=0)
            average5[day, complete] = ranks[day - 4:day + 1, complete].mean(axis=0)
        prior[day], ages[day] = top & keep, np.where(keep, age, 0)
        indices = np.flatnonzero(up[day] == 0)
        top = np.zeros(n, dtype=bool)
        if len(indices) >= 100:
            scores = np.where(keep, final[day], SENTINEL)
            chosen = indices[np.argsort(-scores[indices], kind="stable")[:max(len(indices) // 10, 1)]]
            top[chosen] = keep[chosen]
        age = np.where(top, age + 1, 0)
    x = np.column_stack([ranks.ravel(), ema.ravel(), (ranks * ranks).ravel(),
        (ema * ema).ravel(), (ranks * ema).ravel(), prior.ravel().astype(float),
        np.log1p(np.minimum(ages, 60)).ravel() / np.log(61), change.ravel(), average5.ravel()])
    assert np.isfinite(x).all()
    return x, {"prior_top": prior.ravel(), "prior_top_age": ages.ravel(), "valid": valid.ravel()}


def forward_targets(dates, returns):
    """Y5[t] sums excess y1[t:t+5]; last realization occurs at market date t+5.

    The excess benchmark uses all finite official labels on that signal date,
    including limit-up stocks. It is a research target, not the official Top
    benchmark. Missing labels never become zero and never compress the calendar.
    """
    y = np.asarray(returns, dtype=np.float64)
    assert y.ndim == 2 and len(dates) == len(y)
    finite = np.isfinite(y)
    counts = finite.sum(axis=1)
    market = np.divide(np.where(finite, y, 0.).sum(axis=1), counts,
                       out=np.full(len(y), np.nan), where=counts > 0)
    excess = y - market[:, None]
    target = np.full_like(y, np.nan)
    available = np.full(len(y), -1, dtype=np.int64)
    for day in range(max(0, len(dates) - HORIZON)):
        window = excess[day:day + HORIZON]
        complete = np.isfinite(window).all(axis=0)
        target[day, complete] = window[:, complete].sum(axis=0)
        available[day] = dates[day + HORIZON]
    return target, excess, available


def balanced_weights(dates):
    _, indices, counts = np.unique(dates, return_inverse=True, return_counts=True)
    return 1. / (len(counts) * counts[indices])


def fit_ridge(x, y, dates, columns):
    a = x[:, columns]
    w = balanced_weights(dates)
    center = np.sum(w[:, None] * a, axis=0)
    scale = np.sqrt(np.sum(w[:, None] * (a - center) ** 2, axis=0))
    scale = np.where(scale > 0, scale, 1.)
    z = (a - center) / scale
    intercept = float(w @ y)
    beta = np.linalg.solve(z.T @ (w[:, None] * z) + RIDGE_LAMBDA * np.eye(len(columns)),
                           z.T @ (w * (y - intercept)))
    return {"columns": columns, "center": center.tolist(), "scale": scale.tolist(),
            "coefficients": beta.tolist(), "intercept": intercept,
            "weighted_target_mean": intercept, "training_rows": len(y),
            "training_dates": int(len(np.unique(dates))), "weight_sum": float(w.sum())}


def predict(model, x, valid):
    z = (x[:, model["columns"]] - model["center"]) / model["scale"]
    value = z @ np.asarray(model["coefficients"]) + model["intercept"]
    return np.where(valid, value, SENTINEL)


def corr(x, y):
    if len(x) < 30:
        return np.nan
    a, b = rankdata(x, method="average"), rankdata(y, method="average")
    a, b = a - a.mean(), b - b.mean()
    denom = np.sqrt((a @ a) * (b @ b))
    return float(a @ b / denom) if denom > 0 else np.nan


def daily_metrics(frame, x, states, predictions, target, excess, available):
    dates, n = panel_arrays(frame)
    valid = states["valid"].reshape(-1, n)
    up = frame["flag_limit_up"].to_numpy().reshape(-1, n)
    signals = {**predictions, "raw_rank": np.where(states["valid"], x[:, 0], SENTINEL),
               "ema09": np.where(states["valid"], x[:, 1], SENTINEL)}
    signals = {k: v.reshape(-1, n) for k, v in signals.items()}
    rows = []
    for day, date in enumerate(dates):
        if available[day] < 0:
            continue
        target_valid = valid[day] & np.isfinite(target[day])
        one_valid = valid[day] & np.isfinite(excess[day])
        if target_valid.sum() < 100:
            raise ValueError("Too few complete five-day labels; do not silently drop a date")
        pool = np.flatnonzero(up[day] == 0)
        if len(pool) < 100:
            raise ValueError("Too few current flag-eligible stocks")
        k = max(len(pool) // 10, 1)
        for name, values in signals.items():
            selected = pool[np.argsort(-values[day, pool], kind="stable")[:k]]
            observed = selected[np.isfinite(target[day, selected])]
            if not len(observed):
                raise ValueError("Predetermined Top has no observed target")
            row = {"trade_date": int(date), "signal": name,
                "target_rows": int(target_valid.sum()),
                "rank_ic5": corr(values[day, target_valid], target[day, target_valid]),
                "rank_ic1": corr(values[day, one_valid], excess[day, one_valid]),
                "mse5": float(np.mean((values[day, target_valid] - target[day, target_valid]) ** 2)) if name in MODELS else None,
                "top5_excess_sum_mean": float(target[day, observed].mean()),
                "top_selected": k, "top_target_observed": len(observed),
                "top_target_coverage": len(observed) / k,
                "top_invalid_price_selected": int((~valid[day, selected]).sum())}
            rows.append(row)
    return pl.DataFrame(rows)


def summarize_daily(daily):
    result = {}
    for name in daily["signal"].unique(maintain_order=True):
        d = daily.filter(pl.col("signal") == name)
        result[name] = {"days": len(d)}
        for key in ("rank_ic5", "rank_ic1", "mse5", "top5_excess_sum_mean", "top_target_coverage"):
            values = d[key].to_numpy()
            result[name][key] = float(np.nanmean(values)) if np.isfinite(values).any() else None
        result[name]["min_top_target_coverage"] = float(d["top_target_coverage"].min())
        result[name]["max_top_invalid_price_selected"] = int(d["top_invalid_price_selected"].max())
    return result


def bootstrap_mse(dailies):
    rng = np.random.default_rng(2026)
    samples = np.zeros(5000)
    actual = []
    for daily in dailies:
        a = daily.filter(pl.col("signal") == "candidate").sort("trade_date")
        b = daily.filter(pl.col("signal") == "joint_rank_ema").sort("trade_date")
        assert a["trade_date"].equals(b["trade_date"])
        delta = b["mse5"].to_numpy() - a["mse5"].to_numpy()
        assert np.isfinite(delta).all() and len(delta) >= 20
        actual.append(float(delta.mean()))
        starts = rng.integers(0, len(delta) - 20 + 1, size=(5000, (len(delta) + 19) // 20))
        indices = (starts[:, :, None] + np.arange(20)).reshape(5000, -1)[:, :len(delta)]
        samples += delta[indices].mean(axis=1) / len(dailies)
    return {"seed": 2026, "block_days": 20, "draws": 5000,
        "method": "Within-year noncircular moving blocks; equally weighted annual means",
        "mean_daily_mse_reduction": float(np.mean(actual)),
        "positive_share": float(np.mean(samples > 0)),
        "ci95": np.quantile(samples, [.025, .975]).tolist(),
        "selection_bias_corrected": False}


def comparison(metrics):
    a, b = metrics["candidate"], metrics["joint_rank_ema"]
    return {"relative_daily_mse_improvement": (b["mse5"] - a["mse5"]) / b["mse5"],
            "rank_ic5_delta": a["rank_ic5"] - b["rank_ic5"],
            "top5_return_delta": a["top5_excess_sum_mean"] - b["top5_excess_sum_mean"]}


def gate(metrics_list, bootstrap, confirmation=False):
    aggregate = {name: {key: float(np.mean([m[name][key] for m in metrics_list]))
                            for key in ("mse5", "rank_ic5", "top5_excess_sum_mean")}
                 for name in ("candidate", "joint_rank_ema")}
    cmp = comparison(aggregate)
    tests = {key: cmp[key] >= GATES[key + "_min"] for key in cmp}
    tests["bootstrap"] = bootstrap["positive_share"] >= GATES["bootstrap_positive_share_min"]
    yearly = [comparison(m) for m in metrics_list]
    if confirmation:
        tests["every_year_mse_ic_top_non_decreasing"] = all(
            c[key] >= threshold for c in yearly
            for key, threshold in [(k.removesuffix("_min"), v) for k, v in GATES["confirmation_each_year"].items()])
    return {"reference": "joint_rank_ema only; raw/EMA single heads never selected", "comparison": cmp,
            "annual_comparisons": yearly, "conditions": tests, "passed": all(tests.values())}


def group_metrics(frame, states, predicted, target, edges):
    y = target.ravel()
    valid = states["valid"]
    observed = valid & np.isfinite(y)
    bins = np.searchsorted(edges, predicted, side="right")
    ages = states["prior_top_age"]
    groups = [(f"training_prediction_bin_{i + 1}", bins == i) for i in range(10)]
    groups += [("prior_r4_top", states["prior_top"]), ("not_prior_r4_top", ~states["prior_top"]),
               ("age_1_5", (ages >= 1) & (ages <= 5)), ("age_6_20", (ages >= 6) & (ages <= 20)),
               ("age_21_60", (ages >= 21) & (ages <= 60)), ("age_above60", ages > 60)]
    rows = []
    for name, mask in groups:
        members, keep = mask & valid, mask & observed
        rows.append({"group": name, "prediction_rows": int(members.sum()), "complete_target_rows": int(keep.sum()),
            "target_coverage": float(keep.sum() / members.sum()) if members.any() else None,
            "mean_prediction": float(predicted[keep].mean()) if keep.any() else None,
            "mean_y5": float(y[keep].mean()) if keep.any() else None,
            "mse5": float(np.mean((predicted[keep] - y[keep]) ** 2)) if keep.any() else None,
            "weighting": "row-weighted within fixed group; descriptive, not gate"})
    return pl.DataFrame(rows)


def synthetic_tests():
    dates = np.arange(100, 114)
    returns = np.tile(np.array([-.02, -.01, .01, .02]), (len(dates), 1))
    y, one, end = forward_targets(dates, returns)
    np.testing.assert_allclose(y[0], [-.1, -.05, .05, .1])
    assert end[0] == 105 and (end[-5:] == -1).all() and np.isnan(y[-5:]).all()
    missing = returns.copy(); missing[3, 2] = np.nan
    bad, _, _ = forward_targets(dates, missing)
    assert np.isnan(bad[:4, 2]).all() and np.isfinite(bad[4, 2])
    cutoff = 109
    poison = returns.copy(); poison[dates >= cutoff] = 1e4
    altered, _, _ = forward_targets(dates, poison)
    safe = (end > 0) & (end < cutoff)
    assert np.array_equal(y[safe], altered[safe], equal_nan=True)
    assert dates[safe].max() + 5 < cutoff
    day_count, stocks = 70, 120
    rng = np.random.default_rng(2026)
    price = np.ones((day_count, stocks), bool); price[10:12, 2] = False
    frame = pl.DataFrame({"ts_code": [f"S{i:03d}" for _ in range(day_count) for i in range(stocks)],
        "trade_date": np.repeat(np.arange(day_count), stocks), "price_valid": price.ravel(),
        "flag_limit_up": np.zeros(day_count * stocks, dtype=np.int8),
        "pred_raw": rng.normal(size=day_count * stocks), "pred": rng.normal(size=day_count * stocks),
        "y_ret_1d": rng.normal(size=day_count * stocks)})
    x, state = make_features(frame)
    altered_x, _ = make_features(frame.with_columns(pl.lit(float("nan")).alias("y_ret_1d")))
    assert np.array_equal(x, altered_x)
    prefix, _ = make_features(frame.head(50 * stocks))
    assert np.array_equal(prefix, x[:50 * stocks])
    changed = frame.with_columns(pl.when(pl.col("trade_date") >= 50).then(pl.lit(1e8)).otherwise(pl.col("pred_raw")).alias("pred_raw"),
                                 pl.when(pl.col("trade_date") >= 50).then(pl.lit(-1e8)).otherwise(pl.col("pred")).alias("pred"))
    future_x, _ = make_features(changed)
    assert np.array_equal(future_x[:50 * stocks], prefix)
    assert not state["prior_top"][:stocks].any() and np.all(state["prior_top_age"][:stocks] == 0)
    assert np.all(x[10 * stocks + 2] == [0.5, .5, .25, .25, .25, 0, 0, 0, .5])
    # Fitting uses balanced dates and deterministic training-only normalization.
    sample = rng.normal(size=(80, 9)); labels = .1 * sample[:, 0] + .2 * sample[:, 7]
    sample_dates = np.repeat([1, 2], [20, 60])
    weights = balanced_weights(sample_dates)
    np.testing.assert_allclose([weights[:20].sum(), weights[20:].sum()], [.5, .5])
    model = fit_ridge(sample, labels, sample_dates, MODELS["candidate"])
    reordered = rng.permutation(len(sample))
    other = fit_ridge(sample[reordered], labels[reordered], sample_dates[reordered], MODELS["candidate"])
    np.testing.assert_allclose(model["coefficients"], other["coefficients"], rtol=0, atol=1e-14)
    assert (predict(model, sample, np.zeros(len(sample), bool)) == SENTINEL).all()
    # A missing future target removes one observation, never replaces its Top member.
    fake_target = rng.normal(size=(day_count, stocks))
    fake_target[0, stocks - 1] = np.nan
    fake_values = {name: np.tile(np.arange(stocks, dtype=float), day_count) for name in MODELS}
    fake_end = np.arange(day_count) + 5
    measured = daily_metrics(frame, x, state, fake_values, fake_target,
                             np.nan_to_num(fake_target), fake_end)
    first = measured.filter((pl.col("trade_date") == 0) & (pl.col("signal") == "candidate")).row(0, named=True)
    assert first["top_selected"] == 12 and first["top_target_observed"] == 11
    assert abs(first["top5_excess_sum_mean"] - np.mean(fake_target[0, 108:119])) < 1e-12
    b = {"mse5": 1., "rank_ic5": .1, "top5_excess_sum_mean": .01}
    good = {"candidate": {"mse5": .9, "rank_ic5": .12, "top5_excess_sum_mean": .02}, "joint_rank_ema": b}
    bad_year = {"candidate": {"mse5": .99, "rank_ic5": .099, "top5_excess_sum_mean": .011}, "joint_rank_ema": b}
    assert gate([good], {"positive_share": 1.})["passed"]
    assert not gate([good, bad_year], {"positive_share": 1.}, confirmation=True)["passed"]
    return {"status": "passed", "five_market_dates_exact": True, "missing_not_zero_or_compressed": True,
        "purge_five_label_realization_strictly_before_cutoff": True, "future_labels_cannot_change_safe_target": True,
        "feature_label_invariance": True, "feature_prefix_and_future_prediction_invariance": True,
        "annual_state_cold_start": True, "invalid_feature_reset_and_prediction_low": True,
        "equal_total_weight_per_training_date": True, "ridge_row_permutation_invariance": True,
        "missing_future_top_label_does_not_backfill": True, "each_confirmation_metric_non_decreasing_required": True,
        "market_scores_computed": False}


def freeze():
    OUT.mkdir(parents=True, exist_ok=True)
    if (OUT / "protocol.json").exists():
        raise FileExistsError("Protocol already frozen")
    assert sha(R4_MANIFEST) == R4_MANIFEST_SHA256
    manifest = read(R4_MANIFEST)
    tests = synthetic_tests()
    write_new(OUT / "tests.json", tests)
    paths = [Path(__file__), R4_MANIFEST, R4 / "protocol.json", R4 / "summary.json",
             ROOT / "active_release.json", ROOT / "data" / "raw" / "训练集.csv", OUT / "tests.json",
             ROOT / "experiments/research_r6_20260926/后续优化研究.md"]
    for year in range(2020, 2025):
        p = cache_path(year)
        assert sha(p) == manifest["artifact_sha256"][p.relative_to(ROOT).as_posix()]
        paths += [p, R4 / f"result_{year}.json"]
    protocol = {"experiment": "one_fixed_five_day_oof_value_calibration", "frozen_at_local": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "all_years_previously_viewed": True, "training_years": [2020, 2021], "development_year": 2022,
        "confirmation_years": [2023, 2024], "confirmation_only_after_development_pass": True,
        "refit_after_development": False, "same_2020_2021_coefficients_through_confirmation": True,
        "horizon": HORIZON, "target": "Sum k=0..4 of original Float64 y_ret_1d[t+k] minus each signal date's mean of ALL finite labels, including limit-up rows. All five labels required. Realization date is calendar[t+5]. Last five dates of each evaluation year are excluded; training years form one continuous target calendar.",
        "target_is_official_score": False, "target_is_tradeable_return": False,
        "training_boundary": "All target realization dates strictly before 2022 first prediction; 2020/2021 target may cross their internal boundary; the final five 2021 signal dates are purged.",
        "state_boundary": "Feature EMA/prior-Top/age/history reset independently at each annual OOF model boundary, including 2020 to 2021. Evaluation years likewise cold-start; target continuity and feature-state reset are separate.",
        "features": FEATURES, "models": MODELS, "only_candidate": "candidate",
        "only_gate_reference": "joint_rank_ema", "single_heads_explanation_only": True,
        "ridge": {"lambda": RIDGE_LAMBDA, "objective": "sum(w_i*(y_i-intercept-z_i beta)^2)+lambda*||beta||^2; each training date has identical total w, total w=1", "normalization": "same training-date-balanced weights; train-only feature mean/std, zero std replaced by1; unpenalized intercept; no target clipping"},
        "postprocessing_modified": False, "gates": GATES,
        "gate_logic": "Development: all three aggregate thresholds and bootstrap positive share pass against joint only. Confirmation: each year's MSE improvement, IC5 delta and Top5 delta must all be >=0; equally weighted annual aggregate must also pass the same development thresholds and bootstrap. No alternative winner or retuning.",
        "bootstrap": {"block_days": 20, "draws": 5000, "seed": 2026, "method": "noncircular moving blocks within each year; equal annual weight"},
        "top_measurement": "Select floor(nonlimit_count/10) by t-date predictions with stable code tie order; price-invalid prediction=-1e6; no Y5 mask in membership. Then report observed labels/coverage without backfill. Not an executable portfolio or official score.",
        "metrics": "MSE/IC/Top mean equally weighted per date. Fixed training prediction bins and age/previous-membership groups are descriptive row-weighted summaries. Overlapping Y5 uses block20 uncertainty; selection bias uncorrected.",
        "stop": "A failed mechanism screen stops without confirmation, postprocessor, production prediction or model replacement.",
        "versions": {"python": sys.version, "numpy": np.__version__, "polars": pl.__version__},
        "input_sha256": {p.relative_to(ROOT).as_posix(): sha(p) for p in paths}}
    write_new(OUT / "protocol.json", protocol)
    log("Frozen one target, one candidate, all source/input hashes and gates")


def verify():
    protocol = read(OUT / "protocol.json")
    assert protocol["gates"] == GATES and protocol["models"] == MODELS and protocol["features"] == FEATURES
    for path, expected in protocol["input_sha256"].items():
        if sha(ROOT / path) != expected:
            raise AssertionError(f"Frozen input changed: {path}")
    return protocol


def fit_training():
    frames, xs = [], []
    for year in (2020, 2021):
        frame = load_year(year)
        x, _ = make_features(frame)
        frames.append(frame); xs.append(x)
    all_frame = pl.concat(frames)
    x = np.concatenate(xs)
    dates, n = panel_arrays(all_frame)
    target, _, available = forward_targets(dates, all_frame["y_ret_1d"].to_numpy().reshape(-1, n))
    # The known next signal date is an input-key read, not a read of its outcomes.
    first_development = int(pl.read_parquet(cache_path(2022), columns=["trade_date"])["trade_date"].min())
    end = np.repeat(available, n)
    valid = all_frame["price_valid"].to_numpy()
    keep = valid & np.isfinite(target.ravel()) & (end > 0) & (end < first_development)
    assert dates[-5:].tolist() == sorted(dates[-5:].tolist()) and not keep[-5 * n:].any()
    assert int(end[keep].max()) < first_development
    train_x, train_y = x[keep], target.ravel()[keep]
    train_dates = all_frame["trade_date"].to_numpy()[keep]
    models = {name: fit_ridge(train_x, train_y, train_dates, columns) for name, columns in MODELS.items()}
    train_pred = predict(models["candidate"], train_x, np.ones(len(train_x), bool))
    # Fixed train-only bin boundaries; they do not define any gate.
    edges = np.quantile(train_pred, np.arange(.1, 1., .1)).tolist()
    result = {"models": models, "bin_edges": edges, "training_years": [2020, 2021],
        "first_development_date": first_development, "max_training_label_available_date": int(end[keep].max()),
        "max_training_signal_date": int(train_dates.max()), "purged_final_market_dates": dates[-5:].tolist(),
        "full_prediction_rows": len(all_frame), "complete_purged_training_rows": int(keep.sum()),
        "target_mean": float(train_y.mean()), "target_std": float(train_y.std()),
        "target_min": float(train_y.min()), "target_max": float(train_y.max()),
        "weights": "equal total mass for each eligible training date, then uniform within date",
        "protocol_sha256": sha(OUT / "protocol.json")}
    write_new(OUT / "calibrators.json", result)
    del frames, xs, all_frame, x, train_x, train_y, train_pred
    gc.collect()
    return result


def evaluate_year(year, fitted):
    if (OUT / f"result_{year}.json").exists():
        raise FileExistsError("Preserving completed evaluation")
    frame = load_year(year)
    x, state = make_features(frame)
    dates, n = panel_arrays(frame)
    target, excess, available = forward_targets(dates, frame["y_ret_1d"].to_numpy().reshape(-1, n))
    poisoned, _ = make_features(frame.with_columns(pl.lit(-98765.).alias("y_ret_1d")))
    assert np.array_equal(x, poisoned)
    prefix, _ = make_features(frame.head(50 * n))
    assert np.array_equal(x[:50 * n], prefix)
    values = {name: predict(model, x, state["valid"]) for name, model in fitted["models"].items()}
    daily = daily_metrics(frame, x, state, values, target, excess, available)
    metrics = summarize_daily(daily)
    groups = group_metrics(frame, state, values["candidate"], target, fitted["bin_edges"])
    output = frame.select(KEYS + ["price_valid", "flag_limit_up"]).with_columns(
        pl.Series("raw_rank", x[:, 0]), pl.Series("ema09", x[:, 1]),
        pl.Series("prior_r4_top", state["prior_top"]), pl.Series("prior_top_age", state["prior_top_age"]),
        pl.Series("y1_raw_excess", excess.ravel()), pl.Series("y5_raw_excess_sum", target.ravel()),
        pl.Series("label_available_date", np.repeat(available, n)),
        *[pl.Series("value5_" + name, value) for name, value in values.items()])
    output.write_parquet(OUT / f"predictions_{year}.parquet", compression="zstd")
    daily.write_csv(OUT / f"daily_{year}.csv", float_precision=17)
    groups.write_csv(OUT / f"groups_{year}.csv", float_precision=17)
    bootstrap = bootstrap_mse([daily])
    record = {"year": year, "retrospective_previously_viewed": True,
        "calibrators_sha256": sha(OUT / "calibrators.json"), "input_sha256": sha(cache_path(year)),
        "metrics": metrics, "comparison": comparison(metrics), "bootstrap": bootstrap,
        "last_five_signal_dates_excluded": dates[-5:].tolist(),
        "tests": {"label_perturbation_feature_exact": True, "prefix_50_market_dates_exact": True,
                  "all_calibrated_predictions_finite": all(bool(np.isfinite(v).all()) for v in values.values()),
                  "invalid_price_calibrated_scores_low": all(bool((v[~state['valid']] == SENTINEL).all()) for v in values.values())},
        "artifact_sha256": {f"{kind}_{year}.{suffix}": sha(OUT / f"{kind}_{year}.{suffix}")
                            for kind, suffix in [("predictions", "parquet"), ("daily", "csv"), ("groups", "csv")]}}
    write_new(OUT / f"result_{year}.json", record)
    log(f"{year} relative MSE improvement={record['comparison']['relative_daily_mse_improvement']:+.6%}, IC5 delta={record['comparison']['rank_ic5_delta']:+.6f}, Top5 delta={record['comparison']['top5_return_delta']:+.6f}")
    return record, daily


def develop():
    verify()
    if (OUT / "development.json").exists():
        raise FileExistsError("Development result already exists")
    fitted = fit_training()
    result, daily = evaluate_year(2022, fitted)
    selected = gate([result["metrics"]], result["bootstrap"])
    verify()
    write_new(OUT / "development.json", {"protocol_sha256": sha(OUT / "protocol.json"),
        "calibrators_sha256": sha(OUT / "calibrators.json"), "result_sha256": sha(OUT / "result_2022.json"),
        "gate": selected, "confirmation_allowed": selected["passed"]})
    write_summary()
    log(f"Mechanism screen passed={selected['passed']}")


def confirm():
    verify()
    dev = read(OUT / "development.json")
    assert dev["protocol_sha256"] == sha(OUT / "protocol.json")
    assert dev["calibrators_sha256"] == sha(OUT / "calibrators.json")
    assert dev["result_sha256"] == sha(OUT / "result_2022.json")
    original = read(OUT / "result_2022.json")
    assert gate([original["metrics"]], original["bootstrap"]) == dev["gate"]
    if not dev["confirmation_allowed"] or not dev["gate"]["passed"]:
        raise ValueError("Failed mechanism screen: confirmation is prohibited")
    if (OUT / "confirmation.json").exists():
        raise FileExistsError("Confirmation already exists")
    fitted = read(OUT / "calibrators.json")
    results = [evaluate_year(year, fitted) for year in (2023, 2024)]
    bootstrap = bootstrap_mse([d for _, d in results])
    selected = gate([r["metrics"] for r, _ in results], bootstrap, confirmation=True)
    verify()
    write_new(OUT / "confirmation.json", {"development_sha256": sha(OUT / "development.json"),
        "calibrators_sha256": sha(OUT / "calibrators.json"), "bootstrap": bootstrap, "gate": selected,
        "result_sha256": {str(y): sha(OUT / f"result_{y}.json") for y in (2023, 2024)}})
    write_summary()
    log(f"Fixed-coefficient retrospective confirmation passed={selected['passed']}")


def write_summary():
    dev = read(OUT / "development.json")
    confirmation = read(OUT / "confirmation.json") if (OUT / "confirmation.json").exists() else None
    status = ("mechanism_failed_stop_without_confirmation" if not dev["gate"]["passed"] else
              "mechanism_passed_waiting_confirmation" if confirmation is None else
              "retrospective_confirmation_passed_no_deployment" if confirmation["gate"]["passed"] else
              "retrospective_confirmation_failed_no_deployment")
    years = [2022] + ([2023, 2024] if confirmation is not None else [])
    records = {str(y): read(OUT / f"result_{y}.json") for y in years}
    payload = {"status": status, "training_years": [2020, 2021], "years_evaluated": years,
        "horizon": 5, "all_years_previously_viewed": True, "official_scores_computed": False,
        "new_postprocessor_created": False, "release_changed": False, "development": dev,
        "confirmation": confirmation, "results": records,
        "limitations": ["Research target sums five raw excess labels against all finite-label market means, unlike the official limit-filtered daily score.",
                        "Overlapping target windows; block20 bootstrap is descriptive and not adjusted for historical selection.",
                        "Only stocks with five observed labels contribute errors; Top membership is fixed without labels and coverage is disclosed.",
                        "Feature state cold-starts annually; calibrator remains fixed at 2020/2021 throughout.",
                        "Predictive calibration is not a trading rule, executable portfolio, or proof of a better official score."]}
    (OUT / "summary.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2, allow_nan=False), encoding="utf-8")
    lines = ["# 固定五日收益价值校准：机制结果", "", f"状态：**{status}**。", "",
        "只用2020/2021纠正OOF输入拟合一次；唯一候选为9项状态特征Ridge，唯一门槛对照为raw/EMA联合5项Ridge。各对照拟合同一个5日原始超额目标。全部年份已查看，非新盲测。", "",
        "目标是连续5个市场交易日原始收益标签减全有限标签池日均值后求和，标签实现日为t+5。训练末5日完整purge，缺失不填零；特征状态每年冷启动。拟合与MSE均按日期等权。", "",
        "| 年份 | 信号 | 五日RankIC | 一日RankIC | 五日MSE | 固定Top五日超额和均值 | Top目标覆盖率 |", "|---|---|---:|---:|---:|---:|---:|"]
    for year, record in records.items():
        for name, m in record["metrics"].items():
            mse = "—" if m["mse5"] is None else f"{m['mse5']:.9f}"
            lines.append(f"| {year} | {name} | {m['rank_ic5']:.6f} | {m['rank_ic1']:.6f} | {mse} | {m['top5_excess_sum_mean']:.6f} | {m['top_target_coverage']:.2%} |")
    lines += ["", "## 固定门槛", "", "2022：相对联合对照，MSE至少改善0.1%、五日IC至少+0.002、Top五日原始超额和至少+1bp、20日块5000次重采样MSE改善为正占比至少0.80。确认须两年各项不倒退，年度等权合计也过同样门槛。", "", json.dumps(dev["gate"], ensure_ascii=False, indent=2), ""]
    if confirmation:
        lines += [json.dumps(confirmation["gate"], ensure_ascii=False, indent=2), ""]
    lines += ["## 使用限制", "", "本实验没有计算官方综合分，也没有生成新的留存/换股规则。研究目标的全有限标签池基准不同于官方非涨停收益池；Top先按当时预测与涨停标志选择，再测量可观测目标，不因缺失补选。覆盖率与固定训练分箱、在位年龄分组见groups_年份.csv。", "", "训练拟合、标准化、分箱阈值均不读取开发/确认标签；原始预测特征通过标签污染与50日前缀一致性检查。重叠标签用20日块诊断，但没有校正累计筛选偏差。官方优势、真实交易价值和下一步持仓策略均未由本机制实验确立。", ""]
    (OUT / "结论.md").write_text("\n".join(lines), encoding="utf-8")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("stage", choices=["test", "freeze", "develop", "confirm", "summarize"])
    args = parser.parse_args()
    if args.stage == "test":
        print(json.dumps(synthetic_tests(), indent=2))
    else:
        {"freeze": freeze, "develop": develop, "confirm": confirm, "summarize": write_summary}[args.stage]()
