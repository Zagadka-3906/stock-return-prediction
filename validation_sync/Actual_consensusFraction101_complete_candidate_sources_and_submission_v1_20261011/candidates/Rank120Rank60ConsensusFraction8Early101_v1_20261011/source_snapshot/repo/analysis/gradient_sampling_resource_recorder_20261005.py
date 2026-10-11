"""Record owned CPU-training resources without wrapping or replacing the fitter."""
from pathlib import Path
import hashlib
import json
import threading
import time
import psutil


class Recorder:
    def __init__(self, output):
        self.path = Path(output) / 'actual_resource_samples.jsonl'
        self.stop_event = threading.Event()
        self.thread = None
        self.count = 0
        self.errors = []
        self.min_available = None
        self.max_owned_rss = 0

    def sample(self, stream):
        process = psutil.Process()
        owned = [process, *process.children(recursive=True)]
        rss = sum(p.memory_info().rss for p in owned if p.is_running())
        available = psutil.virtual_memory().available
        self.min_available = available if self.min_available is None else min(self.min_available, available)
        self.max_owned_rss = max(self.max_owned_rss, rss)
        stream.write(json.dumps({'at': time.time(), 'owned_pid': process.pid,
            'owned_rss_bytes': rss, 'host_available_bytes': available,
            'sample_is_shared_host_observation_not_isolated_benchmark': True}) + '\n')
        stream.flush()
        self.count += 1

    def run(self):
        with self.path.open('x', encoding='utf-8') as stream:
            while True:
                try:
                    self.sample(stream)
                except BaseException as error:
                    self.errors.append(f'{type(error).__name__}: {error}')
                if self.stop_event.wait(2):
                    break

    def start(self):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.thread = threading.Thread(target=self.run, daemon=True)
        self.thread.start()

    def finish(self):
        self.stop_event.set()
        self.thread.join()
        assert self.count > 0 and not self.errors
        return {'actual_samples': self.count, 'observation_errors': self.errors,
            'sample_file': str(self.path), 'sample_file_sha256': hashlib.sha256(self.path.read_bytes()).hexdigest(),
            'sampled_minimum_host_available_bytes': self.min_available,
            'sampled_maximum_owned_rss_bytes': self.max_owned_rss,
            'native_fitter_not_wrapped_or_replaced': True,
            'physical_resource_exhaustion_established': False}
