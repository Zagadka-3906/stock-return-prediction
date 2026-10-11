"""Register44 actual 全股票池CPU HGB scores, its sealed winner, complete QA23 and main."""
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
    out = A / 'CPU_FULL_HGB44_round113_actual_registration_v2_20261007'
    assert not out.exists()
    out.mkdir()
    for name in ('full_universe_HGB44_official_comparison_v2', 'cpu_full_universe_HGB24_scores_evidence_publication',
                 'CPU_FULL_HGB44_selected_candidate_sealing', 'classifier_consensus_round89_status_recovery_main_publication',
                 'CPU_HGB44_round112_full_registration'):
        service = A / 'service_owned_workflows_20261006' / name
        while not (service / 'native_launch.json').exists() or owned(read(service / 'native_launch.json')):
            time.sleep(15)
        assert read(service / 'service_execution.json')['status'] == 'passed'
    benchmark = A / 'service_owned_workflows_20261006/official_date_index_speed_benchmark'
    while owned(read(benchmark / 'native_launch.json')):
        time.sleep(15)
    while psutil.virtual_memory().available < 9 * 2**30:
        time.sleep(30)
    state = read(A / 'service_owned_dependency_queue_v4_20261006/state.json')
    assert not any(n.startswith('round') and owned(r) for n, r in state['activated_jobs'].items())
    from prepare_CPU_FULL_HGB44_round113_sources_v2_20261007 import main as prepare_sources
    prepare_sources()
    ready = read(A / 'CPU_FULL_HGB_residual44_selected_release_20261007/selected_candidate_ready_for_registration.json')
    assert ready['status'] == 'passed_actual44_selected_candidate_full_graph_and_metrics_and_source_bytes'
    from register_CPU_FULL_HGB44_round113_artifacts_20261007 import main as prepare
    protocol = prepare()
    folder = A / 'optimization_20261003_r113'
    pins = protocol['input_sha256']
    create(folder / 'frozen_before_actual_full_registration.json', {'at_local': time.strftime('%Y-%m-%dT%H:%M:%S'),
        'input_sha256': pins, 'registration_only': True, 'current_qualified_comparison_parent_round': 112,
        'original_selected_inference_and_all_parameter_bytes_preserved': True,
        'original_live_GPU_training_untouched': True, 'test_labels_read': False})
    scratch = ROOT / 'tmp/CPU_FULL_HGB44_full113_20261007'
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
        publish(113, '全股票池CPU直方图梯度回归与同日CDF融合', 'conditional_flag_residual_causal_checks.json',
            ['预定44项全股票池CPU直方图梯度回归及固定集成的官方比较'])
        from lossless_ranking_runtime_adapter_round113_20261007 import install as lossless
        restore_ranking = lossless(113)
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
        from publish_CPU_FULL_HGB44_round113_full_validation_20261007 import main as github
        helpers.sync.git = retry_git
        github()
        create(folder / 'full_registration_execution.json', {'status': 'passed',
            'at_local': time.strftime('%Y-%m-%dT%H:%M:%S'), 'existing_official_scores_registered': 44,
            'full_rankings_all_original_QA_and_main_publication_completed': True,
            'scientific_workers_suspended_stopped_or_restarted': 0,
            'new_quality_scores_by_registration': 0, 'new_inference_claimed_by_registration': False, 'selected_candidate_actual_new_inference': ready['new_inference_claimed'],
            'global_goal_or_resource_exhaustion_claimed': False, 'test_labels_read': False})
    except BaseException as error:
        create(folder / 'full_registration_failure.json', {'status': 'failed_preserved_CPU_FULL_HGB44_full113_registration',
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
