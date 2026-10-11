"""Close three independent r6 research units after their gates and audits."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import sys
from datetime import datetime

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
T = ROOT / "experiments/r6_transformer_20260926"
V = ROOT / "experiments/r6_value5_20260926"
K = ROOT / "experiments/r6_topk_20260926"
OUT = ROOT / "experiments/r6_results_20260926"


def read(path):
    return json.loads(Path(path).read_text(encoding="utf-8-sig"))


def sha(path):
    with Path(path).open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def write_new(path, value):
    with Path(path).open("x", encoding="utf-8") as stream:
        json.dump(value, stream, ensure_ascii=False, indent=2, allow_nan=False)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    if (OUT / "result_manifest.json").exists():
        raise FileExistsError("Completed research already sealed")
    from experiments.r6_transformer import verify_protocol
    from experiments.r6_transformer_audit import _frozen_development
    verify_protocol()
    td, ta, tm = _frozen_development()
    audit = read(T / "independent_audit/development/score_audit.json")
    assert audit["status"] == "passed"
    assert audit["stage_record_sha256"] == sha(T / "development.json")
    assert audit["stage_gate_passed"] == td["development_gate_passed"]
    if td["development_gate_passed"]:
        tc = read(T / "confirmation.json")
        ac = read(T / "independent_audit/confirmation/score_audit.json")
        assert ac["status"] == "passed" and ac["stage_record_sha256"] == sha(T / "confirmation.json")
        assert ac["stage_gate_passed"] == tc["official_and_noise_gate_passed"]
    else:
        assert not (T / "confirmation.json").exists()
    vd, kd = read(V / "development.json"), read(K / "development.json")
    # Both fixed CPU units must be terminal before writing a combined result.
    for folder, record in ((V, vd), (K, kd)):
        if record["gate"]["passed"]:
            assert (folder / "confirmation.json").is_file()
        else:
            assert not (folder / "confirmation.json").exists()
        protocol = read(folder / "protocol.json")
        for relative, digest in protocol["input_sha256"].items():
            assert sha(ROOT / relative) == digest, relative
    from experiments.verify_r5_results import verify as verify_previous
    previous = verify_previous()
    assert previous["status"] == "passed" and previous["active_release_unchanged"]
    # New independent CPU audit is read as evidence; never append into old unit manifests.
    cross = ROOT / "experiments/r6_cross_audit_20260926/summary.json"
    assert cross.is_file(), "Independent CPU audit must finish first"
    cross_result = read(cross)
    assert cross_result["status"] == "passed"
    assert sha(ROOT / cross_result["source_path"]) == cross_result["source_sha256"]
    evidence = ROOT / cross_result["evidence_manifest_path"]
    assert sha(evidence) == cross_result["evidence_manifest_sha256"]
    for relative, digest in read(evidence)["artifact_sha256"].items():
        assert sha(ROOT / relative) == digest, relative
    for name, folder, record in (("value5", V, vd), ("topk", K, kd)):
        filename = f"{name}_audit.json"
        assert sha(cross.parent / filename) == cross_result["audit_sha256"][filename]
        cpu_audit = read(cross.parent / filename)
        assert cpu_audit["status"] == "passed"
        assert cpu_audit["gate_passed"] == record["gate"]["passed"]
        assert cross_result["candidate_gates_passed"][name] == record["gate"]["passed"]
        for relative, digest in cpu_audit["original_unit_snapshot_sha256"].items():
            assert sha(folder / relative) == digest, relative
    # Top-K also has a final seal for interpretation and model-reproduction evidence.
    for relative, digest in read(K / "final_manifest.json")["artifact_sha256"].items():
        assert sha(K / relative) == digest, relative
    completed = td["completed_years"]
    unit_decision = {"status": "complete_research_no_promotion", "completed_years": completed,
        "early_stop_reason": td["early_stop_reason"], "development_gate_passed": td["development_gate_passed"],
        "mechanism_gate": tm, "aggregate": ta, "independent_audit_passed": True,
        "protocol_sha256": sha(T / "protocol.json"), "development_sha256": sha(T / "development.json"),
        "independent_audit_sha256": sha(T / "independent_audit/development/score_audit.json"),
        "formal_release_retained": "ensemble4_r4"}
    write_new(T / "decision.json", unit_decision)
    rows = []
    for year in completed:
        f = read(T / f"fold_{year}.json")
        a, b = f["candidates"]["shared"], f["candidates"]["feature_identity"]
        rows.append(f"| {year} | {a['raw_metrics']['ic_mean']:.6f} | {b['raw_metrics']['ic_mean']:.6f} | {a['metrics']['final_score']:.9f} | {b['metrics']['final_score']:.9f} | {f['references']['ensemble4']['final_score']:.9f} | {b['metrics']['final_score']-f['references']['ensemble4']['final_score']:+.9f} |")
    lines = ["# r6 三项改进实施结果", "",
        "本轮完成三个独立单元的实现、事前配置冻结、历史验证和独立核验。现有年份均已反复查看；本轮没有新的盲测，也没有改写 r5 的失败结论。正式入口仍为 r4。", "",
        "特征身份修复通过了三年机制对照，但未达到替代现有主干的开发门槛；五日价值校准与连续Top-K损失也未通过各自的开发门槛。三个单元均停止于开发阶段，没有进入2023—2024确认期。", "",
        "## Transformer 特征身份修复", "",
        "已将共享标量编码改为逐特征独立权重与偏置。两组初始函数、encoder、CLS、输出层相同，之后特征参数可独立更新。两组都使用63项特征、30轮、相同种子与日期批次、Adam学习率0.001；只用预测年前已成熟标签及训练期归一化统计。参数量由17,217增至21,185，等训练预算不表示参数量完全相同。", "",
        "| 年份 | 旧结构原始IC | 修复原始IC | 旧结构综合分 | 修复综合分 | r4综合分 | 修复−r4 |",
        "|---|---:|---:|---:|---:|---:|---:|"] + rows
    if td["early_stop_reason"]:
        stage_description = "已完成全部三个开发年份" if len(completed) == 3 else f"已完成开发年份 {completed}"
        lines += ["", f"{stage_description}。在{completed[-1]}年触发训练前固定的最差年度硬门槛：修复组相对至少一个基准的单年分差低于−0.005。因此停止后续确认；没有估算未运行年份的成绩。"]
    lines.append("")
    for name, label in (("ensemble4", "r4"), ("baseline", "pooled")):
        comparison = ta["comparisons"][name]
        lines.append(f"- 相对{label}：平均综合分差 {comparison['mean_score_delta']:+.9f}，最差年度分差 {comparison['worst_year_score_delta']:+.9f}，平均IC差 {comparison['mean_ic_delta']:+.6f}。")
    lines += ["", f"开发门槛通过：{td['development_gate_passed']}；修复相对旧结构的三年机制门槛通过：{tm['passed']}。修复相对旧结构平均综合分变化 {tm['mean_score_delta_vs_shared']:+.9f}，原始IC变化 {tm['mean_raw_ic_delta_vs_shared']:+.6f}。", "",
        "结构修复和原始预测改善必须与最终评分区分。当前后处理原本围绕树模型信号固定；本轮没有以调平滑、改权重或择优轮数挽救候选。",
        "", "## 五日收益价值校准", "",
        "2020—2021年的折外预测与成熟五日标签用于拟合；2022检验。唯一机制基准是联合rank/EMA五项二阶校准器；新增候选含昨日成员、在位年龄、排名变化和过去五日平均排名，共9项。两者同为固定正则的Ridge，训练与门槛评价按日期等权。"]
    vc = vd["gate"]["comparison"]
    lines += ["", f"2022相对该机制对照：MSE相对改善 {vc['relative_daily_mse_improvement']*100:+.6f}%，五日Rank IC变化 {vc['rank_ic5_delta']:+.6f}，预测Top组五日超额变化 {vc['top5_return_delta']*10000:+.4f} bp。门槛通过：{vd['gate']['passed']}。",
        "", "五日目标是连续五个全市场交易日的原始每日超额之和，基准为当日全有限标签池均值（包含涨停行），与官方过滤后的股票池不同。缺失标签不填零，评价排除末五个在当年内无法成熟的信号日；Top先依据当日可用预测形成，未来标签缺失只影响测量覆盖率，不回填成员。20日区块重采样中MSE改善的份额为10.44%，四项门槛全部失败，因此未评估2023—2024。该诊断不是官方综合分，也不是账户净收益。失败只否定本次固定低容量实现，不能证明所有多期价值模型无效。", "",
        "## 连续 Top-K 收益损失", "",
        "新LightGBM主干以连续Float64收益差衡量Top边界交换，采用均匀抽样的条件无偏梯度与对角Hessian。固定31叶、180轮，仍使用原pooled辅助与完整后处理。没有同时优化IC或状态化换手。", "",
        "| 年份 | 新主干综合分 | r4综合分 | 增量 | 新主干最终IC |",
        "|---|---:|---:|---:|---:|"]
    for year in (2020, 2021, 2022):
        f = read(K / f"fold_{year}.json")
        lines.append(f"| {year} | {f['metrics']['final_score']:.9f} | {f['references']['ensemble4']['final_score']:.9f} | {f['metrics']['final_score']-f['references']['ensemble4']['final_score']:+.9f} | {f['metrics']['ic_mean']:.6f} |")
    lines += ["", f"开发门槛通过：{kd['gate']['passed']}。相对r4平均综合分差 {kd['gate']['comparisons']['ensemble4']['mean_score_delta']:+.9f}。仅对齐Top收益，不保证占40%权重的全截面IC与占30%的换手项保留。本轮已按失败门槛停止，没有回选模型或重调损失尺度。", "",
        "## 可复核产物", "",
        "- [Transformer代码](../r6_transformer.py)、[冻结协议](../r6_transformer_20260926/protocol.json)、[开发结果](../r6_transformer_20260926/development.json)、[独立评分审计](../r6_transformer_20260926/independent_audit/development/score_audit.json)。",
        "- [五日校准结论](../r6_value5_20260926/结论.md)、[实现](../r6_value5.py)。",
        "- [Top-K损失结论](../r6_topk_20260926/结论.md)、[分项归因](../r6_topk_20260926/结果解读.md)、[实现](../r6_topk.py)。",
        "- [两个CPU单元的独立核验](../r6_cross_audit_20260926/summary.json)、[此前研究依据](../research_r6_20260926/后续优化研究.md)。", "",
        "在项目根目录运行 `.venv\\Scripts\\python.exe -B -X utf8 experiments/verify_r6_results.py` 可只读复核全部产物与历史正式版本，不需要重训。", "",
        "官方复算使用原CSV Float64标签和未修改的evaluate.py。列置换、梯度、目标连续交易日、标签边界、未来输入/标签不变性等检查与结果同存。当前提交、正式模型、报告和历史证据的完整性校验通过。", "",
        "这些受控实验帮助排除具体方案；它们没有产生已确认优于r4的新版本。后续若继续研究，必须基于新的机制证据独立设计，并持续披露已有历史的选择偏差。"]
    with (OUT / "实施结论.md").open("x", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    write_new(OUT / "verification.json", {"status": "passed", "completed_at_local": datetime.now().astimezone().isoformat(timespec="seconds"),
        "prior_release_verification": previous, "independent_cpu_audit_sha256": sha(cross),
        "active_release_sha256": sha(ROOT / "active_release.json"), "formal_release": "ensemble4_r4"})
    unit_paths = [p for p in T.rglob("*") if p.is_file() and "__pycache__" not in p.parts and p.name != "result_manifest.json"]
    write_new(T / "result_manifest.json", {"status": "complete_research_no_promotion", "artifact_sha256": {p.relative_to(ROOT).as_posix(): sha(p) for p in sorted(unit_paths)}, "source_sha256": sha(ROOT / "experiments/r6_transformer.py")})
    paths = [p for folder in (T, V, K, cross.parent, OUT) for p in folder.rglob("*") if p.is_file() and "__pycache__" not in p.parts]
    paths += [ROOT / "experiments" / name for name in ("r6_transformer.py", "r6_transformer_audit.py", "r6_value5.py", "r6_topk.py", "r6_cross_audit.py", "finalize_r6.py", "verify_r6_results.py")]
    manifest = {"status": "research_complete_no_promotion", "artifact_sha256": {p.relative_to(ROOT).as_posix(): sha(p) for p in sorted(set(paths))}}
    write_new(OUT / "result_manifest.json", manifest)
    for relative, digest in manifest["artifact_sha256"].items(): assert sha(ROOT / relative) == digest
    print(json.dumps({"status": "passed", "files_hashed": len(manifest["artifact_sha256"]), "formal_release": "ensemble4_r4"}))


if __name__ == "__main__":
    main()
