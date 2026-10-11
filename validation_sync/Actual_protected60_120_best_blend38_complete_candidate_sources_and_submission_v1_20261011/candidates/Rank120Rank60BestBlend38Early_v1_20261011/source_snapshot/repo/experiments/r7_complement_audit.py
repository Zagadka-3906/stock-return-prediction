"""Independent audit of one frozen 90% r4 / 10% repaired-neural rank signal.

No fitting and no historical candidate generation. --test is synthetic only.
Explicit stage audits reproduce saved signals in memory, score original Float64
labels, and write new audit evidence without changing runner/frozen artifacts.
"""
from __future__ import annotations

import os
for _name in ("POLARS_MAX_THREADS", "OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_name] = "4"

import argparse
import hashlib
import json
from pathlib import Path
import sys
import tempfile
from unittest.mock import patch

import numpy as np
import polars as pl
from scipy.stats import rankdata

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from experiments.r6_transformer_audit import independent_official_score
from experiments.audit_r5_candidate import paired_block_bootstrap

OUT = ROOT / "experiments/r7_complement_20260926"
R6 = ROOT / "experiments/r6_transformer_20260926"
REFERENCES = ROOT / "experiments/revalidation_20260926/validation"
KEYS = ["ts_code", "trade_date"]
PRIMARY = "neural10"
REFERENCE_NAMES = ("baseline", "ensemble4")
YEARS = {"development": (2020, 2021, 2022), "confirmation": (2023, 2024)}
CONFIG = {"neural_weight": .1, "alpha": .9, "bonus": .3, "pooled_weight": .25, "top_current_weight": 1.0}
THRESHOLDS = {
    "development": {"mean_score_delta_min": .001, "worst_year_score_delta_min": -.005, "mean_ic_delta_min": -.002},
    "confirmation": {"mean_score_delta_min": .0005, "worst_year_score_delta_min": -.003, "mean_ic_delta_min": -.002},
}
BOOTSTRAP = {"block_days": 20, "draws": 20000, "seed": 2026, "positive_share_min": .8}
TRAIN_CONFIG = {"seed": 2026, "epochs": 30, "batch_days": 4, "dim": 32, "layers": 2,
                "heads": 4, "learning_rate": .001, "weight_decay": 1e-6, "alpha": .9,
                "bonus": .3, "pooled": .25, "precision": "float32; TF32 disabled", "threads": 4}


def sha(path: Path) -> str:
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def read(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def confined(base: Path, relative: str) -> Path:
    path = (base / relative).resolve()
    if not path.is_relative_to(base.resolve()):
        raise ValueError("Artifact path escaped its declared directory")
    return path


def _match(actual, expected, context: str = "", tolerance: float = 1e-12) -> float:
    """Strict recursive comparison; numeric tolerance never changes pass decisions."""
    if isinstance(actual, dict):
        if not isinstance(expected, dict) or actual.keys() != expected.keys():
            raise AssertionError(f"Different mapping keys: {context}")
        return max((_match(actual[k], expected[k], f"{context}/{k}", tolerance) for k in actual), default=0.)
    if isinstance(actual, (list, tuple)):
        if not isinstance(expected, (list, tuple)) or len(actual) != len(expected):
            raise AssertionError(f"Different sequence: {context}")
        return max((_match(a, b, f"{context}/{i}", tolerance) for i, (a, b) in enumerate(zip(actual, expected))), default=0.)
    if isinstance(actual, (float, int)) and not isinstance(actual, bool):
        if not isinstance(expected, (float, int)) or isinstance(expected, bool):
            raise AssertionError(f"Not numeric: {context}")
        difference = abs(float(actual) - float(expected))
        if not np.isfinite(actual) or not np.isfinite(expected) or difference > tolerance:
            raise AssertionError(f"Numerical difference {difference}: {context}")
        return difference
    if actual != expected or type(actual) is not type(expected):
        raise AssertionError(f"Value/type mismatch: {context}")
    return 0.


def aligned(frame: pl.DataFrame, other: pl.DataFrame) -> tuple[pl.DataFrame, pl.DataFrame]:
    """Never positionally combine unvalidated stock/date keys."""
    if any(any(f.select(KEYS).null_count().row(0)) for f in (frame, other)):
        raise ValueError("Null prediction keys")
    if not frame.schema["trade_date"].is_integer() or not other.schema["trade_date"].is_integer():
        raise ValueError("Trade dates must be integer YYYYMMDD values")
    other = other.with_columns(pl.col("trade_date").cast(frame.schema["trade_date"], strict=True))
    left, right = (f.sort("trade_date", "ts_code") for f in (frame, other))
    if any(f.select(pl.struct(KEYS).n_unique()).item() != len(f) for f in (left, right)):
        raise ValueError("Duplicate prediction keys")
    if not left.select(KEYS).equals(right.select(KEYS)):
        raise ValueError("Missing, additional or different prediction keys")
    return left, right


def _shape(frame: pl.DataFrame) -> tuple[int, int]:
    if not len(frame):
        raise ValueError("Empty panel")
    dates = frame["trade_date"].unique(maintain_order=True).to_numpy()
    n_days = len(dates)
    n_codes = len(frame) // n_days
    if len(frame) != n_days * n_codes:
        raise ValueError("Nonrectangular panel")
    codes = frame["ts_code"].to_numpy().reshape(n_days, n_codes)
    rows_dates = frame["trade_date"].to_numpy().reshape(n_days, n_codes)
    if (not np.all(codes == codes[:1]) or not np.all(rows_dates == dates[:, None])
            or np.any(np.diff(dates) <= 0)):
        raise ValueError("Dates or securities do not form a canonical full panel")
    return n_days, n_codes


def rebuild_raw(frame: pl.DataFrame, neural: pl.DataFrame, *, weight: float = .1) -> tuple[pl.DataFrame, np.ndarray]:
    """Daily average-tie percentiles on the full current price-valid universe.

    This audit implementation reads no label columns. Nonfinite predictions in
    that universe are errors, not reasons to silently select another universe.
    Alternate weights are used only by synthetic algebra tests.
    """
    if not np.isfinite(weight) or not 0 <= weight <= 1:
        raise ValueError("Invalid rank weight")
    frame, neural = aligned(frame, neural)
    shape = _shape(frame)
    if frame.schema["price_valid"] != pl.Boolean or frame["price_valid"].null_count():
        raise ValueError("Current price validity must be nonnull Boolean")
    valid = frame["price_valid"].to_numpy().reshape(shape)
    base = frame["pred_raw"].to_numpy().astype(np.float64).reshape(shape)
    other = neural["pred_raw"].to_numpy().astype(np.float64).reshape(shape)
    if not np.isfinite(base[valid]).all() or not np.isfinite(other[valid]).all():
        raise ValueError("A price-valid member has a nonfinite raw signal")
    result = np.full(shape, -10., dtype=np.float64)
    for day in range(shape[0]):
        mask = valid[day]
        if mask.any():
            n = int(mask.sum())
            a = rankdata(base[day, mask], method="average") / n
            b = rankdata(other[day, mask], method="average") / n
            result[day, mask] = (1 - weight) * a + weight * b
    return frame, result.reshape(-1)


def rebuild_post(frame: pl.DataFrame, raw: np.ndarray) -> np.ndarray:
    """Independent transcription of the unchanged EMA/retention/protected head.

    The persistence state uses its own historical scores, never the subsequent
    current-rank or auxiliary reorder. Small pools, invalid Top members, and
    boundary ties follow the frozen production fallbacks exactly.
    """
    shape = _shape(frame)
    values = np.asarray(raw, dtype=np.float64).reshape(shape)
    valid = frame["price_valid"].to_numpy().reshape(shape) & np.isfinite(values)
    up = frame["flag_limit_up"].to_numpy().reshape(shape)
    aux = frame["aux_raw"].to_numpy().astype(np.float64).reshape(shape)
    smoothed, stable = np.empty(shape), np.empty(shape)
    previous_top = np.zeros(shape[1], dtype=bool)
    for day in range(shape[0]):
        ranks = np.full(shape[1], -10.)
        if valid[day].any():
            ranks[valid[day]] = rankdata(values[day, valid[day]], method="average") / valid[day].sum()
        smoothed[day] = ranks if day == 0 else np.where(
            valid[day - 1], (1 - CONFIG["alpha"]) * ranks + CONFIG["alpha"] * smoothed[day - 1], ranks)
        smoothed[day, ~valid[day]] = -10.
        stable[day] = smoothed[day]
        stable[day, previous_top] += CONFIG["bonus"]
        eligible = np.flatnonzero(up[day] == 0)
        previous_top[:] = False
        if len(eligible) >= 100:
            pick = eligible[np.argsort(-stable[day, eligible], kind="stable")[:max(len(eligible) // 10, 1)]]
            previous_top[pick] = True

    result = np.full(shape, -10.)
    for day in range(shape[0]):
        eligible = np.flatnonzero(up[day] == 0)
        k = max(len(eligible) // 10, 1)
        if not len(eligible) or not valid[day].any():
            result[day] = stable[day]
            continue
        selected = eligible[np.argsort(-stable[day, eligible], kind="stable")[:k]]
        if not valid[day, selected].all():
            result[day] = stable[day]
            continue
        upper = valid[day] & (stable[day] >= stable[day, selected].min())
        lower = valid[day] & ~upper
        count, lower_count = int(valid[day].sum()), int(lower.sum())
        result[day, lower] = rankdata(values[day, lower], method="average") / count
        upper_rank = rankdata(stable[day, upper], method="average")
        unambiguous = np.count_nonzero(upper & (up[day] == 0)) == k
        if unambiguous:
            current = rankdata(values[day, upper], method="average")
            upper_rank = rankdata((1 - CONFIG["top_current_weight"]) * upper_rank
                                  + CONFIG["top_current_weight"] * current, method="average")
        result[day, upper] = (lower_count + upper_rank) / count
        if unambiguous and np.isfinite(aux[day, upper]).all():
            n_upper = int(upper.sum())
            a = rankdata(values[day, upper], method="average") / n_upper
            b = rankdata(aux[day, upper], method="average") / n_upper
            ranks = rankdata((1 - CONFIG["pooled_weight"]) * a + CONFIG["pooled_weight"] * b, method="average")
            result[day, upper] = (count - n_upper + ranks) / count
    return result.reshape(-1)


def point_gate(metrics: dict, stage: str) -> dict:
    years = YEARS[stage]
    limits, comparisons = THRESHOLDS[stage], {}
    for name in REFERENCE_NAMES:
        scores = [metrics[PRIMARY][str(y)]["final_score"] - metrics[name][str(y)]["final_score"] for y in years]
        ics = [metrics[PRIMARY][str(y)]["ic_mean"] - metrics[name][str(y)]["ic_mean"] for y in years]
        mean, worst, ic = float(np.mean(scores)), min(scores), float(np.mean(ics))
        comparisons[name] = {"mean_score_delta": mean, "worst_year_score_delta": worst,
                             "mean_ic_delta": ic, "score_deltas": dict(zip(map(str, years), scores)),
                             "passed": bool(mean >= limits["mean_score_delta_min"]
                                and worst >= limits["worst_year_score_delta_min"] and ic >= limits["mean_ic_delta_min"])}
    return {"comparisons": comparisons, "passed": all(x["passed"] for x in comparisons.values())}


def _checked_hashes(base: Path, manifest: dict) -> dict:
    if not isinstance(manifest, dict) or not manifest:
        raise AssertionError("Empty artifact/input binding")
    checked = {}
    for relative, expected in manifest.items():
        path = confined(base, relative)
        actual = sha(path)
        if actual != expected:
            raise AssertionError(f"Changed bound file: {relative}")
        checked[path.relative_to(ROOT).as_posix()] = actual
    return checked


def verify_protocol() -> tuple[dict, dict]:
    protocol = read(OUT / "protocol.json")
    _match(protocol["config"], CONFIG, "protocol/config", 0.)
    for stage in YEARS:
        _match(protocol[f"{stage}_years"], list(YEARS[stage]), f"protocol/{stage}_years", 0.)
        _match(protocol["gates"][stage], THRESHOLDS[stage], f"protocol/{stage}_gate", 0.)
    _match(protocol["gates"]["bootstrap"], BOOTSTRAP, "protocol/bootstrap", 0.)
    if protocol["primary_candidate"] != PRIMARY:
        raise AssertionError("Only the predeclared neural10 candidate is permitted")
    required = [Path(__file__), ROOT / "experiments/r6_transformer_audit.py",
                ROOT / "experiments/audit_r5_candidate.py", ROOT / "evaluate.py", ROOT / "data" / "raw" / "训练集.csv"]
    if not {p.relative_to(ROOT).as_posix() for p in required} <= protocol["input_sha256"].keys():
        raise AssertionError("Missing frozen scorer/auditor/original-label source")
    return protocol, _checked_hashes(ROOT, protocol["input_sha256"])


def _check_stage_record(record: dict, stage: str, protocol_sha: str) -> None:
    if (record["protocol_sha256"] != protocol_sha or record["primary_candidate"] != PRIMARY
            or record["completed_years"] != list(YEARS[stage])
            or set(record["fold_sha256"]) != {f"fold_{year}.json" for year in YEARS[stage]}):
        raise AssertionError("Wrong protocol/candidate, missing fold, extra fold or partial stage")


def _stage_pass(gate: dict, bootstrap: dict | None) -> bool:
    if not gate["passed"]:
        if bootstrap is not None:
            raise AssertionError("Bootstrap must be skipped when point gates fail")
        return False
    if bootstrap is None or set(bootstrap) != set(REFERENCE_NAMES):
        raise AssertionError("Both reference bootstraps are required after point-gate success")
    for entry in bootstrap.values():
        if any(entry[name] != BOOTSTRAP[name] for name in ("block_days", "draws", "seed")):
            raise AssertionError("Bootstrap settings changed")
    return all(row["bootstrap_share_positive"] >= BOOTSTRAP["positive_share_min"] for row in bootstrap.values())


def _authorize_confirmation(protocol_sha: str) -> dict:
    """This function touches development artifacts only; failed gates deny access."""
    dev = read(OUT / "development.json")
    _check_stage_record(dev, "development", protocol_sha)
    if not dev["development_gate_passed"] or not _stage_pass(dev["gate"], dev["bootstrap"]):
        raise ValueError("Development failed; confirmation access is prohibited")
    evidence = read(OUT / "independent_audit/development/score_audit.json")
    if (evidence["status"] != "passed" or evidence["stage_gate_passed"] is not True
            or evidence["stage_record_sha256"] != sha(OUT / "development.json")
            or evidence["protocol_sha256"] != protocol_sha or evidence["source_sha256"] != sha(Path(__file__))):
        raise AssertionError("Confirmation requires unchanged passed independent development evidence")
    _checked_hashes(ROOT, evidence["artifacts_sha256"])
    return dev


def _check_training(year: int, fold: dict, protocol_sha: str) -> dict:
    """Validate the new confirmation training lineage without refitting/reinference."""
    folder = OUT / "neural_training"
    paths = [folder / "protocol.json", folder / f"training_feature_identity_{year}.json",
             folder / f"model_feature_identity_{year}.pt", folder / f"checkpoint_feature_identity_{year}.pt",
             folder / f"scaler_{year}.npz", folder / f"raw_feature_identity_{year}.parquet"]
    for path in paths:
        if fold["input_sha256"].get(path.relative_to(ROOT).as_posix()) != sha(path):
            raise AssertionError("Confirmation training source missing from fold binding")
    nested = read(paths[0])
    if nested["parent_protocol_sha256"] != protocol_sha:
        raise AssertionError("Nested training protocol has another r7 parent")
    _match(nested["config"], TRAIN_CONFIG, "nested training config", 0.)
    meta = read(paths[1])
    cutoff = {2023: 20221230, 2024: 20231229}[year]
    if (meta["year"] != year or meta["variant"] != "feature_identity" or meta["epochs"] != 30
            or meta["feature_count"] != 63 or not meta["train_state_has_only_past_rows"]
            or not meta["raw_16day_prefix_exact"] or meta["training_cutoff_exclusive"] != cutoff
            or meta["scaler_stats"]["cutoff_exclusive"] != cutoff
            or not (meta["last_training_date"] < meta["last_label_available_date"] == cutoff < meta["first_validation_date"])
            or [x["epoch"] for x in meta["curve"]] != list(range(1, 31))):
        raise AssertionError("Fixed epochs, feature count or training chronology violated")
    batches = meta["training_days"] // 4 + int(meta["training_days"] % 4 >= 2)
    if any(row["batches"] != batches or not np.isfinite(row["mean_train_loss"]) for row in meta["curve"]):
        raise AssertionError("Training batches/losses disagree with the fixed regime")
    _checked_hashes(folder, meta["artifact_sha256"])
    with np.load(paths[4]) as scaler:
        for name in ("mean", "std"):
            array = scaler[name]
            digest = hashlib.sha256(np.ascontiguousarray(array, dtype=np.float32).tobytes()).hexdigest()
            if (array.shape != (63,) or not np.isfinite(array).all() or (name == "std" and np.any(array <= 0))
                    or digest != meta["scaler_stats"][f"{name}_sha256"]):
                raise AssertionError("Scaler differs from past-only training metadata")
    import torch
    model = torch.load(paths[2], map_location="cpu", weights_only=False)
    checkpoint = torch.load(paths[3], map_location="cpu", weights_only=False)
    if (model["variant"] != "feature_identity" or len(model["features"]) != 63
            or len(set(model["features"])) != 63 or model["protocol_sha256"] != sha(paths[0])
            or checkpoint["protocol_sha256"] != sha(paths[0]) or checkpoint["epoch"] != 30
            or checkpoint["scaler_sha256"] != sha(paths[4])):
        raise AssertionError("Model/checkpoint do not bind final-epoch training artifacts")
    if model["features"] != read(ROOT / "data/feature_manifest.json")["features"]:
        raise AssertionError("Saved model feature identity/order differs from the frozen manifest")
    _match(model["config"], TRAIN_CONFIG, "saved model config", 0.)
    _match(checkpoint["curve"], meta["curve"], "checkpoint/metadata curve")
    if model["state_dict"].keys() != checkpoint["model"].keys() or any(
            not torch.equal(tensor, checkpoint["model"][name]) for name, tensor in model["state_dict"].items()):
        raise AssertionError("Saved model differs from epoch30 checkpoint")
    return {"fixed_epoch30_and_past_only_metadata": True, "scaler_hash_verified": True,
            "model_equals_final_checkpoint": True, "raw_prefix_exact_reported": True,
            "limitation": "Saved metadata/model lineage checked; no independent refit or neural reinference."}


def audit(stage: str = "development") -> dict:
    if stage not in YEARS:
        raise ValueError(stage)
    output = OUT / "independent_audit" / stage
    if output.exists():
        raise FileExistsError("Preserve completed or partial independent audit evidence")
    protocol, artifacts = verify_protocol()
    protocol_sha = sha(OUT / "protocol.json")
    if stage == "confirmation":
        _authorize_confirmation(protocol_sha)
    record_path = OUT / f"{stage}.json"
    record = read(record_path)
    _check_stage_record(record, stage, protocol_sha)
    if stage == "confirmation" and (record["development_sha256"] != sha(OUT / "development.json")
            or record["development_audit_sha256"] != sha(OUT / "independent_audit/development/score_audit.json")):
        raise AssertionError("Confirmation does not bind its audited development decision")
    folds = {}
    for year in YEARS[stage]:
        path = OUT / f"fold_{year}.json"
        if sha(path) != record["fold_sha256"][path.name]:
            raise AssertionError("Fold record checksum mismatch")
        fold = read(path)
        if fold["year"] != year or fold["candidate_key"] != PRIMARY or set(fold["references"]) != set(REFERENCE_NAMES):
            raise AssertionError("Unexpected fold identity or references")
        artifacts.update(_checked_hashes(OUT, fold["artifact_sha256"]))
        artifacts.update(_checked_hashes(ROOT, fold["input_sha256"]))
        artifacts[path.relative_to(ROOT).as_posix()] = sha(path)
        folds[year] = fold
    # Create the audit directory only once all prerequisite bindings pass.
    output.mkdir(parents=True, exist_ok=False)
    metrics, raw_metrics, daily, checks = {}, {}, {}, {}
    maximum = {"runner_metric": 0., "saved_raw": 0., "saved_final": 0., "r4_reconstruction": 0.}
    for year in YEARS[stage]:
        fold = folds[year]
        candidate = OUT / f"predictions_{PRIMARY}_{year}.parquet"
        r4 = REFERENCES / f"predictions_ensemble4_{year}.parquet"
        neural = (R6 if stage == "development" else OUT / "neural_training") / f"raw_feature_identity_{year}.parquet"
        if candidate.name not in fold["artifact_sha256"]:
            raise AssertionError("Candidate parquet is not bound by the fold")
        for path in (r4, neural, REFERENCES / f"predictions_baseline_{year}.parquet"):
            if fold["input_sha256"].get(path.relative_to(ROOT).as_posix()) != sha(path):
                raise AssertionError(f"Missing fixed input binding: {path.name}")
        base, saved = aligned(pl.read_parquet(r4), pl.read_parquet(candidate))
        unchanged = [column for column in base.columns if column not in ("pred_raw", "pred")]
        if set(base.columns) != set(saved.columns) or not base.select(unchanged).equals(saved.select(unchanged)):
            raise AssertionError("Candidate changed original frame fields/Float64 labels/pooled auxiliary")
        base, raw = rebuild_raw(base, pl.read_parquet(neural, columns=KEYS + ["pred_raw"]))
        final = rebuild_post(base, raw)
        r4_rebuilt = rebuild_post(base, base["pred_raw"].to_numpy())
        for name, observed, expected in (("saved_raw", raw, saved["pred_raw"].to_numpy()),
                                          ("saved_final", final, saved["pred"].to_numpy()),
                                          ("r4_reconstruction", r4_rebuilt, base["pred"].to_numpy())):
            error = float(np.max(np.abs(observed - expected)))
            if not np.isfinite(error) or error > 1e-12:
                raise AssertionError(f"Independent signal/post mismatch: {year}/{name}={error}")
            maximum[name] = max(maximum[name], error)
        checks[str(year)] = {"strict_key_alignment": True, "original_frame_preserved": True,
                             "independent_blend_and_post_reconstruction": True}
        if stage == "confirmation":
            checks[str(year)]["training"] = _check_training(year, fold, protocol_sha)
        for key in (PRIMARY, *REFERENCE_NAMES):
            path = candidate if key == PRIMARY else REFERENCES / f"predictions_{key}_{year}.parquet"
            result, rows, details = independent_official_score(path, year)
            expected = fold["metrics"] if key == PRIMARY else fold["references"][key]
            maximum["runner_metric"] = max(maximum["runner_metric"], _match(result, expected, f"{key}/{year}"))
            metrics.setdefault(key, {})[str(year)] = result
            daily.setdefault(key, {})[year] = rows
            checks[str(year)][key] = details
            rows.write_csv(output / f"official_{key}_{year}_daily.csv", float_precision=17)
        result, rows, details = independent_official_score(candidate, year, column="pred_raw")
        maximum["runner_metric"] = max(maximum["runner_metric"], _match(result, fold["raw_metrics"], f"raw/{year}"))
        raw_metrics[str(year)] = result
        checks[str(year)]["raw"] = details
        rows.write_csv(output / f"official_{PRIMARY}_raw_{year}_daily.csv", float_precision=17)
        print(json.dumps({"audit_year_completed": year, "stage": stage}, ensure_ascii=False), flush=True)
    gate = point_gate(metrics, stage)
    _match(gate, record["gate"], "stage/gate")
    _match(gate["passed"], record["point_gate_passed"], "stage/point_gate_passed")
    bootstrap = None
    if gate["passed"]:
        bootstrap = {name: paired_block_bootstrap(daily[PRIMARY], daily[name], block_days=20, draws=20000, seed=2026)
                     for name in REFERENCE_NAMES}
    _match(bootstrap, record["bootstrap"], "stage/bootstrap")
    passed = _stage_pass(gate, bootstrap)
    _match(passed, record[f"{stage}_gate_passed"], "stage/pass")
    artifacts[record_path.relative_to(ROOT).as_posix()] = sha(record_path)
    artifacts[(OUT / "protocol.json").relative_to(ROOT).as_posix()] = protocol_sha
    for path in output.glob("*.csv"):
        artifacts[path.relative_to(ROOT).as_posix()] = sha(path)
    result = {"status": "passed", "status_meaning": "Audit agreement, not candidate qualification or publication",
              "stage": stage, "primary_candidate": PRIMARY, "completed_years": list(YEARS[stage]),
              "stage_gate_passed": passed, "stage_record_sha256": sha(record_path),
              "protocol_sha256": protocol_sha, "source_sha256": sha(Path(__file__)),
              "gate": gate, "bootstrap": bootstrap, "metrics": metrics, "raw_metrics": raw_metrics,
              "max_absolute_difference": maximum, "checks": checks, "artifacts_sha256": artifacts,
              "retrospective_previously_viewed": True, "automatic_publication": False,
              "limitation": "A new historical hypothesis after r6; all years previously viewed. Bootstrap/HAC do not correct cross-round model selection."}
    with (output / "score_audit.json").open("x", encoding="utf-8") as stream:
        json.dump(result, stream, ensure_ascii=False, indent=2, allow_nan=False)
    return result


def synthetic_tests() -> dict:
    """Artificial fixtures only; no protocol, market parquet or historical score reads."""
    from experiments.cached_recheck import make_prediction
    from src.scoring import Panel
    checks = {}
    tiny = pl.DataFrame({"ts_code": ["a", "b", "c", "d"], "trade_date": [20200102] * 4,
                         "price_valid": [True, True, True, False], "pred_raw": [1., 1., 3., np.nan]})
    t = tiny.select(KEYS).with_columns(pl.Series("pred_raw", [3., 1., 1., np.inf]))
    _, observed = rebuild_raw(tiny, t)
    np.testing.assert_allclose(observed, [.55, .5, .95, -10.], rtol=0., atol=2e-16)
    _, zero = rebuild_raw(tiny, t, weight=0.)
    np.testing.assert_array_equal(zero, [.5, .5, 1., -10.])
    _, permuted = rebuild_raw(tiny.reverse(), t.reverse())
    np.testing.assert_array_equal(observed, permuted)
    checks["hand_calculated_average_ties_and_invalid_sentinel"] = True
    checks["zero_weight_and_key_permutation"] = True
    bad_inputs = [(tiny, t.head(3)), (pl.concat([tiny, tiny.head(1)]), t),
                  (tiny, t.with_columns(pl.when(pl.col("ts_code") == "a").then(float("nan")).otherwise(pl.col("pred_raw")).alias("pred_raw")))]
    for frame, neural in bad_inputs:
        try:
            rebuild_raw(frame, neural)
        except ValueError:
            pass
        else:
            raise AssertionError("Invalid keys/predictions were accepted")
    checks["reject_missing_duplicate_nonfinite_valid_input"] = True
    rng = np.random.default_rng(2026)
    n_days, n_codes = 8, 120
    total = n_days * n_codes
    valid = np.ones((n_days, n_codes), dtype=bool)
    valid[1:4, 0] = False
    valid[4, :] = False
    flags = np.zeros((n_days, n_codes), dtype=int)
    flags[3, :30] = 1
    flags[6, :] = 1
    base_values = rng.normal(size=(n_days, n_codes))
    base_values[0] = 1.  # Deliberate protected boundary ties before any retention.
    base_values[2] = 1.
    auxiliary = rng.normal(size=(n_days, n_codes))
    auxiliary[5] = np.nan  # The unchanged pooled-head fallback must remain valid.
    frame = pl.DataFrame({"ts_code": np.tile([f"s{i:03}" for i in range(n_codes)], n_days),
                          "trade_date": np.repeat(np.arange(20200102, 20200102 + n_days), n_codes),
                          "price_valid": valid.reshape(-1), "flag_limit_up": flags.reshape(-1),
                          "pred_raw": base_values.reshape(-1), "aux_raw": auxiliary.reshape(-1),
                          "y_ret_1d": rng.normal(size=total)})
    neural = frame.select(KEYS).with_columns(pl.Series("pred_raw", rng.normal(size=total)))
    base, mixed = rebuild_raw(frame, neural)
    final = rebuild_post(base, mixed)
    panel = Panel.from_frame(base.with_columns(pl.Series("pred_raw", mixed)))
    production = make_prediction(panel, base["aux_raw"].to_numpy(), "top_only", .25)
    np.testing.assert_array_equal(final, production)
    # Exercise exact ties and all production fallback branches with unblended raw.
    np.testing.assert_array_equal(rebuild_post(base, base["pred_raw"].to_numpy()),
                                  make_prediction(Panel.from_frame(base), base["aux_raw"].to_numpy(), "top_only", .25))
    _, raw0 = rebuild_raw(base, neural, weight=0.)
    np.testing.assert_array_equal(rebuild_post(base, raw0), rebuild_post(base, base["pred_raw"].to_numpy()))
    checks["independent_post_equals_frozen_pipeline_ties_empty_small_invalid_resumption"] = True
    checks["zero_neural_weight_preserves_full_post"] = True
    deleted = base.drop("y_ret_1d")
    mutated = base.with_columns(pl.lit(None, dtype=pl.Float64).alias("y_ret_1d"))
    for changed in (deleted, mutated):
        _, changed_raw = rebuild_raw(changed, neural)
        np.testing.assert_array_equal(changed_raw, mixed)
        np.testing.assert_array_equal(rebuild_post(changed, changed_raw), final)
    prefix, prefix_raw = rebuild_raw(base.head(3 * n_codes), neural.head(3 * n_codes))
    np.testing.assert_array_equal(rebuild_post(prefix, prefix_raw), final[:3 * n_codes])
    checks["label_deleted_or_changed_invariance"] = True
    checks["future_append_prefix_exact"] = True
    with tempfile.TemporaryDirectory(prefix="r7-audit-synthetic-") as folder:
        path = Path(folder) / "synthetic.parquet"
        base.with_columns(pl.Series("pred_raw", mixed), pl.Series("pred", final)).write_parquet(path)
        loaded = pl.read_parquet(path)
        np.testing.assert_array_equal(loaded["pred_raw"].to_numpy(), mixed)
        np.testing.assert_array_equal(loaded["pred"].to_numpy(), final)
    checks["parquet_float64_roundtrip"] = True
    metrics = {name: {str(y): {"final_score": 0., "ic_mean": 0.} for y in YEARS["development"]}
               for name in (*REFERENCE_NAMES, PRIMARY)}
    for row in metrics[PRIMARY].values():
        row.update(final_score=.001, ic_mean=-.002)
    assert point_gate(metrics, "development")["passed"]
    metrics[PRIMARY]["2020"]["final_score"] = np.nextafter(.001, -np.inf).item()
    for row in metrics[PRIMARY].values():
        row["final_score"] = np.nextafter(.001, -np.inf).item()
    assert not point_gate(metrics, "development")["passed"]
    assert _stage_pass({"passed": False}, None) is False
    for b in ({}, {name: {**{k: BOOTSTRAP[k] for k in ("block_days", "draws", "seed")},
                           "bootstrap_share_positive": .8} for name in REFERENCE_NAMES}):
        if b:
            assert _stage_pass({"passed": True}, b)
            b["baseline"]["bootstrap_share_positive"] = np.nextafter(.8, 0.).item()
            assert not _stage_pass({"passed": True}, b)
        else:
            try:
                _stage_pass({"passed": True}, b)
            except AssertionError:
                pass
            else:
                raise AssertionError("Missing bootstrap accepted")
    checks["strict_point_and_noise_gate_boundaries"] = True
    fake_record = {"protocol_sha256": "fake", "primary_candidate": PRIMARY,
                   "completed_years": [2020, 2021], "fold_sha256": {"fold_2020.json": "x", "fold_2021.json": "y"}}
    try:
        _check_stage_record(fake_record, "development", "fake")
    except AssertionError:
        pass
    else:
        raise AssertionError("Partial development accepted")
    checks["reject_partial_or_extra_stage_folds"] = True
    with tempfile.TemporaryDirectory(prefix="r7-stage-guard-synthetic-") as folder:
        fake_out = Path(folder)
        fake_dev = {"protocol_sha256": "fake", "primary_candidate": PRIMARY,
                    "completed_years": list(YEARS["development"]),
                    "fold_sha256": {f"fold_{y}.json": "fake" for y in YEARS["development"]},
                    "gate": {"passed": False}, "bootstrap": None, "development_gate_passed": False}
        (fake_out / "development.json").write_text(json.dumps(fake_dev), encoding="utf-8")
        with patch.dict(globals(), OUT=fake_out):
            try:
                _authorize_confirmation("fake")
            except ValueError:
                pass
            else:
                raise AssertionError("Failed development authorized confirmation")
            fake_dev.update(gate={"passed": True}, development_gate_passed=True,
                            bootstrap={name: {"block_days": 20, "draws": 20000, "seed": 2026,
                                              "bootstrap_share_positive": .8} for name in REFERENCE_NAMES})
            (fake_out / "development.json").write_text(json.dumps(fake_dev), encoding="utf-8")
            try:
                _authorize_confirmation("fake")
            except FileNotFoundError:
                pass
            else:
                raise AssertionError("Missing development audit authorized confirmation")
            evidence_dir = fake_out / "independent_audit/development"
            evidence_dir.mkdir(parents=True)
            (evidence_dir / "score_audit.json").write_text(json.dumps({
                "status": "passed", "stage_gate_passed": True, "stage_record_sha256": "altered",
                "protocol_sha256": "fake", "source_sha256": sha(Path(__file__))}), encoding="utf-8")
            try:
                _authorize_confirmation("fake")
            except AssertionError:
                pass
            else:
                raise AssertionError("Changed development audit binding authorized confirmation")
    checks["confirmation_denies_failed_missing_or_changed_development_audit"] = True
    artificial = {}
    for year in (2020, 2021):
        artificial[year] = pl.DataFrame({"trade_date": np.arange(year * 10000 + 101, year * 10000 + 121),
            "rank_ic": np.linspace(-.1, .1, 20), "excess": np.linspace(-.01, .01, 20),
            "turnover": [None] + [.1] * 19})
    positive = {year: rows.with_columns((pl.col("rank_ic") + .01).alias("rank_ic")) for year, rows in artificial.items()}
    b1 = paired_block_bootstrap(positive, artificial, block_days=20, draws=64, seed=2026)
    b2 = paired_block_bootstrap(positive, artificial, block_days=20, draws=64, seed=2026)
    _match(b1, b2, "synthetic bootstrap reproducibility", 0.)
    assert b1["bootstrap_share_positive"] == 1. and abs(b1["observed_mean_annual_score_delta"] - .004) < 1e-14
    checks["paired_bootstrap_fixed_seed_and_finite_turnover_denominator"] = True
    return {"status": "passed", "synthetic_only": True, "historical_artifacts_read": False,
            "checks": checks, "source_sha256": sha(Path(__file__))}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("stage", nargs="?", choices=["development", "confirmation"])
    parser.add_argument("--test", action="store_true")
    args = parser.parse_args()
    if args.test and args.stage:
        parser.error("--test cannot be combined with a historical audit stage")
    result = synthetic_tests() if args.test or args.stage is None else audit(args.stage)
    if args.stage:
        result = {key: result[key] for key in ("status", "stage", "stage_gate_passed", "max_absolute_difference")}
    print(json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False), flush=True)
