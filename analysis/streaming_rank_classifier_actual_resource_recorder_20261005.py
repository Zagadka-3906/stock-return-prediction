"""Record actual CPU classifier residency without importing or touching CUDA."""
from pathlib import Path
import datetime
import hashlib
import json
import os
import threading
import time

import psutil


class ActualCPUResourceRecorder:
    def __init__(self, output):
        self.output = Path(output)
        self.samples = self.output / 'actual_cpu_resource_samples.jsonl'
        self.stop = threading.Event()
        self.context = {'stage': 'before_actual_fit'}
        self.thread = None
        self.maximum_rss = 0
        self.minimum_available = None
        self.sample_count = 0
        self.errors = []

    def sample(self):
        process = psutil.Process()
        available, rss = psutil.virtual_memory().available, process.memory_info().rss
        self.maximum_rss = max(self.maximum_rss, rss)
        self.minimum_available = available if self.minimum_available is None else min(self.minimum_available, available)
        row = {'at_local': datetime.datetime.now().isoformat(), 'monotonic_seconds': time.monotonic(),
               'pid': os.getpid(), 'context': dict(self.context), 'host_available_bytes': available,
               'own_process_rss_bytes': rss, 'own_cpu_seconds': sum(process.cpu_times()[:2])}
        with self.samples.open('a', encoding='utf-8') as stream:
            stream.write(json.dumps(row, ensure_ascii=False) + '\n')
        self.sample_count += 1

    def start(self):
        self.output.mkdir(parents=True, exist_ok=True)
        assert not self.samples.exists(), 'Keep all previous execution attempts.'
        self.sample()
        def observe():
            while not self.stop.wait(.5):
                try:
                    self.sample()
                except Exception as error:
                    self.errors.append(f'{type(error).__name__}: {error}')
        self.thread = threading.Thread(target=observe, daemon=True)
        self.thread.start()

    def finish(self):
        self.stop.set()
        self.thread.join(10)
        assert not self.thread.is_alive()
        self.sample()
        with self.samples.open('rb') as stream:
            digest = hashlib.file_digest(stream, 'sha256').hexdigest()
        return {'sample_count': self.sample_count, 'maximum_process_rss_bytes_sampled': self.maximum_rss,
                'minimum_host_available_bytes_sampled': self.minimum_available,
                'resource_samples_sha256': digest, 'observer_errors': self.errors,
                'no_GPU_allocation_or_original_native_trainer_changes': True,
                'reserve_is_scheduling_policy_not_physical_capacity_limit': True}
