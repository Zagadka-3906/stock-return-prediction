"""Admissible-axis validation of the cross-model Top-set substitution hybrid.

Candidate (ONE fixed definition, no grid, no variants): each day's Top-decile MEMBERSHIP comes from
arm B (the Top-K return-weighted pairwise backbone) and the ORDERING everywhere comes from arm A
(peer67_slow16, the confirmed model). H = is_promoted * (span(pred_A)+1) + pred_A.

Motivation is structural, not empirical: the official composite is
0.4*RankIC + 0.3*annualized_top_decile_excess + 0.3*(1-Jaccard). Rank IC depends on the full
cross-section ordering; excess and turnover depend only on WHICH stocks land in the Top decile. The
two halves are separable, and the two arms are complementary - B has +0.034126 of annualized excess
over A but -0.020857 of Rank IC.

DISCLOSED PRIOR: a feasibility screen on the reconstructed test slice (screen_test_slice.json in
this directory) already returned H - A = +0.027741, CI [+0.005429, +0.058698]. That is
EVALUATION-SET evidence and may not select anything; it is recorded here so that the fold result
below cannot be mistaken for a blind test.

Stages: freeze -> prove -> run -> compare. `freeze` must complete before any hybrid fold score exists.
"""
from __future__ import annotations

import argparse
import ast
import gc
import hashlib
import json
import platform
import sys
import time
import traceback
from pathlib import Path

import numpy as np
import pandas as pd
import polars as pl

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT))
from src.scoring import Panel  # noqa: E402
from experiments.cached_recheck import make_prediction  # noqa: E402
from experiments.revalidate_fold_local import score_official  # noqa: E402
from analysis.official_score_contributions import (  # noqa: E402
    WEIGHTS, composite, metric_denominators, paired_difference,
)

ARCHIVE = ROOT.parent / "赛题五_历史归档_20261001"
CLEANUP = ROOT.parent / "赛题五_清理备份_20261001"
R4 = ARCHIVE / "experiments/revalidation_20260926/validation"
RAW16 = CLEANUP / "experiments/wave23_validation_20260928"
TOPK_OLD = ARCHIVE / "experiments/r6_topk_20260926"
TOPK_NEW = ROOT / "analysis/topk_training_validation_20261001"
W14 = ARCHIVE / "experiments/wave14_seed_average.py"
FEATURES = ROOT / "data/features.parquet"
KEYS = ["ts_code", "trade_date"]
YEARS = (2020, 2021, 2022, 2023, 2024)
POOL16 = tuple(range(2026, 2042))
# Frozen wave-24 reproduction targets for arm A (nine decimals, tolerance 2e-9).
EXPECTED_FULL16 = {2020: 0.432158406, 2021: 0.424889700, 2022: 0.444829865,
                   2023: 0.418670801, 2024: 0.420366222}
TOL16 = 2e-9
# Frozen Top-K fold scores for arm B (2020-2022 from 2026-09-26, 2023-2024 from 2026-10-01).
EXPECTED_TOPK = {2020: 0.40707290913686545, 2021: 0.4152844359357778, 2022: 0.42089053197633397,
                 2023: None, 2024: None}
def daily_full16(year: int) -> Path:
    """The frozen wave-24 per-day official terms for the confirmed arm; the cleanup split the tree."""
    for root in (CLEANUP, ARCHIVE):
        candidate = root / f"experiments/wave24_seed16_delivery_20260929/daily_full16_{year}.csv"
        if candidate.exists():
            return candidate
    raise SystemExit(f"missing frozen daily_full16_{year}.csv in either preserved tree")


def sha(path: Path) -> str:
    value = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for chunk in iter(lambda: stream.read(8 * 1024 * 1024), b""):
            value.update(chunk)
    return value.hexdigest()


def log(message: str) -> None:
    line = f"[{time.strftime('%H:%M:%S')}] {message}"
    print(line, flush=True)
    with (HERE / "run.log").open("a", encoding="utf-8") as stream:
        stream.write(line + "\n")


def write_new(path: Path, value) -> None:
    if path.exists():
        raise FileExistsError(f"refusing to overwrite existing evidence: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def topk_predictions(year: int) -> Path:
    """Arm B's frozen final fold prediction; 2022 exists in both trees and must agree."""
    new = TOPK_NEW / f"predictions_topk_return_backbone_{year}.parquet"
    old = TOPK_OLD / f"predictions_topk_return_backbone_{year}.parquet"
    if new.exists():
        return new
    if old.exists():
        return old
    raise SystemExit(f"no Top-K fold prediction for {year}")


def load_rank_average_n():
    """Exec the frozen wave-14 function verbatim - no import side effects, no transcription risk."""
    source = W14.read_text(encoding="utf-8")
    tree = ast.parse(source)
    node = next(n for n in tree.body
                if isinstance(n, ast.FunctionDef) and n.name == "rank_average_n")
    namespace = {"np": np}
    exec(compile(ast.Module(body=[node], type_ignores=[]), str(W14), "exec"), namespace)
    return namespace["rank_average_n"]


def fold_frame(year: int) -> pl.DataFrame:
    frame = pl.read_parquet(R4 / f"predictions_ensemble4_{year}.parquet").sort("trade_date", "ts_code")
    grid = (pl.scan_parquet(FEATURES)
            .filter(pl.col("is_train") & pl.col("trade_date").is_between(year * 10000 + 101,
                                                                        year * 10000 + 1231))
            .select(KEYS + ["price_valid"]).sort("trade_date", "ts_code").collect())
    if not grid.select(KEYS).equals(frame.select(KEYS)):
        raise AssertionError(f"{year}: reconstructed grid keys != the r4 fold frame keys")
    return frame.with_columns(grid["price_valid"].alias("grid_price_valid"))


def build_A(frame: pl.DataFrame, rank_average_n) -> np.ndarray:
    """Reconstruct the confirmed model's final fold prediction from the 80 surviving seed caches."""
    year = int(frame["trade_date"].min() // 10000)
    raws = []
    for seed in POOL16:
        path = RAW16 / f"raw_deployed67_slow_seed{seed}_{year}.parquet"
        if not path.exists():
            raise SystemExit(f"missing seed cache: {path.name}")
        raws.append(pl.read_parquet(path).sort("trade_date", "ts_code")["pred_raw"].to_numpy())
    days = frame["trade_date"].n_unique()
    codes = len(frame) // days
    assert len(frame) == days * codes, f"{year}: frame is not a rectangular day x code grid"
    averaged = rank_average_n(raws, frame["grid_price_valid"].to_numpy(), codes)
    panel = Panel.from_frame(frame.with_columns(pl.Series("pred_raw", averaged)))
    return make_prediction(panel, frame["aux_raw"].to_numpy().astype(np.float64), "top_only", 0.25)


def top_sets(frame: pd.DataFrame, pred: np.ndarray) -> tuple[np.ndarray, dict]:
    """Evaluator-faithful Top decile on the TURNOVER universe (flag_limit_up == 0); no labels read.

    The fold frames are sorted by trade_date, so each day is one contiguous block; scanning the
    block boundaries once keeps this linear instead of O(days x rows).
    """
    dates = frame["trade_date"].to_numpy()
    flags = frame["flag_limit_up"].to_numpy()
    if not (np.diff(dates) >= 0).all():
        raise AssertionError("top_sets requires a frame sorted by trade_date")
    unique_days, starts = np.unique(dates, return_index=True)
    ends = np.append(starts[1:], len(dates))
    promoted = np.zeros(len(frame), dtype=bool)
    stats = {"days": 0, "skipped_lt100": 0, "boundary_tie_days": 0, "sizes": []}
    for start, end in zip(starts, ends):
        rows = np.arange(start, end)
        eligible = rows[flags[start:end] == 0]
        if len(eligible) < 100:
            stats["skipped_lt100"] += 1
            continue
        values = pred[eligible]
        n_top = max(len(eligible) // 10, 1)
        order = np.argsort(-values, kind="stable")
        if n_top < len(values) and values[order[n_top - 1]] == values[order[n_top]]:
            stats["boundary_tie_days"] += 1
        promoted[eligible[order[:n_top]]] = True
        stats["days"] += 1
        stats["sizes"].append(n_top)
    stats["unique_days"] = int(len(unique_days))
    stats["sizes"] = [int(np.min(stats["sizes"])), int(np.max(stats["sizes"]))] if stats["sizes"] else []
    return promoted, stats


# --------------------------------------------------------------------------- stages

def freeze() -> None:
    screen = json.loads((HERE / "screen_test_slice.json").read_text(encoding="utf-8"))
    inputs = [R4 / f"predictions_ensemble4_{y}.parquet" for y in YEARS]
    inputs += [topk_predictions(y) for y in YEARS]
    inputs += [daily_full16(y) for y in YEARS]
    inputs += [FEATURES, ROOT / "experiments/cached_recheck.py", ROOT / "src/scoring.py",
               ROOT / "src/postprocessing.py", ROOT / "evaluate.py",
               ROOT / "experiments/revalidate_fold_local.py", W14]
    for path in inputs:
        assert path.exists(), f"missing frozen input: {path}"
    seed_caches = sorted(RAW16.glob("raw_deployed67_slow_seed*_*.parquet"))
    assert len(seed_caches) == 80, f"expected 80 seed caches, found {len(seed_caches)}"

    payload = {
        "frozen_at_local": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "status": "descriptive_only_no_promotion",
        "candidate": {
            "name": "topset_substitution_B_membership_A_ordering",
            "arm_A": "peer67_slow16 (the confirmed model), reconstructed per fold from the 80 "
                     "surviving per-seed raw caches via the frozen wave-14 rank average and the "
                     "released postprocess stack with the per-fold pooled auxiliary at top_only 0.25",
            "arm_B": "topk_return_backbone (LightGBM Top-K return-weighted pairwise objective, "
                     "lr 0.05 / 31 leaves / 180 rounds / seed 2026) final fold prediction",
            "construction": "H = is_promoted * (span(pred_A) + 1) + pred_A, where is_promoted marks "
                            "arm B's Top decile on the evaluator's turnover universe",
            "membership_universe": "flag_limit_up == 0, n_top = max(len // 10, 1), stable descending "
                                   "sort by pred_B - identical to evaluate.py's own turnover rule",
            "single_fixed_candidate": True, "grid_searched": False, "variants_scored": 1,
        },
        "causality": "membership uses only flag_limit_up and pred_B. y_ret_1d and its availability "
                     "are never read to build the prediction; the evaluator's label filter for the "
                     "excess term is not available at prediction time and is not used",
        "years": list(YEARS), "scored_once": True,
        "harness_proofs_required_before_any_hybrid_score": {
            "A_reproduction": f"the reconstructed arm A must reproduce the frozen wave-24 full16 "
                              f"composite for every year within {TOL16}, and its per-day official "
                              f"terms must match the frozen daily_full16 CSV",
            "A_targets": {str(k): v for k, v in EXPECTED_FULL16.items()},
            "B_reproduction": "arm B's frozen fold prediction must reproduce its recorded official "
                              "score within 1e-12 for 2020-2022, and the 2023/2024 records produced "
                              "on 2026-10-01 for the remaining years",
            "grid_alignment": "the reconstructed day x code grid keys must equal the r4 fold frame keys",
            "top_set_identity": "the hybrid's own evaluator Top decile must equal arm B's on every "
                                "scored day, with zero boundary ties",
            "scorer_anchor": "score_official must reproduce the frozen baseline and ensemble4 "
                             "reference metrics for each year within 1e-12",
        },
        "instrument": {
            "scorer": "unmodified evaluate.py via experiments.revalidate_fold_local.score_official",
            "paired": "analysis.official_score_contributions.paired_difference",
            "ci": "20-day moving-block bootstrap, 20000 draws, seed 20260929+year, drawn "
                  "independently per year and averaged - the calibrated instrument already used for "
                  "the tree cluster, top2, MLP and Top-K",
        },
        "predeclared_interpretation_rule": {
            "primary_contrast": "H - arm A (the confirmed model) over 2020-2024",
            "also_reported": ["H - arm B", "per-year values", "IC/excess/turnover decomposition",
                              "Top-decile Jaccard overlap between A and B"],
            "ci95_entirely_above_zero": "resolvable ahead on the admissible axis. Recorded as a "
                                        "candidate; NOT auto-promoted - the five years are viewed, "
                                        "no blind period remains, and adoption would require an "
                                        "explicit user override with this disclosure attached",
            "ci95_crosses_zero": "tie; not adoptable",
            "ci95_entirely_below_zero": "mechanism rejected and closed",
            "no_window_substitution": "all five pre-declared years are reported; no 2-, 3- or 4-year "
                                      "window may replace them",
            "no_threshold_relaxation": "the rule is applied as written regardless of the outcome",
        },
        "disclosed_prior": {
            "test_slice_screen": "H - A = "
                                 f"{screen['contrasts']['H_hybrid_minus_A_peer67_slow16__full343']['diff']:+.6f}"
                                 ", CI "
                                 f"{screen['contrasts']['H_hybrid_minus_A_peer67_slow16__full343']['ci95']}",
            "status": "evaluation-set evidence, descriptive only, disclosed before the fold run",
            "test_slice_term_capture": screen["term_capture"],
            "test_slice_top_overlap_jaccard": screen["top_decile_overlap_jaccard_A_vs_B"],
            "why_disclosed": "so the fold result cannot be presented as a blind test, and so a "
                             "favourable fold outcome is read as confirmation of a mechanism already "
                             "seen on the evaluation set rather than as independent discovery",
        },
        "delivery_untouched": "no release, delivery, pointer or upload file is read for writing; "
                              "everything lands in this directory",
        "all_years_previously_viewed": True,
        "seed_caches": {p.name: sha(p) for p in seed_caches},
        "input_sha256": {str(p): sha(p) for p in inputs},
        "source_sha256": sha(Path(__file__)),
        "python": platform.python_version(),
        "package_versions": {n: getattr(__import__(n), "__version__", "unknown")
                             for n in ("lightgbm", "numpy", "polars", "pandas", "scipy", "xgboost")},
    }
    write_new(HERE / "protocol.json", payload)
    log(f"protocol frozen: {sha(HERE / 'protocol.json')}")


def verify_protocol() -> dict:
    protocol = json.loads((HERE / "protocol.json").read_text(encoding="utf-8"))
    assert protocol["source_sha256"] == sha(Path(__file__)), "this script changed after freezing"
    for path, digest in protocol["input_sha256"].items():
        assert sha(Path(path)) == digest, f"frozen input changed: {path}"
    for name, digest in protocol["seed_caches"].items():
        assert sha(RAW16 / name) == digest, f"seed cache changed: {name}"
    return protocol


def prove() -> None:
    """Reconstruct both arms per fold and demand exact reproduction before any hybrid is built."""
    verify_protocol()
    if (HERE / "harness_proof.json").exists():
        raise FileExistsError("harness proof already recorded")
    rank_average_n = load_rank_average_n()
    record = {}
    anchors = {}
    reference_summary = json.loads((R4 / "summary.json").read_text(encoding="utf-8"))["metrics"]
    for year in YEARS:
        frame = fold_frame(year)
        # scorer anchor: the unmodified evaluator must reproduce the frozen reference metrics first
        for name in ("baseline", "ensemble4"):
            ref = pl.read_parquet(R4 / f"predictions_{name}_{year}.parquet").sort("trade_date", "ts_code")
            assert ref.select(KEYS).equals(frame.select(KEYS)), f"{year}/{name}: keys misaligned"
            ref_metrics, _ = score_official(frame, ref["pred"].to_numpy().astype(np.float64))
            expected = reference_summary[str(year)][name]
            anchor = max(abs(ref_metrics[k] - expected[k]) for k in ref_metrics)
            assert anchor <= 1e-12, f"{year}/{name}: scorer anchor off by {anchor:.3e}"
            anchors[f"{year}/{name}"] = anchor
        log(f"{year}: scorer anchor reproduced baseline+ensemble4 to "
            f"{max(anchors[f'{year}/baseline'], anchors[f'{year}/ensemble4']):.1e}")
        a_final = build_A(frame, rank_average_n)
        metrics_a, daily_a = score_official(frame, a_final)
        frozen_daily = pd.read_csv(daily_full16(year))
        daily_pd = daily_a.to_pandas()
        assert np.array_equal(daily_pd["trade_date"].to_numpy(),
                              frozen_daily["trade_date"].to_numpy()), f"{year}: daily dates differ"
        daily_diff = {c: float(np.nanmax(np.abs(daily_pd[c].to_numpy() - frozen_daily[c].to_numpy())))
                      for c in ("rank_ic", "excess", "turnover")}
        diff_a = abs(metrics_a["final_score"] - EXPECTED_FULL16[year])
        assert diff_a <= TOL16, f"{year}: arm A off by {diff_a:.3e} > {TOL16:.0e}"

        b = pl.read_parquet(topk_predictions(year)).sort("trade_date", "ts_code")
        assert b.select(KEYS).equals(frame.select(KEYS)), f"{year}: arm B keys misaligned"
        b_final = b["pred"].to_numpy().astype(np.float64)
        metrics_b, _ = score_official(frame, b_final)
        expected_b = EXPECTED_TOPK[year]
        if expected_b is None:
            frozen = json.loads((TOPK_NEW / f"fold_{year}.json").read_text(encoding="utf-8"))
            expected_b = frozen["metrics"]["final_score"]
        diff_b = abs(metrics_b["final_score"] - expected_b)
        assert diff_b <= 1e-12, f"{year}: arm B off by {diff_b:.3e}"

        record[str(year)] = {"A_composite": metrics_a["final_score"], "A_target": EXPECTED_FULL16[year],
                             "A_abs_diff": diff_a, "A_daily_max_abs_diff": daily_diff,
                             "B_composite": metrics_b["final_score"], "B_target": expected_b,
                             "B_abs_diff": diff_b, "days": int(frame["trade_date"].n_unique()),
                             "rows": len(frame)}
        log(f"{year}: A {metrics_a['final_score']:.9f} (diff {diff_a:.1e}) | "
            f"B {metrics_b['final_score']:.9f} (diff {diff_b:.1e}) | daily max diff "
            f"{max(daily_diff.values()):.1e}")
        del frame, a_final, b, b_final
        gc.collect()
    worst = max(max(r["A_abs_diff"], r["B_abs_diff"]) for r in record.values())
    worst_daily = max(max(r["A_daily_max_abs_diff"].values()) for r in record.values())
    payload = {"passed": bool(worst <= TOL16 and worst_daily <= 1e-12),
               "worst_composite_abs_diff": worst, "worst_daily_abs_diff": worst_daily,
               "scorer_anchors": anchors,
               "worst_scorer_anchor_abs_diff": max(anchors.values()),
               "per_year": record}
    write_new(HERE / "harness_proof.json", payload)
    log(f"harness proof: worst composite diff {worst:.3e}, worst per-day diff {worst_daily:.3e} "
        f"-> {'PASS' if payload['passed'] else 'FAIL'}")
    assert payload["passed"]


def run() -> None:
    verify_protocol()
    proof = json.loads((HERE / "harness_proof.json").read_text(encoding="utf-8"))
    assert proof["passed"], "harness proof did not pass"
    rank_average_n = load_rank_average_n()
    for year in YEARS:
        if (HERE / f"fold_{year}.json").exists():
            log(f"{year}: already scored, preserved")
            continue
        frame = fold_frame(year)
        pdf = frame.to_pandas()
        a_final = build_A(frame, rank_average_n)
        b_final = pl.read_parquet(topk_predictions(year)).sort("trade_date", "ts_code")[
            "pred"].to_numpy().astype(np.float64)

        promoted_B, stats_B = top_sets(pdf, b_final)
        promoted_A, stats_A = top_sets(pdf, a_final)
        span = float(a_final.max() - a_final.min())
        hybrid = promoted_B.astype(np.float64) * (span + 1.0) + a_final
        assert np.isfinite(hybrid).all()
        assert hybrid[promoted_B].min() > hybrid[~promoted_B].max(), f"{year}: blocks overlap"

        promoted_H, stats_H = top_sets(pdf, hybrid)
        mismatches = int((promoted_H != promoted_B).sum())
        overlap = float((promoted_A & promoted_B).sum() / (promoted_A | promoted_B).sum())

        metrics_a, daily_a = score_official(frame, a_final)
        metrics_b, daily_b = score_official(frame, b_final)
        metrics_h, daily_h = score_official(frame, hybrid)
        for name, daily in (("A", daily_a), ("B", daily_b), ("H", daily_h)):
            daily.write_csv(HERE / f"daily_{name}_{year}.csv")

        write_new(HERE / f"fold_{year}.json", {
            "year": year, "protocol_sha256": sha(HERE / "protocol.json"),
            "rows": len(frame), "days": int(frame["trade_date"].n_unique()),
            "metrics": {"A_peer67_slow16": metrics_a, "B_topk": metrics_b, "H_hybrid": metrics_h},
            "top_set": {"jaccard_A_vs_B": overlap,
                        "A_members": int(promoted_A.sum()), "B_members": int(promoted_B.sum()),
                        "hybrid_equals_B_exactly": mismatches == 0, "mismatched_rows": mismatches,
                        "boundary_tie_days": {"A": stats_A["boundary_tie_days"],
                                              "B": stats_B["boundary_tie_days"],
                                              "H": stats_H["boundary_tie_days"]},
                        "scored_days": stats_B["days"], "top_size_range": stats_B["sizes"]},
            "block_offset": span + 1.0,
        })
        log(f"{year}: A {metrics_a['final_score']:.9f} | B {metrics_b['final_score']:.9f} | "
            f"H {metrics_h['final_score']:.9f} (H-A {metrics_h['final_score']-metrics_a['final_score']:+.6f}) "
            f"| Top overlap {overlap:.4f} | hybrid==B top set: {mismatches == 0}")
        del frame, pdf, a_final, b_final, hybrid
        gc.collect()


def compare() -> None:
    verify_protocol()
    rng_seed = 20260929

    def boot(diff: np.ndarray, year: int, draws: int = 20000, block: int = 20):
        rng = np.random.default_rng(rng_seed + year)
        n = len(diff)
        n_blocks = int(np.ceil(n / block))
        starts = rng.integers(0, n - block + 1, size=(draws, n_blocks))
        out = np.empty(draws)
        for i in range(draws):
            out[i] = np.concatenate([diff[s:s + block] for s in starts[i]])[:n].mean()
        return out

    dailies = {arm: {y: pd.read_csv(HERE / f"daily_{arm}_{y}.csv") for y in YEARS}
               for arm in ("A", "B", "H")}
    per_year = {arm: {y: composite(d) for y, d in years.items()} for arm, years in dailies.items()}

    # calibrate on a published interval before trusting any new one
    def find_daily(name: str) -> Path:
        for root in (CLEANUP, ARCHIVE):
            candidate = root / "analysis/top2_training_validation_20260929" / name
            if candidate.exists():
                return candidate
        raise SystemExit(f"missing calibration daily CSV: {name}")

    yearly_means, draws_by_year = [], []
    for y in YEARS:
        diff = paired_difference(pd.read_csv(find_daily(f"daily_top2_{y}.csv")),
                                 pd.read_csv(find_daily(f"daily_slow_only8_{y}.csv")))
        yearly_means.append(float(diff.mean()))
        draws_by_year.append(boot(diff, y))
    cal_draws = np.mean(np.column_stack(draws_by_year), axis=1)
    calibration = {"pair": "top2_lightgbm - slow_only8",
                   "recomputed_ci95": [float(np.percentile(cal_draws, 2.5)),
                                       float(np.percentile(cal_draws, 97.5))],
                   "published_ci95": [-0.060428, -0.006207],
                   "recomputed_mean": float(np.mean(yearly_means)),
                   "published_mean": -0.037270}
    assert abs(calibration["recomputed_ci95"][0] - calibration["published_ci95"][0]) < 5e-7
    assert abs(calibration["recomputed_ci95"][1] - calibration["published_ci95"][1]) < 5e-7
    assert abs(calibration["recomputed_mean"] - calibration["published_mean"]) < 2e-6
    log(f"bootstrap calibrated against the published interval: {calibration['recomputed_ci95']}")

    def contrast(left, right):
        yearly, draws_by_year = [], []
        for y in YEARS:
            diff = paired_difference(dailies[left][y], dailies[right][y])
            yearly.append(float(diff.mean()))
            draws_by_year.append(boot(diff, y))
        stacked = np.mean(np.column_stack(draws_by_year), axis=1)
        ci = [float(np.percentile(stacked, 2.5)), float(np.percentile(stacked, 97.5))]
        return {"per_year": {str(y): v for y, v in zip(YEARS, yearly)},
                "five_year_mean": float(np.mean(yearly)),
                "years_positive": int(sum(1 for v in yearly if v > 0)),
                "ci95": ci, "positive_share": float((stacked > 0).mean()),
                "verdict": "resolvable_ahead" if ci[0] > 0 else (
                    "resolvable_behind" if ci[1] < 0 else "tie")}

    pairs = {"H_minus_A": contrast("H", "A"), "H_minus_B": contrast("H", "B"),
             "B_minus_A": contrast("B", "A")}

    decomposition = {}
    for left, right in (("H", "A"), ("H", "B")):
        rows = {}
        for y in YEARS:
            l, r = dailies[left][y], dailies[right][y]
            row = {name: weight * (l[name].mean() - r[name].mean()) for name, weight in WEIGHTS.items()}
            row["total"] = sum(row.values())
            assert abs(row["total"] - (composite(l) - composite(r))) <= 1e-12
            for name in WEIGHTS:
                row[f"{name}_level_left"] = float(l[name].mean())
                row[f"{name}_level_right"] = float(r[name].mean())
            rows[str(y)] = row
        rows["five_year_mean"] = {n: float(np.mean([rows[str(y)][n] for y in YEARS]))
                                 for n in ("rank_ic", "excess", "turnover", "total")}
        decomposition[f"{left}_minus_{right}"] = rows

    folds = {str(y): json.loads((HERE / f"fold_{y}.json").read_text(encoding="utf-8")) for y in YEARS}
    rule = json.loads((HERE / "protocol.json").read_text(encoding="utf-8"))[
        "predeclared_interpretation_rule"]
    primary = pairs["H_minus_A"]
    branch = {"resolvable_ahead": "ci95_entirely_above_zero", "tie": "ci95_crosses_zero",
              "resolvable_behind": "ci95_entirely_below_zero"}[primary["verdict"]]

    payload = {
        "status": "complete", "completed_at_local": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "protocol_sha256": sha(HERE / "protocol.json"),
        "descriptive_only": True, "promotes_or_adopts_nothing": True,
        "harness_proof": json.loads((HERE / "harness_proof.json").read_text(encoding="utf-8")),
        "bootstrap_calibration": calibration,
        "per_year_composite": {arm: {str(y): v for y, v in years.items()}
                               for arm, years in per_year.items()},
        "five_year_mean": {arm: float(np.mean(list(y.values()))) for arm, y in per_year.items()},
        "pairs": pairs, "term_decomposition": decomposition,
        "top_set_overlap_jaccard": {y: folds[y]["top_set"]["jaccard_A_vs_B"] for y in folds},
        "hybrid_top_set_equals_B_every_day":
            all(folds[y]["top_set"]["hybrid_equals_B_exactly"] for y in folds),
        "boundary_tie_days": {y: folds[y]["top_set"]["boundary_tie_days"] for y in folds},
        "predeclared_rule_applied": {"branch": branch, "rule_text": rule[branch],
                                     "verdict": primary["verdict"],
                                     "five_year_mean": primary["five_year_mean"],
                                     "ci95": primary["ci95"]},
    }
    write_new(HERE / "fold_comparison.json", payload)

    print(f"\n| arm | " + " | ".join(str(y) for y in YEARS) + " | 5y mean |")
    print("|---|" + "---|" * 7)
    for arm, label in (("H", "H_hybrid"), ("A", "A_peer67_slow16"), ("B", "B_topk")):
        print(f"| {label} | " + " | ".join(f"{per_year[arm][y]:.6f}" for y in YEARS)
              + f" | {np.mean([per_year[arm][y] for y in YEARS]):.6f} |")
    print("\n| contrast | 5y diff | yrs>0 | CI95 | verdict | P(>0) |")
    print("|---|---|---|---|---|---|")
    for key, v in pairs.items():
        print(f"| {key} | {v['five_year_mean']:+.6f} | {v['years_positive']}/5 | "
              f"[{v['ci95'][0]:+.6f}, {v['ci95'][1]:+.6f}] | {v['verdict']} | "
              f"{v['positive_share']*100:.1f}% |")
    print("\nTop-decile Jaccard overlap A vs B per year: "
          + " ".join(f"{y}:{folds[y]['top_set']['jaccard_A_vs_B']:.4f}" for y in folds))
    print("\nH - A term contributions (five-year mean):")
    for name in ("rank_ic", "excess", "turnover", "total"):
        print(f"  {name:9s} {decomposition['H_minus_A']['five_year_mean'][name]:+.6f}")
    print(f"\npre-declared rule -> {branch}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("stage", choices=("freeze", "prove", "run", "compare"))
    args = parser.parse_args()
    HERE.mkdir(parents=True, exist_ok=True)
    try:
        globals()[args.stage]()
    except Exception as error:
        write_new(HERE / f"failure_{args.stage}_{time.time_ns()}.json",
                  {"stage": args.stage, "type": type(error).__name__, "message": str(error),
                   "traceback": traceback.format_exc(), "source_sha256": sha(Path(__file__))})
        raise
