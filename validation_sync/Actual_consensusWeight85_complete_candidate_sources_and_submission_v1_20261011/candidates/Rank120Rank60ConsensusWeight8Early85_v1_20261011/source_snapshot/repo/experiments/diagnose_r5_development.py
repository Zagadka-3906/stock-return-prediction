"""Describe the three frozen development folds without opening confirmation."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
from statistics import mean

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "experiments/optimization_r5_20260926"
YEARS = (2020, 2021, 2022)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def main():
    target = OUT / "开发诊断.md"
    if target.exists():
        raise FileExistsError("Preserving the completed development diagnosis")
    dev = read(OUT / "development.json")
    protocol = read(OUT / "protocol.json")
    assert dev["protocol_sha256"] == digest(OUT / "protocol.json")
    assert protocol["development_years"] == list(YEARS)
    folds = {}
    for year in YEARS:
        path = OUT / f"fold_{year}.json"
        assert digest(path) == dev["fold_sha256"][path.name]
        folds[year] = read(path)
    components = {}
    for key, result in dev["candidate_results"].items():
        rows = {}
        for year, fold in folds.items():
            candidate = fold["candidates"][key]["metrics"]
            reference = fold["references"]["ensemble4"]
            row = {"ic": .4 * (candidate["ic_mean"] - reference["ic_mean"]),
                   "excess": .3 * (candidate["annual_excess"] - reference["annual_excess"]),
                   "turnover": -.3 * (candidate["mean_turnover"] - reference["mean_turnover"]),
                   "score": candidate["final_score"] - reference["final_score"]}
            assert abs(row["ic"] + row["excess"] + row["turnover"] - row["score"]) < 1e-12
            rows[year] = row
        rows["mean"] = {name: mean(row[name] for row in rows.values())
                        for name in ("ic", "excess", "turnover", "score")}
        assert abs(rows["mean"]["score"] - result["comparisons"]["ensemble4"]["mean_score_delta"]) < 1e-12
        components[key] = rows
    lines = [
        "# r5 开发期诊断（仅 2020—2022）", "",
        "本诊断只读取冻结协议、development.json 和 fold_2020/2021/2022.json。未读取确认期结果，未重新评分、添加候选或调整参数。所有年份此前均已查看，这次拆分仍属于回顾性研究。", "",
        "开发期唯一入选候选为 **xgb_two_mean**。其三年官方综合分均值为 0.435266633，相对修正 r4 集成平均增加 **0.001618899**，相对 pooled 基线增加 **0.004048643**。其余三项未满足预先冻结的开发门槛。", "",
        "## 分数贡献口径", "",
        "对每个年度，Δ综合分 = 0.4×ΔIC均值 + 0.3×Δ年化Top超额 − 0.3×Δ平均换手。以下三项都已乘官方权重，单位均为综合分；三年平均按年度等权。每行分项之和已与官方综合分之差核对，误差小于 1e−12。", "",
        "这里的换手是比赛定义的Top名单Jaccard换手惩罚，不是手续费，也不能直接推导真实成交成本。收益Top与换手Top仍沿用官方不同的标签过滤口径。", "",
        "| 候选 | IC贡献 | 年化超额贡献 | 换手贡献 | 平均总增量 vs r4 |", "|---|---:|---:|---:|---:|",
    ]
    for key, rows in components.items():
        r = rows["mean"]
        lines.append(f"| {key} | {r['ic']:+.9f} | {r['excess']:+.9f} | {r['turnover']:+.9f} | {r['score']:+.9f} |")
    lines += ["", "## 为什么三项未通过", "",
        "门槛须同时相对 r4 与 pooled 满足：平均综合分增量≥0.001，最差年度增量≥−0.005，平均IC增量≥−0.002。通过其中一个参照不够。", "",
        "| 候选 | 未过的冻结条件 | 其余条件 |", "|---|---|---|",
        "| lgb_xgb_two_median | 对r4平均增量 +0.000125845 < +0.001 | 对r4最差年度 −0.001003394、平均IC −0.000232443 均达标；pooled全部达标 |",
        "| stale_decay | 对r4平均增量 +0.000853878 < +0.001 | 对r4最差年度 −0.003621043、平均IC +0.000361773 均达标；pooled全部达标 |",
        "| downside_ema | 对r4平均增量 −0.001417345 < +0.001；最差年度 −0.008238234 < −0.005；对pooled最差年度 −0.005472966 < −0.005 | 两个参照的IC均达标；对pooled平均分 +0.001012399 勉强达标 |", "",
        "**秩中位数**的收益改善较小：超额贡献 +0.000357212，被IC下降 −0.000092977 和换手惩罚 −0.000138390 部分抵消。它在2021年优于r4，2020、2022年落后。该结果未支持本次固定中位数组合具有足够的开发期改进幅度，不能推广为否定所有稳健集成方法。", "",
        "**留存奖励衰减**确实在三个年度都提高了IC和Top年化超额；但三年平均年化超额增加约1.5178个百分点，平均Jaccard换手同时增加约1.2814个百分点，换手扣分抵消了大部分收益贡献。2021年收益增益足够覆盖换手损失，2020、2022年则不足。因此，它并非没有改善Top收益，而是没有达到本赛题综合目标的冻结门槛。", "",
        "**下行加速EMA**的IC在三个年度均改善，三年平均IC增加0.002473784；但平均Jaccard换手增加约1.6835个百分点，产生 −0.005050430 的分数损失，超过IC与超额的合计正贡献。2020年还伴随Top年化超额下降约1.3633个百分点，导致 −0.008238234 的明显回撤。该固定规则既没有达到平均增益要求，也触发了最差年度约束。", "",
        "## 唯一入选候选的优点与反例", "",
        "xgb_two_mean 使用XGB与两日LightGBM两个主干的等权横截面秩均值，继续使用相同pooled辅助及固定后处理；两个新模型组合均未读取历史泄漏裁剪缓存。相对r4四主干，主干成员数量减少为二，但这不能仅凭成员数推定推理速度或实盘收益。", "",
        "其开发期优势主要来自Top年化超额：三年平均增加约0.5648个百分点，对分数贡献 +0.001694388。IC贡献仅 +0.000052143；换手略升，扣分 −0.000127632。相对pooled三个年度均为正，相对r4只有2021、2022两个年度为正，**2020年仍落后0.000686708**。2021年的IC贡献也为负，说明优势并不是逐项、逐年一致改善。", "",
        "2022年相对r4增量 +0.003499178，约占三年增量总和的72.0%，存在年份集中性；2021年也有正贡献 +0.002044228，抵消2020年的损失。三年最差年度及平均IC仍通过冻结阈值。入选只表示满足开发期工程门槛，不能据此宣称统计显著、成本优势或独立样本外优势；确认与账户审计应由已冻结流程单独决定。", "",
        "## 年度分解（对修正r4）", "",
        "| 候选 | 年份 | IC贡献 | 年化超额贡献 | 换手贡献 | 总增量 |", "|---|---:|---:|---:|---:|---:|",
    ]
    for key, rows in components.items():
        for year in YEARS:
            r = rows[year]
            lines.append(f"| {key} | {year} | {r['ic']:+.9f} | {r['excess']:+.9f} | {r['turnover']:+.9f} | {r['score']:+.9f} |")
    lines += ["", "## 输入校验", "", "本文件为评分后的解释性分解，不参与候选选择或协议修改。", "",
              f"- 协议SHA256：`{dev['protocol_sha256']}`",
              f"- development.json SHA256：`{digest(OUT / 'development.json')}`"]
    lines += [f"- {name} SHA256：`{value}`" for name, value in dev["fold_sha256"].items()]
    lines += [f"- 独立分析源码：`experiments/diagnose_r5_development.py`；SHA256：`{digest(Path(__file__))}`", ""]
    with target.open("x", encoding="utf-8") as stream:
        stream.write("\n".join(lines))
    print(json.dumps({"status": "passed", "decomposition_rows_checked": 12,
                      "years_read": YEARS, "confirmation_read": False,
                      "report": target.relative_to(ROOT).as_posix()}, ensure_ascii=True))


if __name__ == "__main__":
    main()
