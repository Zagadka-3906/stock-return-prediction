"""Persist the final selected fold column so the submission builder can prove against it.

Waves 15-20 scored their arms without saving the arrays. This rebuilds the selected one with the exact
construction its wave used - optimize_wave18's lift for the donor, optimize_wave15's daily_ranks /
weighted_rank_blend for the orderer, optimize_wave13's build_ab for the substitution - and requires it
to reproduce that wave's recorded connected score to 1e-12 before saving. build_w5a_submission.py then
re-scores the saved file as its proof 3, so the number the submission is built against is the number
that was recorded, with no re-derivation in between.

The arm is read from wave20_results.json by name rather than retyped here.
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
from optimize_wave15 import daily_ranks, weighted_rank_blend, TIE_EPS  # noqa: E402
from optimize_wave18 import lift  # noqa: E402
from optimize_wave20 import (SLOW16_FIN, TOPK_FIN, W5A_FIN, W5A_A0B0, SLOW16_A0B0,  # noqa: E402
                             NESTED)


def sha(path) -> str:
    value = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for chunk in iter(lambda: stream.read(8 * 1024 * 1024), b""):
            value.update(chunk)
    return value.hexdigest()


def main() -> None:
    arm_name = sys.argv[1] if len(sys.argv) > 1 else None
    wave20 = json.loads((HERE / "wave20_results.json").read_text(encoding="utf-8"))
    if wave20.get("status") != "complete":
        raise SystemExit("wave 20 is not complete")
    results = wave20["results"]
    if arm_name is None:
        # the harness-proof cells are NOT excluded: wave 20 deliberately scored its reference cell
        # (donor a x W5a+0.25*slow16 x m=0.985) once and used it both as the proof against wave 16's
        # recorded number and as a candidate, so excluding proof cells would skip the winner
        scored = {k: v for k, v in results.items() if "connected_final_score" in v}
        arm_name = max(scored, key=lambda k: scored[k]["connected_final_score"])
    arm = results[arm_name]
    if "connected_final_score" not in arm:
        raise SystemExit(f"{arm_name} has no score: {arm}")
    expected = float(arm["connected_final_score"])
    donor_spec, orderer_spec, m_frac = arm["donor"], arm["orderer"], float(arm["m_frac"])
    print(f"[{time.strftime('%H:%M:%S')}] selected arm: {arm_name}")
    print(f"    donor {donor_spec} | orderer {orderer_spec} | m {m_frac} | recorded {expected:.9f}")

    frame = cs.combined_frame()
    dates = frame["trade_date"].to_numpy()
    flags = frame["flag_limit_up"].to_numpy().astype(np.int64)
    valid = frame["price_valid"].to_numpy().astype(bool)
    codes, uniques = pd.factorize(frame["ts_code"].to_pandas(), sort=True)
    codes = codes.astype(np.int64)
    n_codes = len(uniques)
    tie_key = 1.0 - codes / max(n_codes - 1, 1)
    pdf = frame.select(["trade_date", "flag_limit_up"]).to_pandas()

    slow16_fin = np.load(HERE / SLOW16_FIN)
    topk_fin = np.load(HERE / TOPK_FIN)
    w5a_fin = np.load(HERE / W5A_FIN)
    w5a_a0b0 = np.load(HERE / W5A_A0B0)
    slow16_a0b0 = np.load(HERE / SLOW16_A0B0)

    def blend(a: np.ndarray, b: np.ndarray, na: str, nb: str, w: float) -> np.ndarray:
        cache: dict = {}
        for stem, col in ((na, a), (nb, b)):
            cache[stem] = daily_ranks(col, valid, dates)
        mixed = weighted_rank_blend([a, b], [1.0 - w, w], cache, valid, dates, (na, nb))
        return np.where(mixed > -9.0, mixed + TIE_EPS * tie_key, mixed)

    # ---- donor
    if donor_spec == "a_nested_shipped":
        donor, lift_stats = lift(topk_fin, slow16_fin, pdf)
        frozen = np.load(HERE / NESTED)
        if not np.array_equal(donor, frozen):
            raise AssertionError("the rebuilt nested donor is not connected_pred_hybrid.npy")
        donor_provenance = {"variant": "a", "promotes": TOPK_FIN, "reranks": SLOW16_FIN,
                            "bit_identical_to_frozen_nested": True}
    elif donor_spec.startswith("b_rerank_blend_w"):
        w = float(donor_spec.rsplit("_w", 1)[1])
        donor, lift_stats = lift(topk_fin, blend(slow16_fin, w5a_fin, SLOW16_FIN, W5A_FIN, w), pdf)
        donor_provenance = {"variant": "b", "promotes": TOPK_FIN,
                            "reranks": f"rank_blend(slow16, W5a, {w}) + tie-break",
                            "blend_weight": w}
    else:
        raise SystemExit(f"unknown donor spec: {donor_spec}")

    # ---- orderer
    if orderer_spec == "W5a@a0b0":
        orderer = w5a_a0b0
        orderer_provenance = {"components": [W5A_A0B0], "weights": [1.0]}
    elif orderer_spec.startswith("W5a+") and "*slow16" in orderer_spec:
        w = float(orderer_spec.split("W5a+")[1].split("*slow16")[0])
        orderer = blend(w5a_a0b0, slow16_a0b0, W5A_A0B0, SLOW16_A0B0, w)
        orderer_provenance = {"components": [W5A_A0B0, SLOW16_A0B0], "weights": [1.0 - w, w],
                              "partner_weight": w}
    else:
        raise SystemExit(f"unknown orderer spec: {orderer_spec}")

    hybrid, stats = build_ab(donor, orderer + TIE_EPS * tie_key, orderer + TIE_EPS * tie_key,
                             dates, flags, codes, n_codes, m_frac)
    metrics, _ = score_official(frame, hybrid)
    diff = abs(metrics["final_score"] - expected)
    print(f"[{time.strftime('%H:%M:%S')}] rebuilt connected {metrics['final_score']:.9f}, "
          f"recorded {expected:.9f}, diff {diff:.3e}")
    if diff > 1e-12:
        raise AssertionError(f"the rebuilt arm does not reproduce the recorded score (diff {diff:.3e})")

    stem = f"selected_{arm_name.replace('/', '_')}.npy"
    out = HERE / stem
    np.save(out, hybrid)
    record = {"arm": arm_name, "source_wave": "wave20_results.json",
              "connected_final_score": metrics["final_score"], "recorded": expected,
              "abs_diff": diff, "connected_metrics": metrics,
              "donor": donor_provenance, "donor_lift_stats": lift_stats,
              "orderer": orderer_provenance, "m_frac": m_frac, "tie_break_eps": TIE_EPS,
              "tie_break_key": "1 - ts_code_rank/(n_codes-1), causal and label-free",
              "construction_stats": stats,
              "output": {"path": str(out), "sha256": sha(out), "rows": int(len(hybrid))},
              "saved_at_local": time.strftime("%Y-%m-%dT%H:%M:%S"),
              "no_test_period_data_read": True}
    (HERE / "selected_arm.json").write_text(
        json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"[{time.strftime('%H:%M:%S')}] saved {stem} and selected_arm.json")


if __name__ == "__main__":
    main()
