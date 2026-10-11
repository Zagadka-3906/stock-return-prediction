"""Audit a fixed three-seed ensemble without touching production artifacts."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import polars as pl

from experiments.audit_cached_recheck import digest
from experiments.audit_top_internal import assert_top_sets_equal, paired_intervals, synthetic_panel
from experiments.seed_ensemble import OUT, load_panel, load_seed_raw, make_prediction
from run import ROOT
from src.scoring import Panel, score

SEEDS = (2026, 17, 43)


def locked_selection():
    dev = json.loads((OUT / "development.json").read_text(encoding="utf-8"))
    assert dev["selection_years"] == [2022, 2023]
    assert dev["seeds"] == list(SEEDS)
    assert set(dev["candidates"]) == {"baseline", "full_signal", "top_only"}
    assert all(set(c["years"]) == {"2022", "2023"} for c in dev["candidates"].values())
    chosen = max(dev["candidates"], key=lambda k: min(m["final_score"] for m in dev["candidates"][k]["years"].values()))
    assert chosen == dev["selected_mode"]
    assert digest(Path(__file__).with_name("seed_ensemble.py")) == dev["experiment_source_sha256"]
    for relative, expected in dev["artifacts_sha256"].items():
        assert digest(ROOT / relative) == expected, f"Changed seed artifact: {relative}"
    authority = json.loads((OUT / "official_development.json").read_text(encoding="utf-8"))
    assert authority["development_sha256"] == digest(OUT / "development.json")
    assert authority["original_evaluator_sha256"] == digest(ROOT / "evaluate.py")
    assert authority["official_reconstruction_source_sha256"] == digest(Path(__file__).with_name("official_seed_development.py"))
    for relative, expected in authority["official_daily_sha256"].items():
        assert digest(ROOT / relative) == expected, f"Changed official daily evidence: {relative}"
    assert authority["selection_years"] == [2022, 2023]
    assert set(authority["candidates"]) == set(dev["candidates"])
    assert all(set(c["years"]) == {"2022", "2023"} for c in authority["candidates"].values())
    chosen = max(authority["candidates"], key=lambda k: min(m["final_score"] for m in authority["candidates"][k]["years"].values()))
    assert chosen == authority["selected_mode"]
    return dev, chosen


def synthetic_checks():
    rng = np.random.default_rng(61902)
    days, stocks = 6, 128
    valid = np.ones((days, stocks), dtype=bool)
    valid[2] = False
    valid[3, :122] = False
    up = np.zeros((days, stocks), dtype=np.int8)
    up[4] = 1
    fixture = synthetic_panel(valid, up)
    raw = {seed: rng.normal(size=(days, stocks)).reshape(-1) for seed in SEEDS}
    raw[2026][:stocks] = 1.0
    panel = Panel.from_frame(fixture.frame.with_columns(pl.Series("pred_raw", raw[2026])))
    base = make_prediction(panel, raw, "baseline")
    results = {}
    for mode in ("full_signal", "top_only"):
        prediction = make_prediction(panel, raw, mode)
        assert np.isfinite(prediction).all()
        prefix_rows = 4 * stocks
        short = Panel.from_frame(panel.frame.head(prefix_rows))
        short_raw = {seed: values[:prefix_rows] for seed, values in raw.items()}
        assert np.array_equal(prediction[:prefix_rows], make_prediction(short, short_raw, mode))
        if mode == "top_only":
            assert_top_sets_equal(panel, base, prediction)
            assert np.array_equal(prediction[:stocks], base[:stocks])
        results[mode] = {"finite": True, "prefix_invariance": True,
                         "top_membership_preserved": mode == "top_only"}
    return results


def check_year(year: int, mode: str, expected: dict | None = None):
    panel = load_panel(year)
    raw = {seed: load_seed_raw(year, seed, panel) for seed in SEEDS}
    prediction = make_prediction(panel, raw, mode)
    base = make_prediction(panel, raw, "baseline")
    metrics, daily = score(panel, prediction)
    baseline, base_daily = score(panel, base)
    if expected:
        assert all(abs(metrics[k] - expected[k]) < 1e-12 for k in metrics)
    blank = Panel.from_frame(panel.frame.with_columns(pl.lit(None, dtype=pl.Float64).alias("y_ret_1d")))
    assert np.array_equal(prediction, make_prediction(blank, raw, mode))
    changed = Panel.from_frame(panel.frame.with_columns((pl.col("y_ret_1d").fill_nan(0).fill_null(0) * -7 + 3).alias("y_ret_1d")))
    assert np.array_equal(prediction, make_prediction(changed, raw, mode))
    rows = 50 * panel.rows_per_day
    prefix = Panel.from_frame(panel.frame.head(rows))
    assert np.array_equal(prediction[:rows], make_prediction(prefix, {s: v[:rows] for s, v in raw.items()}, mode))
    if mode == "top_only":
        assert_top_sets_equal(panel, base, prediction)
        assert np.array_equal(daily["turnover"].to_numpy(), base_daily["turnover"].to_numpy(), equal_nan=True)
    result = {"metrics": metrics, "baseline": baseline,
              "score_delta": metrics["final_score"] - baseline["final_score"],
              "label_removal_invariance": True, "label_perturbation_invariance": True,
              "prefix_invariance_50_days": True,
              "paired_uncertainty": paired_intervals(daily, base_daily, metrics["final_score"] - baseline["final_score"])}
    return result, panel, prediction, daily


def develop():
    development, mode = locked_selection()
    authority = json.loads((OUT / "official_development.json").read_text(encoding="utf-8"))
    result = {"selected_mode": mode, "development_sha256": digest(OUT / "development.json"),
              "official_development_sha256": digest(OUT / "official_development.json"),
              "synthetic_checks": synthetic_checks(), "years": {}}
    for year in (2022, 2023):
        expected = development["candidates"][mode]["years"][str(year)]
        item, _, _, _ = check_year(year, mode, expected)
        official_daily = pl.read_csv(OUT / f"official_{mode}_{year}_daily.csv")
        official_base_daily = pl.read_csv(OUT / f"official_baseline_{year}_daily.csv")
        item["official_metrics"] = authority["candidates"][mode]["years"][str(year)]
        item["official_baseline"] = authority["candidates"]["baseline"]["years"][str(year)]
        item["official_paired_uncertainty"] = paired_intervals(official_daily, official_base_daily,
            item["official_metrics"]["final_score"] - item["official_baseline"]["final_score"])
        result["years"][str(year)] = item
        print(year, mode, "audit passed", item["metrics"]["final_score"], "delta", item["score_delta"], flush=True)
    (OUT / "development_audit.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")


def diagnose():
    _, mode = locked_selection()
    dev_audit = json.loads((OUT / "development_audit.json").read_text(encoding="utf-8"))
    assert dev_audit["development_sha256"] == digest(OUT / "development.json")
    assert dev_audit["official_development_sha256"] == digest(OUT / "official_development.json")
    result, panel, prediction, daily = check_year(2024, mode)
    from experiments.official_seed_development import official_score
    official, official_daily = official_score(panel, prediction, 2024)
    baseline_pred = make_prediction(panel, {s: load_seed_raw(2024, s, panel) for s in SEEDS}, "baseline")
    official_baseline, official_base_daily = official_score(panel, baseline_pred, 2024)
    differences = {k: abs(result["metrics"][k] - v) for k, v in official.items()}
    result.update({"selected_mode": mode, "official_metrics": official,
                   "official_baseline": official_baseline,
                   "official_score_delta": official["final_score"] - official_baseline["final_score"],
                   "project_vs_official_absolute_differences": differences,
                   "official_paired_uncertainty": paired_intervals(official_daily, official_base_daily,
                        official["final_score"] - official_baseline["final_score"]),
                   "development_sha256": dev_audit["development_sha256"],
                   "official_development_sha256": dev_audit["official_development_sha256"],
                   "tie_policy": "Original evaluate.py pandas sorting is authoritative; ensembles may tie at return-Top boundaries.",
                   "limitations": ["Historical 2024 diagnosis, not a new holdout.", "HAC intervals do not account for sequential selection."]})
    (OUT / "diagnostic_2024.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    daily.write_csv(OUT / "selected_2024_daily.csv")
    official_daily.write_csv(OUT / "official_selected_2024_daily.csv")
    official_base_daily.write_csv(OUT / "official_baseline_2024_daily.csv")
    panel.frame.select("ts_code", "trade_date").with_columns(pl.Series("pred", prediction)).write_parquet(OUT / "selected_2024.parquet")
    print(json.dumps(result, ensure_ascii=False, indent=2), flush=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("stage", choices=("develop", "diagnose"))
    args = parser.parse_args()
    develop() if args.stage == "develop" else diagnose()
