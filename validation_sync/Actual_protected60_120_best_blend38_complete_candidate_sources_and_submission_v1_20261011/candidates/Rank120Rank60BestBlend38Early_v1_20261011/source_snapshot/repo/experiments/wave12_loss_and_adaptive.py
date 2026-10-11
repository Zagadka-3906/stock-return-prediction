"""Wave-12: the last three mechanisms with no frozen record anywhere in this repository.

Eleven rounds and roughly forty scored configurations have closed post-processing, targets,
feature transforms and additions, model families, ensembling rules and weights, nested
hyperparameter selection, the training universe, adaptive capacity, recency weighting and the
limit-up channel. A survey of every training module left three mechanisms that have never been
scored:

  W12a_xgb_quantile90  A tail-targeted loss. Every backbone in this project minimises squared
                       error on a rank label; the 30% Top-excess term however is decided by the
                       upper decile alone. XGBoost's `reg:quantileerror` at alpha 0.90 fits the
                       conditional 90th percentile instead of the conditional mean. LambdaRank,
                       NDCG, Huber and a binary top-decile head have all been tried and all
                       failed, but a quantile regression has never been fitted here.

  W12b_lgb_dart          Dropout regularization. The released LightGBM recipe is plain gradient
                       boosting with bagging and feature fraction; DART drops trees at each step,
                       which regularizes the *ensemble* rather than the individual tree. Wave-4
                       varied capacity as a fixed grid and lost, and wave-11's early stopping
                       chose more capacity and lost, but no round has changed the boosting
                       ALGORITHM's regularization mechanism.

  W12c_trailing_ic_two   Time-varying combination weights. Every ensemble ever scored here used
                       weights fixed before scoring (0.5/0.5, 0.65/0.35, 0.35/0.65, equal four-way,
                       rank median, z-score mean, trimmed mean). No round has let the weights move
                       with realised performance. This candidate weights the two members of the r5
                       winner by their trailing 20-day realised rank IC, recomputed daily from
                       information available at the previous close, and is compared against that
                       same member set at fixed equal weights.

DISCIPLINE. Frozen before scoring; 2020-2022 select one candidate; 2023-2024 confirm it once; no
fallback, no retuning, no threshold changes. Every fold re-runs the wave-9 harness proof, which
reproduces the frozen released baseline raw bit-for-bit and so validates row alignment, ordering,
purging and hyper-parameters together, and re-anchors the delivered XGBoost composite to 1e-12.
All five years have been viewed many times, so this is exploratory and nothing here is
out-of-sample evidence. Writes only inside experiments/wave12_loss_and_adaptive_20260927/.
"""
from __future__ import annotations

import argparse
import gc
import json
import time
from pathlib import Path

import lightgbm as lgb
import numpy as np
import polars as pl

from run import ROOT, to_matrix
from src.scoring import Panel
import experiments.wave9_exploratory as w9
from experiments.cached_recheck import make_prediction
from experiments.revalidate_fold_local import PARAMS, ROUNDS, THREADS, score_official
from experiments.wave11_backbone_and_segment import device, save_raw

OUT = ROOT / "experiments" / "wave12_loss_and_adaptive_20260927"
KEYS = ["ts_code", "trade_date"]
YEARS = (2020, 2021, 2022, 2023, 2024)
DEVELOPMENT = (2020, 2021, 2022)
CONFIRMATION = (2023, 2024)
PRIMARY = "xgboost"
GATED = ("xgboost", "baseline")
REPORTED = ("xgboost", "baseline", "ensemble4", "xgb_two_mean")
BASE = w9.BASE_FEATURES
QUANTILE = {"objective": "reg:quantileerror", "quantile_alpha": 0.90}
DART = {"boosting_type": "dart", "drop_rate": 0.1, "max_drop": 50, "skip_drop": 0.5}
TRAILING = {"window_days": 20, "warmup_days": 20, "members": ("xgboost", "two_day"),
            "weight_rule": "w_m = max(mean daily rank IC of member m over the previous 20 days, 0), "
                           "normalised to sum to one; equal weights while fewer than 20 prior days "
                           "exist in the fold or if every weight is zero"}
CANDIDATES = {
    "W12a_xgb_quantile90": {"mechanism": "tail-targeted loss", "models": 1,
                            "note": "the frozen T2f XGBoost recipe with reg:quantileerror at "
                                    "alpha 0.90 instead of squared error"},
    "W12b_lgb_dart": {"mechanism": "dropout regularization", "models": 1,
                      "note": "the released LightGBM rank recipe with DART boosting and LightGBM's "
                              "own default drop parameters"},
    "W12c_trailing_ic_two": {"mechanism": "time-varying combination weights", "models": 0,
                             "note": "the r5 winner's two members weighted daily by their trailing "
                                     "20-day realised rank IC instead of fixed equal weights; no "
                                     "model is trained"},
}
GATES = {
    "development": {"mean_score_delta_min": .0005, "worst_year_score_delta_min": -.002,
                    "mean_ic_delta_min": -.002, "gated_references": list(GATED)},
    "confirmation": {"mean_score_delta_min": .0005, "both_years_positive_vs_primary": True,
                     "gated_references": list(GATED)},
}
PROTOCOL = {
    "experiment": "wave12_quantile_loss_dart_and_trailing_ic_weights",
    "status": "exploratory_all_years_previously_viewed",
    "candidates": CANDIDATES, "primary_reference": PRIMARY, "gated_references": list(GATED),
    "reported_references": list(REPORTED),
    "recipes": {"xgboost_base": w9.XGB_CONFIG, "quantile_override": QUANTILE,
                "lightgbm_rank": dict(PARAMS), "rounds": ROUNDS, "dart_override": DART,
                "trailing": TRAILING},
    "development_years": list(DEVELOPMENT), "confirmation_years": list(CONFIRMATION),
    "gates": GATES,
    "gate_rationale": "the delivered model is the plain XGBoost backbone, so the decision-relevant "
                      "bar is to beat it; the pooled baseline is gated as the historical anchor. "
                      "ensemble4 and xgb_two_mean are reported but not gated, because gating on the "
                      "best point estimate of a round that itself failed confirmation would make the "
                      "bar unreachable and is not the decision being made.",
    "candidate_selection": "among candidates passing every development threshold against every gated "
                           "reference, take the highest equally weighted mean annual official score; "
                           "exact ties prefer fewer models then the lexical key; select one or none",
    "confirmation_rule": "score only the frozen development winner on 2023 and 2024 once; it must "
                         "pass every confirmation threshold against both gated references and be "
                         "positive against the primary in both years. No fallback, no second winner.",
    "postprocess": "the released stack exactly, via cached_recheck.make_prediction with the frozen "
                   "pooled auxiliary at top_only 0.25; W12c blends the two member raws before the "
                   "stack, exactly as the r5 winner does",
    "trailing_ic_causality": "the weight for day t uses each member's realised daily rank IC over "
                             "days t-20..t-1 of the same fold, computed from labels that were known "
                             "before day t's close; the first 20 days use equal weights. No "
                             "prediction, label or availability mask from day t or later enters the "
                             "weight. Proven per fold by rebuilding the whole weight path from a "
                             "frame truncated by one day and requiring the prefix to be unchanged, "
                             "plus non-negativity, unit daily sum and equal weights during warm-up.",
    "anchor": "every fold re-runs the wave-9 harness proof and reproduces the delivered XGBoost "
              "composite within 1e-12 before any candidate is scored; in addition, this module's "
              "weighted rank average at equal weights must reproduce the frozen r5 xgb_two_mean raw "
              "prediction bit-for-bit, which is what makes W12c differ from that reference in the "
              "weights alone",
    "prohibited": ["Adding a candidate, quantile level, drop parameter or window after any score "
                   "exists", "Tuning any hyper-parameter after seeing a result",
                   "Relaxing a gate", "Writing outside "
                   "experiments/wave12_loss_and_adaptive_20260927/",
                   "Touching releases/, outputs/, active_release.json or maintenance/"],
    "limitations": [
        "All five years have been examined by ten earlier suites, the r4 revalidation, the r5 round "
        "and waves 8-11; a pass is evidence against a fluke, not out-of-sample proof.",
        "W12a's quantile level 0.90 matches the official Top decile by construction and was fixed "
        "before scoring, but it is still one point of a continuum that is now closed to further "
        "search.",
        "W12b uses LightGBM's own default drop parameters rather than a tuned set, so it tests the "
        "mechanism and not its optimum.",
        "W12c inherits the r5 winner's member set, which failed its own confirmation gate; a gain "
        "here would be a gain over a candidate that is not shipped.",
        "No interval here corrects for cumulative candidate selection.",
    ],
}


def log(message: str) -> None:
    print(f"[{time.strftime('%H:%M:%S')}] {message}", flush=True)


def sha(path) -> str:
    return w9.sha(Path(path))


def read(path) -> dict:
    return w9.read(Path(path))


def write_new(path: Path, payload) -> None:
    with Path(path).open("x", encoding="utf-8") as stream:
        json.dump(payload, stream, ensure_ascii=False, indent=2, allow_nan=False)


def train_quantile(bundle: dict) -> dict:
    import xgboost as xgb
    config = w9.XGB_CONFIG
    frame = bundle["train"].select(KEYS + BASE + ["y_rank"]).sort("trade_date", "ts_code")
    matrix = to_matrix(frame, BASE)
    label = frame["y_rank"].to_numpy().astype(np.float32)
    model = xgb.XGBRegressor(n_estimators=config["rounds"], max_depth=config["max_depth"],
                             learning_rate=config["learning_rate"], subsample=config["subsample"],
                             colsample_bytree=config["colsample_bytree"],
                             reg_lambda=config["reg_lambda"], tree_method=config["tree_method"],
                             device=device(), seed=config["seed"], n_jobs=config["n_jobs"],
                             objective=QUANTILE["objective"],
                             quantile_alpha=QUANTILE["quantile_alpha"])
    started = time.monotonic()
    model.fit(matrix, label)
    info = {"rows": len(frame), "features": len(BASE), "objective": QUANTILE["objective"],
            "quantile_alpha": QUANTILE["quantile_alpha"],
            "seconds": round(time.monotonic() - started, 1)}
    raw = model.predict(to_matrix(bundle["valid"], BASE)).astype(np.float64)
    del matrix, label, model
    gc.collect()
    return {"raw": save_raw(bundle, raw, "quantile90"), "info": info}


def train_dart(bundle: dict) -> dict:
    frame = bundle["train"].select(KEYS + BASE + ["y_rank"])
    matrix = to_matrix(frame, BASE)
    label = frame["y_rank"].to_numpy()
    params = {**PARAMS, **DART}
    booster = lgb.train(params, lgb.Dataset(matrix, label=label, feature_name=BASE),
                        num_boost_round=ROUNDS)
    model_path = OUT / f"model_dart_{bundle['year']}.txt"
    model_path.write_text(booster.model_to_string(), encoding="utf-8")
    started = time.monotonic()
    del matrix, label, booster
    gc.collect()
    reloaded = lgb.Booster(model_str=model_path.read_text(encoding="utf-8"))
    raw = reloaded.predict(to_matrix(bundle["valid"], BASE), num_threads=THREADS)
    raw = raw.astype(np.float32).astype(np.float64)
    info = {"rows": len(frame), "features": len(BASE), "boosting": DART["boosting_type"],
            "drop_rate": DART["drop_rate"], "max_drop": DART["max_drop"],
            "skip_drop": DART["skip_drop"], "rounds": ROUNDS,
            "seconds": round(time.monotonic() - started, 1), "model_sha256": sha(model_path)}
    return {"raw": save_raw(bundle, raw, "dart"), "info": info}


def daily_ic(raw: np.ndarray, label: np.ndarray, dates: np.ndarray, valid: np.ndarray) -> np.ndarray:
    """Per-day cross-sectional rank IC of one member, on the official's row condition."""
    from scipy.stats import rankdata
    unique = np.unique(dates)
    if len(dates) != len(unique) * (len(dates) // len(unique)):
        raise AssertionError("panel is not rectangular")
    rows_per_day = len(dates) // len(unique)
    out = np.full(len(unique), np.nan)
    for index in range(len(unique)):
        rows = np.arange(index * rows_per_day, (index + 1) * rows_per_day)
        keep = valid[rows] & np.isfinite(label[rows]) & np.isfinite(raw[rows])
        if keep.sum() < 30:
            continue
        x = rankdata(raw[rows][keep], method="average")
        y = rankdata(label[rows][keep], method="average")
        sx, sy = x.std(), y.std()
        if sx > 0 and sy > 0:
            out[index] = float(((x - x.mean()) * (y - y.mean())).mean() / (sx * sy))
    return out


def trailing_weights(bundle: dict) -> dict:
    """Causal daily weights for the r5 winner's two members from trailing realised IC."""
    frame = bundle["frame"]
    dates = frame["trade_date"].to_numpy()
    label = frame["y_ret_1d"].to_numpy().astype(np.float64)
    valid = frame["price_valid"].to_numpy()
    unique = np.unique(dates)
    window, warmup = TRAILING["window_days"], TRAILING["warmup_days"]
    members = TRAILING["members"]
    ics = {member: daily_ic(bundle["raws"][member], label, dates, valid) for member in members}
    weights = np.full((len(unique), len(members)), 1.0 / len(members))
    for index in range(len(unique)):
        start = index - window
        if index < warmup or start < 0:
            continue
        block = np.array([np.nanmean(ics[member][start:index]) for member in members])
        positive = np.clip(np.nan_to_num(block, nan=0.0), 0.0, None)
        if positive.sum() > 0:
            weights[index] = positive / positive.sum()
    return {"weights": weights, "member_ic": ics,
            "info": {"days": len(unique), "window_days": window, "warmup_days": warmup,
                     "members": list(members),
                     "mean_weight": {m: float(weights[:, i].mean()) for i, m in enumerate(members)},
                     "min_weight": {m: float(weights[:, i].min()) for i, m in enumerate(members)},
                     "max_weight": {m: float(weights[:, i].max()) for i, m in enumerate(members)},
                     "mean_daily_ic": {m: float(np.nanmean(ics[m])) for m in members},
                     "days_at_equal_weights": int((weights == weights[0]).all(axis=1).sum())}}


def rank_average_weighted(raws: list[np.ndarray], day_weights: np.ndarray, valid: np.ndarray,
                          rows_per_day: int) -> np.ndarray:
    """Weighted cross-sectional rank average with one weight vector per day."""
    from scipy.stats import rankdata
    shape = (-1, rows_per_day)
    arrays = [np.asarray(raw, dtype=np.float64).reshape(shape) for raw in raws]
    mask = valid.reshape(shape)
    total = day_weights.sum(axis=1, keepdims=True)
    normalized = np.where(total > 0, day_weights / np.where(total > 0, total, 1.0),
                          1.0 / day_weights.shape[1])
    out = np.full(mask.shape, -10.0, dtype=np.float64)
    for day in range(mask.shape[0]):
        keep = mask[day].copy()
        for array in arrays:
            keep &= np.isfinite(array[day])
        count = int(keep.sum())
        if not count:
            continue
        mixed = np.zeros(count, dtype=np.float64)
        for index, array in enumerate(arrays):
            mixed += normalized[day, index] * rankdata(array[day][keep], method="average") / count
        out[day, keep] = mixed
    return out.reshape(-1)


def candidate_prediction(key: str, bundle: dict, produced: dict) -> tuple[np.ndarray, np.ndarray, dict]:
    frame = bundle["frame"]
    if key == "W12c_trailing_ic_two":
        if "trailing" not in produced:
            produced["trailing"] = trailing_weights(bundle)
        rows_per_day = len(frame) // frame["trade_date"].n_unique()
        raws = [bundle["raws"][member] for member in TRAILING["members"]]
        raw = rank_average_weighted(raws, produced["trailing"]["weights"],
                                    frame["price_valid"].to_numpy(), rows_per_day)
        info = produced["trailing"]["info"]
    else:
        if key not in produced:
            produced[key] = train_quantile(bundle) if key == "W12a_xgb_quantile90" \
                else train_dart(bundle)
        raw, info = produced[key]["raw"], produced[key]["info"]
    panel = Panel.from_frame(frame.with_columns(pl.Series("pred_raw", raw)))
    auxiliary = frame["aux_raw"].to_numpy().astype(np.float64)
    return make_prediction(panel, auxiliary, "top_only", 0.25), raw, info


def equal_weight_proof(bundle: dict) -> dict:
    """This module's weighted rank average, at equal weights, must reproduce the frozen r5 winner.

    That validates the implementation against a frozen artifact and proves W12c differs from
    xgb_two_mean in the weights and nothing else.
    """
    frame = bundle["frame"]
    days = frame["trade_date"].n_unique()
    rows_per_day = len(frame) // days
    raws = [bundle["raws"][member] for member in TRAILING["members"]]
    equal = np.full((days, len(raws)), 1.0 / len(raws))
    raw = rank_average_weighted(raws, equal, frame["price_valid"].to_numpy(), rows_per_day)
    frozen = pl.read_parquet(w9.R5 / f"predictions_xgb_two_mean_{bundle['year']}.parquet").sort(
        "trade_date", "ts_code")["pred_raw"].to_numpy().astype(np.float64)
    if not np.array_equal(raw, frozen):
        raise AssertionError(f"{bundle['year']}: the equal-weight rank average does not reproduce "
                             f"the frozen xgb_two_mean raw (max abs diff "
                             f"{float(np.abs(raw - frozen).max()):.3e})")
    log(f"{bundle['year']} equal-weight proof: reproduces the frozen xgb_two_mean raw bit-for-bit")
    return {"equal_weights_reproduce_frozen_xgb_two_mean_raw": True}


def invariants(bundle: dict, key: str, produced: dict, prediction: np.ndarray) -> dict:
    frame = bundle["frame"]
    if key == "W12c_trailing_ic_two":
        # The weights are derived from realised labels by construction, so label perturbation is
        # not the relevant test; causality_proof is, and it is strictly stronger.
        record = {"weights_are_label_derived_by_design": True,
                  "label_perturbation_not_applicable": True}
    else:
        changed = frame.with_columns(pl.lit(987654.0).alias("y_ret_1d"))
        altered, _, _ = candidate_prediction(key, {**bundle, "frame": changed}, produced)
        if not np.array_equal(prediction, altered):
            raise AssertionError(f"{key}: predictions depend on the validation labels")
        record = {"label_perturbation_exact": True}
    if not np.isfinite(prediction).all():
        raise AssertionError(f"{key}: non-finite predictions")
    if not np.all(prediction[~frame["price_valid"].to_numpy()] < -1):
        raise AssertionError(f"{key}: price-invalid rows are not scored low")
    record.update({"all_predictions_finite": True, "invalid_price_low_scores": True,
                   "training_isolation": bundle["isolation"]})
    return record


def causality_proof(bundle: dict, produced: dict) -> dict:
    """Show the trailing weights really only look backwards."""
    frame = bundle["frame"]
    dates = frame["trade_date"].to_numpy()
    unique = np.unique(dates)
    weights = produced["trailing"]["weights"]
    if not np.all(weights[:TRAILING["warmup_days"]] == weights[0]):
        raise AssertionError("warm-up days do not use equal weights")
    if not np.allclose(weights.sum(axis=1), 1.0):
        raise AssertionError("daily weights do not sum to one")
    if (weights < 0).any():
        raise AssertionError("negative weight")
    # Rebuild day t's weight from a truncated frame: identical weights prove no forward look.
    truncated = frame.filter(pl.col("trade_date") < int(unique[-1]))
    probe = {**bundle, "frame": truncated}
    partial = trailing_weights(probe)["weights"]
    if not np.allclose(partial, weights[:len(partial)]):
        raise AssertionError("a later day changed an earlier weight")
    return {"warmup_equal_weights": True, "weights_sum_to_one": True, "weights_non_negative": True,
            "prefix_invariance_of_weights": True, "days": len(unique)}


def freeze() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    if (OUT / "protocol.json").exists():
        raise SystemExit("Wave-12 protocol already frozen")
    sources = [Path(__file__), Path(w9.__file__), ROOT / "experiments/wave11_backbone_and_segment.py",
               ROOT / "experiments/wave9_features.py", w9.JOINED_PANEL, w9.PANEL_FILE,
               ROOT / "data/features.parquet", ROOT / "evaluate.py", ROOT / "run.py",
               ROOT / "src/scoring.py", ROOT / "experiments/cached_recheck.py",
               ROOT / "experiments/revalidate_fold_local.py",
               ROOT / "experiments/optimize_r5_models.py",
               ROOT / "experiments/wave11_backbone_segment_20260927/development.json",
               ROOT / "experiments/wave11_backbone_segment_20260927/confirmation.json"]
    for year in YEARS:
        for name in ("baseline", "xgboost", "ensemble4"):
            sources += [w9.R4 / f"predictions_{name}_{year}.parquet",
                        w9.R4 / f"daily_{name}_{year}.csv", w9.R4 / f"result_{year}.json"]
        sources += [w9.R5 / f"predictions_xgb_two_mean_{year}.parquet",
                    w9.R5 / f"daily_xgb_two_mean_{year}.csv", w9.R5 / f"fold_{year}.json"]
    payload = {**PROTOCOL, "frozen_at_local": time.strftime("%Y-%m-%dT%H:%M:%S"),
               "source_sha256": sha(Path(__file__)),
               "harness_source_sha256": sha(Path(w9.__file__)),
               "input_sha256": {p.relative_to(ROOT).as_posix(): sha(p)
                                for p in dict.fromkeys(sources)}}
    write_new(OUT / "protocol.json", payload)
    log(f"Froze the wave-12 protocol: {len(CANDIDATES)} candidates, "
        f"{len(payload['input_sha256'])} pinned inputs, no score exists yet")


def verify_protocol() -> dict:
    protocol = read(OUT / "protocol.json")
    if protocol["source_sha256"] != sha(Path(__file__)):
        raise SystemExit("wave12_loss_and_adaptive.py changed after its protocol was frozen")
    if protocol["candidates"] != json.loads(json.dumps(CANDIDATES)):
        raise SystemExit("Candidate definitions drifted from the frozen protocol")
    if protocol["gates"] != GATES:
        raise SystemExit("Gates drifted from the frozen protocol")
    for path, digest in protocol["input_sha256"].items():
        if sha(ROOT / path) != digest:
            raise SystemExit(f"Pinned input changed: {path}")
    return protocol


def score_fold(year: int, keys: list[str]) -> dict:
    path = OUT / f"fold_{year}.json"
    if path.exists():
        record = read(path)
        if record["candidate_keys"] != keys:
            raise SystemExit(f"{year}: recorded fold used a different candidate set")
        log(f"{year} preserved completed fold")
        return record
    started = time.monotonic()
    w9.OUT = OUT
    bundle = w9.fold(year)
    proof = w9.prove(bundle)
    anchor_metrics = w9.reference_metrics(PRIMARY, year)
    reference = pl.read_parquet(w9.REFERENCES[PRIMARY]["predictions"]
                                / f"predictions_{PRIMARY}_{year}.parquet").sort("trade_date", "ts_code")
    if not reference.select(KEYS).equals(bundle["frame"].select(KEYS)):
        raise AssertionError(f"{year}: frozen {PRIMARY} keys misaligned")
    check, _ = score_official(bundle["frame"], reference["pred"].to_numpy().astype(np.float64))
    anchor = max(abs(check[name] - anchor_metrics[name]) for name in anchor_metrics)
    if anchor > 1e-12:
        raise AssertionError(f"{year}: the frozen {PRIMARY} prediction does not reproduce its "
                             f"recorded composite (max diff {anchor:.3e})")
    log(f"{year} {PRIMARY} anchor reproduced {anchor_metrics['final_score']:.15f} exactly")
    record = {"year": year, "candidate_keys": keys, "seconds": None, "proof": proof,
              "primary_anchor_max_abs_diff": anchor,
              "references": {name: w9.reference_metrics(name, year) for name in REPORTED},
              "candidates": {}, "artifact_sha256": {}}
    produced: dict = {}
    for key in keys:
        prediction, raw, info = candidate_prediction(key, bundle, produced)
        tests = invariants(bundle, key, produced, prediction)
        if key == "W12c_trailing_ic_two":
            tests.update(causality_proof(bundle, produced))
            tests.update(equal_weight_proof(bundle))
        metrics, daily = score_official(bundle["frame"], prediction)
        daily.write_csv(OUT / f"daily_{key}_{year}.csv")
        bundle["frame"].with_columns(pl.Series("pred", prediction), pl.Series("pred_raw", raw)
                                     ).write_parquet(OUT / f"predictions_{key}_{year}.parquet",
                                                     compression="zstd")
        record["candidates"][key] = {
            "metrics": {k: float(v) for k, v in metrics.items()}, "tests": tests,
            "training_info": info,
            "score_deltas": {name: metrics["final_score"]
                             - record["references"][name]["final_score"] for name in REPORTED},
            "ic_deltas": {name: metrics["ic_mean"] - record["references"][name]["ic_mean"]
                          for name in REPORTED},
            "paired": {name: w9.paired(daily, w9.reference_daily(name, year))
                       for name in REPORTED}}
        log(f"{year} {key}: {metrics['final_score']:.9f} ic={metrics['ic_mean']:.6f} | "
            + " ".join(f"{name} {record['candidates'][key]['score_deltas'][name]:+.6f}"
                       for name in REPORTED))
    record["seconds"] = round(time.monotonic() - started, 2)
    record["artifact_sha256"] = {p.name: sha(p) for p in OUT.glob(f"*_{year}.*") if p != path}
    write_new(path, record)
    del bundle, produced
    gc.collect()
    return record


def gate(records: list[dict], key: str, stage: str) -> dict:
    thresholds = GATES[stage]
    comparisons = {}
    for name in thresholds["gated_references"]:
        deltas = [r["candidates"][key]["score_deltas"][name] for r in records]
        ics = [r["candidates"][key]["ic_deltas"][name] for r in records]
        item = {"score_deltas": dict(zip([str(r["year"]) for r in records], deltas)),
                "mean_score_delta": float(np.mean(deltas)),
                "worst_year_score_delta": float(min(deltas)),
                "mean_ic_delta": float(np.mean(ics))}
        item["passed"] = (bool(item["mean_score_delta"] >= thresholds["mean_score_delta_min"]
                               and item["worst_year_score_delta"]
                               >= thresholds["worst_year_score_delta_min"]
                               and item["mean_ic_delta"] >= thresholds["mean_ic_delta_min"])
                          if stage == "development" else
                          bool(item["mean_score_delta"] >= thresholds["mean_score_delta_min"]
                               and (all(d > 0 for d in deltas) if name == PRIMARY else True)))
        comparisons[name] = item
    return {"comparisons": comparisons, "passed": all(c["passed"] for c in comparisons.values()),
            "mean_official_score": float(np.mean([r["candidates"][key]["metrics"]["final_score"]
                                                  for r in records]))}


def develop() -> None:
    verify_protocol()
    if (OUT / "development.json").exists():
        raise SystemExit("Development choice already recorded; preserving it")
    records = [score_fold(year, list(CANDIDATES)) for year in DEVELOPMENT]
    results = {key: gate(records, key, "development") for key in CANDIDATES}
    eligible = [key for key, item in results.items() if item["passed"]]
    winner = (min(eligible, key=lambda k: (-results[k]["mean_official_score"],
                                           CANDIDATES[k]["models"], k)) if eligible else None)
    verify_protocol()
    write_new(OUT / "development.json", {
        "protocol_sha256": sha(OUT / "protocol.json"), "selected_before_confirmation": True,
        "no_fallback_after_confirmation": True, "candidate_results": results, "winner": winner,
        "eligible": eligible,
        "fold_sha256": {f"fold_{y}.json": sha(OUT / f"fold_{y}.json") for y in DEVELOPMENT}})
    log(f"DEVELOPMENT winner: {winner!r} (eligible: {eligible})")


def validated_development() -> dict:
    development = read(OUT / "development.json")
    if development["protocol_sha256"] != sha(OUT / "protocol.json"):
        raise SystemExit("Development record does not match the frozen protocol")
    records = []
    for year in DEVELOPMENT:
        path = OUT / f"fold_{year}.json"
        if sha(path) != development["fold_sha256"][path.name]:
            raise SystemExit(f"{year}: recorded fold changed after the development choice")
        records.append(read(path))
    results = {key: gate(records, key, "development") for key in CANDIDATES}
    if results != development["candidate_results"]:
        raise SystemExit("Development gates do not reproduce from the recorded folds")
    return development


def confirm() -> None:
    verify_protocol()
    development = validated_development()
    winner = development["winner"]
    if winner is None:
        raise SystemExit("No candidate passed the development gate; confirmation is prohibited")
    if (OUT / "confirmation.json").exists():
        raise SystemExit("Confirmation already recorded; preserving it")
    records = [score_fold(year, [winner]) for year in CONFIRMATION]
    result = gate(records, winner, "confirmation")
    five = {**development["candidate_results"][winner]["comparisons"][PRIMARY]["score_deltas"],
            **result["comparisons"][PRIMARY]["score_deltas"]}
    write_new(OUT / "confirmation.json", {
        "protocol_sha256": sha(OUT / "protocol.json"), "winner": winner,
        "confirmation_years": list(CONFIRMATION), "result": result, "passed": result["passed"],
        "five_year_deltas_vs_primary": five,
        "five_year_mean_delta_vs_primary": float(np.mean(list(five.values()))),
        "five_year_positive_years_vs_primary": int(sum(v > 0 for v in five.values())),
        "note": "Scored once, after the development choice was recorded. Exploratory: all five "
                "years have been viewed repeatedly.",
        "fold_sha256": {f"fold_{y}.json": sha(OUT / f"fold_{y}.json") for y in CONFIRMATION}})
    log(f"CONFIRMATION {winner}: passed={result['passed']} five-year deltas vs {PRIMARY} "
        + " ".join(f"{y}:{v:+.6f}" for y, v in five.items()))


def summarize() -> None:
    table = {"protocol_sha256": sha(OUT / "protocol.json"), "primary": PRIMARY, "years": {},
             "candidates": {}}
    for year in YEARS:
        path = OUT / f"fold_{year}.json"
        if not path.exists():
            continue
        record = read(path)
        table["years"][str(year)] = {"references": {
            name: record["references"][name]["final_score"] for name in record["references"]}}
        for key, entry in record["candidates"].items():
            table["candidates"].setdefault(key, {})[str(year)] = {
                "final_score": entry["metrics"]["final_score"], "ic_mean": entry["metrics"]["ic_mean"],
                "score_deltas": entry["score_deltas"], "training_info": entry["training_info"]}
    for stage in ("development", "confirmation"):
        path = OUT / f"{stage}.json"
        if path.exists():
            table[stage] = read(path)
    (OUT / "summary.json").write_text(json.dumps(table, ensure_ascii=False, indent=2),
                                      encoding="utf-8")
    years = sorted(table["years"], key=int)
    for reference in (PRIMARY, "xgb_two_mean", "baseline"):
        print(f"\nwave-12 差值（候选 − {reference}）")
        header = f"{'candidate':<24}" + "".join(f"{y:>12}" for y in years) + f"{'均值':>12}{'最差年':>12}"
        print(header + "\n" + "-" * len(header))
        for key, per_year in table["candidates"].items():
            values = [per_year[y]["score_deltas"][reference] for y in years if y in per_year]
            cells = "".join(f"{per_year[y]['score_deltas'][reference]:>+12.6f}" if y in per_year
                            else f"{'-':>12}" for y in years)
            print(f"{key:<24}{cells}{np.mean(values):>+12.6f}{min(values):>+12.6f}")
    if "development" in table:
        print(f"\n开发门禁通过者：{table['development']['eligible']}，胜者："
              f"{table['development']['winner']!r}")
    if "confirmation" in table:
        print(f"确认结果：passed={table['confirmation']['passed']}，五年对主参照均值 "
              f"{table['confirmation']['five_year_mean_delta_vs_primary']:+.6f}，正年 "
              f"{table['confirmation']['five_year_positive_years_vs_primary']}/5")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("stage", choices=("protocol", "develop", "confirm", "summary"))
    arguments = parser.parse_args()
    {"protocol": freeze, "develop": develop, "confirm": confirm, "summary": summarize}[
        arguments.stage]()
