"""Replace only an exactly idle scheduler; preserve original32 routes and live scientists."""
from pathlib import Path
from copy import deepcopy
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path[:0] = [str(ROOT), str(A)]
from run_dependency_queue_v3_20261006 import read, sha, create, owned
from atomic_optimization_observer_writes_20261005 import write
from handoff_ready_goss_full_execution_20261006 import start_service, pair
from handoff_joint_goss_round97_full_execution_20261006 import suspended_idle

OUT = A / 'dependency_queue_v12_local_cache_actual_handoff_20261007'
QUEUE = A / 'service_owned_dependency_queue_v12_local_cache_20261007'
SHARED = A / 'service_owned_dependency_queue_v4_20261006'


def main():
    assert not OUT.exists() and not QUEUE.exists()
    OUT.mkdir()
    QUEUE.mkdir()
    proof_path = A / 'dependency_queue_v12_local_cache_routes_preflight_20261007/verification.json'
    proof = read(proof_path)
    assert proof['status'] == 'passed_original32_routes_and_R90_only_dispatch_and_strict89_qualification_source_controls'
    old_plan_path = A / 'service_owned_dependency_queue_bootstrap_fields_recovery_v2_20261006/queue_plan.json'
    original = read(old_plan_path)
    assert original['deferred_jobs'] == proof['original_deferred_jobs'] and len(original['deferred_jobs']) == 32
    identity = read(A / 'service_owned_workflows_20261006/dependency_queue_bootstrap_fields_recovery_v2/native_launch.json')
    assert owned(identity)
    pins = {**original['input_sha256'], **proof['input_sha256']}
    sources = [Path(__file__), proof_path,
        A / 'run_dependency_queue_v12_local_cache_and_R89_qualification_20261007.py',
        A / 'run_classifier_consensus_round90_with_precise_gate_and_parent_cache_20261007.py',
        A / 'parent_graph_rank_cache_evidence_github_20261007/receipt.json',
        A / 'CPU_MLP44_round110_full_registration_admission_20261007.json',
        A / 'CPU_MLP44_round110_source_route_preflight_20261007.json',
        A / 'handoff_joint_goss_round97_full_execution_20261006.py',
        A / 'handoff_ready_goss_full_execution_20261006.py']
    pins.update({str(p): sha(p) for p in sources})
    # Validate the complete new immutable plan before holding the old helper.
    for path, digest in pins.items():
        assert sha(path) == digest, path
    names = ('neural16384_annual', 'classifier_consensus_round89_status_recovery',
        'classifier_consensus_round89_status_recovery_main_publication',
        'conditional_residual_mlp44_official_comparison', 'CPU_MLP44_round110_full_registration',
        'CPU_MLP44_selected_candidate_preparation', 'CPU_MLP44_selected_candidate_sealing',
        'cpu_conditional_residual_mlp20_scores_evidence_publication',
        'quantile_tree_quality_queue_v2', 'quantile_distribution_views_quality_queue', 'main_publisher_v7')
    preserved = {name: read(A / 'service_owned_workflows_20261006' / name / 'native_launch.json') for name in names}
    assert all(owned(row) for row in preserved.values())
    parent = worker = new = None
    retired = False
    try:
        parent, worker, idle = suspended_idle(identity, '    main (run_dependency_queue_v11_shared_state_main_20261006.py:36)')
        create(OUT / 'old_controller_exact_idle_before_and_after.json', idle)
        snapshot = read(SHARED / 'state.json')
        assert snapshot['pid'] == worker.pid
        create(OUT / 'old_controller_last_actual_snapshot.json', snapshot)
        prior89 = snapshot['activated_jobs']['round89']
        assert not owned(prior89)
        registry_path = Path(original['registry'])
        registry = read(registry_path)
        create(OUT / 'original_registry_before_actual89_identity_adoption.json', registry)
        assert str(registry_path) not in read(A / 'optimization_20261003_r89/protocol.json')['input_sha256']
        actual89 = {**deepcopy(preserved['classifier_consensus_round89_status_recovery']), 'name': 'round89',
            'round': 89, 'explicit_parent_round': 88, 'prospective_official_workers': 1,
            'actual_unique_status_gate_recovery_service': 'classifier_consensus_round89_status_recovery',
            'original_failed_attempt_preserved': prior89}
        assert owned(actual89)
        activated = deepcopy(snapshot['activated_jobs'])
        activated['round89'] = actual89
        plan = deepcopy(original)
        marker = str(A / 'optimization_20261003_r110/full_registration_execution.json')
        markers = list(dict.fromkeys([*plan['complete_ranking_registration_serialization_markers'], marker]))
        plan.update(status='frozen_all32_routes_local_cache_and_precise_closed89_gate_v12',
            input_sha256=pins, previously_activated_jobs=activated,
            activation_handoff_commit_marker=str(OUT / 'handoff_commit.json'), prior_queue_plan=str(old_plan_path),
            complete_ranking_registration_serialization_markers=markers,
            original_failed_round89_attempt_preserved=prior89,
            original_shared_state_path_preserved=str(SHARED / 'state.json'),
            same_original_scientific_grids_and_arguments_retained=True,
            scientific_workers_stopped_or_restarted=0)
        plan['preserved_active_jobs'].update(preserved)
        assert plan['deferred_jobs'] == original['deferred_jobs']
        plan_path = QUEUE / 'queue_plan.json'
        create(plan_path, plan)
        create(OUT / 'frozen_before_actual_handoff.json', {'input_sha256': pins, 'old_identity': identity,
            'preserved_actual_workers': preserved, 'original_failed89_identity': prior89,
            'actual_new89_identity_alias': actual89, 'new_quality_scores': 0, 'scientific_workers_to_stop': 0})
        new = start_service('dependency_queue_v12_local_cache',
            'run_dependency_queue_v12_local_cache_and_R89_qualification_20261007.py', [str(plan_path)],
            {**pins, str(plan_path): sha(plan_path)})
        for _ in range(120):
            assert owned(new)
            current = read(SHARED / 'state.json')
            if current['pid'] == new['owned_worker_pid']:
                assert current['activated_jobs'] == activated
                break
            time.sleep(.5)
        else:
            raise RuntimeError('New held scheduler did not preserve complete shared state')
        assert all(owned(row) for row in preserved.values())
        old_parent, old_worker = pair(identity)
        assert not old_worker.children()
        old_worker.terminate()
        old_worker.wait(timeout=15)
        old_parent.terminate()
        old_parent.wait(timeout=15)
        retired = True
        registry = [actual89 if row['round'] == 89 else row for row in registry]
        write(registry_path, registry)
        create(A / 'service_owned_workflows_20261006/dependency_queue_bootstrap_fields_recovery_v2/administrative_supersession_local_v12_20261007.json', {
            'status': 'administratively_retired_exact_idle_helper_not_scientific_completion',
            'old_identity': identity, 'new_identity': new, 'scientific_workers_stopped_or_restarted': 0})
        create(OUT / 'handoff_commit.json', {'status': 'retired_original_controller_and_preserved_scientific_workers',
            'at_local': time.strftime('%Y-%m-%dT%H:%M:%S'), 'actual_new_identity': new,
            'all32_original_routes_preserved': True, 'scientific_workers_stopped_or_restarted': 0})
        create(OUT / 'verification.json', {'status': 'passed_actual_all32_local_queue12_handoff_preserved_live89_and_GPU',
            'at_local': time.strftime('%Y-%m-%dT%H:%M:%S'), 'input_sha256': pins,
            'actual_new_identity': new, 'original_failed89_identity_preserved': prior89,
            'actual_new89_owned_identity_alias': actual89, 'preserved_actual_workers': preserved,
            'only_unstarted90_scientific_bridge_changes': True, 'new_quality_scores': 0,
            'scientific_workers_stopped_or_restarted': 0, 'test_labels_read': False})
        print('passed_actual_all32_local_queue12_handoff_preserved_live89_and_GPU', flush=True)
    finally:
        if not retired:
            if new is not None and owned(new):
                assert not (OUT / 'handoff_commit.json').exists()
                new_parent, new_worker = pair(new)
                assert not new_worker.children()
                new_worker.terminate()
                new_worker.wait(timeout=15)
                new_parent.terminate()
                new_parent.wait(timeout=15)
            for process in (parent, worker):
                if process is not None and process.is_running():
                    process.resume()


if __name__ == '__main__':
    main()
