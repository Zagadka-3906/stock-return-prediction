"""Restore all required unfinished jobs after positively verified process loss."""
from pathlib import Path
from datetime import datetime
import hashlib
import json
import os
import subprocess
import sys
import time

import psutil

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
OUT = A / 'system_reboot_workflow_recovery_20261006'
DRIVER = A / 'run_reboot_recovery_attempt_20261006.py'
PYTHON = ROOT / '.venv/Scripts/python.exe'
REGISTRY = A / 'resumed_rounds_reboot_20261006.json'


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8-sig'))


def sha(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def create(path, value):
    with Path(path).open('x', encoding='utf-8') as stream:
        json.dump(value, stream, ensure_ascii=False, indent=2)
        stream.write('\n')


def now():
    return datetime.now().isoformat(timespec='seconds')


def owned(row):
    try:
        process = psutil.Process(row['pid'])
        command = process.cmdline()
        return str(row['script']) in command and command[-len(row.get('script_args', [])):] == row.get('script_args', []) if row.get('script_args') else str(row['script']) in command
    except (psutil.NoSuchProcess, psutil.AccessDenied):
        return False


def main():
    assert not OUT.exists(), 'Preserve all previous recovery attempts.'
    OUT.mkdir()
    original_registry = read(A / 'resumed_rounds_nystrom_locked_20261004.json')
    specifications = []
    bridge = A / 'run_recovery_qualified_workflow_20261005.py'
    # Wide native training remains the original full 168,894,465-parameter fit.
    specifications.append({'name': 'neural16384_annual', 'pid': 31336, 'script': str(bridge),
        'script_args': [str(A / 'run_neural16384_full_bank_20261005.py'),
                        str(A / 'recovery_qualified_workflow_handoff_20261005/neural16384_annual_run.json')],
        'separate_resource_recorder': {'module': 'neural16384_actual_resource_recorder_20261005',
            'class': 'ActualResourceRecorder', 'original_output': str(A / 'neural16384_full_bank_20261005')}})
    specifications.append({'name': 'neural16384_future', 'pid': 31760,
        'script': str(A / 'verify_neural16384_full_future_20261005.py'), 'script_args': []})
    robust = read(A / 'streaming_robust_regression_followups_20261005/verification.json')
    for row in robust['native_jobs']:
        spec = {**row, 'name': 'robust_' + row['kind']}
        if row['kind'] == 'annual':
            spec['separate_resource_recorder'] = {
                'module': 'streaming_rank_classifier_actual_resource_recorder_20261005',
                'class': 'ActualCPUResourceRecorder', 'original_output': str(A / 'streaming_robust_regression_bank_20261005')}
        specifications.append(spec)
    # Resume the ready independent quality branch as well as original rounds 67-80.
    for row in original_registry:
        if row['round'] >= 67 and not (ROOT / f'results/optimization_20261003_r{row["round"]}.json').exists():
            specifications.append({**row, 'name': f'round{row["round"]}'})
    for family, filename in (
        ('gradient_sampling', 'gradient_sampling_followups_20261005/verification.json'),
        ('memory_efficient_neural', 'memory_efficient_neural_followups_20261005/verification.json')):
        for kind in ('native', 'future'):
            row = read(A / filename)[kind]
            specifications.append({**row, 'name': family + '_' + kind})
    specifications.append({**read(A / 'memory_efficient_mlp_gpu_recovery_v2_20261005/verification.json')['job'],
                           'name': 'memory_efficient_gpu_controls'})
    publisher = read(A / 'github_validation_sync_main_20261005/launch_v3.json')['publisher']
    specifications.append({**publisher, 'name': 'main_publisher'})
    specifications.append({**read(A / 'actual_optimization_monitor_launch_v18_20261005.json'),
                           'name': 'progress_monitor'})
    assert all(not owned(row) for row in specifications), 'A matching live job must not be duplicated.'
    boot = psutil.boot_time()
    assert boot > datetime.fromisoformat('2026-10-05T23:50:00').timestamp()
    old_resources = {}
    for family, filename in (
            ('robust', 'streaming_robust_regression_bank_20261005/actual_cpu_resource_samples.jsonl'),
            ('wide', 'neural16384_full_bank_20261005/actual_full_training_resource_samples.jsonl')):
        path = A / filename
        old_resources[family] = {'path': str(path), 'bytes': path.stat().st_size, 'sha256': sha(path)}
    completed = {}
    for family in ('streaming_robust_regression_bank_20261005', 'neural16384_full_bank_20261005'):
        for info_path in (A / family).glob('*/info_202[0-4].json'):
            info = read(info_path)
            model = info_path.with_name(info_path.name.replace('info_', 'model_')).with_suffix('.joblib')
            raw = info_path.with_name(info_path.name.replace('info_', 'raw_')).with_suffix('.parquet')
            assert sha(model) == info['model_sha256'] and sha(raw) == info['prediction_sha256']
            completed[str(info_path)] = {'sha256': sha(info_path), 'model_sha256': info['model_sha256'],
                                        'prediction_sha256': info['prediction_sha256']}
    partial_path = A / 'optimization_20261003_r81/wave325_results.json'
    partial = read(partial_path)
    assert partial['status'] == 'running' and len(partial['results']) == 71
    create(OUT / 'original_round81_partial_results.json', partial)
    frozen = {'status': 'frozen_before_restart_of_verified_absent_jobs', 'at_local': now(),
        'host_boot_at_local': datetime.fromtimestamp(boot).isoformat(timespec='seconds'),
        'source_sha256': {str(Path(__file__).resolve()): sha(__file__), str(DRIVER): sha(DRIVER)},
        'old_registry_sha256': sha(A / 'resumed_rounds_nystrom_locked_20261004.json'),
        'required_rounds': list(range(67, 89)), 'completed_native_artifacts_reverified': completed,
        'old_interrupted_resource_samples': old_resources, 'jobs': specifications,
        'original_round81_completed_records': 71, 'new_quality_scores_at_freeze': 0,
        'partial_unsaved_epochs_must_restart_full_original_fit': True,
        'original_sources_protocols_and_history_not_overwritten': True,
        'test_labels_read': False}
    create(OUT / 'frozen_before_recovery.json', frozen)
    resumed, old_rows = [], {row['round']: row for row in original_registry}
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1', PYTHONUTF8='1',
               OMP_NUM_THREADS='8', OPENBLAS_NUM_THREADS='8', MKL_NUM_THREADS='8', POLARS_MAX_THREADS='8')
    for spec in specifications:
        directory = OUT / spec['name']
        directory.mkdir()
        script = Path(spec['script'])
        args = spec.get('script_args', [])
        inputs = {str(script): sha(script), str(Path(__file__).resolve()): sha(__file__)}
        for value in args:
            path = Path(value)
            if path.is_file():
                inputs[str(path)] = sha(path)
        record = {'name': spec['name'], 'original_script': str(script), 'original_arguments': args,
            'input_sha256': inputs, 'recovery_driver_sha256': sha(DRIVER),
            'original_pid_confirmed_not_owned': spec['pid'],
            'separate_resource_recorder': spec.get('separate_resource_recorder'),
            'host_boot_at_local': frozen['host_boot_at_local'], 'new_model_fits_by_launcher': 0,
            'new_quality_scores_by_launcher': 0, 'test_labels_read': False}
        run_path = directory / 'run.json'
        create(run_path, record)
        stdout, stderr = directory / 'stdout.log', directory / 'stderr.log'
        with stdout.open('xb') as out, stderr.open('xb') as err:
            process = subprocess.Popen([str(PYTHON), '-B', '-X', 'utf8', str(DRIVER), str(run_path)],
                cwd=ROOT, env=env, stdout=out, stderr=err,
                creationflags=subprocess.CREATE_NO_WINDOW | subprocess.DETACHED_PROCESS)
        time.sleep(.8)
        assert process.poll() is None, stderr.read_text(encoding='utf-8')[-3000:]
        parent = psutil.Process(process.pid)
        children = [child for child in parent.children(recursive=True)
                    if child.name().lower() == 'python.exe' and child.cmdline()[1:] == parent.cmdline()[1:]]
        assert len(children) == 1, spec['name']
        row = {'name': spec['name'], 'pid': process.pid, 'script': str(DRIVER), 'script_args': [str(run_path)],
            'owned_worker_pid': children[0].pid, 'owned_worker_creation_time': children[0].create_time(),
            'stdout': str(stdout), 'stderr': str(stderr), 'at_local': now(),
            'original_script': str(script), 'original_arguments': args}
        if 'round' in spec:
            row.update(round=spec['round'], explicit_parent_round=spec.get('explicit_parent_round', spec['round']-1),
                       prospective_official_workers=spec.get('prospective_official_workers', 1))
            old_rows[spec['round']] = row
        resumed.append(row)
        create(directory / 'launch.json', row)
        print(json.dumps({'status': 'owned_recovery_job_live', **row}, ensure_ascii=False), flush=True)
    create(REGISTRY, [old_rows[n] for n in sorted(old_rows)])
    # These are mutable operational pointers; scientific protocols remain unchanged.
    from atomic_optimization_observer_writes_20261005 import write
    for filename in ('ongoing_optimization_state.json', 'resume_optimization_20261004.json'):
        path = A / filename
        state = read(path)
        state['active_run_registry'] = REGISTRY.relative_to(ROOT).as_posix()
        state['verified_reboot_recovery'] = (OUT / 'frozen_before_recovery.json').relative_to(ROOT).as_posix()
        write(path, state)
    for row in resumed:
        assert owned(row), row['name']
    for row in old_resources.values():
        assert sha(row['path']) == row['sha256'], row['path']
    proof = {'status': 'passed_all_required_absent_workflows_relaunched_and_positively_owned',
        'at_local': now(), 'jobs': resumed, 'required_rounds': list(range(67, 89)),
        'completed_full_annual_artifacts_reused': len(completed), 'retained_round81_official_records': 71,
        'original_resource_samples_SHA256_unchanged': True, 'registry': str(REGISTRY),
        'new_model_fits_by_launcher': 0, 'new_quality_scores_by_launcher': 0,
        'goal_complete': False, 'physical_resource_boundary_established': False, 'test_labels_read': False}
    create(OUT / 'verification.json', proof)
    print(json.dumps({'status': proof['status'], 'live_jobs': len(resumed),
                      'reused_annual_artifacts': len(completed)}, ensure_ascii=False), flush=True)


if __name__ == '__main__':
    main()
