"""Wave 26: joint (m_base, k) grid for the adaptive floor, with a split-half decomposition of every arm.

Wave 25 showed the retention floor's objective is not smooth in m_frac. Adjacent grid points that round
to the same integer m score IDENTICALLY (0.984 and 0.985 both give 0.443190552 with integer m mean
450.37), and the curve jumps by +0.0017 between integer m 448 and 449, then falls away. The peak is at
integer m ~ 449, i.e. m_frac 0.982-0.983, worth +2.12e-4 over the 0.985 the selection was made on.

That is a discrete optimum one retained name wide, which is exactly the kind of fine-grained parameter
choice this project's own transfer analysis has repeatedly shown not to rank stably: the 48-candidate
study found Spearman -0.7477 between the 2020-2022 and 2023-2024 halves. So this wave reports every arm
on both halves and per year as well as on the full window, and the shipping recommendation is written
into the payload as a rule decided in advance rather than after seeing the answer:

    an arm is recommended only if it beats the m = 0.985 reference on the FULL window AND on BOTH
    halves. An arm that wins the full window by moving one half is a redistribution, not an improvement.

Wave 23 found the eligibility signal helps and the donor-autocorrelation signal does not, so only
eligibility is carried, over a finer m_base x k grid centred on wave 25's peak.

Harness proof: m_base = 0.985 with k = 0 must reproduce 0.443190552 exactly.

Selection under 后续选模标准.md §4 is still "highest connected composite" and this wave does not
override that; the both-halves rule is a recommendation about what to SHIP, recorded separately, because
§4 has no materiality threshold and the differences here are 1e-4 against a 0.001743 refit noise floor.
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
import polars as pl

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(HERE))
import connected_scorer as cs  # noqa: E402
from experiments.revalidate_fold_local import score_official  # noqa: E402
from optimize_wave15 import daily_ranks, weighted_rank_blend, DONOR, TIE_EPS  # noqa: E402
from optimize_wave23 import build_adaptive  # noqa: E402

YEARS = cs.YEARS
W5A_A0B0 = "orderer_a0b0_W5a_five_way_with_gru__final_sweep_eval.npy"
SLOW16_A0B0 = "pp_a0_b0_top_only_w0.25_rl1_tcw1.npy"
PARTNER_WEIGHT = 0.25
REFERENCE = 0.44319055217888365
REFERENCE_M = 0.985
NOISE_FLOOR = 0.001743
M_BASES = (0.981, 0.982, 0.983, 0.984, 0.985)
K_GRID = (0.0, 0.10, 0.15, 0.20, 0.25, 0.30)
CLIP = (0.95, 1.0)


def sha(path) -> str:
    value = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for chunk in iter(lambda: stream.read(8 * 1024 * 1024), b""):
            value.update(chunk)
    return value.hexdigest()


def main() -> None:
    protocol_path = HERE / "protocol_wave26.json"
    if not protocol_path.exists():
        protocol_path.write_text(json.dumps({
            "frozen_at_local": time.strftime("%Y-%m-%dT%H:%M:%S"),
            "standard": "后续选模标准.md §3 connected composite primary; §4 highest score wins",
            "status": "in_sample_selection_disclosed",
            "hypothesis": "wave 25 located the constant-floor peak at m_frac 0.982-0.983 (integer m 449) "
                          "and wave 23 found the eligibility signal adds to a constant floor. Search the "
                          "two jointly.",
            "signal": "elig = |yesterday's realized Top decile still eligible today| / n_top, causal",
            "rule": "m_frac_t = clip(m_base + k*(elig_t - expanding_mean_of_elig_before_t), 0.95, 1.0)",
            "grid": {"m_base": list(M_BASES), "k": list(K_GRID)},
            "donor_fixed": {"column": DONOR, "provenance": "wave 13 stage 2 argmax"},
            "orderer_fixed": {"members": [W5A_A0B0, SLOW16_A0B0],
                              "weights": [1 - PARTNER_WEIGHT, PARTNER_WEIGHT]},
            "tie_break_eps": TIE_EPS,
            "harness_proof": f"m_base = {REFERENCE_M}, k = 0 must reproduce {REFERENCE} exactly",
            "shipping_recommendation_rule_declared_in_advance": "recommend an arm only if it beats the "
                f"m = {REFERENCE_M} reference on the FULL window AND on BOTH halves (2020-2022 and "
                "2023-2024). An arm that wins the full window by moving one half is a redistribution, "
                "not an improvement. This is a recommendation about what to ship, not a selection gate: "
                "§4 remains highest-full-window-composite and §4 has no materiality threshold.",
            "why_the_both_halves_rule": "the 48-candidate transfer study found Spearman -0.7477 between "
                                        "the two halves, and wave 25 showed this objective is discrete "
                                        "in m with the peak one retained name wide - the exact regime "
                                        "where fine parameter choices have historically not ranked "
                                        "stably",
            "noise_floor_for_context": NOISE_FLOOR,
            "current_best_before_this_wave": REFERENCE,
            "no_test_period_data_read": True,
            "source_sha256": sha(Path(__file__)),
        }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        cs.log(f"wave-26 protocol frozen: {sha(protocol_path)[:16]}…")

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

    unique_days, starts = np.unique(dates, return_index=True)
    ends = np.append(starts[1:], len(dates))
    n_days = len(unique_days)

    # ---- eligibility signal, causal: previous day's realized Top decile from the donor
    elig = np.full(n_days, np.nan)
    in_prev = np.zeros(n_codes, dtype=bool)
    in_cur = np.zeros(n_codes, dtype=bool)
    have_prev = False
    for day_index, (start, end) in enumerate(zip(starts, ends)):
        rows = np.arange(start, end)
        eligible = rows[flags[start:end] == 0]
        if len(eligible) < 100:
            have_prev = False
            continue
        n_top = max(len(eligible) // 10, 1)
        top = eligible[np.argsort(-member[eligible], kind="stable")[:n_top]]
        if have_prev:
            elig[day_index] = int(in_prev[codes[top]].sum()) / n_top
        in_cur[:] = False
        in_cur[codes[top]] = True
        in_prev, in_cur = in_cur, in_prev
        have_prev = True
    centre = np.full(n_days, np.nan)
    total, count = 0.0, 0
    for i, value in enumerate(elig):
        centre[i] = total / count if count else np.nan
        if np.isfinite(value):
            total += float(value)
            count += 1
    cs.log(f"elig signal: {int(np.isfinite(elig).sum())}/{n_days} days, mean {np.nanmean(elig):.6f}, "
           f"sd {np.nanstd(elig):.6f}")

    masks = {str(y): (dates >= y * 10000 + 101) & (dates <= y * 10000 + 1231) for y in YEARS}
    half = {"2020_2022": np.zeros(len(dates), dtype=bool), "2023_2024": np.zeros(len(dates), dtype=bool)}
    for y in (2020, 2021, 2022):
        half["2020_2022"] |= masks[str(y)]
    for y in (2023, 2024):
        half["2023_2024"] |= masks[str(y)]

    results: dict = {}
    proofs: dict = {}
    reference_halves: dict = {}

    def decompose(hybrid: np.ndarray) -> dict:
        out = {}
        for label, mask in half.items():
            metrics, _ = score_official(combined.filter(pl.Series(mask)), hybrid[mask])
            out[label] = metrics["final_score"]
        for year in YEARS:
            mask = masks[str(year)]
            metrics, _ = score_official(combined.filter(pl.Series(mask)), hybrid[mask])
            out[str(year)] = metrics["final_score"]
        return out

    def dump() -> list:
        arms = sorted(((v["connected_final_score"], k, v) for k, v in results.items()
                       if "connected_final_score" in v), reverse=True)
        payload = {"status": "running", "updated_at_local": time.strftime("%Y-%m-%dT%H:%M:%S"),
                   "purpose": "joint (m_base, k) grid for the adaptive floor with a split-half "
                              "decomposition of every arm",
                   "donor_fixed": DONOR, "tie_break_eps": TIE_EPS,
                   "elig_signal": {"days": int(np.isfinite(elig).sum()),
                                   "mean": float(np.nanmean(elig)), "sd": float(np.nanstd(elig))},
                   "harness_proofs": proofs, "reference_halves": reference_halves,
                   "shipping_rule": "beat the m=0.985 reference on the full window AND on both halves",
                   "noise_floor_for_context": NOISE_FLOOR,
                   "current_best_before_this_wave": REFERENCE,
                   "results": results, "n_scored": len(arms),
                   "ranking": [{"arm": k, "connected_final_score": s,
                                "margin_full": s - REFERENCE,
                                "margin_2020_2022": s and v["halves"]["2020_2022"]
                                - reference_halves.get("2020_2022", 0),
                                "margin_2023_2024": v["halves"]["2023_2024"]
                                - reference_halves.get("2023_2024", 0),
                                "recommended_to_ship": v.get("recommended_to_ship"),
                                "annual_excess": v["connected_metrics"]["annual_excess"],
                                "mean_turnover": v["connected_metrics"]["mean_turnover"]}
                               for s, k, v in arms[:25]],
                   "best": arms[0][1] if arms else None,
                   "best_connected_final_score": arms[0][0] if arms else None,
                   "best_recommended_to_ship": next((k for s, k, v in arms
                                                     if v.get("recommended_to_ship")), None),
                   "no_test_period_data_read": True,
                   "source_sha256": sha(Path(__file__))}
        (HERE / "wave26_results.json").write_text(
            json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        return arms

    def score(name: str, m_fracs: np.ndarray, extra: dict) -> float:
        hybrid, stats = build_adaptive(member, orderer, dates, flags, codes, n_codes, m_fracs)
        metrics, _ = score_official(combined, hybrid)
        halves = decompose(hybrid)
        if name == "reference_m0.985":
            reference_halves.update(halves)
            recommended = None
        else:
            recommended = bool(
                metrics["final_score"] > REFERENCE
                and reference_halves
                and halves["2020_2022"] > reference_halves["2020_2022"]
                and halves["2023_2024"] > reference_halves["2023_2024"])
        results[name] = {**extra, "connected_final_score": metrics["final_score"],
                         "connected_metrics": metrics, "halves": halves,
                         "margin_full": metrics["final_score"] - REFERENCE,
                         "boundary_tie_days": stats["boundary_tie_days"],
                         "swaps": stats["swaps"], "m_frac_used": stats["m_frac_used"],
                         "mean_retention_ratio": stats["mean_retention_ratio"],
                         "recommended_to_ship": recommended}
        cs.log(f"{name[:26]:26s} CONNECTED {metrics['final_score']:.9f} "
               f"({metrics['final_score'] - REFERENCE:+.2e}) | 2020-22 {halves['2020_2022']:.9f} "
               f"| 2023-24 {halves['2023_2024']:.9f} | ship={recommended}")
        dump()
        return metrics["final_score"]

    # ---- harness proof / reference
    got = score("reference_m0.985", np.full(n_days, REFERENCE_M),
                {"signal": "none", "m_base": REFERENCE_M, "k": 0.0, "role": "harness_proof"})
    proofs["P_reference"] = {"scored": got, "expected": REFERENCE, "abs_diff": abs(got - REFERENCE),
                             "halves": dict(reference_halves)}
    if abs(got - REFERENCE) > 1e-12:
        raise AssertionError(f"harness proof failed: {got!r} vs {REFERENCE!r}")
    cs.log(f"harness proof passed; reference halves {reference_halves['2020_2022']:.9f} / "
           f"{reference_halves['2023_2024']:.9f}")

    for m_base in M_BASES:
        for k in K_GRID:
            if k == 0.0 and abs(m_base - REFERENCE_M) < 1e-12:
                continue
            deviation = np.where(np.isfinite(elig) & np.isfinite(centre), elig - centre, 0.0)
            m_fracs = np.clip(m_base + k * deviation, CLIP[0], CLIP[1])
            score(f"m{m_base:g}_k{k:+.2f}", m_fracs,
                  {"signal": "elig", "m_base": m_base, "k": k})
        # the constant floor at this m_base, so the adaptive gain is separable from the grid gain
        if abs(m_base - REFERENCE_M) > 1e-12:
            score(f"const_m{m_base:g}", np.full(n_days, m_base),
                  {"signal": "none", "m_base": m_base, "k": 0.0})

    arms = dump()
    payload = json.loads((HERE / "wave26_results.json").read_text(encoding="utf-8"))
    payload["status"] = "complete"
    payload["completed_at_local"] = time.strftime("%Y-%m-%dT%H:%M:%S")
    (HERE / "wave26_results.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print("\n| arm | CONNECTED | margin full | margin 2020-22 | margin 2023-24 | ship? |")
    print("|---|---|---|---|---|---|")
    for s, name, v in arms[:18]:
        print(f"| {name[:20]} | **{s:.9f}** | {v['margin_full']:+.2e} | "
              f"{v['halves']['2020_2022'] - reference_halves['2020_2022']:+.2e} | "
              f"{v['halves']['2023_2024'] - reference_halves['2023_2024']:+.2e} | "
              f"{'YES' if v.get('recommended_to_ship') else '-'} |")
    best_ship = payload["best_recommended_to_ship"]
    cs.log(f"best by §4: {arms[0][1]} {arms[0][0]:.9f}")
    cs.log(f"best that also wins both halves: {best_ship or 'NONE'}")


if __name__ == "__main__":
    main()
