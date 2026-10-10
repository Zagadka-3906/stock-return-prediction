"""Restore absent owned queue entries while retaining old runs and frozen sources."""
from pathlib import Path
from datetime import datetime
import json
import os
import subprocess
import sys
import psutil

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'analysis'))
from locked_read_hash_cache_20261004 import fresh_sha


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8-sig'))


def create(path, value):
    with Path(path).open('x', encoding='utf-8') as stream:
        json.dump(value, stream, ensure_ascii=False, indent=2)


def main():
    analysis = ROOT / 'analysis'
    out = analysis / 'restart_queue_recovery_20261005'
    out.mkdir(exist_ok=True)
    assert not (out / 'plan.json').exists()
    registry_path = analysis / 'resumed_rounds_nystrom_locked_20261004.json'
    registry = read(registry_path)
    tasks = []
    for number in (60, 61, 62):
        old = next(r for r in registry if r['round'] == number)
        tasks.append({'name': f'round{number}', 'old': old, 'script': old['script'],
                      'args': [str(number)], 'round': number})
    scripts = [
        ('neural_width_frontier_run', None, None, []),
        ('official_worker_frontier_run', None, None, []),
        ('official_worker_frontier_audit_run', None, None, []),
        ('neural_width_frontier_audit_run', None, None, []),
        ('nystrom_ridge_training_run', 'nystrom_ridge_training_run_20261005.json', 'run_nystrom_restart_training_20261005.py', []),
        ('nystrom_ridge_observer_run', 'nystrom_ridge_observer_run_20261005.json', 'observe_nystrom_restart_resources_20261005.py', []),
        ('nystrom_ridge_future_run', None, None, []),
        ('nystrom_ridge_complete_scheme_run', None, None, []),
        ('nystrom_ridge_evidence_audits_run', None, 'run_nystrom_restart_evidence_audits_20261005.py', []),
        ('nystrom_ridge_scheme_count_audit_run', None, None, ['nystrom_ridge']),
    ]
    for name, new_name, new_script, args in scripts:
        previous_path = analysis / f'{name}_20261004.json'
        old = read(previous_path)
        tasks.append({'name': name, 'old': old,
                      'previous_registry': str(previous_path),
                      'destination_registry': str(analysis / new_name) if new_name else str(previous_path),
                      'script': 'analysis/' + new_script if new_script else old['script'], 'args': args})
    frozen = {}
    for proto in analysis.glob('*/protocol.json'):
        value = read(proto)
        frozen.update(value.get('input_sha256', {}))
    for task in tasks:
        old = task['old']
        if psutil.pid_exists(old['pid']):
            command = psutil.Process(old['pid']).cmdline()
            assert not any(old['script'] in arg for arg in command), task['name']
        for path, digest in old.get('input_sha256', {}).items():
            assert fresh_sha(path) == digest, path
        target = task.get('destination_registry')
        assert not target or str(Path(target).resolve()) not in frozen, target
    assert str(registry_path.resolve()) not in frozen
    create(out / 'previous_primary_registry.json', registry)
    inputs = {str(Path(__file__).resolve()): fresh_sha(Path(__file__))}
    for task in tasks:
        path = ROOT / task['script']
        inputs[str(path.resolve())] = fresh_sha(path)
    source_audit = analysis / 'nystrom_restart_source_audit_20261005.json'
    inputs[str(source_audit.resolve())] = fresh_sha(source_audit)
    create(out / 'plan.json', {'status': 'frozen_before_restoring_absent_queue_entries',
        'at_local': datetime.now().isoformat(timespec='seconds'),
        'host_boot_at_local': datetime.fromtimestamp(psutil.boot_time()).isoformat(timespec='seconds'),
        'tasks': tasks, 'input_sha256': inputs,
        'existing_frozen_protocols_and_original_nystrom_training_registry_preserved': True,
        'scientific_algorithms_and_configuration_menus_unchanged': True,
        'new_model_fits_at_launch': 0, 'test_labels_read': False})
    environment = os.environ.copy()
    for name in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS', 'NUMEXPR_NUM_THREADS', 'POLARS_MAX_THREADS'):
        environment[name] = '8'
    launched = []
    for task in tasks:
        name = task['name']
        stdout = analysis / 'run_logs' / f'{name}_restart_20261005.stdout.log'
        stderr = analysis / 'run_logs' / f'{name}_restart_20261005.stderr.log'
        with stdout.open('x') as output, stderr.open('x') as error:
            proc = subprocess.Popen([sys.executable, '-B', '-X', 'utf8', task['script'], *task['args']],
                cwd=ROOT, env=environment, stdout=output, stderr=error,
                creationflags=subprocess.CREATE_NO_WINDOW)
        record = {**task['old'], 'previous_root_pid': task['old']['pid'],
            'pid': proc.pid, 'script': task['script'], 'script_args': task['args'],
            'stdout': str(stdout), 'stderr': str(stderr),
            'launched_at_local': datetime.now().isoformat(timespec='seconds'),
            'status': 'restored_waiting_actual_scientific_gates_after_host_restart',
            'restart_recovery_plan': str((out / 'plan.json').relative_to(ROOT))}
        create(out / f'{name}_run.json', record)
        if 'round' in task:
            index = next(i for i, item in enumerate(registry) if item['round'] == task['round'])
            registry[index] = record
        else:
            destination = Path(task['destination_registry'])
            if destination == Path(task['previous_registry']):
                create(out / f'{name}_previous_run.json', task['old'])
                destination.write_text(json.dumps(record, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
            else:
                create(destination, record)
        launched.append({'name': name, 'pid': proc.pid, 'script': task['script']})
    registry_path.write_text(json.dumps(registry, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    for path, digest in inputs.items():
        assert fresh_sha(path) == digest, path
    create(out / 'launch_verification.json', {'status': 'passed',
        'at_local': datetime.now().isoformat(timespec='seconds'), 'launched_entries': launched,
        'all_execution_sources_unchanged': True, 'actual_new_model_fits_at_launch': 0,
        'test_labels_read': False, 'continuous_goal_complete': False})
    print(json.dumps({'status': 'passed', 'restored_queue_entries': launched}), flush=True)


if __name__ == '__main__':
    main()
