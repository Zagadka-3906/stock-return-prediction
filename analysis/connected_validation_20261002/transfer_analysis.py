"""Split-half transfer analysis: how much of the optimization survives a window it was not fitted on.

后续选模标准.md §4 removes statistical significance, worst-year and "must find a new unseen period" as
elimination criteria, and §3 makes the connected 2020-2024 composite the sole objective. That is the
rule and it is applied as written. But this project has two documented prior instances of exactly this
kind of in-sample win reversing: wave-4's nested hyperparameter selection gained +0.0068/+0.0047 on
2020-2021 and then returned +0.0005/-0.0028 on 2022-2024, and wave-8 suite B's alpha 0.95/bonus 0.40
won its selection years by +0.0019 and then lost 0.0186 in 2022. Wave 6's alpha 0.8/bonus 0.6 win is
the same class of object - a post-processing retune picked by maximizing a score on the same years.

So this script does not select anything. It measures, for every finalist, its score in each individual
year and in two disjoint connected windows (2020-2022 and 2023-2024), and reports:
  * rank stability between the two windows (Spearman of the rankings)
  * the TRANSFER LOSS: take the argmax of the 2020-2022 window, score it on 2023-2024, and compare
    with the 2023-2024 argmax - this is what fitting the whole procedure on one half and testing it on
    the other actually costs
  * where the confirmed model peer67_slow16 sits in every window
Nothing here feeds back into selection; it is reported so the choice can be made with the reversal
risk quantified rather than assumed away.
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import numpy as np
import polars as pl
from scipy.stats import spearmanr

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(HERE))
import connected_scorer as cs  # noqa: E402
from experiments.revalidate_fold_local import score_official  # noqa: E402

YEARS = cs.YEARS
WINDOWS = {"2020_2022": (2020, 2021, 2022), "2023_2024": (2023, 2024), "full": YEARS}
PREFIXES = ("wave8_", "wave7b_", "pp_", "connected_pred_")
CONFIRMED = "peer67_slow16"


def find_array(name: str):
    for prefix in PREFIXES:
        path = HERE / f"{prefix}{name}.npy"
        if path.exists():
            return path
    return None


def discover(limit: int = 14) -> list[str]:
    """Take the strongest finalists from the recorded waves, plus the confirmed model and the
    released-post-processing reference, so every window comparison includes the incumbent."""
    names = []
    base = HERE / "connected_results_all.json"
    if base.exists():
        for entry in json.loads(base.read_text(encoding="utf-8"))["ranking_by_connected_score"][:6]:
            names.append(entry["name"])
    for wave_file in ("wave8_results.json", "wave7b_results.json", "wave6_results.json"):
        path = HERE / wave_file
        if not path.exists():
            continue
        results = json.loads(path.read_text(encoding="utf-8")).get("results", {})
        scored = [(v["connected_final_score"], k) for k, v in results.items()
                  if isinstance(v, dict) and "connected_final_score" in v]
        for _, name in sorted(scored, reverse=True)[:limit]:
            names.append(name)
    ordered = []
    for name in names + [CONFIRMED]:
        if name not in ordered and find_array(name) is not None:
            ordered.append(name)
    return ordered


def main() -> None:
    frame = cs.combined_frame()
    dates = frame["trade_date"].to_numpy()
    masks = {}
    for year in YEARS:
        masks[str(year)] = (dates >= year * 10000 + 101) & (dates <= year * 10000 + 1231)
    for label, years in WINDOWS.items():
        mask = np.zeros(len(dates), dtype=bool)
        for year in years:
            mask |= masks[str(year)]
        masks[label] = mask

    names = discover()
    cs.log(f"scoring {len(names)} finalists over {len(YEARS)} years and {len(WINDOWS)} windows")
    table = {}
    for name in names:
        pred = np.load(find_array(name))
        if len(pred) != len(frame):
            cs.log(f"{name}: skipped, {len(pred)} rows")
            continue
        row = {}
        for label, mask in masks.items():
            sub = frame.filter(pl.Series(mask))
            metrics, _ = score_official(sub, pred[mask])
            row[label] = metrics["final_score"]
        table[name] = row
        cs.log(f"{name}: full {row['full']:.9f} | 2020-22 {row['2020_2022']:.9f} | "
               f"2023-24 {row['2023_2024']:.9f} | "
               + " ".join(f"{y} {row[str(y)]:.6f}" for y in YEARS))

    common = [n for n in table if all(k in table[n] for k in ("2020_2022", "2023_2024"))]
    dev = np.array([table[n]["2020_2022"] for n in common])
    conf = np.array([table[n]["2023_2024"] for n in common])
    rho = float(spearmanr(dev, conf).statistic) if len(common) > 2 else None
    dev_best = common[int(np.argmax(dev))]
    conf_best = common[int(np.argmax(conf))]
    transfer_loss = float(table[conf_best]["2023_2024"] - table[dev_best]["2023_2024"])
    full_best = max(common, key=lambda n: table[n]["full"])

    payload = {
        "status": "complete", "completed_at_local": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "purpose": "measure split-half transfer of the optimization; selects nothing",
        "candidates": common, "table": table,
        "rank_stability_spearman_dev_vs_confirm": rho,
        "dev_window_argmax": dev_best,
        "confirm_window_argmax": conf_best,
        "transfer_loss_on_confirm_window": transfer_loss,
        "full_window_argmax": full_best,
        "full_window_argmax_rank_on_confirm_window":
            int(sorted(common, key=lambda n: -table[n]["2023_2024"]).index(full_best) + 1),
        "confirmed_model": {w: table.get(CONFIRMED, {}).get(w) for w in
                            ("full", "2020_2022", "2023_2024")},
        "interpretation_note": "a low or negative rank correlation, or a large transfer loss, means the "
                               "connected-window maximum is picking window-specific settings; that is "
                               "a property of maximizing on viewed years and is disclosed rather than "
                               "gated, per 后续选模标准.md §4",
    }
    (HERE / "transfer_analysis.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"\n| candidate | full 2020-24 | 2020-22 | 2023-24 | " +
          " | ".join(str(y) for y in YEARS) + " |")
    print("|---|" + "---|" * (3 + len(YEARS)))
    for name in sorted(common, key=lambda n: -table[n]["full"]):
        row = table[name]
        print(f"| {name[:44]} | **{row['full']:.9f}** | {row['2020_2022']:.9f} | "
              f"{row['2023_2024']:.9f} | " + " | ".join(f"{row[str(y)]:.6f}" for y in YEARS) + " |")
    print(f"\nrank stability (Spearman, 2020-22 ranking vs 2023-24 ranking): {rho}")
    print(f"2020-22 argmax: {dev_best}")
    print(f"2023-24 argmax: {conf_best}")
    print(f"transfer loss (confirm-window argmax minus the dev-window pick, on 2023-24): "
          f"{transfer_loss:+.6f}")
    print(f"full-window argmax: {full_best} -> ranked "
          f"{payload['full_window_argmax_rank_on_confirm_window']} of {len(common)} on 2023-24 alone")


if __name__ == "__main__":
    main()
