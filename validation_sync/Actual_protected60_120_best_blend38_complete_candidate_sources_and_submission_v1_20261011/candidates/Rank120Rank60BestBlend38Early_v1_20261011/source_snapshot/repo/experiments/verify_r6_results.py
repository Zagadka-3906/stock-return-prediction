"""Read-only hashes and decision-chain verification for the sealed r6 batch.

Run after finalize_r6.py. No training, model inference, scoring, resampling,
artifact writes, or bytecode writes are performed by this entry point.
"""
from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path
import sys

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
OUT = ROOT / "experiments/r6_results_20260926"
TRANSFORMER = ROOT / "experiments/r6_transformer_20260926"
CPU = {"value5": ROOT / "experiments/r6_value5_20260926",
       "topk": ROOT / "experiments/r6_topk_20260926"}
CROSS = ROOT / "experiments/r6_cross_audit_20260926"


def read(path):
    return json.loads(Path(path).read_text(encoding="utf-8-sig"))


def sha(path):
    with Path(path).open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def checked_path(base, relative):
    path = (base / relative).resolve()
    require(path.is_relative_to(base.resolve()) and path.is_file(), f"Invalid artifact path: {relative}")
    return path


def verify_map(base, mapping):
    require(isinstance(mapping, dict) and bool(mapping), "Missing or empty hash map")
    for relative, digest in mapping.items():
        require(sha(checked_path(base, relative)) == digest, f"Artifact changed: {relative}")


def close_record(actual, expected, label):
    """Compare already-recorded metrics without recomputing historical scores."""
    if isinstance(expected, dict):
        require(isinstance(actual, dict) and actual.keys() == expected.keys(), f"Keys differ: {label}")
        for key in expected:
            close_record(actual[key], expected[key], f"{label}/{key}")
    elif isinstance(expected, list):
        require(isinstance(actual, list) and len(actual) == len(expected), f"Length differs: {label}")
        for index, value in enumerate(expected):
            close_record(actual[index], value, f"{label}/{index}")
    elif isinstance(expected, (float, int)) and not isinstance(expected, bool):
        require(not isinstance(actual, bool) and isinstance(actual, (float, int))
                and math.isfinite(actual) and math.isfinite(expected)
                and abs(actual - expected) <= 1e-12, f"Numeric value differs: {label}")
    else:
        require(actual == expected, f"Value differs: {label}")


def transformer_audit(stage, aggregate, gate_passed):
    folder = TRANSFORMER / "independent_audit" / stage
    audit = read(folder / "score_audit.json")
    require(audit["status"] == "passed", f"Transformer {stage} audit failed")
    require(audit["stage"] == stage and audit["primary_candidate"] == "feature_identity", "Wrong audited candidate/stage")
    require(audit["stage_gate_passed"] == gate_passed, "Audit pass was confused with candidate gate")
    for field, path in (("stage_record", TRANSFORMER / f"{stage}.json"),
                        ("protocol", TRANSFORMER / "protocol.json"),
                        ("source", ROOT / "experiments/r6_transformer_audit.py"),
                        ("original_evaluator", ROOT / "evaluate.py"),
                        ("reused_r5_audit", ROOT / "experiments/audit_r5_candidate.py")):
        require(audit[field + "_sha256"] == sha(path), f"Transformer audit chain differs: {field}")
    verify_map(folder, audit["artifacts_sha256"])
    close_record(audit["aggregate"], aggregate, f"Transformer {stage} aggregate")
    for year in audit["completed_years"]:
        fold = read(TRANSFORMER / f"fold_{year}.json")
        for name, metrics_by_year in audit["historical_metrics"].items():
            metrics = fold["candidates"][name]["metrics"] if name in fold["candidates"] else fold["references"][name]
            close_record(metrics_by_year[str(year)], metrics, f"audited metrics/{name}/{year}")
        for name, metrics_by_year in audit["raw_metrics"].items():
            close_record(metrics_by_year[str(year)], fold["candidates"][name]["raw_metrics"], f"audited raw/{name}/{year}")
    return audit


def verify_transformer():
    # These helpers only read frozen files and rederive gates from stored metrics.
    from experiments.r6_transformer_audit import (
        _frozen_development, _checked_folds, point_gate, CONFIRMATION, PRIMARY, REFERENCE_NAMES)
    manifest = read(TRANSFORMER / "result_manifest.json")
    require(manifest["status"] == "complete_research_no_promotion", "Transformer not terminal")
    verify_map(ROOT, manifest["artifact_sha256"])
    require(manifest["source_sha256"] == sha(ROOT / "experiments/r6_transformer.py"), "Transformer source changed")
    protocol = read(TRANSFORMER / "protocol.json")
    verify_map(ROOT, protocol["input_sha256"])
    development, aggregate, mechanism = _frozen_development()
    audit = transformer_audit("development", aggregate, development["development_gate_passed"])
    require(audit["completed_years"] == development["completed_years"], "Audited development years differ")
    close_record(audit["mechanism_gate"], mechanism, "audited mechanism")
    decision = read(TRANSFORMER / "decision.json")
    require(decision["status"] == "complete_research_no_promotion"
            and decision["formal_release_retained"] == "ensemble4_r4"
            and decision["independent_audit_passed"] is True, "Invalid Transformer research decision")
    for field in ("completed_years", "early_stop_reason", "development_gate_passed"):
        require(decision[field] == development[field], f"Decision differs: {field}")
    close_record(decision["aggregate"], aggregate, "decision aggregate")
    close_record(decision["mechanism_gate"], mechanism, "decision mechanism")
    for field, path in (("protocol", TRANSFORMER / "protocol.json"),
                        ("development", TRANSFORMER / "development.json"),
                        ("independent_audit", TRANSFORMER / "independent_audit/development/score_audit.json")):
        require(decision[field + "_sha256"] == sha(path), f"Decision hash differs: {field}")
    confirmation_passed = None
    if development["development_gate_passed"]:
        confirmation = read(TRANSFORMER / "confirmation.json")
        require(confirmation["development_sha256"] == sha(TRANSFORMER / "development.json"), "Confirmation changed development")
        require(confirmation["protocol_sha256"] == sha(TRANSFORMER / "protocol.json"), "Confirmation used another protocol")
        folds = _checked_folds(confirmation, CONFIRMATION, (PRIMARY,))
        metrics = {name: {str(year): folds[year]["candidates"][PRIMARY]["metrics"] if name == PRIMARY
                         else folds[year]["references"][name] for year in CONFIRMATION}
                   for name in (PRIMARY, *REFERENCE_NAMES)}
        confirmed_aggregate = point_gate(metrics, "confirmation", CONFIRMATION)
        # The independent gate adds a diagnostic 'partial' field; the runner
        # aggregate has no such field, even on a complete confirmation period.
        close_record(confirmation["aggregate"], {k: v for k, v in confirmed_aggregate.items() if k != "partial"}, "confirmation aggregate")
        require(set(confirmation["bootstrap"]) == set(REFERENCE_NAMES), "Confirmation missing a reference")
        threshold = protocol["gates"]["bootstrap"]["positive_share"]
        noise = all(item["bootstrap_share_positive"] >= threshold for item in confirmation["bootstrap"].values())
        confirmation_passed = bool(confirmed_aggregate["passed"] and noise)
        require(confirmation["official_and_noise_gate_passed"] == confirmation_passed, "Confirmation gate differs")
        confirmed_audit = transformer_audit("confirmation", confirmed_aggregate, confirmation_passed)
        close_record(confirmed_audit["paired_uncertainty"], confirmation["bootstrap"], "audited bootstrap")
    else:
        require(not (TRANSFORMER / "confirmation.json").exists(), "Forbidden confirmation after failure")
        require(not (TRANSFORMER / "independent_audit/confirmation").exists(), "Forbidden confirmation audit")
    return {"audit_status": "passed", "completed_years": development["completed_years"],
            "development_gate_passed": development["development_gate_passed"],
            "confirmation_gate_passed": confirmation_passed, "formal_promotion": False}


def verify_cpu_chain():
    cross = read(CROSS / "summary.json")
    require(cross["status"] == "passed" and cross["original_cpu_unit_files_unchanged"] is True
            and cross["new_training_or_candidates"] is False, "CPU cross-audit not complete")
    require(sha(checked_path(ROOT, cross["source_path"])) == cross["source_sha256"], "Cross-audit source changed")
    evidence_path = checked_path(ROOT, cross["evidence_manifest_path"])
    require(sha(evidence_path) == cross["evidence_manifest_sha256"], "Cross evidence manifest changed")
    evidence = read(evidence_path)
    verify_map(ROOT, evidence["artifact_sha256"])
    require(evidence["unit_gates_passed"] == cross["candidate_gates_passed"], "Cross manifest gate differs")
    statuses = {}
    for name, folder in CPU.items():
        development = read(folder / "development.json")
        verify_map(ROOT, read(folder / "protocol.json")["input_sha256"])
        audit_path = CROSS / f"{name}_audit.json"
        require(sha(audit_path) == cross["audit_sha256"][audit_path.name], f"Changed CPU audit: {name}")
        audit = read(audit_path)
        require(audit["status"] == "passed" and audit["source_sha256"] == cross["source_sha256"], "CPU audit source/status differs")
        verify_map(folder, audit["original_unit_snapshot_sha256"])
        require(audit["gate_passed"] == development["gate"]["passed"] == cross["candidate_gates_passed"][name], "CPU gate chain differs")
        if name == "value5":
            close_record(audit["conditions"], development["gate"]["conditions"], "value5 conditions")
            close_record(audit["comparison"], development["gate"]["comparison"], "value5 comparison")
        else:
            from experiments.r6_topk import gate
            folds = [read(folder / f"fold_{year}.json") for year in (2020, 2021, 2022)]
            close_record(gate(folds, "development"), development["gate"], "TopK development gate")
            verify_map(folder, read(folder / "final_manifest.json")["artifact_sha256"])
            require(read(folder / "final_audit.json")["status"] == "passed", "TopK model reconstruction audit failed")
        passed = development["gate"]["passed"]
        require((folder / "confirmation.json").is_file() == passed, f"CPU confirmation terminal state differs: {name}")
        statuses[name] = {"audit_status": "passed", "development_gate_passed": passed, "formal_promotion": False}
    # transformer_audit_pending in the cross snapshot is historical, CPU-only.
    # Transformer completion is separately verified above, without editing it.
    return statuses


def verify():
    manifest_path = OUT / "result_manifest.json"
    manifest = read(manifest_path)
    require(manifest["status"] == "research_complete_no_promotion", "Research batch not sealed")
    verify_map(ROOT, manifest["artifact_sha256"])
    own_path = Path(__file__).relative_to(ROOT).as_posix()
    require(manifest["artifact_sha256"].get(own_path) == sha(Path(__file__)), "Final manifest must include this verifier")
    expected = {p.relative_to(ROOT).as_posix() for folder in (TRANSFORMER, *CPU.values(), CROSS, OUT)
                for p in folder.rglob("*") if p.is_file() and "__pycache__" not in p.parts and p != manifest_path}
    require(expected <= set(manifest["artifact_sha256"]), "Final manifest omits an artifact")
    transformer = verify_transformer()
    cpu = verify_cpu_chain()
    from experiments.verify_r5_results import verify as verify_previous
    previous = verify_previous()
    require(previous["status"] == "passed" and previous["active_release_unchanged"], "Prior r5/r4 integrity failed")
    verification = read(OUT / "verification.json")
    require(verification["status"] == "passed" and verification["formal_release"] == "ensemble4_r4", "Final release verification differs")
    close_record(verification["prior_release_verification"], previous, "previous research verification")
    require(verification["independent_cpu_audit_sha256"] == sha(CROSS / "summary.json"), "Final verification changed CPU audit")
    require(verification["active_release_sha256"] == sha(ROOT / "active_release.json"), "Active release changed")
    return {"status": "passed", "status_meaning": "Integrity and audit chains passed; candidate gates are reported separately. No candidate promotion.",
            "candidate_results": {"transformer": transformer, **cpu}, "formal_release": "ensemble4_r4",
            "active_release_unchanged": True, "previous_r5_verification": "passed",
            "direct_artifact_hashes_checked": len(manifest["artifact_sha256"]),
            "result_manifest_sha256": sha(manifest_path), "read_only": True,
            "training_inference_scoring_or_resampling_performed": False}


if __name__ == "__main__":
    try:
        print(json.dumps(verify(), ensure_ascii=False, indent=2))
    except Exception as error:
        print(json.dumps({"status": "failed", "error": f"{type(error).__name__}: {error}"}, ensure_ascii=False), file=sys.stderr)
        raise SystemExit(1)
