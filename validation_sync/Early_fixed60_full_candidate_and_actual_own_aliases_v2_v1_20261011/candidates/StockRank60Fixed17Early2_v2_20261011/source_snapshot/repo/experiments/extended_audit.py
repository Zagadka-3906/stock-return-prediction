"""Extended-year audit of the surviving ensemble on years no gate has ever seen.

Why this exists. Twenty-seven candidates were scored on 2022-2024 under frozen
protocols, and two survived the three-year gate: the XGBoost backbone (T2f) and
the four-way cross-family rank average (W3e). W3e was a pre-declared diagnostic
rather than the primary candidate of its suite, so its survival is partly a
selection effect over five ensemble variants examined on the same two development
years. The only way to test that honestly is new years.

2020 and 2021 have never been scored by any suite in this project. Every member
is retrained for those years by importing the frozen training modules unchanged
and redirecting only their output directories and year lists, so the audit
reuses the exact frozen member definitions instead of reimplementing them. The
harness proves itself first: it rebuilds the released 2022 fold and the pinned
2022/2024 member caches and requires bit-identical predictions.

Scoring caliber. The pooled auxiliary exists only for 2022-2024, so audit years
are scored with the released stack minus the final 25% blend. That blend is
provably Top-set inert (it never changes which names are selected, so turnover
and excess are untouched and only within-block ordering moves IC), and it is
disabled identically for the baseline and every candidate, so the comparison
stays like-for-like. The 2022 anchor is still run through the full released
stack, auxiliary included, and must reproduce the released composite exactly.
"""
from __future__ import annotations

import argparse
import json
import shutil
import tempfile
import time
from pathlib import Path

import numpy as np
import polars as pl

import run as run_module
from evaluate import evaluate
from run import ROOT
from src.scoring import Panel, restore_lower_ranks
from experiments import final_sweep_extra as extra
from experiments import final_sweep_wave2 as wave2
from experiments.bonus_extension import (BASE_BONUS, BLEND_WEIGHT, file_hash, load_auxiliary,
                                         load_panel)
from experiments.final_sweep import blend_top_only, retention_scores, RELEASED
from experiments.final_sweep_wave3 import ensemble_raw
from experiments.official_seed_development import _same_csv_daily, official_score, original_labels

OUT = ROOT / "experiments" / "extended_audit_eval"
FOLDS = OUT / "folds"
MODELS = OUT / "models"
SWEEP = ROOT / "experiments" / "final_sweep_eval"
KEYS = ["ts_code", "trade_date"]
AUDIT_YEARS = (2020, 2021)
REPRODUCTION_YEAR = 2022
PRIMARY = "W3e_lgb_xgb_twoday_pruned"
MEMBER_KEYS = ["T2f_xgboost_backbone", "W2c_two_day_horizon", "W2d_pruned_features"]
NUMERIC_TOLERANCE = 1e-12
RELEASED_2022 = 0.441791933639702

PROTOCOL = {
    "experiment": "extended_year_audit_of_surviving_candidates",
    "audit_years": list(AUDIT_YEARS),
    "reproduction_year": REPRODUCTION_YEAR,
    "question": "Does the surviving ensemble still beat the released backbone on years that no "
                "adoption gate has ever examined?",
    "candidates": [
        {"key": "released_lgb_backbone", "role": "baseline"},
        {"key": "T2f_xgboost_backbone", "role": "three-year survivor, single family"},
        {"key": PRIMARY, "role": "three-year survivor, four-way cross-family rank average"},
    ],
    "ensemble_rule": "imported unchanged from the frozen wave-3 module: per day, over rows "
                     "price-valid and finite in every member, the weighted mean of each member's "
                     "cross-sectional average rank divided by the day's member count, sentinel "
                     "-10.0 elsewhere; weights for W3e are all 1.0",
    "member_definitions": "retrained by calling the frozen final_sweep_extra and "
                          "final_sweep_wave2 training code with only their output directory and "
                          "year list redirected; no rule, parameter, feature set or label changed",
    "released_fold": "run.train_fold(year, 180, 16) with run.VAL_DIR and run.MODEL_DIR redirected "
                     "into this experiment's directories; the pinned validation/ and models/ trees "
                     "are never written",
    "postprocess": "released stack: alpha 0.9, bonus 0.3, protected-block restoration with "
                   "top_current_weight 1.0; the final 25% pooled blend is disabled in audit years "
                   "because the auxiliary cache exists only for 2022-2024",
    "scorer": "the unmodified evaluate.py, invoked through a replica of official_score's "
              "float-17 CSV round trip; the replica is anchored on 2022 against official_score "
              "with the full released stack",
    "harness_proof": [
        "the rebuilt 2022 released fold must equal validation/fold_2022.parquet bit-for-bit",
        "the rebuilt 2022 XGBoost cache must equal the pinned T2f cache bit-for-bit",
        "the rebuilt 2024 two-day and pruned caches must equal their pinned versions bit-for-bit",
        "the replica scorer must reproduce the released 2022 composite to 1e-12",
    ],
    "adoption_rule": "evidence only; this stage adopts nothing. A candidate is called consistent "
                     "when its composite exceeds the released backbone in both audit years.",
    "prohibited_after_results": [
        "Adding audit years after seeing a result",
        "Changing the ensemble, the post-processing or the scorer",
        "Treating an audit outcome as a new gate to be optimized against",
    ],
    "limitations": [
        "Audit years are scored without the pooled blend, so absolute composites are not directly "
        "comparable with the released 2022-2024 numbers; only same-year differences are.",
        "2020 and 2021 have less training history than the scored years, so all backbones are "
        "weaker there than in 2022-2024.",
    ],
}


def log(message: str) -> None:
    print(f"[{time.strftime('%H:%M:%S')}] {message}", flush=True)


def write_protocol() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / "protocol_audit.json"
    if path.exists():
        raise SystemExit("Audit protocol already frozen")
    payload = {**PROTOCOL, "frozen_at_local": time.strftime("%Y-%m-%dT%H:%M:%S"),
               "source_sha256": file_hash(Path(__file__)),
               "pinned_modules": {name: file_hash(ROOT / name) for name in
                                  ("run.py", "evaluate.py", "src/scoring.py",
                                   "experiments/final_sweep_extra.py",
                                   "experiments/final_sweep_wave2.py",
                                   "experiments/final_sweep_wave3.py",
                                   "experiments/official_seed_development.py")},
               "pinned_protocols": {name: file_hash(SWEEP / name) for name in
                                    ("protocol_extra.json", "protocol_wave2.json",
                                     "protocol_wave3.json")}}
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    log("Froze the extended-year audit protocol before any training")


def verify_protocol() -> dict:
    protocol = json.loads((OUT / "protocol_audit.json").read_text(encoding="utf-8"))
    if protocol["source_sha256"] != file_hash(Path(__file__)):
        raise SystemExit("extended_audit.py changed after its protocol was frozen; stop")
    for name, digest in protocol["pinned_modules"].items():
        if file_hash(ROOT / name) != digest:
            raise SystemExit(f"Pinned module {name} changed after the audit protocol was frozen")
    return protocol


def train() -> None:
    verify_protocol()
    result_path = OUT / "training_audit.json"
    if result_path.exists():
        raise SystemExit("Audit training already recorded; preserving it")
    FOLDS.mkdir(parents=True, exist_ok=True)
    MODELS.mkdir(parents=True, exist_ok=True)
    started = time.monotonic()
    record = {"generated_at_local": time.strftime("%Y-%m-%dT%H:%M:%S"),
              "protocol_sha256": file_hash(OUT / "protocol_audit.json"), "years": [],
              "reproduction": {}}
    years = AUDIT_YEARS + (REPRODUCTION_YEAR,)

    # The frozen suites read their protocol next to their caches, so give them
    # byte-identical copies; the hashes therefore still match the pinned ones.
    for name in ("protocol_extra.json", "protocol_wave2.json"):
        shutil.copyfile(SWEEP / name, OUT / name)
        record.setdefault("copied_protocols", {})[name] = file_hash(OUT / name)

    original_val, original_model = run_module.VAL_DIR, run_module.MODEL_DIR
    run_module.VAL_DIR, run_module.MODEL_DIR = FOLDS, MODELS
    try:
        for year in years:
            run_module.train_fold(year, 180, 16)
            record["years"].append({"year": year,
                                    "fold": file_hash(FOLDS / f"fold_{year}.parquet")})
            log(f"released fold {year} rebuilt")
    finally:
        run_module.VAL_DIR, run_module.MODEL_DIR = original_val, original_model

    reference = pl.read_parquet(ROOT / "validation" / f"fold_{REPRODUCTION_YEAR}.parquet").sort(
        "trade_date", "ts_code")
    rebuilt = pl.read_parquet(FOLDS / f"fold_{REPRODUCTION_YEAR}.parquet").sort("trade_date", "ts_code")
    identical = (rebuilt.select(KEYS).equals(reference.select(KEYS))
                 and np.array_equal(rebuilt["pred_raw"].to_numpy(), reference["pred_raw"].to_numpy()))
    record["reproduction"]["released_fold_2022"] = identical
    if not identical:
        raise AssertionError("Rebuilt 2022 released fold differs from the pinned artifact")
    log("Harness proof 1: rebuilt 2022 released fold is bit-identical to the pinned artifact")

    extra.OUT = OUT
    extra.FOLD_YEARS = years
    extra.CANDIDATES = [c for c in extra.CANDIDATES if c["variant"] == "xgboost"]
    extra.train()
    log("XGBoost member retrained for the audit years")

    wave2.OUT = OUT
    wave2.DEVELOPMENT_YEARS = years
    wave2.CANDIDATES = [c for c in wave2.CANDIDATES if c["variant"] in ("two_day", "pruned")]
    wave2.train()
    log("Two-day and pruned members retrained for the audit years")

    pinned_xgb = pl.read_parquet(SWEEP / f"T2f_xgboost_backbone_{REPRODUCTION_YEAR}.parquet").sort(
        "trade_date", "ts_code")
    audit_xgb = pl.read_parquet(OUT / f"T2f_xgboost_backbone_{REPRODUCTION_YEAR}.parquet").sort(
        "trade_date", "ts_code")
    record["reproduction"]["xgboost_2022"] = bool(np.array_equal(
        audit_xgb["pred_raw"].to_numpy(), pinned_xgb["pred_raw"].to_numpy()))
    log(f"Harness proof 2: XGBoost 2022 cache identical = {record['reproduction']['xgboost_2022']}")
    for key in ("W2c_two_day_horizon", "W2d_pruned_features"):
        pinned = pl.read_parquet(SWEEP / f"{key}_2024.parquet").sort("trade_date", "ts_code")
        rebuilt = pl.read_parquet(OUT / f"{key}_2024.parquet").sort("trade_date", "ts_code")
        record["reproduction"][f"{key}_2024"] = bool(np.array_equal(
            rebuilt["pred_raw"].to_numpy(), pinned["pred_raw"].to_numpy()))
        log(f"Harness proof 3: {key} 2024 cache identical = "
            f"{record['reproduction'][f'{key}_2024']}")
    record["elapsed_seconds"] = time.monotonic() - started
    result_path.write_text(json.dumps(record, ensure_ascii=False, indent=2), encoding="utf-8")
    log(f"Wrote {result_path}")


def audit_labels(year: int) -> pl.DataFrame:
    """Same construction as original_labels(), which is pinned to 2022-2024."""
    frame = (pl.scan_csv(ROOT / "data" / "raw" / "训练集.csv",
                         schema_overrides={"ts_code": pl.String, "trade_date": pl.Int32,
                                           "y_ret_1d": pl.Float64},
                         null_values=["NaN", "nan", ""])
             .filter(pl.col("trade_date").is_between(year * 10000 + 101, year * 10000 + 1231))
             .select("ts_code", "trade_date", "y_ret_1d")
             .collect())
    if year in (2022, 2023, 2024) and not frame.equals(original_labels(year)):
        raise AssertionError(f"Audit label reader diverges from the pinned one for {year}")
    return frame


def audit_score(panel: Panel, prediction: np.ndarray, year: int) -> tuple[dict, pl.DataFrame]:
    """Byte-faithful replica of official_score that also accepts audit years."""
    if not np.all((panel.dates >= year * 10000 + 101) & (panel.dates <= year * 10000 + 1231)):
        raise ValueError("Panel contains dates outside the requested label year")
    prediction = np.asarray(prediction, dtype=float).reshape(-1)
    if len(prediction) != len(panel.frame) or not np.isfinite(prediction).all():
        raise ValueError("Predictions must be finite and aligned with every panel row")
    labels = audit_labels(year)
    keys = panel.frame.select(KEYS)
    if len(labels) != len(keys) or not keys.join(labels.select(KEYS), on=KEYS,
                                                 how="anti").is_empty():
        raise ValueError(f"Label keys do not match the audit panel for {year}")
    frame = panel.frame.drop("y_ret_1d").join(labels, on=KEYS, how="left", validate="1:1").sort(
        "trade_date", "ts_code")
    if not frame.select(KEYS).equals(keys):
        raise AssertionError("Label join changed prediction row order")
    with tempfile.TemporaryDirectory(prefix="extended-audit-") as temporary:
        folder = Path(temporary)
        keys.with_columns(pl.Series("pred", prediction)).write_csv(folder / "submission.csv",
                                                                   float_precision=17)
        frame.select(KEYS + ["flag_limit_up"]).write_csv(folder / "测试集_X.csv")
        frame.select(KEYS + ["y_ret_1d"]).write_csv(folder / "测试集_Y.csv", float_precision=17)
        official = {k: float(v) for k, v in evaluate(str(folder / "submission.csv"),
                                                     str(folder)).items()}
        rebuilt, daily = _same_csv_daily(folder)
    for key, value in official.items():
        if abs(value - rebuilt[key]) > NUMERIC_TOLERANCE:
            raise AssertionError((year, key, value, rebuilt[key]))
    return official, daily


def released_stack(panel: Panel, raw: np.ndarray, auxiliary: np.ndarray | None) -> np.ndarray:
    stable = retention_scores(panel, raw, RELEASED["alpha"], BASE_BONUS, "standard")
    if auxiliary is None:
        return restore_lower_ranks(panel, stable, raw, 1.0)
    return blend_top_only(panel, stable, raw, auxiliary, BLEND_WEIGHT)


def member_raws(panel: Panel, year: int) -> dict:
    raws = {"released_lgb": panel.frame["pred_raw"].to_numpy().astype(np.float64)}
    for key in MEMBER_KEYS:
        frame = pl.read_parquet(OUT / f"{key}_{year}.parquet").sort("trade_date", "ts_code")
        if not frame.select(KEYS).equals(panel.frame.select(KEYS)):
            raise AssertionError(f"{key} {year}: cache keys misaligned with the audit fold")
        raws[key] = frame["pred_raw"].to_numpy().astype(np.float64)
    return raws


def score() -> None:
    protocol = verify_protocol()
    result_path = OUT / "audit_results.json"
    if result_path.exists():
        raise SystemExit("Audit results already recorded; preserving them")
    started = time.monotonic()
    wave3 = json.loads((SWEEP / "protocol_wave3.json").read_text(encoding="utf-8"))
    weights = next(c["members"] for c in wave3["candidates"] if c["key"] == PRIMARY)
    if weights != {m: 1.0 for m in weights}:
        raise AssertionError("Primary ensemble weights are not the frozen equal weights")

    anchor_panel = load_panel(REPRODUCTION_YEAR)
    anchor_aux = load_auxiliary(REPRODUCTION_YEAR, anchor_panel)
    anchor_raw = anchor_panel.frame["pred_raw"].to_numpy().astype(np.float64)
    anchor = audit_score(anchor_panel,
                         released_stack(anchor_panel, anchor_raw, anchor_aux), REPRODUCTION_YEAR)
    official, _ = official_score(anchor_panel,
                                 released_stack(anchor_panel, anchor_raw, anchor_aux),
                                 REPRODUCTION_YEAR)
    if abs(anchor[0]["final_score"] - RELEASED_2022) > NUMERIC_TOLERANCE:
        raise AssertionError(f"Replica scorer missed the released 2022 composite: {anchor[0]}")
    if abs(anchor[0]["final_score"] - official["final_score"]) > NUMERIC_TOLERANCE:
        raise AssertionError("Replica scorer disagrees with official_score on 2022")
    no_blend = audit_score(anchor_panel,
                           released_stack(anchor_panel, anchor_raw, None), REPRODUCTION_YEAR)[0]
    log(f"Anchor: replica reproduces the released 2022 composite {RELEASED_2022:.15f}; "
        f"disabling the pooled blend moves it to {no_blend['final_score']:.9f} "
        f"({no_blend['final_score'] - RELEASED_2022:+.9f})")
    del anchor_panel, anchor_aux

    results = {"anchor_2022": {"with_blend": anchor[0], "without_blend": no_blend},
               "blend_effect_2022": no_blend["final_score"] - RELEASED_2022, "years": {}}
    for year in AUDIT_YEARS:
        panel = Panel.from_frame(pl.read_parquet(FOLDS / f"fold_{year}.parquet"))
        raws = member_raws(panel, year)
        ensemble = ensemble_raw(panel, weights, raws)
        entries = {}
        for key, raw in (("released_lgb_backbone", raws["released_lgb"]),
                         ("T2f_xgboost_backbone", raws["T2f_xgboost_backbone"]),
                         (PRIMARY, ensemble)):
            prediction = released_stack(panel, raw, None)
            metrics, daily = audit_score(panel, prediction, year)
            daily.write_csv(OUT / f"{key}_{year}_daily.csv")
            entries[key] = {k: float(v) for k, v in metrics.items()}
            log(f"{year} {key}: score={metrics['final_score']:.9f} ic={metrics['ic_mean']:.6f} "
                f"excess={metrics['annual_excess']:.6f} turn={metrics['mean_turnover']:.6f}")
        base = entries["released_lgb_backbone"]["final_score"]
        for key, entry in entries.items():
            entry["delta_vs_released"] = entry["final_score"] - base
        results["years"][str(year)] = entries
        del panel, raws, ensemble
    for key in ("T2f_xgboost_backbone", PRIMARY):
        deltas = [results["years"][str(y)][key]["delta_vs_released"] for y in AUDIT_YEARS]
        results.setdefault("consistency", {})[key] = {
            "audit_deltas": deltas, "mean_delta": sum(deltas) / len(deltas),
            "consistent_both_years": all(d > 0 for d in deltas)}
    results.update({"stage": "extended_year_audit",
                    "generated_at_local": time.strftime("%Y-%m-%dT%H:%M:%S"),
                    "elapsed_seconds": time.monotonic() - started,
                    "protocol_sha256": file_hash(OUT / "protocol_audit.json"),
                    "caveat": protocol["limitations"]})
    result_path.write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
    for key, item in results["consistency"].items():
        log(f"AUDIT {key}: deltas={['%+.6f' % d for d in item['audit_deltas']]} "
            f"consistent={item['consistent_both_years']}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("stage", choices=("protocol", "train", "score"))
    arguments = parser.parse_args()
    if arguments.stage == "protocol":
        write_protocol()
    elif arguments.stage == "train":
        train()
    else:
        score()
