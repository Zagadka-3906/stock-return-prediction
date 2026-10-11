"""Test four frozen raw-score mixtures on actual five-year rank-model OOF data."""
from pathlib import Path
import hashlib
import json
import os
import sys
import time

for key in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS', 'POLARS_MAX_THREADS'):
    os.environ[key] = '4'
ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT), str(ROOT / 'analysis')]
OUT = ROOT / 'analysis/linear_leaf_ensemble_complementarity_v2_20261005'
MEMBERS = ('rank_lgb_constant_r300', 'rank_lgb_linear_l1_r300', 'rank_lgb_linear_l10_r300')
MIXES = {'all_three_equal': (1/3, 1/3, 1/3), 'linear_pair_equal': (0., .5, .5),
         'constant_linear1_equal': (.5, .5, 0.), 'constant_linear10_equal': (.5, 0., .5)}


def sha(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def create(path, value):
    with Path(path).open('x', encoding='utf-8') as stream:
        json.dump(value, stream, ensure_ascii=False, indent=2)
        stream.write('\n')


def main():
    import gc
    import numpy as np
    import polars as pl
    from refresh_optimization_boundary_evidence_20261004 import complete_round_evidence
    import train_linear_leaf_bank_20261005 as native
    assert complete_round_evidence(64) is not None
    bank = native.OUT
    infos, paths = {}, [Path(__file__), Path(native.__file__), native.STORAGE,
        bank / 'protocol.json', ROOT / 'analysis/optimization_20261003_r64/selection.json',
        ROOT / 'analysis/optimization_20261003_r64/selected_validation.npy',
        ROOT / 'analysis/optimization_20261003_r64/provenance_scope_execution.json',
        ROOT / 'analysis/connected_validation_20261002/combined_fold_frame.parquet',
        ROOT / '后续选模标准.md']
    for name in MEMBERS:
        for year in range(2020, 2025):
            folder = bank / name
            info_path = folder / f'info_{year}.json'
            info = native.read(info_path)
            assert info['status'] == 'passed' and info['model_reload_bit_identical']
            assert info['leaf_summary']['tree_count'] == 300 and info['new_model_fits'] == 1
            assert sha(folder / f'raw_{year}.parquet') == info['prediction_sha256']
            assert sha(folder / f'model_{year}.joblib') == info['model_sha256']
            prefix = bank / f'prefix_control_{name}_{year}.json'
            boundary = bank / f'boundary_control_{name}_{year}.json'
            assert native.read(prefix)['status'] == native.read(boundary)['status'] == 'passed'
            infos[name, year] = info
            paths.extend((info_path, folder / f'raw_{year}.parquet', folder / f'model_{year}.joblib', prefix, boundary))
    for year in range(2020, 2025):
        reference = infos[MEMBERS[0], year]['training_meta']
        assert all(infos[name, year]['training_meta'] == reference for name in MEMBERS)
    OUT.mkdir(exist_ok=True)
    bindings = {str(path.resolve()): sha(path) for path in paths}
    create(OUT / 'frozen_before_controls.json', {
        'status': 'frozen_before_actual_full_oof_mixture_controls', 'at_local': time.strftime('%Y-%m-%dT%H:%M:%S'),
        'members': MEMBERS, 'mixtures': MIXES, 'source_sha256': bindings,
        'no_labels_loaded_for_complementarity_statistics': True, 'no_official_quality_scores_created': True,
        'test_labels_read': False, 'all_choices_are_pending_complete_scheme_official_comparison': True})
    reference = pl.read_parquet(ROOT / 'analysis/connected_validation_20261002/combined_fold_frame.parquet',
        columns=native.engine.KEYS + ['price_valid'])
    assert len(reference) == 5635800 and reference['trade_date'].n_unique() == 1212
    raw = {}
    for name in MEMBERS:
        parts = []
        for year in range(2020, 2025):
            frame = pl.read_parquet(bank / name / f'raw_{year}.parquet')
            assert frame.select(native.engine.KEYS).equals(reference.filter(pl.col('trade_date') // 10000 == year).select(native.engine.KEYS))
            parts.append(frame['pred_raw'].to_numpy())
        raw[name] = np.concatenate(parts)
        assert np.isfinite(raw[name]).all()
    valid = reference['price_valid'].to_numpy()
    dates = reference['trade_date'].to_numpy()
    labels = reference.select('trade_date')
    diagnostic = labels.with_columns([*[pl.Series(name, values) for name, values in raw.items()],
        pl.Series('selected_r64', np.load(ROOT / 'analysis/optimization_20261003_r64/selected_validation.npy')),
        pl.Series('price_valid', valid)]).filter(pl.col('price_valid'))
    correlations = []
    names = [*MEMBERS, 'selected_r64']
    for i, left in enumerate(names):
        for right in names[i+1:]:
            daily = diagnostic.group_by('trade_date').agg(pl.corr(left, right, method='spearman').alias('correlation')).sort('trade_date')
            finite = daily['correlation'].drop_nulls().filter(daily['correlation'].drop_nulls().is_finite())
            assert len(finite) == 1212
            correlations.append({'left': left, 'right': right, 'days': len(finite),
                'mean_daily_rank_correlation': float(finite.mean()),
                'min_daily_rank_correlation': float(finite.min()), 'max_daily_rank_correlation': float(finite.max())})
    controls = []
    import joblib
    for mix, weights in MIXES.items():
        assert sum(weights) == 1. and all(w >= 0. for w in weights)
        values = np.zeros(len(reference), dtype=np.float64)
        for name, weight in zip(MEMBERS, weights):
            if weight:
                values += weight * raw[name]
        values[~valid] = -1e6
        path = OUT / f'{mix}_raw.npy'
        np.save(path, values)
        # An actual serialized composite of full300-round2020 parent models.
        bundle = {'kind': 'linear_leaf_ensemble_control', 'weights': weights,
            'members': [native.engine.load_bundle(bank / name / 'model_2020.joblib') for name in MEMBERS],
            'member_sha256': [infos[name, 2020]['model_sha256'] for name in MEMBERS]}
        model = OUT / f'{mix}_actual2020.joblib'
        joblib.dump(bundle, model, compress=3)
        reloaded = joblib.load(model)
        frame = pl.scan_parquet(native.engine.FEATURE_FILE).filter(pl.col('is_train') &
            (pl.col('trade_date') // 10000 == 2020)).select(native.engine.KEYS + native.engine.feature_names() + ['price_valid']).sort('trade_date', 'ts_code').head(4096).collect()
        x = native.engine.to_matrix(frame, native.engine.feature_names())
        actual = np.zeros(len(x), dtype=np.float64)
        for member, weight in zip(reloaded['members'], reloaded['weights']):
            if weight:
                actual += weight * native.predict_arrays(member, x)
        actual[~frame['price_valid'].to_numpy()] = -1e6
        assert np.array_equal(actual, values[:len(x)])
        counts = (1, 80, 257, 4095)
        for count in counts:
            replay = np.zeros(count, dtype=np.float64)
            for member, weight in zip(reloaded['members'], reloaded['weights']):
                if weight:
                    replay += weight * native.predict_arrays(member, x[:count])
            replay[~frame['price_valid'].to_numpy()[:count]] = -1e6
            assert np.array_equal(replay, actual[:count])
        controls.append({'mixture': mix, 'weights': weights, 'full_oof_rows': len(values),
            'source_annual_models_already_fit': 15, 'new_native_fits': 0,
            'full_oof_raw_sha256': sha(path), 'serialized_actual2020_composite_sha256': sha(model),
            'actual4096_row_saved_full_model_reconstruction_exact': True,
            'native_row_prefix_counts_exact': counts,
            'bit_identical_to_any_single_parent': any(np.array_equal(values, parent) for parent in raw.values()),
            'no_official_quality_score_and_no_adoption_decision': True})
        print('Full OOF raw mixture and actual saved model controls passed: ' + mix, flush=True)
        del values, bundle, reloaded, frame, x, actual
        gc.collect()
    assert not any(row['bit_identical_to_any_single_parent'] for row in controls)
    for path, expected in bindings.items():
        assert sha(path) == expected, path
    create(OUT / 'verification.json', {
        'status': 'passed_actual_five_year_mixture_native_reload_and_prefix_controls',
        'at_local': time.strftime('%Y-%m-%dT%H:%M:%S'), 'source_sha256': bindings,
        'mixture_controls': controls, 'daily_rank_correlations_no_labels': correlations,
        'all15_rank_parent_annual_infos_and_maturity_controls_passed': True,
        'actual_new_annual_fits': 0, 'new_quality_scores': 0, 'test_labels_read': False,
        'raw_signal_statistics_are_not_complete_scheme_official_scores': True,
        'complete_output_official_scoring_and_future_controls_still_required': True,
        'diagnostic_statistics_do_not_add_an_IC_or_correlation_adoption_gate': True})


if __name__ == '__main__':
    main()
