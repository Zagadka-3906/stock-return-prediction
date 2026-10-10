"""Complete the idle-only handoff with recovered-R66 compatibility."""
from pathlib import Path
from datetime import datetime
import json
import os
import time

import psutil
from handoff_idle_dependencies_20261006 import sha, read, create
from run_dependency_queue_20261006 import owned
from windows_hidden_process_launch_20261006 import launch
from atomic_optimization_observer_writes_20261005 import write

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
OLD = A / 'idle_dependency_queue_handoff_20261006'
OUT = A / 'idle_dependency_queue_handoff_v2_20261006'
REGISTRY = A / 'resumed_rounds_dependency_queue_v2_20261006.json'


def main():
    assert not OUT.exists()
    OUT.mkdir()
    prior = read(OLD / 'plan.json')
    queue = read(OLD / 'launch.json')
    state = read(OLD / 'state.json')
    assert not state['activated_jobs'] and owned(queue)
    for row in prior['preserved_active_jobs'].values():
        assert owned(row)
    driver = A / 'run_dependency_queue_v2_20261006.py'
    sources = {str(path.resolve()): sha(path) for path in (
        Path(__file__), driver, OLD / 'plan.json', OLD / 'verification.json',
        A / 'qualified_round_recovery_evidence_v2_20261005.py',
        A / 'qualified_round_recovery_evidence_20261005.py')}
    plan = dict(prior)
    plan.update(status='frozen_before_idle_queue_v2_recovered_R66_verifier', registry=str(REGISTRY),
                input_sha256={**prior['input_sha256'], **sources},
                original_initial_queue_and_failed_R66_scope_preserved=True,
                recovered_R66_uses_same_strict_original_qualification=True)
    create(OUT / 'plan.json', plan)
    worker, parent = psutil.Process(queue['owned_worker_pid']), psutil.Process(queue['pid'])
    assert not [p for p in worker.children(recursive=True) if p.name().lower() != 'conhost.exe']
    assert not read(OLD / 'state.json')['activated_jobs']
    worker.terminate();worker.wait(timeout=10);parent.wait(timeout=10)
    with (OUT / 'stdout.log').open('xb') as out, (OUT / 'stderr.log').open('xb') as err:
        process = launch([str(ROOT / '.venv/Scripts/python.exe'), '-B', '-X', 'utf8', str(driver), str(OUT / 'plan.json')],
            cwd=ROOT, env=dict(os.environ, PYTHONDONTWRITEBYTECODE='1', PYTHONUTF8='1'), stdout=out, stderr=err)
    time.sleep(.5)
    assert process.poll() is None
    parent = psutil.Process(process.pid)
    children = [p for p in parent.children(recursive=True)
                if p.name().lower() == 'python.exe' and p.cmdline()[1:] == parent.cmdline()[1:]]
    assert len(children) == 1
    row = {'pid': parent.pid, 'script': str(driver), 'script_args': [str(OUT / 'plan.json')],
           'owned_worker_pid': children[0].pid, 'owned_worker_creation_time': children[0].create_time(),
           'stdout': str(OUT / 'stdout.log'), 'stderr': str(OUT / 'stderr.log'),
           'at_local': datetime.now().isoformat(timespec='seconds')}
    create(OUT / 'launch.json', row)
    registry = read(prior['registry'])
    for entry in registry:
        if entry.get('queued_without_heavy_imports'):
            entry.update(**row)
            state_path = A / f'ongoing_optimization_r{entry["round"]}_state.json'
            original_state = read(state_path)
            original_state['dependency_queue'] = str(OUT / 'plan.json')
            write(state_path, original_state)
    create(REGISTRY, registry)
    for filename in ('ongoing_optimization_state.json', 'resume_optimization_20261004.json'):
        path = A / filename;value = read(path)
        value['active_run_registry'] = REGISTRY.relative_to(ROOT).as_posix()
        value['dependency_queue_registry'] = (OUT / 'launch.json').relative_to(ROOT).as_posix()
        write(path, value)
    for source, digest in sources.items():
        assert sha(source) == digest
    for job in prior['preserved_active_jobs'].values():
        assert owned(job)
    create(OUT / 'verification.json', {
        'status': 'passed_idle_only_queue_v2_and_original_R66_recovery_qualification_preserved',
        'at_local': datetime.now().isoformat(timespec='seconds'), 'queue': row,
        'preserved_active_jobs': prior['preserved_active_jobs'], 'deferred_jobs': len(plan['deferred_jobs']),
        'same_required_rounds': list(range(67, 89)), 'original_math_and_source_protocols_unchanged': True,
        'prior_queue_never_activated_a_scientific_job': True, 'queue_RSS_bytes': children[0].memory_info().rss,
        'new_model_fits': 0, 'new_quality_scores': 0, 'test_labels_read': False})
    print(json.dumps({'status': 'passed_live_lightweight_queue_v2', 'queue': row,
                      'host_available_GiB': psutil.virtual_memory().available/2**30}, ensure_ascii=False), flush=True)


if __name__ == '__main__':
    main()
