"""Wave-18: remove the draw at its source — the deterministic recipe, measured descriptively.

Every lever class in this project now carries a frozen negative record (seventeen waves), and the
user has asked for more schemes a fourth time. One idea remains that has a coherent mechanism and
has never been measured: the refit noise floor of +/-0.001743 (`experiments/refit_noise_eval/`) and
the whole seed-averaging programme exist *because* the delivered recipe randomises rows and columns
via `subsample=0.85` and `colsample_bytree=0.85`. Setting both to 1.0 makes every tree see the same
rows and columns, so the fit no longer depends on the seed at all: the between-seed spread of the
annual composite should collapse to zero by construction, and with it the "the deliverable is one
draw" concern that motivated releases r6 and the wave-16 measurement.

WHAT THIS CAN AND CANNOT DECIDE. It cannot decide adoption. The deterministic recipe's expected
score can only be compared against the bagged recipe on five previously viewed years, i.e. inside
the noise floor, and adopting it would need a blind period that does not exist. What it CAN do is
measure the mechanism (between-seed sd of eight deterministic fits, expected ~0 against the bagged
0.0012-0.0016) and give the expected-score difference with a paired standard error, so the record
shows whether removing bagging costs anything resolvable. Bagging is a regulariser, so the prior is
that the deterministic fit is slightly worse in expectation; if 2024 - the year nearest the real
test period - is resolvably negative, the idea is closed like every other.

DESIGN. Wave-15's paired instrument: arm A is the frozen wave-14 record (eight seeds of the
delivered bagged recipe), arm B is the identical recipe with subsample=colsample_bytree=1.0, same
eight seeds, same folds; the paired difference per seed and year carries a standard error coming
from arm A's seed spread. Additionally the eight arm-B composites per year give arm B's own
between-seed sd, which is the mechanism proof. Pre-declared criterion: resolvability |mean| > 2 SE,
two-sided, per year and five-year; NO promotion gate, a resolvable positive would need a new blind
period.

Writes only inside experiments/wave18_deterministic_20260928/. Never touches releases/, outputs/,
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

from run import ROOT, to_matrix
import experiments.wave9_exploratory as w9
import experiments.wave14_seed_average as w14
from experiments.revalidate_fold_local import score_official

OUT = ROOT / "experiments" / "wave18_deterministic_20260928"
CACHE = OUT
W14 = w14.OUT
KEYS = ["ts_code", "trade_date"]
YEARS = (2020, 2021, 2022, 2023, 2024)
SEEDS = w14.SEEDS
BASE = w9.BASE_FEATURES
ARM_A = "bagged_085_085"
ARM_B = "deterministic_100_100"
RECIPE_B = {**w14.RECIPE, "subsample": 1.0, "colsample_bytree": 1.0}
RESOLVABILITY = {
    "criterion": "for each year and the five-year mean, report the mean paired difference B-A "
                 "across the eight seeds and its standard error (sd / sqrt(8)); resolvable when "
                 "|mean| > 2 x SE, two-sided",
    "mechanism_proof": "the between-seed sd of arm B's eight composites per year must be reported "
                       "next to arm A's; the deterministic recipe is expected to collapse it to "
                       "floating-point zero",
    "no_promotion": "all five years have been viewed repeatedly; adoption would need a new blind "
                    "period, so this round can only close or keep the idea, never adopt it",
}
PROTOCOL = {
    "experiment": "wave18_deterministic_recipe",
    "status": "exploratory_descriptive_all_years_previously_viewed",
    "arms": {
        ARM_A: {"recipe": w14.RECIPE, "source": "wave-14 frozen per-seed fits and scores"},
        ARM_B: {"recipe": RECIPE_B,
                "source": "fitted here, same eight seeds, same folds, same 63 columns, same "
                          "one-day target; only subsample and colsample_bytree differ"},
    },
    "seeds": list(SEEDS), "years": list(YEARS),
    "design": "paired by seed and year against frozen wave-14 arm A for the expected score; arm B's "
              "own between-seed sd is the mechanism measurement",
    "postprocess": "the released stack exactly, via cached_recheck.make_prediction with the frozen "
                   "pooled auxiliary at top_only 0.25, identical for both arms",
    "scorer": "the unmodified evaluate.py via revalidate_fold_local.score_official",
    "resolvability": RESOLVABILITY,
    "prior_art": {
        "experiments/refit_noise_eval/": "the noise floor this recipe change targets at its source",
        "experiments/wave14_seed_average_20260927/": "arm A and the between-seed spread",
        "experiments/wave16_seed_curve_20260928/": "averaging seeds saturates at K=8, so removing "
                                                   "the draw instead of averaging it is the only "
                                                   "variance lever left",
    },
    "harness_proofs": [
        "the frozen XGBoost reference composite is reproduced from its frozen prediction within "
        "1e-12 in every year before arm B is fitted",
        "the N-member rank average reproduces the frozen r5 xgb_two_mean raw bit-for-bit at N=2 in "
        "every year",
        "arm B fitted with seed 2026 and with seed 2027 must be bit-identical in every year; that "
        "is the determinism claim, checked before any arm-B composite is scored",
        "arm B's training frame is wave-14's exact purged one-day frame, so the only difference "
        "between the arms is the two sampling hyper-parameters",
    ],
    "prohibited": ["Adding a seed, arm or year after any score exists",
                   "Changing the recipe or the criterion after seeing a result",
                   "Presenting a resolvable positive as adoptable without a new blind period",
                   "Writing outside experiments/wave18_deterministic_20260928/",
                   "Touching releases/, outputs/, active_release.json or maintenance/"],
    "limitations": [
        "All five years have been examined repeatedly; nothing here is out-of-sample.",
        "Removing bagging changes the model's bias-variance balance, so arm B is a different model, "
        "not the same model without noise; the paired design controls the seed, not the recipe.",
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


def fit(bundle: dict, seed: int, frame: pl.DataFrame, name: str, recipe: dict) -> np.ndarray:
    path = CACHE / f"raw_{name}_seed{seed}_{bundle['year']}.parquet"
    if path.exists():
        return pl.read_parquet(path).sort("trade_date", "ts_code")["pred_raw"].to_numpy()
    import xgboost as xgb
    ordered = frame.select(KEYS + BASE + ["y_rank"]).sort("trade_date", "ts_code")
    matrix = to_matrix(ordered, BASE)
    label = ordered["y_rank"].to_numpy().astype(np.float32)
    model = xgb.XGBRegressor(**{k: v for k, v in recipe.items() if k != "n_jobs"}, seed=seed,
                             n_jobs=recipe["n_jobs"])
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


def one_day_frame(bundle: dict) -> pl.DataFrame:
    return (w9.lazy_panel()
            .filter(pl.col("is_train") & (pl.col("trade_date") < bundle["cutoff"])
                    & pl.col("y_rank").is_not_null() & pl.col("price_valid"))
            .select(KEYS + BASE + ["y_rank"]).collect())


def determinism_proof(bundle: dict, frame: pl.DataFrame) -> dict:
    first = fit(bundle, SEEDS[0], frame, ARM_B, RECIPE_B)
    second = fit(bundle, SEEDS[1], frame, ARM_B, RECIPE_B)
    if not np.array_equal(first, second):
        raise AssertionError(f"{bundle['year']}: the deterministic recipe is not deterministic "
                             f"(max abs diff {float(np.abs(first - second).max()):.3e})")
    log(f"{bundle['year']} determinism proof: seeds {SEEDS[0]} and {SEEDS[1]} are bit-identical")
    return {"seeds_compared": [SEEDS[0], SEEDS[1]], "bit_identical": True}


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
    frame = one_day_frame(bundle)
    if frame.height != bundle["train"].select(KEYS).height:
        raise AssertionError(f"{year}: arm B's frame is not wave-14's purged frame")
    w14.combination_proof(bundle, len(bundle["valid"]) // bundle["valid"]["trade_date"].n_unique())
    determinism = determinism_proof(bundle, frame)

    arm_a = read(W14 / f"year_{year}.json")
    pairs, b_composites = {}, []
    for seed in SEEDS:
        a = arm_a["singles"][str(seed)]
        raw = fit(bundle, seed, frame, ARM_B, RECIPE_B)
        metrics, daily = score_official(bundle["frame"], w14.stacked(bundle, raw))
        daily.write_csv(OUT / f"daily_{ARM_B}_seed{seed}_{year}.csv")
        b_composites.append(metrics["final_score"])
        pairs[str(seed)] = {"b_final": metrics["final_score"], "a_final": a["final_score"],
                            "delta": float(metrics["final_score"] - a["final_score"]),
                            "b_ic": metrics["ic_mean"], "b_turnover": metrics["mean_turnover"],
                            "b_excess": metrics["annual_excess"]}
        log(f"{year} seed {seed}: deterministic delta {pairs[str(seed)]['delta']:+.6f}")

    deltas = [pairs[str(seed)]["delta"] for seed in SEEDS]
    mean = float(np.mean(deltas))
    se = float(np.std(deltas, ddof=1) / np.sqrt(len(deltas)))
    a_values = [arm_a["singles"][str(s)]["final_score"] for s in SEEDS]
    record = {
        "year": year, "seconds": round(time.monotonic() - started, 2),
        "anchor_max_abs_diff": anchor, "determinism_proof": determinism,
        "arm": {"mean_delta": mean, "se": se, "t": mean / se if se else None,
                "resolvable": bool(abs(mean) > 2 * se), "per_seed_deltas": deltas,
                "mean_ic_delta": float(np.mean([pairs[str(s)]["b_ic"] for s in SEEDS])
                                       - np.mean([arm_a["singles"][str(s)]["ic_mean"]
                                                  for s in SEEDS])),
                "mean_turnover_delta": float(np.mean([pairs[str(s)]["b_turnover"] for s in SEEDS])
                                             - np.mean([arm_a["singles"][str(s)]["mean_turnover"]
                                                        for s in SEEDS])),
                "mean_excess_delta": float(np.mean([pairs[str(s)]["b_excess"] for s in SEEDS])
                                           - np.mean([arm_a["singles"][str(s)]["annual_excess"]
                                                      for s in SEEDS]))},
        "between_seed_sd": {ARM_A: float(np.std(a_values, ddof=1)),
                            ARM_B: float(np.std(b_composites, ddof=1))},
        "between_seed_range": {ARM_A: float(max(a_values) - min(a_values)),
                               ARM_B: float(max(b_composites) - min(b_composites))},
        "pairs": pairs,
    }
    log(f"{year} {ARM_B}: paired mean {mean:+.6f} +/- {se:.6f} "
        f"(t={record['arm']['t']:+.2f}, "
        f"{'resolvable' if record['arm']['resolvable'] else 'unresolvable'}); between-seed sd "
        f"{record['between_seed_sd'][ARM_B]:.2e} vs bagged {record['between_seed_sd'][ARM_A]:.6f}")
    write_new(path, record)
    del bundle, frame
    gc.collect()
    return record


def freeze() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    if (OUT / "protocol.json").exists():
        raise SystemExit("Wave-18 protocol already frozen")
    sources = [Path(__file__), Path(w9.__file__), Path(w14.__file__), w9.JOINED_PANEL,
               ROOT / "data/features.parquet", ROOT / "evaluate.py", ROOT / "run.py",
               ROOT / "src/scoring.py", ROOT / "experiments/cached_recheck.py",
               ROOT / "experiments/revalidate_fold_local.py", W14 / "protocol.json",
               ROOT / "experiments/refit_noise_eval/summary.json"]
    for year in YEARS:
        sources += [w9.R4 / f"predictions_xgboost_{year}.parquet",
                    w9.R4 / f"result_{year}.json", W14 / f"year_{year}.json"]
    payload = {**PROTOCOL, "frozen_at_local": time.strftime("%Y-%m-%dT%H:%M:%S"),
               "source_sha256": sha(Path(__file__)),
               "input_sha256": {p.relative_to(ROOT).as_posix(): sha(p)
                                for p in dict.fromkeys(sources)}}
    write_new(OUT / "protocol.json", payload)
    log(f"Froze the wave-18 protocol: {len(payload['input_sha256'])} pinned inputs, no score exists")


def verify_protocol() -> dict:
    protocol = read(OUT / "protocol.json")
    if protocol["source_sha256"] != sha(Path(__file__)):
        raise SystemExit("wave18_deterministic_recipe.py changed after its protocol was frozen")
    if protocol["seeds"] != list(SEEDS) or protocol["arms"][ARM_B]["recipe"] != RECIPE_B:
        raise SystemExit("Seeds or recipe drifted from the frozen protocol")
    for path, digest in protocol["input_sha256"].items():
        if sha(ROOT / path) != digest:
            raise SystemExit(f"Pinned input changed: {path}")
    return protocol


def summarise() -> None:
    if (OUT / "summary.json").exists():
        raise SystemExit("Summary already recorded; preserving it")
    records = [read(OUT / f"year_{year}.json") for year in YEARS]
    means = [r["arm"]["mean_delta"] for r in records]
    ses = [r["arm"]["se"] for r in records]
    pooled = float(np.mean(means))
    pooled_se = float(np.sqrt(sum(s ** 2 for s in ses)) / len(ses))
    summary = {
        "years": [r["year"] for r in records], "resolvability": RESOLVABILITY,
        "recipe_b": RECIPE_B,
        "per_year": {str(r["year"]): {"arm": r["arm"], "between_seed_sd": r["between_seed_sd"],
                                      "between_seed_range": r["between_seed_range"],
                                      "determinism_proof": r["determinism_proof"]}
                     for r in records},
        "per_year_mean_delta": means, "per_year_se": ses,
        "per_year_resolvable": [r["arm"]["resolvable"] for r in records],
        "five_year_mean_delta": pooled, "five_year_se": pooled_se,
        "five_year_t": pooled / pooled_se if pooled_se else None,
        "five_year_resolvable": bool(abs(pooled) > 2 * pooled_se),
        "mean_between_seed_sd": {ARM_A: float(np.mean([r["between_seed_sd"][ARM_A]
                                                       for r in records])),
                                 ARM_B: float(np.mean([r["between_seed_sd"][ARM_B]
                                                       for r in records]))},
        "mean_ic_delta": float(np.mean([r["arm"]["mean_ic_delta"] for r in records])),
        "mean_turnover_delta": float(np.mean([r["arm"]["mean_turnover_delta"] for r in records])),
        "mean_excess_delta": float(np.mean([r["arm"]["mean_excess_delta"] for r in records])),
        "verdict": {
            "determinism_holds": all(r["determinism_proof"]["bit_identical"] for r in records),
            "seed_variance_collapsed": bool(
                np.mean([r["between_seed_sd"][ARM_B] for r in records])
                < 0.05 * np.mean([r["between_seed_sd"][ARM_A] for r in records])),
            "resolvable_positive_five_year": bool(pooled > 2 * pooled_se),
            "resolvable_negative_2024": bool(
                records[-1]["arm"]["resolvable"] and records[-1]["arm"]["mean_delta"] < 0),
            "note": "Descriptive. No adoption follows from this round; the expected-score "
                    "comparison lives on viewed years inside the noise floor.",
        },
    }
    write_new(OUT / "summary.json", summary)
    print(f"\n{'year':<6}" + "".join(f"{y:>12}" for y in YEARS) + f"{'五年均值':>12}{'SE':>10}{'t':>7}")
    print(f"{ARM_B:<6}" + "".join(f"{m:>+12.6f}" for m in means)
          + f"{pooled:>+12.6f}{pooled_se:>10.6f}{summary['five_year_t']:>+7.2f}")
    print(f"      between-seed sd: deterministic {summary['mean_between_seed_sd'][ARM_B]:.3e} vs "
          f"bagged {summary['mean_between_seed_sd'][ARM_A]:.6f}")
    print(f"      IC {summary['mean_ic_delta']:+.6f}  turnover {summary['mean_turnover_delta']:+.6f}"
          f"  excess {summary['mean_excess_delta']:+.6f}")
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
    frame = one_day_frame(bundle)
    if frame.height != bundle["train"].select(KEYS).height:
        raise AssertionError("arm B's frame is not wave-14's purged frame")
    codes = len(bundle["valid"]) // bundle["valid"]["trade_date"].n_unique()
    w14.combination_proof(bundle, codes)
    determinism = determinism_proof(bundle, frame)
    result = {"year": year, "anchor_max_abs_diff": anchor, "determinism_proof": determinism,
              "frame_rows": frame.height, "scores_produced": 0,
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
