"""Independent R10 data, model-reload, mechanism and stage audit.

Synthetic tests never read market data. Explicit stage audits do not refit any
model. Inner-quarter audits never call an official scorer or postprocessor.
"""
from __future__ import annotations

import os
for _variable in ("POLARS_MAX_THREADS", "OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_variable] = "4"

import argparse
import hashlib
import importlib.metadata
import json
from pathlib import Path
import sys

import numpy as np
import polars as pl
from scipy.stats import spearmanr

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from experiments import r9_residual_audit as previous
from experiments.r6_transformer_audit import _score_frames, _raw_year
from experiments.r7_complement_audit import rebuild_post
from experiments.audit_r5_candidate import paired_block_bootstrap

OUT = ROOT / "experiments/r10_rankic_20260927"
R4 = ROOT / "experiments/revalidation_20260926/validation"
KEYS = ["ts_code", "trade_date"]
ARMS = ("zero", "mse", "rankic")
CONTROLS = ("zero", "mse")
REFERENCES = ("ensemble4", "baseline")
STAGES = {
    "inner": tuple(f"inner_2021q{quarter}" for quarter in range(1, 5)),
    "development": ("development_2022",),
    "extension": ("extension_2023", "extension_2024"),
}
GATES = {
    "inner": {"mean_raw_ic_delta_min": .001, "positive_quarters_min": 3,
              "worst_quarter_delta_min": -.002},
    "development": {"mean_score_delta_min": .001, "mean_ic_delta_min": -.002,
                    "raw_ic_delta_min": .001},
    "extension": {"mean_score_delta_min": .0005, "worst_year_score_delta_min": -.003,
                  "mean_ic_delta_min": -.002, "raw_ic_delta_min": 0.,
                  "worst_year_raw_ic_delta_min": -.002},
    "bootstrap": {"block_days": 20, "draws": 20000, "seed": 2026,
                  "positive_share_min": .8},
}
BASE_ARTIFACTS = {"calibration.json", "training_rows.parquet", "model_mse.txt",
                  "model_rankic.txt", "predictions.parquet", "mechanism_daily.csv"}
PARAMS = {key: value for key, value in previous.PARAMS.items() if key not in {"objective", "metric"}}
PARAMS.update({"metric": "None", "boost_from_average": False, "min_sum_hessian_in_leaf": .001})
sha, read, match = previous.sha, previous.read, previous.match
close_arrays, canonical = previous.close_arrays, previous.canonical
array_sha, check_hashes = previous.array_sha, previous.check_hashes


def fold_layout(fold_id: str) -> tuple[str, int, int | None, int, int]:
    for stage, identifiers in STAGES.items():
        if fold_id in identifiers:
            year = 2021 if stage == "inner" else int(fold_id.rsplit("_", 1)[1])
            quarter = int(fold_id[-1]) if stage == "inner" else None
            first = year * 10000 + (1 if quarter is None else 1 + 3 * (quarter - 1)) * 100 + 1
            end = ((year + 1) * 10000 + 101 if quarter is None or quarter == 4
                   else year * 10000 + (1 + 3 * quarter) * 100 + 1)
            return stage, year, quarter, first, end
    raise ValueError("Unexpected fixed fold")


def independent_training(frame: pl.DataFrame) -> tuple[pl.DataFrame, dict, list[dict]]:
    """Input already contains only mature, past, full daily panels.

    Whole degenerate dates are excluded jointly before calibration and before
    N/D are computed. This is independent of either model objective.
    """
    frame = canonical(frame)
    b, target_u, target = previous.rank_inputs(frame)
    dates = frame["trade_date"].to_numpy()
    keep = target.copy()
    dropped = []
    for date in np.unique(dates):
        selected = (dates == date) & target
        reasons = []
        if selected.sum() < 2:
            reasons.append("fewer_than_two_finite_targets")
        else:
            if np.ptp(b[selected]) == 0:
                reasons.append("constant_base_in_target_pool")
            if np.ptp(target_u[selected]) == 0:
                reasons.append("constant_target")
        if reasons:
            keep[dates == date] = False
            dropped.append({"trade_date": int(date), "finite_target_rows": int(selected.sum()), "reasons": reasons})
    if not keep.any():
        raise ValueError("No nondegenerate training dates")
    fitted = previous.calibration(b[keep], target_u[keep], dates[keep])
    anchor = fitted["intercept"] + fitted["slope"] * b[keep]
    rows = frame.select(KEYS).filter(pl.Series(keep)).with_columns(
        pl.Series("b", b[keep]), pl.Series("target_u", target_u[keep]),
        pl.Series("anchor", anchor), pl.Series("weight", previous.date_balanced_weights(dates[keep])))
    return rows, fitted, dropped


def independent_mechanism(frame: pl.DataFrame, raw: dict[str, np.ndarray]) -> tuple[pl.DataFrame, dict]:
    _, target_u, target = previous.rank_inputs(frame)
    dates = frame["trade_date"].to_numpy()
    if set(raw) != set(ARMS):
        raise AssertionError("All three fixed mechanism arms required")
    for arm in ARMS:
        if np.asarray(raw[arm]).shape != target_u.shape or not np.isfinite(raw[arm][target]).all():
            raise AssertionError("Invalid raw signal in the common mechanism pool")
    rows = []
    for date in np.unique(dates):
        take = (dates == date) & target
        if int(take.sum()) < 30:
            raise AssertionError("An evaluation date has fewer than 30 target rows")
        values = {arm: float(spearmanr(raw[arm][take], target_u[take]).statistic) for arm in ARMS}
        if not np.isfinite(list(values.values())).all():
            raise AssertionError("An evaluation date has undefined IC; do not discard it")
        row = {"trade_date": int(date), "n_target": int(take.sum())}
        row.update({f"mse_{arm}": float(np.mean((raw[arm][take] - target_u[take]) ** 2)) for arm in ARMS})
        row.update({f"raw_ic_{arm}": values[arm] for arm in ARMS})
        rows.append(row)
    daily = pl.DataFrame(rows)
    mse = {arm: float(daily[f"mse_{arm}"].mean()) for arm in ARMS}
    ic = {arm: float(daily[f"raw_ic_{arm}"].mean()) for arm in ARMS}
    summary = {"days": len(daily), "mse": mse, "raw_ic": ic,
               "delta_vs_zero": ic["rankic"] - ic["zero"],
               "delta_vs_mse": ic["rankic"] - ic["mse"]}
    return daily, summary


def inner_gate(dailies: dict[str, pl.DataFrame]) -> dict:
    if tuple(dailies) != STAGES["inner"]:
        raise AssertionError("Exactly the four ordered, complete inner quarters are required")
    all_dates = np.concatenate([daily["trade_date"].to_numpy() for daily in dailies.values()])
    if len(np.unique(all_dates)) != len(all_dates):
        raise AssertionError("Repeated inner evaluation dates")
    limits, comparisons = GATES["inner"], {}
    for control in CONTROLS:
        deltas = {key: daily["raw_ic_rankic"].to_numpy() - daily[f"raw_ic_{control}"].to_numpy()
                  for key, daily in dailies.items()}
        if any(not len(values) or not np.isfinite(values).all() for values in deltas.values()):
            raise AssertionError("All inner IC observations must be finite")
        means = {key: float(values.mean()) for key, values in deltas.items()}
        mean = float(np.concatenate(list(deltas.values())).mean())
        positive, worst = sum(value > 0 for value in means.values()), min(means.values())
        comparisons[control] = {"mean_raw_ic_delta": mean, "quarter_deltas": means,
            "positive_quarters": positive, "worst_quarter_delta": worst,
            "passed": bool(mean >= limits["mean_raw_ic_delta_min"]
                and positive >= limits["positive_quarters_min"]
                and worst >= limits["worst_quarter_delta_min"])}
    return {"comparisons": comparisons, "passed": all(value["passed"] for value in comparisons.values())}


def full_gate(folds: list[dict], stage: str) -> dict:
    if stage not in ("development", "extension") or tuple(fold["fold_id"] for fold in folds) != STAGES[stage]:
        raise AssertionError("Complete fixed full-year stage required")
    limits, comparisons = GATES[stage], {}
    for reference in REFERENCES:
        score = np.array([fold["metrics"]["rankic"]["final_score"] - fold["metrics"][reference]["final_score"] for fold in folds])
        ic = np.array([fold["metrics"]["rankic"]["ic_mean"] - fold["metrics"][reference]["ic_mean"] for fold in folds])
        if not np.isfinite(np.r_[score, ic]).all():
            raise AssertionError("Finite official deltas required")
        passed = score.mean() >= limits["mean_score_delta_min"] and ic.mean() >= limits["mean_ic_delta_min"]
        if stage == "extension":
            passed = passed and score.min() >= limits["worst_year_score_delta_min"]
        comparisons[reference] = {"score_deltas": {str(fold["year"]): float(value) for fold, value in zip(folds, score)},
            "mean_score_delta": float(score.mean()), "worst_year_score_delta": float(score.min()),
            "mean_ic_delta": float(ic.mean()), "passed": bool(passed)}
    official = {"comparisons": comparisons, "passed": all(value["passed"] for value in comparisons.values())}
    comparisons = {}
    for control in CONTROLS:
        delta = np.array([fold["mechanism"]["raw_ic"]["rankic"] - fold["mechanism"]["raw_ic"][control] for fold in folds])
        if not np.isfinite(delta).all():
            raise AssertionError("Finite annual mechanism deltas required")
        passed = delta.mean() >= limits["raw_ic_delta_min"]
        if stage == "extension":
            passed = passed and delta.min() >= limits["worst_year_raw_ic_delta_min"]
        comparisons[control] = {"annual_raw_ic_deltas": {str(fold["year"]): float(value) for fold, value in zip(folds, delta)},
            "mean_raw_ic_delta": float(delta.mean()), "worst_year_raw_ic_delta": float(delta.min()), "passed": bool(passed)}
    mechanism = {"comparisons": comparisons, "passed": all(value["passed"] for value in comparisons.values())}
    return {"official": official, "mechanism": mechanism, "point_passed": official["passed"] and mechanism["passed"]}


def stage_pass(stage: str, gate: dict, bootstrap: dict | None) -> bool:
    if stage == "inner":
        if bootstrap is not None:
            raise AssertionError("No bootstrap or official scoring in the inner stage")
        return bool(gate["passed"])
    if stage not in ("development", "extension"):
        raise ValueError(stage)
    if not gate["point_passed"]:
        if bootstrap is not None:
            raise AssertionError("Failed point checks prohibit bootstrap")
        return False
    if not isinstance(bootstrap, dict) or set(bootstrap) != set(REFERENCES):
        raise AssertionError("Both fixed-reference bootstraps required")
    years = [fold_layout(fold_id)[1] for fold_id in STAGES[stage]]
    for value in bootstrap.values():
        if (any(value[key] != GATES["bootstrap"][key] for key in ("block_days", "draws", "seed"))
                or value["years"] != years or not np.isfinite(value["bootstrap_share_positive"])
                or not 0 <= value["bootstrap_share_positive"] <= 1):
            raise AssertionError("Invalid bootstrap settings, years or finite share")
    return all(value["bootstrap_share_positive"] >= .8 for value in bootstrap.values())


def expected_artifacts(fold_id: str) -> set[str]:
    stage = fold_layout(fold_id)[0]
    names = set(BASE_ARTIFACTS)
    if stage != "inner":
        names |= {f"daily_{arm}.csv" for arm in ("rankic", "mse", *REFERENCES)}
    return {(OUT / "folds" / fold_id / name).relative_to(ROOT).as_posix() for name in names}


def checked_stage(stage: str, protocol_sha: str) -> tuple[dict, list[dict], dict]:
    if stage not in STAGES:
        raise ValueError(stage)
    path = OUT / f"{stage}.json"
    record = read(path)
    fold_paths = {(OUT / "folds" / fold_id / "fold.json").relative_to(ROOT).as_posix()
                  for fold_id in STAGES[stage]}
    if (record["stage"] != stage or record["candidate_key"] != "rankic"
            or record["protocol_sha256"] != protocol_sha or record["folds"] != list(STAGES[stage])
            or set(record["fold_sha256"]) != fold_paths):
        raise AssertionError("Stage identity, protocol or exact fold set changed")
    artifacts = check_hashes(ROOT, record["fold_sha256"])
    artifacts[path.relative_to(ROOT).as_posix()] = sha(path)
    folds = []
    for fold_id in STAGES[stage]:
        fold = read(OUT / "folds" / fold_id / "fold.json")
        _, year, quarter, _, _ = fold_layout(fold_id)
        if (fold["fold_id"] != fold_id or fold["stage"] != stage or fold["year"] != year
                or fold["quarter"] != quarter or fold["protocol_sha256"] != protocol_sha
                or set(fold["artifact_sha256"]) != expected_artifacts(fold_id)):
            raise AssertionError("Fold identity or required exact artifact set differs")
        if stage == "inner" and fold.get("metrics", {}) != {}:
            raise AssertionError("Inner folds must not contain official candidate scores")
        if stage != "inner" and set(fold["metrics"]) != {"rankic", "mse", *REFERENCES}:
            raise AssertionError("Full-year scoring must contain exactly two heads and two references")
        required_tests = {"model_reload_exact", "label_and_availability_invariance",
                          "raw_prefix_50days_exact", "finite_invalid_price_excluded"}
        if stage != "inner":
            required_tests |= {"actual_zero_final_exact_r4", "post_reload_label_prefix_exact"}
        if set(fold["tests"]) != required_tests or not all(value is True for value in fold["tests"].values()):
            raise AssertionError("Required unchanged-prediction checks are incomplete or failed")
        artifacts.update(check_hashes(ROOT, fold["artifact_sha256"]))
        folds.append(fold)
    return record, folds, artifacts


def gate_from_saved(folds: list[dict], stage: str) -> dict:
    if stage == "inner":
        return inner_gate({fold["fold_id"]: pl.read_csv(OUT / "folds" / fold["fold_id"] / "mechanism_daily.csv")
                           for fold in folds})
    return full_gate(folds, stage)


def authorize_previous(stage: str, protocol_sha: str, protocol_artifacts: dict) -> dict:
    """Verify all preceding evidence before any current-stage artifact read."""
    if stage == "inner":
        return {}
    if stage not in ("development", "extension"):
        raise ValueError(stage)
    dependencies = ["inner"] if stage == "development" else ["inner", "development"]
    result = {}
    for preceding in dependencies:
        record, folds, artifacts = checked_stage(preceding, protocol_sha)
        gate = gate_from_saved(folds, preceding)
        match(gate, record["gate"], f"preceding {preceding} gate")
        if not stage_pass(preceding, gate, record["bootstrap"]) or record["passed"] is not True:
            raise RuntimeError(f"Failed {preceding} forbids {stage} access")
        audit_path = OUT / "independent_audit" / f"audit_{preceding}.json"
        audit = read(audit_path)
        if (audit["status"] != "passed" or audit["stage_gate_passed"] is not True
                or audit["stage"] != preceding or audit["candidate_key"] != "rankic"
                or audit["folds"] != list(STAGES[preceding]) or audit["protocol_sha256"] != protocol_sha
                or audit["stage_record_sha256"] != sha(OUT / f"{preceding}.json")
                or audit["source_sha256"] != sha(Path(__file__))):
            raise AssertionError("Unchanged passed independent prerequisite audit required")
        match(audit["gate"], gate, "prerequisite audit gate")
        match(audit["bootstrap"], record["bootstrap"], "prerequisite audit bootstrap")
        expected = {**protocol_artifacts, **artifacts, **result}
        expected[(OUT / "protocol.json").relative_to(ROOT).as_posix()] = protocol_sha
        if any(audit["artifacts_sha256"].get(key) != digest for key, digest in expected.items()):
            raise AssertionError("Prerequisite audit omitted or changed a required bound file")
        result.update(check_hashes(ROOT, audit["artifacts_sha256"]))
        result[audit_path.relative_to(ROOT).as_posix()] = sha(audit_path)
    return result


def verify_protocol() -> tuple[dict, dict]:
    protocol = read(OUT / "protocol.json")
    match(protocol["gates"], GATES, "independently fixed thresholds", 0.)
    match(protocol["params"], PARAMS, "fixed common tree parameters", 0.)
    if (protocol["candidate_key"] != "rankic" or protocol["rounds"] != 80
            or protocol["pairs_per_row"] != 8 or protocol["sigmoid_scale"] != 1.
            or protocol["pair_seed"] != 2026 or protocol["historical_years_previously_viewed"] is not True
            or protocol["formal_promotion"] is not False):
        raise AssertionError("Fixed experiment, pair settings or retrospective scope changed")
    specs = {}
    for stage in STAGES:
        specs[stage] = []
        for fold_id in STAGES[stage]:
            _, year, quarter, first, end = fold_layout(fold_id)
            last = year * 10000 + 1231 if quarter is None or quarter == 4 else {
                1: year * 10000 + 331, 2: year * 10000 + 630, 3: year * 10000 + 930}[quarter]
            specs[stage].append({"fold_id": fold_id, "stage": stage, "year": year,
                                 "quarter": quarter, "start": first, "end": last})
    match(protocol["stage_specs"], specs, "fixed complete stage/date schedule", 0.)
    required_sources = {f"experiments/{name}" for name in
        ("r10_rankic.py", "r10_rankic_core.py", "r10_rankic_audit.py", "r10_rankic_design.md", "r10_rankic_requirements.txt")}
    if set(protocol["source_sha256"]) != required_sources:
        raise AssertionError("Exact R10 implementation/design/runtime sources required")
    required_inputs = {"训练集.csv", "data/features.parquet", "data/feature_manifest.json", "evaluate.py",
        "experiments/r9_residual.py", "experiments/r9_residual_core.py", "experiments/r9_residual_audit.py",
        "experiments/r6_transformer_audit.py", "experiments/r7_complement_audit.py", "experiments/audit_r5_candidate.py",
        "experiments/r9_residual_20260926/result_manifest.json",
        "experiments/research_r10_20260926/research_manifest.json", "experiments/r10_rankic_20260927/tests.json"}
    for year in range(2020, 2025):
        required_inputs |= {f"experiments/revalidation_20260926/validation/predictions_{arm}_{year}.parquet" for arm in REFERENCES}
        required_inputs.add(f"experiments/revalidation_20260926/validation/result_{year}.json")
    if not required_inputs <= set(protocol["input_sha256"]):
        raise AssertionError("Original data, full OOF provenance or independent dependencies were not frozen")
    versions = {name: importlib.metadata.version(name) for name in
                ("numpy", "polars", "scipy", "lightgbm", "numba", "llvmlite")}
    match(protocol["runtime_versions"], versions, "frozen installed runtime", 0.)
    artifacts = check_hashes(ROOT, protocol["source_sha256"])
    artifacts.update(check_hashes(ROOT, protocol["input_sha256"]))
    names = read(ROOT / "data/feature_manifest.json")["features"]
    if names != protocol["feature_names"] or len(names) != 63 or len(set(names)) != 63:
        raise AssertionError("Frozen original feature identity/order changed")
    artifacts[(OUT / "protocol.json").relative_to(ROOT).as_posix()] = sha(OUT / "protocol.json")
    return protocol, artifacts


def original_frame(year: int) -> pl.DataFrame:
    frame = previous.original_label_frame(year)
    bounds = read(R4 / f"result_{year}.json")["boundaries"]
    if not (bounds["one_day_label_available"] < bounds["validation_first"]
            and bounds["two_day_label_available"] < bounds["validation_first"]):
        raise AssertionError("R4 source is not mature past-only OOF")
    return frame


def reconstruct_window(fold_id: str, sources: dict[int, pl.DataFrame], calendar: np.ndarray):
    stage, year, _, first_date, end = fold_layout(fold_id)
    validation = sources[year].filter((pl.col("trade_date") >= first_date) & (pl.col("trade_date") < end))
    if validation.is_empty():
        raise AssertionError("Empty fixed validation interval")
    first = int(validation["trade_date"].min())
    source_years = range(2020, year + (stage == "inner"))
    full = canonical(pl.concat([sources[y] for y in source_years]).filter(pl.col("trade_date") < first))
    availability = previous.label_available_dates(full["trade_date"].to_numpy(), calendar)
    mature = (availability > 0) & (availability < first)
    training = full.filter(pl.Series(mature))
    if training.is_empty():
        raise AssertionError("Empty mature training window")
    bounds = {"validation_first": first, "validation_last": int(validation["trade_date"].max()),
        "first_training_signal": int(training["trade_date"].min()),
        "last_training_signal": int(training["trade_date"].max()),
        "last_label_available": int(availability[mature].max()),
        "training_oof_years": sorted(set(map(int, training["trade_date"].to_numpy() // 10000))),
        "purged_signal_dates": sorted(set(map(int, full["trade_date"].to_numpy()[~mature]))),
        "purged_panel_rows": int((~mature).sum()), "retained_panel_rows": len(training),
        "strict_next_market_date_before_validation": True, "no_post_validation_training": True,
        "degenerate_training_days": "Separate common core mask before calibration, recorded in training.core_metadata"}
    return training, validation, bounds


def verify_fit_metadata(arm: str, metadata: dict, model, rows: pl.DataFrame, versions: dict) -> None:
    match(metadata["params"], PARAMS, "saved common model parameters", 0.)
    if (metadata["kind"] != arm or metadata["requested_rounds"] != 80
            or metadata["initial_increment"] != 0. or metadata["init_score"] is not None
            or metadata["initial_increment_verified"] is not True
            or metadata["training_rows"] != len(rows)
            or metadata["training_dates"] != rows["trade_date"].n_unique()
            or metadata["row_hessian_floor"] is not None
            or metadata["leaf_min_sum_hessian"] != .001):
        raise AssertionError("Fixed fit budget, data or initialization differs")
    if (metadata["actual_booster_iterations"] != model.current_iteration()
            or metadata["actual_trees"] != model.num_trees()
            or not 1 <= model.current_iteration() <= 80 or not 1 <= model.num_trees() <= 80):
        raise AssertionError("Saved tree count differs from the fixed fit record")
    match(metadata["versions"], versions, "model fit runtime", 0.)
    sampling = {"draws_per_row": 8, "replacement": True, "unordered": True,
                "seed": "SeedSequence([2026, zero_based_objective_call, integer_trade_date])",
                "zero_weight_ties": "retained in draw denominator, never resampled"}
    match(metadata["sampling"], sampling, "fixed pair sampler", 0.)
    trace = metadata["trace"]
    if len(trace) != 80 or metadata["objective_calls"] != 80:
        raise AssertionError("Missing or excessive objective trace")
    date_values, date_counts = np.unique(rows["trade_date"].to_numpy(), return_counts=True)
    counts = dict(zip(map(int, date_values), map(int, date_counts)))
    training_dates = set(counts)
    for iteration, record in enumerate(trace):
        excluded = record["degenerate_dates"]
        if (record["iteration"] != iteration or len(set(excluded)) != len(excluded)
                or not set(excluded) <= training_dates
                or record["active_days"] + len(excluded) != len(training_dates)
                or record["active_days"] <= 0
                or not np.isfinite(record["training_loss"]) or not np.isfinite(record["seconds"])
                or record["seconds"] < 0):
            raise AssertionError("Invalid objective date/count/loss trace")
        if arm == "mse":
            if excluded or record["sampled_pairs"] != 0 or record["positive_weight_pairs"] != 0:
                raise AssertionError("MSE must preserve all common training dates")
            close_arrays([record["date_equal_mse"]], [2 * record["training_loss"]], "MSE trace loss")
        else:
            expected_pairs = 8 * (len(rows) - sum(counts[date] for date in excluded))
            if (record["sampled_pairs"] != expected_pairs or not 0 <= record["positive_weight_pairs"] <= expected_pairs
                    or not np.isfinite([record["minimum_full_sum_a"], record["maximum_full_sum_a"]]).all()
                    or not 0 < record["minimum_full_sum_a"] <= record["maximum_full_sum_a"]):
                raise AssertionError("RankIC sampling/complete-pair normalizer trace differs")
    if trace[0]["degenerate_dates"] or trace[0]["initial_increment_zero"] is not True:
        raise AssertionError("Initial anchor must remain nondegenerate on every retained date")
    if arm == "mse":
        error = rows["anchor"].to_numpy() - rows["target_u"].to_numpy()
        initial = float(.5 * np.dot(rows["weight"].to_numpy(), error * error) / len(rows))
        close_arrays([trace[0]["training_loss"]], [initial], "independent initial MSE objective")


def audit(stage: str = "inner") -> dict:
    if stage not in STAGES:
        raise ValueError(stage)
    destination_dir = OUT / "independent_audit"
    destination = destination_dir / f"audit_{stage}.json"
    if destination.exists() or any(destination_dir.glob(f"{stage}_*")):
        raise FileExistsError("Existing or incomplete independent evidence is preserved")
    protocol, artifacts = verify_protocol()
    protocol_sha = sha(OUT / "protocol.json")
    artifacts.update(authorize_previous(stage, protocol_sha, artifacts))
    record, folds, stage_artifacts = checked_stage(stage, protocol_sha)
    artifacts.update(stage_artifacts)
    stage_digest = sha(OUT / f"{stage}.json")
    destination_dir.mkdir(parents=True, exist_ok=True)
    calendar = (pl.scan_parquet(ROOT / "data/features.parquet").filter(pl.col("is_train"))
                .select("trade_date").unique().sort("trade_date").collect()["trade_date"].to_numpy())
    names = protocol["feature_names"]
    versions = {"python": sys.version.split()[0], **{name: importlib.metadata.version(name)
                for name in ("numpy", "lightgbm", "numba", "llvmlite")}}
    sources, audited, checks, mechanisms = {}, [], {}, {}
    official_daily = {arm: {} for arm in ("rankic", "mse", *REFERENCES)}
    maxima = {"calibration": 0., "training_rows": 0., "raw_and_post": 0.,
              "mechanism": 0., "official_metrics": 0., "daily_official": 0.}
    import lightgbm as lgb
    for fold in folds:
        fold_id, year = fold["fold_id"], fold["year"]
        print(json.dumps({"independent_fold_started": fold_id}), flush=True)
        for needed_year in range(2020, year + 1):
            if needed_year not in sources:
                sources[needed_year] = original_frame(needed_year)
        full_train, frame, bounds = reconstruct_window(fold_id, sources, calendar)
        match(bounds, fold["boundaries"], f"{fold_id}/mature chronology", 0.)
        train, fitted, dropped = independent_training(full_train)
        directory = OUT / "folds" / fold_id
        saved = canonical(pl.read_parquet(directory / "training_rows.parquet"))
        if (set(saved.columns) != set(KEYS + ["b", "target_u", "anchor", "weight"])
                or not saved.select(KEYS).equals(train.select(KEYS))
                or any(saved.schema[column] != pl.Float64 for column in ("b", "target_u", "anchor", "weight"))):
            raise AssertionError("Common mature original-label training rows or dtypes differ")
        calibration = read(directory / "calibration.json")
        for key, value in fitted.items():
            maxima["calibration"] = max(maxima["calibration"], match(value, calibration[key], f"{fold_id}/calibration/{key}"))
        for column in ("b", "target_u", "anchor", "weight"):
            maxima["training_rows"] = max(maxima["training_rows"], close_arrays(train[column], saved[column], f"{fold_id}/{column}"))
        # Use verified saved coefficients for actual model-input anchor bytes;
        # independent summation can differ at machine precision without error.
        anchor = calibration["intercept"] + calibration["slope"] * train["b"].to_numpy()
        for column, values in (("target_u", train["target_u"].to_numpy()), ("anchor", anchor), ("weight", train["weight"].to_numpy())):
            field = "target_sha256" if column == "target_u" else f"{column}_sha256"
            if array_sha(values) != fold["training"][field] or array_sha(saved[column].to_numpy()) != fold["training"][field]:
                raise AssertionError(f"Independent Float64 {column} hash differs")
        match(fold["training"]["rows"], len(train), "training row count", 0.)
        match(fold["training"]["dates"], train["trade_date"].n_unique(), "training date count", 0.)
        match(calibration["params"], PARAMS, "calibration parameters", 0.)
        if (calibration["rounds"] != 80 or calibration["feature_names"] != names
                or calibration["model_feature_names"] != names + ["r4_percentile"]
                or calibration["lightgbm_version"] != versions["lightgbm"]):
            raise AssertionError("Fixed calibration/model metadata differs")
        close_arrays([calibration["weight_mean"], calibration["calibration_weight_sum"], calibration["weight_sum"]],
                     [1., 1., float(train["weight"].sum())], "tree/WLS scales", 1e-8)
        _, _, target_before = previous.rank_inputs(full_train)
        retained_dates = train["trade_date"].unique().sort().to_list()
        metadata = {"retained_training_rows": len(train), "retained_training_dates": len(retained_dates),
            "retained_date_values": retained_dates, "excluded_degenerate_dates": dropped,
            "input_rows": len(full_train), "finite_target_rows_before_group_filter": int(target_before.sum()),
            "input_dates": full_train["trade_date"].n_unique(), "feature_names": names + ["r4_percentile"],
            "matrix_dtype": "float32", "matrix_order": "C", "target_anchor_weight_dtype": "float64",
            "initial_increment": 0., "init_score": None, "boost_from_average": False, "versions": versions}
        match(metadata, fold["training"]["core_metadata"], "independent common preparation metadata", 0.)
        matrix_digest = hashlib.sha256(f"float32|{(len(train), 64)}|".encode("ascii"))
        for source_year in sorted(set(map(int, full_train["trade_date"].to_numpy() // 10000))):
            part = full_train.filter(pl.col("trade_date") // 10000 == source_year)
            b, _, target = previous.rank_inputs(part)
            selected = target & np.isin(part["trade_date"].to_numpy(), retained_dates)
            # Strict monotonicity applies to all price-valid training rows.
            price = part["price_valid"].to_numpy()
            previous.require_monotonic(b[price], calibration["intercept"] + calibration["slope"] * b[price])
            x = previous.load_features(part, names)
            matrix = np.ascontiguousarray(np.column_stack([x[selected], b[selected].astype(np.float32)]), dtype=np.float32)
            matrix_digest.update(memoryview(matrix).cast("B"))
            del x, matrix, part
        if matrix_digest.hexdigest() != fold["training"]["matrix_sha256"]:
            raise AssertionError("Independent selected 64-column Float32 training matrix differs")
        actual_rows = saved
        del full_train, train
        b, _, _ = previous.rank_inputs(frame)
        price = frame["price_valid"].to_numpy()
        zero = np.full(len(frame), -10., dtype=np.float64)
        zero[price] = calibration["intercept"] + calibration["slope"] * b[price]
        previous.require_monotonic(b[price], zero[price])
        x = previous.load_features(frame, names)
        matrix = np.ascontiguousarray(np.column_stack([x[price], b[price].astype(np.float32)]), dtype=np.float32)
        raw = {"zero": zero}
        for arm in ("mse", "rankic"):
            model = lgb.Booster(model_str=(directory / f"model_{arm}.txt").read_text(encoding="utf-8"))
            if model.num_feature() != 64 or model.feature_name() != names + ["r4_percentile"]:
                raise AssertionError("Reloaded model feature identity changed")
            verify_fit_metadata(arm, fold["training"]["fit"][arm], model, actual_rows, versions)
            raw[arm] = zero.copy()
            raw[arm][price] += np.asarray(model.predict(matrix, num_threads=4), dtype=np.float64)
        del x, matrix, actual_rows, saved, model
        prediction = canonical(pl.read_parquet(directory / "predictions.parquet"))
        extras = {"b", "zero_raw", "mse_raw", "rankic_raw"}
        if stage != "inner":
            extras |= {"mse_pred", "rankic_pred"}
        if (set(prediction.columns) != set(frame.columns) | extras
                or not prediction.select(frame.columns).equals(frame)):
            raise AssertionError("Saved prediction changed original fields or omitted validation keys/dates")
        maxima["raw_and_post"] = max(maxima["raw_and_post"], close_arrays(b, prediction["b"], "independent inference b", 0.))
        for arm in ARMS:
            if not np.isfinite(raw[arm]).all() or not np.all(raw[arm][~price] == -10.):
                raise AssertionError("Nonfinite raw inference or invalid-price sentinel changed")
            maxima["raw_and_post"] = max(maxima["raw_and_post"], close_arrays(raw[arm], prediction[f"{arm}_raw"], f"{fold_id}/{arm} reload", 0.))
        daily, mechanism = independent_mechanism(frame, raw)
        recorded = pl.read_csv(directory / "mechanism_daily.csv")
        if set(daily.columns) != set(recorded.columns):
            raise AssertionError("Mechanism daily column set differs")
        maxima["mechanism"] = max(maxima["mechanism"], close_arrays(daily.to_numpy(), recorded.select(daily.columns).to_numpy(), "complete mechanism daily"))
        maxima["mechanism"] = max(maxima["mechanism"], match(mechanism, fold["mechanism"], "three-arm mechanism summary"))
        daily.write_csv(destination_dir / f"{stage}_{fold_id}_mechanism.csv", float_precision=17)
        mechanisms[fold_id] = daily
        rebuilt = {"fold_id": fold_id, "year": year, "mechanism": mechanism, "metrics": {}}
        checks[fold_id] = {"original_float64_labels_ranks_and_wls": True, "strict_global_label_maturity": True,
            "complete_validation_keys_and_dates": True, "common_degenerate_date_filter_and_weights": True,
            "training_matrix_sha256": matrix_digest.hexdigest(), "both_models_reloaded_without_refit": True,
            "raw_predictions_exact": True, "official_scoring_performed": stage != "inner"}
        if stage != "inner":
            close_arrays(rebuild_post(frame, zero), frame["pred"], "actual calibrated zero equals r4 final", 0.)
            checks[fold_id]["zero_final_exact_r4"] = True
            for arm in ("mse", "rankic", *REFERENCES):
                if arm in ("mse", "rankic"):
                    final = rebuild_post(frame, raw[arm])
                    maxima["raw_and_post"] = max(maxima["raw_and_post"], close_arrays(final, prediction[f"{arm}_pred"], f"{fold_id}/{arm} independent post", 0.))
                    scored = frame.select(KEYS).with_columns(pl.Series("pred", final))
                elif arm == "ensemble4":
                    scored = frame.select(KEYS + ["pred"])
                else:
                    scored = canonical(pl.read_parquet(R4 / f"predictions_baseline_{year}.parquet")).select(KEYS + ["pred"])
                metrics, evidence, details = _score_frames(scored, frame.select(KEYS + ["y_ret_1d", "flag_limit_up"]))
                maxima["official_metrics"] = max(maxima["official_metrics"], match(metrics, fold["metrics"][arm], f"{fold_id}/{arm} official"))
                recorded = pl.read_csv(directory / f"daily_{arm}.csv")
                if evidence.columns != recorded.columns:
                    raise AssertionError("Official daily schema differs")
                maxima["daily_official"] = max(maxima["daily_official"], close_arrays(evidence.to_numpy(), recorded.to_numpy(), f"{fold_id}/{arm} official daily"))
                evidence.write_csv(destination_dir / f"{stage}_{fold_id}_{arm}_official.csv", float_precision=17)
                official_daily[arm][year] = evidence
                rebuilt["metrics"][arm] = metrics
                checks[fold_id][f"official_{arm}"] = details
        audited.append(rebuilt)
        print(json.dumps({"independent_fold_completed": fold_id}), flush=True)
    gate = inner_gate(mechanisms) if stage == "inner" else full_gate(audited, stage)
    match(gate, record["gate"], "independent stage gate")
    bootstrap = None
    if stage != "inner" and gate["point_passed"]:
        bootstrap = {ref: paired_block_bootstrap(official_daily["rankic"], official_daily[ref],
            block_days=20, draws=20000, seed=2026) for ref in REFERENCES}
    match(bootstrap, record["bootstrap"], "independent stage bootstrap")
    passed = stage_pass(stage, gate, bootstrap)
    match(passed, record["passed"], "stage qualification")
    # Bind exactly the files audited, and detect changes during the run.
    check_hashes(ROOT, artifacts)
    for path in destination_dir.glob(f"{stage}_*.csv"):
        artifacts[path.relative_to(ROOT).as_posix()] = sha(path)
    result = {"status": "passed", "status_meaning": "Independent evidence agreement, not candidate qualification",
        "stage": stage, "candidate_key": "rankic", "folds": list(STAGES[stage]), "stage_gate_passed": passed,
        "stage_record_sha256": stage_digest, "protocol_sha256": protocol_sha, "source_sha256": sha(Path(__file__)),
        "gate": gate, "bootstrap": bootstrap, "fold_results": audited, "checks": checks,
        "max_absolute_difference": maxima, "artifacts_sha256": artifacts,
        "historical_years_previously_viewed": True, "automatic_publication": False,
        "limitation": "Independent data/ranks/WLS/weights/matrix and saved-model inference; no tree refit or recovery of an unseen holdout. Inner stage contains no official scoring."}
    with destination.open("x", encoding="utf-8") as stream:
        json.dump(result, stream, ensure_ascii=False, indent=2, allow_nan=False)
    return result


def synthetic_tests() -> dict:
    """No file reads, model fitting, historical labels or candidate scoring."""
    import copy
    import warnings
    checks = {}

    def rejects(operation):
        try:
            operation()
        except (ValueError, AssertionError, RuntimeError):
            return
        raise AssertionError("Invalid synthetic case was accepted")

    records = []
    for day, date in enumerate((20200102, 20200103, 20200106, 20200107, 20200108)):
        for i in range(4):
            records.append({"ts_code": str(i), "trade_date": date, "price_valid": True,
                "pred_raw": 1. if day == 2 else float(i + 1),
                "y_ret_1d": (.1 if day == 1 else None if day == 3 and i else float(i + 1)),
                "flag_limit_up": 0})
    frame = pl.DataFrame(records).with_columns(pl.col("y_ret_1d").cast(pl.Float64))
    train, fitted, dropped = independent_training(frame)
    assert train["trade_date"].unique().sort().to_list() == [20200102, 20200108]
    assert [value["trade_date"] for value in dropped] == [20200103, 20200106, 20200107]
    close_arrays(train["weight"].to_numpy(), np.ones(8), "joint retained-date weights", 0.)
    close_arrays([fitted["intercept"], fitted["slope"]], [0., 1.], "independent retained-date WLS")
    assert train.schema["target_u"] == pl.Float64 and train.schema["anchor"] == pl.Float64
    checks["same_degenerate_date_exclusion_before_wls_and_weights"] = True
    altered = frame.with_columns(pl.lit(None, dtype=pl.Float64).alias("y_ret_1d"))
    close_arrays(previous.rank_inputs(frame)[0], previous.rank_inputs(altered)[0], "label-free base percentile", 0.)
    rejects(lambda: independent_training(altered))
    checks["base_rank_independent_of_labels_and_empty_target_rejected"] = True
    available = previous.label_available_dates(np.array([20201230, 20201231]), np.array([20201230, 20201231, 20210104]))
    assert (available < 20210104).tolist() == [True, False]
    checks["global_next_market_date_strict_maturity"] = True
    weight = previous.date_balanced_weights(np.array([1, 1, 2, 2, 2]))
    close_arrays(weight, [1.25, 1.25, 5/6, 5/6, 5/6], "mean-one unequal-date weights")
    assert abs(weight[:2].sum() - weight[2:].sum()) < 1e-15
    checks["unequal_size_dates_have_equal_total_weight"] = True

    evaluation = pl.DataFrame({"ts_code": [f"S{i:02}" for i in range(40)],
        "trade_date": [20210401] * 40, "price_valid": [True] * 40,
        "pred_raw": np.arange(40, dtype=np.float64), "y_ret_1d": np.arange(40, dtype=np.float64),
        "flag_limit_up": np.arange(40) % 2})
    baseline = np.arange(1, 41, dtype=np.float64) / 40
    raw = {"zero": baseline, "mse": baseline.copy(), "rankic": baseline[::-1].copy()}
    daily, mechanism = independent_mechanism(evaluation, raw)
    close_arrays([mechanism["raw_ic"]["zero"], mechanism["raw_ic"]["rankic"]], [1., -1.], "same-pool raw IC")
    assert daily["n_target"].to_list() == [40]
    assert daily.columns == ["trade_date", "n_target", "mse_zero", "mse_mse", "mse_rankic", "raw_ic_zero", "raw_ic_mse", "raw_ic_rankic"]
    checks["mechanism_keeps_limit_up_rows_and_exact_three_arm_schema"] = True
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        rejects(lambda: independent_mechanism(evaluation, {**raw, "rankic": np.ones(40)}))
    rejects(lambda: independent_mechanism(evaluation.head(29), {key: value[:29] for key, value in raw.items()}))
    checks["invalid_evaluation_days_fail_without_deletion"] = True

    def fake_quarters(values, lengths=(1, 1, 1, 1)):
        result = {}
        for index, (fold_id, value, length) in enumerate(zip(STAGES["inner"], values, lengths)):
            result[fold_id] = pl.DataFrame({"trade_date": np.arange(length) + index * 1000,
                "raw_ic_zero": [0.] * length, "raw_ic_mse": [0.] * length,
                "raw_ic_rankic": [float(value)] * length})
        return result

    assert inner_gate(fake_quarters((.004, .004, .004, 0.)))["passed"]
    assert not inner_gate(fake_quarters((.004, .004, 0., 0.)))["passed"]
    uneven = inner_gate(fake_quarters((.05, .0001, .0001, -.00199), (1, 1, 1, 100)))
    assert uneven["comparisons"]["zero"]["positive_quarters"] == 3 and not uneven["passed"]
    assert not inner_gate(fake_quarters((.02, .02, .02, -.00201)))["passed"]
    rejects(lambda: inner_gate(dict(list(fake_quarters((.1, .1, .1, .1)).items())[:3])))
    rejects(lambda: inner_gate(fake_quarters((.1, .1, .1, np.nan))))
    checks["inner_gate_uses_pooled_days_strict_positive_and_complete_quarters"] = True

    def full_folds(stage):
        return [{"fold_id": fold_id, "year": fold_layout(fold_id)[1],
            "metrics": {key: {"final_score": .405 if key == "rankic" else .4,
                               "ic_mean": .105 if key == "rankic" else .1}
                        for key in ("rankic", "mse", *REFERENCES)},
            "mechanism": {"raw_ic": {"zero": .1, "mse": .101, "rankic": .105}}}
                for fold_id in STAGES[stage]]

    folds = full_folds("development")
    gate = full_gate(folds, "development")
    assert gate["point_passed"]
    bad = copy.deepcopy(folds)
    bad[0]["mechanism"]["raw_ic"]["mse"] = .106
    assert not full_gate(bad, "development")["point_passed"]
    bad = copy.deepcopy(folds)
    bad[0]["metrics"]["baseline"]["final_score"] = .405
    assert not full_gate(bad, "development")["point_passed"]
    bad = copy.deepcopy(folds)
    bad[0]["metrics"]["rankic"]["ic_mean"] = np.nan
    rejects(lambda: full_gate(bad, "development"))
    assert full_gate(full_folds("extension"), "extension")["point_passed"]
    checks["full_gate_requires_both_official_and_both_mechanism_controls"] = True

    boot = {reference: {"block_days": 20, "draws": 20000, "seed": 2026,
            "years": [2022], "bootstrap_share_positive": .8} for reference in REFERENCES}
    assert stage_pass("development", gate, boot)
    failed = copy.deepcopy(gate)
    failed["point_passed"] = False
    assert stage_pass("development", failed, None) is False
    rejects(lambda: stage_pass("development", failed, boot))
    rejects(lambda: stage_pass("development", gate, None))
    rejects(lambda: stage_pass("development", gate, {"ensemble4": boot["ensemble4"]}))
    bad = copy.deepcopy(boot)
    bad["baseline"]["bootstrap_share_positive"] = np.nan
    rejects(lambda: stage_pass("development", gate, bad))
    bad["baseline"]["bootstrap_share_positive"] = .79999
    assert not stage_pass("development", gate, bad)
    assert stage_pass("inner", {"passed": False}, None) is False
    rejects(lambda: stage_pass("inner", {"passed": True}, boot))
    checks["point_fail_stops_bootstrap_and_inner_never_bootstraps"] = True
    checks["bootstrap_exact_both_references_finite_shares_and_years"] = True
    from unittest.mock import patch
    failed_record = {"gate": {"passed": False}, "bootstrap": None, "passed": False}
    with patch.multiple(sys.modules[__name__],
            checked_stage=lambda *args: (failed_record, [], {}),
            gate_from_saved=lambda *args: {"passed": False},
            read=lambda *args: (_ for _ in ()).throw(AssertionError("No later audit may be read"))):
        try:
            authorize_previous("development", "protocol", {})
        except RuntimeError as error:
            assert "Failed inner" in str(error)
        else:
            raise AssertionError("Failed inner allowed later-stage access")
    checks["failed_inner_stops_before_later_artifact_access"] = True
    passed_record = {"gate": {"passed": True}, "bootstrap": None, "passed": True}
    fake_audit = {"status": "passed", "stage_gate_passed": True, "stage": "inner", "candidate_key": "rankic",
        "folds": list(STAGES["inner"]), "protocol_sha256": "protocol", "stage_record_sha256": "digest",
        "source_sha256": "digest", "gate": {"passed": True}, "bootstrap": None, "artifacts_sha256": {}}
    with patch.multiple(sys.modules[__name__],
            checked_stage=lambda *args: (passed_record, [], {"required_fold": "digest"}),
            gate_from_saved=lambda *args: {"passed": True},
            read=lambda *args: fake_audit, sha=lambda *args: "digest"):
        rejects(lambda: authorize_previous("development", "protocol", {"required_input": "digest"}))
    checks["prerequisite_audit_self_reported_subset_rejected"] = True
    return {"status": "passed", "test_count": len(checks), "checks": checks,
            "historical_data_read": False, "models_trained": False, "official_scores_computed": False}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("stage", nargs="?", choices=tuple(STAGES))
    parser.add_argument("--test", action="store_true", help="Synthetic checks only; never read historical candidate data")
    args = parser.parse_args()
    if args.test:
        if args.stage:
            parser.error("--test cannot be combined with a historical stage")
        result = synthetic_tests()
    else:
        if args.stage is None:
            parser.error("Choose inner/development/extension or --test")
        result = audit(args.stage)
    print(json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False))


if __name__ == "__main__":
    main()
