"""Merge the three comparison layers into one unbiased model-comparison document.

Layer 1 (admissible): 2020-2024 same-protocol official validation, per-year + five-year + paired
moving-block CI95, from analysis/unbiased_model_comparison_20260929/comparison_unbiased.json.
Layer 2 (descriptive only): reconstructed test-period 343 days, paired CI95, from
comparison_test_period.json. Evaluation-set evidence; absolute 2026 levels carry ~+/-0.046 noise.
Layer 3 (pending arm): MLP h64/h128 same-protocol training-period validation, from
analysis/mlp_training_validation_20260929/summary.json when present, plus their recorded test-period
composites from analysis/all_models_test_20260929 (unified-postprocess caliber).

No arm is treated as the default. The document states, per arm, which layers exist and which do not.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "analysis" / "unbiased_model_comparison_20260929"
MLP = ROOT / "analysis" / "mlp_training_validation_20260929" / "summary.json"

DISPLAY = {
    "base63_8": "XGBoost 63特征 原学习率(0.05/180) ×8种子",
    "slow_only8": "XGBoost 63特征 慢学习率(0.025/360) ×8种子",
    "peer67_slow8": "XGBoost 67特征(含同伴列) 慢学习率 ×8种子",
    "peer67_slow16": "XGBoost 67特征(含同伴列) 慢学习率 ×16种子",
    "top2_lightgbm": "LightGBM Top10%样本权重×2（测试期榜首）",
    "mlp_h64": "MLP 隐藏64 窗口1 27轮 + 统一后处理",
    "mlp_h128": "MLP 隐藏128 窗口1 27轮 + 统一后处理",
}
YEARS = (2020, 2021, 2022, 2023, 2024)


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def main() -> None:
    train = load(OUT / "comparison_unbiased.json")
    test = load(OUT / "comparison_test_period.json")
    lines = ["# 模型无偏对比（2026-09-29）", "",
             "不预设任何方案为默认。第一层是唯一可用于选择的证据（2020—2024 同协议官方评分，"
             "测试标签赛后提供）；第二层是评测集上的描述性配对证据，只用于观察形状，不用于选择；"
             "第三层补齐此前唯一缺少训练期数字的神经臂。", "",
             "## 第一层：2020—2024 同协议官方评分", "",
             "| 臂 | " + " | ".join(str(y) for y in YEARS) + " | 五年均分 | 最差年 | 最差年份 | 年际sd |",
             "|---|" + "---|" * 9]
    arms = train["arms"]
    for arm in sorted(arms, key=lambda a: -arms[a]["five_year_mean"]):
        t = arms[arm]
        lines.append(f"| {DISPLAY.get(arm, arm)} | "
                     + " | ".join(f"{t['per_year'][str(y)]:.6f}" for y in YEARS)
                     + f" | {t['five_year_mean']:.6f} | {t['worst_year']:.6f} "
                     f"| {t['worst_year_name']} | {t['year_sd']:.6f} |")
    lines += ["", "配对差（A−B）与 20 日移动块 95% 区间：", "",
              "| 配对 | 五年差 | 年为正 | CI95 | 判定 | 重采样正差比例 |", "|---|---|---|---|---|---|"]
    for key, v in sorted(train["pairs"].items(), key=lambda kv: -abs(kv[1]["five_year_mean"])):
        a, b = key.split("__vs__")
        ci = v["ci95"]
        verdict = "**可分辨**" if ci[0] > 0 or ci[1] < 0 else "平局"
        lines.append(f"| {a} − {b} | {v['five_year_mean']:+.6f} | {v['years_positive']}/5 | "
                     f"[{ci[0]:+.6f}, {ci[1]:+.6f}] | {verdict} | {v['positive_share'] * 100:.1f}% |")

    lines += ["", "## 第二层：测试期 343 日（评测集证据，仅描述）", "",
              "| 臂 | 全期343日 | 2025 | 2026至6/5 |", "|---|---|---|---|"]
    for arm, c in sorted(test["composites"].items(), key=lambda kv: -kv[1]["full343"]):
        lines.append(f"| {DISPLAY.get(arm, arm)} | {c['full343']:.6f} | {c['2025']:.6f} "
                     f"| {c['2026']:.6f} |")
    lines += ["", "| 配对 | 全期差 | CI95 | 判定 | 重采样正差比例 |", "|---|---|---|---|---|"]
    for key, v in sorted(test["pairs"].items(), key=lambda kv: -abs(kv[1]["full343_diff"])):
        a, b = key.split("__vs__")
        ci = v["ci95"]
        verdict = "**可分辨**" if ci[0] > 0 or ci[1] < 0 else "平局"
        lines.append(f"| {a} − {b} | {v['full343_diff']:+.6f} | [{ci[0]:+.6f}, {ci[1]:+.6f}] | "
                     f"{verdict} | {v['positive_share'] * 100:.1f}% |")
    lines += ["", test["absolute_level_noise_note"], ""]

    lines += ["## 第三层：神经臂的训练期同协议验证", ""]
    if MLP.exists():
        m = load(MLP)
        agg = m["aggregate"]
        lines += ["| 臂 | " + " | ".join(str(y) for y in YEARS) + " | 五年均分 | 最差年 |",
                  "|---|" + "---|" * 7]
        for arm in ("mlp_h64", "mlp_h128"):
            per = agg[arm]["per_year_final_score"]
            worst = agg[arm]["worst_year"]
            lines.append(f"| {DISPLAY[arm]} | " + " | ".join(f"{per[str(y)]:.6f}" for y in YEARS)
                         + f" | {agg[arm]['five_year_equal_weight_mean']:.6f} "
                         f"| {worst['final_score']:.6f}（{worst['year']}） |")
        lines += ["", "对树模型臂的配对 20 日移动块区间：", "",
                  "| 配对 | 五年差 | CI95 | 判定 | 重采样正差比例 |", "|---|---|---|---|---|"]
        for key, v in m["paired_bootstrap"]["results"].items():
            arm, comp = key.split("__minus__")
            fy = v["five_year"]
            ci = fy.get("ci95") or [None, None]
            share = fy.get("share_positive", fy.get("positive_share", 0.0))
            verdict = "**可分辨**" if (ci[0] > 0 or ci[1] < 0) else "平局"
            lines.append(f"| {arm} − {comp} | {fy['mean_of_annual_deltas']:+.6f} | "
                         f"[{ci[0]:+.6f}, {ci[1]:+.6f}] | {verdict} | {share * 100:.1f}% |")
        hp = m.get("harness_proof", {})
        lines += ["", f"harness 证明：与已保存全期检查点的测试期原始预测逐位一致 = "
                      f"{hp.get('bit_identical')}，最大绝对差 {hp.get('max_abs_difference_all_rows')}，"
                      f"门通过 = {hp.get('gate_passed')}。"]
        lim = m.get("limitations")
        if lim:
            lines += ["", lim if isinstance(lim, str)
                      else json.dumps(lim, ensure_ascii=False)]
    else:
        lines += ["尚未完成：analysis/mlp_training_validation_20260929/summary.json 不存在。"]

    lines += ["", "## 第四层：其他测试期领先方案的训练期验证状态", "",
              "| 臂 | 测试期全期 | 训练期验证状态 |", "|---|---|---|",
              "| LightGBM Top2 加权 | 0.399530 | 已验证 0.390654，相对 slow-only8 −0.037270，区间全负 → 排除 |",
              "| MLP h128 + 统一后处理 | 0.398590 | 已验证 0.416630，相对 slow-only8 −0.011294，区间全负 → 排除 |",
              "| MLP h64 + 统一后处理 | 0.397935 | 已验证 0.416935，相对 slow-only8 −0.010989，区间全负 → 排除 |",
              "| LightGBM Top-K 原配方+pooled 辅助 | 0.398280 | 待验证：尚未完成完整配方的同口径五年验证；其他配方的历史辅助增益不构成本方案的提升上限，当前不能据此排除 |",
              "| LightGBM Top-K 成对目标（复用2021主干） | 0.397748 | 不可逐折因果验证（主干复用 2021 年模型），排除出合规轴 |",
              "| LightGBM + 16 量价/市场相对特征（79列） | 0.395355 | 已有冻结负记录：wave-9 扩展特征 3/3 年负、2024 −0.002206 |",
              "| LightGBM 留存加分 0.6 | 0.395350 | 已有冻结负记录：后处理轴双向关闭，bonus 扫描过 0.3，各值赢一年输一年 |",
              "| LightGBM 隔夜开盘收益排名目标 | 0.394360 | 已有冻结负记录：隔夜秩目标 IC→0.1047；wave-17 混合 horizon 2024 可分辨负 |",
              "",
              "读法：Top2与两组MLP已有同口径训练期验证，结果落后于slow-only8。"
              "Top-K原配方+pooled仍待验证，不能把其他配方的历史辅助增益当作它的提升上限。"
              "其余方案应按表中各自的实测范围或复现限制解读，未完成验证不等于已经验证失败。"
              "树模型簇内部多数配对区间包含零，不能据此证明方案等价；慢学习率与原学习率的63特征8种子配对区间不含零。"
              "Top2 与 MLP 两次独立呈现同一签名——测试期可分辨领先、训练期可分辨落后——"
              "本报告据此区分已实测结果和待验证方案，不使用已查看测试期的领先分数作采用依据。", "",
              "统计口径：各指标保留原有效交易日分母，首日缺失的换手率不计入分母。"
              "表中正差比例为重采样描述，不能解释为未来胜出概率；区间未校正此前重复选型影响。"]
    (OUT / "模型无偏对比.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"wrote {OUT / '模型无偏对比.md'} ({len(lines)} lines)")


if __name__ == "__main__":
    main()
