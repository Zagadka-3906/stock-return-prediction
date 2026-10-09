"""Two fixed model combinations for a separately frozen retrospective protocol.

This module only verifies and loads existing raw predictions, combines daily
ranks, and runs synthetic tests. It does not score, train, select, or publish.
The caller owns the development/confirmation split and protocol freeze.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Mapping

import numpy as np
import polars as pl
from scipy.stats import rankdata

ROOT = Path(__file__).resolve().parents[1]
VALIDATION = ROOT / "experiments/revalidation_20260926/validation"
R4_MANIFEST = ROOT / "releases/ensemble4_r4/release_manifest.json"
R4_MANIFEST_SHA256 = "ecfbe0dd84e04115f7c1736813ba05ded840c6982ed66c791b483d4bded8a4cf"
KEYS = ["ts_code", "trade_date"]
SENTINEL = -10.0
CANDIDATES = {
    "xgb_two_mean": {"members": ("xgboost", "two_day"), "method": "mean"},
    "lgb_xgb_two_median": {
        "members": ("lgb", "xgboost", "two_day"), "method": "median"
    },
}


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(8 * 1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def _checked(path: Path, expected: str, verified: dict) -> Path:
    path = path.resolve()
    if not path.is_relative_to(ROOT.resolve()):
        raise ValueError(f"Input outside project: {path}")
    relative = path.relative_to(ROOT).as_posix()
    actual = sha256(path)
    if actual != expected:
        raise ValueError(f"Input hash mismatch: {relative}")
    verified[relative] = actual
    return path


def _validate_keys(frame: pl.DataFrame, name: str) -> None:
    if any(key not in frame.columns for key in KEYS):
        raise ValueError(f"{name}: missing key columns")
    keys = frame.select(KEYS)
    if keys.null_count().to_numpy().sum() or keys.n_unique() != len(keys):
        raise ValueError(f"{name}: null or duplicate keys")


def align_raw(reference: pl.DataFrame, member: pl.DataFrame,
              raw_column: str = "pred_raw") -> np.ndarray:
    """Return member values in reference order; reject any key-set difference."""
    _validate_keys(reference, "reference")
    _validate_keys(member, "member")
    if raw_column not in member.columns:
        raise ValueError(f"Member missing {raw_column}")
    ref_keys = reference.select(KEYS)
    if len(reference) != len(member) or len(ref_keys.join(member.select(KEYS), on=KEYS, how="anti")):
        raise ValueError("Member/reference key sets differ")
    aligned = ref_keys.with_row_index("_row_order").join(
        member.select(KEYS + [raw_column]), on=KEYS, how="left", validate="1:1"
    ).sort("_row_order")
    return aligned[raw_column].cast(pl.Float64).to_numpy()


def combine_raw(frame: pl.DataFrame, raw_members: Mapping[str, np.ndarray],
                candidate: str) -> np.ndarray:
    """Combine same-day ranks on a common eligible universe, without labels.

    S_t = {i: price_valid_i and every selected member value is finite}.
    For n_t = |S_t|, r_ijt = average_rank_j(i within S_t) / n_t.
    Return (r_X + r_2)/2 or median(r_L, r_X, r_2); outside S_t use -10.
    One common n_t is used for every selected member. No temporal smoothing is
    done here; the caller applies the unchanged, separately frozen final stack.
    """
    spec = CANDIDATES[candidate]
    _validate_keys(frame, "frame")
    if frame["price_valid"].dtype != pl.Boolean or frame["price_valid"].null_count():
        raise ValueError("price_valid must contain nonnull booleans")
    arrays = [np.asarray(raw_members[name], dtype=np.float64) for name in spec["members"]]
    if any(array.shape != (len(frame),) for array in arrays):
        raise ValueError("Each raw member must be a one-dimensional aligned vector")
    keep = frame["price_valid"].to_numpy().copy()
    for array in arrays:
        keep &= np.isfinite(array)
    dates = frame["trade_date"].to_numpy()
    order = np.argsort(dates, kind="stable")
    boundaries = np.r_[0, np.flatnonzero(np.diff(dates[order])) + 1, len(frame)]
    out = np.full(len(frame), SENTINEL, dtype=np.float64)
    for start, end in zip(boundaries[:-1], boundaries[1:]):
        rows = order[start:end]
        rows = rows[keep[rows]]
        if not len(rows):
            continue
        ranks = np.vstack([rankdata(array[rows], method="average") / len(rows) for array in arrays])
        out[rows] = ranks.mean(axis=0) if spec["method"] == "mean" else np.median(ranks, axis=0)
    return out


def load_year(year: int) -> tuple[pl.DataFrame, dict[str, np.ndarray], dict]:
    """Load r4 LGB/XGB/pooled and its exact hash-pinned two-day raw cache.

    Returns the date/code-sorted corrected r4 ensemble4 frame (including its
    pred_raw, aux_raw and labels for the caller's Top/evaluation branches), three
    independent raw vectors, and provenance. Neither pruned member raw cache is
    opened; corrected ensemble4 is not a member of either new combination.
    """
    if year not in range(2020, 2025):
        raise ValueError("Only the five existing retrospective folds are allowed")
    verified: dict[str, str] = {}
    manifest = read_json(_checked(R4_MANIFEST, R4_MANIFEST_SHA256, verified))
    def r4_record(path: Path) -> dict:
        relative = path.relative_to(ROOT).as_posix()
        return read_json(_checked(path, manifest["artifact_sha256"][relative], verified))
    protocol = r4_record(VALIDATION / "protocol.json")
    result = r4_record(VALIDATION / f"result_{year}.json")
    if result["year"] != year or not result["retrospective_previously_viewed"]:
        raise ValueError("Unexpected fold metadata")
    bounds = result["boundaries"]
    if not (bounds["one_day_label_available"] < bounds["validation_first"]
            and bounds["two_day_label_available"] < bounds["validation_first"]):
        raise ValueError("Training label availability overlaps validation")
    frames = {}
    for name in ("baseline", "xgboost", "ensemble4"):
        filename = f"predictions_{name}_{year}.parquet"
        path = VALIDATION / filename
        expected = result["artifacts_sha256"][filename]
        if manifest["artifact_sha256"][path.relative_to(ROOT).as_posix()] != expected:
            raise ValueError("r4 manifest and fold result disagree")
        frames[name] = pl.read_parquet(_checked(path, expected, verified))
    frame = frames["ensemble4"].sort("trade_date", "ts_code")
    if not np.all(frame["trade_date"].to_numpy() // 10000 == year):
        raise ValueError("Unexpected dates in fold cache")
    source = result["cache_sources"]["two_day"]
    if protocol["original_cache_checks"][str(year)]["two_day"] != source:
        raise ValueError("r4 protocol and fold source disagree")
    if protocol["input_sha256"][source["path"]] != source["sha256"]:
        raise ValueError("r4 input hash disagrees with two-day source")
    two = pl.read_parquet(_checked(ROOT / source["path"], source["sha256"], verified))
    raw = {"lgb": align_raw(frame, frames["baseline"]),
           "xgboost": align_raw(frame, frames["xgboost"]),
           "two_day": align_raw(frame, two)}
    for candidate_frame in (frames["baseline"], frames["xgboost"]):
        for name in ("aux_raw", "price_valid"):
            if not np.array_equal(frame[name].to_numpy(), align_raw(frame, candidate_frame, name), equal_nan=True):
                raise ValueError(f"Inconsistent r4 {name} across candidates")
    provenance = {"year": year, "all_years_previously_viewed": True,
                  "boundaries": bounds, "verified_input_sha256": verified,
                  "members": ["lgb", "xgboost", "two_day"], "pruned_member_cache_used": False,
                  "reference_frame": "corrected_r4_ensemble4",
                  "rows": len(frame), "sort": ["trade_date", "ts_code"]}
    return frame, raw, provenance


def synthetic_tests() -> dict:
    """Test mathematical values, ties, alignment errors and time/label locality."""
    frame = pl.DataFrame({"ts_code": ["a", "b", "c", "d", "a", "b"],
                          "trade_date": [1, 1, 1, 1, 2, 2],
                          "price_valid": [True, True, True, False, True, True],
                          "y_ret_1d": [None, .1, -.2, .3, None, .4]})
    raw = {"lgb": np.array([3., 1., 2., 999., 1., np.nan]),
           "xgboost": np.array([1., 1., 3., -999., 2., np.inf]),
           "two_day": np.array([3., 2., 1., 0., 1., 9.])}
    mean = combine_raw(frame, raw, "xgb_two_mean")
    median = combine_raw(frame, raw, "lgb_xgb_two_median")
    np.testing.assert_allclose(mean, [.75, 7 / 12, 2 / 3, -10, 1, -10], rtol=0, atol=1e-15)
    np.testing.assert_allclose(median, [1, .5, 2 / 3, -10, 1, -10], rtol=0, atol=1e-15)
    member = frame.select(KEYS).with_columns(pl.Series("pred_raw", raw["xgboost"]))
    assert np.array_equal(align_raw(frame, member.reverse()), raw["xgboost"], equal_nan=True)
    failures = 0
    for malformed in (member.head(5), pl.concat([member, member.head(1)]),
                      member.with_columns(pl.when(pl.col("ts_code") == "c").then(pl.lit("z")).otherwise(pl.col("ts_code")).alias("ts_code"))):
        try:
            align_raw(frame, malformed)
        except ValueError:
            failures += 1
    assert failures == 3
    permutation = np.array([5, 0, 4, 2, 1, 3])
    shuffled = frame[permutation]
    for candidate in CANDIDATES:
        expected = combine_raw(frame, raw, candidate)
        changed = frame.with_columns(pl.lit(12345.).alias("y_ret_1d"))
        assert np.array_equal(combine_raw(changed, raw, candidate), expected)
        assert np.array_equal(combine_raw(frame.head(4), {k: v[:4] for k, v in raw.items()}, candidate), expected[:4])
        future = {k: v.copy() for k, v in raw.items()}
        for array in future.values():
            array[4:] = [-123., 999.]
        assert np.array_equal(combine_raw(frame, future, candidate)[:4], expected[:4])
        assert np.array_equal(combine_raw(shuffled, {k: v[permutation] for k, v in raw.items()}, candidate), expected[permutation])
    empty = frame.with_columns(pl.lit(False).alias("price_valid"))
    assert np.all(combine_raw(empty, raw, "xgb_two_mean") == SENTINEL)
    return {"status": "passed", "tests": ["exact_mean_and_median_with_ties", "common_finite_universe",
            "invalid_rows_excluded", "member_key_permutation", "missing_duplicate_or_different_keys_rejected",
            "labels_ignored", "prefix_invariance", "future_predictions_do_not_change_past",
            "reference_order_invariance", "empty_eligible_universe"], "real_scores_computed": False}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--test", action="store_true", required=True)
    parser.parse_args()
    print(json.dumps(synthetic_tests(), ensure_ascii=False, indent=2))
