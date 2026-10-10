"""Measure the current owned full fit without changing its training or RNG."""
from pathlib import Path
from datetime import datetime
import hashlib
import json
import re
import shutil
import subprocess
import time

import psutil
from run_dependency_queue_v3_20261006 import owned
from locked_read_hash_cache_20261004 import LockedReadHashCache
from hidden_windows_child_creation_20261006 import install

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
SERVICE = A / 'service_owned_workflows_20261006/neural16384_annual'
OUT = A / 'service_owned_neural16384_gpu_pressure_20261006'
PWSH = Path('C:/Users/esesl/.cache/codex-runtimes/codex-primary-runtime/dependencies/native/powershell/pwsh.exe')


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8-sig'))


def sha(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def create(path, value):
    with path.open('x', encoding='utf-8') as stream:
        json.dump(value, stream, ensure_ascii=False, indent=2)
        stream.write('\n')


def resource_tail(path):
    with path.open('rb') as stream:
        stream.seek(0, 2)
        stream.seek(max(0, stream.tell() - 32768))
        lines = stream.read().splitlines()
    for line in reversed(lines):
        try:
            return json.loads(line)
        except json.JSONDecodeError:
            continue
    raise AssertionError('No complete current resource observation.')


def main():
    assert not OUT.exists()
    OUT.mkdir()
    restore = install()
    failure = None
    try:
        launch = read(SERVICE / 'native_launch.json')
        assert owned(launch)
        worker = psutil.Process(launch['owned_worker_pid'])
        parent = psutil.Process(launch['pid'])
        assert parent.create_time() == launch['owned_parent_creation_time']
        assert worker.ppid() == parent.pid
        sources = [Path(__file__), SERVICE / 'native_launch.json', SERVICE / 'job_definition.json',
            A / 'train_neural16384_full_bank_20261005.py', A / 'train_diverse_backbones_20261003.py',
            A / 'run_neural16384_full_bank_20261005.py',
            A / 'neural16384_full_bank_20261005/protocol.json',
            A / 'hidden_windows_child_creation_20261006.py',
            A / 'locked_read_hash_cache_20261004.py', A / 'run_dependency_queue_v3_20261006.py']
        bindings = {str(path.resolve()): sha(path) for path in sources}
        create(OUT / 'frozen_before_actual_owned_observations.json', {
            'at_local': datetime.now().isoformat(), 'input_sha256': bindings,
            'native_worker_pid': worker.pid, 'native_worker_creation_time': worker.create_time(),
            'native_worker_command': worker.cmdline(), 'native_root_pid': parent.pid,
            'native_root_creation_time': parent.create_time(), 'observations': 2,
            'minimum_observation_gap_seconds': 30, 'existing_full32_epoch_budget_unchanged': True,
            'no_live_resource_log_hashed_or_locked': True,
            'new_model_fits': 0, 'new_quality_scores': 0, 'test_labels_read': False})
        version = subprocess.run([str(PWSH), '--version'], capture_output=True, text=True,
            encoding='utf-8', timeout=15)
        assert version.returncode == 0 and version.stdout.startswith('PowerShell 7.')
        nvidia = shutil.which('nvidia-smi')
        assert nvidia
        samples = []
        with LockedReadHashCache(bindings) as cache:
            for index in range(2):
                assert owned(launch) and parent.create_time() == launch['owned_parent_creation_time']
                command = (
                    "Get-CimInstance -Namespace root\\cimv2 -ClassName Win32_PerfFormattedData_GPUPerformanceCounters_GPUPROCESSMemory "
                    f"| Where-Object {{ $_.Name -match 'pid_{worker.pid}_' }} "
                    "| Select-Object Name,DedicatedUsage,SharedUsage,TotalCommitted | ConvertTo-Json -Compress")
                result = subprocess.run([str(PWSH), '-NoProfile', '-NonInteractive', '-Command', command],
                    capture_output=True, text=True, encoding='utf-8', timeout=20)
                assert result.returncode == 0 and result.stdout.strip(), result.stderr
                counters = json.loads(result.stdout)
                counters = counters if isinstance(counters, list) else [counters]
                assert counters and all(f'pid_{worker.pid}_' in item['Name'] for item in counters)
                gpu = subprocess.run([nvidia,
                    '--query-gpu=name,memory.total,memory.used,utilization.gpu,temperature.gpu,power.draw',
                    '--format=csv,noheader,nounits'], capture_output=True, text=True,
                    encoding='utf-8', timeout=10)
                assert gpu.returncode == 0, gpu.stderr
                resource = resource_tail(SERVICE / 'resources/actual_full_training_resource_samples.jsonl')
                assert resource['pid'] == worker.pid
                assert abs(datetime.now().timestamp() - datetime.fromisoformat(resource['at_local']).timestamp()) < 30
                stdout = (SERVICE / 'stdout.log').read_bytes()
                stderr = (SERVICE / 'stderr.log').read_bytes()
                assert not stderr
                for name, data in (('stdout', stdout), ('stderr', stderr)):
                    with (OUT / f'observation_{index + 1}_{name}_prefix.log').open('xb') as stream:
                        stream.write(data)
                text = stdout.decode('utf-8')
                log_epochs = [int(item) for item in re.findall(r'MLP y_rank epoch(\d+)/32', text)]
                sample = {'at_local': datetime.now().isoformat(), 'monotonic_seconds': time.monotonic(),
                    'owned_worker_pid': worker.pid, 'owned_worker_creation_time': worker.create_time(),
                    'owned_worker_command': worker.cmdline(),
                    'actual_process_CPU_seconds': sum(worker.cpu_times()[:2]),
                    'actual_process_RSS_bytes': worker.memory_info().rss,
                    'Windows_per_process_GPU_memory_counters': counters,
                    'Windows_total_reported_shared_GPU_bytes': sum(item['SharedUsage'] for item in counters),
                    'Windows_total_reported_dedicated_GPU_bytes': sum(item['DedicatedUsage'] for item in counters),
                    'actual_nvidia_smi_device_report': gpu.stdout.strip(),
                    'actual_resource_sample': resource, 'actual_logged_epochs': log_epochs,
                    'stdout_snapshot_sha256': hashlib.sha256(stdout).hexdigest(),
                    'stderr_snapshot_sha256': hashlib.sha256(stderr).hexdigest(),
                    'actual_power_shell_runtime': version.stdout.strip()}
                create(OUT / f'observation_{index + 1}.json', sample)
                samples.append(sample)
                if index == 0:
                    time.sleep(30)
            assert owned(launch)
            assert samples[1]['actual_process_CPU_seconds'] > samples[0]['actual_process_CPU_seconds']
            assert samples[1]['actual_resource_sample']['monotonic_seconds'] > samples[0]['actual_resource_sample']['monotonic_seconds']
            cache.reverify()
        create(OUT / 'verification.json', {
            'status': 'passed_actual_current_owned_full_fit_and_GPU_pressure_observations',
            'at_local': datetime.now().isoformat(), 'input_sha256': bindings,
            'owned_worker_pid': worker.pid, 'owned_worker_creation_time': worker.create_time(),
            'actual_observation_seconds': samples[1]['monotonic_seconds'] - samples[0]['monotonic_seconds'],
            'actual_process_CPU_seconds_increase': samples[1]['actual_process_CPU_seconds'] - samples[0]['actual_process_CPU_seconds'],
            'Windows_reported_shared_GPU_bytes': [item['Windows_total_reported_shared_GPU_bytes'] for item in samples],
            'actual_logged_epochs': [item['actual_logged_epochs'] for item in samples],
            'sample_contexts': [item['actual_resource_sample']['context'] for item in samples],
            'all_scientific_sources_full_rehash_unchanged': True,
            'no_training_interruption_or_restart_or_RNG_change': True,
            'only_read_owned_native_process_and_current_resource_samples': True,
            'no_inference_of_unlogged_epochs_or_completion_or_remaining_time': True,
            'Windows_shared_memory_counters_alone_do_not_prove_OOM_or_global_resource_boundary': True,
            'original5_annual1_final_full32_epoch_fits_and_all_quality_scopes_still_required': True,
            'all_new_child_processes_hidden': True,
            'physical_resource_boundary_established': False,
            'new_model_fits': 0, 'new_quality_scores': 0, 'test_labels_read': False})
    except BaseException as error:
        failure = f'{type(error).__name__}: {error}'
        create(OUT / 'failure.json', {'status': 'failed_preserved_actual_observation', 'failure': failure})
        raise
    finally:
        create(OUT / 'actual_hidden_observation_children.json', {'actual_CreateProcess_calls': restore(), 'failure': failure})


if __name__ == '__main__':
    main()
