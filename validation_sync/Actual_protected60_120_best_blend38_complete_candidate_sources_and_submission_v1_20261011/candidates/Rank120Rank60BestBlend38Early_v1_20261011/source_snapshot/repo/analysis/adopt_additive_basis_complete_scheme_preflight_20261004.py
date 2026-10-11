"""Adopt passed versioned actual controls while preserving the failed fixture."""
from pathlib import Path
import hashlib
import json
import time

ROOT = Path(__file__).resolve().parents[1]
ACTUAL = ROOT / 'analysis/additive_basis_complete_scheme_preflight_v2_20261004'
CANONICAL = ROOT / 'analysis/additive_basis_complete_scheme_preflight_20261004/verification.json'
AUDIT = ROOT / 'analysis/additive_basis_complete_scheme_preflight_adoption_20261004.json'


def read(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def create(path, value):
    with path.open('x', encoding='utf-8') as stream:
        json.dump(value, stream, ensure_ascii=False, indent=2)


def main():
    proof_path = ACTUAL / 'verification.json'
    if not proof_path.exists():
        print('Actual versioned complete-scheme controls are still pending; no gate created.')
        return
    proof = read(proof_path)
    assert proof['status'] == 'passed'
    assert proof['new_quality_scores'] == 0 and proof['test_labels_read'] is False
    for path, digest in proof['input_sha256'].items():
        assert sha(Path(path)) == digest, path
    replay_path = ACTUAL / 'parameter_andreplay_checks.json'
    assert sha(replay_path) == proof['parameter_replay_sha256']
    assert read(replay_path)['status'] == 'passed'
    cases = ('role_baseline', 'standalone_baseline', 'role_changed', 'pure_changed')
    for label in cases:
        candidate_path = ACTUAL / label / 'candidate/verification.json'
        assert sha(candidate_path) == proof['candidate_verification_sha256'][label]
        candidate = read(candidate_path)
        assert candidate['status'] == 'passed' and candidate['validation_score'] is None
        if label.endswith('baseline'):
            assert sha(candidate_path.parent / 'submission.csv') == sha(ROOT / 'candidates/optimization_20261003_r29/submission.csv')
    required = (
        'actual_new_contexts_complete5635800_row_prior_output_andall8_metrics_exact',
        'new_role_each_target_layout_androle_cold_prefix_controls_passed',
        'actual_standalone_branch_replacement_andindependent_composition_checks_passed',
        'actual_release_context_shared_causal_calibration_passed',
        'actual_new_future_helper_full1599600_row_baseline_CSV_byte_identical',
        'actual_changed_role_andnative_standalone_copied_model_future_CSV_andcold80_day_checks_passed',
    )
    assert all(proof[key] is True for key in required)
    sources = [Path(__file__), proof_path, replay_path,
        ROOT / 'analysis/additive_basis_complete_scheme_preflight_recovery_20261004.json',
        ROOT / 'analysis/additive_basis_complete_scheme_preflight_20261004/frozen_before_controls.json']
    if CANONICAL.exists():
        canonical = read(CANONICAL)
        assert canonical['actual_checker_sha256'] == sha(proof_path)
        for path, digest in canonical['adoption_input_sha256'].items():
            assert sha(Path(path)) == digest, path
    else:
        canonical = {**proof,
            'adopted_at_local': time.strftime('%Y-%m-%dT%H:%M:%S'),
            'actual_checker': str(proof_path.relative_to(ROOT)),
            'actual_checker_sha256': sha(proof_path),
            'fixture_recovery_evidence': str(sources[3].relative_to(ROOT)),
            'original_failed_fixture_preserved': True,
            'production_prediction_search_algorithms_unchanged_by_recovery': True,
            'adoption_input_sha256': {str(path.resolve()): sha(path) for path in sources}}
        create(CANONICAL, canonical)
    if not AUDIT.exists():
        create(AUDIT, {'status': 'passed', 'at_local': time.strftime('%Y-%m-%dT%H:%M:%S'),
            'canonical_verification': str(CANONICAL.relative_to(ROOT)),
            'canonical_verification_sha256': sha(CANONICAL),
            'actual_checker': str(proof_path.relative_to(ROOT)), 'actual_checker_sha256': sha(proof_path),
            'original_failed_fixture_preserved': True,
            'actual_previous_R50_R51_required_for_official_searches': True,
            'prototype_controls_not_added_to_official_quality_rankings': True,
            'new_quality_scores': 0, 'test_labels_read': False})
    assert read(AUDIT)['canonical_verification_sha256'] == sha(CANONICAL)
    print('Passed actual complete-scheme controls adopted; original failed fixture preserved.')


if __name__ == '__main__':
    main()
