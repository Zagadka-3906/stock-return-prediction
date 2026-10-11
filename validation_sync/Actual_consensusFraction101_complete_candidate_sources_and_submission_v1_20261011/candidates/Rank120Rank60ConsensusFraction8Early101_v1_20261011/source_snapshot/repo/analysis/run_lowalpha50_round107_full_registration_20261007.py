"""Close low-alpha50 candidate confirmation, full ranking QA and main publication."""
from pathlib import Path
import os
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path[:0] = [str(ROOT), str(A)]
from run_dependency_queue_v3_20261006 import read, sha, create, owned
from hidden_windows_child_creation_20261006 import install
from handoff_joint_goss_round97_full_execution_20261006 import suspended_idle


def main():
    import psutil
    out = A / 'lowalpha50_round107_actual_registration_20261007'
    assert not out.exists()
    out.mkdir()
    for name in ('simplex_residual47_round106_full_registration_v5',
                 'lowalpha_huber_residual_scores50_evidence_publication'):
        service = A / 'service_owned_workflows_20261006' / name
        assert not owned(read(service / 'native_launch.json'))
        assert read(service / 'service_execution.json')['status'] == 'passed'
    while psutil.virtual_memory().available < 9 * 2**30:
        time.sleep(30)
    state = read(A / 'service_owned_dependency_queue_v4_20261006/state.json')
    assert not any(n.startswith('round') and owned(r) for n, r in state['activated_jobs'].items())
    assert read(A / 'lowalpha50_selected_candidate_reuse_confirmation_20261007.json')['status'] == (
        'passed_actual50_selected_scheme_full_validation_bits_all_metrics_graph_and_all_sealed_candidate_files_unchanged')
    from register_lowalpha50_round107_artifacts_20261007 import main as prepare
    protocol = prepare()
    folder = A / 'optimization_20261003_r107'
    pins = protocol['input_sha256']
    create(folder / 'frozen_before_actual_full_registration.json', {'at_local': time.strftime('%Y-%m-%dT%H:%M:%S'),
        'input_sha256': pins, 'registration_only': True, 'current_qualified_comparison_parent_round': 106,
        'original_selected_inference_and_all_parameter_bytes_preserved': True,
        'current_local92_CPU_scoring_and_original_GPU_training_untouched': True, 'test_labels_read': False})
    scratch = ROOT / 'tmp/lowalpha50_full107_20261007'
    scratch.mkdir(parents=True, exist_ok=True)
    for key in ('TEMP', 'TMP', 'TMPDIR', 'MPLCONFIGDIR'):
        os.environ[key] = str(scratch)
    import tempfile
    tempfile.tempdir = str(scratch)
    held, transport = [], []
    restore_children = install()
    restore_ranking = scope = None
    import publish_classifier_consensus_workflows_20261006 as helpers
    old_git = helpers.sync.git
    def retry_git(*args, **kwargs):
        for attempt in range(3):
            try:
                return old_git(*args, **kwargs)
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
        create(folder / 'actual_main7_idle_before_and_after_hold.json', idle)
        from win32_read_handle_hash_cache_with_filename_v2_20261006 import LockedReadHashCache
        scope = LockedReadHashCache(pins)
        scope.__enter__()
        from publish_explicit_parent_training_round_v2_20261005 import publish
        publish(107, '固定较低Huber阈值条件残差与集成', 'conditional_flag_residual_causal_checks.json',
            ['预定50项固定较低Huber阈值条件残差及集成官方比较'])
        from lossless_ranking_runtime_adapter_round107_20261007 import install as lossless
        restore_ranking = lossless(107)
        import build_all_model_rankings_20261003 as ranking
        import verify_all_model_rankings_20261003 as qa
        ranking.main()
        qa.main()
        scope.reverify()
        create(folder / 'provenance_scope_execution.json', {'status': 'passed',
            'at_local': time.strftime('%Y-%m-%dT%H:%M:%S'), 'input_sha256': pins,
            'initial_full_hash_and_Windows_read_share_only_locks': True,
            'final_full_rehash_after_actual_full_ranking_QA': True, 'sealed_input_files': len(pins),
            'cache_hits': scope.hits, 'nonsealed_paths_rehashed': scope.fresh_calls,
            'actual1599600_row_model_reload_and_cold80_candidate_proofs_preserved': True,
            'exact_existing_candidate_confirmed_by_all_validation_bits_all_metrics_and_parameters': True,
            'all_original_six_view_browser_and_candidate_manifest_QA_passed': True,
            'registered_previously_executed_scope_not_new_inference_or_scientific_freeze': True,
            'new_model_fits': 0, 'new_quality_scores_by_registration': 0, 'test_labels_read': False})
        scope.close()
        scope = None
        from publish_lowalpha50_round107_full_validation_20261007 import main as github
        helpers.sync.git = retry_git
        github()
        create(folder / 'full_registration_execution.json', {'status': 'passed',
            'at_local': time.strftime('%Y-%m-%dT%H:%M:%S'), 'existing_official_scores_registered': 50,
            'full_rankings_all_original_QA_and_main_publication_completed': True,
            'scientific_workers_suspended_stopped_or_restarted': 0,
            'new_quality_scores_by_registration': 0, 'new_inference_claimed': False,
            'global_goal_or_resource_exhaustion_claimed': False, 'test_labels_read': False})
    except BaseException as error:
        create(folder / 'full_registration_failure.json', {'status': 'failed_preserved_lowalpha50_full107_registration',
            'at_local': time.strftime('%Y-%m-%dT%H:%M:%S'), 'error': f'{type(error).__name__}: {error}'})
        raise
    finally:
        helpers.sync.git = old_git
        if scope is not None:
            scope.close()
        if restore_ranking is not None:
            restore_ranking()
        for process in reversed(held):
            if process.is_running():
                process.resume()
        create(folder / 'actual_hidden_registration_children.json', {'events': restore_children(),
            'scientific_workers_not_suspended_stopped_or_restarted': True})
        create(out / 'actual_transport_retries.json', {'attempts': transport, 'TLS_verification_unchanged': True})


if __name__ == '__main__':
    main()
