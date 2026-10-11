"""Audit causality, Top invariance and paired uncertainty of the selected rule."""

from __future__ import annotations

import json

import numpy as np
import polars as pl

from experiments.protected_top import OUT, load_panel, make_candidate
from src.research_stats import hac_stats
from src.scoring import Panel, score


def main() -> None:
    config = json.loads((OUT / "development.json").read_text(encoding="utf-8"))["selected_config"]
    result = {"config": config, "years": {}}
    for year in (2022, 2023, 2024):
        panel = load_panel(year)
        raw = panel.frame["pred_raw"].to_numpy()
        predictions = make_candidate(panel, raw, config)
        stable = make_candidate(panel, raw, config | {"restore_lower": False})
        assert np.isfinite(predictions).all()
        # Check all daily tradable Top identities and ordering, not just average turnover.
        p = predictions.reshape(panel.y.shape)
        s = stable.reshape(panel.y.shape)
        for day in range(len(panel.dates)):
            indices = np.flatnonzero(panel.up[day] == 0)
            k = max(len(indices) // 10, 1)
            a = indices[np.argsort(-p[day, indices], kind="stable")[:k]]
            b = indices[np.argsort(-s[day, indices], kind="stable")[:k]]
            assert np.array_equal(a, b), f"Top list changed on {panel.dates[day]}"
        metrics, daily = score(panel, predictions)
        stable_metrics, stable_daily = score(panel, stable)
        assert np.array_equal(daily["excess"].to_numpy(), stable_daily["excess"].to_numpy(), equal_nan=True)
        assert np.array_equal(daily["turnover"].to_numpy(), stable_daily["turnover"].to_numpy(), equal_nan=True)
        unknown_labels = Panel.from_frame(panel.frame.with_columns(pl.lit(None, dtype=pl.Float32).alias("y_ret_1d")))
        assert np.array_equal(predictions, make_candidate(unknown_labels, raw, config))
        prefix_rows = 50 * panel.rows_per_day
        prefix = Panel.from_frame(panel.frame.head(prefix_rows))
        assert np.array_equal(predictions[:prefix_rows], make_candidate(prefix, raw[:prefix_rows], config))
        legacy, old_daily = score(panel, make_candidate(panel, raw,
            {"alpha": .95, "bonus": .15, "restore_lower": False}))
        # Per-day composite uses t2 onward; first-day turnover does not exist.
        delta = .4 * (daily["rank_ic"].to_numpy() - old_daily["rank_ic"].to_numpy())
        delta += .3 * 252 * (daily["excess"].to_numpy() - old_daily["excess"].to_numpy())
        delta -= .3 * (daily["turnover"].to_numpy() - old_daily["turnover"].to_numpy())
        result["years"][str(year)] = {
            "metrics": metrics, "old_metrics": legacy, "stable_only_metrics": stable_metrics,
            "score_delta": metrics["final_score"] - legacy["final_score"],
            "top_order_unchanged_each_day": True,
            "daily_excess_and_turnover_unchanged_by_restore": True,
            "all_labels_removed_invariance": True, "prefix_invariance_50_days": True,
            "paired_composite_hac_t2_onward": hac_stats(delta),
            "ic_restore_delta_hac": hac_stats(daily["rank_ic"].to_numpy() - stable_daily["rank_ic"].to_numpy()),
        }
        print(year, "passed", "score_delta", result["years"][str(year)]["score_delta"],
              "paired_CI", result["years"][str(year)]["paired_composite_hac_t2_onward"]["normal_95_ci"], flush=True)
    result["limitations"] = ["HAC intervals are not adjusted for prior model selection.",
                              "2024 is historical diagnostic data, not a fresh blind test."]
    (OUT / "audit.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
