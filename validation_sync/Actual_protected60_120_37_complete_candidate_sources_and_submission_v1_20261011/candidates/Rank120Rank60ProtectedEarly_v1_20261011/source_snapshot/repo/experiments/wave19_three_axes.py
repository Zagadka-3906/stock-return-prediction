"""Wave-19: three mechanism-driven axes that nothing has ever scored, paired by seed.

Eighteen waves closed every lever class that had a frozen record, and the user asked for new
schemes again with a time budget. These three axes are not re-rolls of closed classes; each has a
distinct mechanism and has never produced a score anywhere in the repository:

  W19a  TRADABLE-ONLY RANK LABEL. The official composite scores IC over ALL labelled rows but the
        Top excess and the turnover - 60% of the weight - over `flag_limit_up == 0` rows only, while
        the delivered label `y_rank` ranks every price-valid row including the limit-up ones. The
        model therefore spends capacity ordering rows that 60% of the score ignores. Re-defining the
        label as the per-day cross-sectional percentile rank among non-limit price-valid rows, and
        dropping limit-up rows from the training frame, matches the label's row set to the majority
        of the score. Wave-11's "tradable-only" arm filtered TRAINING ROWS of a different kind
        (price-invalid) and is not this; the limit-up exploitation attempts (waves 10 and the
        diagnostics) acted on the PREDICTION side, never on the label.
  W19b  HALF LEARNING RATE, DOUBLE ROUNDS. One single pre-declared configuration
        (lr 0.025, 360 rounds, everything else identical), not a search: the standard GBDT
        generalisation direction. Wave-4 closed *hyperparameter search* because its winner did not
        transfer; a one-config hypothesis test of the shrinkage direction is a different question.
  W19c  REGIME-CONDITIONAL MODEL SWITCH ON TEST-DAY OBSERVABLES. Two fits per seed, one on the
        high-volatility half and one on the low-volatility half of the purged training days, split
        by the cross-sectional median of STD20 on each day against a threshold frozen from the
        training days only; every validation day selects its model by that day's own observable.
        No label is involved in the switch, so it is causal. Wave-12c varied member WEIGHTS by
        trailing IC, which is a different mechanism and needed labels.

DESIGN. Wave-15's paired instrument: arm A is the frozen wave-14 record (eight seeds of the
delivered recipe), each arm B is fitted here with the same seeds, folds and 63 columns, and the
paired difference per seed and year carries a standard error. Pre-declared criterion:
resolvability |mean| > 2 SE, two-sided, per year and five-year. NO promotion gate: all five years
are viewed, so a resolvable positive is hypothesis-generating only and would need a new blind
period.

Writes only inside experiments/wave19_three_axes_20260928/. Never touches releases/, outputs/,
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

OUT = ROOT / "experiments" / "wave19_three_axes_20260928"
CACHE = OUT
W14 = w14.OUT
KEYS = ["ts_code", "trade_date"]
YEARS = (2020, 2021, 2022, 2023, 2024)
SEEDS = w14.SEEDS
BASE = w9.BASE_FEATURES
ARM_A = "base63_one_day"
ARM_LABEL = "tradable_only_rank_label"
ARM_SLOW = "lr0025_rounds360"
ARM_REGIME = "regime_switch_std20"
RECIPE_SLOW = {**w14.RECIPE, "learning_rate": 0.025, "n_estimators": 360}
REGIME_COLUMN = "STD20"
RESOLVABILITY = {
    "criterion": "for each arm, each year and the five-year mean, report the mean paired difference "
                 "B-A across the eight seeds and its standard error (sd / sqrt(8)); resolvable when "
                 "|mean| > 2 x SE, two-sided",
    "no_promotion": "all five years have been viewed repeatedly; a resolvable positive is "
                    "hypothesis-generating only and would require a new blind period",
}
PROTOCOL = {
    "experiment": "wave19_three_mechanism_axes",
    "status": "exploratory_descriptive_all_years_previously_viewed",
    "arms": {
        ARM_A: {"recipe": w14.RECIPE, "target": "y_rank",
                "source": "wave-14 frozen per-seed fits and scores"},
        ARM_LABEL: {"recipe": w14.RECIPE,
                    "target": "per-day percentile rank of y_ret_1d among flag_limit_up==0 and "
                              "price_valid training rows; limit-up rows dropped from training",
                    "source": "fitted here, same eight seeds and folds"},
        ARM_SLOW: {"recipe": RECIPE_SLOW, "target": "y_rank",
                   "source": "fitted here, same eight seeds, folds and frame as arm A"},
        ARM_REGIME: {"recipe": w14.RECIPE, "target": "y_rank",
                     "source": "two fits per seed on the high/low halves of the purged training "
                               f"days split by the daily cross-sectional median of {REGIME_COLUMN} "
                               "against a threshold frozen from training days; each validation day "
                               "uses the model of its own regime"},
    },
    "seeds": list(SEEDS), "years": list(YEARS),
    "regime_rule": {"column": REGIME_COLUMN,
                    "day_statistic": "cross-sectional median over price-valid rows",
                    "threshold": "median of the daily statistic over the purged training days of "
                                 "the fold, frozen before validation",
                    "selection": "validation day d uses the high-volatility model iff its daily "
                                 "statistic exceeds the frozen threshold"},
    "design": "paired by seed and year against frozen wave-14 arm A; eight paired replicates per "
              "arm per year",
    "postprocess": "the released stack exactly, via cached_recheck.make_prediction with the frozen "
                   "pooled auxiliary at top_only 0.25, identical for every arm",
    "scorer": "the unmodified evaluate.py via revalidate_fold_local.score_official",
    "resolvability": RESOLVABILITY,
    "prior_art": {
        "experiments/wave14_seed_average_20260927/": "arm A and the seed-averaging control",
        "experiments/wave11_backbone_and_segment.py": "tradable-only TRAINING rows (a different "
                                                      "filter) and the limit-up segment model",
        "experiments/wave10_limitup_calibration.py": "prediction-side limit-up recalibration",
        "experiments/wave4 nested selection": "hyperparameter search closed for non-transfer, not "
                                              "for the shrinkage direction as a hypothesis",
        "experiments/wave12_loss_and_adaptive.py": "trailing-IC member weights, a labelled and "
                                                   "different mechanism",
    },
    "harness_proofs": [
        "the frozen XGBoost reference composite is reproduced from its frozen prediction within "
        "1e-12 in every year before any arm is fitted",
        "the N-member rank average reproduces the frozen r5 xgb_two_mean raw bit-for-bit at N=2 in "
        "every year",
        "re-fitting seed 2026 with arm A's exact recipe reproduces wave-14's frozen raw bit-for-bit "
        "in every year, which proves this round's fit path is wave-14's",
        "the tradable-only label frame contains no limit-up row and ends strictly before the "
        "validation year",
        "the regime threshold uses training days only, and both regime sub-frames end strictly "
        "before the validation year",
    ],
    "prohibited": ["Adding a seed, arm, regime threshold or year after any score exists",
                   "Changing any recipe or the criterion after seeing a result",
                   "Presenting a resolvable positive as adoptable without a new blind period",
                   "Writing outside experiments/wave19_three_axes_20260928/",
                   "Touching releases/, outputs/, active_release.json or maintenance/"],
    "limitations": [
        "All five years have been examined repeatedly; nothing here is out-of-sample.",
        "Eight paired replicates resolve about 0.001; anything smaller stays unresolvable.",
        "The tradable-only label abandons the limit-up rows that 40% of the IC term still scores, "
        "so its sign is genuinely uncertain a priori.",
        "The regime switch doubles the number of fits and halves each fit's rows, so each regime "
        "model is noisier than the single fit it replaces.",
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


def fit(bundle: dict, seed: int, frame: pl.DataFrame, target: str, name: str,
        recipe: dict | None = None) -> np.ndarray:
    path = CACHE / f"raw_{name}_seed{seed}_{bundle['year']}.parquet"
    if path.exists():
        return pl.read_parquet(path).sort("trade_date", "ts_code")["pred_raw"].to_numpy()
    import xgboost as xgb
    use = recipe or w14.RECIPE
    ordered = frame.select(KEYS + BASE + [target]).sort("trade_date", "ts_code")
    matrix = to_matrix(ordered, BASE)
    label = ordered[target].to_numpy().astype(np.float32)
    model = xgb.XGBRegressor(**{k: v for k, v in use.items() if k != "n_jobs"}, seed=seed,
                             n_jobs=use["n_jobs"])
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


def base_frame(bundle: dict) -> pl.DataFrame:
    # flag_limit_up and STD20 are already among the 63 base features, so deduplicate.
    columns = list(dict.fromkeys(KEYS + BASE + ["y_rank", "flag_limit_up", "y_ret_1d",
                                                REGIME_COLUMN]))
    return (w9.lazy_panel()
            .filter(pl.col("is_train") & (pl.col("trade_date") < bundle["cutoff"])
                    & pl.col("y_rank").is_not_null() & pl.col("price_valid"))
            .select(columns).collect())


def tradable_label_frame(frame: pl.DataFrame) -> pl.DataFrame:
    kept = frame.filter(pl.col("flag_limit_up") == 0)
    if kept.height == 0 or (kept["flag_limit_up"] != 0).any():
        raise AssertionError("Tradable-only frame is empty or still contains limit-up rows")
    return (kept.with_columns(
                (pl.col("y_ret_1d").rank(method="average").over("trade_date")
                 / pl.col("y_ret_1d").count().over("trade_date")).alias("tradable_rank"))
            .select(KEYS + BASE + ["tradable_rank"]))


def regime_split(frame: pl.DataFrame) -> tuple[pl.DataFrame, pl.DataFrame, float]:
    daily = (frame.group_by("trade_date")
             .agg(pl.col(REGIME_COLUMN).median().alias("day_stat"))
             .sort("trade_date"))
    threshold = float(daily["day_stat"].median())
    high_days = set(daily.filter(pl.col("day_stat") > threshold)["trade_date"].to_list())
    flag = pl.Series("high_regime", [d in high_days for d in frame["trade_date"].to_list()])
    return frame.with_columns(flag).filter(pl.col("high_regime")), \
        frame.with_columns(flag).filter(~pl.col("high_regime")), threshold


def regime_of_days(bundle: dict, threshold: float) -> np.ndarray:
    daily = (bundle["valid"].group_by("trade_date")
             .agg(pl.col(REGIME_COLUMN).median().alias("day_stat")).sort("trade_date"))
    high = {int(d): bool(s > threshold) for d, s in
            zip(daily["trade_date"].to_list(), daily["day_stat"].to_list())}
    return np.array([high[int(d)] for d in bundle["valid"]["trade_date"].to_numpy()])


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

    frame = base_frame(bundle)
    if frame.height != bundle["train"].select(KEYS).height:
        raise AssertionError(f"{year}: base frame is not wave-14's purged frame")
    refit = fit(bundle, w14.DELIVERED_SEED, frame.select(KEYS + BASE + ["y_rank"]), "y_rank",
                ARM_A)
    cached = pl.read_parquet(W14 / f"raw_seed{w14.DELIVERED_SEED}_{year}.parquet").sort(
        "trade_date", "ts_code")["pred_raw"].to_numpy()
    if not np.array_equal(refit, cached):
        raise AssertionError(f"{year}: fit path does not reproduce wave-14's seed-2026 raw")
    log(f"{year} fit-path proof: seed 2026 refit is bit-identical to wave-14's cache")

    label_frame = tradable_label_frame(frame)
    high_frame, low_frame, threshold = regime_split(frame)
    first = int(bundle["valid"]["trade_date"].min())
    isolation = {"validation_first_date": first, "threshold": threshold,
                 "base_last": int(frame["trade_date"].max()),
                 "label_last": int(label_frame["trade_date"].max()),
                 "high_last": int(high_frame["trade_date"].max()),
                 "low_last": int(low_frame["trade_date"].max()),
                 "high_rows": high_frame.height, "low_rows": low_frame.height,
                 "label_rows": label_frame.height}
    for name, last in (("base", isolation["base_last"]), ("label", isolation["label_last"]),
                       ("high", isolation["high_last"]), ("low", isolation["low_last"])):
        if last >= first:
            raise AssertionError(f"{year} {name}: training reaches into validation")
    regime_flag = regime_of_days(bundle, threshold)

    arm_a = read(W14 / f"year_{year}.json")
    pairs = {ARM_LABEL: {}, ARM_SLOW: {}, ARM_REGIME: {}}

    def record_pair(arm: str, seed: int, raw: np.ndarray) -> None:
        a = arm_a["singles"][str(seed)]
        metrics, daily = score_official(bundle["frame"], w14.stacked(bundle, raw))
        daily.write_csv(OUT / f"daily_{arm}_seed{seed}_{year}.csv")
        pairs[arm][str(seed)] = {"b": {k: float(v) for k, v in metrics.items()},
                                 "a_final": a["final_score"],
                                 "delta": float(metrics["final_score"] - a["final_score"])}
        log(f"{year} {arm} seed {seed}: delta {pairs[arm][str(seed)]['delta']:+.6f}")

    for seed in SEEDS:
        record_pair(ARM_LABEL, seed,
                    fit(bundle, seed, label_frame, "tradable_rank", ARM_LABEL))
        record_pair(ARM_SLOW, seed,
                    fit(bundle, seed, frame.select(KEYS + BASE + ["y_rank"]), "y_rank", ARM_SLOW,
                        RECIPE_SLOW))
        high = fit(bundle, seed, high_frame.select(KEYS + BASE + ["y_rank"]), "y_rank",
                   f"{ARM_REGIME}_high")
        low = fit(bundle, seed, low_frame.select(KEYS + BASE + ["y_rank"]), "y_rank",
                  f"{ARM_REGIME}_low")
        switched = np.where(regime_flag, high, low)
        record_pair(ARM_REGIME, seed, switched)

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
              "anchor_max_abs_diff": anchor, "isolation": isolation,
              "arms": {arm: summarise(arm) for arm in pairs}, "pairs": pairs}
    for arm in pairs:
        a = record["arms"][arm]
        log(f"{year} {arm}: paired mean {a['mean_delta']:+.6f} +/- {a['se']:.6f} "
            f"(t={a['t']:+.2f}, {'resolvable' if a['resolvable'] else 'unresolvable'}); "
            f"IC {a['mean_ic_delta']:+.6f}, turnover {a['mean_turnover_delta']:+.6f}, "
            f"excess {a['mean_excess_delta']:+.6f}")
    write_new(path, record)
    del bundle, frame, label_frame, high_frame, low_frame
    gc.collect()
    return record


def freeze() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    if (OUT / "protocol.json").exists():
        raise SystemExit("Wave-19 protocol already frozen")
    sources = [Path(__file__), Path(w9.__file__), Path(w14.__file__), w9.JOINED_PANEL,
               ROOT / "data/features.parquet", ROOT / "evaluate.py", ROOT / "run.py",
               ROOT / "src/scoring.py", ROOT / "experiments/cached_recheck.py",
               ROOT / "experiments/revalidate_fold_local.py", W14 / "protocol.json"]
    for year in YEARS:
        sources += [w9.R4 / f"predictions_xgboost_{year}.parquet",
                    w9.R4 / f"result_{year}.json", W14 / f"year_{year}.json",
                    W14 / f"raw_seed{w14.DELIVERED_SEED}_{year}.parquet"]
    payload = {**PROTOCOL, "frozen_at_local": time.strftime("%Y-%m-%dT%H:%M:%S"),
               "source_sha256": sha(Path(__file__)),
               "input_sha256": {p.relative_to(ROOT).as_posix(): sha(p)
                                for p in dict.fromkeys(sources)}}
    write_new(OUT / "protocol.json", payload)
    log(f"Froze the wave-19 protocol: {len(payload['input_sha256'])} pinned inputs, no score exists")


def verify_protocol() -> dict:
    protocol = read(OUT / "protocol.json")
    if protocol["source_sha256"] != sha(Path(__file__)):
        raise SystemExit("wave19_three_axes.py changed after its protocol was frozen")
    if protocol["seeds"] != list(SEEDS) or protocol["arms"][ARM_SLOW]["recipe"] != RECIPE_SLOW:
        raise SystemExit("Seeds or recipes drifted from the frozen protocol")
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
    for arm in (ARM_LABEL, ARM_SLOW, ARM_REGIME):
        means = [r["arms"][arm]["mean_delta"] for r in records]
        ses = [r["arms"][arm]["se"] for r in records]
        pooled = float(np.mean(means))
        pooled_se = float(np.sqrt(sum(s ** 2 for s in ses)) / len(ses))
        summary["arms"][arm] = {
            "per_year_mean_delta": means, "per_year_se": ses,
            "per_year_resolvable": [r["arms"][arm]["resolvable"] for r in records],
            "five_year_mean_delta": pooled, "five_year_se": pooled_se,
            "five_year_t": pooled / pooled_se if pooled_se else None,
            "five_year_resolvable": bool(abs(pooled) > 2 * pooled_se),
            "delta_2024": means[-1],
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
    header = f"{'arm':<26}" + "".join(f"{y:>11}" for y in YEARS) + f"{'五年均值':>11}{'SE':>9}{'t':>7}"
    print("\n" + header)
    for arm in (ARM_LABEL, ARM_SLOW, ARM_REGIME):
        a = summary["arms"][arm]
        print(f"{arm:<26}" + "".join(f"{m:>+11.6f}" for m in a["per_year_mean_delta"])
              + f"{a['five_year_mean_delta']:>+11.6f}{a['five_year_se']:>9.6f}"
              f"{a['five_year_t']:>+7.2f}")
        print(f"{'':<26} IC {a['mean_ic_delta']:+.6f}  turnover {a['mean_turnover_delta']:+.6f}"
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
    frame = base_frame(bundle)
    label_frame = tradable_label_frame(frame)
    high_frame, low_frame, threshold = regime_split(frame)
    first = int(bundle["valid"]["trade_date"].min())
    for name, sub in (("label", label_frame), ("high", high_frame), ("low", low_frame)):
        if int(sub["trade_date"].max()) >= first:
            raise AssertionError(f"{name} reaches into validation")
    regime_flag = regime_of_days(bundle, threshold)
    raw = fit(bundle, w14.DELIVERED_SEED, label_frame, "tradable_rank", ARM_LABEL)
    switched = np.where(regime_flag, raw, raw)
    result = {"year": year, "anchor_max_abs_diff": anchor,
              "threshold": threshold, "high_rows": high_frame.height,
              "low_rows": low_frame.height, "label_rows": label_frame.height,
              "high_share_of_validation_days": float(regime_flag.mean()),
              "label_range": [float(label_frame["tradable_rank"].min()),
                              float(label_frame["tradable_rank"].max())],
              "scores_produced": 0,
              "note": "no arm was scored in this stage; the only composite computed is the frozen "
                      "reference anchor, which is a published number",
              "switched_shape_ok": bool(switched.shape == raw.shape)}
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
