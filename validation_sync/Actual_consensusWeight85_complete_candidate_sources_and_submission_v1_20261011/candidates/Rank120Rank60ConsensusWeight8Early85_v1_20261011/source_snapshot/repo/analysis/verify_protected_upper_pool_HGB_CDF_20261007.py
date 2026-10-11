"""Actual full historical lower-pool CDF bit controls; no selection scores or fits."""
from pathlib import Path
import os
import sys
import time
import hashlib

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path.insert(0, str(A))
for key in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS', 'POLARS_MAX_THREADS'):
    os.environ[key] = '2'
from run_dependency_queue_v3_20261006 import read, sha, create, owned
from atomic_optimization_observer_writes_20261005 import write


def closed(name):
    folder = A / 'service_owned_workflows_20261006' / name
    while owned(read(folder / 'native_launch.json')):
        time.sleep(15)
    assert read(folder / 'service_execution.json')['status'] == 'passed', name


def main():
    import numpy as np
    import pandas as pd
    import polars as pl
    import psutil
    import protected_upper_pool_HGB_CDF_transform_20261007 as transform
    out = A / 'protected_upper_pool_HGB_CDF_preflight_20261007'
    assert not out.exists()
    out.mkdir()
    closed('cpu_full_universe_HGB_native_bank24_v2')
    closed('cpu_full_universe_HGB24_bank_evidence_publication_v2')
    while psutil.virtual_memory().available < 10 * 2**30:
        time.sleep(15)
    plan_path = A / 'protected_upper_pool_HGB_CDF_plan_20261007.json'
    plan = read(plan_path)
    bank = A / plan['training_source']
    bank_proof = read(bank / 'verification.json')
    assert bank_proof['actual_native_fits'] == 24
    parent_path = A / 'optimization_20261003_r112/selected_validation.npy'
    frame_path = A / 'connected_validation_20261002/combined_fold_frame.parquet'
    paths = [Path(__file__), Path(transform.__file__), plan_path, parent_path, frame_path,
        bank / 'verification.json', A / 'github_validation_sync_main_20261005/round112_receipt.json']
    paths += [bank / name / 'raw_oof_predictions.npy' for name in plan['single_native_heads']]
    pins = {str(p): sha(p) for p in paths}
    create(out / 'frozen_before_actual_controls.json', {
        'input_sha256': pins, 'parent_round': 112, 'new_model_fits': 0,
        'new_official_quality_scores': 0, 'labels_not_used_in_forecast_transformation': True,
        'test_labels_read': False})
    from win32_read_handle_hash_cache_with_filename_v2_20261006 import LockedReadHashCache
    with LockedReadHashCache(pins) as scope:
        parent = np.load(parent_path, mmap_mode='r')
        frame = pl.read_parquet(frame_path, columns=['trade_date', 'flag_limit_up', 'price_valid'])
        dates, flags, valid = [frame[c].to_numpy() for c in frame.columns]
        assert len(parent) == len(frame) == 5635800 and frame['trade_date'].n_unique() == 1212
        heads = {name: np.load(bank / name / 'raw_oof_predictions.npy', mmap_mode='r')
            for name in plan['single_native_heads']}
        components = {name: [name] for name in heads}
        components.update(plan['ensembles'])
        days, starts = np.unique(dates, return_index=True)
        ends = np.r_[starts[1:], len(dates)]
        controls = []
        for fraction in plan['lower_fractions']:
            prepared = transform.prepare(parent, dates, flags, valid, fraction)
            independent = []
            for left, right in zip(starts, ends):
                pool = np.arange(left, right)[(flags[left:right] == 0) & valid[left:right]
                    & np.isfinite(parent[left:right]) & (parent[left:right] > -9)]
                if len(pool) < 3:
                    continue
                ordered = pd.Series(np.asarray(parent[pool])).sort_values(kind='mergesort').to_numpy()
                boundary = ordered[min(len(pool) - 1, max(1, int(np.floor(fraction * len(pool)))))]
                positions = pool[parent[pool] < boundary]
                if len(positions) < 2:
                    continue
                independent.append((positions,
                    pd.Series(np.asarray(parent[positions])).rank(method='average', pct=True).to_numpy(),
                    (np.arange(len(positions), dtype=np.float64) + 1.) / len(positions),
                    pd.Series(np.asarray(parent[positions])).sort_values(kind='mergesort').to_numpy()))
            assert len(prepared) == len(independent)
            for actual, expected in zip(prepared, independent):
                for a, b in zip(actual, expected):
                    assert np.array_equal(a.view(np.uint64), b.view(np.uint64))
            selected = np.zeros(len(parent), dtype=bool)
            for positions, _, _, _ in prepared:
                selected[positions] = True
            for name, names in components.items():
                values = [heads[n] for n in names]
                ranks = transform.prepare_heads(values, prepared)
                reference_ranks = []
                for positions, _, _, _ in independent:
                    rows = np.column_stack([pd.Series(np.asarray(head[positions])).rank(method='average', pct=True).to_numpy()
                        for head in values])
                    # The declared component order defines floating-point addition order.
                    combined = rows[:, 0].copy()
                    for column in range(1, rows.shape[1]):
                        combined = combined + rows[:, column]
                    reference_ranks.append(combined / rows.shape[1])
                for actual, expected in zip(ranks, reference_ranks):
                    assert np.array_equal(actual.view(np.uint64), expected.view(np.uint64))
                assert np.array_equal(transform.apply_prepared(parent, 0., prepared, ranks).view(np.uint64), parent.view(np.uint64))
                for weight in plan['weights']:
                    write(out / 'actual_stage.json', {'status': 'actual_full_historical_CDF_bit_controls',
                        'at_local': time.strftime('%Y-%m-%dT%H:%M:%S'), 'completed': len(controls),
                        'expected': 63, 'fraction': fraction, 'model': name, 'weight': weight})
                    actual = transform.apply_prepared(parent, weight, prepared, ranks)
                    reference = np.asarray(parent).copy()
                    for (positions, p, knots, ordered), h in zip(independent, reference_ranks):
                        quantile = p * (1. - weight) + h * weight
                        reference[positions] = np.interp(np.minimum(np.maximum(quantile, knots[0]), knots[-1]), knots, ordered)
                    assert np.array_equal(actual.view(np.uint64), reference.view(np.uint64))
                    assert np.array_equal(actual[~selected].view(np.uint64), parent[~selected].view(np.uint64))
                    for positions, _, _, ordered in prepared:
                        assert actual[positions].min() >= ordered[0] and actual[positions].max() <= ordered[-1]
                    cold = []
                    for count in (80, 260, 975):
                        n = int(ends[count - 1])
                        prefix = transform.transform(parent[:n], dates[:n], flags[:n], valid[:n],
                            [x[:n] for x in values], weight, fraction)
                        assert np.array_equal(prefix.view(np.uint64), actual[:n].view(np.uint64))
                        cold.append({'days': count, 'rows': n, 'bits_exact': True})
                    controls.append({'model': name, 'components': names, 'weight': weight,
                        'lower_fraction': fraction, 'prediction_numeric_sha256': hashlib.sha256(memoryview(actual).cast('B')).hexdigest(),
                        'full_independent_oracle_bits_exact': True, 'unselected_all_bits_preserved': True,
                        'selected_values_inside_parent_subset_range': True, 'cold_prefixes': cold})
                    del actual, reference
            del prepared, independent
        assert len(controls) == 63
        scope.reverify()
        create(out / 'verification.json', {
            'status': 'passed_actual63_full5635800_lower_pool_CDF_independent_oracle_and_cold80_260_975_controls',
            'at_local': time.strftime('%Y-%m-%dT%H:%M:%S'), 'input_sha256': pins, 'controls': controls,
            'rows': 5635800, 'days': 1212, 'symbols': 4650, 'existing_actual_native_bank_fits': 24,
            'new_model_fits': 0, 'new_official_quality_scores': 0,
            'all63_output_definitions_have_weight0_exact_identity_and_upper_flag_invalid_preservation': True,
            'official_Top_with_missing_labels_invariance_not_assumed_or_used_as_hard_gate': True,
            'full_official_scores_selected_freeze_candidate_inference_and_full_QA_still_required': True,
            'test_labels_read': False})


if __name__ == '__main__':
    main()
