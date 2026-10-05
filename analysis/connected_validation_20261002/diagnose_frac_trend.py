"""Wave 33 diagnostic: decompose the frac 0.10 -> 0.20 gain term by term and year by year.

Wave 31 found that widening the Top-K objective's fraction from n//10 to n//5 raises the connected
composite by +1.90e-3 with IC, excess AND turnover all improving - the signature of a real effect. The
per-year decomposition then showed the gain is strictly monotone decreasing in time: +1.20e-2 in 2020,
+6.85e-3 in 2021, -1.70e-4 in 2022, -2.69e-3 in 2023, -6.50e-3 in 2024. The test period is 2025-2026,
later than every training year, so the trend extrapolates the wrong way.

This file works out WHICH term carries the trend, because that decides whether the trend has a mechanism
or is just five numbers that happen to line up. Three readings are produced per year per fraction:

  1. the official composite's three terms, each multiplied by its own weight, so the contributions sum
     to the composite and the movement can be attributed rather than guessed
  2. structural statistics of the cross-section that could drive a regime change: mean stocks per day,
     the limit-up share, and the cross-sectional dispersion of realized returns
  3. the donor's own standalone terms, separated from the hybrid's, so a change in the promote block can
     be told apart from a change in how the outer solve uses it

It also records the arithmetic that makes the trend interpretable: k = floor(frac * n) and n grows over
the sample, so a flatter fraction does not mean a constant number of promoted names - it means a growing
one, and the objective's per-pair weight is scale/(k*samples), so the effective gradient per name shrinks
as n grows. If the trend tracks n, that is a mechanism; if it does not, the trend is unexplained and
should not be extrapolated in either direction.

Reads no test-period data. Selects nothing.
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
from optimize_wave6 import make_prediction_param, fold_frame  # noqa: E402
from optimize_wave13 import build_ab  # noqa: E402
from optimize_wave15 import daily_ranks, weighted_rank_blend  # noqa: E402
from optimize_wave18 import lift  # noqa: E402
from src.scoring import Panel  # noqa: E402

YEARS = (2020, 2021, 2022, 2023, 2024)
RAW = HERE / "wave31_topk/raw"
FRACS = (0.10, 0.15, 0.20, 0.25, 0.30)
TIE_EPS = 1e-9
M_FRAC = 0.985
PARTNER_WEIGHT = 0.25
W_IC, W_EXCESS, W_TURN = 0.4, 0.3, 0.3


def sha(path) -> str:
    value = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for chunk in iter(lambda: stream.read(8 * 1024 * 1024), b""):
            value.update(chunk)
    return value.hexdigest()


def log(message: str) -> None:
    print(f"[{time.strftime('%H:%M:%S')}] {message}", flush=True)


def main() -> None:
    combined = cs.combined_frame()
    dates = combined["trade_date"].to_numpy()
    flags = combined["flag_limit_up"].to_numpy().astype(np.int64)
    valid = combined["price_valid"].to_numpy().astype(bool)
    y = combined["y_ret_1d"].to_numpy().astype(np.float64)
    codes, uniques = pd.factorize(combined["ts_code"].to_pandas(), sort=True)
    codes = codes.astype(np.int64)
    n_codes = len(uniques)
    tie_key = 1.0 - codes / max(n_codes - 1, 1)
    pdf = combined.select(["trade_date", "flag_limit_up"]).to_pandas()
    slow16_fin = np.load(HERE / "connected_pred_peer67_slow16.npy")

    w5a = np.load(HERE / "orderer_a0b0_W5a_five_way_with_gru__final_sweep_eval.npy")
    slow16 = np.load(HERE / "pp_a0_b0_top_only_w0.25_rl1_tcw1.npy")
    rc = {"w5a": daily_ranks(w5a, valid, dates), "slow16": daily_ranks(slow16, valid, dates)}
    bl = weighted_rank_blend([w5a, slow16], [1 - PARTNER_WEIGHT, PARTNER_WEIGHT], rc, valid, dates,
                             ("w5a", "slow16"))
    orderer = np.where(bl > -9.0, bl + TIE_EPS * tie_key, bl) + TIE_EPS * tie_key

    frames = {yy: fold_frame(yy) for yy in YEARS}
    masks = {str(yy): (dates >= yy * 10000 + 101) & (dates <= yy * 10000 + 1231) for yy in YEARS}

    def postprocess(raw_by_year: dict) -> np.ndarray:
        out = []
        for yy in YEARS:
            frame = frames[yy]
            panel = Panel.from_frame(frame.with_columns(pl.Series("pred_raw", raw_by_year[yy])))
            out.append(make_prediction_param(panel, frame["aux_raw"].to_numpy().astype(np.float64),
                                             "top_only", 0.25, 0.9, 0.3, True, 1.0))
            del panel
        return np.concatenate(out)

    # ---- structural statistics per year, the candidate mechanism
    structure = {}
    for yy in YEARS:
        mask = masks[str(yy)]
        d, f, yy_valid, yy_y = dates[mask], flags[mask], valid[mask], y[mask]
        rows_per_day = pd.Series(d).value_counts().sort_index()
        eligible_per_day = pd.DataFrame({"d": d, "f": f}).query("f == 0").groupby("d").size()
        finite = np.isfinite(yy_y) & yy_valid
        disp = (pd.DataFrame({"d": d[finite], "y": yy_y[finite]}).groupby("d")["y"]
                .std().mean())
        structure[str(yy)] = {
            "days": int(len(rows_per_day)),
            "rows_per_day_mean": float(rows_per_day.mean()),
            "eligible_per_day_mean": float(eligible_per_day.mean()),
            "n_top_per_day_mean": float((eligible_per_day // 10).mean()),
            "k_at_frac_0.10": float(np.floor(0.10 * eligible_per_day).mean()),
            "k_at_frac_0.20": float(np.floor(0.20 * eligible_per_day).mean()),
            "limit_up_share": float((f == 1).mean()),
            "realized_return_cross_sectional_sd": float(disp),
            "realized_return_mean": float(np.nanmean(yy_y[finite])),
        }
        log(f"structure {yy}: eligible/day {structure[str(yy)]['eligible_per_day_mean']:.1f}, "
            f"k@0.10 {structure[str(yy)]['k_at_frac_0.10']:.1f}, "
            f"k@0.20 {structure[str(yy)]['k_at_frac_0.20']:.1f}, limit-up "
            f"{structure[str(yy)]['limit_up_share']*100:.2f}%, return sd {disp:.5f}")

    results = {}
    for frac in FRACS:
        raws = {}
        for yy in YEARS:
            path = RAW / f"topk_seed2026_f{frac:.2f}_{yy}.parquet"
            if not path.exists():
                raise SystemExit(f"missing {path.name}")
            raws[yy] = pl.read_parquet(path)["pred_raw"].to_numpy().astype(np.float64)
        finished = postprocess(raws)
        promote = np.where(np.isfinite(finished) & (finished > -9.0), finished + TIE_EPS * tie_key,
                           finished)
        donor, lift_stats = lift(promote, slow16_fin, pdf)
        hybrid, _ = build_ab(donor, orderer, orderer, dates, flags, codes, n_codes, M_FRAC)
        donor_metrics, _ = score_official(combined, donor)
        per_year = {}
        for yy in YEARS:
            mask = masks[str(yy)]
            m, _ = score_official(combined.filter(pl.Series(mask)), hybrid[mask])
            dm, _ = score_official(combined.filter(pl.Series(mask)), donor[mask])
            per_year[str(yy)] = {
                "composite": m["final_score"], "ic_mean": m["ic_mean"],
                "annual_excess": m["annual_excess"], "mean_turnover": m["mean_turnover"],
                "contribution_ic": W_IC * m["ic_mean"],
                "contribution_excess": W_EXCESS * m["annual_excess"],
                "contribution_turnover": W_TURN * (1.0 - m["mean_turnover"]),
                "donor_composite": dm["final_score"], "donor_ic_mean": dm["ic_mean"],
                "donor_annual_excess": dm["annual_excess"], "donor_mean_turnover": dm["mean_turnover"],
            }
        full, _ = score_official(combined, hybrid)
        results[f"frac{frac:.2f}"] = {
            "frac": frac, "lift_stats": lift_stats,
            "full": {"composite": full["final_score"], "ic_mean": full["ic_mean"],
                     "annual_excess": full["annual_excess"], "mean_turnover": full["mean_turnover"],
                     "contribution_ic": W_IC * full["ic_mean"],
                     "contribution_excess": W_EXCESS * full["annual_excess"],
                     "contribution_turnover": W_TURN * (1.0 - full["mean_turnover"])},
            "donor_full": {"composite": donor_metrics["final_score"],
                           "ic_mean": donor_metrics["ic_mean"],
                           "annual_excess": donor_metrics["annual_excess"],
                           "mean_turnover": donor_metrics["mean_turnover"]},
            "per_year": per_year,
        }
        log(f"frac {frac:.2f}: full {full['final_score']:.9f} "
            f"(ic {W_IC * full['ic_mean']:.6f} + exc {W_EXCESS * full['annual_excess']:.6f} "
            f"+ turn {W_TURN * (1 - full['mean_turnover']):.6f})")

    base = results["frac0.10"]
    attribution = {}
    for frac in FRACS:
        cur = results[f"frac{frac:.2f}"]
        row = {}
        for yy in YEARS:
            b, c = base["per_year"][str(yy)], cur["per_year"][str(yy)]
            row[str(yy)] = {
                "composite": c["composite"] - b["composite"],
                "from_ic": W_IC * (c["ic_mean"] - b["ic_mean"]),
                "from_excess": W_EXCESS * (c["annual_excess"] - b["annual_excess"]),
                "from_turnover": W_TURN * (b["mean_turnover"] - c["mean_turnover"]),
                "donor_composite": c["donor_composite"] - b["donor_composite"],
                "donor_excess": c["donor_annual_excess"] - b["donor_annual_excess"],
            }
        attribution[f"frac{frac:.2f}"] = row

    payload = {
        "status": "complete", "generated_at_local": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "purpose": "attribute the frac 0.10 -> 0.20 gain, and its monotone time trend, to individual "
                   "terms, and test whether the trend tracks a structural statistic",
        "selects_nothing": True, "no_test_period_data_read": True,
        "weights": {"ic": W_IC, "excess": W_EXCESS, "turnover": W_TURN},
        "structure_per_year": structure,
        "results": results,
        "attribution_vs_frac0.10": attribution,
        "trend_tests": {},
        "source_sha256": sha(Path(__file__)),
    }

    # does the per-year gain track any structural statistic?
    years_sorted = [str(yy) for yy in YEARS]
    for frac in FRACS:
        if frac == 0.10:
            continue
        gains = np.array([attribution[f"frac{frac:.2f}"][yy]["composite"] for yy in years_sorted])
        row = {"per_year_gain": [float(g) for g in gains],
               "monotone_decreasing": bool(np.all(np.diff(gains) < 0))}
        for stat in ("eligible_per_day_mean", "k_at_frac_0.20", "limit_up_share",
                     "realized_return_cross_sectional_sd"):
            values = np.array([structure[yy][stat] for yy in years_sorted])
            row[f"spearman_gain_vs_{stat}"] = float(pd.Series(gains).corr(pd.Series(values),
                                                                          method="spearman"))
        for term in ("from_ic", "from_excess", "from_turnover"):
            parts = np.array([attribution[f"frac{frac:.2f}"][yy][term] for yy in years_sorted])
            row[f"{term}_monotone_decreasing"] = bool(np.all(np.diff(parts) < 0))
            row[f"{term}_per_year"] = [float(p) for p in parts]
            row[f"spearman_{term}_vs_year"] = float(pd.Series(parts).corr(
                pd.Series(np.arange(len(years_sorted))), method="spearman"))
        payload["trend_tests"][f"frac{frac:.2f}"] = row

    (HERE / "wave33_frac_attribution.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print("\n=== per-year composite gain vs frac 0.10, attributed to terms ===")
    print(f"{'frac':>6} {'term':>14} " + " ".join(f'{yy:>11}' for yy in YEARS) + "   monotone?")
    for frac in FRACS:
        if frac == 0.10:
            continue
        for term in ("composite", "from_ic", "from_excess", "from_turnover"):
            vals = [attribution[f"frac{frac:.2f}"][str(yy)][term] for yy in YEARS]
            mono = "YES" if np.all(np.diff(vals) < 0) else ("no" if np.all(np.diff(vals) > 0) else "-")
            label = term if term != "composite" else "TOTAL"
            print(f"{frac:>6.2f} {label:>14} " + " ".join(f"{v:+11.2e}" for v in vals) + f"   {mono}")
        print()
    print("=== structure per year ===")
    print(f"{'year':>6} {'elig/day':>9} {'k@0.10':>7} {'k@0.20':>7} {'limitup%':>9} {'ret sd':>9}")
    for yy in YEARS:
        s = structure[str(yy)]
        print(f"{yy:>6} {s['eligible_per_day_mean']:9.1f} {s['k_at_frac_0.10']:7.1f} "
              f"{s['k_at_frac_0.20']:7.1f} {s['limit_up_share']*100:9.2f} "
              f"{s['realized_return_cross_sectional_sd']:9.5f}")
    print("\n=== spearman of the per-year gain vs each structural statistic ===")
    for frac, row in payload["trend_tests"].items():
        print(f"{frac}: monotone {row['monotone_decreasing']} | " +
              " ".join(f"{k.replace('spearman_gain_vs_', '')}={v:+.2f}"
                       for k, v in row.items() if k.startswith("spearman_gain_vs_")))
    log("wrote wave33_frac_attribution.json")


if __name__ == "__main__":
    main()
