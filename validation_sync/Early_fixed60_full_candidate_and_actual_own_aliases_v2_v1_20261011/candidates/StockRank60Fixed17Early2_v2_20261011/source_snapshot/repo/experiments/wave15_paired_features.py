"""Wave-15: re-measure the one promising signal change with an instrument that can resolve it.

Waves 8-14 established that a single fit of the delivered recipe has a between-seed composite sd of
0.0012-0.0016 and a range of 0.0033-0.0046, so no candidate effect below roughly 0.005 was ever
measurable. That invalidates the *instrument*, not the candidates. The one signal change in twelve
rounds that showed a consistent direction was wave-9's extended feature set on the XGBoost backbone
(+0.000534/+0.000740/+0.001660 against the same recipe on 63 columns in 2020-2022, then +0.000858 in
2023 and −0.002206 in 2024). Its replication failed, but every one of those numbers was a single
draw compared against another single draw.

This round repeats that one comparison with eight seeds per arm, **paired by seed**, which is the
design that actually resolves a 0.001 effect:

  arm A  XGBoost, frozen delivered recipe, 63 base columns   — already fitted and scored by
         wave-14, whose per-seed composites are frozen artifacts reused here unchanged;
  arm B  the identical recipe on the 83-column extended panel — fitted here, same eight seeds.

For each seed s and year y the paired difference is composite(B,y,s) − composite(A,y,s). Eight
paired replicates per year give a standard error of the mean, so the round can report whether the
extended features have a resolvable effect rather than whether one draw beat another draw.

WHY RE-TESTING A REJECTED CANDIDATE IS NOT GATE SHOPPING. Wave-9's verdicts stand exactly as
recorded and are not reopened. This round asks a different, pre-declared question — "is the effect
larger than the measurement noise" — with a better estimator, and it reports the answer with a
standard error whichever sign it has. Nothing is adopted here; there is no promotion gate at all,
only a resolvability criterion declared before scoring.

Writes only inside experiments/wave15_paired_features_20260927/.
"""
from __future__ import annotations

import argparse
import gc
import json
import time
from pathlib import Path

import numpy as np
import polars as pl

from run import ROOT, to_matrix
from src.scoring import Panel
import experiments.wave9_exploratory as w9
import experiments.wave14_seed_average as w14
from experiments.cached_recheck import make_prediction
from experiments.revalidate_fold_local import score_official

OUT = ROOT / "experiments" / "wave15_paired_features_20260927"
W14 = w14.OUT
KEYS = ["ts_code", "trade_date"]
YEARS = (2020, 2021, 2022, 2023, 2024)
SEEDS = w14.SEEDS
BASE = w9.BASE_FEATURES
EXTENDED = w9.EXTENDED_FEATURES
ARM_A = "base63"
ARM_B = "extended83"
RESOLVABILITY = {"criterion": "for each year, and for the five-year mean, report the mean paired "
                              "difference across the eight seeds and its standard error "
                              "(sd / sqrt(8)); the effect is called resolvable in a year when "
                              "|mean| > 2 x SE, and unresolvable otherwise",
                 "two_sided": True,
                 "note": "declared before scoring; a result either way is reported, and no "
                         "promotion follows from resolvability alone"}
PROTOCOL = {
    "experiment": "wave15_paired_seed_replicated_feature_comparison",
    "status": "exploratory_re_measurement_all_years_previously_viewed",
    "arms": {ARM_A: {"features": len(BASE), "source": "wave-14 frozen per-seed fits and scores",
                     "recipe": w14.RECIPE},
             ARM_B: {"features": len(EXTENDED), "source": "fitted here, same eight seeds, same "
                                                          "recipe, same folds",
                     "recipe": w14.RECIPE}},
    "new_features": w9.NEW_FEATURES, "feature_groups": w9.GROUPS,
    "seeds": list(SEEDS), "years": list(YEARS),
    "design": "paired by seed and by year; eight paired replicates per year",
    "postprocess": "the released stack exactly, via cached_recheck.make_prediction with the frozen "
                   "pooled auxiliary at top_only 0.25, identical for both arms",
    "scorer": "the unmodified evaluate.py via revalidate_fold_local.score_official",
    "resolvability": RESOLVABILITY,
    "harness_proofs": [
        "arm A's per-seed composites are read from the frozen wave-14 records and their protocol "
        "hash is pinned here; nothing is refitted for arm A",
        "the fold reproduces the frozen delivered XGBoost composite within 1e-12 before any arm-B "
        "fit, so both arms are scored against the same anchored reference",
        "the N-member rank average used for the 8-seed arm-B average reproduces the frozen r5 "
        "xgb_two_mean raw bit-for-bit at N=2",
    ],
    "prohibited": ["Adding a seed, year, feature or arm after any score exists",
                   "Reopening or reinterpreting any wave-9 gate verdict",
                   "Adopting anything on the basis of this round",
                   "Writing outside experiments/wave15_paired_features_20260927/",
                   "Touching releases/, outputs/, active_release.json or maintenance/"],
    "limitations": [
        "All five years have been viewed repeatedly; this is a better measurement on viewed data, "
        "not new evidence about unseen periods.",
        "The extended-feature arm was the one candidate chosen for re-measurement because it was the "
        "only one with a consistent development-year direction, which is a selection on past results "
        "and is disclosed here.",
        "Seeds share data, features and recipe, so the eight replicates are not independent draws "
        "from the population of possible models; the standard error is therefore a lower bound on "
        "the true uncertainty about a new seed.",
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


def arm_a_record(year: int) -> dict:
    path = W14 / f"year_{year}.json"
    if not path.exists():
        raise SystemExit(f"wave-14 has no frozen record for {year}; run it first")
    record = read(path)
    missing = [str(seed) for seed in SEEDS if str(seed) not in record["singles"]]
    if missing:
        raise SystemExit(f"{year}: wave-14 is missing arm A seeds {missing}")
    return record


def fit_seed(bundle: dict, seed: int, features: list[str]) -> np.ndarray:
    import xgboost as xgb
    frame = bundle["train"].select(KEYS + features + ["y_rank"]).sort("trade_date", "ts_code")
    matrix = to_matrix(frame, features)
    label = frame["y_rank"].to_numpy().astype(np.float32)
    model = xgb.XGBRegressor(**{k: v for k, v in w14.RECIPE.items() if k != "n_jobs"}, seed=seed,
                             n_jobs=w14.RECIPE["n_jobs"])
    started = time.monotonic()
    model.fit(matrix, label)
    seconds = round(time.monotonic() - started, 1)
    raw = model.predict(to_matrix(bundle["valid"], features)).astype(np.float64)
    raw[~bundle["valid"]["price_valid"].to_numpy()] = -1e6
    bundle["valid"].select(KEYS).with_columns(pl.Series("pred_raw", raw)).write_parquet(
        OUT / f"raw_{ARM_B}_seed{seed}_{bundle['year']}.parquet", compression="zstd")
    log(f"{bundle['year']} arm B seed {seed}: fitted on {len(frame):,} rows x {len(features)} "
        f"features in {seconds}s")
    del matrix, label, model, frame
    gc.collect()
    return raw


def stacked(bundle: dict, raw: np.ndarray) -> np.ndarray:
    panel = Panel.from_frame(bundle["frame"].with_columns(pl.Series("pred_raw", raw)))
    auxiliary = bundle["frame"]["aux_raw"].to_numpy().astype(np.float64)
    return make_prediction(panel, auxiliary, "top_only", 0.25)


def freeze() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    if (OUT / "protocol.json").exists():
        raise SystemExit("Wave-15 protocol already frozen")
    sources = [Path(__file__), Path(w9.__file__), Path(w14.__file__), w9.JOINED_PANEL, w9.PANEL_FILE,
               ROOT / "data/features.parquet", ROOT / "evaluate.py", ROOT / "run.py",
               ROOT / "src/scoring.py", ROOT / "experiments/cached_recheck.py",
               ROOT / "experiments/revalidate_fold_local.py",
               ROOT / "experiments/optimize_r5_models.py", W14 / "protocol.json",
               W14 / "summary.json", ROOT / "experiments/wave9_exploratory_20260927/protocol.json",
               ROOT / "experiments/wave9_exploratory_20260927/development.json"]
    for year in YEARS:
        sources += [W14 / f"year_{year}.json", w9.R4 / f"result_{year}.json",
                    w9.R4 / f"predictions_xgboost_{year}.parquet",
                    w9.R5 / f"predictions_xgb_two_mean_{year}.parquet"]
    payload = {**PROTOCOL, "frozen_at_local": time.strftime("%Y-%m-%dT%H:%M:%S"),
               "source_sha256": sha(Path(__file__)),
               "arm_a_source_sha256": {str(year): sha(W14 / f"year_{year}.json") for year in YEARS},
               "input_sha256": {p.relative_to(ROOT).as_posix(): sha(p)
                                for p in dict.fromkeys(sources)}}
    write_new(OUT / "protocol.json", payload)
    log(f"Froze the wave-15 protocol: {len(SEEDS)} paired seeds x {len(YEARS)} years, "
        f"{len(payload['input_sha256'])} pinned inputs, no score exists yet")


def verify_protocol() -> dict:
    protocol = read(OUT / "protocol.json")
    if protocol["source_sha256"] != sha(Path(__file__)):
        raise SystemExit("wave15_paired_features.py changed after its protocol was frozen")
    if protocol["seeds"] != list(SEEDS) or protocol["resolvability"] != RESOLVABILITY:
        raise SystemExit("Seeds or the resolvability criterion drifted from the frozen protocol")
    for year in YEARS:
        if sha(W14 / f"year_{year}.json") != protocol["arm_a_source_sha256"][str(year)]:
            raise SystemExit(f"{year}: the frozen wave-14 arm A record changed")
    for path, digest in protocol["input_sha256"].items():
        if sha(ROOT / path) != digest:
            raise SystemExit(f"Pinned input changed: {path}")
    return protocol


def run_year(year: int) -> dict:
    path = OUT / f"year_{year}.json"
    if path.exists():
        log(f"{year} already recorded; preserving it")
        return read(path)
    started = time.monotonic()
    protocol = read(OUT / "protocol.json")
    arm_a = arm_a_record(year)
    if sha(W14 / f"year_{year}.json") != protocol["arm_a_source_sha256"][str(year)]:
        raise SystemExit(f"{year}: arm A record does not match the frozen protocol")
    w9.OUT = OUT
    bundle = w9.fold(year)
    reference = w9.reference_metrics("xgboost", year)
    frozen = pl.read_parquet(w9.REFERENCES["xgboost"]["predictions"]
                             / f"predictions_xgboost_{year}.parquet").sort("trade_date", "ts_code")
    check, _ = score_official(bundle["frame"], frozen["pred"].to_numpy().astype(np.float64))
    anchor = max(abs(check[k] - reference[k]) for k in reference)
    if anchor > 1e-12:
        raise AssertionError(f"{year}: frozen xgboost anchor off by {anchor:.3e}")
    proof = w14.combination_proof(bundle, len(bundle["valid"]) // bundle["valid"]["trade_date"].n_unique())
    log(f"{year} anchor reproduced {reference['final_score']:.15f} exactly")
    singles, raws = {}, {}
    for seed in SEEDS:
        raw = fit_seed(bundle, seed, EXTENDED)
        raws[seed] = raw
        metrics, daily = score_official(bundle["frame"], stacked(bundle, raw))
        daily.write_csv(OUT / f"daily_{ARM_B}_seed{seed}_{year}.csv")
        singles[str(seed)] = {k: float(v) for k, v in metrics.items()}
    average = w14.rank_average_n([raws[seed] for seed in SEEDS],
                                 bundle["valid"]["price_valid"].to_numpy(),
                                 len(bundle["valid"]) // bundle["valid"]["trade_date"].n_unique())
    average_metrics, average_daily = score_official(bundle["frame"], stacked(bundle, average))
    average_daily.write_csv(OUT / f"daily_{ARM_B}_average8_{year}.csv")
    paired = {str(seed): float(singles[str(seed)]["final_score"]
                               - arm_a["singles"][str(seed)]["final_score"]) for seed in SEEDS}
    values = np.array(list(paired.values()))
    record = {
        "year": year, "seconds": round(time.monotonic() - started, 2),
        "anchor_max_abs_diff": anchor, "combination_proof": proof,
        "arm_a_composites": {str(s): arm_a["singles"][str(s)]["final_score"] for s in SEEDS},
        "arm_b_composites": {str(s): singles[str(s)]["final_score"] for s in SEEDS},
        "arm_b_single_mean": float(np.mean([singles[str(s)]["final_score"] for s in SEEDS])),
        "arm_b_single_sd": float(np.std([singles[str(s)]["final_score"] for s in SEEDS], ddof=1)),
        "arm_a_single_mean": arm_a["single_seed_mean"], "arm_a_single_sd": arm_a["single_seed_sd"],
        "arm_b_average8": float(average_metrics["final_score"]),
        "arm_a_average8": arm_a["average8_metrics"]["final_score"],
        "average8_paired_delta": float(average_metrics["final_score"]
                                       - arm_a["average8_metrics"]["final_score"]),
        "paired_by_seed": paired,
        "paired_mean": float(values.mean()), "paired_sd": float(values.std(ddof=1)),
        "paired_se": float(values.std(ddof=1) / np.sqrt(len(values))),
        "paired_t": float(values.mean() / (values.std(ddof=1) / np.sqrt(len(values))))
        if values.std(ddof=1) > 0 else None,
        "resolvable": bool(abs(float(values.mean()))
                           > 2 * float(values.std(ddof=1) / np.sqrt(len(values)))),
        "arm_b_average8_minus_delivered": float(average_metrics["final_score"]
                                                - reference["final_score"]),
        "arm_b_metrics": {k: float(v) for k, v in average_metrics.items()},
        "arm_b_single_metrics": singles,
    }
    log(f"{year}: paired B−A mean {record['paired_mean']:+.9f} ± SE {record['paired_se']:.9f} "
        f"(t={record['paired_t']:+.2f}, resolvable={record['resolvable']}); arm B single-seed sd "
        f"{record['arm_b_single_sd']:.6f} vs arm A {record['arm_a_single_sd']:.6f}; 8-seed averages "
        f"B {record['arm_b_average8']:.9f} vs A {record['arm_a_average8']:.9f} "
        f"({record['average8_paired_delta']:+.9f})")
    write_new(path, record)
    del bundle, raws
    gc.collect()
    return record


def run() -> None:
    verify_protocol()
    records = [run_year(year) for year in YEARS]
    means = np.array([r["paired_mean"] for r in records])
    ses = np.array([r["paired_se"] for r in records])
    five_mean = float(means.mean())
    five_se = float(np.sqrt((ses ** 2).sum()) / len(ses))
    summary = {
        "years": [r["year"] for r in records],
        "per_year": {str(r["year"]): {"paired_mean": r["paired_mean"], "paired_se": r["paired_se"],
                                      "paired_t": r["paired_t"], "resolvable": r["resolvable"],
                                      "arm_a_single_sd": r["arm_a_single_sd"],
                                      "arm_b_single_sd": r["arm_b_single_sd"],
                                      "average8_paired_delta": r["average8_paired_delta"],
                                      "arm_b_average8_minus_delivered":
                                          r["arm_b_average8_minus_delivered"]} for r in records},
        "five_year_mean_paired_delta": five_mean, "five_year_se": five_se,
        "five_year_t": five_mean / five_se if five_se > 0 else None,
        "five_year_resolvable": bool(abs(five_mean) > 2 * five_se),
        "resolvable_years": int(sum(r["resolvable"] for r in records)),
        "criterion": RESOLVABILITY,
        "note": "Descriptive re-measurement. Wave-9's verdicts are unchanged; this reports whether "
                "the extended-feature effect is larger than the measurement noise. The five-year "
                "standard error treats years as independent, which they are not (shared training "
                "history and cold starts), so it is a lower bound.",
    }
    (OUT / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2),
                                      encoding="utf-8")
    print(f"\n{'year':<7}{'A单种子sd':>12}{'B单种子sd':>12}{'配对均值B−A':>15}{'标准误':>12}"
          f"{'t':>8}{'可分辨':>9}{'8种子平均B−A':>15}")
    for r in records:
        print(f"{r['year']:<7}{r['arm_a_single_sd']:>12.6f}{r['arm_b_single_sd']:>12.6f}"
              f"{r['paired_mean']:>+15.9f}{r['paired_se']:>12.9f}{r['paired_t']:>+8.2f}"
              f"{('是' if r['resolvable'] else '否'):>9}{r['average8_paired_delta']:>+15.9f}")
    print(f"\n五年：配对均值 {five_mean:+.9f} ± {five_se:.9f}（t={summary['five_year_t']:+.2f}），"
          f"可分辨={summary['five_year_resolvable']}，可分辨年份 {summary['resolvable_years']}/5")
    log(f"Wrote {OUT / 'summary.json'}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("stage", choices=("protocol", "run"))
    arguments = parser.parse_args()
    if arguments.stage == "protocol":
        freeze()
    else:
        run()
