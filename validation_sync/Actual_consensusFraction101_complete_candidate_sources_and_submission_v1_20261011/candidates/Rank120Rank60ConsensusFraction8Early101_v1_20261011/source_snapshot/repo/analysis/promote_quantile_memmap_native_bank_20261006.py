"""Verify real24-fit closure, then expose byte-identical artifacts to the fixed grids."""
from pathlib import Path
import hashlib
import json
import shutil
import sys
import time

import psutil

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path[:0] = [str(ROOT), str(A)]
SOURCE = A / 'quantile_tree_memmap_complete_bank_20261006'
FUTURE = A / 'quantile_tree_memmap_future_qa_20261006'
OUT = A / 'quantile_tree_memmap_native_promotion_20261006'


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8-sig'))


def sha(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def create(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('x', encoding='utf-8') as stream:
        json.dump(value, stream, ensure_ascii=False, indent=2)
        stream.write('\n')


def main():
    from run_dependency_queue_v3_20261006 import owned
    service = A / 'service_owned_workflows_20261006/quantile_tree_memmap_complete_workflow'
    assert not OUT.exists()
    OUT.mkdir()
    while not (service / 'service_execution.json').exists():
        assert owned(read(service / 'native_launch.json')), 'Full native worker disappeared without a terminal record.'
        time.sleep(15)
    assert read(service / 'service_execution.json')['status'] == 'passed'
    while owned(read(service / 'native_launch.json')):
        time.sleep(.2)
    receipt = A / 'quantile_tree_memmap_complete_bank_github_20261006/receipt.json'
    while not receipt.exists():
        publication = A / 'service_owned_workflows_20261006/quantile_tree_memmap_complete_publication'
        assert owned(read(publication / 'native_launch.json')), 'Full native publication stopped without a verified receipt.'
        time.sleep(15)
    assert read(receipt)['status'] == 'pushed_actual_controls_main_only'
    assert read(receipt)['control_status'] == 'passed' and read(receipt)['raw_git_blobs_verified'] > 0
    audit, proof = read(SOURCE / 'oof_audit.json'), read(FUTURE / 'verification.json')
    assert audit['status'] == proof['status'] == 'passed'
    assert audit['actual_annual_fits'] == audit['actual300_round_complete_models'] == 20
    assert proof['actual_full_final_fits'] == 4 and proof['new_native_fits_by_this_verifier'] == 0
    assert read(SOURCE / 'training_execution_scope.json')['status'] == read(FUTURE / 'execution_scope.json')['status'] == 'passed'
    assert len(proof['checks']) == 4
    storage = read(A / 'quantile_tree_storage_20261006.json')
    destination = Path(storage['output_directory']).resolve()
    target_future = A / 'quantile_tree_future_qa_20261006'
    assert destination.is_relative_to(A) and destination != SOURCE and destination.drive.upper() == 'D:'
    assert not target_future.exists()
    assert not destination.exists() or not list(destination.iterdir()), 'Preserve any prior native artifacts.'
    # Stop only the exact zero-fit scheduling controllers. Their original files
    # remain; an administrative supersession never invents a passed execution.
    stopped = {}
    for name in ('quantile_tree_full_workflow', 'quantile_tree_quality_queue'):
        folder = A / f'service_owned_workflows_20261006/{name}'
        row = read(folder / 'native_launch.json')
        assert owned(row)
        parent, worker = psutil.Process(row['pid']), psutil.Process(row['owned_worker_pid'])
        assert parent.create_time() == row['owned_parent_creation_time']
        assert not worker.children(recursive=True)
        if name == 'quantile_tree_full_workflow':
            state = read(A / 'quantile_tree_native_full_workflow_20261006/state.json')
            assert state['actual_new_full_annual_fits'] == state['actual_new_full_final_fits'] == 0
        else:
            state = read(A / 'quantile_tree_quality_queue_20261006/state.json')
            assert state['actual_quality_records_completed'] == 0 and not state.get('current_quality_job')
            replacement = read(A / 'service_owned_workflows_20261006/quantile_tree_quality_queue_v2/native_launch.json')
            assert owned(replacement)
        stopped[name] = {'ownership': row, 'last_actual_zero_work_state': state,
            'reason': 'Actual same-scope24 native fit and future verification completed through measured exact-memory backend.'}
        worker.terminate()
        worker.wait(timeout=10)
        if parent.is_running():
            parent.terminate()
            parent.wait(timeout=10)
        assert not owned(row)
    create(OUT / 'superseded_zero_fit_controllers.json', {'status': 'deliberately_superseded_after_actual_full24_closure',
        'controllers': stopped, 'no_passed_original_controller_execution_fabricated': True,
        'new_native_fits': 0, 'new_quality_scores': 0})
    from locked_read_hash_cache_20261004 import LockedReadHashCache
    source_files = [p for p in SOURCE.rglob('*') if p.is_file() and p.suffix in ('.json', '.jsonl', '.joblib', '.parquet')]
    source_files += [p for p in FUTURE.rglob('*') if p.is_file()]
    pins = [Path(__file__), receipt, service / 'service_execution.json', A / 'quantile_tree_storage_20261006.json',
        A / 'quantile_tree_quality_queue_20261006/plan.json', A / 'quantile_tree_quality_complete_plan_v2_20261006.json',
        A / 'quantile_tree_model_sources_20261006.py', A / 'train_quantile_tree_bank_20261006.py',
        A / 'train_quantile_tree_memmap_bank_20261006.py', A / 'run_quantile_tree_memmap_full_workflow_20261006.py',
        A / 'verify_quantile_tree_memmap_full_future_20261006.py']
    bindings = {str(p.resolve()): sha(p) for p in dict.fromkeys([*source_files, *pins])}
    create(OUT / 'frozen_before_artifact_exposure.json', {'input_sha256': bindings,
        'expected_same_actual_annual_fits': 20, 'expected_same_actual_final_fits': 4,
        'copies_not_additional_fits': True, 'original198_grid_and90_91_parents_unchanged': True})
    copied = []
    with LockedReadHashCache(bindings) as cache:
        for name, cfg in read(SOURCE / 'protocol.json')['configurations'].items():
            assert audit['entire_original_five_year_prediction_coverage'][name]['rows'] == 5635800
            for year in range(2020, 2026):
                info = read(SOURCE / name / f'info_{year}.json')
                assert info['status'] == 'passed' and info['actual_native_boosting_iterations'] == 300
                assert info['configuration'] == cfg and info['native_objective'] == 'quantile'
                reference_name = 'rank_ridge_l01' if cfg['target'] == 'y_rank' else 'return_ridge_l01'
                reference = read(A / f'linear_bank_20261003/{reference_name}/info_{year}.json')['training_meta']
                assert info['training_meta'] == reference
                assert cache.sha(SOURCE / name / f'model_{year}.joblib') == info['model_sha256']
                if year < 2025:
                    assert cache.sha(SOURCE / name / f'raw_{year}.parquet') == info['prediction_sha256']
        for base, target, files in ((SOURCE, destination, [p for p in source_files if p.is_relative_to(SOURCE)]),
                                    (FUTURE, target_future, [p for p in source_files if p.is_relative_to(FUTURE)])):
            for source in files:
                target_path = target / source.relative_to(base)
                target_path.parent.mkdir(parents=True, exist_ok=True)
                assert not target_path.exists()
                shutil.copyfile(source, target_path)
                digest = cache.sha(source)
                assert sha(target_path) == digest
                copied.append({'source': str(source), 'destination': str(target_path), 'sha256': digest,
                               'bytes': target_path.stat().st_size})
        cache.reverify()
    create(OUT / 'verification.json', {'status': 'passed', 'at_local': time.strftime('%Y-%m-%dT%H:%M:%S'),
        'actual_annual_native_fits': 20, 'actual_final_native_fits': 4,
        'actual_native_fits_by_promotion': 0, 'copied_artifacts': copied,
        'complete_native_scope_and_all1599600_future_checks_actually_closed_and_main_published': True,
        'original_quality_model_routes_now_resolve_identical_original_matched_configs_and_bytes': True,
        'original_frozen_scientific_sources_and_full198_grid_and_explicit_parents_unchanged': True,
        'native_source_service_execution': read(service / 'service_execution.json'),
        'native_main_receipt': read(receipt), 'input_sha256': bindings,
        'complete198_official_quality_and_causal_candidates_and_rankings_still_pending': True,
        'new_quality_scores': 0, 'test_labels_read': False, 'global_resource_boundary_established': False})


if __name__ == '__main__':
    main()
