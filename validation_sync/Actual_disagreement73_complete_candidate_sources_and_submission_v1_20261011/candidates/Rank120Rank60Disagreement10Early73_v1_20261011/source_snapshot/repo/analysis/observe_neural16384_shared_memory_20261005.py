"""Read the positively owned live process and Windows GPU counters twice."""
from pathlib import Path
from datetime import datetime
import hashlib
import json
import subprocess
import sys
import time
import psutil

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
OUT = A / 'neural16384_actual_shared_memory_observation_20261005'


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8-sig'))


def create(path, value):
    with Path(path).open('x', encoding='utf-8') as stream:
        json.dump(value, stream, ensure_ascii=False, indent=2)


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def main():
    assert not OUT.exists()
    OUT.mkdir()
    handoff = A / 'recovery_qualified_workflow_handoff_20261005/verification.json'
    job = read(handoff)['jobs'][0]
    assert job['script_args'][0].endswith('run_neural16384_full_bank_20261005.py')
    root = psutil.Process(job['pid'])
    assert root.cmdline()[-len(job['script_args']):] == job['script_args']
    workers = [p for p in root.children(recursive=True) if p.name().lower() == 'python.exe' and p.cmdline()[1:] == root.cmdline()[1:]]
    assert len(workers) == 1
    worker = workers[0]
    identity = {'root_pid': root.pid, 'root_create_time': root.create_time(),
        'worker_pid': worker.pid, 'worker_create_time': worker.create_time(), 'cmdline': worker.cmdline()}
    inputs = {str(path): sha(path) for path in (Path(__file__), handoff,
        A / 'train_neural16384_full_bank_20261005.py', A / 'run_neural16384_full_bank_20261005.py',
        A / 'neural16384_full_bank_20261005/protocol.json')}
    create(OUT / 'frozen_before_observation.json', {'status': 'frozen_before_live_owned_observation',
        'actual_identity': identity, 'input_sha256': inputs, 'no_training_code_or_process_modified': True})
    observations = []
    for number in range(2):
        assert root.is_running() and worker.is_running()
        assert root.create_time() == identity['root_create_time'] and worker.create_time() == identity['worker_create_time']
        command = "Get-CimInstance -Namespace root\\cimv2 -ClassName Win32_PerfFormattedData_GPUPerformanceCounters_GPUPROCESSMemory | Where-Object { $_.Name -match 'pid_" + str(worker.pid) + "_' } | Select-Object Name,DedicatedUsage,SharedUsage,TotalCommitted | ConvertTo-Json -Depth 3 -Compress"
        result = subprocess.run(['powershell.exe', '-NoProfile', '-NonInteractive', '-Command', command],
            capture_output=True, text=True, encoding='utf-8', timeout=20, creationflags=subprocess.CREATE_NO_WINDOW)
        assert result.returncode == 0 and result.stdout.strip(), result.stderr
        counters = json.loads(result.stdout)
        counters = counters if isinstance(counters, list) else [counters]
        assert all(f'pid_{worker.pid}_' in row['Name'] for row in counters)
        sample = read_last_resource(A / 'neural16384_full_bank_20261005/actual_full_training_resource_samples.jsonl')
        assert sample['pid'] == worker.pid
        observations.append({'at_local': datetime.now().isoformat(), 'monotonic': time.monotonic(),
            'owned_process_cpu_seconds': sum(worker.cpu_times()[:2]), 'owned_process_rss_bytes': worker.memory_info().rss,
            'Windows_per_process_GPU_memory_counters': counters, 'latest_resource_sample': sample,
            'training_stdout_last_lines': Path(job['stdout']).read_text(encoding='utf-8').splitlines()[-4:],
            'training_stderr': Path(job['stderr']).read_text(encoding='utf-8')})
        create(OUT / f'observation_{number+1}.json', observations[-1])
        if number == 0:
            time.sleep(30)
    assert not any(row['training_stderr'] for row in observations)
    assert observations[1]['owned_process_cpu_seconds'] > observations[0]['owned_process_cpu_seconds']
    assert observations[1]['latest_resource_sample']['monotonic_seconds'] > observations[0]['latest_resource_sample']['monotonic_seconds']
    assert all(sha(path) == digest for path, digest in inputs.items())
    elapsed = observations[1]['monotonic'] - observations[0]['monotonic']
    report = {'status': 'passed_live_owned_training_cpu_and_resource_progress_observed',
        'at_local': datetime.now().isoformat(), 'actual_identity': identity, 'source_sha256': inputs,
        'observation_seconds': elapsed,
        'actual_process_CPU_seconds_increase': observations[1]['owned_process_cpu_seconds'] - observations[0]['owned_process_cpu_seconds'],
        'Windows_reported_shared_usage_bytes': [sum(c['SharedUsage'] for c in row['Windows_per_process_GPU_memory_counters']) for row in observations],
        'shared_GPU_memory_report_does_not_prove_OOM_or_full_training_feasibility': True,
        'native_training_logger_prints_only_epoch1_and_multiples_of4': True,
        'interpretation': 'The owned fit remains live and computing; Windows reports shared GPU memory. Resource-aware training layouts merit direct GPU measurement after this fit closes.',
        'no_native_training_or_RNG_or_source_or_epoch_budget_modified': True,
        'new_model_fits': 0, 'new_quality_scores': 0, 'test_labels_read': False,
        'physical_resource_exhaustion_established': False,
        'counter_semantics_reference': 'https://devblogs.microsoft.com/directx/gpus-in-the-task-manager/'}
    create(OUT / 'verification.json', report)
    print(json.dumps({key: report[key] for key in ('status', 'observation_seconds', 'actual_process_CPU_seconds_increase', 'Windows_reported_shared_usage_bytes')}), flush=True)


def read_last_resource(path):
    # Only read the append log tail; avoid hashing or copying an open live log.
    with Path(path).open('rb') as stream:
        stream.seek(0, 2)
        size = stream.tell()
        stream.seek(max(0, size - 16384))
        lines = stream.read().splitlines()
    for line in reversed(lines):
        try:
            return json.loads(line)
        except json.JSONDecodeError:
            continue
    raise AssertionError('No complete current resource row.')


if __name__ == '__main__':
    main()
