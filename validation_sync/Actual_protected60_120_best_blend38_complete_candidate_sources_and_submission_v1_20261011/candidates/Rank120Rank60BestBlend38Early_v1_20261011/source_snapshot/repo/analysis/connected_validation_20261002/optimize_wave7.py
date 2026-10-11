"""Wave 7: exact cardinality-constrained (swap-budgeted) Top-set selection.

The metric splits cleanly: Rank IC reads the whole score vector, while the excess and Jaccard terms
read only which n_top names sit in the Top decile. Wave 6 showed the post-processing stack can buy a
large amount of IC and excess by smoothing less - alpha 0 / bonus 0.15 reaches IC 0.127568 and
annualized excess 0.539766 against the released 0.117367 / 0.305583 - but pays for it with turnover
0.597550, which the 0.3-weighted turnover term more than claws back. So the headroom is not in the
predictor, it is in choosing the decile subject to an explicit persistence constraint.

Mechanism, exact rather than an additive score distortion (which is why wave 5's M2/M3 failed):
for each day t, with S_{t-1} the Top decile the evaluator actually realized yesterday,
  U = the n_top highest-scoring eligible names today                (unconstrained choice)
  r = |U cap S_{t-1}|
  if r >= m:  S_t = U
  else:       swap out the (m - r) lowest-scoring names of U \\ S_{t-1} and swap in the (m - r)
              highest-scoring names of S_{t-1} \\ U
This maximizes the total base score of the chosen set subject to |S_t cap S_{t-1}| >= m, so m is a
single interpretable knob trading excess against turnover. m = 0 is the unconstrained solution and
m = n_top freezes the portfolio entirely.

Then S_t is lifted above every other name and ordered internally by the ORDERER, which is what makes
this composable with the wave-4/5 Top-set substitution scheme.

Built-in harness proof, not a separate stage: at m = 0 the construction must reproduce, to the last
digit, (a) the wave-4/5 leader 0.431343420 for base=topk / orderer=W5a, and (b) 0.427407938 for
base=orderer=peer67_slow16, where lifting a set to the top and re-ordering it by the same score is the
identity transform. If either fails the implementation is wrong and nothing else is reported.

Selection is by the highest connected 2020-2024 composite per 后续选模标准.md §4; the cost of scanning
m on five viewed years is disclosed in the protocol. No test-period data is read.
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

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(HERE))
import connected_scorer as cs  # noqa: E402
from experiments.revalidate_fold_local import score_official  # noqa: E402

M_FRACTIONS = (0.0, 0.30, 0.50, 0.70, 0.80, 0.90, 0.95, 1.0)
# (label, base prediction file stem, orderer prediction file stem, expected score at m=0 or None)
CONFIGS = [
    ("topk_x_W5a", "topk", "W5a_five_way_with_gru__final_sweep_eval", 0.431343420),
    ("slow16_self", "peer67_slow16", "peer67_slow16", 0.427407938),
    ("alpha0_bonus0p15_self", "pp_a0_b0.15_top_only_w0.25_rl1_tcw1",
     "pp_a0_b0.15_top_only_w0.25_rl1_tcw1", None),
    ("alpha0_bonus0_self", "pp_a0_b0_top_only_w0.25_rl1_tcw1",
     "pp_a0_b0_top_only_w0.25_rl1_tcw1", None),
    ("alpha0_bonus0p15_x_W5a", "pp_a0_b0.15_top_only_w0.25_rl1_tcw1",
     "W5a_five_way_with_gru__final_sweep_eval", None),
    ("topk_x_slow16", "topk", "peer67_slow16", 0.428891359),
]
TOL_M0 = 2e-9


def sha(path) -> str:
    value = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for chunk in iter(lambda: stream.read(8 * 1024 * 1024), b""):
            value.update(chunk)
    return value.hexdigest()


def load(stem: str) -> np.ndarray:
    for prefix in ("connected_pred_", ""):
        path = HERE / f"{prefix}{stem}.npy"
        if path.exists():
            return np.load(path)
    raise SystemExit(f"no saved connected prediction for {stem}")


def swap_budget(base: np.ndarray, orderer: np.ndarray, dates: np.ndarray, flags: np.ndarray,
                codes: np.ndarray, n_codes: int, m_frac: float) -> tuple[np.ndarray, dict]:
    """Exact cardinality-constrained Top-decile selection, then lift-and-order."""
    if not (np.diff(dates) >= 0).all():
        raise AssertionError("frame must be sorted by trade_date")
    _, starts = np.unique(dates, return_index=True)
    ends = np.append(starts[1:], len(dates))
    span = float(orderer.max() - orderer.min())
    offset = span + 1.0
    out = orderer.copy()
    in_prev = np.zeros(n_codes, dtype=bool)
    in_cur = np.zeros(n_codes, dtype=bool)
    stats = {"days": 0, "m_frac": m_frac, "retained": [], "n_top": [], "swaps": 0,
             "eligibility_limited_days": 0}
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
            retained = n_top if not have_prev else int(in_prev[codes[unconstrained]].sum())
        else:
            # names held yesterday that are still eligible today are the only retainable pool
            pool = eligible[in_prev[codes[eligible]]]
            if len(pool) < m:
                stats["eligibility_limited_days"] += 1
                m = len(pool)
            held_in_u = in_prev[codes[unconstrained]]
            r = int(held_in_u.sum())
            if r >= m:
                chosen = unconstrained
                retained = r
            else:
                need = m - r
                drop_local = np.flatnonzero(~held_in_u)
                drop_local = drop_local[np.argsort(scores[order[:n_top]][drop_local], kind="stable")][:need]
                keep_local = np.setdiff1d(np.arange(n_top), drop_local, assume_unique=True)
                add_scores = base[pool]
                add_local = np.argsort(-add_scores, kind="stable")
                added = []
                chosen_codes = set(codes[unconstrained[keep_local]].tolist())
                for idx in add_local:
                    if len(added) >= need:
                        break
                    code = codes[pool[idx]]
                    if code in chosen_codes:
                        continue
                    added.append(int(pool[idx]))
                    chosen_codes.add(code)
                if len(added) != need:
                    raise AssertionError(f"swap-budget could not retain {need} names")
                chosen = np.concatenate([unconstrained[keep_local], np.array(added, dtype=np.int64)])
                retained = int(in_prev[codes[chosen]].sum())
                stats["swaps"] += need
        if len(chosen) != n_top or len(np.unique(codes[chosen])) != n_top:
            raise AssertionError("chosen set is not exactly n_top distinct names")
        out[chosen] = offset + orderer[chosen]
        stats["days"] += 1
        stats["retained"].append(retained)
        stats["n_top"].append(n_top)
        in_cur[:] = False
        in_cur[codes[chosen]] = True
        in_prev, in_cur = in_cur, in_prev
        have_prev = True
    if not np.isfinite(out).all():
        raise AssertionError("non-finite prediction")
    promoted = out >= offset
    if promoted.any() and (~promoted).any() and out[promoted].min() <= out[~promoted].max():
        raise AssertionError("lifted block is not strictly above the remainder")
    stats["mean_retention_ratio"] = float(np.mean(np.array(stats["retained"]) /
                                                  np.array(stats["n_top"])))
    stats.pop("retained")
    stats.pop("n_top")
    return out, stats


def freeze() -> None:
    available = {}
    for label, base, orderer, expected in CONFIGS:
        for stem in (base, orderer):
            try:
                arr = load(stem)
                available[stem] = {"rows": int(len(arr)), "sha256": sha(HERE / (
                    f"connected_pred_{stem}.npy" if (HERE / f"connected_pred_{stem}.npy").exists()
                    else f"{stem}.npy"))}
            except SystemExit as error:
                available[stem] = {"missing": str(error)}
    payload = {
        "frozen_at_local": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "standard": "后续选模标准.md §3 connected composite primary; §4 highest score wins, no "
                    "significance / worst-year / years-positive gates",
        "status": "in_sample_selection_disclosed",
        "mechanism": "exact cardinality-constrained Top-decile selection: maximize the base score of "
                     "the chosen set subject to retaining at least m of the names the evaluator "
                     "realized in the previous day's Top decile, then lift the set and order it "
                     "internally by the orderer",
        "m_fractions": list(M_FRACTIONS),
        "configs": [{"label": l, "base": b, "orderer": o, "expected_at_m0": e}
                    for l, b, o, e in CONFIGS],
        "harness_proof": "m=0 must reproduce the recorded connected score of the unconstrained "
                         "construction to 2e-9 for every config that has one; for base==orderer that "
                         "transform is the identity, so it must reproduce the arm's own score",
        "selection_rule": "highest connected 2020-2024 official composite over all configs and m "
                          "values; ties broken by smaller m (less intervention) then simpler base",
        "disclosed_selection_cost": f"{len(CONFIGS) * len(M_FRACTIONS)} settings maximized over five "
                                    "repeatedly viewed years with no blind period remaining; the "
                                    "winner's score carries an upward selection bias this protocol "
                                    "cannot quantify",
        "causality": "the retention constraint uses only the previous day's realized Top decile, which "
                     "is a function of past predictions and past limit-up flags. No label or label "
                     "availability is read at any point.",
        "inputs": available,
        "no_test_period_data_read": True,
        "source_sha256": sha(Path(__file__)),
    }
    if (HERE / "protocol_wave7.json").exists():
        raise FileExistsError("protocol already frozen")
    (HERE / "protocol_wave7.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    cs.log(f"wave-7 protocol frozen: {len(CONFIGS)} configs x {len(M_FRACTIONS)} m values")


def run() -> None:
    protocol = json.loads((HERE / "protocol_wave7.json").read_text(encoding="utf-8"))
    assert protocol["source_sha256"] == sha(Path(__file__)), "script changed after freezing"
    frame = cs.combined_frame()
    dates = frame["trade_date"].to_numpy()
    flags = frame["flag_limit_up"].to_numpy()
    codes, uniques = __import__("pandas").factorize(frame["ts_code"].to_pandas(), sort=True)
    codes = codes.astype(np.int64)
    n_codes = len(uniques)
    cs.log(f"identity space: {n_codes} codes, {len(dates):,} rows, "
           f"{int(frame['trade_date'].n_unique())} days")

    results, proofs = {}, {}
    for label, base_stem, orderer_stem, expected in CONFIGS:
        base = load(base_stem)
        orderer = load(orderer_stem)
        for m_frac in M_FRACTIONS:
            name = f"{label}__m{m_frac:g}"
            pred, stats = swap_budget(base, orderer, dates, flags, codes, n_codes, m_frac)
            started = time.monotonic()
            metrics, _ = score_official(frame, pred)
            if m_frac == 0.0 and expected is not None:
                diff = abs(metrics["final_score"] - expected)
                proofs[name] = {"expected": expected, "got": metrics["final_score"],
                                "abs_diff": diff, "passed": bool(diff <= TOL_M0)}
                if diff > TOL_M0:
                    raise AssertionError(f"{name}: m=0 gives {metrics['final_score']!r}, "
                                         f"expected {expected!r} (diff {diff:.3e})")
                cs.log(f"{name}: HARNESS PROOF passed, m=0 reproduces {expected:.9f} exactly")
            np.save(HERE / f"wave7_{name}.npy", pred)
            results[name] = {"label": label, "base": base_stem, "orderer": orderer_stem,
                             "m_frac": m_frac, "connected_final_score": metrics["final_score"],
                             "connected_metrics": metrics, "stats": stats,
                             "seconds": round(time.monotonic() - started, 1)}
            cs.log(f"{name}: CONNECTED {metrics['final_score']:.9f} (ic {metrics['ic_mean']:.6f}, "
                   f"excess {metrics['annual_excess']:.6f}, turnover {metrics['mean_turnover']:.6f}) "
                   f"mean retention {stats['mean_retention_ratio']:.4f}")
            del pred
        cs.log(f"{label}: m scan complete")

    ranked = sorted(results.items(), key=lambda kv: -kv[1]["connected_final_score"])
    payload = {"status": "complete", "completed_at_local": time.strftime("%Y-%m-%dT%H:%M:%S"),
               "protocol_sha256": sha(HERE / "protocol_wave7.json"),
               "harness_proofs": proofs, "results": results,
               "best": ranked[0][0],
               "best_connected_final_score": ranked[0][1]["connected_final_score"],
               "previous_leader": 0.431343420,
               "gain_over_previous_leader": ranked[0][1]["connected_final_score"] - 0.431343420,
               "no_test_period_data_read": True}
    (HERE / "wave7_results.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("\n| rank | config | m | CONNECTED | IC | excess | turnover | retention |")
    print("|---|---|---|---|---|---|---|---|")
    for i, (name, v) in enumerate(ranked[:24]):
        m = v["connected_metrics"]
        print(f"| {i+1} | {v['label']} | {v['m_frac']:g} | **{m['final_score']:.9f}** | "
              f"{m['ic_mean']:.6f} | {m['annual_excess']:.6f} | {m['mean_turnover']:.6f} | "
              f"{v['stats']['mean_retention_ratio']:.4f} |")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("stage", choices=("freeze", "run"))
    args = parser.parse_args()
    try:
        globals()[args.stage]()
    except Exception as error:
        (HERE / f"failure_wave7_{args.stage}_{time.time_ns()}.json").write_text(
            json.dumps({"stage": args.stage, "type": type(error).__name__, "message": str(error),
                        "traceback": traceback.format_exc()}, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8")
        raise
