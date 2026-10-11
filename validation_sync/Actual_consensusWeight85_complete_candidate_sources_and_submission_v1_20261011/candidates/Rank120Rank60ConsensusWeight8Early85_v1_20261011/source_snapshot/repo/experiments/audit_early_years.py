"""Audit two additional historical folds of the already frozen 50/50 blend.

No weights, feature groups, seeds, or years are selected by this script.
Predictions are made with blank labels before original labels enter evaluation.
"""
from __future__ import annotations

import gc
import json
import tempfile
from pathlib import Path

import numpy as np
import polars as pl

from evaluate import evaluate
from experiments import early_year_models as models
from experiments.audit_top_internal import paired_intervals
from experiments.market_blend import CANDIDATES, POSTPROCESS, make_prediction
from experiments.official_seed_development import _same_csv_daily
from experiments.seed_ensemble import file_hash
from src.research_stats import quantile_stats
from run import ROOT, fold_cutoff
from src.scoring import Panel

OUT = models.OUT
KEYS = ["ts_code", "trade_date"]
REPORT = "output/docx/赛题五量价收益预测分析报告_优化版.docx"
REPORT_SHA = "55e9019d4c8f0f6028b02f3356062b824fe5279f948e11aee223501a391f0d26"
SUBMISSION_SHA = "4135c29f64cf52c1d27b659b39da94881362353c3d22fede8cbc72b506173109"


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def verify_protocol() -> dict:
    protocol = models.check_protocol()
    prior_path = ROOT / "experiments/market_blend_eval/development.json"
    prior = read_json(prior_path)
    assert protocol["previous_development_sha256"] == file_hash(prior_path)
    assert protocol["locked_key"] == prior["selected_key"] == "full_signal_w0.5"
    assert protocol["locked_config"] == prior["selected_config"] == models.LOCKED_CONFIG
    assert protocol["postprocess"] == POSTPROCESS
    for year in models.YEARS:
        declared = protocol["folds"][str(year)]
        expected = models.EXPECTED[year]
        assert declared == {"training_cutoff_exclusive": expected["cutoff"],
                            "training_last_date": expected["last_date"],
                            "training_rows": expected["rows"]}
        assert fold_cutoff(year) == expected["cutoff"]
    return protocol


def production_integrity() -> dict:
    recorded = read_json(ROOT / "validation/prediction_audit.json")["input_sha256"]
    expected = {**recorded, REPORT: REPORT_SHA, "outputs/submission.csv": SUBMISSION_SHA}
    for relative, value in expected.items():
        assert file_hash(ROOT / relative) == value, f"Production file changed: {relative}"
    return {"unchanged": True, "verified_sha256": expected}


def source_fingerprints() -> dict:
    verify_protocol()
    sources = {}
    for year in models.YEARS:
        for variant in models.VARIANTS:
            fingerprint = models.fingerprint(year, variant)
            sources.update(fingerprint["source_sha256"])
            meta = read_json(OUT / f"early_{variant}_{year}.json")
            assert meta["fingerprint_sha256"] == fingerprint["fingerprint_sha256"]
            for extension in ("txt", "parquet", "json"):
                path = OUT / f"early_{variant}_{year}.{extension}"
                sources[str(path.relative_to(ROOT))] = file_hash(path)
    helpers = [Path(__file__), ROOT / "experiments/audit_top_internal.py",
               ROOT / "experiments/official_seed_development.py", ROOT / "report_analytics.py",
               ROOT / "validation/prediction_audit.json", ROOT / REPORT,
               ROOT / "outputs/submission.csv"]
    sources.update({str(path.relative_to(ROOT)): file_hash(path) for path in helpers})
    return dict(sorted(sources.items()))


def prediction_checks(panel: Panel, raw: np.ndarray, config: dict) -> tuple[dict, dict]:
    assert not np.isfinite(panel.y).any(), "Prediction panel must contain no labels"
    configs = {"baseline": CANDIDATES["baseline"], "fixed_blend": config}
    predictions, checks = {}, {}
    rng = np.random.default_rng(24092026)
    perturbed = Panel.from_frame(panel.frame.with_columns(
        pl.Series("y_ret_1d", rng.normal(size=len(panel.frame)))))
    prefix_rows = 50 * panel.rows_per_day
    prefix = Panel.from_frame(panel.frame.head(prefix_rows))
    for name, fixed in configs.items():
        pred = make_prediction(panel, raw, fixed)
        assert len(pred) == len(panel.frame) and np.isfinite(pred).all()
        assert np.array_equal(pred, make_prediction(perturbed, raw, fixed))
        assert np.array_equal(pred[:prefix_rows], make_prediction(prefix, raw[:prefix_rows], fixed))
        predictions[name] = pred
        checks[name] = {"prediction_labels_all_missing": True,
                        "label_perturbation_invariant": True, "prefix_50_days_exact": True,
                        "finite_all_rows": True,
                        "top_membership_preservation_claimed": False}
    return predictions, checks


def labelled_panel(panel: Panel, year: int) -> Panel:
    if year not in models.YEARS or not np.all(
            (panel.dates >= year * 10000 + 101) & (panel.dates <= year * 10000 + 1231)):
        raise ValueError("Only the two predeclared years may be evaluated")
    labels = (pl.scan_csv(ROOT / "data" / "raw" / "训练集.csv",
                         schema_overrides={"ts_code": pl.String, "trade_date": pl.Int32,
                                           "y_ret_1d": pl.Float64},
                         null_values=["NaN", "nan", ""])
              .filter(pl.col("trade_date").is_between(year * 10000 + 101, year * 10000 + 1231))
              .select(*KEYS, "y_ret_1d").collect())
    keys = panel.frame.select(KEYS)
    assert len(labels) == len(keys)
    assert keys.join(labels.select(KEYS), on=KEYS, how="anti").is_empty()
    frame = panel.frame.drop("y_ret_1d").join(labels, on=KEYS, how="left", validate="1:1")
    result = Panel.from_frame(frame)
    assert result.frame.select(KEYS).equals(keys), "Label join changed prediction ordering"
    return result


def official_score(panel: Panel, pred: np.ndarray) -> tuple[dict, pl.DataFrame]:
    pred = np.asarray(pred, dtype=float).reshape(-1)
    assert len(pred) == len(panel.frame) and np.isfinite(pred).all()
    with tempfile.TemporaryDirectory(prefix="official-early-year-score-") as temporary:
        folder = Path(temporary)
        panel.frame.select(KEYS).with_columns(pl.Series("pred", pred)).write_csv(
            folder / "submission.csv", float_precision=17)
        panel.frame.select(*KEYS, "flag_limit_up").write_csv(folder / "测试集_X.csv")
        panel.frame.select(*KEYS, "y_ret_1d").write_csv(folder / "测试集_Y.csv", float_precision=17)
        official = {key: float(value) for key, value in
                    evaluate(str(folder / "submission.csv"), str(folder)).items()}
        rebuilt, daily = _same_csv_daily(folder)
    assert set(official) == set(rebuilt)
    for key, value in official.items():
        assert np.isfinite(value) and abs(value - rebuilt[key]) <= 1e-12, (key, value, rebuilt[key])
    return official, daily


def first_day_diagnostic(candidate: pl.DataFrame, baseline: pl.DataFrame) -> dict:
    first, base = candidate.row(0, named=True), baseline.row(0, named=True)
    ic_delta, excess_delta = first["rank_ic"] - base["rank_ic"], first["excess"] - base["excess"]
    assert not np.isfinite(first["turnover"]) and not np.isfinite(base["turnover"])
    n_ic = int(np.isfinite(candidate["rank_ic"].to_numpy()).sum())
    n_excess = int(np.isfinite(candidate["excess"].to_numpy()).sum())
    return {"trade_date": int(first["trade_date"]), "rank_ic_delta": ic_delta,
            "daily_excess_delta": excess_delta,
            "contribution_to_full_score_delta": .4 * ic_delta / n_ic + .3 * 252 * excess_delta / n_excess,
            "note": "First-day component contribution only; t2-onward diagnostic retains original prediction state and is not a new strategy run."}


def run() -> dict:
    protocol = verify_protocol()
    production_before = production_integrity()
    initial = source_fingerprints()
    result = {"experiment": protocol["experiment"], "years": {},
              "fixed_key": protocol["locked_key"], "fixed_config": protocol["locked_config"],
              "no_candidate_reselection": True, "historical_stress_test_not_blind": True,
              "protocol_sha256": file_hash(OUT / "protocol.json"),
              "previous_development_sha256": protocol["previous_development_sha256"],
              "audit_source_sha256": file_hash(Path(__file__)),
              "official_daily_reconstruction_tolerance": 1e-12,
              "limitations": protocol["limitations"] + [
                  "Return Top excludes missing labels; turnover Top does not. Neither label availability nor returns enter prediction.",
                  "Stable-tie deciles are auxiliary ex-post descriptions, not the official sort or net tradeable backtests.",
                  "All annual folds cold-start the unchanged causal postprocessor on their first validation date."],
              "production_before": production_before}
    artifacts = {}
    for year in models.YEARS:
        panel = models.load_panel(year)
        auxiliary = models.load_market_raw(year, panel)
        predictions, checks = prediction_checks(panel, auxiliary, protocol["locked_config"])
        # Only now attach the held-out year's original Float64 labels.
        labelled = labelled_panel(panel, year)
        record = {"rows": len(panel.frame), "trading_days": len(panel.dates),
                  "first_date": int(panel.dates[0]), "last_date": int(panel.dates[-1]),
                  "prediction_checks": checks, "training": {}, "metrics": {}, "deciles": {}}
        for variant in models.VARIANTS:
            meta = read_json(OUT / f"early_{variant}_{year}.json")
            assert meta["training_last_date"] < meta["training_cutoff_exclusive"] < panel.dates[0]
            assert meta["training_cutoff_exclusive"] == fold_cutoff(year)
            record["training"][variant] = {key: meta[key] for key in (
                "training_rows", "training_first_date", "training_last_date",
                "training_cutoff_exclusive", "reload_check_rows", "reload_max_abs_error")}
            record["training"][variant]["feature_count"] = len(meta["features"])
        daily = {}
        for name, prediction in predictions.items():
            metrics, daily[name] = official_score(labelled, prediction)
            record["metrics"][name] = metrics
            record["deciles"][name] = quantile_stats(labelled, prediction)
            daily_path = OUT / f"official_{name}_{year}_daily.csv"
            daily[name].write_csv(daily_path)
            artifacts[str(daily_path.relative_to(ROOT))] = file_hash(daily_path)
            models.log(f"OFFICIAL {year}/{name}: score={metrics['final_score']:.12f}; "
                       f"IC={metrics['ic_mean']:.9f}; excess={metrics['annual_excess']:.9f}; "
                       f"turnover={metrics['mean_turnover']:.9f}")
        delta = record["metrics"]["fixed_blend"]["final_score"] - record["metrics"]["baseline"]["final_score"]
        record["official_score_delta"] = delta
        record["paired_uncertainty"] = paired_intervals(daily["fixed_blend"], daily["baseline"], delta)
        record["first_day_diagnostic"] = first_day_diagnostic(daily["fixed_blend"], daily["baseline"])
        record["decile_note"] = "Stable descending tie sort, bottom-to-top deciles; ex-post finite labels, no net-cost or tradeability claim."
        pred_path = OUT / f"fixed_blend_{year}.parquet"
        panel.frame.select(KEYS).with_columns(pl.Series("pred", predictions["fixed_blend"])).write_parquet(pred_path)
        artifacts[str(pred_path.relative_to(ROOT))] = file_hash(pred_path)
        result["years"][str(year)] = record
        models.log(f"FIXED BLEND {year}: delta={delta:+.12f}")
        del panel, labelled, auxiliary, predictions, daily
        gc.collect()
    assert source_fingerprints() == initial, "A locked input changed during scoring"
    result["production_after"] = production_integrity()
    assert result["production_after"] == production_before
    result["source_and_artifacts_sha256"] = {**initial, **artifacts}
    result["both_additional_years_non_decreasing"] = all(
        value["official_score_delta"] >= 0 for value in result["years"].values())
    result["automatic_promotion"] = False
    (OUT / "results.json").write_text(json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False), encoding="utf-8")
    models.log(f"Historical check complete; both years non-decreasing={result['both_additional_years_non_decreasing']}")
    return result


if __name__ == "__main__":
    run()
