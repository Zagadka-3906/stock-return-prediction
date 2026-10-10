"""Frozen three-arm RankIC experiment with an audited inner walk-forward stop."""
from __future__ import annotations

import os
for _name in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "POLARS_MAX_THREADS"):
    os.environ[_name] = "8"
import argparse
from datetime import datetime, timezone
import gc
import importlib.metadata
import json
from pathlib import Path
import sys
import time

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import lightgbm as lgb
import numpy as np
import polars as pl
from scipy.stats import spearmanr
from experiments import r9_residual as prior
from experiments import r9_residual_core as old_core
from experiments import r10_rankic_core as core
from experiments.r8_diagnose_and_speed import sha, read, write_new, save_frame, hash_map, verify_map, log
from experiments.r8_fast_official import PreparedOfficialPanel
from experiments.audit_r5_candidate import paired_block_bootstrap

OUT = ROOT / "experiments/r10_rankic_20260927"
R4 = prior.R4
RESEARCH = ROOT / "experiments/research_r10_20260926"
PRIMARY = "rankic"
STAGES = ("inner", "development", "extension")
ARMS = ("zero", "mse", "rankic")
SOURCES = ("r10_rankic.py", "r10_rankic_core.py", "r10_rankic_audit.py", "r10_rankic_design.md", "r10_rankic_requirements.txt")
GATES = {
    "inner": {"mean_raw_ic_delta_min": .001, "positive_quarters_min": 3, "worst_quarter_delta_min": -.002},
    "development": {"mean_score_delta_min": .001, "mean_ic_delta_min": -.002, "raw_ic_delta_min": .001},
    "extension": {"mean_score_delta_min": .0005, "worst_year_score_delta_min": -.003,
                  "mean_ic_delta_min": -.002, "raw_ic_delta_min": 0., "worst_year_raw_ic_delta_min": -.002},
    "bootstrap": {"block_days": 20, "draws": 20000, "seed": 2026, "positive_share_min": .8},
}


def relative(path):
    return Path(path).resolve().relative_to(ROOT).as_posix()


def specs(stage):
    if stage == "inner":
        return [{"fold_id": f"inner_2021q{q}", "stage": stage, "year": 2021, "quarter": q,
                 "start": a, "end": b} for q, (a, b) in enumerate(
                     [(20210101, 20210331), (20210401, 20210630), (20210701, 20210930), (20211001, 20211231)], 1)]
    years = {"development": [2022], "extension": [2023, 2024]}[stage]
    return [{"fold_id": f"{stage}_{year}", "stage": stage, "year": year, "quarter": None,
             "start": year*10000+101, "end": year*10000+1231} for year in years]


def fold_dir(fold_id):
    allowed = {s["fold_id"] for stage in STAGES for s in specs(stage)}
    if fold_id not in allowed:
        raise ValueError("Unknown fold")
    return OUT / "folds" / fold_id


def required_artifacts(spec):
    names = ["calibration.json", "training_rows.parquet", "model_mse.txt", "model_rankic.txt",
             "predictions.parquet", "mechanism_daily.csv"]
    if spec["stage"] != "inner":
        names += [f"daily_{name}.csv" for name in ("mse", "rankic", "ensemble4", "baseline")]
    return [fold_dir(spec["fold_id"]) / name for name in names]


def training_frame(spec, market_dates):
    year = spec["year"]
    validation = prior.load_year(year).filter(pl.col("trade_date").is_between(spec["start"], spec["end"]))
    if validation.is_empty():
        raise ValueError("Empty validation window")
    first = int(validation["trade_date"].min())
    source_years = list(range(2020, year + (spec["stage"] == "inner")))
    full = pl.concat([prior.load_year(y) for y in source_years]).sort("trade_date", "ts_code")
    # Remove all later signals before applying the strictly mature-label rule.
    full = full.filter(pl.col("trade_date") < first)
    keep, available = prior.mature_mask(full["trade_date"].to_numpy(), market_dates, first)
    train = full.filter(pl.Series(keep))
    if train.is_empty():
        raise ValueError("Empty mature training window")
    boundaries = {"validation_first": first, "validation_last": int(validation["trade_date"].max()),
        "first_training_signal": int(train["trade_date"].min()), "last_training_signal": int(train["trade_date"].max()),
        "last_label_available": int(available[keep].max()),
        "training_oof_years": sorted(set(map(int, train["trade_date"].to_numpy() // 10000))),
        "purged_signal_dates": sorted(set(map(int, full["trade_date"].to_numpy()[~keep]))),
        "purged_panel_rows": int((~keep).sum()), "retained_panel_rows": len(train),
        "strict_next_market_date_before_validation": True, "no_post_validation_training": True,
        "degenerate_training_days": "Separate common core mask before calibration, recorded in training.core_metadata"}
    if boundaries["last_label_available"] >= first:
        raise AssertionError("Immature label")
    return train, validation, boundaries


def mechanism(frame, signals):
    target = old_core.target_percentile(frame)
    dates = frame["trade_date"].to_numpy()
    rows = []
    for date in np.unique(dates):
        mask = (dates == date) & np.isfinite(target)
        if mask.sum() < 30:
            raise ValueError("Fewer than 30 target-valid evaluation rows; never drop a bad date")
        row = {"trade_date": int(date), "n_target": int(mask.sum())}
        for arm in ARMS:
            score = np.asarray(signals[arm])[mask]
            if not np.isfinite(score).all() or np.ptp(score) == 0 or np.ptp(target[mask]) == 0:
                raise ValueError("Undefined evaluation IC; no date deletion allowed")
            row[f"mse_{arm}"] = float(np.mean((score-target[mask])**2))
            row[f"raw_ic_{arm}"] = float(spearmanr(score, target[mask]).statistic)
        rows.append(row)
    table = pl.DataFrame(rows)
    result = {"days": len(table), "mse": {arm: float(table[f"mse_{arm}"].mean()) for arm in ARMS},
              "raw_ic": {arm: float(table[f"raw_ic_{arm}"].mean()) for arm in ARMS}}
    for ref in ("zero", "mse"):
        result[f"delta_vs_{ref}"] = result["raw_ic"]["rankic"] - result["raw_ic"][ref]
    if not all(np.isfinite(x) for group in (result["mse"], result["raw_ic"]) for x in group.values()):
        raise ValueError("Nonfinite mechanism statistics")
    return result, table


def inner_gate(folds):
    if [f["fold_id"] for f in folds] != [s["fold_id"] for s in specs("inner")]:
        raise AssertionError("All four ordered quarters required")
    result = {}
    for ref in ("zero", "mse"):
        deltas = {f["fold_id"]: f["mechanism"][f"delta_vs_{ref}"] for f in folds}
        days = sum(f["mechanism"]["days"] for f in folds)
        mean = sum(f["mechanism"]["days"]*f["mechanism"][f"delta_vs_{ref}"] for f in folds)/days
        positive, worst = sum(value > 0 for value in deltas.values()), min(deltas.values())
        passed = (mean >= .001 and positive >= 3 and worst >= -.002)
        result[ref] = {"mean_raw_ic_delta": float(mean), "quarter_deltas": deltas,
                       "positive_quarters": positive, "worst_quarter_delta": worst, "passed": bool(passed)}
    return {"comparisons": result, "passed": all(v["passed"] for v in result.values())}


def full_gate(folds, stage):
    if stage not in ("development", "extension") or [f["fold_id"] for f in folds] != [s["fold_id"] for s in specs(stage)]:
        raise AssertionError("Wrong full-year fold scope")
    threshold = GATES[stage]
    official, mechanistic = {}, {}
    for ref in ("ensemble4", "baseline"):
        delta = {str(f["year"]): f["metrics"]["rankic"]["final_score"]-f["metrics"][ref]["final_score"] for f in folds}
        mean, worst = float(np.mean(list(delta.values()))), min(delta.values())
        ic = float(np.mean([f["metrics"]["rankic"]["ic_mean"]-f["metrics"][ref]["ic_mean"] for f in folds]))
        passed = mean >= threshold["mean_score_delta_min"] and ic >= threshold["mean_ic_delta_min"]
        if stage == "extension":
            passed &= worst >= threshold["worst_year_score_delta_min"]
        official[ref] = {"score_deltas": delta, "mean_score_delta": mean, "worst_year_score_delta": worst,
                         "mean_ic_delta": ic, "passed": bool(passed)}
    for ref in ("zero", "mse"):
        delta = {str(f["year"]): f["mechanism"][f"delta_vs_{ref}"] for f in folds}
        mean, worst = float(np.mean(list(delta.values()))), min(delta.values())
        passed = mean >= threshold["raw_ic_delta_min"]
        if stage == "extension":
            passed &= worst >= threshold["worst_year_raw_ic_delta_min"]
        mechanistic[ref] = {"annual_raw_ic_deltas": delta, "mean_raw_ic_delta": mean,
                            "worst_year_raw_ic_delta": worst, "passed": bool(passed)}
    a = {"comparisons": official, "passed": all(v["passed"] for v in official.values())}
    b = {"comparisons": mechanistic, "passed": all(v["passed"] for v in mechanistic.values())}
    return {"official": a, "mechanism": b, "point_passed": a["passed"] and b["passed"]}


def source_map():
    return hash_map([ROOT / "experiments" / name for name in SOURCES])


def runtime_versions():
    return {name: importlib.metadata.version(name) for name in ("numpy", "polars", "scipy", "lightgbm", "numba", "llvmlite")}


def verify_protocol():
    protocol = read(OUT / "protocol.json")
    if protocol["source_sha256"] != source_map() or protocol["gates"] != GATES:
        raise AssertionError("Frozen source or gates changed")
    verify_map(protocol["input_sha256"])
    if protocol["runtime_versions"] != runtime_versions() or protocol["params"] != core.PARAMS or protocol["rounds"] != core.ROUNDS:
        raise AssertionError("Runtime or tree configuration changed")
    return protocol


def check_fold(record, spec):
    for name in ("fold_id", "stage", "year", "quarter"):
        if record[name] != spec[name]:
            raise AssertionError("Fold identity differs")
    if record["protocol_sha256"] != sha(OUT / "protocol.json"):
        raise AssertionError("Fold protocol differs")
    expected = {relative(p) for p in required_artifacts(spec)}
    if set(record["artifact_sha256"]) != expected:
        raise AssertionError("Incomplete/extra fold evidence")
    verify_map(record["artifact_sha256"])
    b = record["boundaries"]
    if not b["last_label_available"] < b["validation_first"] or not all(record["tests"].values()):
        raise AssertionError("Invalid fold boundary or failed invariance")
    return record


def checked_stage(stage):
    record = read(OUT / f"{stage}.json")
    if (record["stage"] != stage or record["candidate_key"] != PRIMARY or
        record["protocol_sha256"] != sha(OUT / "protocol.json") or record["folds"] != [s["fold_id"] for s in specs(stage)]):
        raise AssertionError("Stage identity differs")
    expected = {relative(fold_dir(s["fold_id"]) / "fold.json") for s in specs(stage)}
    if set(record["fold_sha256"]) != expected:
        raise AssertionError("Wrong stage fold closure")
    verify_map(record["fold_sha256"])
    folds = [check_fold(read(fold_dir(s["fold_id"]) / "fold.json"), s) for s in specs(stage)]
    gate = inner_gate(folds) if stage == "inner" else full_gate(folds, stage)
    if gate != record["gate"]:
        raise AssertionError("Recorded gate does not follow verified folds")
    point = gate["passed"] if stage == "inner" else gate["point_passed"]
    bootstrap = record["bootstrap"]
    if stage == "inner" or not point:
        if bootstrap is not None:
            raise AssertionError("Unscheduled bootstrap")
        passed = point if stage == "inner" else False
    else:
        if not isinstance(bootstrap, dict) or set(bootstrap) != {"ensemble4", "baseline"}:
            raise AssertionError("Missing both bootstrap references")
        for ref, values in bootstrap.items():
            if ((values["block_days"], values["draws"], values["seed"]) != (20, 20000, 2026)
                    or values["years"] != [s["year"] for s in specs(stage)]
                    or not np.isfinite(values["bootstrap_share_positive"]) or not 0 <= values["bootstrap_share_positive"] <= 1):
                raise AssertionError("Bootstrap configuration or share invalid")
        passed = all(v["bootstrap_share_positive"] >= .8 for v in bootstrap.values())
    if record["passed"] != bool(passed):
        raise AssertionError("Incorrect stage qualification")
    return record


def require_audit(stage, require_pass=True):
    record = checked_stage(stage)
    if require_pass and not record["passed"]:
        raise RuntimeError(f"{stage} failed: later stages forbidden")
    audit = read(OUT / "independent_audit" / f"audit_{stage}.json")
    if (audit["status"] != "passed" or audit["stage"] != stage or audit["candidate_key"] != PRIMARY
            or audit["stage_gate_passed"] != record["passed"] or audit["protocol_sha256"] != sha(OUT / "protocol.json")
            or audit["stage_record_sha256"] != sha(OUT / f"{stage}.json")):
        raise AssertionError("Independent audit identity/status differs")
    needed = {relative(OUT / f"{stage}.json"), *record["fold_sha256"]}
    protocol = read(OUT / "protocol.json")
    needed.update(protocol["source_sha256"])
    needed.update(protocol["input_sha256"])
    for spec in specs(stage):
        needed.update(relative(p) for p in required_artifacts(spec))
    if not needed <= set(audit["artifacts_sha256"]):
        raise AssertionError("Independent audit omits bound inputs or evidence")
    verify_map(audit["artifacts_sha256"])
    return record


def guard(stage):
    if stage == "development":
        require_audit("inner")
    elif stage == "extension":
        require_audit("inner")
        require_audit("development")


def train_fold(spec, calendar):
    if spec not in specs(spec["stage"]):
        raise ValueError("Undeclared fold specification")
    verify_protocol()
    guard(spec["stage"])
    directory = fold_dir(spec["fold_id"])
    final = directory / "fold.json"
    if final.exists():
        return check_fold(read(final), spec)
    if directory.exists() and any(directory.iterdir()):
        raise FileExistsError("Incomplete fold preserved; no overwriting or silent retraining")
    started = time.monotonic()
    train, frame, bounds = training_frame(spec, calendar)
    x = prior.load_features(train)
    prepared = core.prepare(train, x, prior.feature_names())
    mask = prepared["mask"]
    calibration = prepared["calibration"]
    b = old_core.base_percentile(train)
    training_rows = train.select("ts_code", "trade_date").filter(pl.Series(mask)).with_columns(
        pl.Series("b", b[mask]), pl.Series("target_u", prepared["target"]), pl.Series("anchor", prepared["anchor"]),
        pl.Series("weight", prepared["weights"]))
    directory.mkdir(parents=True, exist_ok=True)
    save_frame(directory / "training_rows.parquet", training_rows)
    write_new(directory / "calibration.json", calibration)
    training = {"rows": int(mask.sum()), "dates": int(np.unique(prepared["dates"]).size),
        "matrix_sha256": prior.array_sha(prepared["matrix"]), "target_sha256": prior.array_sha(prepared["target"]),
        "anchor_sha256": prior.array_sha(prepared["anchor"]), "weight_sha256": prior.array_sha(prepared["weights"]),
        "core_metadata": prepared["metadata"], "fit": {}}
    models = {}
    for arm in ("mse", "rankic"):
        log(f"{spec['fold_id']} fitting {arm}: {training['rows']:,} rows / {training['dates']} dates")
        model, metadata = core.fit(prepared, arm)
        model_path = directory / f"model_{arm}.txt"
        with model_path.open("x", encoding="utf-8") as stream:
            stream.write(model.model_to_string())
        models[arm] = (model, lgb.Booster(model_str=model_path.read_text(encoding="utf-8")))
        training["fit"][arm] = metadata
    del prepared, training_rows, train, x, b
    gc.collect()
    x = prior.load_features(frame)
    signals = {"zero": old_core.predict_raw(frame, x, None, calibration)}
    poisoned = frame.with_columns(pl.lit(-98765.).alias("y_ret_1d"), pl.lit(False).alias("future_available"))
    prefix = min(50, frame["trade_date"].n_unique()) * frame["ts_code"].n_unique()
    for arm, (model, reloaded) in models.items():
        signals[arm] = old_core.predict_raw(frame, x, model, calibration)
        np.testing.assert_array_equal(signals[arm], old_core.predict_raw(frame, x, reloaded, calibration))
        np.testing.assert_array_equal(signals[arm], old_core.predict_raw(poisoned, x, model, calibration))
        np.testing.assert_array_equal(signals[arm][:prefix], old_core.predict_raw(frame.head(prefix), x[:prefix], model, calibration))
    for raw in signals.values():
        if not np.isfinite(raw).all() or not np.all(raw[~frame["price_valid"].to_numpy()] == -10):
            raise AssertionError("Invalid raw prediction")
    mechanistic, daily = mechanism(frame, signals)
    output = frame.with_columns(pl.Series("b", old_core.base_percentile(frame)),
                                 *[pl.Series(f"{arm}_raw", signals[arm]) for arm in ARMS])
    tests = {"model_reload_exact": True, "label_and_availability_invariance": True,
             "raw_prefix_50days_exact": True, "finite_invalid_price_excluded": True}
    metrics = {}
    if spec["stage"] != "inner":
        np.testing.assert_array_equal(old_core.prediction(frame, x, None, calibration), frame["pred"].to_numpy())
        tests["actual_zero_final_exact_r4"] = True
        context = PreparedOfficialPanel.from_frame(frame)
        for arm, (model, reloaded) in models.items():
            pred = old_core.prediction(frame, x, model, calibration)
            np.testing.assert_array_equal(pred, old_core.prediction(frame, x, reloaded, calibration))
            np.testing.assert_array_equal(pred, old_core.prediction(poisoned, x, model, calibration))
            np.testing.assert_array_equal(pred[:prefix], old_core.prediction(frame.head(prefix), x[:prefix], model, calibration))
            output = output.with_columns(pl.Series(f"{arm}_pred", pred))
            metrics[arm], official_daily = context.score(pred)
            save_frame(directory / f"daily_{arm}.csv", official_daily)
        tests["post_reload_label_prefix_exact"] = True
        for ref in ("ensemble4", "baseline"):
            original = pl.read_parquet(R4 / f"predictions_{ref}_{spec['year']}.parquet").sort("trade_date", "ts_code")
            if not original.select(prior.KEYS).equals(frame.select(prior.KEYS)):
                raise AssertionError("Reference keys differ")
            metrics[ref], official_daily = context.score(original["pred"].to_numpy())
            save_frame(directory / f"daily_{ref}.csv", official_daily)
    save_frame(directory / "predictions.parquet", output)
    save_frame(directory / "mechanism_daily.csv", daily)
    record = {**{k: spec[k] for k in ("fold_id", "stage", "year", "quarter")},
        "protocol_sha256": sha(OUT / "protocol.json"), "boundaries": bounds, "training": training,
        "mechanism": mechanistic, "metrics": metrics, "tests": tests,
        "artifact_sha256": hash_map(required_artifacts(spec)), "elapsed_seconds": time.monotonic()-started}
    write_new(final, record)
    log(f"{spec['fold_id']}: raw IC rankic={mechanistic['raw_ic']['rankic']:.8f}; delta zero={mechanistic['delta_vs_zero']:+.8f}; delta MSE={mechanistic['delta_vs_mse']:+.8f}")
    return record


def run_stage(stage):
    verify_protocol()
    guard(stage)
    destination = OUT / f"{stage}.json"
    if destination.exists():
        raise FileExistsError("Completed stage preserved")
    calendar = prior.calendar()
    folds = [train_fold(spec, calendar) for spec in specs(stage)]
    gate = inner_gate(folds) if stage == "inner" else full_gate(folds, stage)
    bootstrap = None
    if stage == "inner":
        passed = gate["passed"]
    elif gate["point_passed"]:
        candidate = {f["year"]: pl.read_csv(fold_dir(f["fold_id"]) / "daily_rankic.csv") for f in folds}
        bootstrap = {ref: paired_block_bootstrap(candidate,
            {f["year"]: pl.read_csv(fold_dir(f["fold_id"]) / f"daily_{ref}.csv") for f in folds},
            block_days=20, draws=20000, seed=2026) for ref in ("ensemble4", "baseline")}
        passed = all(v["bootstrap_share_positive"] >= .8 for v in bootstrap.values())
    else:
        passed = False
    record = {"stage": stage, "candidate_key": PRIMARY, "protocol_sha256": sha(OUT / "protocol.json"),
        "folds": [f["fold_id"] for f in folds], "fold_sha256": hash_map([fold_dir(f["fold_id"]) / "fold.json" for f in folds]),
        "gate": gate, "bootstrap": bootstrap, "passed": bool(passed),
        "historical_years_previously_viewed": True, "formal_promotion": False}
    verify_protocol()
    write_new(destination, record)
    return record


def synthetic_tests():
    from unittest.mock import patch
    folds = [{"fold_id": s["fold_id"], "mechanism": {"days": 60+i, "delta_vs_zero": .002, "delta_vs_mse": .002}}
             for i, s in enumerate(specs("inner"))]
    assert inner_gate(folds)["passed"]
    folds[-1]["mechanism"]["delta_vs_mse"] = -.0021
    assert not inner_gate(folds)["passed"]
    folds[-1]["mechanism"]["delta_vs_mse"] = .002
    folds[0]["mechanism"]["delta_vs_mse"] = 0.
    folds[1]["mechanism"]["delta_vs_mse"] = 0.
    assert not inner_gate(folds)["passed"]
    with patch(__name__ + ".require_audit", side_effect=RuntimeError("failed")) as required:
        try:
            guard("development")
        except RuntimeError:
            pass
        else:
            raise AssertionError("Inner failure allowed development")
        required.assert_called_once_with("inner")
    with patch(__name__ + ".verify_protocol"), patch(__name__ + ".require_audit", side_effect=RuntimeError("failed")):
        try:
            train_fold(specs("development")[0], np.array([], dtype=int))
        except RuntimeError:
            pass
        else:
            raise AssertionError("Direct fold call bypassed stage gate")
    unexpected = {OUT / "inner.json", fold_dir("extension_2023")}
    with patch(__name__ + ".verify_protocol"), patch(__name__ + ".require_audit", return_value={"stage": "inner", "passed": False}), \
            patch.object(Path, "exists", lambda path: path in unexpected):
        try:
            terminal_evidence()
        except AssertionError:
            pass
        else:
            raise AssertionError("Failed inner allowed extension artifacts after absent development")
    full = [{**s, "mechanism": {"delta_vs_zero": .002, "delta_vs_mse": .002},
             "metrics": {"rankic": {"final_score": .5, "ic_mean": .15},
                         "ensemble4": {"final_score": .49, "ic_mean": .15},
                         "baseline": {"final_score": .49, "ic_mean": .15}}} for s in specs("development")]
    assert full_gate(full, "development")["point_passed"]
    full[0]["mechanism"]["delta_vs_mse"] = .0009
    assert not full_gate(full, "development")["point_passed"]
    full[0]["mechanism"]["delta_vs_mse"] = .002
    full[0]["metrics"]["baseline"]["final_score"] = .5
    assert not full_gate(full, "development")["point_passed"]
    keep, available = prior.mature_mask(np.array([20201230, 20201231]),
                                        np.array([20201230, 20201231, 20210104]), 20210104)
    np.testing.assert_array_equal(keep, [True, False])
    assert available[keep].max() == 20201231
    return {"status": "passed", "all_four_quarters_required": True, "strict_positive_count": True,
            "each_reference_gate_required": True, "failed_inner_stops_before_development": True,
            "direct_fold_call_guarded": True, "failed_stage_rejects_nonadjacent_later_artifacts": True,
            "full_both_official_and_mechanism_references_required": True,
            "strict_label_maturity": True, "historical_training_performed": False}


def freeze():
    if OUT.exists() and any(OUT.iterdir()):
        raise FileExistsError("Existing experiment preserved")
    from experiments import r10_rankic_audit as auditor
    from experiments.finalize_r9 import verify as verify_previous
    tests = {"core": core.synthetic_tests(), "runner": synthetic_tests(), "audit": auditor.synthetic_tests()}
    assert all(result["status"] == "passed" for result in tests.values())
    previous = verify_previous()
    research = read(RESEARCH / "research_manifest.json")
    verify_map(research["artifact_sha256"])
    verify_map(research["context_sha256"])
    inputs = dict(read(prior.OUT / "protocol.json")["input_sha256"])
    inputs.update(read(prior.OUT / "protocol.json")["source_sha256"])
    inputs.update(research["artifact_sha256"])
    inputs.update(research["context_sha256"])
    extra = [prior.OUT / "result_manifest.json", RESEARCH / "research_manifest.json", ROOT / "experiments/finalize_r9.py"]
    for package in runtime_versions():
        distribution = importlib.metadata.distribution(package)
        extra += [Path(distribution.locate_file(p)) for p in distribution.files or [] if str(p).endswith(".dist-info/RECORD")]
    inputs.update(hash_map(extra))
    write_new(OUT / "tests.json", tests)
    inputs[relative(OUT / "tests.json")] = sha(OUT / "tests.json")
    protocol = {"experiment": "tie_aware_rankic_correction_with_matched_mse_control", "candidate_key": PRIMARY,
        "frozen_utc": datetime.now(timezone.utc).isoformat(), "stage_specs": {s: specs(s) for s in STAGES},
        "params": core.PARAMS, "rounds": core.ROUNDS, "pairs_per_row": 8, "sigmoid_scale": 1., "pair_seed": 2026,
        "feature_names": prior.feature_names(), "gates": GATES, "source_sha256": source_map(), "input_sha256": inputs,
        "runtime_versions": runtime_versions(), "previous_r9_verification": previous,
        "training": "Shared mature OOF rows; drop entire n<2 or constant b/u days before positive-slope date-equal WLS; 63+b Float32 inputs; original Float64 target/anchor/weights in custom objective; both residual heads start at zero.",
        "rankic_loss": "Per-day average-tie swap absolute weights, exact complete-pair sum normalization, Q=8*n uniformly sampled unordered pairs with replacement and M/Q; scale N/D, sigmoid=1, seed=[2026,iteration0,date]. Stop-gradient lambda. Twice diagonal sampled-pair Hessian majorizer, no per-row Hessian floor. Dynamic degenerate days zeroed with fixed N,D and logged; all-degenerate round fails.",
        "mse_loss": "g=N/(D*n)*(residual+anchor-u), h=N/(D*n); same retained rows, X, anchor and common tree params, no early stopping. Same numerical regularization does not imply equivalent effective regularization.",
        "stage_order": "Four raw-only quarterly inner folds, audit even on failure; only passed+audited inner permits 2022 development. Only passed+audited development permits 2023/24 historical extension. Bootstrap only full-year point-pass. No reselection of MSE control, weights, trees or features.",
        "time_boundary": "Full-market next trading date for Y maturity, strictly before first validation date. Past-only expanding training; no post-test training segment. Inner quarter raw-only avoids resetting R4 full-year post state.",
        "inference": "anchor=m(b) on full price-valid R4 pool; add saved residual tree output; no init_score, target or future availability in prediction. Full years retain R4 EMA/retention/protection/pooled exactly.",
        "historical_years_previously_viewed": True, "formal_promotion": False,
        "limitations": "Retrospective repeated-history study; selection bias remains. Bootstrap share is not alpha probability. Formula/audit success is not candidate qualification."}
    write_new(OUT / "protocol.json", protocol)
    return {"status": "frozen", "protocol_sha256": sha(OUT / "protocol.json")}


def terminal_evidence():
    verify_protocol()
    completed, failed = [], None
    for stage in STAGES:
        exists = (OUT / f"{stage}.json").exists()
        if failed is not None:
            if (exists or any(fold_dir(s["fold_id"]).exists() for s in specs(stage))
                    or (OUT / "independent_audit" / f"audit_{stage}.json").exists()):
                raise AssertionError("Evidence exists after failed stage")
            continue
        if not exists:
            break
        record = require_audit(stage, require_pass=False)
        completed.append(record)
        if not record["passed"]:
            failed = stage
    if not completed or (failed is None and len(completed) != len(STAGES)):
        raise RuntimeError("Required experiment stages or audits are incomplete")
    from experiments.finalize_r9 import verify as verify_previous
    previous = verify_previous()
    decision = {"status": "research_complete_no_promotion", "candidate_key": PRIMARY,
        "completed_stages": [v["stage"] for v in completed], "failed_stage": failed,
        "terminal_reason": f"{failed}_gate_failed" if failed else "historical_gates_passed_no_automatic_promotion",
        "audit_status": "passed", "historical_gates_passed": failed is None, "formal_promotion": False,
        "formal_release": "ensemble4_r4", "previous_r9_verification": previous}
    return completed, decision


def report_text(stages, decision):
    inner = stages[0]
    rows = []
    for spec in specs("inner"):
        fold = read(fold_dir(spec["fold_id"]) / "fold.json")
        m = fold["mechanism"]
        rows.append(f"| 2021 Q{spec['quarter']} | {m['raw_ic']['zero']:.9f} | {m['raw_ic']['mse']:.9f} | {m['raw_ic']['rankic']:.9f} | {m['delta_vs_zero']:+.9f} | {m['delta_vs_mse']:+.9f} |")
    a, b = (inner["gate"]["comparisons"][ref] for ref in ("zero", "mse"))
    text = f"""# R10 平均秩 RankIC 修正结果

内层2021年四季度扩窗：RankIC头相对零修正日期等权原始IC变化 **{a['mean_raw_ic_delta']:+.9f}**，相对同容量MSE头 **{b['mean_raw_ic_delta']:+.9f}**。内层门槛{'通过' if inner['passed'] else '未通过'}；独立审计通过。正式版本仍为r4。

| 验证窗口 | 零修正原始IC | MSE头原始IC | RankIC头原始IC | 相对零修正 | 相对MSE |
|---|---:|---:|---:|---:|---:|
{chr(10).join(rows)}

两个对照分别要求合并日期等权增量≥0.001、至少3/4季度严格正增量、最差季度≥−0.002。相对零修正正季度{a['positive_quarters']}个、最差{a['worst_quarter_delta']:+.9f}；相对MSE正季度{b['positive_quarters']}个、最差{b['worst_quarter_delta']:+.9f}。

仅训练此前已成熟标签的纠正r4折外记录，每个季度重新拟合共同正斜率WLS与两个7叶、80轮、学习率0.05的增量树头。两头特征、训练行、容量和推理初始项相同；MSE控制用Float64自定义梯度、零增量初始化，与旧r9控制的库内标签精度和初始项设置不同，不将两者混称同一模型。

RankIC方法用平均并列秩交换增益加权全截面成对logistic，每日完整权重和归一化；每轮每日期均匀有放回抽取8n对并补M/Q系数。完整分母用Fenwick计算；返回当前抽样局部损失的2倍对角Hessian上界。排名权重停止求导，因此是代理伪梯度，不是真实离散RankIC的普通梯度；局部损失下降不保证原始IC或总分提高。同数值L2不代表两损失有效正则完全相同。

季度筛选只评价原始分数，没有重置季度持仓去冒充r4全年后处理，也没有计算季度官方总分。只有内层与审计都通过才允许2022完整年度开发，后续通过才允许2023—2024历史扩展。所有阶段预声明停止，不选控制臂作替代赢家。
"""
    if not inner["passed"]:
        text += "\n内层失败后停止：未训练2022—2024新候选、未生成这些年份新预测、未计算新的官方综合分或bootstrap。不能将内层IC差解释为综合分差。\n"
    for stage in stages[1:]:
        text += f"\n## {stage['stage']}\n\n```json\n{json.dumps(stage['gate'], ensure_ascii=False, indent=2)}\n```\n\n完整阶段门槛：{stage['passed']}；重采样：{'未计算（点门槛失败）' if stage['bootstrap'] is None else '见阶段JSON'}。\n"
    text += f"""
最终状态：`{decision['terminal_reason']}`。审计重新从原CSV收益构造训练目标、平均秩、WLS、日期权重和64列输入，核验模型重载预测、机制量、时间边界、哈希闭包与完整阶段门槛；不以主程序自己的函数作为唯一复算。审计不重训树，也不证明候选具有泛化优势。

2020—2024均已反复查看，季度和历史扩展均不是新盲测；本次固定配置限制新增自由度，不能消除跨轮选择偏差。探针通过、独立复算一致及完整性通过不等于模型合格，也不证明可执行净收益。

证据：[冻结协议](protocol.json)、[内层结果](inner.json)、[独立审计](independent_audit/audit_inner.json)、[最终决定](decision.json)、[文件清单](result_manifest.json)。只读复核：`.venv\\Scripts\\python.exe -B -X utf8 experiments/r10_rankic.py verify`。源码、模型、预测及失败结果保留；不替换正式提交或报告。
"""
    return text


def inventory():
    paths = [p for p in OUT.rglob("*") if p.is_file() and p != OUT / "result_manifest.json"]
    paths += [ROOT / "experiments" / name for name in SOURCES]
    if any(p.name.endswith(".pending") for p in paths):
        raise AssertionError("Incomplete files remain")
    return hash_map(paths)


def seal():
    final_names = ("decision.json", "结论.md", "verification.json", "result_manifest.json")
    if any((OUT / name).exists() for name in final_names):
        raise FileExistsError("Final evidence preserved")
    stages, decision = terminal_evidence()
    write_new(OUT / "decision.json", decision)
    with (OUT / "结论.md").open("x", encoding="utf-8") as stream:
        stream.write(report_text(stages, decision))
    write_new(OUT / "verification.json", {"status": "passed", "audit_status": "passed",
        "decision_sha256": sha(OUT / "decision.json"), "candidate_qualified": decision["historical_gates_passed"],
        "formal_release_unchanged": True, "meaning": "Integrity and audit agreement, not generalization or promotion"})
    write_new(OUT / "result_manifest.json", {"protocol_sha256": sha(OUT / "protocol.json"), "artifact_sha256": inventory()})
    return {"status": "sealed", "failed_stage": decision["failed_stage"], "formal_release": "ensemble4_r4"}


def verify():
    manifest = read(OUT / "result_manifest.json")
    if manifest["artifact_sha256"] != inventory() or manifest["protocol_sha256"] != sha(OUT / "protocol.json"):
        raise AssertionError("Final inventory differs")
    stages, decision = terminal_evidence()
    if decision != read(OUT / "decision.json") or report_text(stages, decision) != (OUT / "结论.md").read_text(encoding="utf-8"):
        raise AssertionError("Final decision/report differs from evidence")
    verification = read(OUT / "verification.json")
    if verification["decision_sha256"] != sha(OUT / "decision.json") or verification["candidate_qualified"] != decision["historical_gates_passed"]:
        raise AssertionError("Verification decision differs")
    return {"status": "passed", "audit_status": "passed", "candidate_qualified": decision["historical_gates_passed"],
        "failed_stage": decision["failed_stage"], "formal_release": "ensemble4_r4", "active_release_unchanged": True,
        "read_only": True, "training_prediction_scoring_resampling_performed": False,
        "files_hashed": len(manifest["artifact_sha256"]), "result_manifest_sha256": sha(OUT / "result_manifest.json")}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("freeze", *STAGES, "test", "verify-inputs", "seal", "verify"))
    action = parser.parse_args().action
    operations = {"freeze": freeze, "test": synthetic_tests, "verify-inputs": verify_protocol, "seal": seal, "verify": verify}
    try:
        result = operations[action]() if action in operations else run_stage(action)
    except Exception as error:
        if (action in STAGES and (OUT / "protocol.json").exists()
                and not (OUT / "result_manifest.json").exists()):
            write_new(OUT / f"failure_{action}_{datetime.now(timezone.utc):%Y%m%dT%H%M%S%f}.json",
                {"action": action, "error_type": type(error).__name__, "message": str(error),
                 "protocol_sha256": sha(OUT / "protocol.json"), "source_sha256_at_failure": source_map(),
                 "partial_artifacts_preserved": True, "qualification": "incomplete, not passed"})
        raise
    print(json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False))
