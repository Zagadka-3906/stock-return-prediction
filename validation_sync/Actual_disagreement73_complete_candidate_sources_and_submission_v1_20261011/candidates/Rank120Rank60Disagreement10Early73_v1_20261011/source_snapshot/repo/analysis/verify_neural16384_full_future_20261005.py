"""One genuine32-epoch mature final fit and all future-X native controls."""
from pathlib import Path
import gc
import json
import os
import shutil
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT), str(ROOT / 'analysis')]
OUT = ROOT / 'analysis/neural16384_full_future_qa_20261005'


def main():
    import psutil
    import train_neural16384_full_bank_20261005 as bank
    audit = bank.OUT / 'oof_audit.json'
    execution = bank.OUT / 'training_execution_scope.json'
    while not (audit.exists() and execution.exists()):
        if execution.exists() and bank.read(execution)['status'] != 'passed':
            raise RuntimeError('Original complete16384 annual training failed; preserve its actual resource evidence.')
        time.sleep(10)
    assert bank.read(audit)['status'] == bank.read(execution)['status'] == 'passed'
    assert bank.read(audit)['actual_annual_fits'] == 5
    bank.verify()
    while psutil.virtual_memory().available < 14 * 2**30:
        time.sleep(10)
    import numpy as np
    import polars as pl
    import neural16384_full_model_sources_20261005 as router
    from neural16384_actual_resource_recorder_20261005 import ActualResourceRecorder
    from locked_read_hash_cache_20261004 import LockedReadHashCache
    OUT.mkdir(exist_ok=True)
    sources = [Path(__file__), Path(bank.__file__), Path(router.__file__), bank.SOURCE, bank.STORAGE,
        ROOT / 'analysis/neural16384_full_future_run_20261005.json',
        ROOT / 'analysis/neural16384_actual_resource_recorder_20261005.py',
        bank.OUT / 'protocol.json', audit, execution,
        ROOT / 'analysis/neural16384_full_preflight_20261005/verification.json',
        ROOT / 'deliveries/connected_topk0175_20261003/generation_inputs.parquet',
        ROOT / 'deliveries/connected_topk0175_20261003/train_test.json']
    sources += [Path(p) for p in bank.read(bank.OUT / 'protocol.json')['input_sha256']]
    sources += list(bank.OUT.glob('*/info_202[0-4].json'))
    sources += list(bank.OUT.glob('*/model_202[0-4].joblib'))
    inputs = {str(path.resolve()): bank.sha(path) for path in dict.fromkeys(sources)}
    bank.dump(OUT / 'protocol.json', {'status': 'frozen_before_actual_final_fit_and_native_future_X_controls',
        'at_local': time.strftime('%Y-%m-%dT%H:%M:%S'), 'input_sha256': inputs,
        'configurations': bank.CONFIGS, 'expected_final_fits': 1, 'epochs_actual_final_fit': 32,
        'expected_future_rows': 1599600, 'expected_future_days': 344, 'expected_future_codes': 4650,
        'actual_past_training_only_no_validation_early_stopping': True,
        'minimum_available_host_RAM_before_final_fit_GiB': 14.,
        'reserve_is_scheduling_policy_not_physical_limit': True,
        'complete_scheme_official_quality_and_adoption_still_pending': True,
        'new_quality_scores': 0, 'test_labels_read': False}, immutable=True)
    for key in ('TMP', 'TEMP', 'TMPDIR'):
        os.environ[key] = bank.read(bank.STORAGE)['temporary_directory']
    recorder = ActualResourceRecorder(OUT)
    original_fit, original_sha, bank_sha = bank.engine.fit_arrays, bank.engine.sha, bank.sha
    failure, resources, checks = None, None, []
    cache = LockedReadHashCache(inputs)
    try:
        with cache:
            bank.engine.sha = bank.sha = cache.sha
            recorder.start()
            bank.engine.fit_arrays = recorder.measured_fit(original_fit)
            for name, cfg in bank.CONFIGS.items():
                recorder.context = {'stage': 'actual_complete_mature_final_fit', 'model': name, 'year': 2025}
                # Loading future X happens after fitting; its values cannot influence training.
                info = bank.engine.train_one(name, 2025)
                assert info['status'] == 'passed' and info['configuration'] == cfg
                assert info['test_data_read'] is False and info['fulltraining_only_test_prediction_not_generated']
                features = bank.engine.feature_names()
                frame = pl.scan_parquet(bank.engine.FEATURE_FILE).filter(~pl.col('is_train')).select(
                    bank.engine.KEYS + features + ['price_valid']).sort('trade_date', 'ts_code').collect()
                expected = pl.read_parquet(ROOT / 'deliveries/connected_topk0175_20261003/generation_inputs.parquet',
                    columns=bank.engine.KEYS + ['price_valid'])
                assert frame.select(bank.engine.KEYS + ['price_valid']).equals(expected)
                assert len(frame) == 1599600 and frame['trade_date'].n_unique() == 344 and frame['ts_code'].n_unique() == 4650
                first = int(frame['trade_date'].min())
                meta = info['training_meta']
                assert meta['last'] < meta['cutoff_exclusive'] and meta['last_label_end'] <= meta['cutoff_exclusive'] <= first
                x = bank.engine.to_matrix(frame, features)
                cutoff = int(frame['trade_date'].unique().sort()[79])
                prefix = frame.filter(pl.col('trade_date') <= cutoff)
                px = bank.engine.to_matrix(prefix, features)
                model = bank.OUT / name / 'model_2025.joblib'
                copied = OUT / f'{name}.joblib'
                shutil.copyfile(model, copied)
                assert bank.sha(model) == bank.sha(copied) == info['model_sha256']
                bank.dump(OUT / f'{name}_frozen_before_inference.json', {
                    'model_sha256': info['model_sha256'], 'configuration': cfg,
                    'training_info_sha256': bank.sha(bank.OUT / name / 'info_2025.json'),
                    'first_actual_future_date': first, 'new_quality_scores': 0, 'test_labels_read': False}, immutable=True)
                recorder.context = {'stage': 'actual_full_future_reload_and_cold_prefix', 'model': name}
                bundle = router.load_bundle(copied)
                pred = router.predict_arrays(bundle, x)
                replay = router.predict_arrays(router.load_bundle(copied), x)
                assert np.array_equal(pred, replay) and np.isfinite(pred).all()
                assert bundle['config'] == cfg
                assert np.array_equal(pred[:len(prefix)], router.predict_arrays(router.load_bundle(copied), px))
                assert np.array_equal(pred[:131], bank.engine.predict_arrays(router.load_bundle(copied), x[:131]))
                pred[~frame['price_valid'].to_numpy()] = -1e6
                raw = OUT / f'{name}_raw.parquet'
                frame.select(bank.engine.KEYS).with_columns(pl.Series('pred_raw', pred)).write_parquet(raw)
                checks.append({'model': name, 'model_sha256': info['model_sha256'], 'raw_sha256': bank.sha(raw),
                    'mature_training': meta, 'actual_full1599600_row_reload_bit_identical': True,
                    'actual_cold80_day_prefix_bit_identical': True, 'native131_row_prediction_bit_identical': True,
                    'new_quality_scores': 0, 'test_labels_read': False})
                del frame, expected, prefix, x, px, pred, replay, bundle
                gc.collect()
            cache.reverify()
    except BaseException as error:
        failure = f'{type(error).__name__}: {error}'
        raise
    finally:
        bank.engine.fit_arrays, bank.engine.sha, bank.sha = original_fit, original_sha, bank_sha
        if recorder.thread is not None:
            resources = recorder.finish()
        bank.dump(OUT / 'resource_summary.json', {'status': 'passed' if failure is None else 'failed',
            'failure': failure, 'actual_resources': resources, 'all_native_fit_and_hash_bindings_restored': True,
            'physical_resource_boundary_established': False, 'test_labels_read': False}, immutable=True)
    bank.dump(OUT / 'verification.json', {'status': 'passed', 'at_local': time.strftime('%Y-%m-%dT%H:%M:%S'),
        'checks': checks, 'actual_fulltraining_fits': len(checks),
        'all1_model_fullfuture_reload_and_cold80_controls_passed': len(checks) == 1,
        'input_sha256': inputs, 'resource_summary_sha256': bank.sha(OUT / 'resource_summary.json'),
        'complete_output_official_quality_and_adoption_still_pending': True,
        'new_quality_scores': 0, 'test_labels_read': False}, immutable=True)


if __name__ == '__main__':
    main()
