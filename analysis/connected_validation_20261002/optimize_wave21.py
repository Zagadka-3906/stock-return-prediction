"""Wave 21: the nested donor's two components were never re-post-processed for the membership role.

The selected donor is lift(topk promotes, slow16 re-ranks), and BOTH components are finished columns at
the released alpha 0.9 / bonus 0.3. That setting was chosen to maximize each model's OWN standalone
composite, in which smoothing buys turnover at the cost of IC. But a lift component never faces that
trade-off: the promoted block sets which names are eligible, and the re-ranker only orders inside it, so
neither one's turnover is ever observed and neither one's IC is ever read directly. Wave 12 established
exactly this for the orderer role and gained +0.000915 by stripping the smoothing; the same argument
applies to both donor slots and has never been tested.

Wave 18 varied the donor's STRUCTURE (which column promotes, which re-ranks, whether either is a blend)
but always with released-settings inputs. Wave 14 was frozen to vary a simple donor's post-processing and
was never run, superseded by wave 13's 30-donor sweep; this wave covers the live configuration instead.

Orderer, retention floor and tie-break are frozen at the wave-20 selection, so every arm is directly
comparable to 0.443190552.

Harness proof: (topk at released settings, slow16 at released settings) must reproduce
connected_pred_hybrid.npy bit-for-bit and, with the selected blended orderer, score 0.443190552.

Deliverability is checked per component, not assumed. slow16 and W5a at any post-processing are free on
the test period because the delivery carries slow16's pred_raw and reconstruct_w5a_test.py proved W5a's.
A re-tuned TOPK needs its test-period raw, which does not exist as a finished artifact; the documented
path is the ~193 s fulltrain re-fit in middle/run_middle.py::supplemental_topk. Arms that need it are
flagged so the selection can weigh shippability cost.

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
from optimize_wave8 import topk_raw  # noqa: E402
from optimize_wave13 import build_ab  # noqa: E402
from optimize_wave15 import daily_ranks, weighted_rank_blend, TIE_EPS  # noqa: E402
from optimize_wave18 import lift  # noqa: E402
from src.scoring import Panel  # noqa: E402

YEARS = cs.YEARS
M_FRAC = 0.985
W5A_A0B0 = "orderer_a0b0_W5a_five_way_with_gru__final_sweep_eval.npy"
SLOW16_A0B0 = "pp_a0_b0_top_only_w0.25_rl1_tcw1.npy"
W5A_FIN = "connected_pred_W5a_five_way_with_gru__final_sweep_eval.npy"
SLOW16_FIN = "connected_pred_peer67_slow16.npy"
TOPK_FIN = "connected_pred_topk.npy"
NESTED = "connected_pred_hybrid.npy"
PARTNER_WEIGHT = 0.25
CURRENT_BEST = 0.44319055217888365
A08B06 = {**RELEASED, "alpha": 0.8, "bonus": 0.6}
A0B0 = {**RELEASED, "alpha": 0.0, "bonus": 0.0}

# (label, base, post-processing setting, needs a test-period topk refit)
COMPONENTS = [
    ("topk_rel", "topk", RELEASED, False),
    ("topk_a0b0", "topk", A0B0, True),
    ("topk_a08b06", "topk", A08B06, True),
    ("slow16_rel", "slow16", RELEASED, False),
    ("slow16_a0b0", "slow16", A0B0, False),
    ("w5a_rel", "w5a", RELEASED, False),
]
PROMOTE_SLOTS = ("topk_rel", "topk_a0b0", "topk_a08b06", "slow16_rel", "w5a_rel")
RERANK_SLOTS = ("slow16_rel", "slow16_a0b0", "w5a_rel")


def sha(path) -> str:
    value = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for chunk in iter(lambda: stream.read(8 * 1024 * 1024), b""):
            value.update(chunk)
    return value.hexdigest()


def needs_topk_refit(label: str) -> bool:
    """True only for the RE-TUNED topk components.

    topk at the released settings needs no refit: its finished test-period column already exists as
    middle/predictions/supplemental_topk_fulltrain2024.parquet, which is what every shipped submission
    in this directory uses as its membership donor. Only alpha 0 / bonus 0 and alpha 0.8 / bonus 0.6
    require the ~193 s fulltrain re-fit via middle/run_middle.py::supplemental_topk. The first run of
    this wave flagged every topk promote slot, including the released one, which wrongly marked the
    winner as needing a refit. Scores were unaffected; this is metadata only.
    """
    return label in ("topk_a0b0", "topk_a08b06")


def tag(setting: dict) -> str:
    return f"a{setting['alpha']:g}_b{setting['bonus']:g}"


def main() -> None:
    protocol_path = HERE / "protocol_wave21.json"
    if not protocol_path.exists():
        protocol_path.write_text(json.dumps({
            "frozen_at_local": time.strftime("%Y-%m-%dT%H:%M:%S"),
            "standard": "后续选模标准.md §3 connected composite primary; §4 highest score wins",
            "status": "in_sample_selection_disclosed",
            "hypothesis": "both lift components sit at the released alpha 0.9 / bonus 0.3, which was "
                          "tuned for each model's own standalone composite. Neither slot's turnover is "
                          "observed and neither slot's IC is read directly, so the smoothing that buys "
                          "turnover at the cost of IC is pure cost here - the same argument wave 12 "
                          "confirmed for the orderer role, worth +0.000915",
            "supersedes_wave14": "protocol_wave14.json was frozen but never executed; wave 13's 30-donor "
                                 "sweep and wave 18's structure sweep covered its question for the "
                                 "simple donors, and this wave covers the live nested configuration",
            "orderer_fixed": {"components": [W5A_A0B0, SLOW16_A0B0],
                              "weights": [1 - PARTNER_WEIGHT, PARTNER_WEIGHT],
                              "provenance": "wave 20 argmax over shippable arms"},
            "m_frac_fixed_at": M_FRAC, "tie_break_eps": TIE_EPS,
            "components": [{"label": l, "base": b, "postprocess": tag(s),
                            "needs_test_topk_refit": n} for l, b, s, n in COMPONENTS],
            "promote_slots": list(PROMOTE_SLOTS), "rerank_slots": list(RERANK_SLOTS),
            "harness_proof": f"(topk_rel promotes, slow16_rel re-ranks) must reproduce "
                             f"{NESTED} bit-for-bit and score {CURRENT_BEST} with the selected orderer",
            "current_best_before_this_wave": {"name": "wave20 selection",
                                              "connected_final_score": CURRENT_BEST},
            "selection_rule": "highest connected 2020-2024 official composite; no other gate. "
                              "Shippability cost is recorded per arm, not used as a gate",
            "disclosed_selection_cost": "search over the same five repeatedly viewed years; no blind "
                                        "period remains and the winner carries upward selection bias "
                                        "this protocol cannot quantify",
            "causality": "every component is a walk-forward fold prediction; the lift reads only "
                         "same-day predictions and same-day limit-up flags. No label is read.",
            "no_test_period_data_read": True,
            "source_sha256": sha(Path(__file__)),
        }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        cs.log(f"wave-21 protocol frozen: {sha(protocol_path)[:16]}…")

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
    pdf = combined.select(["trade_date", "flag_limit_up"]).to_pandas()

    # the selected orderer, rebuilt exactly as wave 20 built it
    cache: dict = {}
    w5a_a0b0 = np.load(HERE / W5A_A0B0)
    slow16_a0b0 = np.load(HERE / SLOW16_A0B0)
    for stem, col in ((W5A_A0B0, w5a_a0b0), (SLOW16_A0B0, slow16_a0b0)):
        cache[stem] = daily_ranks(col, valid, dates)
    orderer = weighted_rank_blend([w5a_a0b0, slow16_a0b0], [1 - PARTNER_WEIGHT, PARTNER_WEIGHT],
                                  cache, valid, dates, (W5A_A0B0, SLOW16_A0B0))
    orderer = np.where(orderer > -9.0, orderer + TIE_EPS * tie_key, orderer)

    def rebuild(base: str, setting: dict) -> np.ndarray:
        """Re-post-process a raw backbone over the five folds and concatenate."""
        parts = []
        for year in YEARS:
            frame = frames[year]
            if base == "topk":
                source, raw = topk_raw(year)
                if len(raw) != len(frame):
                    raise AssertionError(f"topk {year}: {len(raw)} rows vs frame {len(frame)}")
                if not source.select(cs.KEYS).equals(frame.select(cs.KEYS)):
                    raise AssertionError(f"topk {year}: raw keys do not match the fold frame")
            elif base == "slow16":
                raw = raw_average(frame, rank_average_n)
            elif base == "w5a":
                raw = np.load(HERE / "w5a_raw_fold.npy")
                raw = raw[(dates >= year * 10000 + 101) & (dates <= year * 10000 + 1231)]
                if len(raw) != len(frame):
                    raise AssertionError(f"w5a {year}: {len(raw)} rows vs frame {len(frame)}")
            else:
                raise KeyError(base)
            panel = Panel.from_frame(frame.with_columns(pl.Series("pred_raw", raw)))
            parts.append(make_prediction_param(
                panel, frame["aux_raw"].to_numpy().astype(np.float64), setting["mode"],
                setting["weight"], setting["alpha"], setting["bonus"], setting["restore_lower"],
                setting["top_current_weight"]))
            del panel
        return np.concatenate(parts)

    # ---- component library, with the harness proof on the two released ones
    columns: dict = {}
    for label, base, setting, needs_refit in COMPONENTS:
        frozen_name = {("topk", 0.9): TOPK_FIN, ("slow16", 0.9): SLOW16_FIN,
                       ("slow16", 0.0): SLOW16_A0B0, ("w5a", 0.9): W5A_FIN}.get(
                           (base, setting["alpha"]))
        if frozen_name and (HERE / frozen_name).exists():
            columns[label] = np.load(HERE / frozen_name)
            cs.log(f"component {label:14s} loaded from frozen {frozen_name}")
            continue
        columns[label] = rebuild(base, setting)
        np.save(HERE / f"donor21_{label}.npy", columns[label])
        cs.log(f"component {label:14s} rebuilt at {tag(setting)}")

    proofs: dict = {}
    ref_don, ref_stats = lift(columns["topk_rel"], columns["slow16_rel"], pdf)
    frozen_nested = np.load(HERE / NESTED)
    proofs["P_donor_reproduces_frozen_nested"] = {
        "bit_identical": bool(np.array_equal(ref_don, frozen_nested)),
        "max_abs_diff": float(np.abs(ref_don - frozen_nested).max()), "lift_stats": ref_stats}
    if not np.array_equal(ref_don, frozen_nested):
        raise AssertionError("harness proof failed: the rebuilt nested donor is not "
                             f"{NESTED} (max diff "
                             f"{proofs['P_donor_reproduces_frozen_nested']['max_abs_diff']:.3e})")

    results: dict = {}

    def dump() -> list:
        arms = sorted(((v["connected_final_score"], k, v) for k, v in results.items()
                       if "connected_final_score" in v), reverse=True)
        payload = {"status": "running", "updated_at_local": time.strftime("%Y-%m-%dT%H:%M:%S"),
                   "purpose": "re-post-process the nested donor's two components for the membership "
                              "role instead of for their own standalone composites",
                   "orderer_fixed": [W5A_A0B0, SLOW16_A0B0], "partner_weight": PARTNER_WEIGHT,
                   "m_frac": M_FRAC, "tie_break_eps": TIE_EPS, "harness_proofs": proofs,
                   "components": [{"label": l, "base": b, "postprocess": tag(s),
                                   "needs_test_topk_refit": n} for l, b, s, n in COMPONENTS],
                   "current_best_before_this_wave": CURRENT_BEST,
                   "results": results, "n_scored": len(arms),
                   "ranking": [{"arm": k, "connected_final_score": s,
                                "ic_mean": v["connected_metrics"]["ic_mean"],
                                "annual_excess": v["connected_metrics"]["annual_excess"],
                                "mean_turnover": v["connected_metrics"]["mean_turnover"],
                                "needs_test_topk_refit": v["needs_test_topk_refit"]}
                               for s, k, v in arms[:25]],
                   "best": arms[0][1] if arms else None,
                   "best_connected_final_score": arms[0][0] if arms else None,
                   "best_shippable_without_refit": next(
                       (k for s, k, v in arms if not v["needs_test_topk_refit"]), None),
                   "improves_on_current_best": bool(arms and arms[0][0] > CURRENT_BEST),
                   "no_test_period_data_read": True,
                   "source_sha256": sha(Path(__file__))}
        (HERE / "wave21_results.json").write_text(
            json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        return arms

    for promote in PROMOTE_SLOTS:
        for rerank in RERANK_SLOTS:
            name = f"promote_{promote}__rerank_{rerank}"
            needs_refit = needs_topk_refit(promote)
            try:
                donor, stats = lift(columns[promote], columns[rerank], pdf)
                hybrid, hstats = build_ab(donor, orderer + TIE_EPS * tie_key,
                                          orderer + TIE_EPS * tie_key, dates, flags, codes,
                                          n_codes, M_FRAC)
                metrics, _ = score_official(combined, hybrid)
                results[name] = {"promote": promote, "rerank": rerank, "lift_stats": stats,
                                 "needs_test_topk_refit": needs_refit,
                                 "connected_final_score": metrics["final_score"],
                                 "connected_metrics": metrics,
                                 "boundary_tie_days": hstats["boundary_tie_days"],
                                 "mean_retention_ratio": hstats["mean_retention_ratio"],
                                 "beats_current_best": bool(metrics["final_score"] > CURRENT_BEST)}
                cs.log(f"{name[:48]:48s} CONNECTED {metrics['final_score']:.9f} "
                       f"(ic {metrics['ic_mean']:.6f}, excess {metrics['annual_excess']:.6f}, "
                       f"turn {metrics['mean_turnover']:.6f})"
                       f"{'  [needs topk refit]' if needs_refit else ''}")
                if name == "promote_topk_rel__rerank_slow16_rel":
                    proofs["P_reference_cell"] = {"arm": name, "scored": metrics["final_score"],
                                                  "expected": CURRENT_BEST,
                                                  "abs_diff": abs(metrics["final_score"] - CURRENT_BEST)}
                    if abs(metrics["final_score"] - CURRENT_BEST) > 1e-12:
                        raise AssertionError(
                            f"harness proof failed: the reference cell scored "
                            f"{metrics['final_score']!r}, expected {CURRENT_BEST!r}")
                    cs.log("harness proof passed: the reference cell reproduces 0.443190552")
                dump()
            except BaseException as error:  # noqa: BLE001
                results[name] = {"promote": promote, "rerank": rerank,
                                 "needs_test_topk_refit": needs_refit,
                                 "error": f"{type(error).__name__}: {error}"}
                cs.log(f"{name[:48]:48s} FAILED {type(error).__name__}: {error}")
                dump()

    arms = dump()
    payload = json.loads((HERE / "wave21_results.json").read_text(encoding="utf-8"))
    payload["status"] = "complete"
    payload["completed_at_local"] = time.strftime("%Y-%m-%dT%H:%M:%S")
    (HERE / "wave21_results.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print("\n| rank | donor components | CONNECTED | IC | excess | turnover | needs topk refit |")
    print("|---|---|---|---|---|---|---|")
    for i, (s, name, v) in enumerate(arms):
        m = v["connected_metrics"]
        print(f"| {i+1} | {name[:44]} | **{s:.9f}** | {m['ic_mean']:.6f} | "
              f"{m['annual_excess']:.6f} | {m['mean_turnover']:.6f} | "
              f"{'yes' if v['needs_test_topk_refit'] else 'no'} |")
    ship = [(s, k) for s, k, v in arms if not v["needs_test_topk_refit"]]
    cs.log(f"best: {arms[0][1] if arms else None} {arms[0][0] if arms else 0:.9f}")
    if ship:
        cs.log(f"best shippable without a topk refit: {ship[0][1]} {ship[0][0]:.9f}")


if __name__ == "__main__":
    main()
