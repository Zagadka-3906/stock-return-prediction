"""Build, verify and score the test-period submission for a selected Top-set-substitution scheme.

Everything the scheme needs already exists on disk, so nothing is retrained:
  membership donor  topk_return_backbone at its RELEASED post-processing -> the finished test column
                    middle/predictions/supplemental_topk_fulltrain2024.parquet (carries its own keys)
  ordering donor    W5a_five_way_with_gru -> early/predictions/early_9ec487b9f99e6f94.npy, a keyless
                    array in the early-scope panel order, which is date-major (trade_date, ts_code)
                    over features.parquet[~is_train]; that order is reconstructed here and asserted
                    identical to releases/pooled_rms25/backbone_raw.parquet sorted the same way, which
                    also supplies the row_id bridge back to 测试集_X order
  retention floor   the same exact swap-budget solve validated on the folds, cold-started on the first
                    test day because no earlier Top set exists
  output            the isotonic percentile->return map fitted ONLY on the 2020-2024 folds of this same
                    scheme, so `pred` is a return forecast rather than a rescaled rank (§5)

The scheme must already be selected on the connected 2020-2024 caliber before this runs. The
test-period score it reports at the end is a RETROSPECTIVE comparison required by §5 ("report
separately the scheme validation selected and the scheme that scored best on the test period"); it is
computed after the file is written and plays no part in any choice made here.
"""
from __future__ import annotations

import argparse
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
from optimize_wave7b import build  # noqa: E402
from return_mapping import daily_percentile, fit_mapping, apply_mapping, top_sets  # noqa: E402
import connected_scorer as cs  # noqa: E402
from analysis.official_score_contributions import composite  # noqa: E402

ARCHIVE = ROOT.parent / "赛题五_历史归档_20261001"
ALLMODELS = ARCHIVE / "analysis/all_models_test_20260929"
TOPK_TEST = ALLMODELS / "middle/predictions/supplemental_topk_fulltrain2024.parquet"
W5A_NPY = ALLMODELS / "early/predictions/early_9ec487b9f99e6f94.npy"
W5A_INDEX_KEY = "final_sweep::W5a_five_way_with_gru"
BASELINE_RAW = ARCHIVE / "releases/pooled_rms25/backbone_raw.parquet"
HOLDOUT = ARCHIVE / "analysis/frozen_holdout_20260928/data"
TEST_X = ROOT / "data/raw/测试集_X.csv"
KEYS = ["ts_code", "trade_date"]


def sha(path) -> str:
    value = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for chunk in iter(lambda: stream.read(8 * 1024 * 1024), b""):
            value.update(chunk)
    return value.hexdigest()


def log(message: str) -> None:
    print(f"[{time.strftime('%H:%M:%S')}] {message}", flush=True)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--member-fold-array", default="wave7b_topk_x_W5a__m0.985.npy",
                        help="the selected scheme's saved CONNECTED FOLD prediction, used only to fit "
                             "the return mapping inside the training period")
    parser.add_argument("--m-frac", type=float, default=0.985)
    parser.add_argument("--member-connected", default="0.434034593",
                        help="the selected scheme's connected 2020-2024 score, recorded not recomputed")
    parser.add_argument("--out-name", default="submission_final")
    args = parser.parse_args()

    checks = {"selected_on": "connected 2020-2024 official composite",
              "connected_score_at_selection": float(args.member_connected),
              "m_frac": args.m_frac,
              "member_fold_array": args.member_fold_array}

    # ---- 1. panel order, reconstructed label-free and cross-checked against a keyed artifact
    panel = (pl.scan_parquet(ROOT / "data/features.parquet").filter(~pl.col("is_train"))
             .select(KEYS + ["flag_limit_up"]).sort("trade_date", "ts_code").collect())
    baseline = pl.read_parquet(BASELINE_RAW).sort("trade_date", "ts_code")
    if not panel.select(KEYS).equals(baseline.select(KEYS)):
        raise AssertionError("panel order != backbone_raw order; the .npy alignment is unknown")
    checks["panel_rows"] = len(panel)
    checks["panel_days"] = int(panel["trade_date"].n_unique())
    checks["panel_date_range"] = [int(panel["trade_date"].min()), int(panel["trade_date"].max())]
    checks["panel_order_matches_keyed_baseline"] = True
    log(f"panel: {len(panel):,} rows, {checks['panel_days']} days, "
        f"{checks['panel_date_range'][0]}..{checks['panel_date_range'][1]}")

    # ---- 2. ordering donor: keyless .npy, verified against the prediction index
    index = json.loads((ALLMODELS / "early/prediction_index.json").read_text(encoding="utf-8"))
    entry = index[W5A_INDEX_KEY]
    orderer = np.load(W5A_NPY)
    checks["orderer"] = {"file": W5A_NPY.name, "sha256": sha(W5A_NPY),
                         "index_test_id": entry["test_id"],
                         "index_prediction_sha256": entry["prediction_sha256"],
                         "index_rows": entry["rows"],
                         "rows_match_panel": len(orderer) == len(panel),
                         "labels_read_when_produced": entry.get("labels_read"),
                         "postprocessing_state": entry.get("postprocessing_state")}
    if len(orderer) != len(panel):
        raise AssertionError(f"orderer is {len(orderer)} rows, panel is {len(panel)}")
    if not np.isfinite(orderer).all():
        raise AssertionError("orderer has non-finite values")
    log(f"ordering donor W5a loaded: {len(orderer):,} rows, sha {sha(W5A_NPY)[:16]}…")

    # ---- 3. membership donor: keyed parquet, must land on the same order
    topk = pl.read_parquet(TOPK_TEST).sort("trade_date", "ts_code")
    if not topk.select(KEYS).equals(panel.select(KEYS)):
        raise AssertionError("membership donor keys do not match the panel order")
    member = topk["pred"].to_numpy().astype(np.float64)
    checks["member"] = {"file": TOPK_TEST.name, "sha256": sha(TOPK_TEST), "rows": len(topk),
                        "keys_match_panel": True}
    log(f"membership donor topk loaded: {len(member):,} rows")

    # ---- 4. limit-up flags must agree between the feature panel and the raw test file
    dates = panel["trade_date"].to_numpy()
    flags_panel = panel["flag_limit_up"].to_numpy().astype(np.int64)
    x = pl.read_csv(TEST_X, schema_overrides={"ts_code": pl.String, "trade_date": pl.Int32,
                                              "flag_limit_up": pl.Int64}).sort("trade_date", "ts_code")
    if not np.array_equal(x["flag_limit_up"].to_numpy().astype(np.int64), flags_panel):
        raise AssertionError("flag_limit_up differs between features.parquet and 测试集_X.csv")
    checks["flag_limit_up_agrees_with_test_x"] = True

    # ---- 5. the exact swap-budget solve validated on the folds, cold-started on day one
    codes, uniques = pd.factorize(panel["ts_code"].to_pandas(), sort=True)
    codes = codes.astype(np.int64)
    hybrid, stats = build(member, orderer, dates, flags_panel, codes, len(uniques), args.m_frac)
    checks["construction"] = stats
    if stats["boundary_tie_days"]:
        raise AssertionError(f"{stats['boundary_tie_days']} days have a promotion-boundary tie")
    log(f"hybrid built: {stats['days']} days, mean retention "
        f"{stats['mean_retention_ratio']:.6f}, boundary ties {stats['boundary_tie_days']}")

    # ---- 6. rule 5: fit the return map inside the training period only, then apply
    fold_pred = np.load(HERE / args.member_fold_array)
    fold_frame = cs.combined_frame().to_pandas()
    if len(fold_pred) != len(fold_frame):
        raise AssertionError("fold array does not match the combined fold frame")
    fold_pct = daily_percentile(fold_frame, fold_pred)
    mapping = fit_mapping(fold_pct, fold_frame["y_ret_1d"].to_numpy(dtype=np.float64))
    test_pct = daily_percentile(pd.DataFrame({"trade_date": dates}), hybrid)
    pred = apply_mapping(mapping, test_pct)
    checks["return_mapping"] = {
        "fitted_on": "2020-2024 fold predictions of this same scheme and their realized labels",
        "n_obs": mapping["n_obs"], "bins": mapping["bins"], "eps": mapping["eps"],
        "range": mapping["range"],
        "no_test_period_label_read": True,
        "E_r_at_percentile": {p: float(np.interp(p, mapping["centers"], mapping["fitted"]))
                              for p in (0.5, 0.9, 0.99, 1.0)},
    }
    rank_before = pd.Series(hybrid).groupby(dates, sort=False).rank(method="average").to_numpy()
    rank_after = pd.Series(pred).groupby(dates, sort=False).rank(method="average").to_numpy()
    checks["mapping_preserved_within_day_ranks"] = bool(np.array_equal(rank_before, rank_after))
    if not checks["mapping_preserved_within_day_ranks"]:
        raise AssertionError("the return mapping changed the within-day ranking")
    log(f"return mapping fitted on {mapping['n_obs']:,} training rows; ranks preserved: "
        f"{checks['mapping_preserved_within_day_ranks']}")

    # ---- 7. write in 测试集_X order using the row_id bridge
    submission = (panel.with_columns([pl.Series("pred", pred),
                                      pl.Series("row_id", baseline["row_id"].to_numpy())])
                  .sort("row_id").select(["ts_code", "trade_date", "pred"]))
    x_order = pl.read_csv(TEST_X, schema_overrides={"ts_code": pl.String, "trade_date": pl.Int32}
                          ).select(KEYS)
    if not submission.select(KEYS).equals(x_order):
        raise AssertionError("submission key order is not identical to 测试集_X.csv")
    out_dir = HERE / "final_submission"
    out_dir.mkdir(parents=True, exist_ok=True)
    target = out_dir / f"{args.out_name}.csv"
    if target.exists():
        raise FileExistsError(f"refusing to overwrite {target}")
    submission.write_csv(target, float_precision=12)

    # ---- 8. re-read and verify the artifact that would actually be uploaded
    reread = pd.read_csv(target)
    xk = pd.read_csv(TEST_X, usecols=KEYS)
    checks["submission"] = {
        "path": str(target), "sha256": sha(target), "bytes": target.stat().st_size,
        "rows": int(len(reread)), "columns": list(reread.columns),
        "columns_exact": list(reread.columns) == ["ts_code", "trade_date", "pred"],
        "nulls": int(reread.isna().sum().sum()),
        "duplicate_keys": int(reread.duplicated(KEYS).sum()),
        "key_order_identical_to_test_x": bool((reread[KEYS].to_numpy() == xk.to_numpy()).all()),
        "pred_all_finite": bool(np.isfinite(reread["pred"].to_numpy()).all()),
        "pred_range": [float(reread["pred"].min()), float(reread["pred"].max())],
        "pred_mean": float(reread["pred"].mean()), "pred_std": float(reread["pred"].std()),
        "date_range": [int(reread.trade_date.min()), int(reread.trade_date.max())],
    }
    s = checks["submission"]
    for key, want in (("rows", 1599600), ("nulls", 0), ("duplicate_keys", 0)):
        if s[key] != want:
            raise AssertionError(f"{key} = {s[key]}, expected {want}")
    for key in ("columns_exact", "key_order_identical_to_test_x", "pred_all_finite"):
        if not s[key]:
            raise AssertionError(f"submission check failed: {key}")
    if s["date_range"] != [20250102, 20260608]:
        raise AssertionError(f"unexpected date range {s['date_range']}")
    log(f"submission written: {s['rows']:,} rows, sha {s['sha256'][:16]}…, "
        f"pred range [{s['pred_range'][0]:.6f}, {s['pred_range'][1]:.6f}]")

    # ---- 9. retrospective test-period score, computed AFTER the file was written
    from experiments.revalidate_fold_local import score_official
    labels = pd.read_csv(HOLDOUT / "测试集_Y.csv")
    frame = pl.from_pandas(
        pd.read_csv(HOLDOUT / "测试集_X.csv").merge(labels, on=KEYS, how="left")
        .query("trade_date <= 20260605").reset_index(drop=True))
    test_pred = reread[reread.trade_date <= 20260605]["pred"].to_numpy(np.float64)
    if len(test_pred) != len(frame):
        raise AssertionError(f"scoring slice is {len(test_pred)} rows, frame is {len(frame)}")
    metrics, daily = score_official(frame, test_pred)
    daily_pd = daily.to_pandas()
    checks["test_period_retrospective"] = {
        "note": "computed after the submission was written; reported per §5, never used to select",
        "days": int(len(daily_pd)), "metrics": metrics,
        "segments": {"2025": composite(daily_pd[daily_pd.trade_date < 20260101]),
                     "2026": composite(daily_pd[daily_pd.trade_date >= 20260101])},
    }
    log(f"RETROSPECTIVE test-period score (343 of 344 days): {metrics['final_score']:.9f} "
        f"(ic {metrics['ic_mean']:.6f}, excess {metrics['annual_excess']:.6f}, "
        f"turnover {metrics['mean_turnover']:.6f})")

    record = {"status": "complete", "built_at_local": time.strftime("%Y-%m-%dT%H:%M:%S"),
              "scheme": {"membership_donor": "topk_return_backbone @ released post-processing",
                         "ordering_donor": "W5a_five_way_with_gru @ released post-processing",
                         "top_set_rule": f"exact swap-budget retention floor m = "
                                         f"round({args.m_frac} * n_top) against the previous day's "
                                         "realized Top decile, cold start on the first test day",
                         "output": "isotonic percentile->return map fitted on the 2020-2024 folds"},
              "checks": checks}
    (out_dir / f"{args.out_name}_build_record.json").write_text(
        json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    np.save(out_dir / f"{args.out_name}_pred.npy", pred)
    log(f"build record: {out_dir / (args.out_name + '_build_record.json')}")


if __name__ == "__main__":
    main()
