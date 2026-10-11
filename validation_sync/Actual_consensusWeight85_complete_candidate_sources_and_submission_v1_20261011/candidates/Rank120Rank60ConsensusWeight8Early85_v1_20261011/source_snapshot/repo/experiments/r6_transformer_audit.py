"""Independent audit of the fixed Transformer identity repair.

This module never fits a model or produces candidate predictions. Historical
artifacts are read only by explicit development/confirmation commands. The
default test command uses synthetic data and writes nothing unless requested.
"""
from __future__ import annotations

import os
for _thread_name in ("POLARS_MAX_THREADS", "OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_thread_name] = "4"

import argparse
from functools import lru_cache
import hashlib
import json
from pathlib import Path
import sys
import tempfile

import numpy as np
import polars as pl

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from experiments.audit_r5_candidate import _daily_from_csv, paired_block_bootstrap

OUT = ROOT / "experiments/r6_transformer_20260926"
REFERENCES = ROOT / "experiments/revalidation_20260926/validation"
KEYS = ["ts_code", "trade_date"]
DEVELOPMENT = (2020, 2021, 2022)
CONFIRMATION = (2023, 2024)
VARIANTS = ("shared", "feature_identity")
PRIMARY = "feature_identity"
REFERENCE_NAMES = ("baseline", "ensemble4")
THRESHOLDS = {
    "development": {"mean_score_delta_min": .001, "worst_year_score_delta_min": -.005, "mean_ic_delta_min": -.002},
    "confirmation": {"mean_score_delta_min": .0005, "worst_year_score_delta_min": -.003, "mean_ic_delta_min": -.002},
}


def sha(path: Path) -> str:
    with Path(path).open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def read(path: Path) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8-sig"))


def write_new(path: Path, payload: dict) -> None:
    if not path.resolve().is_relative_to(OUT.resolve()):
        raise ValueError("Audit output must remain in the isolated r6 directory")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x", encoding="utf-8") as stream:
        json.dump(payload, stream, ensure_ascii=False, indent=2, allow_nan=False)


def _root_path(relative: str) -> Path:
    path = (ROOT / relative).resolve()
    if not path.is_relative_to(ROOT.resolve()):
        raise ValueError("An artifact path escaped the workspace")
    return path


def _out_path(relative: str) -> Path:
    path = (OUT / relative).resolve()
    if not path.is_relative_to(OUT.resolve()):
        raise ValueError("An artifact path escaped the r6 experiment")
    return path


def verify_protocol() -> dict:
    protocol = read(OUT / "protocol.json")
    expected = protocol["input_sha256"]
    own = Path(__file__).relative_to(ROOT).as_posix()
    if own not in expected:
        raise AssertionError("Independent audit source was not frozen before development")
    for relative, digest in expected.items():
        if sha(_root_path(relative)) != digest:
            raise AssertionError(f"Frozen input changed: {relative}")
    if protocol["development_years"] != list(DEVELOPMENT) or protocol["confirmation_years"] != list(CONFIRMATION):
        raise AssertionError("Unexpected chronology")
    for stage, thresholds in THRESHOLDS.items():
        if protocol["gates"][stage] != thresholds:
            raise AssertionError("Frozen score thresholds differ from independent auditor")
    return protocol


@lru_cache(maxsize=1)
def _raw_year(year: int) -> pl.DataFrame:
    if year not in (*DEVELOPMENT, *CONFIRMATION):
        raise ValueError("Only predeclared r6 years may be scored")
    return (pl.scan_csv(ROOT / "data" / "raw" / "训练集.csv", schema_overrides={"ts_code": pl.String,
            "trade_date": pl.Int32, "y_ret_1d": pl.Float64}, null_values=["NaN", "nan", ""])
            .filter(pl.col("trade_date").is_between(year * 10000 + 101, year * 10000 + 1231))
            .select(KEYS + ["y_ret_1d", "flag_limit_up"]).sort("trade_date", "ts_code").collect())


def _score_frames(prediction: pl.DataFrame, raw: pl.DataFrame) -> tuple[dict, pl.DataFrame, dict]:
    """Score original Float64 labels; use the frozen r5 daily reconstruction."""
    from evaluate import evaluate
    prediction = prediction.select(KEYS + ["pred"]).sort("trade_date", "ts_code")
    raw = raw.select(KEYS + ["y_ret_1d", "flag_limit_up"]).sort("trade_date", "ts_code")
    if (prediction.select(pl.struct(KEYS).n_unique()).item() != len(prediction)
            or raw.select(pl.struct(KEYS).n_unique()).item() != len(raw)
            or not prediction.select(KEYS).equals(raw.select(KEYS))
            or not prediction["pred"].is_finite().all()
            or raw.schema["y_ret_1d"] != pl.Float64):
        raise ValueError("Unique keys, full coverage, finite scores and original Float64 labels are required")
    with tempfile.TemporaryDirectory(prefix="r6-independent-official-") as temporary:
        folder = Path(temporary)
        prediction.write_csv(folder / "submission.csv", float_precision=17)
        raw.select(KEYS + ["y_ret_1d"]).write_csv(folder / "测试集_Y.csv", float_precision=17)
        raw.select(KEYS + ["flag_limit_up"]).write_csv(folder / "测试集_X.csv")
        official = {key: float(value) for key, value in evaluate(str(folder / "submission.csv"), str(folder)).items()}
        rebuilt, daily, details = _daily_from_csv(folder)
        differences = {key: rebuilt[key] - value for key, value in official.items()}
        if not all(np.isfinite(value) and abs(value) <= 1e-12 for value in differences.values()):
            raise AssertionError(f"Official/daily reconstruction disagreement: {differences}")
        details.update({"official_vs_independent_daily_difference": differences,
                        "scored_csv_sha256": sha(folder / "submission.csv"),
                        "raw_float64_label_csv_sha256": sha(folder / "测试集_Y.csv"),
                        "flags_csv_sha256": sha(folder / "测试集_X.csv")})
    return official, daily, details


def independent_official_score(prediction_path: Path, year: int, *, column: str = "pred") -> tuple[dict, pl.DataFrame, dict]:
    """Public API: frozen parquet -> metrics, daily evidence, checks.

    Development scoring is authorized only by an explicit development audit.
    The CLI verifies the frozen gate before reading confirmation artifacts.
    `column='pred_raw'` independently audits the separately saved raw scores.
    """
    if column not in ("pred", "pred_raw"):
        raise ValueError("Only released or raw prediction columns are scoreable")
    frame = pl.read_parquet(prediction_path, columns=KEYS + [column])
    if column != "pred":
        frame = frame.rename({column: "pred"})
    metric, daily, details = _score_frames(frame, _raw_year(year))
    details.update({"prediction_parquet_sha256": sha(prediction_path), "prediction_column": column,
                    "year": year, "labels_from_original_csv": True})
    return metric, daily, details


def point_gate(metrics: dict, stage: str, years: tuple | None = None) -> dict:
    """Independently recompute both-reference point thresholds; no selection."""
    years = years or (DEVELOPMENT if stage == "development" else CONFIRMATION)
    complete = years == (DEVELOPMENT if stage == "development" else CONFIRMATION)
    threshold = THRESHOLDS[stage]
    comparisons = {}
    for name in REFERENCE_NAMES:
        scores = [metrics[PRIMARY][str(y)]["final_score"] - metrics[name][str(y)]["final_score"] for y in years]
        ics = [metrics[PRIMARY][str(y)]["ic_mean"] - metrics[name][str(y)]["ic_mean"] for y in years]
        comparisons[name] = {"score_deltas": dict(zip(map(str, years), scores)),
                             "mean_score_delta": float(np.mean(scores)), "worst_year_score_delta": min(scores),
                             "mean_ic_delta": float(np.mean(ics)),
                             "passed": bool(np.mean(scores) >= threshold["mean_score_delta_min"]
                                 and min(scores) >= threshold["worst_year_score_delta_min"]
                                 and np.mean(ics) >= threshold["mean_ic_delta_min"])}
    return {"comparisons": comparisons, "passed": complete and all(v["passed"] for v in comparisons.values()),
            "partial": not complete,
            "mean_official_score": float(np.mean([metrics[PRIMARY][str(y)]["final_score"] for y in years]))}


def mechanism_gate(metrics: dict, raw_metrics: dict, years: tuple = DEVELOPMENT) -> dict:
    score = float(np.mean([metrics[PRIMARY][str(y)]["final_score"] - metrics["shared"][str(y)]["final_score"] for y in years]))
    raw_ic = float(np.mean([raw_metrics[PRIMARY][str(y)]["ic_mean"] - raw_metrics["shared"][str(y)]["ic_mean"] for y in years]))
    return {"mean_score_delta_vs_shared": score, "mean_raw_ic_delta_vs_shared": raw_ic,
            "partial": years != DEVELOPMENT,
            "passed": years == DEVELOPMENT and score > 0 and raw_ic > 0}


def _metrics_equal(actual: dict, expected: dict, context: str) -> None:
    if set(actual) != set(expected):
        raise AssertionError(f"Metric keys differ: {context}")
    for key, value in actual.items():
        if not np.isfinite(value) or abs(value - expected[key]) > 1e-12:
            raise AssertionError(f"Independent/runner metric mismatch: {context}/{key}")


def _checked_folds(record: dict, years: tuple, variants: tuple) -> dict:
    if set(record["fold_sha256"]) != {f"fold_{y}.json" for y in years}:
        raise AssertionError("Incomplete or additional folds in stage record")
    folds = {}
    for year in years:
        name = f"fold_{year}.json"
        if sha(OUT / name) != record["fold_sha256"][name]:
            raise AssertionError(f"Fold checksum mismatch: {name}")
        fold = read(OUT / name)
        if fold["year"] != year or set(fold["candidates"]) != set(variants):
            raise AssertionError("Unexpected fold/candidates")
        for relative, digest in fold["artifact_sha256"].items():
            if sha(_out_path(relative)) != digest:
                raise AssertionError(f"Fold artifact changed: {relative}")
        for key in variants:
            for prefix in ("raw", "predictions"):
                if f"{prefix}_{key}_{year}.parquet" not in fold["artifact_sha256"]:
                    raise AssertionError("Predictions were not bound to the frozen fold")
            metadata_name = f"training_{key}_{year}.json"
            if metadata_name not in fold["artifact_sha256"]:
                raise AssertionError("Training metadata was not bound to the fold")
            metadata = read(OUT / metadata_name)
            if (metadata["year"] != year or metadata["variant"] != key
                    or metadata["epochs"] != 30 or metadata["feature_count"] != 63
                    or not metadata["train_state_has_only_past_rows"]
                    or not metadata["raw_16day_prefix_exact"]
                    or not (metadata["last_training_date"] < metadata["last_label_available_date"]
                            < metadata["first_validation_date"])
                    or metadata["last_label_available_date"] != metadata["training_cutoff_exclusive"]
                    or metadata["last_training_date"] >= metadata["training_cutoff_exclusive"]
                    or metadata["scaler_stats"]["cutoff_exclusive"] != metadata["training_cutoff_exclusive"]
                    or len(metadata["curve"]) != 30
                    or [row["epoch"] for row in metadata["curve"]] != list(range(1, 31))):
                raise AssertionError("Training horizon, purge or fixed epoch contract failed")
            batches = metadata["training_days"] // 4 + int(metadata["training_days"] % 4 >= 2)
            if any(row["batches"] != batches or not np.isfinite(row["mean_train_loss"]) for row in metadata["curve"]):
                raise AssertionError("Daily batching, singleton skip or train-loss contract failed")
            for relative, digest in metadata["artifact_sha256"].items():
                if sha(_out_path(relative)) != digest or fold["artifact_sha256"].get(relative) != digest:
                    raise AssertionError("Training/fold artifact chain disagrees")
            with np.load(OUT / f"scaler_{year}.npz") as scaler:
                for field in ("mean", "std"):
                    values = scaler[field]
                    digest = hashlib.sha256(np.ascontiguousarray(values, dtype=np.float32).tobytes()).hexdigest()
                    if values.shape != (63,) or not np.isfinite(values).all() or digest != metadata["scaler_stats"][f"{field}_sha256"]:
                        raise AssertionError("Saved scaler differs from training statistics")
                    if field == "std" and not np.all(values > 0):
                        raise AssertionError("Invalid saved feature scale")
        folds[year] = fold
    return folds


def validate_completed_years(record: dict, metrics: dict) -> tuple:
    """Only a contiguous prefix ending at the first hard failure may stop early."""
    years = tuple(record.get("completed_years", DEVELOPMENT))
    if not years or years != DEVELOPMENT[:len(years)]:
        raise AssertionError("Development years must be a nonempty chronological prefix")
    failures = [year for year in years if any(
        metrics[PRIMARY][str(year)]["final_score"] - metrics[name][str(year)]["final_score"] < -.005
        for name in REFERENCE_NAMES)]
    reason = record.get("early_stop_reason")
    if len(years) < len(DEVELOPMENT) or reason is not None:
        if (reason != "hard_worst_year_gate_failed" or failures != [years[-1]]
                or record["development_gate_passed"] is not False):
            raise AssertionError("Incomplete development requires the first irreversible worst-year failure")
    elif failures and failures[0] != DEVELOPMENT[-1]:
        raise AssertionError("Driver continued after an earlier irreversible hard failure")
    return years


def _frozen_development() -> tuple[dict, dict, dict]:
    """Check selection record from metrics before allowing confirmation reads."""
    dev = read(OUT / "development.json")
    if dev["protocol_sha256"] != sha(OUT / "protocol.json"):
        raise AssertionError("Development used another protocol")
    years = tuple(dev.get("completed_years", DEVELOPMENT))
    if not years or years != DEVELOPMENT[:len(years)]:
        raise AssertionError("Incomplete or reordered development prefix")
    folds = _checked_folds(dev, years, VARIANTS)
    metrics = {key: {str(y): folds[y]["candidates"][key]["metrics"] for y in years} for key in VARIANTS}
    raw_metrics = {key: {str(y): folds[y]["candidates"][key]["raw_metrics"] for y in years} for key in VARIANTS}
    for key in REFERENCE_NAMES:
        metrics[key] = {str(y): folds[y]["references"][key] for y in years}
    validate_completed_years(dev, metrics)
    aggregate, mechanism = point_gate(metrics, "development", years), mechanism_gate(metrics, raw_metrics, years)
    passed = aggregate["passed"] and mechanism["passed"]
    if bool(dev["development_gate_passed"]) != passed:
        raise AssertionError("Frozen development pass disagrees with independent reconstruction")
    for name in REFERENCE_NAMES:
        for metric in ("mean_score_delta", "worst_year_score_delta", "mean_ic_delta"):
            if abs(dev["aggregate"]["comparisons"][name][metric] - aggregate["comparisons"][name][metric]) > 1e-12:
                raise AssertionError("Development aggregate does not match frozen fold metrics")
    for metric in ("mean_score_delta_vs_shared", "mean_raw_ic_delta_vs_shared"):
        if abs(dev["mechanism_gate"][metric] - mechanism[metric]) > 1e-12:
            raise AssertionError("Development mechanism summary does not match its folds")
    return dev, aggregate, mechanism


def audit(stage: str) -> dict:
    if stage not in ("development", "confirmation"):
        raise ValueError(stage)
    output = OUT / "independent_audit" / stage
    if output.exists():
        raise FileExistsError("Preserve any completed or partial independent audit")
    protocol = verify_protocol()
    development, _, _ = _frozen_development()
    if stage == "confirmation" and not development["development_gate_passed"]:
        raise ValueError("Development failed; confirmation access is prohibited")
    if stage == "confirmation":
        prior_audit = read(OUT / "independent_audit/development/score_audit.json")
        if (prior_audit["status"] != "passed" or prior_audit["stage_gate_passed"] is not True
                or prior_audit["stage_record_sha256"] != sha(OUT / "development.json")
                or prior_audit["protocol_sha256"] != sha(OUT / "protocol.json")):
            raise AssertionError("Confirmation needs the passed independent development audit")
    record = development if stage == "development" else read(OUT / "confirmation.json")
    if stage == "confirmation" and record["development_sha256"] != sha(OUT / "development.json"):
        raise AssertionError("Confirmation does not bind the fixed development decision")
    years = tuple(development.get("completed_years", DEVELOPMENT)) if stage == "development" else CONFIRMATION
    variants = VARIANTS if stage == "development" else (PRIMARY,)
    folds = _checked_folds(record, years, variants)
    output.mkdir(parents=True, exist_ok=False)
    metrics, raw_metrics, checks, daily = {}, {}, {}, {}
    for year in years:
        fold = folds[year]
        for key in (*variants, *REFERENCE_NAMES):
            path = OUT / f"predictions_{key}_{year}.parquet" if key in variants else REFERENCES / f"predictions_{key}_{year}.parquet"
            result, frame, details = independent_official_score(path, year)
            expected = fold["candidates"][key]["metrics"] if key in variants else fold["references"][key]
            _metrics_equal(result, expected, f"{key}/{year}")
            metrics.setdefault(key, {})[str(year)] = result
            checks.setdefault(key, {})[str(year)] = details
            daily.setdefault(key, {})[year] = frame
            frame.write_csv(output / f"official_{key}_{year}_daily.csv", float_precision=17)
            if key in variants:
                raw_path = OUT / f"raw_{key}_{year}.parquet"
                standalone = pl.read_parquet(raw_path, columns=KEYS + ["pred_raw"]).sort("trade_date", "ts_code")
                embedded = pl.read_parquet(path, columns=KEYS + ["pred_raw"]).sort("trade_date", "ts_code")
                if (not standalone.select(KEYS).equals(embedded.select(KEYS))
                        or not np.array_equal(standalone["pred_raw"].to_numpy(), embedded["pred_raw"].to_numpy())):
                    raise AssertionError("Standalone and final-frame raw predictions differ")
                result_raw, frame_raw, detail_raw = independent_official_score(raw_path, year, column="pred_raw")
                _metrics_equal(result_raw, fold["candidates"][key]["raw_metrics"], f"raw/{key}/{year}")
                raw_metrics.setdefault(key, {})[str(year)] = result_raw
                checks[key][str(year)]["raw"] = detail_raw
                frame_raw.write_csv(output / f"raw_{key}_{year}_daily.csv", float_precision=17)
            print(f"independent {year} {key}: {result['final_score']:.12f}", flush=True)
    aggregate = point_gate(metrics, stage, years)
    mechanism = mechanism_gate(metrics, raw_metrics, years) if stage == "development" else None
    if stage == "development":
        validate_completed_years(development, metrics)
    uncertainty = ({key: paired_block_bootstrap(daily[PRIMARY], daily[key], block_days=20, draws=20000, seed=2026)
                    for key in REFERENCE_NAMES} if stage == "confirmation" else None)
    passed = aggregate["passed"] and (mechanism["passed"] if mechanism else all(x["passes_positive_share_80pct"] for x in uncertainty.values()))
    expected_pass = record["development_gate_passed"] if stage == "development" else record["official_and_noise_gate_passed"]
    if passed != expected_pass:
        raise AssertionError("Independent and runner stage decision disagree")
    if stage == "confirmation":
        for key in REFERENCE_NAMES:
            expected_uncertainty = record["bootstrap"][key]
            for metric in ("bootstrap_share_positive", "observed_mean_annual_score_delta"):
                if abs(uncertainty[key][metric] - expected_uncertainty[metric]) > 1e-12:
                    raise AssertionError("Independent bootstrap differs from runner")
    result = {"status": "passed", "stage": stage, "primary_candidate": PRIMARY,
              "completed_years": list(years), "development_partial": stage == "development" and years != DEVELOPMENT,
              "early_stop_reason": development.get("early_stop_reason"),
              "source_sha256": sha(Path(__file__)), "protocol_sha256": sha(OUT / "protocol.json"),
              "stage_record_sha256": sha(OUT / f"{stage}.json"),
              "original_evaluator_sha256": sha(ROOT / "evaluate.py"),
              "reused_r5_audit_sha256": sha(ROOT / "experiments/audit_r5_candidate.py"),
              "historical_metrics": metrics, "raw_metrics": raw_metrics,
              "aggregate": aggregate, "mechanism_gate": mechanism,
              "paired_uncertainty": uncertainty, "stage_gate_passed": bool(passed),
              "independent_scoring_checks": checks, "frozen_input_count": len(protocol["input_sha256"]),
              "artifacts_sha256": {p.name: sha(p) for p in sorted(output.glob("*.csv"))},
              "selection_bias_corrected": False, "new_candidates_produced": False,
              "limitation": "Audit pass verifies fixed artifacts and scoring; it is not model promotion, independent unseen validation, or executable-return evidence."}
    write_new(output / "score_audit.json", result)
    return result


def synthetic_tests() -> dict:
    """No historical prices, features, model weights or candidate scores are read."""
    dates = [20200102, 20200103, 20200106, 20200107]
    rows = [{"ts_code": f"S{i:04d}", "trade_date": d, "pred": float(i),
             "y_ret_1d": None if i in (117, 118) else .01 + i * 1e-12 + j * 1e-6,
             "flag_limit_up": int(i == 119)} for j, d in enumerate(dates) for i in range(120)]
    fixture = pl.DataFrame(rows).with_columns(pl.col("y_ret_1d").cast(pl.Float64))
    score, daily, details = _score_frames(fixture, fixture)
    assert abs(score["ic_mean"] - 1) < 1e-12
    assert details["return_top_sets_sha256"] != details["turnover_top_sets_sha256"]
    assert details["turnover_pairs"] == len(dates) - 1
    assert fixture.filter(pl.col("trade_date") == dates[0])["y_ret_1d"].drop_nulls().cast(pl.Float32).n_unique() == 1
    for invalid in (fixture.head(len(fixture)-1), pl.concat([fixture, fixture.head(1)]),
                    fixture.with_columns(pl.lit(float("nan")).alias("pred"))):
        try:
            _score_frames(invalid, fixture)
        except ValueError:
            pass
        else:
            raise AssertionError("Invalid prediction contract was accepted")
    ref = daily.select("trade_date", "rank_ic", "excess", "turnover")
    changed = ref.with_columns((pl.col("rank_ic") + .0025).alias("rank_ic"))
    a = paired_block_bootstrap({2020: changed}, {2020: ref}, draws=256)
    assert abs(a["observed_mean_annual_score_delta"] - .001) < 1e-12
    assert a["bootstrap_share_positive"] == 1
    assert a == paired_block_bootstrap({2020: changed}, {2020: ref}, draws=256)
    metrics = {name: {str(y): {"final_score": .4, "ic_mean": .1} for y in DEVELOPMENT}
               for name in (*VARIANTS, *REFERENCE_NAMES)}
    raw = {name: {str(y): {"ic_mean": .1} for y in DEVELOPMENT} for name in VARIANTS}
    assert not point_gate(metrics, "development")["passed"]
    assert not mechanism_gate(metrics, raw)["passed"]
    for year in DEVELOPMENT:
        metrics[PRIMARY][str(year)]["final_score"] += .002
        raw[PRIMARY][str(year)]["ic_mean"] += .001
    assert point_gate(metrics, "development")["passed"] and mechanism_gate(metrics, raw)["passed"]
    metrics[PRIMARY]["2021"]["final_score"] = .39
    assert not point_gate(metrics, "development")["passed"]
    early = {"completed_years": [2020, 2021], "early_stop_reason": "hard_worst_year_gate_failed", "development_gate_passed": False}
    assert validate_completed_years(early, metrics) == (2020, 2021)
    assert not point_gate(metrics, "development", (2020, 2021))["passed"]
    assert not mechanism_gate(metrics, raw, (2020, 2021))["passed"]
    rejected = 0
    for invalid in ({**early, "completed_years": [2021]}, {**early, "completed_years": [2020]},
                    {**early, "early_stop_reason": "mean_score_low"},
                    {**early, "development_gate_passed": True},
                    {**early, "completed_years": [2020, 2021, 2022]}):
        try:
            validate_completed_years(invalid, metrics)
        except AssertionError:
            rejected += 1
    assert rejected == 5
    return {"status": "passed", "historical_inputs_read": False,
            "float64_labels_preserved_despite_float32_rank_collapse": True,
            "original_evaluate_matches_independent_daily_reconstruction": True,
            "distinct_label_filtered_return_and_unfiltered_turnover_top": True,
            "missing_duplicate_nonfinite_predictions_rejected": True,
            "paired_bootstrap_fixed_seed": True, "two_reference_and_mechanism_gates": True,
            "only_first_irreversible_worst_year_failure_allows_prefix_stop": True,
            "source_sha256": sha(Path(__file__))}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("stage", choices=("test", "development", "confirmation"), nargs="?", default="test")
    parser.add_argument("--record", type=Path, help="Optional new synthetic-test JSON within the r6 directory")
    args = parser.parse_args()
    result = synthetic_tests() if args.stage == "test" else audit(args.stage)
    if args.record:
        if args.stage != "test":
            parser.error("--record is only valid for synthetic tests")
        write_new(args.record, result)
    print(json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False))
