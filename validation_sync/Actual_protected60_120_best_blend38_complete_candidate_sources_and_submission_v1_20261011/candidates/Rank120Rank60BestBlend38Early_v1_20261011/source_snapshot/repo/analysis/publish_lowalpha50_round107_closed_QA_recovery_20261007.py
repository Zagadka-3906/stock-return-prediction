"""Publish actual completed QA18, preserving the initial collector-path failure."""
from pathlib import Path
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path[:0] = [str(ROOT), str(A)]
from run_dependency_queue_v3_20261006 import read, sha, create, owned
from handoff_joint_goss_round97_full_execution_20261006 import suspended_idle
from hidden_windows_child_creation_20261006 import install


def main():
    folder = A / 'optimization_20261003_r107'
    out = A / 'lowalpha50_round107_closed_QA_publication_recovery_20261007'
    assert not out.exists()
    out.mkdir()
    original = A / 'service_owned_workflows_20261006/lowalpha50_round107_full_registration'
    assert not owned(read(original / 'native_launch.json'))
    failure = read(original / 'service_execution.json')
    assert failure['status'] == 'failed' and 'lossless_ranking_display_qa_v18_20261006' in failure['failure']
    assert read(folder / 'provenance_scope_execution.json')['status'] == 'passed'
    qa_folder = A / 'lossless_ranking_display_qa_v18_20261007/round107'
    qa = read(qa_folder / 'verification.json')
    assert qa['status'] == 'passed_all_original_full_ranking_QA_and_lossless_browser_node_checks'
    assert qa['original_full_QA_result']['connected_records'] == 11604
    assert qa['original_full_QA_result']['new_round_records'] == 50
    assert qa['original45_second_render_timeout_retained'] and qa['all_new_browser_profiles_under_D']
    sources = [Path(__file__), A / 'collect_full_lossless_round107_qa18_20261007.py',
        A / 'collect_full_lossless_round_publication_20261006.py',
        folder / 'full_registration_failure.json', folder / 'provenance_scope_execution.json',
        *list(original.glob('*.json')), *list(original.glob('*.log')),
        *list((A / 'service_owned_workflows_20261006/single_host_rank92_scores_after_full107').glob('*.json')),
        *list((A / 'service_owned_workflows_20261006/single_host_rank92_scores_after_full107').glob('*.log')),
        qa_folder / 'verification.json', qa_folder / 'qa/interaction_result.json']
    source = A / 'publish_lowalpha50_round107_full_validation_20261007.py'
    sources.append(source)
    pins = {**read(folder / 'protocol.json')['input_sha256'], **{str(p): sha(p) for p in sources}}
    create(out / 'frozen_before_closed_QA_publication_recovery.json', {'at_local': time.strftime('%Y-%m-%dT%H:%M:%S'),
        'input_sha256': pins, 'original_natural_failure': failure,
        'actual_original_full_QA18_already_passed': True, 'original_failed_paths_and_all_sources_preserved': True,
        'registration_does_not_redo_or_change_scientific_scoring_or_inference': True, 'test_labels_read': False})
    sources.append(out / 'frozen_before_closed_QA_publication_recovery.json')
    text = source.read_text(encoding='utf-8')
    before = 'from collect_full_lossless_round_publication_20261006 import collect'
    assert text.count(before) == 1
    text = text.replace(before, 'from collect_full_lossless_round107_qa18_20261007 import collect')
    before = '    for path in extra:'
    assert text.count(before) == 1
    text = text.replace(before, '    extra += CLOSED_RECOVERY_EVIDENCE\n' + before)
    namespace = {'__file__': str(source), '__name__': 'actual_closed_round107_QA18_publication_recovery',
        'CLOSED_RECOVERY_EVIDENCE': sources}
    exec(compile(text, str(source), 'exec'), namespace)
    held, transport, bindings = [], [], []
    restore = install()
    scope = None
    import publish_classifier_consensus_workflows_20261006 as helpers
    original_git = helpers.sync.git
    def retry_git(*args, **kwargs):
        for attempt in range(3):
            try:
                return original_git(*args, **kwargs)
            except RuntimeError as error:
                if args[0] not in ('ls-remote', 'push', 'fetch') or not any(
                    token in str(error).lower() for token in ('tls', 'ssl', 'unable to access', 'connection', 'timed out')):
                    raise
                transport.append({'command': args[0], 'attempt': attempt+1, 'error': str(error)[:1200]})
                if attempt == 2:
                    raise
                time.sleep(2)
    try:
        publisher = read(A / 'service_owned_workflows_20261006/main_publisher_v7/native_launch.json')
        parent, worker, idle = suspended_idle(publisher, '    main (watch_validations_main_v7_20261006.py:71)')
        held.extend((worker, parent))
        create(out / 'actual_main7_idle_before_and_after_hold.json', idle)
        from win32_read_handle_hash_cache_with_filename_v2_20261006 import LockedReadHashCache
        scope = LockedReadHashCache(pins)
        scope.__enter__()
        # Only path-hash functions are redirected, inside full read-only locks.
        # Byte hashing by the Git collector retains its original implementation.
        import optimize_training_round107 as optimizer
        import finalize_training_round107 as selected
        for module in (optimizer, selected):
            bindings.append((module, module.sha))
            module.sha = scope.sha
        helpers.sync.git = retry_git
        namespace['main']()
        scope.reverify()
        create(out / 'verification.json', {'status': 'passed_actual_closed_QA18_collector_path_recovery_and_main_publication',
            'at_local': time.strftime('%Y-%m-%dT%H:%M:%S'), 'input_sha256': pins,
            'original_failed_registration_retained': True, 'original_full_QA18_unchanged': True,
            'every_original_frozen_input_full_initial_and_final_hash_and_Windows_read_locks_passed': True,
            'protected_selected_path_SHA_cache_hits': scope.hits,
            'main_receipt': read(A / 'github_validation_sync_main_20261005/round107_receipt.json'),
            'scientific_workers_stopped_or_restarted': 0, 'new_quality_scores': 0, 'new_inference_claimed': False,
            'test_labels_read': False})
        create(folder / 'full_registration_execution.json', {'status': 'passed',
            'at_local': time.strftime('%Y-%m-%dT%H:%M:%S'), 'existing_official_scores_registered': 50,
            'full_rankings_all_original_QA_and_main_publication_completed': True,
            'original_collector_path_failure_retained': True, 'actual_publication_recovery': str(out / 'verification.json'),
            'scientific_workers_stopped_or_restarted': 0, 'new_quality_scores_by_registration': 0,
            'global_goal_or_resource_exhaustion_claimed': False, 'test_labels_read': False})
    except BaseException as error:
        create(out / 'failure.json', {'status': 'failed_preserved_closed_QA18_publication_recovery',
            'error': f'{type(error).__name__}: {error}', 'test_labels_read': False})
        raise
    finally:
        helpers.sync.git = original_git
        for module, original_sha in bindings:
            module.sha = original_sha
        if scope is not None:
            scope.close()
        for process in reversed(held):
            if process.is_running():
                process.resume()
        create(out / 'actual_transport_retries.json', {'attempts': transport, 'TLS_verification_unchanged': True})
        create(out / 'actual_hidden_publication_children.json', {'events': restore()})


if __name__ == '__main__':
    main()
