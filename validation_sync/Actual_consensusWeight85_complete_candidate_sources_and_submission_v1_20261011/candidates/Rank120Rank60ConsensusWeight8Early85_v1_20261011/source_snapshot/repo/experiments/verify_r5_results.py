"""Read-only integrity and decision checks for the completed r5 research batch."""
from __future__ import annotations

import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from experiments.optimize_r5 import OUT, read, sha, verify_protocol, validated_development, gate


def verify():
    manifest_path = OUT / "result_manifest.json"
    manifest = read(manifest_path)
    for relative, digest in manifest["artifact_sha256"].items():
        path = (ROOT / relative).resolve()
        assert path.is_relative_to(ROOT.resolve()) and path.is_file(), relative
        assert sha(path) == digest, f"Changed r5 artifact: {relative}"
    protocol = verify_protocol()
    development = validated_development()
    confirmation, decision = [read(OUT / f"{name}.json") for name in ("confirmation", "decision")]
    winner = development["winner"]
    assert decision["candidate_key"] == confirmation["winner"] == winner
    assert confirmation["development_sha256"] == sha(OUT / "development.json")
    assert set(confirmation["fold_sha256"]) == {f"fold_{y}.json" for y in (2023, 2024)}
    folds = []
    for year in (2023, 2024):
        path = OUT / f"fold_{year}.json"
        assert sha(path) == confirmation["fold_sha256"][path.name]
        fold = read(path)
        assert fold["candidate_keys"] == [winner] and set(fold["candidates"]) == {winner}
        for relative, digest in fold["artifact_sha256"].items():
            assert sha(OUT / relative) == digest
        folds.append(fold)
    assert gate(folds, winner, "confirmation") == confirmation["aggregate"]
    bootstrap_pass = all(v["bootstrap_share_positive"] >= protocol["gates"]["bootstrap"]["positive_share_min"]
                         for v in confirmation["bootstrap"].values())
    assert confirmation["official_and_noise_gate_passed"] == (confirmation["aggregate"]["passed"] and bootstrap_pass)
    audit_path = OUT / "independent_audit" / winner / "score_audit.json"
    audit = read(audit_path)
    assert audit["status"] == "passed" and audit["runner_expected_metrics_checked"]
    assert audit["confirmation_passed"] == confirmation["official_and_noise_gate_passed"] is False
    assert decision["status"] == "complete_not_promoted"
    assert decision["active_release_retained"] == "ensemble4_r4"
    assert sha(ROOT / "active_release.json") == decision["active_release_sha256"] == manifest["active_release_sha256"]
    for key, path in (("development", OUT / "development.json"), ("confirmation", OUT / "confirmation.json"),
                      ("independent_audit", audit_path), ("protocol", OUT / "protocol.json")):
        assert decision[key + "_sha256"] == sha(path)
    assert not (audit_path.parent / "execution/summary.json").exists()
    assert not (OUT / "submission.csv").exists()
    return {"status": "passed", "research_status": decision["status"], "candidate": winner,
            "direct_artifact_hashes_checked": len(manifest["artifact_sha256"]),
            "frozen_protocol_inputs_checked": len(protocol["input_sha256"]),
            "r4_integrity_verified": True, "development_choice_rederived": True,
            "only_selected_candidate_confirmed": True, "confirmation_gate_rederived": True,
            "failed_candidate_not_promoted": True, "active_release_unchanged": True,
            "result_manifest_sha256": sha(manifest_path)}


if __name__ == "__main__":
    print(json.dumps(verify(), ensure_ascii=False, indent=2))
