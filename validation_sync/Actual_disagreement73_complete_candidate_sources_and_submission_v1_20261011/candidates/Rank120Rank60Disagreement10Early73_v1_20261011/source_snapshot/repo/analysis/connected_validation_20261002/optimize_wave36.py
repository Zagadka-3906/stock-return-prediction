"""Wave 36: the K-fraction curve is not monotone at 0.15, which undermines confidence in the 0.20 peak.

Wave 31's grid gave 0.10 -> 0.443190552, 0.15 -> 0.442261297, 0.20 -> 0.445092234, 0.25 -> 0.444407311.
The value at 0.15 is BELOW both its neighbours by 9.3e-4 and 2.8e-3. A smooth objective cannot do that,
so one of two things is true: either the excess term is noisy enough at this sample size to move 3e-3
between adjacent settings, or 0.15 is genuinely a bad point for a reason nobody has identified.

This matters directly for the decision in front of the user, because the case for adopting frac 0.20 rests
entirely on it being a peak. If adjacent points can move by 3e-3 for no structural reason, then a +1.90e-3
"peak" is within the curve's own roughness and is not evidence of anything.

Two cheap tests, neither needing a new model family:
  A. fill in the curve at 0.125 and 0.175. If the curve is smooth once the grid is finer, 0.15 was a
     real local dip and the peak structure is meaningful. If the new points are also jagged, the curve is
     rough at the 3e-3 level and no interior point can be trusted.
  B. blend the two Top-K columns that already exist, at frac 0.10 and frac 0.20, and use the blend as the
     promote source. This tests whether the frac 0.20 column's better global ordering can be had without
     taking its volatile excess term wholesale. Wave 18 found that blending the promote source with a
     structurally DIFFERENT model (W5a) collapses excess from 0.352 to 0.320; blending two columns from
     the SAME recipe and the SAME seed at different K is a far more conservative perturbation and has
     not been tried.

Harness proof: frac 0.10 as promote source with the slow16 re-ranker must reproduce 0.443190552.

Everything is reported with the both-halves decomposition, because waves 23/25/26/31 all produced
full-window gains that were redistribution between halves, and because the frac 0.20 excess term is the
specific quantity under suspicion here. Selection is 后续选模标准.md §3/§4. No test-period data is read.
"""
from __future__ import annotations

import gc
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
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(ARCHIVE))

RAW31 = HERE / "wave31_topk/raw"
RAW36 = HERE / "wave36_topk/raw"
YEARS = (2020, 2021, 2022, 2023, 2024)
SEED = 2026
NEW_FRACS = (0.125, 0.175)
EXISTING_FRACS = (0.10, 0.15, 0.20, 0.25, 0.30)
BLEND_WEIGHTS = (0.25, 0.50, 0.75)
TIE_EPS = 1e-9
M_FRAC = 0.985
PARTNER_WEIGHT = 0.25
CURRENT_BEST = 0.44319055217888365
REF_HALF_DEV = 0.442705356
REF_HALF_CONF = 0.443926938
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


def frac_dir(frac: float) -> Path:
    return RAW31 if frac in EXISTING_FRACS else RAW36


def raw_path(frac: float, year: int) -> Path:
    # wave 31 wrote its caches with two decimals, so the two naming conventions have to be honoured
    fmt = f"{frac:.2f}" if frac in EXISTING_FRACS else f"{frac:.3f}"
    return frac_dir(frac) / f"topk_seed{SEED}_f{fmt}_{year}.parquet"


def train_new_fracs() -> None:
    """Train the two fill-in fractions, reusing wave 31's objective via its own module."""
    RAW36.mkdir(parents=True, exist_ok=True)
    import optimize_wave31 as w31
    import lightgbm as lgb
    import experiments.r6_topk as rt
    from run import FEATURE_FILE, feature_names, to_matrix
    from experiments.r6_topk import R4, fixed_prediction

    if not w31.LIVE_TRAIN_CSV.exists():
        raise SystemExit(f"no live training CSV at {w31.LIVE_TRAIN_CSV}")
    digest = sha(w31.LIVE_TRAIN_CSV)
    if not digest.startswith(w31.PINNED_PREFIX):
        raise SystemExit(f"the live 训练集.csv sha256 {digest[:16]}… is not the pinned file")
    rt.RAW_LABELS = w31.LIVE_TRAIN_CSV

    for frac in NEW_FRACS:
        for year in YEARS:
            out = RAW36 / f"topk_seed{SEED}_f{frac:.3f}_{year}.parquet"
            if out.exists():
                log(f"  frac {frac} {year}: cached")
                continue
            frame, raw, info = w31.train(rt, year, SEED, frac, to_matrix, lgb, FEATURE_FILE,
                                         feature_names, R4)
            pred = fixed_prediction(frame, raw)
            nulled = frame.with_columns(pl.lit(None, dtype=pl.Float64).alias("y_ret_1d"))
            if not np.array_equal(pred, fixed_prediction(nulled, raw)):
                raise AssertionError(f"frac {frac} {year}: the stack is not label-independent")
            frame.select(["ts_code", "trade_date"]).with_columns(
                pl.Series("pred_raw", raw)).write_parquet(out, compression="zstd")
            (RAW36 / f"info_f{frac:.3f}_{year}.json").write_text(
                json.dumps(info, ensure_ascii=False, indent=2, default=str) + "\n", encoding="utf-8")
            log(f"  frac {frac} {year}: fit {info['fit_seconds']}s, {info['training_meta']['rows']:,} rows")


def main() -> None:
    protocol_path = HERE / "protocol_wave36.json"
    if not protocol_path.exists():
        protocol_path.write_text(json.dumps({
            "frozen_at_local": time.strftime("%Y-%m-%dT%H:%M:%S"),
            "standard": "后续选模标准.md §3 connected composite primary; §4 highest score wins",
            "status": "in_sample_selection_disclosed",
            "hypothesis": {
                "A_curve_smoothness": "wave 31's grid has 0.15 BELOW both neighbours (0.442261 against "
                                      "0.443191 and 0.445092), which a smooth objective cannot do. Fill "
                                      "in 0.125 and 0.175. If the curve smooths out, the 0.20 peak is "
                                      "meaningful; if the new points are also jagged, the curve is rough "
                                      "at the 3e-3 level and no interior point can be trusted - which "
                                      "would directly undercut the case for adopting frac 0.20.",
                "B_k_blend": "blend the frac 0.10 and frac 0.20 columns and use the blend as the promote "
                             "source, to test whether frac 0.20's better global ordering can be had "
                             "without its volatile excess term. Wave 18 found that blending the promote "
                             "source with a structurally different model collapses excess; two columns "
                             "from the same recipe and seed at different K is a far milder perturbation.",
            },
            "new_fracs": list(NEW_FRACS), "existing_fracs": list(EXISTING_FRACS),
            "blend_weights_on_frac_0.20": list(BLEND_WEIGHTS),
            "seed": SEED,
            "fixed": {"promote_width_q": 0.10, "re_ranker": SLOW16_FIN,
                      "outer_orderer": [W5A_A0B0, SLOW16_A0B0],
                      "outer_weights": [1 - PARTNER_WEIGHT, PARTNER_WEIGHT], "m_frac": M_FRAC,
                      "tie_break_eps": TIE_EPS},
            "harness_proof": f"frac 0.10 with the slow16 re-ranker must reproduce {CURRENT_BEST}",
            "deliverability": "any fraction other than 0.10 needs a test-period fulltrain re-fit of the "
                              "Top-K model; flagged per arm",
            "current_best_before_this_wave": CURRENT_BEST,
            "shipping_rule_declared_in_advance": f"report both halves against {REF_HALF_DEV:.9f} / "
                                                 f"{REF_HALF_CONF:.9f}",
            "selection_rule": "highest connected 2020-2024 official composite; no other gate",
            "disclosed_selection_cost": "two more models trained on the same five repeatedly viewed "
                                        "years, walk-forward cutoffs unchanged",
            "no_test_period_data_read": True,
            "source_sha256": sha(Path(__file__)),
        }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        log(f"wave-36 protocol frozen: {sha(protocol_path)[:16]}…")

    if "--skip-train" not in sys.argv:
        train_new_fracs()

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

    def load_frac(frac: float) -> np.ndarray:
        raws = {}
        for yy in YEARS:
            path = raw_path(frac, yy)
            if not path.exists():
                raise SystemExit(f"missing {path.name}")
            raws[yy] = pl.read_parquet(path)["pred_raw"].to_numpy().astype(np.float64)
        return postprocess(raws)

    finished_cache: dict = {}

    def finished(frac: float) -> np.ndarray:
        if frac not in finished_cache:
            finished_cache[frac] = load_frac(frac)
        return finished_cache[frac]

    results: dict = {}
    proofs: dict = {}

    def dump() -> list:
        arms = sorted(((v["connected_final_score"], k, v) for k, v in results.items()
                       if "connected_final_score" in v), reverse=True)
        payload = {"status": "running", "updated_at_local": time.strftime("%Y-%m-%dT%H:%M:%S"),
                   "purpose": "fill in the K-fraction curve and test a K-blend promote source",
                   "m_frac": M_FRAC, "tie_break_eps": TIE_EPS, "harness_proofs": proofs,
                   "current_best_before_this_wave": CURRENT_BEST,
                   "reference_halves": {"2020_2022": REF_HALF_DEV, "2023_2024": REF_HALF_CONF},
                   "results": results, "n_scored": len(arms),
                   "curve": {k: v["connected_final_score"] for k, v in results.items()
                             if k.startswith("frac") and "connected_final_score" in v},
                   "ranking": [{"arm": k, "connected_final_score": s, "margin_full": v["margin_full"],
                                "margin_2020_2022": v["margin_2020_2022"],
                                "margin_2023_2024": v["margin_2023_2024"],
                                "wins_both_halves": v["wins_both_halves"],
                                "needs_test_fulltrain_refit": v["needs_test_fulltrain_refit"],
                                "ic_mean": v["connected_metrics"]["ic_mean"],
                                "annual_excess": v["connected_metrics"]["annual_excess"],
                                "mean_turnover": v["connected_metrics"]["mean_turnover"]}
                               for s, k, v in arms],
                   "best": arms[0][1] if arms else None,
                   "best_connected_final_score": arms[0][0] if arms else None,
                   "no_test_period_data_read": True, "source_sha256": sha(Path(__file__))}
        (HERE / "wave36_results.json").write_text(
            json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        return arms

    def score(name: str, promote_column: np.ndarray, needs_refit: bool, extra: dict) -> float:
        promote_tb = np.where(np.isfinite(promote_column) & (promote_column > -9.0),
                              promote_column + TIE_EPS * tie_key, promote_column)
        donor, lift_stats = lift(promote_tb, slow16_fin, pdf)
        hybrid, stats = build_ab(donor, orderer, orderer, dates, flags, codes, n_codes, M_FRAC)
        metrics, _ = score_official(combined, hybrid)
        halves = {}
        for label, mask in half.items():
            sub, _ = score_official(combined.filter(pl.Series(mask)), hybrid[mask])
            halves[label] = sub["final_score"]
        results[name] = {**extra, "needs_test_fulltrain_refit": needs_refit,
                         "lift_stats": lift_stats,
                         "connected_final_score": metrics["final_score"],
                         "connected_metrics": metrics, "halves": halves,
                         "margin_full": metrics["final_score"] - CURRENT_BEST,
                         "margin_2020_2022": halves["2020_2022"] - REF_HALF_DEV,
                         "margin_2023_2024": halves["2023_2024"] - REF_HALF_CONF,
                         "wins_both_halves": bool(halves["2020_2022"] > REF_HALF_DEV
                                                  and halves["2023_2024"] > REF_HALF_CONF),
                         "boundary_tie_days": stats["boundary_tie_days"],
                         "swaps": stats["swaps"],
                         "mean_retention_ratio": stats["mean_retention_ratio"]}
        cs.log(f"{name[:26]:26s} CONNECTED {metrics['final_score']:.9f} "
               f"({metrics['final_score'] - CURRENT_BEST:+.2e}) | ic {metrics['ic_mean']:.6f} | "
               f"exc {metrics['annual_excess']:.6f} | turn {metrics['mean_turnover']:.6f} | "
               f"2020-22 {halves['2020_2022'] - REF_HALF_DEV:+.2e} | 2023-24 "
               f"{halves['2023_2024'] - REF_HALF_CONF:+.2e} | refit={needs_refit}")
        dump()
        return metrics["final_score"]

    # ---- harness proof: the shipped promote source. connected_pred_topk IS frac 0.10 finished, so
    # this also proves the rebuild path reproduces the frozen column.
    f010 = finished(0.10)
    frozen_topk = np.load(HERE / TOPK_FIN)
    proofs["frac0.10_equals_frozen_topk"] = {
        "bit_identical": bool(np.array_equal(f010, frozen_topk)),
        "max_abs_diff": float(np.abs(f010 - frozen_topk).max())}
    got = score("frac0.100", f010, False, {"kind": "single_frac", "frac": 0.10,
                                           "role": "harness_proof"})
    proofs["P_frac0.10"] = {"scored": got, "expected": CURRENT_BEST,
                            "abs_diff": abs(got - CURRENT_BEST)}
    if abs(got - CURRENT_BEST) > 1e-12:
        raise AssertionError(f"harness proof failed: {got!r} vs {CURRENT_BEST!r}")
    cs.log("harness proof passed: frac 0.10 reproduces the shipped donor and 0.443190552")

    # ---- A: the filled-in curve
    for frac in (0.125, 0.15, 0.175, 0.20, 0.25):
        score(f"frac{frac:.3f}", finished(frac), frac != 0.10,
              {"kind": "single_frac", "frac": frac})

    # ---- B: blend frac 0.10 with frac 0.20 as the promote source
    f020 = finished(0.20)
    cache_local = {"a": daily_ranks(f010, valid, dates), "b": daily_ranks(f020, valid, dates)}
    for w in BLEND_WEIGHTS:
        mix = weighted_rank_blend([f010, f020], [1.0 - w, w], cache_local, valid, dates, ("a", "b"))
        score(f"blend0.10_0.20_w{w:g}", mix, True,
              {"kind": "k_blend", "fracs": [0.10, 0.20], "weights": [1.0 - w, w]})

    arms = dump()
    payload = json.loads((HERE / "wave36_results.json").read_text(encoding="utf-8"))
    payload["status"] = "complete"
    payload["completed_at_local"] = time.strftime("%Y-%m-%dT%H:%M:%S")
    curve = {float(k[4:]): v["connected_final_score"] for k, v in results.items()
             if k.startswith("frac") and "connected_final_score" in v}
    ordered = sorted(curve.items())
    diffs = [ordered[i + 1][1] - ordered[i][1] for i in range(len(ordered) - 1)]
    payload["curve_ordered"] = [{"frac": f, "connected_final_score": s} for f, s in ordered]
    payload["curve_successive_differences"] = [float(d) for d in diffs]
    payload["curve_is_monotone_or_unimodal"] = bool(
        sum(1 for d in diffs if d > 0) <= 1 or sum(1 for d in diffs if d < 0) <= 1)
    payload["curve_jaggedness_max_abs_second_difference"] = float(
        max(abs(diffs[i + 1] - diffs[i]) for i in range(len(diffs) - 1)) if len(diffs) > 1 else 0.0)
    (HERE / "wave36_results.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print("\n| frac | CONNECTED | margin | IC | excess | turn | 2020-22 | 2023-24 | both? | refit? |")
    print("|---|---|---|---|---|---|---|---|---|---|")
    for s, name, v in arms:
        m = v["connected_metrics"]
        print(f"| {name[:22]} | **{s:.9f}** | {v['margin_full']:+.2e} | {m['ic_mean']:.6f} | "
              f"{m['annual_excess']:.6f} | {m['mean_turnover']:.6f} | "
              f"{v['margin_2020_2022']:+.2e} | {v['margin_2023_2024']:+.2e} | "
              f"{'YES' if v['wins_both_halves'] else 'no'} | "
              f"{'yes' if v['needs_test_fulltrain_refit'] else 'no'} |")
    print("\nK-fraction curve (finer grid):")
    for f, s in ordered:
        print(f"  {f:.3f} -> {s:.9f}")
    print("successive differences: " + ", ".join(f"{d:+.2e}" for d in diffs))
    print(f"max |second difference| (jaggedness): "
          f"{payload['curve_jaggedness_max_abs_second_difference']:.3e}")
    print(f"unimodal: {payload['curve_is_monotone_or_unimodal']}")


if __name__ == "__main__":
    main()
