"""Wave-16: how much variance does seed averaging actually remove, as a function of K?

WHY. The delivered artifact `releases/xgboost_seed8_r6` is the equal-weight per-day cross-sectional
rank average of eight XGBoost fits that differ only in their random seed. Its stated claim is
*variance reduction, not alpha*. That claim currently rests on one number per year: the sd of ten
four-seed averages divided by the sd of the eight single-seed composites, 0.465-0.788 (mean 0.649).
Under an independent-seed model the ratio at K=4 would be 1/sqrt(4) = 0.5, so the measured value is
30% above it — but wave-14 drew its ten subsets as `sorted(combinations(...))[picks]`, which means
**every one of the ten contains seed 2026 or seed 2028**, and its own limitations list records that
overlapping subsets understate the spread. Ten correlated draws give an sd whose relative standard
error is at least 1/sqrt(2*9) = 24%. The 30% excess is therefore not distinguishable from zero, and
neither is the 1/sqrt(K) extrapolation that would justify moving from eight seeds to thirty-two.

The user asked to raise K from 8 to 16 or 32 on the expectation that the score is unchanged and the
variance falls further. This round measures whether it does, with an instrument that can answer it:
32 seeds per year, 60 independent uniform random K-subsets per K in {2,4,8,16}, the disjoint
partitions at K=8 and K=16 as a second estimator, and the exact K=1 and K=32 endpoints.

WHAT IS AND IS NOT UNCERTAIN. Within one validation year the only thing that varies across these
fits is the seed, so the 32 single-seed composites are exchangeable draws and the quantity of
interest is "if a different set of K seeds had been chosen, how far would the official composite
move" — the across-subset sd. Two things stop that sd from falling as 1/sqrt(K): drawing K of the 32
without replacement shrinks it by sqrt((N-K)/N), which is corrected analytically, and the official
composite is a NONLINEAR functional of the averaged prediction (rank IC, a Top-decile excess and a
Jaccard turnover), so the composite of a K-seed average is not the average of the K composites. The
second effect is real and is what the fitted parameter below captures; it is not a correlation
between seeds, because there is none.

PRE-DECLARED DECISION RULE FOR K. Written before any subset is scored, and it can only choose
among 8 (no new release), 16 and 32. Nothing here is an adoption gate for accuracy, and no score
delta inside the +/-0.001743 refit noise floor may be described as an improvement.

Writes only inside experiments/wave16_seed_curve_20260928/. Never touches releases/, outputs/,
active_release.json or maintenance/.
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

from run import ROOT
import experiments.wave9_exploratory as w9
import experiments.wave14_seed_average as w14
from experiments.revalidate_fold_local import score_official

OUT = ROOT / "experiments" / "wave16_seed_curve_20260928"
W14 = w14.OUT
KEYS = ["ts_code", "trade_date"]
YEARS = (2020, 2021, 2022, 2023, 2024)
SEEDS = tuple(range(2026, 2058))
POOL = len(SEEDS)
OVERLAPPING = tuple(w14.SEEDS)
K_GRID = (2, 4, 8, 16)
SUBSETS_PER_K = 60
DISJOINT_K = (8, 16)
NESTED = {8: tuple(SEEDS[:8]), 16: tuple(SEEDS[:16])}
SUBSET_SEED = 20260928
NOISE_FLOOR = 0.001743
RECIPE = w14.RECIPE
CRITERIA = {
    "estimator": "for each year and each K in {1,2,4,8,16}: the sd of the official composite over "
                 f"{SUBSETS_PER_K} independent uniform random K-subsets of the {POOL}-seed pool, "
                 "plus the exact endpoints K=1 (all 32 single-seed composites) and K=32 (the single "
                 "full-pool average), plus the disjoint partitions of the pool at K=8 and K=16 as a "
                 "second, mutually independent estimator",
    "finite_population_correction": "a K-subset drawn without replacement from N=32 has variance "
                                    "(1/K)(1-K/N) of the pool variance, so the infinite-population "
                                    "sd is sd_measured / sqrt((N-K)/N); both are reported and the "
                                    "corrected value is what the decision rule uses",
    "intraclass_model": "sd_inf(K)^2 / sd_inf(1)^2 = rho_eff * (1 - 1/K) + 1/K, with rho_eff "
                        "fitted by no-intercept least squares over K in {2,4,8,16} on the corrected "
                        "ratios; rho_eff is an EFFECTIVE NONLINEARITY parameter of the composite "
                        "functional, not a correlation between seeds (within a year the fits are "
                        "independent draws, for which rho_eff would be 0 and the decay exactly "
                        "1/sqrt(K)); K=32 is projected from that fit because a 32-subset of a "
                        "32-seed pool is unique and has no spread to measure",
    "k_decision_rule": "K_delivery = 32 if projected sd_inf(32) <= 0.90 x mean-over-years sd_inf(16); "
                       "else K_delivery = 16 if mean sd_inf(16) <= 0.90 x mean sd_inf(8); else "
                       "K_delivery = 8 and NO new release is published, the finding being that "
                       "averaging has already saturated",
    "score_neutrality": f"the five-year mean of composite(K_delivery subset) minus the five-year "
                        f"mean of the frozen wave-14 eight-seed average must lie inside +/- "
                        f"{NOISE_FLOOR}; a value inside that band is the expected, correct outcome "
                        "and is recorded as neutral, never as an improvement",
    "role": "descriptive variance measurement on five previously viewed years; NOT an adoption gate "
            "and not out-of-sample evidence",
}
PROTOCOL = {
    "experiment": "wave16_seed_count_variance_curve",
    "status": "exploratory_descriptive_all_years_previously_viewed",
    "seeds": list(SEEDS), "pool_size": POOL,
    "overlapping_seeds_with_wave14": list(OVERLAPPING),
    "recipe": RECIPE, "years": list(YEARS),
    "combination_rule": "equal-weight per-day cross-sectional rank average of the members' raw "
                        "predictions, then the released stack with the frozen pooled auxiliary at "
                        "top_only 0.25 — the rule whose N=2 case reproduces the frozen r5 "
                        "xgb_two_mean raw bit-for-bit, re-proved here in every year",
    "scorer": "the unmodified evaluate.py via revalidate_fold_local.score_official",
    "subsets": {"per_k": SUBSETS_PER_K, "k_grid": list(K_GRID),
                "selection": "for each K in ascending order, draw independent uniform random "
                             "K-subsets by taking the first K entries of np.random.default_rng("
                             f"{SUBSET_SEED}).permutation over the 32 seeds, deduplicated, until "
                             f"{SUBSETS_PER_K} distinct subsets exist; the disjoint partitions at "
                             "K=8 and K=16 and the nested delivery subsets (the first 8 and the "
                             "first 16 seeds) are added and deduplicated against them; all of it is "
                             "materialised in this protocol before any scoring"},
    "criteria": CRITERIA, "noise_floor_reference": NOISE_FLOOR,
    "prior_art": {
        "experiments/wave14_seed_average_20260927/": "eight seeds, ten overlapping four-seed "
                                                     "subsets all containing seed 2026 or 2028, "
                                                     "variance ratio 0.465-0.788, mean 0.649",
        "experiments/refit_noise_eval/summary.json": "the +/-0.001743 noise floor",
        "releases/xgboost_seed8_r6/generation.json": "the delivery this measurement informs",
    },
    "harness_proofs": [
        "the frozen XGBoost reference composite is reproduced from its frozen prediction within "
        "1e-12 in every year before any seed is fitted",
        "the N-member rank average reproduces the frozen r5 xgb_two_mean raw bit-for-bit at N=2 in "
        "every year, which is what validates the generalisation to N=32",
        "the precomputed per-seed rank matrices used to average up to 240 subsets per year cheaply "
        "reproduce w14.rank_average_n BIT-FOR-BIT on three subsets per year, so the fast path is a "
        "proof-checked acceleration and not a reimplementation",
        "the eight seeds shared with wave-14 must retrain to raw predictions bit-identical to "
        "wave-14's frozen caches in every year; a mismatch halts the year before any scoring",
        "the seed-2026 refit is compared against the frozen r4 xgboost member raw and the "
        "comparison is recorded, bit-identity expected for 2022-2024",
        "the nested K=8 subset (seeds 2026-2033) is wave-14's eight-seed average, and re-scoring "
        "it here must reproduce wave-14's frozen composite within 1e-12 in every year",
    ],
    "prohibited": ["Adding a seed, subset or year after any score exists",
                   "Changing the recipe, the combination rule, the correction or the decision rule "
                   "after seeing a result",
                   "Presenting a score delta inside the noise floor as an improvement",
                   "Writing outside experiments/wave16_seed_curve_20260928/",
                   "Touching releases/, outputs/, active_release.json or maintenance/"],
    "limitations": [
        "All five years have been examined repeatedly; nothing here is out-of-sample.",
        "The 32 seeds are a finite pool, so a K-subset draw without replacement understates the "
        "infinite-population spread; the correction is analytic, not empirical.",
        "K=32 has exactly one subset and its spread can only be projected from the fitted rho.",
        "The official test-period composite cannot be measured at all; this is a validation-year "
        "proxy for the variability of the deliverable.",
        "Wave-13 recorded that the frozen 2020/2021 r4 xgboost member is not reproducible from the "
        "release recipe, so the 2020/2021 anchor comparison carries that documented caveat; the "
        "seed-to-seed spread measured here does not depend on it because every seed is fitted here.",
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


def subset_plan() -> dict:
    """Every subset this round will score, materialised before any score exists."""
    rng = np.random.default_rng(SUBSET_SEED)
    plan = {}
    for size in K_GRID:
        draws, seen = [], set()
        while len(draws) < SUBSETS_PER_K:
            picks = rng.permutation(POOL)[:size]
            subset = tuple(sorted(int(SEEDS[int(i)]) for i in picks))
            if subset not in seen:
                seen.add(subset)
                draws.append(subset)
        plan[f"random{size}"] = draws
    for size in DISJOINT_K:
        blocks = POOL // size
        plan[f"disjoint{size}"] = [tuple(SEEDS[b * size:(b + 1) * size]) for b in range(blocks)]
    for size, subset in NESTED.items():
        plan[f"nested{size}"] = [tuple(subset)]
    plan["full32"] = [tuple(SEEDS)]
    return plan


def unique_subsets(plan: dict) -> list[tuple[int, ...]]:
    ordered, seen = [], set()
    for group in plan.values():
        for subset in group:
            if subset not in seen:
                seen.add(subset)
                ordered.append(subset)
    return ordered


def rank_matrices(raws: dict[int, np.ndarray], valid: np.ndarray, days: int,
                  codes: int) -> dict[int, np.ndarray]:
    """Per-seed normalised rank contributions, shaped so that summing a subset reproduces
    w14.rank_average_n's floating-point operations in the same order."""
    from scipy.stats import rankdata
    out = {}
    for seed, raw in raws.items():
        matrix = np.asarray(raw, dtype=np.float64).reshape(days, codes)
        contribution = np.zeros((days, codes), dtype=np.float64)
        for day in range(days):
            keep = valid.reshape(days, codes)[day] & np.isfinite(matrix[day])
            count = int(keep.sum())
            if count:
                contribution[day, keep] = rankdata(matrix[day][keep], method="average") / count
        out[seed] = contribution
    return out


def average_from_matrices(members: list[np.ndarray], valid: np.ndarray, days: int,
                          codes: int) -> np.ndarray:
    shape = (days, codes)
    mask = valid.reshape(shape)
    mixed = np.zeros(shape, dtype=np.float64)
    for member in members:
        mixed += member
    out = np.full(shape, -10.0, dtype=np.float64)
    out[mask] = mixed[mask] / len(members)
    return out.reshape(-1)


def fast_path_proof(mats: dict[int, np.ndarray], raws: dict[int, np.ndarray], valid: np.ndarray,
                    days: int, codes: int, year: int) -> dict:
    """The accelerated subset average must be bit-identical to w14.rank_average_n."""
    probes = [tuple(SEEDS[:2]), tuple(SEEDS[:5]), tuple(SEEDS[:16])]
    worst = 0.0
    for subset in probes:
        fast = average_from_matrices([mats[s] for s in subset], valid, days, codes)
        slow = w14.rank_average_n([raws[s] for s in subset], valid, codes)
        if not np.array_equal(fast, slow):
            raise AssertionError(f"{year}: the fast subset average is not bit-identical to "
                                 f"w14.rank_average_n on {subset}")
        worst = max(worst, float(np.abs(fast - slow).max()))
    log(f"{year} fast-path proof: {len(probes)} subsets bit-identical to w14.rank_average_n")
    return {"probe_subsets": [list(s) for s in probes], "bit_identical": True, "max_abs_diff": worst}


def run_year(year: int) -> dict:
    path = OUT / f"year_{year}.json"
    if path.exists():
        log(f"{year} already recorded; preserving it")
        return read(path)
    started = time.monotonic()
    w9.OUT = OUT
    w14.OUT = OUT
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
    if len(valid) != days * codes:
        raise AssertionError(f"{year}: validation panel is not rectangular")
    combination = w14.combination_proof(bundle, codes)

    raws = {}
    for seed in SEEDS:
        raw = w14.fit_seed(bundle, seed)
        raws[seed] = raw
        cached = W14 / f"raw_seed{seed}_{year}.parquet"
        if seed in OVERLAPPING:
            previous = pl.read_parquet(cached).sort("trade_date", "ts_code")["pred_raw"].to_numpy()
            if not np.array_equal(raw, previous):
                raise AssertionError(f"{year} seed {seed}: the retrained raw is not bit-identical to "
                                     f"wave-14's frozen cache (max abs diff "
                                     f"{float(np.abs(raw - previous).max()):.3e})")
    log(f"{year}: {len(SEEDS)} seeds fitted; the {len(OVERLAPPING)} shared with wave-14 reproduce "
        "its frozen raws bit-for-bit")

    delivered = w14.agreement(raws[w14.DELIVERED_SEED], bundle["raws"]["xgboost"], valid, days)
    mats = rank_matrices(raws, valid, days, codes)
    fast = fast_path_proof(mats, raws, valid, days, codes, year)
    del raws
    gc.collect()

    plan = subset_plan()
    composites: dict[tuple[int, ...], dict] = {}
    wave14_average8 = read(W14 / f"year_{year}.json")["average8_metrics"]["final_score"]

    def score(subset: tuple[int, ...]) -> dict:
        if subset in composites:
            return composites[subset]
        average = average_from_matrices([mats[s] for s in subset], valid, days, codes)
        metrics, daily = score_official(bundle["frame"], w14.stacked(bundle, average))
        record = {k: float(v) for k, v in metrics.items()}
        if subset == NESTED[8]:
            # The first eight seeds are wave-14's eight seeds, the raws are bit-identical and the
            # combination rule is the same, so this composite must equal wave-14's exactly.
            if abs(record["final_score"] - wave14_average8) > 1e-12:
                raise AssertionError(f"{year}: re-scoring wave-14's eight-seed average gives "
                                     f"{record['final_score']:.15f} against its frozen "
                                     f"{wave14_average8:.15f}")
            log(f"{year} end-to-end proof: the nested K=8 subset reproduces wave-14's frozen "
                f"eight-seed composite {wave14_average8:.15f}")
        if len(subset) == POOL:
            daily.write_csv(OUT / f"daily_average{POOL}_{year}.csv")
        composites[subset] = record
        return record

    singles = {}
    for seed in SEEDS:
        average = average_from_matrices([mats[seed]], valid, days, codes)
        metrics, daily = score_official(bundle["frame"], w14.stacked(bundle, average))
        daily.write_csv(OUT / f"daily_seed{seed}_{year}.csv")
        singles[str(seed)] = {k: float(v) for k, v in metrics.items()}
        composites[(seed,)] = singles[str(seed)]
        if len(singles) % 8 == 0:
            log(f"{year}: {len(singles)}/{POOL} single-seed composites scored")
    single_values = [singles[str(seed)]["final_score"] for seed in SEEDS]

    groups = {}
    for name, subsets in plan.items():
        values = []
        for subset in subsets:
            values.append(score(subset)["final_score"])
            log(f"{year} {name} K={len(subset)} {len(values)}/{len(subsets)} "
                f"{values[-1]:.9f} ({time.strftime('%H:%M:%S')})")
        groups[name] = {"subsets": [list(s) for s in subsets], "composites": values}

    def spread(values: list[float], size: int) -> dict:
        """sd across subset draws, and the same sd corrected to an infinite seed population.

        K=1 is a census of the 32 pool members rather than a draw of one, so it carries no
        finite-population factor; its sd is the pool sd itself.
        """
        measured = float(np.std(values, ddof=1)) if len(values) > 1 else 0.0
        if size == 1:
            correction, inferred = 1.0, measured
        else:
            correction = float(np.sqrt((POOL - size) / POOL))
            inferred = float(measured / correction)
        return {"size": size, "draws": len(values), "mean": float(np.mean(values)),
                "sd_measured": measured, "finite_population_factor": correction,
                "sd_inferred": inferred,
                "ratio_to_single": float(inferred / np.std(single_values, ddof=1))}

    curve = [spread(single_values, 1)]
    for size in K_GRID:
        curve.append(spread(groups[f"random{size}"]["composites"], size))
        curve[-1]["disjoint_mean"] = float(np.mean(groups[f"disjoint{size}"]["composites"])) \
            if size in DISJOINT_K else None
        curve[-1]["disjoint_sd_measured"] = float(
            np.std(groups[f"disjoint{size}"]["composites"], ddof=1)) if size in DISJOINT_K else None
    curve.append({"size": POOL, "draws": 1, "mean": groups["full32"]["composites"][0],
                  "sd_measured": None, "finite_population_factor": 0.0, "sd_inferred": None,
                  "ratio_to_single": None,
                  "note": "a 32-subset of a 32-seed pool is unique; its spread is projected from "
                          "the fitted rho, not measured"})

    sd1 = curve[0]["sd_inferred"]
    # sd_inf(K)^2 / sd_inf(1)^2 = rho * (1 - 1/K) + 1/K, so rho is a no-intercept regression of
    # (ratio^2 - 1/K) on (1 - 1/K) over the four measured K.
    sizes = [c["size"] for c in curve[1:-1]]
    slope = np.asarray([1.0 - 1.0 / k for k in sizes], dtype=np.float64)
    residual = np.asarray([c["ratio_to_single"] ** 2 - 1.0 / c["size"] for c in curve[1:-1]],
                          dtype=np.float64)
    rho = float(min(max(float(np.dot(slope, residual) / np.dot(slope, slope)), 0.0), 1.0))
    projected = sd1 * float(np.sqrt(rho + (1.0 - rho) / POOL))
    record = {
        "year": year, "seconds": round(time.monotonic() - started, 2),
        "anchor_max_abs_diff": anchor, "combination_proof": combination,
        "fast_path_proof": fast,
        "delivered_metrics": {k: float(v) for k, v in reference.items()},
        "delivered_seed_agreement": delivered,
        "wave14_reproduction": {"seeds": list(OVERLAPPING), "bit_identical": True},
        "single_seed_composites": single_values,
        "single_seed_mean": float(np.mean(single_values)),
        "single_seed_sd": sd1, "single_seed_range": float(max(single_values) - min(single_values)),
        "curve": curve,
        "intraclass_rho_least_squares": rho,
        "projected_sd_at_32": projected,
        "projected_sd_ratio_32_over_1": float(projected / sd1),
        "groups": {name: {"subsets": value["subsets"], "composites": value["composites"],
                          "mean": float(np.mean(value["composites"])),
                          "sd": float(np.std(value["composites"], ddof=1))
                          if len(value["composites"]) > 1 else None}
                   for name, value in groups.items()},
        "nested": {str(size): {"subset": list(subset),
                               "composite": composites[tuple(subset)]["final_score"],
                               "turnover": composites[tuple(subset)]["mean_turnover"],
                               "ic": composites[tuple(subset)]["ic_mean"]}
                   for size, subset in NESTED.items()},
        "full32_composite": groups["full32"]["composites"][0],
        "full32_metrics": composites[tuple(SEEDS)],
        "wave14_average8_composite": read(W14 / f"year_{year}.json")["average8_metrics"]["final_score"],
        "singles": singles,
    }
    log(f"{year}: sd(K=1) {record['single_seed_sd']:.6f} | corrected sd " +
        " ".join(f"K={c['size']}:{c['sd_inferred']:.6f}" for c in curve[1:-1]) +
        f" | rho {rho:.3f} | projected sd(K=32) {projected:.6f} "
        f"({record['projected_sd_ratio_32_over_1']:.3f} x single)")
    write_new(path, record)
    del bundle, mats, composites
    gc.collect()
    return record


def freeze() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    if (OUT / "protocol.json").exists():
        raise SystemExit("Wave-16 protocol already frozen")
    sources = [Path(__file__), Path(w9.__file__), Path(w14.__file__), w9.JOINED_PANEL,
               ROOT / "data/features.parquet", ROOT / "evaluate.py", ROOT / "run.py",
               ROOT / "src/scoring.py", ROOT / "experiments/cached_recheck.py",
               ROOT / "experiments/revalidate_fold_local.py",
               ROOT / "experiments/optimize_r5_models.py",
               W14 / "protocol.json", W14 / "summary.json",
               ROOT / "experiments/refit_noise_eval/summary.json",
               ROOT / "releases/xgboost_seed8_r6/generation.json"]
    for year in YEARS:
        sources += [w9.R4 / f"predictions_xgboost_{year}.parquet",
                    w9.R4 / f"daily_xgboost_{year}.csv", w9.R4 / f"result_{year}.json",
                    W14 / f"year_{year}.json"]
        sources += [W14 / f"raw_seed{seed}_{year}.parquet" for seed in OVERLAPPING]
    plan = subset_plan()
    payload = {**PROTOCOL, "frozen_at_local": time.strftime("%Y-%m-%dT%H:%M:%S"),
               "source_sha256": sha(Path(__file__)),
               "subset_plan": {name: [list(s) for s in subsets] for name, subsets in plan.items()},
               "unique_subset_count": len(unique_subsets(plan)),
               "input_sha256": {p.relative_to(ROOT).as_posix(): sha(p)
                                for p in dict.fromkeys(sources)}}
    write_new(OUT / "protocol.json", payload)
    log(f"Froze the wave-16 protocol: {POOL} seeds, {payload['unique_subset_count']} distinct "
        f"subsets per year, {len(payload['input_sha256'])} pinned inputs, no score exists yet")


def verify_protocol() -> dict:
    protocol = read(OUT / "protocol.json")
    if protocol["source_sha256"] != sha(Path(__file__)):
        raise SystemExit("wave16_seed_curve.py changed after its protocol was frozen")
    if protocol["seeds"] != list(SEEDS) or protocol["recipe"] != RECIPE:
        raise SystemExit("Seeds or recipe drifted from the frozen protocol")
    if protocol["subset_plan"] != {name: [list(s) for s in subsets]
                                   for name, subsets in subset_plan().items()}:
        raise SystemExit("Subset plan drifted from the frozen protocol")
    for path, digest in protocol["input_sha256"].items():
        if sha(ROOT / path) != digest:
            raise SystemExit(f"Pinned input changed: {path}")
    return protocol


def decide(records: list[dict]) -> dict:
    def sd_at(size: int, record: dict) -> float:
        return float(next(c for c in record["curve"] if c["size"] == size)["sd_inferred"])

    mean = {size: float(np.mean([sd_at(size, r) for r in records])) for size in K_GRID}
    sd1 = float(np.mean([r["single_seed_sd"] for r in records]))
    projected32 = float(np.mean([r["projected_sd_at_32"] for r in records]))
    if projected32 <= 0.90 * mean[16]:
        chosen, reason = 32, "projected sd(K=32) is at most 90% of the measured sd(K=16)"
    elif mean[16] <= 0.90 * mean[8]:
        chosen, reason = 16, "measured sd(K=16) is at most 90% of the measured sd(K=8)"
    else:
        chosen, reason = 8, "averaging has saturated: neither 16 nor 32 buys a 10% sd reduction"
    return {"mean_sd_inferred_over_years": {"1": sd1, **{str(k): v for k, v in mean.items()},
                                            "32_projected": projected32},
            "relative_to_single": {"2": mean[2] / sd1, "4": mean[4] / sd1, "8": mean[8] / sd1,
                                   "16": mean[16] / sd1, "32_projected": projected32 / sd1},
            "iid_benchmark": {str(k): float(1.0 / np.sqrt(k)) for k in (2, 4, 8, 16, 32)},
            "k_delivery": chosen, "reason": reason,
            "mean_intraclass_rho": float(np.mean([r["intraclass_rho_least_squares"]
                                                  for r in records]))}


def summarise() -> None:
    if (OUT / "summary.json").exists():
        raise SystemExit("Summary already recorded; preserving it")
    records = [read(OUT / f"year_{year}.json") for year in YEARS]
    decision = decide(records)
    chosen = decision["k_delivery"]
    if chosen == 8:
        chosen_values = [r["wave14_average8_composite"] for r in records]
    else:
        chosen_values = [r["nested"][str(chosen)]["composite"] if chosen == 16
                         else r["full32_composite"] for r in records]
    baseline = [r["wave14_average8_composite"] for r in records]
    deltas = [a - b for a, b in zip(chosen_values, baseline)]
    summary = {
        "years": [r["year"] for r in records],
        "pool_size": POOL, "seeds": list(SEEDS),
        "criteria": CRITERIA,
        "per_year": {str(r["year"]): {
            "single_seed_sd": r["single_seed_sd"],
            "single_seed_range": r["single_seed_range"],
            "curve": r["curve"],
            "intraclass_rho": r["intraclass_rho_least_squares"],
            "projected_sd_at_32": r["projected_sd_at_32"],
            "nested": r["nested"],
            "full32_composite": r["full32_composite"],
            "full32_minus_delivered": float(r["full32_composite"]
                                            - r["delivered_metrics"]["final_score"]),
            "full32_minus_wave14_average8": float(r["full32_composite"]
                                                  - r["wave14_average8_composite"]),
            "full32_turnover_minus_delivered": float(r["full32_metrics"]["mean_turnover"]
                                                     - r["delivered_metrics"]["mean_turnover"]),
            "full32_ic_minus_delivered": float(r["full32_metrics"]["ic_mean"]
                                               - r["delivered_metrics"]["ic_mean"]),
            "delivered_seed_agreement": r["delivered_seed_agreement"],
            "wave14_reproduction": r["wave14_reproduction"],
            "seconds": r["seconds"]} for r in records},
        "decision": decision,
        "k_delivery": chosen,
        "chosen_five_year_mean": float(np.mean(chosen_values)),
        "wave14_average8_five_year_mean": float(np.mean(baseline)),
        "five_year_mean_delta_vs_wave14_average8": float(np.mean(deltas)),
        "verdict": {
            "k_delivery": chosen,
            "score_neutral_within_noise_floor": bool(abs(float(np.mean(deltas))) <= NOISE_FLOOR),
            "noise_floor": NOISE_FLOOR,
            "variance_reduced_further_than_eight_seeds": bool(
                decision["relative_to_single"][f"{chosen}_projected" if chosen == 32 else str(chosen)]
                < decision["relative_to_single"]["8"]),
        },
        "note": "Descriptive. A delta inside the noise floor is the expected outcome and must be "
                "reported as neutral, not as an improvement or a failure. The variance claim is "
                "about the spread across possible seed sets, never about predictive accuracy.",
    }
    write_new(OUT / "summary.json", summary)
    print(f"\n{'year':<6}{'sd(K=1)':>10}" + "".join(f"{'sd(K=%d)' % k:>11}" for k in K_GRID)
          + f"{'sd(K=32)*':>11}{'rho':>8}")
    for year in YEARS:
        r = next(x for x in records if x["year"] == year)
        cells = {c["size"]: c["sd_inferred"] for c in r["curve"][1:-1]}
        print(f"{year:<6}{r['single_seed_sd']:>10.6f}"
              + "".join(f"{cells[k]:>11.6f}" for k in K_GRID)
              + f"{r['projected_sd_at_32']:>11.6f}{r['intraclass_rho_least_squares']:>8.3f}")
    relative = decision["relative_to_single"]
    print("\n相对单种子的标准差（已做有限总体校正；* 为按 rho 外推）：")
    for label, value in relative.items():
        iid = decision["iid_benchmark"].get(label.split("_")[0], float("nan"))
        print(f"  K={label:<14}{value:>8.3f}   独立种子基准 {iid:>8.3f}")
    print(f"\n判定：K_delivery = {chosen}（{decision['reason']}），平均 rho "
          f"{decision['mean_intraclass_rho']:.3f}")
    print(f"五年均值：K={chosen} − wave-14 八种子平均 "
          f"{summary['five_year_mean_delta_vs_wave14_average8']:+.6f}"
          f"（噪声地板 ±{NOISE_FLOOR}）")


def selftest() -> None:
    """Everything that could break, checked on one year without producing a single new score."""
    OUT.mkdir(parents=True, exist_ok=True)
    folder = OUT / "_selftest"
    folder.mkdir(exist_ok=True)
    w9.OUT = OUT
    w14.OUT = folder
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
    valid = bundle["valid"]["price_valid"].to_numpy()
    days = bundle["valid"]["trade_date"].n_unique()
    codes = len(valid) // days
    w14.combination_proof(bundle, codes)
    probes = list(OVERLAPPING[:2]) + [SEEDS[-1]]
    raws = {seed: w14.fit_seed(bundle, seed) for seed in probes}
    for seed in OVERLAPPING[:2]:
        previous = pl.read_parquet(W14 / f"raw_seed{seed}_{year}.parquet").sort(
            "trade_date", "ts_code")["pred_raw"].to_numpy()
        if not np.array_equal(raws[seed], previous):
            raise AssertionError(f"seed {seed} does not reproduce wave-14's cache")
    mats = rank_matrices(raws, valid, days, codes)
    for subset in [tuple(probes[:1]), tuple(probes[:2]), tuple(probes)]:
        fast = average_from_matrices([mats[s] for s in subset], valid, days, codes)
        slow = w14.rank_average_n([raws[s] for s in subset], valid, codes)
        if not np.array_equal(fast, slow):
            raise AssertionError(f"fast path differs on {subset}")
    plan = subset_plan()
    counts = {name: len(value) for name, value in plan.items()}
    result = {"year": year, "anchor_max_abs_diff": anchor, "days": int(days), "codes": int(codes),
              "rows": int(len(valid)), "seeds_probed": probes,
              "wave14_cache_bit_identical": True, "n2_combination_proof": True,
              "fast_path_bit_identical": True, "subset_plan_counts": counts,
              "unique_subsets_per_year": len(unique_subsets(plan)),
              "scores_produced": 0,
              "note": "no subset average was scored in this stage; the only composite computed is "
                      "the frozen reference anchor, which is a published number"}
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
