"""Prove W5a's test-period raw column is reconstructible, so the wave-12 orderer is shippable.

Wave 12 selected the five-way GRU ensemble W5a as the ordering donor at alpha 0 / bonus 0. The fold
side is already frozen, but the test side was only ever saved AFTER the released post-processing
(all_models_test_20260929 row 138 -> early_9ec487b9f99e6f94.npy), and post-processing is not
invertible. Using the finished column as the orderer is not an option either: wave 7b scored
topk x finished-W5a at m 0.985 as 0.434034593 against 0.441064514 for the alpha 0 / bonus 0 column,
so smoothing costs 0.0070 in this role.

The raw is recoverable. Four of W5a's five members are frozen test raws in releases/ensemble4/; the
fifth, the gru_cat_h64_w20 sequence model, had its raw array deleted by the 20261001 cleanup but
survives byte-identically in 赛题五_清理备份_20261001 (gru.npy and nn_gru_cat_h64_w20.npy share
sha256 011b7f69...). It is copied into w5a_test/ here rather than written back into the archive.

The proof is the production code path itself: rebuild the raw ensemble with final_sweep_wave3's
ensemble_raw, push it through the released stack exactly as all_models_test_20260929/early/runner.py
does for group final_sweep / W5a, and require element-for-element equality with the saved row-138
array. Equality means every input, the panel construction, the row order and the ensemble rule are
right; anything less means the reconstruction is not W5a.

Nothing is trained. No label is read: the panel is built with y_ret_1d set to null.
"""
from __future__ import annotations

import hashlib
import json
import sys
import time
from pathlib import Path

import numpy as np
import polars as pl

HERE = Path(__file__).resolve().parent
OUT = HERE / "w5a_test"
ROOT = HERE.parents[1]
ARCHIVE = ROOT.parent / "赛题五_历史归档_20261001"
EARLY = ARCHIVE / "analysis/all_models_test_20260929/early"
KEYS = ["ts_code", "trade_date"]

sys.path.insert(0, str(ARCHIVE))
sys.path.insert(0, str(EARLY))

GRU_RAW_RESTORED = OUT / "gru_raw_test.npy"
GRU_RAW_ORIGINS = [
    ARCHIVE.parent / "赛题五_清理备份_20261001/analysis/all_models_test_20260929/early/raw/gru.npy",
    ARCHIVE.parent / "赛题五_清理备份_20261001/analysis/all_models_test_20260929/early/raw/"
                     "nn_gru_cat_h64_w20.npy",
]
ROW138 = EARLY / "predictions/early_9ec487b9f99e6f94.npy"

# runner.py: MEMBER maps W5a's member names onto raw cache names; 'gru_cat_sequence' is absent from
# MEMBER so it falls through to the 'gru' default, which is the gru_cat_h64_w20 raw.
WEIGHTS = {"released_lgb": 1.0, "T2f_xgboost_backbone": 1.0, "W2c_two_day_horizon": 1.0,
           "W2d_pruned_features": 1.0, "gru_cat_sequence": 1.0}
RAW_SOURCE = {
    "released_lgb": ARCHIVE / "releases/pooled_rms25/backbone_raw.parquet",
    "T2f_xgboost_backbone": ARCHIVE / "releases/ensemble4/T2f_xgboost_test_raw.parquet",
    "W2c_two_day_horizon": ARCHIVE / "releases/ensemble4/W2c_two_day_test_raw.parquet",
    "W2d_pruned_features": ARCHIVE / "releases/ensemble4/W2d_pruned_test_raw.parquet",
    "gru_cat_sequence": GRU_RAW_RESTORED,
}
POOLED_AUX = ARCHIVE / "releases/pooled_rms25/auxiliary_raw.parquet"
RELEASED = {"alpha": 0.9, "bonus": 0.3, "rule": "standard", "aux_weight": 0.25}


def sha(path) -> str:
    value = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for chunk in iter(lambda: stream.read(8 * 1024 * 1024), b""):
            value.update(chunk)
    return value.hexdigest()


def log(message: str) -> None:
    print(f"[{time.strftime('%H:%M:%S')}] {message}", flush=True)


def main() -> None:
    if not GRU_RAW_RESTORED.exists():
        raise SystemExit(f"restore the GRU raw first: {GRU_RAW_RESTORED}")
    origins = {str(p): {"exists": p.exists(), "sha256": sha(p) if p.exists() else None}
               for p in GRU_RAW_ORIGINS}
    restored_sha = sha(GRU_RAW_RESTORED)
    if not all(v["exists"] and v["sha256"] == restored_sha for v in origins.values()):
        raise SystemExit(f"the restored GRU raw does not match both cleanup-backup origins: {origins}")
    log(f"GRU raw verified against both cleanup-backup origins: {restored_sha[:16]}…")

    import runner as R  # the archive's own test-period harness

    panel = R.load_panel()
    frame = panel.frame
    log(f"panel built: {frame.shape[0]} rows, {frame['trade_date'].n_unique()} days, "
        f"labels null = {frame['y_ret_1d'].null_count() == frame.shape[0]}")

    cache_raws = {}
    for name, path in RAW_SOURCE.items():
        if path.suffix == ".npy":
            array = np.load(path).astype(np.float64)
            if len(array) != frame.shape[0]:
                raise AssertionError(f"{name}: length {len(array)} != {frame.shape[0]}")
        else:
            df = pl.read_parquet(path).sort("trade_date", "ts_code")
            if not df.select(KEYS).equals(frame.select(KEYS)):
                raise AssertionError(f"{name}: keys are not row-aligned with the panel")
            array = df["pred_raw"].to_numpy().astype(np.float64)
        cache_raws[name] = array
        log(f"  member {name:24s} finite {int(np.isfinite(array).sum()):8d} "
            f"sentinel {int((array == -10.0).sum()):7d}")

    aux = pl.read_parquet(POOLED_AUX).sort("trade_date", "ts_code")
    if not aux.select(KEYS).equals(frame.select(KEYS)):
        raise AssertionError("pooled auxiliary is not row-aligned with the panel")
    aux_values = aux["pred_raw"].to_numpy().astype(np.float64)

    raw_w5a = R.ensemble_raw(panel, WEIGHTS, cache_raws)
    log(f"raw W5a rebuilt: sentinel rows {int((raw_w5a == -10.0).sum())}, "
        f"finite {int(np.isfinite(raw_w5a).sum())}")

    # the released stack, verbatim from runner.py's pipeline() for group final_sweep / W5a
    finished = R.blend_top_only(panel,
                                R.retention_scores(panel, raw_w5a, RELEASED["alpha"],
                                                   RELEASED["bonus"], RELEASED["rule"]),
                                raw_w5a, aux_values, RELEASED["aux_weight"])
    target = np.load(ROW138).astype(np.float64)
    identical = bool(np.array_equal(finished, target))
    max_diff = float(np.abs(finished - target).max())
    log(f"PROOF: rebuilt released column {'EQUALS' if identical else 'DIFFERS FROM'} the saved "
        f"row-138 array (max abs diff {max_diff:.3e})")
    if not identical:
        raise AssertionError("the reconstruction is not W5a: the released post-processing of the "
                             f"rebuilt raw does not reproduce row 138 (max diff {max_diff:.3e})")

    np.save(OUT / "w5a_raw_test.npy", raw_w5a)
    record = {
        "status": "proven",
        "proved_at_local": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "claim": "W5a's test-period RAW column is reconstructible from frozen artifacts, so the "
                 "wave-12 alpha 0 / bonus 0 orderer can be shipped",
        "proof": "ensemble_raw over the five frozen member raws, pushed through the released stack "
                 "exactly as all_models_test_20260929/early/runner.py does for group final_sweep / "
                 "W5a, is element-for-element equal to the saved row-138 prediction array",
        "target_row138": {"path": str(ROW138), "sha256": sha(ROW138),
                          "rows": int(len(target))},
        "max_abs_diff": max_diff,
        "bit_identical": identical,
        "weights": WEIGHTS,
        "member_raw_sources": {k: {"path": str(v), "sha256": sha(v)} for k, v in RAW_SOURCE.items()},
        "gru_raw_restored": {"path": str(GRU_RAW_RESTORED), "sha256": restored_sha,
                             "copied_from": {str(p): v["sha256"] for p, v in origins.items()},
                             "note": "deleted from the archive by the 20261001 cleanup; both backup "
                                     "copies are byte-identical to the restored file. Copied into "
                                     "this research directory, never written back into the archive."},
        "pooled_auxiliary": {"path": str(POOLED_AUX), "sha256": sha(POOLED_AUX)},
        "released_postprocess": RELEASED,
        "panel_rows": int(frame.shape[0]),
        "panel_days": int(frame["trade_date"].n_unique()),
        "labels_read": False,
        "labels_null_in_panel": int(frame["y_ret_1d"].null_count()) == int(frame.shape[0]),
        "trained_anything": False,
        "why_the_finished_column_is_not_enough": {
            "topk_x_finished_W5a_m0.985": 0.434034593,
            "topk_x_a0b0_W5a_m0.985": 0.441064514,
            "cost_of_smoothing_in_the_orderer_role": 0.007029921,
            "source": "wave7b_results.json / wave12_results.json",
        },
        "raw_output": {"path": str(OUT / "w5a_raw_test.npy"),
                       "sha256": sha(OUT / "w5a_raw_test.npy"),
                       "sentinel_rows": int((raw_w5a == -10.0).sum())},
        "source_sha256": sha(Path(__file__)),
    }
    (OUT / "reconstruction_proof.json").write_text(
        json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    log(f"wrote {OUT / 'reconstruction_proof.json'}")
    log(f"raw W5a saved: {OUT / 'w5a_raw_test.npy'} ({restored_sha[:8]}… gru input)")


if __name__ == "__main__":
    main()
