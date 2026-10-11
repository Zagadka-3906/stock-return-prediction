"""Point-in-time characteristic-cell peer features from the 63 base columns."""
from __future__ import annotations
import polars as pl
PEER_COLUMNS = ["PEER_RET1", "PEER_RET1_L1", "PEER_RET3", "PEER_DEV"]

def quintile(expression: pl.Expr) -> pl.Expr:
    pct = (expression.rank(method="average").over("trade_date")
           / expression.count().over("trade_date"))
    return (pct * 5).cast(pl.Int8).clip(0, 4)

def add_columns(frame: pl.DataFrame) -> pl.DataFrame:
    lag_ret = {2: "RET2", 3: "RET3", 5: "RET5", 10: "RET10", 20: "RET20", 60: "RET60"}
    previous = {2: "RET1", 3: "RET2", 5: "RET3", 10: "RET5", 20: "RET10", 60: "RET20"}
    out = frame.with_columns(
        (quintile(pl.col("RET20")) * 5 + quintile(pl.col("STD20"))).alias("_cell"))
    group = ["trade_date", "_cell"]
    cell_sum = pl.col("RET1").sum().over(group)
    cell_count = pl.col("RET1").count().over(group)
    out = out.with_columns(
        pl.when(pl.col("price_valid") & (cell_count > 1))
        .then((cell_sum - pl.col("RET1")) / (cell_count - 1)).otherwise(None).alias("PEER_RET1"))
    out = out.with_columns(
        pl.col("PEER_RET1").shift(1).over("ts_code").alias("PEER_RET1_L1"),
        pl.col("PEER_RET1").rolling_mean(3, min_samples=1).over("ts_code").alias("PEER_RET3"),
        (pl.col("RET1") - pl.col("PEER_RET1")).alias("PEER_DEV"))
    for k, column in lag_ret.items():
        out = out.with_columns(
            pl.when((1 + pl.col(previous[k])).abs() > 1e-12)
            .then((1 + pl.col(column)) / (1 + pl.col(previous[k])) - 1)
            .otherwise(None).alias(f"LAGRET{k}"))
    return out.drop("_cell")
