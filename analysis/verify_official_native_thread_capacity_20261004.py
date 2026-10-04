"""Balanced native-thread controls; original official scorer and completed train CSV."""
from concurrent.futures import ProcessPoolExecutor, wait, FIRST_COMPLETED
from collections import Counter
from pathlib import Path
import hashlib
import json
import multiprocessing
import os
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT), str(ROOT / 'analysis')]
OUT = ROOT / 'analysis/official_native_thread_capacity_qa_20261004'
THREAD_ORDER = (8, 4, 2, 1, 1, 2, 4, 8)
WORKERS = 4
JOBS = 8
MINIMUM_FREE = 2 * 2**30
START_FREE = 9 * 2**30
ENV_KEYS = ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS', 'POLARS_MAX_THREADS', 'NUMEXPR_NUM_THREADS', 'VECLIB_MAXIMUM_THREADS')


def read(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))


def sha(path):
    h = hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(8 * 1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def create(path, value):
    with path.open('x', encoding='utf-8') as stream:
        json.dump(value, stream, ensure_ascii=False, indent=2)


def work(job):
    from evaluate import evaluate
    from threadpoolctl import threadpool_info
    import psutil
    block, slot = job
    folder = OUT / f'block{block:02d}' / f'job{slot}'
    started = time.perf_counter()
    metrics = {key: float(value) for key, value in evaluate(str(folder / 'submission.csv'), str(folder)).items()}
    return {'job': slot, 'pid': os.getpid(), 'seconds': time.perf_counter() - started,
        'metrics': metrics, 'rss_at_return': psutil.Process().memory_info().rss,
        'native_thread_environment': {key: os.environ.get(key) for key in ENV_KEYS},
        'loaded_native_threadpools': threadpool_info()}


def main():
    import psutil
    from verify_official_extended_capacity_20261004 import external_state
    OUT.mkdir(exist_ok=True)
    source = ROOT / 'analysis/optimization_20261003_r30'
    expected_path = source / 'calibrated_csv_official.json'
    expected = read(expected_path)
    submission = source / 'calibrated_validation.csv'
    labels = source / 'scoring_validation_only'
    assert expected['status'] == 'passed' and sha(submission) == expected['csv_sha256']
    assert read(ROOT / 'results/optimization_20261003_r30.json')['status'] == 'complete'
    import importlib.util
    assert importlib.util.find_spec('threadpoolctl') is not None
    sources = [Path(__file__), ROOT / 'evaluate.py', ROOT / 'src/scoring.py',
        ROOT / 'analysis/verify_official_extended_capacity_20261004.py', submission,
        labels / '测试集_X.csv', labels / '测试集_Y.csv', expected_path,
        ROOT / 'results/optimization_20261003_r30.json']
    frozen = {str(path.resolve()): sha(path) for path in sources}
    protocol = OUT / 'diagnostic_frozen_before_scoring.json'
    create(protocol, {'status': 'frozen_execution_control', 'at_local': time.strftime('%Y-%m-%dT%H:%M:%S'),
        'thread_order': THREAD_ORDER, 'workers_per_block': WORKERS, 'same_jobs_per_block': JOBS,
        'source': 'Completed R30 training-only5635800-row original official return CSV',
        'order': 'Forward then reversed native-thread counts; repeat measurements retained separately',
        'start_required_available_bytes': START_FREE, 'stop_own_workers_if_available_bytes_below': MINIMUM_FREE,
        'maximum_seconds_per_block': 180, 'all_limits_are_control_policies_not_hardware_maximum': True,
        'background_paused_or_controlled': False, 'no_isolated_causal_throughput_claim': True,
        'new_quality_scores': 0, 'test_labels_read': False, 'input_sha256': frozen})
    results = []
    for block, threads in enumerate(THREAD_ORDER):
        available = psutil.virtual_memory().available
        if available < START_FREE:
            result = {'block': block, 'native_threads': threads, 'status': 'not_launched_for_current_memory_budget',
                'available_bytes_at_launch': available, 'required_bytes_at_launch': START_FREE,
                'background': external_state(), 'physical_exhaustion_proved': False}
            create(OUT / f'block{block:02d}_result.json', result)
            results.append(result)
            print(json.dumps(result), flush=True)
            continue
        for key in ENV_KEYS:
            os.environ[key] = str(threads)
        for slot in range(JOBS):
            folder = OUT / f'block{block:02d}' / f'job{slot}'
            folder.mkdir(parents=True)
            for name, original in (('submission.csv', submission), ('测试集_X.csv', labels / '测试集_X.csv'), ('测试集_Y.csv', labels / '测试集_Y.csv')):
                os.link(original, folder / name)
        samples, jobs, reason = [], [], None
        started = time.perf_counter()
        pool = ProcessPoolExecutor(max_workers=WORKERS, mp_context=multiprocessing.get_context('spawn'))
        try:
            pending = {pool.submit(work, (block, slot)) for slot in range(JOBS)}
            observed, background = 0., external_state()
            while pending:
                completed, pending = wait(pending, timeout=.25, return_when=FIRST_COMPLETED)
                now = time.perf_counter()
                processes = list(pool._processes.values())
                if now - observed >= 2:
                    background, observed = external_state(), now
                rss = 0
                for process in processes:
                    try:
                        rss += psutil.Process(process.pid).memory_info().rss
                    except psutil.Error:
                        pass
                free = psutil.virtual_memory().available
                samples.append({'at_local': time.strftime('%Y-%m-%dT%H:%M:%S'), 'elapsed_seconds': now - started,
                    'available_bytes': free, 'own_worker_rss_sum_bytes': rss, 'background': background})
                jobs.extend(future.result() for future in completed)
                if free < MINIMUM_FREE or now - started > 180:
                    reason = 'sampled_memory_floor' if free < MINIMUM_FREE else 'declared_wall_time_budget'
                    for process in processes:
                        if process.is_alive():
                            process.terminate()
                    for future in pending:
                        future.cancel()
                    break
        finally:
            pool.shutdown(wait=True, cancel_futures=True)
        seconds = time.perf_counter() - started
        equal = all(job['metrics'] == expected['metrics'] for job in jobs)
        assert reason is not None or len(jobs) == JOBS
        sample_path = OUT / f'block{block:02d}_samples.jsonl'
        with sample_path.open('x', encoding='utf-8') as stream:
            for sample in samples:
                stream.write(json.dumps(sample, ensure_ascii=False) + '\n')
        result = {'status': ('passed' if equal else 'metric_parity_failed') if reason is None else 'stopped_at_declared_control_boundary',
            'block': block, 'native_threads': threads, 'workers': WORKERS, 'jobs_completed': len(jobs),
            'jobs_declared': JOBS, 'stop_reason': reason, 'total_seconds_including_spawn_and_shutdown': seconds,
            'records_per_minute_completed_control_only': JOBS * 60 / seconds if reason is None and equal else None,
            'all_completed_jobs_eight_metrics_bit_identical': equal, 'jobs_details': jobs,
            'minimum_available_bytes_sampled': min(s['available_bytes'] for s in samples),
            'maximum_own_worker_rss_sum_bytes_sampled': max(s['own_worker_rss_sum_bytes'] for s in samples),
            'actual_background_official_worker_count_samples': dict(Counter(str(len(s['background'].get('actual_official_worker_pids', []))) for s in samples)),
            'background_stage_samples': sorted({json.dumps(s['background'].get('active_round_stages', {}), sort_keys=True) for s in samples}),
            'samples': len(samples), 'resource_samples_sha256': sha(sample_path),
            'background_controlled_or_paused': False, 'physical_exhaustion_proved': False,
            'new_quality_scores': 0, 'test_labels_read': False}
        create(OUT / f'block{block:02d}_result.json', result)
        results.append(result)
        print(json.dumps({key: result[key] for key in ('status', 'block', 'native_threads', 'jobs_completed', 'records_per_minute_completed_control_only', 'minimum_available_bytes_sampled')}), flush=True)
        if not equal:
            break
    assert all(sha(Path(path)) == digest for path, digest in frozen.items())
    complete = len(results) == len(THREAD_ORDER) and all(r['status'] == 'passed' for r in results)
    create(OUT / 'verification.json', {'status': 'passed' if complete else 'bounded_controls_incomplete',
        'at_local': time.strftime('%Y-%m-%dT%H:%M:%S'), 'execution_controls': results,
        'diagnostic_freeze_sha256': sha(protocol), 'completed_control_jobs': sum(r.get('jobs_completed', 0) for r in results),
        'all_source_hashes_unchanged': True, 'ongoing_rounds_remain_at_frozen_four_workers_eight_native_threads': True,
        'no_incomplete_or_failed_control_has_throughput_rank': True,
        'background_controlled_or_paused': False, 'physical_resource_boundary_established': False,
        'global_search_exhaustion_established': False, 'new_quality_scores': 0, 'test_labels_read': False,
        'scope': 'Original official scorer-only native-thread measurements on identical training CSV; background is observed, not experimentally fixed. No automatic production adoption.'})


if __name__ == '__main__':
    main()
