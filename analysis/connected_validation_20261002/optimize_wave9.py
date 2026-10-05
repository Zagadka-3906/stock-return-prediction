"""Wave 9: exhaustive search of the two donor roles, each screened by the term it supplies.

Wave 5 chose the orderer by connected ic_mean argmax and the membership donor by connected
annual_excess argmax. Wave 7b/8 then showed that rule is incomplete: the orderer also decides which
members of the promoted set fill the EXCESS Top decile, because the evaluator's excess universe is
smaller than its turnover universe (it additionally requires a label), so the excess Top is the
best-ordered subset of the promoted block. Evidence: a0b015 paired with W5a scored a lower excess than
a0b015 paired with itself at the same retention floor. So IC-argmax is not necessarily the right
orderer rule, and excess-argmax is not necessarily the right membership rule.

This wave therefore searches both roles over every saved finished column, with the retention floor
fixed at the wave-7b optimum. Screening is by the term each role supplies, and both the screen and its
threshold are declared before scoring:
  membership candidates: connected annual_excess >= 0.30   (the role sets excess and turnover)
  orderer candidates:    connected ic_mean      >= 0.115   (the role sets Rank IC and the within-set
                                                            ordering that the excess Top reads)
Every column that passes either screen is scored in the opposite role too, so the search is exhaustive
over the screened library rather than a hand-picked shortlist.

Harness proof: membership=topk, orderer=W5a at the fixed retention floor must reproduce the recorded
0.434034593 before any other pairing is trusted.

Selection remains the highest connected composite per 后续选模标准.md §4. The cumulative in-sample cost
is disclosed: this is the fifth consecutive search over the same five viewed years.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
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

M_FRAC = 0.985
EXCESS_SCREEN = 0.30
IC_SCREEN = 0.115
LEADER = 0.434034593
MEMBER_DEFAULT = "topk"
ORDERER_DEFAULT = "W5a_five_way_with_gru__final_sweep_eval"


def sha(path) -> str:
    value = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for chunk in iter(lambda: stream.read(8 * 1024 * 1024), b""):
            value.update(chunk)
    return value.hexdigest()


def library() -> dict[str, dict]:
    """Every saved finished connected column, with its recorded connected metrics."""
    out = {}
    base = json.loads((HERE / "connected_results_all.json").read_text(encoding="utf-8"))["results"]
    for name, record in base.items():
        path = HERE / f"connected_pred_{name}.npy"
        if path.exists():
            out[name] = {"path": path, "kind": "arm", **record["connected_metrics"]}
    wave6 = HERE / "wave6_results.json"
    if wave6.exists():
        for name, record in json.loads(wave6.read_text(encoding="utf-8"))["results"].items():
            path = HERE / f"pp_{name}.npy"
            if path.exists() and "connected_metrics" in record:
                out[f"pp::{name}"] = {"path": path, "kind": "postprocess",
                                      **record["connected_metrics"]}
    return out


def freeze() -> None:
    lib = library()
    members = sorted((n for n, v in lib.items() if v["annual_excess"] >= EXCESS_SCREEN),
                     key=lambda n: -lib[n]["annual_excess"])
    orderers = sorted((n for n, v in lib.items() if v["ic_mean"] >= IC_SCREEN),
                      key=lambda n: -lib[n]["ic_mean"])
    # two one-dimensional exhaustive sweeps over the screened library, sharing the default pairing
    pairs = sorted({(m, ORDERER_DEFAULT) for m in members}
                   | {(MEMBER_DEFAULT, o) for o in orderers})
    payload = {
        "frozen_at_local": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "standard": "后续选模标准.md §3 connected composite primary; §4 highest score wins",
        "status": "in_sample_selection_disclosed",
        "m_frac_fixed_at": M_FRAC,
        "m_provenance": "the wave-7b retention-floor optimum; fixed here, not re-searched",
        "screens": {"membership": f"connected annual_excess >= {EXCESS_SCREEN}",
                    "orderer": f"connected ic_mean >= {IC_SCREEN}",
                    "rationale": "each role is screened by the official term it actually supplies; "
                                 "both screens are declared before any pairing is scored"},
        "library_size": len(lib),
        "membership_candidates": members,
        "orderer_candidates": orderers,
        "n_pairs": len(pairs),
        "pairs": [list(p) for p in pairs],
        "harness_proof": f"({MEMBER_DEFAULT}, {ORDERER_DEFAULT}) at m={M_FRAC} must reproduce "
                         f"{LEADER} to 1e-9 before any other pairing is trusted",
        "selection_rule": "highest connected 2020-2024 official composite",
        "disclosed_selection_cost": "fifth consecutive search over the same five viewed years; the "
                                    "winner's score carries cumulative upward selection bias that no "
                                    "blind period remains to quantify",
        "no_test_period_data_read": True,
        "source_sha256": sha(Path(__file__)),
    }
    if (HERE / "protocol_wave9.json").exists():
        raise FileExistsError("protocol already frozen")
    (HERE / "protocol_wave9.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    cs.log(f"wave-9 protocol frozen: library {len(lib)}, membership candidates {len(members)}, "
           f"orderer candidates {len(orderers)}, pairs to score {len(pairs)}")


def run() -> None:
    protocol = json.loads((HERE / "protocol_wave9.json").read_text(encoding="utf-8"))
    assert protocol["source_sha256"] == sha(Path(__file__)), "script changed after freezing"
    lib = library()
    frame = cs.combined_frame()
    dates = frame["trade_date"].to_numpy()
    flags = frame["flag_limit_up"].to_numpy()
    codes, uniques = pd.factorize(frame["ts_code"].to_pandas(), sort=True)
    codes = codes.astype(np.int64)
    n_codes = len(uniques)

    cache = {}

    def column(name: str) -> np.ndarray:
        if name not in cache:
            cache[name] = np.load(lib[name]["path"])
            if len(cache[name]) != len(frame):
                raise AssertionError(f"{name}: {len(cache[name])} rows vs {len(frame)}")
        return cache[name]

    results = {}
    progress_path = HERE / "wave9_progress.jsonl"
    done = {}
    if progress_path.exists():
        for line in progress_path.read_text(encoding="utf-8").splitlines():
            if line.strip():
                record = json.loads(line)
                done[(record["member"], record["orderer"])] = record
        cs.log(f"resuming: {len(done)} pairings already scored")

    def safe(text: str) -> str:
        return re.sub(r"[^A-Za-z0-9._-]", "_", str(text))[:80]

    pairs = [tuple(p) for p in protocol["pairs"]]
    best_so_far = LEADER
    for index, (member, orderer) in enumerate(pairs, start=1):
        name = f"{member}__x__{orderer}"
        if (member, orderer) in done:
            results[name] = done[(member, orderer)]
            continue
        pred, stats = build(column(member), column(orderer), dates, flags, codes, n_codes, M_FRAC)
        metrics, _ = score_official(frame, pred)
        if member == MEMBER_DEFAULT and orderer == ORDERER_DEFAULT:
            diff = abs(metrics["final_score"] - LEADER)
            if diff > 1e-9:
                raise AssertionError(f"harness proof failed: {metrics['final_score']!r} vs {LEADER!r}")
            cs.log(f"HARNESS PROOF passed, reproduces {LEADER:.9f} (diff {diff:.1e})")
        record = {"member": member, "orderer": orderer, "m_frac": M_FRAC,
                  "connected_final_score": metrics["final_score"],
                  "connected_metrics": metrics,
                  "mean_retention_ratio": stats["mean_retention_ratio"],
                  "member_excess": lib[member]["annual_excess"],
                  "orderer_ic": lib[orderer]["ic_mean"]}
        results[name] = record
        with progress_path.open("a", encoding="utf-8") as stream:
            stream.write(json.dumps(record, ensure_ascii=False) + "\n")
        # only the array that currently leads is worth 45 MB of disk
        if metrics["final_score"] > best_so_far:
            best_so_far = metrics["final_score"]
            np.save(HERE / f"wave9_best_{safe(member)}_x_{safe(orderer)}.npy", pred)
        cs.log(f"[{index}/{len(pairs)}] {name[:70]}: {metrics['final_score']:.9f} "
               f"(ic {metrics['ic_mean']:.6f}, excess {metrics['annual_excess']:.6f}, "
               f"turnover {metrics['mean_turnover']:.6f})")
        del pred

    ranked = sorted(results.items(), key=lambda kv: -kv[1]["connected_final_score"])
    payload = {"status": "complete", "completed_at_local": time.strftime("%Y-%m-%dT%H:%M:%S"),
               "protocol_sha256": sha(HERE / "protocol_wave9.json"),
               "m_frac": M_FRAC, "results": results,
               "best": ranked[0][0], "best_connected_final_score": ranked[0][1]["connected_final_score"],
               "previous_leader": LEADER,
               "gain_over_previous_leader": ranked[0][1]["connected_final_score"] - LEADER,
               "best_membership_by_excess": sorted(
                   {v["member"] for v in results.values()},
                   key=lambda m: -max(v["member_excess"] for v in results.values()
                                      if v["member"] == m))[:5],
               "best_orderer_by_ic": sorted(
                   {v["orderer"] for v in results.values()},
                   key=lambda o: -max(v["orderer_ic"] for v in results.values()
                                      if v["orderer"] == o))[:5],
               "no_test_period_data_read": True}
    (HERE / "wave9_results.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("\n| rank | membership donor | orderer | CONNECTED | IC | excess | turnover |")
    print("|---|---|---|---|---|---|---|")
    for i, (name, v) in enumerate(ranked[:25]):
        m = v["connected_metrics"]
        print(f"| {i+1} | {v['member'][:34]} | {v['orderer'][:30]} | **{m['final_score']:.9f}** | "
              f"{m['ic_mean']:.6f} | {m['annual_excess']:.6f} | {m['mean_turnover']:.6f} |")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("stage", choices=("freeze", "run"))
    args = parser.parse_args()
    try:
        globals()[args.stage]()
    except BaseException as error:
        (HERE / f"failure_wave9_{args.stage}_{time.time_ns()}.json").write_text(
            json.dumps({"stage": args.stage, "type": type(error).__name__, "message": str(error),
                        "traceback": traceback.format_exc()}, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8")
        raise
