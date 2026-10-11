"""Final sweep, wave 8: the two levers no earlier suite touched.

Every mechanism class tested so far is closed with a frozen negative record, and
the adopted release changed the baseline. Two questions remain genuinely open,
both cheap because every member cache already exists for all five years:

  Suite A - the combination RULE. W3e averages the four members' cross-sectional
  ranks. Averaging per-day z-scores instead weights members by magnitude rather
  than by order, and a trimmed mean (drop each member's highest and lowest daily
  rank per observation, average the middle two) down-weights a dissenting member.
  Neither has ever been scored. Suite A is scored through the standing gate and,
  if it passes, audited on 2020/2021, which were never used to choose a rule.

  Suite B - post-processing re-selected FOR the ensemble. The released alpha 0.9
  and bonus 0.3 were tuned against the old single-model backbone; the ensemble's
  raw signal is smoother and stronger, so its own optimum may differ. A 3x3 grid
  is selected by maximin on 2020+2021 (no-blend caliber) BEFORE any gated year is
  touched, and only the single winner is then scored on 2022/2023 and, if it
  passes, once on 2024. Suite B deliberately gets NO audit: its selection years
  are 2020/2021, so auditing it there would be circular. If the winner is the
  released pair (0.9, 0.3) the suite records "keep as is" and scores nothing.

Both suites compare against the recorded W3e numbers as a reference; W3e itself
is not re-scored.
"""
from __future__ import annotations

import argparse
import json
import time
from pathlib import Path

import numpy as np
import polars as pl

from run import ROOT
from experiments.bonus_extension import file_hash
from experiments.final_sweep_wave5 import ALL_YEARS, OUT, log, member_raws, panel_frame

SCORED_YEARS = (2022, 2023, 2024)
AUDIT_YEARS = (2020, 2021)
DEVELOPMENT_YEARS = (2022, 2023)
DIAGNOSTIC_YEAR = 2024
SENTINEL = -1e6
REFERENCE = "W3e_lgb_xgb_twoday_pruned"

RULE_CANDIDATES = [
    {"key": "W8a_zscore_mean", "primary": True, "rule": "zscore",
     "note": "per day, each member centered and scaled by its cross-sectional mean/std over "
             "price-valid rows, then equal-weight mean"},
    {"key": "W8b_trimmed_mean", "primary": False, "rule": "trimmed",
     "note": "per observation, drop the highest and lowest of the four members' daily ranks and "
             "average the middle two"},
]
GRID = [{"alpha": a, "bonus": b} for a in (0.85, 0.90, 0.95) for b in (0.2, 0.3, 0.4)]
RELEASED_PP = {"alpha": 0.9, "bonus": 0.3}
W3E_KEY = "W3e_rank_average"
W3E_PINNED = "W3e_lgb_xgb_twoday_pruned"
W3E_MEMBERS = {"released_lgb": 1.0, "T2f_xgboost_backbone": 1.0, "W2c_two_day_horizon": 1.0,
               "W2d_pruned_features": 1.0}
KEYS = ["ts_code", "trade_date"]

PROTOCOL = {
    "experiment": "final_sweep_wave8_combination_rule_and_ensemble_postprocess",
    "rule_candidates": RULE_CANDIDATES,
    "postprocess_grid": GRID,
    "selection_years": list(AUDIT_YEARS),
    "selection_rule": "suite B only: score all nine (alpha, bonus) pairs on 2020 and 2021 in the "
                      "no-blend caliber on the materialized W3e raw, and take the pair maximizing "
                      "min over the two years of (composite minus the W3e composite at the released "
                      "pair 0.9/0.3 in the same caliber); ties broken toward (0.9, 0.3). The winner "
                      "is fixed and written to disk before any gated year is scored.",
    "development_years": list(DEVELOPMENT_YEARS),
    "diagnostic_year": DIAGNOSTIC_YEAR,
    "adoption_gate": "strictly positive composite delta against BOTH comparators in 2022 AND 2023, "
                     "then once in 2024: (i) the pooled_rms25 released composite, the historical "
                     "anchor used by every earlier suite, and (ii) the recorded W3e composite, which "
                     "is the currently adopted release. Beating (ii) is the decision-relevant test; "
                     "(i) is kept so wave-8 rows stay comparable with waves 1-7.",
    "comparators": {
        "released_backbone": "validation/metrics.json via release_scores(), reproduced in-process to "
                             "1e-12 in every scored year",
        "w3e": "the recorded W3e composites: development_wave3.json (2022, 2023), "
               "confirmation_wave3.json (2024) and extended_audit_eval/audit_results.json (2020, "
               "2021); W3e is never re-scored, only re-materialized as a raw signal",
    },
    "reference": "W3e as recorded in development_wave3.json / confirmation_wave3.json and the "
                 "extended-year audit; not re-scored here",
    "reference_raw": f"the W3e rank average is re-materialized for all five years as "
                     f"{W3E_KEY}_{{year}}.parquet through the frozen wave-3 ensemble_raw and the "
                     f"frozen member weights {W3E_MEMBERS}; for 2022-2024 the recomputed array must "
                     f"equal the pinned {W3E_PINNED}_{{year}}.parquet cache element for element, "
                     f"which is the proof that suite B perturbs only alpha and bonus",
    "suite_b_has_no_audit": "its selection years are 2020/2021, so an audit there would be circular",
    "postprocess": "released stack: alpha EMA on daily percentile ranks, persistence bonus, "
                   "protected-block restoration at top_current_weight 1.0, then the 25% top-only "
                   "pooled blend for 2022-2024; blend disabled for 2020-2021, identically for "
                   "baseline and candidate",
    "scorer": "the unmodified evaluate.py via official_score for 2022-2024 and via the anchored "
              "audit replica for 2020-2021",
    "baseline_anchor": "in 2022-2024 the released backbone through the same code path reproduces the "
                       "released composite to 1e-12; in 2020-2021 both the released backbone and the "
                       "materialized W3e raw at (0.9, 0.3) reproduce audit_results.json to 1e-12",
    "stages": {
        "select": "suite B winner on 2020+2021, written before any gated year is touched",
        "develop": "2022 and 2023, full released stack with the pooled blend, for W8a, W8b and the "
                   "suite-B winner if it differs from (0.9, 0.3)",
        "confirm": "2024 once, only for candidates that passed develop",
        "audit": "2020 and 2021, no blend, only for suite-A candidates that passed all three gated "
                 "years; suite B is excluded by protocol",
    },
    "retraining": "none; all members are byte-pinned caches",
    "prohibited_after_results": [
        "Adding rules, grid points or years",
        "Re-selecting the post-processing winner on a gated year",
        "Auditing suite B on its own selection years",
        "Adopting a diagnostic rule without a fresh protocol",
        "Re-scoring years or modifying the release",
    ],
    "limitations": [
        "2022-2024 have been examined by eight earlier suites; a pass is evidence against a fluke, "
        "not proof of out-of-sample edge.",
        "Suite A's rules are compared against W3e on the same gated years, so the family-wise "
        "selection pressure keeps growing; the audit years are the only freshness left.",
        "The pooled auxiliary is unchanged and Top-set inert, so it cannot interact with either "
        "suite.",
    ],
}


def zscore_mean(raws: list[np.ndarray], valid: np.ndarray) -> np.ndarray:
    shape = valid.shape
    arrays = [np.asarray(r, dtype=np.float64).reshape(shape) for r in raws]
    out = np.full(shape, SENTINEL, dtype=np.float64)
    for day in range(shape[0]):
        keep = valid[day]
        count = int(keep.sum())
        if not count:
            continue
        mixed = np.zeros(count, dtype=np.float64)
        used = 0
        for array in arrays:
            column = array[day][keep]
            std = float(np.nanstd(column))
            if not np.isfinite(std) or std == 0.0:
                continue
            mixed += (column - float(np.nanmean(column))) / std
            used += 1
        if used:
            out[day][keep] = mixed / used
    return out.reshape(-1)


def trimmed_mean(raws: list[np.ndarray], valid: np.ndarray) -> np.ndarray:
    from scipy.stats import rankdata

    shape = valid.shape
    arrays = [np.asarray(r, dtype=np.float64).reshape(shape) for r in raws]
    ranks = np.empty((len(arrays),) + shape, dtype=np.float64)
    for index, array in enumerate(arrays):
        ranks[index] = np.where(valid, np.nan, np.nan)
        for day in range(shape[0]):
            keep = valid[day]
            count = int(keep.sum())
            if count:
                ranks[index][day][keep] = rankdata(array[day][keep], method="average") / count
    ordered = np.sort(ranks, axis=0)
    middle = ordered[1:-1] if ranks.shape[0] >= 4 else ordered
    out = np.where(valid, np.nanmean(middle, axis=0), SENTINEL)
    return np.where(np.isfinite(out), out, SENTINEL).reshape(-1)


def write_protocol() -> None:
    path = OUT / "protocol_wave8.json"
    if path.exists():
        raise SystemExit("Wave-8 protocol already frozen")
    payload = {**PROTOCOL, "frozen_at_local": time.strftime("%Y-%m-%dT%H:%M:%S"),
               "source_sha256": file_hash(Path(__file__))}
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    log("Froze wave-8 protocol before any scoring")


def verify_protocol() -> dict:
    protocol = json.loads((OUT / "protocol_wave8.json").read_text(encoding="utf-8"))
    if protocol["source_sha256"] != file_hash(Path(__file__)):
        raise SystemExit("final_sweep_wave8.py changed after its protocol was frozen; stop")
    return protocol


def build() -> None:
    verify_protocol()
    result_path = OUT / "training_wave8.json"
    if result_path.exists():
        raise SystemExit("Wave-8 caches already built; preserving them")
    from src.scoring import Panel
    from experiments.final_sweep_wave3 import ensemble_raw

    started = time.monotonic()
    record = {"generated_at_local": time.strftime("%Y-%m-%dT%H:%M:%S"),
              "protocol_sha256": file_hash(OUT / "protocol_wave8.json"),
              "w3e_members": W3E_MEMBERS, "caches": {}, "w3e_reproduction": {}}
    for year in ALL_YEARS:
        frame = panel_frame(year)
        raws_dict, _ = member_raws(year, frame)
        panel = Panel.from_frame(frame)

        reference = ensemble_raw(panel, W3E_MEMBERS, raws_dict)
        path = OUT / f"{W3E_KEY}_{year}.parquet"
        frame.select(KEYS).with_columns(
            pl.Series("pred_raw", reference)).write_parquet(path, compression="zstd")
        record["caches"].setdefault(str(year), {})[W3E_KEY] = {
            "path": path.name, "sha256": file_hash(path),
            "sentinel_rows": int((reference == -10.0).sum())}
        proof = {"materialized": True}
        if year in SCORED_YEARS:
            pinned = (pl.read_parquet(OUT / f"{W3E_PINNED}_{year}.parquet")
                      .sort("trade_date", "ts_code"))
            if not pinned.select(KEYS).equals(frame.select(KEYS)):
                raise AssertionError(f"{year}: pinned W3e cache keys misaligned with the panel")
            identical = bool(np.array_equal(pinned["pred_raw"].to_numpy().astype(np.float64),
                                            reference))
            proof["pinned_cache"] = f"{W3E_PINNED}_{year}.parquet"
            proof["elementwise_identical"] = identical
            if not identical:
                raise AssertionError(f"{year}: recomputed W3e raw differs from the pinned cache")
            log(f"{year} W3e reference reproduced the pinned cache element for element")
        record["w3e_reproduction"][str(year)] = proof

        raws = [raws_dict[name] for name in W3E_MEMBERS]
        for candidate in RULE_CANDIDATES:
            raw = (zscore_mean(raws, panel.valid_price) if candidate["rule"] == "zscore"
                   else trimmed_mean(raws, panel.valid_price))
            path = OUT / f"{candidate['key']}_{year}.parquet"
            frame.select(KEYS).with_columns(
                pl.Series("pred_raw", raw)).write_parquet(path, compression="zstd")
            record["caches"].setdefault(str(year), {})[candidate["key"]] = {
                "path": path.name, "sha256": file_hash(path),
                "sentinel_rows": int((raw == SENTINEL).sum())}
            log(f"{candidate['key']} {year}: built ({int((raw == SENTINEL).sum()):,} sentinel rows)")
        del panel, frame, raws, raws_dict, reference
    record["elapsed_seconds"] = time.monotonic() - started
    result_path.write_text(json.dumps(record, ensure_ascii=False, indent=2), encoding="utf-8")
    log(f"Wrote {result_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("stage", choices=("protocol", "build"))
    arguments = parser.parse_args()
    if arguments.stage == "protocol":
        write_protocol()
    else:
        build()
