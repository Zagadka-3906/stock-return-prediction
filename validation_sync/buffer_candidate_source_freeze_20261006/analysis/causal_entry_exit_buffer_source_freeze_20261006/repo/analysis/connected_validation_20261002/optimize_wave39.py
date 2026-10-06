"""Wave 39: the winning objective has only ever run on the 63-feature Alpha158 set. Run it on 83.

Two things are now established separately. The flat-Top-K pairwise objective is the right loss for the
membership donor: wave 37 tested it against lambdarank and rank_xendcg at matched capacity and it won by
6.15e-3 over the best alternative, and the mechanism is visible in the donor's own standalone terms -
flat-Top-K has the LOWER global IC (0.057539 vs lambdarank_graded's 0.092844) and the HIGHER Top-decile
excess (0.349688 vs 0.318659), which is exactly what the donor slot is for.

And the 83-feature extension carries signal: `raw_extended83__wave15_paired_features_20260927` was the
4th best orderer in wave 12's sweep of 27 backbones (0.439797), ahead of most tree families.

Nobody has put those together. Every flat-Top-K model in this project - the shipped donor, wave 24's
five seeds, wave 31's eight fractions, wave 36's two fill-ins - was trained by `r6_topk.training_frame`,
which hard-codes `feature_names()` and asserts `len(features) == 63`.

This wave trains the identical objective, capacity, round count, sample count, return scale and seed on
the 83-feature panel at `experiments/wave9_exploratory_20260927/panel_extended.parquet`, and drops it
into the unchanged downstream construction, so the only thing that moves is the feature set.

Harness proof, and it is the whole reason this wave can be trusted: the SAME code path, restricted to
the 63 base features, must reproduce the frozen predictions_topk_return_backbone_2022.parquet pred_raw
bit-for-bit. run_topk_confirm.py already achieved max|diff| 0.000e+00 on that fold with r6_topk's own
training_frame, so this proves the re-implementation - the different panel source, the derived feature
list, the group construction - is faithful before the 83-feature result is believed.

Deliverability is recorded, not assumed: an 83-feature donor has no test-period prediction. The extended
panel does cover the test period (it is the same file wave 9/15 scored from), so a fulltrain re-fit is
possible, but it is a retrain on a platform that allows one submission and returns no score.

Selection is 后续选模标准.md §3/§4. Both halves are reported for every arm because wave 36 measured this
construction's excess term as rough at the 4.5e-3 level. No test-period data is read here.
"""
from __future__ import annotations

import argparse
import gc
import hashlib
import json
import sys
import time
from pathlib import Path

import numpy as np
import polars as pl

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
ARCHIVE = ROOT.parent / "赛题五_历史归档_20261001"
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(ARCHIVE))

OUT = HERE / "wave39_ext83"
RAW = OUT / "raw"
PANEL = ARCHIVE / "experiments/wave9_exploratory_20260927/panel_extended.parquet"
FROZEN_TOPK_2022 = ROOT / "analysis/topk_training_validation_20261001/predictions_topk_return_backbone_2022.parquet"
LIVE_TRAIN_CSV = ROOT / "data/raw/训练集.csv"
PINNED_PREFIX = "e9d23e87f7e1f943"
META_COLUMNS = ("ts_code", "trade_date", "row_id", "is_train", "y_ret_1d", "y_rank", "price_valid")
KEYS = ["ts_code", "trade_date"]
YEARS = (2020, 2021, 2022, 2023, 2024)
PROOF_YEAR = 2022
SEED = 2026
CURRENT_BEST = 0.44319055217888365
REF_HALF_DEV = 0.442705356
REF_HALF_CONF = 0.443926938
M_FRAC = 0.985
TIE_EPS = 1e-9
PARTNER_WEIGHT = 0.25
W5A_A0B0 = "orderer_a0b0_W5a_five_way_with_gru__final_sweep_eval.npy"
SLOW16_A0B0 = "pp_a0_b0_top_only_w0.25_rl1_tcw1.npy"
SLOW16_FIN = "connected_pred_peer67_slow16.npy"
TOPK_FIN = "connected_pred_topk.npy"


def sha(path) -> str:
    value = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for chunk in iter(lambda: stream.read(8 * 1024 * 1024), b""):
            value.update(chunk)
    return value.hexdigest()


def log(message: str) -> None:
    print(f"[{time.strftime('%H:%M:%S')}] {message}", flush=True)


def training_frame_from(panel: pl.DataFrame, year: int, features: list, cutoff: int,
                        label_source: pl.DataFrame) -> tuple:
    """r6_topk.training_frame, re-pointed at an arbitrary panel and feature list.

    Every filter is copied: is_train, trade_date < cutoff, price_valid, flag_limit_up == 0, a finite
    label joined from the raw CSV (not from the panel's own copy, so the label provenance is the same),
    sorted by (trade_date, ts_code), and days with fewer than 100 rows dropped.
    """
    frame = (panel.filter(pl.col("is_train") & (pl.col("trade_date") < cutoff)
                          & pl.col("price_valid") & (pl.col("flag_limit_up") == 0))
             .select(KEYS + features)
             .join(label_source.select(KEYS + ["y_ret_1d"]), on=KEYS, how="inner", validate="1:1")
             .sort("trade_date", "ts_code"))
    if frame["y_ret_1d"].dtype != pl.Float64:
        raise AssertionError("label dtype is not Float64")
    if frame.select(KEYS).n_unique() != len(frame):
        raise AssertionError("duplicate keys in the training frame")
    counts = frame.group_by("trade_date").len()
    keep = counts.filter(pl.col("len") >= 100)["trade_date"]
    frame = frame.filter(pl.col("trade_date").is_in(keep.implode()))
    if frame["trade_date"].max() >= cutoff:
        raise AssertionError("the training frame crosses its own cutoff")
    meta = {"training_cutoff_exclusive": int(cutoff), "rows": int(len(frame)),
            "days": int(frame["trade_date"].n_unique()),
            "first_date": int(frame["trade_date"].min()), "last_date": int(frame["trade_date"].max()),
            "n_features": len(features)}
    return frame, meta


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("stage", choices=("protocol", "prove", "train", "score"))
    args = parser.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    RAW.mkdir(parents=True, exist_ok=True)

    import lightgbm as lgb
    import experiments.r6_topk as rt
    from run import FEATURE_FILE, feature_names, fold_cutoff, to_matrix
    from experiments.r6_topk import R4, FlatTopKObjective, objective_callback, fixed_prediction

    if not LIVE_TRAIN_CSV.exists():
        raise SystemExit(f"no live training CSV at {LIVE_TRAIN_CSV}")
    digest = sha(LIVE_TRAIN_CSV)
    if not digest.startswith(PINNED_PREFIX):
        raise SystemExit(f"the live 训练集.csv sha256 {digest[:16]}… is not the pinned file")
    rt.RAW_LABELS = LIVE_TRAIN_CSV

    base_features = feature_names()
    schema = list(pl.read_parquet_schema(PANEL))
    ext_features = [c for c in schema if c not in META_COLUMNS]
    log(f"base features {len(base_features)}, extended panel features {len(ext_features)}")
    missing = [f for f in base_features if f not in ext_features]
    if missing:
        raise SystemExit(f"the extended panel lacks {len(missing)} base features, e.g. {missing[:5]}")

    label_source = (pl.scan_csv(LIVE_TRAIN_CSV,
                                schema_overrides={"ts_code": pl.String, "trade_date": pl.Int32,
                                                  "y_ret_1d": pl.Float64},
                                null_values=["NaN", "nan", ""])
                    .select(KEYS + ["y_ret_1d"])
                    .filter(pl.col("y_ret_1d").is_finite()).collect())

    protocol_path = HERE / "protocol_wave39.json"
    if not protocol_path.exists():
        protocol_path.write_text(json.dumps({
            "frozen_at_local": time.strftime("%Y-%m-%dT%H:%M:%S"),
            "standard": "后续选模标准.md §3 connected composite primary; §4 highest score wins",
            "status": "in_sample_selection_disclosed",
            "hypothesis": "the flat-Top-K objective is the right donor loss (wave 37: it beats "
                          "lambdarank and rank_xendcg by 6.15e-3 at matched capacity, with lower global "
                          "IC and higher Top-decile excess, which is the right trade for this slot) and "
                          "the 83-feature extension carries signal (wave 12: extended83 was the 4th best "
                          "of 27 orderers). Every flat-Top-K model so far was trained on 63 features "
                          "because r6_topk.training_frame asserts len(features) == 63. Combine them.",
            "changed": ["the feature set only: 63 Alpha158 -> the 83 columns of panel_extended.parquet"],
            "unchanged": {"objective": "flat-Top-K pairwise, k = n//10, sampled_day with 8 samples",
                          "params": rt.PARAMS, "rounds": rt.ROUNDS, "seed": SEED,
                          "return_scale": rt.RETURN_SCALE,
                          "training_frame_filters": "is_train, trade_date < cutoff, price_valid, "
                                                    "flag_limit_up == 0, finite label from the raw CSV, "
                                                    "days with >= 100 rows",
                          "downstream": "released post-processing, then the shipped nested lift, then "
                                        "the selected orderer at m = 0.985"},
            "feature_counts": {"base": len(base_features), "extended": len(ext_features)},
            "harness_proof": f"the same code path on the {len(base_features)} base features must "
                             f"reproduce {FROZEN_TOPK_2022.name} pred_raw bit-for-bit for {PROOF_YEAR}. "
                             "run_topk_confirm.py already achieved max|diff| 0.000e+00 on this fold with "
                             "r6_topk's own training_frame, so this validates the re-implementation - "
                             "the different panel source, the derived feature list, the group "
                             "construction - before the 83-feature result is believed.",
            "deliverability_recorded_not_assumed": "an 83-feature donor has no test-period prediction. "
                                                   "panel_extended.parquet does cover the test period, so "
                                                   "a fulltrain re-fit is possible, but it is a retrain "
                                                   "on a platform allowing one submission and returning "
                                                   "no score.",
            "labels_rebinding": {"rebound_to": str(LIVE_TRAIN_CSV), "sha256": digest,
                                 "pinned_prefix_matched": True},
            "current_best_before_this_wave": CURRENT_BEST,
            "shipping_rule_declared_in_advance": f"report both halves against {REF_HALF_DEV:.9f} / "
                                                 f"{REF_HALF_CONF:.9f}",
            "roughness_context": "wave 36 measured this construction's excess term as rough at 4.5e-3, "
                                 "so a gain below that is not distinguishable from the curve's own noise",
            "selection_rule": "highest connected 2020-2024 official composite; no other gate",
            "disclosed_selection_cost": "five more models trained on the same five repeatedly viewed "
                                        "years; walk-forward cutoffs unchanged and strictly before each "
                                        "scored year",
            "no_test_period_data_read": True,
            "source_sha256": sha(Path(__file__)),
        }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        log(f"wave-39 protocol frozen: {sha(protocol_path)[:16]}…")
    if args.stage == "protocol":
        return

    log("loading the extended panel (1.8 GB); this is the only large read in this wave")
    t0 = time.monotonic()
    panel = pl.read_parquet(PANEL)
    log(f"panel loaded: {panel.shape}, {time.monotonic() - t0:.0f}s")

    def train_year(year: int, features: list, source: pl.DataFrame) -> tuple:
        cutoff = fold_cutoff(year)
        frame, meta = training_frame_from(source, year, features, cutoff, label_source)
        objective = FlatTopKObjective(frame["trade_date"].to_numpy(),
                                      frame["y_ret_1d"].to_numpy().astype(np.float64))
        x = to_matrix(frame, features)
        dataset = lgb.Dataset(x, label=np.zeros(len(x), dtype=np.float32), feature_name=features,
                              free_raw_data=True)
        del frame
        gc.collect()
        params = dict(rt.PARAMS, objective=objective_callback(objective))
        fit_started = time.monotonic()
        model = lgb.train(params, dataset, num_boost_round=rt.ROUNDS)
        fit_seconds = time.monotonic() - fit_started
        if model.current_iteration() != rt.ROUNDS or objective.iteration != rt.ROUNDS:
            raise AssertionError("round count mismatch")
        del dataset, x
        gc.collect()
        ref = pl.read_parquet(R4 / f"predictions_ensemble4_{year}.parquet").sort("trade_date", "ts_code")
        pred_rows = (source.filter(pl.col("trade_date").is_between(year * 10000 + 101,
                                                                  year * 10000 + 1231))
                     .select(KEYS + features + ["price_valid"]).sort("trade_date", "ts_code"))
        if not ref.select(KEYS).equals(pred_rows.select(KEYS)):
            raise AssertionError(f"{year}: prediction keys do not match the fold frame")
        matrix = to_matrix(pred_rows, features)
        raw = model.predict(matrix, num_threads=8).astype(np.float64)
        raw[~pred_rows["price_valid"].to_numpy()] = -1e6
        del matrix, model
        gc.collect()
        meta.update({"year": year, "n_features": len(features), "fit_seconds": round(fit_seconds, 1)})
        return raw, meta, ref

    if args.stage == "prove":
        base_panel = panel.select(KEYS + list(META_COLUMNS[2:]) + base_features)
        raw, meta, _ = train_year(PROOF_YEAR, base_features, base_panel)
        frozen = pl.read_parquet(FROZEN_TOPK_2022).sort("trade_date", "ts_code")
        target = frozen["pred_raw"].to_numpy().astype(np.float64)
        diff = float(np.abs(raw - target).max())
        identical = bool(np.array_equal(raw, target))
        log(f"PROVE {PROOF_YEAR} on {len(base_features)} base features via the extended panel: "
            f"bit-identical={identical}, max|diff|={diff:.3e}, fit {meta['fit_seconds']}s")
        (OUT / "harness_proof.json").write_text(json.dumps(
            {"proof": "the re-implemented training path on the 63 base features reproduces the frozen "
                      "topk cache", "year": PROOF_YEAR, "n_features": len(base_features),
             "panel_source": str(PANEL), "frozen_cache": str(FROZEN_TOPK_2022),
             "frozen_sha256": sha(FROZEN_TOPK_2022), "bit_identical": identical,
             "max_abs_diff": diff, "training_meta": meta,
             "proved_at_local": time.strftime("%Y-%m-%dT%H:%M:%S")},
            ensure_ascii=False, indent=2, default=str) + "\n", encoding="utf-8")
        if not identical:
            raise AssertionError(f"the re-implementation is not faithful: max|diff| {diff:.3e}. "
                                 "Nothing below can be trusted until this is 0.")
        log("harness proof passed")
        return

    if args.stage == "train":
        from optimize_wave6 import fold_frame
        for year in YEARS:
            path = RAW / f"topk_ext83_seed{SEED}_{year}.parquet"
            if path.exists():
                log(f"  {year}: cached")
                continue
            raw, meta, ref = train_year(year, ext_features, panel)
            # P2: the post-processing stack must not read labels, the assertion r6_topk.fold() makes
            aux_frame = fold_frame(year)
            if not aux_frame.select(KEYS).equals(ref.select(KEYS)):
                raise AssertionError(f"{year}: fold frame keys do not match the prediction frame")
            pred = fixed_prediction(aux_frame, raw)
            nulled = aux_frame.with_columns(pl.lit(None, dtype=pl.Float64).alias("y_ret_1d"))
            if not np.array_equal(pred, fixed_prediction(nulled, raw)):
                raise AssertionError(f"P2 failed for {year}: the stack is not label-independent")
            ref.select(KEYS).with_columns(pl.Series("pred_raw", raw)).write_parquet(
                path, compression="zstd")
            (RAW / f"info_ext83_{year}.json").write_text(
                json.dumps(meta, ensure_ascii=False, indent=2, default=str) + "\n", encoding="utf-8")
            log(f"  ext83 {year}: fit {meta['fit_seconds']}s, {meta['rows']:,} train rows, "
                f"{meta['n_features']} features, label-independence OK")
        log("training complete")
        return

    score_arms(rt, fixed_prediction, ext_features)


def score_arms(rt, fixed_prediction, ext_features) -> None:
    import pandas as pd
    import connected_scorer as cs
    from experiments.revalidate_fold_local import score_official
    from optimize_wave6 import make_prediction_param, fold_frame
    from optimize_wave13 import build_ab
    from optimize_wave15 import daily_ranks, weighted_rank_blend
    from optimize_wave18 import lift
    from src.scoring import Panel

    combined = cs.combined_frame()
    dates = combined["trade_date"].to_numpy()
    flags = combined["flag_limit_up"].to_numpy().astype(np.int64)
    valid = combined["price_valid"].to_numpy().astype(bool)
    codes, uniques = pd.factorize(combined["ts_code"].to_pandas(), sort=True)
    codes = codes.astype(np.int64)
    n_codes = len(uniques)
    tie_key = 1.0 - codes / max(n_codes - 1, 1)
    pdf = combined.select(["trade_date", "flag_limit_up"]).to_pandas()
    slow16_fin = np.load(HERE / SLOW16_FIN)
    frames = {yy: fold_frame(yy) for yy in YEARS}

    w5a = np.load(HERE / W5A_A0B0)
    slow16 = np.load(HERE / SLOW16_A0B0)
    rc = {"w5a": daily_ranks(w5a, valid, dates), "slow16": daily_ranks(slow16, valid, dates)}
    bl = weighted_rank_blend([w5a, slow16], [1 - PARTNER_WEIGHT, PARTNER_WEIGHT], rc, valid, dates,
                             ("w5a", "slow16"))
    orderer = np.where(bl > -9.0, bl + TIE_EPS * tie_key, bl) + TIE_EPS * tie_key

    masks = {str(yy): (dates >= yy * 10000 + 101) & (dates <= yy * 10000 + 1231) for yy in YEARS}
    half = {"2020_2022": np.zeros(len(dates), dtype=bool),
            "2023_2024": np.zeros(len(dates), dtype=bool)}
    for yy in (2020, 2021, 2022):
        half["2020_2022"] |= masks[str(yy)]
    for yy in (2023, 2024):
        half["2023_2024"] |= masks[str(yy)]

    def postprocess(raw_by_year: dict) -> np.ndarray:
        out = []
        for yy in YEARS:
            frame = frames[yy]
            panel = Panel.from_frame(frame.with_columns(pl.Series("pred_raw", raw_by_year[yy])))
            out.append(make_prediction_param(panel, frame["aux_raw"].to_numpy().astype(np.float64),
                                             "top_only", 0.25, 0.9, 0.3, True, 1.0))
            del panel
        return np.concatenate(out)

    results: dict = {}
    proofs: dict = {}

    def dump() -> list:
        arms = sorted(((v["connected_final_score"], k, v) for k, v in results.items()
                       if "connected_final_score" in v), reverse=True)
        payload = {"status": "running", "updated_at_local": time.strftime("%Y-%m-%dT%H:%M:%S"),
                   "purpose": "the winning donor objective on the 83-feature extension",
                   "m_frac": M_FRAC, "tie_break_eps": TIE_EPS, "harness_proofs": proofs,
                   "current_best_before_this_wave": CURRENT_BEST,
                   "reference_halves": {"2020_2022": REF_HALF_DEV, "2023_2024": REF_HALF_CONF},
                   "results": results, "n_scored": len(arms),
                   "ranking": [{"arm": k, "connected_final_score": s, "margin_full": v["margin_full"],
                                "margin_2020_2022": v["margin_2020_2022"],
                                "margin_2023_2024": v["margin_2023_2024"],
                                "wins_both_halves": v["wins_both_halves"],
                                "ic_mean": v["connected_metrics"]["ic_mean"],
                                "annual_excess": v["connected_metrics"]["annual_excess"],
                                "mean_turnover": v["connected_metrics"]["mean_turnover"],
                                "donor_standalone_ic": v.get("donor_standalone_ic"),
                                "donor_standalone_excess": v.get("donor_standalone_excess")}
                               for s, k, v in arms],
                   "best": arms[0][1] if arms else None,
                   "best_connected_final_score": arms[0][0] if arms else None,
                   "no_test_period_data_read": True, "source_sha256": sha(Path(__file__))}
        (HERE / "wave39_results.json").write_text(
            json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        return arms

    def evaluate(name: str, finished: np.ndarray, extra: dict) -> None:
        promote = np.where(np.isfinite(finished) & (finished > -9.0),
                           finished + TIE_EPS * tie_key, finished)
        donor, lift_stats = lift(promote, slow16_fin, pdf)
        hybrid, stats = build_ab(donor, orderer, orderer, dates, flags, codes, n_codes, M_FRAC)
        metrics, _ = score_official(combined, hybrid)
        standalone, _ = score_official(combined, finished)
        halves = {}
        for label, mask in half.items():
            sub, _ = score_official(combined.filter(pl.Series(mask)), hybrid[mask])
            halves[label] = sub["final_score"]
        results[name] = {**extra, "lift_stats": lift_stats,
                         "connected_final_score": metrics["final_score"],
                         "connected_metrics": metrics, "halves": halves,
                         "donor_standalone_connected": standalone["final_score"],
                         "donor_standalone_ic": standalone["ic_mean"],
                         "donor_standalone_excess": standalone["annual_excess"],
                         "margin_full": metrics["final_score"] - CURRENT_BEST,
                         "margin_2020_2022": halves["2020_2022"] - REF_HALF_DEV,
                         "margin_2023_2024": halves["2023_2024"] - REF_HALF_CONF,
                         "wins_both_halves": bool(halves["2020_2022"] > REF_HALF_DEV
                                                  and halves["2023_2024"] > REF_HALF_CONF),
                         "boundary_tie_days": stats["boundary_tie_days"],
                         "mean_retention_ratio": stats["mean_retention_ratio"]}
        cs.log(f"{name[:24]:24s} CONNECTED {metrics['final_score']:.9f} "
               f"({metrics['final_score'] - CURRENT_BEST:+.2e}) | ic {metrics['ic_mean']:.6f} | "
               f"exc {metrics['annual_excess']:.6f} | turn {metrics['mean_turnover']:.6f} | "
               f"donor IC {standalone['ic_mean']:.6f} exc {standalone['annual_excess']:.6f} | "
               f"2020-22 {halves['2020_2022'] - REF_HALF_DEV:+.2e} | 2023-24 "
               f"{halves['2023_2024'] - REF_HALF_CONF:+.2e}")
        dump()

    frozen_topk = np.load(HERE / TOPK_FIN)
    evaluate("P_base63_reference", frozen_topk,
             {"kind": "flat_topk_base63", "role": "harness_proof",
              "needs_test_fulltrain_refit": False})
    proofs["P_base63_reference"] = {
        "scored": results["P_base63_reference"]["connected_final_score"],
        "expected": CURRENT_BEST,
        "abs_diff": abs(results["P_base63_reference"]["connected_final_score"] - CURRENT_BEST),
        "training_path_proof": json.loads((OUT / "harness_proof.json").read_text(encoding="utf-8"))
        if (OUT / "harness_proof.json").exists() else None}
    if proofs["P_base63_reference"]["abs_diff"] > 1e-12:
        raise AssertionError(f"harness proof failed: {proofs['P_base63_reference']}")
    cs.log("harness proof passed: the base-63 donor reproduces 0.443190552")

    raws = {}
    for yy in YEARS:
        path = RAW / f"topk_ext83_seed{SEED}_{yy}.parquet"
        if not path.exists():
            raise SystemExit(f"missing {path.name}; run the train stage first")
        raws[yy] = pl.read_parquet(path)["pred_raw"].to_numpy().astype(np.float64)
    evaluate("ext83_flat_topk", postprocess(raws),
             {"kind": "flat_topk_ext83", "n_features": len(ext_features),
              "needs_test_fulltrain_refit": True})

    arms = dump()
    payload = json.loads((HERE / "wave39_results.json").read_text(encoding="utf-8"))
    payload["status"] = "complete"
    payload["completed_at_local"] = time.strftime("%Y-%m-%dT%H:%M:%S")
    (HERE / "wave39_results.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("\n| donor | CONNECTED | margin | IC | excess | turn | donor IC | donor excess | 2020-22 | 2023-24 | both? |")
    print("|---|---|---|---|---|---|---|---|---|---|---|")
    for s, name, v in arms:
        m = v["connected_metrics"]
        print(f"| {name[:22]} | **{s:.9f}** | {v['margin_full']:+.2e} | {m['ic_mean']:.6f} | "
              f"{m['annual_excess']:.6f} | {m['mean_turnover']:.6f} | "
              f"{v['donor_standalone_ic']:.6f} | {v['donor_standalone_excess']:.6f} | "
              f"{v['margin_2020_2022']:+.2e} | {v['margin_2023_2024']:+.2e} | "
              f"{'YES' if v['wins_both_halves'] else 'no'} |")


if __name__ == "__main__":
    main()
