"""Wave 20: the final cross, restricted to components whose test-period reconstruction is PROVEN bit-exact.

Three levers survived waves 12-19 and they act on different parts of the composite:
  donor     wave 18 variant b, lift(topk promotes, rank-blend(slow16, W5a, 0.25) re-ranks): +0.000232
  orderer   wave 16, W5a@alpha0/bonus0 blended with a second backbone at a low partner weight: +0.000728
  swap rule wave 17, choose the swapped names by the orderer instead of the donor: +0.000131 alone, but
            wave 19 shows it does NOT stack with the blended orderer, so it is dropped here

This crosses the donor lever with the orderer lever over a short m grid, and then applies one filter that
the earlier waves did not: **every component must have a test-period reconstruction that was proved
bit-exact against a frozen artifact.** Two candidates fail that filter and are excluded here rather than
discovered to be unshippable after selection:

  * wave 16's overall winner blends W5a with `raw_peer67_lr0025_360__wave22_additivity_20260928`
    (0.443209042). That family's fold raws live in `experiments/wave22_additivity_20260928/`, while the
    test-period peer67 predictions come from `candidates/peer67_lr0025_360` via `late/pipeline.py`. They
    are plausibly the same recipe, but there is no overlapping artifact to prove it, and discover() also
    showed the family label COLLIDES across two preserved trees (7 seeds in 清理备份_20261001, 1 seed in
    历史归档_20261001), so even the fold-side identity is ambiguous. Excluded.
  * Its margin over the shippable runner-up is 1.8e-5 - two orders of magnitude below this project's
    0.001743 refit noise floor. The exclusion costs nothing measurable.

What is admitted, and the proof behind each:
  W5a@alpha0/bonus0   reconstruct_w5a_test.py: released stack over the rebuilt raw == row 138, 0.0e+00
  slow16@alpha0/bonus0  build_selected_submission.py proof 1: released stack over the delivery's own
                      pred_raw == its shipped rank_score, element-for-element; and
                      orderer_a0b0_raw_deployed67_slow__wave23 is bit-identical to
                      pp_a0_b0_top_only_w0.25_rl1_tcw1 (max diff 0.0), so this partner IS slow16
  nested donor        reconstruct_nested_donor.py: lift rebuilt per year == connected_pred_hybrid.npy,
                      0.0e+00
  donor variant b     the same lift function over finished columns that all exist for the test period

Harness proof: the cell (donor a, orderer W5a alone, m = 0.985) must reproduce 0.442481207 and the cell
(donor a, orderer W5a+0.25*slow16, m = 0.985) must reproduce wave 16's 0.443190552.

Selection is 后续选模标准.md §3/§4 restricted to shippable arms: highest connected 2020-2024 official
composite. No test-period data is read anywhere in this file.
"""
from __future__ import annotations

import hashlib
import json
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(HERE))
import connected_scorer as cs  # noqa: E402
from experiments.revalidate_fold_local import score_official  # noqa: E402
from optimize_wave13 import build_ab  # noqa: E402
from optimize_wave15 import daily_ranks, weighted_rank_blend, TIE_EPS  # noqa: E402
from optimize_wave18 import lift  # noqa: E402

SLOW16_FIN = "connected_pred_peer67_slow16.npy"
TOPK_FIN = "connected_pred_topk.npy"
W5A_FIN = "connected_pred_W5a_five_way_with_gru__final_sweep_eval.npy"
W5A_A0B0 = "orderer_a0b0_W5a_five_way_with_gru__final_sweep_eval.npy"
SLOW16_A0B0 = "pp_a0_b0_top_only_w0.25_rl1_tcw1.npy"
NESTED = "connected_pred_hybrid.npy"
M_GRID = (0.985, 0.988)
DONOR_WEIGHTS = (0.25, 0.50)
PARTNER_WEIGHTS = (0.15, 0.20, 0.25, 0.30)


def frozen_reference() -> tuple[float, float]:
    """Both harness targets, read from the records that produced them rather than retyped.

    The first run of this wave failed its own P2 by comparing against 0.443190552, a value copied from
    a log line and therefore truncated; the recorded value is 0.44319055217888365. Reading the numbers
    back from wave13_results.json and wave16_results.json removes that class of failure.
    """
    w13 = json.loads((HERE / "wave13_results.json").read_text(encoding="utf-8"))
    donor_a = float(w13["results"]["stage2_donor"]["hybrid"]["connected_final_score"])
    w16 = json.loads((HERE / "wave16_results.json").read_text(encoding="utf-8"))
    target = ("W5a+0.25xraw_deployed67_slow__wave23_validation_20260928",
              "w0.25__raw_deployed67_slow__wave23_validation_20260928")
    blend = None
    for bucket in w16["results"].values():
        for key, value in bucket.items():
            if key in target and "connected_final_score" in value:
                blend = float(value["connected_final_score"])
    if blend is None:
        raise SystemExit(f"wave 16 recorded no arm named {target}")
    return donor_a, blend


REF_DONOR_A, REF_ORDERER_BLEND = frozen_reference()


def sha(path) -> str:
    value = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for chunk in iter(lambda: stream.read(8 * 1024 * 1024), b""):
            value.update(chunk)
    return value.hexdigest()


def main() -> None:
    protocol_path = HERE / "protocol_wave20.json"
    if not protocol_path.exists():
        protocol_path.write_text(json.dumps({
            "frozen_at_local": time.strftime("%Y-%m-%dT%H:%M:%S"),
            "standard": "后续选模标准.md §3 connected composite primary; §4 highest score wins, "
                        "restricted here to arms whose every component has a bit-exact proved "
                        "test-period reconstruction (§5 requires a shippable frozen scheme)",
            "status": "in_sample_selection_disclosed",
            "hypothesis": "the donor lever (wave 18 variant b, +0.000232) and the orderer-blend lever "
                          "(wave 16, +0.000728) act on different terms and were each searched with the "
                          "other held fixed, so cross them",
            "levers_dropped": {"swap_rule": "wave 19 showed it does not stack with a blended orderer"},
            "excluded_as_unshippable": {
                "raw_peer67_lr0025_360__wave22_additivity_20260928":
                    "no overlapping artifact proves the fold family equals the test-side "
                    "candidates/peer67_lr0025_360, and the family label collides across two preserved "
                    "trees with different seed counts; its margin over the shippable runner-up is "
                    "1.8e-5, two orders of magnitude below the 0.001743 refit noise floor"},
            "donors": {"a_nested_shipped": "lift(topk promotes, slow16 re-ranks)",
                       "b_rerank_blend": "lift(topk promotes, rank-blend(slow16, W5a, w) re-ranks), "
                                         "w in the donor-weight grid"},
            "donor_weight_grid": list(DONOR_WEIGHTS),
            "orderers": {"w5a_alone": "W5a @ alpha 0 / bonus 0",
                         "w5a_plus_slow16": "per-day rank blend, partner weight in the grid"},
            "m_grid": list(M_GRID), "tie_break_eps": TIE_EPS,
            "harness_proofs": {
                "P1": f"donor a x W5a alone x m=0.985 must reproduce {REF_DONOR_A}",
                "P2": f"donor a x W5a+0.25*slow16 x m=0.985 must reproduce {REF_ORDERER_BLEND}",
            },
            "selection_rule": "highest connected 2020-2024 official composite among shippable arms",
            "disclosed_selection_cost": "search over the same five repeatedly viewed years; no blind "
                                        "period remains and the winner carries upward selection bias "
                                        "this protocol cannot quantify",
            "causality": "the lift and the blend read only same-day finished predictions, same-day "
                         "limit-up flags and the price-valid mask. No label is read.",
            "no_test_period_data_read": True,
            "source_sha256": sha(Path(__file__)),
        }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        cs.log(f"wave-20 protocol frozen: {sha(protocol_path)[:16]}…")

    frame = cs.combined_frame()
    dates = frame["trade_date"].to_numpy()
    flags = frame["flag_limit_up"].to_numpy().astype(np.int64)
    valid = frame["price_valid"].to_numpy().astype(bool)
    codes, uniques = pd.factorize(frame["ts_code"].to_pandas(), sort=True)
    codes = codes.astype(np.int64)
    n_codes = len(uniques)
    tie_key = 1.0 - codes / max(n_codes - 1, 1)
    pdf = frame.select(["trade_date", "flag_limit_up"]).to_pandas()

    slow16_fin = np.load(HERE / SLOW16_FIN)
    topk_fin = np.load(HERE / TOPK_FIN)
    w5a_fin = np.load(HERE / W5A_FIN)
    w5a_a0b0 = np.load(HERE / W5A_A0B0)
    slow16_a0b0 = np.load(HERE / SLOW16_A0B0)
    nested = np.load(HERE / NESTED)

    rank_cache: dict = {}

    def blend(a: np.ndarray, b: np.ndarray, na: str, nb: str, w: float) -> np.ndarray:
        for stem, col in ((na, a), (nb, b)):
            if stem not in rank_cache:
                rank_cache[stem] = daily_ranks(col, valid, dates)
        mixed = weighted_rank_blend([a, b], [1.0 - w, w], rank_cache, valid, dates, (na, nb))
        return np.where(mixed > -9.0, mixed + TIE_EPS * tie_key, mixed)

    results: dict = {}
    proofs: dict = {}

    def dump() -> list:
        arms = sorted(((v["connected_final_score"], k, v) for k, v in results.items()
                       if "connected_final_score" in v), reverse=True)
        payload = {"status": "running", "updated_at_local": time.strftime("%Y-%m-%dT%H:%M:%S"),
                   "purpose": "final cross of the donor and orderer levers over shippable components "
                              "only",
                   "tie_break_eps": TIE_EPS, "m_grid": list(M_GRID), "harness_proofs": proofs,
                   "results": results, "n_scored": len(arms),
                   "ranking": [{"arm": k, "connected_final_score": s,
                                "ic_mean": v["connected_metrics"]["ic_mean"],
                                "annual_excess": v["connected_metrics"]["annual_excess"],
                                "mean_turnover": v["connected_metrics"]["mean_turnover"]}
                               for s, k, v in arms[:25]],
                   "best": arms[0][1] if arms else None,
                   "best_connected_final_score": arms[0][0] if arms else None,
                   "no_test_period_data_read": True,
                   "source_sha256": sha(Path(__file__))}
        (HERE / "wave20_results.json").write_text(
            json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        return arms

    def score(name: str, donor: np.ndarray, orderer: np.ndarray, m_frac: float, extra: dict) -> float:
        hybrid, stats = build_ab(donor, orderer + TIE_EPS * tie_key, orderer + TIE_EPS * tie_key,
                                 dates, flags, codes, n_codes, m_frac)
        metrics, _ = score_official(frame, hybrid)
        results[name] = {**extra, "m_frac": m_frac,
                         "connected_final_score": metrics["final_score"],
                         "connected_metrics": metrics,
                         "boundary_tie_days": stats["boundary_tie_days"],
                         "eligibility_limited_days": stats["eligibility_limited_days"],
                         "swaps": stats["swaps"],
                         "mean_retention_ratio": stats["mean_retention_ratio"]}
        cs.log(f"{name[:62]:62s} CONNECTED {metrics['final_score']:.9f} "
               f"(ic {metrics['ic_mean']:.6f}, excess {metrics['annual_excess']:.6f}, "
               f"turn {metrics['mean_turnover']:.6f})")
        dump()
        return metrics["final_score"]

    # ---- harness proofs against two frozen numbers
    donor_a, stats_a = lift(topk_fin, slow16_fin, pdf)
    proofs["P0_donor_a_is_the_frozen_nested"] = {
        "bit_identical": bool(np.array_equal(donor_a, nested)),
        "max_abs_diff": float(np.abs(donor_a - nested).max()), "lift_stats": stats_a}
    if not np.array_equal(donor_a, nested):
        raise AssertionError("harness proof failed: the rebuilt nested donor is not "
                             "connected_pred_hybrid.npy")
    orderer_blend_ref = blend(w5a_a0b0, slow16_a0b0, W5A_A0B0, SLOW16_A0B0, 0.25)
    got1 = score("P1_donorA_x_W5a_m0.985", donor_a, w5a_a0b0, 0.985,
                 {"donor": "a_nested_shipped", "orderer": "W5a@a0b0", "role": "harness_proof"})
    proofs["P1"] = {"scored": got1, "expected": REF_DONOR_A, "abs_diff": abs(got1 - REF_DONOR_A)}
    if abs(got1 - REF_DONOR_A) > 1e-12:
        raise AssertionError(f"P1 failed: {got1!r} vs {REF_DONOR_A!r}")
    got2 = score("P2_donorA_x_W5a0.25slow16_m0.985", donor_a, orderer_blend_ref, 0.985,
                 {"donor": "a_nested_shipped", "orderer": "W5a+0.25*slow16", "role": "harness_proof"})
    proofs["P2"] = {"scored": got2, "expected": REF_ORDERER_BLEND,
                    "abs_diff": abs(got2 - REF_ORDERER_BLEND)}
    if abs(got2 - REF_ORDERER_BLEND) > 1e-12:
        raise AssertionError(f"P2 failed: {got2!r} vs {REF_ORDERER_BLEND!r}")
    cs.log(f"harness proofs passed: {got1:.9f} and {got2:.9f} reproduce the frozen numbers")

    # ---- the cross
    for w in DONOR_WEIGHTS:
        donor_b, _ = lift(topk_fin, blend(slow16_fin, w5a_fin, SLOW16_FIN, W5A_FIN, w), pdf)
        for ow in PARTNER_WEIGHTS:
            orderer = blend(w5a_a0b0, slow16_a0b0, W5A_A0B0, SLOW16_A0B0, ow)
            for m_frac in M_GRID:
                score(f"donorB_w{w:g}__ord_w{ow:g}__m{m_frac:g}", donor_b, orderer, m_frac,
                      {"donor": f"b_rerank_blend_w{w:g}", "orderer": f"W5a+{ow:g}*slow16",
                       "shippable": True})
        # donor b with W5a alone as the orderer, to separate the two levers
        for m_frac in M_GRID:
            score(f"donorB_w{w:g}__ord_w0__m{m_frac:g}", donor_b, w5a_a0b0, m_frac,
                  {"donor": f"b_rerank_blend_w{w:g}", "orderer": "W5a@a0b0", "shippable": True})

    # donor a with the rest of the orderer-weight grid, so both levers are on the same grid
    for ow in PARTNER_WEIGHTS:
        if ow == 0.25:
            continue
        orderer = blend(w5a_a0b0, slow16_a0b0, W5A_A0B0, SLOW16_A0B0, ow)
        for m_frac in M_GRID:
            score(f"donorA__ord_w{ow:g}__m{m_frac:g}", donor_a, orderer, m_frac,
                  {"donor": "a_nested_shipped", "orderer": f"W5a+{ow:g}*slow16", "shippable": True})

    arms = dump()
    payload = json.loads((HERE / "wave20_results.json").read_text(encoding="utf-8"))
    payload["status"] = "complete"
    payload["completed_at_local"] = time.strftime("%Y-%m-%dT%H:%M:%S")
    (HERE / "wave20_results.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print("\n| rank | arm | CONNECTED | IC | excess | turnover |")
    print("|---|---|---|---|---|---|")
    for i, (s, name, v) in enumerate(arms[:20]):
        m = v["connected_metrics"]
        print(f"| {i+1} | {name[:52]} | **{s:.9f}** | {m['ic_mean']:.6f} | "
              f"{m['annual_excess']:.6f} | {m['mean_turnover']:.6f} |")
    cs.log(f"best shippable arm: {arms[0][1] if arms else None} "
           f"{arms[0][0] if arms else 0:.9f}")


if __name__ == "__main__":
    main()
