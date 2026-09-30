"""Audit causal Top-internal reranking and the two official Top universes.

Run from the project root: python -m experiments.audit_top_internal
The return-Top diagnostics use ex-post label availability only for evaluation;
they are not available to the prediction transform or a live trading strategy.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import replace

import numpy as np
import polars as pl

from experiments.protected_top import load_panel
from src.research_stats import hac_stats
from run import ROOT
from src.scoring import Panel, postprocess_scores, score

OUT = ROOT / "experiments" / "top_internal_eval"


def predict(panel: Panel, raw: np.ndarray, alpha: float, bonus: float,
            weight: float) -> np.ndarray:
    return postprocess_scores(panel, raw, alpha, bonus, restore_lower=True,
                              top_current_weight=weight)


def top_set(panel: Panel, predictions: np.ndarray, day: int,
            *, require_label: bool = False) -> set[int]:
    eligible = panel.up[day] == 0
    if require_label:
        eligible &= np.isfinite(panel.y[day])
    indices = np.flatnonzero(eligible)
    if not len(indices):
        return set()
    order = np.argsort(-predictions[day, indices], kind="stable")
    return set(indices[order[:max(len(indices) // 10, 1)]].tolist())


def jaccard_distance(first: set[int], second: set[int]) -> float:
    union = first | second
    return 1.0 - len(first & second) / len(union) if union else 0.0


def assert_top_sets_equal(panel: Panel, first: np.ndarray,
                          second: np.ndarray) -> None:
    first = first.reshape(panel.y.shape)
    second = second.reshape(panel.y.shape)
    for day, date in enumerate(panel.dates):
        assert top_set(panel, first, day) == top_set(panel, second, day), (
            f"Official turnover Top identities changed on {date}"
        )


def universe_diagnostics(panel: Panel, predictions: np.ndarray,
                         previous: np.ndarray) -> dict:
    predictions = predictions.reshape(panel.y.shape)
    previous = previous.reshape(panel.y.shape)
    holding_counts, return_counts, cross_rule_distances = [], [], []
    same_day_baseline_distances, return_turnovers, previous_return_turnovers = [], [], []
    prior_return = prior_baseline_return = None
    for day in range(len(panel.dates)):
        holdings = top_set(panel, predictions, day)
        return_group = top_set(panel, predictions, day, require_label=True)
        baseline_group = top_set(panel, previous, day, require_label=True)
        holding_counts.append(len(holdings))
        return_counts.append(len(return_group))
        cross_rule_distances.append(jaccard_distance(holdings, return_group))
        same_day_baseline_distances.append(jaccard_distance(return_group, baseline_group))
        if prior_return is not None:
            return_turnovers.append(jaccard_distance(return_group, prior_return))
            previous_return_turnovers.append(jaccard_distance(baseline_group, prior_baseline_return))
        prior_return, prior_baseline_return = return_group, baseline_group
    return {
        "turnover_top_mean_size": float(np.mean(holding_counts)),
        "return_top_mean_size": float(np.mean(return_counts)),
        "same_day_return_vs_turnover_top_mean_jaccard_distance": float(np.mean(cross_rule_distances)),
        "same_day_return_top_vs_weight0_mean_jaccard_distance": float(np.mean(same_day_baseline_distances)),
        "return_top_ex_post_mean_adjacent_day_jaccard_distance": float(np.mean(return_turnovers)),
        "weight0_return_top_ex_post_mean_adjacent_day_jaccard_distance": float(np.mean(previous_return_turnovers)),
        "interpretation": "Return groups use ex-post y_ret_1d availability. Their Jaccard distances are descriptive only, not a causal tradeable portfolio backtest; the official turnover score uses its separate label-agnostic Top set.",
    }


def paired_intervals(candidate: pl.DataFrame, baseline: pl.DataFrame,
                     score_delta: float) -> dict:
    assert np.array_equal(candidate["trade_date"].to_numpy(), baseline["trade_date"].to_numpy())
    ic = candidate["rank_ic"].to_numpy() - baseline["rank_ic"].to_numpy()
    excess = candidate["excess"].to_numpy() - baseline["excess"].to_numpy()
    turnover = candidate["turnover"].to_numpy() - baseline["turnover"].to_numpy()
    composite = .4 * ic + .3 * 252 * excess - .3 * turnover
    # Each official component has its own denominator (turnover starts at t2).
    # Rescale component contributions so the full-day mean exactly equals the
    # difference between official aggregate scores, preserving the first day.
    exact = np.zeros(len(candidate), dtype=float)
    for delta, coefficient in ((ic, .4), (excess, .3 * 252), (turnover, -.3)):
        finite = np.isfinite(delta)
        exact[finite] += coefficient * delta[finite] * len(candidate) / finite.sum()
    assert np.isclose(exact.mean(), score_delta, atol=1e-12)
    return {
        "official_score_delta": score_delta,
        "paired_composite_hac_t2_onward": hac_stats(composite),
        "paired_composite_hac_exact_component_denominators": hac_stats(exact),
        "ic_delta_hac": hac_stats(ic),
        "annualized_excess_delta_hac": hac_stats(252 * excess),
        "turnover_delta_hac": hac_stats(turnover),
        "caveat": "Normal Newey-West intervals are descriptive, not adjusted for parameter selection. The t2-onward interval excludes the initial day; exact-component-denominator interval includes it with component-specific normalization.",
    }


def synthetic_panel(valid: np.ndarray, up: np.ndarray) -> Panel:
    days, count = valid.shape
    frame = pl.DataFrame({
        "ts_code": np.tile([f"S{i:03d}" for i in range(count)], days),
        "trade_date": np.repeat(np.arange(20000101, 20000101 + days), count),
        "y_ret_1d": np.zeros(days * count),
        "flag_limit_up": up.reshape(-1),
        "price_valid": valid.reshape(-1),
    })
    return Panel.from_frame(frame)


def synthetic_checks() -> dict:
    days, count = 5, 128
    rng = np.random.default_rng(918)
    valid = np.ones((days, count), dtype=bool)
    up = np.zeros((days, count), dtype=np.int8)
    ordinary = rng.normal(size=(days, count))
    tied = ordinary.copy()
    tied[0], tied[1] = np.arange(count), np.arange(count)[::-1]
    # With 128 ranks and alpha=1/2, the second day has exact stable ties.
    sparse = valid.copy()
    sparse[2] = False
    sparse[2, :5] = True
    reactivate = valid.copy()
    reactivate[1:3, :32] = False
    nonfinite = ordinary.copy()
    nonfinite[1, 7], nonfinite[2, 8] = np.nan, np.inf
    cases = {
        "exact_cutoff_ties": (valid, up, tied, .5, 0.),
        "no_valid_prices": (np.zeros_like(valid), up, ordinary, .9, .3),
        "no_non_limit_up_stocks": (valid, np.ones_like(up), ordinary, .9, .3),
        "fewer_valid_prices_than_top_size": (sparse, up, ordinary, .9, .3),
        "missing_prices_and_reactivation": (reactivate, up, ordinary, .9, .3),
        "nonfinite_raw_predictions": (valid, up, nonfinite, .9, .3),
    }
    results = {}
    for name, (price_valid, flags, raw, alpha, bonus) in cases.items():
        panel = synthetic_panel(price_valid, flags)
        baseline = predict(panel, raw, alpha, bonus, 0.)
        candidate = predict(panel, raw, alpha, bonus, 1.)
        assert np.isfinite(candidate).all(), name
        assert_top_sets_equal(panel, baseline, candidate)
        if name == "exact_cutoff_ties":
            assert np.array_equal(baseline.reshape(days, count)[1],
                                  candidate.reshape(days, count)[1]), name
        short = Panel.from_frame(panel.frame.head(3 * count))
        assert np.array_equal(candidate[:3 * count], predict(short, raw[:3], alpha, bonus, 1.)), name
        results[name] = {"finite": True, "turnover_top_identities_preserved": True,
                         "prefix_invariance": True}
        if name == "exact_cutoff_ties":
            results[name]["tied_boundary_keeps_original_order"] = True
    return results


def main(production: bool = False) -> None:
    if production:
        # The end-to-end pipeline must not require a manually generated
        # experiment/development.json file to validate its selected rule.
        selected = json.loads((ROOT / "validation/metrics.json").read_text(encoding="utf-8"))
        if not selected["selected_restore_lower"]:
            raise ValueError("Top internal audit requires protected rank restoration")
        alpha = float(selected["selected_alpha"])
        bonus = float(selected["selected_persistence_bonus"])
        weight = float(selected["selected_top_current_weight"])
        selection_years = selected["selection_years"]
    else:
        development = json.loads((OUT / "development.json").read_text(encoding="utf-8"))
        alpha = float(development["fixed_alpha"])
        bonus = float(development["fixed_bonus"])
        weight = float(development["selected_weight"])
        selection_years = development["selection_years"]
    output = {"config": {"alpha": alpha, "bonus": bonus, "top_current_weight": weight},
              "selection_years": selection_years,
              "config_source": "validation/metrics.json" if production else "development.json",
              "synthetic_checks": synthetic_checks(), "years": {}}
    rng = np.random.default_rng(90524)
    for year in (2022, 2023, 2024):
        panel = load_panel(year)
        raw = panel.frame["pred_raw"].to_numpy()
        candidate = predict(panel, raw, alpha, bonus, weight)
        previous = predict(panel, raw, alpha, bonus, 0.)
        assert np.isfinite(candidate).all()
        assert_top_sets_equal(panel, previous, candidate)
        metrics, daily = score(panel, candidate)
        previous_metrics, previous_daily = score(panel, previous)
        assert np.array_equal(daily["turnover"].to_numpy(), previous_daily["turnover"].to_numpy(), equal_nan=True)
        blank_frame = panel.frame.with_columns(pl.lit(None, dtype=pl.Float64).alias("y_ret_1d"))
        blank = Panel.from_frame(blank_frame)
        assert np.array_equal(candidate, predict(blank, raw, alpha, bonus, weight))
        random_y = rng.normal(size=panel.y.size)
        random_frame = panel.frame.with_columns(pl.Series("y_ret_1d", random_y))
        perturbed = Panel.from_frame(random_frame)
        assert np.array_equal(candidate, predict(perturbed, raw, alpha, bonus, weight))
        # Guard against transforms accessing the dataclass array instead of frame.
        array_only = replace(panel, y=rng.normal(size=panel.y.shape))
        assert np.array_equal(candidate, predict(array_only, raw, alpha, bonus, weight))
        prefix_rows = 50 * panel.rows_per_day
        prefix = Panel.from_frame(panel.frame.head(prefix_rows))
        assert np.array_equal(candidate[:prefix_rows], predict(prefix, raw[:prefix_rows], alpha, bonus, weight))
        original = postprocess_scores(panel, raw, .95, .15, restore_lower=False)
        original_metrics, original_daily = score(panel, original)
        output["years"][str(year)] = {
            "metrics": metrics, "weight0_metrics": previous_metrics,
            "original_metrics": original_metrics,
            "turnover_top_identities_unchanged_each_day": True,
            "daily_official_turnover_unchanged": True,
            "all_labels_removed_invariance": True,
            "all_labels_perturbed_invariance": True,
            "label_array_perturbed_invariance": True,
            "prefix_invariance_50_days": True,
            "relative_to_weight0": paired_intervals(daily, previous_daily, metrics["final_score"] - previous_metrics["final_score"]),
            "relative_to_original": paired_intervals(daily, original_daily, metrics["final_score"] - original_metrics["final_score"]),
            "top_universes": universe_diagnostics(panel, candidate, previous),
        }
        print(year, "audit passed", "score", metrics["final_score"],
              "delta", metrics["final_score"] - previous_metrics["final_score"],
              "paired CI", output["years"][str(year)]["relative_to_weight0"]["paired_composite_hac_exact_component_denominators"]["normal_95_ci"], flush=True)
    output["limitations"] = [
        "2022/2023 were used for sequential exploratory selection. Confidence intervals do not adjust for selection.",
        "2024 was inspected in previous project iterations and is historical diagnosis, not an untouched holdout.",
        "Return-Top identities and related Jaccard statistics depend on ex-post label availability; they are not real-time portfolio backtests.",
        "The official return and turnover metrics use different Top universes; low official turnover does not establish low turnover for the return-ranked subset.",
    ]
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "audit.json").write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--production", action="store_true", help="Read the pipeline's selected metrics, not a prior experiment file")
    main(parser.parse_args().production)
