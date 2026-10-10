"""Independent causal and official-score checks for a locked cached candidate.

Run `develop` before any `diagnose` command. This never overwrites production
models, predictions or reports. 2024 remains historical, not a new blind test.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import tempfile
from pathlib import Path

import numpy as np
import polars as pl

from evaluate import evaluate
from experiments.audit_top_internal import assert_top_sets_equal, paired_intervals, synthetic_panel
from experiments.cached_recheck import OUT, load_auxiliary, load_panel, make_prediction
from run import ROOT
from src.scoring import Panel, postprocess_scores, score


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(4 * 1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def selected() -> tuple[dict, dict]:
    development = json.loads((OUT / "development.json").read_text(encoding="utf-8"))
    assert development["selection_years"] == [2022, 2023]
    candidates = development["candidates"]
    assert all(set(item["years"]) == {"2022", "2023"} for item in candidates.values())
    chosen = max(candidates, key=lambda key: min(item["final_score"] for item in candidates[key]["years"].values()))
    assert chosen == development["selected_key"]
    config = development["selected_config"]
    assert config == candidates[chosen]["config"]
    for relative, expected_hash in development["cache_sha256"].items():
        assert digest(ROOT / relative) == expected_hash, f"Development cache changed: {relative}"
    return development, config


def predict(panel: Panel, config: dict):
    auxiliary = None if config["mode"] == "baseline" else load_auxiliary(config["auxiliary"], int(panel.dates[0]) // 10000, panel)
    return make_prediction(panel, auxiliary, config["mode"], config["weight"]), auxiliary


def check_synthetic() -> dict:
    rng = np.random.default_rng(21927)
    n, t = 128, 6
    valid = np.ones((t, n), dtype=bool)
    valid[2] = False
    valid[3, :120] = False
    up = np.zeros((t, n), dtype=np.int8)
    up[4] = 1
    raw = rng.normal(size=(t, n))
    raw[0] = 1.0  # Deliberately tie the Top boundary.
    auxiliary = rng.normal(size=(t, n)).reshape(-1)
    fixture = synthetic_panel(valid, up)
    panel = Panel.from_frame(fixture.frame.with_columns(pl.Series("pred_raw", raw.reshape(-1))))
    baseline = postprocess_scores(panel, raw.reshape(-1), .9, .3, True, 1.)
    assert np.array_equal(baseline, make_prediction(panel, None, "baseline", 0.))
    results = {}
    for mode in ("pure", "full_signal", "top_only"):
        pred = make_prediction(panel, auxiliary, mode, .5)
        assert np.isfinite(pred).all()
        prefix_rows = 4 * n
        prefix = Panel.from_frame(panel.frame.head(prefix_rows))
        assert np.array_equal(pred[:prefix_rows], make_prediction(prefix, auxiliary[:prefix_rows], mode, .5))
        if mode == "top_only":
            assert_top_sets_equal(panel, baseline, pred)
            assert np.array_equal(pred[:n], baseline[:n]), "Tied Top boundary must fall back"
        results[mode] = {"finite": True, "prefix_invariance": True,
                         "top_membership_preserved": mode == "top_only"}
    return results


def check_year(year: int, config: dict, expected: dict | None = None):
    panel = load_panel(year)
    prediction, auxiliary = predict(panel, config)
    baseline = make_prediction(panel, None, "baseline", 0.)
    metrics, daily = score(panel, prediction)
    baseline_metrics, baseline_daily = score(panel, baseline)
    if expected is not None:
        assert all(abs(metrics[k] - expected[k]) < 1e-12 for k in metrics)
    if config["mode"] == "top_only":
        assert_top_sets_equal(panel, baseline, prediction)
        assert np.array_equal(daily["turnover"].to_numpy(), baseline_daily["turnover"].to_numpy(), equal_nan=True)
    blank = Panel.from_frame(panel.frame.with_columns(pl.lit(None, dtype=pl.Float64).alias("y_ret_1d")))
    assert np.array_equal(prediction, make_prediction(blank, auxiliary, config["mode"], config["weight"]))
    rng = np.random.default_rng(year)
    altered = Panel.from_frame(panel.frame.with_columns(pl.Series("y_ret_1d", rng.normal(size=panel.y.size))))
    assert np.array_equal(prediction, make_prediction(altered, auxiliary, config["mode"], config["weight"]))
    rows = 50 * panel.rows_per_day
    prefix = Panel.from_frame(panel.frame.head(rows))
    prefix_aux = None if auxiliary is None else auxiliary[:rows]
    assert np.array_equal(prediction[:rows], make_prediction(prefix, prefix_aux, config["mode"], config["weight"]))
    delta = metrics["final_score"] - baseline_metrics["final_score"]
    result = {"metrics": metrics, "baseline": baseline_metrics, "score_delta": delta,
              "label_removal_invariance": True, "label_perturbation_invariance": True,
              "prefix_invariance_50_days": True,
              "top_membership_invariance": config["mode"] in ("top_only", "baseline"),
              "paired_uncertainty": paired_intervals(daily, baseline_daily, delta)}
    return result, panel, prediction, daily


def develop() -> None:
    development, config = selected()
    result = {"config": config, "development_sha256": digest(OUT / "development.json"),
              "synthetic_checks": check_synthetic(), "years": {}}
    for year in (2022, 2023):
        expected = development["candidates"][development["selected_key"]]["years"][str(year)]
        item, _, _, _ = check_year(year, config, expected)
        result["years"][str(year)] = item
        print(year, "selected audit passed", item["metrics"]["final_score"],
              "delta", item["score_delta"], flush=True)
    (OUT / "development_audit.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")


def diagnose() -> None:
    _, config = selected()
    dev_audit = json.loads((OUT / "development_audit.json").read_text(encoding="utf-8"))
    assert dev_audit["development_sha256"] == digest(OUT / "development.json")
    result, panel, prediction, daily = check_year(2024, config)
    source_y = pl.scan_csv(ROOT / "data" / "raw" / "训练集.csv", schema_overrides={
        "ts_code": pl.String, "trade_date": pl.Int32, "y_ret_1d": pl.Float64},
        null_values=["NaN", "nan", ""]).filter(pl.col("trade_date").is_between(20240101, 20241231))
    source_y = source_y.select("ts_code", "trade_date", "y_ret_1d").collect()
    exact_frame = panel.frame.drop("y_ret_1d").join(source_y, on=["ts_code", "trade_date"],
        how="left", validate="1:1").sort("trade_date", "ts_code")
    exact = Panel.from_frame(exact_frame)
    independent, _ = score(exact, prediction)
    with tempfile.TemporaryDirectory(prefix="cached-candidate-score-") as folder:
        temporary = Path(folder)
        exact_frame.select("ts_code", "trade_date").with_columns(pl.Series("pred", prediction)).write_csv(
            temporary / "submission.csv", float_precision=17)
        exact_frame.select("ts_code", "trade_date", "y_ret_1d").write_csv(temporary / "测试集_Y.csv", float_precision=17)
        exact_frame.select("ts_code", "trade_date", "flag_limit_up").write_csv(temporary / "测试集_X.csv")
        official = {key: float(value) for key, value in evaluate(str(temporary / "submission.csv"), str(temporary)).items()}
    differences = {key: abs(independent[key] - value) for key, value in official.items()}
    for key, value in differences.items():
        tolerance = 1e-4 if key == "icir" else 1e-5
        if key in ("mean_turnover", "ic_positive_ratio"):
            tolerance = 1e-12
        assert value <= tolerance, (key, value)
    result.update({"config": config, "official_metrics": official,
                   "official_comparison_absolute_differences": differences,
                   "development_sha256": dev_audit["development_sha256"],
                   "limitations": ["Exploratory multi-candidate selection; HAC intervals are not selection-adjusted.",
                                   "2024 has been repeatedly examined and is not an untouched holdout."]})
    (OUT / "diagnostic_2024.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    daily.write_csv(OUT / "selected_2024_daily.csv")
    exact_frame.select("ts_code", "trade_date").with_columns(pl.Series("pred", prediction)).write_parquet(OUT / "selected_2024.parquet")
    print(json.dumps(result, ensure_ascii=False, indent=2), flush=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("stage", choices=("develop", "diagnose"))
    args = parser.parse_args()
    develop() if args.stage == "develop" else diagnose()
