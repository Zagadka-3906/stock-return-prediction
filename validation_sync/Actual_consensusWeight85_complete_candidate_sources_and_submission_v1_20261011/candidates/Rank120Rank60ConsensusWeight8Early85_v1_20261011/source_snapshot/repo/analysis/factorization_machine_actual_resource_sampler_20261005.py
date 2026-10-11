"""Observe native CPU training resources without replacing any fitter."""
from pathlib import Path
import datetime
import hashlib
import json
import os
import threading
import time

import psutil


class ResourceSampler:
    def __init__(self, output, target_pid=None):
        self.output = Path(output)
        self.output.mkdir(parents=True, exist_ok=True)
        self.target = psutil.Process(target_pid or os.getpid())
        self.created = self.target.create_time()
        self.samples = self.output / 'actual_resource_samples.jsonl'
        self.stop_event = threading.Event()
        self.context = {'stage': 'waiting_for_native_training'}
        self.count, self.minimum_available, self.maximum_tree_rss = 0, None, 0
        self.errors, self.thread = [], None

    def sample(self):
        assert self.target.create_time() == self.created
        children = self.target.children(recursive=True)
        rss = sum(p.memory_info().rss for p in [self.target, *children] if p.is_running())
        vm = psutil.virtual_memory()
        row = {'at_local': datetime.datetime.now().isoformat(), 'target_pid': self.target.pid,
            'monotonic_seconds': time.monotonic(), 'context': dict(self.context),
            'host_available_bytes': vm.available, 'host_total_bytes': vm.total,
            'target_and_descendant_rss_bytes': rss, 'descendant_pids': [p.pid for p in children],
            'disk_free_bytes': {drive: psutil.disk_usage(drive).free for drive in ('D:/', 'E:/')}}
        with self.samples.open('a', encoding='utf-8') as stream:
            stream.write(json.dumps(row, ensure_ascii=False) + '\n')
        self.minimum_available = vm.available if self.minimum_available is None else min(self.minimum_available, vm.available)
        self.maximum_tree_rss = max(self.maximum_tree_rss, rss)
        self.count += 1

    def start(self):
        assert not self.samples.exists(), 'Preserve earlier execution samples.'
        self.sample()
        def observe():
            while not self.stop_event.wait(1):
                try:
                    self.sample()
                except (psutil.NoSuchProcess, psutil.ZombieProcess):
                    self.stop_event.set()
                except Exception as error:
                    self.errors.append(f'{type(error).__name__}: {error}')
        self.thread = threading.Thread(target=observe, daemon=True)
        self.thread.start()

    def finish(self):
        self.stop_event.set()
        if self.thread is not None:
            self.thread.join(timeout=10)
            assert not self.thread.is_alive()
        with self.samples.open('rb') as stream:
            sha = hashlib.file_digest(stream, 'sha256').hexdigest()
        return {'actual_samples': self.count, 'minimum_host_available_bytes': self.minimum_available,
            'maximum_target_and_descendant_rss_bytes': self.maximum_tree_rss,
            'sample_file_sha256': sha, 'observation_errors': self.errors,
            'no_fitter_or_prediction_bindings_changed': True,
            'host14GiB_admission_is_scheduling_policy': True, 'physical_boundary_established': False}


def main():
    root = Path(__file__).resolve().parents[1]
    run = json.loads((root / 'analysis/factorization_machine_bank_run_20261005.json').read_text(encoding='utf-8'))
    target = psutil.Process(run['pid'])
    assert run['script'] in target.cmdline()
    out = root / 'analysis/factorization_machine_annual_resource_observer_20261005'
    sampler = ResourceSampler(out, target_pid=target.pid)
    sampler.start()
    try:
        while target.is_running() and target.create_time() == sampler.created:
            time.sleep(5)
    finally:
        summary = sampler.finish()
        with (out / 'resource_summary.json').open('x', encoding='utf-8') as stream:
            json.dump({'status': 'completed_owned_process_observation', 'target_run': run,
                'target_process_create_time': sampler.created, 'resource_evidence': summary,
                'observation_completion_is_not_training_completion': True,
                'test_labels_read': False}, stream, ensure_ascii=False, indent=2)


if __name__ == '__main__':
    main()
