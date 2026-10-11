"""Split-half transfer of the wave 13-16 finalist chain. Selects nothing.

The full 48-candidate transfer analysis found Spearman -0.7477 between the 2020-2022 and 2023-2024
halves, which is why every finalist is looked at on both halves before it is shipped. Waves 12-16 moved
the scheme a long way from the arms that analysis covered - a different orderer, a different membership
donor, and now a blended orderer - so the check has to be redone on the actual finalists.

Arms are rebuilt from the components and weights each wave recorded, then required to reproduce that
wave's own recorded full-window score before any half-window number from them is believed. That is the
harness proof here: if the rebuild does not reproduce the frozen number, the halves are meaningless.

Reads no test-period data.
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
from scipy.stats import spearmanr

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(HERE))
import connected_scorer as cs  # noqa: E402
from experiments.revalidate_fold_local import score_official  # noqa: E402
from optimize_wave13 import build_ab  # noqa: E402
from optimize_wave15 import daily_ranks, weighted_rank_blend, W5A_ORDERER, DONOR, M_FRAC, TIE_EPS  # noqa: E402

YEARS = cs.YEARS
TOP_N = 8


def sha(path) -> str:
    value = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for chunk in iter(lambda: stream.read(8 * 1024 * 1024), b""):
            value.update(chunk)
    return value.hexdigest()


def collect_arms() -> dict[str, dict]:
    """Every scored arm from waves 13, 15 and 16 that can be rebuilt from its recorded spec."""
    arms: dict[str, dict] = {}
    arms["wave13::nested_x_W5a_a0b0_m0.985"] = {
        "recorded": 0.4424812067218111,
        "spec": {"components": [W5A_ORDERER], "weights": [1.0]},
        "array": "wave13_nested_x_W5a_a0b0_m0.985_tiebreak.npy",
        "description": "SELECTED before waves 15-16: nested donor x W5a@a0/b0, m=0.985"}
    arms["wave12::topk_x_W5a_a0b0_m0.985"] = {
        "recorded": 0.44106451391794665,
        "spec": {"components": [W5A_ORDERER], "weights": [1.0], "donor": "connected_pred_topk.npy"},
        "description": "wave 12 winner: plain topk donor x W5a@a0/b0, m=0.985"}
    arms["confirmed::peer67_slow16"] = {
        "recorded": 0.42740793751694767,
        "array": "connected_pred_peer67_slow16.npy",
        "description": "CONFIRMED MODEL peer67_slow16, released pipeline, no substitution"}

    for wave, path in (("wave15", HERE / "wave15_results.json"),
                       ("wave16", HERE / "wave16_results.json")):
        if not path.exists():
            continue
        data = json.loads(path.read_text(encoding="utf-8"))
        for bucket in data.get("results", {}).values():
            for key, value in bucket.items():
                if "connected_final_score" not in value or "components" not in value:
                    continue
                arms[f"{wave}::{key}"] = {
                    "recorded": float(value["connected_final_score"]),
                    "spec": {"components": value["components"], "weights": value["weights"]},
                    "description": f"{wave} {key}"}

    # the finally selected arm, if save_final_selected_arm.py has already persisted it
    selected_path = HERE / "selected_arm.json"
    if selected_path.exists():
        selected = json.loads(selected_path.read_text(encoding="utf-8"))
        array = Path(selected["output"]["path"])
        if array.exists():
            arms["SELECTED"] = {"recorded": float(selected["connected_final_score"]),
                                "array": array.name,
                                "description": f"SELECTED {selected['arm']} "
                                               f"(donor {selected['donor'].get('variant')}, "
                                               f"orderer {selected['orderer']}, "
                                               f"m {selected['m_frac']})"}
    return arms


def main() -> None:
    frame = cs.combined_frame()
    dates = frame["trade_date"].to_numpy()
    flags = frame["flag_limit_up"].to_numpy().astype(np.int64)
    valid = frame["price_valid"].to_numpy().astype(bool)
    codes, uniques = pd.factorize(frame["ts_code"].to_pandas(), sort=True)
    codes = codes.astype(np.int64)
    n_codes = len(uniques)
    tie_key = 1.0 - codes / max(n_codes - 1, 1)

    arms = collect_arms()
    ranked = sorted(arms.items(), key=lambda kv: -kv[1]["recorded"])
    shortlist = ranked[:TOP_N]
    for must in ("confirmed::peer67_slow16", "SELECTED"):
        if must in arms and must not in dict(shortlist):
            shortlist.append((must, arms[must]))
    cs.log(f"shortlist: {len(shortlist)} arms")

    rank_cache: dict = {}
    column_cache: dict = {}

    def column(stem: str) -> np.ndarray:
        if stem not in column_cache:
            column_cache[stem] = np.load(HERE / f"{stem}.npy")
        return column_cache[stem]

    def ranks(stem: str) -> np.ndarray:
        if stem not in rank_cache:
            rank_cache[stem] = daily_ranks(column(stem), valid, dates)
        return rank_cache[stem]

    masks = {str(y): (dates >= y * 10000 + 101) & (dates <= y * 10000 + 1231) for y in YEARS}
    for label, years in (("full", YEARS), ("2020_2022", (2020, 2021, 2022)),
                         ("2023_2024", (2023, 2024))):
        mask = np.zeros(len(dates), dtype=bool)
        for year in years:
            mask |= masks[str(year)]
        masks[label] = mask

    table: dict = {}
    for name, arm in shortlist:
        try:
            if "array" in arm:
                pred = np.load(HERE / arm["array"])
            else:
                spec = arm["spec"]
                donor = np.load(HERE / spec.get("donor", DONOR))
                comps = spec["components"]
                weights = spec["weights"]
                if len(comps) == 1:
                    orderer = column(comps[0])
                else:
                    for c in comps:
                        ranks(c)
                    orderer = weighted_rank_blend([column(c) for c in comps], weights, rank_cache,
                                                  valid, dates, tuple(comps))
                pred, _ = build_ab(donor, orderer + TIE_EPS * tie_key, orderer + TIE_EPS * tie_key,
                                   dates, flags, codes, n_codes, M_FRAC)
            metrics, _ = score_official(frame, pred)
            diff = abs(metrics["final_score"] - arm["recorded"])
            row = {"description": arm["description"], "recorded": arm["recorded"],
                   "full": metrics["final_score"], "rebuilt_full": metrics["final_score"],
                   "rebuild_abs_diff": diff, "rebuild_ok": bool(diff < 1e-9)}
            if not row["rebuild_ok"]:
                row["error"] = f"rebuild gave {metrics['final_score']!r}, recorded {arm['recorded']!r}"
                cs.log(f"{name[:56]:56s} REBUILD MISMATCH {diff:.3e} - halves not trusted")
                table[name] = row
                continue
            for label, mask in masks.items():
                if label == "full":
                    continue
                sub, _ = score_official(frame.filter(pl.Series(mask)), pred[mask])
                row[label] = sub["final_score"]
            table[name] = row
            cs.log(f"{name[:56]:56s} full {row['full']:.9f} | 2020-22 {row['2020_2022']:.9f} | "
                   f"2023-24 {row['2023_2024']:.9f} (rebuild diff {diff:.1e})")
        except BaseException as error:  # noqa: BLE001
            table[name] = {"description": arm["description"], "error": f"{type(error).__name__}: {error}"}
            cs.log(f"{name[:56]:56s} FAILED {type(error).__name__}: {error}")

    ok = {k: v for k, v in table.items() if "2020_2022" in v}
    names = list(ok)
    dev = np.array([ok[n]["2020_2022"] for n in names])
    conf = np.array([ok[n]["2023_2024"] for n in names])
    rho = float(spearmanr(dev, conf).statistic) if len(names) > 2 else None
    payload = {"status": "complete", "completed_at_local": time.strftime("%Y-%m-%dT%H:%M:%S"),
               "purpose": "split-half transfer of the wave 13-16 finalists; selects nothing",
               "harness_proof": "each arm is rebuilt from its recorded spec and must reproduce that "
                                "wave's recorded full-window score to 1e-9 before its halves are used",
               "table": table,
               "rank_stability_spearman_dev_vs_confirm": rho,
               "dev_argmax": names[int(np.argmax(dev))] if names else None,
               "confirm_argmax": names[int(np.argmax(conf))] if names else None,
               "full_argmax": max(names, key=lambda n: ok[n]["recorded"]) if names else None,
               "both_halves_beat_confirmed": {
                   n: {"dev": bool(ok[n]["2020_2022"] > ok["confirmed::peer67_slow16"]["2020_2022"]),
                       "confirm": bool(ok[n]["2023_2024"]
                                       > ok["confirmed::peer67_slow16"]["2023_2024"])}
                   for n in names if n != "confirmed::peer67_slow16"}
               if "confirmed::peer67_slow16" in ok else None,
               "no_test_period_data_read": True,
               "source_sha256": sha(Path(__file__))}
    (HERE / "transfer_wave16.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print("\n| arm | full 2020-24 | 2020-22 | 2023-24 | " +
          " | ".join(str(y) for y in YEARS) + " |")
    print("|---|---|---|---|" + "---|" * len(YEARS))
    for name in sorted(names, key=lambda n: -ok[n]["recorded"]):
        row = ok[name]
        cells = " | ".join(f"{row[str(y)]:.6f}" if str(y) in row else "-" for y in YEARS)
        print(f"| {row['description'][:58]} | **{row['recorded']:.9f}** | "
              f"{row['2020_2022']:.9f} | {row['2023_2024']:.9f} | {cells} |")
    print(f"\nrank stability across these finalists (Spearman dev vs confirm): {rho}")
    if names:
        print(f"dev argmax    : {ok[payload['dev_argmax']]['description']}")
        print(f"confirm argmax: {ok[payload['confirm_argmax']]['description']}")


if __name__ == "__main__":
    main()
