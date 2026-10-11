"""Retrospective test-period check of the two in-sample tuning wins, for 后续选模标准.md §5.

§5 requires reporting SEPARATELY (a) the scheme the validation caliber selected and (b) the scheme that
actually scored best on the test period. This computes (b) for the two gains the search produced, so
each can be seen next to its training-window gain:

  wave 6  post-processing retune   alpha 0.9 / bonus 0.3  ->  alpha 0.8 / bonus 0.6
          training gain +0.002817
  wave 7b retention floor          m = 0  ->  m = 0.985 on the same donor pair
          training gain +0.002092

Both are rebuilt here from artifacts that exist on disk, and the released-settings version of each is
required to reproduce its already-recorded test-period score before the re-tuned version is believed.

This uses the locally reconstructed test labels, which 后续选模标准.md §2 forbids for selection. It is
run AFTER the validation-caliber selection was made, purely to produce the §5(b) disclosure, and it
feeds back into nothing.
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd
import polars as pl

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(HERE))
from src.scoring import Panel  # noqa: E402
from experiments.revalidate_fold_local import score_official  # noqa: E402
from optimize_wave6 import make_prediction_param  # noqa: E402
from analysis.official_score_contributions import composite  # noqa: E402

ARCHIVE = ROOT.parent / "赛题五_历史归档_20261001"
DELIVERY = ARCHIVE / "deliveries/peer67_slow16_20260929"
AUX = ARCHIVE / "releases/pooled_rms25/auxiliary_raw.parquet"
HOLDOUT = ARCHIVE / "analysis/frozen_holdout_20260928/data"
KEYS = ["ts_code", "trade_date"]
CUTOFF = 20260605
RELEASED = {"alpha": 0.9, "bonus": 0.3, "restore_lower": True, "top_current_weight": 1.0,
            "mode": "top_only", "weight": 0.25}
RETUNED = {**RELEASED, "alpha": 0.8, "bonus": 0.6}
EXPECTED_RELEASED_TEST = 0.386058


def log(message: str) -> None:
    print(f"[{time.strftime('%H:%M:%S')}] {message}", flush=True)


def main() -> None:
    prediction = pl.read_parquet(DELIVERY / "prediction.parquet")
    aux = pl.read_parquet(AUX)
    if not aux.select(KEYS).equals(prediction.select(KEYS)):
        raise AssertionError("auxiliary_raw and the delivery prediction frame are not row-aligned")
    prediction = (prediction
                  .with_columns(aux["pred_raw"].cast(pl.Float64).alias("aux_raw"))
                  .with_columns(pl.col("flag_limit_up").cast(pl.Int64)))
    for column in ("pred_raw", "aux_raw", "flag_limit_up", "price_valid"):
        if column not in prediction.columns:
            raise SystemExit(f"delivery prediction.parquet lacks {column}")
    log(f"test frame: {len(prediction):,} rows, {prediction['trade_date'].n_unique()} days")

    # Panel requires a label column; supplying an all-null one also proves the stack never reads
    # labels. The stronger proof is that this must reproduce the delivery's own rank_score column -
    # the post-processing output, of which the shipped `pred` is exactly
    # np.where(rank_score < -1, -0.05, 0.04 * (rank_score - 0.5)), verified bit-for-bit.
    shipped = prediction["rank_score"].to_numpy().astype(np.float64)
    affine = np.where(shipped < -1, -0.05, 0.04 * (shipped - 0.5))
    if not np.array_equal(affine, prediction["pred"].to_numpy().astype(np.float64)):
        raise AssertionError("the shipped pred is not the documented affine map of rank_score")
    prediction = prediction.with_columns(pl.lit(None, dtype=pl.Float64).alias("y_ret_1d"))
    panel = Panel.from_frame(prediction)
    aux_values = prediction["aux_raw"].to_numpy().astype(np.float64)
    rebuilt = make_prediction_param(panel, aux_values, RELEASED["mode"], RELEASED["weight"],
                                    RELEASED["alpha"], RELEASED["bonus"], RELEASED["restore_lower"],
                                    RELEASED["top_current_weight"])
    if not np.array_equal(rebuilt, shipped):
        raise AssertionError(f"the parameterized stack does not reproduce the shipped rank_score "
                             f"column (max diff {np.abs(rebuilt - shipped).max():.3e}), so it is not "
                             f"the same pipeline")
    log("causality + pipeline proof passed: rebuilding from pred_raw with null labels reproduces the "
        "shipped rank_score element-for-element, and pred is its affine map")

    # scoring frame: the delivery frame's own key order, truncated to the 343 labelled days, with the
    # reconstructed labels joined on. Building it this way avoids assuming any particular row order.
    mask = (prediction["trade_date"] <= CUTOFF).to_numpy()
    labels = pl.from_pandas(pd.read_csv(HOLDOUT / "测试集_Y.csv"))
    scoring = (prediction.filter(pl.Series(mask)).select(KEYS + ["flag_limit_up"])
               .join(labels.select(KEYS + ["y_ret_1d"]), on=KEYS, how="left"))
    if len(scoring) != int(mask.sum()):
        raise AssertionError(f"label join changed the row count: {len(scoring)} vs {int(mask.sum())}")
    n_labelled = int(scoring["y_ret_1d"].is_not_null().sum())
    log(f"scoring frame: {len(scoring):,} rows, {scoring['trade_date'].n_unique()} days, "
        f"{n_labelled:,} with a reconstructed label")
    if scoring["trade_date"].n_unique() != 343:
        raise AssertionError(f"expected 343 labelled days, got {scoring['trade_date'].n_unique()}")

    results = {}
    for label, setting in (("released_a0.9_b0.3", RELEASED), ("retuned_a0.8_b0.6", RETUNED)):
        pred = make_prediction_param(panel, aux_values, setting["mode"], setting["weight"],
                                     setting["alpha"], setting["bonus"], setting["restore_lower"],
                                     setting["top_current_weight"])
        if not np.isfinite(pred).all():
            raise AssertionError(f"{label}: non-finite prediction")
        metrics, daily = score_official(scoring, pred[mask])
        daily_pd = daily.to_pandas()
        results[label] = {
            "setting": setting, "test_period_score_343_days": metrics["final_score"],
            "metrics": metrics,
            "segments": {"2025": composite(daily_pd[daily_pd.trade_date < 20260101]),
                         "2026": composite(daily_pd[daily_pd.trade_date >= 20260101])},
        }
        log(f"{label}: test-period {metrics['final_score']:.9f} (ic {metrics['ic_mean']:.6f}, "
            f"excess {metrics['annual_excess']:.6f}, turnover {metrics['mean_turnover']:.6f})")

    diff = abs(results["released_a0.9_b0.3"]["test_period_score_343_days"] - EXPECTED_RELEASED_TEST)
    if diff > 1e-6:
        raise AssertionError(f"released settings gave "
                             f"{results['released_a0.9_b0.3']['test_period_score_343_days']:.9f}, "
                             f"expected {EXPECTED_RELEASED_TEST} (diff {diff:.3e})")
    log(f"anchor passed: the released post-processing reproduces the recorded test-period score "
        f"{EXPECTED_RELEASED_TEST} (diff {diff:.1e})")

    training_gain = 0.430224705 - 0.427407938
    test_change = (results["retuned_a0.8_b0.6"]["test_period_score_343_days"]
                   - results["released_a0.9_b0.3"]["test_period_score_343_days"])
    payload = {
        "status": "complete", "completed_at_local": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "purpose": "后续选模标准.md §5(b) - the retrospective test-period comparison, produced after "
                   "the validation-caliber selection and feeding back into nothing",
        "may_not_be_used_for_selection": True,
        "anchor": {"released_settings_expected": EXPECTED_RELEASED_TEST,
                   "released_settings_got":
                       results["released_a0.9_b0.3"]["test_period_score_343_days"],
                   "abs_diff": diff, "passed": bool(diff <= 1e-6)},
        "results": results,
        "postprocessing_retune": {
            "training_window_gain": training_gain, "test_period_change": test_change,
            "transfers": bool(test_change > 0),
            "reading": "positive means the retune helps on the period that will actually be scored; "
                       "negative means the training-window gain was window-specific",
        },
        "retention_floor": {
            "training_window_gain": 0.434034593 - 0.431942948,
            "test_period_change": 0.409885766 - 0.415424964,
            "transfers": False,
            "source": "build_final_submission.py runs at m=0 and m=0.985 on the same donor pair",
        },
        "top_set_substitution_mechanism": {
            "confirmed_model_test_score": EXPECTED_RELEASED_TEST,
            "best_hybrid_test_score_no_retention_floor": 0.415424964,
            "gain": 0.415424964 - EXPECTED_RELEASED_TEST,
            "reading": "the mechanism itself, with no tuned retention floor",
        },
    }
    (HERE / "retrospective_test_comparison.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"\npost-processing retune: training {training_gain:+.6f} | test period "
          f"{test_change:+.6f} -> {'transfers' if test_change > 0 else 'DOES NOT transfer'}")
    print(f"retention floor m=0.985: training {0.434034593-0.431942948:+.6f} | test period "
          f"{0.409885766-0.415424964:+.6f} -> DOES NOT transfer")
    print(f"Top-set substitution alone: test period {0.415424964-EXPECTED_RELEASED_TEST:+.6f} "
          f"over the confirmed model")


if __name__ == "__main__":
    main()
