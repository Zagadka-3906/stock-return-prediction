"""Wave 18: the nested donor won because it is a CONSENSUS. Search the consensus, not just its parts.

Wave 13 stage 2 moved the membership donor from plain topk (0.441064514) to wave 1's nested lift
(0.442481207), and it won on all three terms at once rather than trading one for another. The mechanism
is why: the lift promotes topk's Top decile and then re-ranks that block by peer67_slow16, so the outer
swap-budget solve picks the top n_top by slow16 FROM WITHIN topk's Top decile. The realized Top set is
therefore a consensus - names both models put in the top tenth - which is sharper than either alone.

Every wave so far treated the nested donor as one fixed artifact. But it has three interchangeable
slots: which column supplies the promoted block, which column re-ranks inside it, and whether either
should itself be a blend. None of that has been searched. The three rank-blended donors wave 13 did test
(hybrid_k1/k2) peaked at 0.442265, just below the nested 0.442481, which says the *structure* of the
lift matters more than the blend weight inside it - so the structure is what should be varied.

All inputs are finished columns that exist for the test period (slow16 = the delivery's own rank_score,
topk = supplemental_topk_fulltrain2024.parquet, W5a = all_models_test row 138, reconstructible and
proved), so every arm here is shippable. That is checked explicitly rather than assumed.

Harness proof: variant (a) must reproduce connected_pred_hybrid.npy bit-for-bit and score
0.442481207 with the frozen orderer, since it IS the shipped donor built by the shipped code path.

Selection is 后续选模标准.md §3/§4: highest connected 2020-2024 official composite, no other gate.
No test-period data is read anywhere in this file.
"""
from __future__ import annotations

import hashlib
import json
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(HERE))
import connected_scorer as cs  # noqa: E402
from experiments.revalidate_fold_local import score_official  # noqa: E402
from optimize_wave13 import build_ab  # noqa: E402
from optimize_wave15 import daily_ranks, weighted_rank_blend, M_FRAC, TIE_EPS  # noqa: E402
from analysis.topset_hybrid_20261002 import fold_validation as fv  # noqa: E402

CURRENT_BEST = 0.4424812067218111
CURRENT_BEST_NAME = "nested_x_W5a_a0_b0_m0.985_tiebreak"
SLOW16 = "connected_pred_peer67_slow16.npy"
TOPK = "connected_pred_topk.npy"
W5A_FIN = "connected_pred_W5a_five_way_with_gru__final_sweep_eval.npy"
BLEND_WEIGHTS = (0.25, 0.50)


def sha(path) -> str:
    value = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for chunk in iter(lambda: stream.read(8 * 1024 * 1024), b""):
            value.update(chunk)
    return value.hexdigest()


def lift(promoted_source: np.ndarray, reranker: np.ndarray, pdf) -> tuple[np.ndarray, dict]:
    """Wave 1's lift, via the same fv.top_sets that produced the frozen column."""
    promoted, stats = fv.top_sets(pdf, promoted_source)
    if stats["boundary_tie_days"]:
        raise AssertionError(f"the promoted source has {stats['boundary_tie_days']} tie days")
    span = float(reranker.max() - reranker.min())
    out = promoted.astype(np.float64) * (span + 1.0) + reranker
    check, _ = fv.top_sets(pdf, out)
    if not np.array_equal(check, promoted):
        raise AssertionError("the lifted column's Top set is not exactly the promoted block")
    return out, {"span": span, "promoted_rows": int(promoted.sum()),
                 "promoted_share": float(promoted.mean()), "days": stats["days"]}


def main() -> None:
    orderer_stem = sys.argv[1] if len(sys.argv) > 1 else "orderer_a0b0_W5a_five_way_with_gru__final_sweep_eval"
    orderer_path = HERE / f"{orderer_stem}.npy"
    if not orderer_path.exists():
        raise SystemExit(f"no saved orderer column: {orderer_path}")

    protocol_path = HERE / "protocol_wave18.json"
    if not protocol_path.exists():
        protocol_path.write_text(json.dumps({
            "frozen_at_local": time.strftime("%Y-%m-%dT%H:%M:%S"),
            "supersedes": "protocol_wave18_superseded_001.json; see "
                          "protocol_wave18_amendment_001.json and failure_wave18_run_*.log",
            "defect_fixed": "the first run built every donor variant eagerly, outside the guarded "
                            "scoring loop, so one variant's failure aborted the whole wave. It also "
                            "passed a rank-BLENDED column to fv.top_sets as the promoted source "
                            "without a tie-break; averaging two per-day rank columns creates exact "
                            "ties, and 71 of 1212 days tied across the promotion boundary, which the "
                            "lift correctly refuses. Fixed by making variant construction lazy inside "
                            "the guard and by applying the project's standard causal tie-break to any "
                            "blended column before it is used as a promote source or a re-ranker.",
            "standard": "后续选模标准.md §3 connected composite primary; §4 highest score wins",
            "status": "in_sample_selection_disclosed",
            "hypothesis": "the nested donor is a consensus: topk supplies the promoted block, slow16 "
                          "re-ranks inside it, and the outer solve truncates. Its three slots have "
                          "never been varied. Search which column promotes, which re-ranks, and "
                          "whether either should be a blend.",
            "variants": {
                "a_nested_shipped": "lift(topk promotes, slow16 re-ranks) - the shipped donor",
                "b_rerank_blend": "lift(topk promotes, rank-blend(slow16, W5a) re-ranks)",
                "c_promote_blend": "lift(rank-blend(topk, W5a) promotes, slow16 re-ranks)",
                "d_w5a_reranks": "lift(topk promotes, W5a re-ranks)",
                "e_slow16_promotes": "lift(slow16 promotes, topk re-ranks) - the slots swapped",
                "f_w5a_promotes": "lift(W5a promotes, slow16 re-ranks)",
            },
            "blend_weights": list(BLEND_WEIGHTS),
            "tie_break_eps": TIE_EPS,
            "tie_break_key": "1 - ts_code_rank/(n_codes-1), causal and label-free; applied to blended "
                             "columns only, since the unblended finished columns have no boundary ties",
            "orderer_fixed": orderer_stem,
            "m_frac_fixed_at": M_FRAC,
            "harness_proof": f"variant a must reproduce connected_pred_hybrid.npy bit-for-bit and "
                             f"score {CURRENT_BEST} with this orderer",
            "deliverability": "every input is a finished column that exists for the test period, so "
                              "every variant is shippable",
            "current_best_before_this_wave": {"name": CURRENT_BEST_NAME,
                                              "connected_final_score": CURRENT_BEST},
            "selection_rule": "highest connected 2020-2024 official composite; no other gate",
            "disclosed_selection_cost": "search over the same five repeatedly viewed years; no blind "
                                        "period remains and the winner carries upward selection bias "
                                        "this protocol cannot quantify",
            "causality": "the lift reads only same-day finished predictions and same-day limit-up "
                         "flags. No label is read.",
            "no_test_period_data_read": True,
            "source_sha256": sha(Path(__file__)),
        }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        cs.log(f"wave-18 protocol re-frozen: {sha(protocol_path)[:16]}…")

    frame = cs.combined_frame()
    dates = frame["trade_date"].to_numpy()
    flags = frame["flag_limit_up"].to_numpy().astype(np.int64)
    valid = frame["price_valid"].to_numpy().astype(bool)
    codes, uniques = pd.factorize(frame["ts_code"].to_pandas(), sort=True)
    codes = codes.astype(np.int64)
    n_codes = len(uniques)
    tie_key = 1.0 - codes / max(n_codes - 1, 1)
    pdf = frame.select(["trade_date", "flag_limit_up"]).to_pandas()
    orderer = np.load(orderer_path) + TIE_EPS * tie_key

    slow16 = np.load(HERE / SLOW16)
    topk = np.load(HERE / TOPK)
    w5a = np.load(HERE / W5A_FIN)
    frozen_hybrid = np.load(HERE / "connected_pred_hybrid.npy")

    rank_cache: dict = {}

    def blend(a: np.ndarray, b: np.ndarray, name_a: str, name_b: str, w: float) -> np.ndarray:
        """Per-day weighted rank blend, plus the project's causal tie-break.

        Averaging two rank columns creates exact ties, and fv.top_sets refuses a promoted source with a
        boundary tie. The tie-break is the same one used everywhere else: 1e-9 scaled by the stock's own
        code rank, which is causal and reads no label.
        """
        for stem, col in ((name_a, a), (name_b, b)):
            if stem not in rank_cache:
                rank_cache[stem] = daily_ranks(col, valid, dates)
        mixed = weighted_rank_blend([a, b], [1.0 - w, w], rank_cache, valid, dates, (name_a, name_b))
        return np.where(mixed > -9.0, mixed + TIE_EPS * tie_key, mixed)

    results: dict = {}
    proofs: dict = {}

    def dump() -> list:
        arms = sorted(((v["connected_final_score"], k, v) for k, v in results.items()
                       if "connected_final_score" in v), reverse=True)
        payload = {"status": "running", "updated_at_local": time.strftime("%Y-%m-%dT%H:%M:%S"),
                   "purpose": "search the nested donor's three slots: what promotes, what re-ranks, "
                              "and whether either is a blend",
                   "orderer_fixed": orderer_stem, "m_frac": M_FRAC, "tie_break_eps": TIE_EPS,
                   "harness_proofs": proofs,
                   "current_best_before_this_wave": {"name": CURRENT_BEST_NAME,
                                                     "connected_final_score": CURRENT_BEST},
                   "results": results, "n_scored": len(arms),
                   "ranking": [{"arm": k, "connected_final_score": s,
                                "ic_mean": v["connected_metrics"]["ic_mean"],
                                "annual_excess": v["connected_metrics"]["annual_excess"],
                                "mean_turnover": v["connected_metrics"]["mean_turnover"]}
                               for s, k, v in arms[:25]],
                   "best": arms[0][1] if arms else None,
                   "best_connected_final_score": arms[0][0] if arms else None,
                   "improves_on_current_best": bool(arms and arms[0][0] > CURRENT_BEST),
                   "no_test_period_data_read": True,
                   "source_sha256": sha(Path(__file__))}
        (HERE / "wave18_results.json").write_text(
            json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        return arms

    def score(name: str, donor: np.ndarray, extra: dict) -> float:
        hybrid, stats = build_ab(donor, orderer, orderer, dates, flags, codes, n_codes, M_FRAC)
        metrics, _ = score_official(frame, hybrid)
        results[name] = {**extra, "connected_final_score": metrics["final_score"],
                         "connected_metrics": metrics, "boundary_tie_days": stats["boundary_tie_days"],
                         "mean_retention_ratio": stats["mean_retention_ratio"],
                         "beats_current_best": bool(metrics["final_score"] > CURRENT_BEST)}
        cs.log(f"{name[:56]:56s} CONNECTED {metrics['final_score']:.9f} "
               f"(ic {metrics['ic_mean']:.6f}, excess {metrics['annual_excess']:.6f}, "
               f"turn {metrics['mean_turnover']:.6f})")
        dump()
        return metrics["final_score"]

    # ---- variant a: the shipped donor, and the harness proof that goes with it
    donor_a, stats_a = lift(topk, slow16, pdf)
    proofs["P_variant_a_reproduces_frozen_hybrid"] = {
        "bit_identical": bool(np.array_equal(donor_a, frozen_hybrid)),
        "max_abs_diff": float(np.abs(donor_a - frozen_hybrid).max()), "lift_stats": stats_a}
    if not np.array_equal(donor_a, frozen_hybrid):
        raise AssertionError("harness proof failed: the rebuilt nested donor is not "
                             f"connected_pred_hybrid.npy (max diff "
                             f"{proofs['P_variant_a_reproduces_frozen_hybrid']['max_abs_diff']:.3e})")
    got = score("a_nested_shipped", donor_a, {"variant": "a", "promotes": TOPK, "reranks": SLOW16})
    proofs["P_variant_a_score"] = {"scored": got, "expected": CURRENT_BEST,
                                   "abs_diff": abs(got - CURRENT_BEST)}
    if abs(got - CURRENT_BEST) > 1e-12:
        raise AssertionError(f"harness proof failed: variant a scored {got!r}, expected "
                             f"{CURRENT_BEST!r}")
    cs.log("harness proof passed: variant a is the shipped donor, bit-for-bit, and reproduces "
           f"{CURRENT_BEST:.9f}")

    # variants are built lazily inside the guard, so one failure cannot abort the wave
    variants: list[tuple[str, dict, object]] = []
    for w in BLEND_WEIGHTS:
        variants.append((f"b_rerank_blend_w{w:g}",
                         {"variant": "b", "promotes": TOPK,
                          "reranks": f"rank_blend(slow16, W5a, {w}) + tie-break"},
                         lambda w=w: lift(topk, blend(slow16, w5a, SLOW16, W5A_FIN, w), pdf)[0]))
        variants.append((f"c_promote_blend_w{w:g}",
                         {"variant": "c", "promotes": f"rank_blend(topk, W5a, {w}) + tie-break",
                          "reranks": SLOW16},
                         lambda w=w: lift(blend(topk, w5a, TOPK, W5A_FIN, w), slow16, pdf)[0]))
    variants += [
        ("d_w5a_reranks", {"variant": "d", "promotes": TOPK, "reranks": W5A_FIN},
         lambda: lift(topk, w5a, pdf)[0]),
        ("e_slow16_promotes", {"variant": "e", "promotes": SLOW16, "reranks": TOPK},
         lambda: lift(slow16, topk, pdf)[0]),
        ("f_w5a_promotes", {"variant": "f", "promotes": W5A_FIN, "reranks": SLOW16},
         lambda: lift(w5a, slow16, pdf)[0]),
    ]
    for name, extra, make in variants:
        try:
            score(name, make(), extra)
        except BaseException as error:  # noqa: BLE001
            results[name] = {**extra, "error": f"{type(error).__name__}: {error}"}
            cs.log(f"{name[:56]:56s} FAILED {type(error).__name__}: {error}")
            dump()

    arms = dump()
    payload = json.loads((HERE / "wave18_results.json").read_text(encoding="utf-8"))
    payload["status"] = "complete"
    payload["completed_at_local"] = time.strftime("%Y-%m-%dT%H:%M:%S")
    (HERE / "wave18_results.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print("\n| rank | donor variant | CONNECTED | IC | excess | turnover |")
    print("|---|---|---|---|---|---|")
    for i, (s, name, v) in enumerate(arms):
        m = v["connected_metrics"]
        print(f"| {i+1} | {name[:44]} | **{s:.9f}** | {m['ic_mean']:.6f} | "
              f"{m['annual_excess']:.6f} | {m['mean_turnover']:.6f} |")
    cs.log(f"best: {arms[0][1] if arms else None} {arms[0][0] if arms else 0:.9f} "
           f"({'IMPROVES' if arms and arms[0][0] > CURRENT_BEST else 'does not improve'})")


if __name__ == "__main__":
    main()
