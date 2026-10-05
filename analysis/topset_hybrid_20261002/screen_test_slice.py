"""FEASIBILITY SCREEN (descriptive, evaluation-set evidence) for cross-model Top-set substitution.

Mechanism: the official composite is 0.4*RankIC + 0.3*annualized_top_decile_excess + 0.3*(1-Jaccard).
Rank IC depends on the FULL cross-section ordering, while excess and turnover depend ONLY on which
stocks land in the Top decile. Those are separable, so one model can supply Top-decile membership
and a different model can supply the ordering.

Candidate (one fixed definition, no grid): membership of each day's Top decile comes from arm B
(the Top-K return-weighted pairwise backbone, which has the measured excess advantage), ordering
everywhere comes from arm A (peer67_slow16, the confirmed model, which has ~2x the Rank IC).
H = is_promoted * OFFSET + pred_A, with OFFSET above the full pred_A range so that every promoted
row outranks every non-promoted row and A's ordering (and its ties) is preserved inside each block.

CAUSALITY: membership uses only flag_limit_up and pred_B - never y_ret_1d or its availability. The
label-missing filter the evaluator applies to the excess term is not available at prediction time,
so the promoted block is defined on the TURNOVER universe (flag_limit_up == 0, n_top = len // 10).

This screen runs on the reconstructed test slice because both arms' predictions are already cached
there and no training is needed. IT IS EVALUATION-SET EVIDENCE AND MAY NOT SELECT ANYTHING; the
admissible axis is the 2020-2024 fold validation, run only if this screen says the mechanism works.
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
from experiments.revalidate_fold_local import score_official  # noqa: E402
from analysis.official_score_contributions import (  # noqa: E402
    WEIGHTS, composite, paired_difference,
)

ARCHIVE = ROOT.parent / "赛题五_历史归档_20261001"
DATA = ARCHIVE / "analysis" / "frozen_holdout_20260928" / "data"
ARM_A = ARCHIVE / "deliveries/peer67_slow16_20260929/submission.csv"
ARM_B = ARCHIVE / "analysis/all_models_test_20260929/middle/predictions/supplemental_topk_fulltrain2024.parquet"
CUTOFF = 20260605
KEYS = ["ts_code", "trade_date"]
# Published full-period composites; the anchor must reproduce both before anything is combined.
EXPECTED = {"A_peer67_slow16": 0.386058, "B_topk": 0.39827952757098173}


def sha(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(8 * 1024 * 1024), b""):
            value.update(chunk)
    return value.hexdigest()


def block_bootstrap(diff: np.ndarray, seed: int = 20261002, draws: int = 20000, block: int = 20):
    rng = np.random.default_rng(seed)
    n = len(diff)
    n_blocks = int(np.ceil(n / block))
    starts = rng.integers(0, n - block + 1, size=(draws, n_blocks))
    out = np.empty(draws)
    for i in range(draws):
        out[i] = np.concatenate([diff[s:s + block] for s in starts[i]])[:n].mean()
    return out


def build_frame() -> tuple[pl.DataFrame, pd.DataFrame]:
    x = pd.read_csv(DATA / "测试集_X.csv")
    y = pd.read_csv(DATA / "测试集_Y.csv")
    merged = x.merge(y, on=KEYS, how="left")
    merged = merged[merged.trade_date <= CUTOFF].reset_index(drop=True)
    base = pl.from_pandas(merged)

    a = pd.read_csv(ARM_A)
    a = a[a.trade_date <= CUTOFF].reset_index(drop=True)
    # already in 测试集_X row order (code-major); sorting would break the alignment assertion
    b = pl.read_parquet(ARM_B).to_pandas()
    b = b[b.trade_date <= CUTOFF].reset_index(drop=True)
    for name, sub in (("A", a), ("B", b)):
        assert len(sub) == len(merged), f"arm {name}: {len(sub)} rows vs {len(merged)}"
        assert (sub[KEYS].to_numpy() == merged[KEYS].to_numpy()).all(), f"arm {name}: key order"
    panel = merged.copy()
    panel["pred_A"] = a["pred"].to_numpy()
    panel["pred_B"] = b["pred"].to_numpy() if "pred" in b else b["pred_final"].to_numpy()
    return base, panel


def top_sets(panel: pd.DataFrame, pred_col: str) -> tuple[np.ndarray, dict]:
    """Evaluator-faithful Top decile over the TURNOVER universe (flag_limit_up == 0), no labels used."""
    promoted = np.zeros(len(panel), dtype=bool)
    stats = {"days": 0, "days_skipped_lt100": 0, "boundary_tie_days": 0, "top_sizes": []}
    for _, group in panel.groupby("trade_date", sort=True):
        eligible = group.index[group.flag_limit_up.to_numpy() == 0]
        if len(eligible) < 100:
            stats["days_skipped_lt100"] += 1
            continue
        values = panel.loc[eligible, pred_col].to_numpy()
        n_top = max(len(eligible) // 10, 1)
        order = np.argsort(-values, kind="stable")
        stats["boundary_tie_days"] += int(n_top < len(values) and
                                         values[order[n_top - 1]] == values[order[n_top]])
        promoted[eligible.to_numpy()[order[:n_top]]] = True
        stats["days"] += 1
        stats["top_sizes"].append(n_top)
    stats["top_sizes"] = [int(np.min(stats["top_sizes"])), int(np.max(stats["top_sizes"]))]
    return promoted, stats


def main() -> None:
    started = time.monotonic()
    base, panel = build_frame()
    print(f"panel {len(panel):,} rows, {panel.trade_date.nunique()} days, "
          f"{panel.ts_code.nunique()} codes")

    # ---- anchor: both arms must reproduce their published composites through evaluate.py
    metrics = {}
    dailies = {}
    for name, col in (("A_peer67_slow16", "pred_A"), ("B_topk", "pred_B")):
        m, d = score_official(base, panel[col].to_numpy(np.float64))
        metrics[name] = m
        dailies[name] = d.to_pandas()
        exp = EXPECTED[name]
        diff = abs(m["final_score"] - exp)
        tol = 1e-9 if name == "B_topk" else 1e-6
        assert diff <= tol, f"anchor {name}: {m['final_score']:.9f} vs published {exp:.9f}"
        print(f"anchor {name}: {m['final_score']:.6f} (ic {m['ic_mean']:.6f}, "
              f"excess {m['annual_excess']:.6f}, turnover {m['mean_turnover']:.6f}) OK")

    # ---- the mechanism's precondition: how much do the two arms' Top deciles actually differ?
    promoted_B, stats_B = top_sets(panel, "pred_B")
    promoted_A, stats_A = top_sets(panel, "pred_A")
    assert stats_B["boundary_tie_days"] == 0, f"B has boundary ties: {stats_B}"
    assert stats_A["boundary_tie_days"] == 0, f"A has boundary ties: {stats_A}"
    both = promoted_A & promoted_B
    union = promoted_A | promoted_B
    jaccard_AB = both.sum() / union.sum()
    print(f"Top-decile overlap A vs B: Jaccard {jaccard_AB:.4f} "
          f"({both.sum():,} of {promoted_A.sum():,} A members also in B)")
    print(f"turnover-universe days scored: {stats_B['days']}, skipped <100: "
          f"{stats_B['days_skipped_lt100']}, top size range {stats_B['top_sizes']}")

    # ---- build the hybrid: B supplies membership, A supplies ordering
    span = float(panel.pred_A.max() - panel.pred_A.min())
    offset = span + 1.0
    hybrid = promoted_B.astype(np.float64) * offset + panel.pred_A.to_numpy(np.float64)
    assert np.isfinite(hybrid).all()
    # promoted block must be strictly above the rest, and A's order preserved inside each block
    assert hybrid[promoted_B].min() > hybrid[~promoted_B].max(), "blocks overlap"
    for mask in (promoted_B, ~promoted_B):
        assert np.array_equal(np.argsort(np.argsort(hybrid[mask])),
                              np.argsort(np.argsort(panel.pred_A.to_numpy()[mask])))

    # ---- the hybrid's own Top set must be exactly B's, on the evaluator's universe
    promoted_H, stats_H = top_sets(panel.assign(pred_H=hybrid), "pred_H")
    assert stats_H["boundary_tie_days"] == 0, "hybrid has a Top-boundary tie"
    assert (promoted_H == promoted_B).all(), \
        f"hybrid Top set != B Top set on {(promoted_H != promoted_B).sum()} rows"
    print("assertion passed: the hybrid's Top decile is exactly arm B's on every scored day")

    m_h, d_h = score_official(base, hybrid)
    dailies["H_hybrid"] = d_h.to_pandas()
    metrics["H_hybrid"] = m_h
    print(f"\nhybrid: {m_h['final_score']:.6f} (ic {m_h['ic_mean']:.6f}, "
          f"excess {m_h['annual_excess']:.6f}, turnover {m_h['mean_turnover']:.6f})")

    # ---- how much of B's excess did the hybrid actually capture, and what did IC cost?
    capture = {}
    for term, weight in (("ic_mean", 0.4), ("annual_excess", 0.3), ("mean_turnover", -0.3)):
        a_v, b_v, h_v = (metrics[k][term] for k in ("A_peer67_slow16", "B_topk", "H_hybrid"))
        share = (h_v - a_v) / (b_v - a_v) if abs(b_v - a_v) > 1e-15 else float("nan")
        capture[term] = {"A": a_v, "B": b_v, "H": h_v, "H_minus_A_contribution": weight * (h_v - a_v),
                         "B_minus_A_contribution": weight * (b_v - a_v),
                         "share_of_B_gap_captured": float(share)}
    print("\nterm capture (H vs A, and the share of the A->B gap that H reached):")
    for term, v in capture.items():
        print(f"  {term:14s} A {v['A']:.6f}  B {v['B']:.6f}  H {v['H']:.6f}  "
              f"H-A {v['H_minus_A_contribution']:+.6f}  B-A {v['B_minus_A_contribution']:+.6f}  "
              f"captured {v['share_of_B_gap_captured']*100:6.1f}%")

    # ---- paired uncertainty on the 343-day slice and its two segments
    mask_2025 = (dailies["H_hybrid"].trade_date < 20260101).to_numpy()
    contrasts = {}
    for left, right in (("H_hybrid", "A_peer67_slow16"), ("H_hybrid", "B_topk")):
        for label, mask in (("full343", None), ("2025", mask_2025), ("2026", ~mask_2025)):
            l, r = dailies[left], dailies[right]
            if mask is not None:
                l, r = l[mask], r[mask]
            diff = paired_difference(l, r)
            draws = block_bootstrap(diff)
            ci = [float(np.percentile(draws, 2.5)), float(np.percentile(draws, 97.5))]
            contrasts[f"{left}_minus_{right}__{label}"] = {
                "days": int(len(diff)), "diff": float(diff.mean()), "ci95": ci,
                "positive_share": float((draws > 0).mean()),
                "verdict": "resolvable_ahead" if ci[0] > 0 else (
                    "resolvable_behind" if ci[1] < 0 else "tie")}
    print("\n| contrast | days | diff | CI95 | verdict | P(>0) |")
    print("|---|---|---|---|---|---|")
    for key, v in contrasts.items():
        print(f"| {key} | {v['days']} | {v['diff']:+.6f} | "
              f"[{v['ci95'][0]:+.6f}, {v['ci95'][1]:+.6f}] | {v['verdict']} | "
              f"{v['positive_share']*100:.1f}% |")

    segments = {}
    for name, d in dailies.items():
        segments[name] = {"full343": composite(d),
                          "2025": composite(d[d.trade_date < 20260101]),
                          "2026": composite(d[d.trade_date >= 20260101])}
    payload = {
        "status": "complete", "completed_at_local": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "kind": "feasibility_screen_descriptive_only",
        "axis": "reconstructed test slice 2025-01-02..2026-06-05, 343 days",
        "may_not_select_anything": True,
        "inputs": {"arm_A": str(ARM_A), "arm_A_sha256": sha(ARM_A),
                   "arm_B": str(ARM_B), "arm_B_sha256": sha(ARM_B),
                   "labels": str(DATA / '测试集_Y.csv')},
        "candidate_definition": "Top-decile membership from arm B on the turnover universe "
                                "(flag_limit_up==0, n_top=len//10), ordering from arm A; "
                                "H = is_promoted*(span(pred_A)+1) + pred_A",
        "causality": "membership uses only flag_limit_up and pred_B; y_ret_1d and its availability "
                     "are never read to build the prediction",
        "anchors_reproduced": {k: v["final_score"] for k, v in metrics.items()},
        "top_decile_overlap_jaccard_A_vs_B": float(jaccard_AB),
        "turnover_universe_stats": stats_B,
        "hybrid_top_set_equals_B": True,
        "boundary_tie_days": {"A": stats_A["boundary_tie_days"], "B": stats_B["boundary_tie_days"],
                              "H": stats_H["boundary_tie_days"]},
        "metrics": metrics, "segments": segments, "term_capture": capture,
        "contrasts": contrasts,
        "seconds": round(time.monotonic() - started, 1),
        "next_step_if_promising": "the admissible axis is 2020-2024 folds; that needs arm A's "
                                  "per-fold final predictions reconstructed from the 80 surviving "
                                  "per-seed caches in 赛题五_清理备份_20261001/experiments/"
                                  "wave23_validation_20260928/, with an exact reproduction of the "
                                  "frozen daily_full16 composites as the harness proof",
    }
    (HERE / "screen_test_slice.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"\nsegments: {json.dumps(segments, ensure_ascii=False)}")
    print(f"done in {payload['seconds']}s -> screen_test_slice.json")


if __name__ == "__main__":
    main()
