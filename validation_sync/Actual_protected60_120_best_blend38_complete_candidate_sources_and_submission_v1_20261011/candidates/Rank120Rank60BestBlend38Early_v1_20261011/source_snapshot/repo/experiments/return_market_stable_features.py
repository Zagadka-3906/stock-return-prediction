"""Versioned exact-constant covariance repair; old feature artifacts are immutable.

The new training store copies the eight frozen market columns and changes only
BETA60 under the predeclared Float64 exact-constant-window condition. The pure
build_frame path independently recomputes features from supplied raw rows.
"""
from __future__ import annotations

import argparse
import json
import time
from pathlib import Path

import numpy as np
import polars as pl

from experiments import feature_expansion_features as old
from experiments.day_balance_models import file_hash

ROOT = old.ROOT
OUT = ROOT / "experiments" / "return_market_stable_eval"
ADDED_FEATURE_FILE = OUT / "features.parquet"
KEYS = old.KEYS
INPUT_COLUMNS = old.INPUT_COLUMNS
FEATURE_NAMES = list(old.GROUPS["market_relative"])
EPS = old.EPS
RULE = "Complete finite prior60 Float64 stock returns with exact max==min and complete finite prior60 market returns, with finite sample market variance satisfying abs(var)>1e-12: beta=0 exactly; otherwise retain original beta including nulls."


def _source() -> pl.LazyFrame:
    return pl.scan_csv(old.TRAIN_FILE, schema_overrides={"ts_code": pl.String, "trade_date": pl.Int32,
                       **{name: pl.Float64 for name in INPUT_COLUMNS[2:]}},
                       null_values=["NaN", "nan", ""], low_memory=True).select(INPUT_COLUMNS)


def _eligibility_lazy(frame: pl.LazyFrame) -> pl.LazyFrame:
    frame = frame.select(pl.col("ts_code").cast(pl.String), pl.col("trade_date").cast(pl.Int32),
                         pl.col("close").cast(pl.Float64, strict=False)).sort(KEYS)
    frame = frame.with_columns(pl.when(pl.col("close").is_finite() & (pl.col("close") > 0))
                               .then(pl.col("close")).otherwise(None).alias("close"))
    # Reuse the original division epsilon and finite-return handling verbatim.
    frame = frame.with_columns(old._return(1))
    frame = frame.with_columns(pl.col("_ret1").mean().over("trade_date").alias("_market1"))
    frame = frame.with_columns(
        old._prior(pl.col("_ret1").rolling_min(60, min_samples=60)).alias("_min60"),
        old._prior(pl.col("_ret1").rolling_max(60, min_samples=60)).alias("_max60"),
        old._prior(pl.col("_ret1").is_finite().fill_null(False).cast(pl.Int32)
                   .rolling_sum(60, min_samples=60)).alias("_stock_count60"),
        old._prior(pl.col("_market1").is_finite().fill_null(False).cast(pl.Int32)
                   .rolling_sum(60, min_samples=60)).alias("_market_count60"),
        old._prior(pl.col("_market1").rolling_var(60, min_samples=60, ddof=1)).alias("_market_var60"),
    )
    return frame.select(*KEYS, "_min60", "_max60", "_stock_count60", "_market_count60", "_market_var60",
        ((pl.col("_stock_count60") == 60) & (pl.col("_market_count60") == 60)
         & pl.col("_min60").is_finite() & pl.col("_max60").is_finite()
         & (pl.col("_min60") == pl.col("_max60"))
         & pl.col("_market_var60").is_finite() & (pl.col("_market_var60").abs() > EPS))
        .fill_null(False).alias("_eligible_zero"))


def _repair(base: pl.DataFrame, gate: pl.DataFrame) -> pl.DataFrame:
    joined = base.join(gate.select(*KEYS, "_eligible_zero"), on=KEYS, how="left",
                       validate="1:1", maintain_order="left")
    if joined.height != base.height or joined.get_column("_eligible_zero").null_count():
        raise ValueError("Repair eligibility does not cover the feature keys exactly")
    return joined.with_columns(pl.when(pl.col("_eligible_zero")).then(pl.lit(0, dtype=pl.Float32))
                               .otherwise(pl.col("BETA60")).alias("BETA60")).select(*KEYS, *FEATURE_NAMES)


def build_frame(frame: pl.DataFrame) -> pl.DataFrame:
    """Recompute from raw prefix rows, discarding labels and other extra columns."""
    base = old.build_frame(frame).select(*KEYS, *FEATURE_NAMES)
    gate = _eligibility_lazy(frame.lazy()).collect()
    return _repair(base, gate)


def _comparison(a: pl.DataFrame, b: pl.DataFrame) -> dict:
    if not a.select(KEYS).equals(b.select(KEYS)):
        raise AssertionError("Compared feature keys/order differ")
    result = {}
    for name in FEATURE_NAMES:
        x, y = a.get_column(name).to_numpy(), b.get_column(name).to_numpy()
        mask_equal = bool(np.array_equal(np.isnan(x), np.isnan(y)))
        valid = np.isfinite(x) & np.isfinite(y)
        result[name] = {"null_masks_exact": mask_equal,
                        "nonfinite_nonnull_count": int(np.isinf(x).sum()+np.isinf(y).sum()),
                        "nonexact_count": int(np.count_nonzero(x[valid] != y[valid])),
                        "max_absolute_difference": float(np.max(np.abs(x[valid].astype(float)-y[valid].astype(float)))) if valid.any() else 0.0}
    return result


def _assert_exact(a: pl.DataFrame, b: pl.DataFrame) -> None:
    for name, item in _comparison(a, b).items():
        if not item["null_masks_exact"] or item["nonexact_count"] or item["nonfinite_nonnull_count"]:
            raise AssertionError(f"Exact feature comparison failed for {name}: {item}")


def _fixture() -> pl.DataFrame:
    rng = np.random.default_rng(73017)
    n = 155
    rows = []
    for symbol in ("ZERO", "NONZERO", "NEAR", "VARIABLE", "MISSING", "SHORT"):
        length = 40 if symbol == "SHORT" else n
        if symbol in ("NONZERO", "NEAR"):
            close = np.exp2(np.arange(length, dtype=float))
            if symbol == "NEAR":
                close[70] *= 1 + 1e-10
        elif symbol in ("ZERO", "MISSING"):
            close = np.full(length, 16.0)
            if symbol == "MISSING":
                close[75] = np.nan
                close[110] = np.inf
        else:
            close = 20 * np.cumprod(1 + rng.normal(.001, .013, length))
        for t in range(length):
            rows.append((symbol, 20200101+t, close[t]*1.01, close[t]*.99, close[t],
                         1000+t%17, (1000+t%17)*max(close[t], 1), rng.normal()))
    return pl.DataFrame(rows, schema=INPUT_COLUMNS+["y_ret_1d"], orient="row")


def _numpy_gate(frame: pl.DataFrame) -> pl.DataFrame:
    """Independent direct-window oracle, not a rolling/incremental covariance."""
    frame = frame.select(INPUT_COLUMNS).sort(KEYS)
    codes, dates = frame["ts_code"].to_numpy(), frame["trade_date"].to_numpy()
    close = frame["close"].to_numpy().astype(float).copy()
    close[(close <= 0) | ~np.isfinite(close)] = np.nan
    returns = np.full(len(frame), np.nan)
    indices = [np.flatnonzero(codes == code) for code in sorted(set(codes))]
    for ix in indices:
        with np.errstate(invalid="ignore", divide="ignore", over="ignore"):
            values = close[ix[1:]]/close[ix[:-1]]-1
        values[(np.abs(close[ix[:-1]]) <= EPS) | ~np.isfinite(values)] = np.nan
        returns[ix[1:]] = values
    market = np.full(len(frame), np.nan)
    for date in sorted(set(dates)):
        ix = np.flatnonzero(dates == date)
        valid = returns[ix][np.isfinite(returns[ix])]
        if len(valid):
            market[ix] = np.mean(valid)
    eligible, beta = np.zeros(len(frame), dtype=bool), np.full(len(frame), np.nan)
    for ix in indices:
        for t in range(60, len(ix)):
            prev = ix[t-60:t]
            r, m = returns[prev], market[prev]
            if not (np.isfinite(r).all() and np.isfinite(m).all()):
                continue
            var = np.var(m, ddof=1)
            if not np.isfinite(var) or abs(var) <= EPS:
                continue
            eligible[ix[t]] = bool(np.min(r) == np.max(r))
            beta[ix[t]] = 0.0 if eligible[ix[t]] else np.cov(r, m, ddof=1)[0, 1]/var
    return frame.select(KEYS).with_columns(pl.Series("_eligible_zero", eligible),
                                           pl.Series("_numpy_beta", beta).fill_nan(None).cast(pl.Float32))


def run_tests() -> dict:
    OUT.mkdir(parents=True, exist_ok=True)
    if ADDED_FEATURE_FILE.exists() or (OUT/"feature_manifest.json").exists():
        verify_feature_inputs()
        return json.loads((OUT/"feature_tests.json").read_text(encoding="utf-8"))
    fixture = _fixture()
    gate = _eligibility_lazy(fixture.lazy()).collect()
    oracle = _numpy_gate(fixture)
    assert gate.select(KEYS).equals(oracle.select(KEYS))
    np.testing.assert_array_equal(gate["_eligible_zero"].to_numpy(), oracle["_eligible_zero"].to_numpy())
    actual, legacy = build_frame(fixture), old.build_frame(fixture).select(*KEYS, *FEATURE_NAMES)
    np.testing.assert_array_equal(np.isnan(actual["BETA60"].to_numpy()), np.isnan(oracle["_numpy_beta"].to_numpy()))
    np.testing.assert_allclose(actual["BETA60"].to_numpy(), oracle["_numpy_beta"].to_numpy(), rtol=3e-5, atol=3e-7, equal_nan=True)
    eligible = gate["_eligible_zero"].to_numpy()
    np.testing.assert_array_equal(actual["BETA60"].to_numpy()[eligible], np.zeros(eligible.sum(), dtype=np.float32))
    for name in FEATURE_NAMES:
        if name != "BETA60":
            np.testing.assert_array_equal(actual[name].to_numpy(), legacy[name].to_numpy())
    np.testing.assert_array_equal(actual["BETA60"].to_numpy()[~eligible], legacy["BETA60"].to_numpy()[~eligible])
    _assert_exact(build_frame(fixture.reverse()), actual)
    _assert_exact(build_frame(fixture.drop("y_ret_1d")), actual)
    _assert_exact(build_frame(fixture.with_columns(pl.lit(999999).alias("y_ret_1d"))), actual)
    for cutoff in (20200191, 20200231):
        prefix = actual.filter(pl.col("trade_date") <= cutoff)
        _assert_exact(build_frame(fixture.filter(pl.col("trade_date") <= cutoff)), prefix)
        changed = fixture.with_columns(pl.when(pl.col("trade_date") > cutoff).then(pl.col(name)*3+1)
                                       .otherwise(pl.col(name)).alias(name) for name in INPUT_COLUMNS[2:])
        _assert_exact(build_frame(changed).filter(pl.col("trade_date") <= cutoff), prefix)
    near = gate.filter((pl.col("ts_code") == "NEAR") & (pl.col("trade_date") == 20200181))
    assert near.height == 1 and not near["_eligible_zero"].item()
    assert np.float32(near["_min60"].item()) == np.float32(near["_max60"].item())
    for symbol in ("ZERO", "NONZERO"):
        assert gate.filter(pl.col("ts_code") == symbol)["_eligible_zero"].sum() > 0
    assert not gate.filter(pl.col("ts_code") == "SHORT")["_eligible_zero"].any()
    assert not gate.filter((pl.col("ts_code") == "MISSING") & pl.col("trade_date").is_between(20200177, 20200236))["_eligible_zero"].any()
    # All-market constant returns mean zero market variance: beta must stay null.
    for symbol in ("ZERO", "NONZERO"):
        flat = fixture.filter(pl.col("ts_code") == symbol)
        assert not _eligibility_lazy(flat.lazy()).collect()["_eligible_zero"].any()
        assert build_frame(flat)["BETA60"].null_count() == flat.height
    # Current return affects eligibility only from the following row onward.
    changed = fixture.with_columns(pl.when((pl.col("ts_code") == "ZERO") & (pl.col("trade_date") == 20200181))
                                   .then(pl.col("close")*2).otherwise(pl.col("close")).alias("close"))
    cg = _eligibility_lazy(changed.lazy()).collect()
    assert cg.filter((pl.col("ts_code") == "ZERO") & (pl.col("trade_date") == 20200181))["_eligible_zero"].item()
    assert not cg.filter((pl.col("ts_code") == "ZERO") & (pl.col("trade_date") == 20200182))["_eligible_zero"].item()
    near_epsilon = []
    for amplitude, should_repair in ((2.6e-6, False), (3.0e-6, True)):
        values = amplitude*np.sin(np.arange(100)*2*np.pi/7)
        other_close = 20*np.cumprod(1+values)
        rows = [(symbol, 20200101+t, c*1.01, c*.99, c, 100.0, c*100.0)
                for symbol in ("FLAT", "VARY") for t in range(100)
                for c in [16.0 if symbol == "FLAT" else other_close[t]]]
        small = pl.DataFrame(rows, schema=INPUT_COLUMNS, orient="row")
        sg = _eligibility_lazy(small.lazy()).collect()
        sn = _numpy_gate(small)
        np.testing.assert_array_equal(sg["_eligible_zero"].to_numpy(), sn["_eligible_zero"].to_numpy())
        selected = sg.filter((pl.col("ts_code") == "FLAT") & (pl.col("trade_date") == 20200181))
        assert selected["_eligible_zero"].item() == should_repair
        near_epsilon.append({"amplitude": amplitude, "market_variance": selected["_market_var60"].item(),
                             "repair_applied": should_repair})
        missing_market = small.with_columns(pl.when(pl.col("trade_date") == 20200176)
                                            .then(None).otherwise(pl.col("close")).alias("close"))
        mg = _eligibility_lazy(missing_market.lazy()).collect()
        mn = _numpy_gate(missing_market)
        np.testing.assert_array_equal(mg["_eligible_zero"].to_numpy(), mn["_eligible_zero"].to_numpy())
        selected_missing = mg.filter((pl.col("ts_code") == "FLAT") & (pl.col("trade_date") == 20200181))
        assert selected_missing["_market_count60"].item() < 60 and not selected_missing["_eligible_zero"].item()
    record = {"status": "passed", "passed": True, "feature_count": 8, "rule": RULE,
              "feature_module_sha256": file_hash(Path(__file__)), "legacy_module_sha256": file_hash(Path(old.__file__)),
              "near_epsilon_market_variance_cases": near_epsilon,
              "numpy_beta_tolerance": {"relative": 3e-5, "absolute": 3e-7},
              "checks": ["Independent NumPy exact-constant gate and direct centered covariance",
                         "Zero and nonzero exactly constant returns", "Float32-only pseudo-constant not repaired",
                         "Incomplete, nonfinite and short windows not repaired", "Zero market variance stays null",
                         "Market variance just below/above original epsilon", "Missing paired market-return history stays null",
                         "Grouped symbols with independent histories", "Only eligible beta may change",
                         "Label removal and perturbation", "Row order", "Future and complete-cross-section prefix exactness",
                         "Current observation excluded and following-row exit"]}
    (OUT/"feature_tests.json").write_text(json.dumps(record, ensure_ascii=False, indent=2), encoding="utf-8")
    return record


def build_store() -> dict:
    artifacts = [ADDED_FEATURE_FILE, OUT/"feature_manifest.json", OUT/"real_prefix_audit.json"]
    if any(path.exists() for path in artifacts):
        if not all(path.exists() for path in artifacts):
            raise FileExistsError("Partial stable artifacts exist; refusing to overwrite them")
        verify_feature_inputs()
        return json.loads((OUT/"feature_manifest.json").read_text(encoding="utf-8"))
    from experiments.check_feature_expansion_prefix import _verified_manifest
    legacy_manifest = _verified_manifest()
    tests = json.loads((OUT/"feature_tests.json").read_text(encoding="utf-8"))
    if tests["status"] != "passed" or tests["feature_module_sha256"] != file_hash(Path(__file__)):
        raise ValueError("Run the current stable feature tests before building")
    started = time.monotonic()
    gate = _eligibility_lazy(_source()).collect()
    legacy = pl.read_parquet(old.ADDED_FEATURE_FILE, columns=KEYS+FEATURE_NAMES)
    production_keys = pl.scan_parquet(ROOT/"data/features.parquet").filter(pl.col("is_train")).select(KEYS).collect().sort(KEYS)
    if not production_keys.equals(legacy.select(KEYS)):
        raise ValueError("Stable inputs do not cover the original full training key set")
    del production_keys
    for label, frame in (("eligibility", gate), ("legacy", legacy)):
        if (frame.height != 7900350 or frame.select(pl.struct(KEYS).n_unique()).item() != frame.height
                or any(frame.select(KEYS).null_count().row(0))):
            raise ValueError(f"Invalid full-period {label} keys")
    if not legacy.select(KEYS).equals(gate.select(KEYS)):
        raise ValueError("Full-period legacy feature and eligibility keys differ")
    stable = _repair(legacy, gate)
    if (stable.columns != KEYS+FEATURE_NAMES
            or any(stable.schema[name] != pl.Float32 for name in FEATURE_NAMES)):
        raise ValueError("Stable store schema must be keys plus eight Float32 columns")
    nonfinite_count = sum(int(stable[name].is_infinite().sum()+stable[name].is_nan().sum()) for name in FEATURE_NAMES)
    if nonfinite_count:
        raise AssertionError("Stable store contains nonfinite nonnull features")
    comparison = _comparison(stable, legacy)
    eligible = gate["_eligible_zero"].to_numpy()
    a, b = stable["BETA60"].to_numpy(), legacy["BETA60"].to_numpy()
    changed = ~((a == b) | (np.isnan(a) & np.isnan(b)))
    if np.any(changed & ~eligible):
        raise AssertionError("Beta changed outside the strictly eligible constant windows")
    for name, item in comparison.items():
        if name != "BETA60" and (not item["null_masks_exact"] or item["nonexact_count"]):
            raise AssertionError(f"Unmodified market feature changed: {name}")
    np.testing.assert_array_equal(a[eligible], np.zeros(eligible.sum(), dtype=np.float32))
    stable.write_parquet(ADDED_FEATURE_FILE, compression="zstd", compression_level=3)
    changed_keys = stable.filter(pl.Series(changed)).select(KEYS)
    change_audit = {"rows": len(stable), "eligible_constant_windows": int(eligible.sum()),
                    "beta_changed_rows": int(changed.sum()), "changes_outside_eligible": 0,
                    "beta_null_mask_changed_rows": int(np.count_nonzero(np.isnan(a) != np.isnan(b))),
                    "first_changed_date": changed_keys["trade_date"].min(), "last_changed_date": changed_keys["trade_date"].max(),
                    "changed_securities": changed_keys["ts_code"].n_unique(), "columns": comparison,
                    "nonfinite_nonnull_count": nonfinite_count, "unique_training_keys": True,
                    "complete_production_training_coverage": True, "float32_columns": 8}
    manifest = {"feature_count": 8, "features": FEATURE_NAMES, "rule": RULE,
                "construction": "Copy frozen eight market columns; recompute Float64 exact-constant eligibility from raw training inputs; replace eligible beta only. Other seven columns and noneligible beta are copied exactly, not claimed recalculated.",
                "feature_module_sha256": file_hash(Path(__file__)), "features_sha256": file_hash(ADDED_FEATURE_FILE),
                "source_sha256": legacy_manifest["source_sha256"], "legacy_features_sha256": legacy_manifest["features_sha256"],
                "legacy_module_sha256": file_hash(Path(old.__file__)), "feature_tests_sha256": file_hash(OUT/"feature_tests.json"),
                "source_hashes": {str(path.relative_to(ROOT)):file_hash(path) for path in [Path(old.__file__),old.ADDED_FEATURE_FILE,old.OUT/"feature_manifest.json",old.OUT/"feature_tests.json",old.TRAIN_FILE,ROOT/"experiments/day_balance_models.py"]},
                "input_columns": INPUT_COLUMNS, "labels_used": False, "test_file_read": False,
                "calculation_dtype": "Float64", "storage_dtype": "Float32", "summary": change_audit,
                "seconds": time.monotonic()-started}
    (OUT/"feature_manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    from experiments.check_return_market_stable_prefix import check_prefix_features
    prefix = check_prefix_features()
    (OUT/"real_prefix_audit.json").write_text(json.dumps(prefix, ensure_ascii=False, indent=2), encoding="utf-8")
    if prefix["status"] != "passed":
        raise AssertionError("Stable real prefix is not bitwise exact; do not train or widen the rule")
    return manifest


def verify_feature_inputs(require_prefix: bool = True) -> dict:
    manifest = json.loads((OUT/"feature_manifest.json").read_text(encoding="utf-8"))
    tests = json.loads((OUT/"feature_tests.json").read_text(encoding="utf-8"))
    if (manifest["feature_module_sha256"] != file_hash(Path(__file__))
            or tests["feature_module_sha256"] != manifest["feature_module_sha256"]
            or tests["status"] != "passed" or not tests["passed"]
            or manifest["features"] != FEATURE_NAMES or manifest["feature_count"] != 8
            or manifest["rule"] != RULE or manifest["labels_used"] or manifest["test_file_read"]):
        raise ValueError("Stable feature tests or manifest are stale/incompatible")
    if (manifest["features_sha256"] != file_hash(ADDED_FEATURE_FILE)
            or manifest["feature_tests_sha256"] != file_hash(OUT/"feature_tests.json")):
        raise ValueError("Stable feature artifact hash mismatch")
    if (manifest["summary"]["rows"] != 7900350 or manifest["summary"]["nonfinite_nonnull_count"] != 0
            or not manifest["summary"]["unique_training_keys"]
            or not manifest["summary"]["complete_production_training_coverage"]):
        raise ValueError("Stable feature coverage or finiteness audit failed")
    schema = pl.scan_parquet(ADDED_FEATURE_FILE).collect_schema()
    if schema.names() != KEYS+FEATURE_NAMES or any(schema[name] != pl.Float32 for name in FEATURE_NAMES):
        raise ValueError("Stable feature storage schema differs from the locked eight Float32 columns")
    for relative, expected in manifest["source_hashes"].items():
        if file_hash(ROOT/relative) != expected:
            raise ValueError(f"Frozen source changed: {relative}")
    if require_prefix:
        prefix = json.loads((OUT/"real_prefix_audit.json").read_text(encoding="utf-8"))
        if (prefix["status"] != "passed" or not prefix["all_market_values_float32_exact"]
                or prefix["stored_features_sha256"] != manifest["features_sha256"]
                or prefix["feature_module_sha256"] != manifest["feature_module_sha256"]
                or prefix["prefix_source_sha256"] != file_hash(ROOT/"experiments/check_return_market_stable_prefix.py")):
            raise ValueError("Exact real-prefix test is missing or stale")
    return {"rows": manifest["summary"]["rows"], "feature_count": 8,
            "exact_repair_scope_verified": True, "real_prefix_exact_required": require_prefix}


def joined_frame(mask: pl.Expr, columns: list[str], sort: bool = False) -> pl.DataFrame:
    base_columns = list(dict.fromkeys(KEYS+[name for name in columns if name not in FEATURE_NAMES]))
    base = pl.scan_parquet(ROOT/"data/features.parquet").filter(mask).select(base_columns).collect()
    if sort:
        base = base.sort("trade_date", "ts_code")
    requested = [name for name in FEATURE_NAMES if name in columns]
    extra = pl.scan_parquet(ADDED_FEATURE_FILE).select(KEYS+requested).collect()
    joined = base.join(extra.with_columns(pl.lit(True).alias("_matched")), on=KEYS, how="left",
                       validate="1:1", maintain_order="left")
    if joined.height != base.height or joined["_matched"].null_count() or not joined.select(KEYS).equals(base.select(KEYS)):
        raise ValueError("Stable-feature left join changed row alignment or coverage")
    return joined.drop("_matched")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("stage", choices=("test", "build", "all"))
    args = parser.parse_args()
    if args.stage in ("test", "all"):
        print(json.dumps(run_tests(), ensure_ascii=False, indent=2), flush=True)
    if args.stage in ("build", "all"):
        print(json.dumps(build_store(), ensure_ascii=False, indent=2), flush=True)


if __name__ == "__main__":
    main()
