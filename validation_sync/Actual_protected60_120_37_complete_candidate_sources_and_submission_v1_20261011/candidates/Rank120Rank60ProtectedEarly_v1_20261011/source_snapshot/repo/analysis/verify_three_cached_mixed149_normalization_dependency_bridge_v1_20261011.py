"""Resolve a legacy wait name by verifying the actual after188 normalization output.

This service is a compatibility gate, not a second normalization or scoring run.
Original source files, failed records, scores and frozen hashes remain intact.
"""
from pathlib import Path
import sys

A = Path(__file__).resolve().parent
sys.path[:0] = [str(A.parent), str(A)]
from run_dependency_queue_v3_20261006 import read, sha, create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed, closed

TARGET = 'actual_three_cached_mixed149_after188_normalization_v1_20261011'
LEGACY = 'actual_three_cached_mixed149_after186_normalization_v1_20261011'
PROOF = A / 'three_cached_mixed149_after188_legacy_wait_verified_bridge_v1_20261011.json'


def main():
    assert allowed()
    closed(TARGET)
    pointer = A / 'actual_three_cached_mixed_complete149_after188_location_v1_20261011.json'
    location = read(pointer)
    folder = Path(location['output'])
    pilot_path, verification_path = folder / 'pilot149.json', folder / 'verification.json'
    pilot, verification = read(pilot_path), read(verification_path)
    assert sha(pilot_path) == location['pilot_sha256']
    assert sha(verification_path) == location['verification_sha256']
    assert pilot['status'] == 'passed_normalized149_actual_TRAIN_official_records_selected_native_and_full_future_pending'
    assert verification['status'] == 'passed_complete149_actual_TRAIN_records_without_future_features'
    assert len(pilot['records']) == pilot['expected_scored_records'] == 149
    assert (pilot['actual_nonidentity_full_controls'], pilot['actual_nonidentity_prefix_controls']) == (144, 432)
    assert pilot['actual_comparison_parent_round'] == 188
    assert verification['best'] == pilot['best']
    assert pilot['new_quality_scores_by_normalization'] == pilot['new_native_fits'] == 0
    assert not pilot['actual_future_X_read'] and not pilot['test_labels_read']
    for path, digest in pilot['input_sha256'].items():
        assert sha(path) == digest, path
    assert allowed()
    create(PROOF, {
        'status': 'passed_actual_after188_normalization_provenance_for_legacy_after186_wait',
        'legacy_wait_service_name': LEGACY,
        'actual_normalization_service': TARGET,
        'actual_comparison_parent_round': 188,
        'input_sha256': {str(p): sha(p) for p in (Path(__file__), pointer, pilot_path, verification_path)},
        'actual_records': 149,
        'actual_full_controls': 144,
        'actual_prefix_controls': 432,
        'new_normalization_runs': 0,
        'new_quality_scores': 0,
        'new_native_fits': 0,
        'original_qualifier_sources_and_pins_preserved': True,
        'native_qualification_and_candidate_still_pending': True,
        'test_labels_read': False,
    })
    print({'actual_after188_normalization_verified': True, 'compatibility_wait_resolved': LEGACY}, flush=True)


if __name__ == '__main__':
    main()
