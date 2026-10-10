"""Audit completed full-fit/future-replay samples and their actual overlap."""
from pathlib import Path
from collections import Counter
import hashlib
import json
import time

ROOT = Path(__file__).resolve().parents[1]
QA = ROOT / 'analysis/no_dropout_seed_future_models_qa_20261004'
OUT = ROOT / 'analysis/no_dropout_seed_future_resource_scope_audit_20261004.json'


def read(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    if OUT.exists():
        for path, digest in read(OUT)['input_sha256'].items():
            assert sha(Path(path)) == digest, path
        print('Frozen no-dropout full-fit/future resource scope verified')
        return
    summary_path = QA / 'resource_summary.json'
    samples_path = QA / 'resource_samples.jsonl'
    proof_path = QA / 'verification.json'
    summary, proof = read(summary_path), read(proof_path)
    assert summary['status'] == proof['status'] == 'passed'
    assert sha(summary_path) == proof['resource_summary_sha256']
    assert sha(samples_path) == summary['resource_samples_sha256']
    samples = [json.loads(line) for line in samples_path.read_text(encoding='utf-8').splitlines()]
    assert len(samples) == summary['samples'] and samples
    assert min(s['available_ram_bytes'] for s in samples) == summary['minimum_available_ram_bytes_sampled']
    assert max(s['qa_python_rss_bytes'] for s in samples) == summary['maximum_qa_python_rss_bytes_sampled']
    overlap = sum(bool(s['actual_official_worker_pids']) for s in samples)
    assert overlap == summary['samples_with_actual_official_workers']
    models = proof['native_models']
    assert len(models) == 8 and len({r['model'] for r in models}) == 8
    sources = [Path(__file__), summary_path, samples_path, proof_path]
    for record in models:
        assert record['mature_training']['rows'] == 6754006
        assert record['actual_full1599600_row_copied_model_reload_bit_identical']
        assert record['actual80_day_prefix_bit_identical']
        assert record['frozen_native_fitter_or_virtual_predictor_route_bit_identical']
        model_path = QA / (record['model'] + '.joblib')
        raw_path = QA / (record['model'] + '_raw.parquet')
        assert sha(model_path) == record['model_sha256']
        assert sha(raw_path) == record['raw_sha256']
        sources.extend((model_path, raw_path))
    minimum = min(samples, key=lambda s: s['available_ram_bytes'])
    maximum = max(samples, key=lambda s: s['qa_python_rss_bytes'])
    payload = {
        'status': 'passed', 'at_local': time.strftime('%Y-%m-%dT%H:%M:%S'),
        'actual_completed_fulltraining_artifacts': 8, 'actual_new_native_fulltraining_fits': 4, 'actual_virtual_fulltraining_artifacts': 4, 'mature_training_rows': 6754006,
        'actual_future_rows': proof['rows'], 'actual_future_days': proof['days'],
        'samples': len(samples), 'samples_with_actual_official_workers': overlap,
        'actual_official_worker_count_samples': dict(Counter(str(len(s['actual_official_worker_pids'])) for s in samples)),
        'minimum_available_ram_GiB_sampled': minimum['available_ram_bytes'] / 2**30,
        'maximum_qa_python_rss_GiB_sampled': maximum['qa_python_rss_bytes'] / 2**30,
        'minimum_available_ram_sample': minimum, 'maximum_qa_rss_sample': maximum,
        'phase_sample_counts': dict(Counter(s['phase'] for s in samples)),
        'rss_is_qa_process_only_not_total_physical_memory': True,
        'observed_peak_is_sampled_not_continuous': True,
        'official_overlap_observed_from_actual_process_trees': True,
        '12GiB_start_reserve_does_not_guarantee_peak_available_memory': True,
        'not_a_matched_parallelism_or_throughput_benchmark': True,
        'physical_resource_boundary_established': False,
        'global_resource_exhaustion_established': False,
        'scope': 'Completed four actual native full-training fits andfour embedded virtual artifacts with future/prefix/reload checks, with concurrent official scoring. This proves feasibility of this run only.',
        'new_quality_scores': 0, 'test_labels_read': False,
        'input_sha256': {str(p.resolve()): sha(p) for p in sources},
    }
    with OUT.open('x', encoding='utf-8') as stream:
        json.dump(payload, stream, ensure_ascii=False, indent=2)
    print(json.dumps({key: payload[key] for key in ('status', 'samples', 'actual_official_worker_count_samples', 'minimum_available_ram_GiB_sampled', 'maximum_qa_python_rss_GiB_sampled', 'physical_resource_boundary_established')}))


if __name__ == '__main__':
    main()
