"""Read-only Windows CPU bank resource sampling; never control scientific processes."""
from pathlib import Path
import json
import sys
import time
import psutil

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path.insert(0, str(A))
from run_dependency_queue_v3_20261006 import read, sha, create, owned
from atomic_optimization_observer_writes_20261005 import write

CONFIG = {
    'HGB': ('cpu_full_universe_HGB_native_bank24', 'cpu_full_universe_HGB_bank24_20261007'),
    'ElasticNet': ('cpu_full_universe_ElasticNet_native_bank24', 'cpu_full_universe_ElasticNet_bank24_20261007'),
}


def main():
    kind = sys.argv[1]
    service_name, bank_name = CONFIG[kind]
    service = A / 'service_owned_workflows_20261006' / service_name
    bank = A / bank_name
    out = A / f'CPU_{kind}_full_bank_resource_observation_20261007'
    assert not out.exists()
    out.mkdir()
    identity = read(service / 'native_launch.json')
    assert owned(identity), 'Attach only to the presently live, birth-verified bank worker'
    definition = read(service / 'job_definition.json')
    pins = {str(p.resolve()): sha(p) for p in [Path(__file__),
        service / 'native_launch.json', service / 'job_definition.json', Path(definition['driver'])]}
    create(out / 'frozen_before_read_only_observation.json', {
        'input_sha256': pins, 'worker_identity': identity, 'at_local': time.strftime('%Y-%m-%dT%H:%M:%S'),
        'sampling_interval_seconds': 5, 'expected_native_fits': 24,
        'scientific_process_control_calls': 0, 'dataset_or_labels_read': False,
        'stage_sampled_peaks_are_lower_bounds_not_continuous_peaks': True,
        'Windows_peak_wset_and_peak_pagefile_are_worker_lifetime_counters': True})
    process = psutil.Process(identity['owned_worker_pid'])
    start_cpu = process.cpu_times()
    started = time.monotonic()
    samples = 0
    stages = {}
    boot = []
    maximum = {k: 0 for k in ('rss', 'private', 'peak_wset', 'peak_pagefile')}
    minimum_free = psutil.virtual_memory().available
    last_cpu = start_cpu
    path = out / 'samples.jsonl'
    with path.open('x', encoding='utf-8', newline='\n') as stream:
        while True:
            if not owned(identity):
                # Handle disappearance alone is not a scientific terminal result.
                if not (service / 'service_execution.json').exists():
                    write(out / 'current.json', {'status': 'worker_no_longer_owned_awaiting_actual_terminal',
                        'samples': samples, 'at_local': time.strftime('%Y-%m-%dT%H:%M:%S')})
                    time.sleep(2)
                    continue
                break
            try:
                memory = process.memory_info()._asdict()
                last_cpu = process.cpu_times()
            except psutil.NoSuchProcess:
                continue
            available = psutil.virtual_memory().available
            minimum_free = min(minimum_free, available)
            stage = read(bank / 'actual_stage.json') if (bank / 'actual_stage.json').exists() else {}
            key = json.dumps({k: stage.get(k) for k in ('status', 'model', 'year')}, sort_keys=True)
            summary = stages.setdefault(key, {'stage': stage, 'samples': 0,
                'sampled_max_rss_bytes': 0, 'sampled_max_private_bytes': 0,
                'minimum_available_system_RAM_bytes': available})
            summary['samples'] += 1
            summary['sampled_max_rss_bytes'] = max(summary['sampled_max_rss_bytes'], memory['rss'])
            summary['sampled_max_private_bytes'] = max(summary['sampled_max_private_bytes'], memory['private'])
            summary['minimum_available_system_RAM_bytes'] = min(summary['minimum_available_system_RAM_bytes'], available)
            for field in maximum:
                maximum[field] = max(maximum[field], memory[field])
            row = {'at_local': time.strftime('%Y-%m-%dT%H:%M:%S'), 'strong_identity_owned_live_now': True,
                'worker_pid': process.pid, 'worker_birth_time': process.create_time(),
                'memory_bytes': {k: memory[k] for k in maximum}, 'available_system_RAM_bytes': available,
                'worker_cpu_seconds': last_cpu.user + last_cpu.system, 'actual_stage': stage}
            stream.write(json.dumps(row, ensure_ascii=False) + '\n')
            stream.flush()
            samples += 1
            if samples <= 2:
                boot.append(row)
            if samples == 2:
                assert all(sha(Path(p)) == digest for p, digest in pins.items())
                create(out / 'actual_two_live_samples_attach_verification.json', {
                    'status': 'passed_actual_two_birth_verified_live_read_only_Windows_resource_samples',
                    'at_local': row['at_local'], 'kind': kind, 'samples': boot, 'input_sha256': pins,
                    'observer_pid': psutil.Process().pid, 'scientific_process_control_calls': 0,
                    'scientific_sources_and_original_bank_identity_unchanged': True,
                    'new_model_fits': 0, 'new_quality_scores': 0, 'test_labels_read': False})
            if samples % 3 == 0:
                write(out / 'current.json', {'status': 'observing_actual_original_CPU_full_bank_resources',
                    'at_local': row['at_local'], 'samples': samples, 'actual_stage': stage,
                    'maximum_sampled_or_worker_lifetime_memory_bytes': maximum,
                    'minimum_available_system_RAM_bytes': minimum_free,
                    'science_completed_by_observer': False})
            time.sleep(5)
    terminal = read(service / 'service_execution.json')
    assert all(sha(Path(p)) == digest for p, digest in pins.items())
    proof = read(bank / 'verification.json') if (bank / 'verification.json').exists() else None
    create(out / 'verification.json', {
        'status': 'completed_actual_read_only_resource_observation_of_closed_CPU_bank',
        'at_local': time.strftime('%Y-%m-%dT%H:%M:%S'), 'input_sha256': pins, 'kind': kind,
        'actual_terminal': terminal, 'actual_native_fits': proof.get('actual_native_fits') if proof else None,
        'samples': samples, 'sampled_elapsed_seconds': time.monotonic() - started,
        'worker_CPU_seconds_since_attachment': last_cpu.user + last_cpu.system - start_cpu.user - start_cpu.system,
        'maximum_sampled_or_worker_lifetime_memory_bytes': maximum,
        'minimum_available_system_RAM_bytes': minimum_free, 'stages': list(stages.values()),
        'samples_jsonl_sha256': sha(path), 'scientific_process_control_calls': 0,
        'sampling_includes_initial_waits_and_preprocessing_before_named_fit_stage': True,
        'not_a_scientific_validation_or_global_resource_exhaustion_claim': True,
        'new_model_fits_by_observer': 0, 'new_quality_scores': 0, 'test_labels_read': False})


if __name__ == '__main__':
    main()
