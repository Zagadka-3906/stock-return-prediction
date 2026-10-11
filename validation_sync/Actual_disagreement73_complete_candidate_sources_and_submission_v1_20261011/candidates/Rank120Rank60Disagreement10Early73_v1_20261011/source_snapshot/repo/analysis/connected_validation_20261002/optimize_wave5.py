"""Wave 5: mechanism-driven variants of the leading Top-set-substitution scheme.

The leader (k=1, membership from topk, ordering from W5a) scores 0.431343420 on the connected
2020-2024 caliber. Decomposed against the confirmed model it wins on excess (+0.0109 of composite)
and loses on IC (-0.0050) and turnover (-0.0019). So the two levers worth pulling are exactly those
two losing terms, and each has a causal, label-free mechanism:

MEMBERSHIP side (moves excess and turnover)
  M1  the leader's rule: promote the membership donor's own Top decile
  M2  CONSENSUS: promote only names in the donor's Top decile on BOTH day t and day t-1. Requiring
      agreement across consecutive days is a direct Jaccard-distance reducer; when the intersection is
      smaller than n_top the evaluator fills the remaining slots by the orderer's rank, which is the
      natural behaviour of the block construction and needs no extra rule.
  M3  PERSISTENCE BONUS on membership: rank by the donor's within-day percentile plus 0.3 for names in
      the hybrid's own previous-day Top decile, then promote the top n_top. This is the released
      retention-bonus mechanism moved from the ordering stage to the membership stage, where turnover
      is actually decided. Bonus fixed at 0.3, the released value - not swept.

ORDERING side (moves IC)
  O1  W5a_five_way_with_gru - the connected ic_mean argmax (0.119450)
  O2  equal-weight per-day rank average of the three highest connected ic_mean arms
      (W5a 0.119450, extended83 0.118207, W5b 0.118162); averaging should raise IC above any single
      member the same way seed averaging does, and the donor rule does not forbid a composite donor
  O3  peer67_slow16 - the incumbent, kept because its provenance is the cleanest (16 saved .ubj models)

Everything is cache-only: all donors already have connected prediction columns on disk, so no model is
retrained. Selection is by the highest connected composite per 后续选模标准.md §4; the in-sample cost of
taking a maximum over several variants on five viewed years is disclosed in the protocol, not hidden.
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

MEMBERSHIP_DONOR = "topk"
ORDERING_DONORS = {
    "O1": ["W5a_five_way_with_gru__final_sweep_eval"],
    "O2": ["W5a_five_way_with_gru__final_sweep_eval",
           "raw_extended83__wave15_paired_features_20260927",
           "W5b_gru_half_weight__final_sweep_eval"],
    "O3": ["peer67_slow16"],
}
CANDIDATES = [("M1", "O1"), ("M1", "O2"), ("M1", "O3"),
              ("M2", "O1"), ("M2", "O2"), ("M3", "O1"), ("M3", "O2")]
BONUS = 0.3
REFERENCE_LEADER = 0.431343420
REFERENCE_H1 = 0.4288913586946


def sha(path) -> str:
    value = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for chunk in iter(lambda: stream.read(8 * 1024 * 1024), b""):
            value.update(chunk)
    return value.hexdigest()


def day_blocks(dates: np.ndarray) -> list[tuple[int, int]]:
    if not (np.diff(dates) >= 0).all():
        raise AssertionError("frame must be sorted by trade_date")
    _, starts = np.unique(dates, return_index=True)
    ends = np.append(starts[1:], len(dates))
    return list(zip(starts.tolist(), ends.tolist()))


def daily_percentile(values: np.ndarray, dates: np.ndarray) -> np.ndarray:
    """Within-day average rank / rows in day. Ties stay tied; used for rank averaging and bonuses."""
    out = np.empty(len(values), dtype=np.float64)
    for start, end in day_blocks(dates):
        block = values[start:end]
        out[start:end] = pd.Series(block).rank(method="average").to_numpy() / len(block)
    return out


def eligible_top(pred: np.ndarray, dates: np.ndarray, flags: np.ndarray,
                 blocks: list[tuple[int, int]]) -> list[np.ndarray]:
    """The evaluator's own Top decile per day: flag_limit_up == 0, n_top = len // 10, no label filter."""
    tops = []
    for start, end in blocks:
        rows = np.arange(start, end)
        eligible = rows[flags[start:end] == 0]
        if len(eligible) < 100:
            tops.append(None)
            continue
        n_top = max(len(eligible) // 10, 1)
        order = np.argsort(-pred[eligible], kind="stable")
        tops.append(eligible[order[:n_top]])
    return tops


def build_variant(rule: str, orderer: str, b_pred: np.ndarray, a_pred: np.ndarray,
                  dates: np.ndarray, flags: np.ndarray, codes: np.ndarray,
                  n_codes: int) -> tuple[np.ndarray, dict]:
    """Cross-day set operations run in STOCK-IDENTITY space, never on row indices: day t and day t-1
    occupy disjoint row ranges, so intersecting row indices is always empty. That defect made the
    first M2 run promote nothing and turned M3's retention bonus into a no-op; those results are
    archived as superseded and both rules are re-scored here."""
    blocks = day_blocks(dates)
    span = float(a_pred.max() - a_pred.min())
    offset = span + 1.0
    out = a_pred.copy()
    b_pct = daily_percentile(b_pred, dates)
    donor_tops = eligible_top(b_pred, dates, flags, blocks)
    donor_codes = [None if t is None else codes[t] for t in donor_tops]
    stats = {"rule": rule, "orderer": orderer, "days": 0, "promoted_rows": 0, "eligible_rows": 0,
             "boundary_tie_days": 0, "mean_promoted_over_n_top": [], "identity_space": "ts_code"}
    previous_hybrid_top = None
    code_flag = np.zeros(n_codes, dtype=bool)
    for index, (start, end) in enumerate(blocks):
        rows = np.arange(start, end)
        eligible = rows[flags[start:end] == 0]
        if len(eligible) < 100:
            previous_hybrid_top = None
            continue
        n_top = max(len(eligible) // 10, 1)
        donor = donor_tops[index]
        if rule == "M1":
            block = donor
        elif rule == "M2":
            prior = donor_codes[index - 1] if index > 0 else None
            if prior is None:
                block = donor
            else:
                code_flag[:] = False
                code_flag[prior] = True
                block = donor[code_flag[codes[donor]]]
        elif rule == "M3":
            score = b_pct[eligible].copy()
            if previous_hybrid_top is not None:
                code_flag[:] = False
                code_flag[previous_hybrid_top] = True
                score = score + BONUS * code_flag[codes[eligible]]
            order = np.argsort(-score, kind="stable")
            if n_top < len(score) and score[order[n_top - 1]] == score[order[n_top]]:
                stats["boundary_tie_days"] += 1
            block = eligible[order[:n_top]]
        else:
            raise ValueError(rule)
        out[block] = offset + a_pred[block]
        stats["days"] += 1
        stats["promoted_rows"] += int(len(block))
        stats["eligible_rows"] += int(len(eligible))
        stats["mean_promoted_over_n_top"].append(len(block) / n_top)
        # the Top decile the evaluator will actually realize for this day: everything promoted sits
        # above everything else, ordered by the orderer, and any shortfall is filled by the orderer
        if len(block) >= n_top:
            realized = block[np.argsort(-a_pred[block], kind="stable")[:n_top]]
        else:
            promoted = {int(r) for r in block}
            ordered = eligible[np.argsort(-a_pred[eligible], kind="stable")]
            fill = [int(r) for r in ordered if int(r) not in promoted][:n_top - len(block)]
            realized = np.array([int(r) for r in block] + fill, dtype=np.int64)
        previous_hybrid_top = codes[realized]
    stats["mean_promoted_over_n_top"] = float(np.mean(stats["mean_promoted_over_n_top"]))
    stats["promoted_share"] = stats["promoted_rows"] / max(stats["eligible_rows"], 1)
    if not np.isfinite(out).all():
        raise AssertionError("non-finite variant prediction")
    if out[out >= offset].min() <= out[out < offset].max():
        raise AssertionError("promoted block is not strictly above the remainder")
    return out, stats


def freeze() -> None:
    results = json.loads((HERE / "connected_results_all.json").read_text(encoding="utf-8"))["results"]
    wave4 = json.loads((HERE / "wave4_results.json").read_text(encoding="utf-8"))
    by_ic = sorted(results.items(), key=lambda kv: -kv[1]["connected_metrics"]["ic_mean"])
    donors = {}
    for label, names in ORDERING_DONORS.items():
        for name in names:
            path = HERE / f"connected_pred_{name}.npy"
            if not path.exists():
                raise SystemExit(f"missing ordering donor prediction: {name}")
            donors[name] = {"connected_ic": results[name]["connected_metrics"]["ic_mean"],
                            "connected_final_score": results[name]["connected_final_score"],
                            "sha256": sha(path)}
    payload = {
        "frozen_at_local": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "standard": "后续选模标准.md §3 connected composite is primary; §4 highest score wins, no "
                    "significance / worst-year / years-positive gates",
        "status": "in_sample_selection_disclosed",
        "top_ic_arms_independent_check": [{"name": n, "ic": r["connected_metrics"]["ic_mean"]}
                                          for n, r in by_ic[:5]],
        "membership_donor": {"name": MEMBERSHIP_DONOR,
                             "connected_excess": results[MEMBERSHIP_DONOR]["connected_metrics"]["annual_excess"],
                             "connected_turnover": results[MEMBERSHIP_DONOR]["connected_metrics"]["mean_turnover"]},
        "ordering_donors": donors,
        "rules": {"M1": "promote the donor's own Top decile",
                  "M2": "promote only names in the donor's Top decile on day t AND day t-1; the "
                        "evaluator fills any shortfall by the orderer's rank",
                  "M3": f"rank by donor within-day percentile + {BONUS} for names in the hybrid's own "
                        f"previous-day Top decile, promote the top n_top (released bonus value, not swept)"},
        "candidates": [f"{m}x{o}" for m, o in CANDIDATES],
        "already_scored_references": {"M1xO1_leader": REFERENCE_LEADER, "M1xO3_H1": REFERENCE_H1},
        "selection_rule": "highest connected 2020-2024 official composite; ties broken by lower "
                          "complexity and cleaner provenance",
        "disclosed_selection_cost": "six new variants are scored on five repeatedly viewed years and "
                                    "the maximum is reported. No blind period remains, so the winner's "
                                    "score carries an upward selection bias this protocol cannot "
                                    "quantify; nothing here is a significance claim.",
        "causality": "membership uses only flag_limit_up, the donor prediction and the previous day's "
                     "own Top set - all available at prediction time. No label or label availability "
                     "is read. Day t-1 information is strictly past relative to day t.",
        "no_test_period_data_read": True,
        "source_sha256": sha(Path(__file__)),
    }
    if (HERE / "protocol_wave5.json").exists():
        raise FileExistsError("protocol already frozen")
    (HERE / "protocol_wave5.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    cs.log(f"wave-5 protocol frozen: {len(CANDIDATES)} candidates, membership {MEMBERSHIP_DONOR}, "
           f"ordering {list(ORDERING_DONORS)}")


def run() -> None:
    protocol = json.loads((HERE / "protocol_wave5.json").read_text(encoding="utf-8"))
    assert protocol["source_sha256"] == sha(Path(__file__)), "script changed after freezing"
    frame = cs.combined_frame()
    pdf = frame.select(["trade_date", "flag_limit_up"]).to_pandas()
    dates = pdf["trade_date"].to_numpy()
    flags = pdf["flag_limit_up"].to_numpy()
    codes, uniques = pd.factorize(frame["ts_code"].to_pandas(), sort=True)
    codes = codes.astype(np.int64)
    n_codes = len(uniques)
    cs.log(f"identity space: {n_codes} distinct ts_code labels for cross-day set operations")
    b = np.load(HERE / f"connected_pred_{MEMBERSHIP_DONOR}.npy")

    ordering = {}
    for label, names in ORDERING_DONORS.items():
        if len(names) == 1:
            ordering[label] = np.load(HERE / f"connected_pred_{names[0]}.npy")
        else:
            pcts = [daily_percentile(np.load(HERE / f"connected_pred_{n}.npy"), dates) for n in names]
            ordering[label] = np.mean(pcts, axis=0)
            cs.log(f"{label}: rank-averaged {len(names)} ordering donors")

    out = {}
    for rule, o_label in CANDIDATES:
        name = f"{rule}x{o_label}"
        pred, stats = build_variant(rule, o_label, b, ordering[o_label], dates, flags,
                                    codes, n_codes)
        # guard against the row-index-vs-identity defect recurring: M3 promotes exactly n_top rows
        # and M2 promotes the day-to-day consensus, which for a donor with Jaccard turnover ~0.044
        # must be most of the Top decile, never a rounding error
        if rule == "M3" and abs(stats["mean_promoted_over_n_top"] - 1.0) > 1e-9:
            raise AssertionError(f"M3 promoted {stats['mean_promoted_over_n_top']} x n_top")
        if rule == "M2" and stats["mean_promoted_over_n_top"] < 0.5:
            raise AssertionError(f"M2 consensus collapsed to "
                                   f"{stats['mean_promoted_over_n_top']} x n_top - identity bug?")
        started = time.monotonic()
        metrics, _ = score_official(frame, pred)
        np.save(HERE / f"connected_pred_wave5_{name}.npy", pred)
        out[name] = {"rule": rule, "orderer": o_label,
                     "ordering_donors": ORDERING_DONORS[o_label],
                     "connected_final_score": metrics["final_score"],
                     "connected_metrics": metrics, "stats": stats,
                     "vs_leader": metrics["final_score"] - REFERENCE_LEADER,
                     "seconds": round(time.monotonic() - started, 1)}
        cs.log(f"{name}: CONNECTED {metrics['final_score']:.9f} (ic {metrics['ic_mean']:.6f}, "
               f"excess {metrics['annual_excess']:.6f}, turnover {metrics['mean_turnover']:.6f}) "
               f"promoted {stats['promoted_share']*100:.2f}% "
               f"(mean block/n_top {stats['mean_promoted_over_n_top']:.3f}) "
               f"vs leader {metrics['final_score']-REFERENCE_LEADER:+.6f}")

    ranked = sorted(out.items(), key=lambda kv: -kv[1]["connected_final_score"])
    payload = {"status": "complete", "completed_at_local": time.strftime("%Y-%m-%dT%H:%M:%S"),
               "protocol_sha256": sha(HERE / "protocol_wave5.json"),
               "reference_leader_M1xO1": REFERENCE_LEADER,
               "variants": out, "best": ranked[0][0],
               "best_connected_final_score": ranked[0][1]["connected_final_score"],
               "beats_leader": bool(ranked[0][1]["connected_final_score"] > REFERENCE_LEADER),
               "no_test_period_data_read": True}
    (HERE / "wave5_results.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("\n| variant | rule | orderer | CONNECTED | IC | excess | turnover | vs leader |")
    print("|---|---|---|---|---|---|---|---|")
    for name, v in ranked:
        m = v["connected_metrics"]
        print(f"| {name} | {v['rule']} | {v['orderer']} | **{m['final_score']:.9f}** | "
              f"{m['ic_mean']:.6f} | {m['annual_excess']:.6f} | {m['mean_turnover']:.6f} | "
              f"{v['vs_leader']:+.6f} |")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("stage", choices=("freeze", "run"))
    args = parser.parse_args()
    try:
        globals()[args.stage]()
    except Exception as error:
        (HERE / f"failure_wave5_{args.stage}_{time.time_ns()}.json").write_text(
            json.dumps({"stage": args.stage, "type": type(error).__name__, "message": str(error),
                        "traceback": traceback.format_exc()}, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8")
        raise
