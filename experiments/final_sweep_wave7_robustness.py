"""Wave 7: is the surviving ensemble robust to its own composition?

W3e passed the three-year gate, but the wave-3 record shows the result is not
obviously insensitive to membership: dropping the pruned-feature member (W3d)
swings 2024 from +0.001341 to -0.000105. Before anyone adopts a four-member
average, it is worth knowing whether the advantage belongs to the ensemble or to
one load-bearing member.

This stage answers that question **only on 2020 and 2021** - the years no
adoption gate has ever scored - so it adds no selection pressure to the gated
years and cannot make the existing W3e result look better than it is. Every
three-member subset is built from the same byte-pinned caches and scored through
the same anchored replica, in the same no-blend caliber as the recorded audit.

It is a robustness diagnostic, not a gate. Nothing here is adoptable: choosing a
subset instead of W3e would require a fresh protocol scored on the gated years.
"""
from __future__ import annotations

import argparse
import json
import time
from pathlib import Path

import numpy as np
import polars as pl

from src.scoring import Panel
from experiments.bonus_extension import file_hash
from experiments.extended_audit import audit_score
from experiments.final_sweep_wave3 import ensemble_raw
from experiments.final_sweep_wave5 import AUDIT, AUDIT_YEARS, OUT, log, panel_frame
from experiments.final_sweep_wave5_score import released_stack

FULL = ("released_lgb", "T2f_xgboost_backbone", "W2c_two_day_horizon", "W2d_pruned_features")
SUBSETS = [tuple(m for m in FULL if m != dropped) for dropped in FULL]
DROPPED = {subset: next(m for m in FULL if m not in subset) for subset in map(tuple, SUBSETS)}
NUMERIC_TOLERANCE = 1e-12
PRIOR_AUDIT = {"released_lgb_backbone": (0.426786643, 0.418405538)}

PROTOCOL = {
    "experiment": "wave7_member_dropout_robustness_on_audit_years_only",
    "question": "Does the surviving four-member ensemble's advantage on never-gated years depend on "
                "one load-bearing member, or is it a property of the ensemble?",
    "full_member_set": list(FULL),
    "subsets": [list(s) for s in SUBSETS],
    "years": list(AUDIT_YEARS),
    "gated_years_scored": "none; 2022, 2023 and 2024 are deliberately not touched by this stage",
    "ensemble_rule": "imported unchanged from the frozen wave-3 module: equal-weight mean of the "
                     "members' cross-sectional average ranks over price-valid rows finite in every "
                     "member, sentinel -10.0 elsewhere",
    "member_caches": "trees from extended_audit_eval/{key}_{year}.parquet, released backbone from "
                     "the audit fold panel's own pred_raw column; both byte-pinned by the recorded "
                     "extended-year audit",
    "scorer": "the anchored audit replica over the unmodified evaluate.py, released stack without "
              "the pooled blend, identical for baseline and every subset",
    "baseline_anchor": "the released backbone must reproduce the recorded audit composites "
                       "0.426786643 (2020) and 0.418405538 (2021) to 1e-12",
    "status": "robustness diagnostic only; no subset is adoptable without a fresh protocol",
    "prohibited_after_results": [
        "Scoring any subset on a gated year under this protocol",
        "Adding subsets, weights or years",
        "Adopting a subset in place of W3e",
    ],
    "limitations": [
        "2020 and 2021 have already been used once, to corroborate W3e and T2f, so they are not "
        "pristine; they are simply the least-examined years available.",
        "Two years and four subsets cannot distinguish a robust ensemble from a lucky one; they can "
        "only show whether the sign and rough magnitude survive member dropout.",
    ],
}


def write_protocol() -> None:
    path = OUT / "protocol_wave7.json"
    if path.exists():
        raise SystemExit("Wave-7 protocol already frozen")
    payload = {**PROTOCOL, "frozen_at_local": time.strftime("%Y-%m-%dT%H:%M:%S"),
               "source_sha256": file_hash(Path(__file__))}
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    log("Froze wave-7 protocol before any scoring")


def verify_protocol() -> dict:
    protocol = json.loads((OUT / "protocol_wave7.json").read_text(encoding="utf-8"))
    if protocol["source_sha256"] != file_hash(Path(__file__)):
        raise SystemExit("final_sweep_wave7_robustness.py changed after its protocol was frozen")
    return protocol


def member_raws(year: int, frame: pl.DataFrame) -> dict:
    raws = {"released_lgb": frame["pred_raw"].to_numpy().astype(np.float64)}
    for name in FULL[1:]:
        path = AUDIT / f"{name}_{year}.parquet"
        if not path.exists():
            raise SystemExit(f"Missing audit member cache {path}")
        cache = pl.read_parquet(path).sort("trade_date", "ts_code")
        if not cache.select(["ts_code", "trade_date"]).equals(frame.select(["ts_code", "trade_date"])):
            raise AssertionError(f"{name} {year}: cache keys misaligned with the audit fold")
        raws[name] = cache["pred_raw"].to_numpy().astype(np.float64)
    return raws


def run() -> None:
    protocol = verify_protocol()
    result_path = OUT / "robustness_wave7.json"
    if result_path.exists():
        raise SystemExit("Wave-7 robustness results already recorded; preserving them")
    started = time.monotonic()
    results = {"years": {}}
    for position, year in enumerate(AUDIT_YEARS):
        frame = panel_frame(year)
        panel = Panel.from_frame(frame)
        raws = member_raws(year, frame)
        baseline, _ = audit_score(panel, released_stack(panel, raws["released_lgb"], None), year)
        expected = PRIOR_AUDIT["released_lgb_backbone"][position]
        if abs(baseline["final_score"] - expected) > 1e-9:
            raise AssertionError(f"{year} audit baseline differs from the recorded audit run")
        log(f"{year} baseline anchor reproduced {expected:.9f}")
        entries = {"released_lgb_backbone": {k: float(v) for k, v in baseline.items()}}
        for subset in SUBSETS:
            weights = {name: 1.0 for name in subset}
            raw = ensemble_raw(panel, weights, raws)
            prediction = released_stack(panel, raw, None)
            metrics, daily = audit_score(panel, prediction, year)
            key = "drop_" + DROPPED[tuple(subset)]
            daily.write_csv(OUT / f"W7_{key}_{year}_daily.csv")
            entries[key] = {**{k: float(v) for k, v in metrics.items()},
                            "members": list(subset),
                            "delta_vs_released": float(metrics["final_score"]) - baseline["final_score"]}
            log(f"{year} {key}: score={metrics['final_score']:.9f} ic={metrics['ic_mean']:.6f} "
                f"delta={entries[key]['delta_vs_released']:+.9f}")
        results["years"][str(year)] = entries
        del panel, frame, raws
    full_reference = json.loads((AUDIT.parent / "extended_audit_eval" / "audit_results.json")
                                .read_text(encoding="utf-8"))
    summary = {}
    for subset in SUBSETS:
        key = "drop_" + DROPPED[tuple(subset)]
        deltas = [results["years"][str(y)][key]["delta_vs_released"] for y in AUDIT_YEARS]
        w3e = [full_reference["years"][str(y)]["W3e_lgb_xgb_twoday_pruned"]["delta_vs_released"]
               for y in AUDIT_YEARS]
        summary[key] = {"members": list(subset), "deltas": deltas,
                        "mean_delta": sum(deltas) / len(deltas),
                        "w3e_deltas": w3e, "w3e_mean_delta": sum(w3e) / len(w3e),
                        "positive_both_years": all(d > 0 for d in deltas),
                        "retains_w3e_advantage": all(d > 0 for d in deltas)}
    spread = [item["mean_delta"] for item in summary.values()]
    output = {"stage": "robustness_wave7", "generated_at_local": time.strftime("%Y-%m-%dT%H:%M:%S"),
              "elapsed_seconds": time.monotonic() - started,
              "protocol_sha256": file_hash(OUT / "protocol_wave7.json"),
              "results": results, "summary": summary,
              "subset_mean_spread": {"min": min(spread), "max": max(spread),
                                     "range": max(spread) - min(spread)},
              "status": protocol["status"], "caveat": protocol["limitations"]}
    result_path.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")
    log(f"WAVE-7 ROBUSTNESS: subset mean deltas span "
        f"{min(spread):+.6f} to {max(spread):+.6f}; all positive = "
        f"{all(item['positive_both_years'] for item in summary.values())}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("stage", choices=("protocol", "run"))
    arguments = parser.parse_args()
    if arguments.stage == "protocol":
        write_protocol()
    else:
        run()
