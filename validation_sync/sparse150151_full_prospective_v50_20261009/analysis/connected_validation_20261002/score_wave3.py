"""Wave 3: rebuild and score every candidate that survives only as per-seed RAW fold predictions.

The 2026-10-01 cleanup kept the raw per-seed caches for most wave arms but not their final scored
columns. Under 后续选模标准.md §3 every compliant candidate must be ranked by the same connected
2020-2024 official composite, so each family is rebuilt with the frozen wave-14 rule - equal-weight
per-day cross-sectional rank average, then the released stack (alpha 0.9, bonus 0.3, restore_lower,
top_current_weight 1.0, per-fold pooled auxiliary at top_only 0.25) - and scored identically.

Arms are auto-discovered rather than hard-coded, and each one records the exact seed set and file
paths it was built from so the rebuild is auditable. A family is scored only if it has the same seed
set in all five years; anything short is reported as unscoreable, never padded.
"""
from __future__ import annotations

import json
import re
import sys
import time
from collections import defaultdict
from pathlib import Path

import numpy as np
import polars as pl

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(HERE))
import connected_scorer as cs  # noqa: E402
from src.scoring import Panel  # noqa: E402
from experiments.cached_recheck import make_prediction  # noqa: E402

ARCHIVE = ROOT.parent / "赛题五_历史归档_20261001"
CLEANUP = ROOT.parent / "赛题五_清理备份_20261001"
OLDER = ROOT.parent / "赛题五_清理备份_20260926_003839"
R4 = ARCHIVE / "experiments/revalidation_20260926/validation"
TREES = [CLEANUP, ARCHIVE, OLDER]
YEARS = cs.YEARS
KEYS = cs.KEYS
SEED_RE = re.compile(r"^(?P<stem>.+?)_seed(?P<seed>\d+)_(?P<year>20\d{2})\.parquet$")
SINGLE_RE = re.compile(r"^(?P<name>.+?)_(?P<year>20\d{2})\.parquet$")
STACK = {"mode": "top_only", "weight": 0.25}


def load_raw(path: Path, year: int, reference: pl.DataFrame) -> np.ndarray:
    df = pl.read_parquet(path)
    column = "pred_raw" if "pred_raw" in df.columns else (
        "pred" if "pred" in df.columns else None)
    if column is None:
        raise AssertionError(f"{path.name}: no prediction column")
    df = df.sort("trade_date", "ts_code")
    if not df.select(KEYS).equals(reference.select(KEYS)):
        raise AssertionError(f"{path.name}: keys do not match the fold frame")
    return df[column].to_numpy().astype(np.float64)


def discover():
    """Group surviving raw caches into (family -> year -> {seed: path}) and find single-member arms."""
    families = defaultdict(lambda: defaultdict(dict))
    singles = defaultdict(dict)
    seen = set()
    for tree in TREES:
        for path in sorted(tree.rglob("*.parquet")):
            name = path.name
            match = SEED_RE.match(name)
            if match and "raw" in name.lower():
                key = (match["stem"], path.parent)
                families[key][int(match["year"])][int(match["seed"])] = path
                seen.add(path)
                continue
            match = SINGLE_RE.match(name)
            if match and path.parent.name == "final_sweep_eval":
                try:
                    columns = pl.read_parquet_schema(path)
                except Exception:
                    continue
                if "pred_raw" in columns:
                    singles[(match["name"], path.parent)][int(match["year"])] = path
                    seen.add(path)
    return families, singles


def stack(frame: pl.DataFrame, raw: np.ndarray) -> np.ndarray:
    panel = Panel.from_frame(frame.with_columns(pl.Series("pred_raw", raw)))
    return make_prediction(panel, frame["aux_raw"].to_numpy().astype(np.float64),
                           STACK["mode"], STACK["weight"])


def main() -> None:
    frame_cache = {}
    for year in YEARS:
        frame_cache[year] = pl.read_parquet(
            R4 / f"predictions_ensemble4_{year}.parquet").sort("trade_date", "ts_code")
    combined = cs.combined_frame()
    rank_average_n = None
    sys.path.insert(0, str(ROOT / "analysis"))
    from analysis.topset_hybrid_20261002 import fold_validation as fv
    rank_average_n = fv.load_rank_average_n()

    families, singles = discover()
    cs.log(f"discovered {len(families)} per-seed families and {len(singles)} single-member arms")

    results, unscoreable = {}, {}
    todo = []
    for (stem, parent), by_year in sorted(families.items()):
        label = f"{stem}"
        if not all(y in by_year for y in YEARS):
            unscoreable[label] = {"reason": "missing years", "missing": [y for y in YEARS if y not in by_year],
                                  "source": str(parent)}
            continue
        seed_sets = {y: set(by_year[y]) for y in YEARS}
        common = set.intersection(*seed_sets.values())
        if not common:
            unscoreable[label] = {"reason": "no seed present in all five years",
                                  "seed_sets": {str(y): sorted(s) for y, s in seed_sets.items()},
                                  "source": str(parent)}
            continue
        todo.append(("seedavg", label, parent, sorted(common), by_year))
    for (name, parent), by_year in sorted(singles.items()):
        if not all(y in by_year for y in YEARS):
            unscoreable[name] = {"reason": "missing years", "missing": [y for y in YEARS if y not in by_year],
                                 "source": str(parent)}
            continue
        todo.append(("single", name, parent, None, by_year))

    cs.log(f"{len(todo)} families are complete over all five years")
    for kind, label, parent, seeds, by_year in todo:
        key = f"{label}__{parent.name}"
        try:
            preds = {}
            for year in YEARS:
                frame = frame_cache[year]
                if kind == "seedavg":
                    raws = [load_raw(by_year[year][s], year, frame) for s in seeds]
                    days = frame["trade_date"].n_unique()
                    codes = len(frame) // days
                    averaged = rank_average_n(raws, frame["price_valid"].to_numpy(), codes)
                else:
                    averaged = load_raw(by_year[year], year, frame)
                preds[year] = stack(frame, averaged)
            results[key] = cs.score_arm_dict(combined, preds, key)
            results[key]["rebuilt_from"] = {"kind": kind, "source_directory": str(parent),
                                            "seeds": seeds, "stack": STACK,
                                            "files": {str(y): str(by_year[y] if kind == "single"
                                                                  else sorted(by_year[y].items())[0][1])
                                                      for y in YEARS}}
        except Exception as error:
            unscoreable[key] = {"reason": f"{type(error).__name__}: {error}", "source": str(parent)}
            cs.log(f"{key}: FAILED - {type(error).__name__}: {error}")

    prior = json.loads((HERE / "connected_results_all.json").read_text(encoding="utf-8"))
    merged = dict(prior["results"])
    merged.update(results)
    all_unscoreable = dict(prior.get("unscoreable", {}))
    all_unscoreable.update(unscoreable)
    ranked = sorted(merged.items(), key=lambda kv: -kv[1]["connected_final_score"])

    payload = {
        "status": "complete", "completed_at_local": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "caliber": prior["caliber"], "standard": prior["standard"],
        "no_test_period_data_read": True,
        "frame": prior["frame"], "turnover_accounting": prior["turnover_accounting"],
        "wave3_rebuild_rule": "equal-weight per-day cross-sectional rank average over the surviving "
                              "seed set, then the released stack (alpha 0.9, bonus 0.3, "
                              "restore_lower, top_current_weight 1.0, per-fold pooled auxiliary at "
                              "top_only 0.25) - the frozen wave-14 combination, imported not retyped",
        "results": merged, "unscoreable": all_unscoreable,
        "ranking_by_connected_score": [
            {"rank": i + 1, "name": name, "connected_final_score": r["connected_final_score"],
             "five_year_mean_diagnostic": r["five_year_equal_weight_mean_diagnostic_only"],
             "ic": r["connected_metrics"]["ic_mean"],
             "annual_excess": r["connected_metrics"]["annual_excess"],
             "turnover": r["connected_metrics"]["mean_turnover"]}
            for i, (name, r) in enumerate(ranked)],
    }
    (HERE / "connected_results_all.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"\n| rank | candidate | CONNECTED | IC | ann.excess | turnover | 5y mean (diag) |")
    print("|---|---|---|---|---|---|---|")
    for i, (name, r) in enumerate(ranked):
        m = r["connected_metrics"]
        print(f"| {i+1} | {name} | **{r['connected_final_score']:.9f}** | {m['ic_mean']:.6f} | "
              f"{m['annual_excess']:.6f} | {m['mean_turnover']:.6f} | "
              f"{r['five_year_equal_weight_mean_diagnostic_only']:.9f} |")
    print(f"\n{len(all_unscoreable)} candidates unscoreable from surviving artifacts:")
    for name, info in sorted(all_unscoreable.items()):
        print(f"  {name}: {info.get('reason')} {info.get('missing', '')}")


if __name__ == "__main__":
    main()
