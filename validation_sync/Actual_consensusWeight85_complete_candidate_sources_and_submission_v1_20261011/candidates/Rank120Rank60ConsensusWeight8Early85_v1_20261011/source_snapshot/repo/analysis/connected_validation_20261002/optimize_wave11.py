"""Wave 11: re-select on the EXACT construction that will be shipped, tie-break included.

Wave 10 ranked candidates built without a deterministic tie-break. The submission builder then found
that alpha = 0 leaves 3 of 344 test days with an exact tie across the promotion boundary, which would
hand the realized Top decile to the evaluator's non-stable sort. Breaking those ties with a causal,
label-free key (1 - ts_code_rank/(n_codes-1), scaled by 1e-9) makes the artifact deterministic - but
applying it to the folds moves the connected score by 1.5e-05, because the fold data has ties inside
the promoted block whose order decides which members fill the smaller excess Top decile.

1.5e-05 is 100x below this project's 0.001743 refit noise floor, but wave 10's top two orderers are
only 2.3e-05 apart, so a shift of that size can reorder them. Selecting on a construction that is not
the one being shipped is exactly the error the harness proofs exist to prevent, so the finalists are
re-scored here with the tie-break inside the construction, and the winner is whoever leads on THAT.

Disclosed: this is the seventh consecutive search over the same five viewed years, and the differences
being ranked are two orders of magnitude below the noise floor. §4 has no materiality threshold, so
the curve is reported in full and the plateau, not the spike, is what should be shipped.
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
MEMBER = "connected_pred_topk.npy"
NESTED_MEMBER = "connected_pred_hybrid.npy"
ORDERERS = {
    "a0_b0.15": "pp_a0_b0.15_top_only_w0.25_rl1_tcw1.npy",
    "a0_b0": "pp_a0_b0_top_only_w0.25_rl1_tcw1.npy",
    "a0.5_b0": "pp_a0.5_b0_top_only_w0.25_rl1_tcw1.npy",
    "W5a": "connected_pred_W5a_five_way_with_gru__final_sweep_eval.npy",
}
M_VALUES = (0.985, 0.988)
CONFIRMED = 0.427407938


def sha(path) -> str:
    value = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for chunk in iter(lambda: stream.read(8 * 1024 * 1024), b""):
            value.update(chunk)
    return value.hexdigest()


def main() -> None:
    frame = cs.combined_frame()
    dates = frame["trade_date"].to_numpy()
    flags = frame["flag_limit_up"].to_numpy().astype(np.int64)
    codes, uniques = pd.factorize(frame["ts_code"].to_pandas(), sort=True)
    codes = codes.astype(np.int64)
    n_codes = len(uniques)
    tie_key = 1.0 - codes / max(n_codes - 1, 1)

    member = np.load(HERE / MEMBER)
    nested = np.load(HERE / NESTED_MEMBER)
    results = {}
    for orderer_name, filename in ORDERERS.items():
        orderer = np.load(HERE / filename) + TIE_EPS * tie_key
        for m_frac in M_VALUES:
            pred, stats = build(member, orderer, dates, flags, codes, n_codes, m_frac)
            metrics, _ = score_official(frame, pred)
            key = f"topk_x_{orderer_name}_m{m_frac:g}_tiebreak"
            np.save(HERE / f"wave11_{key}.npy", pred)
            results[key] = {"member": "topk", "orderer": orderer_name, "m_frac": m_frac,
                            "tie_break": TIE_EPS,
                            "connected_final_score": metrics["final_score"],
                            "connected_metrics": metrics,
                            "boundary_tie_days": stats["boundary_tie_days"],
                            "mean_retention_ratio": stats["mean_retention_ratio"]}
            cs.log(f"{key}: CONNECTED {metrics['final_score']:.9f} (ic {metrics['ic_mean']:.6f}, "
                   f"excess {metrics['annual_excess']:.6f}, turnover {metrics['mean_turnover']:.6f}, "
                   f"boundary ties {stats['boundary_tie_days']})")
            del pred

    for m_frac in M_VALUES:
        orderer = np.load(HERE / ORDERERS["a0_b0.15"]) + TIE_EPS * tie_key
        pred, stats = build(nested, orderer, dates, flags, codes, n_codes, m_frac)
        metrics, _ = score_official(frame, pred)
        key = f"nested_x_a0_b0.15_m{m_frac:g}_tiebreak"
        np.save(HERE / f"wave11_{key}.npy", pred)
        results[key] = {"member": "nested_hybrid", "orderer": "a0_b0.15", "m_frac": m_frac,
                        "tie_break": TIE_EPS, "connected_final_score": metrics["final_score"],
                        "connected_metrics": metrics,
                        "boundary_tie_days": stats["boundary_tie_days"],
                        "mean_retention_ratio": stats["mean_retention_ratio"], "nested": True}
        cs.log(f"{key}: CONNECTED {metrics['final_score']:.9f} (turnover "
               f"{metrics['mean_turnover']:.6f}, boundary ties {stats['boundary_tie_days']})")
        del pred

    ranked = sorted(results.items(), key=lambda kv: -kv[1]["connected_final_score"])
    ties = sum(1 for v in results.values() if v["boundary_tie_days"])
    payload = {"status": "complete", "completed_at_local": time.strftime("%Y-%m-%dT%H:%M:%S"),
               "purpose": "re-select on the exact shipped construction, deterministic tie-break included",
               "tie_break_eps": TIE_EPS,
               "candidates_with_remaining_boundary_ties": ties,
               "results": results, "best": ranked[0][0],
               "best_connected_final_score": ranked[0][1]["connected_final_score"],
               "confirmed_model_connected": CONFIRMED,
               "gain_over_confirmed": ranked[0][1]["connected_final_score"] - CONFIRMED,
               "materiality_note": f"the spread across the top of this table is of order 1e-4, i.e. "
                                   f"~{0.001743 / 1e-4:.0f}x below the 0.001743 refit noise floor; "
                                   "§4 sets no materiality threshold, so the plateau is reported "
                                   "rather than only its maximum",
               "no_test_period_data_read": True,
               "source_sha256": sha(Path(__file__))}
    (HERE / "wave11_results.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"\ncandidates still carrying boundary ties: {ties}")
    print("\n| rank | candidate | CONNECTED | IC | excess | turnover | vs confirmed |")
    print("|---|---|---|---|---|---|---|")
    for i, (name, v) in enumerate(ranked):
        m = v["connected_metrics"]
        print(f"| {i+1} | {name} | **{m['final_score']:.9f}** | {m['ic_mean']:.6f} | "
              f"{m['annual_excess']:.6f} | {m['mean_turnover']:.6f} | "
              f"{m['final_score'] - CONFIRMED:+.6f} |")


if __name__ == "__main__":
    main()
