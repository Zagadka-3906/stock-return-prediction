"""Wave 4: optimize on top of the leading scheme, under the connected caliber, donors chosen in-training.

后续选模标准.md §4 removes the extra research gates: among compliant candidates the highest official
composite under the pre-declared validation caliber wins, and a single metric declining does not veto
it. §5 then requires the winner to be freezable and deliverable. So this wave applies one explicit,
in-training donor-selection rule to the mechanism that already leads, plus a single pre-declared
one-dimensional sweep over the mechanism's only free parameter.

DONOR RULE (uses only connected-caliber training metrics already on disk, no test data):
  membership donor = argmax of connected annual_excess  -> topk            (0.349688)
  ordering donor   = argmax of connected ic_mean        -> W5a_five_way_with_gru (0.119450)
Rationale: the official composite splits into a full-cross-section ordering term (Rank IC) and two
terms that depend only on Top-decile membership (excess, turnover), so each donor is chosen by the
metric it actually supplies.

FREE PARAMETER: the promotion multiple k. k=1 promotes exactly the evaluator's n_top rows, so the Top
set is the membership donor's; k>1 promotes ceil(k*n_top) rows and the evaluator then keeps the n_top
best-ordered among them, blending the donor's selection with the orderer's judgment. There is no
in-training way to fix k a priori, so a small pre-declared sweep is run and the selection cost of
making it is disclosed rather than hidden.

Reference already scored: H1 = k=1 with peer67_slow16 ordering, connected 0.428891359.
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

ARCHIVE = ROOT.parent / "赛题五_历史归档_20261001"
MEMBERSHIP_DONOR = "topk"
ORDERING_DONOR = "W5a_five_way_with_gru__final_sweep_eval"
INCUMBENT_ORDERING = "peer67_slow16"
K_VALUES = (1.0, 1.5, 2.0, 3.0)
REFERENCE_H1 = 0.4288913586946
# Deliverability: both donors must have a test-period prediction column on disk.
DELIVERABILITY = {
    "topk": "analysis/all_models_test_20260929/middle/predictions/supplemental_topk_fulltrain2024.parquet",
    "W5a_five_way_with_gru": "analysis/all_models_test_20260929/early/predictions/early_9ec487b9f99e6f94.npy",
    "peer67_slow16": "deliveries/peer67_slow16_20260929/submission.csv",
}


def sha(path) -> str:
    value = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for chunk in iter(lambda: stream.read(8 * 1024 * 1024), b""):
            value.update(chunk)
    return value.hexdigest()


def promote(b_pred: np.ndarray, a_pred: np.ndarray, dates: np.ndarray, flags: np.ndarray,
            k: float) -> tuple[np.ndarray, dict]:
    """Rank-preserving hybrid: B supplies Top-decile membership, A supplies all ordering."""
    out = a_pred.copy()
    unique, starts = np.unique(dates, return_index=True)
    ends = np.append(starts[1:], len(dates))
    if not (np.diff(dates) >= 0).all():
        raise AssertionError("frame must be sorted by trade_date")
    span = float(a_pred.max() - a_pred.min())
    offset = span + 1.0
    stats = {"days": 0, "boundary_tie_days": 0, "promoted_rows": 0, "eligible_rows": 0}
    for start, end in zip(starts, ends):
        rows = np.arange(start, end)
        eligible = rows[flags[start:end] == 0]
        if len(eligible) < 100:
            continue
        n_top = max(len(eligible) // 10, 1)
        n_promote = int(min(np.ceil(k * n_top), len(eligible)))
        values = b_pred[eligible]
        order = np.argsort(-values, kind="stable")
        if n_promote < len(values) and values[order[n_promote - 1]] == values[order[n_promote]]:
            stats["boundary_tie_days"] += 1
        block = eligible[order[:n_promote]]
        out[block] = offset + a_pred[block]
        stats["days"] += 1
        stats["promoted_rows"] += n_promote
        stats["eligible_rows"] += len(eligible)
    if not np.isfinite(out).all():
        raise AssertionError("non-finite hybrid prediction")
    if out[out >= offset].min() <= out[out < offset].max():
        raise AssertionError("promoted block is not strictly above the remainder")
    stats["promoted_share"] = stats["promoted_rows"] / max(stats["eligible_rows"], 1)
    return out, stats


def freeze() -> None:
    results = json.loads((HERE / "connected_results_all.json").read_text(encoding="utf-8"))["results"]
    by_excess = sorted(results.items(), key=lambda kv: -kv[1]["connected_metrics"]["annual_excess"])
    by_ic = sorted(results.items(), key=lambda kv: -kv[1]["connected_metrics"]["ic_mean"])
    for name, relative in DELIVERABILITY.items():
        path = ARCHIVE / relative
        if not path.exists():
            raise SystemExit(f"donor {name} is not deliverable, missing {relative}")
    payload = {
        "frozen_at_local": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "standard": "后续选模标准.md §3 connected 2020-2024 official composite is the primary score; "
                    "§4 no extra research gates, highest score among compliant candidates wins",
        "status": "descriptive_in_sample_selection_disclosed",
        "donor_rule": {
            "membership": "argmax of connected annual_excess",
            "membership_donor": by_excess[0][0],
            "membership_donor_excess": by_excess[0][1]["connected_metrics"]["annual_excess"],
            "runner_up_excess": {n: r["connected_metrics"]["annual_excess"] for n, r in by_excess[1:4]},
            "ordering": "argmax of connected ic_mean",
            "ordering_donor": by_ic[0][0],
            "ordering_donor_ic": by_ic[0][1]["connected_metrics"]["ic_mean"],
            "runner_up_ic": {n: r["connected_metrics"]["ic_mean"] for n, r in by_ic[1:4]},
            "uses_only_training_interval_metrics": True,
        },
        "candidates": [{"k": k, "membership": MEMBERSHIP_DONOR, "ordering": ORDERING_DONOR}
                       for k in K_VALUES],
        "reference_already_scored": {"name": "hybrid (k=1, ordering=peer67_slow16)",
                                     "connected_final_score": REFERENCE_H1},
        "selection_rule": "highest connected 2020-2024 official composite; ties broken by lower "
                          "complexity and run cost",
        "disclosed_selection_cost": "four candidates are scored on five repeatedly viewed years and "
                                    "the maximum is reported. There is no blind period left, so the "
                                    "winner's score is upward-biased by the selection itself and this "
                                    "wave cannot produce a significance claim, only a ranking.",
        "deliverability_gate": {
            "rule": "a candidate may only win if every donor has a test-period prediction on disk, "
                    "so the scheme can be frozen and used to produce submission.csv",
            "verified": {k: {"path": v, "sha256": sha(ARCHIVE / v)} for k, v in DELIVERABILITY.items()},
        },
        "causality": "membership uses only flag_limit_up and the donor's prediction; no label or label "
                     "availability is read; both donors are walk-forward fold predictions trained "
                     "strictly before each validation year",
        "no_test_period_data_read": True,
        "source_sha256": sha(Path(__file__)),
    }
    if (HERE / "protocol_wave4.json").exists():
        raise FileExistsError("protocol already frozen")
    (HERE / "protocol_wave4.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    cs.log(f"wave-4 protocol frozen; membership donor {payload['donor_rule']['membership_donor']} "
           f"(excess {payload['donor_rule']['membership_donor_excess']:.6f}), ordering donor "
           f"{payload['donor_rule']['ordering_donor']} (ic {payload['donor_rule']['ordering_donor_ic']:.6f})")


def run() -> None:
    protocol = json.loads((HERE / "protocol_wave4.json").read_text(encoding="utf-8"))
    assert protocol["source_sha256"] == sha(Path(__file__)), "script changed after freezing"
    frame = cs.combined_frame()
    pdf = frame.select(["trade_date", "flag_limit_up"]).to_pandas()
    dates = pdf["trade_date"].to_numpy()
    flags = pdf["flag_limit_up"].to_numpy()
    b = np.load(HERE / f"connected_pred_{MEMBERSHIP_DONOR}.npy")
    a = np.load(HERE / f"connected_pred_{ORDERING_DONOR}.npy")
    a_inc = np.load(HERE / f"connected_pred_{INCUMBENT_ORDERING}.npy")
    for name, arr in (("membership", b), ("ordering", a), ("incumbent", a_inc)):
        if len(arr) != len(frame):
            raise AssertionError(f"{name} donor array is {len(arr)} of {len(frame)} rows")

    out = {}
    for k in K_VALUES:
        pred, stats = promote(b, a, dates, flags, k)
        if stats["boundary_tie_days"]:
            raise AssertionError(f"k={k}: {stats['boundary_tie_days']} days have a promotion-boundary tie")
        started = time.monotonic()
        metrics, _ = score_official(frame, pred)
        name = f"hybrid_k{k:g}_topk_x_{ORDERING_DONOR.split('__')[0]}"
        np.save(HERE / f"connected_pred_{name}.npy", pred)
        out[f"k={k:g}"] = {"name": name, "k": k, "membership_donor": MEMBERSHIP_DONOR,
                           "ordering_donor": ORDERING_DONOR,
                           "connected_final_score": metrics["final_score"],
                           "connected_metrics": metrics, "promotion_stats": stats,
                           "seconds": round(time.monotonic() - started, 1)}
        cs.log(f"k={k:g}: CONNECTED {metrics['final_score']:.9f} (ic {metrics['ic_mean']:.6f}, "
               f"excess {metrics['annual_excess']:.6f}, turnover {metrics['mean_turnover']:.6f}) "
               f"promoted {stats['promoted_share']*100:.2f}% of eligible rows")

    ranked = sorted(out.items(), key=lambda kv: -kv[1]["connected_final_score"])
    payload = {"status": "complete", "completed_at_local": time.strftime("%Y-%m-%dT%H:%M:%S"),
               "protocol_sha256": sha(HERE / "protocol_wave4.json"),
               "reference_h1_k1_with_peer67_slow16": REFERENCE_H1,
               "variants": out,
               "best_variant": ranked[0][1]["name"],
               "best_connected_final_score": ranked[0][1]["connected_final_score"],
               "beats_reference_h1": bool(ranked[0][1]["connected_final_score"] > REFERENCE_H1),
               "no_test_period_data_read": True}
    (HERE / "wave4_results.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("\n| variant | k | CONNECTED | IC | excess | turnover | vs H1 reference |")
    print("|---|---|---|---|---|---|---|")
    for key, v in ranked:
        m = v["connected_metrics"]
        print(f"| {v['name']} | {v['k']:g} | **{m['final_score']:.9f}** | {m['ic_mean']:.6f} | "
              f"{m['annual_excess']:.6f} | {m['mean_turnover']:.6f} | "
              f"{m['final_score'] - REFERENCE_H1:+.6f} |")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("stage", choices=("freeze", "run"))
    args = parser.parse_args()
    try:
        globals()[args.stage]()
    except Exception as error:
        (HERE / f"failure_wave4_{args.stage}_{time.time_ns()}.json").write_text(
            json.dumps({"stage": args.stage, "type": type(error).__name__, "message": str(error),
                        "traceback": traceback.format_exc()}, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8")
        raise
