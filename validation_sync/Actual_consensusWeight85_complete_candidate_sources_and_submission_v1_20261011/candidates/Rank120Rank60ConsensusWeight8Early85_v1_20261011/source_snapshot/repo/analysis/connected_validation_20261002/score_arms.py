"""Re-score the recoverable arms under the connected 2020-2024 caliber required by 后续选模标准.md.

Every arm gets identical treatment: the same combined fold frame, the same unmodified evaluate.py, the
same five validation years, and its own frozen annual composites asserted first so that a mismatch in
the reconstruction can never be mistaken for a result. No test-period data is read anywhere.

Arms rebuilt here from surviving caches:
  peer67_slow16  the confirmed model, 16 seeds, rebuilt from the 80 per-seed raw caches
  peer67_slow8   the same recipe with the delivered 8-seed subset
  topk           the LightGBM Top-K return-weighted pairwise backbone, frozen fold predictions
  hybrid         Top-decile membership from topk, ordering from peer67_slow16
"""
from __future__ import annotations

import gc
import json
import sys
import time
from pathlib import Path

import numpy as np
import polars as pl

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "analysis"))
from experiments.revalidate_fold_local import score_official  # noqa: E402
from analysis.connected_validation_20261002 import connected_scorer as cs  # noqa: E402
from analysis.topset_hybrid_20261002 import fold_validation as fv  # noqa: E402

YEARS = cs.YEARS
POOL16 = tuple(range(2026, 2042))
DELIVERED8 = tuple(range(2026, 2034))

FROZEN_ANNUAL = {
    "peer67_slow16": ({2020: 0.432158406, 2021: 0.424889700, 2022: 0.444829865,
                       2023: 0.418670801, 2024: 0.420366222}, 2e-9),
    "peer67_slow8": ({2020: 0.43088073116524317, 2021: 0.4239262375157104,
                      2022: 0.4447744734170406, 2023: 0.4191728780576189,
                      2024: 0.4196001207358905}, 1e-12),
    "topk": ({2020: 0.40707290913686545, 2021: 0.4152844359357778, 2022: 0.42089053197633397,
              2023: 0.403864650, 2024: 0.430983374}, 1e-9),
}


def seed_average(frame: pl.DataFrame, seeds, rank_average_n) -> np.ndarray:
    """Equal-weight per-day cross-sectional rank average, then the released stack with per-fold aux."""
    year = int(frame["trade_date"].min() // 10000)
    raws = []
    for seed in seeds:
        path = fv.RAW16 / f"raw_deployed67_slow_seed{seed}_{year}.parquet"
        if not path.exists():
            raise SystemExit(f"missing seed cache: {path.name}")
        raws.append(pl.read_parquet(path).sort("trade_date", "ts_code")["pred_raw"].to_numpy())
    days = frame["trade_date"].n_unique()
    codes = len(frame) // days
    assert len(frame) == days * codes
    averaged = rank_average_n(raws, frame["grid_price_valid"].to_numpy(), codes)
    from src.scoring import Panel
    from experiments.cached_recheck import make_prediction
    panel = Panel.from_frame(frame.with_columns(pl.Series("pred_raw", averaged)))
    return make_prediction(panel, frame["aux_raw"].to_numpy().astype(np.float64), "top_only", 0.25)


def hybrid_pred(pdf, a_final: np.ndarray, b_final: np.ndarray) -> tuple[np.ndarray, float]:
    promoted, stats = fv.top_sets(pdf, b_final)
    if stats["boundary_tie_days"]:
        raise AssertionError(f"arm B has {stats['boundary_tie_days']} Top-boundary tie days")
    span = float(a_final.max() - a_final.min())
    out = promoted.astype(np.float64) * (span + 1.0) + a_final
    promoted_out, _ = fv.top_sets(pdf, out)
    if not np.array_equal(promoted_out, promoted):
        raise AssertionError("the hybrid's Top set is not exactly arm B's")
    return out, promoted.mean()


def main() -> None:
    frame = cs.combined_frame()
    rank_average_n = fv.load_rank_average_n()
    dates = frame["trade_date"].to_numpy()
    year_masks = {y: (dates >= y * 10000 + 101) & (dates <= y * 10000 + 1231) for y in YEARS}

    connected_pred: dict[str, list[np.ndarray]] = {}
    annual: dict[str, dict[int, dict]] = {}
    key_order_ok = True

    for year in YEARS:
        yf = fv.fold_frame(year)
        # the per-year frame must line up with this year's slice of the combined frame
        combined_keys = frame.filter(pl.Series(year_masks[year])).select(cs.KEYS)
        if not yf.select(cs.KEYS).equals(combined_keys):
            key_order_ok = False
            raise AssertionError(f"{year}: per-year frame keys do not match the combined slice")
        pdf = yf.select(["trade_date", "flag_limit_up"]).to_pandas()

        a16 = seed_average(yf, POOL16, rank_average_n)
        a8 = seed_average(yf, DELIVERED8, rank_average_n)
        b = pl.read_parquet(fv.topk_predictions(year)).sort("trade_date", "ts_code")
        assert b.select(cs.KEYS).equals(yf.select(cs.KEYS)), f"{year}: topk keys misaligned"
        b_final = b["pred"].to_numpy().astype(np.float64)
        h, promoted_share = hybrid_pred(pdf, a16, b_final)

        for name, pred in (("peer67_slow16", a16), ("peer67_slow8", a8), ("topk", b_final),
                           ("hybrid", h)):
            metrics, _ = score_official(yf, pred)
            annual.setdefault(name, {})[year] = metrics
            connected_pred.setdefault(name, []).append(pred)
        cs.log(f"{year}: scored 4 arms; hybrid promoted {promoted_share*100:.2f}% of rows")
        del yf, pdf, a16, a8, b, b_final, h
        gc.collect()

    assert key_order_ok
    results = {}
    for name, parts in connected_pred.items():
        pred = np.concatenate(parts)
        assert len(pred) == len(frame)
        started = time.monotonic()
        connected, _ = score_official(frame, pred)
        five_year_mean = float(np.mean([annual[name][y]["final_score"] for y in YEARS]))

        calibration = {}
        if name in FROZEN_ANNUAL:
            frozen, tol = FROZEN_ANNUAL[name]
            for y in YEARS:
                got = annual[name][y]["final_score"]
                calibration[str(y)] = {"recomputed": got, "frozen": frozen[y],
                                       "abs_diff": abs(got - frozen[y])}
                assert abs(got - frozen[y]) <= tol, \
                    f"{name}/{y}: {got!r} vs frozen {frozen[y]!r} (tol {tol})"
            cs.log(f"{name}: all five annual composites reproduce their frozen values")

        results[name] = {
            "connected_final_score": connected["final_score"],
            "connected_metrics": connected,
            "annual_final_scores": {str(y): annual[name][y]["final_score"] for y in YEARS},
            "annual_metrics": {str(y): annual[name][y] for y in YEARS},
            "five_year_equal_weight_mean_diagnostic_only": five_year_mean,
            "connected_minus_five_year_mean": connected["final_score"] - five_year_mean,
            "annual_calibration": calibration,
            "connected_seconds": round(time.monotonic() - started, 1),
        }
        cs.log(f"{name}: CONNECTED {connected['final_score']:.9f} | five-year mean "
               f"{five_year_mean:.9f} | delta {connected['final_score']-five_year_mean:+.9f}")
        np.save(HERE / f"connected_pred_{name}.npy", pred)

    ranked = sorted(results.items(), key=lambda kv: -kv[1]["connected_final_score"])
    payload = {
        "status": "complete", "completed_at_local": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "caliber": "connected 2020-2024 out-of-sample series scored once by the unmodified "
                   "evaluate.py; turnover continuous across year boundaries (1211 observations "
                   "instead of 1207)",
        "standard": "后续选模标准.md §3 - the connected composite is the primary score; the "
                    "five-year equal-weight mean is diagnostic only",
        "no_test_period_data_read": True,
        "frame": {"rows": len(frame), "days": int(frame["trade_date"].n_unique()),
                  "sha256": cs.sha(cs.FRAME_CACHE)},
        "turnover_accounting": cs.turnover_accounting(frame),
        "results": results,
        "ranking_by_connected_score": [
            {"rank": i + 1, "name": name, "connected_final_score": r["connected_final_score"],
             "five_year_mean_diagnostic": r["five_year_equal_weight_mean_diagnostic_only"],
             "delta_connected_minus_mean": r["connected_minus_five_year_mean"]}
            for i, (name, r) in enumerate(ranked)],
    }
    (HERE / "connected_results_wave1.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print("\n| rank | arm | CONNECTED 2020-2024 | 5y mean (diagnostic) | delta |")
    print("|---|---|---|---|---|")
    for i, (name, r) in enumerate(ranked):
        print(f"| {i+1} | {name} | **{r['connected_final_score']:.9f}** | "
              f"{r['five_year_equal_weight_mean_diagnostic_only']:.9f} | "
              f"{r['connected_minus_five_year_mean']:+.9f} |")
    print("\n| arm | " + " | ".join(str(y) for y in YEARS) + " |")
    print("|---|" + "---|" * 6)
    for name, r in ranked:
        print(f"| {name} | " + " | ".join(f"{r['annual_final_scores'][str(y)]:.6f}" for y in YEARS)
              + " |")


if __name__ == "__main__":
    main()
