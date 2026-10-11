"""Independently check a genuine final fit and every native future-X prediction."""
from pathlib import Path
import hashlib
import json
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path.insert(0, str(A))


def sha(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def create(path, value):
    with path.open('x', encoding='utf-8') as stream:
        json.dump(value, stream, ensure_ascii=False, indent=2)
        stream.write('\n')


def main(name):
    import numpy as np
    import polars as pl
    import pyarrow.dataset as ds
    import train_streaming_robust_regression_bank_20261005 as bank
    from locked_read_hash_cache_20261004 import LockedReadHashCache
    assert name in bank.CONFIGS
    cfg = bank.CONFIGS[name]
    future = A / 'streaming_robust_regression_future_qa_20261005'
    folder = bank.OUT / name
    out = A / 'streaming_robust_final_native_audit_20261006' / name
    assert not out.exists()
    info_path = folder / 'info_2025.json'
    original = folder / 'model_2025.joblib'
    copied = future / f'{name}.joblib'
    raw = future / f'{name}_raw.parquet'
    frozen = future / f'{name}_frozen_before_future_inference.json'
    reference = ROOT / 'deliveries/connected_topk0175_20261003/generation_inputs.parquet'
    paths = [Path(__file__), Path(bank.__file__), bank.SOURCE, Path(bank.core.shared.__file__),
             bank.FEATURE_FILE, bank.MANIFEST, bank.OUT / 'protocol.json',
             future / 'protocol.json', A / 'locked_read_hash_cache_20261004.py',
             A / 'streaming_robust_actual_annual_completion_audit_20261006/verification.json',
             bank.core.baseline_path(cfg, 2025), info_path, original, copied, raw, frozen, reference]
    journal = (bank.OUT / 'actual_native_fit_measurements.jsonl').read_bytes()
    rows = [json.loads(line) for line in journal.splitlines() if line]
    actual = [row for row in rows if row['model'] == name and row['year'] == 2025]
    assert len(actual) == 1
    measurement = actual[0]
    out.mkdir(parents=True)
    inputs = {str(path.resolve()): sha(path) for path in dict.fromkeys(paths)}
    create(out / 'frozen_before_inspection.json', {'input_sha256': inputs,
        'native_fit_record_snapshot': measurement, 'journal_snapshot_sha256': hashlib.sha256(journal).hexdigest(),
        'all1599600_future_predictions_require_independent_SGDRegressor_predict': True,
        'future_read_columns': bank.KEYS + ['price_valid'] + bank.feature_names(),
        'new_native_fits': 0, 'new_quality_scores': 0, 'test_labels_read': False})
    try:
        with LockedReadHashCache(inputs) as cache:
            info = bank.read(info_path)
            baseline = bank.read(bank.core.baseline_path(cfg, 2025))['training_meta']
            assert info['status'] == 'passed' and info['configuration'] == cfg
            assert info['completed_epochs'] == 32 and not info['test_data_read']
            meta = info['training_meta']
            for key in ('rows', 'days', 'first', 'last', 'cutoff_exclusive', 'last_label_end', 'features'):
                assert meta[key] == baseline[key], key
            features = bank.feature_names()
            assert meta['features'] == features and len(features) == 63
            assert meta['target'] == cfg['target'] and meta['target_not_clipped']
            assert meta['full_selected_row_keys_match_independent_original_filter']
            y = ds.field(cfg['target'])
            condition = ((ds.field('is_train') == True) & (ds.field('price_valid') == True)
                & (ds.field('trade_date') < meta['cutoff_exclusive']) & y.is_valid()
                & (y < float('inf')) & (y > float('-inf')))
            sizes = [len(batch) for batch in bank.core.scanner(['trade_date'], condition) if len(batch)]
            assert sum(sizes) == meta['rows']
            assert measurement['status'] == 'completed_full_original32passes'
            assert measurement['actual_rows_in_each_epoch'] == [meta['rows']] * 32
            assert measurement['actual_completed_epochs'] == 32
            assert cache.sha(original) == cache.sha(copied) == info['model_sha256']
            before = bank.read(frozen)
            assert before['model_sha256'] == info['model_sha256']
            assert before['training_info_sha256'] == cache.sha(info_path)
            bundle = bank.core.load_bundle(copied)
            regressor = bundle['regressor']
            samples = 1 + 32 * meta['rows']
            assert regressor.t_ == bundle['actual_native_sample_counter'] == info['actual_native_sample_counter'] == samples
            assert measurement['actual_native_sample_counter'] == samples
            assert measurement['actual_training_rows'] == bundle['training_rows'] == meta['rows']
            assert bundle['actual_partial_fit_calls'] == measurement['actual_partial_fit_calls'] == 32 * len(sizes)
            assert bundle['config'] == cfg and bundle['completed_epochs'] == 32
            assert bundle['target_units'] == cfg['target'] and bundle['target_not_clipped']
            assert bundle['no_validation_early_stopping'] and not regressor.early_stopping
            assert regressor.loss == cfg['loss'] and regressor.average == cfg['average']
            assert regressor.shuffle == cfg['shuffle'] and regressor.random_state == cfg['seed']
            assert regressor.coef_.shape == (63,) and np.isfinite(regressor.coef_).all()
            scaling = {'center': bundle['target_center'], 'scale': bundle['target_scale']}
            assert scaling == info['target_scaling_learned_from_mature_past'] == measurement['target_scaling']
            assert np.isfinite(bundle['target_center']) and np.isfinite(bundle['target_scale']) and bundle['target_scale'] > 0

            frame = pl.read_parquet(raw)
            expected = pl.read_parquet(reference, columns=bank.KEYS)
            assert frame.select(bank.KEYS).equals(expected)
            assert len(frame) == 1599600 and frame['pred_raw'].is_finite().all()
            dates = frame['trade_date'].unique().sort().to_numpy()
            codes = frame['ts_code'].unique().sort().to_numpy()
            assert len(dates) == 344 and len(codes) == 4650
            assert np.array_equal(frame['trade_date'].to_numpy().reshape(344, 4650), np.broadcast_to(dates[:, None], (344, 4650)))
            assert np.array_equal(frame['ts_code'].to_numpy().reshape(344, 4650), np.broadcast_to(codes[None, :], (344, 4650)))
            assert meta['last'] < meta['cutoff_exclusive'] and meta['last_label_end'] <= meta['cutoff_exclusive'] <= int(dates[0])
            observed = frame['pred_raw'].to_numpy()
            seen = np.zeros(len(frame), dtype=bool)
            maximum, batches, prefix_checked = 0., 0, False
            for batch in bank.core.scanner(bank.KEYS + ['price_valid'] + features, ds.field('is_train') == False):
                if not len(batch):
                    continue
                days = batch.column('trade_date').to_numpy(zero_copy_only=False)
                names = batch.column('ts_code').to_numpy(zero_copy_only=False)
                day_index, code_index = np.searchsorted(dates, days), np.searchsorted(codes, names)
                assert np.array_equal(dates[day_index], days) and np.array_equal(codes[code_index], names)
                indices = day_index * 4650 + code_index
                assert len(np.unique(indices)) == len(indices) and not seen[indices].any()
                seen[indices] = True
                x = bank.core.matrix(batch, features)
                standardized = bank.core.transform(x, bundle['mean'], bundle['scale'], cfg['clip_z'])
                oracle = regressor.predict(standardized) * bundle['target_scale'] + bundle['target_center']
                valid = batch.column('price_valid').to_numpy(zero_copy_only=False)
                oracle[~valid] = -1e6
                error = float(np.max(np.abs(oracle - observed[indices])))
                assert error < 1e-12, (name, batches, error)
                maximum = max(maximum, error)
                assert np.array_equal(observed[indices][~valid], np.full(np.sum(~valid), -1e6))
                if not prefix_checked and len(x) >= 131:
                    native = bank.core.predict_arrays(bundle, x[:131])
                    for size in (1, 80, 130):
                        assert np.array_equal(native[:size], bank.core.predict_arrays(bundle, x[:size]))
                    assert np.array_equal(native, bank.core.predict_arrays(bank.core.load_bundle(copied), x[:131]))
                    prefix_checked = True
                batches += 1
            assert seen.all() and prefix_checked
            cache.reverify()
        create(out / 'verification.json', {'status': 'passed_actual_full_final_fit_and_independent_all1599600_native_predictions',
            'at_local': time.strftime('%Y-%m-%dT%H:%M:%S'), 'model': name, 'configuration': cfg,
            'mature_training_rows': meta['rows'], 'actual_completed_epochs': 32,
            'actual_native_sample_counter': samples, 'actual_partial_fit_calls': bundle['actual_partial_fit_calls'],
            'all_future_rows_independently_checked': len(frame), 'future_days': 344, 'future_codes': 4650,
            'independent_full_SGDRegressor_predict_max_abs_error': maximum,
            'native_fullfuture_price_invalid_sentinel_exact': True,
            'actual_saved_reload_and131_row_prefix_controls_passed': True,
            'mature_target_units_scaling_and_physical_train_batch_passes_verified': True,
            'target_scaling': scaling, 'input_sha256': inputs,
            'all4_original_fullfuture_execution_scope_and_official_quality_still_required': True,
            'new_native_fits': 0, 'new_quality_scores': 0, 'test_labels_read': False})
        print(json.dumps({'status': 'passed_independent_final_native_fullfuture_audit', 'model': name,
                          'rows': len(frame), 'maximum_oracle_error': maximum}, ensure_ascii=False), flush=True)
    except BaseException as error:
        create(out / 'failure.json', {'status': 'failed_preserved_native_inspection',
            'at_local': time.strftime('%Y-%m-%dT%H:%M:%S'), 'error': f'{type(error).__name__}: {error}'})
        raise


if __name__ == '__main__':
    main(sys.argv[1])
