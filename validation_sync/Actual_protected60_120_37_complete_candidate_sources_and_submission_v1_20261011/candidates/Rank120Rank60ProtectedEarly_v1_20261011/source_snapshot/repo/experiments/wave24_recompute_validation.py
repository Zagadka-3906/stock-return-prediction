"""Wave-24 stage 1: independently recompute the ABSOLUTE per-year official scores of the
sixteen-seed peer67+slow ensemble and of the deployed eight-seed ensemble.

wave-23 stored only `delivered8_metrics` plus sixteen-seed DELTAS against the base-63 control arm;
the absolute sixteen-seed numbers live in analysis/model_comparison_20260928/late_inventory.json.
This stage rebuilds both from wave-23's 80 cached raw prediction frames and scores them through
`revalidate_fold_local.score_official`, which calls the unmodified evaluate.py. No model is refit
and no reduced scoring pipeline is used.

Gates: g1 anchor, g2 delivered8 reproduction (1e-12), g3 full16 reproduction (2e-9), g4 premise.
Writes only inside experiments/wave24_seed16_delivery_20260929/.
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import numpy as np
import polars as pl

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from experiments.revalidate_fold_local import score_official          # noqa: E402
from experiments import wave9_exploratory as w9                        # noqa: E402
from experiments import wave14_seed_average as w14                     # noqa: E402
from experiments import wave21_peer_lags as w21                        # noqa: E402
from experiments import wave23_validation as w23                       # noqa: E402
from experiments import wave24_validation_config as w24                   # noqa: E402

OUT = w24.OUT
CACHE = ROOT / "experiments" / "wave23_validation_20260928"
KEYS = ["ts_code", "trade_date"]
TOL8 = w24.EXPECTED_DELIVERED8_TOLERANCE
TOL16 = w24.EXPECTED_FULL16_TOLERANCE


def log(message: str) -> None:
    print(f"[{time.strftime('%H:%M:%S')}] {message}", flush=True)


def load_raw(seed: int, year: int) -> np.ndarray:
    path = CACHE / f"raw_deployed67_slow_seed{seed}_{year}.parquet"
    if not path.exists():
        raise SystemExit(f"missing wave-23 cached raw: {path.name}")
    return pl.read_parquet(path).sort("trade_date", "ts_code")["pred_raw"].to_numpy()


def run_year(year: int) -> dict:
    started = time.monotonic()
    w9.OUT = OUT
    w23.OUT = OUT
    bundle = w21.fold(year)

    # g1: the frozen reference composite must reproduce exactly before anything is combined.
    reference = w9.reference_metrics("xgboost", year)
    frozen_frame = pl.read_parquet(
        w9.REFERENCES["xgboost"]["predictions"] / f"predictions_xgboost_{year}.parquet"
    ).sort("trade_date", "ts_code")
    check, _ = score_official(bundle["frame"], frozen_frame["pred"].to_numpy().astype(np.float64))
    anchor = max(abs(check[k] - reference[k]) for k in reference)
    if anchor > 1e-12:
        raise AssertionError(f"{year}: g1 FAILED, frozen anchor off by {anchor:.3e}")
    log(f"{year} g1 anchor reproduced {reference['final_score']:.15f} (max diff {anchor:.1e})")

    valid = bundle["valid"]["price_valid"].to_numpy()
    days = bundle["valid"]["trade_date"].n_unique()
    codes = len(valid) // days
    w14.combination_proof(bundle, codes)

    raws = {seed: load_raw(seed, year) for seed in w24.POOL16}

    def score(seeds: tuple[int, ...], daily_name: str | None):
        averaged = w14.rank_average_n([raws[s] for s in seeds], valid, codes)
        metrics, daily = score_official(bundle["frame"], w14.stacked(bundle, averaged))
        if daily_name:
            daily.write_csv(OUT / f"daily_{daily_name}_{year}.csv")
        return metrics

    delivered8 = score(w24.DELIVERED, "delivered8")
    full16 = score(w24.POOL16, "full16")

    exp8 = w24.EXPECTED_DELIVERED8[str(year)] if str(year) in w24.EXPECTED_DELIVERED8 \
        else w24.EXPECTED_DELIVERED8[year]
    exp16 = w24.EXPECTED_FULL16[str(year)] if str(year) in w24.EXPECTED_FULL16 \
        else w24.EXPECTED_FULL16[year]
    diff8 = abs(delivered8["final_score"] - exp8)
    diff16 = abs(full16["final_score"] - exp16)
    if diff8 > TOL8:
        raise AssertionError(f"{year}: g2 FAILED, delivered8 off by {diff8:.3e} > {TOL8:.0e}")
    if diff16 > TOL16:
        raise AssertionError(f"{year}: g3 FAILED, full16 off by {diff16:.3e} > {TOL16:.0e}")
    log(f"{year} g2 delivered8 {delivered8['final_score']:.12f} (diff {diff8:.1e}) | "
        f"g3 full16 {full16['final_score']:.12f} (diff {diff16:.1e})")

    record = {"year": year, "days": int(days), "codes": int(codes),
              "anchor_max_abs_diff": float(anchor),
              "anchor_reference_final_score": float(reference["final_score"]),
              "delivered8_metrics": delivered8, "full16_metrics": full16,
              "gates": {"g1_anchor": True, "g2_delivered8_reproduction": True,
                        "g3_full16_reproduction": True},
              "reproduction_diff": {"delivered8": float(diff8), "full16": float(diff16)},
              "seconds": round(time.monotonic() - started, 1)}
    (OUT / f"validation_year_{year}.json").write_text(
        json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return record


def summarise() -> None:
    records = []
    for year in w24.VALIDATION_YEARS:
        path = OUT / f"validation_year_{year}.json"
        if not path.exists():
            raise SystemExit(f"{year} not recomputed yet")
        records.append(json.loads(path.read_text(encoding="utf-8")))
    eight = [r["delivered8_metrics"]["final_score"] for r in records]
    sixteen = [r["full16_metrics"]["final_score"] for r in records]
    mean8, mean16 = float(np.mean(eight)), float(np.mean(sixteen))
    premise = mean16 > mean8

    def stats(values):
        return {"per_year": values, "five_year_mean": float(np.mean(values)),
                "worst_year": float(np.min(values)),
                "worst_year_index": int(np.argmin(values)),
                "worst_year_name": w24.VALIDATION_YEARS[int(np.argmin(values))],
                "year_sd": float(np.std(values, ddof=1))}

    paired = [b - a for a, b in zip(eight, sixteen)]
    summary = {
        "status": "complete",
        "completed_at_local": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "protocol_sha256": w24.sha(OUT / "protocol.json"),
        "scorer": "revalidate_fold_local.score_official -> unmodified evaluate.py",
        "delivered8": stats(eight), "full16": stats(sixteen),
        "sixteen_minus_eight": {"per_year": paired, "five_year_mean": float(np.mean(paired)),
                                "years_positive": int(sum(1 for p in paired if p > 0)),
                                "worst_year_comparison": {
                                    "delivered8": float(np.min(eight)),
                                    "full16": float(np.min(sixteen)),
                                    "full16_minus_delivered8": float(np.min(sixteen) - np.min(eight))}},
        "gates": {"g1_anchor": all(r["gates"]["g1_anchor"] for r in records),
                  "g2_delivered8_reproduction": all(r["gates"]["g2_delivered8_reproduction"]
                                                    for r in records),
                  "g3_full16_reproduction": all(r["gates"]["g3_full16_reproduction"]
                                                for r in records),
                  "g4_premise": bool(premise)},
        "max_reproduction_diff": {
            "delivered8": max(r["reproduction_diff"]["delivered8"] for r in records),
            "full16": max(r["reproduction_diff"]["full16"] for r in records)},
        "g4_note": "g4 is a premise check on an already-viewed number, not a blind test; see "
                   "protocol.json.disclosure",
    }
    if not summary["gates"]["g4_premise"]:
        summary["action"] = "STOP: the sixteen-seed arm does not exceed the deployed eight-seed arm"
    (OUT / "validation_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    stage = sys.argv[1] if len(sys.argv) > 1 else "all"
    if stage == "summarise":
        summarise()
    else:
        years = ([int(stage)] if stage.isdigit() else w24.VALIDATION_YEARS)
        for year in years:
            path = OUT / f"validation_year_{year}.json"
            if path.exists():
                log(f"{year} already recomputed; preserving it")
                continue
            run_year(year)
        summarise()
