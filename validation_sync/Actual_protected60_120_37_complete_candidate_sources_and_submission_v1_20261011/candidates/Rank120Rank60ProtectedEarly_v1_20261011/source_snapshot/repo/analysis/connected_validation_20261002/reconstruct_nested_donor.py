"""Reproduce wave 1's LIFT construction so the nested membership donor becomes shippable.

Wave 13 stage 2 put the nested donor (`hybrid`) first at 0.442481207 with W5a as the orderer, ahead of
the plain topk donor at 0.441064514. build_selected_submission.py refuses to ship the nested variant,
and it was right to: the fold column that was scored is wave 1's LIFT construction
(score_arms.hybrid_pred), while that builder only knows wave 7b's slot reassignment, and the two differ
by ~0.0006 on the folds. Shipping a slot-reassigned inner member would not be the scheme that was
scored. The fix the builder asked for is to reproduce the lift explicitly. This does that.

The lift is a pure function of two finished columns, both of which exist for the test period:
    promoted = the Top decile of b on the turnover universe (flag_limit_up == 0, >= 100 rows)
    out      = promoted * (span + 1) + a          span = a.max() - a.min() over the same block
with a = peer67_slow16 finished, b = topk finished. It reads no labels, and it is causal: everything
in it is a day-t prediction or a day-t limit-up flag.

`span` only sets the numeric gap between the promoted and non-promoted blocks. Within each block the
ordering is a's, so the value of span cannot change any rank, any Top decile or any score. It is
reproduced per year anyway, because the fold column was built per year and the proof here is
bit-exactness, not merely score equality.

Proof, run before the test column is written: applying this function to the FOLD columns, per year,
must reproduce connected_pred_hybrid.npy element-for-element. That is the same column wave 13 stage 2
scored at 0.442481207, so a bit-exact match means the test column is built by the same rule.
"""
from __future__ import annotations

import hashlib
import json
import sys
import time
from pathlib import Path

import numpy as np
import polars as pl

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
ARCHIVE = ROOT.parent / "赛题五_历史归档_20261001"
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(HERE))
import connected_scorer as cs  # noqa: E402
from analysis.topset_hybrid_20261002 import fold_validation as fv  # noqa: E402

ALLMODELS = ARCHIVE / "analysis/all_models_test_20260929"
TOPK_TEST = ALLMODELS / "middle/predictions/supplemental_topk_fulltrain2024.parquet"
DELIVERY = ARCHIVE / "deliveries/peer67_slow16_20260929"
OUT_DIR = HERE / "nested_donor"
KEYS = ["ts_code", "trade_date"]
YEARS = cs.YEARS


def sha(path) -> str:
    value = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for chunk in iter(lambda: stream.read(8 * 1024 * 1024), b""):
            value.update(chunk)
    return value.hexdigest()


def log(message: str) -> None:
    print(f"[{time.strftime('%H:%M:%S')}] {message}", flush=True)


def lift(pdf, a_final: np.ndarray, b_final: np.ndarray) -> tuple[np.ndarray, dict]:
    """score_arms.hybrid_pred, verbatim, using the same fv.top_sets that produced the fold column."""
    promoted, stats = fv.top_sets(pdf, b_final)
    if stats["boundary_tie_days"]:
        raise AssertionError(f"arm B has {stats['boundary_tie_days']} Top-boundary tie days")
    span = float(a_final.max() - a_final.min())
    out = promoted.astype(np.float64) * (span + 1.0) + a_final
    promoted_out, _ = fv.top_sets(pdf, out)
    if not np.array_equal(promoted_out, promoted):
        raise AssertionError("the hybrid's Top set is not exactly arm B's")
    return out, {"span": span, "promoted_rows": int(promoted.sum()),
                 "promoted_share": float(promoted.mean()), "days": stats["days"],
                 "skipped_lt100": stats["skipped_lt100"],
                 "boundary_tie_days": stats["boundary_tie_days"]}


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    frame = cs.combined_frame()
    dates = frame["trade_date"].to_numpy()
    a_fold = np.load(HERE / "connected_pred_peer67_slow16.npy")
    b_fold = np.load(HERE / "connected_pred_topk.npy")
    target = np.load(HERE / "connected_pred_hybrid.npy")
    for name, array in (("slow16 fold", a_fold), ("topk fold", b_fold), ("hybrid fold", target)):
        if len(array) != len(frame):
            raise AssertionError(f"{name} has {len(array)} rows, combined frame has {len(frame)}")

    # ---- PROOF: rebuild the fold hybrid per year and require bit-exactness
    parts, per_year = [], {}
    for year in YEARS:
        mask = (dates >= year * 10000 + 101) & (dates <= year * 10000 + 1231)
        yf = frame.filter(pl.Series(mask))
        pdf = yf.select(["trade_date", "flag_limit_up"]).to_pandas()
        out, stats = lift(pdf, a_fold[mask], b_fold[mask])
        parts.append(out)
        per_year[str(year)] = {"rows": int(mask.sum()), **stats}
        log(f"  fold {year}: span {stats['span']:.6f}, promoted {stats['promoted_rows']:,} "
            f"({stats['promoted_share']*100:.3f}%), days {stats['days']}")
    rebuilt = np.concatenate(parts)
    if len(rebuilt) != len(target):
        raise AssertionError(f"rebuilt fold hybrid has {len(rebuilt)} rows, target has {len(target)}")
    identical = bool(np.array_equal(rebuilt, target))
    max_diff = float(np.abs(rebuilt - target).max())
    log(f"PROOF: rebuilt fold hybrid {'EQUALS' if identical else 'DIFFERS FROM'} "
        f"connected_pred_hybrid.npy (max abs diff {max_diff:.3e})")
    if not identical:
        raise AssertionError("the lift reproduction is not wave 1's construction: the rebuilt fold "
                             f"hybrid differs from connected_pred_hybrid.npy (max diff {max_diff:.3e})")

    # ---- test side: a = the delivery's own finished rank_score, b = topk's finished test column
    prediction = pl.read_parquet(DELIVERY / "prediction.parquet")
    a_test = prediction["rank_score"].to_numpy().astype(np.float64)
    topk = pl.read_parquet(TOPK_TEST)
    if not topk.select(KEYS).equals(prediction.select(KEYS)):
        topk = prediction.select(KEYS).join(topk.select(KEYS + ["pred"]), on=KEYS, how="left")
        if topk["pred"].null_count():
            raise AssertionError("topk test join lost rows")
    b_test = topk["pred"].to_numpy().astype(np.float64)
    if len(a_test) != len(b_test):
        raise AssertionError("test donor columns differ in length")
    pdf_test = prediction.select(["trade_date", "flag_limit_up"]).to_pandas()
    member, stats = lift(pdf_test, a_test, b_test)
    log(f"test nested donor built: {len(member):,} rows, span {stats['span']:.6f}, "
        f"promoted {stats['promoted_rows']:,} ({stats['promoted_share']*100:.3f}%), "
        f"days {stats['days']}, boundary ties {stats['boundary_tie_days']}")

    np.save(OUT_DIR / "nested_donor_test.npy", member)
    record = {
        "status": "proven",
        "proved_at_local": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "claim": "wave 1's lift construction is reproduced exactly, so the nested membership donor "
                 "that wave 13 stage 2 selected can be shipped",
        "construction": "promoted = fv.top_sets(b) on the turnover universe; out = promoted*(span+1)+a; "
                        "span = a.max()-a.min() over the same block; a = peer67_slow16 finished, "
                        "b = topk finished",
        "fold_proof": {"rebuilt_equals_connected_pred_hybrid": identical, "max_abs_diff": max_diff,
                       "target_sha256": sha(HERE / "connected_pred_hybrid.npy"),
                       "per_year": per_year,
                       "note": "built per year with that year's span, exactly as score_arms.py did, "
                               "because the proof is bit-exactness and not merely score equality"},
        "span_is_rank_irrelevant": "within each block the ordering is a's, so span cannot change any "
                                   "rank, any Top decile or any score; it is reproduced per year only "
                                   "to make the fold proof bit-exact",
        "test_inputs": {
            "a": {"path": str(DELIVERY / "prediction.parquet"), "column": "rank_score",
                  "sha256": sha(DELIVERY / "prediction.parquet"),
                  "provenance": "the peer67_slow16 delivery's own finished column; "
                                "build_selected_submission.py proof 1 shows it is exactly "
                                "make_prediction_param at the released settings"},
            "b": {"path": str(TOPK_TEST), "column": "pred", "sha256": sha(TOPK_TEST)},
        },
        "test_stats": stats,
        "output": {"path": str(OUT_DIR / "nested_donor_test.npy"),
                   "sha256": sha(OUT_DIR / "nested_donor_test.npy"),
                   "rows": int(len(member))},
        "labels_read": False,
        "causality": "every input is a day-t prediction or a day-t limit-up flag; the lift reads no "
                     "label and no future row",
        "source_sha256": sha(Path(__file__)),
    }
    (OUT_DIR / "reconstruction_proof.json").write_text(
        json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    log(f"wrote {OUT_DIR / 'reconstruction_proof.json'}")


if __name__ == "__main__":
    main()
