"""Build the test-period submission for the wave-12/13 selected scheme: W5a as the ordering donor.

Scheme: Top-decile MEMBERSHIP from the topk return-weighted pairwise backbone at its released
post-processing; ORDERING from the five-way GRU ensemble W5a re-post-processed at alpha 0 / bonus 0;
an exact swap-budget retention floor m against the previous day's realized Top decile; the wave-11
deterministic tie-break; and finally the isotonic percentile->return map fitted on the 2020-2024 folds
of this same scheme, so `pred` is a return forecast rather than a rescaled rank (后续选模标准.md §5).

Why this file exists separately from build_selected_submission.py: that builder rebuilds its ordering
donor from the peer67_slow16 delivery's own pred_raw, which cannot express W5a. W5a's test-period raw
was deleted from the archive by the 20261001 cleanup and is reconstructed by reconstruct_w5a_test.py,
which proves the reconstruction by pushing it through the released stack and requiring element-for-
element equality with all_models_test_20260929 row 138. This builder consumes that proven raw.

Nothing here is retrained. Four proofs run before the file is written:
  1. make_prediction_param at the RELEASED settings, applied to the reconstructed W5a raw, must
     reproduce row 138's saved array element-for-element. This proves the parameterized stack used for
     the alpha 0 / bonus 0 orderer is the same production pipeline that produced the frozen W5a column,
     and that it reads no labels.
  2. the W5a raw must be row-aligned with the delivery frame that supplies flags, dates and the key
     order, so the two frames cannot silently disagree.
  3. the selected scheme's connected fold array must reproduce the recorded selection score.
  4. the return mapping must leave every within-day rank untouched, so the official score is unchanged.

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
ARCHIVE = ROOT.parent / "赛题五_历史归档_20261001"
EARLY = ARCHIVE / "analysis/all_models_test_20260929/early"
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(ARCHIVE))
sys.path.insert(0, str(EARLY))
import connected_scorer as cs  # noqa: E402
from src.scoring import Panel  # noqa: E402
from experiments.revalidate_fold_local import score_official  # noqa: E402
from optimize_wave6 import make_prediction_param  # noqa: E402
from optimize_wave7b import build  # noqa: E402
from return_mapping import daily_percentile, fit_mapping, apply_mapping  # noqa: E402
from analysis.official_score_contributions import composite  # noqa: E402

ALLMODELS = ARCHIVE / "analysis/all_models_test_20260929"
TOPK_TEST = ALLMODELS / "middle/predictions/supplemental_topk_fulltrain2024.parquet"
ROW138 = EARLY / "predictions/early_9ec487b9f99e6f94.npy"
DELIVERY = ARCHIVE / "deliveries/peer67_slow16_20260929"
AUX = ARCHIVE / "releases/pooled_rms25/auxiliary_raw.parquet"
W5A_RAW = HERE / "w5a_test/w5a_raw_test.npy"
W5A_PROOF = HERE / "w5a_test/reconstruction_proof.json"
NESTED_TEST = HERE / "nested_donor/nested_donor_test.npy"
NESTED_PROOF = HERE / "nested_donor/reconstruction_proof.json"
TEST_X = ROOT / "data/raw/测试集_X.csv"
KEYS = ["ts_code", "trade_date"]
CUTOFF = 20260605
RELEASED = {"alpha": 0.9, "bonus": 0.3, "restore_lower": True, "top_current_weight": 1.0,
            "mode": "top_only", "weight": 0.25}
TIE_EPS = 1e-9


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
    parser.add_argument("--alpha", type=float, default=0.0)
    parser.add_argument("--bonus", type=float, default=0.0)
    parser.add_argument("--m-frac", type=float, default=0.985)
    parser.add_argument("--fold-array", required=True,
                        help="the connected fold column for this exact scheme, filename under this dir")
    parser.add_argument("--expected-connected", type=float, required=True)
    parser.add_argument("--out-name", required=True)
    parser.add_argument("--member-mode", choices=("topk", "nested"), default="nested",
                        help="nested = wave 1's lift donor (wave 13 stage-2 argmax); "
                             "topk = the plain topk finished column")
    parser.add_argument("--orderer-partner-weight", type=float, default=0.0,
                        help="wave 16/20: blend the orderer with slow16@alpha0/bonus0 at this weight. "
                             "0 keeps W5a alone, which is what waves 12-13 selected")
    args = parser.parse_args()
    if not 0.0 <= args.orderer_partner_weight < 1.0:
        raise SystemExit("--orderer-partner-weight must be in [0, 1)")

    setting = {**RELEASED, "alpha": args.alpha, "bonus": args.bonus}
    checks: dict = {"scheme": {"membership_donor": (
                                    "nested: wave 1's lift of peer67_slow16 finished over topk's Top "
                                    "decile" if args.member_mode == "nested"
                                    else "topk return-weighted pairwise backbone @ released "
                                         "post-processing"),
                               "ordering_donor": f"W5a five-way GRU ensemble @ alpha {args.alpha}, "
                                                 f"bonus {args.bonus}, top_only auxiliary 0.25",
                               "orderer_postprocess": setting, "m_frac": args.m_frac,
                               "tie_break_eps": TIE_EPS},
                    "started_at_local": time.strftime("%Y-%m-%dT%H:%M:%S")}

    if not W5A_PROOF.exists():
        raise SystemExit("run reconstruct_w5a_test.py first; the W5a raw is not proven")
    proof = json.loads(W5A_PROOF.read_text(encoding="utf-8"))
    if proof.get("status") != "proven" or not proof.get("bit_identical"):
        raise SystemExit(f"the W5a reconstruction proof did not pass: {proof.get('status')}")
    checks["w5a_reconstruction_proof"] = {"file": W5A_PROOF.name, "bit_identical": True,
                                          "raw_sha256": proof["raw_output"]["sha256"],
                                          "gru_raw_sha256": proof["gru_raw_restored"]["sha256"]}

    # ---- frames
    prediction = pl.read_parquet(DELIVERY / "prediction.parquet")
    aux = pl.read_parquet(AUX)
    if not aux.select(KEYS).equals(prediction.select(KEYS)):
        raise AssertionError("auxiliary_raw and the delivery prediction frame are not row-aligned")
    raw_w5a = np.load(W5A_RAW).astype(np.float64)
    if len(raw_w5a) != len(prediction):
        raise AssertionError(f"W5a raw has {len(raw_w5a)} rows, delivery frame has {len(prediction)}")

    # ---- proof 2: the W5a raw must be row-aligned with the delivery frame. reconstruct_w5a_test.py
    # built it in load_panel() order, which is backbone_raw sorted by (trade_date, ts_code); this
    # re-derives that order independently and compares keys, not lengths.
    runner_frame = (pl.read_parquet(ARCHIVE / "releases/pooled_rms25/backbone_raw.parquet")
                    .sort("trade_date", "ts_code").select(KEYS))
    if not runner_frame.equals(prediction.select(KEYS)):
        raise AssertionError("proof 2 failed: the W5a raw's row order does not match the delivery frame")
    checks["proof_row_alignment"] = {"w5a_raw_rows": int(len(raw_w5a)),
                                     "keys_equal_delivery_frame": True,
                                     "keys_equal_sorted_backbone_raw": True}
    log("proof 2 passed: the W5a raw is row-aligned with the delivery frame")

    frame = (prediction
             .with_columns(pl.Series("pred_raw", raw_w5a))
             .with_columns(aux["pred_raw"].cast(pl.Float64).alias("aux_raw"))
             .with_columns(pl.col("flag_limit_up").cast(pl.Int64))
             .with_columns(pl.lit(None, dtype=pl.Float64).alias("y_ret_1d")))
    panel = Panel.from_frame(frame)
    aux_values = frame["aux_raw"].to_numpy().astype(np.float64)

    # ---- proof 1: the parameterized stack at the RELEASED settings must reproduce row 138
    target = np.load(ROW138).astype(np.float64)
    rebuilt_released = make_prediction_param(panel, aux_values, RELEASED["mode"], RELEASED["weight"],
                                             RELEASED["alpha"], RELEASED["bonus"],
                                             RELEASED["restore_lower"], RELEASED["top_current_weight"])
    if not np.array_equal(rebuilt_released, target):
        raise AssertionError("proof 1 failed: make_prediction_param at the released settings does not "
                             f"reproduce row 138 (max diff "
                             f"{np.abs(rebuilt_released - target).max():.3e})")
    checks["proof_pipeline_identity"] = {
        "released_settings_reproduce_row138": True,
        "row138_path": str(ROW138), "row138_sha256": sha(ROW138),
        "labels_set_to_null_before_rebuild": True,
        "sentinel_rows": int((rebuilt_released == -10.0).sum()),
    }
    log("proof 1 passed: make_prediction_param reproduces the frozen W5a released column "
        "element-for-element from the reconstructed raw, with null labels")

    orderer = make_prediction_param(panel, aux_values, setting["mode"], setting["weight"],
                                    setting["alpha"], setting["bonus"], setting["restore_lower"],
                                    setting["top_current_weight"])
    if not np.isfinite(orderer).all():
        raise AssertionError("ordering donor has non-finite values")
    log(f"ordering donor rebuilt at alpha={args.alpha} bonus={args.bonus}")

    # ---- proof 1b + the wave 16/20 orderer blend. slow16@alpha0/bonus0 is rebuilt from the
    # delivery's OWN pred_raw, and the same code path at the RELEASED settings must reproduce the
    # delivery's shipped rank_score - that is what makes the blend partner's test column proven
    # rather than assumed. orderer_a0b0_raw_deployed67_slow__wave23 was checked bit-identical to
    # pp_a0_b0_top_only_w0.25_rl1_tcw1 on the folds, so this is the same partner wave 16 blended with.
    if args.orderer_partner_weight > 0.0:
        from optimize_wave15 import daily_ranks, weighted_rank_blend
        slow16_frame = (prediction
                        .with_columns(aux["pred_raw"].cast(pl.Float64).alias("aux_raw"))
                        .with_columns(pl.col("flag_limit_up").cast(pl.Int64))
                        .with_columns(pl.lit(None, dtype=pl.Float64).alias("y_ret_1d")))
        slow16_panel = Panel.from_frame(slow16_frame)
        shipped_rank = prediction["rank_score"].to_numpy().astype(np.float64)
        slow16_released = make_prediction_param(
            slow16_panel, aux_values, RELEASED["mode"], RELEASED["weight"], RELEASED["alpha"],
            RELEASED["bonus"], RELEASED["restore_lower"], RELEASED["top_current_weight"])
        if not np.array_equal(slow16_released, shipped_rank):
            raise AssertionError("proof 1b failed: rebuilding slow16 at the released settings does "
                                 "not reproduce the delivery's shipped rank_score (max diff "
                                 f"{np.abs(slow16_released - shipped_rank).max():.3e})")
        slow16_orderer = make_prediction_param(
            slow16_panel, aux_values, setting["mode"], setting["weight"], setting["alpha"],
            setting["bonus"], setting["restore_lower"], setting["top_current_weight"])
        checks["proof_slow16_pipeline_identity"] = {
            "released_settings_reproduce_shipped_rank_score": True,
            "sentinel_rows": int((shipped_rank == -10.0).sum()),
            "labels_set_to_null_before_rebuild": True}
        log("proof 1b passed: slow16 at the released settings reproduces the delivery's shipped "
            "rank_score element-for-element")

        valid = prediction["price_valid"].to_numpy().astype(bool)
        dates_np = prediction["trade_date"].to_numpy()
        # the tie-break is applied here AND again where orderer_tb is built, because that is literally
        # what optimize_wave20.blend() + score() do on the folds; mirroring the expression keeps the
        # shipped column the same construction as the scored one rather than a merely order-equivalent
        # one. tie_key is recomputed here because the builder derives it later, and equality with the
        # later array is asserted there.
        codes_blend, uniques_blend = pd.factorize(prediction["ts_code"].to_pandas(), sort=True)
        tie_key_blend = 1.0 - codes_blend.astype(np.int64) / max(len(uniques_blend) - 1, 1)
        w = args.orderer_partner_weight
        cache: dict = {}
        blended = weighted_rank_blend([orderer, slow16_orderer], [1.0 - w, w], cache, valid,
                                      dates_np, ("w5a", "slow16"))
        blended = np.where(blended > -9.0, blended + TIE_EPS * tie_key_blend, blended)
        checks["orderer_blend"] = {
            "components": ["W5a @ the selected (alpha, bonus)", "slow16 @ the selected (alpha, bonus)"],
            "weights": [1.0 - w, w],
            "rule": "per-day cross-sectional average rank over the price-valid, non-sentinel subset, "
                    "weighted, then divided by the day's count - the same daily_ranks and "
                    "weighted_rank_blend used on the folds",
            "tie_break_applied_twice": "once here and once in orderer_tb, mirroring optimize_wave20",
            "sentinel_rows": int((blended <= -9.0).sum()),
        }
        orderer = blended
        log(f"orderer blended with slow16 at weight {w}; {checks['orderer_blend']['sentinel_rows']:,} "
            f"sentinel rows")

    # ---- membership donor
    parser_member = args.member_mode
    if parser_member == "nested":
        if not NESTED_PROOF.exists():
            raise SystemExit("run reconstruct_nested_donor.py first; the nested donor is not proven")
        nested_proof = json.loads(NESTED_PROOF.read_text(encoding="utf-8"))
        if not nested_proof.get("fold_proof", {}).get("rebuilt_equals_connected_pred_hybrid"):
            raise SystemExit("the nested donor's fold proof is not bit-exact; refusing to ship it")
        member = np.load(NESTED_TEST).astype(np.float64)
        if len(member) != len(prediction):
            raise AssertionError(f"nested donor has {len(member)} rows, frame has {len(prediction)}")
        checks["membership_donor"] = {
            "mode": "nested", "file": NESTED_TEST.name, "sha256": sha(NESTED_TEST),
            "rows": len(member),
            "construction": nested_proof["construction"],
            "fold_proof_bit_exact": True,
            "fold_proof_max_abs_diff": nested_proof["fold_proof"]["max_abs_diff"],
            "test_stats": nested_proof["test_stats"],
            "inputs": nested_proof["test_inputs"],
        }
        fold_member_stem = "connected_pred_hybrid.npy"
    else:
        topk = pl.read_parquet(TOPK_TEST)
        if not topk.select(KEYS).equals(prediction.select(KEYS)):
            topk = prediction.select(KEYS).join(topk.select(KEYS + ["pred"]), on=KEYS, how="left")
            if topk["pred"].null_count():
                raise AssertionError("membership donor join lost rows")
        member = topk["pred"].to_numpy().astype(np.float64)
        checks["membership_donor"] = {"mode": "topk", "file": TOPK_TEST.name, "sha256": sha(TOPK_TEST),
                                      "rows": len(member), "keys_match_ordering_donor": True}
        fold_member_stem = "connected_pred_topk.npy"
    log(f"membership donor: {parser_member}, {len(member):,} rows")

    dates = prediction["trade_date"].to_numpy()
    flags = prediction["flag_limit_up"].to_numpy().astype(np.int64)
    codes, uniques = pd.factorize(prediction["ts_code"].to_pandas(), sort=True)
    codes = codes.astype(np.int64)
    checks["panel"] = {"rows": len(prediction), "days": int(prediction["trade_date"].n_unique()),
                      "date_range": [int(prediction["trade_date"].min()),
                                     int(prediction["trade_date"].max())],
                      "codes": int(len(uniques))}

    # ---- fold-frame arrays, needed to show whether the tie-break moves the score it was selected on
    fold_frame_pl = cs.combined_frame()
    dates_fold = fold_frame_pl["trade_date"].to_numpy()
    flags_fold = fold_frame_pl["flag_limit_up"].to_numpy().astype(np.int64)
    codes_fold, uniques_fold = pd.factorize(fold_frame_pl["ts_code"].to_pandas(), sort=True)
    codes_fold = codes_fold.astype(np.int64)
    fold_member = np.load(HERE / fold_member_stem)
    if len(fold_member) != len(fold_frame_pl):
        raise AssertionError("fold donor column does not match the combined fold frame")
    tie_key = 1.0 - codes / max(len(uniques) - 1, 1)
    tie_key_fold = 1.0 - codes_fold / max(len(uniques_fold) - 1, 1)
    if args.orderer_partner_weight > 0.0:
        if not np.array_equal(tie_key_blend, tie_key):
            raise AssertionError("the tie key recomputed for the blend differs from the builder's")
        checks["orderer_blend"]["tie_key_matches_builder"] = True
        # rebuild the fold-side blend the same way, so the tie-break diagnostic below is measured on
        # the column that was actually selected rather than on W5a alone
        from optimize_wave15 import daily_ranks as fold_daily_ranks
        from optimize_wave15 import weighted_rank_blend as fold_blend
        fold_valid = fold_frame_pl["price_valid"].to_numpy().astype(bool)
        fold_w5a = np.load(HERE / "orderer_a0b0_W5a_five_way_with_gru__final_sweep_eval.npy")
        fold_slow16 = np.load(HERE / "pp_a0_b0_top_only_w0.25_rl1_tcw1.npy")
        fold_orderer = fold_blend([fold_w5a, fold_slow16],
                                  [1.0 - args.orderer_partner_weight, args.orderer_partner_weight],
                                  {}, fold_valid, dates_fold, ("w5a", "slow16"))
        fold_orderer = np.where(fold_orderer > -9.0,
                                fold_orderer + TIE_EPS * tie_key_fold, fold_orderer)
    else:
        fold_orderer = np.load(HERE / "orderer_a0b0_W5a_five_way_with_gru__final_sweep_eval.npy")
    orderer_tb = orderer + TIE_EPS * tie_key

    fold_plain, fold_stats_plain = build(fold_member, fold_orderer, dates_fold, flags_fold,
                                         codes_fold, len(uniques_fold), args.m_frac)
    fold_tb, fold_stats_tb = build(fold_member, fold_orderer + TIE_EPS * tie_key_fold, dates_fold,
                                   flags_fold, codes_fold, len(uniques_fold), args.m_frac)
    m_plain, _ = score_official(fold_frame_pl, fold_plain)
    m_tb, _ = score_official(fold_frame_pl, fold_tb)
    diff_tb = abs(m_tb["final_score"] - m_plain["final_score"])
    checks["tie_break_on_folds"] = {
        "without": m_plain["final_score"], "with": m_tb["final_score"], "abs_diff": diff_tb,
        "fold_boundary_tie_days_without": fold_stats_plain["boundary_tie_days"],
        "fold_boundary_tie_days_with": fold_stats_tb["boundary_tie_days"],
        "note": "reported, not gated: the tie-break is a determinism device for the shipped file, and "
                "the selection score recorded for this scheme already includes it",
    }
    log(f"tie-break on the folds: {m_plain['final_score']:.9f} -> {m_tb['final_score']:.9f} "
        f"(diff {diff_tb:.3e}, boundary ties {fold_stats_tb['boundary_tie_days']})")

    # ---- the exact swap-budget solve validated on the folds, cold-started on the first test day
    hybrid, stats = build(member, orderer_tb, dates, flags, codes, len(uniques), args.m_frac)
    checks["construction"] = stats
    if stats["boundary_tie_days"]:
        raise AssertionError(f"{stats['boundary_tie_days']} days have a promotion-boundary tie")
    log(f"hybrid built: {stats['days']} days, mean retention {stats['mean_retention_ratio']:.6f}, "
        f"swaps {stats['swaps']}, eligibility-limited days {stats['eligibility_limited_days']}, "
        f"boundary ties {stats['boundary_tie_days']}")

    # ---- proof 3: the fold array for this exact scheme must carry the recorded selection score
    fold_pred = np.load(HERE / args.fold_array)
    if len(fold_pred) != len(fold_frame_pl):
        raise AssertionError("fold array does not match the combined fold frame")
    fold_metrics, _ = score_official(fold_frame_pl, fold_pred)
    diff = abs(fold_metrics["final_score"] - args.expected_connected)
    if diff > 1e-9:
        raise AssertionError(f"fold array scores {fold_metrics['final_score']!r}, expected "
                             f"{args.expected_connected!r} (diff {diff:.3e})")
    checks["proof_fold_score"] = {"array": args.fold_array,
                                  "recomputed_connected": fold_metrics["final_score"],
                                  "expected": args.expected_connected, "abs_diff": diff,
                                  "passed": True}
    log(f"proof 3 passed: the fold array reproduces the recorded selection score "
        f"{args.expected_connected:.9f} (diff {diff:.1e})")

    # ---- rule 5: fit the return map on the training folds only, then apply
    fold_pdf = fold_frame_pl.to_pandas()
    mapping = fit_mapping(daily_percentile(fold_pdf, fold_pred),
                          fold_pdf["y_ret_1d"].to_numpy(dtype=np.float64))
    test_pct = daily_percentile(pd.DataFrame({"trade_date": dates}), hybrid)
    pred = apply_mapping(mapping, test_pct)
    rank_before = pd.Series(hybrid).groupby(dates, sort=False).rank(method="average").to_numpy()
    rank_after = pd.Series(pred).groupby(dates, sort=False).rank(method="average").to_numpy()
    if not np.array_equal(rank_before, rank_after):
        raise AssertionError("proof 4 failed: the return mapping changed the within-day ranking")
    checks["proof_mapping_rank_neutral"] = True
    checks["return_mapping"] = {"fitted_on": "2020-2024 folds of this same scheme",
                                "n_obs": mapping["n_obs"], "bins": mapping["bins"],
                                "eps": mapping["eps"], "range": mapping["range"],
                                "E_r_at_percentile": {p: float(np.interp(p, mapping["centers"],
                                                                        mapping["fitted"]))
                                                      for p in (0.5, 0.9, 0.99, 1.0)},
                                "no_test_period_label_read": True}
    log(f"proof 4 passed: mapping fitted on {mapping['n_obs']:,} training rows, ranks unchanged")

    # ---- write in 测试集_X order, established by an explicit key join (this frame's row_id is its own
    # date-major index, not the test-X bridge)
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
    target_path = out_dir / f"{args.out_name}.csv"
    if target_path.exists():
        raise FileExistsError(f"refusing to overwrite {target_path}")
    # float_precision MUST be 17, not 12. apply_mapping returns iso.predict(p) + EPS*p with EPS = 1e-9,
    # and the isotonic part is a 2000-bin step function, so strict monotonicity lives entirely in the
    # eps term. Adjacent percentiles within a day are EPS/4650 ~ 2.2e-13 apart, which 12 decimals
    # rounds away: a first build at float_precision=12 collapsed 1,599,600 predictions into 1,295
    # distinct values, put ties across every Top-decile boundary, and scored 0.414836 under the official
    # evaluate.py against 0.416955 for the in-memory array it was built from. The project's own delivery
    # writes 17 significant digits for the same reason.
    submission.write_csv(target_path, float_precision=17)

    reread = pd.read_csv(target_path)
    xk = pd.read_csv(TEST_X, usecols=KEYS)
    # 4650 distinct values is the CORRECT count, not a tie collapse: apply_mapping returns
    # iso.predict(p) + EPS*p and p is the within-day percentile, which takes exactly one value per row
    # position, and every day has the same 4650 rows. The first build at float_precision=12 collapsed
    # even those 4650 into 1,295, which is what tied the Top-decile boundaries.
    distinct_written = int(reread["pred"].nunique())
    distinct_memory = int(len(np.unique(pred)))
    if distinct_written != distinct_memory:
        raise AssertionError(f"the CSV lost ordering resolution: {distinct_written:,} distinct pred "
                             f"values written against {distinct_memory:,} in memory, so the float "
                             "precision is too low and Top-decile boundaries would tie")
    # reread is in 测试集_X order while `pred` is in the delivery frame's order, so compare sorted
    # multisets; the key order itself is asserted separately below
    roundtrip = float(np.abs(np.sort(reread["pred"].to_numpy()) - np.sort(pred)).max())
    if roundtrip > 0.0:
        raise AssertionError(f"the CSV does not round-trip the predictions exactly "
                             f"(max abs diff {roundtrip:.3e}); raise float_precision")
    s = {"path": str(target_path), "sha256": sha(target_path), "bytes": target_path.stat().st_size,
         "rows": int(len(reread)), "columns": list(reread.columns),
         "columns_exact": list(reread.columns) == ["ts_code", "trade_date", "pred"],
         "nulls": int(reread.isna().sum().sum()),
         "duplicate_keys": int(reread.duplicated(KEYS).sum()),
         "key_order_identical_to_test_x": bool((reread[KEYS].to_numpy() == xk.to_numpy()).all()),
         "pred_all_finite": bool(np.isfinite(reread["pred"].to_numpy()).all()),
         "pred_distinct_values": distinct_written,
         "pred_distinct_values_in_memory": distinct_memory,
         "pred_max_roundtrip_error": roundtrip,
         "float_precision": 17,
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
        f"[{s['pred_range'][0]:.6f}, {s['pred_range'][1]:.6f}] mean {s['pred_mean']:.6f}")

    checks["finished_at_local"] = time.strftime("%Y-%m-%dT%H:%M:%S")
    record = out_dir / f"{args.out_name}_checks.json"
    if record.exists():
        raise FileExistsError(f"refusing to overwrite {record}")
    record.write_text(json.dumps(checks, ensure_ascii=False, indent=2, default=str) + "\n",
                      encoding="utf-8")
    log(f"wrote {record}")

    # ---- §5(b) retrospective disclosure only. Computed after the file is written, once the
    # selection is already frozen on the training caliber; it feeds back into nothing.
    # Scored by the UNMODIFIED official evaluate.py on the CSV that was actually written, not by a
    # rebuilt frame over the in-memory array: that is what the grader will run, and a first version of
    # this block reported 0.416955 from the in-memory array while the written file scored 0.414836.
    try:
        holdout = ARCHIVE / "analysis/frozen_holdout_20260928/data"
        sys.path.insert(0, str(ROOT))
        from evaluate import evaluate as official_evaluate
        metrics = official_evaluate(str(target_path), str(holdout))
        retro = {"purpose": "后续选模标准.md §5(b) retrospective disclosure",
                 "may_not_be_used_for_selection": True,
                 "scorer": "the unmodified official evaluate.py, run on the written CSV",
                 "data_dir": str(holdout),
                 "test_period_score": float(metrics["final_score"]),
                 "metrics": {k: float(v) for k, v in metrics.items()}}
        log(f"RETROSPECTIVE test-period composite, official evaluate.py on the written CSV "
            f"(disclosure only, selects nothing): {metrics['final_score']:.9f}  "
            f"ic {metrics['ic_mean']:.6f} excess {metrics['annual_excess']:.6f} "
            f"turnover {metrics['mean_turnover']:.6f}")
        (out_dir / f"{args.out_name}_retrospective.json").write_text(
            json.dumps(retro, ensure_ascii=False, indent=2, default=str) + "\n", encoding="utf-8")
    except BaseException as error:  # noqa: BLE001 - disclosure is optional, never gating
        log(f"retrospective disclosure skipped: {type(error).__name__}: {error}")


if __name__ == "__main__":
    main()
