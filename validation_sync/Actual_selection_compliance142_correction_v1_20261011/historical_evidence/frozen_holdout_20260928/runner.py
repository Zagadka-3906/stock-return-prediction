"""Freeze three existing submissions before reconstructing any unseen test returns."""
from __future__ import annotations

import argparse
import hashlib
import importlib.metadata
import json
import math
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd
import polars as pl
from scipy.stats import norm, spearmanr

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
KEYS = ["ts_code", "trade_date"]
ARMS = {
    "base8": "releases/xgboost_seed8_r6",
    "slow8": "candidates/lr0025_rounds360",
    "peer_slow8": "releases/xgboost_peer67_r10",
}
PAIRS = [("slow8", "base8"), ("peer_slow8", "base8"), ("slow8", "peer_slow8")]
BLOCK, DRAWS, SEED = 20, 20000, 20260928
METRICS = ["ic_mean", "ic_std", "icir", "ic_positive_ratio", "annual_excess", "top1_annual_ret", "mean_turnover", "final_score"]


def now():
    return datetime.now(timezone.utc).isoformat()


def sha(path):
    h = hashlib.sha256()
    with Path(path).open("rb") as f:
        while chunk := f.read(2**20):
            h.update(chunk)
    return h.hexdigest()


def read(path):
    return json.loads(Path(path).read_text(encoding="utf-8-sig"))


def write_new(path, obj):
    with Path(path).open("x", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2, allow_nan=False)


def freeze():
    if (OUT / "protocol.json").exists():
        raise RuntimeError("Protocol already frozen; do not replace it.")
    if (OUT / "unblinding_started.json").exists():
        raise RuntimeError("Outcomes were already accessed; cannot create a new pre-registration.")
    audit = read(ROOT / "analysis/model_comparison_20260928/blind_feasibility_training_audit.json")
    assert audit["numeric"]["max_abs_error"] == 0 and audit["finite_mask_mismatches"] == 0
    assert read(OUT / "slow8_reconstruction_audit.json")["status"] == "passed"
    assert (OUT / "pre_freeze_review.json").exists()
    assert read(OUT / "synthetic_preflight.json")["checks"]["no_actual_test_scores"]
    x = pl.read_csv(ROOT / "测试集_X.csv", columns=KEYS)
    assert x.unique().height == x.height
    dates = x["trade_date"].unique().sort().to_list()
    inputs = {}
    for arm, folder in ARMS.items():
        directory = ROOT / folder
        gen = read(directory / "generation.json")
        for name, expected in gen["artifacts_sha256"].items():
            assert sha(ROOT / name) == expected, name
        paths = [directory / "generation.json", directory / "submission.csv", directory / "prediction.parquet", directory / "auxiliary.txt"]
        paths += [directory / f"xgboost_seed{s}.ubj" for s in range(2026, 2034)]
        for p in paths:
            inputs[p.relative_to(ROOT).as_posix()] = sha(p)
        pred = pd.read_csv(directory / "submission.csv")
        assert list(pred.columns) == KEYS + ["pred"]
        assert len(pred) == len(x) and not pred.duplicated(KEYS).any()
        assert np.isfinite(pred["pred"]).all()
        assert pred[KEYS].equals(x.to_pandas()[KEYS])
    for path in [ROOT / "测试集_X.csv", ROOT / "evaluate.py", ROOT / "active_release.json", Path(__file__),
                 OUT / "artifact_review.json", OUT / "slow8_reconstruction_audit.json",
                 OUT / "pre_freeze_review.json", OUT / "synthetic_preflight.json",
                 ROOT / "analysis/model_comparison_20260928/blind_feasibility_training_audit.json"]:
        inputs[path.relative_to(ROOT).as_posix()] = sha(path)
    protocol = {
        "frozen_at_utc": now(), "status_at_freeze": "no_test_returns_constructed_or_prediction_scores_viewed",
        "title": "Frozen comparison on previously unviewed test returns; local reconstructed-label holdout",
        "arms": ARMS, "seeds": list(range(2026, 2034)),
        "period": {"first": dates[0], "last_scored": dates[-2], "excluded_last_date": dates[-1],
                   "scored_days": len(dates) - 1, "full_test_days": len(dates), "stocks_per_day": 4650},
        "label_rule": "Float64 next global market date close / current close - 1; require both prices finite and positive; no fill, no skipping missing dates; drop only the global last date, retain all other rows including missing Y.",
        "scoring": {"authority": "unmodified root evaluate.py on isolated local X/Y and original full submission CSV",
                    "independent_check": "daily pandas implementation, same CSV readers/merge order/default descending sort, max aggregate difference 1e-12",
                    "primary": "0.4*mean daily RankIC + 0.3*252*mean daily Top10 excess + 0.3*(1-mean Jaccard turnover)",
                    "state": "Frozen predictions used as-is, continuous from first test day. No model refit or postprocessing restart.",
                    "segments": "Calendar years 2025 and 2026, slicing full-period daily metrics; cross-year turnover preserved. Descriptive only, not an alternative selection objective."},
        "inference": {"pairs": PAIRS, "main": "paired circular moving-block bootstrap", "block_days": BLOCK,
                      "draws": DRAWS, "rng": f"numpy.default_rng({SEED})", "sample_length": "exact original day count; ceil(n/20) blocks sampled with replacement, wrapped at n and truncated to n",
                      "statistic": "Recompute each component mean on sampled paired day differences, skipping original missing values; never create artificial trades between sampled blocks.",
                      "ci": "percentile 95% descriptive and 98.333333333% per-pair Bonferroni for three two-sided comparisons (nominal familywise 95%)",
                      "sensitivity": "Newey-West Bartlett HAC lags 5,10,20; component-centered influence series with n/component_valid_days weights; normal intervals. Not used to choose among interval methods after results."},
        "decision_rule": {"point_leader": "Highest full-period final_score; differences <=1e-12 reported as a tie.",
                          "clear_comparison_winner": "Only if point leader's bootstrap Bonferroni-adjusted lower confidence bound is >0 against BOTH other frozen arms.",
                          "otherwise": "Report point leader, effect sizes and uncertainty; no claim of a resolved best model. Do not change thresholds or add candidates.",
                          "release": "Comparison and recommendation only; no active_release change or competition upload."},
        "known_before_unblinding": {"2018_2024": "Already used for training and extensive adaptive research; no new blind claim for those years.",
                                     "test_features": "Feature distributions and all three submissions' label-free turnover were already inspected. First reveal concerns IC/return outcomes, not an entirely untouched dataset.",
                                     "prior_recommendation": "slow8 based on historical tradeoffs, not privileged in the holdout scoring rule.",
                                     "training_boundary": "Training rows through 2024-12-31; last training label may mature at first test close, consistent with after-close prediction at t for t+1."},
        "limitations": ["Reconstructed 343-day local outcome labels are not the organizers' complete 344-day hidden labels or an official competition score.",
                        "Bootstrap and HAC are approximate conditional uncertainty, not retraining uncertainty or universal regime generalization.",
                        "After this reveal, the period must be treated as viewed; further tuning or choosing on it consumes its holdout status.",
                        "Return Top and turnover Top use different missing-label eligibility, so gross excess and official turnover are not one executable net portfolio."],
        "input_sha256": inputs,
        "versions": {name: importlib.metadata.version(name) for name in ["numpy", "pandas", "polars", "scipy", "xgboost", "lightgbm"]},
    }
    write_new(OUT / "protocol.json", protocol)
    with (OUT / "protocol.sha256").open("x", encoding="ascii") as f:
        f.write(sha(OUT / "protocol.json") + "\n")
    print(json.dumps({"frozen": True, "protocol_sha256": sha(OUT / "protocol.json"), "period": protocol["period"], "arms": list(ARMS)}, ensure_ascii=False))


def check_frozen():
    assert sha(OUT / "protocol.json") == (OUT / "protocol.sha256").read_text().strip()
    p = read(OUT / "protocol.json")
    for name, expected in p["input_sha256"].items():
        assert sha(ROOT / name) == expected, f"Frozen input changed: {name}"
    return p


def reconstruct(protocol):
    x = pl.read_csv(ROOT / "测试集_X.csv")
    date_map = x.select("trade_date").unique().sort("trade_date").with_columns(pl.col("trade_date").shift(-1).alias("next_market_date"))
    p = x.select(KEYS + ["close"]).sort(KEYS).with_columns(
        pl.col("close").shift(-1).over("ts_code").alias("next_close"),
        pl.col("trade_date").shift(-1).over("ts_code").alias("next_stock_date"),
    ).join(date_map, on="trade_date", how="left")
    valid = (pl.col("next_market_date") == pl.col("next_stock_date")) & pl.col("close").is_finite() & pl.col("next_close").is_finite() & (pl.col("close") > 0) & (pl.col("next_close") > 0)
    p = p.with_columns(pl.when(valid).then(pl.col("next_close") / pl.col("close") - 1).alias("y_ret_1d"))
    last = protocol["period"]["excluded_last_date"]
    keys = x.filter(pl.col("trade_date") != last).select(KEYS)
    labels = keys.join(p.select(KEYS + ["y_ret_1d"]), on=KEYS, how="left", validate="1:1", maintain_order="left")
    local_x = x.filter(pl.col("trade_date") != last).select(KEYS + ["flag_limit_up"])
    assert labels.select(KEYS).equals(local_x.select(KEYS))
    assert labels.height == protocol["period"]["scored_days"] * 4650
    data = OUT / "data"
    data.mkdir(exist_ok=False)
    local_x.write_csv(data / "测试集_X.csv")
    labels.write_csv(data / "测试集_Y.csv", float_scientific=True, float_precision=17)
    return {"rows": labels.height, "days": labels["trade_date"].n_unique(),
            "finite_labels": labels["y_ret_1d"].is_finite().sum(), "missing_labels": labels["y_ret_1d"].null_count(),
            "files": {p.name: sha(p) for p in data.iterdir()}, "created_at_utc": now()}


def daily_metrics(submission):
    pred = pd.read_csv(submission)
    y = pd.read_csv(OUT / "data/测试集_Y.csv")
    x = pd.read_csv(OUT / "data/测试集_X.csv", usecols=KEYS + ["flag_limit_up"])
    df = pred.merge(y, on=KEYS, how="inner", validate="1:1").merge(x, on=KEYS, how="inner", validate="1:1")
    assert len(df) == len(y)
    rows, previous = [], None
    for date, g in df.groupby("trade_date"):
        labeled = g.dropna(subset=["y_ret_1d"])
        ic = float(spearmanr(labeled["pred"], labeled["y_ret_1d"]).statistic) if len(labeled) >= 30 else np.nan
        eligible = g[(g["flag_limit_up"] == 0) & g["y_ret_1d"].notna()].copy()
        excess, top_return = np.nan, np.nan
        if len(eligible) >= 100:
            ordered = eligible.sort_values("pred", ascending=False).reset_index(drop=True)
            top_return = float(ordered["y_ret_1d"].iloc[:max(len(ordered) // 10, 1)].mean())
            excess = top_return - float(ordered["y_ret_1d"].mean())
        tradable = g[g["flag_limit_up"] == 0].copy()
        turnover = np.nan
        if len(tradable) < 100:
            previous = None
        else:
            ordered = tradable.sort_values("pred", ascending=False)
            current = set(ordered["ts_code"].iloc[:max(len(ordered) // 10, 1)])
            if previous:
                turnover = 1 - len(current & previous) / len(current | previous)
            previous = current
        rows.append({"trade_date": int(date), "rank_ic": ic, "excess": excess, "top1_return": top_return,
                     "turnover": turnover, "ic_rows": len(labeled), "return_eligible_rows": len(eligible), "turnover_eligible_rows": len(tradable)})
    return pd.DataFrame(rows)


def aggregate(frame):
    ic, sd = float(frame["rank_ic"].mean()), float(frame["rank_ic"].std(ddof=1))
    excess, turnover = float(frame["excess"].mean() * 252), float(frame["turnover"].mean())
    return {"ic_mean": ic, "ic_std": sd, "icir": ic / sd if sd > 0 else 0.0,
            "ic_positive_ratio": float((frame["rank_ic"].dropna() > 0).mean()), "annual_excess": excess,
            "top1_annual_ret": float(frame["top1_return"].mean() * 252), "mean_turnover": turnover,
            "final_score": .4 * ic + .3 * excess + .3 * (1 - turnover),
            "days": len(frame), "ic_days": int(frame["rank_ic"].count()), "excess_days": int(frame["excess"].count()), "turnover_days": int(frame["turnover"].count())}


def paired(left, right):
    assert left["trade_date"].equals(right["trade_date"])
    cols = ["rank_ic", "excess", "turnover"]
    a, b = left[cols].to_numpy(), right[cols].to_numpy()
    assert np.array_equal(np.isfinite(a), np.isfinite(b))
    delta, w = a - b, np.array([.4, .3 * 252, -.3])
    means, n = np.nanmean(delta, axis=0), len(delta)
    observed = float(means @ w)
    assert abs(observed - (aggregate(left)["final_score"] - aggregate(right)["final_score"])) < 1e-12
    rng = np.random.default_rng(SEED)
    starts = rng.integers(0, n, size=(DRAWS, math.ceil(n / BLOCK)))
    draws = np.empty(DRAWS)
    for begin in range(0, DRAWS, 1000):
        idx = ((starts[begin:begin + 1000, :, None] + np.arange(BLOCK)) % n).reshape(-1, math.ceil(n / BLOCK) * BLOCK)[:, :n]
        draws[begin:begin + len(idx)] = np.nanmean(delta[idx], axis=1) @ w
    counts = np.isfinite(delta).sum(axis=0)
    influence = (np.nan_to_num(delta - means) * (n / counts) * w).sum(axis=1)
    assert abs(influence.mean()) < 1e-12
    hac = {}
    for lag in [5, 10, 20]:
        variance = float(influence @ influence / n)
        for k in range(1, lag + 1):
            variance += 2 * (1 - k / (lag + 1)) * float(influence[k:] @ influence[:-k] / n)
        se = math.sqrt(max(variance, 0) / n)
        t = observed / se if se > 0 else 0.0
        hac[str(lag)] = {"se": se, "t": t, "p_two_sided_normal": float(2 * norm.sf(abs(t))), "ci95": [observed - 1.96 * se, observed + 1.96 * se]}
    return {"score_delta": observed, "component_deltas": dict(zip(cols, means.tolist())),
            "weighted_component_deltas": dict(zip(cols, (means * w).tolist())),
            "bootstrap": {"ci95": np.quantile(draws, [.025, .975]).tolist(),
                          "ci_bonferroni_three_pairs": np.quantile(draws, [.05 / 6, 1 - .05 / 6]).tolist(),
                          "positive_share": float((draws > 0).mean()), "sd": float(draws.std(ddof=1))}, "hac": hac}


def run():
    protocol = check_frozen()
    write_new(OUT / "unblinding_started.json", {"at_utc": now(), "protocol_sha256": sha(OUT / "protocol.json"), "warning": "Outcome period is consumed for holdout purposes after this event."})
    label_info = reconstruct(protocol)
    write_new(OUT / "label_reconstruction.json", label_info)
    import importlib.util
    spec = importlib.util.spec_from_file_location("frozen_official_evaluator", ROOT / "evaluate.py")
    official = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(official)
    arms, daily = {}, {}
    for arm, directory in ARMS.items():
        path = ROOT / directory / "submission.csv"
        metrics = official.evaluate(str(path), str(OUT / "data"))
        frame = daily_metrics(path)
        manual = aggregate(frame)
        error = max(abs(float(metrics[k]) - manual[k]) for k in METRICS)
        assert error < 1e-12, (arm, error)
        frame.to_csv(OUT / f"daily_{arm}.csv", index=False, float_format="%.17g")
        daily[arm] = frame
        segments = {str(y): aggregate(frame[(frame["trade_date"] // 10000) == y]) for y in [2025, 2026]}
        arms[arm] = {"full": manual, "official": {k: float(v) for k, v in metrics.items()}, "independent_max_error": error, "segments_continuous_state": segments}
        write_new(OUT / f"score_{arm}.json", arms[arm])
    pairs = {}
    for left, right in PAIRS:
        pairs[f"{left}_minus_{right}"] = paired(daily[left], daily[right])
    maximum = max(r["full"]["final_score"] for r in arms.values())
    leaders = [arm for arm, r in arms.items() if maximum - r["full"]["final_score"] <= 1e-12]
    resolved = None
    if len(leaders) == 1:
        leader = leaders[0]
        bounds = []
        for other in ARMS:
            if other == leader:
                continue
            if f"{leader}_minus_{other}" in pairs:
                bound = pairs[f"{leader}_minus_{other}"]["bootstrap"]["ci_bonferroni_three_pairs"][0]
            else:
                bound = -pairs[f"{other}_minus_{leader}"]["bootstrap"]["ci_bonferroni_three_pairs"][1]
            bounds.append(bound)
        if min(bounds) > 0:
            resolved = leader
    check_frozen()
    result = {"completed_at_utc": now(), "protocol_sha256": sha(OUT / "protocol.json"), "labels": label_info,
              "arms": arms, "paired_comparisons": pairs, "point_leaders": leaders,
              "clear_comparison_winner_under_preregistered_rule": resolved,
              "frozen_inputs_unchanged_after_scoring": True,
              "active_release_unchanged": read(ROOT / "active_release.json")["release_id"],
              "period_status": "VIEWED: any subsequent tuning on these outcomes is development, not a new blind test."}
    write_new(OUT / "results.json", result)
    write_new(OUT / "output_manifest.json", {p.relative_to(OUT).as_posix(): sha(p) for p in sorted(OUT.rglob("*")) if p.is_file() and p.name not in ["output_manifest.json"]})
    print(json.dumps({"point_leaders": leaders, "clear_winner": resolved, "scores": {k: v["full"]["final_score"] for k, v in arms.items()}}, ensure_ascii=False))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("stage", choices=["freeze", "run", "verify"])
    args = parser.parse_args()
    if args.stage == "freeze":
        freeze()
    elif args.stage == "run":
        run()
    else:
        check_frozen()
        print("Frozen input hashes unchanged.")
