"""Bounded scorer capacity controls on an already selected training-only CSV."""
from concurrent.futures import ProcessPoolExecutor, wait, FIRST_COMPLETED
from pathlib import Path
from collections import Counter
import hashlib
import json
import multiprocessing
import os
import sys
import time

for key in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS', 'POLARS_MAX_THREADS'):
    os.environ[key] = '8'
ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT), str(ROOT / 'analysis')]
QA = ROOT / 'analysis/official_worker_frontier_forward_qa_20261004'
COUNTS = (8, 10, 12, 16)
JOBS = 16
MINIMUM_FREE = 2 * 2**30


def read(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def create(path, value):
    with path.open('x', encoding='utf-8') as stream:
        json.dump(value, stream, ensure_ascii=False, indent=2)


def work(job):
    from evaluate import evaluate
    import psutil
    number, slot = job
    folder = QA / f'workers{number}' / f'job{slot}'
    started = time.perf_counter()
    result = {key: float(value) for key, value in evaluate(str(folder / 'submission.csv'), str(folder)).items()}
    return {'job': slot, 'pid': os.getpid(), 'seconds': time.perf_counter() - started,
        'rss_at_return': psutil.Process().memory_info().rss, 'metrics': result}


def external_state():
    import psutil
    path = ROOT / 'analysis/ongoing_optimization_state.json'
    try:
        registry = read(ROOT / read(path)['active_run_registry'])
    except (OSError, json.JSONDecodeError):
        return {'observation_status': 'transient_state_unavailable'}
    workers, stages = [], {}
    for entry in registry:
        state_path = ROOT / f"analysis/ongoing_optimization_r{entry['round']}_state.json"
        if not psutil.pid_exists(entry['pid']):
            continue
        try:
            state = read(state_path) if state_path.exists() else {}
            if state.get('status') == 'running' and not state.get('stage', '').startswith('waiting'):
                stages[str(entry['round'])] = state.get('stage')
            for process in psutil.Process(entry['pid']).children(recursive=True):
                command = ' '.join(process.cmdline())
                if 'multiprocessing.spawn' in command and '--multiprocessing-fork' in command:
                    workers.append(process.pid)
        except (psutil.Error, OSError, json.JSONDecodeError):
            continue
    return {'actual_official_worker_pids': sorted(set(workers)), 'active_round_stages': stages}


def main():
    import psutil
    QA.mkdir(exist_ok=True)
    assert not (QA / 'diagnostic_frozen_before_scoring.json').exists()
    source = ROOT / 'analysis/optimization_20261003_r30'
    expected_path = source / 'calibrated_csv_official.json'
    expected = read(expected_path)
    assert expected['status'] == 'passed'
    submission = source / 'calibrated_validation.csv'
    labels = source / 'scoring_validation_only'
    assert sha(submission) == expected['csv_sha256']
    assert read(ROOT / 'results/optimization_20261003_r30.json')['status'] == 'complete'
    sources = [Path(__file__), ROOT / 'evaluate.py', ROOT / 'src/scoring.py', submission,
        labels / '测试集_X.csv', labels / '测试集_Y.csv', expected_path,
        ROOT / 'results/optimization_20261003_r30.json',
        ROOT / 'analysis/official_parallel_capacity_qa_20261004/verification.json',
        ROOT / 'analysis/official_worker_frontier_prepared_plan_20261004.json',
        ROOT / 'analysis/neural_width_frontier_20261004/verification.json']
    protocol = QA / 'diagnostic_frozen_before_scoring.json'
    create(protocol, {'status': 'frozen_execution_control', 'at_local': time.strftime('%Y-%m-%dT%H:%M:%S'),
        'worker_counts': COUNTS, 'same_jobs_per_count': JOBS, 'native_threads_per_worker': 8,
        'start_required_bytes_rule': '4GiB reserve plus1.5GiB per proposed worker, scheduling rule only',
        'stop_own_control_workers_if_available_bytes_below': MINIMUM_FREE,
        'maximum_control_seconds_per_count': 240,
        'source': 'Already selected complete 5635800-row R30 training-only actual return CSV',
        'background_work_not_paused': True, 'declared_order_block':'forward',
        'repeated_forward_andreverse_blocks_not_matched_randomized_benchmark':True, 'all_background_stages_and_actual_worker_PIDs_sampled': True,
        'background_variation_prevents_causal_isolated_throughput_claim': True,
        'new_quality_scores': 0, 'test_labels_read': False,
        'input_sha256': {str(path.resolve()): sha(path) for path in sources}})
    results = []
    for number in COUNTS:
        available = psutil.virtual_memory().available
        required = int((4 + 1.5 * number) * 2**30)
        if available < required:
            result = {'workers': number, 'status': 'not_launched_for_current_memory_budget',
                'available_bytes_at_launch': available, 'required_bytes_at_launch': required,
                'background': external_state(), 'physical_exhaustion_proved': False}
            create(QA / f'workers{number}_result.json', result)
            results.append(result)
            print(json.dumps(result, ensure_ascii=False), flush=True)
            continue
        for slot in range(JOBS):
            folder = QA / f'workers{number}' / f'job{slot}'
            folder.mkdir(parents=True, exist_ok=True)
            for name, original in (('submission.csv', submission), ('测试集_X.csv', labels / '测试集_X.csv'), ('测试集_Y.csv', labels / '测试集_Y.csv')):
                os.link(original, folder / name)
        started, samples, jobs, reason = time.perf_counter(), [], [], None
        pool = ProcessPoolExecutor(max_workers=number, mp_context=multiprocessing.get_context('spawn'))
        try:
            pending = {pool.submit(work, (number, slot)) for slot in range(JOBS)}
            last_external, background = 0., external_state()
            while pending:
                completed, pending = wait(pending, timeout=.25, return_when=FIRST_COMPLETED)
                now = time.perf_counter()
                processes = list(pool._processes.values())
                rss = 0
                for process in processes:
                    try:
                        rss += psutil.Process(process.pid).memory_info().rss
                    except psutil.Error:
                        pass
                if now - last_external >= 2:
                    background, last_external = external_state(), now
                free = psutil.virtual_memory().available
                samples.append({'at_local': time.strftime('%Y-%m-%dT%H:%M:%S'),
                    'elapsed_seconds': now - started, 'available_bytes': free,
                    'own_worker_rss_sum_bytes': rss, 'background': background})
                jobs.extend(future.result() for future in completed)
                if free < MINIMUM_FREE or now - started > 240:
                    reason = 'sampled_memory_floor' if free < MINIMUM_FREE else 'declared_wall_time_budget'
                    # Stop only this control's owned processes; official pipelines continue.
                    for process in processes:
                        if process.is_alive():
                            process.terminate()
                    for future in pending:
                        future.cancel()
                    break
        finally:
            pool.shutdown(wait=True, cancel_futures=True)
        seconds = time.perf_counter() - started
        assert all(job['metrics'] == expected['metrics'] for job in jobs)
        if reason is None:
            assert len(jobs) == JOBS
        sample_path = QA / f'workers{number}_samples.jsonl'
        with sample_path.open('x', encoding='utf-8') as stream:
            for sample in samples:
                stream.write(json.dumps(sample, ensure_ascii=False) + '\n')
        result = {'status': 'passed' if reason is None else 'stopped_at_declared_control_boundary',
            'workers': number, 'jobs_completed': len(jobs), 'jobs_declared': JOBS, 'stop_reason': reason,
            'total_seconds_including_spawn_and_shutdown': seconds,
            'records_per_minute_completed_control_only': JOBS * 60 / seconds if reason is None else None,
            'minimum_available_bytes_sampled': min(s['available_bytes'] for s in samples),
            'maximum_own_worker_rss_sum_bytes_sampled': max(s['own_worker_rss_sum_bytes'] for s in samples),
            'all_completed_jobs_eight_metrics_bit_identical': True, 'jobs_details': jobs,
            'actual_background_official_worker_count_samples': dict(Counter(str(len(s['background'].get('actual_official_worker_pids', []))) for s in samples)),
            'background_stage_samples': list({json.dumps(s['background'].get('active_round_stages', {}), sort_keys=True) for s in samples}),
            'samples': len(samples), 'resource_samples_sha256': sha(sample_path),
            'background_controlled_or_paused': False,
            'physical_exhaustion_proved': False, 'new_quality_scores': 0, 'test_labels_read': False}
        create(QA / f'workers{number}_result.json', result)
        results.append(result)
        print(json.dumps({key: result[key] for key in ('status', 'workers', 'jobs_completed', 'stop_reason', 'records_per_minute_completed_control_only', 'minimum_available_bytes_sampled')}, ensure_ascii=False), flush=True)
    for path, digest in read(protocol)['input_sha256'].items():
        assert sha(Path(path)) == digest, path
    create(QA / 'verification.json', {'status': 'passed', 'at_local': time.strftime('%Y-%m-%dT%H:%M:%S'),
        'execution_controls': results, 'diagnostic_freeze_sha256': sha(protocol),
        'completed_counts': [r['workers'] for r in results if r['status'] == 'passed'],
        'guarded_or_not_launched_counts': [r['workers'] for r in results if r['status'] != 'passed'],
        'no_failed_or_incomplete_count_has_throughput_rank': True,
        'ongoing_declared_rounds_remain_at_frozen_four_workers': True,
        'new_quality_scores': 0, 'test_labels_read': False,
        'physical_resource_boundary_established': False, 'global_search_exhaustion_established': False,
        'scope': 'Actual scorer-only sampled capacity and explicit scheduling/stop boundaries under observed changing background work; not an isolated causal throughput or hardware-maximum benchmark.'})
    print('Extended official scorer controls completed with explicit scope', flush=True)


if __name__ == '__main__':
    main()
