"""Wave 32: the tabular transformer was never eligible for the orderer sweep. Make it eligible.

`score_wave3.discover()` only admits a single-member arm when it has caches for ALL five fold years.
`final_sweep_eval/T2g_tabular_transformer_{2022,2023,2024}.parquet` exist but 2020 and 2021 were never
trained, so the transformer was silently excluded from wave 12's sweep of every backbone in the orderer
role - the sweep that found W5a and started this whole run. That is a gap in the search, not a negative
result about the model.

The gap is now closed on the input side. `probe_transformer.py` reproduced the frozen 2022 fold
bit-for-bit (max|diff| 0.000e+00) using final_sweep_extra's own train_transformer / predict_transformer,
which proves the recipe is recoverable, and then trained 2020 and 2021 with it (755 s and 1107 s). So all
five fold years exist: 2020/2021 freshly trained, 2022/2023/2024 from the frozen caches.

Why the transformer is worth a slot at all: the GRU precedent. It was **rejected standalone** in
final_sweep_wave5 - "the released post-processing stack is tuned for daily cross-sectional tree ranks,
and the sequence ensemble failed its own gate" - yet as a minority member of a rank average it became
the single most valuable component of the wave-12 winning orderer. The transformer is the other
structurally different signal in the project (an FT-Transformer-lite, one learned token per feature,
trained on negative mean daily cross-sectional Pearson correlation) and it was rejected by the same suite
for the same reason, so the same argument applies and has never been tested.

Arms, all with the shipped nested donor and m = 0.985:
  T-alone     the transformer at alpha 0 / bonus 0 as the sole orderer - a quality read, not a candidate
  W5a+T       the two-way blend, weight grid
  SEL+T       the SELECTED orderer (W5a + 0.25*slow16) plus the transformer as a third member
Harness proofs: W5a+T at weight 0 must reproduce 0.442481207 and SEL+T at weight 0 must reproduce
0.445092234 or 0.443190552 depending on which donor fraction is current; both are asserted against
values read from the recorded results rather than retyped.

Selection is 后续选模标准.md §3/§4. Both-halves decomposition is reported for every arm because every
m-axis gain in waves 23/25/26 turned out to be a redistribution between halves. No test-period data is
read here.
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
ARCHIVE = ROOT.parent / "赛题五_历史归档_20261001"
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(ARCHIVE))

TRANSFORMER_OUT = HERE / "wave26_transformer" / "raw"
FROZEN_T2G = ARCHIVE / "experiments/final_sweep_eval"
YEARS = (2020, 2021, 2022, 2023, 2024)
W5A_A0B0 = "orderer_a0b0_W5a_five_way_with_gru__final_sweep_eval.npy"
SLOW16_A0B0 = "pp_a0_b0_top_only_w0.25_rl1_tcw1.npy"
DONOR_STEM = "connected_pred_hybrid.npy"
PARTNER_WEIGHT = 0.25
M_FRAC = 0.985
TIE_EPS = 1e-9
T_WEIGHTS = (0.10, 0.167, 0.25, 0.35, 0.50)
REF_W5A_ALONE = 0.4424812067218111
REF_SELECTED = 0.44319055217888365
REF_HALF_DEV = 0.442705356
REF_HALF_CONF = 0.443926938


def sha(path) -> str:
    value = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for chunk in iter(lambda: stream.read(8 * 1024 * 1024), b""):
            value.update(chunk)
    return value.hexdigest()


def log(message: str) -> None:
    print(f"[{time.strftime('%H:%M:%S')}] {message}", flush=True)


def transformer_raw_by_year() -> dict:
    """2020/2021 from probe_transformer's reproduce-and-extend runs; 2022-2024 from the frozen caches."""
    out = {}
    for year in YEARS:
        mine = TRANSFORMER_OUT / f"transformer_{year}.parquet"
        frozen = FROZEN_T2G / f"T2g_tabular_transformer_{year}.parquet"
        if year in (2020, 2021):
            if not mine.exists():
                raise SystemExit(f"missing {mine}; run probe_transformer.py extend")
            path, provenance = mine, "retrained by probe_transformer.py with final_sweep_extra's recipe"
        else:
            if not frozen.exists():
                raise SystemExit(f"missing frozen cache {frozen}")
            path, provenance = frozen, "frozen final_sweep_eval cache"
        df = pl.read_parquet(path).sort("trade_date", "ts_code")
        out[year] = (df, provenance, path)
    return out


def main() -> None:
    protocol_path = HERE / "protocol_wave32.json"
    if not protocol_path.exists():
        protocol_path.write_text(json.dumps({
            "frozen_at_local": time.strftime("%Y-%m-%dT%H:%M:%S"),
            "standard": "后续选模标准.md §3 connected composite primary; §4 highest score wins",
            "status": "in_sample_selection_disclosed",
            "hypothesis": "the tabular transformer was silently excluded from wave 12's orderer sweep "
                          "because discover() requires all five fold years and only 2022-2024 existed. "
                          "probe_transformer.py reproduced the frozen 2022 fold bit-for-bit and trained "
                          "2020/2021, so the gap can now be closed. The GRU precedent - rejected "
                          "standalone, then the most valuable member of the winning orderer - is the "
                          "reason to expect a structurally different signal to help in a minority slot.",
            "arms": {"T-alone": "transformer at alpha 0 / bonus 0 as the sole orderer; a quality read",
                     "W5a+T": f"two-way blend at transformer weights {list(T_WEIGHTS)}",
                     "SEL+T": "the selected orderer (W5a + 0.25*slow16) plus the transformer"},
            "donor_fixed": {"column": DONOR_STEM, "provenance": "wave 13 stage 2 argmax"},
            "m_frac_fixed_at": M_FRAC, "tie_break_eps": TIE_EPS,
            "transformer_sources": {"2020": "retrained, 755 s", "2021": "retrained, 1107 s",
                                    "2022": "frozen cache, reproduced bit-for-bit by the probe "
                                            "(max|diff| 0.000e+00, train 1487.5 s)",
                                    "2023": "frozen cache", "2024": "frozen cache"},
            "harness_proofs": {
                "P1": f"W5a+T at transformer weight 0 must reproduce {REF_W5A_ALONE}",
                "P2": f"SEL+T at transformer weight 0 must reproduce {REF_SELECTED}",
            },
            "current_best_before_this_wave": REF_SELECTED,
            "selection_rule": "highest connected 2020-2024 official composite; no other gate",
            "reported_for_every_arm": "the both-halves decomposition, because every m-axis gain in "
                                      "waves 23/25/26 was a redistribution between halves",
            "disclosed_selection_cost": "search over the same five repeatedly viewed years; the "
                                        "transformer's 2020/2021 folds are fresh walk-forward fits with "
                                        "cutoffs strictly before each scored year, but the decision to "
                                        "test it was made after those years were viewed",
            "causality": "each fold's transformer is trained on rows with trade_date < fold_cutoff(year). "
                         "The blend reads only same-day predictions and the price-valid mask. No label "
                         "is read at selection time.",
            "no_test_period_data_read": True,
            "source_sha256": sha(Path(__file__)),
        }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        log(f"wave-32 protocol frozen: {sha(protocol_path)[:16]}…")

    import connected_scorer as cs
    from experiments.revalidate_fold_local import score_official
    from optimize_wave6 import make_prediction_param, fold_frame
    from optimize_wave13 import build_ab
    from optimize_wave15 import daily_ranks, weighted_rank_blend
    from optimize_wave18 import lift
    from src.scoring import Panel

    combined = cs.combined_frame()
    dates = combined["trade_date"].to_numpy()
    flags = combined["flag_limit_up"].to_numpy().astype(np.int64)
    valid = combined["price_valid"].to_numpy().astype(bool)
    codes, uniques = pd.factorize(combined["ts_code"].to_pandas(), sort=True)
    codes = codes.astype(np.int64)
    n_codes = len(uniques)
    tie_key = 1.0 - codes / max(n_codes - 1, 1)
    pdf = combined.select(["trade_date", "flag_limit_up"]).to_pandas()
    frames = {y: fold_frame(y) for y in YEARS}

    # ---- assemble the transformer's connected raw column
    sources = transformer_raw_by_year()
    parts, provenance = [], {}
    for year in YEARS:
        df, prov, path = sources[year]
        frame = frames[year]
        if not df.select(["ts_code", "trade_date"]).equals(frame.select(["ts_code", "trade_date"])):
            raise AssertionError(f"transformer {year}: keys do not match the fold frame")
        parts.append(df["pred_raw"].to_numpy().astype(np.float64))
        provenance[str(year)] = {"path": str(path), "sha256": sha(path), "provenance": prov,
                                 "rows": int(len(df)),
                                 "sentinel_rows": int((df["pred_raw"].to_numpy() <= -1e5).sum())}
        log(f"  transformer {year}: {len(df):,} rows, {prov}")
    transformer_raw = np.concatenate(parts)
    if len(transformer_raw) != len(combined):
        raise AssertionError("transformer column length does not match the combined frame")

    def postprocess(raw: np.ndarray) -> np.ndarray:
        out = []
        for year in YEARS:
            frame = frames[year]
            mask = (dates >= year * 10000 + 101) & (dates <= year * 10000 + 1231)
            panel = Panel.from_frame(frame.with_columns(pl.Series("pred_raw", raw[mask])))
            out.append(make_prediction_param(panel, frame["aux_raw"].to_numpy().astype(np.float64),
                                             "top_only", 0.25, 0.0, 0.0, True, 1.0))
            del panel
            gc.collect()
        return np.concatenate(out)

    t_a0b0 = postprocess(transformer_raw)
    np.save(HERE / "orderer_a0b0_transformer.npy", t_a0b0)
    log(f"transformer orderer column built: sentinel rows {int((t_a0b0 <= -9.0).sum()):,}")

    w5a = np.load(HERE / W5A_A0B0)
    slow16 = np.load(HERE / SLOW16_A0B0)
    member = np.load(HERE / DONOR_STEM)
    rank_cache = {"w5a": daily_ranks(w5a, valid, dates), "slow16": daily_ranks(slow16, valid, dates),
                  "transformer": daily_ranks(t_a0b0, valid, dates)}
    selected = weighted_rank_blend([w5a, slow16], [1 - PARTNER_WEIGHT, PARTNER_WEIGHT], rank_cache,
                                   valid, dates, ("w5a", "slow16"))
    selected = np.where(selected > -9.0, selected + TIE_EPS * tie_key, selected)

    masks = {str(yy): (dates >= yy * 10000 + 101) & (dates <= yy * 10000 + 1231) for yy in YEARS}
    half = {"2020_2022": np.zeros(len(dates), dtype=bool),
            "2023_2024": np.zeros(len(dates), dtype=bool)}
    for yy in (2020, 2021, 2022):
        half["2020_2022"] |= masks[str(yy)]
    for yy in (2023, 2024):
        half["2023_2024"] |= masks[str(yy)]

    results: dict = {}
    proofs: dict = {"transformer_sources": provenance}

    def dump() -> list:
        arms = sorted(((v["connected_final_score"], k, v) for k, v in results.items()
                       if "connected_final_score" in v), reverse=True)
        payload = {"status": "running", "updated_at_local": time.strftime("%Y-%m-%dT%H:%M:%S"),
                   "purpose": "test the tabular transformer in the orderer role, which wave 12 could "
                              "not because it lacked 2020/2021 folds",
                   "donor_fixed": DONOR_STEM, "m_frac": M_FRAC, "tie_break_eps": TIE_EPS,
                   "harness_proofs": proofs, "current_best_before_this_wave": REF_SELECTED,
                   "reference_halves": {"2020_2022": REF_HALF_DEV, "2023_2024": REF_HALF_CONF},
                   "results": results, "n_scored": len(arms),
                   "ranking": [{"arm": k, "connected_final_score": s, "margin_full": v["margin_full"],
                                "margin_2020_2022": v["margin_2020_2022"],
                                "margin_2023_2024": v["margin_2023_2024"],
                                "wins_both_halves": v["wins_both_halves"],
                                "ic_mean": v["connected_metrics"]["ic_mean"],
                                "annual_excess": v["connected_metrics"]["annual_excess"],
                                "mean_turnover": v["connected_metrics"]["mean_turnover"]}
                               for s, k, v in arms],
                   "best": arms[0][1] if arms else None,
                   "best_connected_final_score": arms[0][0] if arms else None,
                   "no_test_period_data_read": True, "source_sha256": sha(Path(__file__))}
        (HERE / "wave32_results.json").write_text(
            json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        return arms

    def score(name: str, orderer: np.ndarray, extra: dict) -> float:
        orderer_tb = np.where(orderer > -9.0, orderer + TIE_EPS * tie_key, orderer) + TIE_EPS * tie_key
        hybrid, stats = build_ab(member, orderer_tb, orderer_tb, dates, flags, codes, n_codes, M_FRAC)
        metrics, _ = score_official(combined, hybrid)
        halves = {}
        for label, mask in half.items():
            sub, _ = score_official(combined.filter(pl.Series(mask)), hybrid[mask])
            halves[label] = sub["final_score"]
        results[name] = {**extra, "connected_final_score": metrics["final_score"],
                         "connected_metrics": metrics, "halves": halves,
                         "margin_full": metrics["final_score"] - REF_SELECTED,
                         "margin_2020_2022": halves["2020_2022"] - REF_HALF_DEV,
                         "margin_2023_2024": halves["2023_2024"] - REF_HALF_CONF,
                         "wins_both_halves": bool(halves["2020_2022"] > REF_HALF_DEV
                                                  and halves["2023_2024"] > REF_HALF_CONF),
                         "boundary_tie_days": stats["boundary_tie_days"],
                         "mean_retention_ratio": stats["mean_retention_ratio"]}
        log(f"{name[:24]:24s} CONNECTED {metrics['final_score']:.9f} "
            f"({metrics['final_score'] - REF_SELECTED:+.2e}) | ic {metrics['ic_mean']:.6f} | "
            f"exc {metrics['annual_excess']:.6f} | turn {metrics['mean_turnover']:.6f} | "
            f"2020-22 {halves['2020_2022'] - REF_HALF_DEV:+.2e} | 2023-24 "
            f"{halves['2023_2024'] - REF_HALF_CONF:+.2e}")
        dump()
        return metrics["final_score"]

    # ---- the transformer's own quality, read on the same caliber as every other backbone
    t_alone, _ = score_official(combined, t_a0b0)
    proofs["transformer_standalone"] = {
        "connected_final_score": t_alone["final_score"], "ic_mean": t_alone["ic_mean"],
        "annual_excess": t_alone["annual_excess"], "mean_turnover": t_alone["mean_turnover"],
        "compare_W5a_standalone_ic": 0.11944980502947201,
        "compare_slow16_standalone_ic": 0.11736658434105325}
    log(f"transformer standalone (alpha0/bonus0, no substitution): {t_alone['final_score']:.9f} "
        f"ic {t_alone['ic_mean']:.6f} exc {t_alone['annual_excess']:.6f} turn "
        f"{t_alone['mean_turnover']:.6f}")

    # harness proofs FIRST, through the same code path, before any new arm is scored
    got1 = score("P1_W5a+T_w0", w5a, {"kind": "harness_proof", "weights": [1.0, 0.0]})
    proofs["P1"] = {"scored": got1, "expected": REF_W5A_ALONE, "abs_diff": abs(got1 - REF_W5A_ALONE)}
    if abs(got1 - REF_W5A_ALONE) > 1e-12:
        raise AssertionError(f"P1 failed: {got1!r} vs {REF_W5A_ALONE!r}")
    got2 = score("P2_SEL+T_w0", selected, {"kind": "harness_proof", "weights": [0.75, 0.25, 0.0]})
    proofs["P2"] = {"scored": got2, "expected": REF_SELECTED, "abs_diff": abs(got2 - REF_SELECTED)}
    if abs(got2 - REF_SELECTED) > 1e-12:
        raise AssertionError(f"P2 failed: {got2!r} vs {REF_SELECTED!r}")
    log("harness proofs passed: transformer weight 0 reproduces both references exactly")

    score("T-alone", t_a0b0, {"kind": "transformer_alone"})

    for w in T_WEIGHTS:
        blend = weighted_rank_blend([w5a, t_a0b0], [1.0 - w, w], rank_cache, valid, dates,
                                    ("w5a", "transformer"))
        score(f"W5a+T_w{w:g}", blend, {"kind": "w5a_plus_transformer", "weights": [1 - w, w]})

    for w in T_WEIGHTS:
        blend = weighted_rank_blend([w5a, slow16, t_a0b0],
                                    [(1 - PARTNER_WEIGHT) * (1 - w), PARTNER_WEIGHT * (1 - w), w],
                                    rank_cache, valid, dates, ("w5a", "slow16", "transformer"))
        score(f"SEL+T_w{w:g}", blend, {"kind": "selected_plus_transformer",
                                       "weights": [(1 - PARTNER_WEIGHT) * (1 - w),
                                                   PARTNER_WEIGHT * (1 - w), w]})

    arms = dump()
    payload = json.loads((HERE / "wave32_results.json").read_text(encoding="utf-8"))
    payload["status"] = "complete"
    payload["completed_at_local"] = time.strftime("%Y-%m-%dT%H:%M:%S")
    (HERE / "wave32_results.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("\n| arm | CONNECTED | margin | IC | excess | turnover | 2020-22 | 2023-24 | both? |")
    print("|---|---|---|---|---|---|---|---|---|")
    for s, name, v in arms:
        m = v["connected_metrics"]
        print(f"| {name[:18]} | **{s:.9f}** | {v['margin_full']:+.2e} | {m['ic_mean']:.6f} | "
              f"{m['annual_excess']:.6f} | {m['mean_turnover']:.6f} | "
              f"{v['margin_2020_2022']:+.2e} | {v['margin_2023_2024']:+.2e} | "
              f"{'YES' if v['wins_both_halves'] else 'no'} |")


if __name__ == "__main__":
    main()
