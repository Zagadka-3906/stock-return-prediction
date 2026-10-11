"""Keep original unfinished scientific jobs queued without heavy waiting imports."""
from pathlib import Path
from datetime import datetime
import hashlib
import json
import os
import sys
import time

import psutil
from windows_hidden_process_launch_20261006 import launch
from atomic_optimization_observer_writes_20261005 import write

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8-sig'))


def sha(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def create(path, value):
    with Path(path).open('x', encoding='utf-8') as stream:
        json.dump(value, stream, ensure_ascii=False, indent=2)
        stream.write('\n')


def owned(row):
    try:
        worker = psutil.Process(row['owned_worker_pid'])
        return worker.create_time() == row['owned_worker_creation_time'] and worker.cmdline()[-len(row['script_args']):] == row['script_args']
    except psutil.Error:
        return False


def marker(path, statuses=None):
    path = Path(path)
    if not path.exists():
        return False
    return statuses is None or read(path).get('status') in statuses


def ready(job, jobs):
    gate = job['gate']
    if any(not marker(row['path'], row.get('statuses')) for row in gate.get('markers', [])):
        return False
    if any(owned(jobs[name]) for name in gate.get('closed_jobs', []) if name in jobs):
        return False
    if gate.get('parent'):
        number = gate['parent']
        result = ROOT / f'results/optimization_20261003_r{number}.json'
        folder = A / f'optimization_20261003_r{number}'
        candidate = ROOT / f'candidates/optimization_20261003_r{number}/verification.json'
        if not marker(result, ['complete']) or not marker(candidate, ['passed']):
            return False
        if not marker(folder / 'provenance_scope_execution.json', ['passed']):
            return False
    if gate.get('quality_slot'):
        if any(owned(row) for name, row in jobs.items() if name.startswith('round') and name != job['name']):
            return False
    return True


def spawn(job, plan, plan_path):
    output = plan_path.parent / 'activated_jobs' / job['name']
    output.mkdir(parents=True)
    old_run = read(job['previous_run'])
    run = dict(old_run)
    run['input_sha256'] = {**old_run['input_sha256'], **plan['input_sha256'], str(plan_path): sha(plan_path)}
    run.update(dependency_queue_plan=str(plan_path), heavy_scientific_imports_deferred_until_original_prerequisites=True)
    run_path = output / 'run.json'
    create(run_path, run)
    scratch = job.get('scratch', str(ROOT / 'tmp/dependency_queue_20261006'))
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
           'owned_worker_pid': children[0].pid, 'owned_worker_creation_time': children[0].create_time(),
           'stdout': str(output / 'stdout.log'), 'stderr': str(output / 'stderr.log'),
           'at_local': datetime.now().isoformat(timespec='seconds'),
           'original_script': old_run['original_script'], 'original_arguments': old_run['original_arguments']}
    if 'round' in job:
        row.update(round=job['round'], explicit_parent_round=job['gate']['parent'], prospective_official_workers=1)
    create(output / 'launch.json', row)
    return row


def main():
    plan_path = Path(sys.argv[1]).resolve()
    plan = read(plan_path)
    for name, digest in plan['input_sha256'].items():
        assert sha(name) == digest, name
    activated = dict(plan.get('previously_activated_jobs', {}))
    jobs = {**plan['preserved_active_jobs'], **activated}
    state_path = plan_path.parent / 'state.json'
    while True:
        for job in plan['deferred_jobs']:
            name = job['name']
            if name in activated or not ready(job, jobs):
                continue
            # The unchanged original driver performs the complete qualified-parent,
            # immutable-source, maturity and native-proof checks before real work.
            row = spawn(job, plan, plan_path)
            jobs[name] = activated[name] = row
            if 'round' in job:
                rows = read(plan['registry'])
                rows = [row if item['round'] == job['round'] else item for item in rows]
                write(plan['registry'], rows)
            print(json.dumps({'status': 'original_frozen_job_activated', **row}, ensure_ascii=False), flush=True)
        statuses = {name: {'owned_live': owned(row), 'pid': row['owned_worker_pid']}
                    for name, row in jobs.items()}
        write(state_path, {'status': 'waiting_or_executing_original_dependencies',
            'at_local': datetime.now().isoformat(timespec='seconds'), 'pid': os.getpid(),
            'deferred_jobs_remaining': [job['name'] for job in plan['deferred_jobs'] if job['name'] not in activated],
            'activated_jobs': activated, 'job_ownership': statuses,
            'own_RSS_bytes': psutil.Process().memory_info().rss,
            'host_available_bytes': psutil.virtual_memory().available,
            'original_required_rounds_retained': list(range(67, 91)),
            'new_model_fits_by_scheduler': 0, 'new_quality_scores_by_scheduler': 0,
            'global_resource_boundary_established': False, 'test_labels_read': False})
        if len(activated) == len(plan['deferred_jobs']) and not any(owned(row) for row in activated.values()):
            return
        time.sleep(10)


if __name__ == '__main__':
    from run_dependency_queue_v2_20261006 import ready as recovered_ready
    ready = recovered_ready
    main()
