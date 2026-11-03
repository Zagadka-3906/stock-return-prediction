"""Check maintained Markdown links, anchors, SVGs and recorded metric consistency.

Uses the Git tree to resolve archived paths in sparse checkouts. No model runs.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import unicodedata
import xml.etree.ElementTree as ET
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]


def documents() -> list[Path]:
    names = ["README.md", "ABOUT.md", "CONTRIBUTING.md", "后续选模标准.md",
             "analysis/README.md", "experiments/README.md", "results/README.md", "validation_sync/README.md"]
    return sorted(set([ROOT / p for p in names] + list((ROOT / "docs").glob("*.md"))
                      + list((ROOT / "最终交付模型").glob("*.md")) + list((ROOT / "全程排名").glob("*.md"))))


def no_fences(value: str) -> str:
    return re.sub(r"^```[^\n]*\n.*?^```\s*$", "", value, flags=re.M | re.S)


def anchors(value: str) -> set[str]:
    found = set(re.findall(r'\bid=["\']([^"\']+)', value))
    counts: dict[str, int] = {}
    for heading in re.findall(r"^#{1,6}\s+(.+?)\s*#*\s*$", no_fences(value), re.M):
        heading = re.sub(r"<[^>]+>", "", heading).replace("`", "").replace("*", "").lower()
        slug = "".join(c for c in heading if c in " -_" or unicodedata.category(c)[0] in "LN").replace(" ", "-")
        count = counts.get(slug, 0)
        counts[slug] = count + 1
        found.add(slug if count == 0 else f"{slug}-{count}")
    return found


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--reference-repo", type=Path, help="Git checkout supplying the archived path index")
    args = parser.parse_args()
    repo = args.reference_repo or ROOT
    proc = subprocess.run(["git", "-C", str(repo), "ls-tree", "-r", "--name-only", "-z", "HEAD"], capture_output=True)
    tracked = set(proc.stdout.decode("utf-8").split("\0")) if proc.returncode == 0 else set()
    errors: list[str] = []
    checked = 0
    for path in documents():
        if not path.is_file():
            errors.append(f"Missing maintained document: {path}")
            continue
        body = path.read_text(encoding="utf-8")
        if "\ufffd" in body:
            errors.append(f"Replacement character: {path}")
        text = no_fences(body)
        refs = re.findall(r'\]\(([^\s)]+)(?:\s+"[^"\n]*")?\)', text)
        refs += re.findall(r'\b(?:href|src|srcset)=["\']([^"\']+)', text)
        for ref in refs:
            if ref.startswith("<") and ref.endswith(">"):
                ref = ref[1:-1]
            url = urlsplit(ref)
            if url.scheme or url.netloc:
                continue
            checked += 1
            target = (path.parent / unquote(url.path)).resolve() if url.path else path
            try:
                name = target.relative_to(ROOT).as_posix()
            except ValueError:
                errors.append(f"Outside repository: {path.name}: {ref}")
                continue
            exists = target.exists() or name in tracked or any(p.startswith(name.rstrip("/") + "/") for p in tracked)
            if not exists:
                errors.append(f"Missing link: {path.relative_to(ROOT)} -> {ref}")
            if url.fragment and target.is_file() and target.suffix == ".md":
                fragment = unquote(url.fragment)
                if fragment not in anchors(target.read_text(encoding="utf-8")):
                    errors.append(f"Missing anchor: {path.relative_to(ROOT)} -> {ref}")
    for path in (ROOT / "docs/assets").glob("*.svg"):
        try:
            ET.parse(path)
        except ET.ParseError as exc:
            errors.append(f"SVG XML: {path.name}: {exc}")
    snapshot = json.loads((ROOT / "docs/latest_results.json").read_text(encoding="utf-8"))
    ensemble = snapshot["latest_packaged_candidate"]
    metrics = ensemble["metrics"]
    computed = .4 * metrics["ic_mean"] + .3 * metrics["annual_excess"] + .3 * (1 - metrics["mean_turnover"])
    if abs(computed - metrics["final_score"]) > 1e-14:
        errors.append("Composite score does not match its recorded components")
    if ensemble["submission_days"] * ensemble["submission_codes"] != ensemble["submission_rows"]:
        errors.append("Recorded prediction dimensions are inconsistent")
    baseline = snapshot["fixed_direct_return_baseline143"]
    source = ROOT / baseline["source_record"]
    if hashlib.sha256(source.read_bytes()).hexdigest() != baseline["source_record_sha256"]:
        errors.append("Baseline source hash differs")
    if baseline["official_TRAIN_metrics"] != json.loads(source.read_text(encoding="utf-8"))["official_TRAIN_metrics"]:
        errors.append("Baseline metrics differ from the original result record")
    original_manifest = ROOT / "docs/history/local-20261011/manifest.json"
    if original_manifest.exists():
        for entry in json.loads(original_manifest.read_text(encoding="utf-8"))["files"]:
            if hashlib.sha256((ROOT / entry["preserved_snapshot"]).read_bytes()).hexdigest() != entry["original_sha256"]:
                errors.append(f"Original document snapshot changed: {entry['original_path']}")
    if errors:
        print("\n".join(errors))
        raise SystemExit(1)
    print(f"PASS: {len(documents())} maintained Markdown files, {checked} local links, SVG XML, metrics and original-document hashes.")
    if not tracked:
        print("Git tree unavailable: only physically present link targets were checked.")


if __name__ == "__main__":
    main()
