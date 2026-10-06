"""Verify actual completed scoring records without claiming candidate/full QA closure."""
from pathlib import Path
import hashlib
import json
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path[:0] = [str(ROOT), str(A)]
from run_dependency_queue_v3_20261006 import read, sha, create, owned


def main():
    import numpy as np
    from win32_read_handle_hash_cache_with_filename_v2_20261006 import LockedReadHashCache
    folder = A / 'optimization_20261003_r89'
    out = A / 'classifier_consensus124_official_scoring_snapshot_20261007'
    assert not out.exists()
    out.mkdir()
    identity = read(A / 'service_owned_workflows_20261006/classifier_consensus_round89_status_recovery/native_launch.json')
    assert owned(identity)
    paths = [folder / f'wave{n}_results.json' for n in (353, 354, 355, 356)]
    waves = [read(p) for p in paths]
    assert all(v['status'] == 'complete' for v in waves)
    assert [len(v['results']) for v in waves] == [73, 8, 18, 25]
    capsules = [Path(r['official_score_cache']['official_metrics_source']) for v in waves for r in v['results'].values()]
    sources = [Path(__file__), ROOT / 'evaluate.py', folder / 'protocol.json',
        A / 'classifier_consensus_recovery_official_speed_adapter_20261007.py',
        A / 'official_date_index_dataframe_adapter_20261007.py',
        A / 'exact_rank_cache_official_worker_adapter_20261006.py',
        A / 'github_validation_sync_main_20261005/round106_receipt.json',
        A / 'service_owned_workflows_20261006/classifier_consensus_round89_status_recovery/job_definition.json',
        A / 'service_owned_workflows_20261006/classifier_consensus_round89_status_recovery/native_launch.json']
    pins = {str(p): sha(p) for p in dict.fromkeys([*paths, *capsules, *sources])}
    assert pins[str(ROOT / 'evaluate.py')] == '72dc59987e92ba8ae6b506e114dfe8591b5608c9beccd0769d5d1f778f9189c2'
    create(out / 'frozen_before_actual_scoring_snapshot.json', {'input_sha256': pins,
        'actual_scientific_identity': identity, 'candidate_inference_and_full_QA_not_closed_by_this_snapshot': True})
    records = []
    with LockedReadHashCache(pins) as scope:
        for path, wave in zip(paths, waves):
            for key, row in wave['results'].items():
                cache = row['official_score_cache']
                capsule = Path(cache['official_metrics_source'])
                actual = read(capsule)['metrics']
                assert set(actual) == set(row['metrics']) and len(actual) == 8
                names = sorted(actual)
                assert np.array_equal(np.asarray([actual[k] for k in names], dtype='f8').view('u8'),
                    np.asarray([row['metrics'][k] for k in names], dtype='f8').view('u8'))
                assert np.float64(row['connected_final_score']).view('u8') == np.float64(actual['final_score']).view('u8')
                event = row['actual_original_official_date_index_execution']
                assert event['official_source_math_changed'] is False
                assert event['date_index_lookups'] in (0, 1212)
                if cache['cache_hit'] is False:
                    assert event['date_index_lookups'] == 1212
                records.append({'wave_file': str(path), 'case_key': key,
                    'complete_case_descriptor_sha256': hashlib.sha256(json.dumps(row, ensure_ascii=False, sort_keys=True).encode('utf-8')).hexdigest(),
                    'metrics': actual, 'official_capsule': str(capsule), 'official_capsule_sha256': sha(capsule),
                    'cache_hit': cache['cache_hit'], 'actual_date_index_execution': event})
        assert len(records) == 124
        scope.reverify()
        baseline = read(A / 'github_validation_sync_main_20261005/round106_receipt.json')['official_score']
        best = max(r['metrics']['final_score'] for r in records)
        create(out / 'verification.json', {'status': 'passed_actual124_completed_official_capsules_all8_bits_not_candidate_or_full_QA_qualification',
            'at_local': time.strftime('%Y-%m-%dT%H:%M:%S'), 'input_sha256': pins,
            'records': records, 'actual_completed_scoring_records': 124, 'declared_wave_counts': [73, 8, 18, 25],
            'all_original8_official_metric_bits_match_capsules': True,
            'actual_original_official_date_index_executions': sum(r['actual_date_index_execution']['date_index_lookups'] == 1212 for r in records),
            'actual_original_official_capsule_cache_hits': sum(r['cache_hit'] for r in records),
            'highest_completed_grid_score': best, 'qualified106_score': baseline,
            'grid_improves_qualified106': best > baseline,
            'source_and_capsule_initial_and_final_read_locked_full_hash': True,
            'new_model_fits_by_snapshot': 0, 'new_official_scores_by_snapshot': 0,
            'candidate_and_full_QA_or_main_qualification_not_claimed': True,
            'scientific_workers_stopped_or_restarted': 0, 'test_labels_read': False})


if __name__ == '__main__':
    main()
