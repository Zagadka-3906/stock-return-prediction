"""Prepare an unchanged native replay with explicit old64/new128/256 bank routing."""
from pathlib import Path
import ast
import sys

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path[:0] = [str(ROOT), str(A)]
from run_dependency_queue_v3_20261006 import create, sha


def main():
    names = {
        'predict_residual_extrapolation43_native_scheme_20261006.py': 'predict_longer_residual74_native_scheme_20261006.py',
        'freeze_and_infer_residual_extrapolation43_candidate_20261006.py': 'freeze_and_infer_longer_residual74_candidate_20261006.py',
        'freeze_residual_extrapolation43_candidate_sources_20261006.py': 'freeze_longer_residual74_candidate_sources_20261006.py',
        'seal_residual_extrapolation43_candidate_source_package_20261006.py': 'seal_longer_residual74_candidate_source_package_20261006.py',
        'admit_residual_extrapolation43_candidate_20261006.py': 'admit_longer_residual74_candidate_20261006.py',
        'wait_and_seal_residual_extrapolation43_candidate_20261006.py': 'wait_and_seal_longer_residual74_candidate_20261006.py',
    }
    changes = {
        **{old.removesuffix('.py'): new.removesuffix('.py') for old, new in names.items()},
        'conditional_residual_extrapolation43_official_20261006': 'conditional_residual128_256_comparison74_20261006',
        'conditional_residual_extrapolation43_official_comparison': 'conditional_residual128_256_comparison74',
        'conditional_residual_extrapolation43_evidence_publication': 'conditional_residual128_256_scores74_evidence_publication',
        'residual_extrapolation43_source_freeze_20261006': 'longer_residual74_source_freeze_20261006',
        'residual_extrapolation43_release_20261006': 'longer_residual74_release_20261006',
        'residual_extrapolation43_20261006': 'longer_residual74_20261006',
        'residual_extrapolation43_candidate_inference': 'longer_residual74_candidate_inference',
        'residual_extrapolation43_candidate_sealing': 'longer_residual74_candidate_sealing',
        'residual_extrapolation43_candidate_admission_20261006': 'longer_residual74_candidate_admission_20261006',
        'residual_extrapolation43_workflow_preparation_20261006.json': 'longer_residual74_candidate_workflow_preparation_20261006.json',
        'passed_actual43_conditional_residual_extrapolation_full_official_comparisons':
            'passed_actual74_matched128_256_residual_and_ensemble_full_official_comparisons',
        'score_gain_over_parent102': 'score_gain_over_parent100',
        "'explicit_parent_round': 102": "'explicit_parent_round': 100",
        'explicit_parent_round=102': 'explicit_parent_round=100',
        'expected_scored_records=43': 'expected_scored_records=74',
        "'scored_records': 43": "'scored_records': 74",
        '== 43': '== 74', 'all43': 'all74', 'full43': 'full74', 'actual43': 'actual74',
        'selected43-case': 'selected74-case', 'actual43-case': 'actual74-case',
        'actual20_native_and_independent_tree_controls': 'actual40_matched_native_and_independent_tree_controls',
    }
    generated, pins, routes = {}, {}, []
    for old, new in names.items():
        original = (A / old).read_text(encoding='utf-8')
        text, effective = original, {}
        for before in sorted(changes, key=len, reverse=True):
            if before in text:
                text = text.replace(before, changes[before])
                effective[before] = changes[before]
        if old.startswith('freeze_and_infer_'):
            before = "    bank = A / 'conditional_flag_residual_bank_20261006'\n    names = pilot['ensembles'].get(cfg['model'], [cfg['model']])\n    infos = [read(bank / name / 'info_2025.json') for name in names]"
            assert text.count(before) == 1
            text = text.replace(before,
                "    bank = A / 'conditional_residual128_256_bank40_20261006'\n"
                "    reference = A / 'conditional_flag_residual_bank_20261006'\n"
                "    names = pilot['ensembles'].get(cfg['model'], [cfg['model']])\n"
                "    assert names and all(n.endswith(('_e64', '_e128', '_e256')) for n in names)\n"
                "    component_banks = {n: reference if n.endswith('_e64') else bank for n in names}\n"
                "    infos = [read(component_banks[n] / n / 'info_2025.json') for n in names]\n"
                "    assert [i['name'] for i in infos] == names\n"
                "    for n, i in zip(names, infos):\n"
                "        assert Path(i['native_model_path']).resolve().parent == (component_banks[n] / n).resolve()\n")
            before = "        else pilot_folder / f'{cfg[\"model\"]}.npy')"
            assert text.count(before) == 1
            text = text.replace("(bank / cfg['model'] / 'flagged_oof_predictions.npy'",
                                "(component_banks[cfg['model']] / cfg['model'] / 'flagged_oof_predictions.npy'")
            before = "    pins[str(predictor_source)] = sha(predictor_source)"
            assert text.count(before) == 1
            text = text.replace(before, before +
                "\n    for path in [bank / 'verification.json', reference / 'verification.json',\n"
                "        *[component_banks[n] / n / 'info_2025.json' for n in names]]:\n"
                "        pins[str(path)] = sha(path)\n"
                "    assert best['connected_final_score'] >= pilot['records'][1]['connected_final_score']\n")
            before = "'baseline_score': pilot['records'][0]['connected_final_score'], 'score_gain': best['score_gain_over_parent100'],"
            assert text.count(before) == 1
            text = text.replace(before, before +
                "\n            'qualified102_anchor_score': pilot['records'][1]['connected_final_score'],\n"
                "            'score_gain_over_qualified102_anchor': best['connected_final_score'] - pilot['records'][1]['connected_final_score'],\n"
                "            'selected_component_bank_paths': {n: str(component_banks[n]) for n in names},")
            before = "'actual40_matched_native_and_independent_tree_controls': str(bank / 'verification.json'),"
            assert text.count(before) == 1
            text = text.replace(before, before +
                "\n            'actual_original64_reference_native_and_independent_controls': str(reference / 'verification.json'),")
        if old.startswith('seal_'):
            before = "A / 'conditional_flag_residual_bank_20261006/verification.json',"
            assert text.count(before) == 1
            text = text.replace(before, before +
                "\n                A / 'conditional_residual128_256_bank40_20261006/verification.json',")
        if old.startswith('predict_'):
            restored = text
            for before in sorted(effective, key=len, reverse=True):
                restored = restored.replace(effective[before], before)
            assert restored == original, 'The native full/cold/independent prediction arithmetic must be unchanged'
        compile(text, str(A / new), 'exec')
        generated[new] = text
        pins[str(A / old)] = sha(A / old)
        routes.append({'source': old, 'target': new, 'explicit_route_replacements': effective})
    driver = ast.parse(generated['freeze_and_infer_longer_residual74_candidate_20261006.py'])
    assert "expected_scored_records=74" in generated['freeze_and_infer_longer_residual74_candidate_20261006.py']
    assert "explicit_parent_round=100" in generated['freeze_and_infer_longer_residual74_candidate_20261006.py']
    assert "component_banks[n]" in generated['freeze_and_infer_longer_residual74_candidate_20261006.py']
    for name in generated:
        assert not (A / name).exists(), name
    evidence = [A / 'run_conditional_residual128_256_comparison74_20261006.py',
        A / 'train_conditional_residual128_256_bank40_20261006.py',
        A / 'conditional_flag_residual_extrapolation_transform_20261006.py',
        A / 'conditional_residual128_256_bank40_20261006/verification.json',
        A / 'conditional_flag_residual_bank_20261006/verification.json', Path(__file__)]
    pins.update({str(p): sha(p) for p in evidence})
    for new, text in generated.items():
        with (A / new).open('x', encoding='utf-8') as stream:
            stream.write(text)
        pins[str(A / new)] = sha(A / new)
    create(A / 'longer_residual74_candidate_workflow_preparation_20261006.json', {
        'status': 'prepared_actual74_selected_saved_native_full_cold_and_independent_replay',
        'input_sha256': pins, 'routes': routes,
        'actual_final_selection_pending_all74_original_official_scores': True,
        'qualified102_original64_anchor_uses_original_saved_bank': True,
        'new128_256_components_use_real40_native_fit_bank': True,
        'actual_saved_native_count_is_13_plus_selected_component_count': True,
        'native_prediction_arithmetic_reverse_route_replacements_byte_identical': True,
        'all_original_full1599600_twice_cold372000_tree_codec_curve_and_CSV_controls_preserved': True,
        'source_package_complete_all_local_Python_freeze_before_inference': True,
        'full_ranking_registration_and_main_candidate_publication_still_required': True,
        'new_native_fits_by_preparation': 0, 'new_quality_scores_by_preparation': 0,
        'test_labels_read': False,
    })


if __name__ == '__main__':
    main()
