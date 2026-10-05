"""Wave 25: the retention floor was only ever gridded at 0.005 resolution. Grid it at 0.001.

m_frac enters the construction as m = round(m_frac * n_top) with n_top ~ 465, so one name of retention
per day is worth about 1/465 = 0.00215 of m_frac. Every earlier grid was coarser than that: wave 13 used
{0.90, 0.95, 0.97, 0.98, 0.985, 0.99, 0.993, 0.995, 0.997, 1.0}, wave 20 used {0.985, 0.988}. Wave 23
stumbled onto the gap by accident - its m_base grid included 0.983, and the CONSTANT floor at 0.983
scores 0.443371517 against 0.985's 0.443190552. That is +1.81e-4 from grid resolution alone, with no
adaptivity involved.

So the "m = 0.985 is the argmax, confirmed four times" claim in the record is an artifact of the grid,
not a property of the objective. This wave grids m_frac at 0.001 from 0.976 to 0.990 with the donor and
orderer frozen at the selection, and reports the realized integer m per arm so the resolution limit is
visible rather than inferred.

Harness proof: m_frac = 0.985 must reproduce 0.443190552 exactly.

Honest framing, recorded in advance: the entire range this wave spans is a few times 1e-4, which is the
same order as wave 20's top-six spread (2.2e-4) and far below the 0.001743 refit noise floor. A win
here is a real maximum of the measured objective and §4 says to take it, but it is not evidence of a
better model - it is a finer read of the same plateau. The protocol records the plateau width so the
result cannot be quoted without it.

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
from optimize_wave15 import daily_ranks, weighted_rank_blend, DONOR, M_FRAC, TIE_EPS  # noqa: E402

W5A_A0B0 = "orderer_a0b0_W5a_five_way_with_gru__final_sweep_eval.npy"
SLOW16_A0B0 = "pp_a0_b0_top_only_w0.25_rl1_tcw1.npy"
PARTNER_WEIGHT = 0.25
CURRENT_BEST = 0.44319055217888365
PLATEAU_WIDTH = 2.2e-4
M_GRID = tuple(round(0.976 + 0.001 * i, 3) for i in range(15))


def sha(path) -> str:
    value = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for chunk in iter(lambda: stream.read(8 * 1024 * 1024), b""):
            value.update(chunk)
    return value.hexdigest()


def main() -> None:
    protocol_path = HERE / "protocol_wave25.json"
    if not protocol_path.exists():
        protocol_path.write_text(json.dumps({
            "frozen_at_local": time.strftime("%Y-%m-%dT%H:%M:%S"),
            "standard": "后续选模标准.md §3 connected composite primary; §4 highest score wins",
            "status": "in_sample_selection_disclosed",
            "hypothesis": "m enters as round(m_frac * n_top) with n_top ~ 465, so one retained name per "
                          "day is worth ~0.00215 of m_frac. Every earlier grid was coarser than that, "
                          "so the four-fold confirmation of m = 0.985 was a property of the grid, not of "
                          "the objective. Wave 23 found the constant floor at 0.983 scores 0.443371517 "
                          "against 0.985's 0.443190552.",
            "grid": list(M_GRID),
            "donor_fixed": {"column": DONOR, "provenance": "wave 13 stage 2 argmax"},
            "orderer_fixed": {"members": [W5A_A0B0, SLOW16_A0B0],
                              "weights": [1 - PARTNER_WEIGHT, PARTNER_WEIGHT],
                              "provenance": "wave 20 argmax over shippable arms"},
            "tie_break_eps": TIE_EPS,
            "harness_proof": f"m_frac = {M_FRAC} must reproduce {CURRENT_BEST} exactly",
            "reported_per_arm": "the realized integer m distribution (min/max/mean over days), so the "
                                "resolution limit is visible rather than inferred",
            "honest_framing_recorded_in_advance": "the whole range this wave spans is a few times 1e-4, "
                                                  f"the same order as wave 20's top-six spread "
                                                  f"({PLATEAU_WIDTH}) and far below the 0.001743 refit "
                                                  "noise floor. A win here is a real maximum of the "
                                                  "measured objective and §4 says take it, but it is a "
                                                  "finer read of the same plateau, not evidence of a "
                                                  "better model.",
            "current_best_before_this_wave": CURRENT_BEST,
            "selection_rule": "highest connected 2020-2024 official composite; no other gate",
            "disclosed_selection_cost": "search over the same five repeatedly viewed years; no blind "
                                        "period remains",
            "causality": "the retention floor uses only the previous day's realized Top decile, a "
                         "function of past predictions and past limit-up flags. No label is read.",
            "no_test_period_data_read": True,
            "source_sha256": sha(Path(__file__)),
        }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        cs.log(f"wave-25 protocol frozen: {sha(protocol_path)[:16]}…")

    combined = cs.combined_frame()
    dates = combined["trade_date"].to_numpy()
    flags = combined["flag_limit_up"].to_numpy().astype(np.int64)
    valid = combined["price_valid"].to_numpy().astype(bool)
    codes, uniques = pd.factorize(combined["ts_code"].to_pandas(), sort=True)
    codes = codes.astype(np.int64)
    n_codes = len(uniques)
    tie_key = 1.0 - codes / max(n_codes - 1, 1)
    member = np.load(HERE / DONOR)

    w5a = np.load(HERE / W5A_A0B0)
    slow16 = np.load(HERE / SLOW16_A0B0)
    cache = {"w5a": daily_ranks(w5a, valid, dates), "slow16": daily_ranks(slow16, valid, dates)}
    blended = weighted_rank_blend([w5a, slow16], [1 - PARTNER_WEIGHT, PARTNER_WEIGHT], cache, valid,
                                  dates, ("w5a", "slow16"))
    orderer = np.where(blended > -9.0, blended + TIE_EPS * tie_key, blended) + TIE_EPS * tie_key

    # n_top per day, so the integer-m resolution can be reported
    _, starts = np.unique(dates, return_index=True)
    ends = np.append(starts[1:], len(dates))
    n_tops = np.array([max(int((flags[s:e] == 0).sum()) // 10, 1) for s, e in zip(starts, ends)])
    cs.log(f"n_top per day: min {n_tops.min()}, max {n_tops.max()}, mean {n_tops.mean():.1f}; "
           f"one retained name = {1.0 / n_tops.mean():.5f} of m_frac")

    results: dict = {}
    proofs: dict = {}

    def dump() -> list:
        arms = sorted(((v["connected_final_score"], k, v) for k, v in results.items()
                       if "connected_final_score" in v), reverse=True)
        payload = {"status": "running", "updated_at_local": time.strftime("%Y-%m-%dT%H:%M:%S"),
                   "purpose": "grid the retention floor at 0.001 instead of 0.005",
                   "donor_fixed": DONOR, "orderer_fixed": [W5A_A0B0, SLOW16_A0B0],
                   "partner_weight": PARTNER_WEIGHT, "tie_break_eps": TIE_EPS,
                   "n_top_per_day": {"min": int(n_tops.min()), "max": int(n_tops.max()),
                                     "mean": float(n_tops.mean()),
                                     "one_name_in_m_frac": float(1.0 / n_tops.mean())},
                   "plateau_width": PLATEAU_WIDTH, "harness_proofs": proofs,
                   "current_best_before_this_wave": CURRENT_BEST,
                   "results": results, "n_scored": len(arms),
                   "ranking": [{"arm": k, "connected_final_score": s,
                                "margin_over_best": s - CURRENT_BEST,
                                "ic_mean": v["connected_metrics"]["ic_mean"],
                                "annual_excess": v["connected_metrics"]["annual_excess"],
                                "mean_turnover": v["connected_metrics"]["mean_turnover"],
                                "integer_m": v["integer_m"]} for s, k, v in arms],
                   "best": arms[0][1] if arms else None,
                   "best_connected_final_score": arms[0][0] if arms else None,
                   "best_margin": (arms[0][0] - CURRENT_BEST) if arms else None,
                   "improves_on_current_best": bool(arms and arms[0][0] > CURRENT_BEST),
                   "no_test_period_data_read": True,
                   "source_sha256": sha(Path(__file__))}
        (HERE / "wave25_results.json").write_text(
            json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        return arms

    for m_frac in M_GRID:
        integer_m = np.round(m_frac * n_tops).astype(int)
        hybrid, stats = build_ab(member, orderer, orderer, dates, flags, codes, n_codes, m_frac)
        metrics, _ = score_official(combined, hybrid)
        name = f"m{m_frac:.3f}"
        results[name] = {"m_frac": m_frac, "connected_final_score": metrics["final_score"],
                         "connected_metrics": metrics,
                         "integer_m": {"min": int(integer_m.min()), "max": int(integer_m.max()),
                                       "mean": round(float(integer_m.mean()), 2),
                                       "n_distinct": int(len(np.unique(integer_m)))},
                         "boundary_tie_days": stats["boundary_tie_days"],
                         "eligibility_limited_days": stats["eligibility_limited_days"],
                         "swaps": stats["swaps"],
                         "mean_retention_ratio": stats["mean_retention_ratio"],
                         "margin_over_best": metrics["final_score"] - CURRENT_BEST}
        cs.log(f"{name} CONNECTED {metrics['final_score']:.9f} "
               f"(ic {metrics['ic_mean']:.6f}, excess {metrics['annual_excess']:.6f}, "
               f"turn {metrics['mean_turnover']:.6f}) integer m mean {integer_m.mean():.2f} | "
               f"margin {metrics['final_score'] - CURRENT_BEST:+.3e}")
        if abs(m_frac - M_FRAC) < 1e-12:
            proofs["P_reference_m"] = {"m_frac": m_frac, "scored": metrics["final_score"],
                                       "expected": CURRENT_BEST,
                                       "abs_diff": abs(metrics["final_score"] - CURRENT_BEST)}
            if proofs["P_reference_m"]["abs_diff"] > 1e-12:
                raise AssertionError(f"harness proof failed: m={M_FRAC} scored "
                                     f"{metrics['final_score']!r}, expected {CURRENT_BEST!r}")
            cs.log("harness proof passed: m_frac = 0.985 reproduces 0.443190552")
        dump()

    arms = dump()
    payload = json.loads((HERE / "wave25_results.json").read_text(encoding="utf-8"))
    payload["status"] = "complete"
    payload["completed_at_local"] = time.strftime("%Y-%m-%dT%H:%M:%S")
    (HERE / "wave25_results.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print("\n| m_frac | integer m (mean) | CONNECTED | margin | IC | excess | turnover |")
    print("|---|---|---|---|---|---|---|")
    for m_frac in M_GRID:
        v = results[f"m{m_frac:.3f}"]
        m = v["connected_metrics"]
        print(f"| {m_frac:.3f} | {v['integer_m']['mean']:.2f} | **{v['connected_final_score']:.9f}** | "
              f"{v['margin_over_best']:+.2e} | {m['ic_mean']:.6f} | {m['annual_excess']:.6f} | "
              f"{m['mean_turnover']:.6f} |")
    cs.log(f"best: {arms[0][1]} {arms[0][0]:.9f} (margin {arms[0][0] - CURRENT_BEST:+.3e})")


if __name__ == "__main__":
    main()
