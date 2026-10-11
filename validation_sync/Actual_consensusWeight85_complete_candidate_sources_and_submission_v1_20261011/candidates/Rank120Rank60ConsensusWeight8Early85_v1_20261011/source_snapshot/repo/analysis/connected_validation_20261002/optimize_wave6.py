"""Wave 6: sweep the post-processing stack on the connected caliber. No training, cache-only.

Why this is now admissible: the alpha/bonus/auxiliary-weight axes were closed by wave-4 and wave-8
suite B on a DEV/CONFIRM TRANSFER argument - parameters chosen on 2020-2021 did not transfer to
2022-2024. 后续选模标准.md §4 removes transfer, significance, worst-year and years-positive as
elimination criteria and makes the connected 2020-2024 official composite the sole objective. Under
that rule the post-processing parameters are simply free knobs of the final output scheme, and §3
explicitly says the comparison is of FINAL output schemes including smoothing and post-processing.

The cost is stated plainly: this is direct in-sample maximization over five viewed years, so the
winner's score is upward-biased by the search and no blind period remains to measure that bias.

Harness proof first: at the released settings (alpha 0.9, bonus 0.3, restore_lower True,
top_current_weight 1.0, top_only auxiliary weight 0.25) the parameterized stack must reproduce the
frozen peer67_slow16 annual composites AND its saved connected prediction column bit-for-bit. Only
then is any other setting scored.
"""
from __future__ import annotations

import argparse
import gc
import hashlib
import itertools
import json
import sys
import time
import traceback
from pathlib import Path

import numpy as np
import polars as pl
from scipy.stats import rankdata

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(HERE))
import connected_scorer as cs  # noqa: E402
from src.scoring import Panel, add_top_persistence, make_scores, postprocess_scores  # noqa: E402
from experiments.revalidate_fold_local import score_official  # noqa: E402
from experiments.cached_recheck import make_prediction  # noqa: E402

ARCHIVE = ROOT.parent / "赛题五_历史归档_20261001"
CLEANUP = ROOT.parent / "赛题五_清理备份_20261001"
R4 = ARCHIVE / "experiments/revalidation_20260926/validation"
RAW16 = CLEANUP / "experiments/wave23_validation_20260928"
YEARS = cs.YEARS
KEYS = cs.KEYS
POOL16 = tuple(range(2026, 2042))
RELEASED = {"alpha": 0.9, "bonus": 0.3, "restore_lower": True, "top_current_weight": 1.0,
            "mode": "top_only", "weight": 0.25}
EXPECTED_ANNUAL = {2020: 0.432158406, 2021: 0.424889700, 2022: 0.444829865,
                   2023: 0.418670801, 2024: 0.420366222}
TOL = 2e-9

ALPHAS = (0.0, 0.50, 0.80, 0.85, 0.90, 0.95, 0.97)
BONUSES = (0.0, 0.15, 0.30, 0.45, 0.60)
AUX_WEIGHTS = (0.0, 0.125, 0.25, 0.50)
TOP_CURRENT_WEIGHTS = (0.0, 0.50, 1.0)


def sha(path) -> str:
    value = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for chunk in iter(lambda: stream.read(8 * 1024 * 1024), b""):
            value.update(chunk)
    return value.hexdigest()


def make_prediction_param(panel: Panel, auxiliary_raw, mode: str, weight: float, alpha: float,
                          bonus: float, restore_lower: bool, top_current_weight: float) -> np.ndarray:
    """Verbatim mirror of experiments.cached_recheck.make_prediction with BASE_CONFIG parameterized."""
    cfg = {"alpha": alpha, "bonus": bonus, "restore_lower": restore_lower,
           "top_current_weight": top_current_weight}
    if not np.isfinite(weight) or not 0 <= weight <= 1:
        raise ValueError("weight must be in [0, 1]")
    base_raw = panel.frame["pred_raw"].to_numpy().astype(np.float64)
    if mode == "baseline":
        return postprocess_scores(panel, base_raw, **cfg)
    if auxiliary_raw is None:
        raise ValueError("auxiliary required")
    auxiliary_raw = np.asarray(auxiliary_raw, dtype=np.float64)
    if auxiliary_raw.size != base_raw.size:
        raise ValueError("auxiliary size mismatch")
    if mode == "pure":
        return postprocess_scores(panel, auxiliary_raw, **cfg)
    from src.postprocessing import daily_percentiles
    if mode == "full_signal":
        mixed = ((1 - weight) * daily_percentiles(panel, base_raw)
                 + weight * daily_percentiles(panel, auxiliary_raw))
        return postprocess_scores(panel, mixed, **cfg)
    if mode != "top_only":
        raise ValueError(f"unknown mode {mode}")
    out = postprocess_scores(panel, base_raw, **cfg).reshape(panel.valid_price.shape)
    stable = add_top_persistence(panel, make_scores(panel, base_raw, alpha),
                                 bonus).reshape(panel.valid_price.shape)
    base_raw = base_raw.reshape(panel.valid_price.shape)
    auxiliary_raw = auxiliary_raw.reshape(panel.valid_price.shape)
    for day in range(len(panel.dates)):
        valid = panel.valid_price[day] & np.isfinite(base_raw[day])
        indices = np.flatnonzero(panel.up[day] == 0)
        n_top = max(len(indices) // 10, 1)
        if not len(indices) or not valid.any():
            continue
        top = indices[np.argsort(-stable[day, indices], kind="stable")[:n_top]]
        if not valid[top].all():
            continue
        protected = valid & (stable[day] >= stable[day, top].min())
        if np.count_nonzero(protected & (panel.up[day] == 0)) != n_top:
            continue
        if not np.isfinite(auxiliary_raw[day, protected]).all():
            continue
        n_upper = int(protected.sum())
        base_rank = rankdata(base_raw[day, protected], method="average") / n_upper
        auxiliary_rank = rankdata(auxiliary_raw[day, protected], method="average") / n_upper
        blended_rank = rankdata((1 - weight) * base_rank + weight * auxiliary_rank, method="average")
        n_valid = int(valid.sum())
        out[day, protected] = (n_valid - n_upper + blended_rank) / n_valid
    return out.reshape(-1)


def fold_frame(year: int) -> pl.DataFrame:
    frame = pl.read_parquet(R4 / f"predictions_ensemble4_{year}.parquet").sort("trade_date", "ts_code")
    grid = (pl.scan_parquet(ROOT / "data/features.parquet")
            .filter(pl.col("is_train") & pl.col("trade_date").is_between(year * 10000 + 101,
                                                                        year * 10000 + 1231))
            .select(KEYS + ["price_valid"]).sort("trade_date", "ts_code").collect())
    if not grid.select(KEYS).equals(frame.select(KEYS)):
        raise AssertionError(f"{year}: grid keys misaligned")
    return frame.with_columns(grid["price_valid"].alias("grid_price_valid"))


def raw_average(frame: pl.DataFrame, rank_average_n) -> np.ndarray:
    year = int(frame["trade_date"].min() // 10000)
    raws = [pl.read_parquet(RAW16 / f"raw_deployed67_slow_seed{s}_{year}.parquet")
            .sort("trade_date", "ts_code")["pred_raw"].to_numpy() for s in POOL16]
    days = frame["trade_date"].n_unique()
    codes = len(frame) // days
    return rank_average_n(raws, frame["grid_price_valid"].to_numpy(), codes)


def settings_grid() -> list[dict]:
    """alpha x bonus full grid at the released auxiliary settings, plus one-at-a-time moves on the
    auxiliary weight, top_current_weight and restore_lower at the released alpha/bonus."""
    out = []
    for alpha, bonus in itertools.product(ALPHAS, BONUSES):
        out.append({"alpha": alpha, "bonus": bonus, "restore_lower": True,
                    "top_current_weight": 1.0, "mode": "top_only", "weight": 0.25})
    for weight in AUX_WEIGHTS:
        out.append({**RELEASED, "weight": weight})
    for tcw in TOP_CURRENT_WEIGHTS:
        out.append({**RELEASED, "top_current_weight": tcw})
    out.append({**RELEASED, "restore_lower": False, "top_current_weight": 0.0})
    for mode in ("baseline", "full_signal"):
        out.append({**RELEASED, "mode": mode})
    unique, seen = [], set()
    for setting in out:
        key = tuple(sorted(setting.items()))
        if key not in seen:
            seen.add(key)
            unique.append(setting)
    return unique


def label(setting: dict) -> str:
    return (f"a{setting['alpha']:g}_b{setting['bonus']:g}_{setting['mode']}"
            f"_w{setting['weight']:g}_rl{int(setting['restore_lower'])}"
            f"_tcw{setting['top_current_weight']:g}")


def prove(bundles, rank_average_n) -> dict:
    """The parameterized stack must equal the frozen one bit-for-bit at the released settings."""
    reference = np.load(HERE / "connected_pred_peer67_slow16.npy")
    parts = []
    annual = {}
    for year in YEARS:
        frame, raw = bundles[year]
        pred = make_prediction_param(Panel.from_frame(frame.with_columns(pl.Series("pred_raw", raw))),
                                     frame["aux_raw"].to_numpy().astype(np.float64),
                                     RELEASED["mode"], RELEASED["weight"], RELEASED["alpha"],
                                     RELEASED["bonus"], RELEASED["restore_lower"],
                                     RELEASED["top_current_weight"])
        frozen = make_prediction(Panel.from_frame(frame.with_columns(pl.Series("pred_raw", raw))),
                                 frame["aux_raw"].to_numpy().astype(np.float64),
                                 RELEASED["mode"], RELEASED["weight"])
        if not np.array_equal(pred, frozen):
            raise AssertionError(f"{year}: parameterized stack differs from the frozen implementation")
        metrics, _ = score_official(frame, pred)
        diff = abs(metrics["final_score"] - EXPECTED_ANNUAL[year])
        if diff > TOL:
            raise AssertionError(f"{year}: {metrics['final_score']!r} vs frozen {EXPECTED_ANNUAL[year]!r}")
        annual[str(year)] = {"recomputed": metrics["final_score"], "frozen": EXPECTED_ANNUAL[year],
                             "abs_diff": diff}
        parts.append(pred)
        del pred, frozen
        gc.collect()
    connected = np.concatenate(parts)
    if not np.array_equal(connected, reference):
        raise AssertionError("connected column differs from the saved peer67_slow16 reference")
    cs.log("harness proof PASSED: parameterized stack is bit-identical to the frozen implementation "
           "and reproduces all five annual composites and the saved connected column")
    return {"passed": True, "annual": annual,
            "connected_bit_identical_to_saved_reference": True}


def freeze() -> None:
    grid = settings_grid()
    payload = {
        "frozen_at_local": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "standard": "后续选模标准.md §3 connected composite is primary; §4 removes transfer, "
                    "significance, worst-year and years-positive as elimination criteria; the "
                    "comparison is of final output schemes including smoothing and post-processing",
        "status": "in_sample_maximization_disclosed",
        "backbone": "peer67_slow16 raw equal-weight per-day rank average over seeds 2026-2041, "
                    "rebuilt from the 80 surviving per-seed caches",
        "released_settings": RELEASED,
        "parameterized_implementation": "make_prediction_param mirrors "
                                        "experiments.cached_recheck.make_prediction with BASE_CONFIG "
                                        "exposed; identity at the released settings is asserted "
                                        "bit-for-bit before any other setting is scored",
        "grid": {"alpha": list(ALPHAS), "bonus": list(BONUSES), "aux_weight": list(AUX_WEIGHTS),
                 "top_current_weight": list(TOP_CURRENT_WEIGHTS),
                 "modes": ["top_only", "baseline", "full_signal"],
                 "design": "full alpha x bonus grid at the released auxiliary settings, plus "
                           "one-at-a-time moves on auxiliary weight, top_current_weight, "
                           "restore_lower and mode",
                 "n_settings": len(grid),
                 "settings": [label(s) for s in grid]},
        "selection_rule": "highest connected 2020-2024 official composite; ties broken by proximity "
                          "to the released settings, then simplicity",
        "disclosed_selection_cost": f"{len(grid)} settings are maximized over five repeatedly viewed "
                                    "years. The winner's score is upward-biased by the search and no "
                                    "blind period remains to quantify that bias. This is exactly the "
                                    "dev/confirm transfer failure wave-4 and wave-8 recorded, now "
                                    "accepted deliberately because the standard removed that gate.",
        "harness_proof_required_first": True,
        "no_test_period_data_read": True,
        "source_sha256": sha(Path(__file__)),
    }
    if (HERE / "protocol_wave6.json").exists():
        raise FileExistsError("protocol already frozen")
    (HERE / "protocol_wave6.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    cs.log(f"wave-6 protocol frozen: {len(grid)} post-processing settings")


def run() -> None:
    protocol = json.loads((HERE / "protocol_wave6.json").read_text(encoding="utf-8"))
    assert protocol["source_sha256"] == sha(Path(__file__)), "script changed after freezing"
    sys.path.insert(0, str(ROOT / "analysis"))
    from analysis.topset_hybrid_20261002 import fold_validation as fv
    rank_average_n = fv.load_rank_average_n()

    bundles = {}
    for year in YEARS:
        frame = fold_frame(year)
        bundles[year] = (frame, raw_average(frame, rank_average_n))
        cs.log(f"{year}: fold frame {len(frame):,} rows, raw rank average rebuilt")
    proof = prove(bundles, rank_average_n)
    (HERE / "wave6_harness_proof.json").write_text(
        json.dumps(proof, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    frame_all = cs.combined_frame()
    results = {}
    for setting in settings_grid():
        name = label(setting)
        if name in results:
            continue
        try:
            parts = []
            for year in YEARS:
                frame, raw = bundles[year]
                panel = Panel.from_frame(frame.with_columns(pl.Series("pred_raw", raw)))
                parts.append(make_prediction_param(
                    panel, frame["aux_raw"].to_numpy().astype(np.float64), setting["mode"],
                    setting["weight"], setting["alpha"], setting["bonus"],
                    setting["restore_lower"], setting["top_current_weight"]))
                del panel
                gc.collect()
            pred = np.concatenate(parts)
            if not np.isfinite(pred).all():
                raise AssertionError("non-finite prediction")
            started = time.monotonic()
            metrics, _ = score_official(frame_all, pred)
            results[name] = {"setting": setting, "connected_final_score": metrics["final_score"],
                             "connected_metrics": metrics,
                             "is_released": setting == RELEASED,
                             "seconds": round(time.monotonic() - started, 1)}
            np.save(HERE / f"pp_{name}.npy", pred)
            cs.log(f"{name}: CONNECTED {metrics['final_score']:.9f} (ic {metrics['ic_mean']:.6f}, "
                   f"excess {metrics['annual_excess']:.6f}, turnover {metrics['mean_turnover']:.6f})"
                   f"{'  <-- released' if setting == RELEASED else ''}")
            del parts, pred
            gc.collect()
        except Exception as error:
            results[name] = {"setting": setting, "error": f"{type(error).__name__}: {error}"}
            cs.log(f"{name}: FAILED {type(error).__name__}: {error}")

    scored = {k: v for k, v in results.items() if "connected_final_score" in v}
    ranked = sorted(scored.items(), key=lambda kv: -kv[1]["connected_final_score"])
    released_score = next(v["connected_final_score"] for v in scored.values() if v["is_released"])
    payload = {"status": "complete", "completed_at_local": time.strftime("%Y-%m-%dT%H:%M:%S"),
               "protocol_sha256": sha(HERE / "protocol_wave6.json"),
               "harness_proof": proof, "results": results,
               "released_connected_score": released_score,
               "best": ranked[0][0], "best_connected_final_score": ranked[0][1]["connected_final_score"],
               "best_gain_over_released": ranked[0][1]["connected_final_score"] - released_score,
               "n_scored": len(scored), "n_failed": len(results) - len(scored),
               "no_test_period_data_read": True}
    (HERE / "wave6_results.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"\nreleased settings connected score: {released_score:.9f}")
    print(f"\n| rank | setting | CONNECTED | IC | excess | turnover | vs released |")
    print("|---|---|---|---|---|---|---|")
    for i, (name, v) in enumerate(ranked[:20]):
        m = v["connected_metrics"]
        print(f"| {i+1} | {name} | **{m['final_score']:.9f}** | {m['ic_mean']:.6f} | "
              f"{m['annual_excess']:.6f} | {m['mean_turnover']:.6f} | "
              f"{m['final_score']-released_score:+.6f} |")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("stage", choices=("freeze", "run"))
    args = parser.parse_args()
    try:
        globals()[args.stage]()
    except Exception as error:
        (HERE / f"failure_wave6_{args.stage}_{time.time_ns()}.json").write_text(
            json.dumps({"stage": args.stage, "type": type(error).__name__, "message": str(error),
                        "traceback": traceback.format_exc()}, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8")
        raise
