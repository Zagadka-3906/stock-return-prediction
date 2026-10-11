"""Preserve all scientific routes and change only R97's tested worker initializer."""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path.insert(0, str(A))
from run_dependency_queue_v3_20261006 import create, sha, read


def once(source, old, new):
    assert source.count(old) == 1, old
    return source.replace(old, new)


def main():
    original_wrapper = A / 'run_joint_goss_quality_with_exact_rank_cache_v3_20261006.py'
    wrapper = original_wrapper.read_text(encoding='utf-8')
    wrapper = once(wrapper,
        "    for source in sources:\n", "    sources += [A / 'root_and_rank_cache_official_worker_adapter_20261006.py',\n"
        "        A / 'bounded_root_replay_memoization_20261006.py',\n"
        "        A / 'bounded_root_replay_full_controls_20261006/verification.json',\n"
        "        A / 'root_and_rank_cache_actual_worker_controls_20261006/verification.json']\n"
        "    for source in sources:\n")
    wrapper = once(wrapper, "spawn = json.loads(sources[-1].read_text(encoding='utf-8'))",
        "spawn = json.loads((A / 'exact_rank_cache_actual_scoring_adapter_v2_20261006/verification.json').read_text(encoding='utf-8'))")
    wrapper = once(wrapper, 'import exact_rank_cache_official_worker_adapter_20261006 as adapter',
        "import root_and_rank_cache_official_worker_adapter_20261006 as adapter\n"
        "    worker_control = json.loads(sources[-1].read_text(encoding='utf-8'))\n"
        "    assert worker_control['status'] == 'passed_actual_Windows_worker_combined_caches_full_bits_CSV8_metrics_and_changed_downstream_graph'\n"
        "    assert worker_control['all5635800_raw_bits_and_complete_mapped_CSV_bytes_verified_each_call']\n"
        "    assert worker_control['all8_original_official_metrics_exact_each_call']\n"
        "    assert adapter.read_control()['warm_prediction_median_improved']\n")
    wrapper = once(wrapper, "'rank_cache_maximum_bytes_per_worker': adapter.MAXIMUM_BYTES,",
        "'rank_cache_maximum_bytes_per_worker': adapter.ranks.MAXIMUM_BYTES,\n"
        "            'root_cache_maximum_payload_bytes_per_worker': adapter.MAXIMUM_BYTES,\n"
        "            'root_payload_cap_is_not_total_RSS_cap': True,")
    queue_source = A / 'run_dependency_queue_v10_20261006.py'
    queue = once(queue_source.read_text(encoding='utf-8'),
        'run_joint_goss_quality_with_exact_rank_cache_v3_20261006.py',
        'run_joint_goss_quality_with_root_and_rank_cache_v4_20261006.py')
    observer_source = A / 'monitor_actual_optimization_progress_v34_20261006.py'
    observer = once(observer_source.read_text(encoding='utf-8'),
        'for version in (10, 9, 8, 7, 6, 5, 4):',
        'for version in (11, 10, 9, 8, 7, 6, 5, 4):')
    assert observer.count('actual_observer_version=34') == 2
    assert observer.count("'actual_observer_version': 34") == 1
    observer = observer.replace('actual_observer_version=34', 'actual_observer_version=35').replace(
        "'actual_observer_version': 34", "'actual_observer_version': 35")
    files = {A / 'run_joint_goss_quality_with_root_and_rank_cache_v4_20261006.py': wrapper,
        A / 'run_dependency_queue_v11_20261006.py': queue,
        A / 'monitor_actual_optimization_progress_v35_20261006.py': observer}
    for path, source in files.items():
        compile(source, str(path), 'exec')
        with path.open('x', encoding='utf-8', newline='\n') as stream:
            stream.write(source)
    plan = read(A / 'service_owned_dependency_queue_v4_20261006/queue_plan_v10.json')
    create(A / 'root_cached_round97_dispatch_preparation_20261006.json', {
        'status': 'prepared_same_all_original_routes_with_only_root_rank_worker_R97_execution_change',
        'original_sources': {str(p): sha(p) for p in (original_wrapper, queue_source, observer_source)},
        'new_sources': {str(p): sha(p) for p in files},
        'original_deferred_jobs': plan['deferred_jobs'],
        'all_original_markers_parent_gates_and_151_scientific_configurations_unchanged': True,
        'actual_full_worker_controls_required_before_adoption': True,
        'no_live_scientific_job_may_be_stopped_or_restarted': True,
        'runtime_adopted': False, 'new_quality_records': 0, 'new_native_fits': 0})


if __name__ == '__main__':
    main()
