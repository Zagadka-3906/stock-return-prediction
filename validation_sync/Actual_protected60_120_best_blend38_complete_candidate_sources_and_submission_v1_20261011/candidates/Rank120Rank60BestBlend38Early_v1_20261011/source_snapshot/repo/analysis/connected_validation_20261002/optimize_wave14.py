"""Wave 14: the membership donor's post-processing was tuned for the wrong objective. Re-tune it.

Every donor setting in the library was selected to maximize that donor's OWN connected composite,
which is 0.4*IC + 0.3*excess + 0.3*(1-turnover). But in the substitution construction the donor never
supplies an ordering: W5a does. The donor's column is read only through `argsort` to pick the Top
decile, so its contribution to the hybrid is exactly two terms - excess (which names get in) and
turnover (how much the set moves day to day). Its IC is dead weight in the objective it was tuned for.

That is an unexploited degree of freedom, and it is the one wave 8 could not see: wave 8 swept four
donor settings against a slow16 orderer and picked by hybrid composite, but the grid was tiny and
centred on settings inherited from each donor's own standalone optimum.

Here the orderer is frozen at wave 12/13's selection (W5a at alpha 0 / bonus 0, m = 0.985) and the
topk return-weighted pairwise raw is re-post-processed across the full alpha x bonus grid, then
refined over the auxiliary blend weight, the protected-block restoration switch and the
top_current_weight, plus two structural variants (no post-processing at all, and the full-signal
blend instead of top-only). slow16 and W5a raws are carried along as alternative donor bases so the
choice of base is measured rather than assumed.

Harness proof, run before any new arm is scored: re-post-processing the topk raw at the RELEASED
settings must reproduce connected_pred_topk.npy bit-for-bit and score 0.414783593 standalone. Wave 8
asserted the same identity, so this also proves the two waves rebuild the donor identically.

Selection is 后续选模标准.md §3/§4: highest connected 2020-2024 official composite, no other gate.
No test-period data is read anywhere in this file.
"""
from __future__ import annotations

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
from optimize_wave6 import make_prediction_param, fold_frame, raw_average, RELEASED  # noqa: E402
from optimize_wave7b import build  # noqa: E402
from optimize_wave8 import topk_raw  # noqa: E402
from src.scoring import Panel  # noqa: E402

YEARS = cs.YEARS
TIE_EPS = 1e-9
M_FRAC = 0.985
W5A_ORDERER = "orderer_a0b0_W5a_five_way_with_gru__final_sweep_eval"
CURRENT_BEST = 0.44106451391794665
CURRENT_BEST_NAME = "topk_x_W5a_a0_b0_m0.985_tiebreak"
TOPK_RELEASED_SCORE = 0.414783593

ALPHAS = (0.0, 0.50, 0.80, 0.90, 1.00)
BONUSES = (0.0, 0.30, 0.60)
# refinement around the grid argmax, over the axes the coarse grid holds fixed
REFINE_WEIGHTS = (0.0, 0.125, 0.25, 0.50)
REFINE_FLAGS = ((False, 1.0), (True, 0.0), (True, 0.5), (True, 1.0))


def sha(path) -> str:
    value = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for chunk in iter(lambda: stream.read(8 * 1024 * 1024), b""):
            value.update(chunk)
    return value.hexdigest()


def donor_raw(kind: str, year: int, frame: pl.DataFrame, rank_average_n) -> np.ndarray:
    if kind == "topk":
        source, raw = topk_raw(year)
        if len(raw) != len(frame):
            raise AssertionError(f"topk {year}: {len(raw)} rows vs frame {len(frame)}")
        if not source.select(cs.KEYS).equals(frame.select(cs.KEYS)):
            raise AssertionError(f"topk {year}: raw prediction keys do not match the fold frame")
        return raw
    if kind == "slow16":
        return raw_average(frame, rank_average_n)
    raise KeyError(kind)


def build_donor(kind: str, setting: dict, frames: dict, rank_average_n) -> np.ndarray:
    parts = []
    for year in YEARS:
        frame = frames[year]
        raw = donor_raw(kind, year, frame, rank_average_n)
        panel = Panel.from_frame(frame.with_columns(pl.Series("pred_raw", raw)))
        parts.append(make_prediction_param(
            panel, frame["aux_raw"].to_numpy().astype(np.float64), setting["mode"],
            setting["weight"], setting["alpha"], setting["bonus"], setting["restore_lower"],
            setting["top_current_weight"]))
        del panel
    return np.concatenate(parts)


def setting_tag(setting: dict) -> str:
    return (f"a{setting['alpha']:g}_b{setting['bonus']:g}_{setting['mode']}"
            f"_w{setting['weight']:g}_rl{int(setting['restore_lower'])}"
            f"_tcw{setting['top_current_weight']:g}")


def main() -> None:
    protocol_path = HERE / "protocol_wave14.json"
    if not protocol_path.exists():
        protocol_path.write_text(json.dumps({
            "frozen_at_local": time.strftime("%Y-%m-%dT%H:%M:%S"),
            "standard": "后续选模标准.md §3 connected composite primary; §4 highest score wins",
            "status": "in_sample_selection_disclosed",
            "hypothesis": "the donor supplies only excess and turnover to the hybrid, never an "
                          "ordering, so its post-processing should be re-tuned for the hybrid rather "
                          "than inherited from its own standalone composite optimum",
            "orderer_fixed": {"column": W5A_ORDERER, "alpha": 0.0, "bonus": 0.0,
                              "provenance": "wave 12 argmax over every surviving backbone"},
            "m_frac_fixed_at": M_FRAC, "m_provenance": "wave 13 stage 1 argmax with this orderer",
            "tie_break_eps": TIE_EPS,
            "stage1_grid": {"alphas": list(ALPHAS), "bonuses": list(BONUSES),
                            "mode": "top_only", "weight": 0.25, "restore_lower": True,
                            "top_current_weight": 1.0, "donor_bases": ["topk", "slow16"]},
            "stage2_refine": {"weights": list(REFINE_WEIGHTS), "flags": [list(f) for f in REFINE_FLAGS],
                              "structural_variants": ["no post-processing (mode baseline, alpha 0, "
                                                      "bonus 0, no restoration)",
                                                      "full_signal blend instead of top_only"]},
            "harness_proof": "re-post-processing the topk raw at the RELEASED settings must reproduce "
                             f"connected_pred_topk.npy bit-for-bit and score {TOPK_RELEASED_SCORE} "
                             "standalone",
            "current_best_before_this_wave": {"name": CURRENT_BEST_NAME,
                                              "connected_final_score": CURRENT_BEST},
            "selection_rule": "highest connected 2020-2024 official composite; no significance, "
                              "worst-year or single-metric gate",
            "disclosed_selection_cost": "tenth consecutive search over the same five viewed years; no "
                                        "blind period remains and the winner carries upward selection "
                                        "bias this protocol cannot quantify",
            "causality": "every donor is a walk-forward fold prediction trained strictly before its "
                         "scored year; post-processing reads only past predictions, past limit-up "
                         "flags and the frozen pooled auxiliary. No label is read.",
            "no_test_period_data_read": True,
            "source_sha256": sha(Path(__file__)),
        }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        cs.log(f"wave-14 protocol frozen: {sha(protocol_path)[:16]}…")

    sys.path.insert(0, str(ROOT / "analysis"))
    from analysis.topset_hybrid_20261002 import fold_validation as fv
    rank_average_n = fv.load_rank_average_n()

    frames = {y: fold_frame(y) for y in YEARS}
    combined = cs.combined_frame()
    dates = combined["trade_date"].to_numpy()
    flags = combined["flag_limit_up"].to_numpy().astype(np.int64)
    codes, uniques = pd.factorize(combined["ts_code"].to_pandas(), sort=True)
    codes = codes.astype(np.int64)
    n_codes = len(uniques)
    tie_key = 1.0 - codes / max(n_codes - 1, 1)
    orderer = np.load(HERE / f"{W5A_ORDERER}.npy") + TIE_EPS * tie_key

    # ---- harness proof: the released settings must reproduce the frozen topk donor
    proof_donor = build_donor("topk", RELEASED, frames, rank_average_n)
    frozen = np.load(HERE / "connected_pred_topk.npy")
    identical = bool(np.array_equal(proof_donor, frozen))
    proof_metrics, _ = score_official(combined, proof_donor)
    proof = {"bit_identical_to_connected_pred_topk": identical,
             "max_abs_diff": float(np.abs(proof_donor - frozen).max()),
             "standalone_connected": proof_metrics["final_score"],
             "expected_standalone": TOPK_RELEASED_SCORE,
             "standalone_abs_diff": abs(proof_metrics["final_score"] - TOPK_RELEASED_SCORE)}
    if not identical:
        raise AssertionError(f"harness proof failed: rebuilt topk donor differs from the frozen column "
                             f"(max diff {proof['max_abs_diff']:.3e})")
    if proof["standalone_abs_diff"] > 1e-9:
        raise AssertionError(f"harness proof failed: rebuilt topk donor scores "
                             f"{proof_metrics['final_score']!r}, expected {TOPK_RELEASED_SCORE!r}")
    cs.log(f"harness proof passed: the topk donor rebuilds bit-for-bit and scores "
           f"{proof_metrics['final_score']:.9f} standalone")

    results: dict = {}

    def dump() -> list:
        arms = sorted(((v["connected_final_score"], k, v) for k, v in results.items()
                       if "connected_final_score" in v), reverse=True)
        payload = {"status": "running", "updated_at_local": time.strftime("%Y-%m-%dT%H:%M:%S"),
                   "purpose": "re-tune the membership donor's post-processing for the hybrid, not for "
                              "the donor's own composite",
                   "orderer_fixed": W5A_ORDERER, "m_frac": M_FRAC, "tie_break_eps": TIE_EPS,
                   "harness_proof": proof,
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
        (HERE / "wave14_results.json").write_text(
            json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        return arms

    def score_donor(name: str, kind: str, setting: dict) -> float:
        cache = HERE / f"donor14_{kind}_{setting_tag(setting)}.npy"
        if cache.exists():
            donor = np.load(cache)
        else:
            donor = build_donor(kind, setting, frames, rank_average_n)
            np.save(cache, donor)
        hybrid, stats = build(donor, orderer, dates, flags, codes, n_codes, M_FRAC)
        metrics, _ = score_official(combined, hybrid)
        standalone, _ = score_official(combined, donor)
        results[name] = {"donor_base": kind, "donor_postprocess": setting, "m_frac": M_FRAC,
                         "orderer": W5A_ORDERER,
                         "donor_standalone_connected": standalone["final_score"],
                         "donor_standalone_excess": standalone["annual_excess"],
                         "connected_final_score": metrics["final_score"],
                         "connected_metrics": metrics,
                         "boundary_tie_days": stats["boundary_tie_days"],
                         "mean_retention_ratio": stats["mean_retention_ratio"],
                         "beats_current_best": bool(metrics["final_score"] > CURRENT_BEST)}
        cs.log(f"{name[:58]:58s} CONNECTED {metrics['final_score']:.9f} "
               f"(ic {metrics['ic_mean']:.6f}, excess {metrics['annual_excess']:.6f}, "
               f"turn {metrics['mean_turnover']:.6f}) donor standalone "
               f"{standalone['final_score']:.6f}/exc {standalone['annual_excess']:.6f}")
        dump()
        return metrics["final_score"]

    # ---- stage 1: alpha x bonus over two donor bases
    for kind in ("topk", "slow16"):
        for alpha in ALPHAS:
            for bonus in BONUSES:
                setting = {**RELEASED, "alpha": alpha, "bonus": bonus}
                name = f"{kind}__{setting_tag(setting)}"
                try:
                    score_donor(name, kind, setting)
                except BaseException as error:  # noqa: BLE001
                    results[name] = {"donor_base": kind, "donor_postprocess": setting,
                                     "error": f"{type(error).__name__}: {error}"}
                    cs.log(f"{name[:58]:58s} FAILED {type(error).__name__}: {error}")
                    dump()

    ok = {k: v for k, v in results.items() if "connected_final_score" in v and v["donor_base"] == "topk"}
    best_setting = max(ok.items(), key=lambda kv: kv[1]["connected_final_score"])[1]["donor_postprocess"]
    cs.log(f"stage 1 argmax donor setting: {setting_tag(best_setting)}")

    # ---- stage 2: refine the axes stage 1 held fixed, on the topk base
    for weight in REFINE_WEIGHTS:
        setting = {**best_setting, "weight": weight}
        if setting_tag(setting) == setting_tag(best_setting):
            continue
        score_donor(f"topk__{setting_tag(setting)}", "topk", setting)
    for restore_lower, tcw in REFINE_FLAGS:
        setting = {**best_setting, "restore_lower": restore_lower, "top_current_weight": tcw}
        if setting_tag(setting) == setting_tag(best_setting):
            continue
        score_donor(f"topk__{setting_tag(setting)}", "topk", setting)
    structural = {
        "topk__no_postprocess": {"alpha": 0.0, "bonus": 0.0, "restore_lower": False,
                                 "top_current_weight": 0.0, "mode": "baseline", "weight": 0.0},
        "topk__full_signal_w0.25": {**best_setting, "mode": "full_signal"},
    }
    for name, setting in structural.items():
        try:
            score_donor(name, "topk", setting)
        except BaseException as error:  # noqa: BLE001
            results[name] = {"donor_base": "topk", "donor_postprocess": setting,
                             "error": f"{type(error).__name__}: {error}"}
            cs.log(f"{name[:58]:58s} FAILED {type(error).__name__}: {error}")

    arms = dump()
    payload = json.loads((HERE / "wave14_results.json").read_text(encoding="utf-8"))
    payload["status"] = "complete"
    payload["completed_at_local"] = time.strftime("%Y-%m-%dT%H:%M:%S")
    payload["stage1_best_donor_setting"] = best_setting
    (HERE / "wave14_results.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print("\n| rank | donor (base @ post-processing) | CONNECTED | IC | excess | turnover | donor standalone |")
    print("|---|---|---|---|---|---|---|")
    for i, (score, name, v) in enumerate(arms[:20]):
        m = v["connected_metrics"]
        print(f"| {i+1} | {name[:60]} | **{score:.9f}** | {m['ic_mean']:.6f} | "
              f"{m['annual_excess']:.6f} | {m['mean_turnover']:.6f} | "
              f"{v['donor_standalone_connected']:.6f} |")
    cs.log(f"best: {arms[0][1] if arms else None} {arms[0][0] if arms else 0:.9f} "
           f"({'IMPROVES' if arms and arms[0][0] > CURRENT_BEST else 'does not improve'})")


if __name__ == "__main__":
    main()
