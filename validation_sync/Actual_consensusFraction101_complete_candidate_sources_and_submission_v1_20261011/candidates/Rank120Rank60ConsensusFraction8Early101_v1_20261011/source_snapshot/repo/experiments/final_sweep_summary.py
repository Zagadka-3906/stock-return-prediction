"""Merge every frozen sweep suite into one candidate table.

Reads only recorded result files; it never scores anything. A candidate appears
with its per-year composite delta against the released baseline, the two-year
mean and maximin criteria its own protocol declared, and - where the suite
reached the third year - the one-shot 2024 confirmation delta.
"""
from __future__ import annotations

import json
import time

from run import ROOT
from experiments.bonus_extension import file_hash, release_scores

OUT = ROOT / "experiments" / "final_sweep_eval"
AUDIT_OUT = ROOT / "experiments" / "extended_audit_eval"
YEARS = ("2020", "2021", "2022", "2023", "2024")
GATED_YEARS = ("2022", "2023", "2024")
SUITES = [
    ("T1 post-processing", "development.json", None),
    ("T2 backbone retrain", "development_retrain.json", None),
    ("T2 extra learners", "development_extra.json", "confirmation_extra.json"),
    ("Wave-2 mechanisms", "development_wave2.json", "confirmation_wave2.json"),
    ("Wave-3 ensembles", "development_wave3.json", "confirmation_wave3.json"),
    ("Wave-5 sequence member", "development_wave5.json", "confirmation_wave5.json"),
    ("Wave-6 features", "development_wave6.json", "confirmation_wave6.json"),
]
AUDIT_SOURCES = [("extended audit", AUDIT_OUT / "audit_results.json"),
                 ("wave-5 audit", OUT / "audit_wave5.json"),
                 ("wave-6 audit", OUT / "audit_wave6.json")]


def load(name: str) -> dict | None:
    path = OUT / name
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else None


def audit_rows() -> dict:
    """Deltas on the never-gated years, keyed by candidate then year."""
    found = {}
    for _, path in AUDIT_SOURCES:
        if not path.exists():
            continue
        record = json.loads(path.read_text(encoding="utf-8"))
        years = record.get("years") or record.get("results", {}).get("years") or {}
        for year, entries in years.items():
            for key, entry in entries.items():
                if isinstance(entry, dict) and "delta_vs_released" in entry:
                    found.setdefault(key, {})[year] = entry["delta_vs_released"]
    return found


def wave4_rows() -> list[dict]:
    path = OUT / "development_wave4.json"
    if not path.exists():
        return []
    record = json.loads(path.read_text(encoding="utf-8"))
    selection = load("selection_wave4.json") or {}
    deltas = {year: item["score_delta"] for year, item in record.get("years", {}).items()}
    return [{
        "suite": "Wave-4 hyperparameters", "key": record.get("selected", "wave4_winner"),
        "primary": True, "deltas": deltas,
        "mean_delta": sum(deltas.values()) / len(deltas) if deltas else None,
        "minimax_delta": min(deltas.values()) if deltas else None,
        "ic_mean_2023": record.get("years", {}).get("2023", {}).get("ic_mean"),
        "turnover_2023": record.get("years", {}).get("2023", {}).get("mean_turnover"),
        "excess_2023": record.get("years", {}).get("2023", {}).get("annual_excess"),
        "passes_development_gate": bool(record.get("passes_development_gate")),
        "confirmed_year": "2024" in deltas,
        "passes_three_year_gate": (deltas["2024"] > 1e-12) if "2024" in deltas else None,
        "years_scored": sorted(deltas),
        "note": ("selected by maximin on the never-gated 2020+2021 "
                 f"(winner of {len(selection.get('results', {}))} configurations), then scored once"),
    }]


def rows() -> list[dict]:
    released = {str(k): float(v) for k, v in release_scores().items()}
    audit = audit_rows()
    merged = []
    for suite, dev_name, conf_name in SUITES:
        development = load(dev_name)
        if development is None:
            continue
        confirmation = load(conf_name) if conf_name else None
        for key, item in development["candidates"].items():
            deltas = {}
            for year in GATED_YEARS:
                metrics = item["years"].get(year)
                if metrics is not None:
                    deltas[year] = metrics["final_score"] - released[year]
            if confirmation and key in confirmation.get("three_year_summary", {}):
                deltas["2024"] = confirmation["three_year_summary"][key]["score_delta"]["2024"]
            deltas.update(audit.get(key, {}))
            merged.append(row_from(suite, key, item, deltas))
    merged.extend(wave4_rows())
    for entry in merged:
        entry["deltas"] = {y: entry["deltas"][y] for y in YEARS if y in entry["deltas"]}
        scored = entry["deltas"]
        entry["mean_delta"] = sum(scored.values()) / len(scored) if scored else None
        entry["minimax_delta"] = min(scored.values()) if scored else None
    return merged


def row_from(suite: str, key: str, item: dict, deltas: dict) -> dict:
    metrics_last = item["years"].get("2023") or item["years"].get("2022") or {}
    return {
        "suite": suite, "key": key,
        "primary": item.get("primary", key == "baseline_released"),
        "deltas": deltas,
        "mean_delta": None, "minimax_delta": None,
        "ic_mean_2023": metrics_last.get("ic_mean"),
        "turnover_2023": metrics_last.get("mean_turnover"),
        "excess_2023": metrics_last.get("annual_excess"),
        "passes_development_gate": bool(item.get("passes_development_gate")),
        "confirmed_year": "2024" in deltas,
        "passes_three_year_gate": (deltas["2024"] > 1e-12) if "2024" in deltas else None,
        "years_scored": sorted(deltas),
    }


def table() -> str:
    merged = rows()
    released = {str(k): float(v) for k, v in release_scores().items()}
    head = (f"{'suite':<24}{'candidate':<32}" + "".join(f"{y:>11}" for y in YEARS)
            + f"{'mean':>11}{'min':>11}  gate")
    lines = ["released composite (gated years): "
             + "  ".join(f"{y}={released[y]:.6f}" for y in GATED_YEARS),
             "2020/2021 are never-gated audit years, scored without the pooled blend",
             head, "-" * len(head)]
    for row in merged:
        cells = []
        for year in YEARS:
            value = row["deltas"].get(year)
            cells.append(f"{value:+.6f}" if value is not None else f"{'-':>10}")
        if row["key"] == "baseline_released":
            gate = "reference"
        elif row["passes_three_year_gate"] is None:
            gate = "dev FAIL" if not row["passes_development_gate"] else "dev pass, no 2024"
        elif row["passes_three_year_gate"]:
            gate = "3-YEAR PASS"
        else:
            gate = "2024 FAIL"
        lines.append(f"{row['suite']:<24}{row['key']:<32}"
                     f"{''.join(f'{c:>11}' for c in cells)}"
                     f"{row['mean_delta']:+11.6f}{row['minimax_delta']:+11.6f}  {gate}")
    return "\n".join(lines)


def main() -> None:
    merged = rows()
    sources = {}
    for _, dev_name, conf_name in SUITES:
        for name in (dev_name, conf_name):
            if name:
                path = OUT / name
                sources[name] = file_hash(path) if path.exists() else None
    for name in ("selection_wave4.json", "development_wave4.json", "significance.json",
                 "training_wave6.json"):
        path = OUT / name
        sources[name] = file_hash(path) if path.exists() else None
    for label, path in AUDIT_SOURCES:
        sources[path.name] = file_hash(path) if path.exists() else None
    payload = {"generated_at_local": time.strftime("%Y-%m-%dT%H:%M:%S"),
               "released_composite": {str(k): float(v) for k, v in release_scores().items()},
               "candidate_count": len(merged),
               "year_caliber": {"gated": list(GATED_YEARS),
                                "audit": ["2020", "2021"],
                                "audit_note": "scored without the pooled blend, identically for "
                                              "baseline and candidate"},
               "candidates": merged, "sources": sources}
    (OUT / "sweep_summary.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2),
                                            encoding="utf-8")
    print(table())
    passing = [r["key"] for r in merged if r["passes_three_year_gate"]]
    positive_everywhere = [r["key"] for r in merged
                           if len(r["deltas"]) == len(YEARS)
                           and all(v > 1e-12 for v in r["deltas"].values())]
    print(f"\n{len(merged)} candidates scored; three-year survivors: {passing}")
    print(f"positive in all five years: {positive_everywhere}")


if __name__ == "__main__":
    main()
