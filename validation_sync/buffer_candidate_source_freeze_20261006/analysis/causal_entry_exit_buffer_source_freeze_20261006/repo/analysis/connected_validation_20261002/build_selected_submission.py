"""Build the test-period submission for the wave-9/10 selected scheme, end to end, with proofs.

Scheme: Top-decile MEMBERSHIP from the topk return-weighted pairwise backbone at its released
post-processing; ORDERING from the peer67_slow16 backbone re-post-processed at the selected
(alpha, bonus); an exact swap-budget retention floor m against the previous day's realized Top decile;
and finally the isotonic percentile->return map fitted on the 2020-2024 folds of this same scheme, so
`pred` is a return forecast rather than a rescaled rank (后续选模标准.md §5).

Nothing here is retrained. Both donors' test-period inputs already exist:
  membership  middle/predictions/supplemental_topk_fulltrain2024.parquet (finished column, keyed)
  ordering    deliveries/peer67_slow16_20260929/prediction.parquet carries pred_raw, so ANY
              post-processing can be re-applied; the auxiliary comes from
              releases/pooled_rms25/auxiliary_raw.parquet, row-aligned with it

Three proofs run before the file is written:
  1. rebuilding the ordering donor at the RELEASED settings must reproduce the delivery's own
     rank_score column element-for-element, and the shipped pred must be exactly
     np.where(rank_score < -1, -0.05, 0.04*(rank_score - 0.5)) - this proves the parameterized stack
     is the production pipeline and that it never reads labels
  2. the selected scheme's connected fold score must equal the recorded selection score
  3. the return mapping must leave every within-day rank untouched, so the official score is unchanged

The test-period score printed at the end is computed AFTER the file is written and is the §5(b)
retrospective disclosure; it selects nothing.
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
import connected_scorer as cs  # noqa: E402
from src.scoring import Panel  # noqa: E402
from experiments.revalidate_fold_local import score_official  # noqa: E402
from optimize_wave6 import make_prediction_param  # noqa: E402
from optimize_wave7b import build  # noqa: E402
from return_mapping import daily_percentile, fit_mapping, apply_mapping  # noqa: E402
from analysis.official_score_contributions import composite  # noqa: E402

ARCHIVE = ROOT.parent / "赛题五_历史归档_20261001"
ALLMODELS = ARCHIVE / "analysis/all_models_test_20260929"
TOPK_TEST = ALLMODELS / "middle/predictions/supplemental_topk_fulltrain2024.parquet"
DELIVERY = ARCHIVE / "deliveries/peer67_slow16_20260929"
AUX = ARCHIVE / "releases/pooled_rms25/auxiliary_raw.parquet"
HOLDOUT = ARCHIVE / "analysis/frozen_holdout_20260928/data"
TEST_X = ROOT / "data/raw/测试集_X.csv"
KEYS = ["ts_code", "trade_date"]
CUTOFF = 20260605
RELEASED = {"alpha": 0.9, "bonus": 0.3, "restore_lower": True, "top_current_weight": 1.0,
            "mode": "top_only", "weight": 0.25}


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
    parser.add_argument("--alpha", type=float, required=True)
    parser.add_argument("--bonus", type=float, required=True)
    parser.add_argument("--m-frac", type=float, required=True)
    parser.add_argument("--fold-array", required=True,
                        help="saved CONNECTED FOLD prediction of this exact scheme, used only to fit "
                             "the return mapping inside the training period")
    parser.add_argument("--expected-connected", type=float, required=True,
                        help="the connected 2020-2024 score recorded when this scheme was selected")
    parser.add_argument("--out-name", required=True)
    parser.add_argument("--member-mode", choices=("topk", "nested"), default="topk",
                        help="topk = the membership donor is the topk backbone's own finished test "
                             "column; nested = the donor is the wave-1 hybrid (topk membership, "
                             "slow16 ordering at released settings, m=0) rebuilt on the test period "
                             "first, which is what wave 11 ranked highest")
    args = parser.parse_args()
    setting = {**RELEASED, "alpha": args.alpha, "bonus": args.bonus}
    checks = {"selected_on": "connected 2020-2024 official composite",
              "expected_connected": args.expected_connected,
              "orderer_postprocess": setting, "m_frac": args.m_frac}

    # ---- ordering donor frame: the delivery's own test-period raw, plus the pooled auxiliary
    prediction = pl.read_parquet(DELIVERY / "prediction.parquet")
    aux = pl.read_parquet(AUX)
    if not aux.select(KEYS).equals(prediction.select(KEYS)):
        raise AssertionError("auxiliary_raw and the delivery prediction frame are not row-aligned")
    prediction = (prediction
                  .with_columns(aux["pred_raw"].cast(pl.Float64).alias("aux_raw"))
                  .with_columns(pl.col("flag_limit_up").cast(pl.Int64))
                  .with_columns(pl.lit(None, dtype=pl.Float64).alias("y_ret_1d")))
    panel = Panel.from_frame(prediction)
    aux_values = prediction["aux_raw"].to_numpy().astype(np.float64)
    raw = prediction["pred_raw"].to_numpy().astype(np.float64)

    # ---- proof 1: the parameterized stack IS the production pipeline, and reads no labels
    shipped_rank = prediction["rank_score"].to_numpy().astype(np.float64)
    shipped_pred = prediction["pred"].to_numpy().astype(np.float64)
    affine = np.where(shipped_rank < -1, -0.05, 0.04 * (shipped_rank - 0.5))
    if not np.array_equal(affine, shipped_pred):
        raise AssertionError("the shipped pred is not the documented affine map of rank_score")
    rebuilt_released = make_prediction_param(panel, aux_values, RELEASED["mode"], RELEASED["weight"],
                                             RELEASED["alpha"], RELEASED["bonus"],
                                             RELEASED["restore_lower"],
                                             RELEASED["top_current_weight"])
    if not np.array_equal(rebuilt_released, shipped_rank):
        raise AssertionError("the parameterized stack does not reproduce the shipped rank_score "
                             f"(max diff {np.abs(rebuilt_released - shipped_rank).max():.3e})")
    checks["proof_pipeline_identity"] = {
        "rebuilt_rank_score_equals_shipped": True,
        "pred_is_affine_map_of_rank_score": True,
        "labels_set_to_null_before_rebuild": True,
        "sentinel_rows": int((shipped_rank == -10.0).sum()),
    }
    log("proof 1 passed: the parameterized stack reproduces the shipped rank_score element-for-element "
        "from pred_raw with null labels")

    orderer = make_prediction_param(panel, aux_values, setting["mode"], setting["weight"],
                                    setting["alpha"], setting["bonus"], setting["restore_lower"],
                                    setting["top_current_weight"])
    if not np.isfinite(orderer).all():
        raise AssertionError("ordering donor has non-finite values")
    log(f"ordering donor rebuilt at alpha={args.alpha} bonus={args.bonus}")

    # ---- membership donor, keyed, aligned to the ordering donor's own row order
    topk = pl.read_parquet(TOPK_TEST)
    if not topk.select(KEYS).equals(prediction.select(KEYS)):
        topk = prediction.select(KEYS).join(topk.select(KEYS + ["pred"]), on=KEYS, how="left")
        if topk["pred"].null_count():
            raise AssertionError("membership donor join lost rows")
    member = topk["pred"].to_numpy().astype(np.float64)
    checks["membership_donor"] = {"file": TOPK_TEST.name, "sha256": sha(TOPK_TEST),
                                  "rows": len(member), "keys_match_ordering_donor": True}

    dates = prediction["trade_date"].to_numpy()
    flags = prediction["flag_limit_up"].to_numpy().astype(np.int64)
    codes, uniques = pd.factorize(prediction["ts_code"].to_pandas(), sort=True)
    codes = codes.astype(np.int64)
    checks["panel"] = {"rows": len(prediction), "days": int(prediction["trade_date"].n_unique()),
                      "date_range": [int(prediction["trade_date"].min()),
                                     int(prediction["trade_date"].max())],
                      "codes": int(len(uniques))}

    # ---- fold-frame identity arrays, needed to prove the tie-break is inert where it was selected
    fold_frame_pl = cs.combined_frame()
    dates_fold = fold_frame_pl["trade_date"].to_numpy()
    flags_fold = fold_frame_pl["flag_limit_up"].to_numpy().astype(np.int64)
    codes_fold, uniques_fold = pd.factorize(fold_frame_pl["ts_code"].to_pandas(), sort=True)
    codes_fold = codes_fold.astype(np.int64)
    n_codes_fold = len(uniques_fold)
    if n_codes_fold != len(uniques):
        raise AssertionError(f"fold and test panels have different code counts "
                             f"({n_codes_fold} vs {len(uniques)}); the tie key would not be comparable")

    # ---- deterministic tie-break. With alpha = 0 the orderer has fewer distinct values than the
    # smoothed release, and on 3 of 344 test days two eligible rows tie exactly across the promotion
    # boundary, which would leave the realized Top decile to the evaluator's non-stable sort. Breaking
    # those ties with a causal, label-free key (the stock's own code rank, scaled far below any real
    # score gap) makes the artifact deterministic. It is verified inert on the fold data below.
    tie_eps = 1e-9
    tie_key = 1.0 - codes / max(len(uniques) - 1, 1)
    orderer_tb = orderer + tie_eps * tie_key
    checks["tie_break"] = {"eps": tie_eps, "key": "1 - ts_code_rank/(n_codes-1), causal and label-free",
                           "reason": "3 of 344 test days had an exact tie across the promotion "
                                     "boundary in the orderer's values"}

    # ---- proof 2a: the same tie-break must leave the FOLD score unchanged, otherwise the selected
    # score was not measuring the scheme that will be shipped
    fold_member = np.load(HERE / "connected_pred_topk.npy")
    orderer_stem = f"pp_a{args.alpha:g}_b{args.bonus:g}_top_only_w0.25_rl1_tcw1.npy"
    if not (HERE / orderer_stem).exists():
        raise SystemExit(f"no saved fold column for the selected orderer: {orderer_stem}")
    fold_orderer = np.load(HERE / orderer_stem)
    fold_pred_tb, fold_stats_tb = build(
        fold_member, fold_orderer + tie_eps * (1.0 - codes_fold / max(n_codes_fold - 1, 1)),
        dates_fold, flags_fold, codes_fold, n_codes_fold, args.m_frac)
    fold_metrics_tb, _ = score_official(cs.combined_frame(), fold_pred_tb)
    diff_tb = abs(fold_metrics_tb["final_score"] - args.expected_connected)
    checks["proof_tie_break_inert_on_folds"] = {
        "with_tie_break": fold_metrics_tb["final_score"],
        "expected": args.expected_connected, "abs_diff": diff_tb,
        "fold_boundary_tie_days": fold_stats_tb["boundary_tie_days"],
        "inert": bool(diff_tb <= 1e-9)}
    if diff_tb > 1e-9:
        raise AssertionError(f"the tie-break changes the fold score by {diff_tb:.3e}, so the selected "
                             f"scheme and the shipped scheme would differ")
    log(f"proof 2a passed: the tie-break is inert on the folds (score unchanged to {diff_tb:.1e}, "
        f"fold boundary ties {fold_stats_tb['boundary_tie_days']})")

    # ---- the exact swap-budget solve validated on the folds, cold-started on the first test day
    if args.member_mode == "nested":
        raise SystemExit(
            "the nested variant is not built here on purpose. Its fold score (0.440997) was produced "
            "with an inner member built by wave 1's LIFT construction, while this builder uses wave "
            "7b's slot-reassignment construction; the two differ by ~0.0006 on the folds, so shipping "
            "a slot-reassigned inner member would not be the scheme that was scored. Its margin over "
            "the simple variant is +0.000847, which is below this project's 0.001743 refit noise "
            "floor. Reproduce the lift construction explicitly before shipping it.")
    hybrid, stats = build(member, orderer_tb, dates, flags, codes, len(uniques), args.m_frac)
    checks["construction"] = stats
    if stats["boundary_tie_days"]:
        raise AssertionError(f"{stats['boundary_tie_days']} days have a promotion-boundary tie")
    log(f"hybrid built: {stats['days']} days, mean retention {stats['mean_retention_ratio']:.6f}, "
        f"boundary ties {stats['boundary_tie_days']}")

    # ---- proof 2: the fold array for this exact scheme must carry the recorded selection score
    fold_pred = np.load(HERE / args.fold_array)
    fold_frame = cs.combined_frame()
    if len(fold_pred) != len(fold_frame):
        raise AssertionError("fold array does not match the combined fold frame")
    fold_metrics, _ = score_official(fold_frame, fold_pred)
    diff = abs(fold_metrics["final_score"] - args.expected_connected)
    if diff > 1e-9:
        raise AssertionError(f"fold array scores {fold_metrics['final_score']!r}, expected "
                             f"{args.expected_connected!r} (diff {diff:.3e})")
    checks["proof_fold_score"] = {"array": args.fold_array,
                                  "recomputed_connected": fold_metrics["final_score"],
                                  "expected": args.expected_connected, "abs_diff": diff,
                                  "passed": True}
    log(f"proof 2 passed: the fold array reproduces the recorded selection score "
        f"{args.expected_connected:.9f} (diff {diff:.1e})")

    # ---- rule 5: fit the return map on the training folds only, then apply
    fold_pct = daily_percentile(fold_frame.to_pandas(), fold_pred)
    mapping = fit_mapping(fold_pct, fold_frame.to_pandas()["y_ret_1d"].to_numpy(dtype=np.float64))
    test_pct = daily_percentile(pd.DataFrame({"trade_date": dates}), hybrid)
    pred = apply_mapping(mapping, test_pct)
    rank_before = pd.Series(hybrid).groupby(dates, sort=False).rank(method="average").to_numpy()
    rank_after = pd.Series(pred).groupby(dates, sort=False).rank(method="average").to_numpy()
    if not np.array_equal(rank_before, rank_after):
        raise AssertionError("proof 3 failed: the return mapping changed the within-day ranking")
    checks["proof_mapping_rank_neutral"] = True
    checks["return_mapping"] = {"fitted_on": "2020-2024 folds of this same scheme",
                                "n_obs": mapping["n_obs"], "bins": mapping["bins"],
                                "eps": mapping["eps"], "range": mapping["range"],
                                "E_r_at_percentile": {p: float(np.interp(p, mapping["centers"],
                                                                        mapping["fitted"]))
                                                      for p in (0.5, 0.9, 0.99, 1.0)},
                                "no_test_period_label_read": True}
    log(f"proof 3 passed: mapping fitted on {mapping['n_obs']:,} training rows, ranks unchanged")

    # ---- write in 测试集_X order. NOTE: this frame's row_id is its own date-major index, not the
    # test-X bridge (backbone_raw.parquet uses row_id the other way), so the order is established by an
    # explicit key join rather than by sorting on row_id.
    x_order = (pl.read_csv(TEST_X, schema_overrides={"ts_code": pl.String, "trade_date": pl.Int32})
               .select(KEYS).with_row_index("test_pos"))
    submission = (prediction.with_columns(pl.Series("pred", pred))
                  .select(KEYS + ["pred"])
                  .join(x_order, on=KEYS, how="inner", validate="1:1")
                  .sort("test_pos")
                  .select(["ts_code", "trade_date", "pred"]))
    if len(submission) != len(x_order):
        raise AssertionError(f"join lost rows: {len(submission)} of {len(x_order)}")
    if not submission.select(KEYS).equals(x_order.select(KEYS)):
        raise AssertionError("submission key order is not identical to 测试集_X.csv")
    out_dir = HERE / "final_submission"
    out_dir.mkdir(parents=True, exist_ok=True)
    target = out_dir / f"{args.out_name}.csv"
    if target.exists():
        raise FileExistsError(f"refusing to overwrite {target}")
    submission.write_csv(target, float_precision=12)

    reread = pd.read_csv(target)
    xk = pd.read_csv(TEST_X, usecols=KEYS)
    s = {"path": str(target), "sha256": sha(target), "bytes": target.stat().st_size,
         "rows": int(len(reread)), "columns": list(reread.columns),
         "columns_exact": list(reread.columns) == ["ts_code", "trade_date", "pred"],
         "nulls": int(reread.isna().sum().sum()),
         "duplicate_keys": int(reread.duplicated(KEYS).sum()),
         "key_order_identical_to_test_x": bool((reread[KEYS].to_numpy() == xk.to_numpy()).all()),
         "pred_all_finite": bool(np.isfinite(reread["pred"].to_numpy()).all()),
         "pred_range": [float(reread["pred"].min()), float(reread["pred"].max())],
         "pred_mean": float(reread["pred"].mean()), "pred_std": float(reread["pred"].std()),
         "date_range": [int(reread.trade_date.min()), int(reread.trade_date.max())]}
    checks["submission"] = s
    for key, want in (("rows", 1599600), ("nulls", 0), ("duplicate_keys", 0)):
        if s[key] != want:
            raise AssertionError(f"{key} = {s[key]}, expected {want}")
    for key in ("columns_exact", "key_order_identical_to_test_x", "pred_all_finite"):
        if not s[key]:
            raise AssertionError(f"submission check failed: {key}")
    if s["date_range"] != [20250102, 20260608]:
        raise AssertionError(f"unexpected date range {s['date_range']}")
    log(f"submission written: {s['rows']:,} rows, sha {s['sha256'][:16]}…, pred "
        f"[{s['pred_range'][0]:.6f}, {s['pred_range'][1]:.6f}] mean {s['pred_mean']:.6f} "
        f"sd {s['pred_std']:.6f}")

    # ---- §5(b) retrospective test-period score, computed AFTER the file was written
    mask = (prediction["trade_date"] <= CUTOFF).to_numpy()
    labels = pl.from_pandas(pd.read_csv(HOLDOUT / "测试集_Y.csv"))
    scoring = (prediction.filter(pl.Series(mask)).select(KEYS + ["flag_limit_up"])
               .join(labels.select(KEYS + ["y_ret_1d"]), on=KEYS, how="left"))
    metrics, daily = score_official(scoring, pred[mask])
    daily_pd = daily.to_pandas()
    checks["test_period_retrospective"] = {
        "note": "computed after the submission was written; reported per §5(b), never used to select",
        "days": int(len(daily_pd)), "metrics": metrics,
        "segments": {"2025": composite(daily_pd[daily_pd.trade_date < 20260101]),
                     "2026": composite(daily_pd[daily_pd.trade_date >= 20260101])},
    }
    log(f"RETROSPECTIVE test-period score (343 of 344 days): {metrics['final_score']:.9f} "
        f"(ic {metrics['ic_mean']:.6f}, excess {metrics['annual_excess']:.6f}, "
        f"turnover {metrics['mean_turnover']:.6f})")

    record = {"status": "complete", "built_at_local": time.strftime("%Y-%m-%dT%H:%M:%S"),
              "scheme": {
                  "membership_donor": "topk_return_backbone @ released post-processing (alpha 0.9, "
                                      "bonus 0.3, top_only auxiliary 0.25)",
                  "ordering_donor": f"peer67_slow16 backbone @ alpha {args.alpha}, bonus {args.bonus}, "
                                    "top_only auxiliary 0.25",
                  "top_set_rule": f"exact swap-budget retention floor m = round({args.m_frac} * n_top) "
                                  "against the previous day's realized Top decile; cold start on the "
                                  "first test day",
                  "output": "isotonic percentile->return map fitted on the 2020-2024 folds"},
              "proofs_passed": ["pipeline identity and label independence",
                                "fold array reproduces the recorded selection score",
                                "return mapping is rank-neutral"],
              "checks": checks}
    (out_dir / f"{args.out_name}_build_record.json").write_text(
        json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    np.save(out_dir / f"{args.out_name}_pred.npy", pred)
    log(f"build record: {out_dir / (args.out_name + '_build_record.json')}")


if __name__ == "__main__":
    main()
