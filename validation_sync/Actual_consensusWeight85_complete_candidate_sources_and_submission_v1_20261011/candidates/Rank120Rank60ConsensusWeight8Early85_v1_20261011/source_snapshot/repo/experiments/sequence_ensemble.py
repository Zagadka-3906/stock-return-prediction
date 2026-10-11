"""Phase 2: does the GBDT+GRU rank ensemble survive the released post-processing stack?

Phase 1 (experiments/sequence_model_eval) established on the 2022 outer fold that
the GRU alone scores below the raw backbone (IC 0.120625 vs 0.127848) but the
equal-weight rank-average ensemble scores above it (0.132087, +3.32%), with raw
annual excess also higher (0.606795 vs 0.568479). Raw predictions carry roughly
77% Jaccard turnover, so a raw IC gain says nothing yet about the released
composite score, which is dominated by the turnover term.

This phase asks the only question that matters for adoption: after substituting
the ensemble for the backbone and running the *unchanged* released pipeline, does
the official composite score improve?

Nothing is retuned. The post-processing configuration, the pooled auxiliary, the
blend weight, the architecture and the epoch count are all frozen at values
chosen before any of these years was scored in this phase.
"""
from __future__ import annotations

import argparse
import json
import time
from pathlib import Path

import numpy as np
import polars as pl
import torch

from run import ROOT, feature_names, fold_cutoff
from src.scoring import Panel
from experiments.bonus_extension import (AUXILIARY, BASE_BONUS, BLEND_WEIGHT, FOLD,
                                         blend_top_only, file_hash, load_auxiliary,
                                         load_panel, release_scores)
from experiments.official_seed_development import official_score
from experiments.sequence_model import (CLIP_STD, OUT as PHASE1_OUT, apply_scaler,
                                        file_hash_of_array, fit_scaler,
                                        load_panel as load_sequence_panel, log)
import experiments.sequence_training as st

OUT = ROOT / "experiments" / "sequence_ensemble_eval"
DEVELOPMENT_YEARS = (2022, 2023)
DIAGNOSTIC_YEAR = 2024
ALL_YEARS = (2022, 2023, 2024)
NUMERIC_TOLERANCE = 1e-12

# Frozen from phase 1's inner-split selection on 2021. Not revisited here.
ARCHITECTURE = "gru_cat"
HIDDEN = 64
WINDOW = 20
EPOCHS = 26
ENSEMBLE_WEIGHT = 0.5

PROTOCOL = {
    "experiment": "rank_ensemble_through_released_pipeline",
    "predecessor": "experiments/sequence_model_eval (phase 1, 2022 raw-IC gate passed)",
    "question": "After substituting the equal-weight rank ensemble of the frozen LightGBM "
                "backbone and the phase-1 GRU for the backbone's raw prediction, and running the "
                "released post-processing and pooled blend unchanged, does the official composite "
                "score improve?",
    "frozen": {
        "architecture": ARCHITECTURE, "hidden": HIDDEN, "window": WINDOW, "epochs": EPOCHS,
        "epoch_provenance": "selected on the 2021 inner split in phase 1; applied unchanged to "
                            "every fold, never chosen on an outer year",
        "ensemble": {"rule": "per-day cross-sectional percentile rank of each raw signal, "
                             "averaged with equal weight", "weight": ENSEMBLE_WEIGHT},
        "postprocess": {"alpha": 0.9, "bonus": BASE_BONUS, "restore_lower": True,
                        "top_current_weight": 1.0},
        "blend": {"mode": "top_only", "weight": BLEND_WEIGHT},
        "pooled_auxiliary": "experiments/return_pooled_eval/return_pooled1_99_{year}.parquet, "
                            "unchanged; still trained on the backbone era and not refitted",
        "normalization": "nonfinite-aware per-feature mean/std fitted on price-valid rows dated "
                         "strictly before fold_cutoff(year), clip +/-5 std, nonfinite to zero",
        "target": "y_rank, the same daily centered cross-sectional percentile the backbone regresses",
        "loss": "negative mean daily cross-sectional Pearson correlation",
        "optimizer": {"type": "Adam", "lr": 1e-3, "weight_decay": 1e-6, "schedule": "none"},
        "seed": 2026,
        "batch_days": 4,
        "substitution_point": "the ensemble replaces pred_raw in the fold panel; every downstream "
                              "step is the released implementation imported unmodified",
    },
    "development_years": list(DEVELOPMENT_YEARS),
    "diagnostic_year": DIAGNOSTIC_YEAR,
    "scorer": "Unmodified evaluate.py via official_score: float17 CSV round trip, original Float64 "
              "labels, pandas default descending tie order",
    "baseline": "the released pooled_rms25 composite scores recorded in "
                "experiments/return_pooled_eval/decision.json",
    "development_gate": "the ensemble composite must strictly exceed the released composite "
                        "(by more than 1e-12) in BOTH 2022 and 2023. Otherwise stop; the "
                        "diagnostic year is not scored and nothing is adopted.",
    "diagnostic_gate": "the ensemble composite must also strictly exceed the released composite in "
                       "2024. Otherwise do not adopt.",
    "determinism_check": "the 2022 fold is retrained from scratch and its raw IC compared with the "
                         "phase-1 record; cuDNN recurrent backward is not bitwise deterministic, so "
                         "the observed drift is reported rather than suppressed",
    "veto_note": "Consistent with the released score-first preference, IC and HAC intervals do not "
                 "veto, but paired HAC intervals on daily composite contributions are reported in "
                 "full and cumulative selection bias is not corrected.",
    "prohibited_after_results": [
        "Retuning alpha, bonus, restore_lower, top_current_weight or the blend weight for the ensemble",
        "Changing the ensemble weight away from 0.5, or using a weighted search",
        "Reselecting architecture, hidden size, window or epoch count",
        "Refitting the pooled auxiliary on ensemble residuals",
        "Re-scoring a year, or scoring 2024 before the development gate is decided",
        "Modifying the release, its manifest, or any frozen source or prior experiment directory",
    ],
    "limitations": [
        "The pooled auxiliary was trained against the backbone; combining it with an ensemble "
        "backbone is untested territory and may interact unfavourably.",
        "The post-processing stack was tuned on the backbone's signal autocorrelation. A different "
        "model may have a different optimal alpha, but retuning is prohibited here by design.",
        "2022-2024 have been examined many times and are historical diagnosis, not a blind holdout.",
        "Phase 1 selected the architecture on 2021, which is inside the 2023 and 2024 training "
        "windows; that is walk-forward legal but means 2021 is not an independent check for those folds.",
        "A pass here is a historical-composite result only; it is not an official 2025-2026 test score.",
    ],
}


def ensemble_signal(panel: Panel, backbone_raw: np.ndarray, nn_raw: np.ndarray) -> np.ndarray:
    """Equal-weight average of per-day cross-sectional percentile ranks."""
    from scipy.stats import rankdata
    shape = panel.valid_price.shape
    left = np.asarray(backbone_raw, dtype=np.float64).reshape(shape)
    right = np.asarray(nn_raw, dtype=np.float64).reshape(shape)
    out = np.full(shape, -10.0, dtype=np.float64)
    for day in range(shape[0]):
        keep = panel.valid_price[day] & np.isfinite(left[day]) & np.isfinite(right[day])
        count = int(keep.sum())
        if not count:
            continue
        ranked = ((1 - ENSEMBLE_WEIGHT) * rankdata(left[day][keep], method="average") / count
                  + ENSEMBLE_WEIGHT * rankdata(right[day][keep], method="average") / count)
        out[day][keep] = ranked
    return out.reshape(-1)


def pipeline(panel: Panel, auxiliary: np.ndarray, raw_signal: np.ndarray) -> np.ndarray:
    """Released post-processing and blend applied to an arbitrary raw backbone signal."""
    substituted = Panel.from_frame(panel.frame.with_columns(
        pl.Series("pred_raw", np.asarray(raw_signal, dtype=np.float64))))
    if not substituted.frame.select("trade_date", "ts_code").equals(
            panel.frame.select("trade_date", "ts_code")):
        raise AssertionError("Signal substitution changed panel key order")
    if not np.array_equal(substituted.valid_price, panel.valid_price):
        raise AssertionError("Signal substitution changed the price-valid mask")
    return blend_top_only(substituted, auxiliary, BASE_BONUS, BLEND_WEIGHT)


def write_protocol() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / "protocol.json"
    phase1 = json.loads((PHASE1_OUT / "decision.json").read_text(encoding="utf-8"))
    if phase1["gate"]["decision"] != "pass":
        raise SystemExit("Phase 1 did not pass; phase 2 is not authorized")
    payload = {**PROTOCOL,
               "frozen_at_local": time.strftime("%Y-%m-%dT%H:%M:%S"),
               "source_sha256": file_hash(Path(__file__)),
               "phase1_decision_sha256": file_hash(PHASE1_OUT / "decision.json"),
               "phase1_selected_configuration": phase1["selected_configuration"],
               "phase1_2022_raw_ic": phase1["results"],
               "released_baseline_scores": {str(k): v for k, v in release_scores().items()}}
    if path.exists():
        existing = json.loads(path.read_text(encoding="utf-8"))
        drift = {k: (existing.get(k), v) for k, v in PROTOCOL.items() if existing.get(k) != v}
        if drift:
            raise SystemExit(f"Protocol already frozen and differs; do not rewrite after results: {drift}")
        log("Protocol already frozen and unchanged")
        return
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    log(f"Froze phase-2 protocol before any scoring: {ARCHITECTURE} h{HIDDEN} w{WINDOW} "
        f"{EPOCHS} epochs, ensemble weight {ENSEMBLE_WEIGHT}, released pipeline unchanged")


def verify_protocol() -> dict:
    path = OUT / "protocol.json"
    if not path.exists():
        raise SystemExit("Run the protocol stage first")
    protocol = json.loads(path.read_text(encoding="utf-8"))
    if protocol["source_sha256"] != file_hash(Path(__file__)):
        raise SystemExit("sequence_ensemble.py changed after the protocol was frozen; stop rather "
                         "than run edited code against a frozen rule")
    for key, value in (("architecture", ARCHITECTURE), ("hidden", HIDDEN), ("window", WINDOW),
                       ("epochs", EPOCHS)):
        if protocol["frozen"][key] != value:
            raise SystemExit(f"Frozen {key} differs from this source")
    if protocol["frozen"]["ensemble"]["weight"] != ENSEMBLE_WEIGHT:
        raise SystemExit("Frozen ensemble weight differs from this source")
    return protocol


def train_fold(features: list[str], raw_panel, year: int) -> dict:
    """Train the frozen architecture on one fold and return raw predictions for that year."""
    dates, codes, x, y, valid, _ = raw_panel
    cutoff = fold_cutoff(year)
    mean, std, stats = fit_scaler(x, valid, dates, cutoff)
    z = apply_scaler(x, mean, std)
    tensors = st.Tensors(dates, codes, z, y, valid)
    del z
    train_days = tensors.usable_days([t for t, d in enumerate(dates) if d < cutoff], WINDOW)
    outer_days = [t for t, d in enumerate(dates)
                  if year * 10000 + 101 <= d <= year * 10000 + 1231]
    usable_outer = tensors.usable_days(outer_days, WINDOW)
    if len(usable_outer) != len(outer_days):
        raise AssertionError(f"{year}: {len(outer_days) - len(usable_outer)} outer days lack a full window")
    log(f"{year}: cutoff {cutoff}, train {len(train_days)} days, outer {len(usable_outer)} days, "
        f"{EPOCHS} epochs")
    torch.manual_seed(st.SEED)
    model = st.build_model(ARCHITECTURE, tensors.features, HIDDEN).to(st.DEVICE)
    optimizer = torch.optim.Adam(model.parameters(), lr=st.LEARNING_RATE,
                                 weight_decay=st.WEIGHT_DECAY)
    generator = np.random.default_rng(st.SEED)
    started = time.monotonic()
    for epoch in range(EPOCHS):
        model.train()
        order = generator.permutation(np.asarray(train_days, dtype=np.int64))
        for start in range(0, len(order), st.BATCH_DAYS):
            chunk = order[start:start + st.BATCH_DAYS]
            if len(chunk) < 2:
                continue
            prediction = model(tensors.windows(chunk, WINDOW))
            target, mask = tensors.batch_targets(chunk)
            ic, usable = st.daily_pearson_ic(prediction.view(len(chunk), -1), target, mask)
            if not bool(usable.any()):
                continue
            loss = -ic[usable].mean()
            optimizer.zero_grad(set_to_none=True)
            loss.backward()
            optimizer.step()
        if (epoch + 1) % 10 == 0 or epoch + 1 == EPOCHS:
            log(f"  {year} epoch {epoch + 1}/{EPOCHS} elapsed {time.monotonic() - started:.0f}s")
    raw_days = st.predict_days(tensors, model, usable_outer, WINDOW)
    prediction = np.full((len(outer_days), tensors.stocks), st.SENTINEL, dtype=np.float64)
    for row, position in enumerate(outer_days):
        values = raw_days[usable_outer.index(position)].astype(np.float64)
        values[~np.isfinite(values)] = st.SENTINEL
        prediction[row] = values
    elapsed = time.monotonic() - started
    del tensors, model
    if st.DEVICE.type == "cuda":
        torch.cuda.empty_cache()
    return {"prediction": prediction.reshape(-1), "train_days": len(train_days),
            "outer_days": len(usable_outer), "elapsed_seconds": elapsed,
            "cutoff": cutoff, "normalization": stats,
            "normalization_mean_sha256": file_hash_of_array(mean),
            "normalization_std_sha256": file_hash_of_array(std)}


def train() -> None:
    protocol = verify_protocol()
    OUT.mkdir(parents=True, exist_ok=True)
    features = feature_names()
    started = time.monotonic()
    log("Loading the 2018-2024 panel once and renormalizing per fold")
    raw_panel = load_sequence_panel(features, max(ALL_YEARS))
    phase1 = json.loads((PHASE1_OUT / "decision.json").read_text(encoding="utf-8"))
    record = {"generated_at_local": time.strftime("%Y-%m-%dT%H:%M:%S"),
              "protocol_sha256": file_hash(OUT / "protocol.json"),
              "device": str(st.DEVICE), "torch_version": torch.__version__,
              "configuration": {"architecture": ARCHITECTURE, "hidden": HIDDEN, "window": WINDOW,
                                "epochs": EPOCHS, "seed": st.SEED, "batch_days": st.BATCH_DAYS,
                                "clip_std": CLIP_STD, "dropout": st.DROPOUT},
              "folds": {}}
    for year in ALL_YEARS:
        path = OUT / f"nn_raw_{year}.parquet"
        panel = load_panel(year)
        result = train_fold(features, raw_panel, year)
        prediction = result.pop("prediction")
        if len(prediction) != len(panel.frame):
            raise AssertionError(f"{year}: prediction length differs from the fold panel")
        metrics, _ = official_score(panel, prediction, year)
        result["raw_official_metrics"] = {k: float(v) for k, v in metrics.items()}
        if year == 2022:
            prior = phase1["results"]["sequence_raw"]["ic_mean"]
            result["phase1_ic_drift"] = metrics["ic_mean"] - prior
            result["phase1_ic_drift_relative"] = metrics["ic_mean"] / prior - 1
            log(f"2022 determinism: raw IC {metrics['ic_mean']:.9f} vs phase-1 {prior:.9f} "
                f"(drift {result['phase1_ic_drift']:+.3e})")
        pl.DataFrame({"ts_code": [str(c) for c in panel.codes] * len(panel.dates),
                      "trade_date": np.repeat(panel.dates, panel.rows_per_day),
                      "pred_raw": prediction}).write_parquet(path, compression="zstd")
        result["cache"] = str(path.relative_to(ROOT)).replace("\\", "/")
        result["cache_sha256"] = file_hash(path)
        record["folds"][str(year)] = result
        log(f"{year}: raw IC={metrics['ic_mean']:.6f} raw excess={metrics['annual_excess']:.6f} "
            f"({result['elapsed_seconds']:.0f}s train)")
        del panel
    record["elapsed_seconds"] = time.monotonic() - started
    record["source_and_input_sha256"] = {
        "experiments/sequence_ensemble.py": file_hash(Path(__file__)),
        "experiments/sequence_training.py": file_hash(ROOT / "experiments/sequence_training.py"),
        "experiments/sequence_model.py": file_hash(ROOT / "experiments/sequence_model.py"),
        **{PHASE1_OUT.name + "/decision.json": file_hash(PHASE1_OUT / "decision.json")},
        **{FOLD.format(year=y): file_hash(ROOT / FOLD.format(year=y)) for y in ALL_YEARS},
    }
    (OUT / "training.json").write_text(json.dumps(record, ensure_ascii=False, indent=2),
                                       encoding="utf-8")
    log(f"Wrote {OUT / 'training.json'}")


def score_year(year: int, released_composite: float) -> dict:
    """Run the released pipeline on the backbone and on the ensemble, and score both."""
    from experiments.audit_top_internal import paired_intervals
    panel = load_panel(year)
    auxiliary = load_auxiliary(year, panel)
    cache = OUT / f"nn_raw_{year}.parquet"
    if not cache.exists():
        raise SystemExit(f"Run the train stage first; missing {cache.name}")
    nn_frame = pl.read_parquet(cache).sort("trade_date", "ts_code")
    if not nn_frame.select("trade_date", "ts_code").equals(panel.frame.select("trade_date", "ts_code")):
        raise AssertionError(f"{year}: cached sequence predictions do not align with the fold panel")
    nn_raw = nn_frame["pred_raw"].to_numpy().astype(np.float64)
    if not np.isfinite(nn_raw).all():
        raise AssertionError(f"{year}: cached sequence predictions contain a nonfinite value")
    backbone_raw = panel.frame["pred_raw"].to_numpy().astype(np.float64)
    ensemble = ensemble_signal(panel, backbone_raw, nn_raw)

    baseline_prediction = pipeline(panel, auxiliary, backbone_raw)
    baseline_metrics, baseline_daily = official_score(panel, baseline_prediction, year)
    if abs(baseline_metrics["final_score"] - released_composite) > NUMERIC_TOLERANCE:
        raise AssertionError(f"{year}: backbone through the released pipeline gives "
                             f"{baseline_metrics['final_score']:.12f}, not the released "
                             f"{released_composite:.12f}")
    candidate_prediction = pipeline(panel, auxiliary, ensemble)
    candidate_metrics, candidate_daily = official_score(panel, candidate_prediction, year)
    delta = candidate_metrics["final_score"] - baseline_metrics["final_score"]
    baseline_daily.write_csv(OUT / f"official_baseline_{year}_daily.csv")
    candidate_daily.write_csv(OUT / f"official_ensemble_{year}_daily.csv")

    result = {
        "year": year,
        "released_composite": released_composite,
        "baseline_metrics": {k: float(v) for k, v in baseline_metrics.items()},
        "candidate_metrics": {k: float(v) for k, v in candidate_metrics.items()},
        "score_delta": delta,
        "ic_delta": candidate_metrics["ic_mean"] - baseline_metrics["ic_mean"],
        "annual_excess_delta": candidate_metrics["annual_excess"] - baseline_metrics["annual_excess"],
        "turnover_delta": candidate_metrics["mean_turnover"] - baseline_metrics["mean_turnover"],
        "improves": delta > NUMERIC_TOLERANCE,
        "paired_uncertainty": paired_intervals(candidate_daily, baseline_daily, delta),
        "anchored_to_released_composite": True,
    }
    del panel, auxiliary, baseline_prediction, candidate_prediction
    return result


def develop() -> None:
    protocol = verify_protocol()
    training_path = OUT / "training.json"
    if not training_path.exists():
        raise SystemExit("Run the train stage first")
    result_path = OUT / "development.json"
    if result_path.exists():
        raise SystemExit("Development results already recorded; preserving them instead of rescoring")
    training = json.loads(training_path.read_text(encoding="utf-8"))
    if training["protocol_sha256"] != file_hash(OUT / "protocol.json"):
        raise SystemExit("Training was produced under a different protocol")
    released = release_scores()
    started = time.monotonic()
    years = {}
    for year in DEVELOPMENT_YEARS:
        years[str(year)] = score_year(year, released[year])
        item = years[str(year)]
        ci = item["paired_uncertainty"]["paired_composite_hac_exact_component_denominators"]
        log(f"{year}: composite {item['baseline_metrics']['final_score']:.9f} -> "
            f"{item['candidate_metrics']['final_score']:.9f} ({item['score_delta']:+.9f}) | "
            f"IC {item['ic_delta']:+.6f} excess {item['annual_excess_delta']:+.6f} "
            f"turnover {item['turnover_delta']:+.6f} | HAC 95% "
            f"[{ci['normal_95_ci'][0]:+.6f}, {ci['normal_95_ci'][1]:+.6f}]")
    passed = all(years[str(y)]["improves"] for y in DEVELOPMENT_YEARS)
    output = {
        "stage": "develop",
        "generated_at_local": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "elapsed_seconds": time.monotonic() - started,
        "protocol_sha256": file_hash(OUT / "protocol.json"),
        "training_sha256": file_hash(training_path),
        "development_years": list(DEVELOPMENT_YEARS),
        "development_gate": protocol["development_gate"],
        "years": years,
        "development_gate_passed": passed,
        "sequence_determinism_2022": training["folds"]["2022"].get("phase1_ic_drift"),
        "caveat": "Historical development years examined many times; not a blind holdout and not "
                  "an official 2025-2026 test score.",
    }
    result_path.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")
    log(f"DEVELOPMENT gate {'PASSED' if passed else 'FAILED'}")
    if not passed:
        log("Stopping; 2024 is not scored and the release is unchanged.")


def diagnose() -> None:
    protocol = verify_protocol()
    development_path = OUT / "development.json"
    if not development_path.exists():
        raise SystemExit("Run the develop stage first")
    development = json.loads(development_path.read_text(encoding="utf-8"))
    if not development["development_gate_passed"]:
        raise SystemExit("Development gate failed; the frozen protocol does not permit a 2024 diagnostic")
    decision_path = OUT / "decision.json"
    if decision_path.exists():
        raise SystemExit("Decision already recorded; preserving it instead of rescoring 2024")
    released = release_scores()
    item = score_year(DIAGNOSTIC_YEAR, released[DIAGNOSTIC_YEAR])
    ci = item["paired_uncertainty"]["paired_composite_hac_exact_component_denominators"]
    log(f"{DIAGNOSTIC_YEAR}: composite {item['baseline_metrics']['final_score']:.9f} -> "
        f"{item['candidate_metrics']['final_score']:.9f} ({item['score_delta']:+.9f}) | "
        f"IC {item['ic_delta']:+.6f} excess {item['annual_excess_delta']:+.6f} "
        f"turnover {item['turnover_delta']:+.6f} | HAC 95% "
        f"[{ci['normal_95_ci'][0]:+.6f}, {ci['normal_95_ci'][1]:+.6f}]")
    training = json.loads((OUT / "training.json").read_text(encoding="utf-8"))
    decision = {
        "stage": "diagnose",
        "generated_at_local": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "experiment": PROTOCOL["experiment"],
        "protocol_sha256": file_hash(OUT / "protocol.json"),
        "development_sha256": file_hash(development_path),
        "diagnostic_year": DIAGNOSTIC_YEAR,
        "diagnostic_gate_passed": item["improves"],
        "years": {**{str(y): {k: development["years"][str(y)][k] for k in
                              ("released_composite", "score_delta", "ic_delta",
                               "annual_excess_delta", "turnover_delta", "improves")}
                    for y in DEVELOPMENT_YEARS},
                  str(DIAGNOSTIC_YEAR): {k: item[k] for k in
                                         ("released_composite", "score_delta", "ic_delta",
                                          "annual_excess_delta", "turnover_delta", "improves")}},
        "diagnostic_detail": item,
        "configuration": training["configuration"],
        "recommended_for_next_version": bool(item["improves"]),
        "deployed_to_production": False,
        "official_submission_or_report_changed": False,
        "score_first_rule_changed_after_results": False,
        "postprocess_retuned_for_ensemble": False,
        "decision": ("Recommend the rank ensemble for the next version under the predeclared "
                     "score-first rule; a full-training sequence model, regenerated official "
                     "predictions, an independent audit and a synchronized report are still "
                     "required before any adoption."
                     if item["improves"] else
                     "Do not adopt. 2024 did not meet the predeclared strict improvement "
                     "condition; retain the released backbone-only pipeline. Do not retune the "
                     "post-processing stack or the ensemble weight."),
        "caveats": protocol["limitations"],
    }
    decision["all_three_years_improve"] = all(
        development["years"][str(y)]["improves"] for y in DEVELOPMENT_YEARS) and item["improves"]
    decision_path.write_text(json.dumps(decision, ensure_ascii=False, indent=2), encoding="utf-8")
    log(f"DECISION: {'RECOMMEND' if item['improves'] else 'DO NOT ADOPT'} "
        f"(all three years improve: {decision['all_three_years_improve']})")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("stage", choices=("protocol", "train", "develop", "diagnose"))
    arguments = parser.parse_args()
    if arguments.stage == "protocol":
        write_protocol()
    elif arguments.stage == "train":
        train()
    elif arguments.stage == "develop":
        develop()
    else:
        diagnose()
