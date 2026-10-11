"""Wave 31: the Top-K objective's K was fixed at the evaluator's decile and never questioned. Sweep it.

`sampled_day` in experiments/r6_topk.py hard-codes `k = max(n//10, 1)`, matching the evaluator's Top
decile. Wave 24 varied it for the first time and the result is the largest single gain this project has
found since the substitution construction itself:

    K = n//20 (5%)   0.433710440   -9.48e-03
    K = n//10 (10%)  0.443190552    reference
    K = n//5  (20%)  0.445092234   +1.90e-03   <-- IC, excess AND turnover all improved

+1.90e-03 is 8.6x wave 20's top-six plateau width (2.2e-4) and slightly above the 0.001743 refit noise
floor, which makes it the first gain in waves 15-29 that is not a plateau-scale artifact. And it is not
a trade: IC 0.116662 -> 0.118424, excess 0.354106 -> 0.357767, turnover 0.032354 -> 0.032025.

The mechanism is worth stating because it explains why the sharper K is worse and a flatter one better.
The objective's gradient only touches the current predicted Top-k and the pool members sampled against
it. With k = n//20 the model is trained to separate 5% of the day from the rest, which is a much harder
and noisier target and produces a column that is worse at ordering the other 95% - and this donor's job
in the nested construction is to define a promoted block that the re-ranker then orders, so a column
that only knows its own top 5% is a worse promote source. With k = n//5 the model learns a coarser,
better-estimated ordering over the top fifth, and the decile the evaluator actually reads sits inside a
region the model was trained to order well rather than at the edge of its training signal.

That reasoning predicts an interior optimum somewhere above 0.20, so this wave grids the fraction from
0.10 to 0.60 rather than stopping at the first improvement.

K is parameterized as k = max(floor(frac * n), 1), which reproduces n//10 at frac = 0.10 and n//5 at
frac = 0.20 exactly, so frac = 0.10 is the harness proof: it must reproduce the frozen
predictions_topk_return_backbone_2022.parquet bit-for-bit.

Deliverability is NOT free here and is recorded rather than assumed: the test-period topk column
(middle/predictions/supplemental_topk_fulltrain2024.parquet) was trained at K = n//10, so any other
fraction needs a test-period fulltrain re-fit. The recipe is proven reproducible by that same harness
proof, and run_topk_confirm.py already retrained a fold to max|diff| 0.000e+00, so this is a known cost
rather than a risk - but it is a retrain, and the winner must pay it.

Selection is 后续选模标准.md §3/§4: highest connected 2020-2024 official composite, no other gate. The
both-halves rule from waves 26-28 is reported alongside because every m-axis gain so far turned out to
be a redistribution between halves. No test-period data is read anywhere in this file.
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

OUT = HERE / "wave31_topk"
RAW = OUT / "raw"
YEARS = (2020, 2021, 2022, 2023, 2024)
SEED = 2026
PROOF_YEAR = 2022
FROZEN_2022 = ROOT / "analysis/topk_training_validation_20261001/predictions_topk_return_backbone_2022.parquet"
LIVE_TRAIN_CSV = ROOT / "data/raw/训练集.csv"
PINNED_PREFIX = "e9d23e87f7e1f943"
FRACTIONS = (0.10, 0.15, 0.20, 0.25, 0.30, 0.40, 0.50, 0.60)
CURRENT_BEST = 0.445092234
REF_HALF_DEV = 0.442705356
REF_HALF_CONF = 0.443926938
PARTNER_WEIGHT = 0.25
M_FRAC = 0.985
TIE_EPS = 1e-9


def sha(path) -> str:
    value = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for chunk in iter(lambda: stream.read(8 * 1024 * 1024), b""):
            value.update(chunk)
    return value.hexdigest()


def log(message: str) -> None:
    print(f"[{time.strftime('%H:%M:%S')}] {message}", flush=True)


def sampled_day_frac(scores, returns, rng, samples, scale, frac, minimum=100):
    """r6_topk.sampled_day with k = max(floor(frac * n), 1). frac = 0.10 is the original n//10."""
    n = len(scores)
    gradient = np.zeros(n)
    hessian = np.zeros(n)
    if n < minimum:
        return gradient, hessian, 0
    k = max(int(np.floor(frac * n)), 1)
    if k >= n:
        return gradient, hessian, 0
    from experiments.r6_topk import pair_terms
    order = np.argsort(-scores, kind="stable")
    top, outside = order[:k], order[k:]
    if not len(outside):
        return gradient, hessian, 0
    draws = rng.integers(0, len(outside), size=(k, samples))
    first = np.repeat(top, samples)
    second = outside[draws.reshape(-1)]
    _, g, h = pair_terms(scores, returns, first, second, scale / (k * samples))
    gradient[top] = g.reshape(k, samples).sum(axis=1)
    hessian[top] = h.reshape(k, samples).sum(axis=1)
    gradient[outside] = -np.bincount(draws.reshape(-1), g, len(outside))
    hessian[outside] = np.bincount(draws.reshape(-1), h, len(outside))
    return gradient, hessian, len(first)


class ObjectiveFrac:
    def __init__(self, dates, labels, seed, frac, samples):
        self.frac = float(frac)
        self.samples = int(samples)
        self.dates = np.asarray(dates)
        self.labels = np.asarray(labels, dtype=np.float64)
        self.eligible = np.isfinite(self.labels)
        eligible = self.eligible
        self.bounds = np.r_[0, np.flatnonzero(self.dates[1:] != self.dates[:-1]) + 1, len(self.dates)]
        self.groups = [np.flatnonzero(eligible[a:b]) + a for a, b in
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
            g, h, pairs = sampled_day_frac(scores[rows], self.labels[rows], rng, self.samples,
                                           self.scale, self.frac)
            gradient[rows], hessian[rows] = g, h
            count += pairs
        if not np.isfinite(gradient).all() or not np.isfinite(hessian).all() or np.any(hessian < 0):
            raise AssertionError("nonfinite or negative optimization output")
        self.pair_counts.append(count)
        self.iteration += 1
        return gradient, hessian


def train(rt, year: int, seed: int, frac: float, to_matrix, lgb, FEATURE_FILE, feature_names, R4):
    started = time.monotonic()
    train, features, meta = rt.training_frame(year)
    objective = ObjectiveFrac(train["trade_date"].to_numpy(), train["y_ret_1d"].to_numpy(),
                              seed, frac, rt.SAMPLES)
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
        raise AssertionError("round count mismatch")
    del dataset, x
    gc.collect()
    frame = pl.read_parquet(R4 / f"predictions_ensemble4_{year}.parquet").sort("trade_date", "ts_code")
    valid = (pl.scan_parquet(FEATURE_FILE)
             .filter(pl.col("trade_date").is_between(year * 10000 + 101, year * 10000 + 1231))
             .select(["ts_code", "trade_date"] + feature_names()).sort("trade_date", "ts_code").collect())
    if not frame.select(["ts_code", "trade_date"]).equals(valid.select(["ts_code", "trade_date"])):
        raise AssertionError(f"{year}: key mismatch between the fold frame and the feature frame")
    matrix = to_matrix(valid, features)
    raw = model.predict(matrix, num_threads=8).astype(np.float64)
    raw[~frame["price_valid"].to_numpy()] = -1e6
    del matrix, valid, model
    gc.collect()
    info = {"year": year, "seed": seed, "frac": frac, "fit_seconds": round(fit_seconds, 1),
            "total_seconds": round(time.monotonic() - started, 1), "training_meta": meta,
            "rounds": objective.iteration, "sampled_pairs_total": int(sum(objective.pair_counts))}
    return frame, raw, info


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("stage", choices=("protocol", "prove", "train", "score"))
    parser.add_argument("--fracs", type=float, nargs="*", default=None)
    args = parser.parse_args()
    fracs = tuple(args.fracs) if args.fracs else FRACTIONS

    OUT.mkdir(parents=True, exist_ok=True)
    RAW.mkdir(parents=True, exist_ok=True)

    import lightgbm as lgb
    import experiments.r6_topk as rt
    from run import FEATURE_FILE, feature_names, to_matrix
    from experiments.r6_topk import R4, fixed_prediction

    if not LIVE_TRAIN_CSV.exists():
        raise SystemExit(f"no live training CSV at {LIVE_TRAIN_CSV}")
    digest = sha(LIVE_TRAIN_CSV)
    if not digest.startswith(PINNED_PREFIX):
        raise SystemExit(f"the live 训练集.csv sha256 {digest[:16]}… is not the pinned file")
    rt.RAW_LABELS = LIVE_TRAIN_CSV

    protocol_path = HERE / "protocol_wave31.json"
    if not protocol_path.exists():
        protocol_path.write_text(json.dumps({
            "frozen_at_local": time.strftime("%Y-%m-%dT%H:%M:%S"),
            "standard": "后续选模标准.md §3 connected composite primary; §4 highest score wins",
            "status": "in_sample_selection_disclosed",
            "hypothesis": "sampled_day hard-codes k = n//10, matching the evaluator's decile. Wave 24 "
                          "found k = n//5 gives +1.90e-03 with IC, excess AND turnover all improving, "
                          "and k = n//20 gives -9.48e-03, so there is an interior optimum above 0.20. "
                          "Mechanism: the objective's gradient only touches the predicted Top-k and the "
                          "pool sampled against it, so a very sharp k trains the model to separate a "
                          "tiny, noisy head and leaves it worse at ordering the rest - and this donor's "
                          "job is to define a promoted block that the re-ranker orders.",
            "parameterization": "k = max(floor(frac * n), 1), which equals n//10 at frac = 0.10 and "
                                "n//5 at frac = 0.20, so frac = 0.10 is backward compatible with the "
                                "frozen recipe",
            "grid": list(FRACTIONS), "seed": SEED,
            "recipe_unchanged": {"params": rt.PARAMS, "rounds": rt.ROUNDS, "samples": rt.SAMPLES,
                                 "return_scale": rt.RETURN_SCALE},
            "harness_proof": f"frac = 0.10 on {PROOF_YEAR} must reproduce "
                             f"{FROZEN_2022.name} pred_raw bit-for-bit",
            "donor_construction": "the shipped nested lift: promoted = top decile of this donor by "
                                  "fv.top_sets, re-ranked by peer67_slow16 finished, causal tie-break "
                                  "on the promote source",
            "outer_fixed": {"orderer": ["W5a@a0b0", "slow16@a0b0"], "weights": [0.75, 0.25],
                            "m_frac": M_FRAC, "tie_break_eps": TIE_EPS},
            "deliverability_recorded_not_assumed": "the test-period topk column was trained at "
                                                   "k = n//10, so any other fraction needs a test-period "
                                                   "fulltrain re-fit. The recipe is proven reproducible "
                                                   "by the harness proof and run_topk_confirm.py already "
                                                   "retrained a fold to max|diff| 0.000e+00, so this is "
                                                   "a known cost, not a risk.",
            "labels_rebinding": {"original": "archive root 训练集.csv, moved by the 20261001 cleanup",
                                 "rebound_to": str(LIVE_TRAIN_CSV), "sha256": digest,
                                 "pinned_prefix_matched": True},
            "shipping_rule_declared_in_advance": "report the both-halves decomposition; a full-window "
                                                 "win that moves only one half is a redistribution",
            "current_best_before_this_wave": CURRENT_BEST,
            "selection_rule": "highest connected 2020-2024 official composite; no other gate",
            "disclosed_selection_cost": "eight new models trained on the same five repeatedly viewed "
                                        "years; walk-forward cutoffs are unchanged and strictly before "
                                        "each scored year, but the decision to sweep K was made after "
                                        "wave 24 saw those years",
            "no_test_period_data_read": True,
            "source_sha256": sha(Path(__file__)),
        }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        log(f"wave-31 protocol frozen: {sha(protocol_path)[:16]}…")
    if args.stage == "protocol":
        return

    def cache(year: int, frac: float) -> Path:
        return RAW / f"topk_seed{SEED}_f{frac:.2f}_{year}.parquet"

    if args.stage == "prove":
        frame, raw, info = train(rt, PROOF_YEAR, SEED, 0.10, to_matrix, lgb, FEATURE_FILE,
                                 feature_names, R4)
        frozen = pl.read_parquet(FROZEN_2022).sort("trade_date", "ts_code")
        target = frozen["pred_raw"].to_numpy().astype(np.float64)
        diff = float(np.abs(raw - target).max())
        identical = bool(np.array_equal(raw, target))
        log(f"PROVE frac=0.10 {PROOF_YEAR}: fit {info['fit_seconds']}s, bit-identical={identical}, "
            f"max|diff|={diff:.3e}")
        (OUT / "harness_proof.json").write_text(json.dumps(
            {"proof": "frac 0.10 reproduces the frozen k=n//10 cache", "year": PROOF_YEAR,
             "frozen_cache": str(FROZEN_2022), "frozen_sha256": sha(FROZEN_2022),
             "bit_identical": identical, "max_abs_diff": diff, "training_info": info,
             "proved_at_local": time.strftime("%Y-%m-%dT%H:%M:%S")},
            ensure_ascii=False, indent=2, default=str) + "\n", encoding="utf-8")
        if not identical:
            raise AssertionError(f"frac = 0.10 does not reproduce the frozen recipe (max|diff| {diff:.3e})")
        return

    if args.stage == "train":
        for frac in fracs:
            for year in YEARS:
                path = cache(year, frac)
                if path.exists():
                    continue
                frame, raw, info = train(rt, year, SEED, frac, to_matrix, lgb, FEATURE_FILE,
                                         feature_names, R4)
                pred = fixed_prediction(frame, raw)
                nulled = frame.with_columns(pl.lit(None, dtype=pl.Float64).alias("y_ret_1d"))
                if not np.array_equal(pred, fixed_prediction(nulled, raw)):
                    raise AssertionError(f"frac {frac} {year}: the stack is not label-independent")
                frame.select(["ts_code", "trade_date"]).with_columns(
                    pl.Series("pred_raw", raw)).write_parquet(path, compression="zstd")
                (RAW / f"info_f{frac:.2f}_{year}.json").write_text(
                    json.dumps(info, ensure_ascii=False, indent=2, default=str) + "\n",
                    encoding="utf-8")
                log(f"  frac {frac:.2f} {year}: fit {info['fit_seconds']}s, "
                    f"{info['training_meta']['rows']:,} rows")
        log("training complete")
        return

    if args.stage == "score":
        score_fracs(rt)


def score_fracs(rt) -> None:
    import pandas as pd
    import connected_scorer as cs
    from experiments.revalidate_fold_local import score_official
    from optimize_wave6 import make_prediction_param, fold_frame
    from optimize_wave13 import build_ab
    from optimize_wave15 import daily_ranks, weighted_rank_blend, DONOR
    from optimize_wave18 import lift
    from src.scoring import Panel
    from experiments.r6_topk import fixed_prediction  # noqa: F401  (import parity with training)

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
    cache = {"w5a": daily_ranks(w5a, valid, dates), "slow16": daily_ranks(slow16, valid, dates)}
    blended = weighted_rank_blend([w5a, slow16], [1 - PARTNER_WEIGHT, PARTNER_WEIGHT], cache, valid,
                                  dates, ("w5a", "slow16"))
    orderer = np.where(blended > -9.0, blended + TIE_EPS * tie_key, blended) + TIE_EPS * tie_key

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

    masks = {str(yy): (dates >= yy * 10000 + 101) & (dates <= yy * 10000 + 1231) for yy in YEARS}
    half = {"2020_2022": np.zeros(len(dates), dtype=bool),
            "2023_2024": np.zeros(len(dates), dtype=bool)}
    for yy in (2020, 2021, 2022):
        half["2020_2022"] |= masks[str(yy)]
    for yy in (2023, 2024):
        half["2023_2024"] |= masks[str(yy)]

    results: dict = {}
    proofs: dict = {}

    def dump() -> list:
        arms = sorted(((v["connected_final_score"], k, v) for k, v in results.items()
                       if "connected_final_score" in v), reverse=True)
        payload = {"status": "running", "updated_at_local": time.strftime("%Y-%m-%dT%H:%M:%S"),
                   "purpose": "sweep the Top-K objective's fraction, hard-coded at n//10 until wave 24",
                   "seed": SEED, "m_frac": M_FRAC, "tie_break_eps": TIE_EPS,
                   "harness_proofs": proofs, "current_best_before_this_wave": CURRENT_BEST,
                   "reference_halves": {"2020_2022": REF_HALF_DEV, "2023_2024": REF_HALF_CONF},
                   "results": results, "n_scored": len(arms),
                   "ranking": [{"arm": k, "connected_final_score": s, "margin_full": v["margin_full"],
                                "margin_2020_2022": v["margin_2020_2022"],
                                "margin_2023_2024": v["margin_2023_2024"],
                                "wins_both_halves_vs_m0985_reference": v["wins_both_halves"],
                                "ic_mean": v["connected_metrics"]["ic_mean"],
                                "annual_excess": v["connected_metrics"]["annual_excess"],
                                "mean_turnover": v["connected_metrics"]["mean_turnover"],
                                "donor_standalone_excess": v["donor_standalone_excess"]}
                               for s, k, v in arms],
                   "best": arms[0][1] if arms else None,
                   "best_connected_final_score": arms[0][0] if arms else None,
                   "no_test_period_data_read": True, "source_sha256": sha(Path(__file__))}
        (HERE / "wave31_results.json").write_text(
            json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        return arms

    # score whatever has been trained, so the stage can be re-run as more fractions land
    available = sorted({float(p.name.split("_f")[1][:4]) for p in RAW.glob(f"topk_seed{SEED}_f*_*.parquet")})
    log(f"trained fractions available: {available}")
    for frac in available:
        raws = {}
        missing = False
        for year in YEARS:
            path = RAW / f"topk_seed{SEED}_f{frac:.2f}_{year}.parquet"
            if not path.exists():
                log(f"frac {frac:.2f}: missing {path.name}, skipped")
                missing = True
                break
            raws[year] = pl.read_parquet(path)["pred_raw"].to_numpy().astype(np.float64)
        if missing:
            continue
        finished = postprocess(raws)
        promote = np.where(np.isfinite(finished) & (finished > -9.0),
                           finished + TIE_EPS * tie_key, finished)
        donor, lift_stats = lift(promote, slow16_fin, pdf)
        hybrid, stats = build_ab(donor, orderer, orderer, dates, flags, codes, n_codes, M_FRAC)
        metrics, _ = score_official(combined, hybrid)
        standalone, _ = score_official(combined, finished)
        halves = {}
        for label, mask in half.items():
            sub, _ = score_official(combined.filter(pl.Series(mask)), hybrid[mask])
            halves[label] = sub["final_score"]
        name = f"frac{frac:.2f}"
        results[name] = {"frac": frac, "connected_final_score": metrics["final_score"],
                         "connected_metrics": metrics, "halves": halves,
                         "lift_stats": lift_stats,
                         "donor_standalone_connected": standalone["final_score"],
                         "donor_standalone_excess": standalone["annual_excess"],
                         "donor_standalone_ic": standalone["ic_mean"],
                         "margin_full": metrics["final_score"] - CURRENT_BEST,
                         "margin_2020_2022": halves["2020_2022"] - REF_HALF_DEV,
                         "margin_2023_2024": halves["2023_2024"] - REF_HALF_CONF,
                         "wins_both_halves": bool(halves["2020_2022"] > REF_HALF_DEV
                                                  and halves["2023_2024"] > REF_HALF_CONF),
                         "boundary_tie_days": stats["boundary_tie_days"],
                         "swaps": stats["swaps"],
                         "mean_retention_ratio": stats["mean_retention_ratio"]}
        log(f"{name:10s} CONNECTED {metrics['final_score']:.9f} "
            f"({metrics['final_score'] - CURRENT_BEST:+.2e}) | ic {metrics['ic_mean']:.6f} | "
            f"exc {metrics['annual_excess']:.6f} | turn {metrics['mean_turnover']:.6f} | "
            f"donor standalone exc {standalone['annual_excess']:.6f} | 2020-22 "
            f"{halves['2020_2022'] - REF_HALF_DEV:+.2e} | 2023-24 "
            f"{halves['2023_2024'] - REF_HALF_CONF:+.2e}")
        if abs(frac - 0.10) < 1e-12:
            proofs["P_frac0.10_reproduces_the_reference_donor"] = {
                "scored": metrics["final_score"], "expected_reference_donor_score": 0.44319055217888365,
                "abs_diff": abs(metrics["final_score"] - 0.44319055217888365),
                "note": "frac 0.10 with the causal tie-break on the promote source must reproduce the "
                        "shipped nested donor's score; wave 24 already verified this"}
        dump()

    arms = dump()
    payload = json.loads((HERE / "wave31_results.json").read_text(encoding="utf-8"))
    payload["status"] = "complete"
    payload["completed_at_local"] = time.strftime("%Y-%m-%dT%H:%M:%S")
    (HERE / "wave31_results.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("\n| frac | k as share of day | CONNECTED | margin | IC | excess | turnover | donor exc | both halves |")
    print("|---|---|---|---|---|---|---|---|---|")
    for s, name, v in arms:
        m = v["connected_metrics"]
        print(f"| {v['frac']:.2f} | {v['frac']*100:.0f}% | **{s:.9f}** | {v['margin_full']:+.2e} | "
              f"{m['ic_mean']:.6f} | {m['annual_excess']:.6f} | {m['mean_turnover']:.6f} | "
              f"{v['donor_standalone_excess']:.6f} | {'YES' if v['wins_both_halves'] else 'no'} |")


if __name__ == "__main__":
    main()
