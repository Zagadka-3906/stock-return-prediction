"""Seal or read-only verify the single fixed R7 complement experiment.

No training, prediction, official rescoring, bootstrap resampling, or release
publication occurs here. Audit success and candidate qualification are distinct.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path
import re
import sys

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
OUT = ROOT / "experiments/r7_complement_20260926"
SOURCES = tuple(ROOT / "experiments" / f"{name}.py" for name in (
    "r7_complement", "r7_complement_signal", "r7_complement_diagnostics",
    "r7_complement_audit", "finalize_r7"))
FINAL_FILES = ("decision.json", "结论.md", "verification.json", "result_manifest.json")


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def read(path):
    return json.loads(Path(path).read_text(encoding="utf-8-sig"))


def sha(path):
    with Path(path).open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def relative(path):
    return Path(path).resolve().relative_to(ROOT).as_posix()


def confined(base, name):
    require(isinstance(name, str) and not Path(name).is_absolute(), "Expected relative artifact path")
    path = (base / name).resolve()
    require(path.is_relative_to(base.resolve()), f"Artifact escaped directory: {name}")
    return path


def verify_map(base, hashes):
    require(isinstance(hashes, dict) and bool(hashes), "Missing artifact hash map")
    for name, digest in hashes.items():
        require(sha(confined(base, name)) == digest, f"Changed artifact: {name}")


def source_map():
    return {relative(path): sha(path) for path in SOURCES}


def inventory():
    manifest = OUT / "result_manifest.json"
    files = {p for p in OUT.rglob("*") if p.is_file() and p != manifest} | set(SOURCES)
    require(not any(p.name.endswith(".pending") for p in files), "Unfinished writes remain")
    return {relative(path): sha(path) for path in sorted(files)}


def stage_evidence(name, runner, auditor):
    years = runner.DEVELOPMENT if name == "development" else runner.CONFIRMATION
    path = OUT / f"{name}.json"
    record = read(path)
    auditor._check_stage_record(record, name, sha(OUT / "protocol.json"))
    require(record["no_publication"] is True and record["no_weight_or_candidate_selection"] is True,
            "Stage must retain its single-candidate, research-only scope")
    # Validate every path before the runner's own strict fold/hash checks.
    for year in years:
        fold = read(OUT / f"fold_{year}.json")
        for key in fold["input_sha256"]:
            confined(ROOT, key)
        for key in fold["artifact_sha256"]:
            confined(OUT, key)
        require(set(fold["references"]) == {"baseline", "ensemble4"}, "Unexpected fold references")
    folds = runner.checked_folds(record)
    require(runner.gate(folds, name) == record["gate"], "Recorded point gate does not match frozen folds")
    require(record["point_gate_passed"] is record["gate"]["passed"], "Point-gate boolean differs")
    passed = auditor._stage_pass(record["gate"], record["bootstrap"])
    require(record[f"{name}_gate_passed"] is passed, "Combined point/bootstrap gate differs")
    if record["bootstrap"] is not None:
        for key, entry in record["bootstrap"].items():
            share = entry["bootstrap_share_positive"]
            require(math.isfinite(share) and 0 <= share <= 1, "Invalid bootstrap positive share")
            require(abs(entry["observed_mean_annual_score_delta"]
                        - record["gate"]["comparisons"][key]["mean_score_delta"]) <= 1e-12,
                    "Bootstrap observed difference does not match point estimate")
    audit_path = OUT / "independent_audit" / name / "score_audit.json"
    audit = read(audit_path)
    require(audit["status"] == "passed" and audit["stage_gate_passed"] is passed,
            "Independent audit failed or reports a different candidate gate")
    require(audit["stage"] == name and audit["primary_candidate"] == runner.PRIMARY
            and audit["completed_years"] == list(years), "Audit stage/candidate/years differ")
    require(audit["protocol_sha256"] == sha(OUT / "protocol.json")
            and audit["stage_record_sha256"] == sha(path)
            and audit["source_sha256"] == sha(ROOT / "experiments/r7_complement_audit.py"),
            "Independent audit binding changed")
    verify_map(ROOT, audit["artifacts_sha256"])
    expected = dict(read(OUT / "protocol.json")["input_sha256"])
    expected.update({relative(path): sha(path), relative(OUT / "protocol.json"): sha(OUT / "protocol.json")})
    for fold in folds:
        year = fold["year"]
        expected[relative(OUT / f"fold_{year}.json")] = sha(OUT / f"fold_{year}.json")
        expected.update(fold["input_sha256"])
        expected.update({relative(OUT / key): digest for key, digest in fold["artifact_sha256"].items()})
        for key in (runner.PRIMARY, "baseline", "ensemble4", f"{runner.PRIMARY}_raw"):
            daily = audit_path.parent / f"official_{key}_{year}_daily.csv"
            expected[relative(daily)] = sha(daily)
    require(all(audit["artifacts_sha256"].get(key) == value for key, value in expected.items()),
            "Independent audit omits or changes a stage input/artifact")
    metrics = {key: {str(f["year"]): f["metrics"] if key == runner.PRIMARY else f["references"][key]
                     for f in folds} for key in (runner.PRIMARY, "baseline", "ensemble4")}
    auditor._match(audit["metrics"], metrics, f"{name}/audited metrics")
    auditor._match(audit["raw_metrics"], {str(f["year"]): f["raw_metrics"] for f in folds}, f"{name}/raw metrics")
    auditor._match(audit["gate"], record["gate"], f"{name}/audited gate")
    auditor._match(audit["bootstrap"], record["bootstrap"], f"{name}/audited bootstrap")
    if name == "confirmation":
        require(record["development_sha256"] == sha(OUT / "development.json")
                and record["development_audit_sha256"] == sha(OUT / "independent_audit/development/score_audit.json"),
                "Confirmation does not bind its passed development audit")
        for year in years:
            training = audit["checks"][str(year)]["training"]
            require(all(training[key] is True for key in (
                "fixed_epoch30_and_past_only_metadata", "scaler_hash_verified",
                "model_equals_final_checkpoint", "raw_prefix_exact_reported")), "Unverified confirmation training lineage")
    return {"record": record, "folds": folds, "audit": audit, "passed": passed,
            "record_sha256": sha(path), "audit_sha256": sha(audit_path)}


def evidence():
    from experiments import r7_complement as runner, r7_complement_audit as auditor
    from experiments.verify_r6_results import verify as verify_previous
    require(runner.OUT == OUT and auditor.OUT == OUT, "Unexpected experiment output path")
    protocol = runner.verify_protocol()
    # Independent protocol checks include mandatory original-label/scorer hashes.
    auditor.verify_protocol()
    require(protocol["all_historical_years_previously_viewed"] is True
            and protocol["candidate_count"] == 1 and protocol["weight_search"] is False
            and protocol["postprocessor_search"] is False, "Protocol scope changed")
    require(relative(OUT / "sources.json") in protocol["input_sha256"], "References were not frozen")
    require(all(relative(path) in protocol["input_sha256"] for path in SOURCES[:-1]), "Source not frozen before scoring")
    dev = stage_evidence("development", runner, auditor)
    confirmation = None
    if dev["passed"]:
        confirmation = stage_evidence("confirmation", runner, auditor)
    else:
        require(not (OUT / "confirmation.json").exists()
                and not (OUT / "independent_audit/confirmation").exists()
                and not (OUT / "neural_training").exists(), "Confirmation exists after failed development")
        forbidden = [relative(p) for p in OUT.rglob("*")
                     if re.search(r"(?:^|_)(2023|2024)(?:[_.]|$)", p.name)]
        require(not forbidden, f"Confirmation artifacts exist after failed development: {forbidden}")
    previous = verify_previous()
    require(previous["status"] == "passed" and previous["active_release_unchanged"] is True,
            "Prior R6/R5/R4 integrity failed")
    require(previous == protocol["prior_r6_verification"], "Previous research verification differs from frozen evidence")
    active_hash = sha(ROOT / "active_release.json")
    require(protocol["input_sha256"].get("active_release.json") == active_hash
            and read(ROOT / "active_release.json")["release_id"] == "ensemble4_r4", "Active R4 release changed")
    return {"protocol": protocol, "development": dev, "confirmation": confirmation,
            "previous": previous, "active_hash": active_hash}


def decision_record(state):
    dev, confirmation = state["development"], state["confirmation"]
    if not dev["passed"]:
        reason = "development_point_gate_failed" if not dev["record"]["point_gate_passed"] else "development_bootstrap_gate_failed"
    elif not confirmation["passed"]:
        reason = "confirmation_point_gate_failed" if not confirmation["record"]["point_gate_passed"] else "confirmation_bootstrap_gate_failed"
    else:
        reason = "historical_gates_passed_research_only"
    return {"status": "research_complete_no_promotion", "primary_candidate": "neural10",
            "neural_weight": .1, "weight_optimized": False, "audit_status": "passed",
            "development_gate_passed": dev["passed"],
            "confirmation_gate_passed": confirmation["passed"] if confirmation else None,
            "historical_gates_passed": bool(confirmation and confirmation["passed"]), "terminal_reason": reason,
            "completed_years": dev["record"]["completed_years"] + (confirmation["record"]["completed_years"] if confirmation else []),
            "protocol_sha256": sha(OUT / "protocol.json"), "source_sha256": source_map(),
            "development_sha256": dev["record_sha256"], "development_audit_sha256": dev["audit_sha256"],
            "confirmation_sha256": confirmation["record_sha256"] if confirmation else None,
            "confirmation_audit_sha256": confirmation["audit_sha256"] if confirmation else None,
            "all_historical_years_previously_viewed": True, "formal_promotion": False,
            "formal_release_retained": "ensemble4_r4", "active_release_sha256": state["active_hash"]}


def verification_record(state):
    return {"status": "passed", "status_meaning": "Integrity and audit agreement; candidate gates are separate.",
            "formal_release": "ensemble4_r4", "active_release_sha256": state["active_hash"],
            "prior_r6_verification": state["previous"], "decision_sha256": sha(OUT / "decision.json"),
            "protocol_sha256": sha(OUT / "protocol.json"),
            "training_inference_official_scoring_or_resampling_performed": False}


def report(state):
    dev, confirmation = state["development"], state["confirmation"]
    mean_delta = dev["record"]["gate"]["comparisons"]["ensemble4"]["mean_score_delta"]
    minimum = state["protocol"]["gates"]["development"]["mean_score_delta_min"]
    if not dev["passed"] and mean_delta < minimum:
        lead = (f"候选相对 r4 的三年平均综合分变化为 {mean_delta:+.9f}，低于预定门槛 {minimum:+.3f}。"
                "开发已停止，未进入确认阶段；正式版本仍为 r4。")
    elif not dev["passed"]:
        lead = (f"候选相对 r4 的三年平均综合分变化为 {mean_delta:+.9f}，但未通过全部开发门槛。"
                "开发已停止，未进入确认阶段；正式版本仍为 r4。")
    else:
        lead = (f"候选相对 r4 的三年平均综合分变化为 {mean_delta:+.9f}；开发门槛通过，"
                f"确认门槛{'通过' if confirmation['passed'] else '未全部通过'}。本轮仅作重复历史研究，正式版本仍为 r4。")
    lines = ["# R7 固定 10% Transformer 补充信号结论", "",
        lead, "",
        "本轮只检验一个预先固定的补充信号：每日共同有效价格池内，对纠正后的 r4 原始合成信号与修复 Transformer 原始预测分别取平均并列百分位，再以 90%/10% 混合。混合发生在原 EMA 之前；EMA 0.9、留存 0.3、保护名单内部当前排序、原 pooled 辅助及其 25% 权重保持不变。名单和换手仍可能随信号改变。", "",
        "10% 是事前固定的排名信号权重，未经权重搜索，也不代表最优权重、资金配置比例或预期收益份额。三个开发年份复用已有折外神经网络预测，没有重新训练或择优轮次。", "",
        "所有历史年份均已看过，本假设还利用了 r6 的研究结论；开发与确认均为重复历史检验，不是新的盲测。正式版本始终保留 r4。", "",
        "## 开发期官方分数", "",
        "| 年份 | 10%候选 | r4 | pooled基准 | 候选−r4 |", "|---|---:|---:|---:|---:|"]
    for f in dev["folds"]:
        c, r, p = f["metrics"], f["references"]["ensemble4"], f["references"]["baseline"]
        lines.append(f"| {f['year']} | {c['final_score']:.9f} | {r['final_score']:.9f} | {p['final_score']:.9f} | {c['final_score']-r['final_score']:+.9f} |")
    lines += ["", "下表均为候选减 r4；年化超额与换手用小数表示。加权贡献分别为 0.4×IC差、0.3×年化超额差、−0.3×换手差，其和等于综合分差。", "",
              "| 年份 | IC差 | 年化超额差 | 换手差 | IC贡献 | 收益贡献 | 换手贡献 |", "|---|---:|---:|---:|---:|---:|---:|"]
    for f in dev["folds"]:
        c, r = f["metrics"], f["references"]["ensemble4"]
        ic, excess, turn = (c[k] - r[k] for k in ("ic_mean", "annual_excess", "mean_turnover"))
        require(abs(.4 * ic + .3 * excess - .3 * turn - (c["final_score"] - r["final_score"])) <= 1e-12,
                "Score decomposition does not match official final score")
        lines.append(f"| {f['year']} | {ic:+.6f} | {excess:+.6f} | {turn:+.6f} | {.4*ic:+.9f} | {.3*excess:+.9f} | {-.3*turn:+.9f} |")
    lines += ["", "## 事前门槛与独立复核", "",
        "开发要求同时相对 r4 和 pooled：三年平均分差≥0.001、最差年≥−0.005、平均IC差≥−0.002。仅在两个点估计门槛均通过后，才计算20日成对循环区块重采样（20,000次，种子2026），两个基准的正增量份额均须≥80%。确认期点门槛分别为0.0005、−0.003、−0.002，重采样门槛相同。", ""]
    for name, stage in (("开发", dev), ("确认", confirmation)):
        if stage is None:
            continue
        r = stage["record"]
        lines.append(f"{name}点估计门槛通过：{r['point_gate_passed']}；完整门槛通过：{stage['passed']}；独立审计：通过。审计通过表示数值和证据一致，并不表示候选达到门槛。")
        lines.append("")
        for key, label in (("ensemble4", "r4"), ("baseline", "pooled")):
            g = r["gate"]["comparisons"][key]
            noise = "未计算（点门槛失败）" if r["bootstrap"] is None else f"{r['bootstrap'][key]['bootstrap_share_positive']:.2%}"
            lines.append(f"- 相对{label}：平均分差 {g['mean_score_delta']:+.9f}，最差年 {g['worst_year_score_delta']:+.9f}，平均IC差 {g['mean_ic_delta']:+.6f}；重采样正增量份额：{noise}。")
        lines.append("")
    if not dev["passed"]:
        lines += ["开发未通过，已停止。没有产生2023—2024确认候选、确认训练目录或确认评分，也没有用未运行年份补齐成绩。", ""]
    else:
        lines += ["开发及独立审计通过后，才在新目录按原固定30轮协议完成2023—2024修复 Transformer 训练与确认。", "",
                  "| 确认年份 | 候选 | r4 | pooled | 候选−r4 |", "|---|---:|---:|---:|---:|"]
        for f in confirmation["folds"]:
            c, r, p = f["metrics"], f["references"]["ensemble4"], f["references"]["baseline"]
            lines.append(f"| {f['year']} | {c['final_score']:.9f} | {r['final_score']:.9f} | {p['final_score']:.9f} | {c['final_score']-r['final_score']:+.9f} |")
        lines += ["", "确认门槛全部通过；结果仍仅是重复历史研究，不会自动发布。" if confirmation["passed"] else "确认门槛未全部通过，候选停止，不晋级正式版本。", ""]
    lines += ["## 相关性与条件IC诊断", "",
              "以下直接引用各年 diagnostic_YEAR.json 的 date_equal_mean，按有定义的日期等权。共同池相关性包括涨停；IC与partial IC再限制为原始Float64标签可用的同一池。", "",
              "| 年份 | 两信号秩相关 | r4原始IC | 神经原始IC | 条件于r4的神经partial IC | partial有效日 | Top交并比 |",
              "|---|---:|---:|---:|---:|---:|---:|"]
    def fmt(value):
        return "未定义" if value is None else f"{value:.6f}"
    for f in dev["folds"]:
        diagnostic = read(OUT / f"diagnostic_{f['year']}.json")
        require(diagnostic["status"] == "descriptive_diagnostics_only"
                and diagnostic["mixed_predictions_created"] is False and diagnostic["weights_selected"] is False,
                "Diagnostic scope changed")
        means = diagnostic["date_equal_mean"]
        values = [fmt(means[k]) for k in ("raw_rank_correlation", "r4_rank_ic", "neural_rank_ic", "neural_partial_rank_ic_given_r4")]
        lines.append(f"| {f['year']} | " + " | ".join(values) + f" | {diagnostic['valid_days']['neural_partial_rank_ic_given_r4']} | {fmt(means['top_jaccard'])} |")
    lines += ["", "partial IC 是在同日有标签样本内去除截距和 r4 排名后的残差相关，仅用于事后描述；它不参与推理、定权或选模。低相关或正partial IC不能单独证明官方分数改善。官方收益Top先过滤标签，而换手Top不依赖标签；描述性Top池也与二者不同。重采样份额不是后验概率，也未校正跨轮研究选择偏差；本轮没有账户成交收益或交易成本结论。", "",
              "## 资料与复核", "",
              "下列一手资料仅支持研究不同模型信号组合的一般动机，不证明本赛题改善或10%最优；精确出处冻结于 [sources.json](sources.json)。", ""]
    sources = read(OUT / "sources.json")
    for entry in sources["sources"]:
        if "url" in entry:
            lines.append(f"- [{entry['title']}]({entry['url']})。")
    lines += ["", "实现与证据：[冻结协议](protocol.json)、[开发结果](development.json)、[独立开发审计](independent_audit/development/score_audit.json)、[诊断解读](诊断解读.md)、[最终决策](decision.json)、[完整清单](result_manifest.json)。", "",
              "在项目根目录执行 `.venv\\Scripts\\python.exe -B -X utf8 experiments/finalize_r7.py verify` 可只读检查全部R7文件、源代码、阶段门槛、独立审计及R6/R5/R4证据链，无需训练、推理或重复评分。", "",
              "无论门槛是否通过，本轮都不自动修改正式模型、提交、报告或 active_release.json。后续完整研究应新建实验目录，不覆盖本轮冻结结果。"]
    return "\n".join(lines) + "\n"


def write_new(path, value):
    with path.open("x", encoding="utf-8") as stream:
        if isinstance(value, str):
            stream.write(value)
        else:
            json.dump(value, stream, ensure_ascii=False, indent=2, allow_nan=False)


def seal():
    require(OUT.is_dir(), "Experiment directory is missing")
    require((OUT / "诊断解读.md").is_file(), "The diagnostic interpretation must be completed before sealing")
    require(not any((OUT / name).exists() for name in FINAL_FILES), "Finalization files already exist; preserve them")
    inventory()  # Reject partial runner writes before producing final files.
    state = evidence()
    decision, text = decision_record(state), report(state)
    write_new(OUT / "decision.json", decision)
    write_new(OUT / "结论.md", text)
    write_new(OUT / "verification.json", verification_record(state))
    manifest = {"status": "research_complete_no_promotion", "primary_candidate": "neural10",
                "protocol_sha256": sha(OUT / "protocol.json"), "source_sha256": source_map(),
                "artifact_sha256": inventory()}
    write_new(OUT / "result_manifest.json", manifest)
    return {"status": "sealed", "audit_status": "passed",
            "development_gate_passed": decision["development_gate_passed"],
            "confirmation_gate_passed": decision["confirmation_gate_passed"],
            "formal_promotion": False, "formal_release": "ensemble4_r4",
            "files_hashed": len(manifest["artifact_sha256"]),
            "result_manifest_sha256": sha(OUT / "result_manifest.json")}


def verify():
    manifest_path = OUT / "result_manifest.json"
    manifest = read(manifest_path)
    require(manifest["status"] == "research_complete_no_promotion" and manifest["primary_candidate"] == "neural10",
            "Research result is not sealed")
    require(manifest["source_sha256"] == source_map(), "Final source map changed")
    verify_map(ROOT, manifest["artifact_sha256"])
    require(manifest["artifact_sha256"] == inventory(), "Sealed inventory changed, has missing files or additional files")
    require(manifest["protocol_sha256"] == sha(OUT / "protocol.json"), "Manifest protocol differs")
    state = evidence()
    decision = decision_record(state)
    require(read(OUT / "decision.json") == decision, "Decision differs from verified stages")
    require(read(OUT / "verification.json") == verification_record(state), "Final verification evidence differs")
    require((OUT / "结论.md").read_text(encoding="utf-8") == report(state), "Report differs from verified evidence")
    return {"status": "passed", "status_meaning": "Integrity and audit agreement; candidate qualification is reported separately.",
            "audit_status": "passed", "development_gate_passed": decision["development_gate_passed"],
            "confirmation_gate_passed": decision["confirmation_gate_passed"],
            "historical_gates_passed": decision["historical_gates_passed"], "terminal_reason": decision["terminal_reason"],
            "formal_promotion": False, "formal_release": "ensemble4_r4", "active_release_unchanged": True,
            "previous_r6_verification": "passed", "files_hashed": len(manifest["artifact_sha256"]),
            "result_manifest_sha256": sha(manifest_path), "read_only": True,
            "training_inference_official_scoring_or_resampling_performed": False}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("seal", "verify"))
    action = parser.parse_args().action
    try:
        print(json.dumps({"seal": seal, "verify": verify}[action](), ensure_ascii=False, indent=2, allow_nan=False))
    except Exception as error:
        print(json.dumps({"status": "failed", "error": f"{type(error).__name__}: {error}"}, ensure_ascii=False), file=sys.stderr)
        raise SystemExit(1)
