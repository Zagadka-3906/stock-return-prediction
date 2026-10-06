"""Wave 24, direction 4: train new membership donors with the Top-decile-native objective.

Excess is the largest movable term (0.354106; each +0.01 is +0.003 of composite) and it is set almost
entirely by the membership donor. The donor in use is `topk_return_backbone` - a LightGBM fit through a
custom flat-Top-K objective whose gain is the EXACT change in mean Top-decile return for any swap, so it
is already trained for the right target. But it is a **single seed (2026)**, while the ordering side of
this project learned long ago that seed-averaging a rank signal is worth having: peer67_slow16 is a
16-seed rank average, and the 8-seed version was itself a documented variance reduction.

Stage 1 therefore trains four more seeds of the identical recipe and rank-averages them. Nothing about
the objective, the parameters, the round count, the sample count or the return scale changes; only
`PARAMS["seed"]` and the objective's own seed move, and both are moved together because the objective
draws its sampled pairs from a SeedSequence of (seed, iteration).

Stage 2 varies the one structural constant in the objective that has never been questioned: `k = n // 10`
inside sampled_day. The evaluator's excess reads the top len//10 of the LABEL-FILTERED universe, which
is a strict subset of the promoted decile, so a model trained on a sharper K (n//20) may be better at
ordering the very top even though the metric's decile is what gets promoted. A flatter K (n//5) is the
control. Both are run at seed 2026 only, so a gain there is attributable to K and not to seed averaging.

Harness proofs, before any new arm is believed:
  P1  retraining seed 2026 / K = n//10 for 2022 must reproduce the frozen
      predictions_topk_return_backbone_2022.parquet pred_raw column exactly. run_topk_confirm.py already
      achieved max|diff| 0.000e+00 on this fold, so this also proves this file's training path is the
      same one, not a transcription of it.
  P2  the frozen five-seed-2026 donor, lifted and scored with the selected orderer, must reproduce
      0.443190552.
  P3  every raw must be label-independent: fixed_prediction(frame, raw) == fixed_prediction(frame with
      y_ret_1d nulled, raw), the assertion r6_topk.fold() itself makes.

`RAW_LABELS` in experiments/r6_topk.py points at the archive root, where 训练集.csv no longer is - the
20261001 cleanup moved it to 赛题五/data/raw/. This file rebinds the module attribute in memory to the
live path and verifies its sha256 against the value pinned in the release lock before using it, so the
archive is never written to and the substitution is proven rather than assumed.

Selection is 后续选模标准.md §3/§4: highest connected 2020-2024 official composite, no other gate.
No test-period data is read anywhere in this file.
"""
from __future__ import annotations

import argparse
import gc
import hashlib
import json
import sys
import time
from pathlib import Path

import numpy as np
import polars as pl

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
ARCHIVE = ROOT.parent / "赛题五_历史归档_20261001"
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(ARCHIVE))

OUT = HERE / "wave24_topk"
RAW_CACHE = OUT / "raw"
KEYS = ["ts_code", "trade_date"]
YEARS = (2020, 2021, 2022, 2023, 2024)
NEW_SEEDS = (2027, 2028, 2029, 2030)
PROOF_YEAR = 2022
FROZEN_TOPK = {2022: ROOT / "analysis/topk_training_validation_20261001/"
                          "predictions_topk_return_backbone_2022.parquet",
               2023: ROOT / "analysis/topk_training_validation_20261001/"
                          "predictions_topk_return_backbone_2023.parquet",
               2024: ROOT / "analysis/topk_training_validation_20261001/"
                          "predictions_topk_return_backbone_2024.parquet"}
LIVE_TRAIN_CSV = ROOT / "data/raw/训练集.csv"
# pinned by releases/pooled_rms25/protocol.json -> preservation.prior_sha256
PINNED_TRAIN_CSV_SHA256 = "e9d23e87f7e1f943"
CURRENT_BEST = 0.44319055217888365
PARTNER_WEIGHT = 0.25


def sha(path) -> str:
    value = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for chunk in iter(lambda: stream.read(8 * 1024 * 1024), b""):
            value.update(chunk)
    return value.hexdigest()


def log(message: str) -> None:
    print(f"[{time.strftime('%H:%M:%S')}] {message}", flush=True)


def rebind_labels(rt) -> dict:
    """Point r6_topk at the live 训练集.csv and prove it is the pinned file."""
    if not LIVE_TRAIN_CSV.exists():
        raise SystemExit(f"no live training CSV at {LIVE_TRAIN_CSV}")
    digest = sha(LIVE_TRAIN_CSV)
    if not digest.startswith(PINNED_TRAIN_CSV_SHA256):
        raise SystemExit(f"the live 训练集.csv sha256 {digest[:16]}… does not match the value pinned in "
                         f"the release lock ({PINNED_TRAIN_CSV_SHA256}…)")
    original = str(rt.RAW_LABELS)
    rt.RAW_LABELS = LIVE_TRAIN_CSV
    log(f"RAW_LABELS rebound: {original} -> {LIVE_TRAIN_CSV} (sha256 {digest[:16]}…, pinned prefix "
        f"matched)")
    return {"original": original, "rebound_to": str(LIVE_TRAIN_CSV), "sha256": digest,
            "pinned_prefix_expected": PINNED_TRAIN_CSV_SHA256, "pinned_prefix_matched": True}


def sampled_day_k(scores, returns, rng, samples, scale, k_divisor, minimum=100):
    """r6_topk.sampled_day with the Top fraction parameterized. k_divisor = 10 is the original."""
    n = len(scores)
    gradient = np.zeros(n)
    hessian = np.zeros(n)
    if n < minimum:
        return gradient, hessian, 0
    k = max(n // k_divisor, 1)
    if k == n:
        return gradient, hessian, 0
    from experiments.r6_topk import pair_terms
    order = np.argsort(-scores, kind="stable")
    top, outside = order[:k], order[k:]
    draws = rng.integers(0, len(outside), size=(k, samples))
    first = np.repeat(top, samples)
    second = outside[draws.reshape(-1)]
    _, g, h = pair_terms(scores, returns, first, second, scale / (k * samples))
    gradient[top] = g.reshape(k, samples).sum(axis=1)
    hessian[top] = h.reshape(k, samples).sum(axis=1)
    gradient[outside] = -np.bincount(draws.reshape(-1), g, len(outside))
    hessian[outside] = np.bincount(draws.reshape(-1), h, len(outside))
    return gradient, hessian, len(first)


class ObjectiveK:
    """FlatTopKObjective with the Top fraction parameterized; k_divisor = 10 reproduces the original."""

    def __init__(self, dates, labels, seed, k_divisor, samples):
        self.inner = None
        self.k_divisor = int(k_divisor)
        self.samples = int(samples)
        self.dates = np.asarray(dates)
        self.labels = np.asarray(labels, dtype=np.float64)
        self.eligible = np.isfinite(self.labels)
        self.bounds = np.r_[0, np.flatnonzero(self.dates[1:] != self.dates[:-1]) + 1, len(self.dates)]
        self.groups = [np.flatnonzero(self.eligible[a:b]) + a for a, b in
                       zip(self.bounds[:-1], self.bounds[1:])]
        self.groups = [rows for rows in self.groups if len(rows) >= 100]
        if not self.groups:
            raise ValueError("no eligible groups with at least 100 stocks")
        self.scale = sum(len(rows) for rows in self.groups) / len(self.groups)
        self.seed, self.iteration = int(seed), 0
        self.pair_counts = []

    def __call__(self, predictions, dataset=None):
        scores = np.asarray(predictions, dtype=np.float64)
        if scores.shape != self.labels.shape or not np.isfinite(scores[self.eligible]).all():
            raise ValueError("invalid eligible predictions")
        rng = np.random.default_rng(np.random.SeedSequence([self.seed, self.iteration]))
        gradient = np.zeros(len(scores))
        hessian = np.zeros(len(scores))
        count = 0
        for rows in self.groups:
            g, h, pairs = sampled_day_k(scores[rows], self.labels[rows], rng, self.samples,
                                        self.scale, self.k_divisor)
            gradient[rows], hessian[rows] = g, h
            count += pairs
        if not np.isfinite(gradient).all() or not np.isfinite(hessian).all() or np.any(hessian < 0):
            raise AssertionError("nonfinite or negative optimization output")
        self.pair_counts.append(count)
        self.iteration += 1
        return gradient, hessian


def train_raw(rt, year: int, seed: int, k_divisor: int, to_matrix, lgb,
              FEATURE_FILE, feature_names, R4) -> tuple[pl.DataFrame, np.ndarray, dict]:
    started = time.monotonic()
    train, features, meta = rt.training_frame(year)
    objective = ObjectiveK(train["trade_date"].to_numpy(), train["y_ret_1d"].to_numpy(),
                           seed, k_divisor, rt.SAMPLES)
    x = to_matrix(train, features)
    dataset = lgb.Dataset(x, label=np.zeros(len(x), dtype=np.float32), feature_name=features,
                          free_raw_data=True)
    del train
    gc.collect()
    params = dict(rt.PARAMS, seed=seed, objective=rt.objective_callback(objective))
    fit_started = time.monotonic()
    model = lgb.train(params, dataset, num_boost_round=rt.ROUNDS)
    fit_seconds = time.monotonic() - fit_started
    if model.current_iteration() != rt.ROUNDS or objective.iteration != rt.ROUNDS:
        raise AssertionError(f"round count mismatch: {model.current_iteration()}/{objective.iteration}")
    del dataset, x
    gc.collect()

    frame = pl.read_parquet(R4 / f"predictions_ensemble4_{year}.parquet").sort("trade_date", "ts_code")
    valid = (pl.scan_parquet(FEATURE_FILE)
             .filter(pl.col("trade_date").is_between(year * 10000 + 101, year * 10000 + 1231))
             .select(KEYS + feature_names()).sort("trade_date", "ts_code").collect())
    if not frame.select(KEYS).equals(valid.select(KEYS)):
        raise AssertionError(f"{year}: prediction frame keys do not match the feature frame")
    matrix = to_matrix(valid, features)
    raw = model.predict(matrix, num_threads=8).astype(np.float64)
    raw[~frame["price_valid"].to_numpy()] = -1e6
    del matrix, valid, model
    gc.collect()
    info = {"year": year, "seed": seed, "k_divisor": k_divisor, "fit_seconds": round(fit_seconds, 1),
            "total_seconds": round(time.monotonic() - started, 1), "training_meta": meta,
            "objective_rounds": objective.iteration,
            "sampled_pairs_total": int(sum(objective.pair_counts))}
    return frame, raw, info


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("stage", choices=("protocol", "prove", "seeds", "kvariants", "score"))
    args = parser.parse_args()

    OUT.mkdir(parents=True, exist_ok=True)
    RAW_CACHE.mkdir(parents=True, exist_ok=True)

    import lightgbm as lgb
    import experiments.r6_topk as rt
    from run import FEATURE_FILE, feature_names, to_matrix
    from experiments.r6_topk import R4, fixed_prediction

    label_record = rebind_labels(rt)

    protocol_path = HERE / "protocol_wave24.json"
    if args.stage == "protocol" or not protocol_path.exists():
        if protocol_path.exists():
            log("protocol already frozen, leaving it untouched")
        else:
            protocol_path.write_text(json.dumps({
                "frozen_at_local": time.strftime("%Y-%m-%dT%H:%M:%S"),
                "standard": "后续选模标准.md §3 connected composite primary; §4 highest score wins",
                "status": "in_sample_selection_disclosed",
                "hypothesis": {
                    "stage1_seeds": "the membership donor is a single seed (2026) of a Top-K "
                                    "return-weighted pairwise objective. Seed-averaging a rank signal is "
                                    "an established variance reduction here - peer67_slow16 is a 16-seed "
                                    "rank average - and the donor decides which names are promoted, so "
                                    "less noise in that pick should raise excess.",
                    "stage2_k": "sampled_day hard-codes k = n//10. The evaluator's excess reads the top "
                                "len//10 of the LABEL-FILTERED universe, a strict subset of the promoted "
                                "decile, so a sharper K (n//20) may order the very top better. n//5 is "
                                "the flatter control.",
                },
                "recipe_unchanged": {"params": rt.PARAMS, "rounds": rt.ROUNDS, "samples": rt.SAMPLES,
                                     "return_scale": rt.RETURN_SCALE, "base_seed": rt.SEED},
                "new_seeds": list(NEW_SEEDS), "k_divisors": [10, 20, 5],
                "harness_proofs": {
                    "P1": f"seed 2026 / k_divisor 10 on {PROOF_YEAR} must reproduce "
                          f"{FROZEN_TOPK[PROOF_YEAR].name} pred_raw exactly",
                    "P2": f"the frozen seed-2026 donor, lifted and scored with the selected orderer, "
                          f"must reproduce {CURRENT_BEST}",
                    "P3": "fixed_prediction(frame, raw) == fixed_prediction(frame with y nulled, raw) "
                          "for every trained raw",
                },
                "labels_rebinding": label_record,
                "archive_write": "none; every artifact is written under "
                                 "analysis/connected_validation_20261002/wave24_topk/",
                "current_best_before_this_wave": CURRENT_BEST,
                "selection_rule": "highest connected 2020-2024 official composite; no other gate",
                "disclosed_selection_cost": "new models trained on the same five repeatedly viewed "
                                            "years; walk-forward cutoffs are unchanged and strictly "
                                            "before each scored year, but the choice of how many seeds "
                                            "and which K values to try is made with those years already "
                                            "viewed",
                "causality": "training_frame filters trade_date < fold_cutoff(year) and joins labels "
                             "only from before that cutoff, so no fold sees its own year or later",
                "no_test_period_data_read": True,
                "source_sha256": sha(Path(__file__)),
            }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            log(f"wave-24 protocol frozen: {sha(protocol_path)[:16]}…")
    if args.stage == "protocol":
        return

    def cache_path(year: int, seed: int, k_divisor: int) -> Path:
        return RAW_CACHE / f"topk_seed{seed}_k{k_divisor}_{year}.parquet"

    def train_or_load(year: int, seed: int, k_divisor: int) -> np.ndarray:
        path = cache_path(year, seed, k_divisor)
        if path.exists():
            return pl.read_parquet(path)["pred_raw"].to_numpy().astype(np.float64)
        frame, raw, info = train_raw(rt, year, seed, k_divisor, to_matrix, lgb, FEATURE_FILE,
                                     feature_names, R4)
        # P3: label independence
        pred = fixed_prediction(frame, raw)
        nulled = frame.with_columns(pl.lit(None, dtype=pl.Float64).alias("y_ret_1d"))
        if not np.array_equal(pred, fixed_prediction(nulled, raw)):
            raise AssertionError(f"P3 failed for seed {seed} k {k_divisor} year {year}: the "
                                 "post-processing is not label-independent")
        frame.select(KEYS).with_columns(pl.Series("pred_raw", raw)).write_parquet(
            path, compression="zstd")
        (RAW_CACHE / f"info_seed{seed}_k{k_divisor}_{year}.json").write_text(
            json.dumps(info, ensure_ascii=False, indent=2, default=str) + "\n", encoding="utf-8")
        log(f"  trained seed {seed} k//{k_divisor} {year}: {info['fit_seconds']}s fit, "
            f"{info['training_meta']['rows']:,} rows / {info['training_meta']['days']} days")
        return raw

    if args.stage == "prove":
        frame, raw, info = train_raw(rt, PROOF_YEAR, rt.SEED, 10, to_matrix, lgb, FEATURE_FILE,
                                     feature_names, R4)
        frozen = pl.read_parquet(FROZEN_TOPK[PROOF_YEAR]).sort("trade_date", "ts_code")
        if not frozen.select(KEYS).equals(frame.select(KEYS)):
            raise AssertionError("the frozen topk cache's keys do not match the fold frame")
        target = frozen["pred_raw"].to_numpy().astype(np.float64)
        diff = float(np.abs(raw - target).max())
        identical = bool(np.array_equal(raw, target))
        log(f"P1: retrained seed 2026 / k//10 for {PROOF_YEAR} in {info['fit_seconds']}s; "
            f"max|diff| vs the frozen cache = {diff:.3e}, bit-identical = {identical}")
        record = {"proof": "P1", "year": PROOF_YEAR, "seed": rt.SEED, "k_divisor": 10,
                  "frozen_cache": str(FROZEN_TOPK[PROOF_YEAR]),
                  "frozen_sha256": sha(FROZEN_TOPK[PROOF_YEAR]),
                  "max_abs_diff": diff, "bit_identical": identical, "training_info": info,
                  "labels_rebinding": label_record,
                  "proved_at_local": time.strftime("%Y-%m-%dT%H:%M:%S")}
        (OUT / "harness_proof_P1.json").write_text(
            json.dumps(record, ensure_ascii=False, indent=2, default=str) + "\n", encoding="utf-8")
        if not identical and diff > 0.0:
            raise AssertionError(f"P1 failed: max|diff| {diff:.3e}; this training path is not the "
                                 "frozen one, so nothing below can be trusted")
        log("P1 passed")
        return

    if args.stage == "seeds":
        for seed in (rt.SEED,) + NEW_SEEDS:
            for year in YEARS:
                train_or_load(year, seed, 10)
        log("stage 1 training complete")
        return

    if args.stage == "kvariants":
        for k_divisor in (20, 5):
            for year in YEARS:
                train_or_load(year, rt.SEED, k_divisor)
        log("stage 2 training complete")
        return

    if args.stage == "score":
        score_arms(rt, fixed_prediction, feature_names, R4, FEATURE_FILE, to_matrix, lgb)


def score_arms(rt, fixed_prediction, feature_names, R4, FEATURE_FILE, to_matrix, lgb) -> None:
    import pandas as pd
    import connected_scorer as cs
    from experiments.revalidate_fold_local import score_official
    from optimize_wave6 import make_prediction_param
    from optimize_wave13 import build_ab
    from optimize_wave15 import daily_ranks, weighted_rank_blend, DONOR, M_FRAC, TIE_EPS
    from optimize_wave18 import lift
    from src.scoring import Panel
    sys.path.insert(0, str(ROOT / "analysis"))
    from analysis.topset_hybrid_20261002 import fold_validation as fv
    rank_average_n = fv.load_rank_average_n()

    combined = cs.combined_frame()
    dates = combined["trade_date"].to_numpy()
    flags = combined["flag_limit_up"].to_numpy().astype(np.int64)
    valid = combined["price_valid"].to_numpy().astype(bool)
    codes, uniques = pd.factorize(combined["ts_code"].to_pandas(), sort=True)
    codes = codes.astype(np.int64)
    n_codes = len(uniques)
    tie_key = 1.0 - codes / max(n_codes - 1, 1)
    pdf = combined.select(["trade_date", "flag_limit_up"]).to_pandas()
    slow16_fin = np.load(HERE / "connected_pred_peer67_slow16.npy")

    w5a = np.load(HERE / "orderer_a0b0_W5a_five_way_with_gru__final_sweep_eval.npy")
    slow16 = np.load(HERE / "pp_a0_b0_top_only_w0.25_rl1_tcw1.npy")
    cache: dict = {"w5a": daily_ranks(w5a, valid, dates), "slow16": daily_ranks(slow16, valid, dates)}
    blended = weighted_rank_blend([w5a, slow16], [1 - PARTNER_WEIGHT, PARTNER_WEIGHT], cache, valid,
                                  dates, ("w5a", "slow16"))
    orderer = np.where(blended > -9.0, blended + TIE_EPS * tie_key, blended)

    # fold_frame (not the bare R4 parquet) because rank_average_n needs grid_price_valid, which
    # optimize_wave6.fold_frame joins in from data/features.parquet; the bare bundle frame has aux_raw
    # but not that column
    from optimize_wave6 import fold_frame
    frames = {y: fold_frame(y) for y in YEARS}

    def postprocess(raw_by_year: dict) -> np.ndarray:
        parts = []
        for year in YEARS:
            frame = frames[year]
            panel = Panel.from_frame(frame.with_columns(pl.Series("pred_raw", raw_by_year[year])))
            parts.append(make_prediction_param(panel, frame["aux_raw"].to_numpy().astype(np.float64),
                                               "top_only", 0.25, 0.9, 0.3, True, 1.0))
            del panel
        return np.concatenate(parts)

    def load_raws(seed: int, k_divisor: int) -> dict:
        out = {}
        for year in YEARS:
            path = RAW_CACHE / f"topk_seed{seed}_k{k_divisor}_{year}.parquet"
            if not path.exists():
                raise SystemExit(f"missing {path.name}; run the seeds/kvariants stage first")
            out[year] = pl.read_parquet(path)["pred_raw"].to_numpy().astype(np.float64)
        return out

    results: dict = {}
    proofs: dict = {}

    def dump() -> list:
        arms = sorted(((v["connected_final_score"], k, v) for k, v in results.items()
                       if "connected_final_score" in v), reverse=True)
        payload = {"status": "running", "updated_at_local": time.strftime("%Y-%m-%dT%H:%M:%S"),
                   "purpose": "new membership donors trained with the Top-decile-native objective",
                   "orderer_fixed": ["W5a@a0b0", "slow16@a0b0"], "partner_weight": PARTNER_WEIGHT,
                   "m_frac": M_FRAC, "tie_break_eps": TIE_EPS, "harness_proofs": proofs,
                   "current_best_before_this_wave": CURRENT_BEST, "results": results,
                   "n_scored": len(arms),
                   "ranking": [{"arm": k, "connected_final_score": s,
                                "ic_mean": v["connected_metrics"]["ic_mean"],
                                "annual_excess": v["connected_metrics"]["annual_excess"],
                                "mean_turnover": v["connected_metrics"]["mean_turnover"],
                                "donor_standalone_excess": v.get("donor_standalone_excess")}
                               for s, k, v in arms[:25]],
                   "best": arms[0][1] if arms else None,
                   "best_connected_final_score": arms[0][0] if arms else None,
                   "improves_on_current_best": bool(arms and arms[0][0] > CURRENT_BEST),
                   "no_test_period_data_read": True, "source_sha256": sha(Path(__file__))}
        (HERE / "wave24_results.json").write_text(
            json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        return arms

    def evaluate_donor(name: str, finished: np.ndarray, extra: dict) -> None:
        # Rank-averaging seeds creates exact ties, and fv.top_sets refuses a promoted source with a
        # promotion-boundary tie, so the promote source gets the project's standard causal tie-break.
        # The re-ranker is left exactly as shipped. Whether the tie-break is inert for the single-seed
        # reference is NOT assumed - wave 28 assumed it and was wrong by 1.01e-4 - it is settled by the
        # P2 assertion below, which requires the reference to reproduce 0.443190552 to 1e-12.
        promote = np.where(np.isfinite(finished) & (finished > -9.0),
                           finished + TIE_EPS * tie_key, finished)
        donor, lift_stats = lift(promote, slow16_fin, pdf)
        hybrid, stats = build_ab(donor, orderer + TIE_EPS * tie_key, orderer + TIE_EPS * tie_key,
                                 dates, flags, codes, n_codes, M_FRAC)
        metrics, _ = score_official(combined, hybrid)
        standalone, _ = score_official(combined, finished)
        results[name] = {**extra, "connected_final_score": metrics["final_score"],
                         "connected_metrics": metrics, "lift_stats": lift_stats,
                         "donor_standalone_connected": standalone["final_score"],
                         "donor_standalone_excess": standalone["annual_excess"],
                         "boundary_tie_days": stats["boundary_tie_days"],
                         "mean_retention_ratio": stats["mean_retention_ratio"],
                         "margin_over_best": metrics["final_score"] - CURRENT_BEST}
        cs.log(f"{name[:44]:44s} CONNECTED {metrics['final_score']:.9f} "
               f"(ic {metrics['ic_mean']:.6f}, excess {metrics['annual_excess']:.6f}, "
               f"turn {metrics['mean_turnover']:.6f}) donor standalone exc "
               f"{standalone['annual_excess']:.6f} | margin "
               f"{metrics['final_score'] - CURRENT_BEST:+.3e}")
        dump()

    # ---- P2: the frozen seed-2026 donor must reproduce the selection
    single = postprocess(load_raws(rt.SEED, 10))
    frozen_topk = np.load(HERE / "connected_pred_topk.npy")
    proofs["P2_frozen_donor_reproduces"] = {
        "rebuilt_equals_connected_pred_topk": bool(np.array_equal(single, frozen_topk)),
        "max_abs_diff": float(np.abs(single - frozen_topk).max())}
    evaluate_donor("P2_seed2026_k10_reference", single,
                   {"kind": "single_seed", "seeds": [rt.SEED], "k_divisor": 10,
                    "role": "harness_proof"})
    proofs["P2_frozen_donor_reproduces"]["scored"] = results["P2_seed2026_k10_reference"][
        "connected_final_score"]
    proofs["P2_frozen_donor_reproduces"]["expected"] = CURRENT_BEST
    proofs["P2_frozen_donor_reproduces"]["abs_diff"] = abs(
        results["P2_seed2026_k10_reference"]["connected_final_score"] - CURRENT_BEST)
    if proofs["P2_frozen_donor_reproduces"]["abs_diff"] > 1e-12:
        raise AssertionError(f"P2 failed: {proofs['P2_frozen_donor_reproduces']}")
    cs.log("P2 passed: the frozen donor reproduces 0.443190552")
    dump()

    # ---- stage 1: seed averaging, cumulative
    seeds = [rt.SEED] + list(NEW_SEEDS)
    for n in range(2, len(seeds) + 1):
        use = seeds[:n]
        raws = [load_raws(s, 10) for s in use]
        averaged = {}
        for year in YEARS:
            days = frames[year]["trade_date"].n_unique()
            codes_year = len(frames[year]) // days
            averaged[year] = rank_average_n([r[year] for r in raws],
                                            frames[year]["grid_price_valid"].to_numpy(), codes_year)
        evaluate_donor(f"seedavg_{n}seeds_k10", postprocess(averaged),
                       {"kind": "seed_average", "seeds": use, "k_divisor": 10})

    # ---- stage 2: K variants at the base seed
    for k_divisor in (20, 5):
        try:
            evaluate_donor(f"single_seed2026_k{k_divisor}", postprocess(load_raws(rt.SEED, k_divisor)),
                           {"kind": "single_seed", "seeds": [rt.SEED], "k_divisor": k_divisor})
        except SystemExit as error:
            results[f"single_seed2026_k{k_divisor}"] = {"kind": "single_seed", "k_divisor": k_divisor,
                                                        "error": str(error)}
            cs.log(f"k{k_divisor} not trained yet: {error}")
            dump()

    arms = dump()
    payload = json.loads((HERE / "wave24_results.json").read_text(encoding="utf-8"))
    payload["status"] = "complete"
    payload["completed_at_local"] = time.strftime("%Y-%m-%dT%H:%M:%S")
    (HERE / "wave24_results.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("\n| rank | donor | CONNECTED | margin | IC | excess | turnover | donor standalone excess |")
    print("|---|---|---|---|---|---|---|---|")
    for i, (s, name, v) in enumerate(arms):
        m = v["connected_metrics"]
        print(f"| {i+1} | {name[:34]} | **{s:.9f}** | {s - CURRENT_BEST:+.2e} | {m['ic_mean']:.6f} | "
              f"{m['annual_excess']:.6f} | {m['mean_turnover']:.6f} | "
              f"{v.get('donor_standalone_excess', float('nan')):.6f} |")


if __name__ == "__main__":
    main()
