"""Resolve removed exports across cleanup catalogs without changing frozen records."""
from __future__ import annotations

import argparse
import gzip
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def find_record(requested: str, catalogs: list[Path]) -> dict | None:
    """Catalog order determines precedence; callers put the newest first."""
    for catalog in catalogs:
        with gzip.open(catalog, "rt", encoding="utf-8") as stream:
            for line in stream:
                row = json.loads(line)
                if row["removed_path"] == requested:
                    return row
    return None


def resolve_record(record: dict, catalogs: list[Path]) -> dict:
    """Follow a retained copy that was itself removed in a later cleanup."""
    result = dict(record)
    target = record.get("retained_path")
    chain = [record["removed_path"]]
    seen = set(chain)
    while target:
        if target in seen:
            raise ValueError("Archive mapping cycle: " + " -> ".join(chain + [target]))
        seen.add(target)
        chain.append(target)
        next_record = find_record(target, catalogs)
        if next_record is None:
            break
        if (record.get("git_blob_oid") and next_record.get("git_blob_oid")
                and record["git_blob_oid"] != next_record["git_blob_oid"]):
            raise ValueError("Archive mapping changes Git blob identity: " + target)
        target = next_record.get("retained_path")
        if target is None:
            result["resolved_historical_url"] = next_record.get("historical_url")
    if len(chain) > 2 or result.get("retained_path") != target:
        result["original_retained_path"] = result.get("retained_path")
        result["retained_path"] = target
        result["retained_path_chain"] = chain
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description="查询历史归档路径及后续去重后的保留副本")
    parser.add_argument("path", help="原仓库相对路径，例如 validation_sync/round100/文件")
    parser.add_argument("--catalog", type=Path, action="append",
                        help="指定查询目录，可重复传入；默认按日期从新到旧查询全部清理目录")
    args = parser.parse_args()
    catalogs = args.catalog or sorted((ROOT / "validation_sync").glob("archive_index_*.jsonl.gz"), reverse=True)
    if not catalogs or any(not path.is_file() for path in catalogs):
        parser.error("缺少清理查询目录；请先检出 validation_sync/archive_index_*.jsonl.gz")
    requested = args.path.replace("\\", "/").removeprefix("./")
    try:
        record = find_record(requested, catalogs)
        if record is None:
            parser.exit(1, "未找到该路径的清理记录；文件可能仍保留或不在清理范围。\n")
        print(json.dumps(resolve_record(record, catalogs), ensure_ascii=False, indent=2))
    except ValueError as error:
        parser.exit(1, str(error) + "\n")


if __name__ == "__main__":
    main()
