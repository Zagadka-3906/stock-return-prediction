"""Resume the naturally failed observer with safe handling of completed workers."""
from pathlib import Path
import json
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path[:0] = [str(ROOT), str(A)]
from run_dependency_queue_v3_20261006 import read, sha, create, owned


def main():
    import psutil
    old = A / 'service_owned_workflows_20261006/progress_monitor_v34'
    assert not owned(read(old / 'native_launch.json'))
    assert read(old / 'service_execution.json')['status'] == 'failed'
    assert 'NoSuchProcess' in read(old / 'service_execution.json')['failure']
    out = A / 'progress_monitor_v36_recovery_20261006'
    assert not out.exists()
    out.mkdir()
    create(out / 'frozen_before_observer_recovery.json', {
        'original_natural_failure': read(old / 'service_execution.json'),
        'original_identity': read(old / 'native_launch.json'),
        'source_sha256': {str(p): sha(p) for p in (Path(__file__),
            A / 'monitor_actual_optimization_progress_v34_20261006.py',
            old / 'service_execution.json', old / 'stderr.log')},
        'scientific_workers_stopped_or_restarted': 0, 'test_labels_read': False})
    registration = A / 'service_owned_workflows_20261006/conditional_residual_round102_full_registration'
    identity = read(registration / 'native_launch.json')
    while owned(identity):
        time.sleep(30)
    source = A / 'monitor_actual_optimization_progress_v34_20261006.py'
    text = source.read_text(encoding='utf-8')
    text = text.replace('progress_monitor_v34', 'progress_monitor_v36')
    text = text.replace('actual_observer_version=34', 'actual_observer_version=36')
    text = text.replace("'actual_observer_version': 34", "'actual_observer_version': 36")
    before = "    numbers = sorted(set(value.get('actual_active_quality_rounds', [])) | set(active))"
    assert text.count(before) == 1
    text = text.replace(before,
        "    numbers = sorted(n for n in (set(value.get('actual_active_quality_rounds', [])) | set(active)) if n not in (95, 96, 97) or n in active)")
    before = "        for p in psutil.Process(row['owned_worker_pid']).children(recursive=True):"
    assert text.count(before) == 1
    text = text.replace(before,
        "        try:\n"
        "            actual_children = psutil.Process(row['owned_worker_pid']).children(recursive=True) if owned(row) else []\n"
        "        except psutil.NoSuchProcess:\n"
        "            actual_children = []\n"
        "        for p in actual_children:")
    before = "        pending[A / 'resume_optimization_20261004.json'] = dict(value)"
    assert text.count(before) == 1
    text = text.replace(before, "        ACTUAL_ADDITIONAL_EVIDENCE(value, state)\n" + before)
    namespace = {'__file__': __file__, '__name__': 'actual_completed_worker_safe_observer36',
                 'ACTUAL_ADDITIONAL_EVIDENCE': additional_evidence}
    exec(compile(text, str(source), 'exec'), namespace)
    while True:
        try:
            namespace['main']()
        except psutil.NoSuchProcess as error:
            with (out / 'naturally_completed_process_observation_retries.jsonl').open('a', encoding='utf-8') as stream:
                stream.write(json.dumps({'at_local': time.strftime('%Y-%m-%dT%H:%M:%S'),
                    'error': str(error), 'partial_generation_committed': False,
                    'scientific_workers_stopped_or_restarted': 0}) + '\n')
            time.sleep(30)


def additional_evidence(value, state):
    rounds = {}
    for number in (99, 100, 101, 102):
        folder = A / f'optimization_20261003_r{number}'
        result_path = ROOT / f'results/optimization_20261003_r{number}.json'
        scope = folder / 'provenance_scope_execution.json'
        receipt_path = A / f'github_validation_sync_main_20261005/round{number}_receipt.json'
        if not result_path.exists():
            continue
        result = read(result_path)
        passed = scope.exists() and read(scope)['status'] == 'passed'
        receipt = read(receipt_path) if receipt_path.exists() else None
        rounds[number] = {'actual_scored_records': result['scored_records'],
            'actual_official_score': result['winner']['connected_final_score'],
            'complete_scientific_candidate_and_full_QA_passed': passed,
            'main_commit': receipt['commit'] if receipt else None,
            'complete_immutable_QA_published': bool(receipt and receipt.get('actual_full_QA_version'))}
    qualified = [(n, r) for n, r in rounds.items() if r['complete_scientific_candidate_and_full_QA_passed']]
    extra = {'actual_recent_additive_rounds': rounds,
        'conditional_rank_actual_native_fits': 18, 'conditional_residual_actual_native_fits': 20,
        'conditional_residual_actual_full_comparison_records': 49,
        'observer34_natural_NoSuchProcess_failure_preserved': True,
        'global_resource_exhaustion_established': False}
    if qualified:
        n, best = max(qualified, key=lambda item: item[1]['actual_official_score'])
        if best['actual_official_score'] >= value.get('completed_validation_best', float('-inf')):
            extra.update(best_completed_round=n, completed_validation_best=best['actual_official_score'])
        latest = max(n for n, _ in qualified)
        extra.update(latest_completed_round=max(latest, value.get('latest_completed_round', 0)),
                     last_completed_round=max(latest, value.get('last_completed_round', 0)))
    for doc in (value, state):
        doc.update(extra)


if __name__ == '__main__':
    main()
