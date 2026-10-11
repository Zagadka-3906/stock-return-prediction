"""Wave 10: refine the retention floor for the donor pair wave 9 selected.

Wave 9 searched both donor roles exhaustively over the screened library at a retention floor fixed at
m = 0.985 (the wave-7b optimum for a DIFFERENT orderer). Its result changes the picture:

  membership axis (orderer fixed at W5a): topk 0.434035, nested hybrid 0.434058, then a large gap to
    0.425068 - topk is the membership donor decisively
  orderer axis (member fixed at topk): the alpha ~ 0 family occupies the whole top, 0.440138 down to
    0.439149 across eight settings, a plateau only 0.0010 wide

The reason is the decoupling the metric allows: the orderer never chooses the Top decile, so its own
turnover is irrelevant, while its Rank IC and its within-set ordering are used in full. The alpha 0 /
bonus 0.15 column has the highest IC (0.127568) and the highest excess (0.539766) in the library and
the worst turnover (0.597550) - as an orderer that combination is ideal, and standalone it scores only
0.3337.

So the retention floor must be re-optimised for THIS pair, because the floor acts on the membership
donor's set while the orderer now supplies a much sharper within-set ordering. Pre-declared grid, one
harness proof, scored once each.

Harness proof: topk x pp::a0_b0.15 at m = 0.985 must reproduce wave 9's 0.440138185 to 1e-9.
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
from optimize_wave7b import build  # noqa: E402

MEMBER = "topk"
ORDERERS = ["pp::a0_b0.15_top_only_w0.25_rl1_tcw1",
            "pp::a0_b0_top_only_w0.25_rl1_tcw1",
            "pp::a0.5_b0_top_only_w0.25_rl1_tcw1"]
M_VALUES = (0.0, 0.90, 0.95, 0.98, 0.985, 0.988, 0.99, 0.995)
WAVE9_ANCHOR = {"orderer": ORDERERS[0], "m_frac": 0.985, "expected": 0.440138185}
NESTED_MEMBER = "hybrid"


def sha(path) -> str:
    value = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for chunk in iter(lambda: stream.read(8 * 1024 * 1024), b""):
            value.update(chunk)
    return value.hexdigest()


def load(name: str) -> np.ndarray:
    stem = name[4:] if name.startswith("pp::") else name
    for candidate in (f"pp_{stem}.npy", f"connected_pred_{stem}.npy", f"donor_{name}.npy"):
        path = HERE / candidate
        if path.exists():
            return np.load(path)
    raise SystemExit(f"no saved column for {name}")


def freeze() -> None:
    payload = {
        "frozen_at_local": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "standard": "后续选模标准.md §3 connected composite primary; §4 highest score wins, complexity "
                    "and cost break exact ties only",
        "status": "in_sample_selection_disclosed",
        "membership_donor": MEMBER,
        "membership_donor_provenance": "wave 9's exhaustive membership sweep: topk 0.434035 and the "
                                       "nested hybrid 0.434058 against a next-best 0.425068",
        "orderers": ORDERERS,
        "orderer_provenance": "wave 9's exhaustive orderer sweep: the alpha ~ 0 family occupies the "
                              "entire top, 0.440138 to 0.439149 across eight settings",
        "m_values": list(M_VALUES),
        "nested_member_check": {"member": NESTED_MEMBER, "orderer": ORDERERS[0],
                                "reason": "wave 9 scored the nested hybrid 2.3e-5 above topk at the "
                                          "same orderer and m; that is 75x below this project's "
                                          "0.001743 refit noise floor, so it is checked once and "
                                          "reported, and §4's complexity tie-break is recommended "
                                          "because the standard sets no materiality threshold"},
        "harness_proof": f"{MEMBER} x {WAVE9_ANCHOR['orderer']} at m={WAVE9_ANCHOR['m_frac']} must "
                         f"reproduce {WAVE9_ANCHOR['expected']} to 1e-9",
        "selection_rule": "highest connected 2020-2024 official composite",
        "disclosed_selection_cost": "sixth consecutive search over the same five viewed years; "
                                    "cumulative candidate count now exceeds 200 and no blind period "
                                    "remains to quantify the resulting upward bias",
        "materiality_note": "§4 breaks ties on complexity only when scores are EXACTLY equal. Several "
                            "of the differences this wave will produce are of order 1e-4 to 1e-5, far "
                            "below the 0.001743 refit noise floor, so a literal argmax would select on "
                            "noise. The curve is reported in full so a plateau can be chosen instead of "
                            "a spike.",
        "no_test_period_data_read": True,
        "source_sha256": sha(Path(__file__)),
    }
    if (HERE / "protocol_wave10.json").exists():
        raise FileExistsError("protocol already frozen")
    (HERE / "protocol_wave10.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    cs.log(f"wave-10 protocol frozen: {len(ORDERERS)} orderers x {len(M_VALUES)} m values "
           f"+ 1 nested check")


def run() -> None:
    protocol = json.loads((HERE / "protocol_wave10.json").read_text(encoding="utf-8"))
    assert protocol["source_sha256"] == sha(Path(__file__)), "script changed after freezing"
    frame = cs.combined_frame()
    dates = frame["trade_date"].to_numpy()
    flags = frame["flag_limit_up"].to_numpy()
    codes, uniques = pd.factorize(frame["ts_code"].to_pandas(), sort=True)
    codes = codes.astype(np.int64)
    n_codes = len(uniques)

    member_col = load(MEMBER)
    results = {}
    for orderer in ORDERERS:
        order_col = load(orderer)
        for m_frac in M_VALUES:
            name = f"{MEMBER}__x__{orderer}__m{m_frac:g}"
            pred, stats = build(member_col, order_col, dates, flags, codes, n_codes, m_frac)
            metrics, _ = score_official(frame, pred)
            if (orderer == WAVE9_ANCHOR["orderer"]
                    and abs(m_frac - WAVE9_ANCHOR["m_frac"]) < 1e-12):
                diff = abs(metrics["final_score"] - WAVE9_ANCHOR["expected"])
                if diff > 1e-9:
                    raise AssertionError(f"harness proof failed: {metrics['final_score']!r} vs "
                                         f"{WAVE9_ANCHOR['expected']!r} (diff {diff:.3e})")
                cs.log(f"HARNESS PROOF passed, reproduces wave 9's {WAVE9_ANCHOR['expected']:.9f} "
                       f"(diff {diff:.1e})")
            np.save(HERE / f"wave10_{orderer.replace('pp::', '').replace(':', '_')}_m{m_frac:g}.npy",
                    pred)
            results[name] = {"member": MEMBER, "orderer": orderer, "m_frac": m_frac,
                             "connected_final_score": metrics["final_score"],
                             "connected_metrics": metrics,
                             "mean_retention_ratio": stats["mean_retention_ratio"]}
            cs.log(f"{name[:64]}: CONNECTED {metrics['final_score']:.9f} (ic {metrics['ic_mean']:.6f}, "
                   f"excess {metrics['annual_excess']:.6f}, turnover {metrics['mean_turnover']:.6f})")
            del pred

    nested_pred, nested_stats = build(load(NESTED_MEMBER), load(ORDERERS[0]), dates, flags, codes,
                                      n_codes, WAVE9_ANCHOR["m_frac"])
    nested_metrics, _ = score_official(frame, nested_pred)
    results["nested_hybrid__x__best_orderer__m0.985"] = {
        "member": NESTED_MEMBER, "orderer": ORDERERS[0], "m_frac": WAVE9_ANCHOR["m_frac"],
        "connected_final_score": nested_metrics["final_score"],
        "connected_metrics": nested_metrics,
        "mean_retention_ratio": nested_stats["mean_retention_ratio"], "nested": True}
    cs.log(f"nested check: {nested_metrics['final_score']:.9f} vs the simple pair's "
           f"{results[f'{MEMBER}__x__{ORDERERS[0]}__m0.985']['connected_final_score']:.9f}")

    ranked = sorted(results.items(), key=lambda kv: -kv[1]["connected_final_score"])
    payload = {"status": "complete", "completed_at_local": time.strftime("%Y-%m-%dT%H:%M:%S"),
               "protocol_sha256": sha(HERE / "protocol_wave10.json"),
               "results": results, "best": ranked[0][0],
               "best_connected_final_score": ranked[0][1]["connected_final_score"],
               "confirmed_model_connected": 0.427407938,
               "gain_over_confirmed": ranked[0][1]["connected_final_score"] - 0.427407938,
               "curves": {o: {str(m): results[f"{MEMBER}__x__{o}__m{m:g}"]["connected_final_score"]
                              for m in M_VALUES} for o in ORDERERS},
               "no_test_period_data_read": True}
    (HERE / "wave10_results.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("\n| rank | orderer | m | CONNECTED | IC | excess | turnover | retention |")
    print("|---|---|---|---|---|---|---|---|")
    for i, (name, v) in enumerate(ranked):
        m = v["connected_metrics"]
        print(f"| {i+1} | {v['orderer'].replace('pp::', '').replace('_top_only_w0.25_rl1_tcw1', '')} "
              f"| {v['m_frac']:g} | **{m['final_score']:.9f}** | {m['ic_mean']:.6f} | "
              f"{m['annual_excess']:.6f} | {m['mean_turnover']:.6f} | "
              f"{v['mean_retention_ratio']:.4f} |")
    print(f"\nbest {ranked[0][0]} = {ranked[0][1]['connected_final_score']:.9f}, "
          f"gain over the confirmed model "
          f"{ranked[0][1]['connected_final_score'] - 0.427407938:+.9f}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("stage", choices=("freeze", "run"))
    args = parser.parse_args()
    try:
        globals()[args.stage]()
    except BaseException as error:
        (HERE / f"failure_wave10_{args.stage}_{time.time_ns()}.json").write_text(
            json.dumps({"stage": args.stage, "type": type(error).__name__, "message": str(error),
                        "traceback": traceback.format_exc()}, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8")
        raise
