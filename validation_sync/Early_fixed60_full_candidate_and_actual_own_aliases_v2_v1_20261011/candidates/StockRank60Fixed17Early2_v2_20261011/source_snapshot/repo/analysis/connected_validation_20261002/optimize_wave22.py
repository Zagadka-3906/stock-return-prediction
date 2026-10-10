"""Wave 22: blend at the RAW level instead of the post-processed level.

Every blend so far (waves 15, 16, 20) averaged two already-post-processed columns. The released stack is
nonlinear - an EMA across days, a stratified bonus, protected-block restoration, then a 25% pooled
top-only blend - so blending first and post-processing afterwards is a DIFFERENT function, and nothing
in the record says the two agree. This tests it directly, on the same donor, floor and tie-break as the
selection, so every arm is comparable to 0.443190552.

Also tested: a three-way raw blend that adds topk. topk is the membership donor's promote source, so it
is already known to carry Top-decile information the two tree/GRU ensembles lack; whether it also helps
the ordering is a separate question and has never been asked.

Harness proofs, all run before any new arm is scored:
  P1  W5a raw through make_prediction_param at alpha 0 / bonus 0 must reproduce the frozen
      orderer_a0b0_W5a column bit-for-bit (wave 15 proved this; re-asserted because this wave rebuilds
      the raw pipeline itself)
  P2  the raw blend at partner weight 0 must score exactly what W5a alone scores (0.442481207). This is
      the real test of the raw path: the blend emits per-day normalized ranks rather than W5a's own raw
      values, and post-processing only reads the daily ordering, so the score must be unchanged. If it
      is not, the sentinel handling in daily_ranks disagrees with the panel's price_valid mask and the
      whole wave is meaningless.
  P3  the post-processed blend at weight 0.25 must reproduce 0.443190552, pinning the comparison.

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
from optimize_wave6 import make_prediction_param, fold_frame, raw_average  # noqa: E402
from optimize_wave8 import topk_raw  # noqa: E402
from optimize_wave13 import build_ab  # noqa: E402
from optimize_wave15 import daily_ranks, weighted_rank_blend, DONOR, M_FRAC, TIE_EPS  # noqa: E402
from src.scoring import Panel  # noqa: E402

YEARS = cs.YEARS
W5A_A0B0 = "orderer_a0b0_W5a_five_way_with_gru__final_sweep_eval.npy"
SLOW16_A0B0 = "pp_a0_b0_top_only_w0.25_rl1_tcw1.npy"
W5A_RAW_CACHE = HERE / "w5a_raw_fold.npy"
SETTING = {"alpha": 0.0, "bonus": 0.0, "mode": "top_only", "weight": 0.25,
           "restore_lower": True, "top_current_weight": 1.0}
WEIGHTS = (0.15, 0.20, 0.25, 0.30, 0.50)
REF_W5A_ALONE = 0.4424812067218111
REF_POST_BLEND = 0.44319055217888365


def sha(path) -> str:
    value = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for chunk in iter(lambda: stream.read(8 * 1024 * 1024), b""):
            value.update(chunk)
    return value.hexdigest()


def main() -> None:
    protocol_path = HERE / "protocol_wave22.json"
    if not protocol_path.exists():
        protocol_path.write_text(json.dumps({
            "frozen_at_local": time.strftime("%Y-%m-%dT%H:%M:%S"),
            "standard": "后续选模标准.md §3 connected composite primary; §4 highest score wins",
            "status": "in_sample_selection_disclosed",
            "hypothesis": "the released post-processing stack is nonlinear (EMA across days, stratified "
                          "bonus, protected-block restoration, 25% pooled top-only blend), so blending "
                          "two raws and then post-processing is a different function from post-processing "
                          "each and then blending. Waves 15/16/20 only ever did the latter.",
            "donor_fixed": {"column": DONOR, "provenance": "wave 13 stage 2 argmax"},
            "m_frac_fixed_at": M_FRAC, "tie_break_eps": TIE_EPS,
            "arms": {
                "two_way_raw": f"rank-blend(W5a raw, slow16 raw) at partner weights {list(WEIGHTS)}, "
                               "then the stack at alpha 0 / bonus 0",
                "three_way_raw": "the same plus topk raw as a third member, at equal and weighted mixes",
                "post_blend_reference": "the shipped construction, for comparison at identical weights",
            },
            "harness_proofs": {
                "P1": "W5a raw through the stack at alpha 0 / bonus 0 reproduces the frozen "
                      "orderer_a0b0_W5a column bit-for-bit",
                "P2": f"the raw blend at partner weight 0 scores exactly {REF_W5A_ALONE}, which is what "
                      "validates feeding per-day normalized ranks into the stack in place of raw values",
                "P3": f"the post-processed blend at weight 0.25 reproduces {REF_POST_BLEND}",
            },
            "current_best_before_this_wave": REF_POST_BLEND,
            "selection_rule": "highest connected 2020-2024 official composite; no other gate",
            "disclosed_selection_cost": "search over the same five repeatedly viewed years; no blind "
                                        "period remains",
            "causality": "the blend reads only same-day raw predictions and the price-valid mask; the "
                         "stack reads only past predictions, past limit-up flags and the frozen pooled "
                         "auxiliary. No label is read.",
            "no_test_period_data_read": True,
            "source_sha256": sha(Path(__file__)),
        }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        cs.log(f"wave-22 protocol frozen: {sha(protocol_path)[:16]}…")

    sys.path.insert(0, str(ROOT / "analysis"))
    from analysis.topset_hybrid_20261002 import fold_validation as fv
    rank_average_n = fv.load_rank_average_n()

    frames = {y: fold_frame(y) for y in YEARS}
    combined = cs.combined_frame()
    dates = combined["trade_date"].to_numpy()
    flags = combined["flag_limit_up"].to_numpy().astype(np.int64)
    valid = combined["price_valid"].to_numpy().astype(bool)
    codes, uniques = pd.factorize(combined["ts_code"].to_pandas(), sort=True)
    codes = codes.astype(np.int64)
    n_codes = len(uniques)
    tie_key = 1.0 - codes / max(n_codes - 1, 1)
    member = np.load(HERE / DONOR)
    year_masks = {y: (dates >= y * 10000 + 101) & (dates <= y * 10000 + 1231) for y in YEARS}

    # ---- raw materials
    w5a_raw = np.load(W5A_RAW_CACHE) if W5A_RAW_CACHE.exists() else None
    if w5a_raw is None:
        raise SystemExit("run optimize_wave15.py first; w5a_raw_fold.npy is missing")
    slow16_parts, topk_parts = [], []
    for year in YEARS:
        frame = frames[year]
        slow16_parts.append(raw_average(frame, rank_average_n))
        _, raw = topk_raw(year)
        if len(raw) != len(frame):
            raise AssertionError(f"topk {year}: {len(raw)} rows vs frame {len(frame)}")
        topk_parts.append(raw)
    slow16_raw = np.concatenate(slow16_parts)
    topk_raw_all = np.concatenate(topk_parts)
    for name, array in (("W5a", w5a_raw), ("slow16", slow16_raw), ("topk", topk_raw_all)):
        if len(array) != len(combined):
            raise AssertionError(f"{name} raw has {len(array)} rows, combined frame has {len(combined)}")
        cs.log(f"raw {name:7s}: sentinel rows {int((array == -10.0).sum()):7d}, "
               f"finite {int(np.isfinite(array).sum()):8d}")

    def postprocess(raw_column: np.ndarray) -> np.ndarray:
        parts = []
        for year in YEARS:
            frame = frames[year]
            panel = Panel.from_frame(frame.with_columns(
                pl.Series("pred_raw", raw_column[year_masks[year]])))
            parts.append(make_prediction_param(
                panel, frame["aux_raw"].to_numpy().astype(np.float64), SETTING["mode"],
                SETTING["weight"], SETTING["alpha"], SETTING["bonus"], SETTING["restore_lower"],
                SETTING["top_current_weight"]))
            del panel
            gc.collect()
        return np.concatenate(parts)

    results: dict = {}
    proofs: dict = {}

    def dump() -> list:
        arms = sorted(((v["connected_final_score"], k, v) for k, v in results.items()
                       if "connected_final_score" in v), reverse=True)
        payload = {"status": "running", "updated_at_local": time.strftime("%Y-%m-%dT%H:%M:%S"),
                   "purpose": "blend at the raw level instead of the post-processed level",
                   "donor_fixed": DONOR, "m_frac": M_FRAC, "tie_break_eps": TIE_EPS,
                   "orderer_postprocess": SETTING, "harness_proofs": proofs,
                   "current_best_before_this_wave": REF_POST_BLEND,
                   "results": results, "n_scored": len(arms),
                   "ranking": [{"arm": k, "connected_final_score": s,
                                "ic_mean": v["connected_metrics"]["ic_mean"],
                                "annual_excess": v["connected_metrics"]["annual_excess"],
                                "mean_turnover": v["connected_metrics"]["mean_turnover"]}
                               for s, k, v in arms[:25]],
                   "best": arms[0][1] if arms else None,
                   "best_connected_final_score": arms[0][0] if arms else None,
                   "improves_on_current_best": bool(arms and arms[0][0] > REF_POST_BLEND),
                   "no_test_period_data_read": True,
                   "source_sha256": sha(Path(__file__))}
        (HERE / "wave22_results.json").write_text(
            json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        return arms

    def score(name: str, orderer: np.ndarray, extra: dict) -> float:
        hybrid, stats = build_ab(member, orderer + TIE_EPS * tie_key, orderer + TIE_EPS * tie_key,
                                 dates, flags, codes, n_codes, M_FRAC)
        metrics, _ = score_official(combined, hybrid)
        results[name] = {**extra, "connected_final_score": metrics["final_score"],
                         "connected_metrics": metrics, "boundary_tie_days": stats["boundary_tie_days"],
                         "mean_retention_ratio": stats["mean_retention_ratio"],
                         "beats_current_best": bool(metrics["final_score"] > REF_POST_BLEND)}
        cs.log(f"{name[:58]:58s} CONNECTED {metrics['final_score']:.9f} "
               f"(ic {metrics['ic_mean']:.6f}, excess {metrics['annual_excess']:.6f}, "
               f"turn {metrics['mean_turnover']:.6f})")
        dump()
        return metrics["final_score"]

    # ---- P1: the raw pipeline reproduces the frozen W5a orderer column
    rebuilt = postprocess(w5a_raw)
    frozen = np.load(HERE / W5A_A0B0)
    proofs["P1_w5a_raw_pipeline"] = {"bit_identical": bool(np.array_equal(rebuilt, frozen)),
                                     "max_abs_diff": float(np.abs(rebuilt - frozen).max())}
    if not np.array_equal(rebuilt, frozen):
        raise AssertionError(f"P1 failed: max abs diff "
                             f"{proofs['P1_w5a_raw_pipeline']['max_abs_diff']:.3e}")
    cs.log("P1 passed: W5a raw through the stack reproduces the frozen orderer column bit-for-bit")

    # ---- the blend helper, and P2 at weight 0
    cache: dict = {}

    def raw_blend(columns: list[np.ndarray], names: list[str], weights: list[float]) -> np.ndarray:
        for n, c in zip(names, columns):
            if n not in cache:
                cache[n] = daily_ranks(c, valid, dates)
        return weighted_rank_blend(columns, weights, cache, valid, dates, tuple(names))

    zero = postprocess(raw_blend([w5a_raw], ["w5a"], [1.0]))
    got2 = score("P2_raw_w0", zero, {"kind": "raw_blend", "members": ["W5a"], "weights": [1.0],
                                     "role": "harness_proof"})
    proofs["P2_raw_weight_zero"] = {"scored": got2, "expected": REF_W5A_ALONE,
                                    "abs_diff": abs(got2 - REF_W5A_ALONE)}
    if abs(got2 - REF_W5A_ALONE) > 1e-12:
        raise AssertionError(f"P2 failed: raw blend at weight 0 scored {got2!r}, expected "
                             f"{REF_W5A_ALONE!r} - the raw path does not reduce to W5a alone")
    cs.log("P2 passed: the raw path at partner weight 0 reproduces W5a alone exactly")

    # ---- P3: the shipped post-processed blend
    w5a_pp = frozen
    slow16_pp = np.load(HERE / SLOW16_A0B0)
    post_ref = weighted_rank_blend([w5a_pp, slow16_pp], [0.75, 0.25], {}, valid, dates,
                                   ("w5a_pp", "slow16_pp"))
    post_ref = np.where(post_ref > -9.0, post_ref + TIE_EPS * tie_key, post_ref)
    got3 = score("P3_post_blend_w0.25", post_ref,
                 {"kind": "post_blend", "members": ["W5a@a0b0", "slow16@a0b0"],
                  "weights": [0.75, 0.25], "role": "harness_proof"})
    proofs["P3_post_blend_reference"] = {"scored": got3, "expected": REF_POST_BLEND,
                                         "abs_diff": abs(got3 - REF_POST_BLEND)}
    if abs(got3 - REF_POST_BLEND) > 1e-12:
        raise AssertionError(f"P3 failed: {got3!r} vs {REF_POST_BLEND!r}")
    cs.log("P3 passed: the shipped post-processed blend reproduces 0.443190552")

    # ---- two-way raw blends
    for w in WEIGHTS:
        raw = raw_blend([w5a_raw, slow16_raw], ["w5a", "slow16"], [1.0 - w, w])
        score(f"raw2_w{w:g}", postprocess(raw),
              {"kind": "raw_blend", "members": ["W5a", "slow16"], "weights": [1.0 - w, w]})
        # the post-processed comparison at the same weight, so the two are read side by side
        post = weighted_rank_blend([w5a_pp, slow16_pp], [1.0 - w, w], {}, valid, dates,
                                   ("w5a_pp", "slow16_pp"))
        post = np.where(post > -9.0, post + TIE_EPS * tie_key, post)
        score(f"post2_w{w:g}", post,
              {"kind": "post_blend", "members": ["W5a@a0b0", "slow16@a0b0"],
               "weights": [1.0 - w, w]})

    # ---- three-way raw blends adding topk
    for w in (0.15, 0.25):
        for wt in (0.10, 0.20):
            raw = raw_blend([w5a_raw, slow16_raw, topk_raw_all], ["w5a", "slow16", "topk"],
                            [1.0 - w - wt, w, wt])
            score(f"raw3_w{w:g}_topk{wt:g}", postprocess(raw),
                  {"kind": "raw_blend", "members": ["W5a", "slow16", "topk"],
                   "weights": [1.0 - w - wt, w, wt]})
    raw_eq = raw_blend([w5a_raw, slow16_raw, topk_raw_all], ["w5a", "slow16", "topk"],
                       [1.0, 1.0, 1.0])
    score("raw3_equal", postprocess(raw_eq),
          {"kind": "raw_blend", "members": ["W5a", "slow16", "topk"], "weights": [1 / 3] * 3})

    arms = dump()
    payload = json.loads((HERE / "wave22_results.json").read_text(encoding="utf-8"))
    payload["status"] = "complete"
    payload["completed_at_local"] = time.strftime("%Y-%m-%dT%H:%M:%S")
    (HERE / "wave22_results.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print("\n| rank | arm | kind | CONNECTED | IC | excess | turnover |")
    print("|---|---|---|---|---|---|---|")
    for i, (s, name, v) in enumerate(arms[:20]):
        m = v["connected_metrics"]
        print(f"| {i+1} | {name[:34]} | {v['kind']} | **{s:.9f}** | {m['ic_mean']:.6f} | "
              f"{m['annual_excess']:.6f} | {m['mean_turnover']:.6f} |")
    cs.log(f"best: {arms[0][1] if arms else None} {arms[0][0] if arms else 0:.9f} "
           f"({'IMPROVES' if arms and arms[0][0] > REF_POST_BLEND else 'does not improve'})")


if __name__ == "__main__":
    main()
