"""Observe full native fits without changing arrays, RNG, optimizer or epochs."""
from pathlib import Path
import datetime
import hashlib
import json
import math
import os
import shutil
import subprocess
import threading
import time

import psutil


def sha(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


class ActualResourceRecorder:
    def __init__(self, output):
        self.output = Path(output)
        self.output.mkdir(parents=True, exist_ok=True)
        self.samples = self.output / 'actual_full_training_resource_samples.jsonl'
        self.fits = self.output / 'actual_native_fit_measurements.jsonl'
        self.stop_event = threading.Event()
        self.context = {'stage': 'before_annual_training'}
        self.sample_count = 0
        self.fit_count = 0
        self.minimum_host_available = None
        self.maximum_process_rss = 0
        self.errors = []
        self.nvidia_smi = shutil.which('nvidia-smi')
        self.thread = None

    def sample(self):
        vm = psutil.virtual_memory()
        process = psutil.Process()
        row = {'at_local': datetime.datetime.now().isoformat(), 'monotonic_seconds': time.monotonic(),
            'pid': os.getpid(), 'context': dict(self.context),
            'host_available_bytes': vm.available, 'host_total_bytes': vm.total,
            'process_rss_bytes': process.memory_info().rss,
            'disk_free_bytes': {drive: shutil.disk_usage(drive).free for drive in ('D:/', 'E:/')}}
        self.minimum_host_available = vm.available if self.minimum_host_available is None else min(self.minimum_host_available, vm.available)
        self.maximum_process_rss = max(self.maximum_process_rss, row['process_rss_bytes'])
        if self.sample_count % 5 == 0 and self.nvidia_smi:
            result = subprocess.run([self.nvidia_smi,
                '--query-gpu=timestamp,name,memory.total,memory.used,utilization.gpu,utilization.memory',
                '--format=csv,noheader,nounits'], capture_output=True, text=True,
                timeout=6, creationflags=subprocess.CREATE_NO_WINDOW)
            row['nvidia_smi_returncode'] = result.returncode
            row['nvidia_smi_reported_device_memory_and_utilization'] = result.stdout.strip()
            if result.returncode:
                row['nvidia_smi_error'] = result.stderr.strip()[:500]
        with self.samples.open('a', encoding='utf-8') as stream:
            stream.write(json.dumps(row, ensure_ascii=False) + '\n')
        self.sample_count += 1

    def start(self):
        assert not self.samples.exists() and not self.fits.exists(), 'Preserve prior attempts and choose a new execution scope.'
        self.sample()
        def observe():
            while not self.stop_event.wait(1):
                try:
                    self.sample()
                except Exception as error:
                    self.errors.append(f'{type(error).__name__}: {error}')
        self.thread = threading.Thread(target=observe, daemon=True)
        self.thread.start()

    def measured_fit(self, original):
        def fit(x, y, cfg):
            import torch
            self.fit_count += 1
            row = {'fit_call': self.fit_count, 'context': dict(self.context), 'configuration': dict(cfg),
                'actual_training_rows': len(y), 'actual_feature_count': x.shape[1],
                'requested_epochs': cfg['epochs'],
                'planned_native_optimizer_steps': math.ceil(len(y) / cfg['batch_size']) * cfg['epochs'],
                'instrumentation_passes_identical_input_objects_to_unchanged_native_fitter': True,
                'cuda_available': torch.cuda.is_available()}
            if row['cuda_available']:
                free, total = torch.cuda.mem_get_info()
                row.update(device_name=torch.cuda.get_device_name(), device_free_bytes_before=free,
                           device_total_bytes=total)
                torch.cuda.reset_peak_memory_stats()
            started = time.monotonic()
            try:
                bundle = original(x, y, cfg)
                assert len(bundle['training_losses']) == cfg['epochs']
                assert all(math.isfinite(value) for value in bundle['training_losses'])
                assert all(torch.isfinite(value).all().item() for value in bundle['state'].values())
                row.update(status='completed_original_requested_epochs',
                    completed_epochs=len(bundle['training_losses']),
                    training_losses=bundle['training_losses'], returned_state_all_finite=True,
                    parameter_count=sum(value.numel() for value in bundle['state'].values()))
                return bundle
            except BaseException as error:
                row.update(status='failed', error=f'{type(error).__name__}: {error}',
                    actual_cuda_out_of_memory=isinstance(error, torch.cuda.OutOfMemoryError),
                    failure_is_not_an_optimization_score=True)
                raise
            finally:
                row['actual_elapsed_seconds'] = time.monotonic() - started
                if row['cuda_available']:
                    row.update(peak_own_tensor_allocated_bytes=torch.cuda.max_memory_allocated(),
                        peak_own_allocator_reserved_bytes=torch.cuda.max_memory_reserved(),
                        allocator_reserved_is_not_proof_of_resident_physical_VRAM=True)
                with self.fits.open('a', encoding='utf-8') as stream:
                    stream.write(json.dumps(row, ensure_ascii=False) + '\n')
        return fit

    def finish(self):
        self.stop_event.set()
        self.thread.join(timeout=10)
        assert not self.thread.is_alive()
        self.sample()
        return {'resource_samples': self.sample_count, 'native_fit_calls': self.fit_count,
            'minimum_available_host_bytes_sampled': self.minimum_host_available,
            'maximum_process_rss_bytes_sampled': self.maximum_process_rss,
            'resource_samples_sha256': sha(self.samples),
            'native_fit_measurements_sha256': sha(self.fits) if self.fits.exists() else None,
            'external_gpu_telemetry_available': self.nvidia_smi is not None, 'observer_errors': self.errors,
            'one_second_host_sampling_and_every_fifth_sample_external_gpu_query': True,
            'no_declared_wall_time_cap_or_smaller_epoch_substitution': True,
            'admission_reserve_is_not_a_physical_resource_boundary': True}
