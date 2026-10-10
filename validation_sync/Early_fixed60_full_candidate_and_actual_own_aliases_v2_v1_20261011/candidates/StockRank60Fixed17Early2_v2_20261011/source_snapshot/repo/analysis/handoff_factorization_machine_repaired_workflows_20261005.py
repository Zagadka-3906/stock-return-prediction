"""Replace only owned idle FM waiters/publishers and the operational observer."""
from pathlib import Path
import datetime
import hashlib
import json
import os
import subprocess

import psutil

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
OUT = A / 'factorization_machine_v4_workflow_handoff_20261005'


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8-sig'))


def sha(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def create(path, payload):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with Path(path).open('x', encoding='utf-8') as stream:
        json.dump(payload, stream, ensure_ascii=False, indent=2)


def processes(job):
    parent = psutil.Process(job['pid'])
    assert job['script'] in parent.cmdline()
    command = parent.cmdline()
    children = parent.children(recursive=True)
    workers = [p for p in children if p.name().lower() == 'python.exe' and p.cmdline()[1:] == command[1:]]
    assert len(workers) == 1
    assert all(p.pid == workers[0].pid or p.name().lower() == 'conhost.exe' for p in children)
    return workers[0], parent


def stop(job):
    owned = processes(job)
    saved = [{'pid': p.pid, 'create_time': p.create_time(), 'cmdline': p.cmdline()} for p in owned]
    paused = []
    try:
        for process in owned:
            process.suspend()
            paused.append(process)
        processes(job)
        for process in owned:
            process.terminate()
        _, alive = psutil.wait_procs(owned, timeout=10)
        assert not alive
    finally:
        for process in reversed(paused):
            if process.is_running():
                process.resume()
    return saved


def launch(script, label, env):
    stdout, stderr = A / f'run_logs/{label}.stdout.log', A / f'run_logs/{label}.stderr.log'
    with stdout.open('xb') as output, stderr.open('xb') as error:
        process = subprocess.Popen([str(ROOT / '.venv/Scripts/python.exe'), '-B', '-X', 'utf8', str(script)],
            cwd=ROOT, env=env, stdout=output, stderr=error, creationflags=subprocess.CREATE_NO_WINDOW)
    return {'pid': process.pid, 'script': str(script), 'script_args': [],
            'stdout': str(stdout), 'stderr': str(stderr), 'at_local': datetime.datetime.now().isoformat()}


def main():
    assert not (OUT / 'verification.json').exists()
    gen = A / 'factorization_machine_search_generator_preflight_v4_20261005/verification.json'
    direct = A / 'factorization_machine_direct_router_preflight_v2_20261005/verification.json'
    assert read(gen)['status'] == read(direct)['status'] == 'passed'
    assert [r['generated_records'] for r in read(gen)['controls']] == [124, 138, 138]
    for proof in (read(gen), read(direct)):
        for path, expected in proof['source_sha256'].items():
            assert sha(path) == expected, path
    future = read(A / 'factorization_machine_future_launch_v2_20261005.json')
    assert future['script'] in psutil.Process(future['pid']).cmdline()
    old_receipt = read(A / 'factorization_machine_followup_launch_receipt_20261005.json')
    old_quality = old_receipt['quality_rounds']
    for job in old_quality:
        number = job['round']
        assert not (A / f'optimization_20261003_r{number}/protocol.json').exists()
        assert read(A / f'ongoing_optimization_r{number}_state.json')['stage'].startswith('waiting')
        processes(job)
    registry_path = A / 'resumed_rounds_nystrom_locked_20261004.json'
    for number in range(63, 75):
        protocol = A / f'optimization_20261003_r{number}/protocol.json'
        if protocol.exists():
            assert str(registry_path) not in read(protocol)['input_sha256']
    old_publisher = read(A / 'factorization_machine_native_github_run_20261005.json')
    old_monitor = read(A / 'actual_optimization_monitor_run_v8_20261005.json')
    assert not (A / 'factorization_machine_future_qa_20261005/verification.json').exists()
    processes(old_publisher)
    processes(old_monitor)
    bindings = {str(path): sha(path) for path in (Path(__file__), gen, direct,
        A / 'factorization_machine_future_run_v2_20261005.json',
        A / 'factorization_machine_future_launch_v2_20261005.json',
        A / 'factorization_machine_followup_launch_receipt_20261005.json',
        A / 'factorization_machine_native_github_run_20261005.json',
        A / 'actual_optimization_monitor_run_v8_20261005.json')}
    create(OUT / 'frozen_before_handoff.json', {
        'status': 'frozen_before_owned_unstarted_workflow_handoff',
        'input_sha256': bindings, 'old_quality_jobs': old_quality,
        'old_publisher': old_publisher, 'old_monitor': old_monitor,
        'actual_scored_records_before_handoff': {'73': 0, '74': 0},
        'R65_and_other_live_scientific_jobs_untouched': True,
        'actual30_annual_models_and_existing_final_artifact_preserved': True,
        'new_quality_scores': 0, 'test_labels_read': False})
    for name in ('actual_optimization_monitor_state_20261005.json', 'ongoing_optimization_r73_state.json',
                 'ongoing_optimization_r74_state.json', 'factorization_machine_native_github_state_20261005.json'):
        (OUT / f'prior_{name}').write_bytes((A / name).read_bytes())
    stopped = []
    for job in (*old_quality, old_publisher, old_monitor):
        stopped.extend(stop(job))
    sources = set(A.glob('*factorization_machine*20261005.py'))
    sources.update(A / f'{prefix}{n}{suffix}.py' for n in (73, 74)
        for prefix, suffix in (('optimize_training_round', '_v4'), ('finalize_training_round', ''),
                              ('run_training_round', '_v4_pipeline')))
    sources.update((gen, direct, A / 'factorization_machine_complete_search_plan_20261005.json',
                    A / 'factorization_machine_future_run_v2_20261005.json'))
    quality_inputs = {str(path): sha(path) for path in sources}
    create(A / 'factorization_machine_quality_run_v4_20261005.json', {
        'status': 'frozen_before_corrected_direct_router_full_scheme_waiters',
        'input_sha256': quality_inputs, 'planned_records': {'73': 124, '74': 138},
        'qualified_actual_predecessors72_73_still_required': True,
        'actual30_annual6_final_fullfuture_controls_required': True,
        'original_v3_sources_and_runs_preserved': True, 'new_quality_scores': 0, 'test_labels_read': False})
    storage = read(A / 'factorization_machine_storage_20261005.json')
    env = dict(os.environ)
    for variable in ('TMP', 'TEMP', 'TMPDIR'):
        env[variable] = storage['temporary_directory']
    for variable in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS', 'POLARS_MAX_THREADS'):
        env[variable] = '8'
    records = []
    for number, expected in ((73, 124), (74, 138)):
        job = launch(A / f'run_training_round{number}_v4_pipeline.py', f'round{number}_factorization_machine_v4_20261005', env)
        records.append({'round': number, **job, 'expected_scored_records': expected,
                        'status': 'waiting_for_actual_native_fullfuture_and_qualified_predecessor'})
    registry = [job for job in read(registry_path) if job['round'] not in (73, 74)] + records
    temporary = registry_path.with_suffix('.fm_v4_handoff.tmp')
    temporary.write_text(json.dumps(registry, ensure_ascii=False, indent=2), encoding='utf-8')
    temporary.replace(registry_path)
    publisher_script = A / 'publish_factorization_machine_completed_native_v2_20261005.py'
    publisher_inputs = {str(p): sha(p) for p in (publisher_script, Path(__file__),
        A / 'watch_validations_main_v2_20261005.py', A / 'sync_validated_rounds_main_20261005.py', direct,
        A / 'factorization_machine_future_run_v2_20261005.json')}
    # The publisher waits for this immutable run record before taking any action.
    publisher = launch(publisher_script, 'factorization_machine_native_github_v2_20261005', env)
    create(A / 'factorization_machine_native_github_run_v2_20261005.json', {
        **publisher, 'input_sha256': publisher_inputs, 'only_publication_branch': 'main',
        'completed_annual_receipt_reused': True, 'new_quality_scores': 0, 'test_labels_read': False})
    monitor_script = A / 'monitor_actual_optimization_progress_v9_20261005.py'
    monitor_inputs = dict(old_monitor['input_sha256'])
    monitor_inputs.update({str(p): sha(p) for p in (monitor_script, Path(__file__),
        A / 'refresh_optimization_boundary_evidence_v8_20261005.py', gen, direct,
        A / 'factorization_machine_future_launch_v2_20261005.json')})
    monitor = launch(monitor_script, 'actual_optimization_monitor_v9_20261005', env)
    create(A / 'actual_optimization_monitor_run_v9_20261005.json', {
        **monitor, 'input_sha256': monitor_inputs, 'monitors_through_actual_qualified_round': 74,
        'goal_completion_not_inferred': True})
    for path, expected in bindings.items():
        assert sha(path) == expected, path
    result = {'status': 'passed_owned_idle_workflow_handoff',
              'at_local': datetime.datetime.now().isoformat(), 'stopped_owned_processes': stopped,
              'future_recovery': future, 'quality_rounds': records, 'native_publisher': publisher,
              'operational_monitor': monitor, 'only_publication_branch': 'main',
              'R65_and_other_live_scientific_jobs_untouched': True,
              'new_model_fits_by_handoff': 0, 'new_quality_scores': 0, 'test_labels_read': False}
    create(OUT / 'verification.json', result)
    print(json.dumps({'status': result['status'], 'quality_pids': [r['pid'] for r in records],
                      'publisher_pid': publisher['pid'], 'monitor_pid': monitor['pid']}, ensure_ascii=False), flush=True)


if __name__ == '__main__':
    main()
