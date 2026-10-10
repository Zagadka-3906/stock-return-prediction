"""Finish the connected-validation selection using the project's declared rule.

Run stages in order: select, folds, train, build, retrospective. Test labels are
read only by the separate retrospective stage, after the submission is frozen.
Historical protocols and results are never rewritten.
"""
from __future__ import annotations

import argparse
import gc
import hashlib
import json
import os
import sys
import time
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

for name in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "POLARS_MAX_THREADS"):
    os.environ[name] = "8"

ROOT = Path(__file__).resolve().parents[1]
HERE = ROOT / "analysis/connected_validation_20261002"
ARCHIVE = ROOT.parent / "赛题五_历史归档_20261001"
OUT = ROOT / "deliveries/connected_topk0175_20261003"
sys.path[:0] = [str(ROOT), str(HERE)]
KEYS = ["ts_code", "trade_date"]
YEARS = (2020, 2021, 2022, 2023, 2024)
FRAC = 0.175
EXPECTED = 0.4459160901521865
EPS = 1e-9


def now():
    return datetime.now(ZoneInfo("Asia/Taipei")).isoformat(timespec="seconds")


def sha(path):
    h = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for chunk in iter(lambda: stream.read(8 * 1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def read(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def write(path, payload):
    path = Path(path)
    text = json.dumps(payload, ensure_ascii=False, indent=2, allow_nan=False) + "\n"
    if path.exists():
        if read(path) != payload:
            raise FileExistsError(f"Preserve existing evidence: {path}")
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def frozen():
    record = read(OUT / "selection.json")
    for path, digest in record["input_sha256"].items():
        actual = sha(ROOT / path)
        if actual != digest and path == "analysis/complete_connected_delivery.py":
            amendment = read(OUT / "code_amendment_001.json")
            assert amendment["original_source_sha256"] == digest
            assert amendment["amended_source_sha256"] == actual
        else:
            assert actual == digest, f"Frozen input changed: {path}"
    assert record["winner"]["connected_final_score"] == EXPECTED
    return record


def select():
    if (OUT / "selection.json").exists():
        frozen()
        print("Selection already frozen and all source hashes match", flush=True)
        return
    rows = []
    sources = [HERE / "connected_results_all.json", *sorted(HERE.glob("wave*results.json"))]
    for path in sources:
        payload = read(path)
        assert payload.get("status") == "complete", path.name
        for arm, record in payload.get("results", {}).items():
            if isinstance(record, dict) and isinstance(record.get("connected_final_score"), (float, int)):
                rows.append({"source": path.name, "arm": arm,
                             "connected_final_score": record["connected_final_score"],
                             "metrics": record.get("connected_metrics", {}),
                             "needs_test_fulltrain_refit": record.get("needs_test_fulltrain_refit", False)})
    rows.sort(key=lambda r: (-r["connected_final_score"], r["source"], r["arm"]))
    winner = rows[0]
    assert winner["source"] == "wave36_results.json" and winner["arm"] == "frac0.175"
    assert winner["connected_final_score"] == EXPECTED
    paths = sources + [ROOT / "后续选模标准.md", Path(__file__),
                       HERE / "optimize_wave31.py", HERE / "optimize_wave36.py",
                       HERE / "optimize_wave6.py", HERE / "optimize_wave13.py",
                       HERE / "optimize_wave15.py", HERE / "optimize_wave18.py",
                       ROOT / "experiments/r6_topk.py", ROOT / "evaluate.py",
                       ROOT / "data/raw/训练集.csv"]
    record = {"status": "frozen_before_test_prediction", "frozen_at_local": now(),
              "selection_rule": "highest connected 2020-2024 official composite; no extra research gate",
              "winner": winner, "scored_records": len(rows),
              "count_note": "scored records include repeated reference cells and repeated candidates",
              "ranking": rows, "test_labels_read_for_selection": False,
              "scheme": {"donor_topk_training_fraction": FRAC, "donor_seed": 2026,
                         "donor_rounds": 180, "promotion_fraction": 0.10,
                         "reranker": "peer67_slow16 at released settings",
                         "orderer": "0.75 W5a + 0.25 peer67_slow16 daily rank blend at alpha0 bonus0",
                         "retention_fraction": 0.985, "tie_epsilon": EPS,
                         "calibration": "monotone isotonic on training OOF predictions plus epsilon percentile"},
              "correction": "Curve roughness, split-half deterioration and retraining cost are disclosed, not rejection gates.",
              "selection_bias": "All five validation years were repeatedly viewed; this is not independent blind evidence.",
              "input_sha256": {p.relative_to(ROOT).as_posix(): sha(p) for p in paths}}
    write(OUT / "selection.json", record)
    write(ROOT / "results/connected_selection_20261003.json",
          {k: v for k, v in record.items() if k not in ("ranking", "input_sha256")})
    print(f"Frozen winner from {len(rows)} scored records: {winner}", flush=True)


def construct(frame, promote, slow_finished, w5a, slow_orderer):
    import numpy as np
    import pandas as pd
    from optimize_wave13 import build_ab
    from optimize_wave15 import daily_ranks, weighted_rank_blend
    from optimize_wave18 import lift

    dates = frame["trade_date"].to_numpy()
    flags = frame["flag_limit_up"].to_numpy().astype(np.int64)
    valid = frame["price_valid"].to_numpy().astype(bool)
    codes, uniques = pd.factorize(frame["ts_code"].to_pandas(), sort=True)
    codes = codes.astype(np.int64)
    key = 1 - codes / max(len(uniques) - 1, 1)
    promote = np.where(np.isfinite(promote) & (promote > -9), promote + EPS * key, promote)
    donor, lift_stats = lift(promote, slow_finished, frame.select(["trade_date", "flag_limit_up"]).to_pandas())
    cache = {"w5a": daily_ranks(w5a, valid, dates), "slow16": daily_ranks(slow_orderer, valid, dates)}
    blend = weighted_rank_blend([w5a, slow_orderer], [0.75, 0.25], cache, valid, dates, ("w5a", "slow16"))
    orderer = np.where(blend > -9, blend + EPS * key, blend) + EPS * key
    pred, stats = build_ab(donor, orderer, orderer, dates, flags, codes, len(uniques), 0.985)
    return pred, {"lift": lift_stats, "retention": stats}


def folds():
    frozen()
    if (OUT / "fold_verification.json").exists():
        print("Fold verification already exists", flush=True)
        return
    import numpy as np
    import polars as pl
    import connected_scorer as cs
    from optimize_wave6 import fold_frame, make_prediction_param
    from src.scoring import Panel
    from experiments.revalidate_fold_local import score_official
    from return_mapping import fit_mapping, daily_percentile, apply_mapping

    frame = cs.combined_frame()
    parts, training = [], {}
    for year in YEARS:
        f = fold_frame(year)
        p = HERE / f"wave36_topk/raw/topk_seed2026_f0.175_{year}.parquet"
        raw = pl.read_parquet(p)
        assert raw.select(KEYS).equals(f.select(KEYS)), f"Fold key mismatch {year}"
        meta = read(HERE / f"wave36_topk/raw/info_f0.175_{year}.json")["training_meta"]
        assert meta["last_date"] < meta["training_cutoff_exclusive"] < f["trade_date"].min()
        training[str(year)] = {**meta, "raw_sha256": sha(p)}
        panel = Panel.from_frame(f.with_columns(pl.Series("pred_raw", raw["pred_raw"])))
        parts.append(make_prediction_param(panel, f["aux_raw"].to_numpy().astype(np.float64),
                                           "top_only", 0.25, 0.9, 0.3, True, 1.0))
    pred, stats = construct(frame, np.concatenate(parts), np.load(HERE / "connected_pred_peer67_slow16.npy"),
                            np.load(HERE / "orderer_a0b0_W5a_five_way_with_gru__final_sweep_eval.npy"),
                            np.load(HERE / "pp_a0_b0_top_only_w0.25_rl1_tcw1.npy"))
    metrics, daily = score_official(frame, pred)
    assert abs(metrics["final_score"] - EXPECTED) < 1e-12
    pct = daily_percentile(frame.select("trade_date").to_pandas(), pred)
    mapping = fit_mapping(pct, frame["y_ret_1d"].to_numpy().astype(np.float64))
    mapped = apply_mapping(mapping, pct)
    after, _ = score_official(frame, mapped)
    assert abs(after["final_score"] - EXPECTED) < 1e-12
    np.save(OUT / "fold_prediction.npy", pred)
    daily.write_csv(OUT / "validation_daily.csv")
    write(OUT / "return_mapping.json", mapping)
    write(OUT / "fold_verification.json", {"status": "passed", "at_local": now(),
          "metrics": metrics, "calibrated_metrics": after, "rows": len(frame),
          "days": frame["trade_date"].n_unique(), "training_boundaries": training,
          "construction": stats, "test_data_read": False,
          "calibration_scope": "Final map uses all 2020-2024 OOF labels for 2025 onward. Historical calibrated scores demonstrate exact rank invariance, not causal historical return calibration.",
          "fold_prediction_sha256": sha(OUT / "fold_prediction.npy")})
    print(f"Exact reconstruction and mapping verified: {metrics}", flush=True)


def train():
    frozen()
    assert read(OUT / "fold_verification.json")["status"] == "passed"
    if (OUT / "train_test.json").exists():
        print("Model and prediction already saved", flush=True)
        return
    import lightgbm as lgb
    import numpy as np
    import polars as pl
    import experiments.r6_topk as rt
    from optimize_wave31 import ObjectiveFrac
    from run import to_matrix, FEATURE_FILE
    from optimize_wave6 import make_prediction_param
    from src.scoring import Panel

    rt.fold_cutoff = lambda year: 20250101
    tr, features, meta = rt.training_frame(2025)
    assert meta["last_date"] == 20241231
    objective = ObjectiveFrac(tr["trade_date"].to_numpy(), tr["y_ret_1d"].to_numpy(), 2026, FRAC, rt.SAMPLES)
    x = to_matrix(tr, features)
    ds = lgb.Dataset(x, label=np.zeros(len(x), dtype=np.float32), feature_name=features, free_raw_data=True)
    del tr
    gc.collect()
    started = time.monotonic()
    def progress(env):
        if (env.iteration + 1) % 30 == 0:
            print(f"TopK0175 full training {env.iteration + 1}/180, {time.monotonic()-started:.0f}s", flush=True)
    model = lgb.train(dict(rt.PARAMS, objective=rt.objective_callback(objective)), ds,
                      num_boost_round=180, callbacks=[progress])
    assert model.current_iteration() == objective.iteration == 180
    (OUT / "topk0175_fulltrain.txt").write_text(model.model_to_string(), encoding="utf-8")
    del x, ds, objective
    gc.collect()
    base = pl.read_parquet(ARCHIVE / "deliveries/peer67_slow16_20260929/prediction.parquet")
    f = pl.scan_parquet(FEATURE_FILE).filter(~pl.col("is_train")).select(KEYS + features).sort(KEYS[1], KEYS[0]).collect()
    assert f.select(KEYS).equals(base.select(KEYS))
    raw = model.predict(to_matrix(f, features), num_threads=8).astype(np.float64)
    raw[~base["price_valid"].to_numpy()] = -1e6
    nulled = base.with_columns(pl.lit(None, dtype=pl.Float64).alias("y_ret_1d"), pl.Series("pred_raw", raw))
    aux = pl.read_parquet(ARCHIVE / "releases/pooled_rms25/auxiliary_raw.parquet")
    assert aux.select(KEYS).equals(base.select(KEYS))
    panel = Panel.from_frame(nulled)
    promote = make_prediction_param(panel, aux["pred_raw"].to_numpy().astype(np.float64),
                                    "top_only", 0.25, 0.9, 0.3, True, 1.0)
    np.save(OUT / "topk_raw_test.npy", raw)
    np.save(OUT / "topk_finished_test.npy", promote)
    write(OUT / "train_test.json", {"status": "passed", "at_local": now(), "training": meta,
          "features": features, "params": rt.PARAMS, "rounds": 180, "fraction": FRAC,
          "model_sha256": sha(OUT / "topk0175_fulltrain.txt"), "test_rows": len(base),
          "test_period_labels_read": False, "prediction_time": "after close on the signal date",
          "last_label_maturity": "2024-12-31 label matures at 2025-01-02 close, before the first forecast is formed",
          "elapsed_seconds": round(time.monotonic() - started, 1)})
    print("Saved full-train model and label-free test predictions", flush=True)


def build():
    frozen()
    if (OUT / "submission_checks.json").exists():
        print("Submission already built", flush=True)
        return
    import numpy as np
    import pandas as pd
    import polars as pl
    from optimize_wave6 import make_prediction_param
    from return_mapping import daily_percentile, apply_mapping
    from src.scoring import Panel

    base = pl.read_parquet(ARCHIVE / "deliveries/peer67_slow16_20260929/prediction.parquet")
    nulled = base.with_columns(pl.lit(None, dtype=pl.Float64).alias("y_ret_1d"))
    aux = pl.read_parquet(ARCHIVE / "releases/pooled_rms25/auxiliary_raw.parquet")
    assert aux.select(KEYS).equals(base.select(KEYS))
    ar = aux["pred_raw"].to_numpy().astype(np.float64)
    w5a_raw = np.load(HERE / "w5a_test/w5a_raw_test.npy")
    proof = read(HERE / "w5a_test/reconstruction_proof.json")
    assert proof["status"] == "proven" and proof["bit_identical"]
    assert sha(HERE / "w5a_test/w5a_raw_test.npy") == proof["raw_output"]["sha256"]
    w5a_panel = Panel.from_frame(nulled.with_columns(pl.Series("pred_raw", w5a_raw)))
    w5a = make_prediction_param(w5a_panel, ar, "top_only", 0.25, 0, 0, True, 1)
    panel = Panel.from_frame(nulled)
    slow = make_prediction_param(panel, ar, "top_only", 0.25, 0, 0, True, 1)
    pred, stats = construct(nulled, np.load(OUT / "topk_finished_test.npy"),
                            base["rank_score"].to_numpy(), w5a, slow)
    mapping = read(OUT / "return_mapping.json")
    dates = base["trade_date"].to_numpy()
    mapped = apply_mapping(mapping, daily_percentile(base.select("trade_date").to_pandas(), pred))
    before = pd.Series(pred).groupby(dates).rank(method="average").to_numpy()
    after = pd.Series(mapped).groupby(dates).rank(method="average").to_numpy()
    assert np.array_equal(before, after)
    bridge = pl.read_csv(ROOT / "data/raw/测试集_X.csv", schema_overrides={"trade_date": pl.Int32}).select(KEYS).with_row_index("position")
    sub = base.select(KEYS).with_columns(pl.Series("pred", mapped)).join(bridge, on=KEYS, how="inner", validate="1:1").sort("position").select(KEYS + ["pred"])
    target = OUT / "submission.csv"
    assert not target.exists()
    sub.write_csv(target, float_precision=17)
    parsed = pd.read_csv(target)
    mem = sub["pred"].to_numpy()
    assert np.array_equal(parsed[KEYS].to_numpy(), bridge.select(KEYS).to_numpy())
    # pandas' default reader is also the reader used by the official evaluator.
    parsed_ranks = parsed.groupby("trade_date")["pred"].rank(method="average").to_numpy()
    mem_ranks = pd.Series(mem).groupby(parsed["trade_date"].to_numpy()).rank(method="average").to_numpy()
    assert np.array_equal(parsed_ranks, mem_ranks), "CSV serialization changed ranks"
    assert len(parsed) == 1599600 and not parsed.duplicated(KEYS).any()
    assert not parsed.isna().any().any() and np.isfinite(parsed.pred).all()
    np.save(OUT / "test_rank_prediction.npy", pred)
    write(OUT / "submission_checks.json", {"status": "passed", "at_local": now(),
          "rows": len(parsed), "days": int(parsed.trade_date.nunique()), "codes": int(parsed.ts_code.nunique()),
          "columns": list(parsed.columns), "date_range": [int(parsed.trade_date.min()), int(parsed.trade_date.max())],
          "duplicate_keys": 0, "nulls": 0, "all_finite": True, "key_order_identical": True,
          "mapping_preserves_ranks": True, "written_csv_preserves_ranks": True,
          "max_roundtrip_error": float(np.max(np.abs(parsed.pred.to_numpy() - mem))),
          "csv_sha256": sha(target), "float_precision": 17, "construction": stats,
          "test_labels_read": False})
    print(f"Built and verified {target}, SHA256 {sha(target)}", flush=True)


def retrospective():
    frozen()
    assert read(OUT / "submission_checks.json")["status"] == "passed"
    if (OUT / "retrospective.json").exists():
        print("Retrospective disclosure already exists", flush=True)
        return
    from evaluate import evaluate
    m = evaluate(str(OUT / "submission.csv"), str(ARCHIVE / "analysis/frozen_holdout_20260928/data"))
    write(OUT / "retrospective.json", {"status": "complete", "at_local": now(),
          "purpose": "retrospective disclosure after selection and submission freeze; no feedback into selection",
          "scorer": "unchanged official evaluate.py on the written CSV", "metrics": {k: float(v) for k, v in m.items()},
          "submission_sha256": sha(OUT / "submission.csv")})
    print(f"Retrospective score: {m['final_score']:.9f}", flush=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("stage", choices=("select", "folds", "train", "build", "retrospective"))
    globals()[parser.parse_args().stage]()
