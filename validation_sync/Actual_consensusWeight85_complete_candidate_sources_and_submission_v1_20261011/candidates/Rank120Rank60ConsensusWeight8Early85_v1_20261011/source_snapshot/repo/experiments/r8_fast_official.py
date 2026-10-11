"""Prepared, single-pass evaluator preserving the frozen official CSV semantics.

Usage: panel = PreparedOfficialPanel.from_frame(frame)
       metrics, daily = panel.score(prediction)
       merged = panel.merged(prediction)  # optional attribution input

The prepared object snapshots this exact frame's labels, flags and key order;
it has no global/year cache. Build a new object after changing any of those
inputs. Each prediction is freshly serialized at Polars float_precision=17 and
parsed by pandas' default CSV parser, just like the original score_official.
The score loop preserves pandas' default sort, sorted-row summation order,
NaN propagation, distinct return/turnover pools and turnover reset semantics.

This is an engineering implementation, not a new candidate or scoring rule.
``--test`` uses generated fixtures and temporary synthetic CSVs only. No
historical file is opened, and no benchmark result is written by this module.
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass
import hashlib
from io import StringIO
import json
from pathlib import Path
import sys
import tempfile
import warnings

sys.dont_write_bytecode = True
if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import numpy as np
import pandas as pd
import polars as pl
from scipy.stats import spearmanr

KEYS = ["ts_code", "trade_date"]
DAILY_COLUMNS = ["trade_date", "rank_ic", "excess", "top1_return", "turnover"]


@dataclass(frozen=True)
class PreparedOfficialPanel:
    """One immutable-input snapshot; returned merged frames are independent."""

    _keys: pl.DataFrame
    _labels: pd.DataFrame
    _flags: pd.DataFrame
    label_csv_sha256: str
    flag_csv_sha256: str

    @classmethod
    def from_frame(cls, frame: pl.DataFrame) -> "PreparedOfficialPanel":
        required = KEYS + ["y_ret_1d", "flag_limit_up"]
        if not isinstance(frame, pl.DataFrame) or frame.is_empty():
            raise ValueError("frame must be a nonempty Polars DataFrame")
        if not set(required) <= set(frame.columns):
            raise ValueError("frame must contain keys, y_ret_1d and flag_limit_up")
        keys = frame.select(KEYS)
        if any(keys.null_count().row(0)) or keys.select(pl.struct(KEYS).n_unique()).item() != len(keys):
            raise ValueError("frame keys must be unique and non-null")
        if frame.schema["y_ret_1d"] != pl.Float64:
            raise ValueError("Use original Float64 labels, not a float32 feature-cache label")
        if not frame.schema["trade_date"].is_integer():
            raise ValueError("trade_date must contain integer calendar dates")
        # These strings exactly follow the existing score_official's file writes.
        label_csv = frame.select(KEYS + ["y_ret_1d"]).write_csv(float_precision=17)
        flag_csv = frame.select(KEYS + ["flag_limit_up"]).write_csv()
        labels = pd.read_csv(StringIO(label_csv))
        flags = pd.read_csv(StringIO(flag_csv), usecols=KEYS + ["flag_limit_up"])
        if (labels[KEYS].isna().any().any() or labels.duplicated(KEYS).any()
                or not labels[KEYS].equals(flags[KEYS])):
            raise ValueError("CSV parsing changed keys into null, duplicate or inconsistent keys")
        digest = lambda value: hashlib.sha256(value.encode("utf-8")).hexdigest()
        return cls(keys.clone(), labels, flags, digest(label_csv), digest(flag_csv))

    def merged(self, prediction: np.ndarray) -> pd.DataFrame:
        """Return the exact official pred→label→flag inner-merge, in input order.

        Labels/flags are the construction-time snapshot. No prediction, rank,
        outcome or result cache is reused across calls. Callers may modify the
        returned dataframe without changing subsequent evaluations.
        """
        values = np.asarray(prediction)
        if values.ndim != 1 or values.shape != (self._keys.height,):
            raise ValueError("prediction must be one-dimensional and aligned with the original frame")
        if not np.issubdtype(values.dtype, np.number):
            raise ValueError("prediction must be numeric")
        # Keep the supplied numeric dtype: the original Polars Series does too.
        csv = self._keys.with_columns(pl.Series("pred", values)).write_csv(float_precision=17)
        pred = pd.read_csv(StringIO(csv))
        merged = pred.merge(self._labels, on=KEYS, how="inner")
        merged = merged.merge(self._flags, on=KEYS, how="inner")
        if len(merged) != self._keys.height:
            raise AssertionError("Canonical prediction and prepared input keys no longer align")
        return merged.copy(deep=True)

    def score(self, prediction: np.ndarray) -> tuple[dict, pl.DataFrame]:
        """Return the official eight metrics and matching per-date evidence.

        No tolerance/rounding is applied. Missing or constant IC days retain
        the official evaluator's NaN behavior, including its non-nanmean IC
        aggregate and zero ICIR when the standard deviation is not positive.
        """
        merged = self.merged(prediction)
        ic_values, excess_values, top_values, turnovers, records = [], [], [], [], []
        previous = None
        for date, group in merged.groupby("trade_date"):
            row = {"trade_date": int(date), "rank_ic": np.nan, "excess": np.nan,
                   "top1_return": np.nan, "turnover": np.nan}
            labeled = group.dropna(subset=["y_ret_1d"])
            if len(labeled) >= 30:
                ic, _ = spearmanr(labeled["pred"], labeled["y_ret_1d"])
                ic_values.append(ic)
                row["rank_ic"] = float(ic)
            returns = group[(group["flag_limit_up"] == 0) & group["y_ret_1d"].notna()].copy()
            if len(returns) >= 100:
                # Do not use stable sort/argpartition. Even ties must follow the
                # installed pandas default, exactly as in the frozen evaluator.
                returns = returns.sort_values("pred", ascending=False).reset_index(drop=True)
                k = max(len(returns) // 10, 1)
                top = returns["y_ret_1d"].iloc[:k].mean()
                # The official market mean is computed AFTER prediction sorting.
                # A cached pre-sort mean can differ through floating-point order.
                excess = top - returns["y_ret_1d"].mean()
                top_values.append(top)
                excess_values.append(excess)
                row["top1_return"], row["excess"] = float(top), float(excess)
            tradeable = group[group["flag_limit_up"] == 0].copy()
            if len(tradeable) < 100:
                previous = None
            else:
                tradeable = tradeable.sort_values("pred", ascending=False)
                current = set(tradeable["ts_code"].iloc[:max(len(tradeable) // 10, 1)])
                if previous is not None and len(previous) > 0:
                    turnover = 1.0 - len(current & previous) / len(current | previous)
                    turnovers.append(turnover)
                    row["turnover"] = float(turnover)
                previous = current
            records.append(row)
        mean_ic, ic_std = np.mean(ic_values), np.std(ic_values, ddof=1)
        annual_excess, mean_turnover = np.mean(excess_values) * 252, np.mean(turnovers)
        metrics = {"ic_mean": float(mean_ic), "ic_std": float(ic_std),
                   "icir": float(mean_ic / ic_std if ic_std > 0 else 0),
                   "ic_positive_ratio": float(np.mean(np.array(ic_values) > 0)),
                   "annual_excess": float(annual_excess),
                   "top1_annual_ret": float(np.mean(top_values) * 252),
                   "mean_turnover": float(mean_turnover),
                   "final_score": float(mean_ic * .4 + annual_excess * .3 + (1 - mean_turnover) * .3)}
        return metrics, pl.DataFrame(records)


def tests() -> dict:
    """Exact (equal-NaN) agreement with original evaluator and frozen daily code."""
    from evaluate import evaluate
    from experiments.official_seed_development import _same_csv_daily
    from unittest.mock import patch

    checks = {}

    def exact(actual, expected, name):
        np.testing.assert_array_equal(actual, expected, err_msg=name)

    def compare(name, frame, pred, context=None):
        context = context or PreparedOfficialPanel.from_frame(frame)
        with tempfile.TemporaryDirectory(prefix="r8-synthetic-score-") as temporary:
            folder = Path(temporary)
            frame.select(KEYS).with_columns(pl.Series("pred", pred)).write_csv(folder / "submission.csv", float_precision=17)
            frame.select(KEYS + ["y_ret_1d"]).write_csv(folder / "测试集_Y.csv", float_precision=17)
            frame.select(KEYS + ["flag_limit_up"]).write_csv(folder / "测试集_X.csv")
            # Constant/empty synthetic pools intentionally produce NaN warnings.
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                with patch("evaluate.logger"):
                    official = evaluate(str(folder / "submission.csv"), str(folder))
                rebuilt, expected_daily = _same_csv_daily(folder)
                actual, daily = context.score(pred)
            assert actual.keys() == official.keys() == rebuilt.keys()
            for key in actual:
                exact(actual[key], official[key], f"{name}/official/{key}")
                exact(actual[key], rebuilt[key], f"{name}/frozen_daily/{key}")
            assert daily.columns == expected_daily.columns == DAILY_COLUMNS
            exact(daily.to_numpy(), expected_daily.to_numpy(), f"{name}/daily")
            direct = pd.read_csv(folder / "submission.csv").merge(
                pd.read_csv(folder / "测试集_Y.csv"), on=KEYS, how="inner").merge(
                pd.read_csv(folder / "测试集_X.csv", usecols=KEYS + ["flag_limit_up"]), on=KEYS, how="inner")
            pd.testing.assert_frame_equal(context.merged(pred), direct, check_exact=True)
        checks[name] = {"eight_metrics_exact_equal_nan": True, "daily_exact_equal_nan": True,
                        "merged_order_dtypes_values_exact": True}
        return actual, daily, context

    n, days = 120, 8
    stock = np.tile(np.arange(n), days)
    day = np.repeat(np.arange(days), n)
    rng = np.random.default_rng(20260926)
    labels = rng.normal(0, .025, n * days)
    labels[8:14] = [np.nextafter(.1, 1.), np.nextafter(-.1, -1.), 1.234567890123456e-12,
                   1e16, 1., -1e16]
    labels[(day == 0) & (stock < 7)] = np.nan
    # Boundaries: <30 labels, exactly30 labels, all missing, exactly100 labels.
    labels[(day == 3) & (stock >= 29)] = np.nan
    labels[(day == 5) & (stock >= 30)] = np.nan
    labels[day == 6] = np.nan
    labels[(day == 7) & (stock >= 100)] = np.nan
    flags = np.zeros(n * days, dtype=np.int64)
    flags[(day == 1) & (stock < 3)] = 1
    flags[(day == 2) & (stock < 21)] = 1  # 99 -> reset previous turnover Top.
    flags[(day == 3) & (stock < 20)] = 1  # exactly100, starts a new chain.
    pred = ((stock * 7 + day * 3) % 17).astype(float) / 17
    pred[stock == 119] = np.nextafter(.1, 1.)
    frame = pl.DataFrame({"ts_code": [f"{i:06d}.SZ" for i in stock],
                          "trade_date": 20200102 + day, "y_ret_1d": labels,
                          "flag_limit_up": flags})
    # Both temporal and within-day order are intentionally noncanonical.
    order = rng.permutation(len(frame))
    frame, pred = frame[order], pred[order]
    metrics, daily, context = compare("ties_precision_missing_thresholds_and_shuffled_keys", frame, pred)
    assert np.isnan(daily["rank_ic"][3]) and np.isfinite(daily["rank_ic"][5])
    assert np.isnan(daily["turnover"][2]) and np.isnan(daily["turnover"][3])
    assert np.isfinite(daily["turnover"][4]) and np.isfinite(daily["turnover"][6])
    assert np.isnan(daily["excess"][5]) and np.isfinite(daily["excess"][7])
    checks["thresholds_and_label_independent_turnover_reset"] = True
    constant, _, _ = compare("constant_prediction_nan_propagation", frame, np.ones(len(frame)), context)
    assert np.isnan(constant["ic_mean"]) and np.isnan(constant["final_score"])
    assert constant["icir"] == 0 and constant["ic_positive_ratio"] == 0
    compare("same_context_new_prediction_not_cached", frame, -pred, context)
    compare("float32_prediction_csv_dtype_preserved", frame, pred.astype(np.float32), context)
    for count in (29, 30, 99, 100):
        small = frame.filter(pl.col("trade_date") == 20200103).head(count).with_columns(
            pl.lit(0).alias("flag_limit_up"))
        compare(f"single_day_pool_{count}", small, np.arange(count, dtype=float))
    missing = frame.with_columns(pl.lit(None, dtype=pl.Float64).alias("y_ret_1d"))
    compare("all_missing_labels_turnover_still_defined", missing, pred)
    no_trade = frame.with_columns(pl.lit(1).alias("flag_limit_up"))
    compare("no_tradeable_stocks", no_trade, pred)
    modified_labels = frame.with_columns((-pl.col("y_ret_1d") + .0003).alias("y_ret_1d"))
    _, _, new_context = compare("changed_labels_new_context", modified_labels, pred)
    assert context.label_csv_sha256 != new_context.label_csv_sha256
    assert context.flag_csv_sha256 == new_context.flag_csv_sha256
    changed_flags = frame.with_columns((1 - pl.col("flag_limit_up")).alias("flag_limit_up"))
    flag_context = PreparedOfficialPanel.from_frame(changed_flags)
    assert context.flag_csv_sha256 != flag_context.flag_csv_sha256
    assert context.label_csv_sha256 == flag_context.label_csv_sha256
    original_merged = context.merged(pred)
    mutated = context.merged(pred)
    mutated.loc[:, "y_ret_1d"] = 999.
    mutated.loc[:, "flag_limit_up"] = 1
    mutated.loc[:, "pred"] = -100.
    pd.testing.assert_frame_equal(context.merged(pred), original_merged, check_exact=True)
    # Changing the original Polars object must not silently alter an old snapshot.
    mutable_input = frame.clone()
    snapshot = PreparedOfficialPanel.from_frame(mutable_input)
    mutable_input.replace_column(mutable_input.get_column_index("y_ret_1d"),
                                 pl.Series("y_ret_1d", np.full(len(frame), 999.)))
    pd.testing.assert_frame_equal(snapshot.merged(pred), original_merged, check_exact=True)
    checks["input_snapshot_and_returned_frame_isolation"] = True
    checks["label_and_flag_csv_hashes_bind_full_inputs"] = True
    rejects = 0
    for operation in (
        lambda: PreparedOfficialPanel.from_frame(frame.head(0)),
        lambda: PreparedOfficialPanel.from_frame(frame.drop("y_ret_1d")),
        lambda: PreparedOfficialPanel.from_frame(frame.with_columns(pl.col("y_ret_1d").cast(pl.Float32))),
        lambda: PreparedOfficialPanel.from_frame(pl.concat([frame, frame.head(1)])),
        lambda: context.score(pred[:-1]),
        lambda: context.score(pred.reshape(-1, 1)),
    ):
        try:
            operation()
        except ValueError:
            rejects += 1
        else:
            raise AssertionError("Malformed prepared-score input was accepted")
    checks["reject_malformed_inputs"] = rejects == 6
    return {"status": "passed", "checks": checks, "check_count": len(checks),
            "historical_data_read": False, "historical_candidates_created_or_scored": False,
            "comparison": "All 8 official metrics and all daily values exactly equal, including NaNs; no tolerance.",
            "versions": {"numpy": np.__version__, "pandas": pd.__version__, "polars": pl.__version__}}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--test", action="store_true", required=True)
    parser.parse_args()
    print(json.dumps(tests(), ensure_ascii=False, indent=2, allow_nan=False))
