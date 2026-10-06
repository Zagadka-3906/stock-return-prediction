"""Wave 15: push the orderer further - blend it, and re-tune its own post-processing.

Wave 13 closed two axes: the retention floor (m = 0.985 is the argmax with W5a ordering) and the
decoupling of the orderer's two roles (A = B = W5a is the argmax; no split helps). It also moved the
membership donor to the nested lift, giving 0.442481207. Two orderer-side axes are still unsearched.

Stage A - BLEND THE ORDERER. The orderer's turnover is irrelevant because it never chooses the Top
decile, so the usual reason to avoid averaging signals (it blurs a sharp portfolio) does not apply
here; only its ranking quality matters. Averaging two rankers normally beats both on rank IC. This
was never tried: every wave picked a single column as the orderer. Note this is a different thing from
the greedy ensemble of FINISHED pipelines that was already measured and rejected - those were scored
as standalone submissions, where averaging destroys turnover. Here the blend only ever supplies an
ordering.

Stage B - RE-TUNE THE ORDERER'S POST-PROCESSING. Wave 12 put every backbone through the orderer role
at alpha 0 / bonus 0 and W5a won, but alpha and bonus were the only two axes moved. The auxiliary blend
weight (0.25), the blend mode (top_only), the protected-block restoration switch and top_current_weight
were all inherited from the released stack and never varied for W5a. Wave 6 varied them for slow16 only.

The donor and the floor are frozen at wave 13's argmax so every arm here is directly comparable.

Harness proof before any new arm is scored: rebuilding W5a's raw fold column and pushing it through
make_prediction_param at the RELEASED settings must reproduce connected_pred_W5a_...npy bit-for-bit,
and at alpha 0 / bonus 0 must reproduce orderer_a0b0_W5a_...npy bit-for-bit. Both columns are frozen
artifacts scored by earlier waves, so this pins the rebuild.

Selection is 后续选模标准.md §3/§4: highest connected 2020-2024 official composite, no other gate.
No test-period data is read anywhere in this file.
"""
from __future__ import annotations

import gc
import hashlib
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
import connected_scorer as cs  # noqa: E402
from experiments.revalidate_fold_local import score_official  # noqa: E402
from optimize_wave6 import make_prediction_param, RELEASED  # noqa: E402
from optimize_wave13 import build_ab  # noqa: E402
from score_wave3 import discover, load_raw  # noqa: E402
from src.scoring import Panel  # noqa: E402

R4 = ROOT.parent / "赛题五_历史归档_20261001/experiments/revalidation_20260926/validation"
YEARS = cs.YEARS
TIE_EPS = 1e-9
M_FRAC = 0.985
DONOR = "connected_pred_hybrid.npy"
W5A_FINISHED = "W5a_five_way_with_gru__final_sweep_eval"
W5A_ORDERER = f"orderer_a0b0_{W5A_FINISHED}"
W5A_RAW_CACHE = HERE / "w5a_raw_fold.npy"
CURRENT_BEST = 0.4424812067218111
CURRENT_BEST_NAME = "nested_x_W5a_a0_b0_m0.985_tiebreak"
PARTNER_WEIGHTS = (0.25, 0.50, 0.75)
N_PARTNERS = 8

STAGE_B_GRID = [
    {"alpha": 0.0, "bonus": 0.0, "mode": "top_only", "weight": 0.0, "restore_lower": True,
     "top_current_weight": 1.0},
    {"alpha": 0.0, "bonus": 0.0, "mode": "top_only", "weight": 0.125, "restore_lower": True,
     "top_current_weight": 1.0},
    {"alpha": 0.0, "bonus": 0.0, "mode": "top_only", "weight": 0.50, "restore_lower": True,
     "top_current_weight": 1.0},
    {"alpha": 0.0, "bonus": 0.0, "mode": "top_only", "weight": 0.25, "restore_lower": False,
     "top_current_weight": 1.0},
    {"alpha": 0.0, "bonus": 0.0, "mode": "top_only", "weight": 0.25, "restore_lower": True,
     "top_current_weight": 0.5},
    {"alpha": 0.0, "bonus": 0.0, "mode": "top_only", "weight": 0.25, "restore_lower": True,
     "top_current_weight": 0.0},
    {"alpha": 0.0, "bonus": 0.0, "mode": "full_signal", "weight": 0.25, "restore_lower": True,
     "top_current_weight": 1.0},
    {"alpha": 0.0, "bonus": 0.0, "mode": "baseline", "weight": 0.0, "restore_lower": True,
     "top_current_weight": 1.0},
    {"alpha": 0.0, "bonus": 0.15, "mode": "top_only", "weight": 0.25, "restore_lower": True,
     "top_current_weight": 1.0},
    {"alpha": 0.0, "bonus": 0.30, "mode": "top_only", "weight": 0.25, "restore_lower": True,
     "top_current_weight": 1.0},
    {"alpha": 0.5, "bonus": 0.0, "mode": "top_only", "weight": 0.25, "restore_lower": True,
     "top_current_weight": 1.0},
    {"alpha": 0.0, "bonus": 0.0, "mode": "top_only", "weight": 0.25, "restore_lower": False,
     "top_current_weight": 0.0},
]


def sha(path) -> str:
    value = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for chunk in iter(lambda: stream.read(8 * 1024 * 1024), b""):
            value.update(chunk)
    return value.hexdigest()


def setting_tag(setting: dict) -> str:
    return (f"a{setting['alpha']:g}_b{setting['bonus']:g}_{setting['mode']}_w{setting['weight']:g}"
            f"_rl{int(setting['restore_lower'])}_tcw{setting['top_current_weight']:g}")


def daily_ranks(values: np.ndarray, valid: np.ndarray, dates: np.ndarray) -> np.ndarray:
    """Per-day cross-sectional average rank over the usable subset, sentinel -10 elsewhere.

    Same convention as final_sweep_wave3.ensemble_raw (average ranks, divided by the day's count), so a
    weighted blend of two columns is directly comparable to the seed averages that produced them.
    Rows are unusable when the price is invalid, the value is non-finite, or the value is the -10
    sentinel that every upstream stage writes for "no prediction".
    """
    out = np.full(len(values), -10.0, dtype=np.float64)
    keep = valid & np.isfinite(values) & (values > -9.0)
    if not keep.any():
        return out
    frame = pd.DataFrame({"d": dates[keep], "v": values[keep]})
    grouped = frame.groupby("d", sort=False)["v"]
    ranks = grouped.rank(method="average").to_numpy()
    counts = grouped.transform("size").to_numpy()
    out[keep] = ranks / counts
    return out


def weighted_rank_blend(columns: list[np.ndarray], weights: list[float], rank_cache: dict,
                        valid: np.ndarray, dates: np.ndarray, key: tuple) -> np.ndarray:
    total = float(sum(weights))
    acc = np.zeros(len(valid), dtype=np.float64)
    keep = valid.copy()
    for column, weight, k in zip(columns, weights, key):
        if k not in rank_cache:
            rank_cache[k] = daily_ranks(column, valid, dates)
        ranks = rank_cache[k]
        keep &= ranks > -9.0
        acc += (weight / total) * np.where(ranks > -9.0, ranks, 0.0)
    out = np.full(len(valid), -10.0, dtype=np.float64)
    out[keep] = acc[keep]
    return out


def w5a_raw_fold(frames: dict) -> np.ndarray:
    if W5A_RAW_CACHE.exists():
        return np.load(W5A_RAW_CACHE)
    families, singles = discover()
    target = None
    for (name, parent), by_year in singles.items():
        if f"{name}__{parent.name}" == W5A_FINISHED and all(y in by_year for y in YEARS):
            target = by_year
            break
    if target is None:
        raise SystemExit(f"no complete raw cache for {W5A_FINISHED}")
    parts = [load_raw(target[year], year, frames[year]) for year in YEARS]
    raw = np.concatenate(parts)
    np.save(W5A_RAW_CACHE, raw)
    cs.log(f"W5a raw fold column rebuilt and cached: {len(raw):,} rows, sha {sha(W5A_RAW_CACHE)[:16]}…")
    return raw


def main() -> None:
    protocol_path = HERE / "protocol_wave15.json"
    if not protocol_path.exists():
        protocol_path.write_text(json.dumps({
            "frozen_at_local": time.strftime("%Y-%m-%dT%H:%M:%S"),
            "standard": "后续选模标准.md §3 connected composite primary; §4 highest score wins",
            "status": "in_sample_selection_disclosed",
            "hypothesis": {
                "stageA": "the orderer never chooses the Top decile, so its turnover is irrelevant and "
                          "the usual cost of averaging signals does not apply. A weighted per-day rank "
                          "blend of W5a with another alpha 0 / bonus 0 backbone should beat W5a alone "
                          "on rank IC. This is NOT the greedy ensemble of finished pipelines already "
                          "measured and rejected - that was scored standalone, where averaging "
                          "destroys turnover.",
                "stageB": "wave 12 moved only alpha and bonus for the orderer role. The auxiliary "
                          "blend weight, the blend mode, the protected-block restoration switch and "
                          "top_current_weight were inherited from the released stack and never varied "
                          "for W5a.",
            },
            "donor_fixed": {"column": DONOR,
                            "construction": "wave 1's lift: promoted = top_sets(topk finished); "
                                            "out = promoted*(span+1) + peer67_slow16 finished",
                            "provenance": "wave 13 stage 2 argmax over 30 donors"},
            "m_frac_fixed_at": M_FRAC, "m_provenance": "wave 13 stage 1 argmax",
            "tie_break_eps": TIE_EPS,
            "stageA_partners": f"the {N_PARTNERS} highest-scoring alpha 0 / bonus 0 orderers from "
                               f"wave 12, at partner weights {list(PARTNER_WEIGHTS)}, plus the "
                               "equal-weight three-way blends of the top three",
            "stageB_grid": [setting_tag(s) for s in STAGE_B_GRID],
            "harness_proofs": {
                "P1": "W5a raw rebuilt from the frozen caches, through make_prediction_param at the "
                      f"RELEASED settings, must equal connected_pred_{W5A_FINISHED}.npy bit-for-bit",
                "P2": "the same raw at alpha 0 / bonus 0 must equal "
                      f"{W5A_ORDERER}.npy bit-for-bit",
            },
            "current_best_before_this_wave": {"name": CURRENT_BEST_NAME,
                                              "connected_final_score": CURRENT_BEST},
            "selection_rule": "highest connected 2020-2024 official composite; no significance, "
                              "worst-year or single-metric gate",
            "disclosed_selection_cost": "eleventh consecutive search over the same five viewed years; "
                                        "no blind period remains and the winner carries upward "
                                        "selection bias this protocol cannot quantify",
            "causality": "every orderer column is a walk-forward fold prediction; the per-day rank "
                         "blend reads only same-day predictions and the price-valid mask. No label is "
                         "read.",
            "no_test_period_data_read": True,
            "source_sha256": sha(Path(__file__)),
        }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        cs.log(f"wave-15 protocol frozen: {sha(protocol_path)[:16]}…")

    frames = {y: pl.read_parquet(R4 / f"predictions_ensemble4_{y}.parquet").sort("trade_date", "ts_code")
              for y in YEARS}
    combined = cs.combined_frame()
    dates = combined["trade_date"].to_numpy()
    flags = combined["flag_limit_up"].to_numpy().astype(np.int64)
    valid = combined["price_valid"].to_numpy().astype(bool)
    codes, uniques = pd.factorize(combined["ts_code"].to_pandas(), sort=True)
    codes = codes.astype(np.int64)
    n_codes = len(uniques)
    tie_key = 1.0 - codes / max(n_codes - 1, 1)
    member = np.load(HERE / DONOR)
    results: dict = {"stageA_blend": {}, "stageB_postprocess": {}}
    proofs: dict = {}

    # ---- harness proofs on the W5a raw rebuild
    raw = w5a_raw_fold(frames)
    parts_rel, parts_a0b0 = [], []
    for year in YEARS:
        frame = frames[year]
        panel = Panel.from_frame(frame.with_columns(
            pl.Series("pred_raw", raw[(dates >= year * 10000 + 101) & (dates <= year * 10000 + 1231)])))
        auxv = frame["aux_raw"].to_numpy().astype(np.float64)
        parts_rel.append(make_prediction_param(panel, auxv, RELEASED["mode"], RELEASED["weight"],
                                               RELEASED["alpha"], RELEASED["bonus"],
                                               RELEASED["restore_lower"],
                                               RELEASED["top_current_weight"]))
        parts_a0b0.append(make_prediction_param(panel, auxv, "top_only", 0.25, 0.0, 0.0, True, 1.0))
        del panel
        gc.collect()
    rebuilt_rel = np.concatenate(parts_rel)
    rebuilt_a0b0 = np.concatenate(parts_a0b0)
    frozen_rel = np.load(HERE / f"connected_pred_{W5A_FINISHED}.npy")
    frozen_a0b0 = np.load(HERE / f"{W5A_ORDERER}.npy")
    proofs["P1_released_settings"] = {
        "bit_identical": bool(np.array_equal(rebuilt_rel, frozen_rel)),
        "max_abs_diff": float(np.abs(rebuilt_rel - frozen_rel).max())}
    proofs["P2_alpha0_bonus0"] = {
        "bit_identical": bool(np.array_equal(rebuilt_a0b0, frozen_a0b0)),
        "max_abs_diff": float(np.abs(rebuilt_a0b0 - frozen_a0b0).max())}
    for name, proof in proofs.items():
        if not proof["bit_identical"]:
            raise AssertionError(f"{name} failed: max abs diff {proof['max_abs_diff']:.3e}")
        cs.log(f"{name} passed: bit-identical to the frozen column")

    def dump() -> list:
        arms = sorted(((v["connected_final_score"], k, v)
                       for bucket in results.values() for k, v in bucket.items()
                       if "connected_final_score" in v), reverse=True)
        payload = {"status": "running", "updated_at_local": time.strftime("%Y-%m-%dT%H:%M:%S"),
                   "purpose": "blend the orderer, and re-tune the orderer's own post-processing",
                   "donor_fixed": DONOR, "m_frac": M_FRAC, "tie_break_eps": TIE_EPS,
                   "harness_proofs": proofs,
                   "current_best_before_this_wave": {"name": CURRENT_BEST_NAME,
                                                     "connected_final_score": CURRENT_BEST},
                   "results": results, "n_scored": len(arms),
                   "ranking": [{"arm": k, "connected_final_score": s,
                                "ic_mean": v["connected_metrics"]["ic_mean"],
                                "annual_excess": v["connected_metrics"]["annual_excess"],
                                "mean_turnover": v["connected_metrics"]["mean_turnover"]}
                               for s, k, v in arms[:25]],
                   "best": arms[0][1] if arms else None,
                   "best_connected_final_score": arms[0][0] if arms else None,
                   "improves_on_current_best": bool(arms and arms[0][0] > CURRENT_BEST),
                   "no_test_period_data_read": True,
                   "source_sha256": sha(Path(__file__))}
        (HERE / "wave15_results.json").write_text(
            json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        return arms

    def score(name: str, bucket: str, orderer: np.ndarray, extra: dict) -> float:
        hybrid, stats = build_ab(member, orderer + TIE_EPS * tie_key, orderer + TIE_EPS * tie_key,
                                 dates, flags, codes, n_codes, M_FRAC)
        metrics, _ = score_official(combined, hybrid)
        results[bucket][name] = {**extra, "connected_final_score": metrics["final_score"],
                                 "connected_metrics": metrics,
                                 "boundary_tie_days": stats["boundary_tie_days"],
                                 "mean_retention_ratio": stats["mean_retention_ratio"],
                                 "beats_current_best": bool(metrics["final_score"] > CURRENT_BEST)}
        cs.log(f"{name[:62]:62s} CONNECTED {metrics['final_score']:.9f} "
               f"(ic {metrics['ic_mean']:.6f}, excess {metrics['annual_excess']:.6f}, "
               f"turn {metrics['mean_turnover']:.6f})")
        dump()
        return metrics["final_score"]

    # ---- stage A: weighted rank blends of W5a with the best other orderers
    wave12 = json.loads((HERE / "wave12_results.json").read_text(encoding="utf-8"))["results"]
    ranked12 = sorted(((v["connected_final_score"], f"orderer_a0b0_{k[:60]}")
                       for k, v in wave12.items() if "connected_final_score" in v), reverse=True)
    partners = [stem for _, stem in ranked12
                if stem != W5A_ORDERER and (HERE / f"{stem}.npy").exists()][:N_PARTNERS]
    cs.log(f"stage A partners: {len(partners)}")
    w5a = frozen_a0b0
    rank_cache: dict = {W5A_ORDERER: daily_ranks(w5a, valid, dates)}
    for stem in partners:
        other = np.load(HERE / f"{stem}.npy")
        for w in PARTNER_WEIGHTS:
            blend = weighted_rank_blend([w5a, other], [1.0 - w, w], rank_cache, valid, dates,
                                        (W5A_ORDERER, stem))
            score(f"W5a+{w:g}x{stem[len('orderer_a0b0_'):]}", "stageA_blend", blend,
                  {"components": [W5A_ORDERER, stem], "weights": [1.0 - w, w]})
    top3 = [w5a] + [np.load(HERE / f"{s}.npy") for s in partners[:2]]
    names3 = [W5A_ORDERER] + partners[:2]
    score("equal_three_way:" + "+".join(n[len("orderer_a0b0_"):] for n in names3), "stageA_blend",
          weighted_rank_blend(top3, [1.0, 1.0, 1.0], rank_cache, valid, dates, tuple(names3)),
          {"components": names3, "weights": [1 / 3] * 3})

    # ---- stage B: W5a's own post-processing
    for setting in STAGE_B_GRID:
        tag = setting_tag(setting)
        name = f"W5a__{tag}"
        try:
            parts = []
            for year in YEARS:
                frame = frames[year]
                mask = (dates >= year * 10000 + 101) & (dates <= year * 10000 + 1231)
                panel = Panel.from_frame(frame.with_columns(pl.Series("pred_raw", raw[mask])))
                parts.append(make_prediction_param(
                    panel, frame["aux_raw"].to_numpy().astype(np.float64), setting["mode"],
                    setting["weight"], setting["alpha"], setting["bonus"], setting["restore_lower"],
                    setting["top_current_weight"]))
                del panel
                gc.collect()
            column = np.concatenate(parts)
            np.save(HERE / f"orderer_b_{tag}.npy", column)
            score(name, "stageB_postprocess", column, {"setting": setting})
        except BaseException as error:  # noqa: BLE001
            results["stageB_postprocess"][name] = {"setting": setting,
                                                   "error": f"{type(error).__name__}: {error}"}
            cs.log(f"{name[:62]:62s} FAILED {type(error).__name__}: {error}")
            dump()

    arms = dump()
    payload = json.loads((HERE / "wave15_results.json").read_text(encoding="utf-8"))
    payload["status"] = "complete"
    payload["completed_at_local"] = time.strftime("%Y-%m-%dT%H:%M:%S")
    (HERE / "wave15_results.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print("\n| rank | arm | CONNECTED | IC | excess | turnover |")
    print("|---|---|---|---|---|---|")
    for i, (s, name, v) in enumerate(arms[:20]):
        m = v["connected_metrics"]
        print(f"| {i+1} | {name[:66]} | **{s:.9f}** | {m['ic_mean']:.6f} | "
              f"{m['annual_excess']:.6f} | {m['mean_turnover']:.6f} |")
    cs.log(f"best: {arms[0][1] if arms else None} {arms[0][0] if arms else 0:.9f} "
           f"({'IMPROVES' if arms and arms[0][0] > CURRENT_BEST else 'does not improve'})")


if __name__ == "__main__":
    main()
