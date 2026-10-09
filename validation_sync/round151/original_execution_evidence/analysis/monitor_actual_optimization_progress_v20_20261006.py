"""Report current recovered handles and scoring rounds above the retained observer."""
from pathlib import Path
from datetime import datetime
import json
import sys

import psutil

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path[:0] = [str(ROOT), str(A)]
import qualified_round_recovery_evidence_v3_20261006 as qualification
import refresh_optimization_boundary_evidence_20261004 as base
base.complete_round_evidence = qualification.complete_round_evidence
import monitor_actual_optimization_progress_v18_20261005 as previous
from atomic_optimization_observer_writes_20261005 import write
from run_dependency_queue_20261006 import owned

original_update = previous.update


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8-sig'))


def update():
    state = original_update()
    from refresh_classifier_consensus_cost_evidence_20261006 import main as costs
    costs()
    value = read(A / 'ongoing_optimization_state.json')
    queue = read(ROOT / value['dependency_queue_registry'])
    plan_path = Path(read(queue['script_args'][0])['arguments'][0])
    plan = read(plan_path)
    qstate = read(plan_path.parent / 'state.json')
    jobs = {**plan['preserved_active_jobs'], **qstate['activated_jobs'], 'dependency_queue': queue}
    registry = read(ROOT / value['active_run_registry'])
    for row in registry:
        if not row.get('queued_without_heavy_imports') and all(
                key in row for key in ('owned_worker_pid', 'owned_worker_creation_time', 'script_args')):
            jobs[f'round{row["round"]}'] = row
    owned_jobs, active_quality = {}, []
    for name, row in jobs.items():
        live = owned(row)
        owned_jobs[name] = {'owned_live_now': live, 'pid': row['owned_worker_pid'],
                           'creation_time': row['owned_worker_creation_time']}
        if not live:
            continue
        process = psutil.Process(row['owned_worker_pid'])
        owned_jobs[name].update(RSS_bytes=process.memory_info().rss, CPU_seconds=sum(process.cpu_times()[:2]))
        if name.startswith('round') and int(name[5:]) in state['pending_required_rounds']:
            active_quality.append((int(name[5:]), row))
    if active_quality:
        number, row = min(active_quality)
        stage = read(A / f'ongoing_optimization_r{number}_state.json')
        waves, scores = {}, []
        for path in (A / f'optimization_20261003_r{number}').glob('wave*_results.json'):
            payload = read(path)
            waves[path.stem] = len(payload['results'])
            scores.extend(r['connected_final_score'] for r in payload['results'].values())
        workers = []
        for process in psutil.Process(row['owned_worker_pid']).children(recursive=True):
            try:
                cmd = ' '.join(process.cmdline())
                if 'multiprocessing.spawn' in cmd and '--multiprocessing-fork' in cmd:
                    workers.append(process.pid)
            except psutil.Error:
                pass
        value.update(round=number, active_round=number, stage=stage['stage'], status=stage['status'],
            active_root_pid_live=True, active_root_command_owned=True,
            active_wave_records=waves, active_partial_score=max(scores, default=None),
            active_official_worker_pids=workers, active_official_workers=len(workers),
            queued_rounds=[n for n in state['pending_required_rounds'] if n != number])
    cost = read(A / 'optimization_fit_cost_evidence_20261004.json')
    value.update(actual_progress_monitor=str(Path(__file__).relative_to(ROOT)),
        actual_active_quality_rounds=[n for n, _ in active_quality],
        earliest_required_pending_round=min(state['pending_required_rounds'], default=None),
        current_recovered_worker_ownership=owned_jobs,
        classifier_consensus_virtual_annual_outputs=cost.get('classifier_consensus_virtual_annual_outputs', 0),
        classifier_consensus_virtual_final_artifacts=cost.get('classifier_consensus_virtual_final_artifacts', 0),
        classifier_consensus_new_native_fits=0,
        classifier_consensus_fullfuture_status=cost.get('classifier_consensus_fullfuture_status', 'pending'),
        actual_new_annual_fits_completed=cost['total_actual_new_annual_fits'],
        five_year_configuration_count=cost['fully_completed_five_year_configurations'],
        fulltraining_artifacts_ready=cost['fulltraining_artifacts_ready'],
        wide_recovery_resource_sample_path=str(A / 'service_owned_workflows_20261006/neural16384_annual/resources/actual_full_training_resource_samples.jsonl'),
        robust_recovery_resource_sample_path=str(A / 'system_reboot_workflow_recovery_20261006/robust_annual/resources/actual_cpu_resource_samples.jsonl'))
    for filename in ('ongoing_optimization_state.json', 'resume_optimization_20261004.json'):
        write(A / filename, value)
    state.update(active_round=value['active_round'], active_stage=value['stage'], active_status=value['status'],
        active_wave_records=value['active_wave_records'], active_partial_score=value['active_partial_score'],
        actual_active_quality_rounds=value['actual_active_quality_rounds'],
        earliest_required_pending_round=value['earliest_required_pending_round'],
        current_recovered_worker_ownership=owned_jobs, actual_observer_version=20,
        at_local=datetime.now().isoformat(timespec='seconds'))
    write(A / 'actual_optimization_monitor_state_20261005.json', state)
    print(json.dumps({'actual_observer_version': 20, 'actual_active_quality_rounds': state['actual_active_quality_rounds'],
        'earliest_required_pending_round': state['earliest_required_pending_round'],
        'partial_scores_not_qualified_complete': True}, ensure_ascii=False), flush=True)
    return state


def main(once=False):
    previous.update = update
    previous.main(once)


if __name__ == '__main__':
    main('--once' in sys.argv)
