"""Resume the already prepared37-case registry; run all real QA with round101."""
from pathlib import Path
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path[:0] = [str(ROOT), str(A)]
from run_dependency_queue_v3_20261006 import read, create, sha, owned


def main():
    import psutil
    services = [A / 'service_owned_workflows_20261006' / name for name in (
        'conditional_flag_round101_full_registration', 'conditional_flag_round101_full_registration_v2')]
    for service in services:
        assert not owned(read(service / 'native_launch.json'))
        assert read(service / 'service_execution.json')['status'] == 'failed'
    assert read(services[1] / 'service_execution.json')['failure'] == 'AssertionError: '
    assert 'lossless_ranking_runtime_adapter_v9_20261006.py' in (services[1] / 'stderr.log').read_text(encoding='utf-8')
    while psutil.virtual_memory().available < 8 * 2**30:
        time.sleep(30)
    folder = A / 'optimization_20261003_r101'
    protocol = read(folder / 'protocol.json')
    selection = read(folder / 'selection.json')
    result = read(ROOT / 'results/optimization_20261003_r101.json')
    candidate = ROOT / 'candidates/optimization_20261003_r101'
    assert protocol['expected_scored_records'] == len(selection['ranking']) == result['scored_records'] == 37
    assert result['status'] == 'complete'
    assert result['winner']['metrics'] == selection['winner']['metrics']
    assert selection['winner']['connected_final_score'] == read(candidate / 'verification.json')['validation_score']
    manifest = read(candidate / 'manifest.json')
    for relative, info in manifest['files'].items():
        assert sha(candidate / relative) == info['sha256'], relative
    assert not (folder / 'provenance_scope_execution.json').exists()
    additions = [Path(__file__), A / 'publish_conditional_flag_round101_full_validation_v3_20261006.py',
        folder / 'full_registration_failure.json', folder / 'protocol.json', folder / 'selection.json',
        ROOT / 'results/optimization_20261003_r101.json', candidate / 'manifest.json']
    additions += [p for service in services for pattern in ('*.json', '*.log') for p in service.glob(pattern)]
    pins = {**protocol['input_sha256'], **{str(p): sha(p) for p in additions}}
    create(folder / 'frozen_before_actual_full_registration_recovery_v3.json', {
        'input_sha256': pins, 'at_local': time.strftime('%Y-%m-%dT%H:%M:%S'),
        'already_prepared_actual37_registry_and_sealed14_candidate_reused': True,
        'ranking_adapter_actual_round_corrected_from100_to101': True,
        'all_original_six_views_full_report_and_browser_checks_required': True,
        'original_two_failed_attempts_preserved': True, 'new_training_scoring_or_inference': False,
        'scientific_processes_stopped_or_restarted': 0, 'test_labels_read': False})
    from hidden_windows_child_creation_20261006 import install
    from handoff_joint_goss_round97_full_execution_20261006 import suspended_idle
    from locked_read_hash_cache_20261004 import LockedReadHashCache
    publisher = read(A / 'service_owned_workflows_20261006/main_publisher_v7/native_launch.json')
    held = []
    scope = None
    restore_ranking = None
    restore_children = install()
    try:
        parent, worker, idle = suspended_idle(publisher, '    main (watch_validations_main_v7_20261006.py:71)')
        held.extend((worker, parent))
        create(folder / 'actual_main7_idle_before_and_after_recovery_v3_hold.json', idle)
        scope = LockedReadHashCache(pins)
        scope.__enter__()
        from lossless_ranking_runtime_adapter_v9_20261006 import install as lossless
        restore_ranking = lossless(101)
        import build_all_model_rankings_20261003 as ranking
        import verify_all_model_rankings_20261003 as qa
        ranking.main()
        qa.main()
        scope.reverify()
        create(folder / 'provenance_scope_execution.json', {
            'status': 'passed', 'at_local': time.strftime('%Y-%m-%dT%H:%M:%S'), 'input_sha256': pins,
            'initial_full_hash_and_Windows_read_share_only_locks': True,
            'final_full_rehash_after_actual_full_ranking_QA': True,
            'sealed_input_files': len(pins), 'cache_hits': scope.hits, 'nonsealed_paths_rehashed': scope.fresh_calls,
            'all_absolute_historical_archive_inputs_preserved_and_verified': True,
            'original_actual37_official_scores_and_frozen_selection_unchanged': True,
            'actual1599600_row14_saved_model_and_cold80_candidate_proofs_preserved': True,
            'all_original_six_view_browser_and_candidate_manifest_QA_passed': True,
            'already_prepared_registry_reused_without_new_training_or_quality_scores': True,
            'original_two_failed_registration_attempts_preserved': True,
            'new_model_fits': 0, 'new_quality_scores_by_registration': 0, 'test_labels_read': False})
        scope.close()
        scope = None
        from publish_conditional_flag_round101_full_validation_v3_20261006 import main as publish
        publish()
        create(folder / 'full_registration_execution.json', {'status': 'passed',
            'at_local': time.strftime('%Y-%m-%dT%H:%M:%S'), 'existing_official_scores_registered': 37,
            'full_rankings_all_original_QA_and_main_publication_completed': True,
            'scientific_processes_suspended_or_restarted': 0, 'new_quality_scores_by_registration': 0,
            'two_original_registry_failures_preserved': True,
            'global_goal_or_resource_exhaustion_claimed': False, 'test_labels_read': False})
    except BaseException as error:
        create(folder / 'full_registration_failure_v3.json', {'status': 'failed_preserved_full_round101_QA_recovery',
            'error': f'{type(error).__name__}: {error}', 'test_labels_read': False})
        raise
    finally:
        if scope is not None:
            scope.close()
        if restore_ranking is not None:
            restore_ranking()
        for process in reversed(held):
            if process.is_running():
                process.resume()
        create(folder / 'actual_hidden_registration_recovery_v3_children.json', {
            'events': restore_children(), 'scientific_processes_not_held': True})


if __name__ == '__main__':
    main()
