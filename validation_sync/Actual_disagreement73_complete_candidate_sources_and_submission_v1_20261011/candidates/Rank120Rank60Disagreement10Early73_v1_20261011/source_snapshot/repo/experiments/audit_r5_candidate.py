"""Independent r5 confirmation and unified-account audit for one locked winner.

The default CLI command runs synthetic tests only. Historical candidate scores
are not read until an explicit audit/execution command receives a development-
only winner record. The public bootstrap API accepts already-scored daily frames.
"""
from __future__ import annotations

import os

for _name in ("POLARS_MAX_THREADS", "OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_name] = "4"

import argparse
import hashlib
import json
import math
from pathlib import Path
import re
import tempfile
from typing import Mapping

import numpy as np
import pandas as pd
import polars as pl
from scipy.stats import spearmanr


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "experiments/optimization_r5_20260926"
REFERENCES = ROOT / "experiments/revalidation_20260926/validation"
CONFIRM_YEARS = (2023, 2024)
DAILY_COLUMNS = ("rank_ic", "excess", "turnover")
KEYS = ["ts_code", "trade_date"]
REFERENCES_BY_NAME = {"pooled": "baseline", "r4": "ensemble4"}


def sha(path: Path) -> str:
    with path.open("rb") as handle:
        return hashlib.file_digest(handle, "sha256").hexdigest()


def write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x", encoding="utf-8") as handle:
        json.dump(data, handle, ensure_ascii=False, indent=2, allow_nan=False)


def _normalise_years(frames: Mapping[int | str, pl.DataFrame]) -> dict[int, pl.DataFrame]:
    result = {int(year): frame for year, frame in frames.items()}
    if len(result) != len(frames) or not result:
        raise ValueError("Year keys must be unique and nonempty")
    return dict(sorted(result.items()))


def _paired_arrays(candidate: pl.DataFrame, reference: pl.DataFrame, year: int) -> np.ndarray:
    required = ["trade_date", *DAILY_COLUMNS]
    a, b = candidate.select(required), reference.select(required)
    if len(a) < 2 or not a["trade_date"].equals(b["trade_date"]):
        raise ValueError(f"Candidate/reference dates differ in {year}")
    dates = a["trade_date"].to_numpy()
    if np.any(np.diff(dates) <= 0) or not np.all(dates // 10000 == year):
        raise ValueError(f"Dates must be unique, increasing and within year {year}")
    av = a.select(DAILY_COLUMNS).cast(pl.Float64).to_numpy()
    bv = b.select(DAILY_COLUMNS).cast(pl.Float64).to_numpy()
    if not np.array_equal(np.isfinite(av), np.isfinite(bv)):
        raise ValueError(f"Candidate/reference metric validity masks differ in {year}")
    if not np.all(np.isfinite(av[:, :2])) or not np.isfinite(av[:, 2]).any():
        raise ValueError(f"Missing IC/excess or no valid turnover in {year}")
    return av - bv


def _score_delta(values: np.ndarray, axis: int = 0) -> np.ndarray | float:
    means = np.nanmean(values, axis=axis)
    return .4 * means[..., 0] + .3 * 252 * means[..., 1] - .3 * means[..., 2]


def _hac_mean(values: np.ndarray, lag: int) -> dict:
    n = len(values)
    mean = float(values.mean())
    centered = values - mean
    lags = min(lag, n - 1)
    long_run = float(np.dot(centered, centered) / n)
    for k in range(1, lags + 1):
        long_run += 2 * (1 - k / (lags + 1)) * float(np.dot(centered[k:], centered[:-k]) / n)
    variance = max(long_run, 0.0) / n
    se = math.sqrt(variance)
    return {"n": n, "lag": lags, "mean": mean, "variance_of_mean": variance,
            "standard_error": se, "t": mean / se if se > 1e-15 else None,
            "normal_ci95": [mean - 1.96 * se, mean + 1.96 * se]}


def paired_block_bootstrap(
    candidate_daily: Mapping[int | str, pl.DataFrame],
    reference_daily: Mapping[int | str, pl.DataFrame],
    *, block_days: int = 20, draws: int = 20000, seed: int = 2026,
) -> dict:
    """Equal-year official-score delta uncertainty from paired daily evidence.

    Each frame has trade_date, rank_ic, excess and turnover (the first turnover
    can be null/NaN). Inputs must already be aligned with the official CSV
    scoring convention. Resample circular contiguous blocks WITHIN each year,
    preserving the pair and each component's finite-value denominator. Average
    the annual score deltas equally, never join artificial cross-year Top sets.
    """
    candidate, reference = _normalise_years(candidate_daily), _normalise_years(reference_daily)
    if candidate.keys() != reference.keys():
        raise ValueError("Candidate/reference year sets differ")
    if block_days < 1 or draws < 1:
        raise ValueError("Positive block length and draw count are required")
    differences = {year: _paired_arrays(candidate[year], reference[year], year) for year in candidate}
    annual = {str(year): float(_score_delta(value)) for year, value in differences.items()}
    observed = float(np.mean(list(annual.values())))
    rng = np.random.default_rng(seed)
    replicates = np.empty(draws, dtype=np.float64)
    for start in range(0, draws, 256):
        batch = min(256, draws - start)
        pooled = np.zeros(batch, dtype=np.float64)
        for values in differences.values():
            n = len(values)
            width = min(block_days, n)
            blocks = math.ceil(n / width)
            offsets = rng.integers(0, n, size=(batch, blocks))
            indices = ((offsets[..., None] + np.arange(width)) % n).reshape(batch, -1)[:, :n]
            sampled = values[indices]
            if np.any(np.sum(np.isfinite(sampled[:, :, 2]), axis=1) == 0):
                raise ValueError("Bootstrap sample contains no finite turnover; use realistic daily evidence")
            pooled += _score_delta(sampled, axis=1) / len(differences)
        replicates[start:start + batch] = pooled
    if not np.isfinite(replicates).all():
        raise AssertionError("Nonfinite paired bootstrap score delta")
    share = float(np.mean(replicates > 0))
    hac = {}
    for lag in (5, 10, 20):
        by_year = {}
        for year, values in differences.items():
            # Finite-count scaling makes the daily contribution mean reproduce
            # each year's separately-denominated official delta EXACTLY.
            n = len(values)
            scaled = np.where(np.isfinite(values), values, 0.0) * (n / np.isfinite(values).sum(axis=0))
            contribution = .4 * scaled[:, 0] + 75.6 * scaled[:, 1] - .3 * scaled[:, 2]
            if abs(float(contribution.mean()) - annual[str(year)]) > 1e-12:
                raise AssertionError("HAC contributions do not reproduce annual score delta")
            by_year[str(year)] = _hac_mean(contribution, lag)
        se = math.sqrt(sum(v["variance_of_mean"] for v in by_year.values())) / len(by_year)
        hac[str(lag)] = {"annual": by_year, "equal_year_mean_delta": observed,
                        "standard_error_assuming_independent_year_blocks": se,
                        "t": observed / se if se > 1e-15 else None,
                        "normal_ci95": [observed - 1.96 * se, observed + 1.96 * se]}
    return {
        "years": list(differences), "annual_score_deltas": annual,
        "observed_mean_annual_score_delta": observed,
        "block_days": block_days, "draws": draws, "seed": seed,
        "bootstrap_ci95": np.quantile(replicates, [.025, .975]).tolist(),
        "bootstrap_standard_error": float(replicates.std(ddof=1)) if draws > 1 else 0.0,
        "bootstrap_share_positive": share, "passes_positive_share_80pct": share >= .8,
        "hac": hac,
        "resampling": "Within-year paired circular contiguous blocks; annual score means equally weighted; no cross-year transitions; finite turnover denominator retained.",
        "selection_bias_corrected": False,
        "limitation": "All historical years already viewed. Inter-year resampling independence and HAC aggregation are descriptive assumptions; shared training and historical model selection are not corrected. Positive draw share is a predeclared engineering gate, not a posterior probability of alpha.",
    }


def _daily_from_csv(folder: Path) -> tuple[dict, pl.DataFrame, dict]:
    """Independent transcription of evaluate.py, using the exact written bytes."""
    pred = pd.read_csv(folder / "submission.csv")
    labels = pd.read_csv(folder / "测试集_Y.csv")
    flags = pd.read_csv(folder / "测试集_X.csv", usecols=KEYS + ["flag_limit_up"])
    frame = pred.merge(labels, on=KEYS, how="inner").merge(flags, on=KEYS, how="inner")
    records, return_sets, turnover_sets = [], [], []
    previous = None
    for date, group in frame.groupby("trade_date", sort=True):
        row = {"trade_date": int(date), "rank_ic": np.nan, "excess": np.nan,
               "top1_return": np.nan, "turnover": np.nan}
        labeled = group.dropna(subset=["y_ret_1d"])
        if len(labeled) >= 30:
            row["rank_ic"] = float(spearmanr(labeled["pred"], labeled["y_ret_1d"]).statistic)
        eligible = group[(group["flag_limit_up"] == 0) & group["y_ret_1d"].notna()].copy()
        if len(eligible) >= 100:
            eligible = eligible.sort_values("pred", ascending=False).reset_index(drop=True)
            selected = eligible.iloc[:max(len(eligible) // 10, 1)]
            row["top1_return"] = float(selected["y_ret_1d"].mean())
            row["excess"] = float(selected["y_ret_1d"].mean() - eligible["y_ret_1d"].mean())
            return_sets.append([int(date), sorted(map(str, selected["ts_code"]))])
        eligible = group[group["flag_limit_up"] == 0].copy()
        if len(eligible) < 100:
            previous = None
        else:
            eligible = eligible.sort_values("pred", ascending=False)
            selected = set(eligible["ts_code"].iloc[:max(len(eligible) // 10, 1)])
            turnover_sets.append([int(date), sorted(map(str, selected))])
            if previous is not None and previous:
                row["turnover"] = 1 - len(selected & previous) / len(selected | previous)
            previous = selected
        records.append(row)
    daily = pl.DataFrame(records)
    ic = daily["rank_ic"].to_numpy()
    excess = daily["excess"].to_numpy()
    top = daily["top1_return"].to_numpy()
    turnover = daily["turnover"].to_numpy()
    mean, sd = float(np.mean(ic)), float(np.std(ic, ddof=1))
    metrics = {"ic_mean": mean, "ic_std": sd, "icir": mean / sd if sd > 0 else 0.0,
               "ic_positive_ratio": float(np.mean(ic > 0)),
               "annual_excess": float(np.nanmean(excess) * 252),
               "top1_annual_ret": float(np.nanmean(top) * 252),
               "mean_turnover": float(np.nanmean(turnover))}
    metrics["final_score"] = .4 * mean + .3 * metrics["annual_excess"] + .3 * (1 - metrics["mean_turnover"])
    digest = lambda sets: hashlib.sha256(json.dumps(sets, separators=(",", ":")).encode()).hexdigest()
    return metrics, daily, {"return_top_sets_sha256": digest(return_sets),
                            "turnover_top_sets_sha256": digest(turnover_sets),
                            "ic_days": int(np.isfinite(ic).sum()),
                            "excess_days": int(np.isfinite(excess).sum()),
                            "turnover_pairs": int(np.isfinite(turnover).sum()),
                            "return_top_and_turnover_top_are_distinct_definitions": True}


def independent_official_score(prediction_path: Path, year: int) -> tuple[dict, pl.DataFrame, dict]:
    """Read a fixed prediction; score raw Float64 labels through original CSV evaluator."""
    from evaluate import evaluate
    if year not in CONFIRM_YEARS:
        raise ValueError("This independent confirmation auditor only scores 2023/2024")
    prediction = pl.read_parquet(prediction_path, columns=KEYS + ["pred"]).sort("trade_date", "ts_code")
    raw = (pl.scan_csv(ROOT / "data" / "raw" / "训练集.csv", schema_overrides={"ts_code": pl.String,
                "trade_date": pl.Int32, "y_ret_1d": pl.Float64}, null_values=["NaN", "nan", ""])
           .filter(pl.col("trade_date").is_between(year * 10000 + 101, year * 10000 + 1231))
           .select(KEYS + ["y_ret_1d", "flag_limit_up"]).sort("trade_date", "ts_code").collect())
    if (prediction.select(pl.struct(KEYS).n_unique()).item() != len(prediction)
            or not prediction.select(KEYS).equals(raw.select(KEYS))
            or not prediction["pred"].is_finite().all()):
        raise ValueError("Prediction keys, row coverage, year or finite-score contract failed")
    with tempfile.TemporaryDirectory(prefix="r5-independent-official-") as temporary:
        folder = Path(temporary)
        prediction.write_csv(folder / "submission.csv", float_precision=17)
        raw.select(KEYS + ["y_ret_1d"]).write_csv(folder / "测试集_Y.csv", float_precision=17)
        raw.select(KEYS + ["flag_limit_up"]).write_csv(folder / "测试集_X.csv")
        official = {key: float(value) for key, value in evaluate(str(folder / "submission.csv"), str(folder)).items()}
        rebuilt, daily, details = _daily_from_csv(folder)
        differences = {key: rebuilt[key] - value for key, value in official.items()}
        if not all(np.isfinite(value) and abs(value) <= 1e-12 for value in differences.values()):
            raise AssertionError(f"Independent daily/official mismatch: {differences}")
        details.update({"official_vs_independent_daily_difference": differences,
                        "prediction_parquet_sha256": sha(prediction_path),
                        "scored_csv_sha256": sha(folder / "submission.csv"),
                        "raw_float64_label_csv_sha256": sha(folder / "测试集_Y.csv"),
                        "flags_csv_sha256": sha(folder / "测试集_X.csv")})
    return official, daily, details


def _load_winner(path: Path) -> tuple[dict, dict[int, Path]]:
    """CLI schema is deliberately explicit so no failed/dev-only candidate is scored."""
    record = json.loads(path.read_text(encoding="utf-8"))
    if (record.get("status") != "selected" or record.get("development_gate_passed") is not True
            or record.get("selection_uses_confirmation") is not False
            or record.get("selection_years") != [2020, 2021, 2022]
            or record.get("confirmation_years") != [2023, 2024]):
        raise ValueError("A passed development-only, single-winner selection record is required")
    if not re.fullmatch(r"[A-Za-z0-9_.-]+", record["candidate_key"]):
        raise ValueError("Unsafe candidate key")
    protocol_path = ROOT / record["protocol_path"]
    if not protocol_path.resolve().is_relative_to(OUT.resolve()) or sha(protocol_path) != record["protocol_sha256"]:
        raise ValueError("Winner's frozen r5 master protocol does not match")
    predictions = {int(year): ROOT / relative for year, relative in record["prediction_paths"].items()}
    if set(predictions) != set(CONFIRM_YEARS):
        raise ValueError("Exactly two confirmation prediction files are required")
    if any(not value.resolve().is_relative_to(OUT.resolve()) for value in predictions.values()):
        raise ValueError("Winner predictions must remain in the isolated r5 directory")
    return record, predictions


def audit_winner_scores(winner_path: Path) -> dict:
    record, predictions = _load_winner(winner_path)
    output = OUT / "independent_audit" / record["candidate_key"]
    if (output / "score_audit.json").exists():
        raise FileExistsError("Preserve the winner's once-only independent confirmation")
    output.mkdir(parents=True, exist_ok=True)
    paths = {"winner": predictions}
    for name, variant in REFERENCES_BY_NAME.items():
        paths[name] = {year: REFERENCES / f"predictions_{variant}_{year}.parquet" for year in CONFIRM_YEARS}
    all_metrics, all_daily, checks = {}, {}, {}
    for name, by_year in paths.items():
        all_metrics[name], all_daily[name], checks[name] = {}, {}, {}
        for year, path in by_year.items():
            metric, daily, details = independent_official_score(path, year)
            all_metrics[name][str(year)], all_daily[name][year], checks[name][str(year)] = metric, daily, details
            destination = output / f"official_{name}_{year}_daily.csv"
            if destination.exists():
                raise FileExistsError(f"Preserve partial audit evidence: {destination}")
            daily.write_csv(destination, float_precision=17)
    gates, uncertainty = {}, {}
    for name in REFERENCES_BY_NAME:
        differences = [all_metrics["winner"][str(year)]["final_score"] - all_metrics[name][str(year)]["final_score"] for year in CONFIRM_YEARS]
        ic_difference = float(np.mean([all_metrics["winner"][str(year)]["ic_mean"] - all_metrics[name][str(year)]["ic_mean"] for year in CONFIRM_YEARS]))
        uncertainty[name] = paired_block_bootstrap(all_daily["winner"], all_daily[name])
        gates[name] = {"annual_score_differences": differences,
                       "mean_score_difference": float(np.mean(differences)),
                       "mean_ic_difference": ic_difference,
                       "mean_score_at_least_0p0005": float(np.mean(differences)) >= .0005,
                       "worst_annual_difference_at_least_minus_0p003": min(differences) >= -.003,
                       "mean_ic_difference_at_least_minus_0p002": ic_difference >= -.002,
                       "bootstrap_positive_share_at_least_80pct": uncertainty[name]["passes_positive_share_80pct"]}
        gates[name]["passed"] = all(value for key, value in gates[name].items() if key.endswith("0p0005") or key.endswith("minus_0p003") or key.endswith("minus_0p002") or key.endswith("80pct"))
    expected = record.get("expected_confirmation_metrics")
    if expected is not None:
        for year in map(str, CONFIRM_YEARS):
            for key, value in expected[year].items():
                if abs(all_metrics["winner"][year][key] - value) > 1e-12:
                    raise AssertionError(f"Runner/independent metric differs: {year}/{key}")
    result = {"status": "passed", "candidate_key": record["candidate_key"],
              "winner_record_sha256": sha(winner_path), "master_protocol_sha256": record["protocol_sha256"],
              "audit_source_sha256": sha(Path(__file__)), "evaluate_source_sha256": sha(ROOT / "evaluate.py"),
              "historical_metrics": all_metrics, "independent_scoring_checks": checks,
              "confirmation_gates": gates, "confirmation_passed": all(value["passed"] for value in gates.values()),
              "paired_uncertainty": uncertainty,
              "runner_expected_metrics_checked": expected is not None,
              "failed_confirmation_does_not_authorize_another_candidate": True,
              "selection_bias_corrected": False}
    write_json(output / "score_audit.json", result)
    return result


def audit_winner_execution(winner_path: Path) -> dict:
    """Fresh 2023 cash accounts; the same frozen r4 account engine for all parties."""
    from experiments import backtest_causal_portfolio as account
    record, predictions = _load_winner(winner_path)
    output = OUT / "independent_audit" / record["candidate_key"] / "execution"
    if (output / "summary.json").exists():
        raise FileExistsError("Preserve fixed-winner execution evidence")
    output.mkdir(parents=True, exist_ok=True)
    bars = (pl.scan_csv(ROOT / "data" / "raw" / "训练集.csv", schema_overrides={"ts_code": pl.String, "trade_date": pl.Int32},
                null_values=["NaN", "nan", ""]).filter(pl.col("trade_date").is_between(20230101, 20241231))
            .select(account.BAR_COLUMNS).collect())
    files = {"winner": predictions}
    for name, variant in REFERENCES_BY_NAME.items():
        files[name] = {year: REFERENCES / f"predictions_{variant}_{year}.parquet" for year in CONFIRM_YEARS}
    frames = {name: pl.concat([pl.read_parquet(path, columns=KEYS + ["pred"]) for path in by_year.values()])
              for name, by_year in files.items()}
    market = account.market_from_frames(bars, frames)
    if len(market.dates) != 484 or len(market.codes) != 4650:
        raise AssertionError("Confirmation account must use the complete 2023-2024 calendar")
    scenarios, reconciliations = {}, {}
    for cost in account.COSTS:
        key = f"{cost:.4f}"
        daily, reconciliations[key] = {}, {}
        for name in ("winner", "pooled", "r4", "market"):
            frame, final = account.simulate(market, name, cost)
            prefix, _ = account.simulate(market.prefix(60), name, cost)
            if not frame.head(60).equals(prefix):
                raise AssertionError("Confirmation account changes with future append")
            final.pop("final_positions")
            reconciliations[key][name] = final
            frame.write_csv(output / f"daily_{name}_rt{key}.csv", float_precision=17)
            daily[name] = frame
        scenarios[key] = {name: {"whole_period": account.stats(frame, daily["market"]),
                                "by_year": {str(year): account.stats(frame.filter(pl.col("trade_date") // 10000 == year),
                                    daily["market"].filter(pl.col("trade_date") // 10000 == year))
                                    for year in CONFIRM_YEARS}}
                           for name, frame in daily.items()}
    central, gates = scenarios["0.0030"], {}
    for name in REFERENCES_BY_NAME:
        winner, baseline = central["winner"]["whole_period"], central[name]["whole_period"]
        net = winner["net_compound_return"] - baseline["net_compound_return"]
        drawdown = winner["net_max_drawdown"] - baseline["net_max_drawdown"]
        gates[name] = {"net_return_difference": net, "max_drawdown_difference": drawdown,
                       "net_return_difference_at_least_minus_0p01": net >= -.01,
                       "drawdown_difference_at_least_minus_0p02": drawdown >= -.02,
                       "passed": net >= -.01 and drawdown >= -.02}
    result = {"status": "passed", "candidate_key": record["candidate_key"],
              "winner_record_sha256": sha(winner_path), "master_protocol_sha256": record["protocol_sha256"],
              "audit_source_sha256": sha(Path(__file__)), "frozen_account_source_sha256": sha(Path(account.__file__)),
              "reference_account_protocol_sha256": sha(account.OUT / "protocol.json"),
              "execution_period": [20230103, 20241231], "days": 484, "initial_cash": 1.0,
              "accounts_cold_start_2023_and_carry_through_2024": True,
              "execution_gate": gates, "execution_passed": all(value["passed"] for value in gates.values()),
              "central_round_trip_cost": .003, "other_costs_sensitivity_only": True,
              "all_cost_scenarios": scenarios, "account_reconciliation": reconciliations,
              "prefix_60_days_exact_all_accounts": True,
              "prediction_sha256": {name: {str(year): sha(path) for year, path in by_year.items()} for name, by_year in files.items()},
              "artifacts_sha256": {path.name: sha(path) for path in sorted(output.glob("*.csv"))},
              "limitations": "Signal selection is causal; daily execution-day flags and volume are retrospective fill-constraint proxies, not verified auction states. Fractional units, stale marks, no delisting or auction-capacity model. Hypothetical fees, not legal rates. Passing non-inferiority limits does not establish improved executable returns."}
    write_json(output / "summary.json", result)
    return result


def synthetic_tests() -> dict:
    """No model, historical prediction, label CSV, or candidate summary is read."""
    def fixture(year: int, n: int, score_delta: float) -> tuple[pl.DataFrame, pl.DataFrame]:
        t = np.arange(n)
        baseline = pl.DataFrame({"trade_date": year * 10000 + 101 + t,
                                 "rank_ic": .1 + .01 * np.sin(t),
                                 "excess": .001 + .003 * np.cos(t),
                                 "turnover": np.r_[np.nan, .03 + .002 * np.sin(t[1:])]})
        candidate = baseline.with_columns((pl.col("rank_ic") + score_delta / .4).alias("rank_ic"))
        return candidate, baseline
    a, b, c, d = *fixture(2023, 35, .001), *fixture(2024, 50, .003)
    result = paired_block_bootstrap({2023: a, 2024: c}, {2023: b, 2024: d}, draws=256)
    assert abs(result["observed_mean_annual_score_delta"] - .002) < 1e-12
    assert np.max(np.abs(np.array(result["bootstrap_ci95"]) - .002)) < 1e-12
    assert result["bootstrap_share_positive"] == 1.0
    assert result == paired_block_bootstrap({2023: a, 2024: c}, {2023: b, 2024: d}, draws=256)
    identity = paired_block_bootstrap({2023: a}, {2023: a}, draws=64)
    assert identity["observed_mean_annual_score_delta"] == 0 and identity["bootstrap_share_positive"] == 0
    negative = paired_block_bootstrap({2023: b}, {2023: a}, draws=64)
    assert negative["bootstrap_share_positive"] == 0
    shifted = b.with_columns((pl.col("trade_date") + 1).alias("trade_date"))
    try:
        paired_block_bootstrap({2023: a}, {2023: shifted}, draws=2)
    except ValueError:
        pass
    else:
        raise AssertionError("Mismatched dates were not rejected")
    # A constant turnover difference must use n-1 finite observations, not n.
    turnover_candidate = b.with_columns((pl.col("turnover") + .01).alias("turnover"))
    turnover = paired_block_bootstrap({2023: turnover_candidate}, {2023: b}, draws=64)
    assert abs(turnover["observed_mean_annual_score_delta"] + .003) < 1e-12
    for value in turnover["hac"].values():
        assert abs(value["equal_year_mean_delta"] + .003) < 1e-12
    from experiments import backtest_causal_portfolio as account
    account_tests = account.tests()
    return {"status": "passed", "historical_candidates_or_labels_read": False,
            "equal_year_weight_with_unequal_day_counts": True,
            "paired_circular_blocks_within_year_only": True,
            "fixed_seed_exact_reproducibility": True,
            "zero_delta_not_counted_as_positive": True,
            "negative_delta_rejected": True, "misaligned_dates_rejected": True,
            "separate_finite_turnover_denominator": True,
            "frozen_execution_engine_tests": account_tests}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("stage", choices=("test", "audit", "execution"), nargs="?", default="test")
    parser.add_argument("--winner", type=Path)
    parser.add_argument("--record", type=Path, help="Optional synthetic test record, confined to the r5 directory")
    args = parser.parse_args()
    if args.stage == "test":
        result = synthetic_tests()
        if args.record:
            if not args.record.resolve().is_relative_to(OUT.resolve()):
                raise ValueError("Test records must stay in the r5 experiment directory")
            write_json(args.record, result)
    else:
        if args.winner is None:
            parser.error("audit/execution requires --winner with an explicit passed development selection record")
        result = audit_winner_scores(args.winner) if args.stage == "audit" else audit_winner_execution(args.winner)
    print(json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False))
