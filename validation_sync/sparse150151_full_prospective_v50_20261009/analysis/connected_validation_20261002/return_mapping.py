"""Rule 5 of 后续选模标准.md: make `pred` an actual return forecast, fitted inside the training period.

The shipped column is not one. `run.py:257` does
    pred = np.where(ranked < -1, -0.05, 0.04 * (ranked - 0.5))
i.e. the daily rank linearly rescaled into a return-looking range, with -0.05 as a sentinel for
price-invalid rows (44,844 rows, 2.8% of the test file, sit exactly on it). The brief defines pred as
a next-day return prediction, and the standard says a rank-only output may not be presented as one:
if a return mapping is needed it must be fitted in the training period and the MAPPED output brought
into validation.

Construction, deliberately score-neutral by design rather than by hope:
  p    = within-day average rank of the scheme's output / rows in day   (an order-isomorphism of the
         tie classes, so ties are preserved exactly)
  g    = isotonic regression of realized y_ret_1d on p, fitted ONLY on the 2020-2024 walk-forward
         fold predictions and their realized labels - no 2025-2026 data is read
  pred = g(p) + EPS * p, with EPS small enough to be immaterial as a return but large enough to keep
         g's flat regions from merging distinct tie classes

Because p preserves the ordering and the tie structure of the original column exactly, and g is
non-decreasing with a strictly increasing term added, every official metric is unchanged: Rank IC and
both Top-decile terms depend only on within-day ordering. That is asserted here at 1e-12 on the
connected composite and by exact Top-set equality on every day, not assumed.
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd
import polars as pl
from sklearn.isotonic import IsotonicRegression

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(HERE))
import connected_scorer as cs  # noqa: E402
from experiments.revalidate_fold_local import score_official  # noqa: E402

YEARS = cs.YEARS
EPS = 1e-9
BINS = 2000
KEYS = cs.KEYS


def daily_percentile(frame: pd.DataFrame, values: np.ndarray) -> np.ndarray:
    """Within-day average rank divided by the day's row count; ties stay tied."""
    series = pd.Series(values)
    ranks = series.groupby(frame["trade_date"].to_numpy(), sort=False).rank(method="average")
    counts = series.groupby(frame["trade_date"].to_numpy(), sort=False).transform("size")
    out = ranks.to_numpy() / counts.to_numpy()
    if not np.isfinite(out).all() or out.min() <= 0 or out.max() > 1.0 + 1e-12:
        raise AssertionError("daily percentile out of range")
    return out


def fit_mapping(percentile: np.ndarray, realized: np.ndarray) -> dict:
    """Isotonic E[y_ret_1d | within-day percentile], fitted on training-period folds only."""
    finite = np.isfinite(realized)
    p, y = percentile[finite], realized[finite]
    edges = np.linspace(0.0, 1.0, BINS + 1)
    index = np.clip(np.searchsorted(edges, p, side="right") - 1, 0, BINS - 1)
    sums = np.bincount(index, weights=y, minlength=BINS)
    counts = np.bincount(index, minlength=BINS).astype(np.float64)
    centers = 0.5 * (edges[:-1] + edges[1:])
    used = counts > 0
    iso = IsotonicRegression(increasing=True, out_of_bounds="clip")
    iso.fit(centers[used], (sums[used] / counts[used]), sample_weight=counts[used])
    fitted = iso.predict(centers)
    if not (np.diff(fitted) >= -1e-15).all():
        raise AssertionError("the fitted mapping is not monotone non-decreasing")
    return {"bins": BINS, "centers": centers.tolist(), "fitted": fitted.tolist(),
            "bin_counts": counts.tolist(), "n_obs": int(finite.sum()),
            "n_obs_dropped_no_label": int((~finite).sum()),
            "monotone": True, "eps": EPS,
            "range": [float(fitted.min()), float(fitted.max())]}


def apply_mapping(mapping: dict, percentile: np.ndarray) -> np.ndarray:
    iso = IsotonicRegression(increasing=True, out_of_bounds="clip")
    centers = np.asarray(mapping["centers"])
    iso.fit(centers, np.asarray(mapping["fitted"]))
    return iso.predict(percentile) + EPS * percentile


def top_sets(frame: pd.DataFrame, pred: np.ndarray) -> list[frozenset]:
    """The evaluator's own Top decile per day: flag_limit_up == 0, n_top = len // 10, no label filter."""
    out = []
    dates = frame["trade_date"].to_numpy()
    flags = frame["flag_limit_up"].to_numpy()
    unique, starts = np.unique(dates, return_index=True)
    ends = np.append(starts[1:], len(dates))
    for start, end in zip(starts, ends):
        rows = np.arange(start, end)
        eligible = rows[flags[start:end] == 0]
        if len(eligible) < 100:
            out.append(frozenset())
            continue
        n_top = max(len(eligible) // 10, 1)
        order = np.argsort(-pred[eligible], kind="stable")
        out.append(frozenset(eligible[order[:n_top]].tolist()))
    return out


def build(name: str) -> dict:
    frame = cs.combined_frame().to_pandas()
    pred_path = HERE / f"connected_pred_{name}.npy"
    if not pred_path.exists():
        raise SystemExit(f"no saved connected prediction for {name}")
    pred = np.load(pred_path)
    assert len(pred) == len(frame)

    percentile = daily_percentile(frame, pred)
    realized = frame["y_ret_1d"].to_numpy(dtype=np.float64)
    mapping = fit_mapping(percentile, realized)
    mapped = apply_mapping(mapping, percentile)

    # ---- score neutrality: the whole point of the construction, asserted not assumed
    pl_frame = cs.combined_frame()
    before, _ = score_official(pl_frame, pred)
    after, _ = score_official(pl_frame, mapped)
    deltas = {k: abs(after[k] - before[k]) for k in before}
    worst = max(deltas.values())
    sets_before = top_sets(frame, pred)
    sets_after = top_sets(frame, mapped)
    identical_sets = all(a == b for a, b in zip(sets_before, sets_after))
    n_days_differing = sum(1 for a, b in zip(sets_before, sets_after) if a != b)
    # ordering preserved: the within-day rank of every row is unchanged
    rank_before = pd.Series(pred).groupby(frame["trade_date"].to_numpy(), sort=False).rank(method="average")
    rank_after = pd.Series(mapped).groupby(frame["trade_date"].to_numpy(), sort=False).rank(method="average")
    ranks_preserved = bool(np.array_equal(rank_before.to_numpy(), rank_after.to_numpy()))

    record = {
        "arm": name, "status": "complete", "built_at_local": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "fitted_on": "2020-2024 walk-forward fold predictions and their realized labels only",
        "no_test_period_data_read": True,
        "mapping": {k: v for k, v in mapping.items() if k not in ("centers", "fitted", "bin_counts")},
        "mapping_summary": {
            "percentile_50": float(np.interp(0.50, mapping["centers"], mapping["fitted"])),
            "percentile_90": float(np.interp(0.90, mapping["centers"], mapping["fitted"])),
            "percentile_99": float(np.interp(0.99, mapping["centers"], mapping["fitted"])),
            "percentile_100": float(np.interp(1.00, mapping["centers"], mapping["fitted"])),
            "percentile_1": float(np.interp(0.01, mapping["centers"], mapping["fitted"])),
            "realized_mean_all_rows": float(np.nanmean(realized)),
        },
        "score_neutrality": {
            "connected_before": before["final_score"], "connected_after": after["final_score"],
            "max_abs_metric_diff": worst, "per_metric_abs_diff": deltas,
            "top_decile_sets_identical_every_day": identical_sets,
            "days_with_a_different_top_set": n_days_differing,
            "within_day_ranks_preserved": ranks_preserved,
            "passed": bool(worst <= 1e-12 and identical_sets and ranks_preserved),
        },
        "mapped_output_stats": {"min": float(mapped.min()), "max": float(mapped.max()),
                                "mean": float(mapped.mean()), "std": float(mapped.std()),
                                "n_unique": int(len(np.unique(mapped)))},
    }
    np.save(HERE / f"mapped_pred_{name}.npy", mapped)
    (HERE / f"return_mapping_{name}.json").write_text(
        json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    np.savez_compressed(HERE / f"return_mapping_table_{name}.npz",
                        centers=np.asarray(mapping["centers"]),
                        fitted=np.asarray(mapping["fitted"]), eps=EPS)

    cs.log(f"{name}: connected {before['final_score']:.12f} -> {after['final_score']:.12f} "
           f"(max metric diff {worst:.2e}), Top sets identical every day: {identical_sets}, "
           f"ranks preserved: {ranks_preserved}")
    cs.log(f"{name}: mapped pred range [{mapped.min():.6f}, {mapped.max():.6f}], "
           f"mean {mapped.mean():.6f}, sd {mapped.std():.6f}; "
           f"E[r|p=0.99] {record['mapping_summary']['percentile_99']:.6f}, "
           f"E[r|p=0.50] {record['mapping_summary']['percentile_50']:.6f}")
    return record


if __name__ == "__main__":
    names = sys.argv[1:] or ["peer67_slow16", "hybrid"]
    out = {name: build(name) for name in names}
    (HERE / "return_mapping_summary.json").write_text(
        json.dumps({"arms": list(out), "all_passed": all(v["score_neutrality"]["passed"]
                                                         for v in out.values()),
                    "records": {k: v["score_neutrality"] for k, v in out.items()}},
                   ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("\n| arm | connected before | after | max metric diff | Top sets identical | passed |")
    print("|---|---|---|---|---|---|")
    for name, r in out.items():
        s = r["score_neutrality"]
        print(f"| {name} | {s['connected_before']:.12f} | {s['connected_after']:.12f} | "
              f"{s['max_abs_metric_diff']:.2e} | {s['top_decile_sets_identical_every_day']} | "
              f"{s['passed']} |")
