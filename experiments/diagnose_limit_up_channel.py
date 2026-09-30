"""Diagnostic: how much score is available through the limit-up rows?

`evaluate.py` computes the three official terms on DIFFERENT row sets:

  * Rank IC (40%)      — every row with a non-null label, limit-up rows INCLUDED;
  * Top-10% excess (30%) — rows with flag_limit_up == 0 only, >=100 per day;
  * turnover (30%)       — rows with flag_limit_up == 0 only.

So a prediction for a limit-up row influences 40% of the composite and is *filtered out*
of the other 60%. That is a structural asymmetry in the scoring rule, not a modelling
choice, and no round has measured it. This script bounds the headroom before any model is
trained: per day it recomputes Spearman IC for the frozen released baseline, then for an
ORACLE that knows the limit-up rows' realised returns exactly and places them at their
true positions while leaving every other row's relative order untouched. The difference
is the most that any limit-up-specific model could ever add to the IC term, and it costs
nothing in the Top terms because those rows never enter a Top set.

Descriptive only. Reads frozen artifacts, writes to a new directory, changes nothing.
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
OUT = ROOT / "experiments" / "limit_up_channel_eval"
YEARS = (2020, 2021, 2022, 2023, 2024)
KEYS = ["ts_code", "trade_date"]
IC_WEIGHT = 0.4


def log(message: str) -> None:
    print(f"[{time.strftime('%H:%M:%S')}] {message}", flush=True)


def oracle_scores(prediction: np.ndarray, label: np.ndarray, treated: np.ndarray) -> np.ndarray:
    """Best achievable ordering given perfect knowledge of the treated subset only.

    Treated rows take exactly the slots their realised labels warrant; the remaining slots
    are filled by the untreated rows in their existing prediction order, which is the only
    freedom left. Any arrangement with fewer inversions would have to reorder untreated
    rows, which is excluded by construction.
    """
    n = len(prediction)
    label_order = np.argsort(label, kind="stable")
    untreated = np.flatnonzero(~treated)
    untreated_order = untreated[np.argsort(prediction[untreated], kind="stable")]
    slots = np.empty(n, dtype=np.int64)
    cursor = 0
    for position, index in enumerate(label_order):
        if treated[index]:
            slots[position] = index
        else:
            slots[position] = untreated_order[cursor]
            cursor += 1
    scores = np.empty(n, dtype=np.float64)
    scores[slots] = np.arange(n, dtype=np.float64)
    return scores


def analyse(year: int) -> dict:
    path = R4 / f"predictions_baseline_{year}.parquet"
    frame = pl.read_parquet(path).sort("trade_date", "ts_code")
    total_rows = frame.height
    # The evaluator drops rows without a label before computing anything, so do the same.
    frame = frame.filter(pl.col("y_ret_1d").is_not_null() & pl.col("y_ret_1d").is_finite())
    dropped_rows = total_rows - frame.height
    prediction = frame["pred"].to_numpy().astype(np.float64)
    label = frame["y_ret_1d"].to_numpy().astype(np.float64)
    limit_up = frame["flag_limit_up"].to_numpy().astype(bool)
    dates = frame["trade_date"].to_numpy()
    per_day = []
    for day in np.unique(dates):
        rows = np.flatnonzero(dates == day)
        treated = limit_up[rows]
        base = float(spearmanr(prediction[rows], label[rows]).statistic)
        ideal = oracle_scores(prediction[rows], label[rows], treated)
        oracle = float(spearmanr(ideal, label[rows]).statistic)
        # The untreated rows' own IC, to show whether the treated rows are ordered badly today.
        untreated = rows[~treated]
        per_day.append({"trade_date": int(day), "rows": len(rows),
                        "limit_up_rows": int(treated.sum()),
                        "limit_up_share": float(treated.mean()),
                        "ic_baseline": base, "ic_oracle": oracle,
                        "ic_delta": oracle - base,
                        "ic_untreated_only": float(spearmanr(prediction[untreated],
                                                             label[untreated]).statistic),
                        "mean_label_treated": float(label[rows][treated].mean()) if treated.any() else None,
                        "mean_label_untreated": float(label[rows][~treated].mean())})
    daily = pl.DataFrame(per_day)
    daily.write_csv(OUT / f"daily_{year}.csv")
    ic_base = float(daily["ic_baseline"].mean())
    ic_oracle = float(daily["ic_oracle"].mean())
    return {"year": year, "days": len(daily), "rows_scored": frame.height,
            "rows_dropped_for_missing_label": dropped_rows,
            "ic_baseline": ic_base, "ic_oracle_limit_up_subset": ic_oracle,
            "ic_delta": ic_oracle - ic_base,
            "composite_headroom": IC_WEIGHT * (ic_oracle - ic_base),
            "mean_limit_up_rows_per_day": float(daily["limit_up_rows"].mean()),
            "mean_limit_up_share": float(daily["limit_up_share"].mean()),
            "max_limit_up_share": float(daily["limit_up_share"].max()),
            "days_with_no_limit_up": int((daily["limit_up_rows"] == 0).sum()),
            "mean_next_day_return_limit_up": float(daily["mean_label_treated"].mean()),
            "mean_next_day_return_other": float(daily["mean_label_untreated"].mean()),
            "ic_untreated_only": float(daily["ic_untreated_only"].mean())}


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    destination = OUT / "headroom.json"
    if destination.exists():
        raise SystemExit("Headroom diagnostic already recorded; preserving it")
    started = time.monotonic()
    years = [analyse(year) for year in YEARS]
    for item in years:
        log(f"{item['year']}: limit-up {item['mean_limit_up_rows_per_day']:.0f} rows/day "
            f"({item['mean_limit_up_share']:.2%}), IC {item['ic_baseline']:.6f} → oracle "
            f"{item['ic_oracle_limit_up_subset']:.6f} (Δ {item['ic_delta']:+.6f}), composite "
            f"headroom {item['composite_headroom']:+.6f}, limit-up next-day return "
            f"{item['mean_next_day_return_limit_up']:+.5f} vs {item['mean_next_day_return_other']:+.5f}")
    payload = {
        "stage": "limit_up_channel_headroom", "generated_at_local": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "seconds": round(time.monotonic() - started, 2),
        "role": "Descriptive upper bound. No model was trained and no candidate was scored.",
        "mechanism": "evaluate.py ranks IC over all labelled rows but builds the Top decile and the "
                     "turnover sets from flag_limit_up == 0 rows only, so a limit-up row's "
                     "prediction reaches 40% of the composite and none of the other 60%.",
        "oracle_definition": "per day, treated rows are placed at their realised-label ranks while "
                             "every other row keeps its relative order under the frozen baseline "
                             "prediction; the resulting IC is the ceiling for any limit-up-specific "
                             "model",
        "years": years,
        "mean_composite_headroom": float(np.mean([item["composite_headroom"] for item in years])),
        "worst_year_headroom": float(min(item["composite_headroom"] for item in years)),
        "input_sha256": {f"predictions_baseline_{year}.parquet":
                         hashlib.sha256((R4 / f"predictions_baseline_{year}.parquet").read_bytes()
                                        ).hexdigest() for year in YEARS},
        "caveats": [
            "The oracle is unreachable; it measures the size of the channel, not an achievable gain.",
            "Changing limit-up rows' raw scores also shifts every other row's daily percentile rank "
            "inside the released post-processing stack, so the realised effect is not exactly the "
            "IC delta measured here.",
            "The Top-excess and turnover terms are unaffected only if the submitted ordering of "
            "non-limit-up rows is unchanged; the percentile-rank coupling above can perturb it.",
        ],
    }
    destination.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    log(f"Mean composite headroom across five years: {payload['mean_composite_headroom']:+.6f} "
        f"(worst year {payload['worst_year_headroom']:+.6f})")
    log(f"Wrote {destination}")


if __name__ == "__main__":
    main()
