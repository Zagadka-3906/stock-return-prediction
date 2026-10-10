"""Consolidate every connected-caliber result into one ranked selection table.

后续选模标准.md §3 makes the connected 2020-2024 official composite the single primary score and §4
makes the highest-scoring compliant candidate the winner, with complexity and run cost as tie-breaks
only. This script does not re-score anything: it collects every candidate scored under that caliber
across all waves, records for each one WHAT mechanism produced it and WHETHER it can actually be
frozen and used to generate a test submission, and emits one ranking.

Deliverability is a hard requirement, not a preference - §5 says the selected scheme must be fitted on
the allowed training data with features, parameters, ensemble and post-processing fixed, then used to
produce submission.csv covering every test row. A candidate whose test-period inputs no longer exist is
recorded as not deliverable and cannot win, because selecting it would produce a submission nobody can
regenerate or audit.

It also records the cumulative search size, since that is what the winner's score has to be read
against: every wave maximized over the same five viewed years and no blind period remains.
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(HERE))
import connected_scorer as cs  # noqa: E402

ARCHIVE = ROOT.parent / "赛题五_历史归档_20261001"
ALLMODELS = ARCHIVE / "analysis/all_models_test_20260929"
CONFIRMED = "peer67_slow16"

# What each wave's candidates are, and what a winner from that wave would need on the test side.
MECHANISM = {
    "connected_results_all.json": {
        "wave": "1-3", "mechanism": "single historical scheme, rebuilt from surviving fold predictions",
    },
    "wave6_results.json": {
        "wave": "6", "mechanism": "peer67_slow16 backbone with a re-tuned post-processing stack",
    },
    "wave7b_results.json": {
        "wave": "7b", "mechanism": "Top-set substitution (slot reassignment) with an exact "
                                   "swap-budget retention floor",
    },
    "wave8_results.json": {
        "wave": "8", "mechanism": "Top-set substitution with both donors' post-processing re-tuned",
    },
    "wave8b_results.json": {
        "wave": "8b", "mechanism": "retention-floor shape refinement around the wave-7b optimum",
    },
    "wave9_results.json": {
        "wave": "9", "mechanism": "exhaustive one-dimensional search of each donor role over the "
                                  "screened library",
    },
    "wave10_results.json": {
        "wave": "10", "mechanism": "retention floor re-optimised for the donor pair wave 9 selected",
    },
    "wave11_results.json": {
        "wave": "11", "mechanism": "finalists re-scored on the exact shipped construction, with the "
                                   "deterministic tie-break included",
    },
}
# Test-period inputs that exist, by donor. A scheme is deliverable only if every donor it uses is.
DELIVERABLE_DONORS = {
    "topk": {"test_artifact": str(ALLMODELS / "middle/predictions/supplemental_topk_fulltrain2024.parquet"),
             "note": "finished test column at the released post-processing; a re-tuned post-processing "
                     "would need a fulltrain re-fit (~193 s) via middle/run_middle.py::supplemental_topk, "
                     "verifiable against this column"},
    "W5a_five_way_with_gru": {"test_artifact": str(ALLMODELS / "early/predictions/early_9ec487b9f99e6f94.npy"),
                              "note": "keyless .npy in the early-scope panel order, which is date-major "
                                      "over features.parquet[~is_train] and was proved identical to "
                                      "releases/pooled_rms25/backbone_raw.parquet sorted the same way; "
                                      "GRU checkpoints survive in early/models/ so it is re-predictable"},
    "peer67_slow16": {"test_artifact": str(ARCHIVE / "deliveries/peer67_slow16_20260929/prediction.parquet"),
                      "note": "carries pred_raw, so ANY post-processing can be re-applied; the delivery "
                              "verification already proved the submission rebuilds byte-identically from "
                              "the 16 saved .ubj models"},
}


def load(name: str):
    path = HERE / name
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else None


def resolve_donor(donor: str):
    """Map a candidate's donor label onto a donor whose test-period inputs are known to survive."""
    donor = str(donor)
    if donor.startswith("pp_") or donor.startswith("pp::"):
        return "peer67_slow16"
    if donor[:2] in ("a0", "a0.") or donor.startswith("a0_") or donor.startswith("a0."):
        # wave 10/11 shorthand for a peer67_slow16 post-processing variant
        return "peer67_slow16"
    if donor.startswith("W5a"):
        return "W5a_five_way_with_gru"
    if donor.startswith("nested"):
        # its inner member was built with wave 1's lift construction, which this builder does not
        # reproduce; shipping it needs that construction re-implemented and re-scored first
        return None
    for alias, canonical in (("slow16_rel", "peer67_slow16"),
                             ("slow16_a08b06", "peer67_slow16"),
                             ("a0b015", "peer67_slow16"),
                             ("topk_rel", "topk"), ("topk_a08b06", "topk"),
                             ("topk_a09b06", "topk")):
        if donor == alias:
            return canonical
    return next((k for k in DELIVERABLE_DONORS if k in donor), None)


def deliverability(name: str, record: dict, wave: str) -> dict:
    """Which donors a candidate needs, and whether their test-period inputs survive.

    Waves 1-3 re-scored historical schemes whose test-period deliverability varies case by case (some
    used test features that cannot be delivered, some depend on caches the cleanup deleted), so they
    are recorded as not assessed rather than silently assumed deliverable. Wave 6 variants are all the
    peer67_slow16 backbone with a different post-processing stack, and that delivery package saves
    pred_raw, so any of them can be regenerated.
    """
    member = record.get("member") or record.get("base")
    orderer = record.get("orderer")
    if wave in ("1-3",):
        return {"donors": [], "missing_test_inputs": [], "deliverable": None,
                "note": "historical scheme; test-period deliverability not assessed case by case"}
    if wave == "6":
        return {"donors": [{"role": "single", "name": "peer67_slow16",
                            **{k: v for k, v in DELIVERABLE_DONORS["peer67_slow16"].items()}}],
                "missing_test_inputs": [], "deliverable": True,
                "note": "post-processing variant of a backbone whose delivery package saves pred_raw"}
    needed, missing = [], []
    for role, donor in (("membership", member), ("ordering", orderer)):
        if not donor:
            continue
        # a wave-6 post-processing column is the peer67_slow16 backbone under a different stack, and
        # that backbone's delivery package saves pred_raw, so any stack can be re-applied
        resolved = resolve_donor(donor)
        needed.append({"role": role, "name": donor, "resolved_donor": resolved,
                       "test_artifact": DELIVERABLE_DONORS[resolved]["test_artifact"]
                       if resolved else None})
        if resolved is None:
            missing.append(f"{role} donor {donor}")
    return {"donors": needed, "missing_test_inputs": missing, "deliverable": not missing}


def main() -> None:
    rows, search_size = [], 0
    for filename, meta in MECHANISM.items():
        payload = load(filename)
        if payload is None:
            cs.log(f"{filename}: not present yet, skipped")
            continue
        results = payload.get("results", {})
        for name, record in results.items():
            if not isinstance(record, dict) or "connected_final_score" not in record:
                continue
            search_size += 1
            metrics = record.get("connected_metrics", {})
            rows.append({
                "name": name, "wave": meta["wave"], "mechanism": meta["mechanism"],
                "connected_final_score": record["connected_final_score"],
                "ic_mean": metrics.get("ic_mean"), "annual_excess": metrics.get("annual_excess"),
                "mean_turnover": metrics.get("mean_turnover"),
                "member": record.get("member") or record.get("base"),
                "orderer": record.get("orderer"), "m_frac": record.get("m_frac"),
                **deliverability(name, record, meta["wave"]),
            })

    rows.sort(key=lambda r: -r["connected_final_score"])
    for rank, row in enumerate(rows, start=1):
        row["rank"] = rank
    confirmed = next((r for r in rows if r["name"] == CONFIRMED), None)
    deliverable = [r for r in rows if r["deliverable"] is True]
    winner = deliverable[0] if deliverable else None

    payload = {
        "status": "complete", "completed_at_local": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "standard": "后续选模标准.md §3 connected 2020-2024 official composite is the sole primary "
                    "score; §4 highest score among compliant candidates wins, complexity and cost are "
                    "tie-breaks only; §5 the winner must be freezable and able to generate "
                    "submission.csv",
        "candidates_scored_under_this_caliber": search_size,
        "waves_included": sorted({r["wave"] for r in rows}),
        "selection_basis": "training period 2020-2024 only; no test-period label influenced any "
                           "ranking in this table",
        "cumulative_search_disclosure": f"{search_size} candidates were maximized over the same five "
                                        "repeatedly viewed years across nine waves. No blind period "
                                        "remains, so the top of this table carries cumulative upward "
                                        "selection bias that cannot be quantified here; the split-half "
                                        "transfer analysis is reported alongside it rather than used "
                                        "as a gate.",
        "confirmed_model_row": confirmed,
        "winner": winner,
        "winner_gain_over_confirmed": (winner["connected_final_score"]
                                       - confirmed["connected_final_score"])
                                      if winner and confirmed else None,
        "best_regardless_of_deliverability": rows[0] if rows else None,
        "ranking": rows,
        "deliverable_donor_inventory": DELIVERABLE_DONORS,
    }
    (HERE / "master_ranking.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"candidates scored under the connected caliber: {search_size}")
    if confirmed:
        print(f"confirmed model {CONFIRMED}: rank {confirmed['rank']} of {len(rows)}, "
              f"{confirmed['connected_final_score']:.9f}")
    if winner:
        print(f"\nWINNER (highest connected score among deliverable candidates):")
        print(f"  {winner['name']}")
        print(f"  connected {winner['connected_final_score']:.9f}  "
              f"(ic {winner['ic_mean']:.6f}, excess {winner['annual_excess']:.6f}, "
              f"turnover {winner['mean_turnover']:.6f})")
        print(f"  gain over the confirmed model: "
              f"{payload['winner_gain_over_confirmed']:+.9f}")
        print(f"  wave {winner['wave']}: {winner['mechanism']}")
    print(f"\n| rank | candidate | wave | CONNECTED | IC | excess | turnover | deliverable |")
    print("|---|---|---|---|---|---|---|---|")
    for row in rows[:25]:
        print(f"| {row['rank']} | {row['name'][:46]} | {row['wave']} | "
              f"**{row['connected_final_score']:.9f}** | "
              f"{row['ic_mean']:.6f} | {row['annual_excess']:.6f} | "
              f"{row['mean_turnover']:.6f} | {row['deliverable']} |")
    not_deliverable = [r for r in rows[:15] if not r["deliverable"]]
    if not_deliverable:
        print("\ntop-15 candidates that are NOT deliverable (missing test-period inputs):")
        for row in not_deliverable:
            print(f"  rank {row['rank']} {row['name'][:60]}: {row['missing_test_inputs']}")


if __name__ == "__main__":
    main()
