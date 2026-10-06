"""Attribute historical Top ranking changes to fixed ensemble4 processing stages.

This is diagnosis, not model/parameter selection. Corrected validation caches
are the primary source; frozen legacy caches are available for comparison.
Official metrics call the unmodified evaluate.py through a float17 CSV round
trip. Deciles, event counts and membership attribution use a separately named
stable sort and must not be confused with the official tie ordering.
"""
from __future__ import annotations

import os

for _name in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "POLARS_MAX_THREADS"):
    os.environ[_name] = str(min(int(os.environ.get(_name, "8")), 8))

import argparse
import gc
import hashlib
import json
from pathlib import Path
import sys
import tempfile
import time

import numpy as np
import polars as pl

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from evaluate import evaluate  # noqa: E402
from experiments.cached_recheck import make_prediction  # noqa: E402
from experiments.final_sweep import blend_top_only  # noqa: E402
from experiments.official_seed_development import _same_csv_daily, original_labels  # noqa: E402
from src.scoring import Panel, add_top_persistence, make_scores, restore_lower_ranks  # noqa: E402

OUT = ROOT / "experiments/revalidation_20260926/top_diagnosis"
CACHE = ROOT / "experiments/revalidation_20260926/validation"
KEYS = ["ts_code", "trade_date"]
STAGES = ("raw_daily_rank", "ema", "ema_top_persistence", "protected_current_ranks", "pooled25")
NAMES = {
    "raw_daily_rank": "原始当日排名", "ema": "EMA平滑",
    "ema_top_persistence": "EMA＋Top留存", "protected_current_ranks": "保留名单并恢复当前排序",
    "pooled25": "保护区内25% pooled融合",
}
CONFIG = {"alpha": 0.9, "bonus": 0.3, "top_current_weight": 1.0, "pooled_weight": 0.25}


def file_hash(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(2 ** 20), b""):
            h.update(chunk)
    return h.hexdigest()


def mean(values) -> float | None:
    a = np.asarray(values, dtype=float)
    a = a[np.isfinite(a)]
    return float(a.mean()) if len(a) else None


def hac(values, lags: int = 5) -> dict:
    """Fixed-lag Bartlett HAC, descriptive only on repeatedly viewed history."""
    a = np.asarray(values, dtype=float)
    a = a[np.isfinite(a)]
    if len(a) < 2:
        return {"n": int(len(a)), "mean": mean(a), "lags": lags, "se": None, "ci95": None}
    centered = a - a.mean()
    variance = float(centered @ centered / len(a))
    for lag in range(1, min(lags, len(a) - 1) + 1):
        variance += 2 * (1 - lag / (lags + 1)) * float(centered[lag:] @ centered[:-lag] / len(a))
    se = float(np.sqrt(max(variance, 0) / len(a)))
    return {"n": int(len(a)), "mean": float(a.mean()), "lags": lags, "se": se,
            "ci95": [float(a.mean() - 1.96 * se), float(a.mean() + 1.96 * se)]}


def construct_stages(panel: Panel, raw: np.ndarray, auxiliary: np.ndarray) -> dict[str, np.ndarray]:
    daily = make_scores(panel, raw, 0.0)
    ema = make_scores(panel, raw, CONFIG["alpha"])
    stable = add_top_persistence(panel, ema, CONFIG["bonus"])
    restored = restore_lower_ranks(panel, stable, raw, CONFIG["top_current_weight"])
    pooled = blend_top_only(panel, stable, raw, auxiliary, CONFIG["pooled_weight"])
    return dict(zip(STAGES, (daily, ema, stable, restored, pooled), strict=True))


def top_mask(pred: np.ndarray, eligible: np.ndarray) -> np.ndarray:
    mask = np.zeros(len(pred), dtype=bool)
    indices = np.flatnonzero(eligible)
    if len(indices) >= 100:
        order = np.argsort(-pred[indices], kind="stable")
        mask[indices[order[:len(indices) // 10]]] = True
    return mask


def official_metrics(panel: Panel, prediction: np.ndarray) -> tuple[dict, pl.DataFrame]:
    """Use actual unmodified evaluator; verify daily reconstruction separately."""
    if not np.isfinite(prediction).all():
        raise ValueError("Nonfinite prediction")
    with tempfile.TemporaryDirectory(prefix="top-stage-official-") as tmp:
        folder = Path(tmp)
        panel.frame.select(KEYS).with_columns(pl.Series("pred", prediction)).write_csv(
            folder / "submission.csv", float_precision=17)
        panel.frame.select(KEYS + ["y_ret_1d"]).write_csv(folder / "测试集_Y.csv", float_precision=17)
        panel.frame.select(KEYS + ["flag_limit_up"]).write_csv(folder / "测试集_X.csv")
        metrics = {key: float(value) for key, value in
                   evaluate(str(folder / "submission.csv"), str(folder)).items()}
        rebuilt, daily = _same_csv_daily(folder)
    for key, value in metrics.items():
        if not np.isfinite(value) or abs(value - rebuilt[key]) > 1e-12:
            raise AssertionError((key, value, rebuilt[key]))
    return metrics, daily


def load_inputs(year: int, source: str) -> tuple[Panel, np.ndarray, np.ndarray, dict]:
    if source == "corrected":
        path = CACHE / f"predictions_ensemble4_{year}.parquet"
        frame = pl.read_parquet(path, columns=KEYS + ["pred_raw", "pred", "aux_raw", "flag_limit_up",
                                                      "price_valid", "y_ret_1d"]).sort("trade_date", "ts_code")
        provenance = {"source": source, "path": str(path.relative_to(ROOT)), "sha256": file_hash(path)}
    else:
        base = ROOT / f"validation/fold_{year}.parquet"
        raw_path = ROOT / f"experiments/final_sweep_eval/W3e_lgb_xgb_twoday_pruned_{year}.parquet"
        aux_path = ROOT / f"experiments/return_pooled_eval/return_pooled1_99_{year}.parquet"
        frame = pl.read_parquet(base, columns=KEYS + ["flag_limit_up", "price_valid"])
        for path, rename in ((raw_path, "pred_raw"), (aux_path, "aux_raw")):
            values = pl.read_parquet(path, columns=KEYS + ["pred_raw"]).rename({"pred_raw": rename})
            if len(values) != len(frame):
                raise AssertionError("Prediction cache length mismatch")
            frame = frame.join(values, on=KEYS, how="left", validate="1:1")
        frame = frame.join(original_labels(year), on=KEYS, how="left", validate="1:1").sort("trade_date", "ts_code")
        provenance = {"source": source, "files": {str(p.relative_to(ROOT)): file_hash(p)
                                                    for p in (base, raw_path, aux_path)}}
    if frame.select(pl.struct(KEYS).n_unique()).item() != len(frame):
        raise AssertionError("Duplicate panel keys")
    panel = Panel.from_frame(frame)
    raw, auxiliary = (panel.frame[name].to_numpy().astype(np.float64) for name in ("pred_raw", "aux_raw"))
    for values in (raw, auxiliary):
        if not np.isfinite(values.reshape(panel.valid_price.shape)[panel.valid_price]).all():
            raise AssertionError("Nonfinite valid-price raw prediction")
    return panel, raw, auxiliary, provenance


def diagnostics(panel: Panel, predictions: np.ndarray, daily_raw: np.ndarray) -> tuple[dict, pl.DataFrame, np.ndarray, np.ndarray]:
    shape = panel.valid_price.shape
    p = np.asarray(predictions).reshape(shape)
    raw = np.asarray(daily_raw).reshape(shape)
    returns = np.zeros(shape, dtype=bool)
    turnover = np.zeros(shape, dtype=bool)
    raw_turnover = np.zeros(shape, dtype=bool)
    raw_returns = np.zeros(shape, dtype=bool)
    for i in range(len(panel.dates)):
        tradeable = panel.up[i] == 0
        eligible = tradeable & np.isfinite(panel.y[i])
        turnover[i] = top_mask(p[i], tradeable)
        returns[i] = top_mask(p[i], eligible)
        raw_turnover[i] = top_mask(raw[i], tradeable)
        raw_returns[i] = top_mask(raw[i], eligible)
    last_raw_top = np.full(panel.rows_per_day, -1, dtype=int)
    last_resume = np.full(panel.rows_per_day, -1, dtype=int)
    tenure = np.zeros(panel.rows_per_day, dtype=int)
    records = []
    for i, date in enumerate(panel.dates):
        y, pred, valid = panel.y[i], p[i], panel.valid_price[i]
        last_raw_top[raw_turnover[i]] = i
        resumed = valid & ~panel.valid_price[i - 1] if i else np.zeros(panel.rows_per_day, dtype=bool)
        last_resume[resumed] = i
        recent_resume = (last_resume >= 0) & (i - last_resume < 5)
        released_up = (panel.up[i - 1] == 1) & (panel.up[i] == 0) if i else np.zeros_like(valid)
        tenure = np.where(turnover[i], tenure + 1, 0)
        ret_top, turn_top = returns[i], turnover[i]
        nret, nturn = int(ret_top.sum()), int(turn_top.sum())
        record = {"trade_date": int(date), "return_top_n": nret, "turnover_top_n": nturn}
        eligible_indices = np.flatnonzero((panel.up[i] == 0) & np.isfinite(y))
        qreturns = [np.nan] * 10
        if len(eligible_indices) >= 100:
            ordered = eligible_indices[np.argsort(-pred[eligible_indices], kind="stable")]
            width = len(ordered) // 10
            descending = [ordered[j * width:(j + 1) * width] for j in range(9)] + [ordered[9 * width:]]
            qreturns = [float(y[idx].mean()) for idx in descending[::-1]]
        record.update({f"q{j+1}_return": value for j, value in enumerate(qreturns)})
        record["top_minus_q9"] = qreturns[-1] - qreturns[-2]
        record["return_top_mean_raw_percentile"] = mean(raw[i, ret_top])
        record["return_top_not_current_raw_top_share"] = float(np.count_nonzero(ret_top & ~raw_returns[i]) / nret) if nret else None
        record["return_top_raw_below_80pct_share"] = float(np.count_nonzero(ret_top & (raw[i] <= .8)) / nret) if nret else None
        record["return_top_raw_below_50pct_share"] = float(np.count_nonzero(ret_top & (raw[i] <= .5)) / nret) if nret else None
        record["return_top_resumed_today_share"] = float(np.count_nonzero(ret_top & resumed) / nret) if nret else None
        record["return_top_resumed_last5_share"] = float(np.count_nonzero(ret_top & recent_resume) / nret) if nret else None
        record["return_top_previous_day_limit_up_share"] = float(np.count_nonzero(ret_top & released_up) / nret) if nret else None
        record["return_top_resume_mean_y"] = mean(y[ret_top & resumed])
        record["return_top_limit_release_mean_y"] = mean(y[ret_top & released_up])
        record["turnover_top_label_missing_share"] = float(np.count_nonzero(turn_top & ~np.isfinite(y)) / nturn) if nturn else None
        record["turnover_top_missing_price_share"] = float(np.count_nonzero(turn_top & ~valid) / nturn) if nturn else None
        record["top_definition_symmetric_difference"] = int(np.count_nonzero(turn_top ^ ret_top))
        record["turnover_top_mean_consecutive_tenure"] = mean(tenure[turn_top])
        known_age = turn_top & (last_raw_top >= 0)
        record["turnover_top_mean_days_since_raw_top_when_seen"] = mean(i - last_raw_top[known_age])
        record["turnover_top_never_raw_top_share"] = float(np.count_nonzero(turn_top & (last_raw_top < 0)) / nturn) if nturn else None
        for age in (5, 20):
            record[f"turnover_top_not_raw_top_last{age}_share"] = float(np.count_nonzero(
                turn_top & ((last_raw_top < 0) | (i - last_raw_top >= age))) / nturn) if nturn and i >= age - 1 else None
        if i and turnover[i - 1].any():
            previous = turnover[i - 1]
            record["prior_turnover_top_now_limit_up_share"] = float(np.count_nonzero(previous & (panel.up[i] == 1)) / previous.sum())
            record["prior_turnover_top_now_invalid_share"] = float(np.count_nonzero(previous & ~valid) / previous.sum())
            record["stable_jaccard_turnover"] = float(1 - np.count_nonzero(previous & turn_top) / np.count_nonzero(previous | turn_top))
        else:
            record["prior_turnover_top_now_limit_up_share"] = None
            record["prior_turnover_top_now_invalid_share"] = None
            record["stable_jaccard_turnover"] = None
        records.append(record)
    # Resumption cohorts may be absent for over 100 days; infer from the entire
    # small daily table so a later observed return is not cast into Null dtype.
    daily = pl.DataFrame(records, infer_schema_length=None)
    means = {name: mean(daily[name].to_numpy()) for name in daily.columns if name != "trade_date"}
    means["top_minus_q9_hac"] = hac(daily["top_minus_q9"].to_numpy())
    means["decile_mean_daily_returns"] = [means[f"q{j}_return"] for j in range(1, 11)]
    means["top_minus_q9_annualized"] = means["top_minus_q9"] * 252
    means["top_definition_identical_days"] = int(sum(r["top_definition_symmetric_difference"] == 0 for r in records))
    means["days"] = len(records)
    return means, daily, returns, turnover


def transition(panel: Panel, before: tuple, after: tuple, name: str) -> tuple[dict, pl.DataFrame]:
    before_return, before_turnover = before
    after_return, after_turnover = after
    records = []
    for i, date in enumerate(panel.dates):
        entrants = after_return[i] & ~before_return[i]
        exits = before_return[i] & ~after_return[i]
        count = int(after_return[i].sum())
        if count != before_return[i].sum():
            raise AssertionError("Same-day return universe unexpectedly changed")
        swapped = (panel.y[i, entrants].sum() - panel.y[i, exits].sum()) / count if count else np.nan
        records.append({"trade_date": int(date), "return_top_changed_members": int(entrants.sum()),
                        "turnover_top_changed_members": int(np.count_nonzero(after_turnover[i] & ~before_turnover[i])),
                        "entrant_mean_return": mean(panel.y[i, entrants]),
                        "exit_mean_return": mean(panel.y[i, exits]),
                        "membership_daily_top_return_effect": float(swapped),
                        "return_top_changed_fraction": float(entrants.sum() / count) if count else None})
    daily = pl.DataFrame(records, infer_schema_length=None)
    summary = {name: mean(daily[name].to_numpy()) for name in daily.columns if name != "trade_date"}
    summary.update({"transition": name,
                    "return_top_unchanged_days": int(sum(r["return_top_changed_members"] == 0 for r in records)),
                    "turnover_top_unchanged_days": int(sum(r["turnover_top_changed_members"] == 0 for r in records)),
                    "membership_effect_hac": hac(daily["membership_daily_top_return_effect"].to_numpy()),
                    "membership_annual_top_return_effect": summary["membership_daily_top_return_effect"] * 252})
    return summary, daily


def self_test() -> dict:
    rng = np.random.default_rng(260926)
    days, stocks = 9, 140
    valid = np.ones((days, stocks), dtype=bool)
    valid[1, 3] = False
    valid[4:6, 4] = False
    up = np.zeros_like(valid, dtype=np.int8)
    up[2, 5:8] = 1
    raw = rng.normal(size=(days, stocks))
    auxiliary = rng.normal(size=(days, stocks))
    labels = rng.normal(0, .01, size=(days, stocks))
    labels[:, 12] = np.nan
    frame = pl.DataFrame({"ts_code": [f"S{s:03d}" for _ in range(days) for s in range(stocks)],
                          "trade_date": np.repeat(np.arange(20220101, 20220101 + days), stocks),
                          "flag_limit_up": up.ravel(), "price_valid": valid.ravel(),
                          "y_ret_1d": labels.ravel(), "pred_raw": raw.ravel()})
    panel = Panel.from_frame(frame)
    stages = construct_stages(panel, raw.ravel(), auxiliary.ravel())
    assert np.array_equal(stages["pooled25"], make_prediction(panel, auxiliary.ravel(), "top_only", .25))
    changed = Panel.from_frame(frame.with_columns(pl.Series("y_ret_1d", rng.normal(size=days * stocks))))
    perturbed = construct_stages(changed, raw.ravel(), auxiliary.ravel())
    prefix = Panel.from_frame(frame.head(stocks * 6))
    prefix_values = construct_stages(prefix, raw[:6].ravel(), auxiliary[:6].ravel())
    masks = {}
    for name, prediction in stages.items():
        assert np.array_equal(prediction, perturbed[name]), name
        assert np.array_equal(prediction[:stocks * 6], prefix_values[name]), name
        diag, _, ret, turn = diagnostics(panel, prediction, stages["raw_daily_rank"])
        assert diag["days"] == days
        masks[name] = (ret, turn)
    assert np.array_equal(masks[STAGES[2]][1], masks[STAGES[3]][1])
    assert np.array_equal(masks[STAGES[3]][1], masks[STAGES[4]][1])
    resumed = stages["ema"].reshape(valid.shape)
    assert resumed[1, 3] == -10 and resumed[2, 3] == stages["raw_daily_rank"].reshape(valid.shape)[2, 3]
    first = masks[STAGES[0]][0]
    last = masks[STAGES[-1]][0]
    for i in range(days):
        entrant = last[i] & ~first[i]
        exit_ = first[i] & ~last[i]
        effect = (labels[i, entrant].sum() - labels[i, exit_].sum()) / last[i].sum()
        assert np.isclose(effect, labels[i, last[i]].mean() - labels[i, first[i]].mean())
    # Same turnover membership does not imply same return membership when a
    # missing label changes the group size before selection.
    values = np.linspace(0, 1, stocks)
    tradeable = np.ones(stocks, dtype=bool)
    eligible = tradeable.copy()
    eligible[0] = False
    swapped_values = values.copy()
    swapped_values[-14:] = values[-14:][::-1]
    assert np.array_equal(top_mask(values, tradeable), top_mask(swapped_values, tradeable))
    assert not np.array_equal(top_mask(values, eligible), top_mask(swapped_values, eligible))
    # Stable diagnostics use an explicit stock-order tie rule.
    tie_top = top_mask(np.zeros(stocks), tradeable)
    assert np.array_equal(np.flatnonzero(tie_top), np.arange(14))
    sparse = pl.DataFrame([{"event_mean_y": None}] * 101 + [{"event_mean_y": -.001}],
                          infer_schema_length=None)
    assert sparse["event_mean_y"].dtype == pl.Float64 and sparse["event_mean_y"][-1] == -.001
    return {"status": "passed", "cases": ["released_pipeline_exact_match", "label_invariance_all_stages",
            "prefix_invariance_all_stages", "protected_turnover_top_preserved", "resumption_reset",
            "membership_return_attribution_identity", "label_mask_top_definition_difference", "stable_ties",
            "late_sparse_event_schema"]}


def write_report(result: dict, destination: Path) -> None:
    lines = ["# ensemble4 Top 排序逐阶段诊断", "",
             "本次保持模型、alpha=0.9、留存奖励0.3、Top内部当前排序权重1与pooled权重25%不变，仅拆解历史结果。",
             f"数据来源：{result['source']}。主诊断应读取纠正两日标签边界后的缓存；旧缓存仅供历史对照。",
             "官方指标直接调用未改动的 evaluate.py（17位小数CSV往返）；分位与成员归因使用按股票代码稳定打破同分的独立诊断口径。", "",
             "## 固定阶段比较", "",
             "| 年份 | 阶段 | 官方Rank IC | 官方年化Top超额 | 官方换手 | 官方综合分 | 诊断Q10−Q9日均差(bp) | Top当前原始排名均值 |",
             "|---|---|---:|---:|---:|---:|---:|---:|"]
    for year, item in result["years"].items():
        for name in STAGES:
            metrics = item["stages"][name]["official"]
            d = item["stages"][name]["stable_diagnostics"]
            lines.append(f"| {year} | {NAMES[name]} | {metrics['ic_mean']:.5f} | {metrics['annual_excess']:.2%} | "
                         f"{metrics['mean_turnover']:.2%} | {metrics['final_score']:.6f} | {d['top_minus_q9'] * 10000:.3f} | "
                         f"{d['return_top_mean_raw_percentile']:.3f} |")
    lines += ["", "## 损失来自哪一步", ""]
    for year, item in result["years"].items():
        stage_items = item["stages"]
        transitions = item["transitions"]
        worst = min(transitions, key=lambda k: transitions[k]["official_delta"]["annual_excess"])
        change = transitions[worst]
        lines.append(f"- {year}：Top年化超额下降最多的步骤是 `{worst}`，变动 {change['official_delta']['annual_excess']:+.2%}；"
                     f"同期综合分变动 {change['official_delta']['final_score']:+.6f}。这是固定步骤的差异归因，不是调参结论。")
        gap_step = min(transitions, key=lambda k: transitions[k]["stable_q10_minus_q9_daily_change"])
        gap = transitions[gap_step]
        lines.append(f"  Q10−Q9下降最多出现在 `{gap_step}`：差值变动 "
                     f"{gap['stable_q10_minus_q9_daily_change'] * 10000:+.3f}bp/日，其中Q10变动 "
                     f"{gap['stable_q10_daily_change'] * 10000:+.3f}bp、Q9变动 "
                     f"{gap['stable_q9_daily_change'] * 10000:+.3f}bp。次高组改善也会扩大倒挂，不能把差值下降全部解释为最高组变坏。")
        for key, t in transitions.items():
            c = t["official_score_components_delta"]
            lines.append(f"  `{key}` 综合分变化 {t['official_delta']['final_score']:+.6f} = "
                         f"IC项 {c['ic']:+.6f} + 超额项 {c['excess']:+.6f} + 换手项 {c['turnover']:+.6f}。")
        persistence = stage_items["ema_top_persistence"]["stable_diagnostics"]
        final = stage_items["pooled25"]["stable_diagnostics"]
        lines.append(f"  留存阶段收益Top中 {persistence['return_top_not_current_raw_top_share']:.2%} 不在当日原始收益Top；"
                     f"换手Top中 {persistence['turnover_top_not_raw_top_last20_share']:.2%} 已至少20天未进当日原始换手Top"
                     "（只统计本年已观察满20天的日期，包括本年从未进入者，状态每年冷启动）。")
        lines.append(f"  最终收益Top的当日复牌占比 {final['return_top_resumed_today_share']:.3%}、近5日复牌占比 "
                     f"{final['return_top_resumed_last5_share']:.3%}、前日涨停本日解封占比 "
                     f"{final['return_top_previous_day_limit_up_share']:.3%}；换手Top缺标签占比 "
                     f"{final['turnover_top_label_missing_share']:.3%}。")
        for key in (f"{STAGES[2]}->{STAGES[3]}", f"{STAGES[3]}->{STAGES[4]}"):
            t = transitions[key]
            lines.append(f"  `{key}`：{t['turnover_top_unchanged_days']}/{item['days']}天换手Top名单不变，"
                         f"{t['return_top_unchanged_days']}/{item['days']}天收益Top名单不变；名单交换解释的"
                         f"稳定口径Top年化收益变动 {t['membership_annual_top_return_effect']:+.2%}。")
    lines += ["", "## 口径与限制", "",
              "- 收益Top：非涨停且下一日标签有限值；换手Top：仅要求非涨停。后者不读取标签可用性。标签缺失改变候选规模与截断位置，因此保护换手Top后，内部重排仍能改变收益Top。",
              "- Q10为按稳定排序取前floor(N/10)，Q9取紧随的同样数量；其余分组从高到低等宽，余数留在最低组。Q10−Q9是历史排序诊断，不是可直接交易的套利收益。",
              "- 年化超额是252乘日均值，不是复利；没有考虑开盘执行、交易成本、冲击、停牌与卖出约束。",
              "- 每年独立冷启动；持有年龄与最近原始Top年龄不延续上一年。复牌仅指上一观测日价格无效、当日有效。股票池与复权数据的时点来源仍未补全。",
              "- 2022—2024已经反复查看；HAC置信区间（固定5阶）仅作描述，不恢复独立检验资格。诊断不改变参数、正式提交、报告或active_release。",
              "- 本文成员与分位指标均为稳定排序诊断；summary.json中的official及official_delta才是官方评估器结果，边界同分差异保留披露。", "",
              "完整每日事件、分位收益、阶段间名单交换与原始评估器日序列位于本目录CSV文件。"]
    destination.write_text("\n".join(lines), encoding="utf-8")


def run(source: str, years: list[int], output: Path) -> dict:
    output.mkdir(parents=True, exist_ok=True)
    if (output / "summary.json").exists():
        raise FileExistsError("Preserve existing diagnosis evidence; choose another output directory")
    started = time.monotonic()
    tests = self_test()
    fingerprints = {str(p.relative_to(ROOT)): file_hash(p) for p in
                    (Path(__file__), ROOT / "src/scoring.py", ROOT / "evaluate.py", ROOT / "experiments/final_sweep.py")}
    result = {"status": "passed", "source": source, "fixed_config": CONFIG, "stages": list(STAGES),
              "model_or_parameter_selection": False, "tests": tests, "source_sha256": fingerprints,
              "diagnostic_tie_policy": "stable descending score, initial trade_date/ts_code order",
              "official_tie_policy": "unmodified pandas default descending sort through evaluate.py",
              "hac_lags": 5, "years": {}}
    for year in years:
        print(f"Loading {source} ensemble4 {year}", flush=True)
        panel, raw, auxiliary, provenance = load_inputs(year, source)
        stages = construct_stages(panel, raw, auxiliary)
        if source == "corrected":
            expected = panel.frame["pred"].to_numpy()
            if not np.array_equal(stages["pooled25"], expected):
                raise AssertionError(f"Final stage differs from corrected saved prediction, max error {np.max(abs(stages['pooled25']-expected))}")
        item = {"provenance": provenance, "days": int(len(panel.dates)), "rows": len(panel.frame),
                "final_stage_matches_cached_prediction": source == "corrected", "stages": {}, "transitions": {}}
        masks = {}
        for name, prediction in stages.items():
            metrics, official_daily = official_metrics(panel, prediction)
            d, daily, ret, turn = diagnostics(panel, prediction, stages["raw_daily_rank"])
            masks[name] = (ret, turn)
            item["stages"][name] = {"official": metrics, "stable_diagnostics": d,
                                     "stable_top_annual_return_minus_official": d["q10_return"] * 252 - metrics["top1_annual_ret"]}
            official_daily.write_csv(output / f"{year}_{name}_official_daily.csv")
            daily.write_csv(output / f"{year}_{name}_diagnostic_daily.csv")
            print(f"{year} {name}: official score={metrics['final_score']:.8f}, Q10-Q9={d['top_minus_q9']*10000:.3f}bp", flush=True)
        for before, after in zip(STAGES[:-1], STAGES[1:]):
            key = f"{before}->{after}"
            t, daily = transition(panel, masks[before], masks[after], key)
            t["official_delta"] = {metric: item["stages"][after]["official"][metric] - value
                                    for metric, value in item["stages"][before]["official"].items()}
            delta = t["official_delta"]
            t["official_score_components_delta"] = {"ic": .4 * delta["ic_mean"],
                "excess": .3 * delta["annual_excess"], "turnover": -.3 * delta["mean_turnover"]}
            if abs(sum(t["official_score_components_delta"].values()) - delta["final_score"]) > 1e-12:
                raise AssertionError("Score component attribution failed")
            for q in (9, 10):
                t[f"stable_q{q}_daily_change"] = (item["stages"][after]["stable_diagnostics"][f"q{q}_return"]
                    - item["stages"][before]["stable_diagnostics"][f"q{q}_return"])
            t["stable_q10_minus_q9_daily_change"] = t["stable_q10_daily_change"] - t["stable_q9_daily_change"]
            stable_change = (item["stages"][after]["stable_diagnostics"]["q10_return"]
                             - item["stages"][before]["stable_diagnostics"]["q10_return"]) * 252
            if abs(stable_change - t["membership_annual_top_return_effect"]) > 1e-12:
                raise AssertionError("Membership attribution failed to reconstruct stable Top change")
            if before in ("ema_top_persistence", "protected_current_ranks"):
                if t["turnover_top_unchanged_days"] != len(panel.dates):
                    raise AssertionError("Protected turnover Top changed")
            item["transitions"][key] = t
            daily.write_csv(output / f"{year}_{before}_to_{after}_members.csv")
        result["years"][str(year)] = item
        del panel, raw, auxiliary, stages, masks
        gc.collect()
    for path, expected in fingerprints.items():
        if file_hash(ROOT / path) != expected:
            raise AssertionError(f"Source changed during run: {path}")
    result["elapsed_seconds"] = time.monotonic() - started
    result["artifacts_sha256"] = {p.name: file_hash(p) for p in sorted(output.glob("*.csv"))}
    (output / "summary.json").write_text(json.dumps(result, indent=2, ensure_ascii=False, allow_nan=False), encoding="utf-8")
    write_report(result, output / "中文结果.md")
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", choices=("corrected", "legacy"), default="corrected")
    parser.add_argument("--years", nargs="+", type=int, default=[2022, 2023, 2024])
    parser.add_argument("--output", type=Path)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        print(json.dumps(self_test(), indent=2))
    else:
        run(args.source, args.years, args.output or (OUT if args.source == "corrected" else OUT / "legacy"))
