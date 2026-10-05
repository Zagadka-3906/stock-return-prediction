"""Wave 19: cross the two levers that waves 16 and 17 found independently, because they act on different terms.

Wave 16 improves the orderer by blending W5a with a second alpha 0 / bonus 0 backbone at a low partner
weight; the best arms move IC and excess together (0.442481 -> 0.443209). Wave 17 changes which names the
swap-budget solve drops and adds; that moves excess and turnover while IC barely shifts (best 0.442612,
drop-by-donor / add-by-orderer at m = 0.99). The two act on largely disjoint parts of the composite, and
both were searched with the other held at its old value, so neither search saw the combination.

This takes the top orderer blends from wave 16 and the top swap rules from wave 17 and crosses them over
an m grid, with the membership donor frozen at wave 13's argmax. Every arm is rebuilt from the spec its
wave recorded rather than from a re-derivation, and the frozen reference cell - wave 16's best blend with
wave 17's base rule at m = 0.985 - must reproduce that wave's recorded number before anything else is
believed.

Note wave 17 also showed that the "rank" swap key is redundant with the "orderer" key: the per-day
normalized rank is a within-day monotone transform of the orderer, so argsort cannot distinguish them,
and the two produced identical scores to the last digit. Only distinct rules are carried here.

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
from optimize_wave15 import daily_ranks, weighted_rank_blend, DONOR, TIE_EPS  # noqa: E402
from optimize_wave17 import build_swap  # noqa: E402

CURRENT_BEST = 0.443209042
CURRENT_BEST_NAME = "wave16 best blend, base swap rule, m=0.985"
REF_M = 0.985
N_ORDERERS = 3
N_RULES = 3
M_GRID = (0.98, 0.985, 0.988, 0.99, 0.992)
# wave 17 showed "rank" and "orderer" are the same rule; keep one of each distinct pair
RULES = [("base", "base"), ("orderer", "orderer"), ("base", "orderer"), ("orderer", "base")]


def sha(path) -> str:
    value = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for chunk in iter(lambda: stream.read(8 * 1024 * 1024), b""):
            value.update(chunk)
    return value.hexdigest()


def main() -> None:
    global CURRENT_BEST, CURRENT_BEST_NAME
    wave16 = json.loads((HERE / "wave16_results.json").read_text(encoding="utf-8"))
    arms16_all = sorted(((v["connected_final_score"], k)
                         for bucket in wave16["results"].values() for k, v in bucket.items()
                         if "connected_final_score" in v), reverse=True)
    if not arms16_all:
        raise SystemExit("wave 16 recorded no scored arms")
    CURRENT_BEST = float(arms16_all[0][0])
    CURRENT_BEST_NAME = f"wave16::{arms16_all[0][1]}"

    protocol_path = HERE / "protocol_wave19.json"
    if not protocol_path.exists():
        protocol_path.write_text(json.dumps({
            "frozen_at_local": time.strftime("%Y-%m-%dT%H:%M:%S"),
            "standard": "后续选模标准.md §3 connected composite primary; §4 highest score wins",
            "status": "in_sample_selection_disclosed",
            "hypothesis": "wave 16's orderer blend moves IC and excess; wave 17's swap rule moves excess "
                          "and turnover. They act on largely disjoint parts of the composite and each "
                          "was searched with the other held at its old value, so cross them.",
            "donor_fixed": {"column": DONOR, "provenance": "wave 13 stage 2 argmax"},
            "tie_break_eps": TIE_EPS,
            "orderers": f"the top {N_ORDERERS} blends recorded by wave 16, rebuilt from their recorded "
                        "components and weights",
            "swap_rules": [{"drop": d, "add": a} for d, a in RULES],
            "m_grid": list(M_GRID),
            "redundancy_note": "wave 17's 'rank' key is a within-day monotone transform of the orderer, "
                               "so it is the same rule and is not carried here",
            "harness_proof": f"wave 16's best blend with drop=add=base at m=0.985 must reproduce "
                             f"{CURRENT_BEST}",
            "current_best_before_this_wave": {"name": CURRENT_BEST_NAME,
                                              "connected_final_score": CURRENT_BEST},
            "selection_rule": "highest connected 2020-2024 official composite; no other gate",
            "disclosed_selection_cost": "search over the same five repeatedly viewed years; no blind "
                                        "period remains and the winner carries upward selection bias "
                                        "this protocol cannot quantify",
            "causality": "the blend reads only same-day predictions and the price-valid mask; the swap "
                         "keys are day-t predictions and the previous day's realized Top decile. No "
                         "label is read.",
            "no_test_period_data_read": True,
            "source_sha256": sha(Path(__file__)),
        }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        cs.log(f"wave-19 protocol frozen: {sha(protocol_path)[:16]}…")

    frame = cs.combined_frame()
    dates = frame["trade_date"].to_numpy()
    flags = frame["flag_limit_up"].to_numpy().astype(np.int64)
    valid = frame["price_valid"].to_numpy().astype(bool)
    codes, uniques = pd.factorize(frame["ts_code"].to_pandas(), sort=True)
    codes = codes.astype(np.int64)
    n_codes = len(uniques)
    tie_key = 1.0 - codes / max(n_codes - 1, 1)
    member = np.load(HERE / DONOR)

    wave16 = json.loads((HERE / "wave16_results.json").read_text(encoding="utf-8"))
    arms16 = sorted(((v["connected_final_score"], k, v)
                     for bucket in wave16["results"].values() for k, v in bucket.items()
                     if "connected_final_score" in v and "components" in v), reverse=True)
    orderers: list[tuple[str, np.ndarray, dict]] = []
    column_cache: dict = {}
    rank_cache: dict = {}
    for score16, key, value in arms16:
        if len(orderers) == N_ORDERERS:
            break
        comps, weights = value["components"], value["weights"]
        cols = []
        for stem in comps:
            if stem not in column_cache:
                column_cache[stem] = np.load(HERE / f"{stem}.npy")
                rank_cache[stem] = daily_ranks(column_cache[stem], valid, dates)
            cols.append(column_cache[stem])
        if len(comps) == 1:
            column = cols[0]
        else:
            column = weighted_rank_blend(cols, weights, rank_cache, valid, dates, tuple(comps))
        orderer = column + TIE_EPS * tie_key
        orderers.append((key, orderer, {"components": comps, "weights": weights,
                                        "wave16_score": score16}))
        cs.log(f"orderer {len(orderers)}: {key[:60]} (wave 16 {score16:.9f})")

    base_key = member
    results: dict = {}
    proofs: dict = {}

    def swap_keys(orderer: np.ndarray) -> dict:
        """The swap key for each rule. 'rank' is omitted: wave 17 showed it is the same rule as
        'orderer', because the per-day normalized rank is a within-day monotone transform of it."""
        return {"base": base_key, "orderer": orderer}

    def dump() -> list:
        arms = sorted(((v["connected_final_score"], k, v) for k, v in results.items()
                       if "connected_final_score" in v), reverse=True)
        payload = {"status": "running", "updated_at_local": time.strftime("%Y-%m-%dT%H:%M:%S"),
                   "purpose": "cross wave 16's orderer blends with wave 17's swap rules over an m grid",
                   "donor_fixed": DONOR, "tie_break_eps": TIE_EPS,
                   "orderers": [{"wave16_arm": k, **spec} for k, _, spec in orderers],
                   "swap_rules": [{"drop": d, "add": a} for d, a in RULES],
                   "m_grid": list(M_GRID), "harness_proofs": proofs,
                   "current_best_before_this_wave": {"name": CURRENT_BEST_NAME,
                                                     "connected_final_score": CURRENT_BEST},
                   "results": results, "n_scored": len(arms),
                   "ranking": [{"arm": k, "connected_final_score": s,
                                "ic_mean": v["connected_metrics"]["ic_mean"],
                                "annual_excess": v["connected_metrics"]["annual_excess"],
                                "mean_turnover": v["connected_metrics"]["mean_turnover"],
                                "swaps": v["swaps"]} for s, k, v in arms[:25]],
                   "best": arms[0][1] if arms else None,
                   "best_connected_final_score": arms[0][0] if arms else None,
                   "improves_on_current_best": bool(arms and arms[0][0] > CURRENT_BEST),
                   "no_test_period_data_read": True,
                   "source_sha256": sha(Path(__file__))}
        (HERE / "wave19_results.json").write_text(
            json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        return arms

    # ---- harness proof: the reference cell must reproduce wave 16's own recorded number
    ref_key, ref_orderer, ref_spec = orderers[0]
    ref_hybrid, _ = build_swap(member, ref_orderer, ref_orderer, dates, flags, codes, n_codes,
                               REF_M, base_key, base_key)
    ref_metrics, _ = score_official(frame, ref_hybrid)
    proofs["P_reference_cell"] = {
        "arm": f"{ref_key} / drop=base / add=base / m={REF_M}",
        "scored": ref_metrics["final_score"], "wave16_recorded": ref_spec["wave16_score"],
        "abs_diff": abs(ref_metrics["final_score"] - ref_spec["wave16_score"]),
        "note": "wave 16's best blend with the base swap rule at m=0.985 must reproduce wave 16's own "
                "recorded number, which pins the blend rebuild and the swap-rule generalization at once"}
    if proofs["P_reference_cell"]["abs_diff"] > 1e-12:
        raise AssertionError(f"harness proof failed: the reference cell scored "
                             f"{ref_metrics['final_score']!r}, wave 16 recorded "
                             f"{ref_spec['wave16_score']!r}")
    cs.log(f"harness proof passed: the reference cell reproduces wave 16's "
           f"{ref_spec['wave16_score']:.9f}")

    for o_key, orderer, spec in orderers:
        keys = swap_keys(orderer)
        for drop_rule, add_rule in RULES:
            for m_frac in M_GRID:
                name = (f"{o_key[:40]}__drop_{drop_rule}__add_{add_rule}__m{m_frac:g}")
                try:
                    hybrid, stats = build_swap(member, orderer, orderer, dates, flags, codes,
                                               n_codes, m_frac, keys[drop_rule], keys[add_rule])
                    metrics, _ = score_official(frame, hybrid)
                    results[name] = {"orderer_arm": o_key, "orderer_spec": spec,
                                     "drop_rule": drop_rule, "add_rule": add_rule, "m_frac": m_frac,
                                     "connected_final_score": metrics["final_score"],
                                     "connected_metrics": metrics,
                                     "boundary_tie_days": stats["boundary_tie_days"],
                                     "eligibility_limited_days": stats["eligibility_limited_days"],
                                     "swaps": stats["swaps"],
                                     "mean_retention_ratio": stats["mean_retention_ratio"],
                                     "beats_current_best": bool(metrics["final_score"] > CURRENT_BEST)}
                    cs.log(f"{name[:76]:76s} CONNECTED {metrics['final_score']:.9f} "
                           f"(ic {metrics['ic_mean']:.6f}, excess {metrics['annual_excess']:.6f}, "
                           f"turn {metrics['mean_turnover']:.6f})")
                    dump()
                except BaseException as error:  # noqa: BLE001
                    results[name] = {"orderer_arm": o_key, "drop_rule": drop_rule,
                                     "add_rule": add_rule, "m_frac": m_frac,
                                     "error": f"{type(error).__name__}: {error}"}
                    cs.log(f"{name[:76]:76s} FAILED {type(error).__name__}: {error}")
                    dump()

    arms = dump()
    payload = json.loads((HERE / "wave19_results.json").read_text(encoding="utf-8"))
    payload["status"] = "complete"
    payload["completed_at_local"] = time.strftime("%Y-%m-%dT%H:%M:%S")
    (HERE / "wave19_results.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print("\n| rank | arm | CONNECTED | IC | excess | turnover | swaps |")
    print("|---|---|---|---|---|---|---|")
    for i, (s, name, v) in enumerate(arms[:20]):
        m = v["connected_metrics"]
        print(f"| {i+1} | {name[:60]} | **{s:.9f}** | {m['ic_mean']:.6f} | "
              f"{m['annual_excess']:.6f} | {m['mean_turnover']:.6f} | {v['swaps']} |")
    cs.log(f"best: {arms[0][1] if arms else None} {arms[0][0] if arms else 0:.9f} "
           f"({'IMPROVES' if arms and arms[0][0] > CURRENT_BEST else 'does not improve'})")


if __name__ == "__main__":
    main()
