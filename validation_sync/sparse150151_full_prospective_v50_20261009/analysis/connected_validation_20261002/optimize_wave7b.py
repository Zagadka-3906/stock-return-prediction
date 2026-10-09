"""Wave 7b: swap-budgeted Top-set selection with the construction defect from wave 7 fixed.

Wave 7's second harness proof failed and was right to: with base == orderer and m = 0 the transform
must be the identity, but it returned 0.427240 instead of peer67_slow16's 0.427407938. The cause is
the construction, not the swap budget. Wave 7 LIFTED the chosen set above every other row by adding a
large offset, which also demotes limit-up names that outranked them. Limit-up rows are excluded from
the excess and turnover universes but INCLUDED in the Rank IC universe, so that demotion moves the IC
term as a side effect nobody intended, and it makes the identity case not an identity.

Fix: the evaluator filters to flag_limit_up == 0 before choosing the Top decile, so only the ordering
WITHIN the eligible subset can affect excess and turnover. Therefore reassign the eligible rows' own
score values among themselves - the chosen set receives the n_top largest eligible values in the
orderer's order, the remaining eligible rows receive the rest in the orderer's order, and ineligible
rows are left completely untouched. The multiset of scores is preserved, the intervention is confined
to the subset the metric actually reads, and base == orderer with m = 0 becomes a true identity.

That identity is the harness proof here, and it must reproduce 0.427407938 to 1e-12.

The m grid is refined near 1 because the binding region is there: retention ratio rho maps to Jaccard
turnover as 1 - rho/(2-rho), so rho 0.95 -> 0.0952, 0.98 -> 0.0392, 0.99 -> 0.0201.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
import time
import traceback
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(HERE))
import connected_scorer as cs  # noqa: E402
from experiments.revalidate_fold_local import score_official  # noqa: E402

M_FRACTIONS = (0.0, 0.90, 0.95, 0.97, 0.98, 0.985, 0.99, 0.993, 0.995, 0.997, 1.0)
LIFT_LEADER = 0.431343420


def identity_expected() -> float:
    """peer67_slow16's own connected score, read from the recorded results rather than retyped."""
    results = json.loads((HERE / "connected_results_all.json").read_text(encoding="utf-8"))["results"]
    return float(results["peer67_slow16"]["connected_final_score"])


def load(stem: str) -> np.ndarray:
    """Wave 1-3 saved connected_pred_<stem>.npy; wave 6 saved pp_<stem>.npy. Accept either."""
    for prefix in ("connected_pred_", ""):
        path = HERE / f"{prefix}{stem}.npy"
        if path.exists():
            return np.load(path)
    raise SystemExit(f"no saved connected prediction for {stem}")
# (label, base stem, orderer stem, m values to run)
CONFIGS = [
    ("identity_slow16", "peer67_slow16", "peer67_slow16", (0.0,)),
    ("topk_x_W5a", "topk", "W5a_five_way_with_gru__final_sweep_eval", M_FRACTIONS),
    ("topk_x_slow16", "topk", "peer67_slow16", M_FRACTIONS),
    ("a0b015_self", "pp_a0_b0.15_top_only_w0.25_rl1_tcw1",
     "pp_a0_b0.15_top_only_w0.25_rl1_tcw1", M_FRACTIONS),
    ("a0b015_x_W5a", "pp_a0_b0.15_top_only_w0.25_rl1_tcw1",
     "W5a_five_way_with_gru__final_sweep_eval", M_FRACTIONS),
    ("a0b0_self", "pp_a0_b0_top_only_w0.25_rl1_tcw1",
     "pp_a0_b0_top_only_w0.25_rl1_tcw1", M_FRACTIONS),
]


def sha(path) -> str:
    value = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for chunk in iter(lambda: stream.read(8 * 1024 * 1024), b""):
            value.update(chunk)
    return value.hexdigest()


def build(base: np.ndarray, orderer: np.ndarray, dates: np.ndarray, flags: np.ndarray,
          codes: np.ndarray, n_codes: int, m_frac: float) -> tuple[np.ndarray, dict]:
    out = orderer.copy()
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

        # reassign the eligible rows' own values: chosen gets the n_top largest, in orderer order
        values = orderer[eligible]
        order_e = np.argsort(-values, kind="stable")
        sorted_values = values[order_e]
        chosen_local = np.isin(eligible, chosen)
        s_pos = order_e[chosen_local[order_e]]
        ns_pos = order_e[~chosen_local[order_e]]
        if len(s_pos) != n_top:
            raise AssertionError("slot reassignment size mismatch")
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


def freeze() -> None:
    inputs = {}
    for label, base, orderer, _ in CONFIGS:
        for stem in {base, orderer}:
            path = HERE / f"connected_pred_{stem}.npy"
            inputs[stem] = {"exists": path.exists(),
                            "sha256": sha(path) if path.exists() else None}
    payload = {
        "frozen_at_local": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "supersedes": "optimize_wave7.py lift construction; see wave7 failure record "
                      "failure_wave7_run_1790900183841448900.json",
        "defect_fixed": "lifting the chosen set above every row also demoted limit-up names, which are "
                        "excluded from the excess/turnover universes but included in Rank IC, so the "
                        "transform was not the identity when base == orderer",
        "construction": "reassign the eligible subset's own score values among themselves: the chosen "
                        "set receives the n_top largest in orderer order, the rest receive the "
                        "remainder in orderer order, ineligible rows untouched",
        "standard": "后续选模标准.md §3 connected composite primary; §4 highest score wins",
        "status": "in_sample_selection_disclosed",
        "m_fractions": list(M_FRACTIONS),
        "configs": [{"label": l, "base": b, "orderer": o, "m": list(mm)} for l, b, o, mm in CONFIGS],
        "harness_proof": f"identity_slow16 at m=0 must reproduce {identity_expected()!r} to 1e-12; "
                         f"topk_x_W5a at m=0 is compared against the wave-7 lift value {LIFT_LEADER} "
                         "to measure what the limit-up demotion was costing",
        "selection_rule": "highest connected 2020-2024 official composite; ties broken by smaller m "
                          "then simpler base",
        "disclosed_selection_cost": "all settings are maximized over five repeatedly viewed years with "
                                    "no blind period remaining; the winner's score carries an upward "
                                    "selection bias this protocol cannot quantify",
        "causality": "the retention constraint uses only the previous day's realized Top decile, a "
                     "function of past predictions and past limit-up flags; no label or label "
                     "availability is read",
        "inputs": inputs, "no_test_period_data_read": True,
        "source_sha256": sha(Path(__file__)),
    }
    if (HERE / "protocol_wave7b.json").exists():
        raise FileExistsError("protocol already frozen")
    (HERE / "protocol_wave7b.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    cs.log(f"wave-7b protocol frozen: {len(CONFIGS)} configs, m grid {list(M_FRACTIONS)}")


def run() -> None:
    protocol = json.loads((HERE / "protocol_wave7b.json").read_text(encoding="utf-8"))
    assert protocol["source_sha256"] == sha(Path(__file__)), "script changed after freezing"
    frame = cs.combined_frame()
    dates = frame["trade_date"].to_numpy()
    flags = frame["flag_limit_up"].to_numpy()
    codes, uniques = pd.factorize(frame["ts_code"].to_pandas(), sort=True)
    codes = codes.astype(np.int64)
    n_codes = len(uniques)

    results, proofs = {}, {}
    for label, base_stem, orderer_stem, m_values in CONFIGS:
        base = load(base_stem)
        orderer = load(orderer_stem)
        for m_frac in m_values:
            name = f"{label}__m{m_frac:g}"
            pred, stats = build(base, orderer, dates, flags, codes, n_codes, m_frac)
            metrics, _ = score_official(frame, pred)
            if label == "identity_slow16":
                expected = identity_expected()
                diff = abs(metrics["final_score"] - expected)
                proofs[name] = {"expected": expected, "got": metrics["final_score"],
                                "abs_diff": diff, "passed": bool(diff <= 1e-12)}
                if diff > 1e-12:
                    raise AssertionError(f"{name}: identity gave {metrics['final_score']!r}, "
                                         f"expected {expected!r} (diff {diff:.3e})")
                cs.log(f"{name}: IDENTITY PROOF passed to {diff:.1e}")
            np.save(HERE / f"wave7b_{name}.npy", pred)
            results[name] = {"label": label, "base": base_stem, "orderer": orderer_stem,
                             "m_frac": m_frac, "connected_final_score": metrics["final_score"],
                             "connected_metrics": metrics, "stats": stats}
            cs.log(f"{name}: CONNECTED {metrics['final_score']:.9f} (ic {metrics['ic_mean']:.6f}, "
                   f"excess {metrics['annual_excess']:.6f}, turnover {metrics['mean_turnover']:.6f}) "
                   f"retention {stats['mean_retention_ratio']}")
            del pred

    ranked = sorted(results.items(), key=lambda kv: -kv[1]["connected_final_score"])
    payload = {"status": "complete", "completed_at_local": time.strftime("%Y-%m-%dT%H:%M:%S"),
               "protocol_sha256": sha(HERE / "protocol_wave7b.json"),
               "identity_proof": proofs, "results": results,
               "wave7_lift_leader_for_comparison": LIFT_LEADER,
               "same_config_slot_reassigned": results.get("topk_x_W5a__m0", {}).get(
                   "connected_final_score"),
               "best": ranked[0][0],
               "best_connected_final_score": ranked[0][1]["connected_final_score"],
               "gain_over_lift_leader": ranked[0][1]["connected_final_score"] - LIFT_LEADER,
               "no_test_period_data_read": True}
    (HERE / "wave7b_results.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("\n| rank | config | m | CONNECTED | IC | excess | turnover | retention |")
    print("|---|---|---|---|---|---|---|---|")
    for i, (name, v) in enumerate(ranked):
        m = v["connected_metrics"]
        print(f"| {i+1} | {v['label']} | {v['m_frac']:g} | **{m['final_score']:.9f}** | "
              f"{m['ic_mean']:.6f} | {m['annual_excess']:.6f} | {m['mean_turnover']:.6f} | "
              f"{v['stats']['mean_retention_ratio']} |")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("stage", choices=("freeze", "run"))
    args = parser.parse_args()
    try:
        globals()[args.stage]()
    except BaseException as error:
        (HERE / f"failure_wave7b_{args.stage}_{time.time_ns()}.json").write_text(
            json.dumps({"stage": args.stage, "type": type(error).__name__, "message": str(error),
                        "traceback": traceback.format_exc()}, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8")
        raise
