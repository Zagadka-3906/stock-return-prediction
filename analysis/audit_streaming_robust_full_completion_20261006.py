"""Close all four native banks after 24 genuine fits and full independent inference."""
from pathlib import Path
import hashlib
import json
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path.insert(0, str(A))
OUT = A / 'streaming_robust_full_completion_audit_20261006'


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8-sig'))


def sha(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def create(path, value):
    with path.open('x', encoding='utf-8') as stream:
        json.dump(value, stream, ensure_ascii=False, indent=2)
        stream.write('\n')


def main():
    import psutil
    import streaming_robust_regression_20261005 as core
    from locked_read_hash_cache_20261004 import LockedReadHashCache
    bank = core.OUT
    future = A / 'streaming_robust_regression_future_qa_20261005'
    recovered = A / 'system_reboot_workflow_recovery_20261006/robust_future'
    assert read(recovered / 'execution.json')['status'] == 'passed'
    launch = read(recovered / 'launch.json')
    worker = psutil.Process(launch['owned_worker_pid']) if psutil.pid_exists(launch['owned_worker_pid']) else None
    if worker is not None:
        assert abs(worker.create_time() - launch['owned_worker_creation_time']) > 1e-5, 'Original final workflow still live.'
    annual_path = A / 'streaming_robust_actual_annual_completion_audit_20261006/verification.json'
    annual = read(annual_path)
    assert annual['actual_full_annual_fits'] == 20
    assert annual['all20_actual_estimator_counters_and_physical_batch_passes_verified']
    native = read(future / 'verification.json')
    resources = read(future / 'resource_summary.json')
    assert native['status'] == resources['status'] == 'passed'
    assert native['actual_fulltraining_fits'] == 4 and native['all4_model_fullfuture_reload_and_cold80_controls_passed']
    assert native['complete_official_quality_and_adoption_still_pending']
    assert resources['failure'] is None and resources['all_hash_and_resource_bindings_restored']
    assert not native['test_labels_read'] and not resources['test_labels_read']
    assert not resources['physical_resource_limit_established']
    checks = {row['model']: row for row in native['checks']}
    assert set(checks) == set(core.CONFIGS)
    proofs, paths = {}, [Path(__file__), annual_path, future / 'verification.json',
        future / 'resource_summary.json', recovered / 'execution.json', recovered / 'launch.json',
        bank / 'actual_native_fit_measurements.jsonl', A / 'audit_streaming_robust_final_model_20261006.py']
    bindings = {}

    def bind(values):
        for path, digest in values.items():
            key = str(Path(path).resolve())
            assert key not in bindings or bindings[key] == digest, key
            bindings[key] = digest

    bind(annual['input_sha256'])
    bind(native['input_sha256'])
    for name, cfg in core.CONFIGS.items():
        folder = A / 'streaming_robust_final_native_audit_20261006' / name
        path = folder / 'verification.json'
        proof = read(path)
        assert proof['status'] == 'passed_actual_full_final_fit_and_independent_all1599600_native_predictions'
        assert proof['model'] == name and proof['configuration'] == cfg
        assert proof['actual_completed_epochs'] == 32 and proof['mature_training_rows'] == 6754006
        assert proof['actual_native_sample_counter'] == 1 + 32 * proof['mature_training_rows']
        assert proof['all_future_rows_independently_checked'] == 1599600
        assert proof['future_days'] == 344 and proof['future_codes'] == 4650
        assert proof['independent_full_SGDRegressor_predict_max_abs_error'] < 1e-12
        assert proof['native_fullfuture_price_invalid_sentinel_exact']
        assert proof['actual_saved_reload_and131_row_prefix_controls_passed']
        assert proof['mature_target_units_scaling_and_physical_train_batch_passes_verified']
        assert not proof['test_labels_read'] and proof['new_quality_scores'] == proof['new_native_fits'] == 0
        original = checks[name]
        assert original['actual_full1599600_row_reload_bit_identical']
        assert original['actual_cold80_day_prefix_bit_identical']
        assert original['actual_native131_row_and1_80_130_prefix_bit_identical']
        assert proof['input_sha256'][str((future / f'{name}.joblib').resolve())] == original['model_sha256']
        assert proof['input_sha256'][str((future / f'{name}_raw.parquet').resolve())] == original['raw_sha256']
        bind(proof['input_sha256'])
        paths += [path, folder / 'frozen_before_inspection.json']
        proofs[name] = proof
    bind({str(path.resolve()): sha(path) for path in paths})
    assert not OUT.exists()
    OUT.mkdir()
    create(OUT / 'frozen_before_inspection.json', {'input_sha256': bindings,
        'actual_required_native_annual_fits': 20, 'actual_required_native_final_fits': 4,
        'full_future_oracle_rows_each': 1599600, 'official_quality_still_pending': True})
    try:
        with LockedReadHashCache(bindings):
            measurements = [json.loads(line) for line in (bank / 'actual_native_fit_measurements.jsonl').read_text(encoding='utf-8').splitlines() if line]
            assert len(measurements) == 24
            indexed = {(row['model'], row['year']): row for row in measurements}
            assert set(indexed) == {(name, year) for name in core.CONFIGS for year in range(2020, 2026)}
            for row in indexed.values():
                assert row['status'] == 'completed_full_original32passes' and row['actual_completed_epochs'] == 32
                assert row['actual_rows_in_each_epoch'] == [row['actual_training_rows']] * 32
                assert row['actual_native_sample_counter'] == 1 + 32 * row['actual_training_rows']
                assert not row['test_data_read']
            for name, proof in proofs.items():
                row = indexed[(name, 2025)]
                assert row['actual_training_rows'] == proof['mature_training_rows']
                assert row['actual_partial_fit_calls'] == proof['actual_partial_fit_calls']
                assert row['target_scaling'] == proof['target_scaling']
        create(OUT / 'verification.json', {'status': 'passed_all24_actual_full32pass_native_fits_and4_independent_fullfuture_oracles',
            'at_local': time.strftime('%Y-%m-%dT%H:%M:%S'), 'configurations': core.CONFIGS,
            'actual_annual_fits': 20, 'actual_final_fits': 4, 'actual_full_data_passes': 24 * 32,
            'independent_future_rows_checked': 4 * 1599600,
            'all4_future_rows_days_codes': [1599600, 344, 4650],
            'maximum_independent_fullfuture_oracle_error': max(row['independent_full_SGDRegressor_predict_max_abs_error'] for row in proofs.values()),
            'all_original_full_reload_and_real_cold80_controls_passed': True,
            'all_mature_feature_target_scaling_native_counters_and_invalid_price_controls_passed': True,
            'all_bound_inputs_independently_full_rehashed_and_read_locked': True,
            'native_final_workflow_authoritatively_completed': True,
            'complete_official_quality_freeze_causality_candidate_inference_and_board_still_required': True,
            'physical_resource_boundary_established': False, 'input_sha256': bindings,
            'new_native_fits_by_audit': 0, 'new_quality_scores': 0, 'test_labels_read': False})
        print(json.dumps({'status': 'passed_full24_fit_robust_native_completion_audit',
            'actual_final_fits': 4, 'independent_future_rows_checked': 6398400}, ensure_ascii=False), flush=True)
    except BaseException as error:
        create(OUT / 'failure.json', {'status': 'failed_preserved_full_completion_inspection',
            'error': f'{type(error).__name__}: {error}', 'at_local': time.strftime('%Y-%m-%dT%H:%M:%S')})
        raise


if __name__ == '__main__':
    main()
