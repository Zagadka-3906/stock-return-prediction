"""Independent causal and official-score audit for a locked market blend."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import polars as pl

from experiments.audit_cached_recheck import digest
from experiments.audit_feature_expansion import decile_diagnostics
from experiments.audit_top_internal import assert_top_sets_equal, paired_intervals, synthetic_panel
from experiments.market_blend import CANDIDATES, OUT, load_market_raw, load_panel, make_prediction
from experiments.official_seed_development import official_score
from run import ROOT
from src.scoring import Panel


def audit_dependencies():
    return {relative: digest(ROOT / relative) for relative in (
        "experiments/audit_cached_recheck.py", "experiments/audit_feature_expansion.py",
        "experiments/audit_top_internal.py", "report_analytics.py")}


def locked_selection():
    dev = json.loads((OUT / "development.json").read_text(encoding="utf-8"))
    protocol = json.loads((OUT / "protocol.json").read_text(encoding="utf-8"))
    assert dev["selection_years"] == [2022, 2023]
    assert list(CANDIDATES) == protocol["candidate_order"]
    assert list(dev["candidates"]) == list(CANDIDATES)
    for key, candidate in dev["candidates"].items():
        assert candidate["config"] == CANDIDATES[key]
        assert set(candidate["years"]) == {"2022", "2023"}
    selected = max(CANDIDATES, key=lambda key: min(m["final_score"] for m in dev["candidates"][key]["years"].values()))
    assert selected == dev["selected_key"]
    assert dev["selected_config"] == CANDIDATES[selected]
    assert digest(Path(__file__).with_name("market_blend.py")) == dev["experiment_source_sha256"]
    for relative, expected in dev["artifacts_sha256"].items():
        assert digest(ROOT / relative) == expected, f"Changed blend dependency: {relative}"
    return dev, selected


def synthetic_checks():
    rng = np.random.default_rng(73012)
    days, stocks = 6, 128
    valid = np.ones((days, stocks), dtype=bool)
    valid[2] = False
    valid[3, :122] = False
    up = np.zeros((days, stocks), dtype=np.int8)
    up[4] = 1
    raw = rng.normal(size=(days, stocks))
    raw[0] = 1.0
    auxiliary = rng.normal(size=raw.shape).reshape(-1)
    fixture = synthetic_panel(valid, up)
    panel = Panel.from_frame(fixture.frame.with_columns(pl.Series("pred_raw", raw.reshape(-1))))
    baseline = make_prediction(panel, auxiliary, CANDIDATES["baseline"])
    results = {}
    for key, config in CANDIDATES.items():
        pred = make_prediction(panel, auxiliary, config)
        assert np.isfinite(pred).all()
        rows = 4 * stocks
        prefix = Panel.from_frame(panel.frame.head(rows))
        assert np.array_equal(pred[:rows], make_prediction(prefix, auxiliary[:rows], config))
        if config["mode"] == "top_only":
            assert_top_sets_equal(panel, baseline, pred)
            assert np.array_equal(pred[:stocks], baseline[:stocks]), "Ambiguous cutoff must fall back"
        results[key] = {"finite": True, "prefix_invariance": True,
                        "top_membership_check_applies": config["mode"] == "top_only"}
    return results


def prediction_checks(year: int, config: dict):
    panel = load_panel(year)
    auxiliary = load_market_raw(year, panel)
    pred = make_prediction(panel, auxiliary, config)
    baseline = make_prediction(panel, auxiliary, CANDIDATES["baseline"])
    assert np.isfinite(pred).all()
    blank = Panel.from_frame(panel.frame.with_columns(pl.lit(None, dtype=pl.Float64).alias("y_ret_1d")))
    changed = Panel.from_frame(panel.frame.with_columns((pl.col("y_ret_1d").fill_nan(0).fill_null(0) * -9 + 7).alias("y_ret_1d")))
    assert np.array_equal(pred, make_prediction(blank, auxiliary, config))
    assert np.array_equal(pred, make_prediction(changed, auxiliary, config))
    rows = 50 * panel.rows_per_day
    prefix = Panel.from_frame(panel.frame.head(rows))
    assert np.array_equal(pred[:rows], make_prediction(prefix, auxiliary[:rows], config))
    if config["mode"] == "top_only":
        assert_top_sets_equal(panel, baseline, pred)
    return panel, pred, baseline, {
        "finite": True, "label_removal_invariance": True,
        "label_perturbation_invariance": True, "prefix_invariance_50_days": True,
        "top_membership_preserved": config["mode"] in ("baseline", "top_only"),
    }


def develop():
    dev, selected = locked_selection()
    result = {"selected_key": selected, "selected_config": CANDIDATES[selected],
              "development_sha256": digest(OUT / "development.json"),
              "audit_source_sha256": digest(Path(__file__)),
              "audit_dependencies_sha256": audit_dependencies(),
              "synthetic_checks": synthetic_checks(), "years": {}, "candidate_paired_uncertainty": {},
              "limitations": ["HAC intervals do not correct sequential candidate selection."]}
    for year in (2022, 2023):
        baseline_daily = pl.read_csv(OUT / f"official_baseline_{year}_daily.csv")
        baseline = dev["candidates"]["baseline"]["years"][str(year)]
        membership_panel = load_panel(year)
        membership_raw = load_market_raw(year, membership_panel)
        membership_base = make_prediction(membership_panel, membership_raw, CANDIDATES["baseline"])
        for key, config in CANDIDATES.items():
            if key == "baseline":
                continue
            daily = pl.read_csv(OUT / f"official_{key}_{year}_daily.csv")
            delta = dev["candidates"][key]["years"][str(year)]["final_score"] - baseline["final_score"]
            result["candidate_paired_uncertainty"].setdefault(key, {})[str(year)] = paired_intervals(daily, baseline_daily, delta)
            if config["mode"] == "top_only":
                assert np.array_equal(daily["turnover"].to_numpy(), baseline_daily["turnover"].to_numpy(), equal_nan=True)
                member_prediction = make_prediction(membership_panel, membership_raw, config)
                assert_top_sets_equal(membership_panel, membership_base, member_prediction)
        del membership_panel, membership_raw, membership_base
        panel, pred, _, checks = prediction_checks(year, CANDIDATES[selected])
        metrics, _ = official_score(panel, pred, year)
        expected = dev["candidates"][selected]["years"][str(year)]
        assert all(abs(metrics[k] - expected[k]) <= 1e-12 for k in metrics)
        checks.update({"official_metrics_recomputed": metrics,
                       "decile_diagnostics": decile_diagnostics(panel, pred, year)})
        result["years"][str(year)] = checks
        print(f"AUDIT {year}/{selected}: {metrics['final_score']:.12f}", flush=True)
    (OUT / "development_audit.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")


def diagnose():
    _, selected = locked_selection()
    if selected == "baseline":
        raise ValueError("Baseline selected; no new candidate authorized for historical diagnosis")
    audit = json.loads((OUT / "development_audit.json").read_text(encoding="utf-8"))
    assert audit["development_sha256"] == digest(OUT / "development.json")
    assert audit["audit_source_sha256"] == digest(Path(__file__))
    assert audit["audit_dependencies_sha256"] == audit_dependencies()
    assert audit["selected_key"] == selected
    panel, pred, base_pred, checks = prediction_checks(2024, CANDIDATES[selected])
    metrics, daily = official_score(panel, pred, 2024)
    baseline, base_daily = official_score(panel, base_pred, 2024)
    delta = metrics["final_score"] - baseline["final_score"]
    if CANDIDATES[selected]["mode"] == "top_only":
        assert np.array_equal(daily["turnover"].to_numpy(), base_daily["turnover"].to_numpy(), equal_nan=True)
    result = {"selected_key": selected, "selected_config": CANDIDATES[selected],
              "official_metrics": metrics, "official_baseline": baseline,
              "official_score_delta": delta, "checks": checks,
              "paired_uncertainty": paired_intervals(daily, base_daily, delta),
              "decile_diagnostics": decile_diagnostics(panel, pred, 2024),
              "development_sha256": audit["development_sha256"],
              "audit_source_sha256": digest(Path(__file__)),
              "audit_dependencies_sha256": audit["audit_dependencies_sha256"],
              "historical_diagnostic_only": True, "no_candidate_reselection": True,
              "limitations": ["2024 was already viewed and is not an untouched holdout.",
                              "HAC intervals do not correct cumulative selection.",
                              "The official return Top and turnover Top use different label-availability filters.",
                              "Official 2025-2026 test labels are unavailable."]}
    daily.write_csv(OUT / "official_selected_2024_daily.csv")
    base_daily.write_csv(OUT / "official_baseline_2024_daily.csv")
    panel.frame.select("ts_code", "trade_date").with_columns(pl.Series("pred", pred)).write_parquet(OUT / "selected_2024.parquet")
    (OUT / "diagnostic_2024.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2), flush=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("stage", choices=("develop", "diagnose"))
    args = parser.parse_args()
    develop() if args.stage == "develop" else diagnose()
