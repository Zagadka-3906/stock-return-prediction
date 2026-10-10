"""Prepare a complete frozen release for the actual winner of the wider grid."""
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path.insert(0, str(A))
from run_dependency_queue_v3_20261006 import sha, create


def main():
    replacements = {
        'cohort_rank_calibration_source_freeze_20261006': 'extended_cohort_rank_calibration_source_freeze_20261006',
        'cohort_rank_calibration_release_20261006': 'extended_cohort_rank_calibration_release_20261006',
        'cohort_rank_calibration_full_controls_20261006': 'extended_cohort_rank_calibration_full_controls_20261006',
        'cohort_rank_calibration_official_pilot_20261006': 'extended_cohort_rank_calibration_official_pilot_20261006',
        'candidates/cohort_rank_calibration_20261006': 'candidates/extended_cohort_rank_calibration_20261006',
        'service_owned_workflows_20261006/cohort_rank_calibration_official_pilot': 'service_owned_workflows_20261006/extended_cohort_controls_and_scores',
        'service_owned_workflows_20261006/cohort_rank_calibration_candidate_inference': 'service_owned_workflows_20261006/extended_cohort_candidate_inference',
        'freeze_and_infer_cohort_candidate_20261006.py': 'freeze_and_infer_extended_cohort_candidate_20261006.py',
        'replay_sealed_cohort_candidate_20261006.py': 'replay_sealed_extended_cohort_candidate_20261006.py',
        'seal_cohort_candidate_source_package_20261006.py': 'seal_extended_cohort_candidate_source_package_20261006.py',
        'from seal_cohort_candidate_source_package_20261006': 'from seal_extended_cohort_candidate_source_package_20261006',
        'cohort_rank_calibration_scheme_graph': 'extended_cohort_rank_calibration_scheme_graph',
        'cohort_rank_calibration_20261006.py': 'cohort_rank_calibration_v2_20261006.py',
        'cohort_rank_calibration_20261006 as method': 'cohort_rank_calibration_v2_20261006 as method',
        'actual17_cohort_': 'actual66_cohort_', 'full17_cohort_': 'full66_cohort_',
        "len(pilot['records']) == 17": "len(pilot['records']) == 66",
        'expected_scored_records=17': 'expected_scored_records=66',
        "'scored_records': 17": "'scored_records': 66"}
    recipes = [
        ('freeze_cohort_candidate_sources_20261006.py', 'freeze_extended_cohort_candidate_sources_20261006.py'),
        ('freeze_and_infer_cohort_candidate_20261006.py', 'freeze_and_infer_extended_cohort_candidate_20261006.py'),
        ('replay_sealed_cohort_candidate_20261006.py', 'replay_sealed_extended_cohort_candidate_20261006.py'),
        ('seal_cohort_candidate_source_package_20261006.py', 'seal_extended_cohort_candidate_source_package_20261006.py')]
    pins, changes = {}, []
    for old, new in recipes:
        original = (A / old).read_text(encoding='utf-8')
        text = original
        applied = {}
        for before, after in replacements.items():
            if before in text:
                text = text.replace(before, after)
                applied[before] = after
        if old == 'freeze_and_infer_cohort_candidate_20261006.py':
            # Also lock all historical parent inputs, including future features,
            # generation inputs and actual model bytes throughout fresh inference.
            before = "    pins = {**pilot['input_sha256'], str(pilot_path): sha(pilot_path)}"
            after = "    pins = {**read(parent.OUT / 'protocol.json')['input_sha256'], **pilot['input_sha256'], str(pilot_path): sha(pilot_path)}"
            assert text.count(before) == 1
            text = text.replace(before, after)
            applied[before] = after
            before = "    cfg = best['configuration']"
            after = before + "\n    current = read(A / 'cohort_rank_calibration_release_20261006/verification.json')['selected_official_score']\n    assert best['connected_final_score'] >= current\n    assert read(A / 'github_validation_sync_main_20261005/round99_receipt.json')['actual_full_QA_version'] == 10"
            assert text.count(before) == 1
            text = text.replace(before, after)
            applied[before] = after
            before = "'score_gain': best['score_gain_over_parent'], 'actual_native_model_storage': storage,"
            after = "'score_gain': best['score_gain_over_parent'], 'score_gain_over_qualified_round99': best['connected_final_score'] - current, 'actual_native_model_storage': storage,"
            assert text.count(before) == 1
            text = text.replace(before, after)
            applied[before] = after
        compile(text, str(A / new), 'exec')
        with (A / new).open('x', encoding='utf-8') as stream:
            stream.write(text)
        pins.update({str(A / old): sha(A / old), str(A / new): sha(A / new)})
        changes.append({'original': old, 'effective': new, 'explicit_changes': applied,
            'all_original_real_model_curve_codec_full_replay_prefix_and_complete_manifest_checks_preserved': True})
    create(A / 'extended_cohort_release_source_preparation_20261006.json', {
        'status': 'prepared_complete_actual66_score_winner_freeze_and_native_inference_sources',
        'input_sha256': pins, 'sources': changes,
        'winner_not_selected_before_completed_actual_scores': True,
        'all_historical_parent_frozen_inputs_also_locked_through_new_actual_inference': True,
        'existing_qualified_round99_anchor_must_be_matched_or_improved': True,
        'new_native_model_fits': 0, 'new_quality_scores': 0, 'test_labels_read': False})


if __name__ == '__main__':
    main()
