"""Prepare complete source-freeze and sealing for the49-case residual winner."""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path.insert(0, str(A))
from run_dependency_queue_v3_20261006 import create, sha


def main():
    common = {
        'conditional_flag_rank_source_freeze_20261006': 'conditional_residual_source_freeze_20261006',
        'conditional_flag_rank_release_20261006': 'conditional_residual_release_20261006',
        'candidates/conditional_flag_rank_20261006': 'candidates/conditional_residual_20261006'}
    routes = [
        ('freeze_conditional_flag_candidate_sources_20261006.py', 'freeze_conditional_residual_candidate_sources_20261006.py', {
            **common,
            'service_owned_workflows_20261006/conditional_flag_rank_official_comparison_v2': 'service_owned_workflows_20261006/conditional_flag_residual_official_comparison',
            'conditional_flag_rank_official_comparison_v2_20261006/verification.json': 'conditional_flag_residual_official_comparison_20261006/verification.json',
            "len(pilot['records']) == 37": "len(pilot['records']) == 49"}),
        ('seal_conditional_flag_candidate_source_package_20261006.py', 'seal_conditional_residual_candidate_source_package_20261006.py', {
            **common,
            'service_owned_workflows_20261006/conditional_flag_rank_candidate_inference': 'service_owned_workflows_20261006/conditional_residual_candidate_inference',
            'passed_frozen_conditional_native14_full_candidate_independent_decoder_and_cold80': 'passed_frozen_conditional_residual_full_saved_model_candidate_and_independent_decoder_and_cold80',
            'freeze_and_infer_conditional_flag_candidate_20261006.py': 'freeze_and_infer_conditional_residual_candidate_20261006.py',
            'conditional_flag_rank_transform_20261006.py': 'conditional_flag_residual_transform_20261006.py',
            'predict_conditional_flag_native_scheme_20261006.py': 'predict_conditional_residual_native_scheme_20261006.py',
            'seal_conditional_flag_candidate_source_package_20261006.py': 'seal_conditional_residual_candidate_source_package_20261006.py',
            'conditional_flag_rank_official_comparison_v2_20261006/verification.json': 'conditional_flag_residual_official_comparison_20261006/verification.json',
            'conditional_flag_rank_bank_v2_20261006/verification.json': 'conditional_flag_residual_bank_20261006/verification.json',
            "assert sha(CANDIDATE / 'conditional_common_curve.json') == before['future_common_curve_sha256']":
                "assert sha(CANDIDATE / 'cohort_curve.json') == before['parent_curve_sha256']",
            "== len(prediction['actual80_day_prefix_model_controls']) == 14":
                "== len(prediction['actual80_day_prefix_model_controls']) == 13 + len(selection['native_component_names'])",
            'conditional_native_replay_verification.json': 'conditional_residual_native_replay_verification.json',
            'passed_actual14_saved_models_full_independent_conditional_decoder_and_cold80': 'passed_actual_saved_parent13_and_selected_residual_heads_full_independent_decoder_and_cold80',
            'selected_by_actual_full37_original_official_scores': 'selected_by_actual_full49_original_official_scores',
            'passed_sealed_actual_conditional_native14_candidate': 'passed_sealed_actual_conditional_residual_candidate'})]
    pins, proofs = {}, []
    for old, new, changes in routes:
        text = (A / old).read_text(encoding='utf-8')
        for before in sorted(changes, key=len, reverse=True):
            assert before in text, (old, before)
            text = text.replace(before, changes[before])
        compile(text, str(A / new), 'exec')
        with (A / new).open('x', encoding='utf-8') as stream:
            stream.write(text)
        pins.update({str(A / old): sha(A / old), str(A / new): sha(A / new)})
        proofs.append({'original_source': old, 'effective_source': new, 'explicit_routes': changes})
    for name in ('predict_conditional_residual_native_scheme_20261006.py',
        'freeze_and_infer_conditional_residual_candidate_20261006.py',
        'admit_conditional_residual_candidate_inference_20261006.py',
        'wait_and_seal_conditional_residual_candidate_20261006.py'):
        compile((A / name).read_text(encoding='utf-8'), str(A / name), 'exec')
        pins[str(A / name)] = sha(A / name)
    create(A / 'conditional_residual_candidate_source_preparation_20261006.json', {
        'status': 'prepared_complete49_case_residual_saved_model_candidate_freeze_and_seal',
        'input_sha256': pins, 'routes': proofs, 'new_native_fits': 0,
        'actual_native_component_count_follows_frozen_selected_scheme': True,
        'all_original_parent13_curve_and_full_CSV_controls_preserved': True, 'test_labels_read': False})


if __name__ == '__main__':
    main()
