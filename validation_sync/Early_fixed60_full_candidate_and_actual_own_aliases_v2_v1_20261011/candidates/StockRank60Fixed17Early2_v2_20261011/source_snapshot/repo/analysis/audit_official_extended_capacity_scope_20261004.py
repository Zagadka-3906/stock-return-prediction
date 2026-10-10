"""Verify actual capacity records while retaining changing-background scope."""
from pathlib import Path
from collections import Counter
import hashlib
import json
import time

ROOT = Path(__file__).resolve().parents[1]
QA = ROOT / 'analysis/official_extended_capacity_qa_20261004'
OUT = ROOT / 'analysis/official_extended_capacity_scope_audit_20261004.json'


def read(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    if OUT.exists():
        for path, digest in read(OUT)['input_sha256'].items():
            assert sha(Path(path)) == digest, path
        print('Frozen extended official capacity scope verified')
        return
    proof_path = QA / 'verification.json'
    proof = read(proof_path)
    assert proof['status'] == 'passed' and proof['new_quality_scores'] == 0
    protocol_path = QA / 'diagnostic_frozen_before_scoring.json'
    assert sha(protocol_path) == proof['diagnostic_freeze_sha256']
    protocol = read(protocol_path)
    for path, digest in protocol['input_sha256'].items():
        assert sha(Path(path)) == digest, path
    expected_path = ROOT / 'analysis/optimization_20261003_r30/calibrated_csv_official.json'
    expected = read(expected_path)['metrics']
    sources = [Path(__file__), proof_path, protocol_path, expected_path]
    records, actual_jobs = [], 0
    for control in proof['execution_controls']:
        number = control['workers']
        result_path = QA / f'workers{number}_result.json'
        assert read(result_path) == control
        sources.append(result_path)
        if control['status'] != 'passed':
            assert control.get('records_per_minute_completed_control_only') is None
            continue
        samples_path = QA / f'workers{number}_samples.jsonl'
        assert sha(samples_path) == control['resource_samples_sha256']
        samples = [json.loads(line) for line in samples_path.read_text(encoding='utf-8').splitlines()]
        assert len(samples) == control['samples']
        assert min(s['available_bytes'] for s in samples) == control['minimum_available_bytes_sampled']
        assert max(s['own_worker_rss_sum_bytes'] for s in samples) == control['maximum_own_worker_rss_sum_bytes_sampled']
        histogram = dict(Counter(str(len(s['background'].get('actual_official_worker_pids', []))) for s in samples))
        assert histogram == control['actual_background_official_worker_count_samples']
        jobs = control['jobs_details']
        assert len(jobs) == control['jobs_completed'] == control['jobs_declared'] == 16
        assert {job['job'] for job in jobs} == set(range(16))
        assert all(job['metrics'] == expected for job in jobs)
        assert control['records_per_minute_completed_control_only'] == 16 * 60 / control['total_seconds_including_spawn_and_shutdown']
        actual_jobs += len(jobs)
        sources.append(samples_path)
        records.append({'workers': number, 'jobs': len(jobs),
            'observed_records_per_minute': control['records_per_minute_completed_control_only'],
            'minimum_available_ram_GiB_sampled': control['minimum_available_bytes_sampled'] / 2**30,
            'maximum_own_worker_rss_sum_GiB_sampled': control['maximum_own_worker_rss_sum_bytes_sampled'] / 2**30,
            'actual_background_official_worker_count_samples': histogram,
            'background_stage_samples': control['background_stage_samples'],
            'all_eight_metrics_bit_identical': True})
    assert [r['workers'] for r in records] == proof['completed_counts']
    payload = {'status': 'passed', 'at_local': time.strftime('%Y-%m-%dT%H:%M:%S'),
        'actual_completed_control_jobs': actual_jobs, 'execution_controls': records,
        'same5635800_row_actual_training_return_CSV_for_every_count': True,
        'all_completed_jobs_eight_metrics_bit_identical': True,
        'background_stages_and_worker_counts_differ_between_counts': True,
        'causal_isolated_throughput_winner_not_established': True,
        'larger_than_eight_worker_counts_not_tested': True,
        'full_forecast_construction_andmodel_training_throughput_not_tested': True,
        'memory_start_andstop_reserves_are_scheduling_rules_not_hardware_limits': True,
        'sum_RSS_may_include_shared_pages_more_than_once': True,
        'declared_production_rounds_preserve_frozen_four_worker_execution': True,
        'physical_resource_boundary_established': False,
        'global_search_exhaustion_established': False,
        'new_quality_scores': 0, 'test_labels_read': False,
        'input_sha256': {str(path.resolve()): sha(path) for path in sources}}
    with OUT.open('x', encoding='utf-8') as stream:
        json.dump(payload, stream, ensure_ascii=False, indent=2)
    print(json.dumps({'status': 'passed', 'actual_control_jobs': actual_jobs,
        'worker_counts': [r['workers'] for r in records],
        'physical_boundary_established': False, 'isolated_throughput_winner_established': False}))


if __name__ == '__main__':
    main()
