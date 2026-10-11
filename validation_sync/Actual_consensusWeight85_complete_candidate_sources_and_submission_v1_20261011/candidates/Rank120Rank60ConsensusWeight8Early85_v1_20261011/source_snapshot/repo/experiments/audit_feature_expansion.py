"""Independently audit the locked feature-ablation experiment.

Development is restricted to 2022/2023. Historical 2024 is evaluated only for
the already selected variant; it is not a fresh holdout or a reselection set.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import polars as pl
from scipy.stats import spearmanr

from experiments.audit_cached_recheck import digest
from experiments.audit_top_internal import paired_intervals
from experiments.feature_expansion import OUT, VARIANTS, load_panel, load_raw, make_prediction
from experiments.official_seed_development import official_score, original_labels
from run import ROOT
from src.scoring import Panel


def locked_selection():
    path = OUT / "development.json"
    development = json.loads(path.read_text(encoding="utf-8"))
    assert development["selection_years"] == [2022, 2023]
    assert set(development["candidates"]) == set(VARIANTS)
    assert all(set(c["years"]) == {"2022", "2023"} for c in development["candidates"].values())
    selected = max(VARIANTS, key=lambda v: min(m["final_score"] for m in development["candidates"][v]["years"].values()))
    assert selected == development["selected_variant"]
    assert digest(Path(__file__).with_name("feature_expansion.py")) == development["experiment_source_sha256"]
    for relative, expected in development["artifacts_sha256"].items():
        assert digest(ROOT / relative) == expected, f"Changed experimental input/output: {relative}"
    return development, selected


def prediction_checks(year: int, variant: str):
    panel = load_panel(year)
    raw = load_raw(year, variant, panel)
    prediction = make_prediction(panel, raw)
    assert len(prediction) == len(panel.frame) and np.isfinite(prediction).all()
    blank = Panel.from_frame(panel.frame.with_columns(pl.lit(None, dtype=pl.Float64).alias("y_ret_1d")))
    assert np.array_equal(prediction, make_prediction(blank, raw))
    perturbed = Panel.from_frame(panel.frame.with_columns((pl.col("y_ret_1d").fill_nan(0).fill_null(0) * -11 + 5).alias("y_ret_1d")))
    assert np.array_equal(prediction, make_prediction(perturbed, raw))
    count = 50 * panel.rows_per_day
    prefix = Panel.from_frame(panel.frame.head(count))
    assert np.array_equal(prediction[:count], make_prediction(prefix, raw[:count]))
    checks = {"finite_predictions": True, "label_removal_invariance": True,
              "label_perturbation_invariance": True, "prefix_invariance_50_days": True}
    return panel, prediction, checks


def decile_diagnostics(panel: Panel, prediction: np.ndarray, year: int):
    """Descriptive equal-count return groups, not a tradeable backtest."""
    keys = panel.frame.select("ts_code", "trade_date", "flag_limit_up")
    frame = keys.with_columns(pl.Series("pred", prediction)).join(
        original_labels(year), on=["ts_code", "trade_date"], how="left", validate="1:1"
    ).sort("trade_date", "ts_code")
    groups = []
    for day in frame.partition_by("trade_date", maintain_order=True):
        good = day.filter((pl.col("flag_limit_up") == 0) & pl.col("y_ret_1d").is_finite())
        if len(good) < 100:
            continue
        # Explicit stable ties for this auxiliary diagnostic only. Official
        # score and paired intervals use the organizer's separate CSV pathway.
        ordered = good.sort("pred", descending=True, maintain_order=True)["y_ret_1d"].to_numpy()
        edges = np.floor(np.linspace(0, len(ordered), 11)).astype(int)
        means = [float(np.mean(ordered[edges[i]:edges[i + 1]])) for i in range(10)]
        groups.append(means)
    annual = np.mean(np.asarray(groups), axis=0) * 252
    return {"days": len(groups), "annualized_returns_top_to_bottom": annual.tolist(),
            "top_minus_bottom_annualized": float(annual[0] - annual[-1]),
            "decile_quality_spearman": float(spearmanr(np.arange(10, 0, -1), annual).statistic),
            "monotone_top_to_bottom": bool(np.all(np.diff(annual) <= 0)),
            "caveat": "Ex-post label-valid groups; stable tie sorting for this auxiliary diagnostic. Uncosted, not a live portfolio return."}


def develop():
    development, selected = locked_selection()
    real_prefix = json.loads((OUT / "real_prefix_audit.json").read_text(encoding="utf-8"))
    assert real_prefix["status"] == "passed"
    assert real_prefix["feature_module_sha256"] == digest(Path(__file__).with_name("feature_expansion_features.py"))
    assert real_prefix["stored_features_sha256"] == digest(OUT / "features.parquet")
    assert all(item["null_masks_exact"] and item["isclose_all"] for item in real_prefix["features"].values())
    result = {"selected_variant": selected, "development_sha256": digest(OUT / "development.json"),
              "audit_source_sha256": digest(Path(__file__)), "years": {},
              "real_prefix_audit_sha256": digest(OUT / "real_prefix_audit.json"),
              "real_feature_prefix_check": real_prefix,
              "candidate_paired_uncertainty": {},
              "limitations": ["HAC intervals are descriptive and not adjusted for accumulated candidate selection."]}
    for year in (2022, 2023):
        base_daily = pl.read_csv(OUT / f"official_baseline_{year}_daily.csv")
        baseline = development["candidates"]["baseline"]["years"][str(year)]
        for variant in VARIANTS:
            if variant == "baseline":
                continue
            daily = pl.read_csv(OUT / f"official_{variant}_{year}_daily.csv")
            delta = development["candidates"][variant]["years"][str(year)]["final_score"] - baseline["final_score"]
            result["candidate_paired_uncertainty"].setdefault(variant, {})[str(year)] = paired_intervals(daily, base_daily, delta)
        panel, prediction, checks = prediction_checks(year, selected)
        metrics, daily = official_score(panel, prediction, year)
        expected = development["candidates"][selected]["years"][str(year)]
        assert all(abs(metrics[k] - expected[k]) <= 1e-12 for k in metrics)
        checks.update({"official_metrics_recomputed": metrics,
                       "decile_diagnostics": decile_diagnostics(panel, prediction, year)})
        result["years"][str(year)] = checks
        print(f"AUDIT {year} {selected}: {metrics['final_score']:.12f}", flush=True)
    (OUT / "development_audit.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")


def diagnose():
    _, selected = locked_selection()
    if selected == "baseline":
        raise ValueError("Baseline selected in development; no candidate is authorized for 2024 diagnosis")
    audit = json.loads((OUT / "development_audit.json").read_text(encoding="utf-8"))
    assert audit["development_sha256"] == digest(OUT / "development.json")
    assert audit["audit_source_sha256"] == digest(Path(__file__))
    assert audit["real_prefix_audit_sha256"] == digest(OUT / "real_prefix_audit.json")
    assert audit["selected_variant"] == selected
    panel, prediction, checks = prediction_checks(2024, selected)
    baseline_pred = make_prediction(panel, load_raw(2024, "baseline", panel))
    metrics, daily = official_score(panel, prediction, 2024)
    baseline, baseline_daily = official_score(panel, baseline_pred, 2024)
    delta = metrics["final_score"] - baseline["final_score"]
    result = {"selected_variant": selected, "official_metrics": metrics,
              "official_baseline": baseline, "official_score_delta": delta,
              "checks": checks, "paired_uncertainty": paired_intervals(daily, baseline_daily, delta),
              "decile_diagnostics": decile_diagnostics(panel, prediction, 2024),
              "development_sha256": audit["development_sha256"],
              "audit_source_sha256": digest(Path(__file__)),
              "historical_diagnostic_only": True, "no_candidate_reselection": True,
              "limitations": ["2024 was viewed in prior iterations and is not an untouched holdout.",
                              "HAC intervals do not account for sequential selection.",
                              "Official test labels are unavailable."]}
    daily.write_csv(OUT / "official_selected_2024_daily.csv")
    baseline_daily.write_csv(OUT / "official_baseline_2024_daily.csv")
    panel.frame.select("ts_code", "trade_date").with_columns(pl.Series("pred", prediction)).write_parquet(OUT / "selected_2024.parquet")
    (OUT / "diagnostic_2024.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2), flush=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("stage", choices=("develop", "diagnose"))
    args = parser.parse_args()
    develop() if args.stage == "develop" else diagnose()
