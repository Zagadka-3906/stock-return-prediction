"""Point-in-time features for the competition's daily A-share panel.

Qlib supplies the Alpha158 factor definitions. Polars evaluates a documented
subset on the supplied files, avoiding Qlib's unrelated external data feed.
"""

from __future__ import annotations

import json
from pathlib import Path

import polars as pl
import qlib
from qlib.contrib.data.loader import Alpha158DL


PRICE = ("open", "high", "low", "close")
FLOATS = (*PRICE, "vol", "amount", "y_ret_1d")
WINDOWS = (5, 10, 20, 60)


def qlib_spec() -> dict[str, str]:
    expressions, names = Alpha158DL.get_feature_config(
        {
            "kbar": {},
            "price": {"windows": [0], "feature": ["OPEN", "HIGH", "LOW"]},
            "rolling": {
                "windows": list(WINDOWS),
                "include": ["ROC", "MA", "STD", "VMA", "VSTD"],
            },
        }
    )
    spec = dict(zip(names, expressions, strict=True))
    expected = {"KMID", "KLEN", "KMID2", "KUP", "KUP2", "KLOW", "KLOW2", "KSFT", "KSFT2", "OPEN0", "HIGH0", "LOW0"}
    expected |= {f"{family}{w}" for family in ("ROC", "MA", "STD", "VMA", "VSTD") for w in WINDOWS}
    if set(spec) != expected:
        raise RuntimeError(f"Qlib Alpha158 definition changed: {set(spec) ^ expected}")
    return spec


def div(a: pl.Expr, b: pl.Expr) -> pl.Expr:
    return pl.when(b.abs() > 1e-12).then(a / b).otherwise(None)


def source(path: Path, train: bool) -> pl.LazyFrame:
    schema = {
        "ts_code": pl.String,
        "trade_date": pl.Int32,
        "open": pl.Float32,
        "high": pl.Float32,
        "low": pl.Float32,
        "close": pl.Float32,
        "vol": pl.Float32,
        "amount": pl.Float32,
        "flag_limit_up": pl.Int8,
        "flag_limit_down": pl.Int8,
        "y_ret_1d": pl.Float32,
    }
    frame = pl.scan_csv(path, schema_overrides=schema, null_values=["NaN", "nan", ""], low_memory=True)
    if not train:
        frame = frame.with_columns(pl.lit(None, dtype=pl.Float32).alias("y_ret_1d"))
    return frame.with_row_index("row_id").with_columns(pl.lit(train).alias("is_train"))


def build_features(root: Path, output: Path) -> dict:
    spec = qlib_spec()
    train = source(root / "data" / "raw" / "训练集.csv", True)
    test = source(root / "data" / "raw" / "测试集_X.csv", False)
    lf = pl.concat((train, test), how="vertical").sort("ts_code", "trade_date")
    lf = lf.with_columns(pl.col(c).fill_nan(None).alias(c) for c in FLOATS)
    lf = lf.with_columns(
        pl.when(pl.col(c) > 0).then(pl.col(c)).otherwise(None).alias(c) for c in PRICE
    )
    o, h, l, c, v, a = (pl.col(x) for x in ("open", "high", "low", "close", "vol", "amount"))
    spread = h - l
    top = pl.max_horizontal(o, c)
    bottom = pl.min_horizontal(o, c)

    # Qlib Alpha158 k-bar formulas, evaluated at the close of day t.
    qexpr = {
        "KMID": div(c - o, o),
        "KLEN": div(spread, o),
        "KMID2": div(c - o, spread + 1e-12),
        "KUP": div(h - top, o),
        "KUP2": div(h - top, spread + 1e-12),
        "KLOW": div(bottom - l, o),
        "KLOW2": div(bottom - l, spread + 1e-12),
        "KSFT": div(2 * c - h - l, o),
        "KSFT2": div(2 * c - h - l, spread + 1e-12),
        "OPEN0": div(o, c),
        "HIGH0": div(h, c),
        "LOW0": div(l, c),
    }
    for w in WINDOWS:
        qexpr[f"ROC{w}"] = div(c.shift(w).over("ts_code"), c)
        qexpr[f"MA{w}"] = div(c.rolling_mean(w, min_samples=w).over("ts_code"), c)
        qexpr[f"STD{w}"] = div(c.rolling_std(w, min_samples=w).over("ts_code"), c)
        qexpr[f"VMA{w}"] = div(v.rolling_mean(w, min_samples=w).over("ts_code"), v)
        qexpr[f"VSTD{w}"] = div(v.rolling_std(w, min_samples=w).over("ts_code"), v)
    if set(qexpr) != set(spec):
        raise RuntimeError("Implemented Qlib factor names do not match Qlib's configuration")
    lf = lf.with_columns(expr.alias(name) for name, expr in qexpr.items())

    custom = {}
    for w in (1, 2, 3, 5, 10, 20, 60):
        custom[f"RET{w}"] = div(c, c.shift(w).over("ts_code")) - 1
    for w in (5, 20, 60):
        custom[f"AMT_RATIO{w}"] = div(a, a.rolling_mean(w, min_samples=w).over("ts_code"))
        custom[f"VOL_RATIO{w}"] = div(v, v.rolling_mean(w, min_samples=w).over("ts_code"))
    custom["LOG_AMOUNT"] = a.clip(lower_bound=0).log1p()
    custom["LOG_VOL"] = v.clip(lower_bound=0).log1p()
    custom["PRICE_TO_20D_HIGH"] = div(c, h.rolling_max(20, min_samples=20).over("ts_code"))
    custom["PRICE_TO_60D_HIGH"] = div(c, h.rolling_max(60, min_samples=60).over("ts_code"))
    custom["ILLIQ"] = div((div(c, c.shift(1).over("ts_code")) - 1).abs(), a)
    for w in (5, 10, 20):
        custom[f"UP_COUNT{w}"] = pl.col("flag_limit_up").rolling_sum(w, min_samples=w).over("ts_code")
    lf = lf.with_columns(expr.alias(name) for name, expr in custom.items())
    lf = lf.with_columns(div(pl.col("RET1").rolling_std(w, min_samples=w).over("ts_code"), pl.lit(1.0)).alias(f"RVOL{w}") for w in (5, 20))

    feature_names = list(qexpr) + list(custom) + ["RVOL5", "RVOL20", "flag_limit_up", "flag_limit_down"]
    rank_base = ["RET1", "RET5", "RET20", "KLEN", "LOG_AMOUNT", "RVOL20"]
    lf = lf.with_columns(
        (pl.col(name).rank(method="average").over("trade_date") / pl.col(name).count().over("trade_date")).alias(f"CS_{name}")
        for name in rank_base
    )
    feature_names += [f"CS_{name}" for name in rank_base]
    lf = lf.with_columns(
        (pl.col("y_ret_1d").rank(method="average").over("trade_date") / pl.col("y_ret_1d").count().over("trade_date") - 0.5).alias("y_rank"),
        c.is_not_null().alias("price_valid"),
    )
    lf = lf.with_columns(
        pl.when(pl.col(name).is_finite()).then(pl.col(name)).otherwise(None).cast(pl.Float32).alias(name)
        for name in feature_names + ["y_rank"]
    )
    keep = ["ts_code", "trade_date", "row_id", "is_train", "y_ret_1d", "y_rank", "price_valid"] + feature_names
    output.parent.mkdir(parents=True, exist_ok=True)
    print(f"Building {len(feature_names)} features on the combined stock panel...", flush=True)
    lf.select(keep).sink_parquet(output, compression="zstd", compression_level=3)
    info = {
        "feature_count": len(feature_names), "features": feature_names,
        "qlib_version": qlib.__version__, "qlib_alpha158_spec": spec,
        "train_rows": pl.scan_parquet(output).filter(pl.col("is_train")).select(pl.len()).collect().item(),
        "test_rows": pl.scan_parquet(output).filter(~pl.col("is_train")).select(pl.len()).collect().item(),
    }
    (output.parent / "feature_manifest.json").write_text(json.dumps(info, ensure_ascii=False, indent=2), encoding="utf-8")
    return info
