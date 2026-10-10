"""Refresh actual progress, check command ownership, and snapshot new closed rounds."""
from pathlib import Path
from datetime import datetime
import argparse
import json
import sys
import time
import psutil

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT), str(ROOT / 'analysis')]
STATE = ROOT / 'analysis/actual_optimization_monitor_state_20261005.json'


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8-sig'))


def write(path, value):
    Path(path).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def owned(job):
    try:
        process = psutil.Process(job['pid'])
        command = process.cmdline()
        args = job.get('script_args', [])
        matched = any(job['script'].replace('\\', '/') in arg.replace('\\', '/') for arg in command)
        return matched and (not args or command[-len(args):] == args)
    except psutil.Error:
        return False


def update():
    import refresh_continuous_progress_20261004 as progress
    import refresh_optimization_boundary_evidence_20261004 as boundary
    from locked_read_hash_cache_20261004 import fresh_sha
    prior = read(STATE) if STATE.exists() else {}
    published = [int(p.stem.rsplit('_r', 1)[1]) for p in (ROOT / 'results').glob('optimization_20261003_r*.json')]
    latest_published = max(published)
    completed = [n for n in published if n < 50 or boundary.complete_round_evidence(n) is not None]
    latest = max(completed)
    inventory = sorted((str(p.relative_to(ROOT)), p.stat().st_size, p.stat().st_mtime_ns)
        for bank in (ROOT / 'analysis').glob('*bank_*') if bank.is_dir()
        for p in bank.glob('*/info_*.json'))
    inventory_key = json.dumps(inventory, separators=(',', ':'))
    # The cost producer also updates research directions using publication alone.
    # Run it only when all current publications have completed scientific scopes.
    cost_inventory_key = prior.get('cost_inventory_key')
    if cost_inventory_key != inventory_key and latest == latest_published:
        import refresh_expanded_stacking_research_evidence_20261004 as cost
        cost.main()
        cost_inventory_key = inventory_key
    progress.main()
    paths = [ROOT / 'analysis/ongoing_optimization_state.json', ROOT / 'analysis/resume_optimization_20261004.json']
    value = read(paths[0])
    registry = read(ROOT / value['active_run_registry'])
    active = next((r for r in registry if r['round'] == value['active_round']), None)
    root_owned = bool(active and owned(active))
    value.update(active_root_pid_live=root_owned, active_root_command_owned=root_owned,
        active_root_ownership_checked_at_local=datetime.now().isoformat(timespec='seconds'),
        actual_progress_monitor='analysis/monitor_actual_optimization_progress_20261005.py',
        host_boot_at_local=datetime.fromtimestamp(psutil.boot_time()).isoformat(timespec='seconds'))
    if not root_owned and value['status'] == 'running':
        value.update(status='interrupted_owned_process_absent',
                     persisted_stage_before_process_loss=value['stage'],
                     active_official_workers=0, active_official_worker_pids=[])
    recovery_runs = {}
    for field, name in (
            ('nystrom_ridge_owned_training_root_live', 'nystrom_ridge_training_run_20261005.json'),
            ('nystrom_ridge_resource_observer_owned_root_live', 'nystrom_ridge_observer_run_20261005.json'),
            ('nystrom_ridge_scheme_count_audit_owned_root_live', 'nystrom_ridge_scheme_count_audit_run_20261005.json')):
        path = ROOT / 'analysis' / name
        if path.exists():
            job = read(path)
            value[field] = owned(job)
            recovery_runs[name] = {'pid': job['pid'], 'owned_live': value[field], 'registry': str(path)}
    value['nystrom_restart_resource_window'] = 'analysis/nystrom_ridge_resource_observations_recovery_20261005'
    value['nystrom_interrupted_pretraining_wait_samples_retained_separately'] = 31663
    for path in paths:
        write(path, value)
    closed_changed = prior.get('latest_completed_round') != latest
    if closed_changed:
        boundary.main()
    checkpointed = prior.get('latest_checkpointed_round', 58)
    qa = read(ROOT / 'analysis/all_model_ranking_qa/interaction_result.json')
    if latest > checkpointed and latest == latest_published and qa['status'] == 'passed':
        import capture_actual_optimization_checkpoint_20261004 as checkpoint
        checkpoint.main()
        checkpointed = latest
    state = {'status': 'monitoring_actual_progress', 'at_local': datetime.now().isoformat(timespec='seconds'),
        'pid': psutil.Process().pid, 'source_sha256': fresh_sha(Path(__file__)),
        'latest_completed_round': latest, 'latest_published_round': latest_published,
        'active_round': value['active_round'], 'active_stage': value['stage'],
        'active_status': value['status'], 'active_root_command_owned': root_owned,
        'active_wave_records': value['active_wave_records'],
        'active_partial_score': value['active_partial_score'],
        'completed_board_records': qa['connected_records'],
        'recovery_runs': recovery_runs, 'latest_checkpointed_round': checkpointed,
        'inventory_key': inventory_key,
        'cost_inventory_key': cost_inventory_key,
        'global_resource_exhaustion_established': False, 'goal_status_not_modified': True,
        'test_labels_read': False}
    write(STATE, state)
    print(json.dumps({k: v for k, v in state.items() if k not in ('inventory_key', 'cost_inventory_key', 'recovery_runs')}, ensure_ascii=False), flush=True)
    return state


def main(once):
    while True:
        try:
            manifest = ROOT / 'analysis/actual_optimization_monitor_run_20261005.json'
            if manifest.exists():
                from locked_read_hash_cache_20261004 import fresh_sha
                for path, digest in read(manifest)['input_sha256'].items():
                    assert fresh_sha(path) == digest, path
            state = update()
        except (FileNotFoundError, json.JSONDecodeError):
            # Publication can replace a mutable JSON while this observer reads it.
            if once:
                raise
            time.sleep(2)
            continue
        if once or state['latest_completed_round'] >= 62:
            return
        time.sleep(30)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--once', action='store_true')
    main(parser.parse_args().once)
