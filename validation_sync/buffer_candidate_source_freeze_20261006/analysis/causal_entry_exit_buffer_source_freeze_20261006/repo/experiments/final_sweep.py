"""Final sweep: every remaining optimization candidate under one frozen protocol.

The suite exists because the user asked that no plausible lever go untested. The
protocol is frozen before any scoring and uses the project's standing adoption
gate: a candidate is adoptable only if it strictly raises the released official
composite in 2022, 2023 AND 2024. Every candidate is additionally reported under
both the two-year mean and the maximin criterion so the final adoption decision
can be made once, with the whole table in hand, rather than by switching rules
mid-suite.

Candidates already covered by frozen failure records are deliberately NOT
retried: sample weighting, feature expansion, market features, seed ensembles,
OOF Top weighting, equal-day weighting and within-Top reordering. Re-running them
would violate their own protocols and only add selection bias.

Structural fact that shapes the candidate list: the released 25% pooled blend
never changes the official Top set (turnover deltas are exactly zero and the
entire historical excess delta traces to boundary ties), so Excess and Turnover
are controlled solely by the backbone signal and its post-processing. Candidates
therefore target either the post-processing retention rule or the backbone itself.
"""
from __future__ import annotations

import argparse
import json
import time
from pathlib import Path

import numpy as np
import polars as pl
from scipy.stats import rankdata

from run import ROOT
from src.scoring import Panel, add_top_persistence, make_scores, restore_lower_ranks
from experiments.bonus_extension import (AUXILIARY, FOLD, file_hash, load_auxiliary,
                                         load_panel, release_scores)
from experiments.official_seed_development import official_score

OUT = ROOT / "experiments" / "final_sweep_eval"
NN_CACHE = "experiments/sequence_ensemble_eval/nn_raw_{year}.parquet"
DEVELOPMENT_YEARS = (2022, 2023)
DIAGNOSTIC_YEAR = 2024
NUMERIC_TOLERANCE = 1e-12
RETAIN_CONSTANT = 1.0
RELEASED = {"alpha": 0.9, "bonus": 0.3, "rule": "standard", "ens_weight": 0.0,
            "blend_weight": 0.25}

CANDIDATES = [
    {"key": "baseline_released", **RELEASED},
    {"key": "T1a_alpha0.80", **{**RELEASED, "alpha": 0.80}},
    {"key": "T1b_alpha0.95", **{**RELEASED, "alpha": 0.95}},
    {"key": "T1b_alpha0.97", **{**RELEASED, "alpha": 0.97}},
    {"key": "T1c_ens0.5_alpha0.93", **{**RELEASED, "ens_weight": 0.5, "alpha": 0.93}},
    {"key": "T1c_ens0.5_alpha0.95", **{**RELEASED, "ens_weight": 0.5, "alpha": 0.95}},
    {"key": "T1c_ens0.5_alpha0.97", **{**RELEASED, "ens_weight": 0.5, "alpha": 0.97}},
    {"key": "T1d_ens0.20_alpha0.90", **{**RELEASED, "ens_weight": 0.20}},
    {"key": "T1d_ens0.35_alpha0.90", **{**RELEASED, "ens_weight": 0.35}},
    {"key": "T1e_hysteresis_buffer0.30", **{**RELEASED, "rule": "hysteresis", "buffer": 0.30}},
    {"key": "T1f_min_hold2_floor0.20", **{**RELEASED, "rule": "min_hold", "hold": 2, "floor": 0.20}},
]

PROTOCOL = {
    "experiment": "final_sweep_all_remaining_levers",
    "candidates": CANDIDATES,
    "pipeline": "candidate retention rule and alpha applied to the backbone raw signal, then the "
                "released protected-block rank restoration with top_current_weight=1.0, then the "
                "released 25% top-only pooled blend; nothing else changes",
    "scorer": "Unmodified evaluate.py via official_score: float17 CSV round trip, original Float64 "
              "labels, pandas default descending tie order",
    "development_years": list(DEVELOPMENT_YEARS),
    "diagnostic_year": DIAGNOSTIC_YEAR,
    "baseline_anchor": "the baseline_released candidate must reproduce the released composite for "
                       "2022, 2023 and 2024 to within 1e-12 before any candidate is scored",
    "adoption_gate": "strict improvement over the released composite in 2022 AND 2023 (development) "
                     "and in 2024 (diagnostic). A candidate failing the development gate never sees "
                     "2024.",
    "reporting": "every candidate is reported under both the two-year mean and the maximin "
                 "criterion, with paired HAC intervals on daily composite contributions; the "
                 "criteria are descriptive and do not override the adoption gate",
    "prohibited_after_results": [
        "Adding, removing or redefining any candidate",
        "Re-scoring any year or re-running a stage whose output already exists",
        "Switching the adoption gate or the reported criteria",
        "Retrying any candidate already covered by a frozen failure record",
        "Modifying the release, its manifest, or any frozen source or prior experiment directory",
    ],
    "limitations": [
        "2022-2024 have been examined across roughly twenty prior rounds; none is a blind holdout.",
        "With this many candidates on two development years, at least one will look good by "
        "chance; the three-year strict gate is the only protection and it is deliberately harsh.",
        "Retention-rule candidates change the official Top set, so their turnover and excess move "
        "together; a gain in one year can be a regime artifact.",
    ],
}


def log(message: str) -> None:
    print(f"[{time.strftime('%H:%M:%S')}] {message}", flush=True)


def rank_average(left: np.ndarray, right: np.ndarray, weight: float,
                 valid: np.ndarray) -> np.ndarray:
    shape = valid.shape
    out = np.full(shape, -10.0, dtype=np.float64)
    left = np.asarray(left, dtype=np.float64).reshape(shape)
    right = np.asarray(right, dtype=np.float64).reshape(shape)
    for day in range(shape[0]):
        keep = valid[day] & np.isfinite(left[day]) & np.isfinite(right[day])
        count = int(keep.sum())
        if not count:
            continue
        out[day][keep] = ((1 - weight) * rankdata(left[day][keep], method="average") / count
                          + weight * rankdata(right[day][keep], method="average") / count)
    return out.reshape(-1)


def retention_scores(panel: Panel, raw: np.ndarray, alpha: float, bonus: float,
                     rule: str, buffer: float = 0.0, hold: int = 1,
                     floor: float = 0.2) -> np.ndarray:
    """Post-smoothing retention rule; 'standard' is exactly the released one."""
    if rule == "standard":
        return add_top_persistence(panel, make_scores(panel, raw, alpha), bonus)
    smoothed = make_scores(panel, raw, alpha).reshape(panel.valid_price.shape)
    out = smoothed.copy()
    prior = np.zeros(panel.rows_per_day, dtype=bool)
    prior2 = np.zeros(panel.rows_per_day, dtype=bool)
    for day in range(len(panel.dates)):
        tradeable = panel.up[day] == 0
        count = int(tradeable.sum())
        rank_fraction = np.ones(panel.rows_per_day, dtype=float)
        if count:
            indices = np.flatnonzero(tradeable)
            order = np.argsort(-smoothed[day, indices], kind="stable")
            rank_fraction[indices[order]] = np.arange(count) / count
        if rule == "hysteresis":
            retain = prior & (rank_fraction < 0.1 * (1.0 + buffer))
        elif rule == "min_hold":
            retain = prior & prior2 & (rank_fraction < floor)
        else:
            raise ValueError(f"Unknown retention rule {rule}")
        out[day, retain] += RETAIN_CONSTANT
        if count >= 100:
            indices = np.flatnonzero(tradeable)
            selected = indices[np.argsort(-out[day, indices], kind="stable")[:max(count // 10, 1)]]
            prior2, prior = prior.copy(), np.zeros(panel.rows_per_day, dtype=bool)
            prior[selected] = True
        else:
            prior2, prior = prior.copy(), np.zeros(panel.rows_per_day, dtype=bool)
    return out.reshape(-1)


def blend_top_only(panel: Panel, stable: np.ndarray, raw: np.ndarray,
                   auxiliary: np.ndarray, weight: float) -> np.ndarray:
    """Released protected-Top-only blend, parameterized by the stable scores."""
    shape = panel.valid_price.shape
    out = restore_lower_ranks(panel, stable, raw, 1.0).reshape(shape)
    stable = np.asarray(stable, dtype=np.float64).reshape(shape)
    raw = np.asarray(raw, dtype=np.float64).reshape(shape)
    auxiliary = np.asarray(auxiliary, dtype=np.float64).reshape(shape)
    for day in range(len(panel.dates)):
        valid = panel.valid_price[day] & np.isfinite(raw[day])
        indices = np.flatnonzero(panel.up[day] == 0)
        n_top = max(len(indices) // 10, 1)
        if not len(indices) or not valid.any():
            continue
        top = indices[np.argsort(-stable[day, indices], kind="stable")[:n_top]]
        if not valid[top].all():
            continue
        protected = valid & (stable[day] >= stable[day, top].min())
        if np.count_nonzero(protected & (panel.up[day] == 0)) != n_top:
            continue
        if not np.isfinite(auxiliary[day, protected]).all():
            continue
        n_upper, n_valid = int(protected.sum()), int(valid.sum())
        base_rank = rankdata(raw[day, protected], method="average") / n_upper
        aux_rank = rankdata(auxiliary[day, protected], method="average") / n_upper
        blended = rankdata((1 - weight) * base_rank + weight * aux_rank, method="average")
        out[day, protected] = (n_valid - n_upper + blended) / n_valid
    return out.reshape(-1)


def candidate_prediction(panel: Panel, auxiliary: np.ndarray, nn_raw: np.ndarray | None,
                         config: dict) -> np.ndarray:
    backbone = panel.frame["pred_raw"].to_numpy().astype(np.float64)
    raw = backbone
    if config["ens_weight"]:
        if nn_raw is None:
            raise AssertionError("Ensemble candidate requires the cached sequence predictions")
        raw = rank_average(backbone, nn_raw, config["ens_weight"], panel.valid_price)
    stable = retention_scores(panel, raw, config["alpha"], config["bonus"], config["rule"],
                              config.get("buffer", 0.0), config.get("hold", 1),
                              config.get("floor", 0.2))
    return blend_top_only(panel, stable, raw, auxiliary, config["blend_weight"])


def write_protocol() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / "protocol.json"
    payload = {**PROTOCOL, "frozen_at_local": time.strftime("%Y-%m-%dT%H:%M:%S"),
               "source_sha256": file_hash(Path(__file__)),
               "released_baseline_scores": {str(k): v for k, v in release_scores().items()}}
    if path.exists():
        existing = json.loads(path.read_text(encoding="utf-8"))
        drift = {k: (existing.get(k), v) for k, v in PROTOCOL.items() if existing.get(k) != v}
        if drift:
            raise SystemExit(f"Protocol already frozen and differs: {drift}")
        log("Protocol already frozen and unchanged")
        return
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    log(f"Froze final-sweep protocol with {len(CANDIDATES)} candidates before any scoring")


def verify_protocol() -> dict:
    path = OUT / "protocol.json"
    if not path.exists():
        raise SystemExit("Run the protocol stage first")
    protocol = json.loads(path.read_text(encoding="utf-8"))
    if protocol["source_sha256"] != file_hash(Path(__file__)):
        raise SystemExit("final_sweep.py changed after the protocol was frozen; stop")
    if protocol["candidates"] != CANDIDATES:
        raise SystemExit("Candidate list differs from the frozen protocol")
    return protocol


def develop() -> None:
    verify_protocol()
    result_path = OUT / "development.json"
    if result_path.exists():
        raise SystemExit("Development results already recorded; preserving them")
    released = release_scores()
    started = time.monotonic()
    candidates: dict[str, dict] = {}
    for year in DEVELOPMENT_YEARS:
        panel = load_panel(year)
        auxiliary = load_auxiliary(year, panel)
        nn_raw = (pl.read_parquet(ROOT / NN_CACHE.format(year=year))
                  .sort("trade_date", "ts_code")["pred_raw"].to_numpy().astype(np.float64))
        for config in CANDIDATES:
            key = config["key"]
            prediction = candidate_prediction(panel, auxiliary, nn_raw, config)
            metrics, daily = official_score(panel, prediction, year)
            item = candidates.setdefault(key, {"config": config, "years": {}})
            item["years"][str(year)] = {k: float(v) for k, v in metrics.items()}
            daily.write_csv(OUT / f"{key}_{year}_daily.csv")
            if key == "baseline_released":
                delta = metrics["final_score"] - released[year]
                if abs(delta) > NUMERIC_TOLERANCE:
                    raise AssertionError(f"{year} baseline anchor off by {delta:.3e}")
                log(f"{year} baseline anchor reproduced {released[year]:.15f} exactly")
            log(f"{year} {key}: score={metrics['final_score']:.9f} ic={metrics['ic_mean']:.6f} "
                f"excess={metrics['annual_excess']:.6f} turn={metrics['mean_turnover']:.6f}")
        del panel, auxiliary, nn_raw

    baseline = candidates["baseline_released"]["years"]
    for key, item in candidates.items():
        years = item["years"]
        deltas = {y: years[y]["final_score"] - baseline[y]["final_score"]
                  for y in map(str, DEVELOPMENT_YEARS)}
        item["score_delta"] = deltas
        item["turnover_delta"] = {y: years[y]["mean_turnover"] - baseline[y]["mean_turnover"]
                                  for y in map(str, DEVELOPMENT_YEARS)}
        item["ic_delta"] = {y: years[y]["ic_mean"] - baseline[y]["ic_mean"]
                            for y in map(str, DEVELOPMENT_YEARS)}
        item["excess_delta"] = {y: years[y]["annual_excess"] - baseline[y]["annual_excess"]
                                for y in map(str, DEVELOPMENT_YEARS)}
        item["passes_development_gate"] = all(v > NUMERIC_TOLERANCE for v in deltas.values())
        item["two_year_mean"] = sum(years[y]["final_score"] for y in map(str, DEVELOPMENT_YEARS)) / 2
        item["two_year_minimax"] = min(years[y]["final_score"] for y in map(str, DEVELOPMENT_YEARS))
        item["mean_delta"] = item["two_year_mean"] - (
            sum(baseline[y]["final_score"] for y in map(str, DEVELOPMENT_YEARS)) / 2)
        item["minimax_delta"] = item["two_year_minimax"] - min(
            baseline[y]["final_score"] for y in map(str, DEVELOPMENT_YEARS))

    passing = [k for k, v in candidates.items() if v["passes_development_gate"]]
    output = {
        "stage": "develop",
        "generated_at_local": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "elapsed_seconds": time.monotonic() - started,
        "protocol_sha256": file_hash(OUT / "protocol.json"),
        "development_years": list(DEVELOPMENT_YEARS),
        "candidates": candidates,
        "candidates_passing_development_gate": passing,
        "ranking_by_two_year_mean": sorted(candidates, key=lambda k: -candidates[k]["two_year_mean"]),
        "ranking_by_two_year_minimax": sorted(candidates, key=lambda k: -candidates[k]["two_year_minimax"]),
        "caveat": PROTOCOL["limitations"],
    }
    result_path.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")
    log(f"DEVELOPMENT: {len(passing)} of {len(CANDIDATES)} candidates pass the two-year gate: {passing}")
    log("Best by mean: %s | best by minimax: %s" % (output["ranking_by_two_year_mean"][0],
                                                    output["ranking_by_two_year_minimax"][0]))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("stage", choices=("protocol", "develop", "diagnose"))
    arguments = parser.parse_args()
    if arguments.stage == "protocol":
        write_protocol()
    elif arguments.stage == "develop":
        develop()
    else:
        from experiments.final_sweep_diagnose import diagnose
        diagnose()
