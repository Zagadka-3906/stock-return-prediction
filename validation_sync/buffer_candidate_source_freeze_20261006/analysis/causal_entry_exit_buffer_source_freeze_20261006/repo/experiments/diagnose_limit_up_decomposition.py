"""Where does the limit-up oracle headroom actually live: placement, or within-group order?

`headroom.json` bounds a perfect re-ordering of limit-up rows at +0.0105 composite on
average, and `limit_up_rule_eval` showed that a blanket lift of those rows to the top of
each day captures only +0.000197 of it — 1.9% — and is negative in 2022 and 2024. So the
released model already places limit-up stocks near the top, and the residual headroom must
be one of two things:

  (a) the group sits in slightly the wrong PLACE relative to the rest of the cross-section,
      which a fixed placement rule could fix, or
  (b) the group's members are in the wrong ORDER among themselves, which only a model that
      discriminates between limit-up stocks could fix.

This script separates the two, because they have completely different implications. For
each day it measures

  * the mean predicted percentile and the mean realised-label percentile of limit-up rows,
    which shows how far the group as a whole is misplaced;
  * the IC of a WITHIN-GROUP oracle: limit-up rows keep exactly the slots the baseline gave
    them, but are permuted among those slots into their true label order. This is the
    ceiling for any limit-up-specific model, and it is the number that decides whether
    building one is worth anything;
  * the IC of the FULL oracle, whose excess over the within-group oracle is the placement
    residual — the part only relocating the whole group can reach, which
    experiments/limit_up_rule_eval already showed a fixed rule captures almost none of.

Descriptive only, no model, no candidate, no gate. Reads frozen artifacts, writes to a new
directory.
"""
from __future__ import annotations

import hashlib
import json
import time
from pathlib import Path

import numpy as np
import polars as pl
from scipy.stats import spearmanr

from run import ROOT

R4 = ROOT / "experiments" / "revalidation_20260926" / "validation"
OUT = ROOT / "experiments" / "limit_up_decomposition_eval"
YEARS = (2020, 2021, 2022, 2023, 2024)
IC_WEIGHT = 0.4


def log(message: str) -> None:
    print(f"[{time.strftime('%H:%M:%S')}] {message}", flush=True)


def percentiles(values: np.ndarray) -> np.ndarray:
    order = np.argsort(values, kind="stable")
    ranks = np.empty(len(values), dtype=np.float64)
    ranks[order] = np.arange(len(values), dtype=np.float64)
    return ranks / max(len(values) - 1, 1)


def analyse(year: int) -> dict:
    frame = (pl.read_parquet(R4 / f"predictions_baseline_{year}.parquet").sort("trade_date", "ts_code"))
    prediction = frame["pred"].to_numpy().astype(np.float64)
    label = frame["y_ret_1d"].to_numpy().astype(np.float64)
    limit_up = frame["flag_limit_up"].to_numpy().astype(bool)
    dates = frame["trade_date"].to_numpy()
    labelled = np.isfinite(label)
    per_day = []
    for day in np.unique(dates):
        rows = np.flatnonzero((dates == day) & labelled)
        if len(rows) < 30:
            continue
        treated = limit_up[rows]
        if not treated.any():
            continue
        pred, truth = prediction[rows], label[rows]
        base_ic = float(spearmanr(pred, truth).statistic)
        pred_pct, label_pct = percentiles(pred), percentiles(truth)
        treated_positions = np.flatnonzero(treated)
        # Within-group oracle: the group keeps exactly the slots the baseline gave it, and its
        # members are permuted into their true label order. Ceiling for a segment model.
        slots = np.sort(pred_pct[treated])
        by_truth = treated_positions[np.argsort(label_pct[treated], kind="stable")]
        reordered = pred_pct.copy()
        reordered[by_truth] = slots
        within_ic = float(spearmanr(reordered, label_pct).statistic)
        # Full oracle: treated rows take their true label percentiles outright. Ceiling for
        # any intervention on this subset, placement and order together.
        full = pred_pct.copy()
        full[treated] = label_pct[treated]
        full_ic = float(spearmanr(full, label_pct).statistic)
        per_day.append({"trade_date": int(day), "rows": len(rows),
                        "limit_up_rows": int(treated.sum()),
                        "mean_pred_percentile_treated": float(pred_pct[treated].mean()),
                        "mean_label_percentile_treated": float(label_pct[treated].mean()),
                        "mean_pred_percentile_other": float(pred_pct[~treated].mean()),
                        "mean_label_percentile_other": float(label_pct[~treated].mean()),
                        "ic_baseline": base_ic, "ic_within_group_oracle": within_ic,
                        "ic_full_oracle": full_ic})
    daily = pl.DataFrame(per_day)
    daily.write_csv(OUT / f"daily_{year}.csv")
    base = float(daily["ic_baseline"].mean())
    within = float(daily["ic_within_group_oracle"].mean())
    full = float(daily["ic_full_oracle"].mean())
    entry = {"year": year, "days": len(daily),
             "mean_limit_up_rows_per_day": float(daily["limit_up_rows"].mean()),
             "mean_pred_percentile_treated": float(daily["mean_pred_percentile_treated"].mean()),
             "mean_label_percentile_treated": float(daily["mean_label_percentile_treated"].mean()),
             "mean_pred_percentile_other": float(daily["mean_pred_percentile_other"].mean()),
             "mean_label_percentile_other": float(daily["mean_label_percentile_other"].mean()),
             "ic_baseline": base,
             "ic_within_group_oracle": within, "ic_delta_within_group": within - base,
             "composite_headroom_within_group": IC_WEIGHT * (within - base),
             "ic_full_oracle": full, "ic_delta_full": full - base,
             "composite_headroom_full": IC_WEIGHT * (full - base),
             "composite_headroom_placement_residual": IC_WEIGHT * (full - within)}
    log(f"{year}: limit-up rows sit at predicted percentile "
        f"{entry['mean_pred_percentile_treated']:.4f} but belong at "
        f"{entry['mean_label_percentile_treated']:.4f} | composite headroom within-group "
        f"{entry['composite_headroom_within_group']:+.6f}, placement residual "
        f"{entry['composite_headroom_placement_residual']:+.6f}, full "
        f"{entry['composite_headroom_full']:+.6f}")
    return entry


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    destination = OUT / "decomposition.json"
    if destination.exists():
        raise SystemExit("Decomposition already recorded; preserving it")
    started = time.monotonic()
    years = [analyse(year) for year in YEARS]
    means = {key: float(np.mean([item[key] for item in years])) for key in
             ("composite_headroom_within_group", "composite_headroom_placement_residual",
              "composite_headroom_full", "mean_pred_percentile_treated",
              "mean_label_percentile_treated")}
    payload = {"stage": "limit_up_headroom_decomposition",
               "generated_at_local": time.strftime("%Y-%m-%dT%H:%M:%S"),
               "seconds": round(time.monotonic() - started, 2),
               "role": "Descriptive ceilings. No model trained, no candidate scored.",
               "oracle_definitions": {
                   "within_group": "limit-up rows keep exactly the slots the baseline gave them and "
                                   "are permuted into their true label order — the ceiling for a "
                                   "limit-up-specific model that reorders but does not relocate",
                   "full": "limit-up rows take their true label percentiles outright — the ceiling "
                           "for any intervention on this subset",
                   "placement_residual": "full minus within_group: the part that only moving the "
                                         "group as a whole can reach, which limit_up_rule_eval "
                                         "already showed a fixed rule captures almost none of"},
               "years": years, "five_year_means": means,
               "reference": {"limit_up_rule_eval_R1_mean_composite_delta": 0.000197,
                             "headroom_json_mean_composite_headroom": 0.010501},
               "input_sha256": {f"predictions_baseline_{year}.parquet":
                                hashlib.sha256((R4 / f"predictions_baseline_{year}.parquet")
                                               .read_bytes()).hexdigest() for year in YEARS}}
    destination.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    log(f"Five-year means — within-group {means['composite_headroom_within_group']:+.6f}, "
        f"placement residual {means['composite_headroom_placement_residual']:+.6f}, full "
        f"{means['composite_headroom_full']:+.6f}")
    log(f"Wrote {destination}")


if __name__ == "__main__":
    main()
