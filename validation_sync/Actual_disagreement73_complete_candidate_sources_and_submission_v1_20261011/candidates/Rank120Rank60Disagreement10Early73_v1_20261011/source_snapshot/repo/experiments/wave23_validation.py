"""Wave-23: validation of the DEPLOYED scheme, not a search for a new one.

The active delivery (`xgboost_peer67_r9`, submission identical to r7/r8) rests on a viewed-year
paired effect (+0.001384 +/- 0.000303, t=+4.56, wave-22). The user asked to keep testing and
validating *this* scheme and to sync the report with whatever comes out. Four validations answer
whether the deployed artifact is robust rather than lucky; none of them can select a different
model, so none of them re-opens the closed search:

  V1  SEED-SET TYPICALITY. Fit the deployed recipe (67 columns, lr 0.025/360) with sixteen seeds and
      the control recipe (63 columns, base lr) with the eight seeds wave-14 did not cover, then ask
      whether the delivered eight-seed set's advantage is a lucky draw: compare its paired delta
      against the mean and sd of twelve independent random eight-subsets of the sixteen seeds, and
      against the sixteen-seed average. Pre-declared flag: |delivered - subset mean| > 2 sd.
  V2  DAILY-LEVEL SIGNIFICANCE. The wave-22 t-statistic lives across seeds. A stricter lens pairs the
      delivered eight-seed average's DAILY official terms against the frozen wave-14 eight-seed
      average's, then applies Newey-West HAC t (lags 5/10/20) and a 20-day moving-block bootstrap
      (20000 draws) to the daily composite contributions. Descriptive: it can only downgrade or
      corroborate, never promote.
  V3  PLACEBO NEGATIVE CONTROL. Rebuild the four peer columns after jointly permuting them across
      stocks within each day (fixed rng per year, split and day), which preserves each day's
      multiset of values but destroys the cross-stock assignment. Fit the deployed recipe on
      63 + 4 placebo columns with the delivered eight seeds. Pre-declared expectation: unresolvable.
      A resolvable POSITIVE placebo would mean the wave-21/22 effect is not peer information at all
      but an artefact of adding four noisy columns, and the deployment's evidence would be void.
  V4  COVARIATE DRIFT. Standardised train-to-test mean shift and null-share shift of the four peer
      columns. Pre-declared flag: |shift| > 0.5 sd or a null-share shift above 0.05, which would mean
      the feature's meaning changes between the period it was fitted on and the period it is scored
      on.

All four are descriptive. No adoption, rejection or re-weighting follows from them except a report
revision that states whatever they show; the protocol is frozen before any score exists.

Writes only inside experiments/wave23_validation_20260928/. Never touches releases/, outputs/,
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
from experiments.final_sweep_significance import contributions, hac_t
from experiments.revalidate_fold_local import score_official

OUT = ROOT / "experiments/wave23_validation_20260928"
CACHE = OUT
W14 = w14.OUT
W21 = w21.OUT
W22 = ROOT / "experiments/wave22_additivity_20260928"
W22_COMBO_RAW = "peer67_lr0025_360"
KEYS = ["ts_code", "trade_date"]
DATE_ORDER = ["trade_date", "ts_code"]
YEARS = (2020, 2021, 2022, 2023, 2024)
DELIVERED = tuple(range(2026, 2034))
EXTRA = tuple(range(2034, 2042))
POOL16 = DELIVERED + EXTRA
BASE = w9.BASE_FEATURES
PEER = w21.PEER
RECIPE_DEPLOYED = {**w14.RECIPE, "learning_rate": 0.025, "n_estimators": 360}
SUBSETS = 12
SUBSET_SEED = 20260928
CRITERIA = {
    "v1_typicality": "flag when |delivered eight-subset delta - mean of the twelve random "
                     "eight-subset deltas| exceeds 2 x their sd; also report the sixteen-seed delta",
    "v2_daily": "report HAC t at lags 5/10/20 and the block-bootstrap CI95 and positive share of the "
                "daily paired contributions; descriptive only",
    "v3_placebo": "expected unresolvable; a resolvable positive VOIDs the peer-effect evidence and "
                  "must be reported as such",
    "v4_drift": "flag any peer column with |standardised train-to-test mean shift| > 0.5 or a "
                "null-share shift above 0.05",
    "role": "validation of the deployed scheme; no selection, no adoption, no re-weighting",
}
PROTOCOL = {
    "experiment": "wave23_validation_of_the_deployed_scheme",
    "status": "validation_descriptive_all_years_previously_viewed",
    "deployed_recipe": RECIPE_DEPLOYED,
    "deployed_features": len(BASE) + len(PEER),
    "seeds": {"delivered": list(DELIVERED), "pool16": list(POOL16)},
    "subsets": {"count": SUBSETS, "size": 8,
                "draw": f"first eight entries of np.random.default_rng({SUBSET_SEED}+year)"
                        ".permutation over the sixteen seeds, deduplicated, excluding the delivered "
                        "set"},
    "placebo": {"construction": "the four peer columns jointly permuted across stocks within each "
                                "day (days are contiguous blocks of the date-sorted frame), rng "
                                "seeded by 20260928 + year + split offset + day index; each day's "
                                "multiset of values is preserved",
                "split_offsets": {"train": 0, "valid": 100}},
    "criteria": CRITERIA,
    "prior_art": {
        "experiments/wave22_additivity_20260928/": "the deployed scheme's paired effect",
        "experiments/wave21_peer_lags_20260928/": "the peer columns and their certified panel",
        "experiments/wave14_seed_average_20260927/": "the control recipe's eight frozen seeds",
        "releases/xgboost_peer67_r9/": "the deployed artifact this round validates",
    },
    "harness_proofs": [
        "the frozen XGBoost reference composite is reproduced within 1e-12 in every year before any "
        "fit",
        "the N-member rank average reproduces the frozen r5 xgb_two_mean raw bit-for-bit at N=2",
        "the deployed recipe refit for seed 2026 reproduces wave-22's frozen combination raw "
        "bit-for-bit in every year, which ties this round to the deployed artifact",
        "the control recipe refit for seed 2026 reproduces wave-14's frozen raw bit-for-bit",
        "the placebo permutation leaves each day's sorted multiset of every peer column unchanged",
    ],
    "prohibited": ["Adding a seed, subset, year or validation after any score exists",
                   "Changing the recipe, the placebo construction or the criteria after seeing a "
                   "result",
                   "Using any validation here to select, re-weight or reject the deployed scheme",
                   "Writing outside experiments/wave23_validation_20260928/",
                   "Touching releases/, outputs/, active_release.json or maintenance/"],
    "limitations": [
        "All five years have been examined repeatedly; nothing here is out-of-sample.",
        "V2's daily pairing compares two eight-seed averages, so it carries no seed-level error bar; "
        "its HAC and bootstrap quantify day-to-day, not seed-to-seed, uncertainty.",
        "The placebo destroys peer structure but keeps column magnitudes, so it controls for "
        "regularisation, not for every artefact of adding columns.",
    ],
}


def log(message: str) -> None:
    print(f"[{time.strftime('%H:%M:%S')}] {message}", flush=True)


def fmt(value, spec: str = "+.6f") -> str:
    """Display-only helper: a degenerate statistic is None, and a log line must not crash the run."""
    return "n/a" if value is None else format(value, spec)


def sha(path) -> str:
    return w9.sha(Path(path))


def read(path) -> dict:
    return w9.read(Path(path))


def write_new(path: Path, payload) -> None:
    with Path(path).open("x", encoding="utf-8") as stream:
        json.dump(payload, stream, ensure_ascii=False, indent=2, allow_nan=False)


def subset_plan(year: int) -> list[tuple[int, ...]]:
    rng = np.random.default_rng(SUBSET_SEED + year)
    draws, seen = [], set()
    while len(draws) < SUBSETS:
        picks = rng.permutation(len(POOL16))[:8]
        subset = tuple(sorted(POOL16[int(i)] for i in picks))
        if subset not in seen and subset != DELIVERED:
            seen.add(subset)
            draws.append(subset)
    return draws


def fit_raw(bundle: dict, seed: int, train_frame: pl.DataFrame, valid_matrix: np.ndarray,
            features: list[str], name: str, recipe: dict) -> np.ndarray:
    path = CACHE / f"raw_{name}_seed{seed}_{bundle['year']}.parquet"
    if path.exists():
        return pl.read_parquet(path).sort("trade_date", "ts_code")["pred_raw"].to_numpy()
    import xgboost as xgb
    ordered = train_frame.select(KEYS + features + ["y_rank"]).sort("trade_date", "ts_code")
    matrix = to_matrix(ordered, features)
    label = ordered["y_rank"].to_numpy().astype(np.float32)
    model = xgb.XGBRegressor(**{k: v for k, v in recipe.items() if k != "n_jobs"}, seed=seed,
                             n_jobs=recipe["n_jobs"])
    started = time.monotonic()
    model.fit(matrix, label)
    seconds = round(time.monotonic() - started, 1)
    raw = model.predict(valid_matrix).astype(np.float64)
    raw[~bundle["valid"]["price_valid"].to_numpy()] = -1e6
    CACHE.mkdir(parents=True, exist_ok=True)
    bundle["valid"].select(KEYS).with_columns(pl.Series("pred_raw", raw)).write_parquet(
        path, compression="zstd")
    log(f"{bundle['year']} {name} seed {seed}: fitted {len(label):,} rows in {seconds}s")
    del matrix, label, model
    gc.collect()
    return raw


def placebo_frame(frame: pl.DataFrame, year: int, split: str) -> pl.DataFrame:
    """Jointly permute the four peer columns across the stocks of each day.

    The frame is put in date-major order first, which is the order the scorer, the caches and
    bundle['valid'] all use, so each day's rows really are contiguous and the returned frame stays
    row-aligned with the frame that gets scored. Sorting by KEYS instead would be stock-major: the
    'day blocks' would span mixed dates and the predictions would be scored against the wrong rows.
    """
    ordered = frame.sort(DATE_ORDER)
    day_ids = ordered["trade_date"].to_numpy()
    unique_days, starts = np.unique(day_ids, return_index=True)
    ends = np.append(starts[1:], len(day_ids))
    for day, start, end in zip(unique_days, starts, ends):
        if not bool((day_ids[start:end] == day).all()):
            raise AssertionError(f"day {day} is not contiguous in date-major order")
    offset = 0 if split == "train" else 100
    original = {name: ordered[name].to_numpy().astype(np.float64) for name in PEER}
    columns = {name: values.copy() for name, values in original.items()}
    for index, (start, end) in enumerate(zip(starts, ends)):
        rng = np.random.default_rng(20260928 + year + offset + int(index))
        perm = rng.permutation(end - start)
        for name in PEER:
            block = original[name][start:end]
            shuffled = block[perm]
            columns[name][start:end] = shuffled
            before = np.sort(block[~np.isnan(block)])
            after = np.sort(shuffled[~np.isnan(shuffled)])
            if not (len(before) == len(after) and np.array_equal(before, after)):
                raise AssertionError(f"placebo changed day {index}'s multiset of {name}")
    out = ordered.with_columns([pl.Series(name, values).cast(ordered.schema[name])
                                for name, values in columns.items()])
    if not out.select(KEYS).equals(ordered.select(KEYS)):
        raise AssertionError("placebo changed the row order or the key set")
    for name in PEER:
        before = np.sort(columns[name][~np.isnan(columns[name])])
        after = np.sort(original[name][~np.isnan(original[name])])
        if not (len(before) == len(after) and np.array_equal(before, after)):
            raise AssertionError(f"placebo changed the whole-split multiset of {name}")
    return out


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
    valid_matrix = to_matrix(bundle["valid"], BASE + PEER)
    base_matrix = to_matrix(bundle["valid"], BASE)

    proof = fit_raw(bundle, DELIVERED[0], bundle["train"], valid_matrix, BASE + PEER,
                    "deployed67_slow", RECIPE_DEPLOYED)
    cached = pl.read_parquet(W22 / f"raw_{W22_COMBO_RAW}_seed{DELIVERED[0]}_{year}.parquet").sort(
        "trade_date", "ts_code")["pred_raw"].to_numpy()
    if not np.array_equal(proof, cached):
        raise AssertionError(f"{year}: deployed-recipe refit does not reproduce wave-22's raw")
    control = fit_raw(bundle, DELIVERED[0], bundle["train"], base_matrix, BASE, "control63",
                      w14.RECIPE)
    cached_a = pl.read_parquet(W14 / f"raw_seed{DELIVERED[0]}_{year}.parquet").sort(
        "trade_date", "ts_code")["pred_raw"].to_numpy()
    if not np.array_equal(control, cached_a):
        raise AssertionError(f"{year}: control refit does not reproduce wave-14's raw")
    log(f"{year} harness proofs: deployed and control refits bit-identical to wave-22/wave-14")

    combo_raws, control_raws = {}, {}
    for seed in POOL16:
        combo_raws[seed] = fit_raw(bundle, seed, bundle["train"], valid_matrix, BASE + PEER,
                                   "deployed67_slow", RECIPE_DEPLOYED)
        if seed in EXTRA:
            control_raws[seed] = fit_raw(bundle, seed, bundle["train"], base_matrix, BASE,
                                         "control63", w14.RECIPE)
    for seed in DELIVERED:
        control_raws[seed] = pl.read_parquet(W14 / f"raw_seed{seed}_{year}.parquet").sort(
            "trade_date", "ts_code")["pred_raw"].to_numpy()

    def score(raw: np.ndarray, daily_name: str | None = None):
        metrics, daily = score_official(bundle["frame"], w14.stacked(bundle, raw))
        if daily_name:
            daily.write_csv(OUT / f"daily_{daily_name}_{year}.csv")
        return metrics, daily

    def average(seeds: tuple[int, ...]) -> np.ndarray:
        return w14.rank_average_n([combo_raws[s] for s in seeds], valid, codes)

    def control_average(seeds: tuple[int, ...]) -> np.ndarray:
        return w14.rank_average_n([control_raws[s] for s in seeds], valid, codes)

    arm_a = read(W14 / f"year_{year}.json")
    delivered_metrics, delivered_daily = score(average(DELIVERED), "delivered8_combo")
    full16_metrics, _ = score(average(POOL16))
    control16_metrics, _ = score(control_average(POOL16))
    subset_deltas = []
    for subset in subset_plan(year):
        metrics, _ = score(average(subset))
        control_metrics, _ = score(control_average(subset))
        subset_deltas.append(float(metrics["final_score"] - control_metrics["final_score"]))
        log(f"{year} subset {subset[0]}..{subset[-1]} delta {subset_deltas[-1]:+.6f}")
    delivered_delta = float(delivered_metrics["final_score"]
                            - arm_a["average8_metrics"]["final_score"])
    full16_delta = float(full16_metrics["final_score"] - control16_metrics["final_score"])

    placebo_train = placebo_frame(bundle["train"], year, "train")
    placebo_valid = placebo_frame(bundle["valid"], year, "valid")
    if not placebo_valid.select(KEYS).equals(bundle["valid"].select(KEYS)):
        raise AssertionError(f"{year}: placebo validation rows are not aligned with the scored rows")
    if not placebo_train.select(KEYS).equals(bundle["train"].sort(DATE_ORDER).select(KEYS)):
        raise AssertionError(f"{year}: placebo training rows changed identity")
    placebo_matrix = to_matrix(placebo_valid, BASE + PEER)
    placebo_deltas = []
    for seed in DELIVERED:
        raw = fit_raw(bundle, seed, placebo_train, placebo_matrix, BASE + PEER,
                      "placebo67_slow", RECIPE_DEPLOYED)
        metrics, _ = score(raw)
        placebo_deltas.append(float(metrics["final_score"]
                                    - arm_a["singles"][str(seed)]["final_score"]))

    drift = {}
    train_stats = bundle["train"].select(PEER)
    test_stats = bundle["valid"].filter(pl.col("price_valid")).select(PEER)
    for column in PEER:
        tr = train_stats[column].drop_nulls().to_numpy().astype(np.float64)
        te = test_stats[column].drop_nulls().to_numpy().astype(np.float64)
        sd = float(np.std(tr, ddof=1))
        drift[column] = {"train_mean": float(np.mean(tr)), "test_mean": float(np.mean(te)),
                         "standardised_shift": float((np.mean(te) - np.mean(tr)) / sd) if sd else None,
                         "train_null_share": float(1 - len(tr) / train_stats.height),
                         "test_null_share": float(1 - len(te) / test_stats.height)}

    average8_daily = pl.read_csv(W14 / f"daily_average8_{year}.csv")
    left = {n: delivered_daily[n].to_numpy() for n in ("rank_ic", "excess", "turnover")}
    right = {n: average8_daily[n].to_numpy() for n in ("rank_ic", "excess", "turnover")}
    daily_values = contributions(left, right)
    hac = {}
    for lag in (5, 10, 20):
        mean, se, statistic = hac_t(daily_values, lag)
        hac[f"lag{lag}"] = {"t": float(statistic),
                            "ci95_annual": [float((mean - 1.96 * se) * len(daily_values)),
                                            float((mean + 1.96 * se) * len(daily_values))]}
    rng = np.random.default_rng(20260928 + year)
    n, block = len(daily_values), 20
    starts = rng.integers(0, n - block + 1, size=20000)
    draws = np.array([daily_values[s:s + block].mean() for s in starts])
    bootstrap = {"block_days": block, "draws": 20000,
                 "ci95_annual": [float(np.percentile(draws, 2.5) * n),
                                 float(np.percentile(draws, 97.5) * n)],
                 "positive_share": float((draws > 0).mean())}

    sd_sub = float(np.std(subset_deltas, ddof=1))
    record = {
        "year": year, "seconds": round(time.monotonic() - started, 2),
        "anchor_max_abs_diff": anchor,
        "v1_typicality": {
            "delivered_delta": delivered_delta,
            "subset_deltas": subset_deltas, "subset_mean": float(np.mean(subset_deltas)),
            "subset_sd": sd_sub,
            "delivered_z": float((delivered_delta - np.mean(subset_deltas)) / sd_sub) if sd_sub
            else None,
            "flag": bool(abs(delivered_delta - np.mean(subset_deltas)) > 2 * sd_sub),
            "full16_delta": full16_delta,
        },
        "v2_daily": {"hac": hac, "bootstrap": bootstrap,
                     "daily_mean_contribution": float(daily_values.mean()),
                     "days": int(len(daily_values))},
        "v3_placebo": {"per_seed_deltas": placebo_deltas,
                       "mean_delta": float(np.mean(placebo_deltas)),
                       "se": float(np.std(placebo_deltas, ddof=1) / np.sqrt(len(placebo_deltas))),
                       "resolvable": bool(abs(np.mean(placebo_deltas))
                                          > 2 * np.std(placebo_deltas, ddof=1)
                                          / np.sqrt(len(placebo_deltas)))},
        "v4_drift": drift,
        "delivered8_metrics": {k: float(v) for k, v in delivered_metrics.items()},
    }
    v1, v3 = record["v1_typicality"], record["v3_placebo"]
    log(f"{year} V1 delivered8 {fmt(v1['delivered_delta'])} vs subset mean "
        f"{fmt(v1['subset_mean'])} +/- {fmt(v1['subset_sd'], '.6f')} "
        f"(z={fmt(v1['delivered_z'], '+.2f')}, flag={v1['flag']}), full16 "
        f"{fmt(v1['full16_delta'])}")
    log(f"{year} V2 HAC t " + " ".join(f"{k}:{v['t']:+.2f}" for k, v in hac.items())
        + f" bootstrap positive share {bootstrap['positive_share']:.3f}")
    log(f"{year} V3 placebo {v3['mean_delta']:+.6f} +/- {v3['se']:.6f} "
        f"({'resolvable' if v3['resolvable'] else 'unresolvable'})")
    log(f"{year} V4 drift " + " ".join(f"{c}:{fmt(v['standardised_shift'], '+.2f')}"
                                       for c, v in drift.items()))
    write_new(path, record)
    del bundle, combo_raws, control_raws
    gc.collect()
    return record


def freeze() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    if (OUT / "protocol.json").exists():
        raise SystemExit("Wave-23 protocol already frozen")
    sources = [Path(__file__), Path(w9.__file__), Path(w14.__file__), Path(w21.__file__),
               w21.PANEL, ROOT / "data/features.parquet", ROOT / "evaluate.py", ROOT / "run.py",
               ROOT / "src/scoring.py", ROOT / "experiments/cached_recheck.py",
               ROOT / "experiments/revalidate_fold_local.py", W14 / "protocol.json",
               W21 / "protocol.json", W22 / "protocol.json"]
    for year in YEARS:
        sources += [w9.R4 / f"predictions_xgboost_{year}.parquet", W14 / f"year_{year}.json",
                    W14 / f"daily_average8_{year}.csv",
                    W14 / f"raw_seed{w14.DELIVERED_SEED}_{year}.parquet",
                    W22 / f"year_{year}.json",
                    W22 / f"raw_{W22_COMBO_RAW}_seed{w14.DELIVERED_SEED}_{year}.parquet"]
    payload = {**PROTOCOL, "frozen_at_local": time.strftime("%Y-%m-%dT%H:%M:%S"),
               "source_sha256": sha(Path(__file__)),
               "fixed_subsets": {str(y): [list(s) for s in subset_plan(y)] for y in YEARS},
               "input_sha256": {p.relative_to(ROOT).as_posix(): sha(p)
                                for p in dict.fromkeys(sources)}}
    write_new(OUT / "protocol.json", payload)
    log(f"Froze the wave-23 protocol: {len(payload['input_sha256'])} pinned inputs, no score exists")


def verify_protocol() -> dict:
    protocol = read(OUT / "protocol.json")
    if protocol["source_sha256"] != sha(Path(__file__)):
        raise SystemExit("wave23_validation.py changed after its protocol was frozen")
    if protocol["deployed_recipe"] != RECIPE_DEPLOYED:
        raise SystemExit("Recipe drifted from the frozen protocol")
    if protocol["fixed_subsets"] != {str(y): [list(s) for s in subset_plan(y)] for y in YEARS}:
        raise SystemExit("Subset plan drifted from the frozen protocol")
    for path, digest in protocol["input_sha256"].items():
        if sha(ROOT / path) != digest:
            raise SystemExit(f"Pinned input changed: {path}")
    return protocol


def summarise() -> None:
    if (OUT / "summary.json").exists():
        raise SystemExit("Summary already recorded; preserving it")
    records = [read(OUT / f"year_{year}.json") for year in YEARS]
    v1 = [r["v1_typicality"] for r in records]
    v3 = [r["v3_placebo"] for r in records]
    placebo_mean = float(np.mean([v["mean_delta"] for v in v3]))
    placebo_se = float(np.sqrt(sum(v["se"] ** 2 for v in v3)) / len(v3))

    def drift_flags(record: dict) -> list:
        return [[record["year"], c] for c, v in record["v4_drift"].items()
                if (v["standardised_shift"] is not None and abs(v["standardised_shift"]) > 0.5)
                or abs(v["test_null_share"] - v["train_null_share"]) > 0.05]

    summary = {
        "years": [r["year"] for r in records], "criteria": CRITERIA,
        "v1_typicality": {
            "delivered8_delta_per_year": [v["delivered_delta"] for v in v1],
            "subset_mean_per_year": [v["subset_mean"] for v in v1],
            "subset_sd_per_year": [v["subset_sd"] for v in v1],
            "delivered_z_per_year": [v["delivered_z"] for v in v1],
            "flagged_years": [r["year"] for r, v in zip(records, v1) if v["flag"]],
            "full16_delta_per_year": [v["full16_delta"] for v in v1],
            "five_year_delivered8": float(np.mean([v["delivered_delta"] for v in v1])),
            "five_year_subset_mean": float(np.mean([v["subset_mean"] for v in v1])),
            "five_year_full16": float(np.mean([v["full16_delta"] for v in v1])),
        },
        "v2_daily": {str(r["year"]): r["v2_daily"] for r in records},
        "v3_placebo": {
            "per_year_mean_delta": [v["mean_delta"] for v in v3],
            "five_year_mean_delta": placebo_mean, "five_year_se": placebo_se,
            "five_year_t": placebo_mean / placebo_se if placebo_se else None,
            "resolvable_positive": bool(placebo_mean > 2 * placebo_se),
        },
        "v4_drift": {str(r["year"]): r["v4_drift"] for r in records},
        "v4_flagged": [flag for r in records for flag in drift_flags(r)],
        "verdict": {
            "delivered_set_typical": not any(v["flag"] for v in v1),
            "placebo_null_confirmed": not (placebo_mean > 2 * placebo_se),
            "drift_flagged": [flag for r in records for flag in drift_flags(r)],
            "note": "Validation of the deployed scheme. No selection or adoption follows; the "
                    "report revision states whatever these show.",
        },
    }
    write_new(OUT / "summary.json", summary)
    print("\nV1 delivered8 vs subset mean (per year):")
    for r, v in zip(records, v1):
        print(f"  {r['year']}: delivered {fmt(v['delivered_delta'])}, subset mean "
              f"{fmt(v['subset_mean'])} +/- {fmt(v['subset_sd'], '.6f')}, "
              f"z={fmt(v['delivered_z'], '+.2f')}, full16 {fmt(v['full16_delta'])}")
    print("V2 HAC t per year: " + "; ".join(
        f"{r['year']}: " + "/".join(f"{v['t']:+.2f}" for v in r['v2_daily']['hac'].values())
        + f" boot+{r['v2_daily']['bootstrap']['positive_share']:.2f}" for r in records))
    print(f"V3 placebo five-year {placebo_mean:+.6f} +/- {placebo_se:.6f} "
          f"(t={fmt(summary['v3_placebo']['five_year_t'], '+.2f')})")
    print(f"V4 flagged: {summary['v4_flagged']}")
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
    valid_matrix = to_matrix(bundle["valid"], BASE + PEER)
    proof = fit_raw(bundle, DELIVERED[0], bundle["train"], valid_matrix, BASE + PEER,
                    "deployed67_slow", RECIPE_DEPLOYED)
    cached = pl.read_parquet(W22 / f"raw_{W22_COMBO_RAW}_seed{DELIVERED[0]}_{year}.parquet").sort(
        "trade_date", "ts_code")["pred_raw"].to_numpy()
    if not np.array_equal(proof, cached):
        raise AssertionError("deployed-recipe refit does not reproduce wave-22's raw")
    placebo_valid = placebo_frame(bundle["valid"], year, "valid")
    if not placebo_valid.select(KEYS).equals(bundle["valid"].select(KEYS)):
        raise AssertionError("placebo validation rows are not aligned with the scored rows")

    def day_multisets(source: pl.DataFrame, name: str) -> list[tuple[np.ndarray, int]]:
        """Per-day sorted finite values plus a missing count. The permutation turns polars nulls
        into NaN, and the two representations sort to opposite ends, so a plain sorted-list compare
        would report a difference where the multiset is identical."""
        grouped = (source.group_by("trade_date").agg(pl.col(name).alias("v")).sort("trade_date")
                   ["v"].to_list())
        out = []
        for values in grouped:
            array = np.asarray([np.nan if value is None else float(value) for value in values],
                               dtype=np.float64)
            out.append((np.sort(array[~np.isnan(array)]), int(np.isnan(array).sum())))
        return out

    for name in PEER:
        before = day_multisets(bundle["valid"], name)
        after = day_multisets(placebo_valid, name)
        if len(before) != len(after) or not all(
                count_before == count_after and np.array_equal(values_before, values_after)
                for (values_before, count_before), (values_after, count_after)
                in zip(before, after)):
            raise AssertionError(f"placebo moved {name} across days")
    moved = float((placebo_valid[PEER[0]] != bundle["valid"][PEER[0]]).fill_null(False).mean())
    if moved < 0.5:
        raise AssertionError(f"placebo barely permuted {PEER[0]}: only {moved:.3f} of rows moved")
    subsets = subset_plan(year)
    result = {"year": year, "anchor_max_abs_diff": anchor,
              "deployed_refit_bit_identical_to_wave22": True,
              "placebo_multiset_preserved": True, "subset_count": len(subsets),
              "subset_disjoint_from_delivered": all(set(s) != set(DELIVERED) for s in subsets),
              "placebo_row_aligned_with_scored_frame": True,
              "placebo_within_day_verified_by_independent_group_by": True,
              "placebo_share_of_rows_moved": round(moved, 4),
              "scores_produced": 0,
              "note": "no validation was scored in this stage; the only composite computed is the "
                      "frozen reference anchor, which is a published number"}
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
