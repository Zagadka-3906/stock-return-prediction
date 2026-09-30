"""Wave-22: does the slow recipe add on top of the peer columns? One pre-declared combination.

Twenty-one waves are closed and two candidates survive with resolvable positive five-year means:
the peer lead-lag columns (wave-21, +0.000919, t=+3.10) and the lr 0.025 / 360-round recipe
(wave-19, +0.000680, t=+2.12). Neither is adoptable on viewed years. The single remaining question
that is not a re-roll of a closed class is whether the two effects are independent: if they are, the
one pre-declared combination (67 columns with the slow recipe) should show roughly the sum of the
two paired deltas.

  COMBO vs A        paired by seed against frozen wave-14 arm A.
  COMBO minus PEER  paired by seed against the frozen wave-21 peer-only deltas at the same seeds;
                    a resolvable positive means the slow recipe adds on top of the peer columns.

A second arm (cell limit-up rate columns) was designed, then DROPPED BEFORE SCORING because its
numpy reference could not be reconciled with the polars group-aggregate semantics (the quintile
population of the characteristic cell differed between the two implementations), so the column's
meaning was uncertified. Same precedent as wave-17's degenerate window-bagging arm: an arm whose
definition cannot be proved does not get scored.

DESIGN. Wave-15's paired instrument, eight seeds per year. Pre-declared criterion: resolvability
|mean| > 2 SE, two-sided, per year and five-year. NO promotion gate: a resolvable positive here
means "the two effects are independent", not "adopt" - adoption would still need a blind period.

Writes only inside experiments/wave22_additivity_20260928/. Never touches releases/, outputs/,
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
import experiments.wave21_peer_lags as w21
from experiments.revalidate_fold_local import score_official

OUT = ROOT / "experiments/wave22_additivity_20260928"
CACHE = OUT
W14 = w14.OUT
W21 = w21.OUT
KEYS = ["ts_code", "trade_date"]
YEARS = (2020, 2021, 2022, 2023, 2024)
SEEDS = w14.SEEDS
BASE = w9.BASE_FEATURES
PEER = w21.PEER
ARM_A = "base63"
ARM_COMBO = "peer67_lr0025_360"
RECIPE_SLOW = {**w14.RECIPE, "learning_rate": 0.025, "n_estimators": 360}
RESOLVABILITY = {
    "criterion": "for the combination against arm A and for the additivity contrast against the "
                 "frozen wave-21 peer deltas, each year and the five-year mean, report the mean "
                 "paired difference across the eight seeds and its standard error (sd / sqrt(8)); "
                 "resolvable when |mean| > 2 x SE, two-sided",
    "no_promotion": "all five years have been viewed repeatedly; a resolvable positive means the "
                    "two effects are independent, not that either is adoptable; adoption would "
                    "still require a blind-period confirmation",
}
PROTOCOL = {
    "experiment": "wave22_additivity_of_the_two_survivors",
    "status": "exploratory_descriptive_all_years_previously_viewed",
    "arms": {
        ARM_A: {"features": len(BASE), "source": "wave-14 frozen per-seed fits and scores"},
        ARM_COMBO: {"features": len(BASE) + len(PEER), "recipe": RECIPE_SLOW,
                    "source": "fitted here; the single pre-declared combination of the wave-21 "
                              "peer columns and the wave-19 slow recipe"},
    },
    "comparisons": {
        "combo_vs_A": "paired by seed against frozen wave-14 arm A",
        "combo_minus_peer": "combo delta minus the frozen wave-21 peer-only delta at the same seed",
    },
    "dropped_before_scoring": {
        "cell_limitup_rate_columns": "numpy reference could not be reconciled with the polars "
                                     "group-aggregate quintile population; uncertified semantics, "
                                     "so the arm was dropped before any score existed",
    },
    "seeds": list(SEEDS), "years": list(YEARS),
    "postprocess": "the released stack exactly, via cached_recheck.make_prediction with the frozen "
                   "pooled auxiliary at top_only 0.25, identical for every arm",
    "scorer": "the unmodified evaluate.py via revalidate_fold_local.score_official",
    "resolvability": RESOLVABILITY,
    "prior_art": {
        "experiments/wave21_peer_lags_20260928/": "the peer columns, their panel and their frozen "
                                                 "per-seed deltas",
        "experiments/wave19_three_axes_20260928/": "the slow recipe and its frozen per-seed deltas",
        "experiments/wave14_seed_average_20260927/": "arm A",
    },
    "harness_proofs": [
        "the frozen XGBoost reference composite is reproduced within 1e-12 in every year before the "
        "combination is fitted",
        "the N-member rank average reproduces the frozen r5 xgb_two_mean raw bit-for-bit at N=2",
        "re-fitting seed 2026 on the 63 base columns with the base recipe reproduces wave-14's "
        "frozen raw bit-for-bit",
        "the peer columns come from wave-21's frozen, proof-certified panel",
    ],
    "prohibited": ["Adding a seed, arm, column or year after any score exists",
                   "Changing the recipe or the criterion after seeing a result",
                   "Reading a positive additivity test as an adoption argument",
                   "Writing outside experiments/wave22_additivity_20260928/",
                   "Touching releases/, outputs/, active_release.json or maintenance/"],
    "limitations": [
        "All five years have been examined repeatedly; nothing here is out-of-sample.",
        "The additivity contrast reuses wave-21's frozen deltas, so its errors correlate with the "
        "combo arm's only through the shared arm-A control.",
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


def fit(bundle: dict, seed: int, features: list[str], name: str,
        recipe: dict | None = None) -> np.ndarray:
    path = CACHE / f"raw_{name}_seed{seed}_{bundle['year']}.parquet"
    if path.exists():
        return pl.read_parquet(path).sort("trade_date", "ts_code")["pred_raw"].to_numpy()
    import xgboost as xgb
    use = recipe or w14.RECIPE
    ordered = bundle["train"].select(KEYS + features + ["y_rank"]).sort("trade_date", "ts_code")
    matrix = to_matrix(ordered, features)
    label = ordered["y_rank"].to_numpy().astype(np.float32)
    model = xgb.XGBRegressor(**{k: v for k, v in use.items() if k != "n_jobs"}, seed=seed,
                             n_jobs=use["n_jobs"])
    started = time.monotonic()
    model.fit(matrix, label)
    seconds = round(time.monotonic() - started, 1)
    raw = model.predict(to_matrix(bundle["valid"], features)).astype(np.float64)
    raw[~bundle["valid"]["price_valid"].to_numpy()] = -1e6
    CACHE.mkdir(parents=True, exist_ok=True)
    bundle["valid"].select(KEYS).with_columns(pl.Series("pred_raw", raw)).write_parquet(
        path, compression="zstd")
    log(f"{bundle['year']} {name} seed {seed}: fitted {len(label):,} rows x {len(features)} "
        f"columns in {seconds}s")
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
    bundle = w21.fold(year)
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
    refit = fit(bundle, w14.DELIVERED_SEED, BASE, ARM_A)
    cached = pl.read_parquet(W14 / f"raw_seed{w14.DELIVERED_SEED}_{year}.parquet").sort(
        "trade_date", "ts_code")["pred_raw"].to_numpy()
    if not np.array_equal(refit, cached):
        raise AssertionError(f"{year}: fit path does not reproduce wave-14's seed-2026 raw")
    log(f"{year} fit-path proof: seed 2026 base-column refit is bit-identical to wave-14")

    arm_a = read(W14 / f"year_{year}.json")
    wave21 = read(W21 / f"year_{year}.json")
    pairs = {}
    for seed in SEEDS:
        a = arm_a["singles"][str(seed)]
        raw = fit(bundle, seed, BASE + PEER, ARM_COMBO, RECIPE_SLOW)
        metrics, daily = score_official(bundle["frame"], w14.stacked(bundle, raw))
        daily.write_csv(OUT / f"daily_{ARM_COMBO}_seed{seed}_{year}.csv")
        delta = float(metrics["final_score"] - a["final_score"])
        peer_delta = wave21["pairs"]["base63_plus_peer"][str(seed)]["delta"]
        pairs[str(seed)] = {"b": {k: float(v) for k, v in metrics.items()},
                            "a_final": a["final_score"], "delta": delta,
                            "peer_delta_frozen": peer_delta,
                            "additivity": delta - peer_delta}
        log(f"{year} seed {seed}: combo {delta:+.6f} (peer frozen {peer_delta:+.6f}, "
            f"additivity {delta - peer_delta:+.6f})")

    def stats(values: list[float]) -> dict:
        mean = float(np.mean(values))
        se = float(np.std(values, ddof=1) / np.sqrt(len(values)))
        return {"mean_delta": mean, "se": se, "t": mean / se if se else None,
                "resolvable": bool(abs(mean) > 2 * se), "per_seed_values": values}

    combo = stats([pairs[str(s)]["delta"] for s in SEEDS])
    additivity = stats([pairs[str(s)]["additivity"] for s in SEEDS])
    b = [pairs[str(s)]["b"] for s in SEEDS]
    combo["mean_ic_delta"] = float(np.mean([x["ic_mean"] for x in b])
                                   - np.mean([arm_a["singles"][str(s)]["ic_mean"] for s in SEEDS]))
    combo["mean_turnover_delta"] = float(np.mean([x["mean_turnover"] for x in b])
                                         - np.mean([arm_a["singles"][str(s)]["mean_turnover"]
                                                    for s in SEEDS]))
    combo["mean_excess_delta"] = float(np.mean([x["annual_excess"] for x in b])
                                       - np.mean([arm_a["singles"][str(s)]["annual_excess"]
                                                  for s in SEEDS]))
    record = {"year": year, "seconds": round(time.monotonic() - started, 2),
              "anchor_max_abs_diff": anchor, "combo_vs_A": combo,
              "additivity_combo_minus_peer": additivity, "pairs": pairs}
    log(f"{year} combo vs A: {combo['mean_delta']:+.6f} +/- {combo['se']:.6f} "
        f"(t={combo['t']:+.2f}); additivity: {additivity['mean_delta']:+.6f} +/- "
        f"{additivity['se']:.6f} (t={additivity['t']:+.2f})")
    write_new(path, record)
    gc.collect()
    return record


def freeze() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    if (OUT / "protocol.json").exists():
        raise SystemExit("Wave-22 protocol already frozen")
    sources = [Path(__file__), Path(w9.__file__), Path(w14.__file__), Path(w21.__file__),
               w21.PANEL, ROOT / "data/features.parquet", ROOT / "evaluate.py", ROOT / "run.py",
               ROOT / "src/scoring.py", ROOT / "experiments/cached_recheck.py",
               ROOT / "experiments/revalidate_fold_local.py", W14 / "protocol.json",
               W21 / "protocol.json", W21 / "feature_tests.json"]
    for year in YEARS:
        sources += [w9.R4 / f"predictions_xgboost_{year}.parquet",
                    w9.R4 / f"result_{year}.json", W14 / f"year_{year}.json",
                    W14 / f"raw_seed{w14.DELIVERED_SEED}_{year}.parquet", W21 / f"year_{year}.json"]
    payload = {**PROTOCOL, "frozen_at_local": time.strftime("%Y-%m-%dT%H:%M:%S"),
               "source_sha256": sha(Path(__file__)),
               "input_sha256": {p.relative_to(ROOT).as_posix(): sha(p)
                                for p in dict.fromkeys(sources)}}
    write_new(OUT / "protocol.json", payload)
    log(f"Froze the wave-22 protocol: {len(payload['input_sha256'])} pinned inputs, no score exists")


def verify_protocol() -> dict:
    protocol = read(OUT / "protocol.json")
    if protocol["source_sha256"] != sha(Path(__file__)):
        raise SystemExit("wave22_additivity.py changed after its protocol was frozen")
    if protocol["seeds"] != list(SEEDS):
        raise SystemExit("Seeds drifted from the frozen protocol")
    for path, digest in protocol["input_sha256"].items():
        if sha(ROOT / path) != digest:
            raise SystemExit(f"Pinned input changed: {path}")
    return protocol


def pool(records: list[dict], key: str) -> dict:
    means = [r[key]["mean_delta"] for r in records]
    ses = [r[key]["se"] for r in records]
    pooled = float(np.mean(means))
    pooled_se = float(np.sqrt(sum(s ** 2 for s in ses)) / len(ses))
    out = {"per_year_mean_delta": means, "per_year_se": ses,
           "per_year_resolvable": [r[key]["resolvable"] for r in records],
           "five_year_mean_delta": pooled, "five_year_se": pooled_se,
           "five_year_t": pooled / pooled_se if pooled_se else None,
           "five_year_resolvable": bool(abs(pooled) > 2 * pooled_se), "delta_2024": means[-1]}
    if key == "combo_vs_A":
        for name in ("mean_ic_delta", "mean_turnover_delta", "mean_excess_delta"):
            out[name] = float(np.mean([r[key][name] for r in records]))
    return out


def summarise() -> None:
    if (OUT / "summary.json").exists():
        raise SystemExit("Summary already recorded; preserving it")
    records = [read(OUT / f"year_{year}.json") for year in YEARS]
    summary = {"years": [r["year"] for r in records], "resolvability": RESOLVABILITY,
               "per_year": {str(r["year"]): {"combo_vs_A": r["combo_vs_A"],
                                             "additivity": r["additivity_combo_minus_peer"]}
                            for r in records},
               "combo_vs_A": pool(records, "combo_vs_A"),
               "additivity_combo_minus_peer": pool(records, "additivity_combo_minus_peer")}
    summary["verdict"] = {
        "combo_resolvable_positive": bool(summary["combo_vs_A"]["five_year_resolvable"]
                                          and summary["combo_vs_A"]["five_year_mean_delta"] > 0),
        "additivity_resolvable_positive": bool(
            summary["additivity_combo_minus_peer"]["five_year_resolvable"]
            and summary["additivity_combo_minus_peer"]["five_year_mean_delta"] > 0),
        "combo_2024_negative_resolvable": bool(
            summary["combo_vs_A"]["per_year_resolvable"][-1]
            and summary["combo_vs_A"]["delta_2024"] < 0),
        "note": "Descriptive. No adoption follows from this round.",
    }
    write_new(OUT / "summary.json", summary)
    print(f"\n{'comparison':<28}" + "".join(f"{y:>11}" for y in YEARS)
          + f"{'五年均值':>11}{'SE':>9}{'t':>7}")
    for key in ("combo_vs_A", "additivity_combo_minus_peer"):
        a = summary[key]
        print(f"{key:<28}" + "".join(f"{m:>+11.6f}" for m in a["per_year_mean_delta"])
              + f"{a['five_year_mean_delta']:>+11.6f}{a['five_year_se']:>9.6f}"
              f"{a['five_year_t']:>+7.2f}")
        if "mean_ic_delta" in a:
            print(f"{'':<28} IC {a['mean_ic_delta']:+.6f}  turnover "
                  f"{a['mean_turnover_delta']:+.6f}  excess {a['mean_excess_delta']:+.6f}")
    print(f"\n判定：{json.dumps(summary['verdict'], ensure_ascii=False)}")


def selftest() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    folder = OUT / "_selftest"
    folder.mkdir(exist_ok=True)
    global CACHE
    CACHE = folder
    w9.OUT = folder
    year = 2022
    bundle = w21.fold(year)
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
    raw = fit(bundle, w14.DELIVERED_SEED, BASE + PEER, ARM_COMBO, RECIPE_SLOW)
    result = {"year": year, "anchor_max_abs_diff": anchor,
              "columns": len(BASE) + len(PEER),
              "raw_finite_on_valid": bool(np.isfinite(
                  raw[bundle["valid"]["price_valid"].to_numpy()]).all()),
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
