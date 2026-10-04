"""Finalize verified artifacts, preserve the old pointer and activate the new package."""
from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo
import hashlib
import json
import shutil
from zipfile import ZipFile, ZIP_DEFLATED

ROOT = Path(__file__).resolve().parents[1]
ARCHIVE = ROOT.parent / "赛题五_历史归档_20261001"
OUT = ROOT / "deliveries/connected_topk0175_20261003"
BUNDLE = ROOT / "delivery_day_connected_20261003"


def sha(path):
    h = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for chunk in iter(lambda: stream.read(8 * 1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def read(path):
    return json.loads(Path(path).read_text(encoding="utf-8-sig"))


def dump(path, value):
    Path(path).write_text(json.dumps(value, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")


def main():
    for name in ("fold_verification.json", "train_test.json", "submission_checks.json", "verification.json"):
        assert read(OUT / name)["status"] == "passed", name
    audit = read(OUT / "report_audit.json")
    assert audit["status"] == "passed" and audit["visual_review"]["all_final_pages_checked"]
    assert sha(OUT / "量价分工集成股票收益预测分析报告.docx") == audit["docx_sha256"]
    assert sha(OUT / "量价分工集成股票收益预测分析报告.pdf") == audit["renderers"]["LibreOffice"]["pdf_sha256"]
    selection = read(OUT / "selection.json")
    check = read(OUT / "submission_checks.json")
    assert sha(OUT / "submission.csv") == check["csv_sha256"]
    protocol = read(ARCHIVE / "releases/pooled_rms25/protocol.json")
    assert all(sha(ARCHIVE / path) == digest for path, digest in protocol["preservation"]["prior_sha256"].items())
    source_names = ["analysis/complete_connected_delivery.py", "analysis/verify_connected_delivery.py",
                    "analysis/build_connected_report.py", "analysis/check_connected_report.py",
                    "analysis/finalize_connected_delivery.py"]
    snap = OUT / "source_snapshot"
    snap.mkdir(exist_ok=True)
    source_hashes = {}
    for name in source_names:
        source = ROOT / name
        dest = snap / source.name
        if dest.exists():
            assert sha(dest) == sha(source)
        else:
            shutil.copyfile(source, dest)
        source_hashes[name] = sha(source)
    files = {p.relative_to(OUT).as_posix(): {"sha256": sha(p), "bytes": p.stat().st_size}
             for p in sorted(OUT.rglob("*")) if p.is_file() and "qa" not in p.relative_to(OUT).parts
             and p.name not in ("delivery_manifest.json",)}
    manifest = {"status": "passed", "delivery_id": "connected_topk0175_20261003",
                "completed_at_local": datetime.now(ZoneInfo("Asia/Taipei")).isoformat(timespec="seconds"),
                "scheme": selection["scheme"], "validation_score": selection["winner"]["connected_final_score"],
                "retrospective_score": read(OUT / "retrospective.json")["metrics"]["final_score"],
                "test_highest_recorded": {"scheme": "wave13 W5a-only ordering", "score": 0.417099224,
                                          "scope": "existing official written-CSV scoring records; retrospective only"},
                "artifacts": files, "source_sha256": source_hashes,
                "source_snapshot_note": "Audit snapshots; run scripts from the project root with the local frozen experiment caches.",
                "submission_verification": "saved model raw predictions bit-identical; label-free pipeline replay byte-identical",
                "report": {"total_pages": 10, "body_pages": 8, "font": "宋体10.5pt", "line_spacing": 1.5,
                           "pdf_measured_spacing_pt": 22.2, "word_measured_spacing_pt": 20.4},
                "preserved_historical_files": 365, "official_preservation_check_files": 369,
                "platform_upload_performed": False}
    manifest_path = OUT / "delivery_manifest.json"
    assert not manifest_path.exists(), "Delivery is already finalized; do not rewrite it"
    dump(manifest_path, manifest)
    BUNDLE.mkdir(exist_ok=True)
    names = {"submission.csv": "submission.csv", "report_to_upload.docx": "量价分工集成股票收益预测分析报告.docx",
             "report_to_upload.pdf": "量价分工集成股票收益预测分析报告.pdf"}
    hashes = {}
    for target, source in names.items():
        dest = BUNDLE / target
        assert not dest.exists()
        shutil.copyfile(OUT / source, dest)
        assert sha(dest) == sha(OUT / source)
        hashes[target] = sha(dest)
    previous = ARCHIVE / "active_release.json"
    backup = BUNDLE / "previous_active_release.json"
    shutil.copyfile(previous, backup)
    assert sha(previous) == sha(backup)
    dump(BUNDLE / "upload_manifest.json", {"status": "passed", "delivery": str(OUT), "sha256": hashes,
          "previous_active_release_sha256": sha(backup), "submission_checks": check,
          "model_selected_by": "training-only connected validation highest official score",
          "platform_upload_performed": False})
    (BUNDLE / "checklist.md").write_text(
        "# 提交件核对\n\n"
        "当前方案为训练期连接验证选中的Top-K17.5%完整方案，验证0.445916，回顾0.414869。\n\n"
        "上传前只核对既有文件，不重新训练或重新导出。\n\n"
        "1. 使用本目录submission.csv，字段ts_code、trade_date、pred，共1,599,600行。\n"
        "2. 使用report_to_upload.pdf，正文8页；Word版为可编辑备份。\n"
        "3. 使用Get-FileHash -Algorithm SHA256核对upload_manifest.json中的三个哈希。\n"
        "4. 平台要求重命名PDF时只改文件名，保持内容与哈希。\n"
        "5. 测试回顾最佳的波13方案为0.417099，仅作披露，不用于反向改选。\n\n"
        "原版本指针已备份为previous_active_release.json，旧交付件仍保留。\n", encoding="utf-8")
    zip_path = BUNDLE / "赛题五提交包_连接验证选模_20261003.zip"
    with ZipFile(zip_path, "x", compression=ZIP_DEFLATED, compresslevel=6) as archive:
        for name in [*names, "upload_manifest.json", "checklist.md"]:
            archive.write(BUNDLE / name, arcname=name)
    pointer = {"status": "active", "artifact_kind": "local_verified_delivery_package",
               "release_id": manifest["delivery_id"], "model_name": "Top-K17.5%共识成员 × W5a与slow16排序融合 × 留存约束 × 训练期单调收益映射",
               "selected_by": "后续选模标准.md training-period connected official argmax",
               "authorization": "查看新尝试的模型，完成未完成的任务",
               "delivery_directory": str(OUT), "manifest": str(manifest_path), "manifest_sha256": sha(manifest_path),
               "submission": str(OUT / "submission.csv"), "submission_sha256": check["csv_sha256"],
               "report": str(OUT / names["report_to_upload.docx"]), "report_pdf": str(OUT / names["report_to_upload.pdf"]),
               "upload_bundle": str(BUNDLE), "upload_zip": str(zip_path), "previous_pointer": str(backup),
               "validation_score": manifest["validation_score"], "retrospective_score": manifest["retrospective_score"],
               "platform_upload_performed": False}
    dump(ROOT / "active_release.json", pointer)
    dump(previous, pointer)
    summary = {k: v for k, v in manifest.items() if k not in ("artifacts", "source_sha256")}
    summary["submission_sha256"] = check["csv_sha256"]
    dump(ROOT / "results/connected_delivery_20261003.json", summary)
    dump(ROOT / "results/connected_all_model_ranking_20261003.json", {"scored_records": len(selection["ranking"]),
         "repeated_candidates_included": True, "selection_rule": selection["selection_rule"], "ranking": selection["ranking"]})
    assert read(ROOT / "active_release.json") == read(previous)
    print(f"Finalized {OUT}; upload bundle {BUNDLE}; both pointers now agree")


if __name__ == "__main__":
    main()
