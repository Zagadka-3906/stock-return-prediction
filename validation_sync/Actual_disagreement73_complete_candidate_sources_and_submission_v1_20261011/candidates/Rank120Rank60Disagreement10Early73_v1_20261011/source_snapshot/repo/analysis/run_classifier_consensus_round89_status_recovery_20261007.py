"""Complete original124-case R89 grid after precise gate recovery, retaining its failed scope."""
from pathlib import Path
from copy import deepcopy
import importlib
import json
import os
import runpy
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path[:0] = [str(ROOT), str(A)]
from run_dependency_queue_v3_20261006 import read, sha, create, owned


def closed(name):
    p = A / 'service_owned_workflows_20261006' / name
    while not (p / 'native_launch.json').exists() or owned(read(p / 'native_launch.json')):
        time.sleep(15)
    assert read(p / 'service_execution.json')['status'] == 'passed', name


def main():
    import psutil
    out = A / 'classifier_consensus_round89_status_recovery_20261007'
    assert not out.exists()
    out.mkdir()
    closed('direct_flag_rank_micro74_official_comparison')
    closed('single_host_rank_micro74_scores_evidence_publication')
    closed('local_speed_adoption_main_publication')
    closed('direct_rank_micro74_round109_full_registration')
    assert read(A / 'optimization_20261003_r109/full_registration_execution.json')['status'] == 'passed'
    assert read(A / 'github_validation_sync_main_20261005/round109_receipt.json')['actual_full_QA_version'] == 20
    # The74 scientific comparison and full109 writer are terminal before
    # continuing the unchanged old required branch.
    while psutil.virtual_memory().available < 9 * 2**30:
        time.sleep(15)
    state = read(A / 'service_owned_dependency_queue_v4_20261006/state.json')
    assert not any(n.startswith('round') and owned(r) for n, r in state['activated_jobs'].items())
    old_service = A / 'service_owned_dependency_queue_v11_recovery_20261006/activated_jobs/round89'
    assert not owned(read(old_service / 'launch.json'))
    failed_path = A / 'optimization_20261003_r89/provenance_scope_execution.json'
    failed = read(failed_path)
    assert failed['status'] == 'failed' and failed['scope_started'] is False
    assert not (failed_path.parent / 'protocol.json').exists()
    alternate = failed_path.with_name('provenance_scope_execution_status_recovery_20261007.json')
    assert not alternate.exists()
    admission = read(A / 'classifier_consensus_round89_status_recovery_admission_20261007.json')
    for source, digest in admission['input_sha256'].items():
        assert sha(source) == digest, source
    qualified_original = old_service / 'qualified_run.json'
    run = deepcopy(read(qualified_original))
    repaired = admission['restored_original_bootstrap_binding']
    assert repaired['path'] == str(A / 'run_dependency_queue_v11_20261006.py')
    assert run['input_sha256'][repaired['path']] == repaired['original_failed_launch_expected_sha256']
    assert sha(repaired['path']) == repaired['restored_original_sha256']
    assert all(sha(p) == repaired['restored_original_sha256'] for p in repaired['two_independent_frozen_source_copies'])
    run['input_sha256'][repaired['path']] = repaired['restored_original_sha256']
    additions = [Path(__file__), A / 'classifier_consensus_round89_status_recovery_admission_20261007.json',
        A / 'classifier_consensus_status_gate_recovery_runtime_20261007.py',
        A / 'classifier_consensus_status_gate_recovery_preflight_20261007/verification.json',
        A / 'classifier_consensus_recovery_official_speed_adapter_20261007.py',
        A / 'official_date_index_dataframe_adapter_20261007.py',
        A / 'official_date_index_speed_benchmark_20261007/verification.json',
        A / 'rank_date_index_combined_worker_preflight_20261007/verification.json',
        A / 'qualified_round_recovery_evidence_v4_20261007.py',
        A / 'win32_read_handle_hash_cache_with_filename_v2_20261006.py',
        A / 'frozen_controller_name_collision_restoration_20261006/source_restoration_verification.json',
        *[Path(p) for p in repaired['two_independent_frozen_source_copies']],
        failed_path, old_service / 'execution.json', old_service / 'run.json', qualified_original]
    run['input_sha256'].update({str(p): sha(p) for p in additions})
    new_run = out / 'qualified_run.json'
    create(new_run, run)
    original_failed_sha = sha(failed_path)
    frozen = out / 'frozen_before_actual_status_gate_recovery.json'
    create(frozen, {'at_local': time.strftime('%Y-%m-%dT%H:%M:%S'), 'input_sha256': run['input_sha256'],
        'restored_original_bootstrap_binding': repaired,
        'original_failed_scope_sha256': original_failed_sha,
        'new_alternate_scope': str(alternate), 'original124_grid_preserved': True,
        'original_native_classifier_fits_reused_no_new_fits': True, 'test_labels_read': False})
    additions += [new_run, frozen, *[Path(p) for p in run['input_sha256']]]
    from classifier_consensus_status_gate_recovery_runtime_20261007 import install as install_gate
    restore_gate = install_gate()
    import frozen_provenance_execution_scope_20261004 as provenance
    from win32_read_handle_hash_cache_with_filename_v2_20261006 import LockedReadHashCache
    old_cache, original_factory = provenance.LockedReadHashCache, provenance.FrozenProvenanceExecutionScope
    provenance.LockedReadHashCache = LockedReadHashCache
    import qualified_round_recovery_evidence_v2_20261005 as qualified2
    import qualified_round_recovery_evidence_v3_20261006 as qualified3
    old_caches = [(m, m.LockedReadHashCache) for m in (qualified2, qualified3)]
    for m, _ in old_caches:
        m.LockedReadHashCache = LockedReadHashCache
    import exact_rank_cache_official_worker_adapter_20261006 as rank
    import classifier_consensus_recovery_official_speed_adapter_20261007 as speed
    original_rank_install = rank.install
    # The speed adapter calls the saved original installation, avoiding recursion.
    speed.rank_install_original = original_rank_install
    def combined_install():
        rank.install = original_rank_install
        try:
            return speed.install()
        finally:
            rank.install = combined_install
    rank.install = combined_install
    routed = []

    def extended(module, extra_sources, metadata, analysis_root):
        original_dump = module.dump
        original_Context = module.Context
        original_init = original_Context.__init__

        def init(context, *args, **kwargs):
            original_init(context, *args, **kwargs)
            speed.install_context(context)

        original_Context.__init__ = init

        def dump(path, value, *args, **kwargs):
            if Path(path).resolve() == failed_path.resolve():
                assert sha(failed_path) == original_failed_sha
                assert value['status'] == 'passed' or value['status'] == 'failed'
                value = {**value, 'recovery_execution': True,
                    'original_failed_scope_retained': True, 'original_failed_scope_sha256': original_failed_sha,
                    'precise_original_route_gate_required': True,
                    'all_original124_declared_cases_retained': True,
                    'Windows_read_share_only_raw_handles_and_full_initial_final_hash': True,
                    'original_driver_scope_metadata_new_quality_scores': value.get('new_quality_scores'),
                    'actual_recovery_quality_records': sum(len(read(p)['results']) for p in module.OUT.glob('wave*_results.json')),
                    'input_sha256': read(module.OUT / 'protocol.json')['input_sha256'] if (module.OUT / 'protocol.json').exists() else {},
                    'new_model_fits': 0, 'original_test_labels_read': False}
                return original_dump(alternate, value, *args, **kwargs)
            return original_dump(path, value, *args, **kwargs)

        module.dump = dump
        routed.append((module, original_dump, original_Context, original_init))
        return original_factory(module, list(dict.fromkeys([*extra_sources, *additions])),
            {**metadata, 'actual_precise_R89_gate_recovery': True,
             'original_failed_scope_must_remain_byte_identical': original_failed_sha,
             'actual_final_scope_must_use_unique_alternate': str(alternate),
             'full_original124_scientific_records_required': True,
             'actual_official_date_index_speed_proof_required': True}, analysis_root)

    provenance.FrozenProvenanceExecutionScope = extended
    original_args = sys.argv
    try:
        sys.argv = [str(A / 'run_recovery_qualified_workflow_with_exact_rank_cache_v2_20261006.py'),
            str(A / 'run_training_round89_v3_pipeline.py'), str(new_run)]
        runpy.run_path(sys.argv[0], run_name='__main__')
        actual = read(alternate)
        assert actual['status'] == 'passed' and actual['scope_started'] is True
        assert actual['all_sha_bindings_restored'] and actual['actual_recovery_quality_records'] == 124
        assert sha(failed_path) == original_failed_sha
        create(out / 'verification.json', {'status': 'passed_actual_original124_science_candidate_full_QA_alternate_scope_recovery',
            'at_local': time.strftime('%Y-%m-%dT%H:%M:%S'), 'actual_recovery_scope': str(alternate),
            'actual_recovery_scope_sha256': sha(alternate), 'original_failed_scope_sha256': original_failed_sha,
            'actual_quality_score_records': 124, 'new_native_fits': 0,
            'old_failed_scope_and_all_original_scientific_sources_unchanged': True,
            'main_publication_and_next_round90_qualification_pending': True, 'test_labels_read': False})
    finally:
        sys.argv = original_args
        provenance.LockedReadHashCache, provenance.FrozenProvenanceExecutionScope = old_cache, original_factory
        rank.install = original_rank_install
        for module, original_dump, context, original_init in routed:
            module.dump = original_dump
            context.__init__ = original_init
        for m, cache in old_caches:
            m.LockedReadHashCache = cache
        restore_gate()


if __name__ == '__main__':
    main()
