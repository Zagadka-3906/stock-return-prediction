"""Prospective qualified bridge retaining full grids with tested exact scoring execution."""
from pathlib import Path
import json
import runpy
import sys

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path[:0] = [str(ROOT), str(A)]


def main():
    driver, run_path, *arguments = sys.argv[1:]
    run_path = Path(run_path).resolve()
    run = json.loads(run_path.read_text(encoding='utf-8-sig'))
    assert run['round'] == 97
    from locked_read_hash_cache_20261004 import fresh_sha
    sources = [Path(__file__).resolve(), A / 'exact_daily_rank_memoization_20261006.py',
        A / 'exact_rank_cache_official_worker_adapter_20261006.py',
        A / 'exact_daily_rank_memoization_preflight_20261006/verification.json',
        A / 'exact_rank_cache_complete_scheme_20261006/verification.json',
        A / 'exact_rank_cache_complete_scheme_v2_20261006/verification.json',
        A / 'exact_rank_cache_windows_scoring_initializer_20261006/verification.json',
        A / 'exact_rank_cache_actual_scoring_adapter_v2_20261006/verification.json']
    sources += [A / 'root_and_rank_cache_official_worker_adapter_20261006.py',
        A / 'bounded_root_replay_memoization_20261006.py',
        A / 'bounded_root_replay_full_controls_20261006/verification.json',
        A / 'root_and_rank_cache_actual_worker_controls_20261006/verification.json']
    for source in sources:
        assert run['input_sha256'][str(source)] == fresh_sha(source), source
    spawn = json.loads((A / 'exact_rank_cache_actual_scoring_adapter_v2_20261006/verification.json').read_text(encoding='utf-8'))
    assert spawn['status'] == 'passed_actual_two_candidate_adapter_calls_original_official_capsule_and_full_bits'
    import frozen_provenance_execution_scope_20261004 as provenance
    import root_and_rank_cache_official_worker_adapter_20261006 as adapter
    worker_control = json.loads(sources[-1].read_text(encoding='utf-8'))
    assert worker_control['status'] == 'passed_actual_Windows_worker_combined_caches_full_bits_CSV8_metrics_and_changed_downstream_graph'
    assert worker_control['all5635800_raw_bits_and_complete_mapped_CSV_bytes_verified_each_call']
    assert worker_control['all8_original_official_metrics_exact_each_call']
    assert adapter.read_control()['warm_prediction_median_improved']

    original_scope = provenance.FrozenProvenanceExecutionScope

    def extended_scope(module, extra_sources, metadata, analysis_root):
        return original_scope(module, list(dict.fromkeys([*extra_sources, *sources])), {
            **metadata, 'exact_daily_rank_execution_adapter': str(Path(adapter.__file__).resolve()),
            'effective_exact_rank_cache_launcher': str(Path(__file__).resolve()),
            'actual_Windows_spawn_and_complete5635800_row_bit_controls_required': True,
            'rank_cache_maximum_bytes_per_worker': adapter.ranks.MAXIMUM_BYTES,
            'root_cache_maximum_payload_bytes_per_worker': adapter.MAXIMUM_BYTES,
            'root_payload_cap_is_not_total_RSS_cap': True,
            'scientific_grid_full_rows_and_official_evaluator_unchanged': True,
            'scoring_executor_initializer_and_each_case_statistics_recorded': True}, analysis_root)

    restore = adapter.install()
    provenance.FrozenProvenanceExecutionScope = extended_scope
    sys.argv = [str(A / 'run_joint_goss_quality_qualified_workflow_v3_20261006.py'), driver, str(run_path), *arguments]
    try:
        runpy.run_path(sys.argv[0], run_name='__main__')
    finally:
        adapter.original.shutdown()
        restore()
        provenance.FrozenProvenanceExecutionScope = original_scope


if __name__ == '__main__':
    main()
