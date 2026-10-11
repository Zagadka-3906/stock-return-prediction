"""Seal or read-only verify the fixed R9 OOF residual research experiment.

Only JSON arithmetic and bound-file hashes are checked. This module never
trains, predicts, scores, resamples, changes gates or publishes a release.
Its own source is bound by the final manifest, outside the training protocol.
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
OUT = ROOT / "experiments/r9_residual_20260926"
SOURCE_NAMES = ("r9_residual.py", "r9_residual_core.py", "r9_residual_audit.py",
                "r9_research_notes_20260926.md", "finalize_r9.py")
FINAL_FILES = ("decision.json", "verification.json", "结论.md", "result_manifest.json")


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
    require(isinstance(name, str) and not Path(name).is_absolute(), "Expected a relative bound path")
    path = (base / name).resolve()
    require(path.is_relative_to(base.resolve()), f"Bound path escaped its directory: {name}")
    return path


def verify_map(base, hashes):
    require(isinstance(hashes, dict) and bool(hashes), "Missing hash bindings")
    for name, digest in hashes.items():
        require(sha(confined(base, name)) == digest, f"Changed bound file: {name}")


def source_map():
    return {f"experiments/{name}": sha(ROOT / "experiments" / name) for name in SOURCE_NAMES}


def inventory():
    manifest = OUT / "result_manifest.json"
    paths = {p for p in OUT.rglob("*") if p.is_file() and p != manifest}
    paths.update(ROOT / "experiments" / name for name in SOURCE_NAMES)
    require(not any(p.name.endswith(".pending") for p in paths), "Incomplete writes remain")
    return {relative(path): sha(path) for path in sorted(paths)}


def combined_gate(record, official, mechanism, protocol):
    require(record["gate"] == official and record["mechanism_gate"] == mechanism,
            "Point gates disagree with verified fold JSON")
    point = bool(official["passed"] and mechanism["passed"])
    require(record["point_gate_passed"] is point, "Combined point-gate flag differs")
    bootstrap = record["bootstrap"]
    if not point:
        require(bootstrap is None, "Bootstrap must be absent after a failed point gate")
        return False
    require(isinstance(bootstrap, dict) and set(bootstrap) == {"ensemble4", "baseline"},
            "Both reference bootstraps are required after point-gate success")
    settings = protocol["gates"]["bootstrap"]
    passes = []
    for name, entry in bootstrap.items():
        require(all(entry[key] == settings[key] for key in ("block_days", "draws", "seed"))
                and entry["years"] == record["years"], "Bootstrap settings or years changed")
        share = entry["bootstrap_share_positive"]
        require(math.isfinite(share) and 0 <= share <= 1, "Invalid bootstrap positive share")
        passed = share >= settings["positive_share_min"]
        require(entry["passes_positive_share_80pct"] is passed, "Bootstrap pass flag differs")
        require(abs(entry["observed_mean_annual_score_delta"]
                    - official["comparisons"][name]["mean_score_delta"]) <= 1e-12,
                "Bootstrap observed mean differs from fold scores")
        passes.append(passed)
    return all(passes)


def stage_evidence(name, protocol, runner, auditor):
    years = runner.DEVELOPMENT if name == "development" else runner.CONFIRMATION
    path = OUT / f"{name}.json"
    record = read(path)
    require(record["stage"] == name and record["candidate_key"] == runner.PRIMARY
            and record["years"] == list(years)
            and record["protocol_sha256"] == sha(OUT / "protocol.json"), "Stage identity changed")
    require(record["historical_years_previously_viewed"] is True and record["formal_promotion"] is False,
            "Stage no longer has its repeated-history, research-only scope")
    require(set(record["fold_sha256"]) == {f"fold_{y}.json" for y in years}, "Missing or extra stage folds")
    verify_map(OUT, record["fold_sha256"])
    folds = []
    required_bindings = dict(protocol["input_sha256"])
    required_bindings.update(protocol["source_sha256"])
    required_bindings.update({relative(path): sha(path), relative(OUT / "protocol.json"): sha(OUT / "protocol.json")})
    for year in years:
        fold_path = OUT / f"fold_{year}.json"
        fold = read(fold_path)
        for key in fold["artifact_sha256"]:
            confined(OUT, key)
        runner.check_fold(fold, year)
        require(set(fold["references"]) == {"baseline", "ensemble4"}, "Unexpected references")
        bounds, training = fold["boundaries"], fold["training"]
        require(bounds["last_label_available"] < bounds["validation_first"]
                and bounds["last_training_signal"] < bounds["validation_first"]
                and bounds["training_oof_years"] == list(range(2020, year))
                and bounds["strict_next_market_date_before_validation"] is True, "Immature or wrong-year training labels")
        require(all(fold["tests"][key] is True for key in (
            "actual_zero_calibration_exact_r4", "model_reload_exact", "label_and_availability_invariance",
            "prefix_50days_exact", "finite_and_invalid_price_excluded")), "Missing fold invariance checks")
        calibration = read(OUT / f"calibration_{year}.json")
        require(math.isfinite(calibration["intercept"]) and math.isfinite(calibration["slope"])
                and calibration["slope"] > 0 and math.isfinite(calibration["weighted_mse"])
                and calibration["weighted_mse"] >= 0, "Invalid WLS calibration")
        require(calibration["training_rows"] == training["rows"]
                and calibration["training_dates"] == training["dates"]
                and calibration["params"] == protocol["params"] and calibration["rounds"] == protocol["rounds"]
                and calibration["feature_names"] == protocol["feature_names"]
                and calibration["model_feature_names"] == training["model_feature_names"]
                == protocol["feature_names"] + ["r4_percentile"], "Calibration/model training metadata changed")
        require(training["feature_cache_labels_never_used"] is True and training["feature_matrix_dtype"] == "float32"
                and abs(training["mean_weight"] - 1) <= 1e-12, "Feature precision or mean-one weighting changed")
        required_bindings[relative(fold_path)] = sha(fold_path)
        required_bindings.update({relative(OUT / key): value for key, value in fold["artifact_sha256"].items()})
        folds.append(fold)
    official, mechanism = runner.point_gate(folds, name)
    passed = combined_gate(record, official, mechanism, protocol)
    require(record[f"{name}_gate_passed"] is passed, "Final stage gate differs")
    audit_path = OUT / "independent_audit" / f"audit_{name}.json"
    audit = read(audit_path)
    require(audit["status"] == "passed" and audit["stage_gate_passed"] is passed
            and audit["stage"] == name and audit["candidate_key"] == runner.PRIMARY
            and audit["years"] == list(years), "Independent audit status/stage/gate differs")
    require(audit["stage_record_sha256"] == sha(path)
            and audit["protocol_sha256"] == sha(OUT / "protocol.json")
            and audit["source_sha256"] == sha(ROOT / "experiments/r9_residual_audit.py"), "Audit source/input binding changed")
    verify_map(ROOT, audit["artifacts_sha256"])
    for year in years:
        names = [f"{name}_mechanism_{year}.csv"] + [
            f"{name}_official_{key}_{year}.csv" for key in (runner.PRIMARY, "baseline", "ensemble4")]
        for filename in names:
            daily = OUT / "independent_audit" / filename
            required_bindings[relative(daily)] = sha(daily)
    if name == "confirmation":
        for prior in (OUT / "development.json", OUT / "independent_audit/audit_development.json"):
            required_bindings[relative(prior)] = sha(prior)
        required_bindings.update(read(OUT / "independent_audit/audit_development.json")["artifacts_sha256"])
    require(all(audit["artifacts_sha256"].get(key) == value for key, value in required_bindings.items()),
            "Independent audit omits or changes required source/input/fold/stage evidence")
    for field in ("gate", "mechanism_gate", "bootstrap"):
        auditor.match(audit[field], record[field], f"{name}/{field}")
    expected = [{key: fold[key] for key in ("year", "mechanism", "metrics", "references")} for fold in folds]
    auditor.match(audit["folds"], expected, f"{name}/audited folds")
    return {"record": record, "folds": folds, "passed": passed,
            "record_sha256": sha(path), "audit_sha256": sha(audit_path)}


def evidence():
    from experiments import r9_residual as runner, r9_residual_audit as auditor
    from experiments.r8_diagnose_and_speed import verify as verify_previous
    require(runner.OUT == OUT and auditor.OUT == OUT, "Unexpected research directory")
    protocol = runner.verify_protocol()
    require(protocol["primary_candidate"] == runner.PRIMARY and protocol["candidate_count"] == 1
            and protocol["development_years"] == [2022] and protocol["confirmation_years"] == [2023, 2024]
            and protocol["historical_years_previously_viewed"] is True, "Protocol scope changed")
    expected_sources = {k: v for k, v in source_map().items() if k != relative(Path(__file__))}
    require(protocol["source_sha256"] == expected_sources, "Frozen R9 source set differs")
    development = stage_evidence("development", protocol, runner, auditor)
    confirmation = None
    if development["passed"]:
        confirmation = stage_evidence("confirmation", protocol, runner, auditor)
    else:
        forbidden = [relative(path) for path in OUT.rglob("*")
                     if re.search(r"(?:^|_)(2023|2024)(?:[_.]|$)", path.name)
                     or path.name in {"confirmation.json", "audit_confirmation.json", "confirmation", "neural_training"}]
        require(not forbidden, f"Confirmation exists after failed development: {forbidden}")
    previous = verify_previous()
    require(previous["status"] == "passed" and previous == protocol["previous_r8_verification"],
            "Previous R8/R7/R6/R5/R4 evidence changed")
    active_hash = sha(ROOT / "active_release.json")
    require(protocol["input_sha256"].get("active_release.json") == active_hash
            and read(ROOT / "active_release.json")["release_id"] == "ensemble4_r4", "Formal R4 release changed")
    return {"protocol": protocol, "development": development, "confirmation": confirmation,
            "previous": previous, "active_hash": active_hash}


def decision_record(state):
    dev, conf = state["development"], state["confirmation"]
    stopped = "development" if not dev["passed"] else "confirmation" if not conf["passed"] else None
    failed = state[stopped]["record"] if stopped else None
    reason = (f"{stopped}_point_gate_failed" if failed and not failed["point_gate_passed"]
              else f"{stopped}_bootstrap_gate_failed" if failed else "historical_gates_passed_research_only")
    stages = {name: {"audit_status": "passed", "gate_passed": stage["passed"],
                    "official_gate_passed": stage["record"]["gate"]["passed"],
                    "mechanism_gate_passed": stage["record"]["mechanism_gate"]["passed"],
                    "stage_sha256": stage["record_sha256"], "audit_sha256": stage["audit_sha256"]}
              for name, stage in (("development", dev), ("confirmation", conf)) if stage}
    return {"status": "research_complete_no_promotion", "candidate_key": "oof_residual",
            "audit_status": "passed", "development_gate_passed": dev["passed"],
            "confirmation_gate_passed": conf["passed"] if conf else None,
            "historical_gates_passed": bool(conf and conf["passed"]), "terminal_reason": reason,
            "completed_years": dev["record"]["years"] + (conf["record"]["years"] if conf else []),
            "stages": stages, "protocol_sha256": sha(OUT / "protocol.json"), "source_sha256": source_map(),
            "formal_release_retained": "ensemble4_r4", "active_release_sha256": state["active_hash"],
            "formal_promotion": False, "historical_years_previously_viewed": True}


def verification_record(state):
    return {"status": "passed", "meaning": "Integrity/audit agreement; candidate qualification is separate.",
            "formal_release": "ensemble4_r4", "active_release_sha256": state["active_hash"],
            "previous_r8_verification": state["previous"], "decision_sha256": sha(OUT / "decision.json"),
            "protocol_sha256": sha(OUT / "protocol.json"),
            "training_prediction_scoring_or_resampling_performed": False}


def report(state):
    dev, conf = state["development"], state["confirmation"]
    first = dev["folds"][0]
    mechanism, metric, references = first["mechanism"], first["metrics"], first["references"]
    status = ("开发门槛未全部通过，已停止，没有进入2023—2024确认。" if not dev["passed"] else
              "开发通过，确认门槛未全部通过，候选停止。" if not conf["passed"] else
              "预设开发与确认门槛均通过，但只构成重复历史研究结果，不自动晋级。")
    lines = ["# R9 固定 OOF 误差修正结论", "",
        f"2022年日期等权MSE从零修正的 {mechanism['mse_zero']:.9f} 变为 {mechanism['mse_candidate']:.9f}，"
        f"相对改善 {mechanism['relative_daily_mse_improvement']:.4%}；同池原始RankIC变化 {mechanism['mean_raw_rank_ic_delta']:+.6f}。"
        f"完整后处理综合分 {metric['final_score']:.9f}，相对r4 {metric['final_score']-references['ensemble4']['final_score']:+.9f}，"
        f"相对pooled {metric['final_score']-references['baseline']['final_score']:+.9f}。{status}正式版本仍为r4。", "",
        "## 实际结果", "",
        "| 年份 | 零修正MSE | 修正MSE | 相对MSE改善 | 零修正原始IC | 修正原始IC | 原始IC差 |",
        "|---|---:|---:|---:|---:|---:|---:|"]
    folds = dev["folds"] + (conf["folds"] if conf else [])
    for fold in folds:
        m = fold["mechanism"]
        lines.append(f"| {fold['year']} | {m['mse_zero']:.9f} | {m['mse_candidate']:.9f} | {m['relative_daily_mse_improvement']:.4%} | {m['raw_rank_ic_zero']:.6f} | {m['raw_rank_ic_candidate']:.6f} | {m['mean_raw_rank_ic_delta']:+.6f} |")
    lines += ["", "| 年份 | 候选综合分 | r4综合分 | pooled综合分 | 候选−r4 | 候选−pooled |", "|---|---:|---:|---:|---:|---:|"]
    for fold in folds:
        c, r, p = fold["metrics"]["final_score"], fold["references"]["ensemble4"]["final_score"], fold["references"]["baseline"]["final_score"]
        lines.append(f"| {fold['year']} | {c:.9f} | {r:.9f} | {p:.9f} | {c-r:+.9f} | {c-p:+.9f} |")
    lines += ["", "综合分差仅作恒等式分解：0.4×IC差＋0.3×年化超额差−0.3×Jaccard换手差。下表是各分项对分差的算术贡献，不据此推断市场状态或模型因果。", "",
              "| 年份 | 参照 | IC项贡献 | 收益项贡献 | 换手项贡献 | 合计 |", "|---|---|---:|---:|---:|---:|"]
    for fold in folds:
        for key, label in (("ensemble4", "r4"), ("baseline", "pooled")):
            c, r = fold["metrics"], fold["references"][key]
            parts = [.4*(c["ic_mean"]-r["ic_mean"]), .3*(c["annual_excess"]-r["annual_excess"]), -.3*(c["mean_turnover"]-r["mean_turnover"])]
            require(abs(sum(parts) - (c["final_score"]-r["final_score"])) <= 1e-12, "Official decomposition mismatch")
            lines.append(f"| {fold['year']} | {label} | {parts[0]:+.9f} | {parts[1]:+.9f} | {parts[2]:+.9f} | {sum(parts):+.9f} |")
    lines += ["", "## 固定方法与成熟边界", "",
        "输入为原63项特征加完整价格有效池内的r4原始百分位b，共64项。只用此前年度纠正后的r4折外预测，先拟合日期等权正斜率WLS：m(b)=a+beta×b，再用固定7叶、80轮、学习率0.05、min_data_in_leaf=1000、L2=10、种子2026的LightGBM拟合u−m(b)。推理为m(b)+残差，沿用原EMA、留存、保护排序和25% pooled辅助，没有新增融合权重、早停或参数选择。", "",
        "原始收益、b/u、WLS及残差构造保留Float64；模型输入矩阵为Float32，LightGBM内部标签/权重使用库自身精度。校准权重总和为1；树权重N/(D×n日)均值为1，保证日期等权并保持固定L2尺度。min_data_in_leaf是库的近似限制，不保证每叶实数样本严格≥1000。", "",
        "| 预测年 | 训练OOF年 | 最后训练信号日 | 最后标签成熟日 | 首个预测日 | 剔除未成熟信号日 |",
        "|---|---|---:|---:|---:|---|"]
    for fold in folds:
        b = fold["boundaries"]
        lines.append(f"| {fold['year']} | {','.join(map(str,b['training_oof_years']))} | {b['last_training_signal']} | {b['last_label_available']} | {b['validation_first']} | {','.join(map(str,b['purged_signal_dates'])) or '无'} |")
    lines += ["", "标签成熟日取全市场下一个交易日，并严格早于首个预测日；不是自然日加一或单股压缩序列的下一行。预测只读当时可用输入，标签和未来可用性不进入推理。真实零修正实际计算m(b)，逐日检查平均秩完全不变，并精确复原r4完整后处理；浮点排名坍缩会报错，不回退到原分数来绕过校验。模型保存重载及前缀一致性检查已由每折证据和独立审计核验。", "",
        "目标u仅在价格有效且原Float64收益有限的池内排名，包含涨停；b始终在全价格有效池排名，不随未来标签缺失改变。机制MSE与原始IC使用同一有标签目标池，以零修正m(b)为参照。官方最终IC、过滤涨停与标签的收益Top、仅过滤涨停的换手Top具有不同口径；机制改善不等于官方改善，Jaccard换手也不是资金换手。", "",
        "## 门槛、审计与保留结果", "",
        "2022开发要求相对零修正MSE至少改善0.1%、原始IC差≥0；同时相对r4及pooled官方增分均≥0.001、最终IC差均≥−0.002。确认要求平均相对MSE改善≥0、最差年≥−0.001、平均原始IC差≥0；双基准平均增分≥0.0005、最差年≥−0.003、平均最终IC差≥−0.002。只有机制与官方点门槛均通过才运行20日配对块重采样，20,000次、种子2026，两个基准正增量份额均须≥80%。", ""]
    for name, stage in (("开发", dev), ("确认", conf)):
        if stage:
            r = stage["record"]
            noise = "未计算（点门槛失败）" if r["bootstrap"] is None else "；".join(
                f"{key} {value['bootstrap_share_positive']:.2%}" for key, value in r["bootstrap"].items())
            lines.append(f"- {name}：机制门槛 {r['mechanism_gate']['passed']}，官方门槛 {r['gate']['passed']}，完整门槛 {stage['passed']}；重采样正增量份额：{noise}；独立审计通过。")
    lines += ["", "审计通过只说明输入、实现、官方复算与记录一致，不代表候选合格。所有历史年份此前均已查看，本假设也受到此前研究结果影响；固定配置限制了本轮自由度，不能恢复盲测或消除跨轮选择偏差。80%重采样份额不是alpha有效概率。没有同容量直接目标对照，不能把变化完全归因于残差学习思想；本轮也不证明可执行净收益。", "",
        "证据：[研究依据](../r9_research_notes_20260926.md)、[冻结协议](protocol.json)、[开发记录](development.json)、[独立开发审计](independent_audit/audit_development.json)、[最终决策](decision.json)、[完整清单](result_manifest.json)。", "",
        "只读复核命令：`.venv\\Scripts\\python.exe -B -X utf8 experiments/finalize_r9.py verify`。核对全部文件与源码、JSON门槛及R8至r4证据链，不重训、不生成预测、不重算评分或重采样。即使全部历史门槛通过，也不自动更换正式模型、提交、报告或版本指针。完整重跑须另建目录，保留本轮结果。"]
    return "\n".join(lines) + "\n"


def write_new(path, value):
    with path.open("x", encoding="utf-8") as stream:
        stream.write(value) if isinstance(value, str) else json.dump(value, stream, ensure_ascii=False, indent=2, allow_nan=False)


def seal():
    require(OUT.is_dir() and not any((OUT / name).exists() for name in FINAL_FILES), "Final files missing prerequisites or already exist")
    inventory()
    state = evidence()
    decision, text = decision_record(state), report(state)
    write_new(OUT / "decision.json", decision)
    write_new(OUT / "结论.md", text)
    write_new(OUT / "verification.json", verification_record(state))
    manifest = {"status": "research_complete_no_promotion", "candidate_key": "oof_residual",
                "protocol_sha256": sha(OUT / "protocol.json"), "source_sha256": source_map(),
                "artifact_sha256": inventory()}
    write_new(OUT / "result_manifest.json", manifest)
    return {"status": "sealed", "audit_status": "passed", "terminal_reason": decision["terminal_reason"],
            "formal_promotion": False, "formal_release": "ensemble4_r4", "files_hashed": len(manifest["artifact_sha256"])}


def verify():
    manifest_path = OUT / "result_manifest.json"
    manifest = read(manifest_path)
    require(manifest["status"] == "research_complete_no_promotion" and manifest["candidate_key"] == "oof_residual", "Result is not sealed")
    require(manifest["source_sha256"] == source_map() and manifest["protocol_sha256"] == sha(OUT / "protocol.json"), "Source/protocol changed")
    verify_map(ROOT, manifest["artifact_sha256"])
    require(manifest["artifact_sha256"] == inventory(), "Manifest inventory changed or contains missing/additional files")
    state = evidence()
    decision = decision_record(state)
    require(read(OUT / "decision.json") == decision, "Decision differs from verified evidence")
    require(read(OUT / "verification.json") == verification_record(state), "Previous/final verification evidence differs")
    require((OUT / "结论.md").read_text(encoding="utf-8") == report(state), "Report differs from verified JSON results")
    return {"status": "passed", "audit_status": "passed", "status_meaning": "Integrity/audit agreement, not candidate qualification.",
            "development_gate_passed": decision["development_gate_passed"], "confirmation_gate_passed": decision["confirmation_gate_passed"],
            "historical_gates_passed": decision["historical_gates_passed"], "terminal_reason": decision["terminal_reason"],
            "formal_promotion": False, "formal_release": "ensemble4_r4", "active_release_unchanged": True,
            "previous_r8_verification": "passed", "files_hashed": len(manifest["artifact_sha256"]),
            "result_manifest_sha256": sha(manifest_path), "read_only": True,
            "training_prediction_scoring_or_resampling_performed": False}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("seal", "verify"))
    action = parser.parse_args().action
    try:
        print(json.dumps({"seal": seal, "verify": verify}[action](), ensure_ascii=False, indent=2, allow_nan=False))
    except Exception as error:
        print(json.dumps({"status": "failed", "error": f"{type(error).__name__}: {error}"}, ensure_ascii=False), file=sys.stderr)
        raise SystemExit(1)
