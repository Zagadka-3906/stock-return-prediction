"""Persist the wave-13 winning fold column so the submission builder can prove against it.

Wave 13 scored its arms without saving the arrays. The winner is the nested donor (wave 1's lift of
peer67_slow16 finished over topk's Top decile) with W5a at alpha 0 / bonus 0 as both orderer roles at
m = 0.985, connected 2020-2024 composite 0.442481207. build_w5a_submission.py needs that exact array
on disk so its proof 3 can recompute the selection score from the file it is shipping against.

This rebuilds it with the same build_ab and the same tie-break wave 13 used and requires the score to
match the recorded value to 1e-12 before saving.
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
from optimize_wave13 import build_ab, W5A_ORDERER, TIE_EPS  # noqa: E402

OUT = HERE / "wave13_nested_x_W5a_a0b0_m0.985_tiebreak.npy"
M_FRAC = 0.985


def sha(path) -> str:
    value = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for chunk in iter(lambda: stream.read(8 * 1024 * 1024), b""):
            value.update(chunk)
    return value.hexdigest()


def main() -> None:
    wave13 = json.loads((HERE / "wave13_results.json").read_text(encoding="utf-8"))
    arm = wave13["results"]["stage2_donor"]["hybrid"]
    expected = float(arm["connected_final_score"])

    frame = cs.combined_frame()
    dates = frame["trade_date"].to_numpy()
    flags = frame["flag_limit_up"].to_numpy().astype(np.int64)
    codes, uniques = pd.factorize(frame["ts_code"].to_pandas(), sort=True)
    codes = codes.astype(np.int64)
    tie_key = 1.0 - codes / max(len(uniques) - 1, 1)

    member = np.load(HERE / "connected_pred_hybrid.npy")
    orderer = np.load(HERE / f"{W5A_ORDERER}.npy") + TIE_EPS * tie_key
    hybrid, stats = build_ab(member, orderer, orderer, dates, flags, codes, len(uniques), M_FRAC)
    metrics, _ = score_official(frame, hybrid)
    diff = abs(metrics["final_score"] - expected)
    print(f"[{time.strftime('%H:%M:%S')}] rebuilt connected {metrics['final_score']:.9f}, "
          f"recorded {expected:.9f}, diff {diff:.3e}")
    if diff > 1e-12:
        raise AssertionError(f"the rebuilt arm does not reproduce the recorded score (diff {diff:.3e})")

    np.save(OUT, hybrid)
    record = {"arm": "stage2_donor::hybrid", "connected_final_score": metrics["final_score"],
              "recorded_in_wave13": expected, "abs_diff": diff,
              "connected_metrics": metrics, "construction_stats": stats,
              "membership_donor": {"column": "connected_pred_hybrid.npy",
                                   "sha256": sha(HERE / "connected_pred_hybrid.npy"),
                                   "construction": "wave 1 lift: promoted = top_sets(topk finished); "
                                                   "out = promoted*(span+1) + peer67_slow16 finished",
                                   "reproduced_bit_exactly_by": "reconstruct_nested_donor.py"},
              "orderer": {"column": f"{W5A_ORDERER}.npy",
                          "sha256": sha(HERE / f"{W5A_ORDERER}.npy"),
                          "postprocess": {"alpha": 0.0, "bonus": 0.0, "mode": "top_only",
                                          "weight": 0.25, "restore_lower": True,
                                          "top_current_weight": 1.0},
                          "roles": "A and B (wave 13 stage 3 showed decoupling them does not help)"},
              "m_frac": M_FRAC, "tie_break_eps": TIE_EPS,
              "tie_break_key": "1 - ts_code_rank/(n_codes-1), causal and label-free",
              "output": {"path": str(OUT), "sha256": sha(OUT), "rows": int(len(hybrid))},
              "saved_at_local": time.strftime("%Y-%m-%dT%H:%M:%S")}
    (HERE / "wave13_selected_arm.json").write_text(
        json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"[{time.strftime('%H:%M:%S')}] saved {OUT.name} and wave13_selected_arm.json")


if __name__ == "__main__":
    main()
