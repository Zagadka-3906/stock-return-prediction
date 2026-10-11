"""Sixteen predeclared, custom point-in-time features for a bounded experiment.

This module never reads labels for feature computation, never forward fills,
and does not modify the production feature store. Statistics named ``prior``
use the previous w panel rows and require all w observations to be valid.
Current-day cross-sectional information assumes prediction after market close.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import time
from pathlib import Path

import numpy as np
import polars as pl


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "experiments" / "feature_expansion_eval"
ADDED_FEATURE_FILE = OUT / "features.parquet"
TRAIN_FILE = ROOT / "data" / "raw" / "训练集.csv"
KEYS = ["ts_code", "trade_date"]
INPUT_COLUMNS = [*KEYS, "high", "low", "close", "vol", "amount"]
GROUPS = {
    "price_volume": [f"{family}{w}" for w in (20, 60)
                     for family in ("PX_POS", "AMT_Z", "PV_CORR", "SIGNED_FLOW")],
    "market_relative": ["EXCESS_RET1", "EXCESS_RET5", "EXCESS_RET20",
                        "MARKET_RET1", "MARKET_DISP1", "MARKET_BREADTH1",
                        "BETA60", "IDIO_VOL20"],
}
FEATURE_NAMES = [name for names in GROUPS.values() for name in names]
EPS = 1e-12
FORMULAS = {
    "PX_POSw": "(close_t - prior_w_min(low)) / (prior_w_max(high) - prior_w_min(low))",
    "AMT_Zw": "(log1p(amount_t) - prior_w_mean(log1p(amount))) / prior_w_sample_std(log1p(amount))",
    "PV_CORRw": "prior_w_sample_corr(RET1, diff(log1p(vol)))",
    "SIGNED_FLOWw": "prior_w_sum(sign(RET1) * vol) / prior_w_sum(vol)",
    "EXCESS_RETw": "RET_w(t) - cross_section_equal_weight_mean(RET_w(t)); w in 1,5,20",
    "MARKET_RET1": "cross_section_equal_weight_mean(RET1)",
    "MARKET_DISP1": "cross_section_sample_std(RET1); ddof=1",
    "MARKET_BREADTH1": "count(valid RET1 > 0) / count(valid RET1)",
    "BETA60": "prior_60_sample_cov(RET1, MARKET_RET1) / prior_60_sample_var(MARKET_RET1)",
    "IDIO_VOL20": "prior_20_sample_std(EXCESS_RET1); ddof=1",
    "RET_w": "close_t / close_(t-w) - 1; shift is within ts_code, no fill",
    "prior_w": "previous w panel rows excluding current row; min_samples=w, grouped by ts_code",
}


def file_hash(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(8 * 1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _div(a: pl.Expr, b: pl.Expr) -> pl.Expr:
    return pl.when(b.is_finite() & (b.abs() > EPS)).then(a / b).otherwise(None)


def _prior(expr: pl.Expr) -> pl.Expr:
    return expr.shift(1).over("ts_code")


def _return(w: int) -> pl.Expr:
    value = _div(pl.col("close"), pl.col("close").shift(w).over("ts_code")) - 1
    return pl.when(value.is_finite()).then(value).otherwise(None).alias(f"_ret{w}")


def _build_lazy(frame: pl.LazyFrame) -> pl.LazyFrame:
    # Projection intentionally discards labels or any other supplied columns.
    lf = frame.select(INPUT_COLUMNS).with_columns(
        pl.col("ts_code").cast(pl.String), pl.col("trade_date").cast(pl.Int32),
        *(pl.col(name).cast(pl.Float64, strict=False) for name in INPUT_COLUMNS[2:]),
    ).sort(KEYS)
    lf = lf.with_columns(
        *(pl.when(pl.col(name).is_finite() & (pl.col(name) > 0))
          .then(pl.col(name)).otherwise(None).alias(name) for name in ("high", "low", "close")),
        *(pl.when(pl.col(name).is_finite() & (pl.col(name) >= 0))
          .then(pl.col(name)).otherwise(None).alias(name) for name in ("vol", "amount")),
    )
    lf = lf.with_columns(
        *(_return(w) for w in (1, 5, 20)),
        pl.col("amount").log1p().alias("_logamount"),
        pl.col("vol").log1p().alias("_logvol"),
    )
    lf = lf.with_columns(
        pl.col("_logvol").diff().over("ts_code").alias("_dlogvol"),
        (pl.col("_ret1").sign() * pl.col("vol")).alias("_signedvol"),
        *(pl.col(f"_ret{w}").mean().over("trade_date").alias(f"_market{w}") for w in (1, 5, 20)),
        pl.col("_ret1").std(ddof=1).over("trade_date").alias("MARKET_DISP1"),
        (pl.col("_ret1") > 0).cast(pl.Float64).mean().over("trade_date").alias("MARKET_BREADTH1"),
    )
    lf = lf.with_columns(
        *((pl.col(f"_ret{w}") - pl.col(f"_market{w}")).alias(f"EXCESS_RET{w}") for w in (1, 5, 20)),
        pl.col("_market1").alias("MARKET_RET1"),
    )
    expressions = []
    for w in (20, 60):
        prior_low = _prior(pl.col("low").rolling_min(w, min_samples=w))
        prior_high = _prior(pl.col("high").rolling_max(w, min_samples=w))
        prior_amount_mean = _prior(pl.col("_logamount").rolling_mean(w, min_samples=w))
        prior_amount_std = _prior(pl.col("_logamount").rolling_std(w, min_samples=w, ddof=1))
        return_std = _prior(pl.col("_ret1").rolling_std(w, min_samples=w, ddof=1))
        volume_std = _prior(pl.col("_dlogvol").rolling_std(w, min_samples=w, ddof=1))
        correlation = _prior(pl.rolling_corr("_ret1", "_dlogvol", window_size=w, min_samples=w, ddof=1))
        expressions.extend([
            _div(pl.col("close") - prior_low, prior_high - prior_low).alias(f"PX_POS{w}"),
            _div(pl.col("_logamount") - prior_amount_mean, prior_amount_std).alias(f"AMT_Z{w}"),
            pl.when((return_std > EPS) & (volume_std > EPS)).then(correlation).otherwise(None).alias(f"PV_CORR{w}"),
            _div(_prior(pl.col("_signedvol").rolling_sum(w, min_samples=w)),
                 _prior(pl.col("vol").rolling_sum(w, min_samples=w))).alias(f"SIGNED_FLOW{w}"),
        ])
    expressions.extend([
        _div(_prior(pl.rolling_cov("_ret1", "_market1", window_size=60, min_samples=60, ddof=1)),
             _prior(pl.col("_market1").rolling_var(60, min_samples=60, ddof=1))).alias("BETA60"),
        _prior(pl.col("EXCESS_RET1").rolling_std(20, min_samples=20, ddof=1)).alias("IDIO_VOL20"),
    ])
    lf = lf.with_columns(expressions)
    return lf.select(
        *KEYS,
        *(pl.when(pl.col(name).cast(pl.Float32).is_finite())
          .then(pl.col(name).cast(pl.Float32)).otherwise(None).alias(name) for name in FEATURE_NAMES),
    )


def build_frame(frame: pl.DataFrame) -> pl.DataFrame:
    if frame.select(pl.struct(KEYS).n_unique()).item() != frame.height:
        raise ValueError("Duplicate ts_code/trade_date input keys")
    if frame.select(pl.any_horizontal(pl.col(KEYS).is_null()).any()).item():
        raise ValueError("Input keys cannot be null")
    return _build_lazy(frame.lazy()).collect()


def build_store() -> dict:
    OUT.mkdir(parents=True, exist_ok=True)
    start = time.monotonic()
    source_sha = file_hash(TRAIN_FILE)
    source = pl.scan_csv(
        TRAIN_FILE,
        schema_overrides={"ts_code": pl.String, "trade_date": pl.Int32,
                          **{name: pl.Float64 for name in INPUT_COLUMNS[2:]}},
        null_values=["NaN", "nan", ""], low_memory=True,
    ).select(INPUT_COLUMNS)
    checks = source.select(pl.len().alias("rows"), pl.struct(KEYS).n_unique().alias("unique_keys"),
                           pl.any_horizontal(pl.col(KEYS).is_null()).any().alias("null_keys")).collect().row(0, named=True)
    if checks["rows"] != checks["unique_keys"] or checks["null_keys"]:
        raise ValueError(f"Invalid source keys: {checks}")
    print(f"Building {len(FEATURE_NAMES)} custom features for {checks['rows']:,} training rows", flush=True)
    _build_lazy(source).sink_parquet(ADDED_FEATURE_FILE, compression="zstd", compression_level=3)
    summary = pl.scan_parquet(ADDED_FEATURE_FILE).select(
        pl.len().alias("rows"), pl.col("trade_date").min().alias("first_date"),
        pl.col("trade_date").max().alias("last_date"),
        pl.any_horizontal(*(pl.col(name).is_infinite() | pl.col(name).is_nan()
                            for name in FEATURE_NAMES)).any().alias("any_nonfinite_output"),
        *((pl.col(name).is_infinite() | pl.col(name).is_nan()).sum()
          .alias(f"nonfinite_count_{name}") for name in FEATURE_NAMES),
        *(pl.col(name).null_count().alias(name) for name in FEATURE_NAMES),
    ).collect().row(0, named=True)
    if summary["rows"] != checks["rows"]:
        raise AssertionError("Feature construction changed row count")
    if summary["any_nonfinite_output"]:
        raise AssertionError("Feature construction produced nonfinite nonnull values")
    manifest = {
        "feature_count": len(FEATURE_NAMES), "features": FEATURE_NAMES, "groups": GROUPS,
        "input_columns": INPUT_COLUMNS, "labels_used": False, "test_file_read": False,
        "source_file": str(TRAIN_FILE.relative_to(ROOT)), "source_sha256": source_sha,
        "feature_module_sha256": file_hash(Path(__file__)),
        "features_sha256": file_hash(ADDED_FEATURE_FILE), "polars_version": pl.__version__,
        "feature_origin": "Custom fixed experiment; not claimed equivalent to Qlib factors",
        "formula": FORMULAS, "denominator_epsilon": EPS, "calculation_dtype": "Float64",
        "storage_dtype": "Float32", "sort_order": KEYS,
        "prediction_timing": "After current-day close; daily aggregates use current observable full cross-section",
        "cleaning": "Prices <= 0 or nonfinite -> null; volume/amount < 0 or nonfinite -> null; no filling",
        "rolling_policy": "Fixed w panel rows, min_samples=w, shift(1) per symbol; sample std/cov/var ddof=1",
        "summary": summary, "seconds": time.monotonic() - start,
    }
    (OUT / "feature_manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"rows": summary["rows"], "seconds": manifest["seconds"],
                      "features_sha256": manifest["features_sha256"]}), flush=True)
    return manifest


def _fixture() -> pl.DataFrame:
    rng = np.random.default_rng(84021)
    rows = []
    for j, symbol in enumerate(("A", "B", "CONSTANT", "ZERO", "NEW")):
        n = 19 if symbol == "NEW" else 155
        returns = rng.normal(0.0002, .012, n)
        close = (10 + 3 * j) * np.cumprod(1 + returns)
        high, low = close * (1 + rng.uniform(.001, .02, n)), close * (1 - rng.uniform(.001, .02, n))
        vol = rng.lognormal(7, .35, n)
        amount = vol * close * rng.uniform(.98, 1.02, n)
        if symbol == "CONSTANT":
            close[:] = high[:] = low[:] = 20
            vol[:] = 100
            amount[:] = 2000
        if symbol == "ZERO":
            vol[:] = amount[:] = 0
        if symbol == "A":
            close[72], high[83], low[100], vol[101], amount[110] = 0, np.inf, np.nan, -2, -5
        if symbol == "B":
            close[3], vol[85], amount[25], low[15] = np.nan, np.inf, np.nan, 0
        for t in range(n):
            rows.append((symbol, 20200101 + t, high[t], low[t], close[t], vol[t], amount[t], rng.normal()))
    return pl.DataFrame(rows, schema=[*INPUT_COLUMNS, "y_ret_1d"], orient="row")


def _numpy_reference(frame: pl.DataFrame) -> pl.DataFrame:
    """Independent simple loops, with no Polars feature/window expressions."""
    frame = frame.select(INPUT_COLUMNS).sort(KEYS)
    codes = frame.get_column("ts_code").to_numpy()
    dates = frame.get_column("trade_date").to_numpy()
    data = {name: frame.get_column(name).to_numpy().astype(float).copy() for name in INPUT_COLUMNS[2:]}
    for name, values in data.items():
        values[~np.isfinite(values) | ((values <= 0) if name in ("high", "low", "close") else (values < 0))] = np.nan
    n = frame.height
    groups = [np.flatnonzero(codes == symbol) for symbol in sorted(set(codes))]
    returns = {w: np.full(n, np.nan) for w in (1, 5, 20)}
    dlogvol = np.full(n, np.nan)
    for ix in groups:
        for w in returns:
            if len(ix) > w:
                returns[w][ix[w:]] = data["close"][ix[w:]] / data["close"][ix[:-w]] - 1
        dlogvol[ix[1:]] = np.diff(np.log1p(data["vol"][ix]))
    result = {name: np.full(n, np.nan) for name in FEATURE_NAMES}
    markets = {w: np.full(n, np.nan) for w in returns}
    for date in sorted(set(dates)):
        ix = np.flatnonzero(dates == date)
        for w in returns:
            valid = returns[w][ix][np.isfinite(returns[w][ix])]
            if len(valid):
                markets[w][ix] = valid.mean()
        valid = returns[1][ix][np.isfinite(returns[1][ix])]
        if len(valid):
            result["MARKET_BREADTH1"][ix] = np.mean(valid > 0)
        if len(valid) > 1:
            result["MARKET_DISP1"][ix] = np.std(valid, ddof=1)
    result["MARKET_RET1"] = markets[1].copy()
    for w in returns:
        result[f"EXCESS_RET{w}"] = returns[w] - markets[w]
    for ix in groups:
        for t, i in enumerate(ix):
            for w in (20, 60):
                if t < w:
                    continue
                prev = ix[t-w:t]
                highs, lows = data["high"][prev], data["low"][prev]
                if np.isfinite(highs).all() and np.isfinite(lows).all():
                    denom = np.max(highs) - np.min(lows)
                    if abs(denom) > EPS:
                        result[f"PX_POS{w}"][i] = (data["close"][i] - np.min(lows)) / denom
                logamount = np.log1p(data["amount"][prev])
                if np.isfinite(logamount).all():
                    denom = np.std(logamount, ddof=1)
                    if denom > EPS:
                        result[f"AMT_Z{w}"][i] = (np.log1p(data["amount"][i]) - np.mean(logamount)) / denom
                ret, dvol = returns[1][prev], dlogvol[prev]
                if np.isfinite(ret).all() and np.isfinite(dvol).all():
                    if np.std(ret, ddof=1) > EPS and np.std(dvol, ddof=1) > EPS:
                        result[f"PV_CORR{w}"][i] = np.corrcoef(ret, dvol)[0, 1]
                volume = data["vol"][prev]
                if np.isfinite(ret).all() and np.isfinite(volume).all() and abs(volume.sum()) > EPS:
                    result[f"SIGNED_FLOW{w}"][i] = np.sum(np.sign(ret) * volume) / np.sum(volume)
            if t >= 60:
                prev = ix[t-60:t]
                ret, market = returns[1][prev], markets[1][prev]
                if np.isfinite(ret).all() and np.isfinite(market).all() and np.var(market, ddof=1) > EPS:
                    result["BETA60"][i] = np.cov(ret, market, ddof=1)[0, 1] / np.var(market, ddof=1)
            if t >= 20:
                excess = result["EXCESS_RET1"][ix[t-20:t]]
                if np.isfinite(excess).all():
                    result["IDIO_VOL20"][i] = np.std(excess, ddof=1)
    return frame.select(KEYS).with_columns(
        pl.Series(name, values).fill_nan(None).cast(pl.Float32) for name, values in result.items()
    ).select(*KEYS, *FEATURE_NAMES)


def _assert_equal(actual: pl.DataFrame, expected: pl.DataFrame, features: list[str] | None = None) -> float:
    features = FEATURE_NAMES if features is None else features
    assert actual.select(KEYS).equals(expected.select(KEYS))
    largest = 0.0
    for name in features:
        a, b = actual.get_column(name).to_numpy(), expected.get_column(name).to_numpy()
        np.testing.assert_array_equal(np.isnan(a), np.isnan(b), err_msg=f"Null mask differs: {name}")
        np.testing.assert_allclose(a, b, rtol=3e-5, atol=3e-7, equal_nan=True, err_msg=name)
        valid = np.isfinite(a) & np.isfinite(b)
        if valid.any():
            largest = max(largest, float(np.max(np.abs(a[valid] - b[valid]))))
    return largest


def run_tests() -> dict:
    OUT.mkdir(parents=True, exist_ok=True)
    fixture = _fixture()
    actual = build_frame(fixture)
    expected = _numpy_reference(fixture)
    largest = _assert_equal(actual, expected)
    assert actual.columns == KEYS + FEATURE_NAMES
    assert all(actual.schema[name] == pl.Float32 for name in FEATURE_NAMES)
    for cutoff in (20200101 + 90, 20200101 + 130):
        _assert_equal(build_frame(fixture.filter(pl.col("trade_date") <= cutoff)),
                      actual.filter(pl.col("trade_date") <= cutoff))
        future = fixture.with_columns(
            pl.when(pl.col("trade_date") > cutoff).then(pl.col(name) * 3.7 + 9)
            .otherwise(pl.col(name)).alias(name) for name in INPUT_COLUMNS[2:]
        )
        _assert_equal(build_frame(future).filter(pl.col("trade_date") <= cutoff),
                      actual.filter(pl.col("trade_date") <= cutoff))
    _assert_equal(build_frame(fixture.drop("y_ret_1d")), actual)
    _assert_equal(build_frame(fixture.with_columns((pl.col("y_ret_1d") * -999 + 87).alias("y_ret_1d"))), actual)
    _assert_equal(build_frame(fixture.reverse()), actual)
    changed_symbol = fixture.with_columns(
        pl.when(pl.col("ts_code") == "B").then(pl.col(name) * 2 + 3)
        .otherwise(pl.col(name)).alias(name) for name in INPUT_COLUMNS[2:]
    )
    _assert_equal(build_frame(changed_symbol).filter(pl.col("ts_code") != "B"),
                  actual.filter(pl.col("ts_code") != "B"), GROUPS["price_volume"])
    short = actual.filter(pl.col("ts_code") == "NEW")
    assert all(short.get_column(name).null_count() == short.height
               for name in GROUPS["price_volume"] + ["BETA60", "IDIO_VOL20"])
    constant = actual.filter(pl.col("ts_code") == "CONSTANT")
    assert all(constant.get_column(name).null_count() == constant.height
               for w in (20, 60) for name in (f"PX_POS{w}", f"AMT_Z{w}", f"PV_CORR{w}"))
    zero = actual.filter(pl.col("ts_code") == "ZERO")
    assert all(zero.get_column(name).null_count() == zero.height
               for w in (20, 60) for name in (f"AMT_Z{w}", f"PV_CORR{w}", f"SIGNED_FLOW{w}"))
    flat_only = build_frame(fixture.filter(pl.col("ts_code") == "CONSTANT"))
    assert flat_only.get_column("BETA60").null_count() == flat_only.height
    # Missing current close and its following one-day return remain null, without carry-forward.
    missing = actual.filter((pl.col("ts_code") == "A") & pl.col("trade_date").is_in([20200101 + 72, 20200101 + 73]))
    assert missing.get_column("EXCESS_RET1").null_count() == 2
    # Changing today's inputs cannot change any feature based exclusively on prior observations.
    target = 20200101 + 70
    altered = fixture.with_columns(
        pl.when((pl.col("ts_code") == "A") & (pl.col("trade_date") == target))
        .then(pl.col(name) * 2 + 1).otherwise(pl.col(name)).alias(name) for name in INPUT_COLUMNS[2:]
    )
    pure_prior = ["PV_CORR20", "PV_CORR60", "SIGNED_FLOW20", "SIGNED_FLOW60", "BETA60", "IDIO_VOL20"]
    selection = (pl.col("ts_code") == "A") & (pl.col("trade_date") == target)
    _assert_equal(build_frame(altered).filter(selection), actual.filter(selection), pure_prior)
    record = {
        "status": "passed", "passed": True, "feature_module_sha256": file_hash(Path(__file__)),
        "fixture_rows": fixture.height, "feature_count": len(FEATURE_NAMES),
        "numpy_tolerance": {"relative": 3e-5, "absolute": 3e-7, "null_mask": "exact"},
        "numpy_max_absolute_difference": largest,
        "checks": ["independent NumPy formulas and null masks for all 16 features",
                   "two full-cross-section prefix cutoffs", "two future perturbation cutoffs",
                   "labels removed and perturbed", "input ordering invariant",
                   "price-volume symbol isolation", "new short-history security",
                   "constant prices, amount and volume", "zero volume and zero denominators",
                   "missing, negative and nonfinite raw inputs", "no missing-price fill",
                   "prior-only statistics ignore current-day perturbation"],
    }
    (OUT / "feature_tests.json").write_text(json.dumps(record, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(record, ensure_ascii=False, indent=2), flush=True)
    return record


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("stage", choices=["test", "build", "all"])
    args = parser.parse_args()
    if args.stage in ("test", "all"):
        run_tests()
    if args.stage in ("build", "all"):
        build_store()


if __name__ == "__main__":
    main()
