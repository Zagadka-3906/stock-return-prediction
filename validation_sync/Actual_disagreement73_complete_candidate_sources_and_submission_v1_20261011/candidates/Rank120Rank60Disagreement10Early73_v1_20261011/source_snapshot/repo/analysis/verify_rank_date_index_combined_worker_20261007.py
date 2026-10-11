"""Execute the actual candidate adapter while reusing a byte-identical frozen official capsule."""
from pathlib import Path
from datetime import datetime
import json
import os
import sys
import time

for variable in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS', 'POLARS_MAX_THREADS'):
    os.environ[variable] = '8'
ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path[:0] = [str(ROOT), str(A), str(A / 'connected_validation_20261002')]
OUT = A / 'rank_date_index_combined_worker_preflight_20261007'
from handoff_distribution_views_progress_monitor_20261006 import read, sha, create
from win32_read_handle_hash_cache_with_filename_v2_20261006 import LockedReadHashCache


def initialize_with_readonly_observer(module_name, output, slots):
    import types
    import numpy as np
    import evaluate
    import classifier_consensus_recovery_official_speed_adapter_20261007 as adapter
    adapter.initialize(module_name, output, slots)
    ctx = adapter.original._CONTEXT
    ctx._rank_cache_control_original_score = ctx.score
    expected = np.load(A / 'optimization_20261003_r65/selected_validation.npy', mmap_mode='r')

    def observed_score(self, prediction):
        assert prediction.dtype == expected.dtype == np.dtype('float64')
        assert np.array_equal(prediction.view(np.uint64), expected.view(np.uint64))
        metrics = self._rank_cache_control_original_score(prediction)
        assert self.last_official_score_cache['cache_hit']
        assert metrics == read(A / 'optimization_20261003_r65/selection.json')['winner']['metrics']
        assert sha(Path(self.scoring) / 'submission.csv') == read(A / 'optimization_20261003_r65/calibrated_csv_official.json')['csv_sha256']
        return metrics

    ctx.score = types.MethodType(observed_score, ctx)

    def reject_unexpected_official_evaluator(*args, **kwargs):
        raise AssertionError('This control requires the original identical official capsule; no additional evaluator is allowed.')

    evaluate.evaluate = reject_unexpected_official_evaluator


def main():
    import psutil
    import classifier_consensus_recovery_official_speed_adapter_20261007 as adapter
    from hidden_windows_child_creation_20261006 import install as hide_children
    assert not OUT.exists()
    assert psutil.virtual_memory().available >= 8 * 1024**3
    prior = A / 'exact_rank_cache_windows_scoring_initializer_20261006/verification.json'
    proof = read(prior)
    assert proof['status'] == 'passed_actual_Windows_spawn_original_scoring_initializer_full_scheme_bits'
    winner = read(A / 'optimization_20261003_r65/selection.json')['winner']
    capsule = A / 'optimization_20261003_r65/identical_official_scores/e40e0143c78ed21b9471f98886f2a48dd29a90075c0db0c4055e8fc4e95de402.json'
    assert read(capsule)['metrics'] == winner['metrics']
    bindings = dict(proof['input_sha256'])
    for path in (Path(__file__).resolve(), A / 'verify_exact_rank_cache_actual_scoring_adapter_20261006.py', A / 'exact_rank_cache_actual_scoring_adapter_20261006/failure.json', prior, capsule, A / 'evaluate.py',
                 A / 'score_calibrated_candidates_20261003.py', A / 'official_validation_csv_parse_cache_20261003.py',
                 A / 'cross_round_official_score_reuse_20261003.py', A / 'identical_official_score_cache_20261003.py'):
        # evaluate.py is at the project root.
        path = ROOT / 'evaluate.py' if path == A / 'evaluate.py' else path
        bindings[str(path.resolve())] = sha(path)
    for extra in (A / 'classifier_consensus_recovery_official_speed_adapter_20261007.py', A / 'official_date_index_dataframe_adapter_20261007.py', A / 'official_date_index_speed_benchmark_20261007/verification.json'):
        bindings[str(extra.resolve())] = sha(extra)
    OUT.mkdir()
    create(OUT / 'frozen_before_actual_candidate_adapter.json', {
        'at_local': datetime.now().isoformat(timespec='seconds'), 'input_sha256': bindings,
        'original_complete_winner_repeated_for_cold_and_warm_execution': True,
        'scoring_cold_and_warm_controls_are_not_new_quality_records': True,
        'unexpected_official_evaluator_call_forbidden': True, 'test_labels_read': False})
    restore_children = hide_children()
    restore_adapter = adapter.install()
    adapter.original._initialize = initialize_with_readonly_observer
    timings = []
    rows = []
    try:
        with LockedReadHashCache(bindings):
            started = time.perf_counter()
            stream = adapter.original.evaluate_many('optimize_training_round65',
                [('cold', winner), ('warm', winner)], OUT)
            for key, row in stream:
                elapsed = time.perf_counter() - started
                started = time.perf_counter()
                assert row['metrics'] == winner['metrics']
                assert row['official_score_cache']['cache_hit']
                assert row['actual_original_official_date_index_execution']['date_index_lookups'] == 0
                execution = row['exact_daily_rank_execution']
                assert execution['installed_in_actual_scoring_worker']
                assert execution['maximum_bytes'] == 1024 * 1024**2
                create(OUT / (key + '_actual_complete_row.json'), row)
                if key == 'warm':
                    assert 0 < execution['after']['hits'] - execution['before']['hits'] <= 23
                    assert execution['after']['misses'] == execution['before']['misses']
                timings.append({'control': key, 'complete_candidate_seconds': elapsed,
                    'initialization_included_in_cold_only': key == 'cold', 'execution': execution})
                rows.append(row)
                print(json.dumps(timings[-1], ensure_ascii=False), flush=True)
            assert len(rows) == 2
            for key in ('metrics', 'construction', 'connected_final_score'):
                assert rows[0][key] == rows[1][key], key
            assert rows[0]['parallel_execution']['worker_pid'] == rows[1]['parallel_execution']['worker_pid']
        adapter.original.shutdown()
        adapter.original._initialize = adapter.initialize
        restore_adapter()
        restore_adapter = None
        events = restore_children()
        restore_children = None
        create(OUT / 'verification.json', {
            'status': 'passed_actual_combined_rank_date_index_two_candidate_Windows_spawn_and_original_capsule_bits',
            'at_local': datetime.now().isoformat(timespec='seconds'), 'input_sha256': bindings,
            'actual_complete_candidate_measurements': timings, 'actual_hidden_child_creations': events,
            'actual_original_candidate_pool_and_evaluate_functions_executed': True,
            'original_parent_root_signal_cache_retention_preserved': True,
            'warm_rank_call_count_measured_instead_of_assumed_from_independent_root_cache_clearing': True,
            'original_full5635800_predictions_and_scored_CSV_bytes_verified_each_call': True,
            'all8_original_official_metrics_exact': True, 'unexpected_official_evaluator_calls': 0, 'date_index_layer_present_but_not_claimed_invoked_for_cached_official_capsules': True, 'actual_fresh_official_date_index_full_and_tied_and_prefix_proof': str(A / 'official_date_index_speed_benchmark_20261007/verification.json'),
            'new_quality_records': 0, 'new_model_fits': 0,
            'training_only_validation_labels_read_for_original_causal_mapping': True,
            'test_labels_read': False, 'production_adoption_still_pending': True})
    except BaseException as error:
        create(OUT / 'failure.json', {'status': 'failed_preserved_actual_candidate_adapter_control',
            'error': f'{type(error).__name__}: {error}'})
        raise
    finally:
        adapter.original.shutdown()
        adapter.original._initialize = adapter.initialize if restore_adapter else adapter.original._initialize
        if restore_adapter:
            restore_adapter()
        if restore_children:
            create(OUT / 'actual_hidden_child_creations_failure.json', {'events': restore_children()})


if __name__ == '__main__':
    main()
