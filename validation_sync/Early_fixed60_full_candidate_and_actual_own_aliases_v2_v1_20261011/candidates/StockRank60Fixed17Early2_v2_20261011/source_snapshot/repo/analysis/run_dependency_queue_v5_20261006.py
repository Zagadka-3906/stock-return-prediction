"""Preserve every original waiting workflow and use tested exact rank execution for unstarted rounds."""
from pathlib import Path
from copy import deepcopy
import json
import os
import sys
import time

import psutil
import run_dependency_queue_v3_20261006 as previous
from windows_hidden_process_launch_20261006 import launch

ROOT, A = previous.ROOT, previous.A
original_ready = previous.ready
_ACTIVATION_COMMIT = None


def ready(job, jobs):
    if _ACTIVATION_COMMIT is not None and not _ACTIVATION_COMMIT.exists():
        return False
    gate = job['gate']
    if any(not previous.marker(row['path'], row.get('statuses')) for row in gate.get('markers', [])):
        return False
    if any(previous.owned(jobs[name]) for name in gate.get('closed_jobs', []) if name in jobs):
        return False
    if gate.get('quality_slot') and psutil.virtual_memory().available < 8 * 1024**3:
        return False
    if gate.get('quality_slot') and any(previous.owned(row) for name, row in jobs.items()
                                       if name.startswith('round') and name != job['name']):
        return False
    number = gate.get('parent')
    if number in (66, 81):
        import qualified_round_recovery_evidence_v3_20261006 as qualification
        try:
            return qualification.complete_round_evidence(number) is not None
        finally:
            qualification.close()
    return original_ready(job, jobs)


def original_driver_and_bridge(job, old_run):
    script = Path(old_run['original_script']).resolve()
    if script.name.startswith('run_recovery_qualified_workflow_'):
        old_driver, old_bridge_run, *arguments = old_run['original_arguments']
        bridge = deepcopy(previous.read(old_bridge_run))
        assert bridge['original_driver'] == old_driver and bridge['original_arguments'] == arguments
        return old_driver, arguments, bridge, Path(old_bridge_run).resolve()
    assert script.parent == A and script.name.startswith(f'run_training_round{job["round"]}') and script.name.endswith('_pipeline.py')
    arguments = deepcopy(old_run['original_arguments'])
    bridge = {'round': job['round'], 'original_driver': str(script), 'original_arguments': arguments,
        'input_sha256': deepcopy(old_run['input_sha256']), 'previous_direct_workflow_run': job['previous_run']}
    return str(script), arguments, bridge, None


def spawn(job, plan, plan_path):
    output = plan_path.parent / 'activated_jobs' / job['name']
    output.mkdir(parents=True)
    old_run = previous.read(job['previous_run'])
    run = deepcopy(old_run)
    bindings = {**old_run['input_sha256'], **plan['input_sha256'],
        str(plan_path): previous.sha(plan_path), str(Path(job['previous_run']).resolve()): previous.sha(job['previous_run'])}
    if _ACTIVATION_COMMIT is not None:
        assert previous.read(_ACTIVATION_COMMIT)['status'] == 'retired_original_controller_and_preserved_scientific_workers'
        bindings[str(_ACTIVATION_COMMIT)] = previous.sha(_ACTIVATION_COMMIT)
    if 'round' in job:
        assert not (A / f'optimization_20261003_r{job["round"]}/protocol.json').exists(), 'Only unstarted and unfrozen rounds can adopt this execution path.'
        old_driver, arguments, bridge, old_bridge_run = original_driver_and_bridge(job, old_run)
        bridge.update(round=job['round'], previous_recovery_run=str(old_bridge_run) if old_bridge_run else None,
                      original_full_scientific_grid_and_arguments_preserved=True)
        bridge['input_sha256'] = {**bridge['input_sha256'], **bindings}
        if old_bridge_run is not None:
            bridge['input_sha256'][str(old_bridge_run)] = previous.sha(old_bridge_run)
        bridge_path = output / 'qualified_run.json'
        previous.create(bridge_path, bridge)
        bindings[str(bridge_path)] = previous.sha(bridge_path)
        run.update(original_script=str(A / ('run_recovery_qualified_workflow_with_exact_rank_cache_v2_20261006.py'
            if job['round'] in plan['exact_rank_cached_rounds'] else 'run_recovery_qualified_workflow_v2_20261006.py')),
            original_arguments=[old_driver, str(bridge_path), *arguments])
    run['input_sha256'] = bindings
    run.update(dependency_queue_plan=str(plan_path),
        heavy_scientific_imports_deferred_until_original_prerequisites=True,
        prior_attempts_and_original_scientific_sources_preserved=True)
    run_path = output / 'run.json'
    previous.create(run_path, run)
    scratch = job.get('scratch', str(ROOT / 'tmp/dependency_queue_v4_20261006'))
    assert Path(scratch).drive.upper() in ('D:', 'E:')
    Path(scratch).mkdir(parents=True, exist_ok=True)
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1', PYTHONUTF8='1',
        OMP_NUM_THREADS='8', OPENBLAS_NUM_THREADS='8', MKL_NUM_THREADS='8', POLARS_MAX_THREADS='8')
    for key in ('TMP', 'TEMP', 'TMPDIR'):
        env[key] = scratch
    driver = A / 'run_reboot_recovery_attempt_20261006.py'
    with (output / 'stdout.log').open('xb') as out, (output / 'stderr.log').open('xb') as err:
        process = launch([str(ROOT / '.venv/Scripts/python.exe'), '-B', '-X', 'utf8', str(driver), str(run_path)],
                         cwd=ROOT, env=env, stdout=out, stderr=err)
    time.sleep(.5)
    assert process.poll() is None, (output / 'stderr.log').read_text(encoding='utf-8')
    parent = psutil.Process(process.pid)
    children = [child for child in parent.children(recursive=True)
        if child.name().lower() == 'python.exe' and child.cmdline()[1:] == parent.cmdline()[1:]]
    assert len(children) == 1
    row = {'name': job['name'], 'pid': parent.pid, 'script': str(driver), 'script_args': [str(run_path)],
        'owned_parent_creation_time': parent.create_time(),
        'owned_worker_pid': children[0].pid, 'owned_worker_creation_time': children[0].create_time(),
        'stdout': str(output / 'stdout.log'), 'stderr': str(output / 'stderr.log'),
        'original_script': old_run['original_script'], 'original_arguments': old_run['original_arguments'],
        'at_local': time.strftime('%Y-%m-%dT%H:%M:%S'),
        'parent_controller_is_service_owned_and_outside_command_session': True}
    if 'round' in job:
        row.update(round=job['round'], explicit_parent_round=job['gate']['parent'], prospective_official_workers=1)
    previous.create(output / 'launch.json', row)
    return row


def main():
    global _ACTIVATION_COMMIT
    _ACTIVATION_COMMIT = Path(previous.read(Path(sys.argv[1]))['activation_handoff_commit_marker'])
    from hidden_windows_child_creation_20261006 import install
    restore_children = install()
    old_ready, old_spawn = previous.ready, previous.spawn
    previous.ready, previous.spawn = ready, spawn
    try:
        previous.main()
    finally:
        previous.ready, previous.spawn = old_ready, old_spawn
        events = restore_children()
        plan = Path(sys.argv[1]).resolve()
        previous.create(plan.parent / 'queue_hidden_child_process_launches.json',
            {'actual_child_creations': events, 'all_creation_flags_restored': True})


if __name__ == '__main__':
    main()
