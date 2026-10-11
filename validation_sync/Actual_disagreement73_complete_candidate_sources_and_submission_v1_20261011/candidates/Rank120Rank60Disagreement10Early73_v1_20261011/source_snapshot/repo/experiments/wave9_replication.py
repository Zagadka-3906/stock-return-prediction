"""Wave-9 replication: one pre-declared question, on the two years wave-9 never scored.

Wave-9's development stage scored four candidates on 2020-2022 and **none passed** its
frozen gate, so its confirmation stage is prohibited and stays prohibited. One result was
nevertheless internally consistent enough to be worth a disclosed replication rather than
a silent re-roll of the gate:

    W9c_xgb_ext — the frozen T2f XGBoost recipe on the 83-column panel — beat the SAME
    recipe on the base 63 columns by +0.000534 (2020), +0.000740 (2021), +0.001660 (2022),
    mean +0.000978, positive in all three years, with mean IC +0.000982. It missed the
    pre-frozen +0.001 development threshold against that reference by 0.000022, and it
    failed against the r4 ensemble (worst year -0.003918 in 2022).

This module asks exactly one question, fixed before any scoring: does the same candidate,
with its definition copied verbatim and nothing retuned, also beat the plain XGBoost
backbone on 2023 and 2024 — the two years wave-9 never scored for it?

WHAT THIS IS NOT. It is not an adoption gate and it does not revive the wave-9 gate, which
failed and stays failed. Every year involved has been examined repeatedly by eight earlier
suites, the r4 revalidation and the r5 round, so a positive result here is a *replication
with a disclosed prior*, not out-of-sample evidence, and it carries the additional bias
that this is the one candidate out of four whose development pattern looked favourable.
No release, submission, report or pointer changes as a result of this module. All writes
stay inside experiments/wave9_replication_20260927/.
"""
from __future__ import annotations

import argparse
import gc
import json
import time
from pathlib import Path

import numpy as np
import polars as pl

from run import ROOT
import experiments.wave9_exploratory as w9

REPLICATION = ROOT / "experiments" / "wave9_replication_20260927"
CANDIDATE = "W9c_xgb_ext"
YEARS = (2023, 2024)
PRIMARY_REFERENCE = "xgboost"
DISCLOSED_DEVELOPMENT_PRIOR = {
    "years": [2020, 2021, 2022],
    "score_deltas_vs_xgboost": {"2020": 0.000534, "2021": 0.000740, "2022": 0.001660},
    "mean_score_delta_vs_xgboost": 0.000978,
    "mean_ic_delta_vs_xgboost": 0.000982,
    "positive_years_vs_xgboost": 3,
    "wave9_development_gate": "FAILED",
    "wave9_failure_reasons": ["mean delta vs xgboost +0.000978 is below the frozen +0.001 "
                              "threshold by 0.000022",
                              "mean delta vs ensemble4 +0.000207 with a worst year of -0.003918"],
    "selection_note": "this is the one candidate of four whose development pattern looked "
                      "favourable, so the replication carries that selection bias",
}
CRITERION = {
    "consistent": "the mean official-score delta against the plain XGBoost backbone over "
                  "2023+2024 is positive AND both years are positive",
    "role": "descriptive replication criterion fixed before scoring; NOT an adoption gate",
}
PROTOCOL = {
    "experiment": "wave9_replication_extended_features_on_the_xgboost_backbone",
    "status": "exploratory_replication_with_disclosed_prior_all_years_previously_viewed",
    "candidate": CANDIDATE,
    "candidate_definition_copied_from": "experiments/wave9_exploratory_20260927/protocol.json",
    "candidate_definition": None,
    "features": None,
    "xgboost_recipe": None,
    "postprocess": None,
    "years": list(YEARS),
    "primary_reference": PRIMARY_REFERENCE,
    "reported_references": list(w9.REFERENCES),
    "disclosed_development_prior": DISCLOSED_DEVELOPMENT_PRIOR,
    "criterion": CRITERION,
    "prohibited": ["Retuning any hyper-parameter, feature or weight",
                   "Adding a second candidate or a second question",
                   "Treating a positive result as an adoption gate or as out-of-sample evidence",
                   "Writing outside experiments/wave9_replication_20260927/",
                   "Touching releases/, outputs/, active_release.json or maintenance/"],
    "harness_proofs": "every fold re-runs the wave-9 proof: the released stack reproduces the "
                      "frozen baseline prediction exactly, the baseline composite anchors to the "
                      "recorded value within 1e-12, and all four reference composites rebuild from "
                      "their frozen daily evidence within 1e-9",
}


def log(message: str) -> None:
    print(f"[{time.strftime('%H:%M:%S')}] {message}", flush=True)


def read(path: Path) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8-sig"))


def write_new(path: Path, payload) -> None:
    with Path(path).open("x", encoding="utf-8") as stream:
        json.dump(payload, stream, ensure_ascii=False, indent=2, allow_nan=False)


def freeze() -> None:
    REPLICATION.mkdir(parents=True, exist_ok=True)
    if (REPLICATION / "protocol.json").exists():
        raise SystemExit("Replication protocol already frozen")
    wave9 = read(w9.OUT / "protocol.json")
    if not (w9.OUT / "development.json").exists():
        raise SystemExit("Wave-9 development must be recorded before a replication is declared")
    development = read(w9.OUT / "development.json")
    if development["winner"] is not None:
        raise SystemExit("Wave-9 produced a winner; use its own confirmation stage instead")
    for year in YEARS:
        if (w9.OUT / f"fold_{year}.json").exists():
            raise SystemExit(f"{year} was already scored in wave-9; this replication would not be "
                             "on unseen years")
    payload = {**PROTOCOL,
               "candidate_definition": wave9["candidates"][CANDIDATE],
               "features": {"base_count": wave9["base_feature_count"],
                            "new": wave9["new_features"], "groups": wave9["feature_groups"],
                            "extended_count": wave9["extended_feature_count"]},
               "xgboost_recipe": w9.XGB_CONFIG,
               "postprocess": wave9["postprocess"],
               "auxiliary": wave9["auxiliary"],
               "wave9_protocol_sha256": w9.sha(w9.OUT / "protocol.json"),
               "wave9_development_sha256": w9.sha(w9.OUT / "development.json"),
               "frozen_at_local": time.strftime("%Y-%m-%dT%H:%M:%S"),
               "source_sha256": w9.sha(Path(__file__)),
               "harness_source_sha256": w9.sha(Path(w9.__file__))}
    write_new(REPLICATION / "protocol.json", payload)
    log(f"Froze the replication protocol for {CANDIDATE} on {list(YEARS)}; the development prior "
        "is disclosed inside it and no score exists yet")


def verify_protocol() -> dict:
    protocol = read(REPLICATION / "protocol.json")
    if protocol["source_sha256"] != w9.sha(Path(__file__)):
        raise SystemExit("This module changed after the replication protocol was frozen")
    if protocol["harness_source_sha256"] != w9.sha(Path(w9.__file__)):
        raise SystemExit("wave9_exploratory.py changed after the replication protocol was frozen")
    if protocol["candidate_definition"] != w9.CANDIDATES[CANDIDATE]:
        raise SystemExit("Candidate definition drifted from the frozen protocol")
    if protocol["xgboost_recipe"] != w9.XGB_CONFIG:
        raise SystemExit("XGBoost recipe drifted from the frozen protocol")
    return protocol


def gain_share(bundle: dict) -> dict:
    """Descriptive mechanism check: how much split gain the twenty new columns take."""
    import xgboost as xgb
    import torch
    from run import to_matrix
    frame = bundle["train"].select(w9.KEYS + w9.EXTENDED_FEATURES + ["y_rank"]).sort(
        "trade_date", "ts_code")
    matrix = to_matrix(frame, w9.EXTENDED_FEATURES)
    label = frame["y_rank"].to_numpy().astype(np.float32)
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model = xgb.XGBRegressor(n_estimators=w9.XGB_CONFIG["rounds"],
                             max_depth=w9.XGB_CONFIG["max_depth"],
                             learning_rate=w9.XGB_CONFIG["learning_rate"],
                             subsample=w9.XGB_CONFIG["subsample"],
                             colsample_bytree=w9.XGB_CONFIG["colsample_bytree"],
                             reg_lambda=w9.XGB_CONFIG["reg_lambda"],
                             tree_method=w9.XGB_CONFIG["tree_method"], device=device,
                             seed=w9.XGB_CONFIG["seed"], n_jobs=w9.XGB_CONFIG["n_jobs"])
    model.fit(matrix, label)
    raw = model.predict(to_matrix(bundle["valid"], w9.EXTENDED_FEATURES)).astype(np.float64)
    frozen = pl.read_parquet(REPLICATION / f"raw_xgb_ext_{bundle['year']}.parquet").sort(
        "trade_date", "ts_code")["pred_raw"].to_numpy().astype(np.float64)
    valid = bundle["valid"]["price_valid"].to_numpy()
    identical = bool(np.array_equal(raw[valid], frozen[valid]))
    booster = model.get_booster()
    scores = booster.get_score(importance_type="gain")
    # XGBoost names matrix columns f0..fn, so map both conventions and default to zero.
    gains = np.array([scores.get(f"f{index}", scores.get(name, 0.0))
                      for index, name in enumerate(w9.EXTENDED_FEATURES)], dtype=np.float64)
    if gains.sum() <= 0:
        raise AssertionError(f"XGBoost reported no split gain; keys look like {list(scores)[:3]}")
    new = gains[len(w9.BASE_FEATURES):]
    per_feature = {name: float(gains[index] / gains.sum())
                   for index, name in enumerate(w9.EXTENDED_FEATURES)}
    top_new = sorted(((name, per_feature[name]) for name in w9.NEW_FEATURES),
                     key=lambda item: -item[1])[:8]
    del matrix, label, model, frame
    gc.collect()
    return {"refit_reproduces_the_scored_raw_exactly": identical,
            "new_feature_gain_share": float(new.sum() / gains.sum()),
            "new_feature_count": len(w9.NEW_FEATURES),
            "column_share": len(w9.NEW_FEATURES) / len(w9.EXTENDED_FEATURES),
            "top_new_features_by_gain_share": [{"feature": name, "gain_share": value}
                                               for name, value in top_new]}


def run() -> None:
    protocol = verify_protocol()
    w9.OUT = REPLICATION
    if (REPLICATION / "results.json").exists():
        raise SystemExit("Replication already recorded; preserving it")
    w9.joined_panel()
    started = time.monotonic()
    folds = {}
    for year in YEARS:
        bundle = w9.fold(year)
        proof = w9.prove(bundle)
        raw = w9.train_xgboost(bundle, w9.EXTENDED_FEATURES, "xgb_ext")
        prediction, raw = w9.predict(bundle, CANDIDATE, {CANDIDATE: raw})
        tests = w9.invariants(bundle, CANDIDATE, {CANDIDATE: raw}, prediction)
        metrics, daily = w9.score_official(bundle["frame"], prediction)
        daily.write_csv(REPLICATION / f"daily_{CANDIDATE}_{year}.csv")
        bundle["frame"].with_columns(pl.Series("pred", prediction), pl.Series("pred_raw", raw)
                                     ).write_parquet(REPLICATION
                                                     / f"predictions_{CANDIDATE}_{year}.parquet",
                                                     compression="zstd")
        diagnostics = gain_share(bundle)
        paired_vs = {name: w9.paired(daily, w9.reference_daily(name, year))
                     for name in w9.REFERENCES}
        deltas = {name: metrics["final_score"] - w9.reference_metrics(name, year)["final_score"]
                  for name in w9.REFERENCES}
        folds[str(year)] = {"metrics": metrics, "tests": tests, "proof": proof,
                            "references": {name: w9.reference_metrics(name, year)
                                           for name in w9.REFERENCES},
                            "score_deltas": deltas, "paired": paired_vs,
                            "diagnostics": diagnostics}
        log(f"{year} {CANDIDATE}: {metrics['final_score']:.9f} ic={metrics['ic_mean']:.6f} "
            f"excess={metrics['annual_excess']:.6f} turn={metrics['mean_turnover']:.6f} | "
            + " ".join(f"{name} {deltas[name]:+.6f}" for name in w9.REFERENCES)
            + f" | new-feature gain share {diagnostics['new_feature_gain_share']:.4f}")
        del bundle
        gc.collect()
    primary = [folds[str(year)]["score_deltas"][PRIMARY_REFERENCE] for year in YEARS]
    mean_primary = float(np.mean(primary))
    consistent = bool(mean_primary > 0 and all(value > 0 for value in primary))
    five_year = {**{str(year): value for year, value in
                    zip((2020, 2021, 2022),
                        [DISCLOSED_DEVELOPMENT_PRIOR["score_deltas_vs_xgboost"][str(y)]
                         for y in (2020, 2021, 2022)])},
                 **{str(year): folds[str(year)]["score_deltas"][PRIMARY_REFERENCE]
                    for year in YEARS}}
    write_new(REPLICATION / "results.json", {
        "stage": "wave9_replication", "generated_at_local": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "seconds": round(time.monotonic() - started, 2),
        "protocol_sha256": w9.sha(REPLICATION / "protocol.json"),
        "candidate": CANDIDATE, "years": list(YEARS), "primary_reference": PRIMARY_REFERENCE,
        "folds": folds,
        "criterion": protocol["criterion"],
        "mean_score_delta_vs_primary": mean_primary,
        "score_deltas_vs_primary": dict(zip([str(y) for y in YEARS], primary)),
        "consistent_with_development": consistent,
        "five_year_deltas_vs_primary": five_year,
        "five_year_mean_delta_vs_primary": float(np.mean(list(five_year.values()))),
        "five_year_positive_years_vs_primary": int(sum(v > 0 for v in five_year.values())),
        "verdict": ("replication consistent" if consistent else "replication NOT consistent"),
        "not_an_adoption_gate": True,
        "limitations": [
            "All five years have been examined repeatedly; this is a replication with a disclosed "
            "prior, not out-of-sample evidence.",
            "This candidate is the one of four whose development pattern looked favourable, so the "
            "replication inherits that selection bias.",
            "The wave-9 development gate failed and is not revived by anything recorded here.",
            "No confidence interval here corrects for cumulative candidate selection.",
        ]})
    log(f"REPLICATION vs {PRIMARY_REFERENCE}: 2023 {primary[0]:+.6f}, 2024 {primary[1]:+.6f}, "
        f"mean {mean_primary:+.6f} → {protocol['criterion']['role'].split(';')[0]}: "
        f"{'CONSISTENT' if consistent else 'NOT CONSISTENT'}")
    log(f"Five-year deltas vs {PRIMARY_REFERENCE}: "
        + " ".join(f"{y}:{v:+.6f}" for y, v in five_year.items()))


def summarize() -> None:
    results = read(REPLICATION / "results.json")
    print(f"\n{CANDIDATE} — XGBoost 主干，63 列 vs 83 列（同一配方，只多 20 个新特征）")
    print(f"{'年份':<8}{'候选综合分':>16}{'XGBoost 参照':>16}{'差值':>14}{'新特征增益占比':>16}")
    prior = DISCLOSED_DEVELOPMENT_PRIOR["score_deltas_vs_xgboost"]
    for year in (2020, 2021, 2022):
        print(f"{year:<8}{'(开发年，已披露)':>16}{'-':>16}{prior[str(year)]:>+14.6f}{'-':>16}")
    for year in YEARS:
        fold = results["folds"][str(year)]
        print(f"{year:<8}{fold['metrics']['final_score']:>16.9f}"
              f"{fold['references'][PRIMARY_REFERENCE]['final_score']:>16.9f}"
              f"{fold['score_deltas'][PRIMARY_REFERENCE]:>+14.6f}"
              f"{fold['diagnostics']['new_feature_gain_share']:>16.4f}")
    print(f"\n五年均值 {results['five_year_mean_delta_vs_primary']:+.6f}，"
          f"为正年份 {results['five_year_positive_years_vs_primary']}/5，"
          f"复核判定：{results['verdict']}")
    print("这不是采纳门禁；wave-9 的开发门禁仍然是失败的。")
    print("\n对全部四个参照的差值：")
    for year in YEARS:
        fold = results["folds"][str(year)]
        print(f"  {year}: " + "  ".join(f"{name} {value:+.6f}"
                                        for name, value in fold["score_deltas"].items()))
    print("\n新特征增益占比最高的项（2024 折）：")
    for item in results["folds"][str(YEARS[-1])]["diagnostics"]["top_new_features_by_gain_share"]:
        print(f"  {item['feature']:<20}{item['gain_share']:.4f}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("stage", choices=("protocol", "run", "summary"))
    arguments = parser.parse_args()
    {"protocol": freeze, "run": run, "summary": summarize}[arguments.stage]()
