"""Wave-17: the one axis nothing has ever scored, measured with the only instrument that resolves.

Sixteen rounds of search carry frozen negative records, and wave-16 closed the last delivery-side
lever (the seed count). One axis remains that was never *scored*:

  BLENDED-HORIZON TARGET. `two_target = 0.5*y_rank + 0.5*y_rank.shift(-1)` per stock exists in the
  revalidation pipeline and trained the r4 `two_day` LightGBM member and wave-13's `xgb2`, but
  wave-13 was blocked at its self-proof and never produced a score, and in r4 the target only ever
  lived inside a heterogeneous ensemble whose gain wave-14's seed-average control later dissolved.
  The *standalone* delivered XGBoost recipe on the blended target has therefore never been measured.
  Its mechanism is not averaging: a two-day-blended rank is a lower-noise label and a more
  persistent list, and persistence is worth +0.0003 composite per 0.001 of Jaccard turnover — the
  one official term that is nearly saturated rather than exhausted, and the only channel through
  which a label change could still pay.

A second candidate axis, training-window bagging, was designed and then dropped *before* the
protocol freeze: the training history is only two to six years long, so "last four years" is
identical to the full history in 2020-2022 and the arm would be degenerate in exactly the years it
is meant to diversify; and wave-14's control plus wave-16's saturation already show that averaging
heterogeneous fits adds nothing resolvable on top of seed averaging.

DESIGN. Exactly wave-15's: arm A is the frozen wave-14 record (eight seeds of the delivered recipe,
63 columns, one-day target, per-seed composites hash-pinned), arm B is fitted here with the same
seeds, recipe and folds, and the paired difference per seed and year carries a standard error. The
pre-declared criterion is resolvability (|mean| > 2 SE), two-sided, per year and for the five-year
mean. There is NO promotion gate: all five years have been viewed repeatedly, so a resolvable
positive here is hypothesis-generating only and would need a new blind period, exactly as
xgb_two_mean did.

Writes only inside experiments/wave17_last_axes_20260928/. Never touches releases/, outputs/,
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

OUT = ROOT / "experiments" / "wave17_last_axes_20260928"
CACHE = OUT
W14 = w14.OUT
KEYS = ["ts_code", "trade_date"]
YEARS = (2020, 2021, 2022, 2023, 2024)
SEEDS = w14.SEEDS
BASE = w9.BASE_FEATURES
ARM_A = "base63_one_day"
ARM_B = "blended_two_day_target"
RESOLVABILITY = {
    "criterion": "for each year and the five-year mean, report the mean paired difference B-A "
                 "across the eight seeds and its standard error (sd / sqrt(8)); the effect is "
                 "called resolvable when |mean| > 2 x SE, unresolvable otherwise",
    "two_sided": True,
    "no_promotion": "all five years have been viewed repeatedly; a resolvable positive is "
                    "hypothesis-generating only and would require a new blind period before any "
                    "delivery change, exactly as xgb_two_mean did",
}
PROTOCOL = {
    "experiment": "wave17_blended_horizon_target",
    "status": "exploratory_descriptive_all_years_previously_viewed",
    "arms": {
        ARM_A: {"features": len(BASE), "target": "y_rank",
                "source": "wave-14 frozen per-seed fits and scores, hash-pinned",
                "recipe": w14.RECIPE},
        ARM_B: {"features": len(BASE), "target": "0.5*y_rank + 0.5*y_rank.shift(-1) per stock",
                "source": "fitted here, same eight seeds, same recipe, same folds, purged at the "
                          "frozen two-day cutoff so no blended label reaches into the validation "
                          "year",
                "recipe": w14.RECIPE},
    },
    "seeds": list(SEEDS), "years": list(YEARS),
    "design": "paired by seed and by year against the frozen wave-14 arm A; eight paired replicates "
              "per year",
    "postprocess": "the released stack exactly, via cached_recheck.make_prediction with the frozen "
                   "pooled auxiliary at top_only 0.25, identical for both arms",
    "scorer": "the unmodified evaluate.py via revalidate_fold_local.score_official",
    "resolvability": RESOLVABILITY,
    "prior_art": {
        "experiments/wave14_seed_average_20260927/": "arm A and the seed-averaging control",
        "experiments/wave15_paired_features_20260927/": "the paired-by-seed instrument reused here",
        "experiments/revalidate_fold_local.py": "the two-day cutoff and the two_target definition",
        "experiments/wave13_diversity.py": "fitted the blended target on XGBoost but was blocked at "
                                           "its self-proof and never scored it",
        "experiments/wave16_seed_curve_20260928/": "seed averaging saturates at K=8 and averaging "
                                                   "heterogeneous fits adds nothing resolvable, "
                                                   "which is why only a label change is left",
    },
    "harness_proofs": [
        "the frozen XGBoost reference composite is reproduced from its frozen prediction within "
        "1e-12 in every year before any arm is fitted",
        "the N-member rank average reproduces the frozen r5 xgb_two_mean raw bit-for-bit at N=2 in "
        "every year",
        "re-fitting seed 2026 on the one-day target here reproduces wave-14's frozen raw bit-for-bit "
        "in every year, which proves this round's fit path is wave-14's",
        "the blended-target training frame ends strictly before the validation year AND its label "
        "(which needs the next day's rank) is available strictly before validation begins, per the "
        "frozen r4 boundaries",
    ],
    "prohibited": ["Adding a seed, arm or year after any score exists",
                   "Changing the recipe, the target or the criterion after seeing a result",
                   "Presenting a resolvable positive as adoptable without a new blind period",
                   "Writing outside experiments/wave17_last_axes_20260928/",
                   "Touching releases/, outputs/, active_release.json or maintenance/"],
    "limitations": [
        "All five years have been examined repeatedly; nothing here is out-of-sample.",
        "Eight paired replicates resolve about 0.001; anything smaller stays unresolvable.",
        "The blended label is correlated across adjacent days, so arm B's per-seed composites are "
        "not independent of arm A's; pairing removes the shared part.",
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


def fit(bundle: dict, seed: int, frame: pl.DataFrame, target: str, name: str) -> np.ndarray:
    """One fit of the frozen delivered recipe on an arbitrary frame and label, predicted in memory
    exactly as wave-14 did, and cached so a re-run never refits."""
    path = CACHE / f"raw_{name}_seed{seed}_{bundle['year']}.parquet"
    if path.exists():
        return pl.read_parquet(path).sort("trade_date", "ts_code")["pred_raw"].to_numpy()
    import xgboost as xgb
    ordered = frame.select(KEYS + BASE + [target]).sort("trade_date", "ts_code")
    matrix = to_matrix(ordered, BASE)
    label = ordered[target].to_numpy().astype(np.float32)
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


def blended_frame(bundle: dict) -> pl.DataFrame:
    cutoff = bundle["provenance"]["boundaries"]["two_day_cutoff_exclusive"]
    return (w9.lazy_panel()
            .with_columns((0.5 * pl.col("y_rank")
                           + 0.5 * pl.col("y_rank").shift(-1).over("ts_code")).alias("two_target"))
            .filter(pl.col("is_train") & (pl.col("trade_date") < cutoff)
                    & pl.col("two_target").is_finite())
            .select(KEYS + BASE + ["two_target"]).collect())


def one_day_frame(bundle: dict) -> pl.DataFrame:
    return (w9.lazy_panel()
            .filter(pl.col("is_train") & (pl.col("trade_date") < bundle["cutoff"])
                    & pl.col("y_rank").is_not_null() & pl.col("price_valid"))
            .select(KEYS + BASE + ["y_rank"]).collect())


def causality(bundle: dict, blended: pl.DataFrame, one_day: pl.DataFrame) -> dict:
    first = int(bundle["valid"]["trade_date"].min())
    bounds = bundle["provenance"]["boundaries"]
    record = {"validation_first_date": first,
              "one_day": {"training_last_date": int(one_day["trade_date"].max()),
                          "rows": one_day.height},
              "blended": {"training_last_date": int(blended["trade_date"].max()),
                          "rows": blended.height},
              "two_day_label_available": int(bounds["two_day_label_available"])}
    for name in ("one_day", "blended"):
        if record[name]["training_last_date"] >= first:
            raise AssertionError(f"{bundle['year']} {name}: training reaches into validation")
    if record["two_day_label_available"] >= first:
        raise AssertionError(f"{bundle['year']}: the blended label is not available before "
                             "validation begins")
    return record


def proofs(bundle: dict, one_day: pl.DataFrame) -> None:
    valid = bundle["valid"]["price_valid"].to_numpy()
    days = bundle["valid"]["trade_date"].n_unique()
    codes = len(valid) // days
    w14.combination_proof(bundle, codes)
    refit = fit(bundle, w14.DELIVERED_SEED, one_day, "y_rank", ARM_A)
    cached = pl.read_parquet(W14 / f"raw_seed{w14.DELIVERED_SEED}_{bundle['year']}.parquet").sort(
        "trade_date", "ts_code")["pred_raw"].to_numpy()
    if not np.array_equal(refit, cached):
        raise AssertionError(f"{bundle['year']}: this round's fit path does not reproduce wave-14's "
                             f"seed-2026 raw bit-for-bit (max abs diff "
                             f"{float(np.abs(refit - cached).max()):.3e})")
    log(f"{bundle['year']} fit-path proof: seed 2026 one-day refit is bit-identical to wave-14's "
        "cache")


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
    one_day = one_day_frame(bundle)
    blended = blended_frame(bundle)
    isolation = causality(bundle, blended, one_day)
    proofs(bundle, one_day)

    arm_a = read(W14 / f"year_{year}.json")
    pairs = {}
    for seed in SEEDS:
        a = arm_a["singles"][str(seed)]
        raw = fit(bundle, seed, blended, "two_target", ARM_B)
        metrics, daily = score_official(bundle["frame"], w14.stacked(bundle, raw))
        daily.write_csv(OUT / f"daily_{ARM_B}_seed{seed}_{year}.csv")
        pairs[str(seed)] = {"b": {k: float(v) for k, v in metrics.items()},
                            "a_final": a["final_score"],
                            "delta": float(metrics["final_score"] - a["final_score"])}
        log(f"{year} seed {seed}: blended-target delta {pairs[str(seed)]['delta']:+.6f}")

    deltas = [pairs[str(seed)]["delta"] for seed in SEEDS]
    mean = float(np.mean(deltas))
    se = float(np.std(deltas, ddof=1) / np.sqrt(len(deltas)))
    b = [pairs[str(seed)]["b"] for seed in SEEDS]
    arm = {"mean_delta": mean, "se": se, "t": mean / se if se else None,
           "resolvable": bool(abs(mean) > 2 * se), "per_seed_deltas": deltas,
           "mean_ic_delta": float(np.mean([x["ic_mean"] for x in b])
                                  - np.mean([arm_a["singles"][str(s)]["ic_mean"] for s in SEEDS])),
           "mean_turnover_delta": float(np.mean([x["mean_turnover"] for x in b])
                                        - np.mean([arm_a["singles"][str(s)]["mean_turnover"]
                                                   for s in SEEDS])),
           "mean_excess_delta": float(np.mean([x["annual_excess"] for x in b])
                                      - np.mean([arm_a["singles"][str(s)]["annual_excess"]
                                                 for s in SEEDS]))}
    record = {"year": year, "seconds": round(time.monotonic() - started, 2),
              "anchor_max_abs_diff": anchor, "isolation": isolation, "arm": arm, "pairs": pairs}
    log(f"{year} {ARM_B}: paired mean {mean:+.6f} +/- {se:.6f} "
        f"(t={arm['t']:+.2f}, {'resolvable' if arm['resolvable'] else 'unresolvable'}); "
        f"IC {arm['mean_ic_delta']:+.6f}, turnover {arm['mean_turnover_delta']:+.6f}, "
        f"excess {arm['mean_excess_delta']:+.6f}")
    write_new(path, record)
    del bundle, one_day, blended
    gc.collect()
    return record


def freeze() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    if (OUT / "protocol.json").exists():
        raise SystemExit("Wave-17 protocol already frozen")
    sources = [Path(__file__), Path(w9.__file__), Path(w14.__file__), w9.JOINED_PANEL,
               ROOT / "data/features.parquet", ROOT / "evaluate.py", ROOT / "run.py",
               ROOT / "src/scoring.py", ROOT / "experiments/cached_recheck.py",
               ROOT / "experiments/revalidate_fold_local.py",
               ROOT / "experiments/optimize_r5_models.py", W14 / "protocol.json"]
    for year in YEARS:
        sources += [w9.R4 / f"predictions_xgboost_{year}.parquet",
                    w9.R4 / f"result_{year}.json", W14 / f"year_{year}.json",
                    W14 / f"raw_seed{w14.DELIVERED_SEED}_{year}.parquet"]
    payload = {**PROTOCOL, "frozen_at_local": time.strftime("%Y-%m-%dT%H:%M:%S"),
               "source_sha256": sha(Path(__file__)),
               "input_sha256": {p.relative_to(ROOT).as_posix(): sha(p)
                                for p in dict.fromkeys(sources)}}
    write_new(OUT / "protocol.json", payload)
    log(f"Froze the wave-17 protocol: {len(payload['input_sha256'])} pinned inputs, no score exists")


def verify_protocol() -> dict:
    protocol = read(OUT / "protocol.json")
    if protocol["source_sha256"] != sha(Path(__file__)):
        raise SystemExit("wave17_last_axes.py changed after its protocol was frozen")
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
    means = [r["arm"]["mean_delta"] for r in records]
    ses = [r["arm"]["se"] for r in records]
    pooled = float(np.mean(means))
    pooled_se = float(np.sqrt(sum(s ** 2 for s in ses)) / len(ses))
    summary = {
        "years": [r["year"] for r in records], "resolvability": RESOLVABILITY,
        "per_year": {str(r["year"]): r["arm"] for r in records},
        "per_year_mean_delta": means, "per_year_se": ses,
        "per_year_resolvable": [r["arm"]["resolvable"] for r in records],
        "five_year_mean_delta": pooled, "five_year_se": pooled_se,
        "five_year_t": pooled / pooled_se if pooled_se else None,
        "five_year_resolvable": bool(abs(pooled) > 2 * pooled_se),
        "mean_ic_delta": float(np.mean([r["arm"]["mean_ic_delta"] for r in records])),
        "mean_turnover_delta": float(np.mean([r["arm"]["mean_turnover_delta"] for r in records])),
        "mean_excess_delta": float(np.mean([r["arm"]["mean_excess_delta"] for r in records])),
        "verdict": {
            "resolvable_positive_five_year": bool(pooled > 2 * pooled_se),
            "resolvable_positive_years": [r["year"] for r in records
                                          if r["arm"]["resolvable"] and r["arm"]["mean_delta"] > 0],
            "turnover_reduced": bool(np.mean([r["arm"]["mean_turnover_delta"] for r in records])
                                     < 0),
            "note": "Descriptive. No adoption follows from this round; all five years are viewed "
                    "and a resolvable positive would need a new blind period.",
        },
    }
    write_new(OUT / "summary.json", summary)
    print(f"\n{'year':<6}" + "".join(f"{y:>12}" for y in YEARS) + f"{'五年均值':>12}{'SE':>10}{'t':>7}")
    print(f"{ARM_B:<6}" + "".join(f"{m:>+12.6f}" for m in means)
          + f"{pooled:>+12.6f}{pooled_se:>10.6f}{summary['five_year_t']:>+7.2f}")
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
    one_day = one_day_frame(bundle)
    blended = blended_frame(bundle)
    isolation = causality(bundle, blended, one_day)
    proofs(bundle, one_day)
    raw = fit(bundle, w14.DELIVERED_SEED, blended, "two_target", ARM_B)
    valid = bundle["valid"]["price_valid"].to_numpy()
    result = {"year": year, "anchor_max_abs_diff": anchor, "isolation": isolation,
              "fit_path_bit_identical_to_wave14": True, "n2_combination_proof": True,
              "blended_raw_finite_on_valid_rows": bool(np.isfinite(raw[valid]).all()),
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
