"""Wave 35: the last untested slot in the construction - what re-ranks INSIDE the promoted block.

The construction has eight slots and seven are now searched: the promote source (wave 13, 30 candidates;
wave 31, 8 K fractions), the promote width (wave 28, 5 values), the outer orderer (waves 12, 15, 16, 20,
22, 27, 32, 34), the retention floor (waves 13, 17, 19, 20, 23, 25, 26), the swap-budget rule (waves 17,
19), the limit-up shift (wave 29), and the return map (score-neutral by construction, proved). The
eighth is the column that re-ranks inside the promoted block.

Wave 18 tried three re-rankers - slow16 finished, W5a finished, and a blend of the two - and they span
only 4.5e-4 (0.442265 to 0.442714 against the shipped slow16 at 0.442481), which is why the slot looked
unimportant. But that was before wave 31 showed the Top-K columns exist at several fractions, and wave 34
showed something specific about them: as a SOLE orderer the frac 0.20 column is poor (hybrid IC
0.068772), because it is a specialist Top-decile picker rather than a global ranker. The re-ranker slot
is the one place in the construction where a specialist picker is exactly the right tool - its only job
is to order a block of ~457 already-promoted names so the swap-budget solve keeps the right ones.

Arms, all with the shipped promote source (topk at n//10), q = 0.10, the selected outer orderer and
m = 0.985:
  slow16                the shipped re-ranker, and the harness proof
  topk@n//10            the promote source re-ranking its own block
  topk@frac0.20         the wave-31 column, in the role it is actually suited to
  blend(slow16, f0.20)  weights 0.25 / 0.50 / 0.75 on f0.20
  blend(slow16, W5a)    wave 18's best, re-run here so all arms share one code path
Harness proof: the slow16 re-ranker must reproduce 0.443190552 exactly.

Note the re-ranker's tie-break question is settled rather than assumed here, because wave 28 asserted it
and was wrong by 1.01e-4: blended re-rankers get the causal tie-break, unblended ones do not, and the
harness proof is what makes the unblended case comparable to the frozen donor.

Deliverability per arm is recorded, not assumed: anything using frac 0.20 needs a test-period fulltrain
re-fit of the Top-K model. Selection is 后续选模标准.md §3/§4, with the both-halves decomposition
reported for every arm. No test-period data is read here.
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
from experiments.revalidate_fold_local import score_official  # noqa: E402
from optimize_wave13 import build_ab  # noqa: E402
from optimize_wave15 import daily_ranks, weighted_rank_blend, DONOR, M_FRAC, TIE_EPS  # noqa: E402
from optimize_wave18 import lift  # noqa: E402

YEARS = cs.YEARS
W5A_A0B0 = "orderer_a0b0_W5a_five_way_with_gru__final_sweep_eval.npy"
SLOW16_A0B0 = "pp_a0_b0_top_only_w0.25_rl1_tcw1.npy"
SLOW16_FIN = "connected_pred_peer67_slow16.npy"
W5A_FIN = "connected_pred_W5a_five_way_with_gru__final_sweep_eval.npy"
TOPK_A0B0 = "orderer_a0b0_topk.npy"
F20_A0B0 = "orderer_a0b0_topk_frac0.20.npy"
TOPK_FIN = "connected_pred_topk.npy"
NESTED = "connected_pred_hybrid.npy"
PARTNER_WEIGHT = 0.25
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
    protocol_path = HERE / "protocol_wave35.json"
    if not protocol_path.exists():
        protocol_path.write_text(json.dumps({
            "frozen_at_local": time.strftime("%Y-%m-%dT%H:%M:%S"),
            "standard": "后续选模标准.md §3 connected composite primary; §4 highest score wins",
            "status": "in_sample_selection_disclosed",
            "hypothesis": "the re-ranker inside the promoted block is the last unsearched slot. Wave 34 "
                          "showed the Top-K columns are poor GLOBAL rankers (frac 0.20 alone gives "
                          "hybrid IC 0.068772) because they are specialist Top-decile pickers - and "
                          "this slot is the one place where a specialist picker is the right tool, since "
                          "its only job is to order ~457 already-promoted names so the swap-budget solve "
                          "keeps the right ones.",
            "why_wave18_underestimated_this_slot": "wave 18 tried only slow16, W5a and their blend, "
                                                   "which span 4.5e-4. It predates wave 31's K fractions "
                                                   "and wave 34's finding about what those columns are "
                                                   "good for.",
            "fixed": {"promote_source": TOPK_FIN, "q": 0.10, "outer_orderer": [W5A_A0B0, SLOW16_A0B0],
                      "outer_weights": [1 - PARTNER_WEIGHT, PARTNER_WEIGHT], "m_frac": M_FRAC,
                      "tie_break_eps": TIE_EPS},
            "rerankers": ["slow16_finished (shipped, harness proof)", "topk@n//10 at alpha0/bonus0",
                          "topk@frac0.20 at alpha0/bonus0",
                          "blend(slow16, frac0.20) at 0.25/0.50/0.75",
                          "blend(slow16, W5a) at 0.25, re-run for a common code path"],
            "tie_break_policy": "blended re-rankers get the causal code-rank tie-break, unblended ones "
                                "do not, so the unblended slow16 arm is directly comparable to the "
                                "frozen donor. Wave 28 asserted the tie-break was inert and was wrong by "
                                "1.01e-4, so this is settled by the harness proof rather than assumed.",
            "harness_proof": f"the slow16 re-ranker must reproduce {CURRENT_BEST} exactly",
            "deliverability": "arms using frac 0.20 need a test-period fulltrain re-fit of the Top-K "
                              "model; flagged per arm rather than assumed away",
            "current_best_before_this_wave": CURRENT_BEST,
            "shipping_rule_declared_in_advance": f"report both halves against {REF_HALF_DEV:.9f} / "
                                                 f"{REF_HALF_CONF:.9f}; a full-window-only win is not "
                                                 "evidence",
            "selection_rule": "highest connected 2020-2024 official composite; no other gate",
            "disclosed_selection_cost": "search over the same five repeatedly viewed years; no blind "
                                        "period remains",
            "causality": "the lift reads only same-day finished predictions and same-day limit-up flags. "
                         "No label is read.",
            "no_test_period_data_read": True,
            "source_sha256": sha(Path(__file__)),
        }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        cs.log(f"wave-35 protocol frozen: {sha(protocol_path)[:16]}…")

    combined = cs.combined_frame()
    dates = combined["trade_date"].to_numpy()
    flags = combined["flag_limit_up"].to_numpy().astype(np.int64)
    valid = combined["price_valid"].to_numpy().astype(bool)
    codes, uniques = pd.factorize(combined["ts_code"].to_pandas(), sort=True)
    codes = codes.astype(np.int64)
    n_codes = len(uniques)
    tie_key = 1.0 - codes / max(n_codes - 1, 1)
    pdf = combined.select(["trade_date", "flag_limit_up"]).to_pandas()

    promote = np.load(HERE / TOPK_FIN)
    slow16_fin = np.load(HERE / SLOW16_FIN)
    w5a_fin = np.load(HERE / W5A_FIN)
    for stem in (TOPK_A0B0, F20_A0B0):
        if not (HERE / stem).exists():
            raise SystemExit(f"missing {stem}; run optimize_wave34.py first")
    topk_a0b0 = np.load(HERE / TOPK_A0B0)
    f20_a0b0 = np.load(HERE / F20_A0B0)

    w5a = np.load(HERE / W5A_A0B0)
    slow16 = np.load(HERE / SLOW16_A0B0)
    rank_cache = {}
    for name, col in (("w5a", w5a), ("slow16", slow16), ("slow16fin", slow16_fin),
                      ("w5afin", w5a_fin), ("topk", topk_a0b0), ("f20", f20_a0b0)):
        rank_cache[name] = daily_ranks(col, valid, dates)
    blended = weighted_rank_blend([w5a, slow16], [1 - PARTNER_WEIGHT, PARTNER_WEIGHT], rank_cache,
                                  valid, dates, ("w5a", "slow16"))
    orderer = np.where(blended > -9.0, blended + TIE_EPS * tie_key, blended) + TIE_EPS * tie_key

    masks = {str(yy): (dates >= yy * 10000 + 101) & (dates <= yy * 10000 + 1231) for yy in YEARS}
    half = {"2020_2022": np.zeros(len(dates), dtype=bool),
            "2023_2024": np.zeros(len(dates), dtype=bool)}
    for yy in (2020, 2021, 2022):
        half["2020_2022"] |= masks[str(yy)]
    for yy in (2023, 2024):
        half["2023_2024"] |= masks[str(yy)]

    results: dict = {}
    proofs: dict = {}

    def dump() -> list:
        arms = sorted(((v["connected_final_score"], k, v) for k, v in results.items()
                       if "connected_final_score" in v), reverse=True)
        payload = {"status": "running", "updated_at_local": time.strftime("%Y-%m-%dT%H:%M:%S"),
                   "purpose": "search the re-ranker slot inside the promoted block",
                   "promote_source": TOPK_FIN, "q": 0.10, "m_frac": M_FRAC,
                   "tie_break_eps": TIE_EPS, "harness_proofs": proofs,
                   "current_best_before_this_wave": CURRENT_BEST,
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
        (HERE / "wave35_results.json").write_text(
            json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        return arms

    def score(name: str, reranker: np.ndarray, needs_refit: bool, extra: dict) -> float:
        donor, lift_stats = lift(promote, reranker, pdf)
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
        cs.log(f"{name[:30]:30s} CONNECTED {metrics['final_score']:.9f} "
               f"({metrics['final_score'] - CURRENT_BEST:+.2e}) | ic {metrics['ic_mean']:.6f} | "
               f"exc {metrics['annual_excess']:.6f} | turn {metrics['mean_turnover']:.6f} | "
               f"2020-22 {halves['2020_2022'] - REF_HALF_DEV:+.2e} | 2023-24 "
               f"{halves['2023_2024'] - REF_HALF_CONF:+.2e} | refit={needs_refit}")
        dump()
        return metrics["final_score"]

    # ---- harness proof: the shipped re-ranker
    got = score("P_slow16_reranker", slow16_fin, False,
                {"reranker": "slow16_finished", "role": "harness_proof"})
    donor_ref, _ = lift(promote, slow16_fin, pdf)
    proofs["P_slow16_reproduces_the_shipped_donor"] = {
        "scored": got, "expected": CURRENT_BEST, "abs_diff": abs(got - CURRENT_BEST),
        "donor_bit_identical_to_frozen_nested": bool(
            np.array_equal(donor_ref, np.load(HERE / NESTED))),
        "donor_max_abs_diff": float(np.abs(donor_ref - np.load(HERE / NESTED)).max())}
    if abs(got - CURRENT_BEST) > 1e-12:
        raise AssertionError(f"harness proof failed: {got!r} vs {CURRENT_BEST!r}")
    cs.log("harness proof passed: the slow16 re-ranker reproduces the shipped donor and 0.443190552")

    def blended_reranker(other: np.ndarray, other_name: str, w: float) -> np.ndarray:
        mix = weighted_rank_blend([slow16_fin, other], [1.0 - w, w], rank_cache, valid, dates,
                                  ("slow16fin", other_name))
        return np.where(mix > -9.0, mix + TIE_EPS * tie_key, mix)

    score("rerank_topk_a0b0", topk_a0b0, False, {"reranker": "topk@n//10 at alpha0/bonus0"})
    score("rerank_f0.20_a0b0", f20_a0b0, True, {"reranker": "topk@frac0.20 at alpha0/bonus0"})
    score("rerank_promote_source", promote, False,
          {"reranker": "topk finished (the promote source re-ranking its own block)"})
    for w in (0.25, 0.50, 0.75):
        score(f"rerank_blend_slow16+f0.20_w{w:g}", blended_reranker(f20_a0b0, "f20", w), True,
              {"reranker": f"blend(slow16, frac0.20, {w}) + tie-break"})
    score("rerank_blend_slow16+W5a_w0.25", blended_reranker(w5a_fin, "w5afin", 0.25), False,
          {"reranker": "blend(slow16, W5a finished, 0.25) + tie-break"})

    arms = dump()
    payload = json.loads((HERE / "wave35_results.json").read_text(encoding="utf-8"))
    payload["status"] = "complete"
    payload["completed_at_local"] = time.strftime("%Y-%m-%dT%H:%M:%S")
    (HERE / "wave35_results.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("\n| re-ranker | CONNECTED | margin | IC | excess | turn | 2020-22 | 2023-24 | both? | refit? |")
    print("|---|---|---|---|---|---|---|---|---|---|")
    for s, name, v in arms:
        m = v["connected_metrics"]
        print(f"| {name[:32]} | **{s:.9f}** | {v['margin_full']:+.2e} | {m['ic_mean']:.6f} | "
              f"{m['annual_excess']:.6f} | {m['mean_turnover']:.6f} | "
              f"{v['margin_2020_2022']:+.2e} | {v['margin_2023_2024']:+.2e} | "
              f"{'YES' if v['wins_both_halves'] else 'no'} | "
              f"{'yes' if v['needs_test_fulltrain_refit'] else 'no'} |")
    cs.log(f"best: {arms[0][1]} {arms[0][0]:.9f} | best shippable without a refit: "
           f"{payload['best_shippable']}")


if __name__ == "__main__":
    main()
