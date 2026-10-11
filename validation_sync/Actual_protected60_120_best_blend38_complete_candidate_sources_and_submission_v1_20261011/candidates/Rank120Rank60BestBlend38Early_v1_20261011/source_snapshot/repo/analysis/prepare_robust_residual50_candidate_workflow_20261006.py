"""Prepare the actual50-case winner replay with explicit native-bank provenance."""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path[:0] = [str(ROOT), str(A)]
from run_dependency_queue_v3_20261006 import create, sha, read


def main():
    old_stems = [
        'predict_longer_residual74_native_scheme_20261006',
        'freeze_and_infer_longer_residual74_candidate_20261006',
        'freeze_longer_residual74_candidate_sources_20261006',
        'seal_longer_residual74_candidate_source_package_20261006',
        'admit_longer_residual74_candidate_20261006',
        'wait_and_seal_longer_residual74_candidate_20261006',
        'launch_longer_residual74_candidate_workflow_20261006',
    ]
    names = {s + '.py': s.replace('longer_residual74', 'robust_residual50') + '.py' for s in old_stems}
    changes = {
        'conditional_residual128_256_comparison74_20261006': 'robust_conditional_residual_comparison50_v2_20261006',
        'conditional_residual128_256_comparison74': 'robust_conditional_residual_comparison50_v2',
        'conditional_residual128_256_scores74_evidence_publication': 'robust_conditional_residual_scores50_evidence_publication_v2',
        'passed_actual74_matched128_256_residual_and_ensemble_full_official_comparisons':
            'passed_actual50_matched_L1_Huber_residual_and_ensemble_full_official_comparisons',
        'longer_residual74': 'robust_residual50',
        'qualified102_anchor_score': 'selected74_anchor_score',
        'score_gain_over_qualified102_anchor': 'score_gain_over_selected74_anchor',
        'actual40_matched_native_and_independent_tree_controls': 'actual40_reference_native_and_independent_tree_controls',
        'expected_scored_records=74': 'expected_scored_records=50',
        "'scored_records': 74": "'scored_records': 50",
        '== 74': '== 50', 'all74': 'all50', 'full74': 'full50', 'actual74': 'actual50',
        'selected74-case': 'selected50-case', 'Actual74-case': 'Actual50-case',
        'owned74_candidate': 'owned50_candidate',
    }
    generated, pins, routes = {}, {}, []
    for old, new in names.items():
        original = (A / old).read_text(encoding='utf-8')
        text, effective = original, {}
        for before in sorted(changes, key=len, reverse=True):
            if before in text:
                text = text.replace(before, changes[before])
                effective[before] = changes[before]
        if old.startswith('predict_'):
            before = 'from conditional_flag_rank_codec_20261006 import '
            assert text.count(before) == 1
            text = text.replace(before, 'from conditional_identity_regression_tree_codec_20261006 import ')
            restored = text.replace('from conditional_identity_regression_tree_codec_20261006 import ', before)
            for before in sorted(effective, key=len, reverse=True):
                restored = restored.replace(effective[before], before)
            assert restored == original, 'Full/cold/native prediction arithmetic must remain byte-identical'
        if old.startswith('freeze_and_infer_'):
            before = "    assert names and all(n.endswith(('_e64', '_e128', '_e256')) for n in names)\n    component_banks = {n: reference if n.endswith('_e64') else bank for n in names}"
            assert text.count(before) == 1
            text = text.replace(before,
                "    robust = A / 'robust_conditional_residual_bank20_v2_20261006'\n"
                "    def component_bank(name):\n"
                "        if name.startswith('robust_residual_'):\n"
                "            assert name.endswith('_e128')\n"
                "            return robust\n"
                "        assert name.startswith('flag_residual_') and name.endswith(('_e64', '_e128', '_e256'))\n"
                "        return reference if name.endswith('_e64') else bank\n"
                "    assert names\n"
                "    component_banks = {n: component_bank(n) for n in names}")
            before = "    for path in [bank / 'verification.json', reference / 'verification.json',"
            assert text.count(before) == 1
            text = text.replace(before,
                "    for path in [bank / 'verification.json', reference / 'verification.json',\n"
                "        robust / 'verification.json', A / 'robust_conditional_residual_codec_recovery_preflight_20261006.json',")
            before = "'actual40_reference_native_and_independent_tree_controls': str(bank / 'verification.json'),"
            assert text.count(before) == 1
            text = text.replace(before, before +
                "\n            'actual20_matched_L1_Huber_native_and_independent_tree_controls': str(robust / 'verification.json'),\n"
                "            'actual19_fresh_native_fits_and1_preserved_reused_fit': read(robust / 'verification.json'),")
        if old.startswith('seal_'):
            text = text.replace("'conditional_flag_rank_codec_20261006.py'):",
                "'conditional_flag_rank_codec_20261006.py', 'conditional_identity_regression_tree_codec_20261006.py'):")
            before = "A / 'conditional_residual128_256_bank40_20261006/verification.json',"
            assert text.count(before) == 1
            text = text.replace(before, before +
                "\n                A / 'robust_conditional_residual_bank20_v2_20261006/verification.json',\n"
                "                A / 'robust_conditional_residual_codec_recovery_preflight_20261006.json',")
        if old.startswith('launch_'):
            text = text.replace("'official_selection_still_pending_all50_cases': True,",
                "'official_selection_complete_all50_cases': True,")
        compile(text, str(A / new), 'exec')
        generated[new] = text
        pins[str(A / old)] = sha(A / old)
        routes.append({'source': old, 'target': new, 'explicit_route_replacements': effective})
    pilot = read(A / 'robust_conditional_residual_comparison50_v2_20261006/verification.json')
    assert pilot['status'] == changes['passed_actual74_matched128_256_residual_and_ensemble_full_official_comparisons']
    assert len(pilot['records']) == 50
    assert min(pilot['records'], key=lambda r: (-r['connected_final_score'], r['configuration']['weight'], r['case'])) == pilot['best']
    assert pilot['best']['connected_final_score'] >= pilot['records'][1]['connected_final_score']
    evidence = [Path(__file__), A / 'conditional_identity_regression_tree_codec_20261006.py',
        A / 'run_robust_conditional_residual_comparison50_v2_20261006.py',
        A / 'train_robust_conditional_residual_bank20_v2_20261006.py',
        A / 'conditional_flag_residual_extrapolation_transform_20261006.py',
        A / 'robust_conditional_residual_bank20_v2_20261006/verification.json',
        A / 'robust_conditional_residual_codec_recovery_preflight_20261006.json',
        A / 'robust_conditional_residual_comparison50_v2_20261006/verification.json',
        A / 'robust_conditional_residual_scores_github_v2_20261006/receipt.json',
        A / 'conditional_residual128_256_bank40_20261006/verification.json',
        A / 'conditional_flag_residual_bank_20261006/verification.json']
    pins.update({str(p): sha(p) for p in evidence})
    for new in generated:
        assert not (A / new).exists(), new
    for new, text in generated.items():
        with (A / new).open('x', encoding='utf-8') as stream:
            stream.write(text)
        pins[str(A / new)] = sha(A / new)
    create(A / 'robust_residual50_candidate_workflow_preparation_20261006.json', {
        'status': 'prepared_actual50_selected_saved_native_full_cold_and_independent_replay',
        'input_sha256': pins, 'routes': routes,
        'actual_all50_original_official_scores_complete': True,
        'actual_selected_configuration': pilot['best']['configuration'],
        'actual_selected_validation_score': pilot['best']['connected_final_score'],
        'reference74_and_old64_components_route_to_their_actual_saved_native_banks': True,
        'new_L1_Huber_components_route_to_actual20_matched_native_bank': True,
        'identity_output_codec_preserves_original_tree_arithmetic': True,
        'actual_saved_native_count_is_13_plus_selected_component_count': True,
        'all_original_full1599600_twice_cold372000_tree_codec_curve_and_CSV_controls_preserved': True,
        'source_package_complete_all_local_Python_freeze_before_inference': True,
        'full_ranking_registration_and_main_candidate_publication_still_required': True,
        'new_native_fits_by_preparation': 0, 'new_quality_scores_by_preparation': 0,
        'test_labels_read': False,
    })


if __name__ == '__main__':
    main()
