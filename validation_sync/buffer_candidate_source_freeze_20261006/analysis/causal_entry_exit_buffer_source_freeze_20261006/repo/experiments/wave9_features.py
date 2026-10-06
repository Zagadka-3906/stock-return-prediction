"""Wave-9 exploratory round: extended OHLCV features no earlier round constructed.

The competition supplies only open/high/low/close/vol/amount and two limit flags, so
every feature in this project is a function of that one panel. The base 63 columns use
rolling windows of 5/10/20/60 days, and the single prior expansion round
(`experiments/feature_expansion_features.py`) added price-volume and market-relative
columns at 20/60 days. Five information axes were left untouched, confirmed by a
read-only survey of every feature-building module in the repository:

  1. windows longer than 60 days — nothing anywhere exceeds 60;
  2. higher moments of daily returns — only the standard deviation exists (RVOL5/20);
  3. return autocorrelation, the classic reversal-structure proxy — never a feature;
  4. the overnight/intraday decomposition as an INPUT. It exists only as a prediction
     TARGET, which failed at −0.025 composite, and base OPEN0 is the same-day
     open/close, not the gap open_t / close_{t−1};
  5. trend efficiency (Kaufman ratio), a path-shape measure no existing column encodes.

Conventions are copied from `src/features.py` so the new columns are drop-in: `div()`
guards |denominator| > 1e-12, every rolling window uses `min_samples=w` and
`.over("ts_code")`, non-finite values become null, and everything is stored Float32.
Rows keep the base panel's `row_id`, so the extended columns join back without
re-sorting and the unsorted stock-major training order that LightGBM bagging depends
on is preserved.

Only 训练集.csv is read. That is sufficient because the five retrospective validation
folds (2020-2024) and all of their history lie inside it, and it keeps this round
unable to produce a submission or to leak. Extending the panel to 测试集_X.csv is a
separate step that only an adopted candidate would need.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import time
from pathlib import Path

import numpy as np
import polars as pl

from run import ROOT

OUT = ROOT / "experiments" / "wave9_exploratory_20260927"
TRAIN_FILE = ROOT / "data" / "raw" / "训练集.csv"
BASE_PANEL = ROOT / "data" / "features.parquet"
PANEL_FILE = OUT / "features_extended.parquet"
MANIFEST = OUT / "feature_manifest.json"
TESTS = OUT / "feature_tests.json"
KEYS = ["ts_code", "trade_date"]
EPS = 1e-12
LONG = 120

NEW_FEATURES = [
    "ROC120", "MA120", "STD120", "VMA120", "VSTD120", "PRICE_TO_120D_HIGH",
    "SKEW20", "SKEW60", "KURT20", "KURT60",
    "ACF1_20", "ACF1_60",
    "ON_RET1", "ON_MEAN5", "ON_MEAN20", "ON_STD20", "ON_MAX20", "ON_RATIO20",
    "EFF20", "EFF60",
]
GROUPS = {
    "long_window": ["ROC120", "MA120", "STD120", "VMA120", "VSTD120", "PRICE_TO_120D_HIGH"],
    "higher_moments": ["SKEW20", "SKEW60", "KURT20", "KURT60"],
    "autocorrelation": ["ACF1_20", "ACF1_60"],
    "overnight_intraday": ["ON_RET1", "ON_MEAN5", "ON_MEAN20", "ON_STD20", "ON_MAX20", "ON_RATIO20"],
    "trend_efficiency": ["EFF20", "EFF60"],
}
FORMULAS = {
    "ROC120": "Ref($close,120)/$close, matching the base ROC family",
    "MA120": "Mean($close,120)/$close",
    "STD120": "Std($close,120)/$close",
    "VMA120": "Mean($volume,120)/($volume+1e-12)",
    "VSTD120": "Std($volume,120)/($volume+1e-12)",
    "PRICE_TO_120D_HIGH": "$close/Max($high,120)",
    "SKEWw": "population skewness of RET1 over the trailing w days, from rolling moments",
    "KURTw": "population excess kurtosis of RET1 over the trailing w days, from rolling moments",
    "ACF1_w": "corr(RET1_t, RET1_{t-1}) over the trailing w days",
    "ON_RET1": "$open_t/$close_{t-1} - 1, the overnight gap; the base panel has no such column",
    "ON_MEANw": "Mean(ON_RET1,w)",
    "ON_STDw": "Std(ON_RET1,w)",
    "ON_MAX20": "Max(|ON_RET1|,20)",
    "ON_RATIO20": "Sum(|ON_RET1|,20)/(Sum(|ON_RET1|,20)+Sum(|INTRA_RET1|,20)), INTRA_RET1=$close/$open-1",
    "EFFw": "|$close_t - $close_{t-w}| / Sum(|$close_i - $close_{i-1}|, w), the Kaufman efficiency ratio",
    "RET1": "$close_t/$close_{t-1} - 1, identical to the base column of the same name",
    "prior_w": "trailing w panel rows including the current day, min_samples=w, grouped by ts_code",
}


def file_hash(path: Path) -> str:
    digest = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for block in iter(lambda: stream.read(8 * 1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def log(message: str) -> None:
    print(f"[{time.strftime('%H:%M:%S')}] {message}", flush=True)


def div(a: pl.Expr, b: pl.Expr) -> pl.Expr:
    return pl.when(b.is_finite() & (b.abs() > EPS)).then(a / b).otherwise(None)


def source(path: Path) -> pl.LazyFrame:
    """Byte-for-byte the base builder's reader, restricted to the training file."""
    schema = {"ts_code": pl.String, "trade_date": pl.Int32, "open": pl.Float32,
              "high": pl.Float32, "low": pl.Float32, "close": pl.Float32, "vol": pl.Float32,
              "amount": pl.Float32, "flag_limit_up": pl.Int8, "flag_limit_down": pl.Int8,
              "y_ret_1d": pl.Float32}
    return (pl.scan_csv(path, schema_overrides=schema, null_values=["NaN", "nan", ""],
                        low_memory=True)
            .with_row_index("row_id"))


def clean(lf: pl.LazyFrame) -> pl.LazyFrame:
    floats = ("open", "high", "low", "close", "vol", "amount")
    lf = lf.with_columns(pl.col(name).fill_nan(None).alias(name) for name in floats)
    return lf.with_columns(pl.when(pl.col(name) > 0).then(pl.col(name)).otherwise(None).alias(name)
                           for name in ("open", "high", "low", "close"))


def stage_a(lf: pl.LazyFrame) -> pl.LazyFrame:
    """Columns that need a shift or a plain rolling aggregate of a raw price column."""
    o, h, c, v = (pl.col(name) for name in ("open", "high", "close", "vol"))
    prior = c.shift(1).over("ts_code")
    return lf.with_columns(
        (div(c, prior) - 1).alias("_ret1"),
        (div(o, prior) - 1).alias("_on1"),
        (div(c, o) - 1).alias("_intra1"),
        (c - prior).abs().alias("_step"),
        div(c.shift(LONG).over("ts_code"), c).alias("ROC120"),
        div(c.rolling_mean(LONG, min_samples=LONG).over("ts_code"), c).alias("MA120"),
        div(c.rolling_std(LONG, min_samples=LONG).over("ts_code"), c).alias("STD120"),
        div(v.rolling_mean(LONG, min_samples=LONG).over("ts_code"), v).alias("VMA120"),
        div(v.rolling_std(LONG, min_samples=LONG).over("ts_code"), v).alias("VSTD120"),
        div(c, h.rolling_max(LONG, min_samples=LONG).over("ts_code")).alias("PRICE_TO_120D_HIGH"),
        c.shift(20).over("ts_code").alias("_c20"),
        c.shift(60).over("ts_code").alias("_c60"),
    )


def stage_b(lf: pl.LazyFrame) -> pl.LazyFrame:
    """Rolling statistics over the stage-A intermediates."""
    ret1, on1, intra1, step, c = (pl.col(name) for name in ("_ret1", "_on1", "_intra1", "_step",
                                                            "close"))
    expressions = []
    for window in (20, 60):
        m1 = ret1.rolling_mean(window, min_samples=window).over("ts_code")
        m2 = (ret1 ** 2).rolling_mean(window, min_samples=window).over("ts_code")
        m3 = (ret1 ** 3).rolling_mean(window, min_samples=window).over("ts_code")
        m4 = (ret1 ** 4).rolling_mean(window, min_samples=window).over("ts_code")
        variance = m2 - m1 ** 2
        central3 = m3 - 3 * m1 * m2 + 2 * m1 ** 3
        central4 = m4 - 4 * m1 * m3 + 6 * m1 ** 2 * m2 - 3 * m1 ** 4
        expressions.append(div(central3, variance ** 1.5).alias(f"SKEW{window}"))
        expressions.append(div(central4, variance ** 2).fill_nan(None)
                           .sub(3).alias(f"KURT{window}"))
        expressions.append(pl.rolling_corr(ret1, ret1.shift(1), window_size=window,
                                           min_samples=window).over("ts_code")
                           .alias(f"ACF1_{window}"))
        path = step.rolling_sum(window, min_samples=window).over("ts_code")
        expressions.append(div((c - pl.col(f"_c{window}")).abs(), path).alias(f"EFF{window}"))
    expressions += [
        on1.alias("ON_RET1"),
        on1.rolling_mean(5, min_samples=5).over("ts_code").alias("ON_MEAN5"),
        on1.rolling_mean(20, min_samples=20).over("ts_code").alias("ON_MEAN20"),
        on1.rolling_std(20, min_samples=20).over("ts_code").alias("ON_STD20"),
        on1.abs().rolling_max(20, min_samples=20).over("ts_code").alias("ON_MAX20"),
        div(on1.abs().rolling_sum(20, min_samples=20).over("ts_code"),
            on1.abs().rolling_sum(20, min_samples=20).over("ts_code")
            + intra1.abs().rolling_sum(20, min_samples=20).over("ts_code")).alias("ON_RATIO20"),
    ]
    return lf.with_columns(*expressions)


def build_frame(lf: pl.LazyFrame) -> pl.LazyFrame:
    """Sorted by symbol then date for the rolling windows, as the base builder does."""
    lf = clean(lf).sort("ts_code", "trade_date")
    lf = stage_b(stage_a(lf))
    return lf.with_columns(
        pl.when(pl.col(name).is_finite()).then(pl.col(name)).otherwise(None).cast(pl.Float32)
        .alias(name) for name in NEW_FEATURES)


def build() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    if PANEL_FILE.exists():
        raise SystemExit("Extended panel already built; preserving it")
    if not TESTS.exists():
        raise SystemExit("Run the synthetic tests before materializing the panel")
    tests = json.loads(TESTS.read_text(encoding="utf-8"))
    if tests["status"] != "passed":
        raise SystemExit("Synthetic tests did not pass")
    started = time.monotonic()
    frame = (build_frame(source(TRAIN_FILE))
             .select(["row_id", *KEYS, *NEW_FEATURES])
             .sort("row_id").collect())
    base_keys = (pl.scan_parquet(BASE_PANEL).filter(pl.col("is_train"))
                 .select(["row_id", *KEYS]).sort("row_id").collect())
    if not frame.select(["row_id", *KEYS]).equals(base_keys):
        raise AssertionError("Extended panel keys do not align row-for-row with the base panel's "
                             "training rows")
    if frame.select(KEYS).n_unique() != frame.height:
        raise AssertionError("Keys are not unique; a join back to the base panel would be ambiguous")
    nulls = {name: int(frame[name].null_count()) for name in NEW_FEATURES}
    frame.drop("row_id").write_parquet(PANEL_FILE, compression="zstd", compression_level=3)
    elapsed = time.monotonic() - started
    payload = {
        "built_at_local": time.strftime("%Y-%m-%dT%H:%M:%S"), "seconds": round(elapsed, 2),
        "polars_version": pl.__version__, "rows": frame.height, "feature_count": len(NEW_FEATURES),
        "features": NEW_FEATURES, "groups": GROUPS, "formulas": FORMULAS,
        "long_window_days": LONG, "min_samples": "window length, so shorter history is null",
        "row_alignment": "row_id equals the base panel's row_id for every training row, keys "
                         "verified equal and unique; the base panel's row_id repeats across its "
                         "train and test halves, so downstream joins use (ts_code, trade_date)",
        "source_files": {"训练集.csv": file_hash(TRAIN_FILE)},
        "test_file_read": False,
        "null_counts": nulls,
        "null_share": {name: round(nulls[name] / frame.height, 6) for name in NEW_FEATURES},
        "panel_sha256": file_hash(PANEL_FILE),
        "source_sha256": file_hash(Path(__file__)),
    }
    MANIFEST.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    log(f"Built {PANEL_FILE.name}: {frame.height:,} rows x {len(NEW_FEATURES)} features in "
        f"{elapsed:.1f}s; worst null share {max(payload['null_share'].values()):.4f}")


# --------------------------------------------------------------------------- tests

def _fixture(days: int = 150) -> pl.DataFrame:
    rng = np.random.default_rng(20260927)
    frames = []
    for index, symbol in enumerate(("A", "B", "FLAT", "SHORT")):
        count = days if symbol != "SHORT" else 40
        close = 10.0 * np.exp(np.cumsum(rng.normal(0.0005, 0.02, count)))
        open_ = close * (1 + rng.normal(0, 0.006, count))
        high = np.maximum(open_, close) * (1 + np.abs(rng.normal(0, 0.005, count)))
        low = np.minimum(open_, close) * (1 - np.abs(rng.normal(0, 0.005, count)))
        vol = np.abs(rng.normal(1e6, 2e5, count)) + 1e3
        if symbol == "FLAT":
            close[:] = 10.0
            open_[:] = 10.0
            high[:] = 10.0
            low[:] = 10.0
        frames.append(pl.DataFrame({
            "ts_code": [symbol] * count,
            "trade_date": [20180101 + i for i in range(count)],
            "open": open_.astype(np.float32), "high": high.astype(np.float32),
            "low": low.astype(np.float32), "close": close.astype(np.float32),
            "vol": vol.astype(np.float32), "amount": (vol * close).astype(np.float32),
            "y_ret_1d": rng.normal(0, 0.02, count).astype(np.float32),
        }))
    return pl.concat(frames).with_row_index("row_id")


def _numpy_reference(frame: pl.DataFrame) -> dict[str, np.ndarray]:
    """Independent per-symbol numpy implementation of all twenty features."""
    out = {name: np.full(frame.height, np.nan) for name in NEW_FEATURES}
    data = {key: frame[key].to_numpy() for key in
            ("open", "high", "low", "close", "vol", "y_ret_1d")}
    codes = frame["ts_code"].to_numpy()

    def ratio(numerator, denominator):
        with np.errstate(invalid="ignore", divide="ignore"):
            value = np.where(np.isfinite(denominator) & (np.abs(denominator) > EPS),
                             numerator / denominator, np.nan)
        return value

    def rolling(values, window, statistic):
        result = np.full(len(values), np.nan)
        for stop in range(window, len(values) + 1):
            block = values[stop - window:stop]
            if np.isfinite(block).all():
                result[stop - 1] = statistic(block)
        return result

    for symbol in np.unique(codes):
        rows = np.flatnonzero(codes == symbol)
        close = data["close"][rows].astype(np.float64)
        open_ = data["open"][rows].astype(np.float64)
        high = data["high"][rows].astype(np.float64)
        vol = data["vol"][rows].astype(np.float64)
        prior = np.concatenate(([np.nan], close[:-1]))
        ret1 = ratio(close, prior) - 1
        on1 = ratio(open_, prior) - 1
        intra1 = ratio(close, open_) - 1
        step = np.abs(close - prior)

        def shift(lag, series=close):
            shifted = np.full(len(series), np.nan)
            if lag < len(series):
                shifted[lag:] = series[:len(series) - lag]
            return shifted
        out["ROC120"][rows] = ratio(shift(120), close)
        out["MA120"][rows] = ratio(rolling(close, 120, np.mean), close)
        out["STD120"][rows] = ratio(rolling(close, 120, lambda b: np.std(b, ddof=1)), close)
        out["VMA120"][rows] = ratio(rolling(vol, 120, np.mean), vol)
        out["VSTD120"][rows] = ratio(rolling(vol, 120, lambda b: np.std(b, ddof=1)), vol)
        out["PRICE_TO_120D_HIGH"][rows] = ratio(close, rolling(high, 120, np.max))
        for window in (20, 60):
            def moments(block):
                mean = block.mean()
                return (((block - mean) ** 2).mean(), ((block - mean) ** 3).mean(),
                        ((block - mean) ** 4).mean())
            variance = rolling(ret1, window, lambda b: moments(b)[0])
            third = rolling(ret1, window, lambda b: moments(b)[1])
            fourth = rolling(ret1, window, lambda b: moments(b)[2])
            with np.errstate(invalid="ignore", divide="ignore"):
                out[f"SKEW{window}"][rows] = np.where(variance > EPS, third / variance ** 1.5,
                                                      np.nan)
                out[f"KURT{window}"][rows] = np.where(variance > EPS,
                                                      fourth / variance ** 2 - 3, np.nan)
            lagged = np.concatenate(([np.nan], ret1[:-1]))
            autocorrelation = np.full(len(ret1), np.nan)
            for stop in range(window, len(ret1) + 1):
                left = ret1[stop - window:stop]
                right = lagged[stop - window:stop]
                if not (np.isfinite(left).all() and np.isfinite(right).all()):
                    continue
                spread_x, spread_y = left.std(), right.std()
                if spread_x > 0 and spread_y > 0:
                    autocorrelation[stop - 1] = float(
                        ((left - left.mean()) * (right - right.mean())).mean()
                        / (spread_x * spread_y))
            out[f"ACF1_{window}"][rows] = autocorrelation
            out[f"EFF{window}"][rows] = ratio(np.abs(close - shift(window)),
                                              rolling(step, window, np.sum))
        out["ON_RET1"][rows] = on1
        out["ON_MEAN5"][rows] = rolling(on1, 5, np.mean)
        out["ON_MEAN20"][rows] = rolling(on1, 20, np.mean)
        out["ON_STD20"][rows] = rolling(on1, 20, lambda b: np.std(b, ddof=1))
        out["ON_MAX20"][rows] = rolling(np.abs(on1), 20, np.max)
        out["ON_RATIO20"][rows] = ratio(rolling(np.abs(on1), 20, np.sum),
                                        rolling(np.abs(on1), 20, np.sum)
                                        + rolling(np.abs(intra1), 20, np.sum))
    return out


def run_tests() -> dict:
    OUT.mkdir(parents=True, exist_ok=True)
    fixture = _fixture()
    built = build_frame(fixture.lazy()).collect().sort("row_id")

    reference = _numpy_reference(fixture)
    worst = {}
    for name in NEW_FEATURES:
        actual = built[name].cast(pl.Float64).to_numpy()
        expected = reference[name]
        actual = np.where(np.isnan(actual), np.nan, actual)
        null_actual, null_expected = np.isnan(actual), np.isnan(expected)
        if not np.array_equal(null_actual, null_expected):
            raise AssertionError(f"{name}: null pattern differs from the numpy reference "
                                 f"({int(null_actual.sum())} vs {int(null_expected.sum())} rows)")
        finite = ~null_actual
        difference = np.abs(actual[finite] - expected[finite])
        worst[name] = float(difference.max()) if difference.size else 0.0
        if difference.size and difference.max() > 1e-4:
            raise AssertionError(f"{name}: max abs difference {difference.max():.3e}")

    truncated = (build_frame(fixture.filter(pl.col("trade_date") <= 20180101 + 99).lazy())
                 .collect().select(["row_id", *NEW_FEATURES]))
    joined = truncated.join(built.select(["row_id", *NEW_FEATURES]), on="row_id", suffix="_full")
    if joined.height != truncated.height:
        raise AssertionError("Prefix rows did not all survive the join")
    for name in NEW_FEATURES:
        left = joined[name].cast(pl.Float64).to_numpy()
        right = joined[f"{name}_full"].cast(pl.Float64).to_numpy()
        left = np.where(np.isnan(left), np.nan, left)
        right = np.where(np.isnan(right), np.nan, right)
        left_null, right_null = np.isnan(left), np.isnan(right)
        if not np.array_equal(left_null, right_null):
            raise AssertionError(f"{name}: 100-day prefix changed the null pattern")
        if not np.allclose(left[~left_null], right[~right_null], atol=1e-6, rtol=0):
            raise AssertionError(f"{name}: a later row changed an earlier feature value")

    poisoned = fixture.with_columns(pl.lit(987654.0, dtype=pl.Float32).alias("y_ret_1d"))
    altered = build_frame(poisoned.lazy()).collect().sort("row_id")
    for name in NEW_FEATURES:
        if not altered[name].equals(built[name]):
            raise AssertionError(f"{name}: depends on the return label")

    finite_source = {}
    for name in NEW_FEATURES:
        values = built[name].cast(pl.Float64).to_numpy()
        nulls = int(np.isnan(values).sum())
        finite_source[name] = {"rows": len(values), "null_rows": nulls,
                               "non_null_rows": len(values) - nulls}

    payload = {
        "status": "passed", "ran_at_local": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "fixture_rows": fixture.height, "fixture_symbols": fixture["ts_code"].unique().to_list(),
        "fixture_includes": ["a constant-price symbol (zero dispersion guards)",
                             "a symbol shorter than every window (insufficient history)",
                             "150-day symbols for the 20/60 windows"],
        "numpy_reference_max_abs_difference": worst,
        "checks": {
            "numpy_reference_matches_polars": True,
            "null_pattern_matches_reference": True,
            "100_day_prefix_invariance": True,
            "return_label_poisoning_invariance": True,
            "test_file_never_read": True,
        },
        "feature_row_accounting": finite_source,
        "source_sha256": file_hash(Path(__file__)),
    }
    TESTS.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    log(f"Synthetic tests passed; worst numpy/polars gap "
        f"{max(worst.values()):.2e} across {len(NEW_FEATURES)} features")
    return payload


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("stage", choices=("tests", "build"))
    arguments = parser.parse_args()
    if arguments.stage == "tests":
        run_tests()
    else:
        build()
