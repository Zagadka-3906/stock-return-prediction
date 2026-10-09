"""Predeclared post-processing scan: extend the Top persistence bonus above 0.3.

Only the persistence bonus varies. Alpha, rank restoration, the internal Top
reorder weight and the 25% protected-Top pooled blend stay frozen at the
released pooled_rms25 configuration. No model is retrained: both the rank
backbone and the pooled auxiliary are read from their frozen historical caches.

Rationale recorded before scoring. The original joint search covered
bonus in {0.05, 0.15, 0.30} only, and selected 0.30 as a boundary solution of
the maximin rule: 2022 already peaked at 0.15 and fell to 0.4200 at 0.30, while
2023 was still rising. Official Jaccard turnover fell monotonically across that
grid (0.1146 -> 0.0649 -> 0.0358 in 2022), and the turnover term supplies about
70% of the composite score at its current 3.75%, leaving roughly +0.011 of
theoretical headroom. Values above 0.30 were never evaluated.

Stages refuse to overwrite existing evidence. The 2024 diagnostic is reachable
only if the frozen development gate passes.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import time
from pathlib import Path

import numpy as np
import polars as pl
from scipy.stats import rankdata

from run import ROOT
from src.scoring import Panel, add_top_persistence, make_scores, postprocess_scores
from experiments.official_seed_development import official_score

OUT = ROOT / "experiments" / "bonus_extension_eval"
FOLD = "validation/fold_{year}.parquet"
AUXILIARY = "experiments/return_pooled_eval/return_pooled1_99_{year}.parquet"
AUTHORITY = "experiments/return_pooled_eval/decision.json"

SELECTION_YEARS = (2022, 2023)
DIAGNOSTIC_YEAR = 2024
BLEND_WEIGHT = 0.25
FROZEN = {"alpha": 0.9, "restore_lower": True, "top_current_weight": 1.0}
BASE_BONUS = 0.3
CANDIDATE_BONUS = (0.4, 0.5, 0.6)
NUMERIC_TOLERANCE = 1e-12
BASELINE_KEY = "release_bonus0.3"

PROTOCOL = {
    "experiment": "top_persistence_bonus_extension_above_released_value",
    "candidate_key_prefix": "bonus",
    "question": "Does a stronger causal Top retention bonus lower official Jaccard turnover "
                "enough to raise the composite score, once the released 25% pooled blend is applied?",
    "frozen": {
        "alpha": FROZEN["alpha"],
        "restore_lower": FROZEN["restore_lower"],
        "top_current_weight": FROZEN["top_current_weight"],
        "blend": {"mode": "top_only", "weight": BLEND_WEIGHT},
        "baseline_bonus": BASE_BONUS,
        "rank_backbone": "models/final_lightgbm.txt fold caches in validation/fold_{year}.parquet",
        "pooled_auxiliary": "experiments/return_pooled_eval/return_pooled1_99_{year}.parquet",
        "retraining": "None; frozen historical caches only",
    },
    "candidate_bonus": list(CANDIDATE_BONUS),
    "selection_years": list(SELECTION_YEARS),
    "diagnostic_year": DIAGNOSTIC_YEAR,
    "scorer": "Unmodified evaluate.py through official_score: float17 CSV round trip, "
              "original Float64 labels, pandas default descending tie order",
    "selection_rule": "Among candidates whose 2022 AND 2023 official composite scores both exceed "
                      "the frozen release baseline by more than 1e-12, select the one maximizing "
                      "min(score_2022, score_2023). Exact ties prefer the smaller bonus. "
                      "If no candidate satisfies the strict two-year condition, stop and adopt nothing.",
    "diagnostic_gate": "The selected candidate must also raise the 2024 official composite score by "
                       "more than 1e-12. Otherwise do not adopt.",
    "veto_note": "Consistent with the released score-first preference, IC and HAC intervals do not "
                 "veto, but paired HAC intervals are reported in full and the cumulative selection "
                 "bias across roughly twenty prior rounds is not corrected.",
    "prohibited_after_results": [
        "Adding, removing or substituting any bonus value",
        "Changing the tie, sort or label-filtering convention",
        "Changing alpha, restore_lower, top_current_weight or the blend weight",
        "Re-scoring a year to obtain a different number",
        "Overwriting the release, official artifacts or any prior experiment directory",
        "Reading test labels or any label-availability mask when constructing predictions",
    ],
    "baseline_anchor": {
        "authority": AUTHORITY,
        "requirement": "The recomputed bonus=0.3 candidate must equal the frozen release composite "
                       "score for all three years to within 1e-12 before any candidate is scored.",
    },
    "limitations": [
        "2022-2024 have been examined roughly twenty times and are historical diagnosis, not a blind holdout.",
        "A stronger retention bonus holds stale signals longer, so Top excess return may fall faster "
        "than the turnover term gains; the 2022 gradient already shows this between 0.15 and 0.30.",
        "Official turnover Top and return Top use different missing-label filters; an unchanged or lower "
        "official Jaccard distance is not an executable after-cost portfolio result.",
        "Predictions remain ordinal rank scores, not calibrated next-day returns.",
    ],
}


def log(message: str) -> None:
    print(message, flush=True)


def file_hash(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def release_scores() -> dict[int, float]:
    """Read the frozen released composite scores from their own decision record."""
    record = json.loads((ROOT / AUTHORITY).read_text(encoding="utf-8"))
    if record.get("selected_candidate") != "protected_return_pooled_w0p25":
        raise AssertionError("Authority record is not the released pooled_rms25 candidate")
    return {int(year): float(item["candidate_score"]) for year, item in record["years"].items()}


def load_panel(year: int) -> Panel:
    return Panel.from_frame(pl.read_parquet(ROOT / FOLD.format(year=year)))


def load_auxiliary(year: int, panel: Panel) -> np.ndarray:
    """Read keys and auxiliary predictions only; never a cached label column."""
    frame = pl.read_parquet(ROOT / AUXILIARY.format(year=year),
                            columns=["ts_code", "trade_date", "pred_raw"]).sort("trade_date", "ts_code")
    if not frame.select("trade_date", "ts_code").equals(panel.frame.select("trade_date", "ts_code")):
        raise AssertionError(f"Auxiliary cache keys differ from the fold panel: {year}")
    raw = frame["pred_raw"].to_numpy().astype(np.float64)
    if not np.isfinite(raw.reshape(panel.valid_price.shape)[panel.valid_price]).all():
        raise AssertionError(f"Auxiliary cache has a nonfinite valid-price prediction: {year}")
    return raw


def blend_top_only(panel: Panel, auxiliary: np.ndarray, bonus: float, weight: float) -> np.ndarray:
    """Released protected-Top-only blend, parameterized solely by the bonus.

    Reads current and past predictions, prices and limit-up flags only. Returns
    and label availability are never consulted. Days whose protected block is
    ambiguous or contains an invalid observation keep the post-processed state.
    """
    config = {**FROZEN, "bonus": bonus}
    shape = panel.valid_price.shape
    base_raw = panel.frame["pred_raw"].to_numpy().astype(np.float64)
    out = postprocess_scores(panel, base_raw, **config).reshape(shape)
    stable = add_top_persistence(panel, make_scores(panel, base_raw, config["alpha"]),
                                 bonus).reshape(shape)
    base_raw = base_raw.reshape(shape)
    auxiliary = np.asarray(auxiliary, dtype=np.float64).reshape(shape)
    for day in range(len(panel.dates)):
        valid = panel.valid_price[day] & np.isfinite(base_raw[day])
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
        base_rank = rankdata(base_raw[day, protected], method="average") / n_upper
        auxiliary_rank = rankdata(auxiliary[day, protected], method="average") / n_upper
        blended = rankdata((1 - weight) * base_rank + weight * auxiliary_rank, method="average")
        out[day, protected] = (n_valid - n_upper + blended) / n_valid
    return out.reshape(-1)


def causality_checks(panel: Panel, auxiliary: np.ndarray, bonus: float) -> dict:
    """Label perturbation and causal-prefix invariance for a candidate bonus."""
    prediction = blend_top_only(panel, auxiliary, bonus, BLEND_WEIGHT)
    rng = np.random.default_rng(260926)
    perturbed = Panel.from_frame(panel.frame.with_columns(
        pl.Series("y_ret_1d", rng.normal(size=len(panel.frame)))))
    if not np.array_equal(prediction, blend_top_only(perturbed, auxiliary, bonus, BLEND_WEIGHT)):
        raise AssertionError("Candidate prediction reads return labels")
    rows = 50 * panel.rows_per_day
    prefix = Panel.from_frame(panel.frame.head(rows))
    if not np.array_equal(prediction[:rows],
                          blend_top_only(prefix, auxiliary[:rows], bonus, BLEND_WEIGHT)):
        raise AssertionError("Candidate prediction is not causal over a 50-day prefix")
    if not np.isfinite(prediction).all():
        raise AssertionError("Candidate prediction is not finite everywhere")
    return {"label_perturbation_invariant": True, "prefix_50_days_exact": True,
            "finite_all_rows": True, "bonus": bonus}


def dependencies(years: tuple[int, ...]) -> dict[str, str]:
    sources = {str(Path(__file__).relative_to(ROOT)).replace("\\", "/"): file_hash(Path(__file__)),
               "evaluate.py": file_hash(ROOT / "evaluate.py"),
               "src/scoring.py": file_hash(ROOT / "src/scoring.py"),
               "experiments/official_seed_development.py": file_hash(ROOT / "experiments/official_seed_development.py"),
               "experiments/cached_recheck.py": file_hash(ROOT / "experiments/cached_recheck.py"),
               AUTHORITY: file_hash(ROOT / AUTHORITY)}
    for year in years:
        for template in (FOLD, AUXILIARY):
            relative = template.format(year=year)
            sources[relative] = file_hash(ROOT / relative)
    return dict(sorted(sources.items()))


def anchor(panel: Panel, auxiliary: np.ndarray, year: int, expected: float) -> dict:
    """Prove the parameterized pipeline reproduces the released number exactly."""
    from experiments.cached_recheck import BASE_CONFIG, make_prediction
    reference = make_prediction(panel, auxiliary, "top_only", BLEND_WEIGHT)
    if BASE_CONFIG != {**FROZEN, "bonus": BASE_BONUS}:
        raise AssertionError("Released post-processing configuration changed")
    mine = blend_top_only(panel, auxiliary, BASE_BONUS, BLEND_WEIGHT)
    if not np.array_equal(reference, mine):
        raise AssertionError("Parameterized blend differs from the released implementation")
    metrics, daily = official_score(panel, mine, year)
    delta = metrics["final_score"] - expected
    if abs(delta) > NUMERIC_TOLERANCE:
        raise AssertionError(f"{year} baseline anchor differs from the release by {delta:.3e}")
    return {"year": year, "final_score": metrics["final_score"], "expected": expected,
            "absolute_delta": abs(delta), "matches_released_implementation": True,
            "daily": daily}


def write_protocol() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / "protocol.json"
    if path.exists():
        if json.loads(path.read_text(encoding="utf-8")) != PROTOCOL:
            raise SystemExit("Protocol already frozen and differs; do not rewrite it after seeing results")
        log("Protocol already frozen and unchanged")
        return
    payload = {**PROTOCOL, "frozen_at_local": time.strftime("%Y-%m-%dT%H:%M:%S"),
               "source_sha256": file_hash(Path(__file__)),
               "release_baseline_authority_sha256": file_hash(ROOT / AUTHORITY),
               "release_baseline_scores": {str(k): v for k, v in release_scores().items()}}
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    log(f"Froze protocol before any scoring: bonus {list(CANDIDATE_BONUS)} vs released {BASE_BONUS}")


def develop() -> None:
    protocol_path = OUT / "protocol.json"
    if not protocol_path.exists():
        raise SystemExit("Run the protocol stage first; the rule must be frozen before scoring")
    protocol = json.loads(protocol_path.read_text(encoding="utf-8"))
    if {k: protocol["frozen"][k] for k in FROZEN} != FROZEN or protocol["candidate_bonus"] != list(CANDIDATE_BONUS):
        raise SystemExit("Protocol on disk differs from this source; stop rather than silently rescore")
    result_path = OUT / "development.json"
    if result_path.exists():
        raise SystemExit("Development results already exist; preserving them instead of rescoring")

    expected = release_scores()
    started = time.monotonic()
    candidates: dict[str, dict] = {}
    anchors, daily_evidence = {}, {}
    for year in SELECTION_YEARS:
        panel = load_panel(year)
        auxiliary = load_auxiliary(year, panel)
        anchored = anchor(panel, auxiliary, year, expected[year])
        daily_evidence[f"{BASELINE_KEY}_{year}"] = anchored.pop("daily")
        anchors[str(year)] = anchored
        log(f"{year} anchor reproduced release score {expected[year]:.15f} exactly")

        for bonus in (BASE_BONUS, *CANDIDATE_BONUS):
            key = BASELINE_KEY if bonus == BASE_BONUS else f"bonus{bonus:g}"
            item = candidates.setdefault(key, {"bonus": bonus, "years": {}})
            prediction = blend_top_only(panel, auxiliary, bonus, BLEND_WEIGHT)
            metrics, daily = official_score(panel, prediction, year)
            item["years"][str(year)] = metrics
            daily_evidence[f"{key}_{year}"] = daily
            log(f"{year} {key}: score={metrics['final_score']:.9f} ic={metrics['ic_mean']:.6f} "
                f"excess={metrics['annual_excess']:.6f} turn={metrics['mean_turnover']:.6f}")
        del panel, auxiliary

    baseline = candidates[BASELINE_KEY]
    passing = []
    for key, item in candidates.items():
        if key == BASELINE_KEY:
            continue
        deltas = {year: item["years"][year]["final_score"] - baseline["years"][year]["final_score"]
                  for year in map(str, SELECTION_YEARS)}
        item["score_delta"] = deltas
        item["turnover_delta"] = {year: item["years"][year]["mean_turnover"] - baseline["years"][year]["mean_turnover"]
                                  for year in map(str, SELECTION_YEARS)}
        item["ic_delta"] = {year: item["years"][year]["ic_mean"] - baseline["years"][year]["ic_mean"]
                            for year in map(str, SELECTION_YEARS)}
        item["annual_excess_delta"] = {year: item["years"][year]["annual_excess"] - baseline["years"][year]["annual_excess"]
                                       for year in map(str, SELECTION_YEARS)}
        item["improves_both_selection_years"] = all(v > NUMERIC_TOLERANCE for v in deltas.values())
        item["minimum_annual_score"] = min(item["years"][year]["final_score"] for year in map(str, SELECTION_YEARS))
        if item["improves_both_selection_years"]:
            passing.append(key)

    selected = None
    if passing:
        selected = min(passing, key=lambda k: (-candidates[k]["minimum_annual_score"], candidates[k]["bonus"]))
    output = {
        "selection_years": list(SELECTION_YEARS),
        "selection_rule": protocol["selection_rule"],
        "scorer": protocol["scorer"],
        "baseline_key": BASELINE_KEY,
        "baseline_anchors": anchors,
        "candidates": candidates,
        "candidates_passing_two_year_gate": passing,
        "selected_key": selected,
        "development_gate_passed": selected is not None,
        "elapsed_seconds": time.monotonic() - started,
        "source_and_input_sha256": dependencies(SELECTION_YEARS),
        "caveat": "Exploratory development over historical folds that have been examined many times; "
                  "not an untouched holdout and not an official 2025-2026 test score.",
    }
    for key, daily in daily_evidence.items():
        daily.write_csv(OUT / f"official_{key}_daily.csv")
    result_path.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")
    log(f"DEVELOPMENT gate {'PASSED' if selected else 'FAILED'}; selected={selected}")
    if selected is None:
        log("No bonus above 0.3 raised both 2022 and 2023. Stopping; the release is unchanged.")


def diagnose() -> None:
    result_path = OUT / "development.json"
    if not result_path.exists():
        raise SystemExit("Run develop first")
    development = json.loads(result_path.read_text(encoding="utf-8"))
    if not development["development_gate_passed"]:
        raise SystemExit("Development gate failed; the frozen protocol does not permit a 2024 diagnostic")
    decision_path = OUT / "decision.json"
    if decision_path.exists():
        raise SystemExit("Decision already recorded; preserving it instead of rescoring 2024")

    selected = development["selected_key"]
    bonus = development["candidates"][selected]["bonus"]
    expected = release_scores()[DIAGNOSTIC_YEAR]
    panel = load_panel(DIAGNOSTIC_YEAR)
    auxiliary = load_auxiliary(DIAGNOSTIC_YEAR, panel)
    anchored = anchor(panel, auxiliary, DIAGNOSTIC_YEAR, expected)
    baseline_daily = anchored.pop("daily")
    anchored.pop("year", None)
    log(f"{DIAGNOSTIC_YEAR} anchor reproduced release score {expected:.15f} exactly")

    prediction = blend_top_only(panel, auxiliary, bonus, BLEND_WEIGHT)
    metrics, daily = official_score(panel, prediction, DIAGNOSTIC_YEAR)
    baseline_metrics, _ = official_score(panel, blend_top_only(panel, auxiliary, BASE_BONUS, BLEND_WEIGHT),
                                         DIAGNOSTIC_YEAR)
    checks = causality_checks(panel, auxiliary, bonus)
    baseline_daily.write_csv(OUT / f"official_{BASELINE_KEY}_{DIAGNOSTIC_YEAR}_daily.csv")
    daily.write_csv(OUT / f"official_{selected}_{DIAGNOSTIC_YEAR}_daily.csv")

    delta = metrics["final_score"] - baseline_metrics["final_score"]
    adopted = delta > NUMERIC_TOLERANCE
    decision = {
        "experiment": PROTOCOL["experiment"],
        "selected_candidate": selected,
        "bonus": bonus,
        "baseline_key": BASELINE_KEY,
        "diagnostic_year": DIAGNOSTIC_YEAR,
        "diagnostic_2024_score_gate_passed": adopted,
        "years": {str(DIAGNOSTIC_YEAR): {
            "reference_score": baseline_metrics["final_score"],
            "candidate_score": metrics["final_score"],
            "score_delta": delta,
            "ic_delta": metrics["ic_mean"] - baseline_metrics["ic_mean"],
            "annual_excess_delta": metrics["annual_excess"] - baseline_metrics["annual_excess"],
            "turnover_delta": metrics["mean_turnover"] - baseline_metrics["mean_turnover"],
            "candidate_metrics": metrics,
            "reference_metrics": baseline_metrics,
        }},
        "causality_checks": checks,
        "baseline_anchor": anchored,
        "recommended_for_next_version": adopted,
        "deployed_to_production": False,
        "official_submission_or_report_changed": False,
        "score_first_rule_changed_after_results": False,
        "decision": ("Adopt candidate for the next version under the predeclared score-first rule."
                     if adopted else
                     "Do not adopt. 2024 did not meet the predeclared strict improvement condition; "
                     "retain the released bonus=0.3 configuration. Do not try another bonus value."),
        "source_and_input_sha256": dependencies((DIAGNOSTIC_YEAR,)),
        "caveats": PROTOCOL["limitations"],
    }
    decision_path.write_text(json.dumps(decision, ensure_ascii=False, indent=2), encoding="utf-8")
    log(f"{DIAGNOSTIC_YEAR} candidate score={metrics['final_score']:.9f} "
        f"baseline={baseline_metrics['final_score']:.9f} delta={delta:+.9f}")
    log(f"DECISION: {'RECOMMEND' if adopted else 'DO NOT ADOPT'}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("stage", choices=("protocol", "develop", "diagnose"))
    arguments = parser.parse_args()
    if arguments.stage == "protocol":
        write_protocol()
    elif arguments.stage == "develop":
        develop()
    else:
        diagnose()
