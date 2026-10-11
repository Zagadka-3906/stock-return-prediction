"""Wave 16: refine the orderer blend weight, then optimize a multi-way blend.

Wave 15's stage A found that blending W5a with a second alpha 0 / bonus 0 backbone raises BOTH terms of
the hybrid it feeds - at partner weight 0.25, IC 0.116610 -> 0.116662 and excess 0.351811 -> 0.354106,
composite 0.442481207 -> 0.443190552. Two things follow. First, 0.25 was the smallest weight on wave
15's grid and the score is monotone decreasing in the weight over 0.25/0.5/0.75, so the optimum is at or
below the grid's edge and has to be located. Second, if one partner helps, a weighted combination of the
best few may help more, and that has never been searched either.

Stage A sweeps a fine weight grid for each of wave 15's distinct top partners. Stage B searches
two-partner weights over the best two. Stage C checks the equal-weight multi-way blends as a cheap
robustness read on whether the gain is a property of blending or of one specific partner.

The donor and the retention floor stay frozen at wave 13's argmax, so every arm is directly comparable
to wave 15's and to the shipped 0.442481207.

Harness proof: at partner weight 0 the blend must reduce to W5a alone and reproduce 0.442481207 to
1e-12. That pins the blending code against the frozen number rather than against a re-derivation.

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
from optimize_wave15 import (daily_ranks, weighted_rank_blend, W5A_ORDERER, DONOR,  # noqa: E402
                             M_FRAC, TIE_EPS)

CURRENT_BEST = 0.4424812067218111
CURRENT_BEST_NAME = "nested_x_W5a_a0_b0_m0.985_tiebreak"
FINE_WEIGHTS = (0.0, 0.05, 0.10, 0.15, 0.20, 0.25, 0.30, 0.35, 0.40)
N_PARTNERS = 4
TWO_PARTNER_GRID = (0.10, 0.20, 0.30)


def sha(path) -> str:
    value = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for chunk in iter(lambda: stream.read(8 * 1024 * 1024), b""):
            value.update(chunk)
    return value.hexdigest()


def main() -> None:
    protocol_path = HERE / "protocol_wave16.json"
    if not protocol_path.exists():
        protocol_path.write_text(json.dumps({
            "frozen_at_local": time.strftime("%Y-%m-%dT%H:%M:%S"),
            "standard": "后续选模标准.md §3 connected composite primary; §4 highest score wins",
            "status": "in_sample_selection_disclosed",
            "hypothesis": "wave 15's partner-weight grid had its optimum at the grid edge (0.25, the "
                          "smallest value tried) and the score was monotone decreasing in the weight, "
                          "so locate the optimum; and if one partner helps, a weighted two-partner "
                          "blend may help more",
            "donor_fixed": {"column": DONOR, "provenance": "wave 13 stage 2 argmax"},
            "m_frac_fixed_at": M_FRAC, "m_provenance": "wave 13 stage 1 argmax",
            "tie_break_eps": TIE_EPS,
            "stageA": {"fine_weights": list(FINE_WEIGHTS),
                       "partners": f"the {N_PARTNERS} distinct best from wave 15 stage A"},
            "stageB": {"two_partner_weights": list(TWO_PARTNER_GRID)},
            "stageC": "equal-weight three- and four-way blends of W5a with its best partners",
            "harness_proof": "partner weight 0 must reduce to W5a alone and reproduce "
                             f"{CURRENT_BEST} to 1e-12",
            "current_best_before_this_wave": {"name": CURRENT_BEST_NAME,
                                              "connected_final_score": CURRENT_BEST},
            "selection_rule": "highest connected 2020-2024 official composite; no significance, "
                              "worst-year or single-metric gate",
            "disclosed_selection_cost": "twelfth consecutive search over the same five viewed years; "
                                        "cumulative candidate count now exceeds 500, no blind period "
                                        "remains, and the winner carries upward selection bias this "
                                        "protocol cannot quantify",
            "causality": "the per-day rank blend reads only same-day predictions and the price-valid "
                         "mask. No label is read.",
            "no_test_period_data_read": True,
            "source_sha256": sha(Path(__file__)),
        }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        cs.log(f"wave-16 protocol frozen: {sha(protocol_path)[:16]}…")

    combined = cs.combined_frame()
    dates = combined["trade_date"].to_numpy()
    flags = combined["flag_limit_up"].to_numpy().astype(np.int64)
    valid = combined["price_valid"].to_numpy().astype(bool)
    codes, uniques = pd.factorize(combined["ts_code"].to_pandas(), sort=True)
    codes = codes.astype(np.int64)
    n_codes = len(uniques)
    tie_key = 1.0 - codes / max(n_codes - 1, 1)
    member = np.load(HERE / DONOR)

    wave15 = json.loads((HERE / "wave15_results.json").read_text(encoding="utf-8"))
    stage_a = {k: v for k, v in wave15["results"]["stageA_blend"].items()
               if "connected_final_score" in v}
    ranked = sorted(((v["connected_final_score"], v["components"][1]) for v in stage_a.values()),
                    reverse=True)
    partners: list[str] = []
    for _, stem in ranked:
        if stem not in partners:
            partners.append(stem)
        if len(partners) == N_PARTNERS:
            break
    cs.log(f"stage A partners from wave 15: {partners}")

    w5a = np.load(HERE / f"{W5A_ORDERER}.npy")
    rank_cache: dict = {W5A_ORDERER: daily_ranks(w5a, valid, dates)}
    columns = {W5A_ORDERER: w5a}
    for stem in partners:
        columns[stem] = np.load(HERE / f"{stem}.npy")
        rank_cache[stem] = daily_ranks(columns[stem], valid, dates)

    results: dict = {"stageA_fine": {}, "stageB_two_partner": {}, "stageC_multiway": {}}
    proofs: dict = {}

    def dump() -> list:
        arms = sorted(((v["connected_final_score"], k, v)
                       for bucket in results.values() for k, v in bucket.items()
                       if "connected_final_score" in v), reverse=True)
        payload = {"status": "running", "updated_at_local": time.strftime("%Y-%m-%dT%H:%M:%S"),
                   "purpose": "locate the orderer blend-weight optimum and search two-partner weights",
                   "donor_fixed": DONOR, "m_frac": M_FRAC, "tie_break_eps": TIE_EPS,
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
        (HERE / "wave16_results.json").write_text(
            json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        return arms

    def score(name: str, bucket: str, orderer: np.ndarray, extra: dict) -> float:
        hybrid, stats = build_ab(member, orderer + TIE_EPS * tie_key, orderer + TIE_EPS * tie_key,
                                 dates, flags, codes, n_codes, M_FRAC)
        metrics, _ = score_official(combined, hybrid)
        results[bucket][name] = {**extra, "connected_final_score": metrics["final_score"],
                                 "connected_metrics": metrics,
                                 "boundary_tie_days": stats["boundary_tie_days"],
                                 "mean_retention_ratio": stats["mean_retention_ratio"],
                                 "beats_current_best": bool(metrics["final_score"] > CURRENT_BEST)}
        cs.log(f"{name[:64]:64s} CONNECTED {metrics['final_score']:.9f} "
               f"(ic {metrics['ic_mean']:.6f}, excess {metrics['annual_excess']:.6f}, "
               f"turn {metrics['mean_turnover']:.6f})")
        dump()
        return metrics["final_score"]

    # ---- harness proof: weight 0 must be W5a alone. The blend returns per-day normalized ranks
    # rather than W5a's own values, so the proof is that the score is unchanged, not that the array is.
    zero = weighted_rank_blend([w5a], [1.0], rank_cache, valid, dates, (W5A_ORDERER,))
    got = score("P0_W5a_alone", "stageA_fine", zero, {"components": [W5A_ORDERER], "weights": [1.0]})
    proofs["P0_weight_zero_reduces_to_w5a"] = {
        "scored": got, "expected": CURRENT_BEST, "abs_diff": abs(got - CURRENT_BEST),
        "note": "the blend emits per-day normalized ranks, a within-day monotone transform of W5a, so "
                "score equality - not array equality - is the right identity here"}
    if abs(got - CURRENT_BEST) > 1e-12:
        raise AssertionError(f"harness proof failed: W5a alone scored {got!r}, expected "
                             f"{CURRENT_BEST!r}")
    cs.log("harness proof passed: partner weight 0 reproduces the shipped 0.442481207")
    dump()

    # ---- stage A: fine weight grid per partner
    for stem in partners:
        for w in FINE_WEIGHTS:
            if w == 0.0:
                continue
            blend = weighted_rank_blend([w5a, columns[stem]], [1.0 - w, w], rank_cache, valid, dates,
                                        (W5A_ORDERER, stem))
            score(f"w{w:g}__{stem[len('orderer_a0b0_'):]}", "stageA_fine", blend,
                  {"components": [W5A_ORDERER, stem], "weights": [1.0 - w, w]})

    # ---- stage B: two partners
    if len(partners) >= 2:
        p1, p2 = partners[0], partners[1]
        short1 = p1[len("orderer_a0b0_"):][:24]
        short2 = p2[len("orderer_a0b0_"):][:24]
        for w1 in TWO_PARTNER_GRID:
            for w2 in TWO_PARTNER_GRID:
                blend = weighted_rank_blend([w5a, columns[p1], columns[p2]],
                                            [1.0 - w1 - w2, w1, w2], rank_cache, valid, dates,
                                            (W5A_ORDERER, p1, p2))
                score(f"w{w1:g}+{w2:g}__{short1}|{short2}", "stageB_two_partner", blend,
                      {"components": [W5A_ORDERER, p1, p2], "weights": [1.0 - w1 - w2, w1, w2]})

    # ---- stage C: equal-weight multi-way
    for k in (3, 4):
        if len(partners) >= k - 1:
            names = [W5A_ORDERER] + partners[:k - 1]
            blend = weighted_rank_blend([columns[n] for n in names], [1.0] * k, rank_cache, valid,
                                        dates, tuple(names))
            score(f"equal_{k}way:" + "+".join(n[len("orderer_a0b0_")][:20] for n in names),
                  "stageC_multiway", blend, {"components": names, "weights": [1.0 / k] * k})

    arms = dump()
    payload = json.loads((HERE / "wave16_results.json").read_text(encoding="utf-8"))
    payload["status"] = "complete"
    payload["completed_at_local"] = time.strftime("%Y-%m-%dT%H:%M:%S")
    payload["partners"] = partners
    (HERE / "wave16_results.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print("\n| rank | arm | CONNECTED | IC | excess | turnover |")
    print("|---|---|---|---|---|---|")
    for i, (s, name, v) in enumerate(arms[:20]):
        m = v["connected_metrics"]
        print(f"| {i+1} | {name[:66]} | **{s:.9f}** | {m['ic_mean']:.6f} | "
              f"{m['annual_excess']:.6f} | {m['mean_turnover']:.6f} |")
    cs.log(f"best: {arms[0][1] if arms else None} {arms[0][0] if arms else 0:.9f} "
           f"({'IMPROVES' if arms and arms[0][0] > CURRENT_BEST else 'does not improve'})")


if __name__ == "__main__":
    main()
