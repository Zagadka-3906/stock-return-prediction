"""Split-half transfer check on the finalists only.

The full 48-candidate transfer analysis showed rank stability between the 2020-2022 and 2023-2024 halves
of Spearman -0.7477, which is why every finalist has to be looked at on both halves separately before
it is shipped. This reruns that check on the short list produced by waves 6-10, including the nested
membership variant, which is regenerated here because wave 10 did not persist it.

Selects nothing. Reported so the choice can be made with the reversal risk quantified.
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd
import polars as pl
from scipy.stats import spearmanr

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(HERE))
import connected_scorer as cs  # noqa: E402
from experiments.revalidate_fold_local import score_official  # noqa: E402
from optimize_wave7b import build  # noqa: E402

YEARS = cs.YEARS
NESTED_NAME = "nested_hybrid_x_a0_b0.15_m0.985"
NESTED_EXPECTED = 0.441013125
FINALISTS = {
    "wave10_a0_b0.15_top_only_w0.25_rl1_tcw1_m0.985.npy": "SELECTED simple: topk x slow16@a0/b0.15, m=0.985",
    "wave10_a0_b0.15_top_only_w0.25_rl1_tcw1_m0.npy": "same pair, m=0 (no retention floor)",
    "wave10_a0_b0_top_only_w0.25_rl1_tcw1_m0.985.npy": "topk x slow16@a0/b0, m=0.985",
    "wave7b_topk_x_W5a__m0.985.npy": "previous leader: topk x W5a, m=0.985",
    "pp_a0.8_b0.6_top_only_w0.25_rl1_tcw1.npy": "best standalone: slow16 @ a0.8/b0.6",
    "connected_pred_peer67_slow16.npy": "CONFIRMED MODEL peer67_slow16",
    "connected_pred_topk.npy": "membership donor topk alone",
    "connected_pred_W5a_five_way_with_gru__final_sweep_eval.npy": "orderer W5a alone",
}


def main() -> None:
    frame = cs.combined_frame()
    dates = frame["trade_date"].to_numpy()
    flags = frame["flag_limit_up"].to_numpy()
    codes, uniques = pd.factorize(frame["ts_code"].to_pandas(), sort=True)
    codes = codes.astype(np.int64)

    nested_path = HERE / f"{NESTED_NAME}.npy"
    if not nested_path.exists():
        member = np.load(HERE / "connected_pred_hybrid.npy")
        orderer = np.load(HERE / "pp_a0_b0.15_top_only_w0.25_rl1_tcw1.npy")
        pred, _ = build(member, orderer, dates, flags, codes, len(uniques), 0.985)
        metrics, _ = score_official(frame, pred)
        diff = abs(metrics["final_score"] - NESTED_EXPECTED)
        if diff > 1e-9:
            raise AssertionError(f"nested regeneration gave {metrics['final_score']!r}, expected "
                                 f"{NESTED_EXPECTED!r} (diff {diff:.3e})")
        np.save(nested_path, pred)
        cs.log(f"nested variant regenerated and reproduces {NESTED_EXPECTED:.9f} (diff {diff:.1e})")
    finalists = {nested_path.name: "NESTED: (topk x slow16) x slow16@a0/b0.15, m=0.985"}
    finalists.update(FINALISTS)

    masks = {str(y): (dates >= y * 10000 + 101) & (dates <= y * 10000 + 1231) for y in YEARS}
    for label, years in (("full", YEARS), ("2020_2022", (2020, 2021, 2022)),
                         ("2023_2024", (2023, 2024))):
        mask = np.zeros(len(dates), dtype=bool)
        for year in years:
            mask |= masks[str(year)]
        masks[label] = mask

    table = {}
    for filename, description in finalists.items():
        path = HERE / filename
        if not path.exists():
            cs.log(f"{filename}: missing, skipped")
            continue
        pred = np.load(path)
        row = {"description": description}
        for label, mask in masks.items():
            metrics, _ = score_official(frame.filter(pl.Series(mask)), pred[mask])
            row[label] = metrics["final_score"]
        table[filename] = row
        cs.log(f"{description[:52]:52s} full {row['full']:.9f} | 2020-22 {row['2020_2022']:.9f} | "
               f"2023-24 {row['2023_2024']:.9f}")

    names = list(table)
    dev = np.array([table[n]["2020_2022"] for n in names])
    conf = np.array([table[n]["2023_2024"] for n in names])
    rho = float(spearmanr(dev, conf).statistic) if len(names) > 2 else None
    payload = {"status": "complete", "completed_at_local": time.strftime("%Y-%m-%dT%H:%M:%S"),
               "purpose": "split-half transfer of the finalist short list; selects nothing",
               "table": table, "rank_stability_spearman_dev_vs_confirm": rho,
               "dev_argmax": names[int(np.argmax(dev))],
               "confirm_argmax": names[int(np.argmax(conf))],
               "full_argmax": max(names, key=lambda n: table[n]["full"]),
               "no_test_period_data_read": True}
    (HERE / "transfer_finalists.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print("\n| candidate | full 2020-24 | 2020-22 | 2023-24 | 2020 | 2021 | 2022 | 2023 | 2024 |")
    print("|---|---|---|---|---|---|---|---|---|")
    for name in sorted(names, key=lambda n: -table[n]["full"]):
        row = table[name]
        print(f"| {row['description'][:56]} | **{row['full']:.9f}** | {row['2020_2022']:.9f} | "
              f"{row['2023_2024']:.9f} | " + " | ".join(f"{row[str(y)]:.6f}" for y in YEARS) + " |")
    print(f"\nrank stability across finalists (Spearman dev vs confirm): {rho}")
    print(f"dev argmax    : {table[payload['dev_argmax']]['description']}")
    print(f"confirm argmax: {table[payload['confirm_argmax']]['description']}")


if __name__ == "__main__":
    main()
