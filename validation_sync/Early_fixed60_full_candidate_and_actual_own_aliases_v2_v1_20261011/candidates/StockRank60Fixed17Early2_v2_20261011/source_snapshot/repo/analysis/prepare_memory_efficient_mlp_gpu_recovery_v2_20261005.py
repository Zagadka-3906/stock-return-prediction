"""Preserve the terminal pre-fit error and validate actual waiter dependencies."""
from pathlib import Path
from datetime import datetime
import hashlib
import importlib.util
import json
import os
import subprocess
import sys
import time
import psutil

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path[:0] = [str(ROOT), str(A)]


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8-sig'))


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def create(path, value):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with Path(path).open('x', encoding='utf-8') as stream:
        json.dump(value, stream, ensure_ascii=False, indent=2)


def main():
    out = A / 'memory_efficient_mlp_gpu_recovery_v2_20261005'
    assert not out.exists()
    out.mkdir()
    old_launch = A / 'memory_efficient_mlp_followup_launch_20261005.json'
    old = read(old_launch)['job']
    for process in psutil.process_iter(['pid', 'cmdline']):
        assert old['script'] not in (process.info['cmdline'] or []), 'The original task is still live; never duplicate it.'
    error = Path(old['stderr']).read_text(encoding='utf-8')
    assert "KeyError: 'native_future'" in error
    old_run_path = Path(old['run'])
    old_run = read(old_run_path)
    for source, expected in old_run['input_sha256'].items():
        assert sha(source) == expected, source
    storage = read(A / 'memory_efficient_mlp_storage_20261005.json')
    assert not Path(storage['GPU_control_directory']).exists()
    create(out / 'original_failure_retained.json', {'status': 'verified_terminal_before_any_GPU_fit',
        'old_job': old, 'error': error, 'original_error_sha256': sha(old['stderr']),
        'old_run_sha256': sha(old_run_path), 'original_sources_preserved': True,
        'actual_GPU_fits': 0, 'new_quality_scores': 0})
    old_source = Path(old['script'])
    source = old_source.read_text(encoding='utf-8')
    assert source.count("['native_future']") == 1
    source = source.replace("['native_future']", "['future']")
    source = source.replace('memory_efficient_mlp_gpu_control_run_20261005.json', 'memory_efficient_mlp_gpu_control_run_v2_20261005.json')
    source = source.replace('memory_efficient_mlp_gpu_control_state_20261005.json', 'memory_efficient_mlp_gpu_control_state_v2_20261005.json')
    driver = A / 'run_memory_efficient_mlp_gpu_controls_v2_20261005.py'
    with driver.open('x', encoding='utf-8', newline='\n') as stream:
        stream.write(source)
    spec = importlib.util.spec_from_file_location('memory_gpu_actual_waiter_preflight_v2', driver)
    actual = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(actual)
    annual_job = read(A / 'recovery_qualified_workflow_handoff_20261005/verification.json')['jobs'][0]
    final_job = read(A / 'neural16384_full_followup_launch_receipt_20261005.json')['future']
    assert actual.owned_live(annual_job) and actual.owned_live(final_job)
    assert actual.original_gpu_work_closed() is False
    assert psutil.Process(annual_job['pid']).cmdline()[-len(annual_job['script_args']):] == annual_job['script_args']
    assert final_job['script'] in psutil.Process(final_job['pid']).cmdline()
    proof = out / 'actual_waiter_preflight.json'
    create(proof, {'status': 'passed_actual_annual_and_final_registry_dispatch_and_live_wait',
        'source_sha256': {str(path): sha(path) for path in (Path(__file__), driver,
            A / 'recovery_qualified_workflow_handoff_20261005/verification.json',
            A / 'neural16384_full_followup_launch_receipt_20261005.json')},
        'actual_live_annual_root': annual_job['pid'], 'actual_live_final_waiter_root': final_job['pid'],
        'actual_waiter_returns_not_closed': True, 'new_GPU_fits': 0})
    run_path = A / 'memory_efficient_mlp_gpu_control_run_v2_20261005.json'
    run = dict(old_run)
    run['input_sha256'] = {**old_run['input_sha256'],
        **{str(path): sha(path) for path in (driver, Path(__file__), proof, out / 'original_failure_retained.json')}}
    run.update(status='frozen_before_actual_registry_verified_GPU_control_waiter',
        previous_terminal_attempt_preserved=True, actual_annual_and_final_waiter_dispatch_preflight_passed=True)
    create(run_path, run)
    env = dict(os.environ)
    env.pop('CUDA_VISIBLE_DEVICES', None)
    for key in ('TMP', 'TEMP', 'TMPDIR'):
        env[key] = storage['temporary_directory']
    stdout = A / 'run_logs/memory_efficient_mlp_gpu_controls_v2_20261005.stdout.log'
    stderr = A / 'run_logs/memory_efficient_mlp_gpu_controls_v2_20261005.stderr.log'
    with stdout.open('xb') as output_log, stderr.open('xb') as error_log:
        process = subprocess.Popen([str(ROOT / '.venv/Scripts/python.exe'), '-B', '-X', 'utf8', str(driver)],
            cwd=ROOT, env=env, stdout=output_log, stderr=error_log, creationflags=subprocess.CREATE_NO_WINDOW)
    job = {'pid': process.pid, 'script': str(driver), 'script_args': [], 'run': str(run_path),
        'stdout': str(stdout), 'stderr': str(stderr), 'at_local': datetime.now().isoformat()}
    create(out / 'launch.json', {'status': 'launched_owned_actual_registry_verified_GPU_waiter', 'job': job})
    time.sleep(5)
    assert str(driver) in psutil.Process(process.pid).cmdline()
    assert not stderr.read_text(encoding='utf-8')
    assert read(A / 'memory_efficient_mlp_gpu_control_state_v2_20261005.json')['stage'].startswith('waiting')
    create(out / 'verification.json', {'status': 'passed_actual_waiter_dispatch_and_owned_deferred_GPU_controls',
        'job': job, 'source_sha256': {str(path): sha(path) for path in (driver, run_path, Path(__file__), proof)},
        'original_terminal_attempt_sources_RUN_and_error_preserved': True,
        'current_native_training_and_final_waiter_untouched': True, 'new_GPU_fits': 0,
        'full_native_and_official_quality_sources_still_pending': True, 'new_quality_scores': 0,
        'test_labels_read': False})
    print(json.dumps({'status': 'passed', 'actual_owned_GPU_control_root_pid': process.pid,
        'actual_original_GPU_work_verified_waiting': True}), flush=True)


if __name__ == '__main__':
    main()
