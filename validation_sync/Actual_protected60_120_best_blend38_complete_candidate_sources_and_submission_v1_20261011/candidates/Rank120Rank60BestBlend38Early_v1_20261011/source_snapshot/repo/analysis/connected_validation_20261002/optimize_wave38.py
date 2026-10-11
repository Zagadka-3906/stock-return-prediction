"""Wave 38: the A role - which orders WITHIN the chosen Top set and therefore drives excess - was closed over a candidate list that never contained the excess specialist.

Wave 13 stage 3 decoupled the orderer into A (orders within the chosen Top decile; the excess universe's
own top len//10 is a prefix of the chosen set in A's order, so A drives excess) and B (orders the
remaining eligible rows, ~81% of eligible pairs, so B drives IC). It found A = B = W5a optimal and
declared the axis closed. But its A grid was "the five best excess drivers from wave 12", and wave 12's
candidate list was built by `score_wave3.discover()`, which - as wave 34 established - does not scan the
r6_topk / topk_training_validation naming convention. **The flat-Top-K backbone was never in the pool.**

That is a real omission rather than a formality, because the flat-Top-K objective's gain is by
construction the exact change in mean Top-decile return for any swap. It is, in other words, a model
trained precisely for the quantity A controls. Wave 34 tested it in the FULL orderer role and it failed
badly (hybrid IC 0.068772) because B needs global ranking and a Top-decile specialist does not have it.
The A role does not need global ranking at all - it only ever orders ~457 already-chosen names.

Arms, all with the shipped nested donor and m = 0.985, and B fixed at the selected blend:
  A = B = selected blend            the reference, and the harness proof
  A = topk@alpha0/bonus0            the excess specialist ordering the chosen set
  A = topk@frac0.20@alpha0/bonus0   the wave-31 column, whose own excess was higher
  A = blend(selected, topk, w)      w = 0.25 / 0.50, in case the specialist helps only in part
  A = selected, B = topk@a0b0       the reverse assignment, as a control: this should be clearly worse
                                    because B drives IC and the specialist is a poor global ranker
The control arm matters. If A = topk helps and B = topk also helps, the effect is not about the role
separation and the interpretation would be wrong.

Harness proof: A = B = the selected blend must reproduce 0.443190552 exactly.

Both halves are reported for every arm because waves 23/25/26/31 all produced full-window gains that
were redistribution, and wave 36 established that this construction's excess term is rough at the 4.5e-3
level - larger than any effect this wave is likely to find. Selection is 后续选模标准.md §3/§4. No
test-period data is read here.
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
TOPK_A0B0 = "orderer_a0b0_topk.npy"
F20_A0B0 = "orderer_a0b0_topk_frac0.20.npy"
PARTNER_WEIGHT = 0.25
CURRENT_BEST = 0.44319055217888365
REF_HALF_DEV = 0.442705356
REF_HALF_CONF = 0.443926938
BLEND_WEIGHTS = (0.25, 0.50)


def sha(path) -> str:
    value = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for chunk in iter(lambda: stream.read(8 * 1024 * 1024), b""):
            value.update(chunk)
    return value.hexdigest()


def main() -> None:
    protocol_path = HERE / "protocol_wave38.json"
    if not protocol_path.exists():
        protocol_path.write_text(json.dumps({
            "frozen_at_local": time.strftime("%Y-%m-%dT%H:%M:%S"),
            "standard": "后续选模标准.md §3 connected composite primary; §4 highest score wins",
            "status": "in_sample_selection_disclosed",
            "hypothesis": "wave 13 stage 3 closed the A/B decoupling axis over 'the five best excess "
                          "drivers from wave 12', and wave 12's pool was built by discover(), which does "
                          "not scan the r6_topk naming convention. The flat-Top-K backbone - whose "
                          "objective gain IS the exact change in mean Top-decile return for any swap, "
                          "i.e. a model trained for precisely the quantity A controls - was never a "
                          "candidate for A. Wave 34 showed it fails as a FULL orderer (hybrid IC "
                          "0.068772) because B needs global ranking; the A role only ever orders ~457 "
                          "already-chosen names and does not need global ranking at all.",
            "roles": {"A": "orders within the chosen Top decile; the excess universe's top len//10 is a "
                           "prefix of the chosen set in A's order, so A drives excess",
                      "B": "orders the remaining eligible rows, ~81% of eligible pairs, so B drives IC"},
            "arms": ["A = B = selected blend (reference and harness proof)",
                     "A = topk@alpha0/bonus0, B = selected blend",
                     "A = topk@frac0.20@alpha0/bonus0, B = selected blend",
                     f"A = blend(selected, topk@a0b0, w), w in {list(BLEND_WEIGHTS)}",
                     "CONTROL: A = selected blend, B = topk@alpha0/bonus0"],
            "why_the_control_matters": "if A = topk helps AND B = topk helps, the effect is not about "
                                       "role separation and the interpretation would be wrong. The "
                                       "control should be clearly worse, since B drives IC and the "
                                       "specialist is a poor global ranker.",
            "donor_fixed": {"column": DONOR, "provenance": "wave 13 stage 2 argmax"},
            "m_frac_fixed_at": M_FRAC, "tie_break_eps": TIE_EPS,
            "harness_proof": f"A = B = the selected blend must reproduce {CURRENT_BEST} exactly",
            "roughness_context": "wave 36 measured this construction's excess term as rough at the "
                                 "4.5e-3 level, larger than any effect this wave is likely to find, so "
                                 "the both-halves decomposition is reported for every arm",
            "current_best_before_this_wave": CURRENT_BEST,
            "selection_rule": "highest connected 2020-2024 official composite; no other gate",
            "disclosed_selection_cost": "search over the same five repeatedly viewed years; no blind "
                                        "period remains",
            "causality": "A and B are both day-t prediction columns; the retention floor uses the "
                         "previous day's realized Top decile. No label is read.",
            "no_test_period_data_read": True,
            "source_sha256": sha(Path(__file__)),
        }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        cs.log(f"wave-38 protocol frozen: {sha(protocol_path)[:16]}…")

    combined = cs.combined_frame()
    dates = combined["trade_date"].to_numpy()
    flags = combined["flag_limit_up"].to_numpy().astype(np.int64)
    valid = combined["price_valid"].to_numpy().astype(bool)
    codes, uniques = pd.factorize(combined["ts_code"].to_pandas(), sort=True)
    codes = codes.astype(np.int64)
    n_codes = len(uniques)
    tie_key = 1.0 - codes / max(n_codes - 1, 1)
    member = np.load(HERE / DONOR)

    for stem in (TOPK_A0B0, F20_A0B0):
        if not (HERE / stem).exists():
            raise SystemExit(f"missing {stem}; run optimize_wave34.py first")
    w5a = np.load(HERE / W5A_A0B0)
    slow16 = np.load(HERE / SLOW16_A0B0)
    topk = np.load(HERE / TOPK_A0B0)
    f20 = np.load(HERE / F20_A0B0)

    rc = {}
    for name, col in (("w5a", w5a), ("slow16", slow16), ("topk", topk), ("f20", f20)):
        rc[name] = daily_ranks(col, valid, dates)
    sel = weighted_rank_blend([w5a, slow16], [1 - PARTNER_WEIGHT, PARTNER_WEIGHT], rc, valid, dates,
                              ("w5a", "slow16"))
    selected = np.where(sel > -9.0, sel + TIE_EPS * tie_key, sel)
    rc["selblend"] = daily_ranks(selected, valid, dates)

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
                   "purpose": "test the excess specialist in the A role, which wave 13-3 never could",
                   "donor_fixed": DONOR, "m_frac": M_FRAC, "tie_break_eps": TIE_EPS,
                   "harness_proofs": proofs, "current_best_before_this_wave": CURRENT_BEST,
                   "reference_halves": {"2020_2022": REF_HALF_DEV, "2023_2024": REF_HALF_CONF},
                   "results": results, "n_scored": len(arms),
                   "ranking": [{"arm": k, "connected_final_score": s, "margin_full": v["margin_full"],
                                "margin_2020_2022": v["margin_2020_2022"],
                                "margin_2023_2024": v["margin_2023_2024"],
                                "wins_both_halves": v["wins_both_halves"],
                                "ic_mean": v["connected_metrics"]["ic_mean"],
                                "annual_excess": v["connected_metrics"]["annual_excess"],
                                "mean_turnover": v["connected_metrics"]["mean_turnover"]}
                               for s, k, v in arms],
                   "best": arms[0][1] if arms else None,
                   "best_connected_final_score": arms[0][0] if arms else None,
                   "no_test_period_data_read": True, "source_sha256": sha(Path(__file__))}
        (HERE / "wave38_results.json").write_text(
            json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        return arms

    def tb(col: np.ndarray) -> np.ndarray:
        return np.where(col > -9.0, col + TIE_EPS * tie_key, col) + TIE_EPS * tie_key

    def score(name: str, a: np.ndarray, b: np.ndarray, extra: dict) -> float:
        hybrid, stats = build_ab(member, tb(a), tb(b), dates, flags, codes, n_codes, M_FRAC)
        metrics, _ = score_official(combined, hybrid)
        halves = {}
        for label, mask in half.items():
            sub, _ = score_official(combined.filter(pl.Series(mask)), hybrid[mask])
            halves[label] = sub["final_score"]
        results[name] = {**extra, "connected_final_score": metrics["final_score"],
                         "connected_metrics": metrics, "halves": halves,
                         "margin_full": metrics["final_score"] - CURRENT_BEST,
                         "margin_2020_2022": halves["2020_2022"] - REF_HALF_DEV,
                         "margin_2023_2024": halves["2023_2024"] - REF_HALF_CONF,
                         "wins_both_halves": bool(halves["2020_2022"] > REF_HALF_DEV
                                                  and halves["2023_2024"] > REF_HALF_CONF),
                         "boundary_tie_days": stats["boundary_tie_days"],
                         "swaps": stats["swaps"],
                         "mean_retention_ratio": stats["mean_retention_ratio"]}
        cs.log(f"{name[:34]:34s} CONNECTED {metrics['final_score']:.9f} "
               f"({metrics['final_score'] - CURRENT_BEST:+.2e}) | ic {metrics['ic_mean']:.6f} | "
               f"exc {metrics['annual_excess']:.6f} | turn {metrics['mean_turnover']:.6f} | "
               f"2020-22 {halves['2020_2022'] - REF_HALF_DEV:+.2e} | 2023-24 "
               f"{halves['2023_2024'] - REF_HALF_CONF:+.2e}")
        dump()
        return metrics["final_score"]

    got = score("P_A_eq_B_selected", selected, selected,
                {"A": "selected", "B": "selected", "role": "harness_proof"})
    proofs["P_reference"] = {"scored": got, "expected": CURRENT_BEST,
                             "abs_diff": abs(got - CURRENT_BEST)}
    if abs(got - CURRENT_BEST) > 1e-12:
        raise AssertionError(f"harness proof failed: {got!r} vs {CURRENT_BEST!r}")
    cs.log("harness proof passed: A = B = the selected blend reproduces 0.443190552")

    score("A_topk__B_selected", topk, selected, {"A": "topk@a0b0", "B": "selected"})
    score("A_f0.20__B_selected", f20, selected,
          {"A": "topk@frac0.20 a0b0", "B": "selected", "needs_test_fulltrain_refit": True})
    for w in BLEND_WEIGHTS:
        mix = weighted_rank_blend([selected, topk], [1 - w, w], rc, valid, dates,
                                  ("selblend", "topk"))
        score(f"A_blend_sel_topk_w{w:g}", mix, selected,
              {"A": f"blend(selected, topk@a0b0, {w})", "B": "selected"})
    score("CONTROL_A_selected__B_topk", selected, topk,
          {"A": "selected", "B": "topk@a0b0", "role": "control"})

    arms = dump()
    payload = json.loads((HERE / "wave38_results.json").read_text(encoding="utf-8"))
    payload["status"] = "complete"
    payload["completed_at_local"] = time.strftime("%Y-%m-%dT%H:%M:%S")
    (HERE / "wave38_results.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("\n| arm | CONNECTED | margin | IC | excess | turn | 2020-22 | 2023-24 | both? |")
    print("|---|---|---|---|---|---|---|---|---|")
    for s, name, v in arms:
        m = v["connected_metrics"]
        print(f"| {name[:30]} | **{s:.9f}** | {v['margin_full']:+.2e} | {m['ic_mean']:.6f} | "
              f"{m['annual_excess']:.6f} | {m['mean_turnover']:.6f} | "
              f"{v['margin_2020_2022']:+.2e} | {v['margin_2023_2024']:+.2e} | "
              f"{'YES' if v['wins_both_halves'] else 'no'} |")
    cs.log(f"best: {arms[0][1]} {arms[0][0]:.9f}")


if __name__ == "__main__":
    main()
