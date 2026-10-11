"""Lightweight read-only observation of local tasks; never rescan model/data hashes."""
from pathlib import Path
import json
import re
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path[:0] = [str(ROOT), str(A)]
from run_dependency_queue_v3_20261006 import read, owned
from atomic_optimization_observer_writes_20261005 import write


def service_status(name):
    folder = A / 'service_owned_workflows_20261006' / name
    identity = folder / 'native_launch.json'
    if not identity.exists():
        return {'status': 'not_launched'}
    row = read(identity)
    terminal = folder / 'service_execution.json'
    return {'strong_identity_owned_live_now': owned(row), 'worker_pid': row['owned_worker_pid'],
        'worker_birth_time': row['owned_worker_creation_time'],
        'actual_console_handle': row['actual_native_console_handle'],
        'terminal': read(terminal) if terminal.exists() else None}


def update():
    import psutil
    bank = A / 'direct_flag_centered_rank_bank36_20261007'
    score = A / 'direct_flag_rank92_official_comparison_20261007'
    records = [read(p) for p in sorted(score.glob('case*_official.json'))]
    final = score / 'verification.json'
    log = A / 'service_owned_workflows_20261006/neural16384_annual/stdout.log'
    with log.open('rb') as stream:
        stream.seek(max(0, log.stat().st_size - 65536))
        tail = stream.read().decode('utf-8')
    epochs = re.findall(r'\[([^]]+)\] MLP y_rank epoch(\d+)/(\d+) mature-training loss=([^\s]+)', tail)
    services = {name: service_status(name) for name in (
        'neural16384_annual', 'direct_flag_centered_rank_native_bank36',
        'direct_flag_rank92_official_comparison', 'single_host_rank92_scores_evidence_publication',
        'dependency_queue_bootstrap_fields_recovery_v2', 'main_publisher_v7')}
    value = {'status': 'monitoring_actual_local_only_tasks', 'at_local': time.strftime('%Y-%m-%dT%H:%M:%S'),
        'monitor_pid': psutil.Process().pid, 'execution_mode': 'single_host',
        'remote_tasks_dispatched': 0, 'services': services,
        'CPU_thread_benchmark': read(A / 'local_flag_tree_thread_benchmark_20261007/verification.json'),
        'actual_native_models': read(bank / 'verification.json')['actual_native_fits'],
        'actual_native_bank_elapsed_seconds': read(bank / 'verification.json')['elapsed_seconds'],
        'actual_official_cases_completed': len(records), 'expected_official_cases': 92,
        'actual_official_case_stage': read(score / 'actual_stage.json') if (score / 'actual_stage.json').exists() else None,
        'official92_terminal_verification': read(final)['status'] if final.exists() else None,
        'partial_best_score_not_new_qualified_candidate': max((r['connected_final_score'] for r in records), default=None),
        'current_qualified_best_round': 106, 'current_qualified_best_score': 0.45110171046668335,
        'current_qualified_main_receipt': read(A / 'github_validation_sync_main_20261005/round106_receipt.json'),
        'local_bank_main_receipt': read(A / 'single_host_rank36_bank_github_20261007/receipt.json'),
        'last_observed_NN_epoch_log': {'log_time_of_day': epochs[-1][0],
            'completed_epoch': int(epochs[-1][1]), 'required_epochs': int(epochs[-1][2]),
            'training_loss': float(epochs[-1][3]), 'log_date_must_be_read_from_source_file_context': True} if epochs else None,
        'available_RAM_GiB': psutil.virtual_memory().available / 2**30,
        'pending_previous_validation_closure': ['lowalpha50_candidate_confirmation_and_full_round107_registration',
            'original89_status_gate_and_preserved_failed_scope_recovery'],
        'legacy_progress_monitor36_terminal': service_status('progress_monitor_v36'),
        'this_lightweight_monitor_does_not_replace_old_scientific_or_ranking_records': True,
        'global_resource_or_feasible_direction_exhaustion_not_claimed': True,
        'scientific_workers_stopped_or_restarted': 0, 'test_labels_read': False}
    receipt = A / 'single_host_rank36_scores_github_20261007/receipt.json'
    if receipt.exists():
        value['actual_completed92_scores_main_receipt'] = read(receipt)
    write(A / 'single_host_optimization_live_status_20261007.json', value)
    print(json.dumps({'at_local': value['at_local'], 'actual_official_cases_completed': len(records),
        'CPU_science_owned_live': services['direct_flag_rank92_official_comparison']['strong_identity_owned_live_now'],
        'GPU_science_owned_live': services['neural16384_annual']['strong_identity_owned_live_now']}), flush=True)


if __name__ == '__main__':
    while True:
        try:
            update()
        except (FileNotFoundError, json.JSONDecodeError) as error:
            print(json.dumps({'status': 'transient_output_observation_retry', 'error': str(error)}), flush=True)
        time.sleep(30)
