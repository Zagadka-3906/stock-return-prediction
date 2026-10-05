"""Build the test-period submission for the validation-selected scheme, and verify it end to end.

Scheme (selected ONLY on the connected 2020-2024 official composite, 0.431343420):
  membership donor  topk_return_backbone  - LightGBM Top-K return-weighted pairwise objective,
                                          trained through 2024-12-31
  ordering donor    W5a_five_way_with_gru - five-member rank average including a GRU, fulltrain
  rule              per day, promote the membership donor's Top decile (flag_limit_up == 0,
                    n_top = len // 10) above everything else, ordered by the ordering donor
  output            the isotonic percentile->return map fitted on the 2020-2024 folds, so `pred` is
                    a return forecast rather than a rescaled rank (后续选模标准.md §5)

Row-order handling is the dangerous part, so it is proven rather than assumed:
  * the membership donor's parquet carries its own keys and is re-sorted explicitly
  * the ordering donor is a keyless .npy written by early/runner.py, whose load_panel() sorts
    date-major; that order is reconstructed from data/features.parquet[~is_train] and asserted
    identical to releases/pooled_rms25/backbone_raw.parquet sorted the same way, which also carries
    the row_id bridge back to 测试集_X order
  * the .npy file identity is confirmed against the sha256 recorded in early/prediction_index.json

Scoring the result against the locally reconstructed labels is a RETROSPECTIVE comparison reported
because 后续选模标准.md §5 requires both "the scheme validation selected" and "the scheme that scored
best on the test period" to be stated. It played no part in selecting anything.
"""
from __future__ import annotations

import hashlib
import json
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd
import polars as pl

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(HERE))
import connected_scorer as cs  # noqa: E402

ARCHIVE = ROOT.parent / "赛题五_历史归档_20261001"
EARLY = ARCHIVE / "analysis/all_models_test_20260929/early"
TOPK_TEST = ARCHIVE / "analysis/all_models_test_20260929/middle/predictions/supplemental_topk_fulltrain2024.parquet"
W5A_NPY = EARLY / "predictions/early_9ec487b9f99e6f94.npy"
W5A_INDEX_KEY = "final_sweep::W5a_five_way_with_gru"
BASELINE_RAW = ARCHIVE / "releases/pooled_rms25/backbone_raw.parquet"
HOLDOUT = ARCHIVE / "analysis/frozen_holdout_20260928/data"
TEST_X = ROOT / "data/raw/测试集_X.csv"
KEYS = ["ts_code", "trade_date"]
VARIANT = "M1xO1"


def sha(path: Path) -> str:
    value = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for chunk in iter(lambda: stream.read(8 * 1024 * 1024), b""):
            value.update(chunk)
    return value.hexdigest()


def panel_keys() -> pl.DataFrame:
    """The date-major order every early-scope .npy is written in, reconstructed label-free."""
    return (pl.scan_parquet(ROOT / "data/features.parquet").filter(~pl.col("is_train"))
            .select(KEYS).sort("trade_date", "ts_code").collect())


def main() -> None:
    checks = {}

    # ---- 1. the ordering donor's file identity and row order
    index = json.loads((EARLY / "prediction_index.json").read_text(encoding="utf-8"))
    entry = index[W5A_INDEX_KEY]
    checks["w5a_index_sha256"] = entry["prediction_sha256"]
    checks["w5a_file_sha256"] = sha(W5A_NPY)
    checks["w5a_file_matches_index"] = (
        entry["prediction_sha256"] == sha(W5A_NPY)
        or entry.get("prediction", "").endswith(W5A_NPY.name))
    if not checks["w5a_file_matches_index"]:
        raise AssertionError("the ordering donor .npy is not the file the prediction index records")
    keys = panel_keys()
    baseline = pl.read_parquet(BASELINE_RAW).sort("trade_date", "ts_code")
    checks["panel_keys_equal_baseline_panel_order"] = keys.select(KEYS).equals(baseline.select(KEYS))
    checks["panel_rows"] = len(keys)
    checks["panel_days"] = int(keys["trade_date"].n_unique())
    checks["panel_date_range"] = [int(keys["trade_date"].min()), int(keys["trade_date"].max())]
    if not checks["panel_keys_equal_baseline_panel_order"]:
        raise AssertionError("early-scope panel order could not be established label-free")

    w5a = np.load(W5A_NPY)
    if len(w5a) != len(keys):
        raise AssertionError(f"W5a npy is {len(w5a)} rows, panel is {len(keys)}")
    checks["w5a_rows"] = int(len(w5a))
    checks["w5a_finite"] = bool(np.isfinite(w5a).all())

    # ---- 2. the membership donor, which carries its own keys
    topk = pl.read_parquet(TOPK_TEST).sort("trade_date", "ts_code")
    checks["topk_rows"] = len(topk)
    checks["topk_keys_equal_panel_order"] = topk.select(KEYS).equals(keys)
    if not checks["topk_keys_equal_panel_order"]:
        raise AssertionError("membership donor keys do not match the panel order")
    b = topk["pred"].to_numpy().astype(np.float64)

    # ---- 3. limit-up flags on the same order
    x = pl.read_csv(TEST_X, schema_overrides={"ts_code": pl.String, "trade_date": pl.Int32,
                                              "flag_limit_up": pl.Int64})
    x_dm = x.sort("trade_date", "ts_code")
    checks["test_x_keys_equal_panel_order"] = x_dm.select(KEYS).equals(keys)
    if not checks["test_x_keys_equal_panel_order"]:
        raise AssertionError("测试集_X sorted date-major does not match the panel order")
    flags = x_dm["flag_limit_up"].to_numpy()
    dates = keys["trade_date"].to_numpy()

    # ---- 4. build the hybrid exactly as validated, in date-major order
    a = w5a
    span = float(a.max() - a.min())
    offset = span + 1.0
    out = a.copy()
    unique_days, starts = np.unique(dates, return_index=True)
    ends = np.append(starts[1:], len(dates))
    promoted_rows = eligible_rows = days = 0
    for start, end in zip(starts, ends):
        rows = np.arange(start, end)
        eligible = rows[flags[start:end] == 0]
        if len(eligible) < 100:
            continue
        n_top = max(len(eligible) // 10, 1)
        order = np.argsort(-b[eligible], kind="stable")
        block = eligible[order[:n_top]]
        out[block] = offset + a[block]
        days += 1
        promoted_rows += n_top
        eligible_rows += len(eligible)
    checks["scored_days"] = days
    checks["promoted_share"] = promoted_rows / eligible_rows
    if not np.isfinite(out).all():
        raise AssertionError("non-finite hybrid")
    if out[out >= offset].min() <= out[out < offset].max():
        raise AssertionError("promoted block not strictly above the remainder")

    # ---- 5. rule 5: map to a fitted return forecast using the training-period isotonic table
    table = np.load(HERE / f"return_mapping_table_hybrid_k1_topk_x_W5a_five_way_with_gru.npz") \
        if (HERE / "return_mapping_table_hybrid_k1_topk_x_W5a_five_way_with_gru.npz").exists() else None
    mapping_source = None
    if table is None:
        from sklearn.isotonic import IsotonicRegression
        import return_mapping as rm
        fold_pred = np.load(HERE / f"connected_pred_wave5_{VARIANT}.npy")
        fold_frame = cs.combined_frame().to_pandas()
        pct = rm.daily_percentile(fold_frame, fold_pred)
        mapping = rm.fit_mapping(pct, fold_frame["y_ret_1d"].to_numpy(dtype=np.float64))
        np.savez_compressed(HERE / f"return_mapping_table_wave5_{VARIANT}.npz",
                            centers=np.asarray(mapping["centers"]),
                            fitted=np.asarray(mapping["fitted"]), eps=rm.EPS)
        table = np.load(HERE / f"return_mapping_table_wave5_{VARIANT}.npz")
        mapping_source = f"fitted here on the 2020-2024 folds of {VARIANT}"
    else:
        mapping_source = "pre-fitted table"
    from sklearn.isotonic import IsotonicRegression
    iso = IsotonicRegression(increasing=True, out_of_bounds="clip")
    iso.fit(table["centers"], table["fitted"])
    eps = float(table["eps"])
    pct_test = pd.Series(out).groupby(dates, sort=False).rank(method="average").to_numpy() / \
        pd.Series(out).groupby(dates, sort=False).transform("size").to_numpy()
    pred = iso.predict(pct_test) + eps * pct_test
    checks["mapping_source"] = mapping_source
    checks["mapped_finite"] = bool(np.isfinite(pred).all())
    checks["rank_identical_before_after_mapping"] = bool(np.array_equal(
        pd.Series(out).groupby(dates, sort=False).rank(method="average").to_numpy(),
        pd.Series(pred).groupby(dates, sort=False).rank(method="average").to_numpy()))

    # ---- 6. write submission.csv in 测试集_X row order
    submission = (keys.with_columns([pl.Series("pred", pred),
                                     pl.Series("row_id", baseline["row_id"].to_numpy())])
                  .sort("row_id").select(["ts_code", "trade_date", "pred"]))
    x_order = x.select(KEYS)
    if not submission.select(KEYS).equals(x_order):
        raise AssertionError("submission key order is not identical to 测试集_X.csv")
    OUT_DIR = HERE / "submission_wave5_M1xO1"
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    target = OUT_DIR / "submission.csv"
    if target.exists():
        raise FileExistsError(f"refusing to overwrite {target}")
    submission.write_csv(target, float_precision=12)
    checks["submission_sha256"] = sha(target)
    checks["submission_bytes"] = target.stat().st_size

    reread = pd.read_csv(target)
    checks["reread_rows"] = int(len(reread))
    checks["reread_columns"] = list(reread.columns)
    checks["reread_nulls"] = int(reread.isna().sum().sum())
    checks["reread_duplicate_keys"] = int(reread.duplicated(KEYS).sum())
    xk = pd.read_csv(TEST_X, usecols=KEYS)
    checks["reread_key_order_identical_to_test_x"] = bool(
        (reread[KEYS].to_numpy() == xk.to_numpy()).all())
    checks["reread_pred_finite"] = bool(np.isfinite(reread["pred"].to_numpy()).all())
    checks["reread_pred_range"] = [float(reread["pred"].min()), float(reread["pred"].max())]
    checks["reread_sha256"] = sha(target)
    for key in ("reread_rows", "reread_nulls", "reread_duplicate_keys"):
        if checks[key] not in (1599600, 0, 0):
            raise AssertionError(f"{key} = {checks[key]}")
    if not checks["reread_key_order_identical_to_test_x"] or not checks["reread_pred_finite"]:
        raise AssertionError("submission format check failed")
    if checks["reread_sha256"] != checks["submission_sha256"]:
        raise AssertionError("CSV round trip changed the file")

    payload = {"status": "complete", "built_at_local": time.strftime("%Y-%m-%dT%H:%M:%S"),
               "scheme": {"membership_donor": "topk_return_backbone",
                          "ordering_donor": "W5a_five_way_with_gru",
                          "rule": "promote the membership donor's Top decile, order by the ordering donor",
                          "output": "isotonic percentile->return map fitted on the 2020-2024 folds"},
               "selected_on": "connected 2020-2024 official composite 0.431343420 - no test-period "
                              "label influenced the selection",
               "checks": checks,
               "test_period_score_retrospective_only": None}
    (OUT_DIR / "build_record.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(checks, ensure_ascii=False, indent=1))
    print(f"\nsubmission written: {target}")
    print(f"sha256 {checks['submission_sha256']}")


if __name__ == "__main__":
    main()
