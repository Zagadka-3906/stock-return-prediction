"""Independent saved-model and written-submission verification, without test labels."""
from pathlib import Path
import hashlib
import json
import sys

import lightgbm as lgb
import numpy as np
import pandas as pd
import polars as pl

ROOT = Path(__file__).resolve().parents[1]
HERE = ROOT / "analysis/connected_validation_20261002"
OUT = ROOT / "deliveries/connected_topk0175_20261003"
ARCHIVE = ROOT.parent / "赛题五_历史归档_20261001"
sys.path[:0] = [str(ROOT), str(HERE), str(ROOT / "analysis")]
from complete_connected_delivery import construct, frozen, sha, now
from optimize_wave6 import make_prediction_param
from return_mapping import apply_mapping, daily_percentile
from src.scoring import Panel
from run import FEATURE_FILE, to_matrix


def main():
    frozen()
    meta = json.loads((OUT / "train_test.json").read_text(encoding="utf-8"))
    assert sha(OUT / "topk0175_fulltrain.txt") == meta["model_sha256"]
    base = pl.read_parquet(ARCHIVE / "deliveries/peer67_slow16_20260929/prediction.parquet")
    keys = ["ts_code", "trade_date"]
    feature = pl.scan_parquet(FEATURE_FILE).filter(~pl.col("is_train")).select(keys + meta["features"]).sort("trade_date", "ts_code").collect()
    assert feature.select(keys).equals(base.select(keys))
    model = lgb.Booster(model_str=(OUT / "topk0175_fulltrain.txt").read_text(encoding="utf-8"))
    raw = model.predict(to_matrix(feature, meta["features"]), num_threads=8)
    raw[~base["price_valid"].to_numpy()] = -1e6
    assert np.array_equal(raw, np.load(OUT / "topk_raw_test.npy")), "Saved model changed raw predictions"
    del feature
    aux = pl.read_parquet(ARCHIVE / "releases/pooled_rms25/auxiliary_raw.parquet")
    assert aux.select(keys).equals(base.select(keys))
    label_free = base.select(keys + ["flag_limit_up", "price_valid", "pred_raw", "rank_score"]).with_columns(
        pl.lit(None, dtype=pl.Float64).alias("y_ret_1d"),
        aux["pred_raw"].alias("aux_raw"),
        pl.Series("w5a_raw", np.load(HERE / "w5a_test/w5a_raw_test.npy")),
        pl.Series("topk_raw", raw))
    inputs_path = OUT / "generation_inputs.parquet"
    if not inputs_path.exists():
        label_free.drop("y_ret_1d").write_parquet(inputs_path, compression="zstd")
    replay = pl.read_parquet(inputs_path).with_columns(pl.lit(None, dtype=pl.Float64).alias("y_ret_1d")).select(label_free.columns)
    assert replay.equals(label_free)
    ar = replay["aux_raw"].to_numpy()
    def processed(col, alpha, bonus):
        panel = Panel.from_frame(replay.with_columns(replay[col].alias("pred_raw")))
        return make_prediction_param(panel, ar, "top_only", 0.25, alpha, bonus, True, 1)
    topk = processed("topk_raw", 0.9, 0.3)
    assert np.array_equal(topk, np.load(OUT / "topk_finished_test.npy"))
    rank, stats = construct(replay, topk, replay["rank_score"].to_numpy(),
                            processed("w5a_raw", 0, 0), processed("pred_raw", 0, 0))
    assert np.array_equal(rank, np.load(OUT / "test_rank_prediction.npy"))
    mapping = json.loads((OUT / "return_mapping.json").read_text(encoding="utf-8"))
    pred = apply_mapping(mapping, daily_percentile(replay.select("trade_date").to_pandas(), rank))
    written = pl.read_csv(OUT / "submission.csv", schema_overrides={"trade_date": pl.Int32}).select(keys).with_row_index("position")
    sub = replay.select(keys).with_columns(pl.Series("pred", pred)).join(written, on=keys, how="inner", validate="1:1").sort("position").select(keys + ["pred"])
    rebuilt = sub.write_csv(float_precision=17).encode("utf-8")
    original = (OUT / "submission.csv").read_bytes()
    assert rebuilt == original, "Submission reconstruction differs byte for byte"
    report = {"status": "passed", "verified_at_local": now(), "model_reload_raw_bit_identical": True,
              "label_free_input_replay": True, "submission_rebuilt_byte_identical": True,
              "test_labels_read": False, "submission_sha256": hashlib.sha256(original).hexdigest(),
              "generation_inputs_sha256": sha(inputs_path), "rows": len(sub), "construction": stats}
    (OUT / "verification.json").write_text(json.dumps(report, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False), flush=True)


if __name__ == "__main__":
    main()
