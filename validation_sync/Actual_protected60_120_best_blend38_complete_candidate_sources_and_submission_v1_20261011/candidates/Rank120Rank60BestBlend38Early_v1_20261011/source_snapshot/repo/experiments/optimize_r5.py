"""Four predeclared refinements; chronological retrospective model selection.

Do not edit this source after freeze, add candidates after development, inspect
confirmation results to select a substitute, or overwrite the existing release.
"""
from __future__ import annotations

import os
for _thread_var in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "POLARS_MAX_THREADS"):
    os.environ[_thread_var] = "4"

import argparse
import gc
import hashlib
import json
from pathlib import Path
import sys
import time

import numpy as np
import polars as pl

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from src.scoring import Panel
from experiments.cached_recheck import make_prediction
from experiments.revalidate_fold_local import score_official, paired
from experiments.optimize_r5_models import load_year, combine_raw, CANDIDATES as MODEL_CANDIDATES
from experiments.optimize_r5_postprocess import candidate_prediction as post_prediction, CANDIDATES as POST_CANDIDATES

OUT = ROOT / "experiments/optimization_r5_20260926"
R4 = ROOT / "experiments/revalidation_20260926/validation"
DEVELOPMENT = (2020, 2021, 2022)
CONFIRMATION = (2023, 2024)
REFERENCES = ("baseline", "ensemble4")
GATES = {
    "development": {"mean_score_delta_min": .001, "worst_year_score_delta_min": -.005, "mean_ic_delta_min": -.002},
    "confirmation": {"mean_score_delta_min": .0005, "worst_year_score_delta_min": -.003, "mean_ic_delta_min": -.002},
    "bootstrap": {"block_days": 20, "draws": 20000, "seed": 2026, "positive_share_min": .80},
    "execution": {"start": 20230101, "end": 20241231, "round_trip": .003,
                  "net_compound_return_delta_min": -.01, "max_drawdown_delta_min": -.02,
                  "other_costs_disclosure_only": [0., .001, .005]},
}


def sha(path):
    h = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for block in iter(lambda: stream.read(4 * 1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def read(path):
    return json.loads(Path(path).read_text(encoding="utf-8-sig"))


def write_new(path, data):
    with Path(path).open("x", encoding="utf-8") as stream:
        json.dump(data, stream, ensure_ascii=False, indent=2, allow_nan=False)


def log(text):
    print(f"[{time.strftime('%H:%M:%S')}] {text}", flush=True)


def candidates():
    result = {k: {"family": "model", "config": v, "model_count": 2 if k == "xgb_two_mean" else 3}
              for k, v in MODEL_CANDIDATES.items()}
    result.update({k: {"family": "postprocess", "config": v, "model_count": 4} for k, v in POST_CANDIDATES.items()})
    assert len(result) == 4
    return json.loads(json.dumps(result))


def freeze():
    OUT.mkdir(parents=True, exist_ok=True)
    if (OUT / "protocol.json").exists():
        raise FileExistsError("Protocol already frozen")
    from verify_current_release import verify as verify_release
    assert verify_release()["release_id"] == "ensemble4_r4"
    source_files = [Path(__file__), ROOT / "experiments/optimize_r5_models.py",
                    ROOT / "experiments/optimize_r5_postprocess.py", ROOT / "experiments/audit_r5_candidate.py",
                    ROOT / "experiments/revalidate_fold_local.py", ROOT / "experiments/cached_recheck.py",
                    ROOT / "experiments/final_sweep.py", ROOT / "experiments/official_seed_development.py",
                    ROOT / "experiments/final_sweep_significance.py", ROOT / "src/scoring.py", ROOT / "evaluate.py",
                    ROOT / "experiments/backtest_causal_portfolio.py", ROOT / "data" / "raw" / "训练集.csv", ROOT / "active_release.json",
                    ROOT / "releases/ensemble4_r4/release_manifest.json", ROOT / "verify_current_release.py",
                    ROOT / "run.py", R4 / "summary.json", R4 / "protocol.json"]
    # Freeze every potential fold input without computing candidate predictions.
    old = read(R4 / "summary.json")
    for year in (*DEVELOPMENT, *CONFIRMATION):
        for name in ("baseline", "xgboost", "ensemble4"):
            source_files.extend([R4 / f"predictions_{name}_{year}.parquet", R4 / f"daily_{name}_{year}.csv"])
        source_files.append(R4 / f"result_{year}.json")
        source_files.append(ROOT / old["year_results"][str(year)]["cache_sources"]["two_day"]["path"])
    for name in ("model_tests.json", "postprocess_tests.json", "audit_tests.json"):
        assert read(OUT / name)["status"] == "passed", name
        source_files.append(OUT / name)
    protocol = {
        "experiment": "r5_four_fixed_refinements", "frozen_at_local": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "all_years_previously_viewed": True, "no_new_independent_holdout": True,
        "development_years": list(DEVELOPMENT), "confirmation_years": list(CONFIRMATION),
        "candidates": candidates(), "reference_names": list(REFERENCES), "gates": GATES,
        "candidate_selection": "Among candidates passing ALL development thresholds against BOTH references, highest equally weighted mean annual official score. Exact ties: fewer primary models, then lexical candidate key. Select exactly one or none.",
        "confirmation_rule": "Evaluate only the frozen development winner on 2023 and 2024 once. All confirmation, bootstrap and account gates must pass against both references; otherwise no adoption. No fallback to another candidate.",
        "fixed_postprocess": {"alpha": .9, "bonus": .3, "pooled_top_only_weight": .25},
        "training": "Reuse hash-verified, purged fold predictions; no new fitting and no future-importance pruning. Any r4 ensemble raw uses corrected fold-local pruning. Five years share identical pooled auxiliary recipe.",
        "information_time": "Signals formed after same-day close; no return label or future availability mask enters candidate construction. Current OHLCV is available.",
        "scorer": "Unmodified evaluate.py; Float64 original labels from locked r4 frame; float17 CSV; official default pandas sorting. Independent original-source check required for a winner.",
        "noise_note": "Bootstrap/HAC are descriptive and do not correct repeated historical candidate selection. Gates are frozen engineering thresholds, not a proof of statistical or trading superiority.",
        "execution_note": "All three strategies and market cold-start on first 2023 quote date, identical actual-holdings bookkeeping. Daily execution-day limits/volume are ex-post fill assumptions, not known opening conditions.",
        "prohibited": ["Adding candidates or parameter values after scores", "Selecting a second winner after confirmation", "Changing gates based on results", "Editing frozen evidence or active artifacts before a complete release audit"],
        "input_sha256": {p.relative_to(ROOT).as_posix(): sha(p) for p in dict.fromkeys(source_files)},
    }
    write_new(OUT / "protocol.json", protocol)
    log("Four candidates and all gates frozen before candidate scoring")


def verify_protocol():
    p = read(OUT / "protocol.json")
    assert p["candidates"] == candidates() and p["gates"] == GATES
    for path, digest in p["input_sha256"].items():
        if sha(ROOT / path) != digest:
            raise AssertionError(f"Frozen input changed: {path}")
    from verify_current_release import verify as verify_release
    assert verify_release()["release_id"] == "ensemble4_r4"
    return p


def predict(frame, raws, key):
    if key in MODEL_CANDIDATES:
        raw = combine_raw(frame, raws, key)
        panel = Panel.from_frame(frame.with_columns(pl.Series("pred_raw", raw)))
        return make_prediction(panel, frame["aux_raw"].to_numpy(), "top_only", .25), raw
    panel = Panel.from_frame(frame)
    raw = frame["pred_raw"].to_numpy()
    return post_prediction(panel, raw, frame["aux_raw"].to_numpy(), key), raw


def invariants(frame, raws, key, pred):
    changed = frame.with_columns(pl.lit(987654.).alias("y_ret_1d"), pl.lit(False).alias("future_available"))
    altered, _ = predict(changed, raws, key)
    assert np.array_equal(pred, altered), (key, "label invariance")
    n = frame["ts_code"].n_unique() * 50
    prefix, _ = predict(frame.head(n), {name: values[:n] for name, values in raws.items()}, key)
    assert np.array_equal(pred[:n], prefix), (key, "prefix invariance")
    assert np.isfinite(pred).all()
    assert np.all(pred[~frame["price_valid"].to_numpy()] < -1)
    return {"label_perturbation_exact": True, "future_availability_ignored": True,
            "50_day_prefix_exact": True, "invalid_price_low_scores": True, "all_predictions_finite": True}


def score_fold(year, keys):
    path = OUT / f"fold_{year}.json"
    if path.exists():
        record = read(path)
        assert record["candidate_keys"] == keys
        for name, digest in record["artifact_sha256"].items():
            assert sha(OUT / name) == digest
        log(f"Preserved completed {year} fold")
        return record
    frame, raws, provenance = load_year(year)
    expected = read(R4 / "summary.json")["metrics"][str(year)]
    result = {"year": year, "candidate_keys": keys, "provenance": provenance, "references": {}, "candidates": {}}
    daily_references = {}
    # Real evaluator anchors before any new candidate in this fold.
    for name in REFERENCES:
        reference = pl.read_parquet(R4 / f"predictions_{name}_{year}.parquet").sort("trade_date", "ts_code")
        assert frame.select("trade_date", "ts_code").equals(reference.select("trade_date", "ts_code"))
        metrics, daily = score_official(frame, reference["pred"].to_numpy())
        assert all(abs(value - expected[name][metric]) <= 1e-12 for metric, value in metrics.items())
        result["references"][name] = metrics
        daily_references[name] = daily
        daily.write_csv(OUT / f"daily_{name}_{year}.csv")
    for key in keys:
        pred, raw = predict(frame, raws, key)
        tests = invariants(frame, raws, key, pred)
        metrics, daily = score_official(frame, pred)
        daily.write_csv(OUT / f"daily_{key}_{year}.csv")
        frame.with_columns(pl.Series("pred", pred), pl.Series("pred_raw", raw)).write_parquet(OUT / f"predictions_{key}_{year}.parquet", compression="zstd")
        result["candidates"][key] = {"metrics": metrics, "tests": tests,
                                    "paired": {name: paired(daily, reference) for name, reference in daily_references.items()}}
        log(f"{year} {key}: {metrics['final_score']:.9f}; r4 delta {metrics['final_score']-result['references']['ensemble4']['final_score']:+.9f}")
    result["artifact_sha256"] = {p.name: sha(p) for p in OUT.glob(f"*_{year}.*") if p != path}
    write_new(path, result)
    del frame, raws
    gc.collect()
    return result


def gate(results, key, stage):
    thresholds = GATES[stage]
    comparisons = {}
    for reference in REFERENCES:
        score_deltas = [r["candidates"][key]["metrics"]["final_score"]-r["references"][reference]["final_score"] for r in results]
        ic_deltas = [r["candidates"][key]["metrics"]["ic_mean"]-r["references"][reference]["ic_mean"] for r in results]
        comparisons[reference] = {
            "score_deltas": dict(zip([str(r["year"]) for r in results], score_deltas)),
            "mean_score_delta": float(np.mean(score_deltas)), "worst_year_score_delta": min(score_deltas),
            "mean_ic_delta": float(np.mean(ic_deltas)),
            "passed": bool(np.mean(score_deltas) >= thresholds["mean_score_delta_min"]
                           and min(score_deltas) >= thresholds["worst_year_score_delta_min"]
                           and np.mean(ic_deltas) >= thresholds["mean_ic_delta_min"]),
        }
    return {"comparisons": comparisons, "passed": all(c["passed"] for c in comparisons.values()),
            "mean_official_score": float(np.mean([r["candidates"][key]["metrics"]["final_score"] for r in results]))}


def develop():
    verify_protocol()
    if (OUT / "development.json").exists():
        raise FileExistsError("Development choice already frozen")
    options = candidates()
    results = [score_fold(year, list(options)) for year in DEVELOPMENT]
    scores = {key: gate(results, key, "development") for key in options}
    eligible = [key for key, score in scores.items() if score["passed"]]
    winner = min(eligible, key=lambda k: (-scores[k]["mean_official_score"], options[k]["model_count"], k)) if eligible else None
    verify_protocol()
    record = {"protocol_sha256": sha(OUT / "protocol.json"), "selected_before_confirmation": True,
              "candidate_results": scores, "winner": winner, "no_fallback_after_confirmation": True,
              "fold_sha256": {f"fold_{y}.json": sha(OUT / f"fold_{y}.json") for y in DEVELOPMENT}}
    write_new(OUT / "development.json", record)
    write_summary()
    log(f"Development winner: {winner!r}")


def validated_development():
    dev = read(OUT / "development.json")
    assert dev["protocol_sha256"] == sha(OUT / "protocol.json")
    assert dev["selected_before_confirmation"] and dev["no_fallback_after_confirmation"]
    assert set(dev["fold_sha256"]) == {f"fold_{y}.json" for y in DEVELOPMENT}
    options = candidates()
    folds = []
    for year in DEVELOPMENT:
        path = OUT / f"fold_{year}.json"
        assert sha(path) == dev["fold_sha256"][path.name]
        fold = read(path)
        assert fold["year"] == year and fold["candidate_keys"] == list(options)
        assert set(fold["candidates"]) == set(options)
        for artifact, digest in fold["artifact_sha256"].items():
            assert sha(OUT / artifact) == digest
        folds.append(fold)
    scores = {key: gate(folds, key, "development") for key in options}
    assert scores == dev["candidate_results"]
    eligible = [key for key, score in scores.items() if score["passed"]]
    winner = min(eligible, key=lambda k: (-scores[k]["mean_official_score"], options[k]["model_count"], k)) if eligible else None
    assert winner == dev["winner"], "Development choice does not follow the frozen rule"
    return dev


def confirm():
    verify_protocol()
    dev = validated_development()
    if dev["winner"] is None:
        raise ValueError("No eligible development candidate; confirmation is prohibited")
    if (OUT / "confirmation.json").exists():
        raise FileExistsError("Confirmation already recorded")
    winner = dev["winner"]
    results = [score_fold(y, [winner]) for y in CONFIRMATION]
    from experiments.audit_r5_candidate import paired_block_bootstrap
    def daily(key):
        return {year: pl.read_csv(OUT / f"daily_{key}_{year}.csv", null_values=["NaN"]) for year in CONFIRMATION}
    candidate_daily = daily(winner)
    bootstrap = {name: paired_block_bootstrap(candidate_daily, daily(name), block_days=20, draws=20000, seed=2026) for name in REFERENCES}
    aggregate = gate(results, winner, "confirmation")
    passed = aggregate["passed"] and all(r["bootstrap_share_positive"] >= .80 for r in bootstrap.values())
    record = {"winner": winner, "development_sha256": sha(OUT / "development.json"),
              "aggregate": aggregate, "bootstrap": bootstrap, "official_and_noise_gate_passed": bool(passed),
              "execution_and_independent_audit_required": True,
              "fold_sha256": {f"fold_{y}.json": sha(OUT / f"fold_{y}.json") for y in CONFIRMATION}}
    verify_protocol()
    write_new(OUT / "confirmation.json", record)
    write_summary()
    log(f"Confirmation official/noise gate: {passed}; independent and account audit remain")


def write_summary():
    dev = read(OUT / "development.json")
    status = "no_development_candidate_passed" if dev["winner"] is None else "winner_waiting_for_confirmation"
    conf = read(OUT / "confirmation.json") if (OUT / "confirmation.json").exists() else None
    if conf:
        status = "confirmation_passed_audit_pending" if conf["official_and_noise_gate_passed"] else "confirmation_failed_no_adoption"
    lines = ["# r5固定候选优化结果", "", f"状态：{status}。", "", "所有年份均已查看。本轮固定4个候选；2020—2022只选择一个候选，2023—2024只确认该候选，失败不替换、不追加参数。", "", "## 开发结果", "", "| 候选 | 2020 | 2021 | 2022 | 对r4平均增量 | 对pooled平均增量 | 开发门槛 |", "|---|---:|---:|---:|---:|---:|---|"]
    folds = {y: read(OUT / f"fold_{y}.json") for y in DEVELOPMENT}
    for key, result in dev["candidate_results"].items():
        values = [folds[y]["candidates"][key]["metrics"]["final_score"] for y in DEVELOPMENT]
        lines.append(f"| {key} | {values[0]:.9f} | {values[1]:.9f} | {values[2]:.9f} | {result['comparisons']['ensemble4']['mean_score_delta']:+.9f} | {result['comparisons']['baseline']['mean_score_delta']:+.9f} | {'通过' if result['passed'] else '未通过'} |")
    lines += ["", f"开发阶段唯一候选：{dev['winner'] or '无'}。", "", "开发门槛：对r4及pooled均分增量至少0.001，最差单年不低于−0.005，平均IC不低于−0.002。具体每项门槛见protocol.json；这是评分前冻结的工程阈值，不代表显著性。"]
    if conf:
        lines += ["", "## 一次确认", "", json.dumps({"winner": dev["winner"], "passed": conf["official_and_noise_gate_passed"], "aggregate": conf["aggregate"]}, ensure_ascii=False, indent=2)]
    lines += ["", "## 证据与使用限制", "", "- protocol.json：候选公式、时间划分、门槛及全部输入哈希。", "- development.json：只用开发年份固定的选择结果。", "- fold_年份.json、daily_候选_年份.csv与predictions_候选_年份.parquet：官方分项、每日证据、预测及信息隔离检查。", "- model_tests.json、postprocess_tests.json、audit_tests.json：独立行为测试。", "- 新候选构建不读取标签或未来可用性；原始评分标签保持Float64，直接调用主办方evaluate.py。", "- HAC与bootstrap均未校正累计历史筛选偏差；无正式测试标签，不能推断隐藏测试成绩。", "- 当前正式文件保持r4；只有完整确认、执行及独立审计通过后，才考虑另存新版并更新入口。"]
    (OUT / "优化结果.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("stage", choices=("freeze", "develop", "confirm", "summarize"))
    args = parser.parse_args()
    {"freeze": freeze, "develop": develop, "confirm": confirm, "summarize": write_summary}[args.stage]()
