"""Wave-14: seed averaging on the delivered backbone, measured as variance reduction.

WHY THIS AND NOT ANOTHER CANDIDATE. `experiments/refit_noise_eval/` established that refitting
the delivered XGBoost recipe while changing only the random seed moves the official composite
by -0.001542 (2022) and -0.001036 (2024) and replaces 26-27% of the Top decile; changing only
the thread count moved 2024 by +0.001944. Every improvement claimed in twelve rounds is smaller
than that. So further candidate search on these five years cannot resolve anything, and the only
property left that can be improved *reliably* is the variance of the deliverable itself: the
shipped model is one draw from a distribution whose spread is of the same order as the entire
search's effect sizes.

WHAT WAS ALREADY TESTED. `experiments/seed_ensemble.py` averaged three LightGBM seeds (2026, 17,
43) in both `full_signal` and `top_only` modes on 2022/2023 with a 2024 diagnostic; `top_only`
was selected and scored +0.000493 in 2024 with a paired HAC t of 1.27 and a CI crossing zero, so
it was not adopted. That round measured only the MEAN effect, on a different backbone, with three
seeds, and it never reported the across-seed spread. This round measures the spread directly, on
the delivered XGBoost backbone, with eight seeds.

TWO MECHANISMS COULD MAKE AVERAGING BETTER THAN NEUTRAL, and both are pre-declared rather than
discovered afterwards:
  * the 30% turnover term. Averaging removes idiosyncratic day-to-day rank noise, so the Top
    decile should persist more across days. Each 0.001 reduction in mean Jaccard turnover is
    worth +0.0003 composite, and this effect is systematic rather than a draw.
  * the 40% IC term, to the extent that seed noise is estimation error rather than signal.

WHAT THIS IS NOT. It is not an adoption gate and it does not claim out-of-sample evidence. The
pre-declared criteria are about variance and about score neutrality, not about beating anything:
a mean delta inside the measured noise floor is the expected, correct outcome. All five years
have been viewed repeatedly. Writes only inside experiments/wave14_seed_average_20260927/.
"""
from __future__ import annotations

import argparse
import gc
import json
import time
from itertools import combinations
from pathlib import Path

import numpy as np
import polars as pl

from run import ROOT, to_matrix
from src.scoring import Panel
import experiments.wave9_exploratory as w9
from experiments.cached_recheck import make_prediction
from experiments.revalidate_fold_local import ROUNDS, score_official

OUT = ROOT / "experiments" / "wave14_seed_average_20260927"
KEYS = ["ts_code", "trade_date"]
YEARS = (2020, 2021, 2022, 2023, 2024)
BASE = w9.BASE_FEATURES
SEEDS = (2026, 2027, 2028, 2029, 2030, 2031, 2032, 2033)
DELIVERED_SEED = 2026
SUBSET_SIZE = 4
SUBSETS = 10
SUBSET_SEED = 20260927
NOISE_FLOOR = 0.001743
RECIPE = {"n_estimators": ROUNDS, "max_depth": 7, "learning_rate": 0.05, "subsample": 0.85,
          "colsample_bytree": 0.85, "reg_lambda": 5.0, "tree_method": "hist", "device": "cuda",
          "n_jobs": 16}
CRITERIA = {
    "variance_reduction": f"sd of the {SUBSETS} pre-declared {SUBSET_SIZE}-seed average composites "
                          f"must be below 0.5 x the sd of the {len(SEEDS)} single-seed composites, "
                          "in at least four of the five years",
    "score_neutrality": f"the five-year mean of (8-seed average minus the frozen delivered "
                        f"composite) must lie inside +/- {NOISE_FLOOR}, the measured refit noise "
                        "floor; a value inside that band is the expected, correct outcome and is "
                        "recorded as neutral, not as a failure",
    "turnover": "the mean Jaccard turnover of the 8-seed average is reported against the delivered "
                "model's; a reduction is the one mechanism that could make averaging better than "
                "neutral, and it is declared here before scoring",
    "role": "descriptive variance measurement; NOT an adoption gate and not out-of-sample evidence",
}
PROTOCOL = {
    "experiment": "wave14_seed_averaging_variance_reduction",
    "status": "exploratory_descriptive_all_years_previously_viewed",
    "seeds": list(SEEDS), "delivered_seed": DELIVERED_SEED,
    "recipe": RECIPE, "combination_rule": "equal-weight cross-sectional rank average of the seed "
                                          "members' raw predictions, then the released stack with "
                                          "the frozen pooled auxiliary at top_only 0.25",
    "subsets": {"size": SUBSET_SIZE, "count": SUBSETS, "selection": "the first 10 four-seed "
                                                                    f"combinations drawn without "
                                                                    f"replacement from "
                                                                    f"np.random.default_rng("
                                                                    f"{SUBSET_SEED}) over the "
                                                                    "sorted combination list; fixed "
                                                                    "before scoring"},
    "criteria": CRITERIA, "noise_floor_reference": NOISE_FLOOR,
    "prior_art": {"experiments/seed_ensemble.py": "three LightGBM seeds (2026, 17, 43), "
                                                 "full_signal and top_only modes, selected on "
                                                 "2022/2023, 2024 diagnostic +0.000493 with paired "
                                                 "HAC t 1.27 and a CI crossing zero, not adopted; "
                                                 "measured the mean only, never the spread, and "
                                                 "never on the XGBoost backbone",
                  "experiments/refit_noise_eval/": "the noise floor this round is designed around"},
    "harness_proofs": [
        "the frozen XGBoost reference composite is reproduced from its frozen prediction within "
        "1e-12 in every year before any seed is fitted",
        "the N-member rank average used for every average in this round reproduces the frozen r5 "
        "xgb_two_mean raw bit-for-bit when applied at N=2 to the frozen xgboost and two_day "
        "members, which is what validates the generalisation",
        "the seed-2026 refit must reproduce the frozen xgboost member raw bit-for-bit in every year "
        "where that is achievable; where it is not (2020/2021, a documented provenance gap) the "
        "max |diff|, mean daily Spearman and Top-decile Jaccard against the frozen member are "
        "recorded instead of asserted",
    ],
    "prohibited": ["Adding a seed, subset or year after any score exists",
                   "Changing the recipe, the combination rule or the criteria after seeing a result",
                   "Presenting a score delta inside the noise floor as an improvement",
                   "Writing outside experiments/wave14_seed_average_20260927/",
                   "Touching releases/, outputs/, active_release.json or maintenance/"],
    "limitations": [
        "All five years have been examined repeatedly; nothing here is out-of-sample.",
        "Eight seeds bound the between-seed spread but do not estimate it to high precision.",
        "The subset averages share seeds with each other, so their spread understates the variance "
        "of independent four-seed averages.",
        "Averaging raises inference cost eight-fold, which matters for a daily production run.",
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


def fixed_subsets() -> list[tuple[int, ...]]:
    all_subsets = sorted(combinations(SEEDS, SUBSET_SIZE))
    rng = np.random.default_rng(SUBSET_SEED)
    picks = rng.choice(len(all_subsets), size=SUBSETS, replace=False)
    return [all_subsets[int(i)] for i in sorted(picks)]


def rank_average_n(raws: list[np.ndarray], valid: np.ndarray, rows_per_day: int) -> np.ndarray:
    """Equal-weight cross-sectional rank average of N members.

    w9.rank_average only accepts two members, so this generalises it. It is not taken on trust:
    every fold asserts that at N=2, applied to the frozen xgboost and two_day members, it
    reproduces the frozen r5 xgb_two_mean raw bit-for-bit.
    """
    from scipy.stats import rankdata
    shape = (-1, rows_per_day)
    arrays = [np.asarray(raw, dtype=np.float64).reshape(shape) for raw in raws]
    mask = valid.reshape(shape)
    out = np.full(mask.shape, -10.0, dtype=np.float64)
    for day in range(mask.shape[0]):
        keep = mask[day].copy()
        for array in arrays:
            keep &= np.isfinite(array[day])
        count = int(keep.sum())
        if not count:
            continue
        mixed = np.zeros(count, dtype=np.float64)
        for array in arrays:
            mixed += rankdata(array[day][keep], method="average") / count
        out[day, keep] = mixed / len(arrays)
    return out.reshape(-1)


def combination_proof(bundle: dict, rows_per_day: int) -> dict:
    """At N=2 this implementation must reproduce the frozen r5 winner exactly."""
    reference = pl.read_parquet(w9.R5 / f"predictions_xgb_two_mean_{bundle['year']}.parquet").sort(
        "trade_date", "ts_code")["pred_raw"].to_numpy().astype(np.float64)
    mine = rank_average_n([bundle["raws"]["xgboost"], bundle["raws"]["two_day"]],
                          bundle["valid"]["price_valid"].to_numpy(), rows_per_day)
    if not np.array_equal(mine, reference):
        raise AssertionError(f"{bundle['year']}: the N-member rank average does not reproduce the "
                             f"frozen xgb_two_mean raw at N=2 (max abs diff "
                             f"{float(np.abs(mine - reference).max()):.3e})")
    log(f"{bundle['year']} combination proof: N=2 reproduces the frozen xgb_two_mean raw "
        "bit-for-bit")
    return {"n2_reproduces_frozen_xgb_two_mean": True}


def fit_seed(bundle: dict, seed: int) -> np.ndarray:
    import xgboost as xgb
    frame = bundle["train"].select(KEYS + BASE + ["y_rank"]).sort("trade_date", "ts_code")
    matrix = to_matrix(frame, BASE)
    label = frame["y_rank"].to_numpy().astype(np.float32)
    model = xgb.XGBRegressor(**{k: v for k, v in RECIPE.items() if k != "n_jobs"}, seed=seed,
                             n_jobs=RECIPE["n_jobs"])
    started = time.monotonic()
    model.fit(matrix, label)
    seconds = round(time.monotonic() - started, 1)
    raw = model.predict(to_matrix(bundle["valid"], BASE)).astype(np.float64)
    raw[~bundle["valid"]["price_valid"].to_numpy()] = -1e6
    path = OUT / f"raw_seed{seed}_{bundle['year']}.parquet"
    bundle["valid"].select(KEYS).with_columns(pl.Series("pred_raw", raw)).write_parquet(
        path, compression="zstd")
    log(f"{bundle['year']} seed {seed}: fitted in {seconds}s")
    del matrix, label, model
    gc.collect()
    return raw


def stacked(bundle: dict, raw: np.ndarray) -> np.ndarray:
    panel = Panel.from_frame(bundle["frame"].with_columns(pl.Series("pred_raw", raw)))
    auxiliary = bundle["frame"]["aux_raw"].to_numpy().astype(np.float64)
    return make_prediction(panel, auxiliary, "top_only", 0.25)


def agreement(left: np.ndarray, right: np.ndarray, valid: np.ndarray, days: int) -> dict:
    from scipy.stats import spearmanr
    codes = len(valid) // days
    a, b, mask = left.reshape(days, codes), right.reshape(days, codes), valid.reshape(days, codes)
    rhos, jaccard = [], []
    for day in range(days):
        rows = np.flatnonzero(mask[day])
        rhos.append(float(spearmanr(a[day][rows], b[day][rows]).statistic))
        top = max(len(rows) // 10, 1)
        first = set(rows[np.argsort(-a[day][rows], kind="stable")[:top]])
        second = set(rows[np.argsort(-b[day][rows], kind="stable")[:top]])
        jaccard.append(len(first & second) / len(first | second))
    return {"bit_identical": bool(np.array_equal(left, right)),
            "max_abs_diff": float(np.abs(left[valid] - right[valid]).max()),
            "mean_daily_spearman": float(np.mean(rhos)),
            "min_daily_spearman": float(min(rhos)),
            "mean_top_decile_jaccard": float(np.mean(jaccard))}


def run_year(year: int) -> dict:
    path = OUT / f"year_{year}.json"
    if path.exists():
        log(f"{year} already recorded; preserving it")
        return read(path)
    started = time.monotonic()
    w9.OUT = OUT
    bundle = w9.fold(year)
    reference = w9.reference_metrics("xgboost", year)
    frozen_frame = pl.read_parquet(w9.REFERENCES["xgboost"]["predictions"]
                                   / f"predictions_xgboost_{year}.parquet").sort("trade_date", "ts_code")
    check, _ = score_official(bundle["frame"], frozen_frame["pred"].to_numpy().astype(np.float64))
    anchor = max(abs(check[k] - reference[k]) for k in reference)
    if anchor > 1e-12:
        raise AssertionError(f"{year}: frozen xgboost anchor off by {anchor:.3e}")
    log(f"{year} anchor reproduced {reference['final_score']:.15f} exactly")
    frozen_raw = bundle["raws"]["xgboost"]
    valid = bundle["valid"]["price_valid"].to_numpy()
    days = bundle["valid"]["trade_date"].n_unique()
    rows_per_day = len(valid) // days
    raws, singles = {}, {}
    for seed in SEEDS:
        raw = fit_seed(bundle, seed)
        raws[seed] = raw
        metrics, daily = score_official(bundle["frame"], stacked(bundle, raw))
        daily.write_csv(OUT / f"daily_seed{seed}_{year}.csv")
        singles[str(seed)] = {k: float(v) for k, v in metrics.items()}
        if seed == DELIVERED_SEED:
            singles[str(seed)]["agreement_with_frozen_member"] = agreement(
                raw, frozen_raw, valid, days)
    combination = combination_proof(bundle, rows_per_day)
    full = rank_average_n([raws[seed] for seed in SEEDS], valid, rows_per_day)
    full_metrics, full_daily = score_official(bundle["frame"], stacked(bundle, full))
    full_daily.write_csv(OUT / f"daily_average8_{year}.csv")
    bundle["frame"].with_columns(pl.Series("pred", stacked(bundle, full)),
                                 pl.Series("pred_raw", full)).write_parquet(
        OUT / f"predictions_average8_{year}.parquet", compression="zstd")
    subset_scores = {}
    for subset in fixed_subsets():
        average = rank_average_n([raws[seed] for seed in subset], valid, rows_per_day)
        metrics, _ = score_official(bundle["frame"], stacked(bundle, average))
        subset_scores["+".join(map(str, subset))] = float(metrics["final_score"])
    single_values = [singles[str(seed)]["final_score"] for seed in SEEDS]
    subset_values = list(subset_scores.values())
    record = {
        "year": year, "seconds": round(time.monotonic() - started, 2),
        "anchor_max_abs_diff": anchor, "combination_proof": combination,
        "delivered_composite": reference["final_score"],
        "delivered_metrics": {k: float(v) for k, v in reference.items()},
        "single_seed_composites": single_values,
        "single_seed_mean": float(np.mean(single_values)),
        "single_seed_sd": float(np.std(single_values, ddof=1)),
        "single_seed_min": float(min(single_values)), "single_seed_max": float(max(single_values)),
        "single_seed_range": float(max(single_values) - min(single_values)),
        "delivered_seed_percentile_within_refits": float(
            np.mean([v <= reference["final_score"] for v in single_values])),
        "average8_metrics": {k: float(v) for k, v in full_metrics.items()},
        "average8_minus_delivered": float(full_metrics["final_score"] - reference["final_score"]),
        "average8_minus_single_seed_mean": float(full_metrics["final_score"] - np.mean(single_values)),
        "average8_turnover_minus_delivered": float(full_metrics["mean_turnover"]
                                                   - reference["mean_turnover"]),
        "average8_ic_minus_delivered": float(full_metrics["ic_mean"] - reference["ic_mean"]),
        "average8_excess_minus_delivered": float(full_metrics["annual_excess"]
                                                 - reference["annual_excess"]),
        "subset_size": SUBSET_SIZE, "subset_count": SUBSETS,
        "subset_composites": subset_scores,
        "subset_mean": float(np.mean(subset_values)), "subset_sd": float(np.std(subset_values, ddof=1)),
        "variance_ratio_subset_over_single": float(np.std(subset_values, ddof=1)
                                                   / np.std(single_values, ddof=1)),
        "singles": singles,
    }
    log(f"{year}: single-seed composite mean {record['single_seed_mean']:.9f} sd "
        f"{record['single_seed_sd']:.6f} range {record['single_seed_range']:.6f} | 8-seed average "
        f"{full_metrics['final_score']:.9f} (vs delivered {record['average8_minus_delivered']:+.9f}, "
        f"vs single-seed mean {record['average8_minus_single_seed_mean']:+.9f}) | turnover "
        f"{record['average8_turnover_minus_delivered']:+.6f} | variance ratio "
        f"{record['variance_ratio_subset_over_single']:.3f}")
    write_new(path, record)
    del bundle, raws
    gc.collect()
    return record


def freeze() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    if (OUT / "protocol.json").exists():
        raise SystemExit("Wave-14 protocol already frozen")
    sources = [Path(__file__), Path(w9.__file__), w9.JOINED_PANEL, ROOT / "data/features.parquet",
               ROOT / "evaluate.py", ROOT / "run.py", ROOT / "src/scoring.py",
               ROOT / "experiments/cached_recheck.py", ROOT / "experiments/revalidate_fold_local.py",
               ROOT / "experiments/optimize_r5_models.py",
               ROOT / "experiments/refit_noise_eval/summary.json",
               ROOT / "experiments/seed_ensemble_eval/development.json"]
    for year in YEARS:
        sources += [w9.R4 / f"predictions_xgboost_{year}.parquet",
                    w9.R4 / f"daily_xgboost_{year}.csv", w9.R4 / f"result_{year}.json"]
    payload = {**PROTOCOL, "frozen_at_local": time.strftime("%Y-%m-%dT%H:%M:%S"),
               "source_sha256": sha(Path(__file__)), "fixed_subsets": [list(s) for s in fixed_subsets()],
               "input_sha256": {p.relative_to(ROOT).as_posix(): sha(p) for p in dict.fromkeys(sources)}}
    write_new(OUT / "protocol.json", payload)
    log(f"Froze the wave-14 protocol: {len(SEEDS)} seeds, {SUBSETS} fixed {SUBSET_SIZE}-seed subsets, "
        f"{len(payload['input_sha256'])} pinned inputs, no score exists yet")


def verify_protocol() -> dict:
    protocol = read(OUT / "protocol.json")
    if protocol["source_sha256"] != sha(Path(__file__)):
        raise SystemExit("wave14_seed_average.py changed after its protocol was frozen")
    if protocol["seeds"] != list(SEEDS) or protocol["recipe"] != RECIPE:
        raise SystemExit("Seeds or recipe drifted from the frozen protocol")
    if [list(s) for s in fixed_subsets()] != protocol["fixed_subsets"]:
        raise SystemExit("Subset selection drifted from the frozen protocol")
    for path, digest in protocol["input_sha256"].items():
        if sha(ROOT / path) != digest:
            raise SystemExit(f"Pinned input changed: {path}")
    return protocol


def run() -> None:
    verify_protocol()
    records = [run_year(year) for year in YEARS]
    if (OUT / "summary.json").exists():
        raise SystemExit("Summary already recorded; preserving it")
    deltas = [r["average8_minus_delivered"] for r in records]
    ratios = [r["variance_ratio_subset_over_single"] for r in records]
    turnover = [r["average8_turnover_minus_delivered"] for r in records]
    summary = {
        "years": [r["year"] for r in records],
        "per_year": {str(r["year"]): {
            "delivered_composite": r["delivered_composite"],
            "single_seed_mean": r["single_seed_mean"], "single_seed_sd": r["single_seed_sd"],
            "single_seed_range": r["single_seed_range"],
            "average8_composite": r["average8_metrics"]["final_score"],
            "average8_minus_delivered": r["average8_minus_delivered"],
            "average8_minus_single_seed_mean": r["average8_minus_single_seed_mean"],
            "average8_turnover_minus_delivered": r["average8_turnover_minus_delivered"],
            "average8_ic_minus_delivered": r["average8_ic_minus_delivered"],
            "subset_sd": r["subset_sd"],
            "variance_ratio_subset_over_single": r["variance_ratio_subset_over_single"],
            "delivered_seed_percentile_within_refits": r["delivered_seed_percentile_within_refits"],
            "delivered_seed_agreement": r["singles"][str(DELIVERED_SEED)].get(
                "agreement_with_frozen_member")} for r in records},
        "five_year_mean_average8_minus_delivered": float(np.mean(deltas)),
        "five_year_mean_average8_minus_single_seed_mean": float(
            np.mean([r["average8_minus_single_seed_mean"] for r in records])),
        "five_year_mean_turnover_delta": float(np.mean(turnover)),
        "mean_variance_ratio": float(np.mean(ratios)),
        "criteria": CRITERIA,
        "verdict": {
            "variance_reduction_demonstrated": bool(sum(r < 0.5 for r in ratios) >= 4),
            "score_neutral_within_noise_floor": bool(abs(float(np.mean(deltas))) <= NOISE_FLOOR),
            "noise_floor": NOISE_FLOOR,
            "turnover_reduced": bool(np.mean(turnover) < 0),
        },
        "note": "Descriptive. A delta inside the noise floor is the expected outcome and must be "
                "reported as neutral, not as an improvement or a failure.",
    }
    write_new(OUT / "summary.json", summary)
    print(f"\n{'year':<6}{'交付综合分':>14}{'8种子均值':>14}{'单种子sd':>12}{'单种子极差':>13}"
          f"{'8种子平均':>14}{'−交付':>11}{'−单种子均值':>13}{'Δ换手':>10}{'方差比':>9}")
    for year in YEARS:
        r = next(x for x in records if x["year"] == year)
        print(f"{year:<6}{r['delivered_composite']:>14.9f}{r['single_seed_mean']:>14.9f}"
              f"{r['single_seed_sd']:>12.6f}{r['single_seed_range']:>13.6f}"
              f"{r['average8_metrics']['final_score']:>14.9f}{r['average8_minus_delivered']:>+11.6f}"
              f"{r['average8_minus_single_seed_mean']:>+13.6f}"
              f"{r['average8_turnover_minus_delivered']:>+10.6f}"
              f"{r['variance_ratio_subset_over_single']:>9.3f}")
    print(f"\n五年均值：8种子平均 − 交付 {summary['five_year_mean_average8_minus_delivered']:+.6f}"
          f"（噪声地板 ±{NOISE_FLOOR}），− 单种子均值 "
          f"{summary['five_year_mean_average8_minus_single_seed_mean']:+.6f}，"
          f"Δ换手 {summary['five_year_mean_turnover_delta']:+.6f}，平均方差比 "
          f"{summary['mean_variance_ratio']:.3f}")
    print(f"判定：{json.dumps(summary['verdict'], ensure_ascii=False)}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("stage", choices=("protocol", "run"))
    arguments = parser.parse_args()
    if arguments.stage == "protocol":
        freeze()
    else:
        run()
