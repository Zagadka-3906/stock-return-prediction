"""Prepare explicit source-freeze, seal and admission routes for the14-model replay."""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path.insert(0, str(A))
from run_dependency_queue_v3_20261006 import create, sha


def main():
    routes = {
        'freeze_cohort_candidate_sources_20261006.py': ('freeze_conditional_flag_candidate_sources_20261006.py', {
            'cohort_rank_calibration_source_freeze_20261006': 'conditional_flag_rank_source_freeze_20261006',
            'cohort_rank_calibration_release_20261006': 'conditional_flag_rank_release_20261006',
            'candidates/cohort_rank_calibration_20261006': 'candidates/conditional_flag_rank_20261006',
            'service_owned_workflows_20261006/cohort_rank_calibration_official_pilot': 'service_owned_workflows_20261006/conditional_flag_rank_official_comparison_v2',
            'cohort_rank_calibration_official_pilot_20261006/verification.json': 'conditional_flag_rank_official_comparison_v2_20261006/verification.json',
            "len(pilot['records']) == 17": "len(pilot['records']) == 37"}),
        'seal_cohort_candidate_source_package_20261006.py': ('seal_conditional_flag_candidate_source_package_20261006.py', {
            'cohort_rank_calibration_source_freeze_20261006': 'conditional_flag_rank_source_freeze_20261006',
            'cohort_rank_calibration_release_20261006': 'conditional_flag_rank_release_20261006',
            'candidates/cohort_rank_calibration_20261006': 'candidates/conditional_flag_rank_20261006',
            'service_owned_workflows_20261006/cohort_rank_calibration_candidate_inference': 'service_owned_workflows_20261006/conditional_flag_rank_candidate_inference',
            'passed_frozen_cohort_full_native_candidate_curve_codec_replay_and_cold80': 'passed_frozen_conditional_native14_full_candidate_independent_decoder_and_cold80',
            'freeze_and_infer_cohort_candidate_20261006.py': 'freeze_and_infer_conditional_flag_candidate_20261006.py',
            'cohort_rank_calibration_20261006.py': 'conditional_flag_rank_transform_20261006.py',
            'predict_cohort_calibrated_scheme_20261006.py': 'predict_conditional_flag_native_scheme_20261006.py',
            'seal_cohort_candidate_source_package_20261006.py': 'seal_conditional_flag_candidate_source_package_20261006.py',
            'replay_sealed_cohort_candidate_20261006.py': 'conditional_flag_rank_codec_20261006.py',
            'cohort_rank_calibration_official_pilot_20261006/verification.json': 'conditional_flag_rank_official_comparison_v2_20261006/verification.json',
            'cohort_rank_calibration_full_controls_20261006/verification.json': 'conditional_flag_rank_bank_v2_20261006/verification.json',
            "assert sha(CANDIDATE / 'cohort_curve.json') == before['future_curve_model_sha256']":
                "assert sha(CANDIDATE / 'conditional_common_curve.json') == before['future_common_curve_sha256']\n    assert sha(CANDIDATE / 'cohort_curve.json') == prediction['whole_scheme_graph']['cohort_rank_calibration']['future_curve_model']['sha256']\n    assert len(prediction['models']) == len(prediction['actual_model_reload_controls']) == len(prediction['actual80_day_prefix_model_controls']) == 14\n    assert read(CANDIDATE / 'conditional_native_replay_verification.json')['status'] == 'passed_actual14_saved_models_full_independent_conditional_decoder_and_cold80'",
            'selected_by_actual_full17_original_official_scores': 'selected_by_actual_full37_original_official_scores',
            'passed_sealed_actual_cohort_candidate': 'passed_sealed_actual_conditional_native14_candidate'}),
        'admit_extended_cohort_candidate_inference_20261006.py': ('admit_conditional_flag_candidate_inference_20261006.py', {
            'freeze_and_infer_extended_cohort_candidate_20261006.py': 'freeze_and_infer_conditional_flag_candidate_20261006.py',
            'extended_cohort_rank_calibration_release_20261006': 'conditional_flag_rank_release_20261006',
            'extended_cohort_rank_calibration_source_freeze_20261006': 'conditional_flag_rank_source_freeze_20261006',
            'extended_cohort_candidate_actual_admission_20261006.json': 'conditional_flag_candidate_actual_admission_20261006.json'})}
    pins, proofs = {}, []
    for old, (new, changes) in routes.items():
        source = A / old
        text = source.read_text(encoding='utf-8')
        for before in sorted(changes, key=len, reverse=True):
            assert before in text, (old, before)
            text = text.replace(before, changes[before])
        compile(text, str(A / new), 'exec')
        with (A / new).open('x', encoding='utf-8') as stream:
            stream.write(text)
        pins.update({str(source): sha(source), str(A / new): sha(A / new)})
        proofs.append({'original_source': old, 'effective_source': new, 'explicit_changes': changes})
    for name in ('predict_conditional_flag_native_scheme_20261006.py',
        'freeze_and_infer_conditional_flag_candidate_20261006.py'):
        compile((A / name).read_text(encoding='utf-8'), str(A / name), 'exec')
        pins[str(A / name)] = sha(A / name)
    create(A / 'conditional_flag_candidate_source_preparation_20261006.json', {
        'status': 'prepared_actual14_native_conditional_candidate_freeze_replay_and_seal',
        'input_sha256': pins, 'explicit_routes': proofs, 'new_native_training': False,
        'all_original_parent13_codec_curve_and_full_CSV_controls_preserved': True,
        'additional_saved_specialist_and_independent_tree_and_common_curve_controls_required': True,
        'test_labels_read': False})


if __name__ == '__main__':
    main()
