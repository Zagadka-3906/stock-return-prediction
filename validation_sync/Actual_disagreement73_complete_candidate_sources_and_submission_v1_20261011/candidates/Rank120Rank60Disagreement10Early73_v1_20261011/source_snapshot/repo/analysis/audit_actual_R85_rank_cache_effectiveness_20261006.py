"""Summarize measured scoring-cache behavior without inferring parent-prefix speed or exhaustion."""
from pathlib import Path
import json
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path[:0] = [str(ROOT), str(A)]
from run_dependency_queue_v3_20261006 import read, sha, create

OUT = A / 'actual_R85_rank_cache_effectiveness_20261006'


def main():
    assert not OUT.exists(); OUT.mkdir()
    paths = sorted((A / 'optimization_20261003_r85').glob('wave*_results.json'))
    receipt_path = A / 'github_validation_sync_main_20261005/round85_receipt.json'
    receipt = read(receipt_path)
    assert receipt['status'] == 'pushed_and_remote_head_verified' and receipt['scored_records'] == 100
    inputs = {str(p.resolve()): sha(p) for p in [Path(__file__), receipt_path, *paths]}
    create(OUT / 'frozen_before_audit.json', {'input_sha256': inputs,
        'scope': 'All100 completed R85 scoring-worker cache events; parent prefix runtime not measured here'})
    records = []
    for path in paths:
        payload = read(path); assert payload['status'] == 'complete'
        for key, row in payload['results'].items():
            event = row['exact_daily_rank_execution']
            before, after = event['before'], event['after']
            assert event['installed_in_actual_scoring_worker'] is True
            assert event['scientific_configuration_and_official_evaluator_unchanged'] is True
            assert event['maximum_bytes'] == after['maximum_bytes'] == 1024**3
            assert after['retained_bytes'] <= 1024**3
            fields = ('hits', 'misses', 'evictions', 'hash_seconds', 'original_function_seconds')
            delta = {name: after[name] - before[name] for name in fields}
            assert all(value >= 0 for value in delta.values())
            records.append({'wave': path.stem, 'case': key, 'delta': delta,
                'retained_bytes': after['retained_bytes'], 'official_score': row['connected_final_score']})
    assert len(records) == 100
    totals = {name: sum(row['delta'][name] for row in records) for name in fields}
    for path, digest in inputs.items(): assert sha(path) == digest, path
    proof = {'status': 'passed_all100_actual_R85_scoring_worker_cache_events_audited',
        'at_local': time.strftime('%Y-%m-%dT%H:%M:%S'), 'input_sha256': inputs,
        'actual_scored_records': len(records), 'all_case_events': records, 'measured_totals': totals,
        'maximum_retained_bytes': max(row['retained_bytes'] for row in records),
        'zero_hit_cases_with_evictions': sum(row['delta']['hits'] == 0 and row['delta']['evictions'] > 0 for row in records),
        'max_cache_bytes': 1024**3, 'source_round_main_commit': receipt['commit'],
        'decision': 'Keep current1GiB scoring cache; these observed events do not justify enlarging scoring-worker memory.',
        'parent_prefix_cache_adoption_requires_separate_full_control': True,
        'scoring_worker_statistics_not_used_to_infer_parent_prefix_or_entire_pipeline_speedup': True,
        'global_resource_exhaustion_established': False,
        'new_model_fits': 0, 'new_quality_scores': 0, 'test_labels_read': False}
    create(OUT / 'verification.json', proof)
    print(json.dumps({'status': proof['status'], 'records': len(records), 'measured_totals': totals}, ensure_ascii=False), flush=True)


if __name__ == '__main__': main()
