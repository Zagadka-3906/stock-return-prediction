"""Wave 13: with W5a established as the orderer, re-search everything that was tuned against slow16.

Wave 12 showed the orderer role wants maximum IC and no smoothing, and the winner was the five-way
GRU ensemble W5a (0.441064514) rather than peer67_slow16 (0.440149630). That invalidates three
earlier tuning decisions, all of which were made with a slow16-family orderer held fixed:

  stage 1  the retention floor m was optimized in wave 10/11 against the slow16 orderer. Excess now
           comes from a different ordering, so the m optimum can move.
  stage 2  the membership donor was searched exhaustively in wave 8/9 against a slow16 orderer.
           Membership sets the turnover term and the candidate pool for excess; with W5a ordering
           inside the Top set, a donor that was previously dominated may now win.
  stage 3  the orderer has two separable jobs that every wave so far forced onto one column. Excess
           reads only the ordering WITHIN the chosen Top decile (the filtered universe's own top
           len//10 is a prefix of the chosen set, because every chosen row is assigned a value above
           every non-chosen row). IC reads the whole ordering, and ~81% of eligible pairs are
           rest-vs-rest. So A = the within-Top orderer drives excess, B = the rest orderer drives IC,
           and nothing but habit says A == B.

Two harness proofs run before any new arm is scored:
  P1  build_ab with base == A == B at m == 0 and no tie-break must be the identity, reproducing
      W5a's own recorded connected score 0.426451498 exactly.
  P2  build_ab with A == B must return a bit-identical array to wave 7b's build for the same base,
      m and tie-break, so stage 3 generalizes rather than replaces the shipped construction.

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
from optimize_wave7b import build  # noqa: E402

TIE_EPS = 1e-9
W5A_ORDERER = "orderer_a0b0_W5a_five_way_with_gru__final_sweep_eval"
W5A_FINISHED = "W5a_five_way_with_gru__final_sweep_eval"
CURRENT_BEST = 0.44106451391794665
CURRENT_BEST_NAME = "topk_x_W5a_a0_b0_m0.985_tiebreak"

M_GRID = (0.0, 0.90, 0.95, 0.97, 0.98, 0.985, 0.99, 0.993, 0.995, 0.997, 1.0)

DONORS = [
    "topk", "peer67_slow16", "peer67_slow8", W5A_FINISHED,
    "W3e_rank_average__final_sweep_eval", "W5b_gru_half_weight__final_sweep_eval",
    "W6a_daily_rank_features__final_sweep_eval", "W6b_daily_zscore_features__final_sweep_eval",
    "W8a_zscore_mean__final_sweep_eval", "W8b_trimmed_mean__final_sweep_eval",
    "pooled_rms25", "ensemble4_r4", "ensemble4_old_pruned", "base63_8", "hybrid",
    "top2_lightgbm", "xgb_two_mean", "slow_only8", "slow8_monthly",
    "raw_extended83__wave15_paired_features_20260927",
    "raw_deployed67_slow__wave23_validation_20260928",
    "raw_base63_plus_peer__wave21_peer_lags_20260928",
    "raw_control63__wave23_validation_20260928",
    "hybrid_k1_topk_x_W5a_five_way_with_gru", "hybrid_k2_topk_x_W5a_five_way_with_gru",
    "pp_a0.9_b0.3_top_only_w0.25_rl1_tcw1", "pp_a0.9_b0.6_top_only_w0.25_rl1_tcw1",
    "pp_a0.8_b0.6_top_only_w0.25_rl1_tcw1", "pp_a0_b0_top_only_w0.25_rl1_tcw1",
    "pp_a0_b0.15_top_only_w0.25_rl1_tcw1",
]


def sha(path) -> str:
    value = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for chunk in iter(lambda: stream.read(8 * 1024 * 1024), b""):
            value.update(chunk)
    return value.hexdigest()


def load(stem: str) -> np.ndarray:
    for prefix in ("", "connected_pred_", "orderer_a0b0_", "pp_"):
        path = HERE / f"{prefix}{stem}.npy"
        if path.exists():
            return np.load(path)
    raise SystemExit(f"no saved fold column for {stem}")


def build_ab(base: np.ndarray, orderer_top: np.ndarray, orderer_rest: np.ndarray, dates: np.ndarray,
             flags: np.ndarray, codes: np.ndarray, n_codes: int,
             m_frac: float) -> tuple[np.ndarray, dict]:
    """Wave 7b's swap-budget construction with the orderer's two roles split.

    Membership and the retention floor are decided by `base` alone, identically to wave 7b. Then the
    eligible rows' own values - taken from `orderer_rest`, so the multiset is preserved - are
    reassigned: the chosen set receives the n_top largest, ordered among themselves by `orderer_top`,
    and the remaining eligible rows receive the rest in `orderer_rest` order. Ineligible rows are
    untouched, because limit-up names sit inside the Rank IC universe.
    """
    out = orderer_rest.copy()
    _, starts = np.unique(dates, return_index=True)
    ends = np.append(starts[1:], len(dates))
    in_prev = np.zeros(n_codes, dtype=bool)
    in_cur = np.zeros(n_codes, dtype=bool)
    stats = {"days": 0, "m_frac": m_frac, "retention": [], "boundary_tie_days": 0,
             "eligibility_limited_days": 0, "swaps": 0}
    have_prev = False
    for start, end in zip(starts, ends):
        rows = np.arange(start, end)
        eligible = rows[flags[start:end] == 0]
        if len(eligible) < 100:
            have_prev = False
            continue
        n_top = max(len(eligible) // 10, 1)
        m = int(round(m_frac * n_top))
        scores = base[eligible]
        order = np.argsort(-scores, kind="stable")
        unconstrained = eligible[order[:n_top]]
        if not have_prev or m == 0:
            chosen = unconstrained
        else:
            pool = eligible[in_prev[codes[eligible]]]
            if len(pool) < m:
                stats["eligibility_limited_days"] += 1
                m = len(pool)
            held = in_prev[codes[unconstrained]]
            r = int(held.sum())
            if r >= m:
                chosen = unconstrained
            else:
                need = m - r
                not_held = np.flatnonzero(~held)
                drop = not_held[np.argsort(scores[order[:n_top]][not_held], kind="stable")][:need]
                keep = np.setdiff1d(np.arange(n_top), drop, assume_unique=True)
                picked = set(codes[unconstrained[keep]].tolist())
                add = []
                for idx in np.argsort(-base[pool], kind="stable"):
                    if len(add) >= need:
                        break
                    code = codes[pool[idx]]
                    if code in picked:
                        continue
                    add.append(int(pool[idx]))
                    picked.add(code)
                if len(add) != need:
                    raise AssertionError("swap budget could not be met")
                chosen = np.concatenate([unconstrained[keep], np.array(add, dtype=np.int64)])
                stats["swaps"] += need
        if len(chosen) != n_top or len(np.unique(codes[chosen])) != n_top:
            raise AssertionError("chosen set is not exactly n_top distinct names")

        values = orderer_rest[eligible]
        order_e = np.argsort(-values, kind="stable")
        sorted_values = values[order_e]
        chosen_local = np.isin(eligible, chosen)
        s_pos = order_e[chosen_local[order_e]]
        ns_pos = order_e[~chosen_local[order_e]]
        if len(s_pos) != n_top:
            raise AssertionError("slot reassignment size mismatch")
        # order the chosen slots by orderer_top instead; ns_pos is already orderer_rest-descending
        a_vals = orderer_top[eligible][s_pos]
        s_pos = s_pos[np.argsort(-a_vals, kind="stable")]
        if n_top < len(sorted_values) and sorted_values[n_top - 1] == sorted_values[n_top]:
            stats["boundary_tie_days"] += 1
        new_values = np.empty_like(values)
        new_values[s_pos] = sorted_values[:n_top]
        new_values[ns_pos] = sorted_values[n_top:]
        out[eligible] = new_values

        stats["days"] += 1
        stats["retention"].append(int(in_prev[codes[chosen]].sum()) / n_top if have_prev else np.nan)
        in_cur[:] = False
        in_cur[codes[chosen]] = True
        in_prev, in_cur = in_cur, in_prev
        have_prev = True
    if not np.isfinite(out).all():
        raise AssertionError("non-finite prediction")
    known = np.array([r for r in stats["retention"] if not np.isnan(r)])
    stats["mean_retention_ratio"] = float(known.mean()) if len(known) else None
    stats["retention"] = None
    return out, stats


def main() -> None:
    protocol_path = HERE / "protocol_wave13.json"
    if not protocol_path.exists():
        protocol_path.write_text(json.dumps({
            "frozen_at_local": time.strftime("%Y-%m-%dT%H:%M:%S"),
            "standard": "后续选模标准.md §3 connected composite primary; §4 highest score wins",
            "status": "in_sample_selection_disclosed",
            "hypothesis": "wave 12 replaced the orderer, so the retention floor (tuned in wave 10/11), "
                          "the membership donor (searched in wave 8/9) and the assumption that one "
                          "column must serve both orderer roles are all stale. Re-search all three.",
            "stage1": {"what": "retention floor m", "donor": "topk", "orderer": W5A_ORDERER,
                       "grid": list(M_GRID)},
            "stage2": {"what": "membership donor", "m": "stage-1 argmax", "orderer": W5A_ORDERER,
                       "donors": DONORS},
            "stage3": {"what": "decouple the orderer into A (within the chosen Top decile, drives "
                               "excess) and B (the remaining eligible rows, drives most of IC)",
                       "donor": "stage-2 argmax", "m": "stage-1 argmax",
                       "A_grid": "the five best excess drivers from wave 12",
                       "B_grid": "every saved alpha 0 / bonus 0 backbone column"},
            "tie_break_eps": TIE_EPS,
            "tie_break_key": "1 - ts_code_rank/(n_codes-1), causal and label-free",
            "harness_proofs": {
                "P1": f"build_ab(base=orderer_top=orderer_rest={W5A_FINISHED}, m=0, no tie-break) must "
                      "be the identity and reproduce W5a's recorded connected score 0.426451498",
                "P2": "build_ab with A == B must return a bit-identical array to wave 7b's build for "
                      "the same base, m and tie-break",
            },
            "current_best_before_this_wave": {"name": CURRENT_BEST_NAME,
                                              "connected_final_score": CURRENT_BEST},
            "selection_rule": "highest connected 2020-2024 official composite; no significance, "
                              "worst-year or single-metric gate (后续选模标准.md §4)",
            "disclosed_selection_cost": "ninth consecutive search over the same five viewed years; no "
                                        "blind period remains and the winner carries upward "
                                        "selection bias this protocol cannot quantify",
            "causality": "membership uses the donor's own prediction; the retention floor uses the "
                         "previous day's realized Top decile, a function of past predictions and past "
                         "limit-up flags. No label or label availability is read.",
            "no_test_period_data_read": True,
            "source_sha256": sha(Path(__file__)),
        }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        cs.log(f"wave-13 protocol frozen: {sha(protocol_path)[:16]}…")

    combined = cs.combined_frame()
    dates = combined["trade_date"].to_numpy()
    flags = combined["flag_limit_up"].to_numpy().astype(np.int64)
    codes, uniques = pd.factorize(combined["ts_code"].to_pandas(), sort=True)
    codes = codes.astype(np.int64)
    n_codes = len(uniques)
    tie_key = 1.0 - codes / max(n_codes - 1, 1)
    results: dict = {"stage1_m": {}, "stage2_donor": {}, "stage3_decoupled": {}}
    proofs = {}
    stage_argmax: dict = {"best_m": None, "best_donor": None}

    # ---- P1: identity, no tie-break
    w5a_fin = load(W5A_FINISHED)
    ident, ident_stats = build_ab(w5a_fin, w5a_fin, w5a_fin, dates, flags, codes, n_codes, 0.0)
    if not np.array_equal(ident, w5a_fin):
        raise AssertionError("P1 failed: build_ab at m=0 with base == A == B is not the identity")
    ident_metrics, _ = score_official(combined, ident)
    recorded = json.loads((HERE / "connected_results_all.json").read_text(encoding="utf-8"))
    expected = float(recorded["results"][W5A_FINISHED]["connected_final_score"])
    proofs["P1_identity"] = {"array_equal_to_input": True,
                             "scored": ident_metrics["final_score"], "recorded": expected,
                             "abs_diff": abs(ident_metrics["final_score"] - expected)}
    if abs(ident_metrics["final_score"] - expected) > 1e-12:
        raise AssertionError(f"P1 failed: identity scored {ident_metrics['final_score']!r}, "
                             f"recorded {expected!r}")
    cs.log(f"P1 passed: identity reproduces W5a's connected score to "
           f"{proofs['P1_identity']['abs_diff']:.1e}")

    # ---- P2: A == B reduces exactly to wave 7b's build
    member0 = load("topk")
    ord0 = load(W5A_ORDERER) + TIE_EPS * tie_key
    ref, _ = build(member0, ord0, dates, flags, codes, n_codes, 0.985)
    ab, _ = build_ab(member0, ord0, ord0, dates, flags, codes, n_codes, 0.985)
    max_diff = float(np.abs(ref - ab).max())
    proofs["P2_reduces_to_wave7b"] = {"max_abs_array_diff": max_diff,
                                      "bit_identical": bool(np.array_equal(ref, ab))}
    if not np.array_equal(ref, ab):
        raise AssertionError(f"P2 failed: A == B is not bit-identical to wave 7b (max diff {max_diff:.3e})")
    cs.log("P2 passed: build_ab with A == B is bit-identical to the shipped wave-7b construction")

    def dump(status: str = "running") -> None:
        all_arms = [(f"{bucket}::{key}", v)
                    for bucket in results for key, v in results[bucket].items()
                    if "connected_final_score" in v]
        all_arms.sort(key=lambda kv: -kv[1]["connected_final_score"])
        payload = {"status": status, "updated_at_local": time.strftime("%Y-%m-%dT%H:%M:%S"),
                   "purpose": "re-search m, the membership donor and the orderer roles against W5a",
                   "harness_proofs": proofs, "tie_break_eps": TIE_EPS,
                   "stage1_best_m": stage_argmax["best_m"],
                   "stage2_best_donor": stage_argmax["best_donor"],
                   "current_best_before_this_wave": {"name": CURRENT_BEST_NAME,
                                                     "connected_final_score": CURRENT_BEST},
                   "results": results,
                   "ranking": [{"arm": k, "connected_final_score": v["connected_final_score"],
                                "ic_mean": v["connected_metrics"]["ic_mean"],
                                "annual_excess": v["connected_metrics"]["annual_excess"],
                                "mean_turnover": v["connected_metrics"]["mean_turnover"],
                                "boundary_tie_days": v["boundary_tie_days"]} for k, v in all_arms[:25]],
                   "n_scored": len(all_arms),
                   "best": all_arms[0][0] if all_arms else None,
                   "best_connected_final_score": all_arms[0][1]["connected_final_score"] if all_arms else None,
                   "improves_on_current_best": bool(all_arms and all_arms[0][1]["connected_final_score"]
                                                    > CURRENT_BEST),
                   "no_test_period_data_read": True,
                   "source_sha256": sha(Path(__file__))}
        (HERE / "wave13_results.json").write_text(
            json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        return all_arms

    def score_arm(key: str, bucket: str, base: np.ndarray, a: np.ndarray, b: np.ndarray,
                  m_frac: float, extra: dict) -> float:
        hybrid, stats = build_ab(base, a + TIE_EPS * tie_key, b + TIE_EPS * tie_key,
                                 dates, flags, codes, n_codes, m_frac)
        metrics, _ = score_official(combined, hybrid)
        results[bucket][key] = {**extra, "m_frac": m_frac,
                                "connected_final_score": metrics["final_score"],
                                "connected_metrics": metrics,
                                "boundary_tie_days": stats["boundary_tie_days"],
                                "eligibility_limited_days": stats["eligibility_limited_days"],
                                "swaps": stats["swaps"],
                                "mean_retention_ratio": stats["mean_retention_ratio"],
                                "beats_current_best": bool(metrics["final_score"] > CURRENT_BEST)}
        cs.log(f"{key[:64]:64s} CONNECTED {metrics['final_score']:.9f} "
               f"(ic {metrics['ic_mean']:.6f}, excess {metrics['annual_excess']:.6f}, "
               f"turn {metrics['mean_turnover']:.6f})")
        dump()  # checkpoint after every scored arm: wave 9 lost eleven pairs to one crash
        return metrics["final_score"]

    # ---- stage 1: retention floor
    for m_frac in M_GRID:
        score_arm(f"m{m_frac:g}", "stage1_m", member0, ord0, ord0, m_frac,
                  {"donor": "topk", "orderer_A": W5A_ORDERER, "orderer_B": W5A_ORDERER})
    best_m = max(results["stage1_m"].items(), key=lambda kv: kv[1]["connected_final_score"])[0]
    best_m = float(best_m[1:])
    stage_argmax["best_m"] = best_m
    cs.log(f"stage 1 argmax: m = {best_m:g}")

    # ---- stage 2: membership donor
    for stem in DONORS:
        try:
            score_arm(stem, "stage2_donor", load(stem), ord0, ord0, best_m,
                      {"donor": stem, "orderer_A": W5A_ORDERER, "orderer_B": W5A_ORDERER})
        except BaseException as error:  # noqa: BLE001 - record and keep going
            results["stage2_donor"][stem] = {"donor": stem, "error": f"{type(error).__name__}: {error}"}
            cs.log(f"{stem[:64]:64s} FAILED {type(error).__name__}: {error}")
    ok2 = {k: v for k, v in results["stage2_donor"].items() if "connected_final_score" in v}
    best_donor = max(ok2.items(), key=lambda kv: kv[1]["connected_final_score"])[0]
    best_base = load(best_donor)
    stage_argmax["best_donor"] = best_donor
    cs.log(f"stage 2 argmax: donor = {best_donor}")

    # ---- stage 3: decouple A and B
    wave12 = json.loads((HERE / "wave12_results.json").read_text(encoding="utf-8"))["results"]
    by_excess = sorted(((v["connected_metrics"]["annual_excess"], k) for k, v in wave12.items()
                        if "connected_metrics" in v), reverse=True)
    # wave 12 saved its columns under label[:60], so resolve through the same truncation
    a_grid = []
    for _, label in by_excess[:5]:
        stem = f"orderer_a0b0_{label[:60]}"
        if (HERE / f"{stem}.npy").exists() and stem not in a_grid:
            a_grid.append(stem)
    b_grid = sorted(p.name[:-4] for p in HERE.glob("orderer_a0b0_*.npy"))

    def guarded(key: str, a_stem: str, b_stem: str) -> None:
        try:
            score_arm(key, "stage3_decoupled", best_base, load(a_stem), load(b_stem), best_m,
                      {"donor": best_donor, "orderer_A": a_stem, "orderer_B": b_stem})
        except BaseException as error:  # noqa: BLE001 - record and keep going
            results["stage3_decoupled"][key] = {"donor": best_donor, "orderer_A": a_stem,
                                                "orderer_B": b_stem,
                                                "error": f"{type(error).__name__}: {error}"}
            cs.log(f"{key[:64]:64s} FAILED {type(error).__name__}: {error}")
            dump()

    for stem in b_grid:
        if stem != W5A_ORDERER:
            guarded(f"A=W5a__B={stem}", W5A_ORDERER, stem)
    for stem in a_grid:
        if stem != W5A_ORDERER:
            guarded(f"A={stem}__B=W5a", stem, W5A_ORDERER)
    guarded("A=W5a__B=W5a", W5A_ORDERER, W5A_ORDERER)  # coupled reference at stage-2 donor and m

    all_arms = dump("complete")
    payload = json.loads((HERE / "wave13_results.json").read_text(encoding="utf-8"))
    payload["stage1_best_m"] = best_m
    payload["stage2_best_donor"] = best_donor
    (HERE / "wave13_results.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    cs.log(f"best: {payload['best']} {payload['best_connected_final_score']:.9f} "
           f"({'IMPROVES' if payload['improves_on_current_best'] else 'does not improve'})")

    print("\n| rank | arm | CONNECTED | IC | excess | turnover |")
    print("|---|---|---|---|---|---|")
    for i, (key, v) in enumerate(all_arms[:20]):
        m = v["connected_metrics"]
        print(f"| {i+1} | {key[:64]} | **{m['final_score']:.9f}** | {m['ic_mean']:.6f} | "
              f"{m['annual_excess']:.6f} | {m['mean_turnover']:.6f} |")


if __name__ == "__main__":
    main()
