"""Frozen rolling-origin Top flags and one weighted pooled-return auxiliary."""
from __future__ import annotations

import argparse
import gc
import hashlib
import json
import time
from pathlib import Path

import lightgbm as lgb
import numpy as np
import polars as pl

from experiments import return_pooled_models as frozen
from experiments.seed_ensemble import params_for_seed
from run import FEATURE_FILE, MANIFEST, ROOT, feature_names, fold_cutoff, to_matrix
from src.scoring import Panel


OUT = ROOT / "experiments" / "oof_top_eval"
PRIMARY_YEARS = (2022, 2023)
MODEL_KEY = "pooled_oof_top1p5"
CANDIDATE_KEY = "protected_pooled_oof_top1p5_w0p25"
BASELINE_KEY = "protected_return_pooled_w0p25"
ROUNDS, SEED, THREADS = 180, 2026, 16
BLEND = {"mode": "top_only", "weight": .25}
POSTPROCESS = {"alpha": .9, "bonus": .3, "restore_lower": True, "top_current_weight": 1.0}
KEYS = ["ts_code", "trade_date"]
EXPECTED = {
    2022: {"training_cutoff_exclusive": 20211231, "training_first_date": 20180102,
           "training_last_date": 20211230, "training_rows": 3568878, "training_days": 972},
    2023: {"training_cutoff_exclusive": 20221230, "training_first_date": 20180102,
           "training_last_date": 20221229, "training_rows": 4597785, "training_days": 1214},
    2024: {"training_cutoff_exclusive": 20231229, "training_first_date": 20180102,
           "training_last_date": 20231228, "training_rows": 5659954, "training_days": 1456},
}
file_hash = frozen.file_hash


def log(message: str) -> None:
    print(f"[{time.strftime('%H:%M:%S')}] {message}", flush=True)


def features_for_model() -> list[str]:
    features = feature_names()
    if len(features) != 63:
        raise ValueError("Exactly the frozen original 63 features are required")
    return features


# Pure fixed target implementation; weights never enter centering or RMS.
_target_with_stats = frozen._target_with_stats
training_target = frozen.training_target
OOF_YEARS = (2019, 2020, 2021, 2022, 2023)
OOF_EXPECTED = {
    2019: {"training_cutoff_exclusive": 20181228, "training_first_date": 20180102,
           "training_last_date": 20181227, "training_rows": 830098, "training_days": 242,
           "prediction_rows": 1134600, "prediction_days": 244,
           "prediction_first_date": 20190102, "prediction_last_date": 20191231},
    2020: {"training_cutoff_exclusive": 20191231, "training_first_date": 20180102,
           "training_last_date": 20191230, "training_rows": 1694259, "training_days": 486,
           "prediction_rows": 1129950, "prediction_days": 243,
           "prediction_first_date": 20200102, "prediction_last_date": 20201231},
    2021: {"training_cutoff_exclusive": 20201231, "training_first_date": 20180102,
           "training_last_date": 20201230, "training_rows": 2594048, "training_days": 729,
           "prediction_rows": 1129950, "prediction_days": 243,
           "prediction_first_date": 20210104, "prediction_last_date": 20211231},
    2022: {**EXPECTED[2022], "prediction_rows": 1125300, "prediction_days": 242,
           "prediction_first_date": 20220104, "prediction_last_date": 20221230},
    2023: {**EXPECTED[2023], "prediction_rows": 1125300, "prediction_days": 242,
           "prediction_first_date": 20230103, "prediction_last_date": 20231229},
}


def key_hash(frame: pl.DataFrame) -> str:
    return hashlib.sha256(frame.select(KEYS).write_csv().encode("utf-8")).hexdigest()


def oof_top_flags(frame: pl.DataFrame) -> np.ndarray:
    """Rank a complete feature-only block, preserving input row order.

    Eligible nonfinite predictions are corrupt, not silently discarded. Sorting
    uses cached Float32 predictions and ascending code as the exact tie break.
    No realized labels, portfolio state, or postprocessing are consulted.
    """
    columns = KEYS + ["price_valid", "flag_limit_up", "pred_raw"]
    if any(name not in frame.columns for name in columns):
        raise ValueError("OOF selector requires keys, contemporaneous flags and raw predictions")
    if (frame.select(pl.struct(KEYS).n_unique()).item() != len(frame)
            or frame.select(KEYS).null_count().sum_horizontal().item() != 0
            or frame["price_valid"].dtype != pl.Boolean
            or frame["price_valid"].null_count()
            or frame["flag_limit_up"].null_count()
            or frame["pred_raw"].dtype != pl.Float32):
        raise ValueError("OOF keys/flags/types must be complete and unique; raw must be Float32")
    raw = frame["pred_raw"].to_numpy()
    eligible = frame["price_valid"].to_numpy() & (frame["flag_limit_up"].to_numpy() == 0)
    if np.any(eligible & ~np.isfinite(raw)):
        raise ValueError("Eligible OOF prediction must be finite")
    dates = frame["trade_date"].to_numpy()
    codes = frame["ts_code"].to_numpy()
    flags = np.zeros(len(frame), dtype=bool)
    for day in np.unique(dates):
        indices = np.flatnonzero((dates == day) & eligible & np.isfinite(raw))
        take = len(indices) // 10
        if take:
            order = np.lexsort((codes[indices], -raw[indices].astype(np.float64)))
            flags[indices[order[:take]]] = True
    return flags


def training_weights(top_flags: np.ndarray) -> np.ndarray:
    flags = np.asarray(top_flags)
    if flags.ndim != 1 or not len(flags) or flags.dtype != np.bool_:
        raise ValueError("Training Top flags must be a nonempty Boolean vector")
    raw = np.where(flags, 1.5, 1.0).astype(np.float64)
    weights = (raw / raw.mean(dtype=np.float64)).astype(np.float32)
    if not np.isfinite(weights).all() or abs(float(weights.mean(dtype=np.float64)) - 1) > 1e-7:
        raise AssertionError("Normalized weights must be finite and mean one")
    return weights


def weight_checks(top_flags: np.ndarray, weights: np.ndarray) -> dict:
    expected = training_weights(top_flags)
    if weights.dtype != np.float32 or not np.array_equal(weights, expected):
        raise AssertionError("Training weight bytes differ from fixed 1.5/1 rule")
    raw = np.where(top_flags, 1.5, 1.0).astype(np.float64)
    return {"training_rows": len(weights), "oof_top_training_rows": int(top_flags.sum()),
            "non_top_training_rows": int((~top_flags).sum()),
            "raw_weight_mean_float64": float(raw.mean()),
            "min_weight": float(weights.min()), "max_weight": float(weights.max()),
            "actual_mean_float64": float(weights.mean(dtype=np.float64)),
            "weight_array_sha256": hashlib.sha256(weights.tobytes()).hexdigest(),
            "top_flags_array_sha256": hashlib.sha256(top_flags.tobytes()).hexdigest(),
            "global_mean_one_tolerance": 1e-7, "sample_weights_dtype": "Float32",
            "target_centering_and_rms_unweighted": True}


def _join_top_flags(frame: pl.DataFrame, oof: pl.DataFrame) -> np.ndarray:
    """Complete OOF Top selection is already frozen before training-label filtering."""
    if (frame.select(pl.struct(KEYS).n_unique()).item() != len(frame)
            or oof.select(pl.struct(KEYS).n_unique()).item() != len(oof)
            or oof["is_oof_top"].dtype != pl.Boolean or oof["is_oof_top"].null_count()):
        raise ValueError("Training and OOF keys must be unique with nonnull Boolean flags")
    joined = frame.select(KEYS).with_row_index("_training_order").join(
        oof.select(KEYS + ["is_oof_top"]), on=KEYS, how="left", validate="1:1",
        maintain_order="left")
    if len(joined) != len(frame) or not joined.select(KEYS).equals(frame.select(KEYS)):
        raise AssertionError("OOF join reordered or removed training keys")
    is_2018 = joined["trade_date"].is_between(20180101, 20181231).to_numpy()
    missing = joined["is_oof_top"].is_null().to_numpy()
    if np.any(missing != is_2018):
        raise ValueError("Only initial-year 2018 may lack OOF flags; all later training keys require coverage")
    return joined["is_oof_top"].fill_null(False).to_numpy()


def test_model() -> dict:
    read_protocol()
    # Float32 ties prefer ascending ts_code; n<10, invalid-price and limit-up excluded.
    frame = pl.DataFrame({"ts_code": [f"S{i:02d}" for i in range(25)],
        "trade_date": [20190102]*25, "price_valid": [True]*24+[False],
        "flag_limit_up": [0]*23+[1, 0],
        "pred_raw": pl.Series([1.0]*23+[100.0, 200.0], dtype=pl.Float32)})
    flags = oof_top_flags(frame)
    assert np.array_equal(np.flatnonzero(flags), [0, 1])
    assert not oof_top_flags(frame.head(9)).any()
    assert oof_top_flags(frame.head(10)).sum() == 1
    assert oof_top_flags(frame.head(0)).size == 0
    perm = np.arange(len(frame))[::-1]
    assert np.array_equal(oof_top_flags(frame[perm]), flags[perm])
    labels = frame.with_columns(pl.Series("y_ret_1d", [None, 9.0]+[0.0]*23))
    assert np.array_equal(oof_top_flags(labels), flags)
    selected = labels.with_columns(pl.Series("is_oof_top", flags)).select(KEYS+["is_oof_top"])
    train = labels.filter(pl.col("y_ret_1d").is_not_null() & pl.col("price_valid")).select(KEYS)
    # Missing y on S00 does not give the quota slot to S02.
    aligned = _join_top_flags(train, selected)
    assert train.filter(pl.Series(aligned))["ts_code"].to_list() == ["S01"]
    fallback = pl.DataFrame({"ts_code": ["A"], "trade_date": [20180102]})
    train = pl.concat([fallback, train], how="vertical_relaxed")
    aligned = _join_top_flags(train, selected)
    weights = training_weights(aligned)
    checks = weight_checks(aligned, weights)
    assert np.array_equal(training_weights(aligned[::-1]), weights[::-1])
    assert not aligned[0] and weights[0] != 1
    assert abs(float(weights[aligned][0]) / float(weights[~aligned][0]) - 1.5) < 1e-7
    assert np.array_equal(training_weights(np.zeros(4, bool)), np.ones(4, np.float32))
    assert np.array_equal(training_weights(np.ones(4, bool)), np.ones(4, np.float32))
    future = frame.with_columns((pl.col("trade_date")+10000).alias("trade_date"))
    combined = pl.concat([frame, future])
    assert np.array_equal(oof_top_flags(combined)[:len(frame)], flags)
    rejected = []
    for name, bad in (("empty_weights", []), ("numeric_flags", [0, 1]),
                      ("nonvector_flags", [[True]]), ("nullable_flags", [True, None])):
        try:
            training_weights(bad)
        except ValueError:
            rejected.append(name)
        else:
            raise AssertionError(name)
    for name, bad in (("duplicate_keys", pl.concat([frame, frame.head(1)])),
                      ("eligible_nonfinite", frame.with_columns(
                          pl.when(pl.col("ts_code") == "S00").then(float("nan"))
                          .otherwise(pl.col("pred_raw")).cast(pl.Float32).alias("pred_raw"))),
                      ("float64_raw", frame.with_columns(pl.col("pred_raw").cast(pl.Float64)))):
        try:
            oof_top_flags(bad)
        except ValueError:
            rejected.append(name)
        else:
            raise AssertionError(name)
    try:
        _join_top_flags(train, selected.filter(pl.col("ts_code") != "S01"))
    except ValueError:
        rejected.append("missing_later_year_key")
    else:
        raise AssertionError("missing OOF coverage accepted")
    return {"status": "passed", "complete_universe_selection_before_label_filter": True,
        "float32_raw_ts_code_tie_break": True, "floor_n_over_10_including_zero": True,
        "prefix_and_permutation_invariant": True, "one_to_one_join_original_order": True,
        "initial_year_raw_one_normalized_with_fold": True, "pooled_target_alias_unchanged": True,
        "rejected_invalid_inputs": rejected, "fixture_weight_stats": checks,
        "source_sha256": file_hash(Path(__file__)), "protocol_sha256": file_hash(OUT / "protocol.json")}


_FIXED_DESIGN = json.loads(r'''{
  "experiment": "fixed_annual_oof_predicted_top_training_weight",
  "declared_before_training_and_scoring": true,
  "candidate_key": "protected_pooled_oof_top1p5_w0p25",
  "baseline_key": "protected_return_pooled_w0p25",
  "model_key": "pooled_oof_top1p5",
  "candidate_count": 1,
  "primary_years": [
    2022,
    2023
  ],
  "conditional_diagnostic_year": 2024,
  "feature_count": 63,
  "feature_variant": "original_63",
  "added_features": [],
  "rounds": 180,
  "seed": 2026,
  "threads": 16,
  "training_filter": "is_train & trade_date < fold_cutoff(year) & y_rank.not_null & price_valid",
  "blend": {
    "mode": "top_only",
    "weight": 0.25
  },
  "postprocess": {
    "alpha": 0.9,
    "bonus": 0.3,
    "restore_lower": true,
    "top_current_weight": 1
  },
  "folds": {
    "2022": {
      "training_cutoff_exclusive": 20211231,
      "training_first_date": 20180102,
      "training_last_date": 20211230,
      "training_rows": 3568878,
      "training_days": 972
    },
    "2023": {
      "training_cutoff_exclusive": 20221230,
      "training_first_date": 20180102,
      "training_last_date": 20221229,
      "training_rows": 4597785,
      "training_days": 1214
    },
    "2024": {
      "training_cutoff_exclusive": 20231229,
      "training_first_date": 20180102,
      "training_last_date": 20231228,
      "training_rows": 5659954,
      "training_days": 1456
    }
  },
  "oof": {
    "scheme": "Annual rolling-origin with expanding training history from 2018; not a fixed-length rolling window.",
    "primary_block_years": [
      2019,
      2020,
      2021,
      2022
    ],
    "conditional_block_year": 2023,
    "warmup_year": 2018,
    "warmup_raw_weight": 1,
    "training_filter": "is_train & trade_date < fold_cutoff(year) & y_rank.not_null & price_valid",
    "target": "Original cached Float32 y_rank, already equal to daily average-rank/count minus 0.5; do not center again. No OOF sample weights.",
    "features": "The original 63 features in unchanged order",
    "rounds": 180,
    "seed": 2026,
    "threads": 16,
    "prediction_scope": "All supplied is_train rows in the complete calendar block, sorted trade_date then ts_code; do not select or materialize block return labels or label-availability masks.",
    "prediction_precision": "Saved Float32 pred_raw; promote that Float32 value to Float64 only for sorting. Invalid-price rows retain -1e6 sentinel and are excluded from the selection universe.",
    "eligibility": "price_valid == true and flag_limit_up == 0; predictions must be finite. Fail on nonfinite model output, do not silently shrink the universe.",
    "top_fraction": 0.1,
    "count_rule": "floor(number of eligible stocks / 10), including zero when fewer than 10 are eligible",
    "tie_rule": "pred_raw descending then ts_code ascending; deterministic per-date total order",
    "postprocess": "None in OOF region generation; no smoothing, persistence or cross-block holdings state. Raw predicted Top is not identical to the final protected holdings.",
    "outer_block_years": {
      "2022": [
        2019,
        2020,
        2021
      ],
      "2023": [
        2019,
        2020,
        2021,
        2022
      ],
      "2024": [
        2019,
        2020,
        2021,
        2022,
        2023
      ]
    },
    "folds": {
      "2019": {
        "training_cutoff_exclusive": 20181228,
        "training_first_date": 20180102,
        "training_last_date": 20181227,
        "training_rows": 830098,
        "training_days": 242,
        "prediction_rows": 1134600,
        "prediction_days": 244,
        "prediction_first_date": 20190102,
        "prediction_last_date": 20191231
      },
      "2020": {
        "training_cutoff_exclusive": 20191231,
        "training_first_date": 20180102,
        "training_last_date": 20191230,
        "training_rows": 1694259,
        "training_days": 486,
        "prediction_rows": 1129950,
        "prediction_days": 243,
        "prediction_first_date": 20200102,
        "prediction_last_date": 20201231
      },
      "2021": {
        "training_cutoff_exclusive": 20201231,
        "training_first_date": 20180102,
        "training_last_date": 20201230,
        "training_rows": 2594048,
        "training_days": 729,
        "prediction_rows": 1129950,
        "prediction_days": 243,
        "prediction_first_date": 20210104,
        "prediction_last_date": 20211231
      },
      "2022": {
        "training_cutoff_exclusive": 20211231,
        "training_first_date": 20180102,
        "training_last_date": 20211230,
        "training_rows": 3568878,
        "training_days": 972,
        "prediction_rows": 1125300,
        "prediction_days": 242,
        "prediction_first_date": 20220104,
        "prediction_last_date": 20221230
      },
      "2023": {
        "training_cutoff_exclusive": 20221230,
        "training_first_date": 20180102,
        "training_last_date": 20221229,
        "training_rows": 4597785,
        "training_days": 1214,
        "prediction_rows": 1125300,
        "prediction_days": 242,
        "prediction_first_date": 20230103,
        "prediction_last_date": 20231229
      }
    },
    "scope": "Outer 2022 reads only 2019-2021 OOF regions, outer 2023 only 2019-2022. OOF 2023 and outer 2024 are forbidden until this experiment's two development folds pass."
  },
  "weighting": {
    "source": "Prediction-only is_oof_top membership computed on the full OOF X universe before outer training-label filtering",
    "top_weight": 1.5,
    "other_weight": 1,
    "normalization": "raw=(1.5 if is_oof_top else 1.0); divide by mean(raw) over all final filtered outer training rows, then cast Float32",
    "join": "Exact 1:1 left join on ts_code,trade_date preserving original training row order; complete OOF keys required for covered years; only 2018 may default to not selected",
    "target_unchanged": "Reuse unweighted pooled target statistics and exact target bytes from the current pooled reference; never recompute a weighted mean, RMS or clipping quantile",
    "no_coverage_action": "2018 raw weight=1.0; after whole-fold normalization it is not necessarily exactly 1",
    "tuning": "None; one predeclared 1.5x Top10% weighting rule"
  },
  "rule": {
    "numerical_score_tolerance": 1e-12,
    "development": "Both 2022 and 2023 weighted candidate official final_score minus fixed pooled-RMS 63-feature 25% reference final_score > 1e-12, and all integrity, coverage, time-boundary, OOF-causality, target/weight, original-scoring and exact official daily Top/turnover checks pass. Only then permit OOF 2023 and one fixed 2024 train/diagnosis.",
    "diagnostic": "The unchanged 2024 candidate must also improve official composite score over the fixed pooled-RMS 25% reference by >1e-12 and pass all checks to recommend adoption.",
    "components": "Report IC, excess and turnover; IC or excess need not individually increase. Exact protected daily turnover/Top identity is an implementation invariant, not a new component-score gate.",
    "uncertainty": "Report paired HAC confidence intervals and first-day/t2 diagnostics. CI including zero is not an automatic veto.",
    "failure": "Stop and retain the previously recommended pooled-RMS 63-feature 25% scheme. Do not retune the OOF schedule, Top fraction, weights, target, features, blend, postprocess or test extra years.",
    "promotion": "Recommendation only. No production, official submission or DOCX changes."
  },
  "diagnostic_prerequisite": {
    "receipt": "experiments/oof_top_eval/diagnosis_receipt.json",
    "required_stage": "Complete the fixed 2024 pooled-vs-daily-z Top-boundary attribution first. Root verifies the diagnosis and freezes hashes in this receipt before any OOF or weighted fit. Diagnosis is descriptive, not used to choose weights, dates or securities."
  },
  "prior_manifest": "experiments/oof_top_eval/prior_artifacts_sha256.json",
  "prior_directories": [
    "experiments/return_head_eval",
    "experiments/return_head_scorefirst_eval",
    "experiments/return_market_eval",
    "experiments/return_market_stable_eval",
    "experiments/return_pooled_eval"
  ],
  "target_audit_tolerance": {
    "rtol": 0.000001,
    "atol": 1e-7,
    "max_abs_float32": 0.000001,
    "pooled_rms_rtol": 1e-12,
    "pooled_rms_atol": 1e-15
  }
}''')


def read_protocol() -> dict:
    protocol = json.loads((OUT / "protocol.json").read_text(encoding="utf-8"))
    if any(protocol.get(key) != value for key, value in _FIXED_DESIGN.items()):
        raise ValueError("The single predeclared OOF/weight/model/score design changed")
    if protocol.get("target") != frozen.read_protocol()["target"]:
        raise ValueError("The pooled unweighted target must remain exactly unchanged")
    return protocol


def _read(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def diagnosis_prerequisite() -> dict[str, str]:
    """No fit is allowed until root completes and freezes the descriptive diagnosis."""
    receipt_path = ROOT / read_protocol()["diagnostic_prerequisite"]["receipt"]
    if not receipt_path.exists():
        raise ValueError("Any OOF or weighted fit is forbidden before the root-reviewed diagnosis receipt")
    receipt = _read(receipt_path)
    source = ROOT / "experiments/diagnose_pooled_ties.py"
    if (receipt.get("status") != "completed"
            or receipt.get("protocol_sha256") != file_hash(OUT / "protocol.json")
            or receipt.get("diagnosis_source_sha256") != file_hash(source)
            or receipt.get("completed_before_any_fit") is not True
            or receipt.get("reviewed_by") != "root"):
        raise ValueError("Boundary diagnosis receipt is absent, changed or not approved before fitting")
    folder = ROOT / "experiments/pooled_tie_diagnosis"
    artifacts = receipt.get("artifacts_sha256", {})
    actual = {path.relative_to(ROOT).as_posix(): file_hash(path)
              for path in folder.rglob("*") if path.is_file()}
    normalized = {name.replace("\\", "/"): digest for name, digest in artifacts.items()}
    if not actual or actual != normalized:
        raise ValueError("Diagnosis receipt must cover the complete unchanged diagnosis directory")
    return {**normalized, source.relative_to(ROOT).as_posix(): file_hash(source),
            receipt_path.relative_to(ROOT).as_posix(): file_hash(receipt_path)}


def _digest(payload: dict) -> dict:
    payload["fingerprint_sha256"] = hashlib.sha256(
        json.dumps(payload, sort_keys=True).encode("utf-8")).hexdigest()
    return payload


def _reference_metadata(year: int) -> dict:
    stem = f"{frozen.MODEL_KEY}_{year}"
    meta = _read(frozen.OUT / f"{stem}.json")
    if (meta["model_sha256"] != file_hash(frozen.OUT / f"{stem}.txt")
            or meta["cache_sha256"] != file_hash(frozen.OUT / f"{stem}.parquet")
            or meta["features"] != features_for_model()
            or meta["target"] != read_protocol()["target"]
            or meta["sample_weight"] is not None
            or meta["params"] != params_for_seed(SEED, THREADS)
            or meta["rounds"] != ROUNDS or meta["reload_max_abs_error"] != 0):
        raise ValueError("Frozen pooled reference model or target changed")
    return meta


def _locked_sources() -> dict[str, str]:
    protocol = read_protocol()
    manifest_path = ROOT / protocol["prior_manifest"]
    manifest = _read(manifest_path)
    for relative, expected in manifest.items():
        if file_hash(ROOT / relative) != expected:
            raise ValueError(f"Prior evidence changed: {relative}")
    for relative in protocol["prior_directories"]:
        directory = ROOT / relative
        prefix = directory.relative_to(ROOT).as_posix() + "/"
        actual = {path.relative_to(ROOT).as_posix(): file_hash(path)
                  for path in directory.rglob("*") if path.is_file()}
        if actual != {name: value for name, value in manifest.items() if name.startswith(prefix)}:
            raise ValueError(f"Frozen prior directory changed: {relative}")
    sources = {**frozen._locked_sources(), **manifest}
    for name in ("development.json", "diagnostic_2024.json"):
        sources.update(_read(frozen.OUT / name)["artifacts_sha256"])
    decision = _read(frozen.OUT / "decision.json")
    if (decision.get("recommended_for_next_version") is not True
            or decision.get("selected_candidate") != BASELINE_KEY
            or decision.get("development_sha256") != file_hash(frozen.OUT / "development.json")
            or decision.get("diagnostic_2024_sha256") != file_hash(frozen.OUT / "diagnostic_2024.json")
            or decision.get("deployed_to_production") is not False):
        raise ValueError("Comparison must remain the recommended undeployed pooled 25% scheme")
    sources.update(diagnosis_prerequisite())
    test_path = OUT / "model_tests.json"
    if _read(test_path) != test_model():
        raise ValueError("Frozen OOF/weight unit tests differ from source/protocol")
    for path in (Path(__file__), ROOT / "experiments/audit_oof_top.py",
                 OUT / "protocol.json", test_path, manifest_path):
        sources[path.relative_to(ROOT).as_posix()] = file_hash(path)
    for relative, expected in sources.items():
        if file_hash(ROOT / relative) != expected:
            raise ValueError(f"Transitive source or evidence changed: {relative}")
    return dict(sorted(sources.items()))


def _check_year(year: int) -> None:
    if year not in (*PRIMARY_YEARS, 2024):
        raise ValueError("Only primary 2022/2023 and conditionally permitted 2024 are supported")


def _paths(year: int) -> tuple[Path, Path, Path]:
    _check_year(year)
    stem = f"{MODEL_KEY}_{year}"
    return OUT / f"{stem}.txt", OUT / f"{stem}.parquet", OUT / f"{stem}.json"


def oof_paths(year: int) -> tuple[Path, Path, Path]:
    if year not in OOF_YEARS:
        raise ValueError("Only predeclared annual OOF blocks are supported")
    return tuple(OUT / f"oof_rank_{year}.{extension}" for extension in ("txt", "parquet", "json"))


def _block_frame(year: int, include_features: bool = False) -> pl.DataFrame:
    columns = KEYS + (features_for_model() if include_features else ["flag_limit_up"]) + ["price_valid"]
    return (pl.scan_parquet(FEATURE_FILE)
        .filter(pl.col("is_train") & pl.col("trade_date").is_between(year*10000+101, year*10000+1231))
        .select(columns).sort("trade_date", "ts_code").collect())


def oof_fingerprint(year: int) -> dict:
    oof_paths(year)
    gate = diagnostic_gate() if year == 2023 else None
    protocol = read_protocol()
    boundary = protocol["oof"]["folds"][str(year)]
    if fold_cutoff(year) != boundary["training_cutoff_exclusive"]:
        raise ValueError("OOF one-day purge boundary changed")
    payload = {"year": year, "model_key": "oof_rank", "kind": "training_only_rolling_origin_region",
        "features": features_for_model(), "params": params_for_seed(SEED, THREADS),
        "rounds": ROUNDS, "seed": SEED, "threads": THREADS, "sample_weight": None,
        "training_filter": protocol["training_filter"], "target": protocol["oof"]["target"],
        "boundaries": boundary, "prediction_labels_loaded": False,
        "oof_rules": protocol["oof"], "source_sha256": _locked_sources(),
        "lightgbm_version": lgb.__version__, "numpy_version": np.__version__, "polars_version": pl.__version__}
    if gate is not None:
        payload["diagnostic_gate"] = gate
    return _digest(payload)


def load_oof(year: int) -> pl.DataFrame:
    model_path, cache_path, meta_path = oof_paths(year)
    meta = _read(meta_path)
    expected = oof_fingerprint(year)
    if any(meta.get(key) != value for key, value in expected.items()):
        raise ValueError("OOF model provenance differs from frozen rolling-origin design")
    if (meta["model_sha256"] != file_hash(model_path) or meta["cache_sha256"] != file_hash(cache_path)
            or meta["reload_check_rows"] != 4096 or meta["reload_max_abs_error"] != 0):
        raise ValueError("OOF model/cache/reload evidence changed")
    cache = pl.read_parquet(cache_path)
    block = _block_frame(year)
    if (cache.columns != KEYS + ["pred_raw", "is_oof_top"]
            or not cache.select(KEYS).equals(block.select(KEYS))
            or cache["pred_raw"].dtype != pl.Float32 or cache["is_oof_top"].dtype != pl.Boolean
            or not np.isfinite(cache["pred_raw"].to_numpy()).all()
            or meta["prediction_keys_sha256"] != key_hash(block)):
        raise ValueError("OOF block completeness, ordering or raw precision changed")
    raw = cache["pred_raw"].to_numpy()
    if np.any(raw[~block["price_valid"].to_numpy()] != np.float32(-1e6)):
        raise ValueError("OOF invalid-price sentinel changed")
    expected_flags = oof_top_flags(block.with_columns(cache["pred_raw"]))
    if not np.array_equal(expected_flags, cache["is_oof_top"].to_numpy()):
        raise ValueError("Saved OOF region disagrees with complete unlabeled daily universe")
    boundary = expected["boundaries"]
    for key in ("training_rows", "training_days", "training_first_date", "training_last_date",
                "prediction_rows", "prediction_days", "prediction_first_date", "prediction_last_date"):
        if meta[key] != boundary[key]:
            raise ValueError(f"OOF boundary/count metadata changed: {key}")
    if len(cache) != boundary["prediction_rows"] or cache["trade_date"].n_unique() != boundary["prediction_days"]:
        raise ValueError("OOF actual full-year coverage differs")
    return cache


def build_oof(year: int) -> None:
    expected = oof_fingerprint(year)
    model_path, cache_path, meta_path = oof_paths(year)
    if any(path.exists() for path in (model_path, cache_path, meta_path)):
        if not all(path.exists() for path in (model_path, cache_path, meta_path)):
            raise ValueError("Partial OOF artifacts exist; preserve them for inspection")
        load_oof(year)
        log(f"Validated frozen OOF {year}")
        return
    # Explicit chronological construction, never auto-fit unrequested blocks.
    if year > OOF_YEARS[0]:
        load_oof(year - 1)
    boundary = expected["boundaries"]
    cutoff, features = boundary["training_cutoff_exclusive"], expected["features"]
    frame = (pl.scan_parquet(FEATURE_FILE)
        .filter(pl.col("is_train") & (pl.col("trade_date") < cutoff)
                & pl.col("y_rank").is_not_null() & pl.col("price_valid"))
        .select(KEYS + features + ["y_rank"]).collect())
    y = frame["y_rank"].to_numpy().astype(np.float32)
    if (frame["y_rank"].dtype != pl.Float32 or not np.isfinite(y).all()
            or y.min() < -.5 or y.max() > .5
            or len(frame) != boundary["training_rows"]
            or frame["trade_date"].n_unique() != boundary["training_days"]
            or int(frame["trade_date"].min()) != boundary["training_first_date"]
            or int(frame["trade_date"].max()) != boundary["training_last_date"]
            or frame.select(pl.struct(KEYS).n_unique()).item() != len(frame)):
        raise AssertionError("OOF training rows/order, already-centered rank target or dates differ")
    training_keys_sha256 = key_hash(frame)
    target_sha256 = hashlib.sha256(y.tobytes()).hexdigest()
    missingness = frozen.feature_missingness(frame)
    x = to_matrix(frame, features)
    del frame
    gc.collect()
    log(f"Training OOF {year}: rows={len(y):,}, days={boundary['training_days']}, purge={cutoff}")
    started = time.monotonic()
    dataset = lgb.Dataset(x, label=y, feature_name=features, free_raw_data=True)
    model = lgb.train(expected["params"], dataset, num_boost_round=ROUNDS)
    model_path.write_text(model.model_to_string(), encoding="utf-8")
    del x, y, dataset
    gc.collect()
    block = _block_frame(year, include_features=True)
    matrix = to_matrix(block, features)
    raw = model.predict(matrix, num_threads=THREADS).astype(np.float32)
    if not np.isfinite(raw).all():
        raise AssertionError("Nonfinite OOF model output cannot shrink the Top universe")
    raw[~block["price_valid"].to_numpy()] = -1e6
    flags = oof_top_flags(block.with_columns(pl.Series("pred_raw", raw)))
    reloaded = lgb.Booster(model_str=model_path.read_text(encoding="utf-8"))
    indices = np.linspace(0, len(block)-1, 4096, dtype=int)
    checked = reloaded.predict(matrix[indices], num_threads=THREADS).astype(np.float32)
    checked[~block["price_valid"].to_numpy()[indices]] = -1e6
    if (reloaded.feature_name() != features or reloaded.current_iteration() != ROUNDS
            or not np.array_equal(checked, raw[indices])):
        raise AssertionError("OOF model save/reload is not exact")
    result = block.select(KEYS).with_columns(pl.Series("pred_raw", raw), pl.Series("is_oof_top", flags))
    result.write_parquet(cache_path, compression="zstd")
    if oof_fingerprint(year) != expected:
        raise AssertionError("Source changed during OOF construction")
    meta = {**expected, **boundary, "training_keys_sha256": training_keys_sha256,
        "target_array_sha256": target_sha256, "target_is_cached_already_centered_y_rank": True,
        "prediction_keys_sha256": key_hash(block), "oof_top_rows": int(flags.sum()),
        "oof_top_flags_sha256": hashlib.sha256(flags.tobytes()).hexdigest(),
        "training_feature_missingness": missingness,
        "prediction_feature_missingness": frozen.feature_missingness(block),
        "model_sha256": file_hash(model_path), "cache_sha256": file_hash(cache_path),
        "reload_check_rows": len(indices), "reload_max_abs_error": 0.0,
        "elapsed_seconds": time.monotonic()-started}
    meta_path.write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")
    del model, reloaded, matrix, block, raw, flags, result
    gc.collect()
    load_oof(year)
    log(f"Saved OOF {year}: rows={meta['prediction_rows']:,}, elapsed={meta['elapsed_seconds']:.1f}s")


def weights_for_frame(frame: pl.DataFrame, year: int) -> tuple[np.ndarray, dict]:
    _check_year(year)
    if year == 2024:
        diagnostic_gate()
    cutoff = EXPECTED[year]["training_cutoff_exclusive"]
    if (len(frame) != EXPECTED[year]["training_rows"]
            or int(frame["trade_date"].min()) != EXPECTED[year]["training_first_date"]
            or int(frame["trade_date"].max()) != EXPECTED[year]["training_last_date"]
            or not (frame["trade_date"] < cutoff).all()):
        raise ValueError("Weight normalization must use the complete filtered purged outer fold")
    years = read_protocol()["oof"]["outer_block_years"][str(year)]
    oof = pl.concat([load_oof(block_year) for block_year in years])
    flags = _join_top_flags(frame, oof)
    weights = training_weights(flags)
    stats = weight_checks(flags, weights)
    stats.update({"training_keys_sha256": key_hash(frame), "oof_block_years": years,
        "initial_2018_training_rows": int(frame["trade_date"].is_between(20180101, 20181231).sum()),
        "all_other_training_keys_covered": True, "training_row_order_preserved": True,
        "selection_uses_complete_oof_x_before_training_label_filter": True})
    return weights, stats


def diagnostic_gate() -> dict:
    path = OUT / "development.json"
    if not path.exists():
        raise ValueError("2024 forbidden until both new development folds pass")
    record = json.loads(path.read_text(encoding="utf-8"))
    audit_source = ROOT / "experiments/audit_oof_top.py"
    if (record.get("primary_gate_passed") is not True
            or record.get("all_integrity_and_causality_checks_passed") is not True
            or record.get("candidate_key") != CANDIDATE_KEY
            or record.get("baseline_key") != BASELINE_KEY
            or record.get("primary_years") != list(PRIMARY_YEARS)
            or record.get("protocol_sha256") != file_hash(OUT / "protocol.json")
            or record.get("audit_source_sha256") != file_hash(audit_source)):
        raise ValueError("2024 development gate is failed, mismatched or unaudited")
    required = {str(path.relative_to(ROOT)) for path in (
        audit_source, OUT / "protocol.json", OUT / "model_tests.json")}
    for year in PRIMARY_YEARS:
        yearly = record.get("years", {}).get(str(year), {})
        reference, candidate = yearly.get("reference", {}), yearly.get("candidate", {})
        old, new = reference.get("final_score", np.nan), candidate.get("final_score", np.nan)
        if not np.isfinite(old) or not np.isfinite(new) or new - old <= 1e-12:
            raise ValueError("2024 requires positive score gain over the recommended reference in BOTH years")
        if (yearly.get("passes_score_first_rule") is not True
                or yearly.get("all_integrity_and_causality_checks_passed") is not True
                or yearly.get("official_turnover_top_identities_equal") is not True
                or yearly.get("official_daily_turnover_exact") is not True
                or reference.get("mean_turnover") != candidate.get("mean_turnover")):
            raise ValueError("2024 requires all audits and actual daily Top/turnover checks")
        current = fingerprint(year)
        if record.get("model_fingerprints", {}).get(str(year)) != current["fingerprint_sha256"]:
            raise ValueError("New primary model fingerprints changed after evaluation")
        load_raw(year)
        required.update(current["source_sha256"])
        required.update(str(path.relative_to(ROOT)) for path in _paths(year))
        for name in ("reference", "candidate"):
            required.add(str((OUT / f"official_{name}_{year}_daily.csv").relative_to(ROOT)))
            required.add(str((OUT / f"{name}_processed_{year}.parquet").relative_to(ROOT)))
    artifacts = record.get("artifacts_sha256", {})
    normalized_required = {name.replace("\\", "/") for name in required}
    normalized_artifacts = {name.replace("\\", "/") for name in artifacts}
    if not normalized_required.issubset(normalized_artifacts):
        raise ValueError("Development gate omits required source/model/daily evidence")
    for relative, expected_hash in artifacts.items():
        if file_hash(ROOT / relative) != expected_hash:
            raise ValueError(f"New development artifact changed: {relative}")
    return {"development_sha256": file_hash(path), "primary_gate_passed": True}


def fingerprint(year: int) -> dict:
    _check_year(year)
    gate = diagnostic_gate() if year == 2024 else None
    protocol = read_protocol()
    cutoff = fold_cutoff(year)
    if cutoff != EXPECTED[year]["training_cutoff_exclusive"]:
        raise ValueError("Outer one-day purge boundary changed")
    sources = _locked_sources()
    oof_fingerprints = {}
    for block_year in protocol["oof"]["outer_block_years"][str(year)]:
        load_oof(block_year)
        meta = _read(oof_paths(block_year)[2])
        oof_fingerprints[str(block_year)] = meta["fingerprint_sha256"]
        sources.update(meta["source_sha256"])
        sources.update({p.relative_to(ROOT).as_posix(): file_hash(p) for p in oof_paths(block_year)})
    for path in (ROOT / f"models/fold_{year}.txt", ROOT / f"validation/fold_{year}.parquet"):
        sources[path.relative_to(ROOT).as_posix()] = file_hash(path)
    reference = _reference_metadata(year)
    payload = {"year": year, "candidate_key": CANDIDATE_KEY, "baseline_key": BASELINE_KEY,
        "model_key": MODEL_KEY, "rounds": ROUNDS, "seed": SEED, "threads": THREADS,
        "params": params_for_seed(SEED, THREADS), "features": features_for_model(),
        "training_cutoff_exclusive": cutoff, "training_filter": protocol["training_filter"],
        "target": protocol["target"], "sample_weight": protocol["weighting"],
        "reference_target_array_sha256": reference["target_stats"]["target_array_sha256"],
        "reference_training_keys_sha256": reference["training_keys_sha256"],
        "oof_model_fingerprints": oof_fingerprints, "blend": BLEND, "postprocess": POSTPROCESS,
        "validation_labels_loaded": False, "lightgbm_version": lgb.__version__,
        "numpy_version": np.__version__, "polars_version": pl.__version__,
        "source_sha256": dict(sorted(sources.items()))}
    if gate is not None:
        payload["diagnostic_gate"] = gate
    return _digest(payload)


def load_panel(year: int) -> Panel:
    _check_year(year)
    if year == 2024:
        diagnostic_gate()
    frame = pl.read_parquet(ROOT / f"validation/fold_{year}.parquet",
                            columns=KEYS + ["flag_limit_up", "price_valid", "pred_raw"])
    if (frame.select(pl.struct(KEYS).n_unique()).item() != len(frame)
            or not frame.select(KEYS).equals(frame.sort("trade_date", "ts_code").select(KEYS))
            or not frame["trade_date"].is_between(year * 10000 + 101, year * 10000 + 1231).all()):
        raise ValueError("Panel keys/order/year differ from original baseline")
    panel = Panel.from_frame(frame.with_columns(pl.lit(None, dtype=pl.Float64).alias("y_ret_1d")))
    if np.isfinite(panel.y).any():
        raise AssertionError("Prediction panel must contain no validation labels")
    return panel


def load_raw(year: int, panel: Panel | None = None) -> np.ndarray:
    model_path, cache_path, meta_path = _paths(year)
    meta, expected = _read(meta_path), fingerprint(year)
    if any(meta.get(key) != value for key, value in expected.items()):
        raise ValueError("Weighted model provenance differs from frozen design")
    if meta["model_sha256"] != file_hash(model_path) or meta["cache_sha256"] != file_hash(cache_path):
        raise ValueError("Weighted model/cache hash changed")
    base = load_panel(year) if panel is None else panel
    frame = pl.read_parquet(cache_path)
    if (frame.columns != KEYS + ["pred_raw"] or not frame.select(KEYS).equals(base.frame.select(KEYS))
            or frame.select(pl.struct(KEYS).n_unique()).item() != len(frame)):
        raise ValueError("Weighted raw cache coverage/order differs from original panel")
    for field in ("training_first_date", "training_last_date", "training_rows"):
        if meta[field] != EXPECTED[year][field]:
            raise ValueError(f"Weighted model training boundary changed: {field}")
    stats = meta["weight_statistics"]
    if (meta["target_stats"] != _reference_metadata(year)["target_stats"]
            or meta["target_matches_pooled_reference_exact"] is not True
            or meta["training_keys_sha256"] != expected["reference_training_keys_sha256"]
            or stats["training_keys_sha256"] != meta["training_keys_sha256"]
            or stats["training_rows"] != EXPECTED[year]["training_rows"]
            or abs(stats["actual_mean_float64"] - 1) > 1e-7
            or meta["validation_rows"] != len(frame) or meta["reload_check_rows"] != 4096
            or meta["reload_max_abs_error"] != 0):
        raise ValueError("Weighted target/weight/key/reload evidence differs")
    raw = frame["pred_raw"].to_numpy()
    if (raw.dtype != np.float32 or not np.isfinite(raw).all()
            or np.any(raw[~base.valid_price.reshape(-1)] != np.float32(-1e6))):
        raise ValueError("Weighted raw predictions must be finite Float32 with invalid-price sentinel")
    return raw


def train(year: int) -> None:
    expected = fingerprint(year)
    model_path, cache_path, meta_path = _paths(year)
    if any(path.exists() for path in (model_path, cache_path, meta_path)):
        if not all(path.exists() for path in (model_path, cache_path, meta_path)):
            raise ValueError("Incomplete weighted pooled auxiliary cache exists; preserve for inspection")
        load_raw(year)
        log(f"Validated frozen OOF-weighted pooled-return cache: {year}")
        return
    features, cutoff = expected["features"], expected["training_cutoff_exclusive"]
    mask = (pl.col("is_train") & (pl.col("trade_date") < cutoff)
            & pl.col("y_rank").is_not_null() & pl.col("price_valid"))
    frame = pl.scan_parquet(FEATURE_FILE).filter(mask).select(KEYS + features + ["y_ret_1d"]).collect()
    if frame["y_ret_1d"].dtype != pl.Float32:
        raise AssertionError("Training target input must retain the original Float32 cache")
    x = to_matrix(frame, features)
    dates, returns = frame["trade_date"].to_numpy(), frame["y_ret_1d"].to_numpy()
    rows, first_date, last_date = len(frame), int(dates.min()), int(dates.max())
    if (rows != EXPECTED[year]["training_rows"] or first_date != EXPECTED[year]["training_first_date"]
            or last_date != EXPECTED[year]["training_last_date"] or last_date >= cutoff
            or not np.isfinite(returns).all()
            or frame.select(pl.struct(KEYS).n_unique()).item() != rows):
        raise AssertionError("Training mask rows, date boundaries or targets differ")
    y, target_stats = _target_with_stats(dates, returns)
    if (target_stats["training_days"] != EXPECTED[year]["training_days"]
            or target_stats["training_rows"] != rows
            or target_stats["pooled_nearconstant"]
            or target_stats["target_array_sha256"] != expected["reference_target_array_sha256"]):
        raise AssertionError("Pooled target counts or exact reference target equality failed")
    if target_stats != _reference_metadata(year)["target_stats"]:
        raise AssertionError("Unweighted pooled target stats or training row order differ from reference")
    weights, weight_stats = weights_for_frame(frame, year)
    training_keys_sha256 = hashlib.sha256(frame.select(KEYS).write_csv().encode("utf-8")).hexdigest()
    if training_keys_sha256 != expected["reference_training_keys_sha256"]:
        raise AssertionError("Original training key order differs from pooled reference")
    train_missingness = frozen.feature_missingness(frame)
    del frame, dates, returns
    gc.collect()
    log(f"Training {year}/{MODEL_KEY}: rows={rows:,}, days={target_stats['training_days']}, "
        f"features={len(features)}, dates={first_date}..{last_date}, purge={cutoff}")
    started = time.monotonic()
    dataset = lgb.Dataset(x, label=y, weight=weights, feature_name=features, free_raw_data=True)
    model = lgb.train(expected["params"], dataset, num_boost_round=ROUNDS)
    model_path.write_text(model.model_to_string(), encoding="utf-8")
    del dataset, x, y, weights
    gc.collect()
    valid_mask = pl.col("is_train") & pl.col("trade_date").is_between(
        year * 10000 + 101, year * 10000 + 1231)
    valid = (pl.scan_parquet(FEATURE_FILE).filter(valid_mask).sort("trade_date", "ts_code")
             .select(features + KEYS + ["price_valid"]).collect())
    valid_missingness = frozen.feature_missingness(valid)
    matrix = to_matrix(valid, features)
    raw = model.predict(matrix, num_threads=THREADS).astype(np.float32)
    valid_price = valid["price_valid"].to_numpy()
    raw[~valid_price] = -1e6
    if not np.isfinite(raw).all():
        raise AssertionError("Pooled auxiliary emitted nonfinite raw predictions")
    reloaded = lgb.Booster(model_str=model_path.read_text(encoding="utf-8"))
    if reloaded.feature_name() != features or reloaded.current_iteration() != ROUNDS:
        raise AssertionError("Saved weighted pooled auxiliary feature order or rounds differ")
    indices = np.linspace(0, len(raw) - 1, min(4096, len(raw)), dtype=int)
    checked = reloaded.predict(matrix[indices], num_threads=THREADS).astype(np.float32)
    checked[~valid_price[indices]] = -1e6
    reload_error = float(np.max(np.abs(checked.astype(float) - raw[indices].astype(float))))
    if reload_error != 0:
        raise AssertionError(f"Reloaded weighted pooled auxiliary differs: {reload_error}")
    result = valid.select(KEYS).with_columns(pl.Series("pred_raw", raw))
    if not result.select(KEYS).equals(load_panel(year).frame.select(KEYS)):
        raise AssertionError("Pooled auxiliary cache coverage/order differs from baseline")
    result.write_parquet(cache_path, compression="zstd")
    if fingerprint(year) != expected:
        raise AssertionError("Frozen source/input changed during OOF-weighted pooled-return training")
    metadata = {**expected, "training_rows": rows, "training_first_date": first_date,
                "training_last_date": last_date, "validation_rows": len(raw),
                "validation_days": valid["trade_date"].n_unique(),
                "validation_first_date": int(valid["trade_date"].min()),
                "validation_last_date": int(valid["trade_date"].max()),
                "target_stats": target_stats,
                "training_keys_sha256": training_keys_sha256,
                "training_keys_hash_encoding": "frame.select(KEYS).write_csv().encode('utf-8'); original training row order",
                "target_matches_pooled_reference_exact": True,
                "weight_statistics": weight_stats,
                "training_feature_missingness": train_missingness,
                "validation_feature_missingness": valid_missingness,
                "model_sha256": file_hash(model_path), "cache_sha256": file_hash(cache_path),
                "reload_check_rows": len(indices), "reload_max_abs_error": reload_error,
                "elapsed_seconds": time.monotonic() - started}
    meta_path.write_text(json.dumps(metadata, ensure_ascii=False, indent=2), encoding="utf-8")
    log(f"Saved {year}: rows={len(raw):,}, elapsed={metadata['elapsed_seconds']:.1f}s, reload={reload_error}")
    del model, reloaded, matrix, valid, raw, result
    gc.collect()
    load_raw(year)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("step", choices=("test", "check", "oof", "train"))
    parser.add_argument("--year", type=int)
    args = parser.parse_args()
    if args.step == "test":
        result = test_model()
        path = OUT / "model_tests.json"
        if path.exists() and _read(path) != result:
            raise ValueError("Preserve previous model tests: source or protocol changed")
        if not path.exists():
            path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
        log("Frozen OOF-region and 1.5x training-weight tests passed")
    elif args.step == "check":
        if args.year is None:
            log(f"Verified {len(_locked_sources())} frozen sources")
        else:
            log(f"Verified weighted {args.year} fingerprint {fingerprint(args.year)['fingerprint_sha256']}")
    elif args.year is None:
        parser.error("oof/train require --year; OOF2023 and outer2024 are independently gated")
    elif args.step == "oof":
        build_oof(args.year)
    else:
        train(args.year)
