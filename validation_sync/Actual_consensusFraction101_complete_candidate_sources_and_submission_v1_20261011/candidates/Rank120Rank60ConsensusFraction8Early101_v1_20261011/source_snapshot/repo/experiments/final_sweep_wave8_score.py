"""Scoring stage for wave 8: combination rule and ensemble-specific post-processing.

Split from final_sweep_wave8.py so that scoring-side fixes can never invalidate the
frozen protocol that pins the rules and the grid. Four stages, each one-shot and each
refusing to overwrite a recorded result:

  select   suite B only. Nine (alpha, bonus) pairs are scored on 2020 and 2021 in the
           no-blend caliber on the materialized W3e raw; the maximin winner against the
           recorded W3e composite is written to disk before any gated year is touched.
  develop  2022 and 2023 through the full released stack, anchored to 1e-12, for the two
           suite-A rules and, if it differs from the released pair, the suite-B winner.
  confirm  2024 once, only for candidates that already passed develop. This suite keeps
           its own confirmation stage because a suite-B candidate carries a post-processing
           override that the generic experiments.final_sweep_confirm cannot express.
  audit    2020 and 2021 for suite-A candidates that survived all three gated years.
           Suite B is excluded by protocol: those years are its selection years.

Both comparators are checked in every scored year: the pooled_rms25 released composite
(the historical anchor, for comparability with waves 1-7) and the recorded W3e composite
(the currently adopted release, and therefore the decision-relevant test).
"""
from __future__ import annotations

import argparse
import json
import time

import numpy as np
import polars as pl

from src.scoring import Panel, restore_lower_ranks
from experiments.bonus_extension import (BASE_BONUS, BLEND_WEIGHT, file_hash, load_auxiliary,
                                         load_panel, release_scores)
from experiments.extended_audit import audit_score
from experiments.final_sweep import blend_top_only, retention_scores, RELEASED
from experiments.final_sweep_wave5 import AUDIT, KEYS, OUT, log, panel_frame
from experiments.final_sweep_wave8 import (AUDIT_YEARS, DEVELOPMENT_YEARS, DIAGNOSTIC_YEAR, GRID,
                                           RELEASED_PP, RULE_CANDIDATES, W3E_KEY, W3E_PINNED,
                                           verify_protocol)
from experiments.official_seed_development import official_score

NUMERIC_TOLERANCE = 1e-12
TIE_TOLERANCE = 1e-15
REFERENCE = W3E_PINNED
AUDIT_RECORD = AUDIT / "audit_results.json"
SCORED_YEARS = DEVELOPMENT_YEARS + (DIAGNOSTIC_YEAR,)
BACKBONE = "released_lgb_backbone"


def stack(panel: Panel, raw: np.ndarray, auxiliary: np.ndarray | None, alpha: float,
          bonus: float) -> np.ndarray:
    """The released post-processing stack with alpha and bonus as explicit arguments."""
    stable = retention_scores(panel, raw, alpha, bonus, "standard")
    if auxiliary is None:
        return restore_lower_ranks(panel, stable, raw, 1.0)
    return blend_top_only(panel, stable, raw, auxiliary, BLEND_WEIGHT)


def cache_raw(year: int, key: str, panel: Panel) -> np.ndarray:
    frame = pl.read_parquet(OUT / f"{key}_{year}.parquet").sort("trade_date", "ts_code")
    if not frame.select(KEYS).equals(panel.frame.select(KEYS)):
        raise AssertionError(f"{key} {year}: cache keys misaligned with the panel")
    return frame["pred_raw"].to_numpy().astype(np.float64)


def pp_key(config: dict) -> str:
    return f"W8c_pp_a{config['alpha']:.2f}_b{config['bonus']:.2f}"


def inventory() -> dict:
    record = json.loads((OUT / "training_wave8.json").read_text(encoding="utf-8"))
    if record["protocol_sha256"] != file_hash(OUT / "protocol_wave8.json"):
        raise SystemExit("Wave-8 caches were built under a different protocol")
    return record


def pinned(year: int, key: str) -> str:
    return inventory()["caches"][str(year)][key]["sha256"]


def check_pinned(year: int, key: str) -> None:
    if file_hash(OUT / f"{key}_{year}.parquet") != pinned(year, key):
        raise SystemExit(f"{key} {year}: cache hash drifted from the pinned inventory")


def reference_scores() -> dict:
    """The recorded W3e composite in all five years, read from the frozen earlier records."""
    develop = json.loads((OUT / "development_wave3.json").read_text(encoding="utf-8"))
    confirm = json.loads((OUT / "confirmation_wave3.json").read_text(encoding="utf-8"))
    prior = json.loads(AUDIT_RECORD.read_text(encoding="utf-8"))
    scores = {year: develop["candidates"][REFERENCE]["years"][str(year)]["final_score"]
              for year in DEVELOPMENT_YEARS}
    scores[DIAGNOSTIC_YEAR] = confirm["records"][REFERENCE]["final_score"]
    for year in AUDIT_YEARS:
        scores[year] = prior["years"][str(year)][REFERENCE]["final_score"]
    return scores


def reference_deltas() -> dict:
    prior = json.loads(AUDIT_RECORD.read_text(encoding="utf-8"))
    return {year: prior["years"][str(year)][REFERENCE]["delta_vs_released"] for year in AUDIT_YEARS}


def audit_anchors(year: int, panel: Panel, frame: pl.DataFrame, reference: dict) -> dict:
    """Reproduce both recorded audit-year baselines to 1e-12 before scoring anything new."""
    prior = json.loads(AUDIT_RECORD.read_text(encoding="utf-8"))
    backbone = frame["pred_raw"].to_numpy().astype(np.float64)
    base, _ = audit_score(panel, stack(panel, backbone, None, RELEASED["alpha"], BASE_BONUS), year)
    expected = prior["years"][str(year)][BACKBONE]["final_score"]
    if abs(base["final_score"] - expected) > NUMERIC_TOLERANCE:
        raise AssertionError(f"{year}: audit backbone anchor off by "
                             f"{base['final_score'] - expected:.3e}")
    check_pinned(year, W3E_KEY)
    raw = cache_raw(year, W3E_KEY, panel)
    ref, _ = audit_score(panel, stack(panel, raw, None, RELEASED_PP["alpha"], RELEASED_PP["bonus"]),
                         year)
    if abs(ref["final_score"] - reference[year]) > NUMERIC_TOLERANCE:
        raise AssertionError(f"{year}: materialized W3e raw does not reproduce the recorded audit "
                             f"composite ({ref['final_score']:.12f} vs {reference[year]:.12f})")
    log(f"{year} audit anchors reproduced: backbone {expected:.9f}, W3e {reference[year]:.9f}")
    return {"released_backbone": {k: float(v) for k, v in base.items()},
            "w3e_at_released_pp": {k: float(v) for k, v in ref.items()}}


def scored_anchors(year: int, panel: Panel, auxiliary: np.ndarray, reference: dict) -> dict:
    released = {int(k): float(v) for k, v in release_scores().items()}
    backbone = panel.frame["pred_raw"].to_numpy().astype(np.float64)
    base, _ = official_score(panel, stack(panel, backbone, auxiliary, RELEASED["alpha"], BASE_BONUS),
                             year)
    if abs(base["final_score"] - released[year]) > NUMERIC_TOLERANCE:
        raise AssertionError(f"{year}: released backbone anchor off")
    log(f"{year} baseline anchor reproduced {released[year]:.15f} exactly")
    return {"released_backbone": {k: float(v) for k, v in base.items()},
            "released_composite": released[year], "recorded_w3e": reference[year]}


def develop_candidates() -> list:
    """Suite A plus the suite-B winner, formed only from the frozen protocol and selection."""
    candidates = [{"key": item["key"], "suite": "A", "raw": item["key"], "rule": item["rule"],
                   "alpha": RELEASED_PP["alpha"], "bonus": RELEASED_PP["bonus"],
                   "primary": item["primary"], "note": item["note"]} for item in RULE_CANDIDATES]
    selection = json.loads((OUT / "selection_wave8.json").read_text(encoding="utf-8"))
    winner = selection["winner"]
    if selection["winner_differs_from_released"]:
        candidates.append({"key": pp_key(winner), "suite": "B", "raw": W3E_KEY, "rule": "rank_average",
                           "alpha": winner["alpha"], "bonus": winner["bonus"], "primary": False,
                           "note": "the W3e rank average with post-processing re-selected on "
                                   "2020+2021"})
    else:
        log("Suite B selected the released pair (0.9, 0.3): keep as is, nothing to develop")
    return candidates


def select() -> None:
    verify_protocol()
    result_path = OUT / "selection_wave8.json"
    if result_path.exists():
        raise SystemExit("Wave-8 selection already recorded; preserving it")
    inventory()
    reference = reference_scores()
    started = time.monotonic()
    grid, anchors = {}, {}
    for year in AUDIT_YEARS:
        frame = panel_frame(year)
        panel = Panel.from_frame(frame)
        anchors[str(year)] = audit_anchors(year, panel, frame, reference)
        raw = cache_raw(year, W3E_KEY, panel)
        for config in GRID:
            key = pp_key(config)
            metrics, daily = audit_score(panel, stack(panel, raw, None, config["alpha"],
                                                      config["bonus"]), year)
            daily.write_csv(OUT / f"{key}_{year}_daily.csv")
            entry = grid.setdefault(key, {"config": config, "years": {}})
            entry["years"][str(year)] = {k: float(v) for k, v in metrics.items()}
            log(f"{year} {key}: score={metrics['final_score']:.9f} "
                f"delta_vs_w3e={metrics['final_score'] - reference[year]:+.9f}")
        del panel, frame, raw
    for key, entry in grid.items():
        deltas = {y: entry["years"][y]["final_score"] - reference[int(y)]
                  for y in map(str, AUDIT_YEARS)}
        entry["delta_vs_w3e"] = deltas
        entry["maximin_delta"] = min(deltas.values())
        entry["mean_delta"] = sum(deltas.values()) / len(deltas)
        entry["is_released_pair"] = entry["config"] == RELEASED_PP
    best = max(entry["maximin_delta"] for entry in grid.values())
    tied = sorted((key for key, entry in grid.items()
                   if entry["maximin_delta"] >= best - TIE_TOLERANCE),
                  key=lambda k: (not grid[k]["is_released_pair"], grid[k]["config"]["alpha"],
                                 grid[k]["config"]["bonus"]))
    winner_key = tied[0]
    winner = grid[winner_key]["config"]
    output = {
        "stage": "select_wave8", "generated_at_local": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "elapsed_seconds": time.monotonic() - started,
        "protocol_sha256": file_hash(OUT / "protocol_wave8.json"),
        "selection_years": list(AUDIT_YEARS), "caliber": "no pooled blend; identical for every "
                                                         "grid point and for the W3e reference",
        "objective": "maximin over 2020+2021 of the composite minus the recorded W3e composite at "
                     "the released pair (0.9, 0.3)",
        "anchors": anchors, "grid": grid, "tied_keys": tied,
        "winner_key": winner_key, "winner": winner,
        "winner_differs_from_released": bool(winner != RELEASED_PP),
        "winner_maximin_delta": grid[winner_key]["maximin_delta"],
        "note": "Written before any gated year was scored; the winner is not re-selectable.",
    }
    result_path.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")
    log(f"WAVE-8 SELECTION: winner {winner_key} maximin={grid[winner_key]['maximin_delta']:+.9f} "
        f"(differs from released pair: {output['winner_differs_from_released']})")


def develop() -> None:
    protocol = verify_protocol()
    if tuple(protocol["development_years"]) != DEVELOPMENT_YEARS:
        raise SystemExit("Scorer years disagree with the frozen protocol")
    result_path = OUT / "development_wave8.json"
    if result_path.exists():
        raise SystemExit("Wave-8 development already recorded; preserving it")
    if not (OUT / "selection_wave8.json").exists():
        raise SystemExit("Run the select stage first; the suite-B winner must be fixed beforehand")
    reference = reference_scores()
    released = {int(k): float(v) for k, v in release_scores().items()}
    candidates = develop_candidates()
    started = time.monotonic()
    records, anchors = {}, {}
    for year in DEVELOPMENT_YEARS:
        panel = load_panel(year)
        auxiliary = load_auxiliary(year, panel)
        anchors[str(year)] = scored_anchors(year, panel, auxiliary, reference)
        for candidate in candidates:
            key = candidate["key"]
            check_pinned(year, candidate["raw"])
            raw = cache_raw(year, candidate["raw"], panel)
            metrics, daily = official_score(
                panel, stack(panel, raw, auxiliary, candidate["alpha"], candidate["bonus"]), year)
            daily.write_csv(OUT / f"{key}_{year}_daily.csv")
            entry = records.setdefault(key, {k: v for k, v in candidate.items() if k != "key"})
            entry.setdefault("years", {})[str(year)] = {k: float(v) for k, v in metrics.items()}
            log(f"{year} {key}: score={metrics['final_score']:.9f} ic={metrics['ic_mean']:.6f} "
                f"excess={metrics['annual_excess']:.6f} turn={metrics['mean_turnover']:.6f} "
                f"vs_released={metrics['final_score'] - released[year]:+.9f} "
                f"vs_w3e={metrics['final_score'] - reference[year]:+.9f}")
        del panel, auxiliary
    for key, entry in records.items():
        versus_released = {y: entry["years"][y]["final_score"] - released[int(y)]
                           for y in map(str, DEVELOPMENT_YEARS)}
        versus_w3e = {y: entry["years"][y]["final_score"] - reference[int(y)]
                      for y in map(str, DEVELOPMENT_YEARS)}
        entry["delta_vs_released"] = versus_released
        entry["delta_vs_w3e"] = versus_w3e
        entry["passes_development_gate"] = (all(v > NUMERIC_TOLERANCE for v in versus_released.values())
                                            and all(v > NUMERIC_TOLERANCE for v in versus_w3e.values()))
        entry["minimax_delta_vs_w3e"] = min(versus_w3e.values())
    passing = [k for k, v in records.items() if v["passes_development_gate"]]
    output = {"stage": "develop_wave8", "generated_at_local": time.strftime("%Y-%m-%dT%H:%M:%S"),
              "elapsed_seconds": time.monotonic() - started,
              "protocol_sha256": file_hash(OUT / "protocol_wave8.json"),
              "comparators": {"released_backbone": {str(y): released[y] for y in DEVELOPMENT_YEARS},
                              "recorded_w3e": {str(y): reference[y] for y in DEVELOPMENT_YEARS}},
              "anchors": anchors, "candidates": records,
              "candidates_passing_development_gate": passing,
              "gate": protocol["adoption_gate"], "caveat": protocol["limitations"]}
    result_path.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")
    log(f"WAVE-8 DEVELOPMENT: {len(passing)} of {len(records)} pass: {passing}")


def confirm() -> None:
    protocol = verify_protocol()
    result_path = OUT / "confirmation_wave8.json"
    if result_path.exists():
        raise SystemExit("Wave-8 confirmation already recorded; preserving it")
    develop_record = json.loads((OUT / "development_wave8.json").read_text(encoding="utf-8"))
    passing = develop_record["candidates_passing_development_gate"]
    if not passing:
        raise SystemExit("No wave-8 candidate passed the development gate; nothing to confirm")
    reference = reference_scores()
    released = {int(k): float(v) for k, v in release_scores().items()}
    candidates = {c["key"]: c for c in develop_candidates()}
    year = DIAGNOSTIC_YEAR
    started = time.monotonic()
    panel = load_panel(year)
    auxiliary = load_auxiliary(year, panel)
    anchors = scored_anchors(year, panel, auxiliary, reference)
    records = {}
    for key in passing:
        candidate = candidates[key]
        check_pinned(year, candidate["raw"])
        raw = cache_raw(year, candidate["raw"], panel)
        metrics, daily = official_score(
            panel, stack(panel, raw, auxiliary, candidate["alpha"], candidate["bonus"]), year)
        daily.write_csv(OUT / f"{key}_{year}_daily.csv")
        records[key] = {**{k: float(v) for k, v in metrics.items()},
                        "delta_vs_released": float(metrics["final_score"]) - released[year],
                        "delta_vs_w3e": float(metrics["final_score"]) - reference[year]}
        records[key]["passes_diagnostic_gate"] = bool(
            records[key]["delta_vs_released"] > NUMERIC_TOLERANCE
            and records[key]["delta_vs_w3e"] > NUMERIC_TOLERANCE)
        log(f"{year} {key}: score={metrics['final_score']:.9f} ic={metrics['ic_mean']:.6f} "
            f"excess={metrics['annual_excess']:.6f} turn={metrics['mean_turnover']:.6f} "
            f"vs_released={records[key]['delta_vs_released']:+.9f} "
            f"vs_w3e={records[key]['delta_vs_w3e']:+.9f}")
    three_year = {}
    for key in passing:
        versus_released = dict(develop_record["candidates"][key]["delta_vs_released"])
        versus_w3e = dict(develop_record["candidates"][key]["delta_vs_w3e"])
        versus_released[str(year)] = records[key]["delta_vs_released"]
        versus_w3e[str(year)] = records[key]["delta_vs_w3e"]
        three_year[key] = {"suite": candidates[key]["suite"], "delta_vs_released": versus_released,
                           "delta_vs_w3e": versus_w3e,
                           "mean_delta_vs_w3e": sum(versus_w3e.values()) / len(versus_w3e),
                           "minimax_delta_vs_w3e": min(versus_w3e.values()),
                           "passes_three_year_gate": (records[key]["passes_diagnostic_gate"]
                                                      and all(v > NUMERIC_TOLERANCE
                                                              for v in versus_w3e.values()))}
    adopted = [k for k, v in three_year.items() if v["passes_three_year_gate"]]
    output = {"stage": "confirm_wave8", "generated_at_local": time.strftime("%Y-%m-%dT%H:%M:%S"),
              "elapsed_seconds": time.monotonic() - started, "diagnostic_year": year,
              "protocol_sha256": file_hash(OUT / "protocol_wave8.json"),
              "released_composite": released[year], "recorded_w3e": reference[year],
              "anchors": anchors, "records": records, "three_year_summary": three_year,
              "candidates_passing_three_year_gate": adopted,
              "note": "Scored once, after the development years were recorded; no development year "
                      "was re-scored and no rule was changed.",
              "caveat": protocol["limitations"]}
    result_path.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")
    log(f"WAVE-8 CONFIRMATION: {len(adopted)} of {len(passing)} pass all three gated years: {adopted}")


def audit() -> None:
    """Score the never-gated years for suite-A survivors; suite B is excluded by protocol."""
    protocol = verify_protocol()
    result_path = OUT / "audit_wave8.json"
    if result_path.exists():
        raise SystemExit("Wave-8 audit already recorded; preserving it")
    confirmation = json.loads((OUT / "confirmation_wave8.json").read_text(encoding="utf-8"))
    eligible = [key for key in confirmation["candidates_passing_three_year_gate"]
                if key in {item["key"] for item in RULE_CANDIDATES}]
    excluded = [key for key in confirmation["candidates_passing_three_year_gate"]
                if key not in {item["key"] for item in RULE_CANDIDATES}]
    if excluded:
        log(f"Excluded from the audit by protocol (selection years are 2020/2021): {excluded}")
    if not eligible:
        raise SystemExit("No suite-A candidate passed the three-year gate; nothing to audit")
    reference, reference_delta = reference_scores(), reference_deltas()
    started = time.monotonic()
    results = {"years": {}}
    for year in AUDIT_YEARS:
        frame = panel_frame(year)
        panel = Panel.from_frame(frame)
        anchors = audit_anchors(year, panel, frame, reference)
        entries = dict(anchors)
        for key in eligible:
            check_pinned(year, key)
            raw = cache_raw(year, key, panel)
            metrics, daily = audit_score(panel, stack(panel, raw, None, RELEASED_PP["alpha"],
                                                      RELEASED_PP["bonus"]), year)
            daily.write_csv(OUT / f"{key}_{year}_daily.csv")
            entries[key] = {**{k: float(v) for k, v in metrics.items()},
                            "delta_vs_released": float(metrics["final_score"])
                            - anchors["released_backbone"]["final_score"],
                            "delta_vs_w3e": float(metrics["final_score"]) - reference[year],
                            "recorded_w3e_delta": reference_delta[year]}
            log(f"{year} {key}: score={metrics['final_score']:.9f} "
                f"vs_released={entries[key]['delta_vs_released']:+.9f} "
                f"vs_w3e={entries[key]['delta_vs_w3e']:+.9f}")
        results["years"][str(year)] = entries
        del panel, frame
    summary = {}
    for key in eligible:
        versus_released = [results["years"][str(y)][key]["delta_vs_released"] for y in AUDIT_YEARS]
        versus_w3e = [results["years"][str(y)][key]["delta_vs_w3e"] for y in AUDIT_YEARS]
        summary[key] = {"delta_vs_released": versus_released, "delta_vs_w3e": versus_w3e,
                        "mean_delta_vs_w3e": sum(versus_w3e) / len(versus_w3e),
                        "positive_vs_released_both_years": all(d > 0 for d in versus_released),
                        "beats_w3e_both_years": all(d > 0 for d in versus_w3e),
                        "five_year_positive_vs_w3e": all(
                            d > 0 for d in versus_w3e) and all(
                            v > 0 for v in confirmation["three_year_summary"][key]["delta_vs_w3e"].values())}
    output = {"stage": "audit_wave8", "generated_at_local": time.strftime("%Y-%m-%dT%H:%M:%S"),
              "elapsed_seconds": time.monotonic() - started, "audit_years": list(AUDIT_YEARS),
              "protocol_sha256": file_hash(OUT / "protocol_wave8.json"),
              "caliber": "released stack without the pooled blend, identical for baseline and "
                         "candidate; matches the recorded extended-year audit",
              "excluded_by_protocol": excluded, "results": results, "summary": summary,
              "caveat": protocol["limitations"]}
    result_path.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")
    for key, item in summary.items():
        log(f"WAVE-8 AUDIT {key}: vs_w3e={['%+.6f' % d for d in item['delta_vs_w3e']]} "
            f"beats_w3e_both={item['beats_w3e_both_years']} "
            f"five_year_positive={item['five_year_positive_vs_w3e']}")


def released_composites() -> dict:
    """The released backbone composite in all five years, from the two frozen records."""
    released = {int(k): float(v) for k, v in release_scores().items()}
    prior = json.loads(AUDIT_RECORD.read_text(encoding="utf-8"))
    for year in AUDIT_YEARS:
        released[year] = prior["years"][str(year)][BACKBONE]["final_score"]
    return released


def summary() -> None:
    """Merge every wave-8 record into one verdict table against the adopted release."""
    verify_protocol()
    reference = reference_scores()
    released = released_composites()
    selection = json.loads((OUT / "selection_wave8.json").read_text(encoding="utf-8"))
    rows = [{"candidate": "W3e (adopted release)", "suite": "-", "alpha": RELEASED_PP["alpha"],
             "bonus": RELEASED_PP["bonus"],
             "delta_vs_w3e": {str(y): 0.0 for y in AUDIT_YEARS + SCORED_YEARS},
             "delta_vs_released": {str(y): reference[y] - released[y]
                                   for y in AUDIT_YEARS + SCORED_YEARS},
             "verdict": "adopted"}]
    develop_path = OUT / "development_wave8.json"
    confirmation = (json.loads((OUT / "confirmation_wave8.json").read_text(encoding="utf-8"))
                    if (OUT / "confirmation_wave8.json").exists() else None)
    audit_record = (json.loads((OUT / "audit_wave8.json").read_text(encoding="utf-8"))
                    if (OUT / "audit_wave8.json").exists() else None)
    if develop_path.exists():
        develop = json.loads(develop_path.read_text(encoding="utf-8"))
        for key, entry in develop["candidates"].items():
            deltas = {y: entry["years"][y]["final_score"] - reference[int(y)]
                      for y in map(str, DEVELOPMENT_YEARS)}
            versus_released = dict(entry["delta_vs_released"])
            if confirmation and key in confirmation["records"]:
                deltas[str(DIAGNOSTIC_YEAR)] = confirmation["records"][key]["delta_vs_w3e"]
                versus_released[str(DIAGNOSTIC_YEAR)] = confirmation["records"][key]["delta_vs_released"]
            if audit_record and key in audit_record["summary"]:
                for year, value in zip(AUDIT_YEARS, audit_record["summary"][key]["delta_vs_w3e"]):
                    deltas[str(year)] = value
                for year, value in zip(AUDIT_YEARS,
                                       audit_record["summary"][key]["delta_vs_released"]):
                    versus_released[str(year)] = value
            known = [v for v in deltas.values()]
            if confirmation and key in confirmation.get("candidates_passing_three_year_gate", []):
                verdict = "passes the three-year gate"
            elif key in develop["candidates_passing_development_gate"]:
                verdict = f"passed 2022/2023, failed {DIAGNOSTIC_YEAR}"
            else:
                verdict = "failed the development gate"
            rows.append({"candidate": key, "suite": entry["suite"], "alpha": entry["alpha"],
                         "bonus": entry["bonus"],
                         "delta_vs_w3e": {y: deltas.get(y) for y in
                                          map(str, AUDIT_YEARS + SCORED_YEARS)},
                         "delta_vs_released": {y: versus_released.get(y) for y in
                                               map(str, AUDIT_YEARS + SCORED_YEARS)},
                         "years_scored": len(known), "min_delta_vs_w3e": min(known),
                         "mean_delta_vs_w3e": sum(known) / len(known), "verdict": verdict})
    output = {"stage": "summary_wave8", "generated_at_local": time.strftime("%Y-%m-%dT%H:%M:%S"),
              "protocol_sha256": file_hash(OUT / "protocol_wave8.json"),
              "released_composites": {str(y): released[y] for y in AUDIT_YEARS + SCORED_YEARS},
              "audit_stage": ("recorded" if audit_record else
                              "not reached: no candidate passed the three-year gate, and the "
                              "protocol audits only survivors"),
              "selection": {"winner_key": selection["winner_key"], "winner": selection["winner"],
                            "winner_differs_from_released": selection["winner_differs_from_released"],
                            "winner_maximin_delta_vs_w3e": selection["winner_maximin_delta"],
                            "grid_maximin": {k: v["maximin_delta"] for k, v in selection["grid"].items()}},
              "recorded_w3e": {str(y): reference[y] for y in AUDIT_YEARS + SCORED_YEARS},
              "rows": rows}
    (OUT / "wave8_summary.json").write_text(json.dumps(output, ensure_ascii=False, indent=2),
                                            encoding="utf-8")
    header = f"{'candidate':<26}{'suite':<7}" + "".join(f"{y:>13}" for y in AUDIT_YEARS + SCORED_YEARS)
    print(header + "\n" + "-" * len(header))
    for row in rows:
        cells = "".join(f"{row['delta_vs_w3e'][str(y)]:>+13.6f}"
                        if row["delta_vs_w3e"][str(y)] is not None else f"{'-':>13}"
                        for y in AUDIT_YEARS + SCORED_YEARS)
        print(f"{row['candidate']:<26}{row['suite']:<7}{cells}  {row['verdict']}")
    print("\nDeltas are candidate minus the adopted W3e release; 2020/2021 are the no-blend audit "
          "caliber, 2022-2024 the full released stack.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("stage", choices=("select", "develop", "confirm", "audit", "summary"))
    arguments = parser.parse_args()
    {"select": select, "develop": develop, "confirm": confirm, "audit": audit,
     "summary": summary}[arguments.stage]()
