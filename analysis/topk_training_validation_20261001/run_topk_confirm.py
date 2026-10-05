"""Descriptive completion of the last open cell in the unbiased model comparison.

analysis/unbiased_model_comparison_20260929/模型无偏对比.md layer 4 carries exactly one arm marked
待验证: the LightGBM Top-K return-weighted pairwise backbone plus the pooled auxiliary
(`supplemental_topk_fulltrain2024`), which scores 0.398280 on the reconstructed test slice - above
every tree arm - and is +0.0102 over slow_only8 in BOTH test segments (2025 and 2026). Its
2026-09-26 development folds (2020-2022) are frozen, but the confirmation years were never run
because the development gate failed, so no five-year row exists and the arm can neither be adopted
nor excluded.

This script produces that row. It is descriptive: it promotes nothing, adopts nothing, reopens no
gate and touches no release. The recipe is imported from experiments/r6_topk.py so that identity is
structural rather than transcribed.

Stages: freeze -> prove -> run -> compare. `freeze` must complete before any score exists.
"""
from __future__ import annotations

import argparse
import gc
import hashlib
import json
import platform
import sys
import time
import traceback
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
import lightgbm as lgb  # noqa: E402
import numpy as np  # noqa: E402
import polars as pl  # noqa: E402
from run import FEATURE_FILE, feature_names, fold_cutoff, to_matrix  # noqa: E402
from experiments.r6_topk import (  # noqa: E402
    KEYS, PARAMS, RETURN_SCALE, ROUNDS, SAMPLES, SEED, FlatTopKObjective,
    fixed_prediction, objective_callback, training_frame,
)
from experiments.revalidate_fold_local import score_official  # noqa: E402

OUT = Path(__file__).resolve().parent
# The 2026-10-01 cleanup preserved the 2026-09-26 revalidation bundle outside the live tree.
R4 = ROOT.parent / "赛题五_历史归档_20261001" / "experiments" / "revalidation_20260926" / "validation"
FROZEN_TOPK = ROOT.parent / "赛题五_历史归档_20261001" / "experiments" / "r6_topk_20260926"
KEY = "topk_return_backbone"
PROOF_YEAR = 2022
NEW_YEARS = (2023, 2024)
ALL_YEARS = (2020, 2021, 2022, 2023, 2024)
REFERENCES = ("baseline", "ensemble4")
# Frozen 2026-09-26 development record; the harness proof must reproduce these exactly.
FROZEN_PROOF_METRICS = {
    "ic_mean": 0.06459874434345639, "ic_std": 0.11157495652965951,
    "icir": 0.5789717186785044, "ic_positive_ratio": 0.743801652892562,
    "annual_excess": 0.35667830827826275, "top1_annual_ret": 0.22555009121349257,
    "mean_turnover": 0.039841527481757906, "final_score": 0.42089053197633397,
}
TOL = 1e-12

DEPENDENCIES = [
    ROOT / "experiments" / "r6_topk.py", ROOT / "experiments" / "cached_recheck.py",
    ROOT / "experiments" / "revalidate_fold_local.py", ROOT / "run.py",
    ROOT / "src" / "scoring.py", ROOT / "src" / "postprocessing.py", ROOT / "evaluate.py",
    ROOT / "data" / "features.parquet", ROOT / "data" / "feature_manifest.json",
    ROOT / "data" / "raw" / "训练集.csv",
]


def sha(path) -> str:
    value = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for chunk in iter(lambda: stream.read(8 * 1024 * 1024), b""):
            value.update(chunk)
    return value.hexdigest()


def write_new(path: Path, value) -> None:
    if path.exists():
        raise FileExistsError(f"refusing to overwrite existing evidence: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def log(message: str) -> None:
    line = f"[{time.strftime('%H:%M:%S')}] {message}"
    print(line, flush=True)
    with (OUT / "run.log").open("a", encoding="utf-8") as stream:
        stream.write(line + "\n")


# --------------------------------------------------------------------------- freeze

def freeze() -> None:
    """Pin the recipe, the interpretation rule and every input hash before a single score exists."""
    versions = {name: getattr(__import__(name), "__version__", "unknown")
                for name in ("lightgbm", "numpy", "polars", "pandas", "scipy")}
    payload = {
        "frozen_at_local": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "purpose": "produce the missing 2023/2024 training-period row for the Top-K return-weighted "
                   "pairwise backbone so that the last 待验证 cell of 模型无偏对比.md layer 4 is "
                   "measured rather than argued away",
        "status": "descriptive_only",
        "promotes_or_adopts_nothing": True,
        "reopens_no_frozen_gate": ("the 2026-09-26 r6_topk development gate failed and stays failed; "
                                   "this run does not re-roll it, change its thresholds, or make "
                                   "promotion possible"),
        "candidate": KEY,
        "recipe_identity": "imported from experiments/r6_topk.py, not transcribed",
        "parameters": PARAMS, "rounds": ROUNDS, "seed": SEED, "samples_per_top": SAMPLES,
        "return_scale": RETURN_SCALE,
        "features": "original 63, no selection",
        "postprocess": {"alpha": 0.9, "bonus": 0.3, "protected_current_weight": 1.0,
                        "pooled_top_only_weight": 0.25},
        "auxiliary": "per-fold aux_raw carried in the revalidation bundle; the frozen full-history "
                     "pooled auxiliary is NOT used because it leaks for 2020-2024",
        "proof_year": PROOF_YEAR,
        "new_years": list(NEW_YEARS),
        "reporting_years": list(ALL_YEARS),
        "harness_proof_required_first": {
            "rule": f"retrain fold {PROOF_YEAR} from scratch and require every official metric within "
                    f"{TOL} of the frozen 2026-09-26 record; also require score_official to reproduce "
                    "the frozen baseline and ensemble4 reference metrics for each new year. Any "
                    "failure stops the run and 2023/2024 scores are not reported.",
            "frozen_proof_metrics": FROZEN_PROOF_METRICS,
        },
        "instrument": {
            "scorer": "unmodified evaluate.py via experiments.revalidate_fold_local.score_official",
            "paired": "analysis.official_score_contributions.paired_difference",
            "ci": "20-day moving-block bootstrap, 20000 draws, seed 20260929+year, drawn "
                  "independently per year and averaged - verbatim from "
                  "analysis/unbiased_tree_comparison.py",
            "calibration": "already reproduced three published intervals to <5e-7 "
                           "(verification.json in this directory)",
        },
        "predeclared_interpretation_rule": {
            "primary_contrast": f"{KEY} minus slow_only8 over 2020-2024",
            "also_reported": ["peer67_slow16", "peer67_slow8", "base63_8"],
            "ci95_entirely_below_zero": "excluded from the admissible frontier, same status as "
                                        "top2_lightgbm and the MLP arms",
            "ci95_crosses_zero": "tie; the arm remains an undominated alternative and choosing among "
                                 "tied arms is a user decision, not a data decision",
            "ci95_entirely_above_zero": "resolvable ahead on the admissible axis - the first such "
                                        "challenger; still not promoted, because all five years are "
                                        "viewed and no blind period remains",
            "no_window_substitution": "the five pre-declared years are reported; no 2-, 3- or 4-year "
                                      "window may replace them, and per-year values are reported "
                                      "alongside the mean",
        },
        "known_prior_evidence": {
            "frozen_2020_2022_scores": {str(y): v for y, v in
                                        zip((2020, 2021, 2022),
                                            (0.40707290913686545, 0.4152844359357778,
                                             0.42089053197633397))},
            "partial_three_year_paired_mean_vs_slow_only8": -0.020598,
            "partial_three_year_ci95": [-0.050309, 0.015856],
            "partial_verdict": "tie - not resolvable on three years, which is why the row stayed open",
            "test_slice_full_period": 0.39827952757098173,
            "test_slice_2025": 0.4156992257975275,
            "test_slice_2026": 0.3559452954671738,
        },
        "all_years_previously_viewed": True,
        "dependency_sha256": {p.relative_to(ROOT).as_posix(): sha(p) for p in DEPENDENCIES},
        "source_sha256": sha(Path(__file__)),
        "python": platform.python_version(), "package_versions": versions,
        "cpu_threads": PARAMS["num_threads"],
    }
    write_new(OUT / "protocol.json", payload)
    log(f"protocol frozen: {sha(OUT / 'protocol.json')}")


def verify_protocol() -> dict:
    protocol = json.loads((OUT / "protocol.json").read_text(encoding="utf-8"))
    assert protocol["parameters"] == PARAMS and protocol["rounds"] == ROUNDS
    assert protocol["source_sha256"] == sha(Path(__file__)), "this script changed after freezing"
    for relative, digest in protocol["dependency_sha256"].items():
        assert sha(ROOT / relative) == digest, f"frozen input changed: {relative}"
    return protocol


# --------------------------------------------------------------------------- fold

def fold(year: int) -> dict:
    """Retrain one fold with the imported frozen recipe and score it through the official evaluator."""
    record_path = OUT / f"fold_{year}.json"
    if record_path.exists():
        return json.loads(record_path.read_text(encoding="utf-8"))
    for existing in OUT.glob(f"*_{year}.*"):
        raise FileExistsError(f"incomplete fold evidence exists, no overwrite: {existing.name}")

    started = time.monotonic()
    train, features, meta = training_frame(year)
    objective = FlatTopKObjective(train["trade_date"].to_numpy(), train["y_ret_1d"].to_numpy())
    x = to_matrix(train, features)
    dataset = lgb.Dataset(x, label=np.zeros(len(x), dtype=np.float32), feature_name=features,
                          free_raw_data=True)
    del train
    gc.collect()
    log(f"{year}: fitting {meta['rows']:,} rows / {meta['days']} days, {len(features)} features, "
        f"{ROUNDS} rounds")
    model = lgb.train(dict(PARAMS, objective=objective_callback(objective)), dataset,
                      num_boost_round=ROUNDS)
    assert model.current_iteration() == ROUNDS and objective.iteration == ROUNDS
    model_path = OUT / f"model_{year}.txt"
    with model_path.open("x", encoding="utf-8") as stream:
        stream.write(model.model_to_string())
    del dataset, x
    gc.collect()

    frame = pl.read_parquet(R4 / f"predictions_ensemble4_{year}.parquet").sort("trade_date", "ts_code")
    valid = (pl.scan_parquet(FEATURE_FILE)
             .filter(pl.col("trade_date").is_between(year * 10000 + 101, year * 10000 + 1231))
             .select(KEYS + features).sort("trade_date", "ts_code").collect())
    assert frame.select(KEYS).equals(valid.select(KEYS)), f"{year}: fold frame misaligned"
    assert fold_cutoff(year) == meta["training_cutoff_exclusive"]

    matrix = to_matrix(valid, features)
    raw = model.predict(matrix, num_threads=PARAMS["num_threads"]).astype(np.float64)
    loaded = lgb.Booster(model_str=model_path.read_text(encoding="utf-8"))
    np.testing.assert_allclose(loaded.predict(matrix[:4096], num_threads=PARAMS["num_threads"]),
                               raw[:4096], rtol=0, atol=0)
    invalid = ~frame["price_valid"].to_numpy()
    raw[invalid] = -1e6
    del matrix, valid, model, loaded
    gc.collect()

    pred = fixed_prediction(frame, raw)
    assert np.isfinite(pred).all() and np.all(pred[invalid] < -1)
    assert np.array_equal(
        pred, fixed_prediction(frame.with_columns(
            pl.lit(None, dtype=pl.Float64).alias("y_ret_1d")), raw)), "prediction reads labels"
    prefix = 50 * frame["ts_code"].n_unique()
    assert np.array_equal(pred[:prefix], fixed_prediction(frame.head(prefix), raw[:prefix]))

    expected = json.loads((R4 / "summary.json").read_text(encoding="utf-8"))["metrics"][str(year)]
    references = {}
    for name in REFERENCES:
        ref = pl.read_parquet(R4 / f"predictions_{name}_{year}.parquet").sort("trade_date", "ts_code")
        assert frame.select(KEYS).equals(ref.select(KEYS))
        metrics, daily = score_official(frame, ref["pred"].to_numpy())
        for key, value in metrics.items():
            assert abs(value - expected[name][key]) <= TOL, \
                f"{year}/{name}: scorer anchor drifted on {key}"
        daily.write_csv(OUT / f"daily_{name}_{year}.csv")
        references[name] = metrics

    metrics, daily = score_official(frame, pred)
    daily.write_csv(OUT / f"daily_{KEY}_{year}.csv")
    frame.with_columns(pl.Series("pred_raw", raw), pl.Series("pred", pred)).write_parquet(
        OUT / f"predictions_{KEY}_{year}.parquet", compression="zstd")

    record = {"year": year, "protocol_sha256": sha(OUT / "protocol.json"), "training": meta,
              "candidate": KEY, "metrics": metrics, "references": references,
              "objective_rounds": objective.iteration,
              "objective_seconds": sum(objective.timings),
              "sampled_pairs_total": sum(objective.pair_counts),
              "elapsed_seconds": time.monotonic() - started,
              "tests": {"model_reload_exact": True,
                        "prediction_label_missingness_invariance": True,
                        "50_day_prefix_exact": True, "invalid_low": True,
                        "scorer_anchor_reproduced": True},
              "artifact_sha256": {p.name: sha(p) for p in OUT.glob(f"*_{year}.*")
                                  if p != record_path}}
    write_new(record_path, record)
    log(f"{year}: official score {metrics['final_score']:.9f} "
        f"(ic {metrics['ic_mean']:.6f}, excess {metrics['annual_excess']:.6f}, "
        f"turnover {metrics['mean_turnover']:.6f}) in {record['elapsed_seconds']:.0f}s")
    del frame, objective
    gc.collect()
    return record


def prove() -> None:
    """Retrain the frozen 2022 fold and demand exact reproduction before any new year is trusted."""
    verify_protocol()
    if (OUT / "harness_proof.json").exists():
        raise FileExistsError("harness proof already recorded")
    record = fold(PROOF_YEAR)
    deltas = {key: abs(record["metrics"][key] - value)
              for key, value in FROZEN_PROOF_METRICS.items()}
    worst = max(deltas.values())
    frozen = json.loads((FROZEN_TOPK / f"fold_{PROOF_YEAR}.json").read_text(encoding="utf-8"))
    payload = {"year": PROOF_YEAR, "max_abs_metric_diff": worst, "tolerance": TOL,
               "per_metric_abs_diff": deltas, "passed": bool(worst <= TOL),
               "recomputed": record["metrics"], "frozen_20260926": frozen["metrics"],
               "frozen_record_sha256": sha(FROZEN_TOPK / f"fold_{PROOF_YEAR}.json"),
               "training_rows_match": record["training"]["rows"] == frozen["training"]["rows"],
               "training_target_sha256_match":
                   record["training"]["target_sha256"] == frozen["training"]["target_sha256"]}
    write_new(OUT / "harness_proof.json", payload)
    log(f"harness proof max|diff| = {worst:.3e} -> {'PASS' if payload['passed'] else 'FAIL'}")
    assert payload["passed"], f"2022 not reproduced (max diff {worst:.3e}); stopping"


def run() -> None:
    verify_protocol()
    proof = json.loads((OUT / "harness_proof.json").read_text(encoding="utf-8"))
    assert proof["passed"], "harness proof did not pass"
    records = [fold(year) for year in NEW_YEARS]
    write_new(OUT / "folds_complete.json", {
        "years": [r["year"] for r in records],
        "scores": {str(r["year"]): r["metrics"]["final_score"] for r in records},
        "completed_at_local": time.strftime("%Y-%m-%dT%H:%M:%S"),
    })
    log("2023/2024 folds complete")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("stage", choices=("freeze", "prove", "run"))
    args = parser.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    try:
        globals()[args.stage]()
    except Exception as error:
        write_new(OUT / f"failure_{time.time_ns()}.json",
                  {"stage": args.stage, "type": type(error).__name__, "message": str(error),
                   "traceback": traceback.format_exc(), "source_sha256": sha(Path(__file__))})
        raise
