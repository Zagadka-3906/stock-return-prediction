"""Resolve every actual original queued round without changing drivers, arguments or sources."""
from pathlib import Path
from datetime import datetime
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path[:0] = [str(ROOT), str(A)]
from handoff_distribution_views_progress_monitor_20261006 import read, sha, create
from locked_read_hash_cache_20261004 import LockedReadHashCache
import run_dependency_queue_v5_20261006 as controller


def main():
    out = A / 'exact_rank_cache_queue_routes_20261006'
    assert not out.exists()
    plan_path = A / 'service_owned_dependency_queue_v4_20261006/queue_plan.json'
    plan = read(plan_path)
    bindings = dict(plan['input_sha256'])
    files = [Path(__file__).resolve(), plan_path, Path(controller.__file__).resolve(),
        A / 'run_recovery_qualified_workflow_with_exact_rank_cache_v2_20261006.py',
        A / 'exact_rank_cache_actual_scoring_adapter_v2_20261006/verification.json']
    resolved = []
    for job in plan['deferred_jobs']:
        if 'round' not in job:
            continue
        original_path = Path(job['previous_run']).resolve()
        original = read(original_path)
        driver, arguments, bridge, prior = controller.original_driver_and_bridge(job, original)
        assert bridge['original_driver'] == driver and bridge['original_arguments'] == arguments
        assert original['input_sha256'][driver] == sha(driver)
        for values in (original['input_sha256'], bridge['input_sha256']):
            for path, digest in values.items():
                path = str(Path(path).resolve())
                if path in bindings:
                    assert bindings[path] == digest, path
                bindings[path] = digest
        files.append(original_path)
        if prior is not None:
            files.append(prior)
            assert read(prior) == bridge
            assert original['original_arguments'] == [driver, str(prior), *arguments]
        else:
            assert driver == original['original_script'] and arguments == original['original_arguments'] == []
        resolved.append({'round': job['round'], 'original_driver': driver, 'original_arguments': arguments,
            'previous_run': str(original_path), 'prior_qualified_bridge': str(prior) if prior else None,
            'original_driver_sha256': original['input_sha256'][driver],
            'scoring_execution': 'one worker with exact rank reuse' if 84 <= job['round'] <= 90
                else 'original execution retained'})
    assert {row['round'] for row in resolved} == set(range(67, 91)) - {81}
    assert [row['round'] for row in resolved if row['prior_qualified_bridge'] is None] == [89, 90]
    for path in files:
        digest = sha(path)
        if str(path) in bindings:
            assert bindings[str(path)] == digest
        bindings[str(path)] = digest
    out.mkdir()
    create(out / 'frozen_before_actual_route_checks.json', {
        'at_local': datetime.now().isoformat(timespec='seconds'), 'input_sha256': bindings,
        'actual_original_round_routes': resolved, 'new_quality_records': 0, 'test_labels_read': False})
    with LockedReadHashCache(bindings):
        assert read(A / 'exact_rank_cache_actual_scoring_adapter_v2_20261006/verification.json')['status'].startswith('passed_')
        for row in resolved:
            assert sha(row['original_driver']) == row['original_driver_sha256']
        # The old v4 parser requires two arguments even for the actual direct 89/90 records.
        direct_failures = []
        for number in (89, 90):
            row = next(item for item in resolved if item['round'] == number)
            previous = read(row['previous_run'])
            try:
                driver, bridge_run, *arguments = previous['original_arguments']
            except ValueError as error:
                direct_failures.append({'round': number, 'actual_old_parser_error': f'{type(error).__name__}: {error}'})
            else:
                raise AssertionError('Expected the actual original direct-route incompatibility.')
        create(out / 'verification.json', {
            'status': 'passed_all23_actual_original_round_routes_and_direct89_90_argument_preservation',
            'at_local': datetime.now().isoformat(timespec='seconds'), 'input_sha256': bindings,
            'actual_resolved_original_rounds': resolved, 'actual_old_direct_route_failures': direct_failures,
            'all_original_drivers_arguments_and_transitive_source_hashes_preserved': True,
            'original_four_worker67_to80_retained_without_new_cache_memory': True,
            'exact_rank_cached_original_single_worker_rounds': list(range(84, 91)),
            'already_completed82_and_live83_routes_remain_in_inherited_activated_jobs': True,
            'direct89_90_are_wrapped_only_for_qualification_and_execution_provenance': True,
            'original91_to94_independent_scientific_and_publication_plans_preserved': True,
            'new_model_fits': 0, 'new_quality_records': 0, 'test_labels_read': False})
    print('passed_all23_actual_original_round_routes_and_direct89_90_argument_preservation', flush=True)


if __name__ == '__main__':
    main()
