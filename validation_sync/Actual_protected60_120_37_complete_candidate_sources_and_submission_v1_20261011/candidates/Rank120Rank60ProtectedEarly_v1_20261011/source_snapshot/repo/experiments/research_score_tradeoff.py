"""Verify the official score's marginal turnover penalty; no model fitting.

This is an analytical/synthetic research diagnostic, not a trading rule or an
empirical improvement claim. The frozen official evaluator is not modified.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import sys

import numpy as np
import pandas as pd
from loguru import logger

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from evaluate import evaluate

OUT = ROOT / "experiments/research_r6_20260926"


def marginal_jaccard(k: int, replaced: int) -> float:
    if not 0 <= replaced < k:
        raise ValueError("Require 0 <= replaced < portfolio size")
    return 2 * k / ((k + replaced) * (k + replaced + 1))


def one_transition_edge(k: int, replaced: int, return_days: int = 242,
                        turnover_days: int = 241) -> float:
    """Stock return gap, ignoring IC and every other affected transition."""
    return k * return_days / (252 * turnover_days) * marginal_jaccard(k, replaced)


def selected_set(k: int, replaced: int) -> set[int]:
    return set(range(replaced, k)) | set(range(k, k + replaced))


def synthetic_official_check():
    folder = OUT / "score_tradeoff_toy"
    folder.mkdir(parents=True, exist_ok=True)
    days, k, replaced, edge = 21, 40, 2, .005
    n = k * 10
    dates = pd.bdate_range("2020-01-02", periods=days).strftime("%Y%m%d").astype(int)
    codes = [f"toy_{i:04d}" for i in range(n)]
    frame = pd.DataFrame({"trade_date": np.repeat(dates, n), "ts_code": codes * days})
    labels = np.tile(np.linspace(-.02, .02, n), days).reshape(days, n)
    # The extra substitution removes stock m and adds stock K+m.
    labels[-1, replaced] = 0
    labels[-1, k + replaced] = edge
    frame.assign(y_ret_1d=labels.reshape(-1)).to_csv(folder / "测试集_Y.csv", index=False,
                                                 float_format="%.17g")
    frame.assign(flag_limit_up=0).to_csv(folder / "测试集_X.csv", index=False)
    scores = {}
    for name, m in (("baseline", replaced), ("candidate", replaced + 1)):
        pred = np.empty((days, n))
        for day in range(days):
            selected = selected_set(k, m if day == days - 1 else 0)
            pred[day] = np.arange(n) / n + 2 * np.isin(np.arange(n), list(selected))
        path = folder / f"{name}.csv"
        frame.assign(pred=pred.reshape(-1)).to_csv(path, index=False, float_format="%.17g")
        scores[name] = evaluate(str(path), str(folder))
    delta = {key: scores["candidate"][key] - scores["baseline"][key]
             for key in scores["baseline"]}
    expected_excess = 252 * edge / (k * days)
    expected_turnover = marginal_jaccard(k, replaced) / (days - 1)
    residual = delta["final_score"] - .4 * delta["ic_mean"]
    expected_residual = .3 * (expected_excess - expected_turnover)
    for actual, expected in ((delta["annual_excess"], expected_excess),
                             (delta["mean_turnover"], expected_turnover),
                             (residual, expected_residual)):
        assert abs(actual - expected) < 1e-12, (actual, expected)
    return {"status": "passed", "days": days, "top_k": k,
            "already_replaced": replaced, "stock_return_gap": edge,
            "score_delta_without_ic": residual,
            "expected_score_delta_without_ic": expected_residual,
            "metric_delta": delta, "metrics": scores,
            "construction": "Only final-day Top membership differs by one stock; all labels finite, no limit flags or ties."}


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    output = OUT / "score_tradeoff.json"
    if output.exists():
        raise FileExistsError(output)
    logger.disable("evaluate")
    cases = 0
    for k in (10, 20, 100, 400, 465):
        previous = selected_set(k, 0)
        for m in (0, 1, k // 2, k - 1):
            current, changed = selected_set(k, m), selected_set(k, m + 1)
            direct = len(previous & current) / len(previous | current)
            direct -= len(previous & changed) / len(previous | changed)
            assert abs(direct - marginal_jaccard(k, m)) < 1e-14
            cases += 1
    result = {
        "purpose": "Analytical diagnostic only; no alpha model, parameter search, or release change",
        "formula": "J(m)=2m/(K+m); delta_J=2K/((K+m)*(K+m+1))",
        "edge_threshold": "e > K*N_return/(252*N_turnover)*delta_J, ignoring IC and all other transitions",
        "set_identity_cases_passed": cases,
        "reference_examples": [
            {"top_k": k, "already_replaced": m, "return_days": 242,
             "turnover_days": 241,
             "one_transition_stock_edge_bp": 1e4 * one_transition_edge(k, m)}
            for k, m in ((400, 0), (400, 8), (465, 0), (465, 9))
        ],
        "official_evaluator_check": synthetic_official_check(),
        "limitations": [
            "The threshold is a difference in per-stock returns, not portfolio return or a real transaction fee.",
            "Holding a substitution longer changes its cumulative expected advantage; later exits may add turnover penalties.",
            "IC changes, different eligible return/turnover universes, varying Top size and ranking ties require exact separate treatment.",
            "No observed future return may enter the prediction or replacement rule.",
            "The fixed 0.3 rank retention bonus has no direct conversion to expected stock returns.",
        ],
        "input_sha256": {p.relative_to(ROOT).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
                         for p in (Path(__file__), ROOT / "evaluate.py")},
    }
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": "passed", "identity_cases": cases,
                      "official_check": result["official_evaluator_check"]["status"],
                      "reference_examples": result["reference_examples"]}, indent=2))


if __name__ == "__main__":
    main()
