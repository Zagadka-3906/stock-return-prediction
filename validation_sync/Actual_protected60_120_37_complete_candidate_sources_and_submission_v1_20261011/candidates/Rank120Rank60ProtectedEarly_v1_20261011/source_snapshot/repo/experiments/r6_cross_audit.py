"""Read-only independent checks of the frozen r6 CPU experiments.

New audit evidence is written only to r6_cross_audit_20260926. No experiment
source, fitted model, prediction, original report or original manifest is edited.
"""
from __future__ import annotations

import os
for _thread in ("POLARS_MAX_THREADS", "OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_thread] = "4"

import argparse
import hashlib
import json
from pathlib import Path
import sys

import numpy as np
import polars as pl
from scipy.stats import spearmanr

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from experiments.r6_transformer_audit import independent_official_score

OUT = ROOT / "experiments/r6_cross_audit_20260926"
R4 = ROOT / "experiments/revalidation_20260926/validation"
KEYS = ["ts_code", "trade_date"]
HASH_CACHE = {}


def sha(path):
    path = Path(path).resolve()
    stat = path.stat()
    key = (str(path), stat.st_size, stat.st_mtime_ns)
    if key not in HASH_CACHE:
        with path.open("rb") as stream:
            HASH_CACHE[key] = hashlib.file_digest(stream, "sha256").hexdigest()
    return HASH_CACHE[key]


def read(path):
    return json.loads(Path(path).read_text(encoding="utf-8-sig"))


def write_new(path, value):
    if not Path(path).resolve().is_relative_to(OUT.resolve()):
        raise ValueError("Audit writes are restricted to the new cross-audit directory")
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with Path(path).open("x", encoding="utf-8") as stream:
        json.dump(value, stream, ensure_ascii=False, indent=2, allow_nan=False)


def verify_map(base, mapping):
    for relative, digest in mapping.items():
        path = (base / relative).resolve()
        if not path.is_relative_to(ROOT.resolve()) or sha(path) != digest:
            raise AssertionError(f"Frozen artifact/hash mismatch: {relative}")


def checked_protocol(unit):
    protocol = read(unit / "protocol.json")
    verify_map(ROOT, protocol["input_sha256"])
    return protocol


def unchanged_snapshot(unit):
    return {p.name: sha(p) for p in unit.iterdir() if p.is_file()}


def assert_unchanged(unit, snapshot):
    for name, digest in snapshot.items():
        if sha(unit / name) != digest:
            raise AssertionError(f"Original unit changed during independent audit: {name}")


def close_numbers(actual, expected, context, tolerance=1e-12):
    differences = {}
    for key, value in actual.items():
        if value is None:
            assert expected[key] is None, context
            continue
        delta = float(value) - float(expected[key])
        if not np.isfinite(delta) or abs(delta) > tolerance:
            raise AssertionError(f"Mismatch: {context}/{key}: {delta}")
        differences[key] = delta
    return differences


def independently_sum_five(dates, returns):
    """Separate implementation using cumulative sums and missing-count windows."""
    finite = np.isfinite(returns)
    mean = np.array([row[keep].mean() for row, keep in zip(returns, finite)])
    excess = returns - mean[:, None]
    safe = np.where(finite, excess, 0.)
    cumulative = np.vstack([np.zeros((1, returns.shape[1])), np.cumsum(safe, axis=0)])
    missing = np.vstack([np.zeros((1, returns.shape[1]), dtype=np.int32), np.cumsum(~finite, axis=0)])
    target = np.full_like(returns, np.nan)
    length = len(dates) - 5
    values = cumulative[5:5+length] - cumulative[:length]
    complete = missing[5:5+length] == missing[:length]
    target[:length] = np.where(complete, values, np.nan)
    available = np.r_[dates[5:], np.full(5, -1)]
    return target, excess, available


def audit_value5():
    unit = ROOT / "experiments/r6_value5_20260926"
    destination = OUT / "value5_audit.json"
    if destination.exists():
        raise FileExistsError("Independent value5 audit already recorded")
    protocol = checked_protocol(unit)
    before = unchanged_snapshot(unit)
    development, record, fitted = read(unit / "development.json"), read(unit / "result_2022.json"), read(unit / "calibrators.json")
    assert development["protocol_sha256"] == fitted["protocol_sha256"] == sha(unit / "protocol.json")
    assert development["calibrators_sha256"] == record["calibrators_sha256"] == sha(unit / "calibrators.json")
    assert development["result_sha256"] == sha(unit / "result_2022.json")
    verify_map(unit, record["artifact_sha256"])
    prediction = pl.read_parquet(unit / "predictions_2022.parquet").sort("trade_date", "ts_code")
    reference = pl.read_parquet(R4 / "predictions_ensemble4_2022.parquet", columns=KEYS + ["pred_raw", "price_valid", "flag_limit_up", "y_ret_1d"]).sort("trade_date", "ts_code")
    assert prediction.select(KEYS).equals(reference.select(KEYS))
    assert prediction.select("price_valid", "flag_limit_up").equals(reference.select("price_valid", "flag_limit_up"))
    # Read only the already evaluated 2020-2022 original labels, in Float64.
    original = (pl.scan_csv(ROOT / "data" / "raw" / "训练集.csv", schema_overrides={"ts_code": pl.String,
        "trade_date": pl.Int32, "y_ret_1d": pl.Float64}, null_values=["NaN", "nan", ""])
        .filter(pl.col("trade_date").is_between(20200101, 20221231))
        .select(KEYS + ["y_ret_1d"]).sort("trade_date", "ts_code").collect())
    current = original.filter(pl.col("trade_date") // 10000 == 2022)
    assert current.select(KEYS).equals(prediction.select(KEYS))
    assert np.array_equal(current["y_ret_1d"].to_numpy(), reference["y_ret_1d"].to_numpy(), equal_nan=True)
    dates = current["trade_date"].unique(maintain_order=True).to_numpy()
    stocks = current["ts_code"].n_unique()
    expected_y5, expected_y1, available = independently_sum_five(dates, current["y_ret_1d"].to_numpy().reshape(-1, stocks))
    saved_y5 = prediction["y5_raw_excess_sum"].to_numpy().reshape(-1, stocks)
    saved_y1 = prediction["y1_raw_excess"].to_numpy().reshape(-1, stocks)
    assert np.array_equal(np.isfinite(expected_y5), np.isfinite(saved_y5))
    target_error = float(np.nanmax(np.abs(expected_y5-saved_y5)))
    one_error = float(np.nanmax(np.abs(expected_y1-saved_y1)))
    assert target_error <= 1e-12 and one_error <= 1e-12
    assert np.array_equal(np.repeat(available, stocks), prediction["label_available_date"].to_numpy())
    assert dates[-5:].tolist() == record["last_five_signal_dates_excluded"]

    # Independently validate the continuous 2020/2021 target and five-date purge.
    training_raw = original.filter(pl.col("trade_date") // 10000 < 2022)
    training_reference = pl.concat([pl.read_parquet(R4 / f"predictions_ensemble4_{year}.parquet", columns=KEYS+["price_valid", "y_ret_1d"]) for year in (2020, 2021)]).sort("trade_date", "ts_code")
    assert training_raw.select(KEYS).equals(training_reference.select(KEYS))
    assert np.array_equal(training_raw["y_ret_1d"].to_numpy(), training_reference["y_ret_1d"].to_numpy(), equal_nan=True)
    train_dates = training_raw["trade_date"].unique(maintain_order=True).to_numpy()
    training_y5, _, training_available = independently_sum_five(train_dates, training_raw["y_ret_1d"].to_numpy().reshape(-1, stocks))
    ends = np.repeat(training_available, stocks)
    keep = training_reference["price_valid"].to_numpy() & np.isfinite(training_y5.ravel()) & (ends > 0) & (ends < dates[0])
    train_values = training_y5.ravel()[keep]
    selected_dates = training_raw["trade_date"].to_numpy()[keep]
    training_stats = {"target_mean": float(train_values.mean()), "target_std": float(train_values.std()),
                      "target_min": float(train_values.min()), "target_max": float(train_values.max()),
                      "complete_purged_training_rows": int(keep.sum()),
                      "max_training_signal_date": int(selected_dates.max()),
                      "max_training_label_available_date": int(ends[keep].max())}
    close_numbers(training_stats, fitted, "training_target")
    assert train_dates[-5:].tolist() == fitted["purged_final_market_dates"]
    assert not keep[-5*stocks:].any() and training_stats["max_training_label_available_date"] < dates[0]
    weighted_intercept = float(np.mean([train_values[selected_dates == date].mean() for date in np.unique(selected_dates)]))
    for model in fitted["models"].values():
        assert abs(model["intercept"] - weighted_intercept) <= 1e-12
        assert model["training_dates"] == len(np.unique(selected_dates)) and model["training_rows"] == len(train_values)

    # Independent daily reconstruction uses verified saved Float64 targets to
    # preserve exact ties instead of breaking them by cumsum rounding (~1e-15).
    valid = (prediction["price_valid"].to_numpy() & np.isfinite(reference["pred_raw"].to_numpy())).reshape(-1, stocks)
    flags = prediction["flag_limit_up"].to_numpy().reshape(-1, stocks)
    names = ("candidate", "joint_rank_ema", "raw_only", "ema_only", "raw_rank", "ema09")
    signals = {name: prediction["value5_"+name if name in fitted["models"] else name].to_numpy().reshape(-1, stocks) for name in names}
    rows = []
    for day, date in enumerate(dates[:-5]):
        observed = valid[day] & np.isfinite(saved_y5[day])
        one_observed = valid[day] & np.isfinite(saved_y1[day])
        pool = np.flatnonzero(flags[day] == 0)
        count = max(len(pool)//10, 1)
        for name, values in signals.items():
            signal = np.where(valid[day], values[day], -1e6)
            members = pool[np.argsort(-signal[pool], kind="stable")[:count]]
            measured = members[np.isfinite(saved_y5[day, members])]
            rows.append({"trade_date": int(date), "signal": name, "target_rows": int(observed.sum()),
                "rank_ic5": float(spearmanr(signal[observed], saved_y5[day, observed]).statistic),
                "rank_ic1": float(spearmanr(signal[one_observed], saved_y1[day, one_observed]).statistic),
                "mse5": float(np.mean((signal[observed]-saved_y5[day, observed])**2)) if name in fitted["models"] else None,
                "top5_excess_sum_mean": float(saved_y5[day, measured].mean()),
                "top_selected": count, "top_target_observed": len(measured), "top_target_coverage": len(measured)/count,
                "top_invalid_price_selected": int((~valid[day, members]).sum())})
    rebuilt = pl.DataFrame(rows).sort("trade_date", "signal")
    frozen_daily = pl.read_csv(unit / "daily_2022.csv").sort("trade_date", "signal")
    assert rebuilt.select("trade_date", "signal").equals(frozen_daily.select("trade_date", "signal"))
    daily_errors = {}
    for column in rebuilt.columns:
        if column in ("trade_date", "signal"):
            continue
        a, b = rebuilt[column].cast(pl.Float64).to_numpy(), frozen_daily[column].cast(pl.Float64).to_numpy()
        assert np.array_equal(np.isfinite(a), np.isfinite(b)), column
        daily_errors[column] = float(np.nanmax(np.abs(a-b)))
        assert daily_errors[column] <= 1e-12, (column, daily_errors[column])
    summary = {}
    for name in names:
        frame = rebuilt.filter(pl.col("signal") == name)
        summary[name] = {"days": len(frame), **{k: (float(frame[k].mean()) if frame[k].drop_nulls().len() else None) for k in
            ("rank_ic5", "rank_ic1", "mse5", "top5_excess_sum_mean", "top_target_coverage")},
            "min_top_target_coverage": float(frame["top_target_coverage"].min()),
            "max_top_invalid_price_selected": int(frame["top_invalid_price_selected"].max())}
        close_numbers(summary[name], record["metrics"][name], name)
    a = rebuilt.filter(pl.col("signal") == "candidate")
    b = rebuilt.filter(pl.col("signal") == "joint_rank_ema")
    delta = b["mse5"].to_numpy() - a["mse5"].to_numpy()
    rng = np.random.default_rng(2026)
    starts = rng.integers(0, len(delta)-19, size=(5000, (len(delta)+19)//20))
    positions = (starts[..., None] + np.arange(20)).reshape(5000, -1)[:, :len(delta)]
    draws = delta[positions].mean(1)
    bootstrap = {"mean_daily_mse_reduction": float(delta.mean()), "positive_share": float((draws > 0).mean()),
                 "ci95": np.quantile(draws, [.025, .975]).tolist()}
    close_numbers({k: bootstrap[k] for k in ("mean_daily_mse_reduction", "positive_share")}, record["bootstrap"], "bootstrap")
    np.testing.assert_allclose(bootstrap["ci95"], record["bootstrap"]["ci95"], rtol=0, atol=1e-12)
    c, b = summary["candidate"], summary["joint_rank_ema"]
    comparison = {"relative_daily_mse_improvement": (b["mse5"]-c["mse5"])/b["mse5"],
                  "rank_ic5_delta": c["rank_ic5"]-b["rank_ic5"],
                  "top5_return_delta": c["top5_excess_sum_mean"]-b["top5_excess_sum_mean"]}
    close_numbers(comparison, development["gate"]["comparison"], "gate")
    expected_gates = {"relative_daily_mse_improvement_min": .001, "rank_ic5_delta_min": .002, "top5_return_delta_min": .0001, "bootstrap_positive_share_min": .8}
    assert all(protocol["gates"][key] == value for key, value in expected_gates.items())
    conditions = {k: value >= expected_gates[k+"_min"] for k, value in comparison.items()}
    conditions["bootstrap"] = bootstrap["positive_share"] >= .8
    assert conditions == development["gate"]["conditions"]
    passed = all(conditions.values())
    assert passed == development["gate"]["passed"] == development["confirmation_allowed"]
    if not passed:
        assert not (unit / "confirmation.json").exists()
        assert not any((unit/f"result_{year}.json").exists() or (unit/f"predictions_{year}.parquet").exists() for year in (2023, 2024))
    OUT.mkdir(parents=True, exist_ok=True)
    rebuilt.write_csv(OUT / "value5_2022_independent_daily.csv", float_precision=17)
    assert_unchanged(unit, before)
    result = {"status": "passed", "gate_passed": passed, "confirmation_absent_after_failure": not passed,
        "source_sha256": sha(Path(__file__)), "original_unit_snapshot_sha256": before,
        "original_float64_labels_exact_in_r4_2020_2021_2022": True,
        "five_day_target_full_2022_max_abs_error": target_error, "one_day_excess_max_abs_error": one_error,
        "label_missingness_and_available_dates_exact": True, "continuous_training_target_stats": training_stats,
        "train_date_balanced_intercept_max_abs_error": max(abs(m["intercept"]-weighted_intercept) for m in fitted["models"].values()),
        "daily_metric_max_abs_errors": daily_errors, "metrics": summary, "comparison": comparison,
        "bootstrap": bootstrap, "conditions": conditions,
        "original_unit_files_unchanged": True, "new_model_fitting": False,
        "limitations": "Independent numeric/chronology audit, not proof of prediction quality. Verified saved target used for IC to retain original exact ties; independently rebuilt cumsum target agrees within 1e-12. Overlapping five-day research excess is neither official score nor executable return."}
    write_new(destination, result)
    return result


def audit_topk():
    unit = ROOT / "experiments/r6_topk_20260926"
    destination = OUT / "topk_audit.json"
    if destination.exists():
        raise FileExistsError("Independent Top-K audit already recorded")
    protocol = checked_protocol(unit)
    before = unchanged_snapshot(unit)
    development = read(unit / "development.json")
    assert development["protocol_sha256"] == sha(unit / "protocol.json")
    metrics, errors = {}, {}
    key = "topk_return_backbone"
    for year in (2020, 2021, 2022):
        path = unit / f"fold_{year}.json"
        assert sha(path) == development["fold_sha256"][str(year)]
        fold = read(path)
        assert fold["year"] == year and fold["candidate"] == key
        verify_map(unit, fold["artifact_sha256"])
        prediction_path = unit / f"predictions_{key}_{year}.parquet"
        assert prediction_path.name in fold["artifact_sha256"]
        measured, daily, checks = independent_official_score(prediction_path, year)
        difference = close_numbers(measured, fold["metrics"], f"topk/{year}")
        frozen_daily = pl.read_csv(unit / f"daily_{key}_{year}.csv", null_values=["NaN"])
        assert daily["trade_date"].equals(frozen_daily["trade_date"])
        daily_errors = {}
        for column in ("rank_ic", "excess", "turnover"):
            a, b = daily[column].to_numpy(), frozen_daily[column].to_numpy()
            assert np.array_equal(np.isfinite(a), np.isfinite(b))
            daily_errors[column] = float(np.nanmax(np.abs(a-b)))
            assert daily_errors[column] <= 1e-12
        OUT.mkdir(parents=True, exist_ok=True)
        daily.write_csv(OUT / f"topk_{year}_independent_daily.csv", float_precision=17)
        metrics[str(year)] = measured
        errors[str(year)] = {"metric_differences": difference, "daily_max_abs_differences": daily_errors, "official_reconstruction": checks}
        print(f"independent TopK {year}: {measured['final_score']:.12f}", flush=True)
    thresholds = protocol["gates"]["development"]
    assert thresholds == {"mean": .001, "worst": -.005, "ic": -.002}
    anchor = read(R4 / "summary.json")["metrics"]
    comparisons = {}
    for reference in ("baseline", "ensemble4"):
        score = [metrics[str(y)]["final_score"] - anchor[str(y)][reference]["final_score"] for y in (2020, 2021, 2022)]
        ic = [metrics[str(y)]["ic_mean"] - anchor[str(y)][reference]["ic_mean"] for y in (2020, 2021, 2022)]
        comparisons[reference] = {"annual_score_delta": dict(zip(map(str, (2020,2021,2022)), score)),
            "mean_score_delta": float(np.mean(score)), "worst_score_delta": min(score), "mean_ic_delta": float(np.mean(ic)),
            "passed": bool(np.mean(score)>=.001 and min(score)>=-.005 and np.mean(ic)>=-.002)}
        expected = development["gate"]["comparisons"][reference]
        close_numbers({k: v for k,v in comparisons[reference].items() if k not in ("annual_score_delta", "passed")}, expected, reference)
        assert comparisons[reference]["passed"] == expected["passed"]
    passed = all(v["passed"] for v in comparisons.values())
    assert passed == development["gate"]["passed"]
    if not passed:
        assert not (unit / "confirmation.json").exists()
        assert not any((unit/f"fold_{y}.json").exists() for y in (2023,2024))
    assert_unchanged(unit, before)
    result = {"status": "passed", "gate_passed": passed, "source_sha256": sha(Path(__file__)),
        "original_unit_snapshot_sha256": before, "historical_metrics": metrics,
        "independent_scoring_checks": errors, "comparisons": comparisons,
        "original_unit_files_unchanged": True, "original_float64_csv_labels_used": True,
        "new_model_fitting": False, "confirmation_absent_after_failure": not passed,
        "limitation": "References anchored to frozen audited r4 summary; no new candidate or confirmation scored. Numeric audit does not establish unseen superiority or executable returns."}
    write_new(destination, result)
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("stage", choices=("value5", "topk", "all"))
    args = parser.parse_args()
    stages = ("value5", "topk") if args.stage == "all" else (args.stage,)
    for stage in stages:
        result = {"value5": audit_value5, "topk": audit_topk}[stage]()
        print(json.dumps({"unit": stage, "status": result["status"], "gate_passed": result["gate_passed"]}, ensure_ascii=False))
