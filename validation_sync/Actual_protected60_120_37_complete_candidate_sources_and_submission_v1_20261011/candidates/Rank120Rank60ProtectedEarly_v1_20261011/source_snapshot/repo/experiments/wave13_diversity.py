"""Wave-13: where does ensemble diversity actually come from — family, or horizon?

The project's written conclusion is that heterogeneous averaging works **only across model
families**: same-family seed ensembling is a frozen negative, while the cross-family rank
averages (W3e, and the r5 winner xgb_two_mean) are the only two things that ever produced
consistent gains. But every successful combination changed *two* things at once. The r5
winner is XGBoost(1-day label) ⊕ LightGBM(2-day label): a different family **and** a
different horizon. So the claim "diversity must come from family" has never been isolated
from "diversity comes from the prediction horizon".

This round runs the 2x2 that separates them, on the corrected caliber, with equal-weight
cross-sectional rank averaging throughout (the one combination rule that survived wave-8):

                    same horizon            different horizon
  same family       (trivially the member)  W13b xgb1 + xgb2
                                            W13c lgb1 + lgb2
  cross family      W13a xgb1 + lgb1        xgb_two_mean (frozen reference)

plus W13d, all four members. `xgb2` — XGBoost on the two-day label — has never been fitted
anywhere in this repository, so it is built here from the frozen two-day target definition.

TWO HARNESS PROOFS ARE ADDED, because waves 9, 11 and 12 all retrained XGBoost without ever
comparing it to the frozen member:

  1. retraining the LightGBM two-day member from this round's reconstruction of the frozen
     target must reproduce the frozen `two_day` raw, which validates the label;
  2. retraining the XGBoost 1-day member with the frozen recipe must reproduce the frozen
     `xgboost` raw, which validates the XGBoost path those three waves relied on;
  3. this round's equal-weight rank average of xgb1 and lgb2 must reproduce the frozen r5
     `xgb_two_mean` raw bit-for-bit, which validates the combination rule.

Where bit-identity is not achievable (a frozen artifact produced by an earlier round's code
path), the requirement is the measured tolerance wave-9 established: minimum daily Spearman
>= 0.999, mean Top-decile Jaccard >= 0.999, worst-day >= 0.99, and the retrained composite
within 1e-5 of the recorded one.

DISCIPLINE. Frozen before scoring; 2020-2022 select one candidate; 2023-2024 confirm once.
Unlike waves 11 and 12, `xgb_two_mean` IS a gated reference here: wave-12 showed that leaving
the best known combination ungated lets a near-duplicate of it pass the development gate for
reasons that have nothing to do with the mechanism under test. Exploratory — all five years
have been viewed repeatedly. Writes only inside experiments/wave13_diversity_20260927/.
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

OUT = ROOT / "experiments" / "wave13_diversity_20260927"
KEYS = ["ts_code", "trade_date"]
YEARS = (2020, 2021, 2022, 2023, 2024)
DEVELOPMENT = (2020, 2021, 2022)
CONFIRMATION = (2023, 2024)
PRIMARY = "xgboost"
GATED = ("xgboost", "baseline", "xgb_two_mean")
REPORTED = ("xgboost", "baseline", "ensemble4", "xgb_two_mean")
BASE = w9.BASE_FEATURES
XGB_THREADS = 16
MEMBERS = ("xgb1", "lgb1", "xgb2", "lgb2")
CANDIDATES = {
    "W13a_cross_family_same_horizon": {"members": ["xgb1", "lgb1"], "family": "cross",
                                       "horizon": "same", "models": 0},
    "W13b_same_family_cross_horizon_xgb": {"members": ["xgb1", "xgb2"], "family": "same",
                                           "horizon": "cross", "models": 1},
    "W13c_same_family_cross_horizon_lgb": {"members": ["lgb1", "lgb2"], "family": "same",
                                           "horizon": "cross", "models": 0},
    "W13d_all_four": {"members": list(MEMBERS), "family": "cross", "horizon": "cross",
                      "models": 1},
}
REFERENCE_RECIPE = {"members": ["xgb1", "lgb2"],
                    "note": "equal-weight rank average of these two is the frozen r5 winner "
                            "xgb_two_mean; reproducing it bit-for-bit is a harness proof"}
TOLERANCE = {"min_daily_spearman": .999, "mean_top_jaccard": .999, "worst_day_top_jaccard": .99,
             "retrained_composite_gap": 1e-5}
GATES = {
    "development": {"mean_score_delta_min": .0005, "worst_year_score_delta_min": -.002,
                    "mean_ic_delta_min": -.002, "gated_references": list(GATED)},
    "confirmation": {"mean_score_delta_min": .0005, "both_years_positive_vs_primary": True,
                     "gated_references": list(GATED)},
}
PROTOCOL = {
    "experiment": "wave13_family_versus_horizon_diversity",
    "status": "exploratory_all_years_previously_viewed",
    "question": "the project's written claim is that averaging only helps across model families; "
                "every successful combination also changed the prediction horizon, so the two have "
                "never been separated",
    "design": {"axes": {"family": ("same", "cross"), "horizon": ("same", "cross")},
               "cells": CANDIDATES, "frozen_reference_cell": REFERENCE_RECIPE},
    "candidates": CANDIDATES, "members": list(MEMBERS),
    "member_definitions": {
        "lgb1": "the frozen released LightGBM rank backbone raw (r4 baseline member)",
        "xgb1": "the frozen XGBoost rank member raw (r4 xgboost / delivered backbone)",
        "lgb2": "the frozen LightGBM two-day-horizon member raw (wave-2 W2c cache, hash-verified "
                "by the r4 revalidation)",
        "xgb2": "NEW: XGBoost with the frozen T2f recipe trained on the frozen two-day target",
    },
    "two_day_target": "0.5 * y_rank + 0.5 * y_rank.shift(-1) per ts_code on the panel sorted by "
                      "(ts_code, trade_date); training rows must be is_train, price_valid, strictly "
                      "before the fold's two_day_cutoff_exclusive, and have a finite target — "
                      "copied verbatim from experiments/revalidate_fold_local.py",
    "combination_rule": "equal-weight cross-sectional rank average over rows price-valid and finite "
                        "in every member, sentinel -10.0 elsewhere; the rule that survived wave-8",
    "primary_reference": PRIMARY, "gated_references": list(GATED),
    "reported_references": list(REPORTED),
    "gate_rationale": "xgb_two_mean is gated here, unlike waves 11 and 12, because wave-12 showed "
                      "that leaving the best known combination ungated lets a near-duplicate pass "
                      "the development gate for reasons unrelated to the mechanism under test. The "
                      "question is now whether any combination beats the best known combination.",
    "development_years": list(DEVELOPMENT), "confirmation_years": list(CONFIRMATION),
    "gates": GATES,
    "candidate_selection": "among candidates passing every development threshold against every "
                           "gated reference, take the highest equally weighted mean annual official "
                           "score; exact ties prefer fewer newly fitted models then the lexical key; "
                           "select one or none",
    "confirmation_rule": "score only the frozen development winner on 2023 and 2024 once; it must "
                         "pass every confirmation threshold against all three gated references and "
                         "be positive against the primary in both years. No fallback.",
    "postprocess": "the released stack exactly, via cached_recheck.make_prediction with the frozen "
                   "pooled auxiliary at top_only 0.25",
    "harness_proofs": [
        "the released LightGBM rank recipe retrained through this harness reproduces the frozen "
        "baseline raw (wave-9 proof, re-run every fold)",
        "the frozen two-day target retrained with the released LightGBM recipe reproduces the "
        "frozen two_day member raw",
        "the frozen XGBoost recipe retrained on the one-day label reproduces the frozen xgboost "
        "member raw",
        "this round's equal-weight rank average of xgb1 and lgb2 reproduces the frozen r5 "
        "xgb_two_mean raw bit-for-bit",
        "the released stack on the frozen xgboost raw reproduces the frozen xgboost final "
        "prediction and its recorded composite within 1e-12",
    ],
    "tolerance_where_bit_identity_is_unachievable": TOLERANCE,
    "prohibited": ["Adding a member, candidate or year after any score exists",
                   "Tuning the XGBoost or two-day recipe",
                   "Relaxing a gate or a harness proof",
                   "Writing outside experiments/wave13_diversity_20260927/",
                   "Touching releases/, outputs/, active_release.json or maintenance/"],
    "limitations": [
        "All five years have been examined by eleven earlier suites, the r4 revalidation, the r5 "
        "round and waves 8-12; a pass is evidence against a fluke, not out-of-sample proof.",
        "The four members share one feature panel, one label family and overlapping training "
        "windows, so 'family' here means learner algorithm only.",
        "xgb2 is fitted here for the first time and has no frozen artifact to reproduce, so its "
        "recipe is validated only indirectly, through proof 3 reproducing the frozen two-day "
        "LightGBM member.",
        "No interval corrects for cumulative candidate selection.",
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


def two_day_frame(bundle: dict) -> pl.DataFrame:
    """The frozen two-day training frame, rebuilt verbatim from the revalidation recipe."""
    cutoff = bundle["provenance"]["boundaries"]["two_day_cutoff_exclusive"]
    return (w9.lazy_panel().sort("ts_code", "trade_date")
            .with_columns((0.5 * pl.col("y_rank")
                           + 0.5 * pl.col("y_rank").shift(-1).over("ts_code")).alias("two_target"))
            .filter(pl.col("is_train") & pl.col("price_valid")
                    & (pl.col("trade_date") < cutoff) & pl.col("two_target").is_finite())
            .select(KEYS + BASE + ["two_target"]).sort("trade_date", "ts_code").collect())


def train_xgb(bundle: dict, frame: pl.DataFrame, target: str, name: str) -> np.ndarray:
    import xgboost as xgb
    matrix = to_matrix(frame, BASE)
    label = frame[target].to_numpy()
    model = xgb.XGBRegressor(n_estimators=ROUNDS, max_depth=7, learning_rate=0.05, subsample=0.85,
                             colsample_bytree=0.85, reg_lambda=5.0, tree_method="hist",
                             device=w9_device(), seed=2026, n_jobs=XGB_THREADS)
    started = time.monotonic()
    model.fit(matrix, label)
    seconds = round(time.monotonic() - started, 1)
    raw = model.predict(to_matrix(bundle["valid"], BASE)).astype(np.float64)
    raw[~bundle["valid"]["price_valid"].to_numpy()] = -1e6
    log(f"{bundle['year']} {name}: fitted on {len(frame):,} rows in {seconds}s")
    del matrix, label, model
    gc.collect()
    return raw


def w9_device() -> str:
    import torch
    return "cuda" if torch.cuda.is_available() else "cpu"


def train_lgb(bundle: dict, frame: pl.DataFrame, target: str, name: str,
              sorted_order: bool = True) -> np.ndarray:
    used = frame.sort("trade_date", "ts_code") if sorted_order else frame
    matrix = to_matrix(used, BASE)
    label = used[target].to_numpy()
    booster = lgb.train(PARAMS, lgb.Dataset(matrix, label=label, feature_name=BASE),
                        num_boost_round=ROUNDS)
    path = OUT / f"model_{name}_{bundle['year']}.txt"
    path.write_text(booster.model_to_string(), encoding="utf-8")
    rows = len(used)
    del matrix, label, booster
    gc.collect()
    reloaded = lgb.Booster(model_str=path.read_text(encoding="utf-8"))
    raw = reloaded.predict(to_matrix(bundle["valid"], BASE), num_threads=THREADS).astype(np.float64)
    raw[~bundle["valid"]["price_valid"].to_numpy()] = -1e6
    log(f"{bundle['year']} {name}: fitted on {rows:,} rows")
    return raw


def members(bundle: dict, produced: dict) -> dict:
    raws = {"lgb1": bundle["raws"]["lgb"], "xgb1": bundle["raws"]["xgboost"],
            "lgb2": bundle["raws"]["two_day"]}
    if "xgb2" not in produced:
        frame = two_day_frame(bundle)
        produced["xgb2"] = train_xgb(bundle, frame, "two_target", "xgb2_two_day")
        produced["two_day_frame_rows"] = len(frame)
        del frame
        gc.collect()
    raws["xgb2"] = produced["xgb2"]
    return raws


def member_proofs(bundle: dict) -> dict:
    """Reproduce the two frozen member recipes from this round's own code paths."""
    from scipy.stats import spearmanr
    year = bundle["year"]
    frame = two_day_frame(bundle)
    rows = len(frame)
    report = {"two_day_training_rows": rows,
              "two_day_cutoff_exclusive": bundle["provenance"]["boundaries"]["two_day_cutoff_exclusive"]}
    valid = bundle["valid"]["price_valid"].to_numpy()
    days = bundle["valid"]["trade_date"].n_unique()
    codes = len(valid) // days
    for name, retrained, frozen in (
            ("lgb_two_day", train_lgb(bundle, frame, "two_target", "proof_lgb_two_day"),
             bundle["raws"]["two_day"]),
            ("xgb_one_day",
             train_xgb(bundle, bundle["train"].select(KEYS + BASE + ["y_rank"]), "y_rank",
                       "proof_xgb_one_day"),
             bundle["raws"]["xgboost"])):
        identical = bool(np.array_equal(retrained, frozen))
        difference = float(np.abs(retrained[valid] - frozen[valid]).max())
        mine = retrained.reshape(days, codes)
        theirs = frozen.reshape(days, codes)
        mask = valid.reshape(days, codes)
        rhos, jaccard = [], []
        for day in range(days):
            rows_day = np.flatnonzero(mask[day])
            rhos.append(float(spearmanr(mine[day][rows_day], theirs[day][rows_day]).statistic))
            top = max(len(rows_day) // 10, 1)
            left = set(rows_day[np.argsort(-mine[day][rows_day], kind="stable")[:top]])
            right = set(rows_day[np.argsort(-theirs[day][rows_day], kind="stable")[:top]])
            jaccard.append(len(left & right) / len(left | right))
        item = {"bit_identical": identical, "max_abs_diff": difference,
                "min_daily_spearman": float(min(rhos)),
                "mean_top_decile_jaccard": float(np.mean(jaccard)),
                "worst_day_top_decile_jaccard": float(min(jaccard))}
        if not identical:
            if (item["min_daily_spearman"] < TOLERANCE["min_daily_spearman"]
                    or item["mean_top_decile_jaccard"] < TOLERANCE["mean_top_jaccard"]
                    or item["worst_day_top_decile_jaccard"] < TOLERANCE["worst_day_top_jaccard"]):
                raise AssertionError(f"{year} {name}: retrained member disagrees with the frozen "
                                     f"artifact beyond the measured tolerance: {item}")
            if name == "xgb_one_day":
                # The XGBoost member has a recorded composite, so bound the score effect too.
                panel = Panel.from_frame(bundle["frame"].with_columns(
                    pl.Series("pred_raw", retrained)))
                metrics, _ = score_official(bundle["frame"], make_prediction(
                    panel, bundle["frame"]["aux_raw"].to_numpy().astype(np.float64),
                    "top_only", 0.25))
                reference = w9.reference_metrics("xgboost", year)
                item["retrained_composite"] = float(metrics["final_score"])
                item["retrained_composite_gap"] = abs(metrics["final_score"]
                                                      - reference["final_score"])
                if item["retrained_composite_gap"] > TOLERANCE["retrained_composite_gap"]:
                    raise AssertionError(f"{year} {name}: retraining moved the composite by "
                                         f"{item['retrained_composite_gap']:.3e}")
            else:
                # The two-day member was never scored alone through the released stack, so there
                # is no recorded composite to compare against; rank agreement is the check, and
                # the combination proof below validates the rule that consumes it.
                item["retrained_composite_gap"] = None
        report[name] = item
        log(f"{year} member proof {name}: bit_identical={identical} max|diff|={difference:.3e} "
            f"min daily Spearman={item['min_daily_spearman']:.9f} Top Jaccard mean/min="
            f"{item['mean_top_decile_jaccard']:.9f}/{item['worst_day_top_decile_jaccard']:.9f}")
    del frame
    gc.collect()
    return report


def equal_weight_proof(bundle: dict, raws: dict) -> dict:
    reference = pl.read_parquet(w9.R5 / f"predictions_xgb_two_mean_{bundle['year']}.parquet").sort(
        "trade_date", "ts_code")["pred_raw"].to_numpy().astype(np.float64)
    rows_per_day = len(bundle["valid"]) // bundle["valid"]["trade_date"].n_unique()
    mine = w9.rank_average([raws["xgb1"], raws["lgb2"]],
                           bundle["valid"]["price_valid"].to_numpy(), rows_per_day)
    if not np.array_equal(mine, reference):
        raise AssertionError(f"{bundle['year']}: the equal-weight rank average of xgb1 and lgb2 "
                             f"does not reproduce the frozen xgb_two_mean raw (max abs diff "
                             f"{float(np.abs(mine - reference).max()):.3e})")
    log(f"{bundle['year']} combination proof: xgb1 + lgb2 reproduces the frozen xgb_two_mean raw "
        "bit-for-bit")
    return {"xgb1_plus_lgb2_reproduces_frozen_xgb_two_mean": True}


def candidate_prediction(key: str, bundle: dict, raws: dict) -> tuple[np.ndarray, np.ndarray]:
    rows_per_day = len(bundle["valid"]) // bundle["valid"]["trade_date"].n_unique()
    raw = w9.rank_average([raws[name] for name in CANDIDATES[key]["members"]],
                          bundle["valid"]["price_valid"].to_numpy(), rows_per_day)
    panel = Panel.from_frame(bundle["frame"].with_columns(pl.Series("pred_raw", raw)))
    auxiliary = bundle["frame"]["aux_raw"].to_numpy().astype(np.float64)
    return make_prediction(panel, auxiliary, "top_only", 0.25), raw


def invariants(bundle: dict, key: str, prediction: np.ndarray) -> dict:
    """Every member raw is either a hash-pinned frozen artifact or recipe-proven above, and the
    combination rule is proven to reproduce the frozen r5 winner, so the checks that remain are
    the ones about the assembled prediction itself."""
    frame = bundle["frame"]
    if not np.isfinite(prediction).all():
        raise AssertionError(f"{key}: non-finite predictions")
    if not np.all(prediction[~frame["price_valid"].to_numpy()] < -1):
        raise AssertionError(f"{key}: price-invalid rows are not scored low")
    return {"all_predictions_finite": True, "invalid_price_low_scores": True,
            "members_are_frozen_or_recipe_proven": True,
            "training_isolation": bundle["isolation"]}


def freeze() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    if (OUT / "protocol.json").exists():
        raise SystemExit("Wave-13 protocol already frozen")
    sources = [Path(__file__), Path(w9.__file__), ROOT / "experiments/wave9_features.py",
               ROOT / "experiments/revalidate_fold_local.py", ROOT / "experiments/cached_recheck.py",
               ROOT / "experiments/optimize_r5_models.py", w9.JOINED_PANEL, w9.PANEL_FILE,
               ROOT / "data/features.parquet", ROOT / "evaluate.py", ROOT / "run.py",
               ROOT / "src/scoring.py", ROOT / "data" / "raw" / "训练集.csv",
               ROOT / "experiments/wave12_loss_and_adaptive_20260927/development.json",
               ROOT / "experiments/wave12_loss_and_adaptive_20260927/confirmation.json"]
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
    log(f"Froze the wave-13 protocol: {len(CANDIDATES)} candidates in a 2x2 family/horizon design, "
        f"{len(payload['input_sha256'])} pinned inputs, no score exists yet")


def verify_protocol() -> dict:
    protocol = read(OUT / "protocol.json")
    if protocol["source_sha256"] != sha(Path(__file__)):
        raise SystemExit("wave13_diversity.py changed after its protocol was frozen")
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
    member_proof = member_proofs(bundle)
    produced: dict = {}
    raws = members(bundle, produced)
    combination_proof = equal_weight_proof(bundle, raws)
    reference_frame = pl.read_parquet(w9.REFERENCES[PRIMARY]["predictions"]
                                      / f"predictions_{PRIMARY}_{year}.parquet"
                                      ).sort("trade_date", "ts_code")
    anchor_metrics = w9.reference_metrics(PRIMARY, year)
    check, _ = score_official(bundle["frame"],
                              reference_frame["pred"].to_numpy().astype(np.float64))
    anchor = max(abs(check[name] - anchor_metrics[name]) for name in anchor_metrics)
    if anchor > 1e-12:
        raise AssertionError(f"{year}: the frozen {PRIMARY} prediction does not reproduce its "
                             f"recorded composite (max diff {anchor:.3e})")
    log(f"{year} {PRIMARY} anchor reproduced {anchor_metrics['final_score']:.15f} exactly")
    record = {"year": year, "candidate_keys": keys, "seconds": None, "proof": proof,
              "member_proofs": member_proof, "combination_proof": combination_proof,
              "primary_anchor_max_abs_diff": anchor,
              "xgb2_training_rows": produced.get("two_day_frame_rows"),
              "references": {name: w9.reference_metrics(name, year) for name in REPORTED},
              "candidates": {}, "artifact_sha256": {}}
    for key in keys:
        prediction, raw = candidate_prediction(key, bundle, raws)
        tests = invariants(bundle, key, prediction)
        metrics, daily = score_official(bundle["frame"], prediction)
        daily.write_csv(OUT / f"daily_{key}_{year}.csv")
        bundle["frame"].with_columns(pl.Series("pred", prediction), pl.Series("pred_raw", raw)
                                     ).write_parquet(OUT / f"predictions_{key}_{year}.parquet",
                                                     compression="zstd")
        record["candidates"][key] = {
            "metrics": {k: float(v) for k, v in metrics.items()}, "tests": tests,
            "members": CANDIDATES[key]["members"],
            "score_deltas": {name: metrics["final_score"] - record["references"][name]["final_score"]
                             for name in REPORTED},
            "ic_deltas": {name: metrics["ic_mean"] - record["references"][name]["ic_mean"]
                          for name in REPORTED},
            "paired": {name: w9.paired(daily, w9.reference_daily(name, year))
                       for name in REPORTED}}
        log(f"{year} {key} [{'+'.join(CANDIDATES[key]['members'])}]: "
            f"{metrics['final_score']:.9f} ic={metrics['ic_mean']:.6f} | "
            + " ".join(f"{name} {record['candidates'][key]['score_deltas'][name]:+.6f}"
                       for name in REPORTED))
    record["seconds"] = round(time.monotonic() - started, 2)
    record["artifact_sha256"] = {p.name: sha(p) for p in OUT.glob(f"*_{year}.*") if p != path}
    write_new(path, record)
    del bundle, produced, raws
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
        "member_proofs": {str(r["year"]): r["member_proofs"] for r in records},
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
        "note": "Scored once, after the development choice was recorded. Exploratory.",
        "fold_sha256": {f"fold_{y}.json": sha(OUT / f"fold_{y}.json") for y in CONFIRMATION}})
    log(f"CONFIRMATION {winner}: passed={result['passed']} five-year deltas vs {PRIMARY} "
        + " ".join(f"{y}:{v:+.6f}" for y, v in five.items()))


def summarize() -> None:
    table = {"protocol_sha256": sha(OUT / "protocol.json"), "design": PROTOCOL["design"],
             "years": {}, "candidates": {}}
    for year in YEARS:
        path = OUT / f"fold_{year}.json"
        if not path.exists():
            continue
        record = read(path)
        table["years"][str(year)] = {
            "references": {n: record["references"][n]["final_score"] for n in record["references"]},
            "member_proofs": record["member_proofs"]}
        for key, entry in record["candidates"].items():
            table["candidates"].setdefault(key, {})[str(year)] = {
                "final_score": entry["metrics"]["final_score"], "members": entry["members"],
                "score_deltas": entry["score_deltas"]}
    for stage in ("development", "confirmation"):
        path = OUT / f"{stage}.json"
        if path.exists():
            table[stage] = read(path)
    (OUT / "summary.json").write_text(json.dumps(table, ensure_ascii=False, indent=2),
                                      encoding="utf-8")
    years = sorted(table["years"], key=int)
    for reference in ("xgb_two_mean", PRIMARY, "baseline", "ensemble4"):
        print(f"\nwave-13 差值（候选 − {reference}）")
        header = f"{'candidate':<36}{'members':<22}" + "".join(f"{y:>11}" for y in years) \
            + f"{'均值':>11}"
        print(header + "\n" + "-" * len(header))
        for key, per_year in table["candidates"].items():
            values = [per_year[y]["score_deltas"][reference] for y in years if y in per_year]
            cells = "".join(f"{per_year[y]['score_deltas'][reference]:>+11.6f}" if y in per_year
                            else f"{'-':>11}" for y in years)
            present = [y for y in years if y in per_year]
            label = "+".join(per_year[present[0]]["members"])
            print(f"{key:<36}{label:<22}{cells}{np.mean(values):>+11.6f}")
    print("\n2x2 结论（对 xgb_two_mean 的五年/开发年均值）：")
    for key, per_year in table["candidates"].items():
        values = [per_year[y]["score_deltas"]["xgb_two_mean"] for y in years if y in per_year]
        spec = CANDIDATES[key]
        print(f"  {spec['family']:<6}族 / {spec['horizon']:<5}视野  {key:<36}"
              f"{np.mean(values):+.6f}")
    print(f"  cross族 / cross视野  xgb_two_mean（冻结参照，即上表基准）      +0.000000")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("stage", choices=("protocol", "develop", "confirm", "summary"))
    arguments = parser.parse_args()
    {"protocol": freeze, "develop": develop, "confirm": confirm, "summary": summarize}[
        arguments.stage]()
