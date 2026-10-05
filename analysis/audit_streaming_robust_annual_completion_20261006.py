"""Inspect all genuine annual regressor counters, keys, scaling and native oracles."""
from pathlib import Path
import hashlib
import json
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path.insert(0, str(A))
OUT = A / 'streaming_robust_actual_annual_completion_audit_20261006'


def sha(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def create(path, value):
    with Path(path).open('x', encoding='utf-8') as stream:
        json.dump(value, stream, ensure_ascii=False, indent=2)
        stream.write('\n')


def main():
    import numpy as np
    import polars as pl
    import pyarrow.dataset as ds
    import train_streaming_robust_regression_bank_20261005 as bank
    assert not OUT.exists()
    annual = bank.read(bank.OUT / 'oof_audit.json')
    scope = bank.read(bank.OUT / 'training_execution_scope.json')
    assert annual['status'] == scope['status'] == 'passed'
    assert annual['actual_annual_fits'] == 20 and annual['configurations'] == bank.CONFIGS
    reference = A / 'connected_validation_20261002/combined_fold_frame.parquet'
    paths = [Path(__file__), Path(bank.__file__), bank.SOURCE, reference, bank.FEATURE_FILE,
        bank.MANIFEST, bank.OUT / 'protocol.json', bank.OUT / 'oof_audit.json',
        bank.OUT / 'training_execution_scope.json', A / 'run_streaming_robust_regression_bank_20261005.py']
    paths += list(bank.OUT.glob('*/info_202[0-4].json')) + list(bank.OUT.glob('*/model_202[0-4].joblib'))
    paths += list(bank.OUT.glob('*/raw_202[0-4].parquet')) + list(bank.OUT.glob('prefix_control_*.json'))
    paths += [bank.core.baseline_path(cfg, year) for cfg in bank.CONFIGS.values() for year in bank.YEARS]
    OUT.mkdir()
    inputs = {str(path.resolve()): sha(path) for path in dict.fromkeys(paths)}
    create(OUT / 'frozen_before_inspection.json', {'input_sha256': inputs,
        'all20_actual_full32pass_fits_required': True, 'new_native_fits': 0, 'test_labels_read': False})
    from locked_read_hash_cache_20261004 import LockedReadHashCache
    physical, checks = {}, []
    with LockedReadHashCache(inputs) as cache:
        keys = pl.read_parquet(reference, columns=bank.KEYS)
        features = bank.feature_names()
        for cfg in bank.CONFIGS.values():
            target = cfg['target']
            for year in bank.YEARS:
                tag = (target, year)
                if tag in physical:
                    continue
                meta = bank.read(bank.core.baseline_path(cfg, year))['training_meta']
                y = ds.field(target)
                condition = ((ds.field('is_train') == True) & (ds.field('price_valid') == True)
                    & (ds.field('trade_date') < meta['cutoff_exclusive']) & y.is_valid()
                    & (y < float('inf')) & (y > float('-inf')))
                options = ds.ParquetFragmentScanOptions(pre_buffer=False, use_buffered_stream=True, buffer_size=2**20)
                source = ds.dataset(bank.FEATURE_FILE, format=ds.ParquetFileFormat(default_fragment_scan_options=options))
                batches = source.scanner(columns=['trade_date'], filter=condition, batch_size=65536,
                    batch_readahead=0, fragment_readahead=0, use_threads=False).to_batches()
                sizes = [len(b) for b in batches if len(b)]
                assert sum(sizes) == meta['rows']
                physical[tag] = {'batches': len(sizes), 'rows': sum(sizes)}
        condition = (ds.field('is_train') == True) & (ds.field('trade_date') >= 20200101) & (ds.field('trade_date') < 20210101)
        batch = next(b for b in bank.core.scanner(bank.KEYS + features, condition) if len(b))
        x = bank.core.matrix(batch.slice(0, 131), features)
        for name, cfg in bank.CONFIGS.items():
            for year in bank.YEARS:
                folder = bank.OUT / name
                info_path = folder / f'info_{year}.json'
                info = bank.read(info_path)
                baseline = bank.read(bank.core.baseline_path(cfg, year))['training_meta']
                meta = info['training_meta']
                assert info['status'] == 'passed' and info['configuration'] == cfg and info['completed_epochs'] == 32
                assert meta['target'] == cfg['target'] and meta['target_not_clipped']
                assert meta['rows'] == baseline['rows'] == physical[(cfg['target'], year)]['rows']
                assert meta['last'] < meta['cutoff_exclusive'] and meta['last_label_end'] <= meta['cutoff_exclusive'] < year * 10000 + 101
                for key in ('cutoff_exclusive', 'first', 'last', 'last_label_end', 'features'):
                    assert meta[key] == baseline[key], key
                assert meta['features'] == features and len(features) == 63
                assert meta['full_selected_row_keys_match_independent_original_filter']
                bundle = bank.core.load_bundle(folder / f'model_{year}.joblib')
                counter = 1 + 32 * meta['rows']
                assert bundle['regressor'].t_ == bundle['actual_native_sample_counter'] == info['actual_native_sample_counter'] == counter
                assert bundle['actual_partial_fit_calls'] == 32 * physical[(cfg['target'], year)]['batches']
                assert bundle['config'] == cfg and bundle['training_rows'] == meta['rows'] and bundle['completed_epochs'] == 32
                assert bundle['no_validation_early_stopping'] and bundle['target_not_clipped']
                assert bundle['target_units'] == cfg['target']
                scaling = info['target_scaling_learned_from_mature_past']
                assert scaling == {'center': bundle['target_center'], 'scale': bundle['target_scale']}
                assert np.isfinite(bundle['target_center']) and np.isfinite(bundle['target_scale']) and bundle['target_scale'] > 0
                assert bundle['regressor'].coef_.shape == (63,)
                native = bank.core.predict_arrays(bundle, x)
                standardized = bank.core.transform(x, bundle['mean'], bundle['scale'], cfg['clip_z'])
                oracle = bundle['regressor'].predict(standardized) * bundle['target_scale'] + bundle['target_center']
                error = float(np.max(np.abs(native - oracle)))
                assert error < 1e-12
                for size in (1, 80, 130):
                    assert np.array_equal(native[:size], bank.core.predict_arrays(bundle, x[:size]))
                frame = pl.read_parquet(folder / f'raw_{year}.parquet')
                assert frame.select(bank.KEYS).equals(keys.filter(pl.col('trade_date') // 10000 == year))
                assert frame['pred_raw'].is_finite().all() and len(frame) == info['rows']
                assert cache.sha(folder / f'model_{year}.joblib') == info['model_sha256']
                assert cache.sha(folder / f'raw_{year}.parquet') == info['prediction_sha256']
                assert bank.read(bank.OUT / f'prefix_control_{name}_{year}.json')['actual_saved_model_full_reload_and_cold80_day_prefix_bit_identical']
                checks.append({'model': name, 'year': year, 'target': cfg['target'], 'loss': cfg['loss'],
                    'mature_training_rows': meta['rows'], 'actual32pass_counter': counter,
                    'actual_partial_fit_calls': bundle['actual_partial_fit_calls'],
                    'full_validation_keys_exact_and_predictions_finite': True,
                    'validation_rows': len(frame), 'validation_days': frame['trade_date'].n_unique(),
                    'independent_SGDRegressor_predict_max_abs_error': error,
                    'target_scaling': scaling, 'model_sha256': info['model_sha256'],
                    'raw_sha256': info['prediction_sha256'], 'info_sha256': cache.sha(info_path)})
        for name in bank.CONFIGS:
            assert sum(row['validation_rows'] for row in checks if row['model'] == name) == 5635800
            assert sum(row['validation_days'] for row in checks if row['model'] == name) == 1212
        cache.reverify()
    create(OUT / 'verification.json', {'status': 'passed_actual20_full32pass_robust_annual_models_independently_inspected',
        'at_local': time.strftime('%Y-%m-%dT%H:%M:%S'), 'checks': checks,
        'actual_full_annual_fits': 20, 'configurations': bank.CONFIGS,
        'all4_same5635800_validation_rows1212days_and_exact_keys': True,
        'all20_actual_estimator_counters_and_physical_batch_passes_verified': True,
        'all20_mature_feature_and_target_scaling_and_no_target_clipping_verified': True,
        'actual20_native_prediction_oracles_and_prefix_controls_passed': True,
        'all_frozen_inputs_full_rehash_and_read_locks_held': True,
        'input_sha256': inputs, 'final4_fits_fullfuture_and_full_official_quality_still_required': True,
        'new_native_fits_by_audit': 0, 'new_quality_scores': 0, 'test_labels_read': False})
    print(json.dumps({'status': 'passed_independent20_full_robust_annual_audit',
        'maximum_native_oracle_error': max(row['independent_SGDRegressor_predict_max_abs_error'] for row in checks)}, ensure_ascii=False), flush=True)


if __name__ == '__main__':
    main()
