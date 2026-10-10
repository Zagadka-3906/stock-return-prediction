"""Fixed seven-candidate rank blend, using only 2022/2023 for selection.

Reuse the prior market-feature model and production model without training or
postprocessor tuning. Every candidate is evaluated by the original evaluator;
the stable-sort project scorer is retained only as a diagnostic comparison.
"""
from __future__ import annotations

import argparse
import gc
import json
import time
from pathlib import Path

import numpy as np

from experiments import cached_recheck, feature_expansion
from experiments.official_seed_development import official_score
from experiments.seed_ensemble import file_hash
from run import ROOT, fold_cutoff
from src.scoring import Panel, score


OUT = ROOT / "experiments" / "market_blend_eval"
YEARS = (2022, 2023)
WEIGHTS = (0.1, 0.25, 0.5)
CANDIDATES = {"baseline": {"mode": "baseline", "weight": 0.0}}
for _mode in ("full_signal", "top_only"):
    for _weight in WEIGHTS:
        CANDIDATES[f"{_mode}_w{_weight:g}"] = {"mode": _mode, "weight": _weight}
POSTPROCESS = {"alpha": 0.9, "bonus": 0.3, "restore_lower": True,
               "top_current_weight": 1.0}


def log(message: str) -> None:
    print(f"[{time.strftime('%H:%M:%S')}] {message}", flush=True)


def check_protocol() -> None:
    protocol = json.loads((OUT / "protocol.json").read_text(encoding="utf-8"))
    if (protocol["development_years"] != list(YEARS)
            or protocol["candidate_order"] != list(CANDIDATES)
            or protocol["market_weights"] != list(WEIGHTS)
            or protocol["postprocess"] != POSTPROCESS
            or protocol.get("declared_before_blend_evaluation") is not True
            or cached_recheck.BASE_CONFIG != POSTPROCESS):
        raise ValueError("Fixed blending protocol or postprocessor changed")
    cached_recheck.check_production_config()


def load_panel(year: int) -> Panel:
    return feature_expansion.load_panel(year)


def load_market_raw(year: int, panel: Panel) -> np.ndarray:
    """Require the saved model, cache, source and fold fingerprint to match."""
    raw = feature_expansion.load_raw(year, "market", panel)
    metadata_path = feature_expansion.OUT / f"feature_market_{year}.json"
    metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
    expected_rows = {2022: 3568878, 2023: 4597785, 2024: 5659954}
    expected_cutoff = fold_cutoff(year)
    if (metadata["training_cutoff_exclusive"] != expected_cutoff
            or metadata["training_last_date"] >= expected_cutoff
            or metadata["training_rows"] != expected_rows[year]
            or metadata["validation_rows"] != len(panel.frame)
            or metadata["reload_max_abs_error"] != 0
            or metadata["rounds"] != 180
            or metadata["seed"] != 2026
            or len(metadata["features"]) != 71):
        raise ValueError(f"Unexpected saved market-model metadata for {year}")
    return raw


def make_prediction(panel: Panel, market_raw: np.ndarray | None,
                    config: dict) -> np.ndarray:
    if config not in CANDIDATES.values():
        raise ValueError("Only the seven predeclared configurations are supported")
    return cached_recheck.make_prediction(
        panel, market_raw, config["mode"], config["weight"])


def source_fingerprints() -> dict[str, str]:
    """Lock development-only cache provenance and all executable dependencies."""
    check_protocol()
    previous_path = feature_expansion.OUT / "development.json"
    previous = json.loads(previous_path.read_text(encoding="utf-8"))
    if (previous["selection_years"] != list(YEARS)
            or previous["selected_variant"] != "market"
            or previous["experiment_source_sha256"] != file_hash(Path(feature_expansion.__file__))):
        raise ValueError("Previous feature-group selection or its runner changed")
    previous_winner = max(feature_expansion.VARIANTS, key=lambda variant: min(
        previous["candidates"][variant]["years"][str(year)]["final_score"]
        for year in YEARS))
    if previous_winner != "market":
        raise ValueError("Market variant no longer matches the prior locked selection")
    paths = {Path(__file__), Path(cached_recheck.__file__), previous_path,
             OUT / "protocol.json", ROOT / "validation/metrics.json"}
    for relative, expected in previous["artifacts_sha256"].items():
        path = ROOT / relative
        if file_hash(path) != expected:
            raise ValueError(f"Previous development artifact changed: {relative}")
        paths.add(path)
    for year in YEARS:
        fingerprint = feature_expansion.fingerprint(year, "market")
        paths.update(ROOT / relative for relative in fingerprint["source_sha256"])
        paths.update(feature_expansion.OUT / f"feature_market_{year}.{extension}"
                     for extension in ("txt", "parquet", "json"))
    return {str(path.relative_to(ROOT)): file_hash(path) for path in sorted(paths)}


def develop() -> dict:
    initial = source_fingerprints()
    OUT.mkdir(exist_ok=True)
    result = {
        "selection_years": list(YEARS), "candidate_count": len(CANDIDATES),
        "postprocess": POSTPROCESS,
        "selection_rule": "maximize_minimum_official_annual_score_2022_2023; exact ties prefer declaration order",
        "tie_policy_note": "Unmodified evaluate.py and default pandas descending sort; official daily evidence rebuilt from identical CSV bytes and original Float64 labels.",
        "candidates": {key: {"config": dict(config), "years": {}}
                       for key, config in CANDIDATES.items()},
        "project_metrics": {key: {} for key in CANDIDATES},
        "official_minus_project_score": {key: {} for key in CANDIDATES},
        "note": "Fixed prior market-feature auxiliary, no retraining or new data. Development uses 2022/2023 only; 2024 labels are not loaded or scored here. Historical folds are not untouched holdouts.",
    }
    daily_paths = set()
    for year in YEARS:
        panel = load_panel(year)
        market_raw = load_market_raw(year, panel)
        for key, config in CANDIDATES.items():
            prediction = make_prediction(panel, market_raw, config)
            project_metrics, _ = score(panel, prediction)
            official_metrics, daily = official_score(panel, prediction, year)
            result["candidates"][key]["years"][str(year)] = official_metrics
            result["project_metrics"][key][str(year)] = project_metrics
            result["official_minus_project_score"][key][str(year)] = (
                official_metrics["final_score"] - project_metrics["final_score"])
            daily_path = OUT / f"official_{key}_{year}_daily.csv"
            daily.write_csv(daily_path)
            daily_paths.add(daily_path)
            log(f"OFFICIAL {year}/{key}: score={official_metrics['final_score']:.12f}; "
                f"IC={official_metrics['ic_mean']:.9f}; "
                f"excess={official_metrics['annual_excess']:.9f}; "
                f"turnover={official_metrics['mean_turnover']:.9f}")
            del prediction, daily
            gc.collect()
        del panel, market_raw
        gc.collect()
    for candidate in result["candidates"].values():
        candidate["minimum_annual_score"] = min(
            candidate["years"][str(year)]["final_score"] for year in YEARS)
    chosen = max(CANDIDATES, key=lambda key: result["candidates"][key]["minimum_annual_score"])
    result["selected_key"] = chosen
    result["selected_config"] = dict(CANDIDATES[chosen])
    result["selected_improves_both_years"] = all(
        result["candidates"][chosen]["years"][str(year)]["final_score"]
        > result["candidates"]["baseline"]["years"][str(year)]["final_score"]
        for year in YEARS)
    if source_fingerprints() != initial:
        raise AssertionError("A locked source or saved artifact changed during development")
    # Re-run the model/cache alignment and strong fingerprint checks after scoring.
    for year in YEARS:
        panel = load_panel(year)
        load_market_raw(year, panel)
        del panel
    result["experiment_source_sha256"] = file_hash(Path(__file__))
    result["artifacts_sha256"] = {
        **initial,
        **{str(path.relative_to(ROOT)): file_hash(path) for path in sorted(daily_paths)},
    }
    (OUT / "development.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    log(f"LOCKED {chosen}; both development years improved={result['selected_improves_both_years']}")
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("step", choices=("develop",))
    parser.parse_args()
    develop()
