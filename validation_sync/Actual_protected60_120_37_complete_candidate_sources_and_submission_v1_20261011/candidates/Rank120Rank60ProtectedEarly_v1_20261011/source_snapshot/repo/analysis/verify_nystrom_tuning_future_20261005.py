"""Ten mature final fits; copied-model future-X reload and cold-prefix controls."""
from pathlib import Path
import json
import os
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT), str(ROOT / 'analysis')]
OUT = ROOT / 'analysis/nystrom_tuning_future_qa_20261005'


def main():
    import train_nystrom_tuning_bank_20261005 as bank
    import psutil
    audit = bank.OUT / 'oof_audit.json'
    while not audit.exists():
        time.sleep(10)
    assert bank.read(audit)['status'] == 'passed'
    assert bank.read(audit)['actual_annual_fits'] == 50
    bank.verify()
    scratch = Path(bank.read(bank.STORAGE)['temporary_directory'])
    assert scratch.drive.upper() in ('D:', 'E:')
    for key in ('TMP', 'TEMP', 'TMPDIR'):
        os.environ[key] = str(scratch)
    while psutil.virtual_memory().available < 14 * 2**30:
        time.sleep(10)
    import gc
    import shutil
    import threading
    import numpy as np
    import polars as pl
    OUT.mkdir(exist_ok=True)
    assert not (OUT / 'verification.json').exists()
    sources = [Path(__file__), Path(bank.__file__), bank.SOURCE, bank.native.SOURCE,
        bank.STORAGE, bank.OUT / 'protocol.json', audit,
        ROOT / 'analysis/nystrom_tuning_preflight_20261005/verification.json',
        ROOT / 'deliveries/connected_topk0175_20261003/generation_inputs.parquet',
        ROOT / 'deliveries/connected_topk0175_20261003/train_test.json']
    sources += list(bank.OUT.glob('*/info_202[0-4].json'))
    sources += list(bank.OUT.glob('*/model_202[0-4].joblib'))
    inputs = {str(path.resolve()): bank.sha(path) for path in sources}
    bank.dump(OUT / 'protocol.json', {
        'status': 'frozen_before_fulltraining_and_future_X_controls', 'at_local': time.strftime('%Y-%m-%dT%H:%M:%S'),
        'configurations': bank.CONFIGS, 'expected_fulltraining_fits': 10,
        'expected_future_rows': 1599600, 'input_sha256': inputs,
        'fulltraining_uses_original_mature_past_eligibility_only': True,
        'minimum_available_ram_before_fullfit_GiB': 14.,
        'reserve_is_scheduling_policy_not_physical_capacity_evidence': True,
        'scope': 'Native raw signals only. Complete schemes, training-only quality scores and adoption require separate subsequent rounds.',
        'new_quality_scores': 0, 'test_labels_read': False}, immutable=True)
    stopped = threading.Event()
    phase = ['load_future_X']
    samples = []

    def observe():
        with (OUT / 'resource_samples.jsonl').open('x', encoding='utf-8') as stream:
            while not stopped.is_set():
                row = {'at_local': time.strftime('%Y-%m-%dT%H:%M:%S'), 'phase': phase[0],
                    'available_ram_bytes': psutil.virtual_memory().available,
                    'qa_python_rss_bytes': psutil.Process().memory_info().rss,
                    'D_free_bytes': psutil.disk_usage('D:/').free,
                    'E_free_bytes': psutil.disk_usage('E:/').free}
                stream.write(json.dumps(row, separators=(',', ':')) + '\n')
                stream.flush()
                samples.append(row)
                stopped.wait(1.)

    thread = threading.Thread(target=observe, daemon=True)
    thread.start()
    checks, failure = [], None
    try:
        features = bank.engine.feature_names()
        assert len(features) == 63
        frame = pl.scan_parquet(bank.engine.FEATURE_FILE).filter(~pl.col('is_train')).select(bank.engine.KEYS + features + ['price_valid']).sort('trade_date', 'ts_code').collect()
        expected = pl.read_parquet(ROOT / 'deliveries/connected_topk0175_20261003/generation_inputs.parquet', columns=bank.engine.KEYS + ['price_valid'])
        assert frame.select(bank.engine.KEYS + ['price_valid']).equals(expected)
        assert len(frame) == 1599600 and frame['trade_date'].n_unique() == 344 and frame['ts_code'].n_unique() == 4650
        first_future_date = int(frame['trade_date'].min())
        x = bank.engine.to_matrix(frame, features)
        valid = frame['price_valid'].to_numpy()
        cutoff = int(frame['trade_date'].unique().sort()[79])
        prefix = frame.filter(pl.col('trade_date') <= cutoff)
        px = bank.engine.to_matrix(prefix, features)
        del expected
        gc.collect()
        for name, cfg in bank.CONFIGS.items():
            phase[0] = 'wait_fullfit_' + name
            while psutil.virtual_memory().available < 14 * 2**30:
                time.sleep(10)
            phase[0] = 'fit_' + name
            info = bank.native.train_one(name, 2025)
            assert info['test_data_read'] is False and info['fulltraining_only_test_prediction_not_generated']
            meta = info['training_meta']
            assert meta['last'] < meta['cutoff_exclusive']
            assert meta['last_label_end'] <= meta['cutoff_exclusive'] <= first_future_date
            model = bank.OUT / name / 'model_2025.joblib'
            copied = OUT / f'{name}.joblib'
            shutil.copyfile(model, copied)
            assert bank.sha(model) == bank.sha(copied) == info['model_sha256']
            bank.dump(OUT / f'{name}_frozen_before_inference.json', {
                'configuration': cfg, 'model_sha256': info['model_sha256'],
                'training_info_sha256': bank.sha(bank.OUT / name / 'info_2025.json'),
                'first_actual_future_date': first_future_date,
                'new_quality_scores': 0, 'test_labels_read': False}, immutable=True)
            phase[0] = 'predict_' + name
            bundle = bank.engine.load_bundle(copied)
            pred = bank.predict_arrays(bundle, x)
            replay = bank.predict_arrays(bank.engine.load_bundle(copied), x)
            assert np.array_equal(pred, replay) and np.isfinite(pred).all()
            assert bundle['config'] == cfg
            phase[0] = 'prefix_' + name
            assert np.array_equal(pred[:len(prefix)], bank.predict_arrays(bank.engine.load_bundle(copied), px))
            assert np.array_equal(pred[:131], bank.native.predict_arrays(bank.engine.load_bundle(copied), x[:131]))
            pred[~valid] = -1e6
            raw = OUT / f'{name}_raw.parquet'
            frame.select(bank.engine.KEYS).with_columns(pl.Series('pred_raw', pred)).write_parquet(raw)
            checks.append({'model': name, 'model_sha256': info['model_sha256'],
                'raw_sha256': bank.sha(raw), 'mature_training': meta,
                'actual_full1599600_rows_copied_model_reload_bit_identical': True,
                'actual_cold80_day_prefix_bit_identical': True,
                'native_fitter131_row_prediction_bit_identical': True,
                'new_quality_scores': 0, 'test_labels_read': False})
            del pred, replay, bundle
            gc.collect()
            print('Expanded kernel final model and future-X controls passed: ' + name, flush=True)
        bank.verify()
        for path, digest in inputs.items():
            assert bank.sha(Path(path)) == digest, path
    except BaseException as error:
        failure = f'{type(error).__name__}: {error}'
        raise
    finally:
        stopped.set()
        thread.join(timeout=10)
        bank.dump(OUT / 'resource_summary.json', {
            'status': 'passed' if failure is None else 'failed', 'failure': failure,
            'samples': len(samples), 'minimum_available_ram_bytes_sampled': min((s['available_ram_bytes'] for s in samples), default=None),
            'maximum_qa_python_rss_bytes_sampled': max((s['qa_python_rss_bytes'] for s in samples), default=None),
            'resource_samples_sha256': bank.sha(OUT / 'resource_samples.jsonl'),
            'physical_resource_boundary_established': False, 'test_labels_read': False}, immutable=True)
    bank.dump(OUT / 'verification.json', {
        'status': 'passed', 'at_local': time.strftime('%Y-%m-%dT%H:%M:%S'),
        'checks': checks, 'actual_fulltraining_fits': len(checks),
        'all10_models_fullfuture_reload_and_cold80_controls_passed': len(checks) == 10,
        'complete_output_official_quality_and_adoption_still_pending': True,
        'new_quality_scores': 0, 'test_labels_read': False}, immutable=True)


if __name__ == '__main__':
    main()
