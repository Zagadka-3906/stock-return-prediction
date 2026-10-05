"""Independently inspect all twenty real classifier fits, saved counters and forecasts."""
from pathlib import Path
import hashlib
import json
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path.insert(0, str(A))
OUT = A / 'streaming_classifier_actual_annual_completion_audit_20261005'


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
    import train_streaming_rank_classifier_bank_v3_20261005 as bank
    assert not OUT.exists()
    audit = bank.read(bank.OUT / 'oof_audit.json')
    execution = bank.read(bank.OUT / 'training_execution_scope.json')
    assert audit['status'] == execution['status'] == 'passed'
    assert audit['actual_annual_fits'] == 20 and audit['configurations'] == bank.CONFIGS
    sources = [Path(__file__), bank.OUT / 'oof_audit.json', bank.OUT / 'training_execution_scope.json',
        bank.OUT / 'protocol.json', Path(bank.__file__), bank.SOURCE,
        A / 'run_streaming_rank_classifier_bank_v3_20261005.py']
    sources += list(bank.OUT.glob('*/info_202[0-4].json'))
    OUT.mkdir()
    create(OUT / 'frozen_before_inspection.json', {'input_sha256': {str(p): sha(p) for p in sources},
        'actual20_full_fits_not_fixture_fits': True, 'test_labels_read': False})
    counts = {2020: 1694259, 2021: 2594048, 2022: 3568878, 2023: 4597785, 2024: 5659954}
    physical_batches = {}
    for year in bank.YEARS:
        cutoff = bank.read(bank.core.BASELINE / f'info_{year}.json')['training_meta']['cutoff_exclusive']
        condition = ((ds.field('is_train') == True) & (ds.field('price_valid') == True)
            & (ds.field('trade_date') < cutoff) & ds.field('y_rank').is_valid()
            & (ds.field('y_rank') < float('inf')) & (ds.field('y_rank') > float('-inf')))
        options = ds.ParquetFragmentScanOptions(pre_buffer=False, use_buffered_stream=True, buffer_size=2**20)
        data = ds.dataset(ROOT / 'data/features.parquet',
            format=ds.ParquetFileFormat(default_fragment_scan_options=options))
        batches = data.scanner(columns=['trade_date'], filter=condition, batch_size=65536,
            batch_readahead=0, fragment_readahead=0, use_threads=False).to_batches()
        sizes = [len(batch) for batch in batches if len(batch)]
        assert sum(sizes) == counts[year]
        physical_batches[year] = len(sizes)
    checks = []
    for name, cfg in bank.CONFIGS.items():
        for year in bank.YEARS:
            folder = bank.OUT / name
            info_path, model, raw = (folder / f'{prefix}_{year}.{suffix}' for prefix, suffix in
                                    (('info', 'json'), ('model', 'joblib'), ('raw', 'parquet')))
            info = bank.read(info_path)
            meta = info['training_meta']
            baseline = bank.read(bank.core.BASELINE / f'info_{year}.json')['training_meta']
            assert info['status'] == 'passed' and info['configuration'] == cfg
            assert info['completed_epochs'] == 32 and not info['test_data_read']
            assert meta['rows'] == baseline['rows'] == counts[year]
            assert meta['cutoff_exclusive'] == baseline['cutoff_exclusive']
            assert meta['last'] < meta['cutoff_exclusive'] and meta['last_label_end'] <= meta['cutoff_exclusive'] < year * 10000 + 101
            assert meta['full_selected_row_keys_match_independent_original_filter']
            assert meta['features'] == bank.feature_names() and len(meta['features']) == 63
            assert sha(model) == info['model_sha256'] and sha(raw) == info['prediction_sha256']
            bundle = bank.core.load_bundle(model)
            expected_counter = 1 + 32 * counts[year]
            assert bundle['classifier'].t_ == bundle['actual_native_sample_counter'] == info['actual_native_sample_counter'] == expected_counter
            assert bundle['actual_partial_fit_calls'] == 32 * physical_batches[year]
            assert bundle['training_rows'] == counts[year] and bundle['completed_epochs'] == 32
            assert bundle['config'] == cfg and bundle['no_validation_early_stopping']
            classes = 2 if cfg['rank_objective'] == 'top10' else 10
            assert np.array_equal(bundle['classifier'].classes_, np.arange(classes))
            cuts = np.asarray(info['class_thresholds_learned_from_mature_past'])
            assert len(cuts) == classes - 1 and np.all(np.diff(cuts) > 0) and np.array_equal(cuts, bundle['class_thresholds'])
            frame = pl.scan_parquet(raw).select(pl.len().alias('rows'),
                pl.col('trade_date').n_unique().alias('days'), pl.col('ts_code').n_unique().alias('codes'),
                pl.col('pred_raw').is_finite().all().alias('finite')).collect().row(0, named=True)
            assert frame['rows'] == info['rows'] and frame['codes'] == 4650 and frame['finite']
            checks.append({'model': name, 'year': year, 'mature_training_rows': counts[year],
                'full32_passes_saved_counter': expected_counter, 'actual_partial_fit_calls': bundle['actual_partial_fit_calls'],
                'original_mature_window_and63_features_match': True, 'model_sha256': info['model_sha256'],
                'raw_sha256': info['prediction_sha256'], 'thresholds_from_mature_past': info['class_thresholds_learned_from_mature_past'],
                'forecast_rows': frame['rows'], 'forecast_days': frame['days'], 'forecast_codes': frame['codes'],
                'training_info_sha256': sha(info_path), 'fit_seconds': info['fit_seconds']})
    rows = [sum(c['forecast_rows'] for c in checks if c['model'] == name) for name in bank.CONFIGS]
    days = [sum(c['forecast_days'] for c in checks if c['model'] == name) for name in bank.CONFIGS]
    assert rows == [5635800] * 4 and days == [1212] * 4
    for path, digest in bank.read(OUT / 'frozen_before_inspection.json')['input_sha256'].items():
        assert sha(path) == digest, path
    value = {'status': 'passed_actual20_full32pass_annual_models_and_forecasts_independently_inspected',
        'at_local': time.strftime('%Y-%m-%dT%H:%M:%S'), 'checks': checks,
        'actual_annual_fits': len(checks), 'configurations': bank.CONFIGS,
        'all4_models_cover_same5635800_rows_and1212_continuous_days': True,
        'all20_saved_estimator_counters_show1_plus32_times_actual_training_rows': True,
        'per_pass_actual_nonempty_physical_scanner_batches': physical_batches,
        'fit_seconds_total': sum(c['fit_seconds'] for c in checks),
        'final4_fits_full_future_checks_and_actual_quality_remain_required': True,
        'new_model_fits_by_audit': 0, 'new_quality_scores': 0, 'test_labels_read': False,
        'source_sha256': {str(p): sha(p) for p in sources}}
    create(OUT / 'verification.json', value)
    print(json.dumps({'status': value['status'], 'actual_annual_fits': 20,
        'fit_seconds_total': value['fit_seconds_total']}, ensure_ascii=False), flush=True)


if __name__ == '__main__':
    main()
