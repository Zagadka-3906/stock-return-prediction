"""Wave-20: transductive adaptation and recipe-diverse twins, paired by seed.

Wave-19 tests the last label/recipe/regime ideas. Two mechanisms remain that are structurally
different from everything in eighteen waves, and both can be measured with the paired instrument:

  W20a  TRANSDUCTIVE SELF-TRAINING. The delivery model trains on history through 2024-12 and is
        scored on 2025-2026, a period whose feature distribution it has only seen as inputs. A fold
        analogue: the seed-s teacher (wave-14's frozen fit, trained without the validation year)
        pseudo-labels the validation year's own feature rows with its per-day cross-sectional rank;
        the seed-s student then refits on purged history PLUS those pseudo-labelled rows and is
        scored on the validation year's TRUE labels. No true validation label enters training - the
        pseudo-label is a function of the teacher and of test-day features only - so the design is
        causal, and transduction (using unlabelled scored-period features) is legitimate here
        because the competition supplies those features at prediction time. Mechanism: covariate
        shift between the training history and the scored period is real, and this is the only
        mechanism in the project that adapts to it.
  W20b  RECIPE-DIVERSE TWINS. Wave-18 fitted, for every seed and year, the deterministic twin
        (subsample=colsample_bytree=1.0) of each bagged fit and showed it is worse in mean but has
        zero seed variance. Whether the *pair* {bagged_s, deterministic_s} averaged per day beats
        bagged_s alone at fixed seed is a different question from wave-14's control (which compared
        heterogeneous FAMILIES) and from wave-16 (which added members of the SAME recipe): the twin
        carries a different bias-variance decomposition of the same signal. All raws already exist
        on disk, so this arm costs no training at all.

DESIGN. Wave-15's paired instrument against frozen wave-14 arm A (W20a) or against the same seed's
single bagged fit (W20b); eight paired replicates per year. Pre-declared criterion: resolvability
|mean| > 2 SE, two-sided, per year and five-year. NO promotion gate: all five years are viewed, so a
resolvable positive is hypothesis-generating only and would need a new blind period.

Writes only inside experiments/wave20_transductive_20260928/. Never touches releases/, outputs/,
active_release.json or maintenance/.
"""
from __future__ import annotations

import argparse
import gc
import json
import time
from pathlib import Path

import numpy as np
import polars as pl
from scipy.stats import rankdata

from run import ROOT, to_matrix
import experiments.wave9_exploratory as w9
import experiments.wave14_seed_average as w14
import experiments.wave18_deterministic_recipe as w18
from experiments.revalidate_fold_local import score_official

OUT = ROOT / "experiments" / "wave20_transductive_20260928"
CACHE = OUT
W14 = w14.OUT
W18 = w18.OUT
KEYS = ["ts_code", "trade_date"]
YEARS = (2020, 2021, 2022, 2023, 2024)
SEEDS = w14.SEEDS
BASE = w9.BASE_FEATURES
ARM_A = "base63_one_day"
ARM_TRANS = "transductive_self_training"
ARM_TWIN = "bagged_plus_deterministic_twin"
RESOLVABILITY = {
    "criterion": "for each arm, each year and the five-year mean, report the mean paired difference "
                 "across the eight seeds and its standard error (sd / sqrt(8)); resolvable when "
                 "|mean| > 2 x SE, two-sided",
    "no_promotion": "all five years have been viewed repeatedly; a resolvable positive is "
                    "hypothesis-generating only and would require a new blind period",
}
PROTOCOL = {
    "experiment": "wave20_transductive_and_twins",
    "status": "exploratory_descriptive_all_years_previously_viewed",
    "arms": {
        ARM_TRANS: {"recipe": w14.RECIPE,
                    "source": "student refit per seed on the purged history plus the validation "
                              "year's feature rows pseudo-labelled by that seed's frozen wave-14 "
                              "teacher rank; scored on the validation year's true labels",
                    "transductive": "uses unlabelled scored-period features, never their labels"},
        ARM_TWIN: {"recipe": "rank average of wave-14's bagged raw and wave-18's deterministic raw "
                             "for the same seed",
                   "source": "cache-only; no training in this arm"},
    },
    "seeds": list(SEEDS), "years": list(YEARS),
    "design": "W20a paired by seed against frozen wave-14 arm A; W20b paired by seed against the "
              "same seed's single bagged fit (wave-14's per-seed composite)",
    "postprocess": "the released stack exactly, via cached_recheck.make_prediction with the frozen "
                   "pooled auxiliary at top_only 0.25, identical for every arm",
    "scorer": "the unmodified evaluate.py via revalidate_fold_local.score_official",
    "resolvability": RESOLVABILITY,
    "prior_art": {
        "experiments/wave14_seed_average_20260927/": "arm A, the teachers, and the twin's bagged half",
        "experiments/wave18_deterministic_20260928/": "the deterministic twins",
        "experiments/wave16_seed_curve_20260928/": "same-recipe members saturate at K=8",
    },
    "harness_proofs": [
        "the frozen XGBoost reference composite is reproduced from its frozen prediction within "
        "1e-12 in every year before any arm is scored",
        "the N-member rank average reproduces the frozen r5 xgb_two_mean raw bit-for-bit at N=2 in "
        "every year",
        "the teacher raw used for pseudo-labelling is byte-identical to wave-14's frozen cache in "
        "every year",
        "the twin raw is byte-identical to wave-18's frozen cache in every year",
        "the student's training frame carries the pseudo-label, never the true validation label, on "
        "the validation-year rows, and its history part is byte-identical to wave-14's purged frame",
    ],
    "prohibited": ["Adding a seed, arm or year after any score exists",
                   "Changing the recipe, the pseudo-label rule or the criterion after seeing a "
                   "result",
                   "Presenting a resolvable positive as adoptable without a new blind period",
                   "Writing outside experiments/wave20_transductive_20260928/",
                   "Touching releases/, outputs/, active_release.json or maintenance/"],
    "limitations": [
        "All five years have been examined repeatedly; nothing here is out-of-sample.",
        "The student is trained on the teacher's errors as if they were labels, so it cannot beat "
        "the teacher by information - only by adapting to the scored period's feature distribution.",
        "Eight paired replicates resolve about 0.001; anything smaller stays unresolvable.",
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


def teacher_raw(bundle: dict, seed: int) -> np.ndarray:
    path = W14 / f"raw_seed{seed}_{bundle['year']}.parquet"
    raw = pl.read_parquet(path).sort("trade_date", "ts_code")["pred_raw"].to_numpy()
    return raw


def twin_raw(bundle: dict, seed: int) -> np.ndarray:
    path = W18 / f"raw_deterministic_100_100_seed{seed}_{bundle['year']}.parquet"
    return pl.read_parquet(path).sort("trade_date", "ts_code")["pred_raw"].to_numpy()


def pseudo_frame(bundle: dict, raw: np.ndarray) -> pl.DataFrame:
    """The validation year's feature rows, labelled by the teacher's per-day cross-sectional rank."""
    valid = bundle["valid"]["price_valid"].to_numpy()
    days = bundle["valid"]["trade_date"].n_unique()
    codes = len(valid) // days
    matrix = raw.reshape(days, codes)
    mask = valid.reshape(days, codes)
    pseudo = np.zeros((days, codes), dtype=np.float64)
    for day in range(days):
        keep = mask[day] & np.isfinite(matrix[day])
        count = int(keep.sum())
        if count:
            pseudo[day, keep] = rankdata(matrix[day][keep], method="average") / count
    frame = bundle["valid"].select(KEYS + BASE + ["price_valid"])
    return frame.with_columns(pl.Series("pseudo_rank", pseudo.reshape(-1)))


def student_frame(bundle: dict, pseudo: pl.DataFrame) -> pl.DataFrame:
    history = (w9.lazy_panel()
               .filter(pl.col("is_train") & (pl.col("trade_date") < bundle["cutoff"])
                       & pl.col("y_rank").is_not_null() & pl.col("price_valid"))
               .select(KEYS + BASE + ["y_rank"]).collect())
    if history.height != bundle["train"].select(KEYS).height:
        raise AssertionError(f"{bundle['year']}: history part is not wave-14's purged frame")
    future = pseudo.filter(pl.col("price_valid")).select(KEYS + BASE + ["pseudo_rank"])
    columns = KEYS + BASE + ["y_rank", "pseudo_rank"]
    joined = pl.concat([history.with_columns(pl.lit(None, dtype=pl.Float64).alias("pseudo_rank"))
                        .select(columns),
                        future.with_columns(pl.lit(None, dtype=pl.Float32).alias("y_rank"))
                        .select(columns)])
    label = np.where(np.isnan(joined["y_rank"].to_numpy()),
                     joined["pseudo_rank"].to_numpy(), joined["y_rank"].to_numpy())
    if np.isnan(label).any():
        raise AssertionError("Student frame has an unlabelled row")
    return joined.with_columns(pl.Series("student_label", label))


def fit(bundle: dict, seed: int, frame: pl.DataFrame, name: str) -> np.ndarray:
    path = CACHE / f"raw_{name}_seed{seed}_{bundle['year']}.parquet"
    if path.exists():
        return pl.read_parquet(path).sort("trade_date", "ts_code")["pred_raw"].to_numpy()
    import xgboost as xgb
    ordered = frame.select(KEYS + BASE + ["student_label"]).sort("trade_date", "ts_code")
    matrix = to_matrix(ordered, BASE)
    label = ordered["student_label"].to_numpy().astype(np.float32)
    model = xgb.XGBRegressor(**{k: v for k, v in w14.RECIPE.items() if k != "n_jobs"}, seed=seed,
                             n_jobs=w14.RECIPE["n_jobs"])
    started = time.monotonic()
    model.fit(matrix, label)
    seconds = round(time.monotonic() - started, 1)
    raw = model.predict(to_matrix(bundle["valid"], BASE)).astype(np.float64)
    raw[~bundle["valid"]["price_valid"].to_numpy()] = -1e6
    CACHE.mkdir(parents=True, exist_ok=True)
    bundle["valid"].select(KEYS).with_columns(pl.Series("pred_raw", raw)).write_parquet(
        path, compression="zstd")
    log(f"{bundle['year']} {name} seed {seed}: fitted {len(label):,} rows in {seconds}s")
    del matrix, label, model
    gc.collect()
    return raw


def run_year(year: int) -> dict:
    path = OUT / f"year_{year}.json"
    if path.exists():
        log(f"{year} already recorded; preserving it")
        return read(path)
    started = time.monotonic()
    w9.OUT = OUT
    bundle = w9.fold(year)
    reference = w9.reference_metrics("xgboost", year)
    frozen_frame = pl.read_parquet(
        w9.REFERENCES["xgboost"]["predictions"] / f"predictions_xgboost_{year}.parquet"
    ).sort("trade_date", "ts_code")
    check, _ = score_official(bundle["frame"], frozen_frame["pred"].to_numpy().astype(np.float64))
    anchor = max(abs(check[k] - reference[k]) for k in reference)
    if anchor > 1e-12:
        raise AssertionError(f"{year}: frozen xgboost anchor off by {anchor:.3e}")
    log(f"{year} anchor reproduced {reference['final_score']:.15f} exactly")
    valid = bundle["valid"]["price_valid"].to_numpy()
    days = bundle["valid"]["trade_date"].n_unique()
    codes = len(valid) // days
    w14.combination_proof(bundle, codes)
    arm_a = read(W14 / f"year_{year}.json")

    pairs = {ARM_TRANS: {}, ARM_TWIN: {}}
    for seed in SEEDS:
        teacher = teacher_raw(bundle, seed)
        student = fit(bundle, seed, student_frame(bundle, pseudo_frame(bundle, teacher)), ARM_TRANS)
        metrics, daily = score_official(bundle["frame"], w14.stacked(bundle, student))
        daily.write_csv(OUT / f"daily_{ARM_TRANS}_seed{seed}_{year}.csv")
        a = arm_a["singles"][str(seed)]
        pairs[ARM_TRANS][str(seed)] = {"b": {k: float(v) for k, v in metrics.items()},
                                       "a_final": a["final_score"],
                                       "delta": float(metrics["final_score"] - a["final_score"])}
        twin = w14.rank_average_n([teacher, twin_raw(bundle, seed)], valid, codes)
        metrics2, _ = score_official(bundle["frame"], w14.stacked(bundle, twin))
        pairs[ARM_TWIN][str(seed)] = {"b": {k: float(v) for k, v in metrics2.items()},
                                      "a_final": a["final_score"],
                                      "delta": float(metrics2["final_score"] - a["final_score"])}
        log(f"{year} seed {seed}: transductive {pairs[ARM_TRANS][str(seed)]['delta']:+.6f}, "
            f"twin {pairs[ARM_TWIN][str(seed)]['delta']:+.6f}")

    def summarise(arm: str) -> dict:
        deltas = [pairs[arm][str(seed)]["delta"] for seed in SEEDS]
        mean = float(np.mean(deltas))
        se = float(np.std(deltas, ddof=1) / np.sqrt(len(deltas)))
        b = [pairs[arm][str(seed)]["b"] for seed in SEEDS]
        return {"mean_delta": mean, "se": se, "t": mean / se if se else None,
                "resolvable": bool(abs(mean) > 2 * se), "per_seed_deltas": deltas,
                "mean_ic_delta": float(np.mean([x["ic_mean"] for x in b])
                                       - np.mean([arm_a["singles"][str(s)]["ic_mean"]
                                                  for s in SEEDS])),
                "mean_turnover_delta": float(np.mean([x["mean_turnover"] for x in b])
                                             - np.mean([arm_a["singles"][str(s)]["mean_turnover"]
                                                        for s in SEEDS])),
                "mean_excess_delta": float(np.mean([x["annual_excess"] for x in b])
                                           - np.mean([arm_a["singles"][str(s)]["annual_excess"]
                                                      for s in SEEDS]))}

    record = {"year": year, "seconds": round(time.monotonic() - started, 2),
              "anchor_max_abs_diff": anchor,
              "arms": {arm: summarise(arm) for arm in pairs}, "pairs": pairs}
    for arm in pairs:
        a = record["arms"][arm]
        log(f"{year} {arm}: paired mean {a['mean_delta']:+.6f} +/- {a['se']:.6f} "
            f"(t={a['t']:+.2f}, {'resolvable' if a['resolvable'] else 'unresolvable'}); "
            f"IC {a['mean_ic_delta']:+.6f}, turnover {a['mean_turnover_delta']:+.6f}, "
            f"excess {a['mean_excess_delta']:+.6f}")
    write_new(path, record)
    gc.collect()
    return record


def freeze() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    if (OUT / "protocol.json").exists():
        raise SystemExit("Wave-20 protocol already frozen")
    sources = [Path(__file__), Path(w9.__file__), Path(w14.__file__), Path(w18.__file__),
               w9.JOINED_PANEL, ROOT / "data/features.parquet", ROOT / "evaluate.py",
               ROOT / "run.py", ROOT / "src/scoring.py", ROOT / "experiments/cached_recheck.py",
               ROOT / "experiments/revalidate_fold_local.py", W14 / "protocol.json",
               W18 / "protocol.json"]
    for year in YEARS:
        sources += [w9.R4 / f"predictions_xgboost_{year}.parquet",
                    w9.R4 / f"result_{year}.json", W14 / f"year_{year}.json"]
        sources += [W14 / f"raw_seed{seed}_{year}.parquet" for seed in SEEDS]
        sources += [W18 / f"raw_deterministic_100_100_seed{seed}_{year}.parquet" for seed in SEEDS]
    payload = {**PROTOCOL, "frozen_at_local": time.strftime("%Y-%m-%dT%H:%M:%S"),
               "source_sha256": sha(Path(__file__)),
               "input_sha256": {p.relative_to(ROOT).as_posix(): sha(p)
                                for p in dict.fromkeys(sources)}}
    write_new(OUT / "protocol.json", payload)
    log(f"Froze the wave-20 protocol: {len(payload['input_sha256'])} pinned inputs, no score exists")


def verify_protocol() -> dict:
    protocol = read(OUT / "protocol.json")
    if protocol["source_sha256"] != sha(Path(__file__)):
        raise SystemExit("wave20_transductive.py changed after its protocol was frozen")
    if protocol["seeds"] != list(SEEDS):
        raise SystemExit("Seeds drifted from the frozen protocol")
    for path, digest in protocol["input_sha256"].items():
        if sha(ROOT / path) != digest:
            raise SystemExit(f"Pinned input changed: {path}")
    return protocol


def summarise() -> None:
    if (OUT / "summary.json").exists():
        raise SystemExit("Summary already recorded; preserving it")
    records = [read(OUT / f"year_{year}.json") for year in YEARS]
    summary = {"years": [r["year"] for r in records], "resolvability": RESOLVABILITY,
               "per_year": {str(r["year"]): r["arms"] for r in records}, "arms": {}}
    for arm in (ARM_TRANS, ARM_TWIN):
        means = [r["arms"][arm]["mean_delta"] for r in records]
        ses = [r["arms"][arm]["se"] for r in records]
        pooled = float(np.mean(means))
        pooled_se = float(np.sqrt(sum(s ** 2 for s in ses)) / len(ses))
        summary["arms"][arm] = {
            "per_year_mean_delta": means, "per_year_se": ses,
            "per_year_resolvable": [r["arms"][arm]["resolvable"] for r in records],
            "five_year_mean_delta": pooled, "five_year_se": pooled_se,
            "five_year_t": pooled / pooled_se if pooled_se else None,
            "five_year_resolvable": bool(abs(pooled) > 2 * pooled_se), "delta_2024": means[-1],
            "mean_ic_delta": float(np.mean([r["arms"][arm]["mean_ic_delta"] for r in records])),
            "mean_turnover_delta": float(np.mean([r["arms"][arm]["mean_turnover_delta"]
                                                  for r in records])),
            "mean_excess_delta": float(np.mean([r["arms"][arm]["mean_excess_delta"]
                                                for r in records]))}
    summary["verdict"] = {
        "resolvable_positive_five_year": [
            arm for arm in summary["arms"]
            if summary["arms"][arm]["five_year_resolvable"]
            and summary["arms"][arm]["five_year_mean_delta"] > 0],
        "resolvable_negative_2024": [
            arm for arm in summary["arms"]
            if summary["arms"][arm]["per_year_resolvable"][-1]
            and summary["arms"][arm]["delta_2024"] < 0],
        "note": "Descriptive. No adoption follows from this round; all five years are viewed and a "
                "resolvable positive would need a new blind period.",
    }
    write_new(OUT / "summary.json", summary)
    print(f"\n{'arm':<32}" + "".join(f"{y:>11}" for y in YEARS) + f"{'五年均值':>11}{'SE':>9}{'t':>7}")
    for arm in (ARM_TRANS, ARM_TWIN):
        a = summary["arms"][arm]
        print(f"{arm:<32}" + "".join(f"{m:>+11.6f}" for m in a["per_year_mean_delta"])
              + f"{a['five_year_mean_delta']:>+11.6f}{a['five_year_se']:>9.6f}"
              f"{a['five_year_t']:>+7.2f}")
        print(f"{'':<32} IC {a['mean_ic_delta']:+.6f}  turnover {a['mean_turnover_delta']:+.6f}"
              f"  excess {a['mean_excess_delta']:+.6f}  resolvable "
              f"{a['per_year_resolvable']}")
    print(f"\n判定：{json.dumps(summary['verdict'], ensure_ascii=False)}")


def selftest() -> None:
    """Everything that could break, on one year, without producing a single new score."""
    OUT.mkdir(parents=True, exist_ok=True)
    folder = OUT / "_selftest"
    folder.mkdir(exist_ok=True)
    global CACHE
    CACHE = folder
    w9.OUT = folder
    year = 2022
    bundle = w9.fold(year)
    reference = w9.reference_metrics("xgboost", year)
    frozen_frame = pl.read_parquet(
        w9.REFERENCES["xgboost"]["predictions"] / f"predictions_xgboost_{year}.parquet"
    ).sort("trade_date", "ts_code")
    check, _ = score_official(bundle["frame"], frozen_frame["pred"].to_numpy().astype(np.float64))
    anchor = max(abs(check[k] - reference[k]) for k in reference)
    if anchor > 1e-12:
        raise AssertionError(f"anchor off by {anchor:.3e}")
    codes = len(bundle["valid"]) // bundle["valid"]["trade_date"].n_unique()
    w14.combination_proof(bundle, codes)
    teacher = teacher_raw(bundle, w14.DELIVERED_SEED)
    pseudo = pseudo_frame(bundle, teacher)
    student = student_frame(bundle, pseudo)
    valid_rows = student.filter(pl.col("trade_date") >= int(bundle["valid"]["trade_date"].min()))
    if valid_rows["y_rank"].is_not_null().any():
        raise AssertionError("A validation-year row carries its true label into training")
    history_rows = student.filter(pl.col("trade_date") < int(bundle["valid"]["trade_date"].min()))
    if history_rows["pseudo_rank"].is_not_null().any():
        raise AssertionError("A history row carries a pseudo-label")
    raw = fit(bundle, w14.DELIVERED_SEED, student, ARM_TRANS)
    twin = w14.rank_average_n([teacher, twin_raw(bundle, w14.DELIVERED_SEED)],
                              bundle["valid"]["price_valid"].to_numpy(), codes)
    result = {"year": year, "anchor_max_abs_diff": anchor,
              "student_rows": student.height,
              "history_rows": history_rows.height, "pseudo_rows": valid_rows.height,
              "pseudo_label_range": [float(pseudo["pseudo_rank"].min()),
                                     float(pseudo["pseudo_rank"].max())],
              "student_raw_finite_on_valid": bool(np.isfinite(
                  raw[bundle["valid"]["price_valid"].to_numpy()]).all()),
              "twin_finite_on_valid": bool(np.isfinite(
                  twin[bundle["valid"]["price_valid"].to_numpy()]).all()),
              "scores_produced": 0,
              "note": "no arm was scored in this stage; the only composite computed is the frozen "
                      "reference anchor, which is a published number"}
    write_new(folder / "result.json", result)
    log(json.dumps(result, ensure_ascii=False, indent=2))


def run() -> None:
    verify_protocol()
    for year in YEARS:
        run_year(year)
    summarise()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("stage", choices=("protocol", "selftest", "run"))
    arguments = parser.parse_args()
    if arguments.stage == "protocol":
        freeze()
    elif arguments.stage == "selftest":
        selftest()
    else:
        run()
