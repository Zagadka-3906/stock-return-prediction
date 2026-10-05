"""Wave 34: the Top-K-native columns have only ever been used as membership donors. Try them as orderers.

Wave 12 swept "every surviving backbone" in the orderer role at alpha 0 / bonus 0 and found W5a. It did
not include the Top-K pairwise backbone, and the omission was structural rather than deliberate:
`score_wave3.discover()` scans the three preserved trees for `*_seed*_{year}.parquet` and
`final_sweep_eval/*_{year}.parquet`, while the topk caches live in
`experiments/r6_topk_20260926/` and `analysis/topk_training_validation_20261001/` under a different
naming convention. So the one model in this project that is explicitly TRAINED for the Top decile has
only ever been used to decide membership, never to order.

That is worth testing on its own terms, and wave 31 made it more interesting: widening the objective's
fraction from n//10 to n//5 raised the column's global rank quality as well as its Top-decile quality
(hybrid IC 0.116662 -> 0.118424). A column with better whole-cross-section ordering is precisely what
the orderer role wants, since IC reads the whole ordering and the orderer's own turnover is irrelevant.

Arms, all with the shipped nested donor and m = 0.985:
  topk@α0b0        the frozen Top-K backbone at n//10, as sole orderer
  f0.20@α0b0       the frac 0.20 column, as sole orderer
  W5a + w*topk     two-way blends
  W5a + w*f0.20    two-way blends
  SEL + w*f0.20    the SELECTED orderer (W5a + 0.25*slow16) plus frac 0.20 as a third member
Harness proof: the selected orderer with no third member must reproduce 0.443190552 exactly.

Every input is a fold column that already exists or is rebuilt here from frozen raws by the same
`make_prediction_param` path whose identity with the production stack was proved in wave 6 and re-proved
in the submission builder. Test-period deliverability is NOT claimed for the frac 0.20 column: its test
counterpart would need a fulltrain re-fit, which is recorded in wave 31's protocol. Arms that need it are
flagged so the selection can weigh that.

Selection is 后续选模标准.md §3/§4. Both-halves decomposition is reported for every arm because waves
23/25/26/31 all produced full-window gains that were redistribution between halves. No test-period data
is read here.
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
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(HERE))
import connected_scorer as cs  # noqa: E402
from experiments.revalidate_fold_local import score_official  # noqa: E402
from optimize_wave6 import make_prediction_param, fold_frame  # noqa: E402
from optimize_wave8 import topk_raw  # noqa: E402
from optimize_wave13 import build_ab  # noqa: E402
from optimize_wave15 import daily_ranks, weighted_rank_blend, DONOR, M_FRAC, TIE_EPS  # noqa: E402
from src.scoring import Panel  # noqa: E402

YEARS = cs.YEARS
W5A_A0B0 = "orderer_a0b0_W5a_five_way_with_gru__final_sweep_eval.npy"
SLOW16_A0B0 = "pp_a0_b0_top_only_w0.25_rl1_tcw1.npy"
FRAC20_DIR = HERE / "wave31_topk/raw"
SETTING = {"alpha": 0.0, "bonus": 0.0, "mode": "top_only", "weight": 0.25,
           "restore_lower": True, "top_current_weight": 1.0}
PARTNER_WEIGHT = 0.25
BLEND_WEIGHTS = (0.15, 0.25, 0.35)
CURRENT_BEST = 0.44319055217888365
REF_HALF_DEV = 0.442705356
REF_HALF_CONF = 0.443926938


def sha(path) -> str:
    value = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for chunk in iter(lambda: stream.read(8 * 1024 * 1024), b""):
            value.update(chunk)
    return value.hexdigest()


def main() -> None:
    protocol_path = HERE / "protocol_wave34.json"
    if not protocol_path.exists():
        protocol_path.write_text(json.dumps({
            "frozen_at_local": time.strftime("%Y-%m-%dT%H:%M:%S"),
            "standard": "后续选模标准.md §3 connected composite primary; §4 highest score wins",
            "status": "in_sample_selection_disclosed",
            "hypothesis": "the Top-K pairwise backbone is the only model here explicitly trained for the "
                          "Top decile, and it has only ever been used to decide membership. Wave 12's "
                          "orderer sweep missed it because discover() does not scan the r6_topk / "
                          "topk_training_validation naming convention. Wave 31 also showed that "
                          "widening the objective's fraction improves the column's GLOBAL ordering, "
                          "which is what the orderer role rewards.",
            "arms": ["topk@alpha0/bonus0 as sole orderer", "frac0.20@alpha0/bonus0 as sole orderer",
                     "W5a + w*topk", "W5a + w*frac0.20", "selected orderer + w*frac0.20"],
            "blend_weights": list(BLEND_WEIGHTS),
            "donor_fixed": {"column": DONOR, "provenance": "wave 13 stage 2 argmax"},
            "m_frac_fixed_at": M_FRAC, "tie_break_eps": TIE_EPS,
            "orderer_postprocess": SETTING,
            "harness_proof": f"the selected orderer (W5a + {PARTNER_WEIGHT}*slow16) with no third "
                             f"member must reproduce {CURRENT_BEST}",
            "deliverability": {
                "topk_at_n_over_10": "shippable - its test-period finished column is "
                                     "middle/predictions/supplemental_topk_fulltrain2024.parquet, and "
                                     "the raw is reproducible via middle/run_middle.py::supplemental_topk",
                "frac_0.20": "NOT shippable without a test-period fulltrain re-fit; flagged per arm",
            },
            "current_best_before_this_wave": CURRENT_BEST,
            "shipping_rule_declared_in_advance": f"report the both-halves decomposition against "
                                                 f"{REF_HALF_DEV:.9f} / {REF_HALF_CONF:.9f}; a "
                                                 "full-window-only win is not evidence",
            "selection_rule": "highest connected 2020-2024 official composite; no other gate",
            "disclosed_selection_cost": "search over the same five repeatedly viewed years; no blind "
                                        "period remains",
            "causality": "every orderer column is a walk-forward fold prediction; the blend reads only "
                         "same-day predictions and the price-valid mask. No label is read.",
            "no_test_period_data_read": True,
            "source_sha256": sha(Path(__file__)),
        }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        cs.log(f"wave-34 protocol frozen: {sha(protocol_path)[:16]}…")

    combined = cs.combined_frame()
    dates = combined["trade_date"].to_numpy()
    flags = combined["flag_limit_up"].to_numpy().astype(np.int64)
    valid = combined["price_valid"].to_numpy().astype(bool)
    codes, uniques = pd.factorize(combined["ts_code"].to_pandas(), sort=True)
    codes = codes.astype(np.int64)
    n_codes = len(uniques)
    tie_key = 1.0 - codes / max(n_codes - 1, 1)
    member = np.load(HERE / DONOR)
    frames = {yy: fold_frame(yy) for yy in YEARS}
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
                                             SETTING["mode"], SETTING["weight"], SETTING["alpha"],
                                             SETTING["bonus"], SETTING["restore_lower"],
                                             SETTING["top_current_weight"]))
            del panel
            gc.collect()
        return np.concatenate(out)

    # ---- build the two Top-K orderer columns
    topk_raws, f20_raws = {}, {}
    for yy in YEARS:
        source, raw = topk_raw(yy)
        if not source.select(cs.KEYS).equals(frames[yy].select(cs.KEYS)):
            raise AssertionError(f"topk {yy}: keys misaligned with the fold frame")
        topk_raws[yy] = raw
        path = FRAC20_DIR / f"topk_seed2026_f0.20_{yy}.parquet"
        if not path.exists():
            raise SystemExit(f"missing {path.name}; run optimize_wave31.py train --fracs 0.20 first")
        df = pl.read_parquet(path).sort("trade_date", "ts_code")
        if not df.select(cs.KEYS).equals(frames[yy].select(cs.KEYS)):
            raise AssertionError(f"frac0.20 {yy}: keys misaligned with the fold frame")
        f20_raws[yy] = df["pred_raw"].to_numpy().astype(np.float64)
    topk_a0b0 = postprocess(topk_raws)
    f20_a0b0 = postprocess(f20_raws)
    np.save(HERE / "orderer_a0b0_topk.npy", topk_a0b0)
    np.save(HERE / "orderer_a0b0_topk_frac0.20.npy", f20_a0b0)

    # the frozen topk finished column is the harness anchor for the topk rebuild: re-post-processing
    # the topk raw at the RELEASED settings must reproduce connected_pred_topk.npy bit-for-bit
    released_parts = []
    for yy in YEARS:
        frame = frames[yy]
        panel = Panel.from_frame(frame.with_columns(pl.Series("pred_raw", topk_raws[yy])))
        released_parts.append(make_prediction_param(panel, frame["aux_raw"].to_numpy().astype(np.float64),
                                                    "top_only", 0.25, 0.9, 0.3, True, 1.0))
        del panel
    frozen_topk = np.load(HERE / "connected_pred_topk.npy")
    rebuilt_released = np.concatenate(released_parts)
    if not np.array_equal(rebuilt_released, frozen_topk):
        raise AssertionError("the topk raw rebuild does not reproduce connected_pred_topk.npy "
                             f"(max diff {np.abs(rebuilt_released - frozen_topk).max():.3e})")
    cs.log("anchor passed: the topk raw through the released stack reproduces connected_pred_topk.npy "
           "bit-for-bit")

    w5a = np.load(HERE / W5A_A0B0)
    slow16 = np.load(HERE / SLOW16_A0B0)
    rank_cache = {}

    def ranks(name: str, column: np.ndarray) -> np.ndarray:
        if name not in rank_cache:
            rank_cache[name] = daily_ranks(column, valid, dates)
        return rank_cache[name]

    for name, col in (("w5a", w5a), ("slow16", slow16), ("topk", topk_a0b0), ("f20", f20_a0b0)):
        ranks(name, col)

    selected = weighted_rank_blend([w5a, slow16], [1 - PARTNER_WEIGHT, PARTNER_WEIGHT], rank_cache,
                                   valid, dates, ("w5a", "slow16"))
    selected = np.where(selected > -9.0, selected + TIE_EPS * tie_key, selected)

    results: dict = {}
    proofs: dict = {"topk_raw_rebuild_anchor": {
        "bit_identical_to_connected_pred_topk": True,
        "target_sha256": sha(HERE / "connected_pred_topk.npy")}}

    def dump() -> list:
        arms = sorted(((v["connected_final_score"], k, v) for k, v in results.items()
                       if "connected_final_score" in v), reverse=True)
        payload = {"status": "running", "updated_at_local": time.strftime("%Y-%m-%dT%H:%M:%S"),
                   "purpose": "test the Top-K-native columns in the orderer role, which wave 12 missed",
                   "donor_fixed": DONOR, "m_frac": M_FRAC, "tie_break_eps": TIE_EPS,
                   "harness_proofs": proofs, "current_best_before_this_wave": CURRENT_BEST,
                   "reference_halves": {"2020_2022": REF_HALF_DEV, "2023_2024": REF_HALF_CONF},
                   "results": results, "n_scored": len(arms),
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
                   "best_shippable": next((k for s, k, v in arms
                                           if not v["needs_test_fulltrain_refit"]), None),
                   "no_test_period_data_read": True, "source_sha256": sha(Path(__file__))}
        (HERE / "wave34_results.json").write_text(
            json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        return arms

    def score(name: str, orderer: np.ndarray, needs_refit: bool, extra: dict) -> float:
        orderer_tb = np.where(orderer > -9.0, orderer + TIE_EPS * tie_key, orderer) + TIE_EPS * tie_key
        hybrid, stats = build_ab(member, orderer_tb, orderer_tb, dates, flags, codes, n_codes, M_FRAC)
        metrics, _ = score_official(combined, hybrid)
        halves = {}
        for label, mask in half.items():
            sub, _ = score_official(combined.filter(pl.Series(mask)), hybrid[mask])
            halves[label] = sub["final_score"]
        results[name] = {**extra, "needs_test_fulltrain_refit": needs_refit,
                         "connected_final_score": metrics["final_score"],
                         "connected_metrics": metrics, "halves": halves,
                         "margin_full": metrics["final_score"] - CURRENT_BEST,
                         "margin_2020_2022": halves["2020_2022"] - REF_HALF_DEV,
                         "margin_2023_2024": halves["2023_2024"] - REF_HALF_CONF,
                         "wins_both_halves": bool(halves["2020_2022"] > REF_HALF_DEV
                                                  and halves["2023_2024"] > REF_HALF_CONF),
                         "boundary_tie_days": stats["boundary_tie_days"],
                         "mean_retention_ratio": stats["mean_retention_ratio"]}
        cs.log(f"{name[:28]:28s} CONNECTED {metrics['final_score']:.9f} "
               f"({metrics['final_score'] - CURRENT_BEST:+.2e}) | ic {metrics['ic_mean']:.6f} | "
               f"exc {metrics['annual_excess']:.6f} | turn {metrics['mean_turnover']:.6f} | "
               f"2020-22 {halves['2020_2022'] - REF_HALF_DEV:+.2e} | 2023-24 "
               f"{halves['2023_2024'] - REF_HALF_CONF:+.2e} | refit={needs_refit}")
        dump()
        return metrics["final_score"]

    # ---- harness proof first
    got = score("P_selected_orderer", selected, False,
                {"kind": "harness_proof", "components": ["W5a", "slow16"],
                 "weights": [1 - PARTNER_WEIGHT, PARTNER_WEIGHT]})
    proofs["P_selected_orderer"] = {"scored": got, "expected": CURRENT_BEST,
                                    "abs_diff": abs(got - CURRENT_BEST)}
    if abs(got - CURRENT_BEST) > 1e-12:
        raise AssertionError(f"harness proof failed: {got!r} vs {CURRENT_BEST!r}")
    cs.log("harness proof passed: the selected orderer reproduces 0.443190552")

    # ---- sole-orderer quality reads
    score("topk_a0b0_alone", topk_a0b0, False, {"kind": "sole_orderer", "column": "topk@n//10"})
    score("f0.20_a0b0_alone", f20_a0b0, True, {"kind": "sole_orderer", "column": "topk@frac0.20"})

    # ---- two-way blends
    for w in BLEND_WEIGHTS:
        score(f"W5a+topk_w{w:g}",
              weighted_rank_blend([w5a, topk_a0b0], [1 - w, w], rank_cache, valid, dates,
                                  ("w5a", "topk")), False,
              {"kind": "two_way", "components": ["W5a", "topk@n//10"], "weights": [1 - w, w]})
        score(f"W5a+f0.20_w{w:g}",
              weighted_rank_blend([w5a, f20_a0b0], [1 - w, w], rank_cache, valid, dates,
                                  ("w5a", "f20")), True,
              {"kind": "two_way", "components": ["W5a", "topk@frac0.20"], "weights": [1 - w, w]})

    # ---- three-way on top of the selection
    for w in BLEND_WEIGHTS:
        score(f"SEL+f0.20_w{w:g}",
              weighted_rank_blend([w5a, slow16, f20_a0b0],
                                  [(1 - PARTNER_WEIGHT) * (1 - w), PARTNER_WEIGHT * (1 - w), w],
                                  rank_cache, valid, dates, ("w5a", "slow16", "f20")), True,
              {"kind": "three_way", "components": ["W5a", "slow16", "topk@frac0.20"],
               "weights": [(1 - PARTNER_WEIGHT) * (1 - w), PARTNER_WEIGHT * (1 - w), w]})
        score(f"SEL+topk_w{w:g}",
              weighted_rank_blend([w5a, slow16, topk_a0b0],
                                  [(1 - PARTNER_WEIGHT) * (1 - w), PARTNER_WEIGHT * (1 - w), w],
                                  rank_cache, valid, dates, ("w5a", "slow16", "topk")), False,
              {"kind": "three_way", "components": ["W5a", "slow16", "topk@n//10"],
               "weights": [(1 - PARTNER_WEIGHT) * (1 - w), PARTNER_WEIGHT * (1 - w), w]})

    arms = dump()
    payload = json.loads((HERE / "wave34_results.json").read_text(encoding="utf-8"))
    payload["status"] = "complete"
    payload["completed_at_local"] = time.strftime("%Y-%m-%dT%H:%M:%S")
    (HERE / "wave34_results.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print("\n| arm | CONNECTED | margin | IC | excess | turn | 2020-22 | 2023-24 | both? | refit? |")
    print("|---|---|---|---|---|---|---|---|---|---|")
    for s, name, v in arms:
        m = v["connected_metrics"]
        print(f"| {name[:22]} | **{s:.9f}** | {v['margin_full']:+.2e} | {m['ic_mean']:.6f} | "
              f"{m['annual_excess']:.6f} | {m['mean_turnover']:.6f} | "
              f"{v['margin_2020_2022']:+.2e} | {v['margin_2023_2024']:+.2e} | "
              f"{'YES' if v['wins_both_halves'] else 'no'} | "
              f"{'yes' if v['needs_test_fulltrain_refit'] else 'no'} |")
    cs.log(f"best: {arms[0][1]} {arms[0][0]:.9f} | best shippable without a refit: "
           f"{payload['best_shippable']}")


if __name__ == "__main__":
    main()
