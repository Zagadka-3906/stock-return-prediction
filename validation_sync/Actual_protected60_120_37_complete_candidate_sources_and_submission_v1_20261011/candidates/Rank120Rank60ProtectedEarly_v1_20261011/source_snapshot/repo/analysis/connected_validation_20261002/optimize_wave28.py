"""Wave 28: the promoted block is almost exactly n_top, so the nested donor is a pass-through, not a consensus.

The numbers: wave 18's lift stats report 110,992 promoted rows over 243 days in 2020, i.e. ~457 per day,
and the evaluator's own n_top is len(eligible)//10 ~ 455. The promoted block and the block the outer
solve selects are the SAME SIZE. So `lift(topk promotes, slow16 re-ranks)` does not actually let slow16
choose - the outer solve takes essentially the whole promoted block, and slow16's ranking only matters
through the handful of names the retention floor swaps.

That is why wave 13's nested donor beat plain topk by only +0.0014, and it means the mechanism the
nested donor was credited with - "names both models put in the top tenth" - was never actually operating.
The real content is still topk's decile.

The fix is to promote a WIDER block and let the re-ranker select the decile inside it, which turns the
construction into the two-stage consensus it was assumed to be:
    promoted = top q of the eligible universe by topk          q in {0.10, 0.15, 0.20, 0.30, 0.50}
    donor    = promoted * (span + 1) + reranker
    realized Top decile = the n_top names the reranker likes best inside the promoted block
q = 0.10 is the current construction and is the harness proof; q > 0.10 is the untested region, and the
larger q is, the more of the selection the re-ranker owns. Two re-rankers are crossed with it (slow16
finished, and the selected orderer blend) because widening the block changes which of them is the better
selector - a wide block wants a re-ranker with good Top-decile precision, which is not necessarily the
one with the best global rank IC.

Everything is causal and label-free: same-day predictions and same-day limit-up flags only. Every input
is a finished column that exists for the test period, so every arm is shippable.

Selection is 后续选模标准.md §3/§4 for the ranking; the both-halves rule from waves 26/27 governs the
shipping recommendation, because waves 23/25/26 all produced full-window gains that turned out to be
redistribution between the two halves. No test-period data is read here.
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

W5A_A0B0 = "orderer_a0b0_W5a_five_way_with_gru__final_sweep_eval.npy"
SLOW16_A0B0 = "pp_a0_b0_top_only_w0.25_rl1_tcw1.npy"
SLOW16_FIN = "connected_pred_peer67_slow16.npy"
TOPK_FIN = "connected_pred_topk.npy"
W5A_FIN = "connected_pred_W5a_five_way_with_gru__final_sweep_eval.npy"
NESTED = "connected_pred_hybrid.npy"
PARTNER_WEIGHT = 0.25
Q_GRID = (0.10, 0.15, 0.20, 0.30, 0.50)
RERANKERS = ("slow16_finished", "orderer_blend", "w5a_finished")
CURRENT_BEST = 0.44319055217888365
REF_HALF_DEV = 0.442705356
REF_HALF_CONF = 0.443926938


def sha(path) -> str:
    value = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for chunk in iter(lambda: stream.read(8 * 1024 * 1024), b""):
            value.update(chunk)
    return value.hexdigest()


def top_sets_q(frame: pd.DataFrame, pred: np.ndarray, q: float) -> tuple[np.ndarray, dict]:
    """fold_validation.top_sets with the promoted fraction parameterized; q = 0.10 is the original.

    Same universe as the evaluator's turnover term: flag_limit_up == 0, day skipped below 100 rows.
    Reads no label.
    """
    dates = frame["trade_date"].to_numpy()
    flags = frame["flag_limit_up"].to_numpy()
    if not (np.diff(dates) >= 0).all():
        raise AssertionError("top_sets_q requires a frame sorted by trade_date")
    _, starts = np.unique(dates, return_index=True)
    ends = np.append(starts[1:], len(dates))
    promoted = np.zeros(len(frame), dtype=bool)
    stats = {"days": 0, "skipped_lt100": 0, "boundary_tie_days": 0, "sizes": [], "q": q}
    for start, end in zip(starts, ends):
        rows = np.arange(start, end)
        eligible = rows[flags[start:end] == 0]
        if len(eligible) < 100:
            stats["skipped_lt100"] += 1
            continue
        values = pred[eligible]
        # floor, not round: fold_validation.top_sets uses max(len//10, 1), and at q = 0.10 this must
        # agree with it exactly or the harness proof compares a different promoted block. For a day with
        # 4557 eligible rows round(0.1*4557) = 456 but 4557//10 = 455.
        n_promote = max(int(np.floor(q * len(eligible))), 1)
        n_promote = min(n_promote, len(eligible))
        order = np.argsort(-values, kind="stable")
        if n_promote < len(values) and values[order[n_promote - 1]] == values[order[n_promote]]:
            stats["boundary_tie_days"] += 1
        promoted[eligible[order[:n_promote]]] = True
        stats["days"] += 1
        stats["sizes"].append(n_promote)
    stats["sizes"] = ([int(np.min(stats["sizes"])), int(np.max(stats["sizes"])),
                       round(float(np.mean(stats["sizes"])), 2)] if stats["sizes"] else [])
    stats["promoted_share"] = float(promoted.mean())
    return promoted, stats


def lift_q(promote_source: np.ndarray, reranker: np.ndarray, pdf, q: float,
           tie_key: np.ndarray) -> tuple[np.ndarray, dict]:
    """Wave 1's lift with a width-q promoted block. The re-ranker gets a causal tie-break because a
    widened block makes boundary ties in the re-ranker reachable, and an arbitrary tie would let
    argsort's stability decide membership."""
    promoted, stats = top_sets_q(pdf, promote_source, q)
    span = float(reranker.max() - reranker.min())
    reranker_tb = reranker + TIE_EPS * tie_key
    out = promoted.astype(np.float64) * (span + 1.0) + reranker_tb
    check, _ = top_sets_q(pdf, out, q)
    if not np.array_equal(check, promoted):
        raise AssertionError("the lifted column's promoted block is not the one that was built")
    return out, stats


def main() -> None:
    protocol_path = HERE / "protocol_wave28.json"
    if not protocol_path.exists():
        protocol_path.write_text(json.dumps({
            "frozen_at_local": time.strftime("%Y-%m-%dT%H:%M:%S"),
            "standard": "后续选模标准.md §3 connected composite primary; §4 highest score wins",
            "status": "in_sample_selection_disclosed",
            "hypothesis": "the promoted block (~457/day) and the evaluator's n_top (~455/day) are the "
                          "same size, so the nested donor is a pass-through and the re-ranker never "
                          "actually selects. Widening the block turns it into the two-stage consensus "
                          "it was assumed to be.",
            "evidence_for_the_size_claim": "wave 18 lift stats: 110,992 promoted rows over 243 days in "
                                           "2020 = 456.8/day; n_top = len(eligible)//10 ~ 455",
            "grid": {"q": list(Q_GRID), "rerankers": list(RERANKERS)},
            "promote_source_fixed": {"column": TOPK_FIN,
                                     "reason": "wave 13 stage 2 argmax over 30 donors and wave 18 "
                                               "showed blending the promote source collapses excess"},
            "outer_orderer_fixed": {"members": [W5A_A0B0, SLOW16_A0B0],
                                    "weights": [1 - PARTNER_WEIGHT, PARTNER_WEIGHT],
                                    "provenance": "wave 20 argmax over shippable arms"},
            "m_frac_fixed_at": M_FRAC, "tie_break_eps": TIE_EPS,
            "tie_break_on_the_reranker": "the re-ranker gets the causal code-rank tie-break because a "
                                         "widened block makes boundary ties reachable. At q = 0.10 this "
                                         "means the donor ARRAY differs from the frozen "
                                         "connected_pred_hybrid.npy by up to 1e-9 while its ordering is "
                                         "identical, so the harness proof asserts on the SCORE, not on "
                                         "bit-identity",
            "harness_proof": f"q = 0.10 with the slow16 re-ranker must score {CURRENT_BEST} to 1e-12",
            "deliverability": "topk, slow16 and W5a finished columns all exist for the test period, so "
                              "every arm is shippable",
            "shipping_rule_declared_in_advance": f"beat {CURRENT_BEST} on the full window AND on both "
                                                 f"halves ({REF_HALF_DEV:.9f} / {REF_HALF_CONF:.9f})",
            "current_best_before_this_wave": CURRENT_BEST,
            "selection_rule": "highest connected 2020-2024 official composite; no other gate",
            "disclosed_selection_cost": "search over the same five repeatedly viewed years; no blind "
                                        "period remains",
            "causality": "the promoted block and the re-ranking read only same-day predictions and "
                         "same-day limit-up flags. No label is read.",
            "no_test_period_data_read": True,
            "source_sha256": sha(Path(__file__)),
        }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        cs.log(f"wave-28 protocol frozen: {sha(protocol_path)[:16]}…")

    combined = cs.combined_frame()
    dates = combined["trade_date"].to_numpy()
    flags = combined["flag_limit_up"].to_numpy().astype(np.int64)
    valid = combined["price_valid"].to_numpy().astype(bool)
    codes, uniques = pd.factorize(combined["ts_code"].to_pandas(), sort=True)
    codes = codes.astype(np.int64)
    n_codes = len(uniques)
    tie_key = 1.0 - codes / max(n_codes - 1, 1)
    pdf = combined.select(["trade_date", "flag_limit_up"]).to_pandas()

    topk = np.load(HERE / TOPK_FIN)
    slow16_fin = np.load(HERE / SLOW16_FIN)
    w5a_fin = np.load(HERE / W5A_FIN)
    frozen_nested = np.load(HERE / NESTED)

    w5a = np.load(HERE / W5A_A0B0)
    slow16 = np.load(HERE / SLOW16_A0B0)
    cache = {"w5a": daily_ranks(w5a, valid, dates), "slow16": daily_ranks(slow16, valid, dates)}
    blended = weighted_rank_blend([w5a, slow16], [1 - PARTNER_WEIGHT, PARTNER_WEIGHT], cache, valid,
                                  dates, ("w5a", "slow16"))
    orderer = np.where(blended > -9.0, blended + TIE_EPS * tie_key, blended) + TIE_EPS * tie_key
    rerankers = {"slow16_finished": slow16_fin, "orderer_blend": orderer, "w5a_finished": w5a_fin}

    masks = {str(yy): (dates >= yy * 10000 + 101) & (dates <= yy * 10000 + 1231)
             for yy in cs.YEARS}
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
                   "purpose": "widen the promoted block so the re-ranker actually selects",
                   "promote_source": TOPK_FIN, "m_frac": M_FRAC, "tie_break_eps": TIE_EPS,
                   "harness_proofs": proofs, "current_best_before_this_wave": CURRENT_BEST,
                   "reference_halves": {"2020_2022": REF_HALF_DEV, "2023_2024": REF_HALF_CONF},
                   "results": results, "n_scored": len(arms),
                   "ranking": [{"arm": k, "connected_final_score": s, "margin_full": v["margin_full"],
                                "margin_2020_2022": v["margin_2020_2022"],
                                "margin_2023_2024": v["margin_2023_2024"],
                                "recommended_to_ship": v.get("recommended_to_ship"),
                                "promoted_per_day": v["lift_stats"]["sizes"],
                                "ic_mean": v["connected_metrics"]["ic_mean"],
                                "annual_excess": v["connected_metrics"]["annual_excess"],
                                "mean_turnover": v["connected_metrics"]["mean_turnover"]}
                               for s, k, v in arms[:25]],
                   "best": arms[0][1] if arms else None,
                   "best_connected_final_score": arms[0][0] if arms else None,
                   "best_recommended_to_ship": next((k for s, k, v in arms
                                                     if v.get("recommended_to_ship")), None),
                   "no_test_period_data_read": True,
                   "source_sha256": sha(Path(__file__))}
        (HERE / "wave28_results.json").write_text(
            json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        return arms

    for q in Q_GRID:
        for name, reranker in rerankers.items():
            arm = f"q{q:g}__{name}"
            try:
                donor, lift_stats = lift_q(topk, reranker, pdf, q, tie_key)
                if q == 0.10 and name == "slow16_finished":
                    identical = bool(np.array_equal(donor, frozen_nested))
                    proofs["P_q0.10_slow16_reproduces_frozen_nested"] = {
                        "bit_identical": identical,
                        "max_abs_diff": float(np.abs(donor - frozen_nested).max()),
                        "note": "bit-identity is NOT expected and is not the proof. This arm's re-ranker "
                                "carries the causal tie-break and the frozen connected_pred_hybrid.npy "
                                "does not, so the values differ by up to 1e-9. slow16's finished values "
                                "have no boundary ties at q = 0.10, so the tie-break cannot reorder "
                                "anything and the promoted block, the ordering and therefore the SCORE "
                                "must be unchanged. The score assertion below is the binding proof; "
                                "max_abs_diff is recorded so a genuine ordering change would be visible "
                                "as a diff far larger than 1e-9."}
                hybrid, stats = build_ab(donor, orderer, orderer, dates, flags, codes, n_codes,
                                         M_FRAC)
                metrics, _ = score_official(combined, hybrid)
                halves = {}
                for label, mask in half.items():
                    sub, _ = score_official(combined.filter(pl.Series(mask)), hybrid[mask])
                    halves[label] = sub["final_score"]
                margin_full = metrics["final_score"] - CURRENT_BEST
                m_dev = halves["2020_2022"] - REF_HALF_DEV
                m_conf = halves["2023_2024"] - REF_HALF_CONF
                results[arm] = {"q": q, "reranker": name, "lift_stats": lift_stats,
                                "connected_final_score": metrics["final_score"],
                                "connected_metrics": metrics, "halves": halves,
                                "margin_full": margin_full, "margin_2020_2022": m_dev,
                                "margin_2023_2024": m_conf,
                                "boundary_tie_days": stats["boundary_tie_days"],
                                "swaps": stats["swaps"],
                                "mean_retention_ratio": stats["mean_retention_ratio"],
                                "recommended_to_ship": bool(margin_full > 0 and m_dev > 0
                                                            and m_conf > 0)}
                cs.log(f"{arm[:34]:34s} CONNECTED {metrics['final_score']:.9f} ({margin_full:+.2e}) | "
                       f"2020-22 {m_dev:+.2e} | 2023-24 {m_conf:+.2e} | promoted/day "
                       f"{lift_stats['sizes']} | ic {metrics['ic_mean']:.6f} exc "
                       f"{metrics['annual_excess']:.6f} turn {metrics['mean_turnover']:.6f} | "
                       f"ship={results[arm]['recommended_to_ship']}")
                if q == 0.10 and name == "slow16_finished":
                    proofs["P_q0.10_slow16_reproduces_frozen_nested"]["scored"] = \
                        metrics["final_score"]
                    proofs["P_q0.10_slow16_reproduces_frozen_nested"]["expected"] = CURRENT_BEST
                    proofs["P_q0.10_slow16_reproduces_frozen_nested"]["abs_diff"] = \
                        abs(metrics["final_score"] - CURRENT_BEST)
                    if abs(metrics["final_score"] - CURRENT_BEST) > 1e-12:
                        raise AssertionError(
                            f"harness proof failed: q=0.10/slow16 scored "
                            f"{metrics['final_score']!r}, expected {CURRENT_BEST!r}")
                    cs.log("harness proof passed: q = 0.10 with the slow16 re-ranker reproduces the "
                           "shipped nested donor and 0.443190552")
                dump()
            except BaseException as error:  # noqa: BLE001
                results[arm] = {"q": q, "reranker": name, "error": f"{type(error).__name__}: {error}"}
                cs.log(f"{arm[:34]:34s} FAILED {type(error).__name__}: {error}")
                dump()

    arms = dump()
    payload = json.loads((HERE / "wave28_results.json").read_text(encoding="utf-8"))
    payload["status"] = "complete"
    payload["completed_at_local"] = time.strftime("%Y-%m-%dT%H:%M:%S")
    (HERE / "wave28_results.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print("\n| arm | promoted/day | CONNECTED | margin full | 2020-22 | 2023-24 | IC | excess | turn | ship? |")
    print("|---|---|---|---|---|---|---|---|---|---|")
    for s, name, v in arms:
        m = v["connected_metrics"]
        print(f"| {name[:26]} | {v['lift_stats']['sizes']} | **{s:.9f}** | {v['margin_full']:+.2e} | "
              f"{v['margin_2020_2022']:+.2e} | {v['margin_2023_2024']:+.2e} | {m['ic_mean']:.6f} | "
              f"{m['annual_excess']:.6f} | {m['mean_turnover']:.6f} | "
              f"{'YES' if v.get('recommended_to_ship') else '-'} |")
    cs.log(f"best by full window: {arms[0][1]} {arms[0][0]:.9f}")
    cs.log(f"best that also wins both halves: {payload['best_recommended_to_ship'] or 'NONE'}")


if __name__ == "__main__":
    main()
