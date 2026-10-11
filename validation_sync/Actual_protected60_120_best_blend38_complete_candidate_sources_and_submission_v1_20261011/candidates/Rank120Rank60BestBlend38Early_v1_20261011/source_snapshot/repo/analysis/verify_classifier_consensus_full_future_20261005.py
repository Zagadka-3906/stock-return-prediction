"""Six actual full future-X, saved reload and cold80 fixed-consensus controls."""
from pathlib import Path
import gc
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path.insert(0, str(A))


def main():
    import build_classifier_consensus_bank_20261005 as bank
    from locked_read_hash_cache_20261004 import LockedReadHashCache
    from streaming_rank_classifier_actual_resource_recorder_20261005 import ActualCPUResourceRecorder
    audit, scope = bank.OUT / 'oof_audit.json', bank.OUT / 'construction_execution_scope.json'
    while not (audit.exists() and scope.exists()):
        if scope.exists() and bank.read(scope)['status'] != 'passed':
            raise RuntimeError('Preserve the failed consensus construction attempt.')
        time.sleep(10)
    assert bank.read(audit)['status'] == bank.read(scope)['status'] == 'passed'
    assert bank.read(audit)['actual_virtual_annual_outputs'] == 30
    run = A / 'classifier_consensus_future_run_20261005.json'
    for path, digest in bank.read(run)['input_sha256'].items():
        assert bank.sha(path) == digest, path
    bank.verify()
    import numpy as np
    import polars as pl
    import pyarrow.dataset as ds
    out = bank.FUTURE
    out.mkdir(exist_ok=True)
    assert not (out / 'protocol.json').exists()
    paths = [Path(__file__), run, audit, scope, bank.OUT / 'protocol.json']
    paths += [Path(p) for p in bank.read(bank.OUT / 'protocol.json')['input_sha256']]
    paths += list(bank.OUT.glob('*/info_202[0-4].json')) + list(bank.OUT.glob('*/model_202[0-4].joblib'))
    expected_keys = ROOT / 'deliveries/connected_topk0175_20261003/generation_inputs.parquet'
    paths.append(expected_keys)
    inputs = {str(path.resolve()): bank.sha(path) for path in dict.fromkeys(paths)}
    bank.dump(out / 'protocol.json', {'status': 'frozen_before6_actual_virtual_final_and_fullfuture_controls',
        'input_sha256': inputs, 'configurations': bank.CONFIGS, 'new_native_fits': 0,
        'reused_native_final_fits': 4, 'expected_future_rows': 1599600,
        'expected_future_days': 344, 'expected_future_codes': 4650,
        'test_labels_read': False, 'new_quality_scores': 0}, immutable=True)
    recorder = ActualCPUResourceRecorder(out)
    original_sha, failure, resources, checks = bank.sha, None, None, []
    try:
        with LockedReadHashCache(inputs) as cache:
            bank.sha = cache.sha
            recorder.start()
            for name, cfg in bank.CONFIGS.items():
                recorder.context = {'stage': 'actual_virtual_final_fullfuture_reload_and_cold80', 'model': name}
                info = bank.train_one(name, 2025)
                model = bank.OUT / name / 'model_2025.joblib'
                frozen = out / f'{name}.joblib'
                import shutil
                shutil.copyfile(model, frozen)
                assert bank.sha(frozen) == info['model_sha256'] == bank.sha(model)
                bank.dump(out / f'{name}_frozen_before_future_inference.json', {
                    'model_sha256': info['model_sha256'], 'parent_sources': info['parent_source_sha256'],
                    'training_meta': info['training_meta'], 'new_native_fits': 0,
                    'test_labels_read': False}, immutable=True)
                condition = ds.field('is_train') == False
                first, replay = out / f'{name}_raw.parquet', out / f'{name}_reload_control.parquet'
                bank.infer_stream(bank.parent.core.load_bundle(frozen), condition, first)
                bank.infer_stream(bank.parent.core.load_bundle(frozen), condition, replay)
                frame = pl.read_parquet(first).sort('trade_date', 'ts_code')
                rebuilt = pl.read_parquet(replay).sort('trade_date', 'ts_code')
                assert frame.equals(rebuilt) and frame['pred_raw'].is_finite().all()
                assert (len(frame), frame['trade_date'].n_unique(), frame['ts_code'].n_unique()) == (1599600, 344, 4650)
                assert frame.select(bank.KEYS).equals(pl.read_parquet(expected_keys, columns=bank.KEYS))
                meta = info['training_meta']
                assert meta['last'] < meta['cutoff_exclusive'] and meta['last_label_end'] <= meta['cutoff_exclusive'] <= frame['trade_date'].min()
                cutoff = int(frame['trade_date'].unique().sort()[79])
                prefix_path = out / f'{name}_cold80_control.parquet'
                bank.infer_stream(bank.parent.core.load_bundle(frozen), condition & (ds.field('trade_date') <= cutoff), prefix_path)
                prefix = pl.read_parquet(prefix_path).sort('trade_date', 'ts_code')
                assert prefix.equals(frame.filter(pl.col('trade_date') <= cutoff))
                batch = next(b for b in bank.parent.core.scanner(bank.KEYS + bank.parent.feature_names(), condition) if len(b))
                x = bank.parent.core.matrix(batch.slice(0, 131), bank.parent.feature_names())
                values = bank.predict_arrays(bank.parent.core.load_bundle(frozen), x)
                for size in (1, 80, 130):
                    assert np.array_equal(values[:size], bank.predict_arrays(bank.parent.core.load_bundle(frozen), x[:size]))
                frame.write_parquet(first)
                checks.append({'model': name, 'model_sha256': info['model_sha256'],
                    'raw_sha256': bank.sha(first), 'new_native_fits': 0,
                    'actual_full1599600_row_reload_bit_identical': True,
                    'actual_cold80_day_prefix_bit_identical': True,
                    'actual131_row_and1_80_130_prefix_bit_identical': True})
                for duplicate in (replay, prefix_path):
                    assert duplicate.resolve().is_relative_to(out.resolve())
                    duplicate.unlink()
                del frame, rebuilt, prefix, batch, x, values
                gc.collect()
            cache.reverify()
    except BaseException as error:
        failure = f'{type(error).__name__}: {error}'
        raise
    finally:
        bank.sha = original_sha
        if recorder.thread is not None:
            resources = recorder.finish()
        bank.dump(out / 'resource_summary.json', {'status': 'passed' if failure is None else 'failed',
            'failure': failure, 'actual_resources': resources, 'all_bindings_restored': True,
            'physical_resource_limit_established': False, 'test_labels_read': False}, immutable=True)
    bank.dump(out / 'verification.json', {'status': 'passed', 'checks': checks,
        'actual_virtual_final_artifacts': 6, 'new_native_fits': 0, 'reused_native_final_fits': 4,
        'all6_fullfuture_reload_and_cold80_controls_passed': len(checks) == 6,
        'input_sha256': inputs, 'resource_summary_sha256': bank.sha(out / 'resource_summary.json'),
        'complete_official_quality_and_adoption_still_pending': True,
        'test_labels_read': False, 'new_quality_scores': 0}, immutable=True)


if __name__ == '__main__':
    main()
