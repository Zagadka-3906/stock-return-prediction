"""Four genuine mature final fits followed by complete copied-model future-X checks."""
from pathlib import Path
import gc
import json
import shutil
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path.insert(0, str(A))
OUT = A / 'streaming_robust_regression_future_qa_20261005'


def main():
    import train_streaming_robust_regression_bank_20261005 as bank
    from locked_read_hash_cache_20261004 import LockedReadHashCache
    from streaming_rank_classifier_actual_resource_recorder_20261005 import ActualCPUResourceRecorder
    audit, execution = bank.OUT / 'oof_audit.json', bank.OUT / 'training_execution_scope.json'
    while not (audit.exists() and execution.exists()):
        if execution.exists() and bank.read(execution)['status'] != 'passed':
            raise RuntimeError('Preserve the failed actual regressor annual attempt.')
        time.sleep(10)
    assert bank.read(audit)['status'] == bank.read(execution)['status'] == 'passed'
    assert bank.read(audit)['actual_annual_fits'] == 20
    run = bank.read(A / 'streaming_robust_regression_future_run_20261005.json')
    for filename, digest in run['input_sha256'].items():
        assert bank.sha(filename) == digest, filename
    bank.verify()
    import numpy as np
    import polars as pl
    import pyarrow as pa
    import pyarrow.dataset as ds
    OUT.mkdir(exist_ok=True)
    paths = [Path(__file__), Path(bank.__file__), bank.SOURCE, bank.STORAGE, audit, execution,
             bank.OUT / 'protocol.json', A / 'streaming_robust_regression_future_run_20261005.json',
             A / 'streaming_rank_classifier_actual_resource_recorder_20261005.py']
    paths += [Path(filename) for filename in bank.read(bank.OUT / 'protocol.json')['input_sha256']]
    paths += list(bank.OUT.glob('*/info_202[0-4].json')) + list(bank.OUT.glob('*/model_202[0-4].joblib'))
    inputs = {str(path.resolve()): bank.sha(path) for path in dict.fromkeys(paths)}
    bank.dump(OUT / 'protocol.json', {'status': 'frozen_before4_actual_mature_final32pass_fits_and_future_X_inference',
        'input_sha256': inputs, 'configurations': bank.CONFIGS, 'expected_final_fits': 4,
        'expected_future_rows': 1599600, 'expected_future_days': 344, 'expected_future_codes': 4650,
        'regression_scores_still_require_mature_return_mapping_in_complete_quality': True,
        'no_validation_early_stopping_or_test_labels': True, 'new_quality_scores': 0}, immutable=True)
    recorder = ActualCPUResourceRecorder(OUT)
    original_sha, original_resource = bank.sha, bank.RESOURCE
    cache = LockedReadHashCache(inputs)
    failure, resources, checks = None, None, []
    try:
        with cache:
            bank.sha, bank.RESOURCE = cache.sha, recorder
            recorder.start()
            for name, cfg in bank.CONFIGS.items():
                info = bank.train_one(name, 2025)
                assert info['configuration'] == cfg and info['completed_epochs'] == 32
                assert info['fulltraining_only_test_prediction_not_generated'] and not info['test_data_read']
                original = bank.OUT / name / 'model_2025.joblib'
                copied = OUT / f'{name}.joblib'
                shutil.copyfile(original, copied)
                assert bank.sha(copied) == bank.sha(original) == info['model_sha256']
                bank.dump(OUT / f'{name}_frozen_before_future_inference.json', {
                    'model_sha256': info['model_sha256'], 'training_info_sha256': bank.sha(bank.OUT / name / 'info_2025.json'),
                    'target_scaling_learned_from_mature_past': info['target_scaling_learned_from_mature_past'],
                    'configuration': cfg, 'test_labels_read': False}, immutable=True)
                recorder.context = {'stage': 'actual_full_future_reload_and_cold80_controls', 'model': name}
                condition = ds.field('is_train') == False
                first, replay = OUT / f'{name}_raw.parquet', OUT / f'{name}_reload_control.parquet'
                bank.infer_stream(bank.core.load_bundle(copied), condition, first)
                bank.infer_stream(bank.core.load_bundle(copied), condition, replay)
                frame = pl.read_parquet(first).sort('trade_date', 'ts_code')
                rebuilt = pl.read_parquet(replay).sort('trade_date', 'ts_code')
                assert frame.equals(rebuilt) and frame['pred_raw'].is_finite().all()
                assert len(frame) == 1599600 and frame['trade_date'].n_unique() == 344 and frame['ts_code'].n_unique() == 4650
                expected = pl.read_parquet(ROOT / 'deliveries/connected_topk0175_20261003/generation_inputs.parquet', columns=bank.KEYS)
                assert frame.select(bank.KEYS).equals(expected)
                first_date = int(frame['trade_date'].min())
                meta = info['training_meta']
                assert meta['last'] < meta['cutoff_exclusive'] and meta['last_label_end'] <= meta['cutoff_exclusive'] <= first_date
                prefix_cutoff = int(frame['trade_date'].unique().sort()[79])
                prefix_path = OUT / f'{name}_cold80_control.parquet'
                bank.infer_stream(bank.core.load_bundle(copied), condition & (ds.field('trade_date') <= prefix_cutoff), prefix_path)
                prefix = pl.read_parquet(prefix_path).sort('trade_date', 'ts_code')
                assert frame.filter(pl.col('trade_date') <= prefix_cutoff).equals(prefix)
                features = bank.feature_names()
                batch = next(batch for batch in bank.core.scanner(bank.KEYS + features, condition) if len(batch))
                x = bank.core.matrix(batch.slice(0, 131), features)
                native = bank.core.predict_arrays(bank.core.load_bundle(copied), x)
                assert np.array_equal(native, bank.engine.predict_arrays(bank.core.load_bundle(copied), x))
                for size in (1, 80, 130):
                    assert np.array_equal(native[:size], bank.core.predict_arrays(bank.core.load_bundle(copied), x[:size]))
                # Keep the final raw artifact in the same date/code order as all
                # other complete native banks and the formal future key table.
                frame.write_parquet(first)
                checks.append({'model': name, 'model_sha256': info['model_sha256'], 'raw_sha256': bank.sha(first),
                    'actual_full1599600_row_reload_bit_identical': True, 'actual_cold80_day_prefix_bit_identical': True,
                    'actual_native131_row_and1_80_130_prefix_bit_identical': True, 'mature_training': meta,
                    'test_labels_read': False, 'new_quality_scores': 0})
                # Remove only the verified duplicate controls in this own QA directory.
                for path in (replay, prefix_path):
                    assert path.resolve().is_relative_to(OUT.resolve())
                    path.unlink()
                del frame, rebuilt, prefix, expected, batch, x, native
                gc.collect()
            cache.reverify()
    except BaseException as error:
        failure = f'{type(error).__name__}: {error}'
        raise
    finally:
        bank.sha, bank.RESOURCE = original_sha, original_resource
        if recorder.thread is not None:
            resources = recorder.finish()
        bank.dump(OUT / 'resource_summary.json', {'status': 'passed' if failure is None else 'failed',
            'failure': failure, 'actual_resources': resources, 'all_hash_and_resource_bindings_restored': True,
            'physical_resource_limit_established': False, 'test_labels_read': False}, immutable=True)
    bank.dump(OUT / 'verification.json', {'status': 'passed', 'checks': checks,
        'actual_fulltraining_fits': len(checks), 'all4_model_fullfuture_reload_and_cold80_controls_passed': len(checks) == 4,
        'input_sha256': inputs, 'resource_summary_sha256': bank.sha(OUT / 'resource_summary.json'),
        'complete_official_quality_and_adoption_still_pending': True,
        'test_labels_read': False, 'new_quality_scores': 0}, immutable=True)


if __name__ == '__main__':
    main()
