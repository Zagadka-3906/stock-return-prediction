"""Wave 37, direction 4c: a different learning-to-rank family for the membership donor.

The donor is the highest-leverage component in the construction - wave 13 measured that swapping it moves
the composite by up to 1.4e-3 while every orderer-side change in waves 15-35 moved it by less - and every
donor tested so far comes from ONE objective family: the custom flat-Top-K pairwise logistic loss in
experiments/r6_topk.py. Wave 31 swept that family's only structural constant (K) and wave 24 swept its
seeds. The family itself has never been questioned.

LightGBM ships two production ranking objectives that optimize a different surrogate:
  lambdarank   LambdaRank, which weights pair gradients by the change in NDCG from swapping the pair
  rank_xendcg  Xu's et al. cross-entropy NDCG, a listwise loss that is top-heavy by construction rather
               than by an explicit truncation level
Both are built-in C++ rather than a Python callback, so they are also roughly an order of magnitude faster
per round than the flat-Top-K objective, which makes a wider grid affordable.

Relevance labels are the one design choice that matters, and three are tested because they encode three
different bets about what the evaluator rewards:
  graded     relevance = the decile of next-day return within the day, 0..9. Rewards ordering the whole
             cross-section, which is what NDCG's discount normally wants.
  binary     relevance = 1 if the name is in the day's top return decile else 0. Matches the evaluator's
             Top-decile membership exactly and ignores everything below it.
  topheavy   relevance = the band index min(decile//3, 3), with LightGBM's label_gain set to
             [0, 1, 3, 27]. Same information as graded but with exponential emphasis on the head,
             which is where the excess term comes from.

The construction downstream is untouched: released post-processing, then the shipped nested lift as the
promote source, then the selected orderer at m = 0.985. So every arm is directly comparable to
0.443190552, and any gain is attributable to the objective family rather than to the plumbing.

Harness proofs:
  P1  the flat-Top-K frac 0.10 donor, rebuilt through this wave's own scoring path, must reproduce
      0.443190552. That pins the shared plumbing before any new objective is believed.
  P2  every trained raw must be label-independent under the post-processing stack, the same assertion
      r6_topk.fold() makes about itself.

Deliverability is recorded, not assumed: none of these models has a test-period prediction, so the winner
would need a fulltrain re-fit. That is a known cost - run_topk_confirm.py already retrained a fold to
max|diff| 0.000e+00 with this exact frame and feature plumbing - but it is a retrain on a platform that
allows one submission and gives no score back.

Selection is 后续选模标准.md §3/§4. Both halves are reported for every arm because waves 23/25/26/31 all
produced full-window gains that were redistribution, and wave 33 showed the mechanism: the excess term
carries a time trend no structural statistic explains. No test-period data is read here.
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

OUT = HERE / "wave37_ltr"
RAW = OUT / "raw"
YEARS = (2020, 2021, 2022, 2023, 2024)
SEED = 2026
ROUNDS = 180
LIVE_TRAIN_CSV = ROOT / "data/raw/训练集.csv"
PINNED_PREFIX = "e9d23e87f7e1f943"
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

BASE_PARAMS = dict(metric="None", learning_rate=0.05, num_leaves=31, min_data_in_leaf=300,
                   feature_fraction=0.85, bagging_fraction=0.85, bagging_freq=1, lambda_l2=5.0,
                   max_bin=127, num_threads=8, seed=SEED, verbosity=-1, force_col_wise=True)

# Every label is an INTEGER. The first run of this wave passed graded_float (decile/9) and
# topheavy_float (band/27) to rank_xendcg; LightGBM's ranking objectives int-cast the label, so both
# collapsed to {0, 1} and the two arms trained BIT-IDENTICAL models (max|diff| 0.0 on the raws) while
# being reported as two different relevance encodings. See protocol_wave37_amendment_001.json.
VARIANTS = {
    "lambdarank_graded": {"objective": "lambdarank", "label": "graded",
                          "params": {"lambdarank_truncation_level": 30, "label_gain": list(range(10))}},
    "lambdarank_binary": {"objective": "lambdarank", "label": "binary",
                          "params": {"lambdarank_truncation_level": 30, "label_gain": [0, 1]}},
    "lambdarank_topheavy": {"objective": "lambdarank", "label": "topheavy",
                            "params": {"lambdarank_truncation_level": 30, "label_gain": [0, 1, 3, 27]}},
    # truncation 30 out of ~4570 rows per day gives gradient to 0.7% of the cross-section, which is a
    # confound rather than a property of LambdaRank: it may explain the negative donor IC of the binary
    # and topheavy arms. Truncation 500 covers the evaluator's whole Top decile.
    "lambdarank_graded_trunc500": {"objective": "lambdarank", "label": "graded",
                                   "params": {"lambdarank_truncation_level": 500,
                                              "label_gain": list(range(10))}},
    "lambdarank_binary_trunc500": {"objective": "lambdarank", "label": "binary",
                                   "params": {"lambdarank_truncation_level": 500,
                                              "label_gain": [0, 1]}},
    "xendcg_graded_int": {"objective": "rank_xendcg", "label": "graded", "params": {}},
    "xendcg_topheavy_int": {"objective": "rank_xendcg", "label": "topheavy", "params": {}},
}


def sha(path) -> str:
    value = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for chunk in iter(lambda: stream.read(8 * 1024 * 1024), b""):
            value.update(chunk)
    return value.hexdigest()


def log(message: str) -> None:
    print(f"[{time.strftime('%H:%M:%S')}] {message}", flush=True)


def relevance(kind: str, y: np.ndarray, dates: np.ndarray) -> np.ndarray:
    """Relevance labels from next-day returns, computed within each day.

    `graded` is the return decile 0..9. `binary` is 1 inside the top decile. `topheavy` collapses the
    deciles into four bands with exponential weights. The `_float` variants keep the raw return, which
    rank_xendcg accepts directly.
    """
    out = np.zeros(len(y), dtype=np.float64)
    _, starts = np.unique(dates, return_index=True)
    ends = np.append(starts[1:], len(dates))
    for start, end in zip(starts, ends):
        rows = np.arange(start, end)
        finite = np.isfinite(y[start:end])
        if finite.sum() < 100:
            continue
        idx = rows[finite]
        vals = y[idx]
        n = len(vals)
        order = np.argsort(vals, kind="stable")
        decile = np.empty(n, dtype=np.int64)
        decile[order] = np.minimum((np.arange(n) * 10) // n, 9)
        if kind in ("graded_float", "topheavy_float"):
            raise AssertionError(
                f"refusing to build float relevance '{kind}': LightGBM's ranking objectives int-cast "
                "the label, so a float encoding silently collapses to {0, 1}. This is the defect "
                "recorded in protocol_wave37_amendment_001.json.")
        if kind == "graded":
            out[idx] = decile
        elif kind == "binary":
            out[idx] = (decile == 9).astype(np.float64)
        elif kind == "topheavy":
            # the band INDEX, not the band value: LightGBM's lambdarank maps label i to label_gain[i],
            # so the exponential emphasis belongs in label_gain, not in the label
            out[idx] = np.minimum(decile // 3, 3)
        else:
            raise KeyError(kind)
    return out


def train_variant(rt, lgb, to_matrix, FEATURE_FILE, feature_names, R4, name: str, year: int):
    spec = VARIANTS[name]
    started = time.monotonic()
    train, features, meta = rt.training_frame(year)
    dates_tr = train["trade_date"].to_numpy()
    y_tr = train["y_ret_1d"].to_numpy().astype(np.float64)
    label = relevance(spec["label"], y_tr, dates_tr)
    label = label.astype(np.int32)   # every label is an integer; see the amendment
    # LightGBM ranking objectives need the group sizes; training_frame already dropped days with < 100
    # rows and sorted by (trade_date, ts_code), so consecutive equal dates are the groups
    _, counts = np.unique(dates_tr, return_counts=True)
    x = to_matrix(train, features)
    dataset = lgb.Dataset(x, label=label, group=counts, feature_name=features, free_raw_data=True)
    del train
    gc.collect()
    params = dict(BASE_PARAMS, objective=spec["objective"], **spec["params"])
    fit_started = time.monotonic()
    model = lgb.train(params, dataset, num_boost_round=ROUNDS)
    fit_seconds = time.monotonic() - fit_started
    if model.current_iteration() != ROUNDS:
        raise AssertionError(f"{name} {year}: {model.current_iteration()} rounds, expected {ROUNDS}")
    del dataset, x
    gc.collect()

    frame = pl.read_parquet(R4 / f"predictions_ensemble4_{year}.parquet").sort("trade_date", "ts_code")
    valid = (pl.scan_parquet(FEATURE_FILE)
             .filter(pl.col("trade_date").is_between(year * 10000 + 101, year * 10000 + 1231))
             .select(["ts_code", "trade_date"] + feature_names()).sort("trade_date", "ts_code").collect())
    if not frame.select(["ts_code", "trade_date"]).equals(valid.select(["ts_code", "trade_date"])):
        raise AssertionError(f"{name} {year}: key mismatch")
    matrix = to_matrix(valid, features)
    raw = model.predict(matrix, num_threads=8).astype(np.float64)
    raw[~frame["price_valid"].to_numpy()] = -1e6
    del matrix, valid, model
    gc.collect()
    info = {"variant": name, "year": year, "objective": spec["objective"], "label": spec["label"],
            "params": {k: v for k, v in params.items() if k != "objective"},
            "rounds": ROUNDS, "fit_seconds": round(fit_seconds, 1),
            "total_seconds": round(time.monotonic() - started, 1), "training_meta": meta,
            "label_distribution": {str(k): int(v) for k, v in
                                   zip(*np.unique(label, return_counts=True))}
            if len(np.unique(label)) <= 12 else "continuous",
            "groups": int(len(counts))}
    return frame, raw, info


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("stage", choices=("protocol", "train", "score"))
    parser.add_argument("--variants", nargs="*", default=None)
    args = parser.parse_args()

    OUT.mkdir(parents=True, exist_ok=True)
    RAW.mkdir(parents=True, exist_ok=True)

    import lightgbm as lgb
    import experiments.r6_topk as rt
    from run import FEATURE_FILE, feature_names, to_matrix
    from experiments.r6_topk import R4, fixed_prediction

    if not LIVE_TRAIN_CSV.exists():
        raise SystemExit(f"no live training CSV at {LIVE_TRAIN_CSV}")
    digest = sha(LIVE_TRAIN_CSV)
    if not digest.startswith(PINNED_PREFIX):
        raise SystemExit(f"the live 训练集.csv sha256 {digest[:16]}… is not the pinned file")
    rt.RAW_LABELS = LIVE_TRAIN_CSV

    protocol_path = HERE / "protocol_wave37.json"
    if not protocol_path.exists():
        protocol_path.write_text(json.dumps({
            "frozen_at_local": time.strftime("%Y-%m-%dT%H:%M:%S"),
            "supersedes": "protocol_wave37_superseded_001.json; see "
                          "protocol_wave37_amendment_001.json and "
                          "failure_wave37_labels_truncated.log",
            "defect_fixed": "graded_float and topheavy_float relevance labels were passed to "
                            "rank_xendcg, which int-casts labels, so both arms trained bit-identical "
                            "binary models while being reported as two relevance encodings. All labels "
                            "are now integers and the float kinds raise instead of silently coercing. "
                            "Two LambdaRank arms at truncation level 500 are added, because truncation "
                            "30 out of ~4570 rows per day gives gradient to 0.7% of the cross-section "
                            "and is a plausible confound for the negative donor IC those arms showed.",
            "standard": "后续选模标准.md §3 connected composite primary; §4 highest score wins",
            "status": "in_sample_selection_disclosed",
            "hypothesis": "the membership donor is the highest-leverage component and every donor tested "
                          "so far comes from one objective family, the custom flat-Top-K pairwise "
                          "logistic loss. Wave 31 swept its K and wave 24 its seeds; the family itself "
                          "was never questioned. LightGBM's built-in lambdarank and rank_xendcg optimize "
                          "a different surrogate (NDCG-swap-weighted pairs, and a listwise top-heavy "
                          "cross-entropy) and are an order of magnitude faster per round, so a wider "
                          "grid is affordable.",
            "variants": {k: {"objective": v["objective"], "label": v["label"], "params": v["params"]}
                         for k, v in VARIANTS.items()},
            "relevance_labels": {
                "graded": "return decile 0..9 within the day",
                "binary": "1 if in the day's top return decile else 0, matching the evaluator exactly",
                "topheavy": "four bands (decile//3, capped at 3) with exponential label_gain [0,1,3,27]",
                "all_labels_are_integers": "LightGBM's ranking objectives int-cast the label, so a "
                                           "float encoding collapses to {0,1}; relevance() now raises "
                                           "rather than coerce"
            },
            "capacity_matched_to_the_topk_recipe": {"params": BASE_PARAMS, "rounds": ROUNDS,
                                                    "seed": SEED},
            "downstream_unchanged": "released post-processing, then the shipped nested lift as promote "
                                    "source, then the selected orderer at m = 0.985, so every arm is "
                                    "directly comparable to 0.443190552",
            "harness_proofs": {
                "P1": "the flat-Top-K frac 0.10 donor rebuilt through this wave's own scoring path must "
                      f"reproduce {CURRENT_BEST}",
                "P2": "every trained raw must be label-independent under the post-processing stack",
            },
            "deliverability_recorded_not_assumed": "none of these models has a test-period prediction, so "
                                                   "the winner needs a fulltrain re-fit. Known cost: "
                                                   "run_topk_confirm.py retrained a fold to max|diff| "
                                                   "0.000e+00 with this frame and feature plumbing. But "
                                                   "the platform allows one submission and returns no "
                                                   "score, so a retrain is a new failure surface.",
            "labels_rebinding": {"rebound_to": str(LIVE_TRAIN_CSV), "sha256": digest,
                                 "pinned_prefix_matched": True},
            "current_best_before_this_wave": CURRENT_BEST,
            "shipping_rule_declared_in_advance": f"report both halves against {REF_HALF_DEV:.9f} / "
                                                 f"{REF_HALF_CONF:.9f}",
            "selection_rule": "highest connected 2020-2024 official composite; no other gate",
            "disclosed_selection_cost": "five new model families trained on the same five repeatedly "
                                        "viewed years; walk-forward cutoffs unchanged and strictly "
                                        "before each scored year, but the decision to try these "
                                        "objectives was made after those years were viewed",
            "no_test_period_data_read": True,
            "source_sha256": sha(Path(__file__)),
        }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        log(f"wave-37 protocol frozen: {sha(protocol_path)[:16]}…")
    if args.stage == "protocol":
        return

    wanted = tuple(args.variants) if args.variants else tuple(VARIANTS)

    if args.stage == "train":
        for name in wanted:
            if name not in VARIANTS:
                raise SystemExit(f"unknown variant {name}")
            for year in YEARS:
                path = RAW / f"{name}_{year}.parquet"
                if path.exists():
                    continue
                frame, raw, info = train_variant(rt, lgb, to_matrix, FEATURE_FILE, feature_names, R4,
                                                 name, year)
                pred = fixed_prediction(frame, raw)
                nulled = frame.with_columns(pl.lit(None, dtype=pl.Float64).alias("y_ret_1d"))
                if not np.array_equal(pred, fixed_prediction(nulled, raw)):
                    raise AssertionError(f"P2 failed for {name} {year}: the stack reads labels")
                frame.select(["ts_code", "trade_date"]).with_columns(
                    pl.Series("pred_raw", raw)).write_parquet(path, compression="zstd")
                (RAW / f"info_{name}_{year}.json").write_text(
                    json.dumps(info, ensure_ascii=False, indent=2, default=str) + "\n",
                    encoding="utf-8")
                log(f"  {name} {year}: fit {info['fit_seconds']}s, groups {info['groups']}, "
                    f"{info['training_meta']['rows']:,} rows")
        log("training complete")
        return

    score_variants(rt)


def score_variants(rt) -> None:
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
            gc.collect()
        return np.concatenate(out)

    results: dict = {}
    proofs: dict = {}

    def dump() -> list:
        arms = sorted(((v["connected_final_score"], k, v) for k, v in results.items()
                       if "connected_final_score" in v), reverse=True)
        payload = {"status": "running", "updated_at_local": time.strftime("%Y-%m-%dT%H:%M:%S"),
                   "purpose": "different learning-to-rank objective families for the membership donor",
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
                                "donor_standalone_excess": v.get("donor_standalone_excess")}
                               for s, k, v in arms],
                   "best": arms[0][1] if arms else None,
                   "best_connected_final_score": arms[0][0] if arms else None,
                   "no_test_period_data_read": True, "source_sha256": sha(Path(__file__))}
        (HERE / "wave37_results.json").write_text(
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
                         "donor_standalone_excess": standalone["annual_excess"],
                         "donor_standalone_ic": standalone["ic_mean"],
                         "margin_full": metrics["final_score"] - CURRENT_BEST,
                         "margin_2020_2022": halves["2020_2022"] - REF_HALF_DEV,
                         "margin_2023_2024": halves["2023_2024"] - REF_HALF_CONF,
                         "wins_both_halves": bool(halves["2020_2022"] > REF_HALF_DEV
                                                  and halves["2023_2024"] > REF_HALF_CONF),
                         "boundary_tie_days": stats["boundary_tie_days"],
                         "mean_retention_ratio": stats["mean_retention_ratio"]}
        cs.log(f"{name[:26]:26s} CONNECTED {metrics['final_score']:.9f} "
               f"({metrics['final_score'] - CURRENT_BEST:+.2e}) | ic {metrics['ic_mean']:.6f} | "
               f"exc {metrics['annual_excess']:.6f} | turn {metrics['mean_turnover']:.6f} | "
               f"donor standalone exc {standalone['annual_excess']:.6f} ic "
               f"{standalone['ic_mean']:.6f} | 2020-22 {halves['2020_2022'] - REF_HALF_DEV:+.2e} | "
               f"2023-24 {halves['2023_2024'] - REF_HALF_CONF:+.2e}")
        dump()

    # ---- P1: the shared plumbing, via the frozen Top-K frac 0.10 donor
    frozen_topk = np.load(HERE / TOPK_FIN)
    evaluate("P1_topk_frac0.10", frozen_topk, {"kind": "flat_topk_reference", "role": "harness_proof"})
    proofs["P1"] = {"scored": results["P1_topk_frac0.10"]["connected_final_score"],
                    "expected": CURRENT_BEST,
                    "abs_diff": abs(results["P1_topk_frac0.10"]["connected_final_score"] - CURRENT_BEST)}
    if proofs["P1"]["abs_diff"] > 1e-12:
        raise AssertionError(f"P1 failed: {proofs['P1']}")
    cs.log("P1 passed: the shared plumbing reproduces 0.443190552")

    for name in VARIANTS:
        raws = {}
        missing = False
        for yy in YEARS:
            path = RAW / f"{name}_{yy}.parquet"
            if not path.exists():
                log(f"{name}: missing {path.name}, skipped")
                missing = True
                break
            raws[yy] = pl.read_parquet(path)["pred_raw"].to_numpy().astype(np.float64)
        if missing:
            continue
        evaluate(name, postprocess(raws),
                 {"kind": "ltr_variant", "objective": VARIANTS[name]["objective"],
                  "label": VARIANTS[name]["label"], "needs_test_fulltrain_refit": True})

    arms = dump()
    payload = json.loads((HERE / "wave37_results.json").read_text(encoding="utf-8"))
    payload["status"] = "complete"
    payload["completed_at_local"] = time.strftime("%Y-%m-%dT%H:%M:%S")
    (HERE / "wave37_results.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("\n| donor objective | CONNECTED | margin | IC | excess | turn | donor IC | donor excess | 2020-22 | 2023-24 | both? |")
    print("|---|---|---|---|---|---|---|---|---|---|---|")
    for s, name, v in arms:
        m = v["connected_metrics"]
        print(f"| {name[:24]} | **{s:.9f}** | {v['margin_full']:+.2e} | {m['ic_mean']:.6f} | "
              f"{m['annual_excess']:.6f} | {m['mean_turnover']:.6f} | "
              f"{v.get('donor_standalone_ic', float('nan')):.6f} | "
              f"{v.get('donor_standalone_excess', float('nan')):.6f} | "
              f"{v['margin_2020_2022']:+.2e} | {v['margin_2023_2024']:+.2e} | "
              f"{'YES' if v['wins_both_halves'] else 'no'} |")


if __name__ == "__main__":
    main()
