"""Attribute frozen R7 predictions and benchmark an equivalent scoring path.

No model, signal, parameter or promotion gate is changed by this diagnostic.
Prepare freezes code and input hashes before reading historical attribution.
"""
from __future__ import annotations

import argparse
from datetime import datetime
import gc
import hashlib
import json
import os
from pathlib import Path
import sys
import time

sys.dont_write_bytecode = True
os.environ.setdefault("POLARS_MAX_THREADS", "6")
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import numpy as np
import pandas as pd
import polars as pl
from loguru import logger

OUT = ROOT / "experiments/r8_diagnostics_20260926"
R7 = ROOT / "experiments/r7_complement_20260926"
R4 = ROOT / "experiments/revalidation_20260926/validation"
YEARS = (2020, 2021, 2022)
SOURCES = ("r8_diagnose_and_speed.py", "r8_fast_official.py", "r8_attribution_core.py",
           "r8_notes_20260926.md")
KEYS = ["ts_code", "trade_date"]
DAILY = ["rank_ic", "excess", "top1_return", "turnover"]
logger.disable("evaluate")


def sha(path):
    with Path(path).open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def read(path):
    return json.loads(Path(path).read_text(encoding="utf-8-sig"))


def write_new(path, value):
    path = Path(path)
    if path.exists():
        raise FileExistsError(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    pending = path.with_name("." + path.name + ".pending")
    content = value if isinstance(value, str) else json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False) + "\n"
    with pending.open("x", encoding="utf-8", newline="\n") as stream:
        stream.write(content)
    pending.rename(path)


def save_frame(path, frame):
    path = Path(path)
    if path.exists():
        raise FileExistsError(path)
    pending = path.with_name("." + path.name + ".pending")
    if pending.exists():
        raise FileExistsError(pending)
    if isinstance(frame, pd.DataFrame):
        frame = pl.from_pandas(frame)
    if path.suffix == ".parquet":
        frame.write_parquet(pending, compression="zstd")
    else:
        frame.write_csv(pending, float_precision=17)
    pending.rename(path)


def log(message):
    print(f"[{datetime.now():%H:%M:%S}] {message}", flush=True)


def hash_map(paths):
    return {p.relative_to(ROOT).as_posix(): sha(p) for p in sorted(set(paths))}


def verify_map(hashes):
    for name, expected in hashes.items():
        path = (ROOT / name).resolve()
        if not path.is_relative_to(ROOT.resolve()) or sha(path) != expected:
            raise AssertionError(f"Changed or unsafe input: {name}")


def input_paths():
    paths = [ROOT / "active_release.json", R7 / "result_manifest.json", R7 / "decision.json",
             ROOT / "evaluate.py", ROOT / "experiments/revalidate_fold_local.py",
             ROOT / "experiments/official_seed_development.py"]
    for year in YEARS:
        paths += [R7 / f"fold_{year}.json", R7 / f"predictions_neural10_{year}.parquet",
                  R4 / f"predictions_ensemble4_{year}.parquet"]
        paths += [R7 / "independent_audit/development" / f"official_{name}_{year}_daily.csv"
                  for name in ("ensemble4", "neural10")]
    paths.append(R7 / "independent_audit/development/official_neural10_raw_2021_daily.csv")
    return paths


def integration_tests():
    from experiments.r8_fast_official import PreparedOfficialPanel
    from experiments.r8_attribution_core import attribute_year
    rng = np.random.default_rng(2026)
    count = 360
    fixture = pl.DataFrame({"ts_code": [f"S{i:03}" for i in range(120)] * 3,
        "trade_date": np.repeat([20200102, 20200103, 20200203], 120),
        "flag_limit_up": np.zeros(count, dtype=int), "y_ret_1d": rng.normal(0, .02, count),
        "pred": rng.integers(0, 15, count).astype(float)})
    context = PreparedOfficialPanel.from_frame(fixture)
    first = fixture["pred"].to_numpy()
    second = first + rng.integers(-2, 3, count)
    pair = context.merged(first).rename(columns={"pred": "pred_base"})
    pair["pred_candidate"] = context.merged(second)["pred"].to_numpy()
    daily, _, summary = attribute_year(pair)
    for name, predictions in (("base", first), ("candidate", second)):
        metrics, expected_daily = context.score(predictions)
        compare_metrics(summary["metrics"][name], metrics)
        derived = daily[["trade_date"] + [f"{name}_{key}" for key in DAILY]].rename(
            columns={f"{name}_{key}": key for key in DAILY})
        compare_daily(derived, expected_daily)
    return {"status": "passed", "synthetic_only": True, "fast_to_attribution_roundtrip": True}


def prepare():
    from experiments import r8_fast_official as fast, r8_attribution_core as attribution
    from experiments.finalize_r7 import verify as verify_r7
    if (OUT / "protocol.json").exists():
        raise FileExistsError("Frozen diagnostic already exists")
    tests = {"fast_official": fast.tests(), "attribution": attribution.synthetic_tests(),
             "integration": integration_tests()}
    if any(result["status"] != "passed" for result in tests.values()):
        raise AssertionError(tests)
    previous = verify_r7()
    write_new(OUT / "tests.json", tests)
    protocol = {
        "purpose": "Frozen R7 final-Top attribution and equivalent scorer engineering benchmark",
        "frozen_at_local": datetime.now().astimezone().isoformat(), "years": list(YEARS),
        "new_predictive_candidates": 0, "training": False, "retune_or_promotion": False,
        "historical_years_previously_viewed": True,
        "attribution": "Official return Top filters missing labels; turnover Top does not. Return delta is the signed sum of added/removed y divided by common daily K. IC, return, turnover use separate annual observation counts.",
        "sensitivity": "Remove at most five positive daily/stock attribution terms, keeping annual denominators and all predictions unchanged. Arithmetic concentration diagnostic, never a counterfactual portfolio or new score gate.",
        "scoring": "Reuse original float17 Polars CSV serialization and pandas default parsing, original merge order and default descending sort. Compare all eight aggregate and four daily metrics to frozen independent official records.",
        "benchmark": {"year": 2021, "prediction": "r4 final", "warmup_pairs": 1,
                      "measured_pairs": 3, "alternating_order": True,
                      "baseline": "revalidate_fold_local.score_official including CSV IO and official/daily double computation",
                      "optimized": "PreparedOfficialPanel.score including prediction CSV round trip and daily metrics",
                      "context_preparation_timed_separately": True},
        "sources_sha256": hash_map([ROOT / "experiments" / name for name in SOURCES]),
        "input_sha256": hash_map(input_paths() + [OUT / "tests.json"]),
        "previous_r7_verification": previous,
        "versions": {"python": sys.version, "numpy": np.__version__, "pandas": pd.__version__, "polars": pl.__version__},
        "documentation": ["https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.sort_values.html",
                          "https://pandas.pydata.org/docs/user_guide/groupby.html"],
    }
    write_new(OUT / "protocol.json", protocol)
    return {"status": "frozen", "historical_attribution_run": False, "protocol_sha256": sha(OUT / "protocol.json")}


def checked_protocol():
    protocol = read(OUT / "protocol.json")
    verify_map(protocol["sources_sha256"])
    verify_map(protocol["input_sha256"])
    if protocol["years"] != list(YEARS) or protocol["new_predictive_candidates"] != 0:
        raise AssertionError("Unexpected diagnostic scope")
    return protocol


def compare_metrics(actual, expected):
    if set(actual) != set(expected):
        raise AssertionError("Metric keys differ")
    differences = {name: float(abs(actual[name] - expected[name])) for name in actual}
    if not all(np.isfinite(d) and d <= 1e-12 for d in differences.values()):
        raise AssertionError(differences)
    return differences


def compare_daily(actual, expected):
    if isinstance(actual, pd.DataFrame):
        actual = pl.from_pandas(actual)
    np.testing.assert_array_equal(actual["trade_date"].to_numpy(), expected["trade_date"].to_numpy())
    differences = {}
    for name in DAILY:
        a, b = actual[name].to_numpy().astype(float), expected[name].to_numpy().astype(float)
        np.testing.assert_allclose(a, b, atol=1e-12, rtol=0, equal_nan=True)
        differences[name] = float(np.nanmax(np.abs(a - b)))
    return differences


def frames(year):
    cols = KEYS + ["flag_limit_up", "y_ret_1d", "pred"]
    base = pl.read_parquet(R4 / f"predictions_ensemble4_{year}.parquet", columns=cols).sort("trade_date", "ts_code")
    candidate = pl.read_parquet(R7 / f"predictions_neural10_{year}.parquet", columns=cols + ["pred_raw"]).sort("trade_date", "ts_code")
    if not base.select(KEYS + ["flag_limit_up", "y_ret_1d"]).equals(candidate.select(KEYS + ["flag_limit_up", "y_ret_1d"])):
        raise AssertionError("Prediction keys, flags or original Float64 labels differ")
    if base.schema["y_ret_1d"] != pl.Float64:
        raise AssertionError("Float64 labels required")
    return base, candidate


def timed(call):
    started = time.perf_counter()
    result = call()
    return result, time.perf_counter() - started


def benchmark():
    from experiments.r8_fast_official import PreparedOfficialPanel
    from experiments.revalidate_fold_local import score_official
    base, _ = frames(2021)
    pred = base["pred"].to_numpy()
    context, prep_seconds = timed(lambda: PreparedOfficialPanel.from_frame(base))
    expected = read(R7 / "fold_2021.json")["references"]["ensemble4"]
    original = lambda: score_official(base, pred)
    optimized = lambda: context.score(pred)
    for call in (original, optimized):
        metric, _ = call()
        compare_metrics(metric, expected)
    runs = []
    for pair in range(3):
        current = {"pair": pair + 1}
        functions = (("original", original), ("optimized", optimized))
        for name, call in (functions if pair % 2 == 0 else functions[::-1]):
            (metric, daily), seconds = timed(call)
            compare_metrics(metric, expected)
            compare_daily(daily, pl.read_csv(R7 / "independent_audit/development/official_ensemble4_2021_daily.csv"))
            current[name + "_seconds"] = seconds
        runs.append(current)
        log(f"benchmark pair {pair + 1}: {current}")
    old = float(np.median([r["original_seconds"] for r in runs]))
    new = float(np.median([r["optimized_seconds"] for r in runs]))
    return {"year": 2021, "rows": base.height, "context_preparation_seconds": prep_seconds,
            "measured_pairs": runs, "original_median_seconds": old, "optimized_median_seconds": new,
            "warm_reuse_speedup": old / new, "first_context_plus_median_score_seconds": prep_seconds + new,
            "cold_estimate_speedup": old / (prep_seconds + new),
            "limitation": "Same process, warm filesystem, three alternating pairs. Hardware-specific engineering timing, not model quality or guaranteed deployment latency."}


def run():
    from experiments.r8_fast_official import PreparedOfficialPanel
    from experiments.r8_attribution_core import attribute_year
    checked_protocol()
    if (OUT / "result_manifest.json").exists():
        raise FileExistsError("Completed diagnostic is immutable; use verify")
    results = {}
    for year in YEARS:
        log(f"attribution and exact-score checks {year}")
        base, candidate = frames(year)
        context = PreparedOfficialPanel.from_frame(base)
        previous = read(R7 / f"fold_{year}.json")
        checks = {}
        for name, values, expected in (("ensemble4", base["pred"], previous["references"]["ensemble4"]),
                                       ("neural10", candidate["pred"], previous["metrics"])):
            metrics, daily = context.score(values.to_numpy())
            frozen = pl.read_csv(R7 / "independent_audit/development" / f"official_{name}_{year}_daily.csv")
            checks[name] = {"aggregate_abs_difference": compare_metrics(metrics, expected),
                            "daily_max_abs_difference": compare_daily(daily, frozen)}
        if year == 2021:
            metrics, daily = context.score(candidate["pred_raw"].to_numpy())
            checks["existing_raw_control"] = {"aggregate_abs_difference": compare_metrics(metrics, previous["raw_metrics"]),
                "daily_max_abs_difference": compare_daily(daily, pl.read_csv(R7 / "independent_audit/development/official_neural10_raw_2021_daily.csv"))}
        pair = context.merged(base["pred"].to_numpy()).rename(columns={"pred": "pred_base"})
        other = context.merged(candidate["pred"].to_numpy())
        pd.testing.assert_frame_equal(pair.drop(columns="pred_base"), other.drop(columns="pred"))
        pair["pred_candidate"] = other["pred"].to_numpy()
        daily, stocks, summary = attribute_year(pair)
        # The attribution core computes its own official metrics and daily series.
        for name, saved_name in (("base", "ensemble4"), ("candidate", "neural10")):
            expected = previous["references"]["ensemble4"] if name == "base" else previous["metrics"]
            compare_metrics(summary["metrics"][name], expected)
            derived = daily[["trade_date"] + [f"{name}_{key}" for key in DAILY]].rename(columns={f"{name}_{key}": key for key in DAILY})
            compare_daily(derived, pl.read_csv(R7 / "independent_audit/development" / f"official_{saved_name}_{year}_daily.csv"))
        save_frame(OUT / f"daily_attribution_{year}.csv", daily)
        save_frame(OUT / f"stock_attribution_{year}.parquet", stocks)
        write_new(OUT / f"attribution_{year}.json", summary)
        results[str(year)] = {"score_checks": checks, "summary": summary}
        del pair, other, context, base, candidate, daily, stocks
        gc.collect()
    timing = benchmark()
    write_new(OUT / "benchmark.json", timing)
    write_new(OUT / "summary.json", {"years": results, "benchmark": timing, "new_candidates": 0,
                                      "formal_release": "ensemble4_r4", "promotion": False})
    checked_protocol()
    return {"status": "computed", "warm_reuse_speedup": timing["warm_reuse_speedup"], "new_candidates": 0}


def inventory():
    paths = [p for p in OUT.rglob("*") if p.is_file() and p.name != "result_manifest.json"]
    if any(p.name.endswith(".pending") for p in paths):
        raise AssertionError("Incomplete write exists")
    return hash_map(paths)


def seal():
    checked_protocol()
    if not (OUT / "结论.md").exists() or not (OUT / "summary.json").exists():
        raise AssertionError("Complete and review the diagnostic report before sealing")
    write_new(OUT / "result_manifest.json", {"status": "diagnostics_and_speedup_complete",
        "protocol_sha256": sha(OUT / "protocol.json"), "artifact_sha256": inventory(),
        "formal_promotion": False, "new_predictive_candidates": 0})
    return {"status": "sealed", "manifest_sha256": sha(OUT / "result_manifest.json")}


def verify():
    checked_protocol()
    manifest = read(OUT / "result_manifest.json")
    if manifest["protocol_sha256"] != sha(OUT / "protocol.json") or manifest["artifact_sha256"] != inventory():
        raise AssertionError("Sealed diagnostic inventory changed")
    verify_map(manifest["artifact_sha256"])
    from experiments.finalize_r7 import verify as verify_r7
    previous = verify_r7()
    if previous != read(OUT / "protocol.json")["previous_r7_verification"]:
        raise AssertionError("Previous frozen evidence changed")
    return {"status": "passed", "read_only": True, "previous_r7_r6_r5_r4": "passed",
            "files_hashed": len(manifest["artifact_sha256"]), "formal_release": "ensemble4_r4",
            "new_predictive_candidates": 0, "manifest_sha256": sha(OUT / "result_manifest.json")}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("prepare", "run", "seal", "verify"))
    action = parser.parse_args().action
    print(json.dumps(globals()[action](), ensure_ascii=False, indent=2, allow_nan=False))
