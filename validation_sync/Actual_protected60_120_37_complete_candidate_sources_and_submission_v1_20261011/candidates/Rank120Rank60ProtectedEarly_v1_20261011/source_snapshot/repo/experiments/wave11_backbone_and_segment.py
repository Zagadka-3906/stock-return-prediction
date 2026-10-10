"""Wave-11: the four mechanisms that survive the survey of everything already closed.

After wave-8 (combination rules, ensemble post-processing), wave-9 (extended features,
binary auxiliary head) and wave-10 (causal limit-up recalibration) all returned zero passes,
a read-only survey of every training module in this repository left exactly four mechanisms
that have never been scored. All four are tested here on the **delivered** backbone, the
plain 63-feature XGBoost, so the comparison answers the decision that is actually open.

  W11a_tradable_only  Train on rows with flag_limit_up == 0 only. The portfolio terms are
                      built from exactly those rows, so this focuses all capacity where 60%
                      of the composite is decided. `experiments/research_r6_20260926/
                      core_findings.md` considered it and advised against it ("涨停股票仍属于
                      IC 任务") but never ran it; `r6_topk` restricted the pool AND changed the
                      objective, so its failure is confounded.

  W11b_early_stop     Adaptive capacity. Every model in this project uses a fixed 180 rounds
                      with no validation set — `run.fit_model` has no eval set and no early
                      stopping, and wave-4 varied the round count only as a FIXED grid, which
                      is a different mechanism. Here the round count is chosen per fold by
                      early stopping on the last 60 trading days of that fold's own purged
                      training window, with a 600-round ceiling.

  W11c_age_decay      Smooth recency emphasis. `recent2x` (weight 2.0 on the most recent two
                      years) scored +0.000981/+0.001736 on 2022/2023 under the superseded
                      alpha 0.95 stack and −0.002382 on 2024, and `rolling3` (hard truncation
                      to three years) was negative. A continuous exponential half-life of two
                      years has never been tried, and neither has any recency scheme under the
                      current stack.

  W11d_limitup_segment  The only measured headroom left in the project. Limit-up rows reach
                      the 40% IC term and none of the 60% portfolio terms, and
                      `experiments/limit_up_decomposition_eval/decomposition.json` bounds a
                      perfect WITHIN-GROUP reordering of them at +0.004427 composite. Wave-10
                      showed the group's mean placement is already optimal in both directions
                      (lifting gains +0.000197, demoting loses up to −0.002348), so the entire
                      residual is per-row discrimination. A LightGBM fitted only on limit-up
                      rows reorders them inside the slots the delivered model already gave
                      them, which by construction cannot move a portfolio term.

DISCIPLINE. Frozen before scoring; 2020-2022 select one candidate; 2023-2024 confirm it once;
no fallback, no retuning, no threshold changes. Every fold first re-runs the wave-9 harness
proof, which reproduces the frozen released baseline raw bit-for-bit and therefore validates
row alignment, ordering, purging and hyper-parameters together. All five years have been
viewed many times, so this is exploratory and nothing here is out-of-sample evidence.
Writes only inside experiments/wave11_backbone_segment_20260927/.
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

OUT = ROOT / "experiments" / "wave11_backbone_segment_20260927"
KEYS = ["ts_code", "trade_date"]
YEARS = (2020, 2021, 2022, 2023, 2024)
DEVELOPMENT = (2020, 2021, 2022)
CONFIRMATION = (2023, 2024)
PRIMARY = "xgboost"
GATED = ("xgboost", "baseline")
REPORTED = ("xgboost", "baseline", "ensemble4", "xgb_two_mean")
BASE = w9.BASE_FEATURES
EARLY_STOP = {"inner_validation_days": 60, "early_stopping_rounds": 30, "max_rounds": 600}
AGE_DECAY = {"half_life_trading_days": 504}
CANDIDATES = {
    "W11a_tradable_only": {"mechanism": "training universe", "models": 1,
                           "needs_backbone": True,
                           "note": "the frozen T2f XGBoost recipe trained only on rows with "
                                   "flag_limit_up == 0"},
    "W11b_early_stop": {"mechanism": "adaptive capacity", "models": 1, "needs_backbone": True,
                        "note": f"XGBoost with early stopping on the fold's own last "
                                f"{EARLY_STOP['inner_validation_days']} training days, ceiling "
                                f"{EARLY_STOP['max_rounds']} rounds"},
    "W11c_age_decay": {"mechanism": "recency weighting", "models": 1, "needs_backbone": True,
                       "note": f"XGBoost with sample weight 0.5 ** (age / "
                               f"{AGE_DECAY['half_life_trading_days']}), age in trading days"},
    "W11d_limitup_segment": {"mechanism": "within-group limit-up ordering", "models": 1,
                             "needs_backbone": False,
                             "note": "a LightGBM fitted on limit-up rows only, used to permute "
                                     "those rows inside the slots the delivered prediction already "
                                     "gave them; portfolio terms are invariant by construction"},
}
GATES = {
    "development": {"mean_score_delta_min": .0005, "worst_year_score_delta_min": -.002,
                    "mean_ic_delta_min": -.002, "gated_references": list(GATED)},
    "confirmation": {"mean_score_delta_min": .0005, "both_years_positive_vs_primary": True,
                     "gated_references": list(GATED)},
}
PROTOCOL = {
    "experiment": "wave11_training_universe_adaptive_capacity_recency_and_limitup_segment",
    "status": "exploratory_all_years_previously_viewed",
    "candidates": CANDIDATES, "primary_reference": PRIMARY,
    "gated_references": list(GATED), "reported_references": list(REPORTED),
    "gate_rationale": "the delivered model is the plain XGBoost backbone, so the "
                      "decision-relevant bar is to beat it; the pooled baseline is gated too "
                      "because it is the historical anchor. ensemble4 and xgb_two_mean are "
                      "reported for context but not gated, because gating on the best point "
                      "estimate of a round that itself failed confirmation would make the bar "
                      "unreachable and is not the decision being made.",
    "development_years": list(DEVELOPMENT), "confirmation_years": list(CONFIRMATION),
    "gates": GATES,
    "candidate_selection": "among candidates passing every development threshold against every "
                           "gated reference, take the highest equally weighted mean annual official "
                           "score; exact ties prefer fewer models then the lexical key; select one "
                           "or none",
    "confirmation_rule": "score only the frozen development winner on 2023 and 2024 once; it must "
                         "pass every confirmation threshold against both gated references and be "
                         "positive against the primary in both years. No fallback, no second winner.",
    "recipes": {
        "xgboost": w9.XGB_CONFIG,
        "lightgbm_rank": {k: v for k, v in PARAMS.items()}, "rounds": ROUNDS,
        "early_stop": EARLY_STOP, "age_decay": AGE_DECAY,
        "segment_model": "LightGBM with the released rank PARAMS and 180 rounds, fitted only on "
                         "purged training rows with flag_limit_up == 1, price_valid and a non-null "
                         "label; no hyper-parameter is tuned for the small sample, and the "
                         "overfitting risk is recorded rather than mitigated",
    },
    "postprocess": "the released stack exactly, via cached_recheck.make_prediction with the frozen "
                   "pooled auxiliary at top_only 0.25; W11d is applied AFTER that stack to the "
                   "delivered final prediction",
    "segment_splice": "per day, the limit-up rows keep the multiset of scores the delivered "
                      "prediction gave them and are permuted into the segment model's order; every "
                      "other row's score is byte-identical, so the Top-decile excess and turnover "
                      "terms, which the evaluator builds from flag_limit_up == 0 rows only, cannot "
                      "change",
    "portfolio_neutrality": "hard requirement for W11d: annual excess and mean turnover must equal "
                            "the reference's to the last bit, or the run aborts",
    "anchor": "every fold re-runs the wave-9 proof: the released LightGBM rank recipe retrained "
              "through this harness reproduces the frozen r4 baseline raw bit-for-bit where that is "
              "achievable and to the measured float-noise tolerance elsewhere, the released stack "
              "reproduces the frozen baseline prediction exactly, and the primary reference "
              "composite reproduces its recorded value within 1e-12",
    "prohibited": ["Adding a candidate, recipe or year after any score exists",
                   "Tuning the early-stopping patience, the inner window, the half-life or any "
                   "segment-model hyper-parameter after seeing a result",
                   "Relaxing a gate or the portfolio-neutrality requirement",
                   "Writing outside experiments/wave11_backbone_segment_20260927/",
                   "Touching releases/, outputs/, active_release.json or maintenance/"],
    "limitations": [
        "All five years have been examined by nine earlier suites, the r4 revalidation, the r5 round "
        "and waves 8-10; a pass is evidence against a fluke, not out-of-sample proof.",
        "W11a changes the training universe and therefore also the model's behaviour on limit-up "
        "rows, which the IC term does see; a gain there is not portfolio-neutral.",
        "W11b's inner validation window is the most recent 60 training days, which is also the "
        "period most similar to the fold being predicted; that is causal but optimistic about "
        "adaptive capacity.",
        "W11d's ceiling is +0.004427 composite and it is a ceiling for perfect within-group "
        "ordering, not an expected gain; the segment model sees 27k-66k training rows against 63 "
        "features.",
        "No interval here corrects for cumulative candidate selection.",
    ],
}


def log(message: str) -> None:
    print(f"[{time.strftime('%H:%M:%S')}] {message}", flush=True)


def sha(path: Path) -> str:
    return w9.sha(Path(path))


def read(path: Path) -> dict:
    return w9.read(Path(path))


def write_new(path: Path, payload) -> None:
    with Path(path).open("x", encoding="utf-8") as stream:
        json.dump(payload, stream, ensure_ascii=False, indent=2, allow_nan=False)


def xgb_model(device: str, rounds: int | None = None, early_stopping_rounds: int | None = None):
    import xgboost as xgb
    config = w9.XGB_CONFIG
    kwargs = {} if early_stopping_rounds is None else {
        "early_stopping_rounds": early_stopping_rounds}
    return xgb.XGBRegressor(n_estimators=rounds or config["rounds"],
                            max_depth=config["max_depth"],
                            learning_rate=config["learning_rate"], subsample=config["subsample"],
                            colsample_bytree=config["colsample_bytree"],
                            reg_lambda=config["reg_lambda"], tree_method=config["tree_method"],
                            device=device, seed=config["seed"], n_jobs=config["n_jobs"], **kwargs)


def device() -> str:
    import torch
    return "cuda" if torch.cuda.is_available() else "cpu"


def save_raw(bundle: dict, raw: np.ndarray, name: str) -> np.ndarray:
    valid = bundle["valid"]
    out = np.asarray(raw, dtype=np.float64).copy()
    out[~valid["price_valid"].to_numpy()] = -1e6
    valid.select(KEYS).with_columns(pl.Series("pred_raw", out)).write_parquet(
        OUT / f"raw_{name}_{bundle['year']}.parquet", compression="zstd")
    return out


def train_plain(bundle: dict, name: str, keep: str | None = None, decay: bool = False,
                early: bool = False) -> dict:
    """Fit the frozen XGBoost recipe, optionally restricted, weighted or early-stopped.

    The row mask and the sample weights are derived from the same sorted frame that is fed to
    the learner, so they cannot drift out of alignment with it.
    """
    # flag_limit_up is already one of the 63 base features, so it must not be
    # selected twice.
    frame = bundle["train"].select(KEYS + BASE + ["y_rank"]).sort("trade_date", "ts_code")
    if keep == "tradable":
        frame = frame.filter(pl.col("flag_limit_up") == 0)
    matrix = to_matrix(frame, BASE)
    label = frame["y_rank"].to_numpy().astype(np.float32)
    info = {"rows": len(frame), "features": len(BASE)}
    fit_kwargs = {}
    if decay:
        dates = frame["trade_date"].to_numpy()
        unique = np.unique(dates)
        position = {value: index for index, value in enumerate(unique)}
        age = np.array([len(unique) - 1 - position[value] for value in dates], dtype=np.float64)
        weight = (0.5 ** (age / AGE_DECAY["half_life_trading_days"])).astype(np.float32)
        fit_kwargs["sample_weight"] = weight
        info.update({"weight_min": float(weight.min()), "weight_max": float(weight.max()),
                     "effective_rows": float(weight.sum()),
                     "half_life_trading_days": AGE_DECAY["half_life_trading_days"]})
    model = (xgb_model(device(), rounds=EARLY_STOP["max_rounds"],
                       early_stopping_rounds=EARLY_STOP["early_stopping_rounds"]) if early
             else xgb_model(device()))
    started = time.monotonic()
    if early:
        dates = np.unique(frame["trade_date"].to_numpy())
        if len(dates) <= EARLY_STOP["inner_validation_days"] + 20:
            raise AssertionError("training window too short for an inner validation split")
        split = int(dates[-EARLY_STOP["inner_validation_days"]])
        inner = frame["trade_date"].to_numpy() >= split
        model.fit(matrix[~inner], label[~inner], eval_set=[(matrix[inner], label[inner])],
                  verbose=False, **fit_kwargs)
        info.update({"inner_validation_rows": int(inner.sum()),
                     "best_iteration": int(model.best_iteration), "inner_split_date": split,
                     "max_rounds": EARLY_STOP["max_rounds"],
                     "early_stopping_rounds": EARLY_STOP["early_stopping_rounds"]})
    else:
        model.fit(matrix, label, **fit_kwargs)
    info["seconds"] = round(time.monotonic() - started, 1)
    raw = model.predict(to_matrix(bundle["valid"], BASE)).astype(np.float64)
    del matrix, label, model
    gc.collect()
    return {"raw": save_raw(bundle, raw, name), "info": info}


def train_segment(bundle: dict) -> dict:
    # flag_limit_up is already one of the 63 base features, so it must not be
    # selected twice.
    frame = bundle["train"].select(KEYS + BASE + ["y_rank"]).sort("trade_date", "ts_code").filter(pl.col("flag_limit_up") == 1)
    if frame.height < 5000:
        raise AssertionError(f"{bundle['year']}: only {frame.height} limit-up training rows")
    matrix = to_matrix(frame, BASE)
    label = frame["y_rank"].to_numpy()
    booster = lgb.train(PARAMS, lgb.Dataset(matrix, label=label, feature_name=BASE),
                        num_boost_round=ROUNDS)
    model_path = OUT / f"model_segment_{bundle['year']}.txt"
    model_path.write_text(booster.model_to_string(), encoding="utf-8")
    del matrix, label, booster
    gc.collect()
    reloaded = lgb.Booster(model_str=model_path.read_text(encoding="utf-8"))
    valid = bundle["valid"]
    scored = reloaded.predict(to_matrix(valid, BASE), num_threads=THREADS).astype(np.float64)
    return {"score": scored, "info": {"training_rows": frame.height, "features": len(BASE),
                                      "model_sha256": sha(model_path)}}


def splice_within_group(prediction: np.ndarray, dates: np.ndarray, treated: np.ndarray,
                        score: np.ndarray) -> np.ndarray:
    """Permute treated rows inside the slots they already occupy; every other row is untouched."""
    out = prediction.copy()
    for day in np.unique(dates):
        rows = np.flatnonzero(dates == day)
        group = rows[treated[rows]]
        if group.size < 2:
            continue
        slots = np.sort(out[group])
        order = group[np.argsort(score[group], kind="stable")]
        out[order] = slots
    return out


def candidate_prediction(key: str, bundle: dict, produced: dict) -> tuple[np.ndarray, np.ndarray, dict]:
    frame = bundle["frame"]
    if key == "W11d_limitup_segment":
        if "segment" not in produced:
            produced["segment"] = train_segment(bundle)
        reference = pl.read_parquet(w9.REFERENCES[PRIMARY]["predictions"]
                                    / f"predictions_{PRIMARY}_{bundle['year']}.parquet"
                                    ).sort("trade_date", "ts_code")
        if not reference.select(KEYS).equals(frame.select(KEYS)):
            raise AssertionError(f"{bundle['year']}: frozen {PRIMARY} keys misaligned")
        base_prediction = reference["pred"].to_numpy().astype(np.float64)
        spliced = splice_within_group(base_prediction, frame["trade_date"].to_numpy(),
                                      frame["flag_limit_up"].to_numpy().astype(bool),
                                      produced["segment"]["score"])
        return spliced, base_prediction, produced["segment"]["info"]
    if key not in produced:
        produced[key] = build_backbone(key, bundle)
    raw = produced[key]["raw"]
    panel = Panel.from_frame(frame.with_columns(pl.Series("pred_raw", raw)))
    auxiliary = frame["aux_raw"].to_numpy().astype(np.float64)
    return make_prediction(panel, auxiliary, "top_only", 0.25), raw, produced[key]["info"]


def build_backbone(key: str, bundle: dict) -> dict:
    if key == "W11a_tradable_only":
        return train_plain(bundle, "tradable_only", keep="tradable")
    if key == "W11b_early_stop":
        return train_plain(bundle, "early_stop", early=True)
    if key == "W11c_age_decay":
        return train_plain(bundle, "age_decay", decay=True)
    raise KeyError(key)


def invariants(bundle: dict, key: str, produced: dict, prediction: np.ndarray) -> dict:
    frame = bundle["frame"]
    changed = frame.with_columns(pl.lit(987654.0).alias("y_ret_1d"))
    altered, _, _ = candidate_prediction(key, {**bundle, "frame": changed}, produced)
    if not np.array_equal(prediction, altered):
        raise AssertionError(f"{key}: predictions depend on the validation labels")
    if not np.isfinite(prediction).all():
        raise AssertionError(f"{key}: non-finite predictions")
    treated = frame["flag_limit_up"].to_numpy().astype(bool)
    record = {"label_perturbation_exact": True, "all_predictions_finite": True,
              "training_isolation": bundle["isolation"]}
    if key == "W11d_limitup_segment":
        reference = pl.read_parquet(w9.REFERENCES[PRIMARY]["predictions"]
                                    / f"predictions_{PRIMARY}_{bundle['year']}.parquet"
                                    ).sort("trade_date", "ts_code")["pred"].to_numpy().astype(np.float64)
        if not np.array_equal(prediction[~treated], reference[~treated]):
            raise AssertionError(f"{key}: non-limit-up scores were modified")
        moved = np.sort(prediction[treated])
        if not np.allclose(moved, np.sort(reference[treated]), rtol=0, atol=0):
            raise AssertionError(f"{key}: the limit-up slot multiset changed")
        record["untreated_scores_byte_identical"] = True
        record["treated_slot_multiset_preserved"] = True
    return record


def freeze() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    if (OUT / "protocol.json").exists():
        raise SystemExit("Wave-11 protocol already frozen")
    sources = [Path(__file__), Path(w9.__file__), ROOT / "experiments/wave9_features.py",
               w9.JOINED_PANEL, w9.PANEL_FILE, ROOT / "data/features.parquet", ROOT / "evaluate.py",
               ROOT / "run.py", ROOT / "src/scoring.py", ROOT / "experiments/cached_recheck.py",
               ROOT / "experiments/revalidate_fold_local.py",
               ROOT / "experiments/optimize_r5_models.py",
               ROOT / "experiments/limit_up_decomposition_eval/decomposition.json",
               ROOT / "experiments/wave10_limitup_calibration_20260927/protocol.json"]
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
    log(f"Froze the wave-11 protocol: {len(CANDIDATES)} candidates, "
        f"{len(payload['input_sha256'])} pinned inputs, no score exists yet")


def verify_protocol() -> dict:
    protocol = read(OUT / "protocol.json")
    if protocol["source_sha256"] != sha(Path(__file__)):
        raise SystemExit("wave11_backbone_and_segment.py changed after its protocol was frozen")
    if protocol["harness_source_sha256"] != sha(Path(w9.__file__)):
        raise SystemExit("wave9_exploratory.py changed after the wave-11 protocol was frozen")
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
    reference_frame = pl.read_parquet(w9.REFERENCES[PRIMARY]["predictions"]
                                      / f"predictions_{PRIMARY}_{year}.parquet"
                                      ).sort("trade_date", "ts_code")
    check, _ = score_official(bundle["frame"], reference_frame["pred"].to_numpy().astype(np.float64))
    anchor = max(abs(check[name] - anchor_metrics[name]) for name in anchor_metrics)
    if anchor > 1e-12:
        raise AssertionError(f"{year}: the frozen {PRIMARY} prediction does not reproduce its "
                             f"recorded composite (max diff {anchor:.3e})")
    log(f"{year} {PRIMARY} anchor reproduced {anchor_metrics['final_score']:.15f} exactly")
    record = {"year": year, "candidate_keys": keys, "seconds": None, "proof": proof,
              "primary_anchor_max_abs_diff": anchor,
              "references": {name: w9.reference_metrics(name, year) for name in REPORTED},
              "reference_daily": {}, "candidates": {}, "artifact_sha256": {}}
    produced: dict = {}
    for key in keys:
        prediction, raw, info = candidate_prediction(key, bundle, produced)
        tests = invariants(bundle, key, produced, prediction)
        metrics, daily = score_official(bundle["frame"], prediction)
        daily.write_csv(OUT / f"daily_{key}_{year}.csv")
        bundle["frame"].with_columns(pl.Series("pred", prediction)).write_parquet(
            OUT / f"predictions_{key}_{year}.parquet", compression="zstd")
        deltas = {name: metrics["final_score"] - record["references"][name]["final_score"]
                  for name in REPORTED}
        if key == "W11d_limitup_segment":
            for term in ("annual_excess", "mean_turnover"):
                drift = abs(metrics[term] - record["references"][PRIMARY][term])
                if drift > 0.0:
                    raise AssertionError(f"{year} {key}: portfolio term {term} moved by {drift:.3e}")
        record["candidates"][key] = {
            "metrics": {k: float(v) for k, v in metrics.items()}, "tests": tests,
            "training_info": info, "score_deltas": deltas,
            "ic_deltas": {name: metrics["ic_mean"] - record["references"][name]["ic_mean"]
                          for name in REPORTED},
            "paired": {name: w9.paired(daily, w9.reference_daily(name, year))
                       for name in REPORTED}}
        log(f"{year} {key}: {metrics['final_score']:.9f} ic={metrics['ic_mean']:.6f} | "
            + " ".join(f"{name} {deltas[name]:+.6f}" for name in REPORTED)
            + (f" | best_iteration={info['best_iteration']}" if "best_iteration" in info else "")
            + (f" | rows={info['rows']:,}" if "rows" in info else "")
            + (f" | segment_rows={info['training_rows']:,}" if "training_rows" in info else ""))
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
        if stage == "development":
            item["passed"] = bool(
                item["mean_score_delta"] >= thresholds["mean_score_delta_min"]
                and item["worst_year_score_delta"] >= thresholds["worst_year_score_delta_min"]
                and item["mean_ic_delta"] >= thresholds["mean_ic_delta_min"])
        else:
            item["passed"] = bool(
                item["mean_score_delta"] >= thresholds["mean_score_delta_min"]
                and (all(d > 0 for d in deltas) if name == PRIMARY else True))
        comparisons[name] = item
    return {"comparisons": comparisons, "passed": all(c["passed"] for c in comparisons.values()),
            "mean_official_score": float(np.mean([r["candidates"][key]["metrics"]["final_score"]
                                                  for r in records]))}


def develop() -> None:
    verify_protocol()
    if (OUT / "development.json").exists():
        raise SystemExit("Development choice already recorded; preserving it")
    results = {}
    records = [score_fold(year, list(CANDIDATES)) for year in DEVELOPMENT]
    for key in CANDIDATES:
        results[key] = gate(records, key, "development")
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
                "final_score": entry["metrics"]["final_score"],
                "ic_mean": entry["metrics"]["ic_mean"],
                "score_deltas": entry["score_deltas"], "training_info": entry["training_info"]}
    for stage in ("development", "confirmation"):
        path = OUT / f"{stage}.json"
        if path.exists():
            table[stage] = read(path)
    (OUT / "summary.json").write_text(json.dumps(table, ensure_ascii=False, indent=2),
                                      encoding="utf-8")
    years = sorted(table["years"], key=int)
    print(f"\nwave-11，主参照 = {PRIMARY}（当前交付主干）；差值为候选减参照")
    header = f"{'candidate':<24}" + "".join(f"{y:>12}" for y in years) + f"{'均值':>12}{'最差年':>12}"
    print(header + "\n" + "-" * len(header))
    for key, per_year in table["candidates"].items():
        deltas = [per_year[y]["score_deltas"][PRIMARY] for y in years if y in per_year]
        cells = "".join(f"{per_year[y]['score_deltas'][PRIMARY]:>+12.6f}" if y in per_year
                        else f"{'-':>12}" for y in years)
        print(f"{key:<24}{cells}{np.mean(deltas):>+12.6f}{min(deltas):>+12.6f}")
    print(f"\n对 pooled 基线的差值：")
    for key, per_year in table["candidates"].items():
        cells = "".join(f"{per_year[y]['score_deltas']['baseline']:>+12.6f}" if y in per_year
                        else f"{'-':>12}" for y in years)
        print(f"{key:<24}{cells}")
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
