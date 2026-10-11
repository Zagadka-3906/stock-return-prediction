"""Check the highest closed candidate and preserve the historical delivery separately."""
from pathlib import Path
from datetime import datetime
import json
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path[:0] = [str(ROOT), str(A)]
from handoff_distribution_views_progress_monitor_20261006 import read, sha, create
from locked_read_hash_cache_20261004 import LockedReadHashCache
from atomic_optimization_observer_writes_20261005 import write


def main():
    import qualified_round_recovery_evidence_v3_20261006 as qualification
    out = A / 'current_best_frozen_candidate_audit_20261006'
    assert not out.exists()
    state = read(A / 'ongoing_optimization_state.json')
    assert state['actual_observer_version'] == 25
    number = state['best_completed_round']
    assert number == 65 and state['latest_completed_round'] == 82
    report_path = ROOT / f'results/optimization_20261003_r{number}.json'
    report = read(report_path)
    score = report['winner']['connected_final_score']
    assert score == state['completed_validation_best']
    candidate = Path(report['candidate_submission']).resolve()
    selection, manifest = read(candidate.parent / 'selection.json'), read(candidate.parent / 'manifest.json')
    verification = read(candidate.parent / 'verification.json')
    folder = A / f'optimization_20261003_r{number}'
    official = read(folder / 'calibrated_csv_official.json')
    assert selection['status'] == 'frozen_before_test_prediction'
    assert selection['winner']['connected_final_score'] == score
    assert report['test_labels_read_this_round'] is False
    assert verification['status'] == official['status'] == manifest['status'] == 'passed'
    assert official['metrics']['final_score'] == score
    assert (verification['rows'], verification['days'], verification['codes']) == (1599600, 344, 4650)
    for field in ('model_reload_bit_identical', 'pipeline_replay_bit_identical',
                  'csv_replay_byte_identical', 'csv_ranks_unchanged', 'cold80_day_prefix_bit_identical'):
        assert verification[field] is True
    assert verification['test_labels_read'] is official['test_labels_read'] is False
    release = read(ROOT / 'active_release.json')
    assert release['validation_score'] < score
    bindings = {}

    def bind(path, digest):
        path = Path(path)
        path = (path if path.is_absolute() else ROOT / path).resolve()
        assert not re.search(r'(?:Test[_-]?Y|测试集[_-]?Y|测试标签)', path.name, re.I), path
        if str(path) in bindings:
            assert bindings[str(path)] == digest
        bindings[str(path)] = digest

    for name, digest in selection['frozen_sha256'].items():
        bind(name, digest)
    for name, meta in manifest['files'].items():
        path = (candidate.parent / name).resolve()
        assert path.is_relative_to(candidate.parent) and path.stat().st_size == meta['bytes']
        bind(path, meta['sha256'])
    for path in (Path(__file__).resolve(), ROOT / '后续选模标准.md', ROOT / 'active_release.json',
                 report_path, candidate.parent / 'manifest.json', folder / 'calibrated_csv_official.json'):
        bind(path, sha(path))
    bind(candidate, verification['csv_sha256'])
    bind(folder / 'calibrated_validation.csv', official['csv_sha256'])
    out.mkdir()
    create(out / 'frozen_before_candidate_audit.json', {
        'at_local': datetime.now().isoformat(timespec='seconds'), 'input_sha256': bindings,
        'selected_round': number, 'selected_score': score, 'pending_required_rounds': state['pending_required_rounds'],
        'original_candidate_selected_before_future_inference': selection['frozen_at_local'],
        'current_published_full_ranking_records': state['completed_board_records'],
        'old_active_release_score': release['validation_score'],
        'new_model_fits': 0, 'new_quality_scores': 0, 'test_labels_read': False})
    try:
        with LockedReadHashCache(bindings) as cache:
            for path, digest in bindings.items():
                assert cache.sha(path) == digest
            evidence = qualification.complete_round_evidence(number)
            assert evidence is not None and evidence['score'] == score
            assert evidence['scored_records'] == report['scored_records'] == 172
            assert evidence['candidate_csv_sha256'] == verification['csv_sha256']
            qualification.close()
            cache.reverify()
            proof = {'status': 'passed_actual_current_best_closed_candidate_frozen_bytes_audit',
                'at_local': datetime.now().isoformat(timespec='seconds'), 'input_sha256': bindings,
                'actual_qualified_round_evidence': evidence, 'selected_round': number,
                'validation_score': score, 'candidate_submission': str(candidate),
                'candidate_sha256': verification['csv_sha256'], 'whole_future_shape': [1599600, 344, 4650],
                'original_complete_future_reload_cold80_and_causal_checks_preserved': True,
                'prior_complete_candidate_checks_freshly_validated_by_strict_round_gate': True,
                'additional_candidate_inference_performed_this_audit': False,
                'copied_manifest_files_checked': len(manifest['files']),
                'original_frozen_selection_bindings_checked': len(selection['frozen_sha256']),
                'all_input_bytes_rehashed_before_read_lock_release': True,
                'old_active_release_unchanged': True, 'old_active_release_score': release['validation_score'],
                'pending_required_rounds': state['pending_required_rounds'],
                'optimization_goal_complete': False, 'new_quality_scores': 0, 'new_model_fits': 0,
                'test_labels_read': False, 'global_resource_exhaustion_established': False}
            create(out / 'verification.json', proof)
        write(A / 'current_best_frozen_candidate.json', {
            'status': 'current_best_closed_validation_candidate', 'round': number,
            'validation_score': score, 'candidate_submission': str(candidate),
            'candidate_sha256': verification['csv_sha256'], 'audit': str(out / 'verification.json'),
            'audit_sha256': sha(out / 'verification.json'), 'pending_required_rounds': state['pending_required_rounds'],
            'all_validation_years_previously_viewed': True, 'selection_bias_uncorrected': True,
            'optimization_goal_complete': False, 'updated_at_local': datetime.now().isoformat(timespec='seconds')})
    except BaseException as error:
        create(out / 'failure.json', {'status': 'failed_actual_candidate_audit_preserved',
            'error': f'{type(error).__name__}: {error}', 'historical_delivery_pointer_unchanged': True})
        raise
    finally:
        qualification.close()
    print(json.dumps({'status': 'passed', 'round': number, 'validation_score': score,
        'manifest_files_checked': len(manifest['files']), 'frozen_bindings_checked': len(selection['frozen_sha256']),
        'old_release_score': release['validation_score'], 'pending_rounds': len(state['pending_required_rounds'])}), flush=True)


if __name__ == '__main__':
    main()
