"""Wave-21: two deliverable, literature-motivated feature axes, paired by seed.

The web survey (2026-09-28) found two channels with external evidence and no frozen record here:
cross-stock / peer lead-lag ("Dissecting Cross-Stock Momentum", ShanghaiTech 2025 - the lead-lag
component of cross-stock momentum does not revert; "The net peer momentum effect in China") and the
Qlib-style raw-lag representation (Alpha360). A hard constraint shapes what can be tested: the raw
OHLCV panel exists only for the TRAINING file, so any feature needing raw price lags can be measured
on 2020-2024 but can NEVER be delivered on the 2025-2026 test period - that is exactly why wave-9's
extended columns were validation-only. Both axes here are therefore built **only from the 63 base
columns**, which exist on every row including the test rows, so a positive result would be
deliverable:

  W21a  PEER LEAD-LAG. Per day, assign each price-valid stock to a characteristic cell (quintile of
        RET20 x quintile of STD20, both base columns, both known at close) and compute the cell's
        ex-self mean same-day return, its one-day lag, its three-day mean, and the stock's own
        deviation from the cell mean. This is a characteristic-sorted proxy for the correlation
        clusters the peer-momentum literature uses, computable cross-sectionally with no history.
  W21b  SINGLE-DAY LAG DECOMPOSITION. The base panel carries cumulative returns RET1..RET60 but not
        the individual daily returns; each single-day return at lag k is recovered exactly as
        (1+RET_k)/(1+RET_{k-1})-1 for k in {2,3,5,10,20,60}. This gives trees direct access to the
        specific-day values that rolling windows smooth away - the part of Alpha360 that is
        recoverable without raw prices.

DESIGN. Wave-15's paired instrument against frozen wave-14 arm A (eight seeds, delivered recipe,
63 columns): each arm adds its columns and nothing else changes. Pre-declared criterion:
resolvability |mean| > 2 SE, two-sided, per year and five-year; NO promotion gate, and - unlike
wave-9 - a resolvable positive here would be *deliverable*, so it would still require a separately
frozen confirmation round on a blind period before any release.

Feature proofs before any scoring: a numpy reference for PEER_RET1 and LAGRET5 on sampled days,
100-day prefix invariance (every new column is a same-day cross-sectional statistic or a per-stock
function of base columns, so dropping history must not move it), and label-poisoning invariance.

Writes only inside experiments/wave21_peer_lags_20260928/. Never touches releases/, outputs/,
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

OUT = ROOT / "experiments" / "wave21_peer_lags_20260928"
CACHE = OUT
W14 = w14.OUT
KEYS = ["ts_code", "trade_date"]
YEARS = (2020, 2021, 2022, 2023, 2024)
SEEDS = w14.SEEDS
BASE = w9.BASE_FEATURES
PANEL = OUT / "panel_wave21.parquet"
PEER = ["PEER_RET1", "PEER_RET1_L1", "PEER_RET3", "PEER_DEV"]
LAGS = [f"LAGRET{k}" for k in (2, 3, 5, 10, 20, 60)]
ARM_A = "base63"
ARM_PEER = "base63_plus_peer"
ARM_LAG = "base63_plus_lags"
RESOLVABILITY = {
    "criterion": "for each arm, each year and the five-year mean, report the mean paired difference "
                 "B-A across the eight seeds and its standard error (sd / sqrt(8)); resolvable when "
                 "|mean| > 2 x SE, two-sided",
    "no_promotion": "all five years have been viewed repeatedly; a resolvable positive is "
                    "deliverable in principle (the columns exist on test rows) but would still "
                    "require a separately frozen confirmation on a blind period",
}
PROTOCOL = {
    "experiment": "wave21_peer_leadlag_and_lag_decomposition",
    "status": "exploratory_descriptive_all_years_previously_viewed",
    "arms": {
        ARM_A: {"features": len(BASE), "source": "wave-14 frozen per-seed fits and scores"},
        ARM_PEER: {"features": len(BASE) + len(PEER), "new": PEER,
                   "source": "fitted here, same eight seeds, folds and recipe"},
        ARM_LAG: {"features": len(BASE) + len(LAGS), "new": LAGS,
                  "source": "fitted here, same eight seeds, folds and recipe"},
    },
    "seeds": list(SEEDS), "years": list(YEARS),
    "deliverability": "every new column is a function of base columns only, which exist on the test "
                      "rows, unlike wave-9's raw-lag columns",
    "design": "paired by seed and year against frozen wave-14 arm A; eight paired replicates per "
              "arm per year",
    "postprocess": "the released stack exactly, via cached_recheck.make_prediction with the frozen "
                   "pooled auxiliary at top_only 0.25, identical for every arm",
    "scorer": "the unmodified evaluate.py via revalidate_fold_local.score_official",
    "resolvability": RESOLVABILITY,
    "prior_art": {
        "https://www.shanghaitech.edu.cn/2025/1130/c9a1117513/page.htm": "cross-stock momentum "
            "decomposes into a non-reverting lead-lag component and a reversing factor-momentum "
            "component",
        "https://mf-journal.com/article/view/347": "net peer momentum effect in China",
        "experiments/wave9_exploratory_20260927/": "engineered long-window columns; undeliverable "
                                                   "because raw prices are training-only",
        "experiments/wave15_paired_features_20260927/": "the paired instrument reused here",
    },
    "harness_proofs": [
        "a numpy reference reproduces PEER_RET1 and LAGRET5 on sampled days within 1e-9",
        "dropping the first 100 days of history leaves every new column unchanged on the overlap",
        "poisoning the label columns leaves every new column unchanged",
        "the frozen XGBoost reference composite is reproduced within 1e-12 in every year before any "
        "arm is fitted",
        "the N-member rank average reproduces the frozen r5 xgb_two_mean raw bit-for-bit at N=2",
        "re-fitting seed 2026 on the 63 base columns here reproduces wave-14's frozen raw "
        "bit-for-bit",
    ],
    "prohibited": ["Adding a seed, arm, column or year after any score exists",
                   "Changing the recipe or the criterion after seeing a result",
                   "Presenting a resolvable positive as adoptable without a blind-period "
                   "confirmation",
                   "Writing outside experiments/wave21_peer_lags_20260928/",
                   "Touching releases/, outputs/, active_release.json or maintenance/"],
    "limitations": [
        "All five years have been examined repeatedly; nothing here is out-of-sample.",
        "Characteristic cells are a proxy for correlation clusters; true peer groups would need "
        "industry codes, which the competition does not supply.",
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


def quintile(expression: pl.Expr) -> pl.Expr:
    pct = (expression.rank(method="average").over("trade_date")
           / expression.count().over("trade_date"))
    return (pct * 5).cast(pl.Int8).clip(0, 4)


def add_columns(frame: pl.DataFrame) -> pl.DataFrame:
    lag_ret = {2: "RET2", 3: "RET3", 5: "RET5", 10: "RET10", 20: "RET20", 60: "RET60"}
    previous = {2: "RET1", 3: "RET2", 5: "RET3", 10: "RET5", 20: "RET10", 60: "RET20"}
    out = frame.with_columns(
        (quintile(pl.col("RET20")) * 5 + quintile(pl.col("STD20"))).alias("_cell"))
    group = ["trade_date", "_cell"]
    cell_sum = pl.col("RET1").sum().over(group)
    cell_count = pl.col("RET1").count().over(group)
    out = out.with_columns(
        pl.when(pl.col("price_valid") & (cell_count > 1))
        .then((cell_sum - pl.col("RET1")) / (cell_count - 1)).otherwise(None).alias("PEER_RET1"))
    out = out.with_columns(
        pl.col("PEER_RET1").shift(1).over("ts_code").alias("PEER_RET1_L1"),
        pl.col("PEER_RET1").rolling_mean(3, min_samples=1).over("ts_code").alias("PEER_RET3"),
        (pl.col("RET1") - pl.col("PEER_RET1")).alias("PEER_DEV"))
    for k, column in lag_ret.items():
        out = out.with_columns(
            pl.when((1 + pl.col(previous[k])).abs() > 1e-12)
            .then((1 + pl.col(column)) / (1 + pl.col(previous[k])) - 1)
            .otherwise(None).alias(f"LAGRET{k}"))
    return out.drop("_cell")


def build_panel() -> None:
    if PANEL.exists():
        raise SystemExit("Panel already built; preserving it")
    base = pl.read_parquet(ROOT / "data/features.parquet")
    panel = add_columns(base)
    panel.write_parquet(PANEL, compression="zstd")
    log(f"Built {PANEL} with {len(PEER) + len(LAGS)} new columns on {panel.height:,} rows")


def feature_proofs() -> None:
    base = pl.read_parquet(ROOT / "data/features.parquet")
    panel = pl.read_parquet(PANEL)
    new = PEER + LAGS
    # 1. label poisoning: new columns must not read any label.
    poisoned = base.with_columns((pl.col("y_ret_1d") * 0 + 7.5).alias("y_ret_1d"),
                                 (pl.col("y_rank") * 0 + 0.25).alias("y_rank"))
    rebuilt = add_columns(poisoned)
    for column in new:
        if not panel[column].equals(rebuilt[column]):
            raise AssertionError(f"{column} reads a label column")
    # 2. prefix invariance: dropping the first 100 days must not move any new column. The lagged
    #    peer columns need their own warm-up, so compare from three days after the cut.
    days = sorted(base["trade_date"].unique().to_list())
    cut = days[100]
    compare_from = days[103]
    trimmed = add_columns(base.filter(pl.col("trade_date") >= cut))
    overlap = panel.filter(pl.col("trade_date") >= compare_from)
    worst = 0.0
    for column in new:
        left = overlap.select(KEYS + [column]).sort(KEYS)
        right = trimmed.filter(pl.col("trade_date") >= compare_from).select(KEYS + [column]).sort(KEYS)
        a = left[column].to_numpy()
        b = right[column].to_numpy()
        if not np.array_equal(np.isnan(a), np.isnan(b)):
            raise AssertionError(f"{column} changes its null pattern when history is dropped")
        finite = np.isfinite(a) & np.isfinite(b)
        if finite.any():
            worst = max(worst, float(np.abs(a[finite] - b[finite]).max()))
    # Group-aggregate window sums accumulate in chunk-dependent order, so prefix invariance holds
    # to floating-point reassociation, not bit-for-bit; 1e-12 is three orders below any score effect.
    if worst > 1e-12:
        raise AssertionError(f"prefix invariance gap {worst:.3e} exceeds 1e-12")
    # 3. numpy reference for PEER_RET1 and LAGRET5 on sampled days, valid rows only (polars ranks
    #    and counts exclude nulls, so the reference must too).
    sample = panel.filter(pl.col("trade_date").is_in(days[200:203]))
    for day in days[200:203]:
        # polars ranks and counts exclude nulls, so the reference is built on the rows where every
        # input of the peer statistic is finite.
        day_rows = (sample.filter((pl.col("trade_date") == day) & pl.col("price_valid")
                                  & pl.col("RET1").is_finite() & pl.col("RET20").is_finite()
                                  & pl.col("STD20").is_finite())
                    .sort("ts_code"))
        ret1 = day_rows["RET1"].to_numpy()
        ret20 = day_rows["RET20"].to_numpy()
        std20 = day_rows["STD20"].to_numpy()

        def quint(values: np.ndarray) -> np.ndarray:
            order = values.argsort(kind="stable")
            ranks = np.empty(len(values), dtype=np.float64)
            sorted_values = values[order]
            i = 0
            while i < len(values):
                j = i
                while j + 1 < len(values) and sorted_values[j + 1] == sorted_values[i]:
                    j += 1
                ranks[order[i:j + 1]] = (i + j + 2) / 2  # average 1-based rank
                i = j + 1
            return np.clip((ranks / len(values) * 5).astype(np.int8), 0, 4)

        cell = quint(ret20) * 5 + quint(std20)
        reference = np.full(len(ret1), np.nan)
        for c in np.unique(cell):
            members = np.flatnonzero(cell == c)
            if len(members) < 2:
                continue
            total = float(np.nansum(ret1[members]))
            count = int(np.isfinite(ret1[members]).sum())
            for i in members:
                if np.isfinite(ret1[i]) and count > 1:
                    reference[i] = (total - ret1[i]) / (count - 1)
        mine = day_rows["PEER_RET1"].to_numpy()
        mask = np.isfinite(reference) & np.isfinite(mine)
        gap = float(np.abs(reference[mask] - mine[mask]).max()) if mask.any() else 0.0
        # polars accumulates the Float32 panel columns in Float32, the reference in Float64.
        if gap > 1e-6:
            raise AssertionError(f"PEER_RET1 numpy reference gap {gap:.3e} on {day}")
        lag5 = day_rows["LAGRET5"].to_numpy()
        ref5 = (1 + day_rows["RET5"].to_numpy()) / (1 + day_rows["RET3"].to_numpy()) - 1
        ok = np.isfinite(ref5) & np.isfinite(lag5)
        if ok.any() and float(np.abs(ref5[ok] - lag5[ok]).max()) > 1e-6:
            raise AssertionError(f"LAGRET5 numpy reference gap on {day}")
    log("Feature proofs passed: label-poisoning, 100-day prefix invariance, numpy reference")
    write_new(OUT / "feature_tests.json",
              {"status": "passed", "columns": new,
               "tests": ["label_poisoning", "prefix_invariance_100_days",
                         "numpy_reference_peer_ret1_and_lagret5_on_3_days"],
               "first_day": days[0], "prefix_cut_day": cut, "compared_from": compare_from,
               "prefix_invariance_worst_gap": worst,
               "prefix_tolerance": 1e-12,
               "numpy_reference_tolerance": 1e-6,
               "numpy_tolerance_note": "polars accumulates the Float32 panel columns in Float32 "
                                       "while the numpy reference accumulates in Float64",
               "tolerance_note": "group-aggregate window sums reassociate across chunkings, so "
                                 "prefix invariance is exact to floating-point reassociation only"})


def lazy_panel() -> pl.LazyFrame:
    return pl.scan_parquet(PANEL)


def fold(year: int) -> dict:
    frame, raws, provenance = w9.load_year(year)
    valid = (lazy_panel()
             .filter(pl.col("is_train")
                     & pl.col("trade_date").is_between(year * 10000 + 101, year * 10000 + 1231))
             .select(KEYS + BASE + PEER + LAGS + ["price_valid", "y_rank"])
             .sort("trade_date", "ts_code").collect())
    if not valid.select(KEYS).equals(frame.select(KEYS)):
        raise AssertionError(f"{year}: wave-21 panel keys misaligned with the r4 fold frame")
    cutoff = provenance["boundaries"]["one_day_cutoff_exclusive"]
    train = (lazy_panel()
             .filter(pl.col("is_train") & (pl.col("trade_date") < cutoff)
                     & pl.col("y_rank").is_not_null() & pl.col("price_valid"))
             .select(KEYS + BASE + PEER + LAGS + ["y_rank"]).collect())
    return {"year": year, "frame": frame, "raws": raws, "valid": valid, "train": train,
            "cutoff": cutoff, "provenance": provenance}


def fit(bundle: dict, seed: int, features: list[str], name: str) -> np.ndarray:
    path = CACHE / f"raw_{name}_seed{seed}_{bundle['year']}.parquet"
    if path.exists():
        return pl.read_parquet(path).sort("trade_date", "ts_code")["pred_raw"].to_numpy()
    import xgboost as xgb
    ordered = bundle["train"].select(KEYS + features + ["y_rank"]).sort("trade_date", "ts_code")
    matrix = to_matrix(ordered, features)
    label = ordered["y_rank"].to_numpy().astype(np.float32)
    model = xgb.XGBRegressor(**{k: v for k, v in w14.RECIPE.items() if k != "n_jobs"}, seed=seed,
                             n_jobs=w14.RECIPE["n_jobs"])
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
    bundle = fold(year)
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
    pairs = {ARM_PEER: {}, ARM_LAG: {}}
    for seed in SEEDS:
        a = arm_a["singles"][str(seed)]
        for arm, features in ((ARM_PEER, BASE + PEER), (ARM_LAG, BASE + LAGS)):
            raw = fit(bundle, seed, features, arm)
            metrics, daily = score_official(bundle["frame"], w14.stacked(bundle, raw))
            daily.write_csv(OUT / f"daily_{arm}_seed{seed}_{year}.csv")
            pairs[arm][str(seed)] = {"b": {k: float(v) for k, v in metrics.items()},
                                     "a_final": a["final_score"],
                                     "delta": float(metrics["final_score"] - a["final_score"])}
        log(f"{year} seed {seed}: peer {pairs[ARM_PEER][str(seed)]['delta']:+.6f}, "
            f"lags {pairs[ARM_LAG][str(seed)]['delta']:+.6f}")

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
        raise SystemExit("Wave-21 protocol already frozen")
    sources = [Path(__file__), Path(w9.__file__), Path(w14.__file__), PANEL,
               ROOT / "data/features.parquet", ROOT / "evaluate.py", ROOT / "run.py",
               ROOT / "src/scoring.py", ROOT / "experiments/cached_recheck.py",
               ROOT / "experiments/revalidate_fold_local.py", W14 / "protocol.json",
               OUT / "feature_tests.json"]
    for year in YEARS:
        sources += [w9.R4 / f"predictions_xgboost_{year}.parquet",
                    w9.R4 / f"result_{year}.json", W14 / f"year_{year}.json",
                    W14 / f"raw_seed{w14.DELIVERED_SEED}_{year}.parquet"]
    payload = {**PROTOCOL, "frozen_at_local": time.strftime("%Y-%m-%dT%H:%M:%S"),
               "source_sha256": sha(Path(__file__)),
               "input_sha256": {p.relative_to(ROOT).as_posix(): sha(p)
                                for p in dict.fromkeys(sources)}}
    write_new(OUT / "protocol.json", payload)
    log(f"Froze the wave-21 protocol: {len(payload['input_sha256'])} pinned inputs, no score exists")


def verify_protocol() -> dict:
    protocol = read(OUT / "protocol.json")
    if protocol["source_sha256"] != sha(Path(__file__)):
        raise SystemExit("wave21_peer_lags.py changed after its protocol was frozen")
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
    for arm in (ARM_PEER, ARM_LAG):
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
        "note": "Descriptive. No adoption follows from this round.",
    }
    write_new(OUT / "summary.json", summary)
    print(f"\n{'arm':<22}" + "".join(f"{y:>11}" for y in YEARS) + f"{'五年均值':>11}{'SE':>9}{'t':>7}")
    for arm in (ARM_PEER, ARM_LAG):
        a = summary["arms"][arm]
        print(f"{arm:<22}" + "".join(f"{m:>+11.6f}" for m in a["per_year_mean_delta"])
              + f"{a['five_year_mean_delta']:>+11.6f}{a['five_year_se']:>9.6f}"
              f"{a['five_year_t']:>+7.2f}")
        print(f"{'':<22} IC {a['mean_ic_delta']:+.6f}  turnover {a['mean_turnover_delta']:+.6f}"
              f"  excess {a['mean_excess_delta']:+.6f}  resolvable {a['per_year_resolvable']}")
    print(f"\n判定：{json.dumps(summary['verdict'], ensure_ascii=False)}")


def selftest() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    folder = OUT / "_selftest"
    folder.mkdir(exist_ok=True)
    global CACHE
    CACHE = folder
    w9.OUT = folder
    year = 2022
    bundle = fold(year)
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
    raw = fit(bundle, w14.DELIVERED_SEED, BASE + PEER, ARM_PEER)
    result = {"year": year, "anchor_max_abs_diff": anchor,
              "peer_columns_non_null_share": {
                  column: float(bundle["valid"][column].is_not_null().mean())
                  for column in PEER},
              "lag_columns_non_null_share": {
                  column: float(bundle["valid"][column].is_not_null().mean())
                  for column in LAGS},
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
    parser.add_argument("stage", choices=("features", "proofs", "protocol", "selftest", "run"))
    arguments = parser.parse_args()
    if arguments.stage == "features":
        OUT.mkdir(parents=True, exist_ok=True)
        build_panel()
    elif arguments.stage == "proofs":
        feature_proofs()
    elif arguments.stage == "protocol":
        freeze()
    elif arguments.stage == "selftest":
        selftest()
    else:
        run()
