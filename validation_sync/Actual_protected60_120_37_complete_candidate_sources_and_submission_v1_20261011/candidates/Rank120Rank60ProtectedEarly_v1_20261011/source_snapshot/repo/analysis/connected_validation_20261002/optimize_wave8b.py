"""Wave 8b: refine the retention floor around the observed optimum and characterise its shape.

Wave 7b's m scan for the leading pair peaked sharply - 0.98 -> 0.432589, 0.985 -> 0.434035,
0.99 -> 0.432647 - and m is an integer retention floor (round(m_frac * n_top) with n_top ~ 450, so
0.98/0.985/0.99 are 441/443/446 retained names). A one-name difference should not be worth 0.0014,
which is below this project's 0.001743 refit noise floor, so the peak has to be characterised before
it is trusted: a plateau means the choice is robust, an isolated spike means the argmax is fitting
integer granularity.

This adds the intermediate values for the two best member/orderer pairs and reports the curve shape.
It selects nothing on its own; the winner is still whatever the connected composite says across every
wave, and the shape is reported alongside so the choice can be made on a plateau rather than a spike.
"""
from __future__ import annotations

import hashlib
import itertools
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
from optimize_wave7b import build  # noqa: E402

PAIRS = [("topk_rel", "W5a_rel"), ("topk_a08b06", "W5a_rel")]
M_VALUES = (0.981, 0.982, 0.983, 0.984, 0.986, 0.987, 0.988, 0.989)
ALREADY_SCORED = {("topk_rel", "W5a_rel"): {0.98: 0.432589440, 0.985: 0.434034593,
                                            0.99: 0.432646698, 0.97: 0.431719326,
                                            0.95: 0.432246686, 0.0: 0.431942948},
                  ("topk_a08b06", "W5a_rel"): {0.98: 0.433369778, 0.99: 0.430437010,
                                               0.0: 0.433270949}}


def sha(path) -> str:
    value = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for chunk in iter(lambda: stream.read(8 * 1024 * 1024), b""):
            value.update(chunk)
    return value.hexdigest()


# wave 8 saved rebuilt donors as donor_<name>.npy but loaded W5a straight from its wave-3 column
ALIASES = {"W5a_rel": "connected_pred_W5a_five_way_with_gru__final_sweep_eval.npy"}


def load_donor(name: str) -> np.ndarray:
    for candidate in (f"donor_{name}.npy", f"connected_pred_{name}.npy", ALIASES.get(name, "")):
        path = HERE / candidate
        if candidate and path.exists():
            return np.load(path)
    raise SystemExit(f"no saved donor column for {name}")


def main() -> None:
    frame = cs.combined_frame()
    dates = frame["trade_date"].to_numpy()
    flags = frame["flag_limit_up"].to_numpy()
    codes, uniques = pd.factorize(frame["ts_code"].to_pandas(), sort=True)
    codes = codes.astype(np.int64)
    n_codes = len(uniques)

    results = {}
    for member, orderer in PAIRS:
        base = load_donor(member)
        order = load_donor(orderer)
        for m_frac in M_VALUES:
            name = f"{member}__x__{orderer}__m{m_frac:g}"
            pred, stats = build(base, order, dates, flags, codes, n_codes, m_frac)
            metrics, _ = score_official(frame, pred)
            results[name] = {"member": member, "orderer": orderer, "m_frac": m_frac,
                             "connected_final_score": metrics["final_score"],
                             "connected_metrics": metrics,
                             "mean_retention_ratio": stats["mean_retention_ratio"]}
            cs.log(f"{name}: CONNECTED {metrics['final_score']:.9f} (ic {metrics['ic_mean']:.6f}, "
                   f"excess {metrics['annual_excess']:.6f}, turnover {metrics['mean_turnover']:.6f})")
            del pred

    curves = {}
    for pair, known in ALREADY_SCORED.items():
        merged = dict(known)
        for name, v in results.items():
            if (v["member"], v["orderer"]) == pair:
                merged[v["m_frac"]] = v["connected_final_score"]
        curves[f"{pair[0]}_x_{pair[1]}"] = {str(k): v for k, v in sorted(merged.items())}

    ranked = sorted(results.items(), key=lambda kv: -kv[1]["connected_final_score"])
    payload = {"status": "complete", "completed_at_local": time.strftime("%Y-%m-%dT%H:%M:%S"),
               "purpose": "characterise the retention-floor optimum as plateau or spike",
               "pairs": [list(p) for p in PAIRS], "m_values": list(M_VALUES),
               "results": results, "curves": curves,
               "best_new": ranked[0][0] if ranked else None,
               "best_new_score": ranked[0][1]["connected_final_score"] if ranked else None,
               "noise_floor_reference": 0.001743,
               "source_sha256": sha(Path(__file__)),
               "no_test_period_data_read": True}
    (HERE / "wave8b_results.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    for name, curve in curves.items():
        print(f"\n{name}: retention-floor curve")
        print("| m | CONNECTED |")
        print("|---|---|")
        for m, score in sorted((float(k), v) for k, v in curve.items()):
            print(f"| {m:g} | {score:.9f} |")
        values = [v for _, v in sorted((float(k), v) for k, v in curve.items())]
        print(f"range {max(values) - min(values):.6f}, best {max(values):.9f}")


if __name__ == "__main__":
    main()
