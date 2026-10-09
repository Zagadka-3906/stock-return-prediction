"""Close all original scientific, candidate, full ranking and main publication gates."""
from pathlib import Path
import json
import os
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path[:0] = [str(ROOT), str(A)]
from run_dependency_queue_v3_20261006 import read, sha, create, owned
from hidden_windows_child_creation_20261006 import install


def main():
    import psutil
    assert psutil.virtual_memory().available >= 8 * 2**30
    scratch = ROOT / 'tmp/cohort_round103_registration_20261006'
    scratch.mkdir(parents=True, exist_ok=True)
    for name in ('TMP', 'TEMP', 'TMPDIR', 'MPLCONFIGDIR'):
        os.environ[name] = str(scratch)
    import tempfile
    tempfile.tempdir = str(scratch)
    from register_residual_extrapolation43_round103_artifacts_20261006 import main as prepare
    protocol = prepare()
    folder = A / 'optimization_20261003_r103'
    from handoff_joint_goss_round97_full_execution_20261006 import suspended_idle
    publisher = read(A / 'service_owned_workflows_20261006/main_publisher_v7/native_launch.json')
    assert owned(publisher)
    queue = read(A / 'service_owned_dependency_queue_v4_20261006/state.json')
    live = {name: row for name, row in queue['activated_jobs'].items() if name.startswith('round') and owned(row)}
    wide = read(A / 'service_owned_workflows_20261006/neural16384_annual/native_launch.json')
    if owned(wide):
        live['neural16384_annual'] = wide
    create(folder / 'frozen_before_actual_full_registration.json', {'input_sha256': protocol['input_sha256'],
        'original_scientific_workers_to_preserve': live, 'new_scoring_or_training': False,
        'original_pilot_and_selected_candidate_proofs_already_actual': True, 'test_labels_read': False})
    suspended = []
    restore_children = install()
    restore_ranking = None
    scope = None
    try:
        parent, worker, idle = suspended_idle(publisher, '    main (watch_validations_main_v7_20261006.py:71)')
        suspended.extend((worker, parent))
        create(folder / 'actual_main7_idle_before_and_after_hold.json', idle)
        from locked_read_hash_cache_20261004 import LockedReadHashCache
        scope = LockedReadHashCache(protocol['input_sha256'])
        scope.__enter__()
        # Every original pinned input, source and saved model byte remains read
        # locked through registration and full QA, then is fully rehashed.
        from publish_explicit_parent_training_round_v2_20261005 import publish
        publish(103, '成熟历史标签的涨停条件残差原生模型与等权集成', 'conditional_flag_residual_causal_checks.json', ['预定43项条件残差放大系数及集成官方比较'])
        from lossless_ranking_runtime_adapter_v11_20261006 import install as lossless
        restore_ranking = lossless(103)
        import build_all_model_rankings_20261003 as ranking
        import verify_all_model_rankings_20261003 as qa
        ranking.main()
        qa.main()
        scope.reverify()
        create(folder / 'provenance_scope_execution.json', {'status': 'passed',
            'at_local': time.strftime('%Y-%m-%dT%H:%M:%S'), 'input_sha256': protocol['input_sha256'],
            'initial_full_hash_and_Windows_read_share_only_locks': True,
            'final_full_rehash_after_actual_full_ranking_QA': True,
            'sealed_input_files': len(protocol['input_sha256']), 'cache_hits': scope.hits,
            'nonsealed_paths_rehashed': scope.fresh_calls,
            'original_actual_official37_scores_and_frozen_selection_unchanged': True,
            'actual1599600_row_model_reload_and_cold80_candidate_proofs_preserved': True,
            'all_original_six_view_browser_and_candidate_manifest_QA_passed': True,
            'registered_previously_executed_scope_not_a_new_scientific_freeze': True,
            'new_model_fits': 0, 'new_quality_scores_by_registration': 0, 'test_labels_read': False})
        scope.close()
        scope = None
        from publish_residual_extrapolation43_round103_full_validation_20261006 import main as github
        github()
        create(folder / 'full_registration_execution.json', {'status': 'passed',
            'at_local': time.strftime('%Y-%m-%dT%H:%M:%S'), 'existing_official_scores_registered': 43,
            'full_rankings_and_all_original_QA_and_main_publication_completed': True,
            'scientific_processes_suspended_or_restarted': 0, 'new_quality_scores_by_registration': 0,
            'global_goal_or_resource_exhaustion_claimed': False, 'test_labels_read': False})
    except BaseException as error:
        if not (folder / 'full_registration_failure.json').exists():
            create(folder / 'full_registration_failure.json', {'status': 'failed_preserved_full_round103_registration',
                'error': f'{type(error).__name__}: {error}', 'test_labels_read': False})
        raise
    finally:
        if scope is not None:
            scope.close()
        if restore_ranking is not None:
            restore_ranking()
        for p in reversed(suspended):
            if p.is_running():
                p.resume()
        create(folder / 'actual_hidden_registration_children.json', {'events': restore_children(),
            'only_exact_idle_main_publisher_temporarily_held': True,
            'scientific_training_and_scoring_processes_not_held': True})


if __name__ == '__main__':
    main()
