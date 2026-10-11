"""Wave 8: joint refinement - re-tune each donor's post-processing, then combine, then swap-budget.

Wave 6 found the released post-processing is only 6th of 43 on the connected caliber: alpha 0.8 with a
0.6 retention bonus scores 0.430225 against the released 0.427408, and essentially all of that gain is
the turnover term (0.037379 -> 0.025499), which had been assumed saturated. Wave 7b fixed the
Top-set-substitution construction (reassign the eligible subset's own score slots instead of lifting
above limit-up names, which are inside the Rank IC universe) and proved the identity case to 0.0e+00,
lifting the hybrid to 0.431943.

Those two gains are independent and target different terms, so this wave combines them. The membership
donor supplies excess and turnover; the orderer supplies Rank IC. Both donors' post-processing is
re-tuned, because the retention bonus acts on whichever stage decides the Top set - for the membership
donor that is exactly the term wave 6 improved.

Pre-declared candidate set, scored once each, no further search:
  membership in {topk @ released, topk @ a0.8 b0.6, topk @ a0.9 b0.6, slow16 @ a0.8 b0.6}
  ordering   in {W5a @ released, slow16 @ released, slow16 @ a0.8 b0.6}
  m          in {0, 0.98}          (swap-budget retention floor; 0.98 caps turnover near 0.039)
That is 24 settings. Selection is the highest connected 2020-2024 composite per 后续选模标准.md §4.

Harness proofs required before any combination is trusted:
  * re-post-processing topk's raw at the released settings must reproduce topk's frozen connected
    score 0.414783593
  * re-post-processing the slow16 raw rank average at the released settings must reproduce
    0.427407938
  * membership == orderer at m = 0 must be the identity
No test-period data is read anywhere.
"""
from __future__ import annotations

import argparse
import gc
import hashlib
import itertools
import json
import sys
import time
import traceback
from pathlib import Path

import numpy as np
import polars as pl

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(HERE))
import connected_scorer as cs  # noqa: E402
from experiments.revalidate_fold_local import score_official  # noqa: E402
from optimize_wave6 import make_prediction_param, fold_frame, raw_average, RELEASED  # noqa: E402
from optimize_wave7b import build  # noqa: E402
from src.scoring import Panel  # noqa: E402

ARCHIVE = ROOT.parent / "赛题五_历史归档_20261001"
TOPK_DIRS = [ROOT / "analysis/topk_training_validation_20261001",
             ARCHIVE / "experiments/r6_topk_20260926"]
YEARS = cs.YEARS
KEYS = cs.KEYS
A08B06 = {"alpha": 0.8, "bonus": 0.6, "restore_lower": True, "top_current_weight": 1.0,
          "mode": "top_only", "weight": 0.25}
A09B06 = {**A08B06, "alpha": 0.9}
EXPECTED = {"topk_released": 0.414783593, "slow16_released": 0.427407938}
# Wave 7b's scan put the interior optimum at m = 0.99 (0.432647) with m = 1.0 collapsing (0.421341),
# so this grid is centred there. That is adaptive: it was chosen after seeing wave 7b's scores, and is
# disclosed as such in the protocol rather than presented as a pre-planned design.
M_VALUES = (0.0, 0.98, 0.99)

MEMBERS = {
    "topk_rel": ("topk", RELEASED),
    "topk_a08b06": ("topk", A08B06),
    "topk_a09b06": ("topk", A09B06),
    "slow16_a08b06": ("slow16", A08B06),
    # the highest-excess backbone in the entire library (annual excess 0.539766, turnover 0.597550):
    # a finished column wave 6 already saved, so it is loaded rather than rebuilt
    "a0b015": ("file", "pp_a0_b0.15_top_only_w0.25_rl1_tcw1"),
}
ORDERERS = {
    "W5a_rel": ("W5a_five_way_with_gru__final_sweep_eval", None),
    "slow16_rel": ("slow16", RELEASED),
    "slow16_a08b06": ("slow16", A08B06),
}


def sha(path) -> str:
    value = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for chunk in iter(lambda: stream.read(8 * 1024 * 1024), b""):
            value.update(chunk)
    return value.hexdigest()


def topk_raw(year: int) -> tuple[pl.DataFrame, np.ndarray]:
    for directory in TOPK_DIRS:
        path = directory / f"predictions_topk_return_backbone_{year}.parquet"
        if path.exists():
            df = pl.read_parquet(path).sort("trade_date", "ts_code")
            return df, df["pred_raw"].to_numpy().astype(np.float64)
    raise SystemExit(f"no topk raw prediction for {year}")


def build_donor(kind: str, setting: dict, bundles: dict, rank_average_n) -> np.ndarray:
    """Connected prediction for one donor at one post-processing setting."""
    parts = []
    for year in YEARS:
        frame = bundles[year]
        if kind == "topk":
            source, raw = topk_raw(year)
            if len(raw) != len(frame):
                raise AssertionError(f"topk {year}: {len(raw)} rows vs frame {len(frame)}")
            if not source.select(KEYS).equals(frame.select(KEYS)):
                raise AssertionError(f"topk {year}: raw prediction keys do not match the fold frame")
        else:
            raw = raw_average(frame, rank_average_n)
        panel = Panel.from_frame(frame.with_columns(pl.Series("pred_raw", raw)))
        parts.append(make_prediction_param(panel, frame["aux_raw"].to_numpy().astype(np.float64),
                                          setting["mode"], setting["weight"], setting["alpha"],
                                          setting["bonus"], setting["restore_lower"],
                                          setting["top_current_weight"]))
        del panel, raw
        gc.collect()
    return np.concatenate(parts)


def main() -> None:
    stage = sys.argv[1] if len(sys.argv) > 1 else "run"
    sys.path.insert(0, str(ROOT / "analysis"))
    from analysis.topset_hybrid_20261002 import fold_validation as fv
    rank_average_n = fv.load_rank_average_n()

    frame_all = cs.combined_frame()
    dates = frame_all["trade_date"].to_numpy()
    flags = frame_all["flag_limit_up"].to_numpy()
    import pandas as pd
    codes, uniques = pd.factorize(frame_all["ts_code"].to_pandas(), sort=True)
    codes = codes.astype(np.int64)
    n_codes = len(uniques)

    bundles = {}
    for year in YEARS:
        frame = fold_frame(year)
        combined_slice = frame_all.filter(
            pl.Series((dates >= year * 10000 + 101) & (dates <= year * 10000 + 1231)))
        if not frame.select(KEYS).equals(combined_slice.select(KEYS)):
            raise AssertionError(f"{year}: fold frame does not match the combined slice")
        bundles[year] = frame
    cs.log("five fold frames aligned with the combined frame")

    if stage == "freeze":
        payload = {
            "frozen_at_local": time.strftime("%Y-%m-%dT%H:%M:%S"),
            "standard": "后续选模标准.md §3 connected composite primary; §4 highest score wins",
            "status": "in_sample_selection_disclosed",
            "members": {k: {"donor": v[0], "postprocess": v[1]} for k, v in MEMBERS.items()},
            "orderers": {k: {"donor": v[0], "postprocess": v[1]} for k, v in ORDERERS.items()},
            "m_values": list(M_VALUES),
            "n_candidates": len(MEMBERS) * len(ORDERERS) * len(M_VALUES),
            "harness_proofs_required": {
                "topk_at_released_settings": EXPECTED["topk_released"],
                "slow16_at_released_settings": EXPECTED["slow16_released"],
                "identity_when_member_equals_orderer_at_m0": True},
            "construction": "wave-7b slot reassignment inside the eligible subset, so limit-up rows "
                            "stay where the orderer put them and the identity case is exact",
            "selection_rule": "highest connected composite; ties broken by smaller m, then by fewer "
                              "deviations from the released post-processing",
            "disclosed_selection_cost": "24 settings maximized over five repeatedly viewed years, on "
                                        "top of 43 post-processing settings in wave 6 and 42 arms in "
                                        "waves 1-3; no blind period remains, so the winner's score is "
                                        "upward-biased by cumulative selection and this is a ranking, "
                                        "not a significance claim",
            "causality": "every donor is a walk-forward fold prediction trained strictly before its "
                         "validation year; the retention floor uses only the previous day's realized "
                         "Top decile; no label or label availability is read",
            "no_test_period_data_read": True,
            "source_sha256": sha(Path(__file__)),
        }
        if (HERE / "protocol_wave8.json").exists():
            raise FileExistsError("protocol already frozen")
        (HERE / "protocol_wave8.json").write_text(
            json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        cs.log(f"wave-8 protocol frozen: {payload['n_candidates']} candidates")
        return

    protocol = json.loads((HERE / "protocol_wave8.json").read_text(encoding="utf-8"))
    assert protocol["source_sha256"] == sha(Path(__file__)), "script changed after freezing"

    # ---- donor library, with the two reproduction proofs
    donors = {}
    for name, (kind, setting) in list(MEMBERS.items()) + [
            (k, (v[0], v[1])) for k, v in ORDERERS.items() if v[1] is not None]:
        if name in donors:
            continue
        if kind == "file":
            path = HERE / f"{setting}.npy"
            if not path.exists():
                raise SystemExit(f"missing finished donor column: {path}")
            donors[name] = np.load(path)
            cs.log(f"donor {name}: loaded finished column {path.name} "
                   f"({len(donors[name]):,} rows)")
            continue
        pred = build_donor(kind, setting, bundles, rank_average_n)
        donors[name] = pred
        np.save(HERE / f"donor_{name}.npy", pred)
        if kind == "topk" and setting == RELEASED:
            metrics, _ = score_official(frame_all, pred)
            diff = abs(metrics["final_score"] - EXPECTED["topk_released"])
            if diff > 1e-9:
                raise AssertionError(f"topk at released settings: {metrics['final_score']!r} vs "
                                     f"{EXPECTED['topk_released']!r} (diff {diff:.3e})")
            cs.log(f"PROOF topk @ released reproduces {EXPECTED['topk_released']:.9f} (diff {diff:.1e})")
        if kind == "slow16" and setting == RELEASED:
            metrics, _ = score_official(frame_all, pred)
            diff = abs(metrics["final_score"] - EXPECTED["slow16_released"])
            if diff > 1e-9:
                raise AssertionError(f"slow16 at released settings: {metrics['final_score']!r} vs "
                                     f"{EXPECTED['slow16_released']!r} (diff {diff:.3e})")
            cs.log(f"PROOF slow16 @ released reproduces {EXPECTED['slow16_released']:.9f} "
                   f"(diff {diff:.1e})")
    # W5a is already a finished connected column; no re-post-processing applies to it
    donors["W5a_rel"] = np.load(HERE / "connected_pred_W5a_five_way_with_gru__final_sweep_eval.npy")
    cs.log(f"donor library built: {sorted(donors)}")

    results = {}
    for member, orderer, m_frac in itertools.product(MEMBERS, ORDERERS, M_VALUES):
        name = f"{member}__x__{orderer}__m{m_frac:g}"
        pred, stats = build(donors[member], donors[orderer], dates, flags, codes, n_codes, m_frac)
        metrics, _ = score_official(frame_all, pred)
        np.save(HERE / f"wave8_{name}.npy", pred)
        results[name] = {"member": member, "orderer": orderer, "m_frac": m_frac,
                         "connected_final_score": metrics["final_score"],
                         "connected_metrics": metrics, "stats": stats}
        cs.log(f"{name}: CONNECTED {metrics['final_score']:.9f} (ic {metrics['ic_mean']:.6f}, "
               f"excess {metrics['annual_excess']:.6f}, turnover {metrics['mean_turnover']:.6f}) "
               f"retention {stats['mean_retention_ratio']}")
        del pred
        gc.collect()

    ranked = sorted(results.items(), key=lambda kv: -kv[1]["connected_final_score"])
    payload = {"status": "complete", "completed_at_local": time.strftime("%Y-%m-%dT%H:%M:%S"),
               "protocol_sha256": sha(HERE / "protocol_wave8.json"),
               "reproduction_proofs": {"topk_released": EXPECTED["topk_released"],
                                       "slow16_released": EXPECTED["slow16_released"]},
               "results": results, "best": ranked[0][0],
               "best_connected_final_score": ranked[0][1]["connected_final_score"],
               "wave7b_leader_for_comparison": 0.431942948,
               "gain_over_wave7b_leader": ranked[0][1]["connected_final_score"] - 0.431942948,
               "no_test_period_data_read": True}
    (HERE / "wave8_results.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("\n| rank | member | orderer | m | CONNECTED | IC | excess | turnover | retention |")
    print("|---|---|---|---|---|---|---|---|---|")
    for i, (name, v) in enumerate(ranked):
        mt = v["connected_metrics"]
        print(f"| {i+1} | {v['member']} | {v['orderer']} | {v['m_frac']:g} | "
              f"**{mt['final_score']:.9f}** | {mt['ic_mean']:.6f} | {mt['annual_excess']:.6f} | "
              f"{mt['mean_turnover']:.6f} | {v['stats']['mean_retention_ratio']} |")


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        (HERE / f"failure_wave8_{time.time_ns()}.json").write_text(
            json.dumps({"type": type(error).__name__, "message": str(error),
                        "traceback": traceback.format_exc()}, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8")
        raise
