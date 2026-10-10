"""Read-only strong-PID-bound WDDM observations during actual full mature annual training."""
from pathlib import Path
import json
import os
import subprocess
import sys
import time
ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path[:0] = [str(ROOT), str(A)]
from run_dependency_queue_v3_20261006 import read, sha, create, owned


def main():
    import psutil
    path = A / 'service_owned_workflows_20261006/actual_neural_BF16_micro8192_bank6_v2_20261008/native_launch.json'
    row = read(path)
    assert owned(row)
    pid = row['owned_worker_pid']
    bank = Path('E:/赛题五_本机临时/neural_BF16_micro8192_bank6_v2_20261008')
    stage = read(bank / 'actual_stage.json')
    assert stage['status'] == 'actual_mature_annual_BF16_fit'
    year = stage['year']
    inputs = bank / str(year) / 'frozen_training_inputs.json'
    meta = read(inputs)
    assert meta['rows'] == stage['training_rows'] and meta['last'] < meta['cutoff_exclusive'] and meta['last_label_end'] <= meta['cutoff_exclusive']
    out = A / 'actual_BF16_full_annual_GPU_resource_observations_v1_20261008'
    assert not out.exists()
    out.mkdir()
    paths = [Path(__file__), path, inputs, bank / 'protocol.json',
             A / 'neural_BF16_micro8192_native_v1_20261008.py',
             A / 'train_neural_BF16_micro8192_bank6_v2_20261008.py']
    pins = {str(p): sha(p) for p in paths}
    create(out / 'frozen_before_actual_resource_observation.json', {'input_sha256': pins,
            'actual_identity': row, 'actual_full_mature_training': meta, 'actual_phase': stage,
            'read_only_no_worker_pause_or_training_source_change': True})
    shell = Path('C:/Users/esesl/.cache/codex-runtimes/codex-primary-runtime/dependencies/native/powershell/pwsh.exe')
    command = ("Get-CimInstance Win32_PerfFormattedData_GPUPerformanceCounters_GPUProcessMemory | "
               "Where-Object { $_.Name -like 'pid_" + str(pid) + "_*' } | "
               "Select-Object Name,DedicatedUsage,SharedUsage,TotalCommitted | ConvertTo-Json -Compress")
    samples = []
    for index in range(5):
        assert owned(row) and read(bank / 'actual_stage.json')['year'] == year
        with (out / f'sample{index}.json').open('wb') as stdout, (out / f'sample{index}.stderr').open('wb') as stderr:
            result = subprocess.run([str(shell), '-NoLogo', '-NoProfile', '-Command', command],
                stdin=subprocess.DEVNULL, stdout=stdout, stderr=stderr, timeout=20,
                creationflags=subprocess.CREATE_NO_WINDOW, close_fds=True)
        assert result.returncode == 0
        rows = json.loads((out / f'sample{index}.json').read_text(encoding='utf-8-sig'))
        if isinstance(rows, dict): rows = [rows]
        assert rows and all(r['Name'].startswith(f'pid_{pid}_') for r in rows)
        process = psutil.Process(pid)
        item = {'at_local': time.strftime('%Y-%m-%dT%H:%M:%S'), 'pid': pid,
                'creation_time': process.create_time(), 'own_RSS_bytes': process.memory_info().rss,
                'available_RAM_bytes': psutil.virtual_memory().available,
                'dedicated_bytes': sum(int(r['DedicatedUsage']) for r in rows),
                'shared_bytes': sum(int(r['SharedUsage']) for r in rows), 'rows': rows}
        assert item['creation_time'] == row['owned_worker_creation_time']
        samples.append(item)
        if index < 4: time.sleep(2)
    for p, d in pins.items(): assert sha(p) == d, p
    create(out / 'verification.json', {'status': 'observed_actual_full_mature_annual_GPU_WDDM_resources_read_only',
            'at_local': time.strftime('%Y-%m-%dT%H:%M:%S'), 'input_sha256': pins,
            'actual_year': year, 'actual_full_mature_training_rows': meta['rows'], 'samples': samples,
            'maximum_observed_dedicated_bytes': max(s['dedicated_bytes'] for s in samples),
            'maximum_observed_shared_bytes': max(s['shared_bytes'] for s in samples),
            'minimum_observed_available_RAM_bytes': min(s['available_RAM_bytes'] for s in samples),
            'observations_not_continuous_peak_or_GPU_bus_traffic_measurements': True,
            'new_recipe_quality_or_full_annual_speedup_not_established_by_this_observation': True,
            'training_worker_unchanged_running_not_stopped_or_suspended': owned(row),
            'actual_new_complete_annual_fits_by_observation': 0, 'new_quality_scores': 0, 'test_labels_read': False})
    print('Actual full annual resource observations saved', flush=True)


if __name__ == '__main__': main()
