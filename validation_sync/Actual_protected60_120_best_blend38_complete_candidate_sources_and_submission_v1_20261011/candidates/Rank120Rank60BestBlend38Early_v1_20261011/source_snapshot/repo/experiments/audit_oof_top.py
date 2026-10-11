"""OOF predicted-Top training weights versus the frozen pooled-RMS 25% head."""
from __future__ import annotations

import argparse
import gc
import hashlib
import json
from functools import lru_cache
from pathlib import Path

import lightgbm as lgb
import numpy as np
import polars as pl

from experiments import oof_top_models as models
from experiments import audit_return_pooled as pooled_audit
from experiments import return_pooled_models as reference_models
from experiments import return_head_scorefirst as reference_2024
from experiments import audit_return_head as protected
from tests.audit_predictions import check_feature_prefix, check_time_boundaries
from experiments.audit_top_weight import baseline_reload, production_integrity
from experiments.audit_top_internal import paired_intervals
from experiments.official_seed_development import official_score, original_labels
from src.research_stats import quantile_stats
from run import FEATURE_FILE, ROOT, feature_names, to_matrix
from src.scoring import Panel

OUT = ROOT / "experiments/oof_top_eval"
KEYS = ["ts_code", "trade_date"]
file_hash = models.file_hash


def read(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def prior_integrity() -> dict:
    path = ROOT / models.read_protocol()["prior_manifest"]
    expected = read(path)
    for relative, digest in expected.items():
        assert file_hash(ROOT / relative) == digest, f"Prior evidence changed: {relative}"
    counts = {}
    for relative in models.read_protocol()["prior_directories"]:
        folder = ROOT / relative
        prefix = folder.relative_to(ROOT).as_posix() + "/"
        actual = {p.relative_to(ROOT).as_posix() for p in folder.rglob("*") if p.is_file()}
        assert actual == {key for key in expected if key.startswith(prefix)}
        counts[prefix] = len(actual)
    assert read(ROOT / "experiments/return_head_eval" / "development.json")["primary_gate_passed"] is False
    decision = read(reference_2024.OUT / "decision.json")
    assert decision["recommended_for_next_version"] is True and decision["deployed_to_production"] is False
    failed = read(ROOT / "experiments/return_market_eval/decision.json")
    assert failed["adopt_new_candidate"] is False and failed["official_scores"] is None
    stable = read(ROOT / "experiments/return_market_stable_eval/decision.json")
    assert stable["recommended_for_next_version"] is False and stable["deployed_to_production"] is False
    assert stable["development_gate_passed"] is True and stable["diagnostic_2024_score_gate_passed"] is False
    pooled = read(reference_models.OUT / "decision.json")
    assert pooled["recommended_for_next_version"] is True and pooled["deployed_to_production"] is False
    return {"unchanged": True, "prior_files_checked": len(expected), "directory_file_counts": counts,
            "manifest_sha256": file_hash(path), "old_failed_rule_preserved": True,
            "previous_score_first_recommendation_preserved": True}


def independent_target(frame: pl.DataFrame) -> tuple[np.ndarray, dict]:
    """Polars aggregation/window implementation, independent of the trainer."""
    frame = frame.select("trade_date", pl.col("ret").cast(pl.Float32).cast(pl.Float64))
    bounds = frame.group_by("trade_date").agg(
        pl.col("ret").quantile(.01, interpolation="linear").alias("lo"),
        pl.col("ret").quantile(.99, interpolation="linear").alias("hi"))
    joined = frame.join(bounds, on="trade_date", how="left", validate="m:1", maintain_order="left")
    assert joined.select(frame.columns).equals(frame)
    joined = joined.with_columns(pl.col("ret").clip(pl.col("lo"), pl.col("hi")).alias("clipped"))
    joined = joined.with_columns(
        pl.col("clipped").mean().over("trade_date").alias("mu"),
        pl.col("clipped").std(ddof=0).over("trade_date").alias("sd"))
    joined = joined.with_columns(pl.when(pl.col("sd") <= 1e-12).then(0.)
        .otherwise(pl.col("clipped") - pl.col("mu")).alias("centered"))
    rms = float(joined.select(pl.col("centered").pow(2).mean().sqrt()).item())
    target = joined.select(
        (pl.lit(0.) if rms <= 1e-12 else pl.col("centered") / rms)
        .cast(pl.Float32).alias("target"))
    expected = (np.zeros(len(frame), dtype=np.float32) if rms <= 1e-12
                else target["target"].to_numpy())
    return expected, {"pooled_rms": rms, "rows": len(frame), "days": len(bounds),
        "nearconstant_days": joined.filter(pl.col("sd") <= 1e-12)["trade_date"].n_unique(),
        "all_rows_including_constant_day_zeros_in_rms_denominator": True}


def independent_top_flags(frame: pl.DataFrame) -> np.ndarray:
    """Independent Polars sort/window implementation, no labels or model helper."""
    eligible = frame.filter(pl.col("price_valid") & (pl.col("flag_limit_up") == 0))
    assert eligible["pred_raw"].is_finite().all()
    ordered = (frame.with_row_index("_row").filter(pl.col("price_valid") & (pl.col("flag_limit_up") == 0))
        .sort(["trade_date", "pred_raw", "ts_code"], descending=[False, True, False])
        .with_columns(pl.len().over("trade_date").alias("_n"),
                      pl.col("trade_date").cum_count().over("trade_date").alias("_ordinal")))
    chosen = ordered.filter(pl.col("_ordinal") <= pl.col("_n") // 10)["_row"].to_numpy()
    flags = np.zeros(len(frame), dtype=bool)
    flags[chosen] = True
    return flags


def tests() -> dict:
    protocol = models.read_protocol()
    assert protocol["target"] == reference_models.read_protocol()["target"]
    assert models.features_for_model() == feature_names()
    assert pooled_audit.tests() == read(reference_models.OUT / "tests.json")
    fixture = pl.DataFrame({
        "ts_code": [f"S{i:02d}" for i in range(23)],
        "trade_date": [20190102]*23, "price_valid": [True]*22+[False],
        "flag_limit_up": [0]*21+[1,0],
        "pred_raw": pl.Series([1.0]*21+[99.0,100.0], dtype=pl.Float32)})
    flags = independent_top_flags(fixture)
    assert np.array_equal(np.flatnonzero(flags), [0,1])
    assert np.array_equal(models.oof_top_flags(fixture), flags)
    assert not independent_top_flags(fixture.head(9)).any()
    altered = fixture.with_columns(pl.Series("y_ret_1d", [None, 99.0]+[0.0]*21))
    assert np.array_equal(models.oof_top_flags(altered), flags)
    assert np.array_equal(independent_top_flags(altered), flags)
    return {"status": "passed", "only_final_dataset_weights_change": True,
        "original_63_feature_causality_rechecked": pooled_audit.tests()["original_63_feature_causality_rechecked"],
        "purge_boundaries_rechecked": check_time_boundaries(),
        "independent_polars_top_fixture": True, "pre_label_filter_selection_fixture": True,
        "frozen_pooled_target_and_protected_prediction_tests_reproduced": True,
        "prior_integrity": prior_integrity(), "protocol_sha256": file_hash(OUT / "protocol.json"),
        "audit_source_sha256": file_hash(Path(__file__))}


def reference_artifacts(year: int) -> tuple[Path, dict, Path]:
    if year not in (2022,2023,2024):
        raise ValueError("Only predeclared years are permitted")
    folder = reference_models.OUT
    path = folder / ("diagnostic_2024.json" if year == 2024 else "development.json")
    record = read(path)["years"][str(year)]
    return folder, record["candidate"], folder / f"candidate_processed_{year}.parquet"


@lru_cache(maxsize=5)
def oof_checks(year: int) -> dict:
    protocol = models.read_protocol()
    boundary = protocol["oof"]["folds"][str(year)]
    cache = models.load_oof(year)
    model_path, _, meta_path = models.oof_paths(year)
    meta = read(meta_path)
    train = (pl.scan_parquet(FEATURE_FILE)
        .filter(pl.col("is_train") & (pl.col("trade_date") < boundary["training_cutoff_exclusive"])
                & pl.col("y_rank").is_not_null() & pl.col("price_valid"))
        .select(*KEYS, "y_rank").collect())
    assert len(train) == boundary["training_rows"]
    assert train["trade_date"].n_unique() == boundary["training_days"]
    assert train["trade_date"].min() == boundary["training_first_date"]
    assert train["trade_date"].max() == boundary["training_last_date"] < boundary["training_cutoff_exclusive"]
    assert boundary["training_cutoff_exclusive"] < boundary["prediction_first_date"]
    assert models.key_hash(train) == meta["training_keys_sha256"]
    assert train["y_rank"].dtype == pl.Float32
    assert hashlib.sha256(train["y_rank"].to_numpy().tobytes()).hexdigest() == meta["target_array_sha256"]
    assert meta["sample_weight"] is None and meta["target_is_cached_already_centered_y_rank"] is True
    del train
    # Deliberately select no actual labels or label-availability fields.
    block = (pl.scan_parquet(FEATURE_FILE)
        .filter(pl.col("is_train") & pl.col("trade_date").is_between(year*10000+101,year*10000+1231))
        .select(*KEYS,"price_valid","flag_limit_up").sort("trade_date","ts_code").collect())
    assert cache.select(KEYS).equals(block.select(KEYS))
    assert len(cache) == boundary["prediction_rows"] and cache["trade_date"].n_unique() == boundary["prediction_days"]
    frame = block.with_columns(cache["pred_raw"])
    flags = independent_top_flags(frame)
    assert np.array_equal(flags, cache["is_oof_top"].to_numpy())
    assert hashlib.sha256(flags.tobytes()).hexdigest() == meta["oof_top_flags_sha256"]
    assert int(flags.sum()) == meta["oof_top_rows"]
    assert not np.any(flags & (~frame["price_valid"].to_numpy() | (frame["flag_limit_up"].to_numpy() != 0)))
    # Fake returns and missingness can change, never the prediction-defined region.
    changed = frame.with_row_index("_i").with_columns(
        pl.when(pl.col("_i") % 3 == 0).then(None).otherwise(pl.col("_i") * .001).alias("y_ret_1d"),
        pl.when(pl.col("_i") % 7 == 0).then(None).otherwise(.2).alias("y_rank"))
    assert np.array_equal(models.oof_top_flags(changed), flags)
    assert np.array_equal(models.oof_top_flags(changed.with_columns(
        pl.lit(None,dtype=pl.Float64).alias("y_ret_1d"),pl.lit(None,dtype=pl.Float64).alias("y_rank"))),flags)
    assert np.array_equal(models.oof_top_flags(frame.reverse()), flags[::-1])
    prefix = frame.head(50*4650)
    assert np.array_equal(models.oof_top_flags(prefix), flags[:len(prefix)])
    # Independent saved model inference, feature order and invalid-price treatment.
    indices = np.linspace(0,len(frame)-1,4096,dtype=int)
    sample = (pl.scan_parquet(FEATURE_FILE)
        .filter(pl.col("is_train") & pl.col("trade_date").is_between(year*10000+101,year*10000+1231))
        .select(*KEYS,*feature_names()).sort("trade_date","ts_code").with_row_index("_row")
        .filter(pl.col("_row").is_in(indices.tolist())).collect())
    assert sample.select(KEYS).equals(frame.with_row_index("_row").filter(pl.col("_row").is_in(indices.tolist())).select(KEYS))
    model = lgb.Booster(model_str=model_path.read_text(encoding="utf-8"))
    assert model.feature_name() == feature_names() and model.num_trees() == 180
    expected = model.predict(to_matrix(sample,feature_names()),num_threads=16).astype(np.float32)
    expected[~frame["price_valid"].to_numpy()[indices]] = -1e6
    assert np.array_equal(expected,cache["pred_raw"].to_numpy()[indices])
    return {"year":year,"status":"passed","boundaries":boundary,
        "full_unlabeled_x_coverage_before_selection":True,"training_target_sha256":meta["target_array_sha256"],
        "independent_polars_top_reconstruction_exact":True,"oof_top_rows":int(flags.sum()),
        "selected_rows_not_required_to_have_future_labels":True,
        "label_values_and_missingness_perturbation_invariant":True,
        "prefix_50_days_and_row_permutation_invariant":True,"reload_check_rows":4096,"reload_max_abs_error":0.0}


def weight_checks(year: int, frame: pl.DataFrame, meta: dict) -> dict:
    blocks = models.read_protocol()["oof"]["outer_block_years"][str(year)]
    assert max(blocks) == year-1
    audits = {str(block):oof_checks(block) for block in blocks}
    # Audited caches contain all rows; reconstruct flags independently through a relational key join.
    full = pl.concat([pl.read_parquet(models.oof_paths(block)[1],columns=KEYS+["is_oof_top"]) for block in blocks])
    joined = frame.select(KEYS).join(full,on=KEYS,how="left",validate="1:1",maintain_order="left")
    assert joined.select(KEYS).equals(frame.select(KEYS)) and len(joined)==len(frame)
    warmup = joined["trade_date"].is_between(20180101,20181231).to_numpy()
    assert np.array_equal(joined["is_oof_top"].is_null().to_numpy(),warmup)
    flags = joined["is_oof_top"].fill_null(False).to_numpy()
    expected = np.ones(len(frame),dtype=np.float64)
    expected[flags] = 1.5
    raw_mean = float(expected.mean())
    expected = (expected/raw_mean).astype(np.float32)
    actual,stats = models.weights_for_frame(frame,year)
    assert np.array_equal(actual,expected) and stats == meta["weight_statistics"]
    assert hashlib.sha256(expected.tobytes()).hexdigest() == stats["weight_array_sha256"]
    assert hashlib.sha256(flags.tobytes()).hexdigest() == stats["top_flags_array_sha256"]
    assert not flags[warmup].any() and np.all(expected[warmup] == np.float32(1/raw_mean))
    assert abs(float(expected.mean(dtype=np.float64))-1) <= 1e-7
    assert np.isclose(float(expected[flags][0])/float(expected[~flags][0]),1.5,rtol=0,atol=1e-7)
    yearly = (joined.with_columns(pl.col("is_oof_top").fill_null(False),
            (pl.col("trade_date")//10000).alias("year"),pl.Series("weight",expected))
        .group_by("year").agg(pl.len().alias("training_rows"),pl.col("is_oof_top").sum().alias("top_rows"),
                            pl.col("weight").cast(pl.Float64).mean().alias("mean_normalized_weight")).sort("year"))
    return {"status":"passed","oof_blocks":audits,"weight_statistics":stats,
        "independent_weight_vector_exact":True,"weights_normalized_over_final_outer_rows":True,
        "initial_2018_raw_one_not_normalized_one":True,"target_stats_unweighted_unchanged":True,
        "year_breakdown":yearly.to_dicts()}


def target_checks(year: int) -> dict:
    fold = models.EXPECTED[year]
    frame = (pl.scan_parquet(FEATURE_FILE)
        .filter(pl.col("is_train") & (pl.col("trade_date") < fold["training_cutoff_exclusive"])
                & pl.col("y_rank").is_not_null() & pl.col("price_valid"))
        .select(*KEYS, "y_ret_1d").collect())
    assert frame["y_ret_1d"].dtype == pl.Float32
    dates, returns = frame["trade_date"].to_numpy(), frame["y_ret_1d"].to_numpy()
    assert np.isfinite(returns).all() and len(frame) == fold["training_rows"]
    assert frame["trade_date"].n_unique() == fold["training_days"]
    assert int(dates.min()) == fold["training_first_date"]
    assert int(dates.max()) == fold["training_last_date"] < fold["training_cutoff_exclusive"]
    expected, independent = independent_target(frame.select("trade_date", pl.col("y_ret_1d").alias("ret")))
    actual, stats = models._target_with_stats(dates, returns)
    tolerance = models.read_protocol()["target_audit_tolerance"]
    maximum_error = float(np.max(np.abs(actual.astype(float) - expected.astype(float))))
    assert np.allclose(actual, expected, rtol=tolerance["rtol"], atol=tolerance["atol"])
    assert maximum_error <= tolerance["max_abs_float32"]
    assert np.isclose(stats["pooled_rms_float64"], independent["pooled_rms"],
        rtol=tolerance["pooled_rms_rtol"], atol=tolerance["pooled_rms_atol"])
    meta = read(OUT / f"{models.MODEL_KEY}_{year}.json")
    assert stats == meta["target_stats"]
    sha = lambda values: hashlib.sha256(values.tobytes()).hexdigest()
    assert sha(actual) == stats["target_array_sha256"]
    assert sha(returns.astype(np.float32)) == stats["raw_return_float32_sha256"]
    assert sha(dates.astype(np.int64)) == stats["training_dates_int64_sha256"]
    key_sha = hashlib.sha256(frame.select(KEYS).write_csv().encode("utf-8")).hexdigest()
    assert key_sha == meta["training_keys_sha256"]
    _, old_stats = reference_models._target_with_stats(dates, returns)
    folder, _, _ = reference_artifacts(year)
    old_meta = read(folder / f"{reference_models.MODEL_KEY}_{year}.json")
    assert old_stats == old_meta["target_stats"]
    assert stats == old_stats
    weights = weight_checks(year, frame, meta)
    assert meta["sample_weight"] == models.read_protocol()["weighting"]
    assert old_meta["sample_weight"] is None
    # Cross-check all original columns/params, not only a verbal single-variable claim.
    assert meta["features"] == old_meta["features"] == feature_names()
    for key in ("params", "rounds", "seed", "threads", "training_filter",
                "training_cutoff_exclusive", "training_rows", "training_first_date",
                "training_last_date", "blend", "postprocess"):
        assert meta[key] == old_meta[key], key
    return {"training_only_independent_polars_reconstruction_passed": True,
            "training_rows": len(frame), "training_days": independent["days"],
            "training_keys_sha256": key_sha, "target_stats_exactly_reproduced": True,
            "target_array_sha256": stats["target_array_sha256"],
            "reference_target_reproduced_on_identical_training_rows": True,
            "reference_target_sha256": old_stats["target_array_sha256"],
            "training_inputs_and_order_hashes_match": True,
            "only_dataset_weights_differ_model_configuration_equal": True,
            "oof_region_and_weight_audit": weights,
            "max_abs_float32_target_difference": maximum_error, "tolerance": tolerance,
            "independent_pooled_rms": independent["pooled_rms"],
            "training_pooled_rms": stats["pooled_rms_float64"],
            "nearconstant_days": independent["nearconstant_days"],
            "global_scale_only_uses_filtered_training_labels": True}


def reload_checks(year: int, panel: Panel, ref_raw: np.ndarray, new_raw: np.ndarray) -> dict:
    original = feature_names()
    features = models.features_for_model()
    indices = np.linspace(0, len(panel.frame) - 1, 4096, dtype=int)
    sample = (pl.scan_parquet(FEATURE_FILE)
              .filter(pl.col("is_train") & pl.col("trade_date").is_between(year * 10000 + 101, year * 10000 + 1231))
              .select(*KEYS, *original).sort("trade_date", "ts_code").with_row_index("_index")
              .filter(pl.col("_index").is_in(indices.tolist())).collect())
    assert sample.select(KEYS).equals(panel.frame.with_row_index("_index")
        .filter(pl.col("_index").is_in(indices.tolist())).select(KEYS))
    joined = sample
    folder, _, _ = reference_artifacts(year)
    result = {"original_rank_backbone": baseline_reload(year, panel)}
    for name, names, path, raw in (
        ("reference_63_return_head", original, folder / f"{reference_models.MODEL_KEY}_{year}.txt", ref_raw),
        ("candidate_63_oof_top_weighted_return_head", features, OUT / f"{models.MODEL_KEY}_{year}.txt", new_raw),
    ):
        model = lgb.Booster(model_str=path.read_text(encoding="utf-8"))
        assert model.feature_name() == names and model.num_trees() == 180
        pred = model.predict(to_matrix(joined, names), num_threads=16).astype(np.float32)
        pred[~panel.frame["price_valid"].to_numpy()[indices]] = -1e6
        assert np.array_equal(pred, raw[indices])
        result[name] = {"rows": len(indices), "max_abs_error": 0.0,
                        "feature_order_and_180_trees_verified": True}
    return result


def predictions(year: int):
    panel = models.load_panel(year)
    assert not np.isfinite(panel.y).any()
    reference_raw = reference_models.load_raw(year, panel)
    candidate_raw = models.load_raw(year, panel)
    reloads = reload_checks(year, panel, reference_raw, candidate_raw)
    # BOTH heads use the same original rank backbone, never recursively blended.
    backbone = protected.predict(panel, None, False)
    predictions = {"reference": protected.predict(panel, reference_raw, True),
                   "candidate": protected.predict(panel, candidate_raw, True)}
    changed = Panel.from_frame(panel.frame.with_columns(pl.Series(
        "y_ret_1d", np.random.default_rng(260926).normal(size=len(panel.frame)))))
    rows = 50 * panel.rows_per_day
    prefix = Panel.from_frame(panel.frame.head(rows))
    block_checks = {}
    for name, raw in (("reference", reference_raw), ("candidate", candidate_raw)):
        pred = predictions[name]
        assert np.isfinite(pred).all()
        assert np.array_equal(pred, protected.predict(changed, raw, True))
        assert np.array_equal(pred[:rows], protected.predict(prefix, raw[:rows], True))
        block_checks[name] = protected.protected_checks(panel, raw, backbone, pred)
    _, _, frozen_path = reference_artifacts(year)
    frozen = pl.read_parquet(frozen_path)
    assert frozen.select(KEYS).equals(panel.frame.select(KEYS))
    assert np.array_equal(frozen["pred"].to_numpy(), predictions["reference"])
    identity = protected.official_top_identity_check(panel, predictions["reference"], predictions["candidate"])
    checks = {"prediction_labels_all_missing": True, "label_perturbation_invariant": True,
              "prefix_50_days_exact": True, "finite_all_rows": True,
              "reference_processed_predictions_match_frozen_exact": True,
              "both_heads_use_original_rank_state_no_recursive_blend": True,
              "protected_blocks": block_checks, "official_top_identity": identity}
    return panel, predictions, checks, reloads


def dependencies(years: tuple[int, ...]) -> dict:
    sources = {}
    for year in years:
        sources.update(models.fingerprint(year)["source_sha256"])
        for extension in ("txt", "parquet", "json"):
            path = OUT / f"{models.MODEL_KEY}_{year}.{extension}"
            sources[path.relative_to(ROOT).as_posix()] = file_hash(path)
    sources.update(read(ROOT / models.read_protocol()["prior_manifest"]))
    for path in (Path(__file__), OUT / "tests.json", ROOT / "tests/audit_predictions.py",
                 ROOT / "experiments/audit_return_head.py", ROOT / "experiments/audit_return_head_scorefirst.py",
                 ROOT / "experiments/audit_top_weight.py", ROOT / "experiments/audit_top_internal.py",
                 ROOT / "experiments/official_seed_development.py", ROOT / "experiments/cached_recheck.py",
                 ROOT / "report_analytics.py"):
        sources[path.relative_to(ROOT).as_posix()] = file_hash(path)
    return dict(sorted(sources.items()))


def evaluate_year(year: int) -> dict:
    target = target_checks(year)
    panel, predicted, checks, reloads = predictions(year)
    # Load evaluation labels only after all predictions/causality checks.
    labelled = Panel.from_frame(panel.frame.drop("y_ret_1d").join(original_labels(year),
        on=KEYS, how="left", validate="1:1", maintain_order="left"))
    assert labelled.frame.select(KEYS).equals(panel.frame.select(KEYS))
    record = {"rows": len(panel.frame), "days": len(panel.dates), "target_checks": target,
              "prediction_checks": checks, "model_reload_checks": reloads,
              "original_feature_causality": read(OUT / "tests.json")["original_63_feature_causality_rechecked"],
              "deciles": {}}
    daily = {}
    for name, pred in predicted.items():
        metrics, daily[name] = official_score(panel, pred, year)
        record[name] = metrics
        record["deciles"][name] = quantile_stats(labelled, pred)
        daily[name].write_csv(OUT / f"official_{name}_{year}_daily.csv")
        panel.frame.select(KEYS).with_columns(pl.Series("pred", pred)).write_parquet(OUT / f"{name}_processed_{year}.parquet")
        print(f"OFFICIAL {year}/{name}: score={metrics['final_score']:.12f}; IC={metrics['ic_mean']:.9f}; "
              f"excess={metrics['annual_excess']:.9f}; turnover={metrics['mean_turnover']:.9f}", flush=True)
    folder, expected, _ = reference_artifacts(year)
    assert set(expected) == set(record["reference"])
    assert all(abs(record["reference"][key] - value) <= 1e-12 for key, value in expected.items())
    frozen_daily = pl.read_csv(folder / f"official_candidate_{year}_daily.csv")
    assert frozen_daily.columns == daily["reference"].columns
    for column in frozen_daily.columns:
        assert np.allclose(frozen_daily[column].to_numpy(), daily["reference"][column].to_numpy(),
                           rtol=0, atol=1e-12, equal_nan=True)
    assert np.array_equal(daily["reference"]["turnover"].to_numpy(), daily["candidate"]["turnover"].to_numpy(), equal_nan=True)
    record["reference_official_metrics_and_daily_match_frozen"] = True
    record["official_turnover_top_identities_equal"] = checks["official_top_identity"]["daily_top_identities_exact"]
    record["official_daily_turnover_exact"] = True
    record["delta"] = {key: record["candidate"][key] - record["reference"][key] for key in record["reference"]}
    record["paired_uncertainty"] = paired_intervals(daily["candidate"], daily["reference"], record["delta"]["final_score"])
    record["score_components"] = {"ic": .4 * record["delta"]["ic_mean"],
                                   "annual_excess": .3 * record["delta"]["annual_excess"],
                                   "turnover": -.3 * record["delta"]["mean_turnover"]}
    assert abs(sum(record["score_components"].values()) - record["delta"]["final_score"]) < 1e-12
    first = {name: frame.row(0, named=True) for name, frame in daily.items()}
    n_ic = int(np.isfinite(daily["reference"]["rank_ic"].to_numpy()).sum())
    n_excess = int(np.isfinite(daily["reference"]["excess"].to_numpy()).sum())
    record["first_day_score_contribution"] = (
        .4 * (first["candidate"]["rank_ic"] - first["reference"]["rank_ic"]) / n_ic
        + 75.6 * (first["candidate"]["excess"] - first["reference"]["excess"]) / n_excess)
    record["all_integrity_and_causality_checks_passed"] = True
    record["passes_score_first_rule"] = record["delta"]["final_score"] > models.read_protocol()["rule"]["numerical_score_tolerance"]
    record["cold_start_note"] = "Full-year score retained; t2 sensitivity preserves original prediction state, not a restarted strategy."
    record["decile_note"] = "Auxiliary stable-tie ex-post quantiles; not official default sorting or executable net returns."
    return record


def run(stage: str) -> dict:
    protocol = models.read_protocol()
    if stage not in ("develop", "diagnose"):
        raise ValueError("Only predeclared development or gated diagnosis")
    years = (2022, 2023) if stage == "develop" else (2024,)
    if stage == "diagnose":
        models.diagnostic_gate()
    destination = OUT / ("development.json" if stage == "develop" else "diagnostic_2024.json")
    paths = [OUT / f"{name}_{year}{suffix}" for year in years for name, suffix in (
        ("official_reference", "_daily.csv"), ("official_candidate", "_daily.csv"),
        ("reference_processed", ".parquet"), ("candidate_processed", ".parquet"))]
    if destination.exists() or any(path.exists() for path in paths):
        raise FileExistsError("Preserve existing complete or partial audit evidence")
    assert read(OUT / "tests.json") == tests()
    before = dependencies(years)
    production_before, prior_before = production_integrity(), prior_integrity()
    result = {"experiment": protocol["experiment"], "candidate_key": models.CANDIDATE_KEY,
              "baseline_key": protocol["baseline_key"], "candidate_count": 1, "primary_years": [2022, 2023],
              "protocol_sha256": file_hash(OUT / "protocol.json"), "audit_source_sha256": file_hash(Path(__file__)),
              "model_fingerprints": {str(y): models.fingerprint(y)["fingerprint_sha256"] for y in years},
              "blend": protocol["blend"], "postprocess": protocol["postprocess"], "decision_rule": protocol["rule"],
              "production_before": production_before, "prior_before": prior_before,
              "limitations": protocol["limitations"], "official_daily_reconstruction_tolerance": 1e-12, "years": {}}
    for year in years:
        result["years"][str(year)] = evaluate_year(year)
        gc.collect()
    assert dependencies(years) == before
    result["artifacts_sha256"] = {**before, **{p.relative_to(ROOT).as_posix(): file_hash(p) for p in paths}}
    result["production_after"], result["prior_after"] = production_integrity(), prior_integrity()
    assert result["production_after"] == production_before and result["prior_after"] == prior_before
    result["all_integrity_and_causality_checks_passed"] = True
    if stage == "develop":
        result["primary_gate_passed"] = all(r["passes_score_first_rule"] for r in result["years"].values())
        result["next_action"] = ("fixed_2024_diagnostic_permitted" if result["primary_gate_passed"]
                                 else "stop_retain_recommended_63_feature_25_percent_scheme")
    else:
        result["development_sha256"] = file_hash(OUT / "development.json")
        result["passes_score_first_rule"] = result["years"]["2024"]["passes_score_first_rule"]
    result["deployed_to_production"] = False
    result["official_submission_or_report_changed"] = False
    destination.write_text(json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False), encoding="utf-8")
    print(f"COMPLETED {stage}: {result.get('next_action', result.get('passes_score_first_rule'))}", flush=True)
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("step", choices=("test", "develop", "diagnose"))
    args = parser.parse_args()
    if args.step == "test":
        result = tests()
        path = OUT / "tests.json"
        if path.exists():
            assert read(path) == result, "Frozen tests changed"
        else:
            path.write_text(json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False), encoding="utf-8")
        print("OOF Top weighting, feature causality, protected Top and prior-preservation tests passed", flush=True)
    else:
        run(args.step)


