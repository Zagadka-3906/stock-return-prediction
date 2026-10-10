"""Wave 12: the orderer role wants maximum IC and no smoothing - so sweep EVERY backbone, not just slow16.

Wave 9 found the orderer by screening the library on connected ic_mean, and the winner was the
peer67_slow16 backbone re-post-processed at alpha 0 / bonus 0.15 (IC 0.127568, the library maximum).
The mechanism explains why: the orderer never chooses the Top decile, so its own turnover is
irrelevant, and smoothing exists purely to buy turnover at the cost of IC. Stripping smoothing
therefore converts a bad standalone scheme (0.3337) into the best orderer in the library.

But wave 6 only swept the post-processing stack on ONE backbone. Every other surviving backbone has
only ever been scored at the released alpha 0.9 / bonus 0.3, so none of them has been tried in the role
where smoothing should be removed. This wave rebuilds each surviving raw family at alpha 0 / bonus 0
and scores it as the orderer against the fixed membership donor (topk) at the selected retention floor.

Everything is cache-only: the raw per-fold columns survive, the fold frames come from the frozen
revalidation bundle, and the post-processing is the same parameterized stack whose identity with the
production pipeline wave 6 already proved bit-for-bit. The deterministic tie-break from wave 11 is
applied so the construction matches what would be shipped.
"""
from __future__ import annotations

import gc
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
sys.path.insert(0, str(HERE))
import connected_scorer as cs  # noqa: E402
from experiments.revalidate_fold_local import score_official  # noqa: E402
from optimize_wave6 import make_prediction_param  # noqa: E402
from optimize_wave7b import build  # noqa: E402
from score_wave3 import discover, load_raw  # noqa: E402
from src.scoring import Panel  # noqa: E402

R4 = ROOT.parent / "赛题五_历史归档_20261001/experiments/revalidation_20260926/validation"
YEARS = cs.YEARS
KEYS = cs.KEYS
ORDERER_SETTING = {"alpha": 0.0, "bonus": 0.0, "restore_lower": True, "top_current_weight": 1.0,
                   "mode": "top_only", "weight": 0.25}
M_FRAC = 0.985
TIE_EPS = 1e-9
CURRENT_BEST = 0.440149630
CURRENT_BEST_NAME = "topk_x_a0_b0_m0.985_tiebreak"


def sha(path) -> str:
    value = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for chunk in iter(lambda: stream.read(8 * 1024 * 1024), b""):
            value.update(chunk)
    return value.hexdigest()


def main() -> None:
    # freeze before any score exists
    protocol_path = HERE / "protocol_wave12.json"
    if not protocol_path.exists():
        protocol_path.write_text(json.dumps({
            "frozen_at_local": time.strftime("%Y-%m-%dT%H:%M:%S"),
            "standard": "后续选模标准.md §3 connected composite primary; §4 highest score wins",
            "status": "in_sample_selection_disclosed",
            "hypothesis": "the orderer role never chooses the Top decile, so its own turnover is "
                          "irrelevant and smoothing - which exists only to buy turnover at the cost of "
                          "IC - should be removed. Wave 6 swept the post-processing stack on ONE "
                          "backbone; this sweeps every surviving backbone at alpha 0 / bonus 0 in the "
                          "orderer role.",
            "membership_donor_fixed": "topk @ released post-processing (wave 9's exhaustive membership "
                                      "argmax; not re-searched here)",
            "m_frac_fixed_at": M_FRAC,
            "m_provenance": "the wave 10/11 optimum for this membership donor",
            "tie_break_eps": TIE_EPS,
            "candidate_set": "every raw family and single-member arm with all five fold years present, "
                             "auto-discovered across the three preserved trees",
            "selection_rule": "highest connected 2020-2024 official composite",
            "current_best_before_this_wave": {"name": CURRENT_BEST_NAME,
                                              "connected_final_score": CURRENT_BEST},
            "disclosed_selection_cost": "eighth consecutive search over the same five viewed years; "
                                        "cumulative candidate count now exceeds 400 and no blind "
                                        "period remains",
            "no_test_period_data_read": True,
            "source_sha256": sha(Path(__file__)),
        }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        cs.log(f"wave-12 protocol frozen: {sha(protocol_path)[:16]}…")

    sys.path.insert(0, str(ROOT / "analysis"))
    from analysis.topset_hybrid_20261002 import fold_validation as fv
    rank_average_n = fv.load_rank_average_n()

    frames = {y: pl.read_parquet(R4 / f"predictions_ensemble4_{y}.parquet").sort("trade_date", "ts_code")
              for y in YEARS}
    combined = cs.combined_frame()
    dates = combined["trade_date"].to_numpy()
    flags = combined["flag_limit_up"].to_numpy().astype(np.int64)
    codes, uniques = pd.factorize(combined["ts_code"].to_pandas(), sort=True)
    codes = codes.astype(np.int64)
    n_codes = len(uniques)
    tie_key = 1.0 - codes / max(n_codes - 1, 1)
    member = np.load(HERE / "connected_pred_topk.npy")

    families, singles = discover()
    todo = []
    for (stem, parent), by_year in sorted(families.items()):
        if not all(y in by_year for y in YEARS):
            continue
        common = set.intersection(*[set(by_year[y]) for y in YEARS])
        if common:
            todo.append(("seedavg", f"{stem}__{parent.name}", parent, sorted(common), by_year))
    for (name, parent), by_year in sorted(singles.items()):
        if all(y in by_year for y in YEARS):
            todo.append(("single", f"{name}__{parent.name}", parent, None, by_year))
    cs.log(f"{len(todo)} raw families are complete over all five years")

    results = {}
    for kind, label, parent, seeds, by_year in todo:
        try:
            parts, standalone = [], None
            for year in YEARS:
                frame = frames[year]
                if kind == "seedavg":
                    raws = [load_raw(by_year[year][s], year, frame) for s in seeds]
                    days = frame["trade_date"].n_unique()
                    codes_year = len(frame) // days
                    averaged = rank_average_n(raws, frame["price_valid"].to_numpy(), codes_year)
                else:
                    averaged = load_raw(by_year[year], year, frame)
                panel = Panel.from_frame(frame.with_columns(pl.Series("pred_raw", averaged)))
                parts.append(make_prediction_param(
                    panel, frame["aux_raw"].to_numpy().astype(np.float64),
                    ORDERER_SETTING["mode"], ORDERER_SETTING["weight"], ORDERER_SETTING["alpha"],
                    ORDERER_SETTING["bonus"], ORDERER_SETTING["restore_lower"],
                    ORDERER_SETTING["top_current_weight"]))
                del panel
                gc.collect()
            orderer = np.concatenate(parts)
            np.save(HERE / f"orderer_a0b0_{label[:60]}.npy", orderer)

            hybrid, stats = build(member, orderer + TIE_EPS * tie_key, dates, flags, codes,
                                  n_codes, M_FRAC)
            metrics, _ = score_official(combined, hybrid)
            results[label] = {
                "backbone": label, "kind": kind, "n_seeds": len(seeds) if seeds else 1,
                "orderer_postprocess": ORDERER_SETTING, "m_frac": M_FRAC,
                "connected_final_score": metrics["final_score"], "connected_metrics": metrics,
                "boundary_tie_days": stats["boundary_tie_days"],
                "mean_retention_ratio": stats["mean_retention_ratio"],
                "beats_current_best": bool(metrics["final_score"] > CURRENT_BEST)}
            cs.log(f"{label[:56]:56s} as orderer: CONNECTED {metrics['final_score']:.9f} "
                   f"(ic {metrics['ic_mean']:.6f}, excess {metrics['annual_excess']:.6f}, "
                   f"turnover {metrics['mean_turnover']:.6f}, ties {stats['boundary_tie_days']})")
            del parts, orderer, hybrid
            gc.collect()
        except Exception as error:
            results[label] = {"backbone": label, "error": f"{type(error).__name__}: {error}"}
            cs.log(f"{label[:56]:56s} FAILED {type(error).__name__}: {error}")

    scored = {k: v for k, v in results.items() if "connected_final_score" in v}
    ranked = sorted(scored.items(), key=lambda kv: -kv[1]["connected_final_score"])
    payload = {"status": "complete", "completed_at_local": time.strftime("%Y-%m-%dT%H:%M:%S"),
               "purpose": "sweep every surviving backbone as the ORDERER at alpha 0 / bonus 0, the "
                          "setting wave 9 identified as optimal for that role",
               "membership_donor_fixed": "topk @ released post-processing",
               "m_frac": M_FRAC, "tie_break_eps": TIE_EPS,
               "current_best_before_this_wave": {"name": CURRENT_BEST_NAME,
                                                 "connected_final_score": CURRENT_BEST},
               "results": results, "n_scored": len(scored),
               "n_failed": len(results) - len(scored),
               "best": ranked[0][0] if ranked else None,
               "best_connected_final_score": ranked[0][1]["connected_final_score"] if ranked else None,
               "improves_on_current_best": bool(ranked and ranked[0][1]["connected_final_score"]
                                                > CURRENT_BEST),
               "no_test_period_data_read": True,
               "source_sha256": sha(Path(__file__))}
    (HERE / "wave12_results.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"\n| rank | backbone as orderer (alpha 0 / bonus 0) | seeds | CONNECTED | IC | excess | "
          f"turnover |")
    print("|---|---|---|---|---|---|---|")
    for i, (name, v) in enumerate(ranked[:20]):
        m = v["connected_metrics"]
        print(f"| {i+1} | {name[:52]} | {v['n_seeds']} | **{m['final_score']:.9f}** | "
              f"{m['ic_mean']:.6f} | {m['annual_excess']:.6f} | {m['mean_turnover']:.6f} |")
    print(f"\ncurrent best before this wave: {CURRENT_BEST_NAME} {CURRENT_BEST:.9f}")
    if ranked:
        print(f"best here: {ranked[0][0]} {ranked[0][1]['connected_final_score']:.9f} -> "
              f"{'IMPROVES' if payload['improves_on_current_best'] else 'does not improve'}")


if __name__ == "__main__":
    main()
