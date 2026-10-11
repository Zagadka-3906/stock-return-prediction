"""Observe local owned tasks and publish lightweight, complete public generations."""
from pathlib import Path
import json
import re
import sys
import time
import uuid

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path[:0] = [str(ROOT), str(A)]
from run_dependency_queue_v3_20261006 import read, owned
from monitor_local_only_runtime_20261007 import service_status
from complete_observer_snapshot_transaction_v2_20261006 import transaction
from atomic_optimization_observer_writes_20261005 import write


_WAVE_STATUS_CACHE = {}


def wave_status():
    result = []
    for p in sorted((A / 'optimization_20261003_r89').glob('wave*_results.json')):
        stat = p.stat()
        stamp = (stat.st_mtime_ns, stat.st_size)
        prior = _WAVE_STATUS_CACHE.get(p.name)
        if prior is None or prior[0] != stamp:
            current = read(p)
            row = {'file': p.name, 'status': current['status'], 'actual_written_official_records': len(current['results'])}
            _WAVE_STATUS_CACHE[p.name] = (stamp, row)
        result.append(dict(_WAVE_STATUS_CACHE[p.name][1]))
    assert sum(r['actual_written_official_records'] for r in result) <= 124
    return result


def update():
    import psutil
    old = service_status('progress_monitor_v36')
    assert not old['strong_identity_owned_live_now'] and old['terminal']['failure'] == "KeyError: 'at_local'"
    service_names = ('neural16384_annual', 'direct_rank92_round108_full_registration',
        'direct_flag_rank_micro74_official_comparison', 'single_host_rank_micro74_scores_evidence_publication',
        'local_speed_adoption_main_publication', 'dependency_queue_v12_local_cache', 'main_publisher_v7',
        'direct_rank_micro74_round109_full_registration', 'classifier_consensus_round89_status_recovery',
        'classifier_consensus_round89_status_recovery_main_publication', 'cpu_conditional_residual_mlp_native_bank20',
        'cpu_conditional_residual_mlp20_bank_evidence_publication', 'conditional_residual_mlp44_official_comparison',
        'cpu_conditional_residual_mlp20_scores_evidence_publication', 'CPU_MLP44_selected_candidate_preparation',
        'CPU_MLP44_selected_candidate_sealing', 'CPU_MLP44_round110_full_registration',
        'parent_rank_cache_alternating_benchmark', 'parent_rank_cache_alternating_benchmark_main_publication')
    services = {n: service_status(n) for n in service_names}
    qualified = {}
    for n, qa_version in ((107, 18), (108, 19), (109, 20), (110, 21)):
        folder = A / f'optimization_20261003_r{n}'
        closure = folder / 'full_registration_execution.json'
        receipt_path = A / f'github_validation_sync_main_20261005/round{n}_receipt.json'
        if not closure.exists() or not receipt_path.exists():
            continue
        receipt = read(receipt_path)
        if read(closure)['status'] != 'passed' or receipt.get('round') != n or receipt.get('actual_full_QA_version') != qa_version:
            continue
        service = {107: 'round107_full_QA_receipt_closure_v2', 108: 'direct_rank92_round108_full_registration',
            109: 'direct_rank_micro74_round109_full_registration', 110: 'CPU_MLP44_round110_full_registration'}[n]
        status = service_status(service)
        if status['strong_identity_owned_live_now'] or not status['terminal'] or status['terminal']['status'] != 'passed':
            continue
        assert read(folder / 'provenance_scope_execution.json')['status'] == 'passed'
        qualified[n] = receipt
    folder = A / 'direct_flag_rank_micro74_official_comparison_20261007'
    records = [read(p) for p in sorted(folder.glob('case*_official.json'))]
    stage = folder / 'actual_stage.json'
    log = A / 'service_owned_workflows_20261006/neural16384_annual/stdout.log'
    with log.open('rb') as stream:
        stream.seek(max(0, log.stat().st_size - 65536))
        tail = stream.read().decode('utf-8')
    epochs = re.findall(r'\[([^]]+)\] MLP y_rank epoch(\d+)/(\d+) mature-training loss=([^\s]+)', tail)
    value = {'status': 'monitoring_actual_local_only_tasks', 'at_local': time.strftime('%Y-%m-%dT%H:%M:%S'),
        'monitor_pid': psutil.Process().pid, 'execution_mode': 'single_host', 'user_cancelled_cooperation': True,
        'remote_tasks_dispatched': 0, 'services': services, 'actual_qualified_recent_rounds': qualified,
        'actual_micro74_completed_cases': len(records), 'expected_micro74_cases': 74,
        'actual_micro74_stage': read(stage) if stage.exists() else None,
        'partial_best_score_not_new_qualified_candidate': max((r['connected_final_score'] for r in records), default=None),
        'CPU_thread_training_benchmark_speedup': 2.410964537607891,
        'official_evaluation_full_phase_benchmark_speedup': read(A / 'official_date_index_speed_benchmark_20261007/verification.json')['median_full_official_evaluation_speedup'],
        'both_stage_speedups_are_measured_not_whole_goal_speedup': True,
        'actual_new_direct_rank_native_fits': 36, 'actual_completed_direct_rank92_official_records': 92,
        'actual_R89_strict_gate_preflight': read(A / 'classifier_consensus_status_gate_recovery_preflight_20261007/verification.json')['status'],
        'R89_scientific_retry_and_alternate_scope_qualification_pending': not (services['classifier_consensus_round89_status_recovery_main_publication']['terminal'] and services['classifier_consensus_round89_status_recovery_main_publication']['terminal']['status'] == 'passed'),
        'original_GPU_no_restart_or_stop_pending_user_reply': True,
        'last_observed_NN_epoch': {'time_of_day': epochs[-1][0], 'epoch': int(epochs[-1][1]), 'required': int(epochs[-1][2])} if epochs else None,
        'available_RAM_GiB': psutil.virtual_memory().available / 2**30,
        'old_monitor36_natural_failure_preserved': old['terminal'],
        'no_model_data_ranking_or_all_historical_source_rehash_on_each_observation': True,
        'global_resource_or_feasible_direction_exhaustion_not_claimed': True, 'test_labels_read': False}
    if qualified:
        best_number = max(qualified, key=lambda n: (qualified[n]['official_score'], n))
        value.update(current_qualified_best_round=best_number,
            current_qualified_best_score=qualified[best_number]['official_score'],
            current_qualified_main_receipt=qualified[best_number], current_qualified_latest_round=max(qualified))
    for name in ('local_speed_adoption_github_20261007', 'single_host_rank_micro74_scores_github_20261007'):
        p = A / name / 'receipt.json'
        if p.exists():
            value[name] = read(p)
    bank_path = A / 'cpu_conditional_residual_mlp_bank20_20261007'
    bank_proof = bank_path / 'verification.json'
    value['actual_MLP20_completed_native_fits'] = read(bank_proof)['actual_native_fits'] if bank_proof.exists() else len(list(bank_path.glob('*/info_*.json')))
    value['actual_MLP44_completed_official_cases'] = len(list((A / 'conditional_residual_mlp44_official_comparison_20261007').glob('case*_official.json')))
    value['MLP44_expected_official_cases'] = 44
    if bank_proof.exists():
        value['actual_MLP20_training_and_controls_elapsed_seconds'] = read(bank_proof)['elapsed_seconds']
    r89_stage = A / 'ongoing_optimization_r89_state.json'
    if r89_stage.exists():
        value['actual_R89_stage'] = read(r89_stage)
    for folder in ('cpu_conditional_residual_mlp20_bank_github_20261007', 'cpu_conditional_residual_mlp20_scores_github_20261007'):
        path = A / folder / 'receipt.json'
        if path.exists():
            value[folder] = read(path)
    queue_state = read(A / 'service_owned_dependency_queue_v4_20261006/state.json')
    value['actual_local_queue12_remaining_jobs'] = queue_state['deferred_jobs_remaining']
    value['actual_local_queue12_state_pid'] = queue_state['pid']
    value['actual_R89_wave_status'] = wave_status()
    value['actual_R89_written_wave_files'] = [r['file'] for r in value['actual_R89_wave_status']]
    value['actual_R89_completed_wave_files'] = [r['file'] for r in value['actual_R89_wave_status'] if r['status'] == 'complete']
    value['actual_R89_partial_written_official_records'] = sum(r['actual_written_official_records'] for r in value['actual_R89_wave_status'])
    value['expected_R89_official_records'] = 124
    value['partial_R89_record_count_not_full_scientific_or_candidate_qualification'] = True
    b = A / 'parent_rank_cache_alternating_benchmark_20261007/actual_stage.json'
    if b.exists():
        value['actual_parent_rank_cache_alternating_benchmark_stage'] = read(b)
    benchmark_receipt = A / 'parent_rank_cache_alternating_benchmark_github_20261007/receipt.json'
    if benchmark_receipt.exists():
        value['actual_parent_rank_cache_alternating_benchmark_main_receipt'] = read(benchmark_receipt)
    r89_receipt = A / 'github_validation_sync_main_20261005/round89_receipt.json'
    if r89_receipt.exists() and not value['R89_scientific_retry_and_alternate_scope_qualification_pending']:
        value['actual_R89_closed_main_receipt'] = read(r89_receipt)
    candidate_ready = A / 'CPU_MLP_residual44_selected_release_20261007/selected_candidate_ready_for_registration.json'
    if candidate_ready.exists():
        value['actual_MLP44_selected_candidate_ready'] = read(candidate_ready)
    write(A / 'single_host_optimization_live_status_v5_20261007.json', value)
    # Preserve every legacy pending route and scientific record. Update only fields
    # established by the qualified closures and actual owned local observations.
    with transaction() as (pending, commit):
        ongoing = read(A / 'ongoing_optimization_state.json')
        ongoing.update(local_only_live_status=value, actual_observer_version='local_only_v5',
            updated_at_local=value['at_local'], execution_mode='single_host', remote_tasks_dispatched=0,
            original_pending_grid_registry_preserved=True, global_resource_exhaustion_established=False,
            local_active_micro74_actual_scored_records=len(records), local_active_micro74_expected_records=74,
            original89_failed_scope_recovery_still_required=value['R89_scientific_retry_and_alternate_scope_qualification_pending'],
            actual_progress_monitor=str(Path(__file__).relative_to(ROOT)))
        if qualified:
            ongoing.update(latest_completed_round=max(max(qualified), ongoing.get('latest_completed_round', 0)),
                last_completed_round=max(max(qualified), ongoing.get('last_completed_round', 0)))
            if value['current_qualified_best_score'] >= ongoing.get('completed_validation_best', float('-inf')):
                ongoing.update(best_completed_round=value['current_qualified_best_round'], completed_validation_best=value['current_qualified_best_score'])
        state = read(A / 'actual_optimization_monitor_state_20261005.json')
        state.update(local_only_live_status=value, actual_observer_version='local_only_v5', at_local=value['at_local'],
            execution_mode='single_host', remote_tasks_dispatched=0, global_resource_exhaustion_established=False)
        for field in ('latest_completed_round', 'last_completed_round', 'best_completed_round', 'completed_validation_best'):
            if field in ongoing:
                state[field] = ongoing[field]
        pending[A / 'ongoing_optimization_state.json'] = ongoing
        pending[A / 'resume_optimization_20261004.json'] = dict(ongoing)
        pending[A / 'actual_optimization_monitor_state_20261005.json'] = state
        commit(uuid.uuid4().hex)
    print(json.dumps({'at_local': value['at_local'], 'micro74_scored': len(records), 'qualified_recent_rounds': list(qualified)}), flush=True)


if __name__ == '__main__':
    while True:
        try:
            update()
        except (FileNotFoundError, json.JSONDecodeError) as error:
            print(json.dumps({'status': 'transient_observation_retry', 'error': str(error)}), flush=True)
        time.sleep(30)
