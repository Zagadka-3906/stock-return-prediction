"""How much of the limit-up channel does a purely causal re-ranking rule capture?

`evaluate.py` builds the Top decile and the turnover sets from `flag_limit_up == 0` rows
only, but computes Rank IC over every labelled row. `flag_limit_up` for day t is supplied
in the test file and is known when the day-t prediction is formed, so re-ordering those
rows is causal. If the relative order of all OTHER rows is left untouched, the Top decile
and the turnover sets cannot change, so the composite moves by exactly 0.4 x the IC change.

This script tests that claim empirically instead of assuming it: it re-scores the frozen
released baseline prediction through the unmodified evaluator under a family of
deterministic promotion rules and reports all three official terms for each.

  R0_unchanged     the frozen baseline, as an anchor;
  R1_lift_to_top   the limit-up rows take exactly the day's top n_treated positions;
  R2_band_p        the limit-up rows sit inside the top (1 - p) share of the day, and the
                   best-scoring untreated rows fill the rest of that band.

Inside the band the existing relative order of all rows is preserved, and below it the
untreated rows keep theirs, so the intervention is the smallest one that achieves the
placement. No model is trained and no parameter is fitted: this measures how much of the
oracle headroom in experiments/limit_up_channel_eval/headroom.json is reachable with a rule
that uses only day-t information. Descriptive only; writes to a new directory.
"""
from __future__ import annotations

import hashlib
import json
import time
from pathlib import Path

import numpy as np
import polars as pl

from run import ROOT
from experiments.revalidate_fold_local import score_official

R4 = ROOT / "experiments" / "revalidation_20260926" / "validation"
OUT = ROOT / "experiments" / "limit_up_rule_eval"
YEARS = (2020, 2021, 2022, 2023, 2024)
BANDS = (0.90, 0.95, 0.97, 0.98, 0.99)
IC_WEIGHT = 0.4


def log(message: str) -> None:
    print(f"[{time.strftime('%H:%M:%S')}] {message}", flush=True)


def promote(prediction: np.ndarray, dates: np.ndarray, treated: np.ndarray, band_of) -> np.ndarray:
    """Move treated rows into each day's top `band_of(n_day, n_treated)` positions.

    Untreated rows below the band keep their relative order; rows inside the band keep
    their existing relative order with respect to each other. Every day is re-scored to an
    ascending rank, which the evaluator cannot distinguish from the original values because
    all three of its terms are computed within a single day.
    """
    out = prediction.astype(np.float64).copy()
    for day in np.unique(dates):
        rows = np.flatnonzero(dates == day)
        count = len(rows)
        lifted = rows[treated[rows]]
        if lifted.size == 0:
            continue
        rest = rows[~treated[rows]]
        band = int(np.clip(band_of(count, lifted.size), lifted.size, count))
        needed = band - lifted.size
        ordered = rest[np.argsort(out[rest], kind="stable")]
        promoted_rows = ordered[len(ordered) - needed:] if needed else ordered[:0]
        below = ordered[:len(ordered) - needed]
        inside = np.concatenate([promoted_rows, lifted])
        inside = inside[np.argsort(out[inside], kind="stable")]
        out[np.concatenate([below, inside])] = np.arange(count, dtype=np.float64)
    return out


def analyse(year: int) -> dict:
    # Deliberately NOT filtered. evaluate.py drops null labels for the IC and Top-excess terms
    # only, while the turnover term uses every row with flag_limit_up == 0; filtering here
    # changed the Top sets and inflated mean turnover by up to 0.244. The R0 anchor below must
    # reproduce the recorded baseline composite exactly, which is what proves the frame is right.
    frame = (pl.read_parquet(R4 / f"predictions_baseline_{year}.parquet")
             .sort("trade_date", "ts_code"))
    dates = frame["trade_date"].to_numpy()
    treated = frame["flag_limit_up"].to_numpy().astype(bool)
    base = frame["pred"].to_numpy().astype(np.float64)
    recorded = json.loads((R4 / f"result_{year}.json").read_text(encoding="utf-8-sig")
                          )["metrics"]["baseline"]
    rules = {"R0_unchanged": base,
             "R1_lift_to_top": promote(base, dates, treated, lambda n, t: t)}
    for band in BANDS:
        rules[f"R2_band_{band:.2f}"] = promote(base, dates, treated,
                                               lambda n, t, b=band: int(round((1.0 - b) * n)))
    entry = {"year": year, "days": int(len(np.unique(dates))), "rows": int(len(dates)),
             "rows_without_label": int(frame["y_ret_1d"].is_null().sum()),
             "limit_up_rows": int(treated.sum()),
             "limit_up_share": float(treated.mean()),
             "recorded_baseline": {k: float(v) for k, v in recorded.items()}, "rules": {}}
    for name, prediction in rules.items():
        metrics, daily = score_official(frame, prediction)
        if name == "R0_unchanged":
            anchor = max(abs(metrics[key] - recorded[key]) for key in recorded)
            if anchor > 1e-12:
                raise AssertionError(f"{year}: the unchanged baseline does not reproduce the "
                                     f"recorded composite (max diff {anchor:.3e}); every delta in "
                                     "this run would be meaningless")
            log(f"{year} R0 anchor reproduced {recorded['final_score']:.15f} exactly")
        daily.write_csv(OUT / f"daily_{name}_{year}.csv")
        item = {k: float(v) for k, v in metrics.items()}
        item["composite_delta"] = metrics["final_score"] - recorded["final_score"]
        item["ic_delta"] = metrics["ic_mean"] - recorded["ic_mean"]
        item["excess_delta"] = metrics["annual_excess"] - recorded["annual_excess"]
        item["turnover_delta"] = metrics["mean_turnover"] - recorded["mean_turnover"]
        entry["rules"][name] = item
        log(f"{year} {name}: score={metrics['final_score']:.9f} ({item['composite_delta']:+.9f}) "
            f"ic Δ={item['ic_delta']:+.6f} excess Δ={item['excess_delta']:+.3e} "
            f"turnover Δ={item['turnover_delta']:+.3e}")
    return entry


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    destination = OUT / "results.json"
    if destination.exists():
        raise SystemExit("Limit-up rule diagnostic already recorded; preserving it")
    started = time.monotonic()
    years = [analyse(year) for year in YEARS]
    headroom = json.loads((ROOT / "experiments/limit_up_channel_eval/headroom.json")
                          .read_text(encoding="utf-8"))
    summary = {}
    for name in years[0]["rules"]:
        deltas = [entry["rules"][name]["composite_delta"] for entry in years]
        summary[name] = {
            "composite_deltas": dict(zip([str(e["year"]) for e in years], deltas)),
            "mean_composite_delta": float(np.mean(deltas)),
            "worst_year_composite_delta": float(min(deltas)),
            "positive_years": int(sum(d > 0 for d in deltas)),
            "mean_ic_delta": float(np.mean([e["rules"][name]["ic_delta"] for e in years])),
            "max_abs_excess_delta": max(abs(e["rules"][name]["excess_delta"]) for e in years),
            "max_abs_turnover_delta": max(abs(e["rules"][name]["turnover_delta"]) for e in years),
            "top_terms_untouched": bool(
                max(abs(e["rules"][name]["excess_delta"]) for e in years) < 1e-12
                and max(abs(e["rules"][name]["turnover_delta"]) for e in years) < 1e-12),
            "share_of_oracle_headroom": float(np.mean(deltas) / headroom["mean_composite_headroom"]),
        }
    payload = {
        "stage": "limit_up_causal_rule", "generated_at_local": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "seconds": round(time.monotonic() - started, 2),
        "role": "Descriptive. No model trained, nothing fitted, no candidate scored.",
        "claim_under_test": "re-ordering only the limit-up rows leaves the Top-excess and turnover "
                            "terms bit-identical, so the composite moves by exactly 0.4 x the IC "
                            "change",
        "rules": {"R0_unchanged": "the frozen released baseline",
                  "R1_lift_to_top": "limit-up rows take exactly the day's top n_treated positions",
                  "R2_band_p": "limit-up rows sit inside the top (1-p) share of the day"},
        "bands": list(BANDS), "ic_weight": IC_WEIGHT,
        "oracle_headroom_reference": headroom["mean_composite_headroom"],
        "oracle_worst_year_reference": headroom["worst_year_headroom"],
        "years": years, "summary": summary,
        "input_sha256": {f"predictions_baseline_{year}.parquet":
                         hashlib.sha256((R4 / f"predictions_baseline_{year}.parquet").read_bytes()
                                        ).hexdigest() for year in YEARS},
        "caveats": [
            "Applied to the FINAL prediction, so it bypasses the released post-processing stack. "
            "Adopting it would change how the deliverable is constructed, and the stack's "
            "percentile coupling would have to be re-measured end to end.",
            "flag_limit_up for day t is supplied in the test file and is known when the day-t "
            "prediction is formed, so the rule is causal.",
            "The gain is IC-term alignment: limit-up stocks are excluded from the portfolio terms, "
            "so this raises the measured score without changing the portfolio those terms describe. "
            "It must be disclosed as metric alignment, not presented as a trading gain.",
            "The band grid is reported for every value; nothing here selects one on a gated year.",
        ],
    }
    destination.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\n{'rule':<16}{'mean Δscore':>13}{'worst year':>12}{'正年':>6}{'mean ΔIC':>11}"
          f"{'Top两项未变':>12}{'占oracle上限':>13}")
    for name, item in summary.items():
        print(f"{name:<16}{item['mean_composite_delta']:>+13.6f}"
              f"{item['worst_year_composite_delta']:>+12.6f}{item['positive_years']:>4}/5"
              f"{item['mean_ic_delta']:>+11.6f}"
              f"{('yes' if item['top_terms_untouched'] else 'NO'):>12}"
              f"{item['share_of_oracle_headroom']:>12.1%}")
    log(f"Wrote {destination}")


if __name__ == "__main__":
    main()
