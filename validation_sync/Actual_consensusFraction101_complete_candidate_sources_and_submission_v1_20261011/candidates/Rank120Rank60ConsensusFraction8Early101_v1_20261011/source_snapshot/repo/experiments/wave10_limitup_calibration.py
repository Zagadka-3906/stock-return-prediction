"""Wave-10: causal recalibration of limit-up rows in the final ranking.

WHAT THE EVALUATOR ACTUALLY MEASURES. `evaluate.py` computes Rank IC (40%) over every
labelled row, but builds the Top-decile excess (30%) and the turnover (30%) sets from
`flag_limit_up == 0` rows only. A limit-up row's score therefore reaches 40% of the
composite and none of the other 60%, and re-ordering limit-up rows *among themselves or
relative to the rest* cannot change which non-limit-up stocks form the Top decile, because
their relative order is untouched. That makes this the one lever in the project whose
portfolio terms are provably invariant, so any IC gain is a pure gain.

THE MEASURED DEFECT. `experiments/limit_up_decomposition_eval/decomposition.json`: limit-up
rows sit at mean predicted percentile 0.73-0.78 in the final ranking while their realised
label percentile averages only 0.58-0.62 — the models systematically over-rank them by
0.15-0.20. The same bias is visible in the RAW backbone output (baseline 0.777/0.837/0.842,
XGBoost 0.744/0.806/0.812 in 2020/2022/2024), so it is a model calibration defect that the
post-processing stack only partially damps. Oracle ceilings: within-group reordering
+0.004427 composite, placement +0.006036, both together +0.010463. A blanket *lift* of
these rows to the top — the intuitive guess, and the wrong direction — captured only
+0.000197 and was negative in 2022 and 2024 (`experiments/limit_up_rule_eval/results.json`).

THE RULE. Per fold, estimate q = the mean realised label percentile of limit-up rows over
that fold's purged TRAINING rows only (causal; the statistic is stable at 0.578-0.619 across
the five validation years). Per day, map each limit-up row's percentile p to
p' = p + lambda * (q - mean(p over that day's limit-up rows)), leave every other row's score
byte-identical, and convert p' back to a score through the day's own empirical score
distribution. lambda = 0 reproduces the input exactly; lambda = 1 recentres the group's mean
percentile onto q while preserving its internal order.

DISCIPLINE. lambda is selected on 2020-2022 only and confirmed once on 2023-2024. Every
rule must reproduce the frozen reference composite exactly at lambda = 0, and must show an
excess delta and a turnover delta of exactly zero, or the run aborts. All five years have
been examined many times, so this is exploratory and no number here is out-of-sample
evidence. Writes only inside experiments/wave10_limitup_calibration_20260927/.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import time
from pathlib import Path

import numpy as np
import polars as pl

from run import ROOT, FEATURE_FILE
from experiments.revalidate_fold_local import boundaries, calendar, score_official

R4 = ROOT / "experiments" / "revalidation_20260926" / "validation"
R5 = ROOT / "experiments" / "optimization_r5_20260926"
OUT = ROOT / "experiments" / "wave10_limitup_calibration_20260927"
KEYS = ["ts_code", "trade_date"]
YEARS = (2020, 2021, 2022, 2023, 2024)
DEVELOPMENT = (2020, 2021, 2022)
CONFIRMATION = (2023, 2024)
LAMBDAS = (0.25, 0.50, 1.00)
PRIMARY = "xgboost"
REPORTED = ("xgboost", "baseline", "ensemble4", "xgb_two_mean")
GATES = {
    "development": {"mean_score_delta_min": .0005, "worst_year_score_delta_min": -.0005,
                    "mean_ic_delta_min": .0002},
    "confirmation": {"mean_score_delta_min": .0005, "both_years_positive": True},
}
PROTOCOL = {
    "experiment": "wave10_causal_limit_up_recalibration",
    "status": "exploratory_all_years_previously_viewed",
    "primary_reference": PRIMARY,
    "reported_references": list(REPORTED),
    "lambdas": list(LAMBDAS),
    "rule": "per day, limit-up rows' percentiles are shifted by lambda * (q - their mean "
            "percentile that day) and mapped back through the day's own empirical score "
            "distribution; every other row's score is left byte-identical",
    "q_estimation": "mean of (y_rank + 0.5) over the fold's purged training rows with "
                    "flag_limit_up == 1, price_valid and a non-null label; training rows only, "
                    "so q is causal and never sees the validation year",
    "development_years": list(DEVELOPMENT), "confirmation_years": list(CONFIRMATION),
    "selection_rule": "among lambdas whose mean development delta against the primary reference "
                      "passes every development threshold, take the highest mean official score; "
                      "exact ties prefer the smaller lambda; select one or none",
    "gates": GATES,
    "portfolio_neutrality": "hard requirement, checked per rule per year: the annual excess and "
                            "the mean turnover must equal the reference's to the last bit, because "
                            "the evaluator builds both from flag_limit_up == 0 rows whose relative "
                            "order is untouched. A non-zero delta aborts the run.",
    "anchor": "lambda = 0 must reproduce the frozen reference composite exactly in every year "
              "before any lambda is scored",
    "measured_ceiling": {"within_group_oracle": .004427, "placement_oracle": .006036,
                         "full_oracle": .010463,
                         "blanket_lift_to_top": .000197,
                         "source": "experiments/limit_up_decomposition_eval/decomposition.json and "
                                   "experiments/limit_up_rule_eval/results.json"},
    "prohibited": ["Adding a lambda, a backbone or a year after any score exists",
                   "Estimating q from validation-year rows",
                   "Relaxing the portfolio-neutrality requirement",
                   "Changing the rule's functional form after seeing a lambda's result",
                   "Writing outside experiments/wave10_limitup_calibration_20260927/",
                   "Touching releases/, outputs/, active_release.json or maintenance/"],
    "limitations": [
        "All five years have been examined by nine earlier suites, the r4 revalidation and the r5 "
        "round; a pass is evidence against a fluke, not out-of-sample proof.",
        "The gain is IC-term alignment. Limit-up stocks are excluded from the portfolio terms, so "
        "this improves the measured score without changing the portfolio those terms describe. It "
        "must be disclosed as metric alignment plus a genuine calibration fix, never as a trading "
        "gain on its own.",
        "q is estimated per fold from a stable statistic (0.578-0.619 across five years), so it is "
        "not a tuned parameter, but it is still estimated on historical data.",
        "The rule corrects the group's mean placement only; the within-group ceiling of +0.004427 "
        "would need a model that discriminates between limit-up stocks, which is not attempted here.",
    ],
}


def log(message: str) -> None:
    print(f"[{time.strftime('%H:%M:%S')}] {message}", flush=True)


def sha(path: Path) -> str:
    digest = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for block in iter(lambda: stream.read(8 * 1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def read(path: Path) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8-sig"))


def write_new(path: Path, payload) -> None:
    with Path(path).open("x", encoding="utf-8") as stream:
        json.dump(payload, stream, ensure_ascii=False, indent=2, allow_nan=False)


def percentiles(values: np.ndarray) -> np.ndarray:
    order = np.argsort(values, kind="stable")
    ranks = np.empty(len(values), dtype=np.float64)
    ranks[order] = np.arange(len(values), dtype=np.float64)
    return ranks / max(len(values) - 1, 1)


def reference_frame(name: str, year: int) -> pl.DataFrame:
    folder = R5 if name == "xgb_two_mean" else R4
    return pl.read_parquet(folder / f"predictions_{name}_{year}.parquet").sort("trade_date", "ts_code")


def reference_metrics(name: str, year: int) -> dict:
    if name == "xgb_two_mean":
        fold = read(R5 / f"fold_{year}.json")
        if name in fold["references"]:
            return {k: float(v) for k, v in fold["references"][name].items()}
        return {k: float(v) for k, v in fold["candidates"][name]["metrics"].items()}
    return {k: float(v) for k, v in read(R4 / f"result_{year}.json")["metrics"][name].items()}


def estimate_q(year: int) -> dict:
    """Mean realised label percentile of limit-up rows over the fold's purged training rows."""
    cutoff = boundaries(year, calendar())["one_day_cutoff_exclusive"]
    frame = (pl.scan_parquet(FEATURE_FILE)
             .filter(pl.col("is_train") & (pl.col("trade_date") < cutoff) & pl.col("price_valid")
                     & pl.col("y_rank").is_not_null() & (pl.col("flag_limit_up") == 1))
             .select([((pl.col("y_rank") + 0.5).mean()).alias("q"), pl.len().alias("rows")])
             .collect())
    q = float(frame["q"][0])
    rows = int(frame["rows"][0])
    if not 0.0 < q < 1.0 or rows < 1000:
        raise AssertionError(f"{year}: implausible causal q={q} from {rows} training rows")
    return {"q": q, "training_limit_up_rows": rows, "cutoff_exclusive": int(cutoff)}


def recenter(prediction: np.ndarray, dates: np.ndarray, treated: np.ndarray, q: float,
             lam: float) -> np.ndarray:
    """Shift limit-up rows toward percentile q, leaving every other score byte-identical."""
    out = prediction.copy()
    if lam == 0.0:
        return out
    for day in np.unique(dates):
        rows = np.flatnonzero(dates == day)
        group = rows[treated[rows]]
        if group.size < 2:
            continue
        scores = out[rows]
        current = percentiles(scores)[treated[rows]]
        target = current + lam * (q - float(current.mean()))
        target = np.clip(target, 0.0, 1.0)
        grid = np.sort(scores)
        positions = target * (len(grid) - 1)
        low = np.floor(positions).astype(int)
        high = np.minimum(low + 1, len(grid) - 1)
        weight = positions - low
        out[group] = grid[low] * (1.0 - weight) + grid[high] * weight
    return out


def key(name: str, lam: float) -> str:
    return f"W10_{name}_lam{lam:.2f}"


def freeze() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    if (OUT / "protocol.json").exists():
        raise SystemExit("Wave-10 protocol already frozen")
    sources = [Path(__file__), ROOT / "evaluate.py", ROOT / "run.py", ROOT / "src/scoring.py",
               ROOT / "experiments/revalidate_fold_local.py", FEATURE_FILE, ROOT / "data" / "raw" / "训练集.csv",
               ROOT / "experiments/limit_up_decomposition_eval/decomposition.json",
               ROOT / "experiments/limit_up_rule_eval/results.json",
               ROOT / "experiments/limit_up_channel_eval/headroom.json"]
    for year in YEARS:
        for name in REPORTED:
            folder = R5 if name == "xgb_two_mean" else R4
            sources.append(folder / f"predictions_{name}_{year}.parquet")
        sources.append(R4 / f"result_{year}.json")
        sources.append(R5 / f"fold_{year}.json")
    payload = {**PROTOCOL, "frozen_at_local": time.strftime("%Y-%m-%dT%H:%M:%S"),
               "source_sha256": sha(Path(__file__)),
               "causal_q_per_fold": {str(year): estimate_q(year) for year in YEARS},
               "input_sha256": {p.relative_to(ROOT).as_posix(): sha(p)
                                for p in dict.fromkeys(sources)}}
    write_new(OUT / "protocol.json", payload)
    log("Froze the wave-10 protocol; causal q per fold: "
        + " ".join(f"{y}={v['q']:.6f}" for y, v in payload["causal_q_per_fold"].items()))


def verify_protocol() -> dict:
    protocol = read(OUT / "protocol.json")
    if protocol["source_sha256"] != sha(Path(__file__)):
        raise SystemExit("wave10_limitup_calibration.py changed after its protocol was frozen")
    if tuple(protocol["lambdas"]) != LAMBDAS or protocol["gates"] != GATES:
        raise SystemExit("Lambdas or gates drifted from the frozen protocol")
    for path, digest in protocol["input_sha256"].items():
        if sha(ROOT / path) != digest:
            raise SystemExit(f"Pinned input changed: {path}")
    return protocol


def score_year(year: int, protocol: dict, lambdas) -> dict:
    path = OUT / f"fold_{year}.json"
    if path.exists():
        record = read(path)
        if [float(x) for x in record["lambdas"]] != [float(x) for x in lambdas]:
            raise SystemExit(f"{year}: recorded fold used a different lambda set")
        log(f"{year} preserved completed fold")
        return record
    started = time.monotonic()
    q_info = protocol["causal_q_per_fold"][str(year)]
    frame = reference_frame(PRIMARY, year)
    dates = frame["trade_date"].to_numpy()
    treated = frame["flag_limit_up"].to_numpy().astype(bool)
    base_prediction = frame["pred"].to_numpy().astype(np.float64)
    expected = reference_metrics(PRIMARY, year)
    anchor_metrics, anchor_daily = score_official(frame, base_prediction)
    anchor = max(abs(anchor_metrics[name] - expected[name]) for name in expected)
    if anchor > 1e-12:
        raise AssertionError(f"{year}: the frozen {PRIMARY} prediction does not reproduce its "
                             f"recorded composite (max diff {anchor:.3e})")
    log(f"{year} anchor reproduced {expected['final_score']:.15f} exactly; causal q="
        f"{q_info['q']:.6f} from {q_info['training_limit_up_rows']:,} training limit-up rows; "
        f"limit-up rows in fold {int(treated.sum()):,} ({treated.mean():.4%})")
    record = {"year": year, "lambdas": [float(x) for x in lambdas], "primary": PRIMARY,
              "seconds": None, "q": q_info,
              "anchor_max_abs_diff": anchor,
              "reference_metrics": {name: reference_metrics(name, year) for name in REPORTED},
              "rules": {}}
    for lam in lambdas:
        name = key(PRIMARY, lam)
        prediction = recenter(base_prediction, dates, treated, q_info["q"], lam)
        if lam == 0.0 and not np.array_equal(prediction, base_prediction):
            raise AssertionError(f"{year}: lambda 0 is not the identity")
        untouched = np.flatnonzero(~treated)
        if not np.array_equal(prediction[untouched], base_prediction[untouched]):
            raise AssertionError(f"{year} {name}: non-limit-up scores were modified")
        metrics, daily = score_official(frame, prediction)
        daily.write_csv(OUT / f"daily_{name}_{year}.csv")
        excess_delta = metrics["annual_excess"] - expected["annual_excess"]
        turnover_delta = metrics["mean_turnover"] - expected["mean_turnover"]
        if abs(excess_delta) > 0.0 or abs(turnover_delta) > 0.0:
            raise AssertionError(f"{year} {name}: portfolio terms moved (excess {excess_delta:.3e}, "
                                 f"turnover {turnover_delta:.3e}); neutrality is a hard requirement")
        record["rules"][name] = {
            "lambda": float(lam), "metrics": {k: float(v) for k, v in metrics.items()},
            "score_delta_vs_primary": metrics["final_score"] - expected["final_score"],
            "ic_delta": metrics["ic_mean"] - expected["ic_mean"],
            "excess_delta": excess_delta, "turnover_delta": turnover_delta,
            "portfolio_terms_bit_identical": True,
            "deltas_vs_others": {other: metrics["final_score"]
                                 - record["reference_metrics"][other]["final_score"]
                                 for other in REPORTED if other != PRIMARY}}
        log(f"{year} {name}: score={metrics['final_score']:.9f} "
            f"({record['rules'][name]['score_delta_vs_primary']:+.9f}) "
            f"ic Δ={record['rules'][name]['ic_delta']:+.6f} excess Δ=0 turnover Δ=0")
    record["seconds"] = round(time.monotonic() - started, 2)
    write_new(path, record)
    return record


def gate(records: list[dict], name: str, stage: str) -> dict:
    thresholds = GATES[stage]
    deltas = [record["rules"][name]["score_delta_vs_primary"] for record in records]
    ics = [record["rules"][name]["ic_delta"] for record in records]
    result = {"score_deltas": dict(zip([str(r["year"]) for r in records], deltas)),
              "mean_score_delta": float(np.mean(deltas)),
              "worst_year_score_delta": float(min(deltas)),
              "mean_ic_delta": float(np.mean(ics))}
    if stage == "development":
        result["passed"] = bool(result["mean_score_delta"] >= thresholds["mean_score_delta_min"]
                                and result["worst_year_score_delta"]
                                >= thresholds["worst_year_score_delta_min"]
                                and result["mean_ic_delta"] >= thresholds["mean_ic_delta_min"])
    else:
        result["passed"] = bool(result["mean_score_delta"] >= thresholds["mean_score_delta_min"]
                                and all(d > 0 for d in deltas))
    return result


def develop() -> None:
    protocol = verify_protocol()
    if (OUT / "development.json").exists():
        raise SystemExit("Development choice already recorded; preserving it")
    lambdas = (0.0, *LAMBDAS)
    records = [score_year(year, protocol, lambdas) for year in DEVELOPMENT]
    results = {}
    for lam in LAMBDAS:
        name = key(PRIMARY, lam)
        results[name] = {**gate(records, name, "development"), "lambda": float(lam)}
    eligible = [name for name, item in results.items() if item["passed"]]
    winner = (min(eligible, key=lambda n: (-results[n]["mean_score_delta"], results[n]["lambda"]))
              if eligible else None)
    write_new(OUT / "development.json", {
        "protocol_sha256": sha(OUT / "protocol.json"), "primary": PRIMARY,
        "selected_before_confirmation": True, "no_fallback_after_confirmation": True,
        "results": results, "eligible": eligible, "winner": winner,
        "anchors": {str(r["year"]): r["anchor_max_abs_diff"] for r in records},
        "causal_q": {str(r["year"]): r["q"] for r in records},
        "fold_sha256": {f"fold_{y}.json": sha(OUT / f"fold_{y}.json") for y in DEVELOPMENT}})
    log(f"DEVELOPMENT winner: {winner!r} (eligible: {eligible})")


def validated_development() -> dict:
    development = read(OUT / "development.json")
    if development["protocol_sha256"] != sha(OUT / "protocol.json"):
        raise SystemExit("Development record does not match the frozen protocol")
    records = []
    for year in DEVELOPMENT:
        path = OUT / f"fold_{year}.json"
        if sha(path) != development["fold_sha256"][path.name]:
            raise SystemExit(f"{year}: recorded fold changed after the development choice")
        records.append(read(path))
    results = {}
    for lam in LAMBDAS:
        name = key(PRIMARY, lam)
        results[name] = {**gate(records, name, "development"), "lambda": float(lam)}
    if results != development["results"]:
        raise SystemExit("Development gates do not reproduce from the recorded folds")
    return development


def confirm() -> None:
    protocol = verify_protocol()
    development = validated_development()
    winner = development["winner"]
    if winner is None:
        raise SystemExit("No lambda passed the development gate; confirmation is prohibited")
    if (OUT / "confirmation.json").exists():
        raise SystemExit("Confirmation already recorded; preserving it")
    lam = next(l for l in LAMBDAS if key(PRIMARY, l) == winner)
    records = [score_year(year, protocol, (0.0, lam)) for year in CONFIRMATION]
    result = gate(records, winner, "confirmation")
    write_new(OUT / "confirmation.json", {
        "protocol_sha256": sha(OUT / "protocol.json"), "winner": winner, "lambda": lam,
        "confirmation_years": list(CONFIRMATION), "result": result, "passed": result["passed"],
        "portfolio_terms_bit_identical_every_year": all(
            r["rules"][winner]["portfolio_terms_bit_identical"] for r in records),
        "five_year_deltas_vs_primary": {
            **development["results"][winner]["score_deltas"], **result["score_deltas"]},
        "note": "Scored once, after the development choice was recorded. Exploratory: all five "
                "years have been viewed repeatedly.",
        "fold_sha256": {f"fold_{y}.json": sha(OUT / f"fold_{y}.json") for y in CONFIRMATION}})
    log(f"CONFIRMATION {winner}: mean {result['mean_score_delta']:+.9f}, "
        f"deltas {result['score_deltas']} → {'PASSED' if result['passed'] else 'FAILED'}")


def summarize() -> None:
    protocol = read(OUT / "protocol.json")
    table = {"protocol_sha256": sha(OUT / "protocol.json"), "primary": PRIMARY,
             "causal_q": protocol["causal_q_per_fold"], "measured_ceiling": PROTOCOL["measured_ceiling"],
             "years": {}, "lambdas": {}}
    for year in YEARS:
        path = OUT / f"fold_{year}.json"
        if not path.exists():
            continue
        record = read(path)
        table["years"][str(year)] = {
            "references": {name: record["reference_metrics"][name]["final_score"]
                           for name in record["reference_metrics"]},
            "rules": {name: {"final_score": item["metrics"]["final_score"],
                             "score_delta_vs_primary": item["score_delta_vs_primary"],
                             "ic_delta": item["ic_delta"],
                             "deltas_vs_others": item["deltas_vs_others"]}
                      for name, item in record["rules"].items()}}
    for stage in ("development", "confirmation"):
        path = OUT / f"{stage}.json"
        if path.exists():
            table[stage] = read(path)
    for lam in (0.0, *LAMBDAS):
        name = key(PRIMARY, lam)
        deltas = {year: table["years"][year]["rules"][name]["score_delta_vs_primary"]
                  for year in table["years"] if name in table["years"][year]["rules"]}
        if deltas:
            table["lambdas"][f"{lam:.2f}"] = {
                "deltas": deltas, "years_scored": len(deltas),
                "mean_delta": float(np.mean(list(deltas.values()))),
                "worst_year": float(min(deltas.values())),
                "positive_years": int(sum(v > 0 for v in deltas.values()))}
    (OUT / "summary.json").write_text(json.dumps(table, ensure_ascii=False, indent=2),
                                      encoding="utf-8")
    print(f"\n涨停股因果重校准，主参照 = {PRIMARY}（当前交付主干）")
    print(f"{'lambda':<9}" + "".join(f"{y:>13}" for y in sorted(table['years'], key=int))
          + f"{'均值':>13}{'最差年':>13}{'正年':>7}")
    for lam, item in table["lambdas"].items():
        cells = "".join(f"{item['deltas'].get(str(y), float('nan')):>+13.6f}"
                        if str(y) in item["deltas"] else f"{'-':>13}"
                        for y in sorted(table["years"], key=int))
        print(f"{lam:<9}{cells}{item['mean_delta']:>+13.6f}{item['worst_year']:>+13.6f}"
              f"{item['positive_years']:>5}/{item['years_scored']}")
    print(f"\n各折因果 q（只用训练期涨停行估计）："
          + " ".join(f"{y}={v['q']:.4f}" for y, v in table["causal_q"].items()))
    ceiling = table["measured_ceiling"]
    print(f"上限参照：组内排序 oracle {ceiling['within_group_oracle']:+.6f}，位置 oracle "
          f"{ceiling['placement_oracle']:+.6f}，合计 {ceiling['full_oracle']:+.6f}；"
          f"反向的『整体抬到最顶』只有 {ceiling['blanket_lift_to_top']:+.6f}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("stage", choices=("protocol", "develop", "confirm", "summary"))
    arguments = parser.parse_args()
    {"protocol": freeze, "develop": develop, "confirm": confirm, "summary": summarize}[
        arguments.stage]()
