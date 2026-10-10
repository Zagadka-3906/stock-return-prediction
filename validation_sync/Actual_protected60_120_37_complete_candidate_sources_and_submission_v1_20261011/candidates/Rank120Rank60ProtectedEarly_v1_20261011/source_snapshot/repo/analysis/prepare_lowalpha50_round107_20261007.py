"""Register the complete low-alpha search, with explicit reuse of an unchanged candidate."""
from pathlib import Path
import ast
import hashlib
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path[:0] = [str(ROOT), str(A)]
from run_dependency_queue_v3_20261006 import read, create, sha

NAMES = {
    'register_simplex_residual47_round106_artifacts_20261006.py': 'register_lowalpha50_round107_artifacts_20261007.py',
    'optimize_training_round106.py': 'optimize_training_round107.py',
    'finalize_training_round106.py': 'finalize_training_round107.py',
    'publish_simplex_residual47_round106_full_validation_20261006.py': 'publish_lowalpha50_round107_full_validation_20261007.py',
    'build_lossless_ranking_display_v15_20261006.py': 'build_lossless_ranking_display_round107_20261007.py',
    'verify_lossless_ranking_display_v17_20261006.py': 'verify_lossless_ranking_display_round107_20261007.py',
    'lossless_ranking_runtime_adapter_v14_20261006.py': 'lossless_ranking_runtime_adapter_round107_20261007.py',
}


def confirm_candidate():
    import numpy as np
    candidate = ROOT / 'candidates/simplex_residual47_20261006'
    release = A / 'simplex_residual47_release_20261006'
    pilot = read(A / 'lowalpha_huber_residual_comparison50_20261006/verification.json')
    assert pilot['status'] == 'passed_actual50_fixed_lowalpha_Huber_residual_and_ensemble_full_official_comparisons'
    assert len(pilot['records']) == 50 and pilot['best']['case'] == 1
    selection, actual, manifest = (read(candidate / f'{name}.json') for name in ('selection', 'verification', 'manifest'))
    assert pilot['best']['configuration'] == selection['chosen_postprocessor']
    assert pilot['best']['metrics'] == selection['winner']['metrics']
    assert pilot['best']['metrics'] == read(A / 'optimization_20261003_r106/calibrated_csv_official.json')['metrics']
    raw = np.load(release / 'selected_validation.npy', mmap_mode='r')
    assert raw.shape == (5635800,)
    numeric = hashlib.sha256(memoryview(np.ascontiguousarray(raw)).cast('B')).hexdigest()
    assert numeric == pilot['best']['prediction_numeric_bytes_sha256']
    assert actual['whole_scheme_graph'] == selection['winner']['conditional_flag_residual_scheme_graph']
    assert actual['status'] == 'passed' and actual['rows'] == 1599600 and actual['days'] == 344 and actual['codes'] == 4650
    for key in ('model_reload_bit_identical', 'pipeline_replay_bit_identical',
                'csv_replay_byte_identical', 'csv_ranks_unchanged', 'cold80_day_prefix_bit_identical'):
        assert actual[key], key
    assert sha(candidate / 'submission.csv') == actual['csv_sha256']
    for relative, item in manifest['files'].items():
        assert sha(candidate / relative) == item['sha256'], relative
    assert sha(candidate / 'manifest.json') == read(release / 'source_package_verification.json')['manifest_sha256']
    proof = {'status': 'passed_actual50_selected_scheme_full_validation_bits_all_metrics_graph_and_all_sealed_candidate_files_unchanged',
        'at_local': time.strftime('%Y-%m-%dT%H:%M:%S'), 'actual_selected_full_validation_rows': len(raw),
        'selected_numeric_sha256': numeric, 'all8_original_official_metrics_exact': True,
        'chosen_postprocessor': pilot['best']['configuration'], 'original_case1_source': str(A / 'lowalpha_huber_residual_comparison50_20261006/case01_official.json'),
        'actual_candidate_source': str(candidate), 'actual_candidate_files_rehashed': len(manifest['files']),
        'source_manifest_sha256': sha(candidate / 'manifest.json'), 'actual_submission_sha256': actual['csv_sha256'],
        'original_pre_inference_freeze_time': selection['frozen_at_local'], 'actual_native_models': len(actual['models']),
        'previously_completed_full_model_reload_pipeline_csv_and_cold80_proofs_preserved': True,
        'new_inference_or_training_claimed_by_reuse': False, 'actual_new_native_fits_by_this_confirmation': 0,
        'test_labels_read': False}
    create(A / 'lowalpha50_selected_candidate_reuse_confirmation_20261007.json', proof)
    return proof


def main():
    targets = [A / name for name in NAMES.values()]
    targets += [A / 'lowalpha50_round107_preparation_20261007.json',
                A / 'lowalpha50_selected_candidate_reuse_confirmation_20261007.json']
    for p in targets:
        assert not p.exists(), p
    assert (A / 'run_lowalpha50_round107_full_registration_20261007.py').exists()
    confirm_candidate()
    generated, routes = {}, []
    common = {**{k.removesuffix('.py'): v.removesuffix('.py') for k, v in NAMES.items()},
        'round106': 'round107', '_r106': '_r107', 'NUMBER = 106': 'NUMBER = 107',
        'WAVES = (389,)': 'WAVES = (390,)', 'wave=389': 'wave=390',
        'wave389_results': 'wave390_results', "'waves': [389]": "'waves': [390]",
        'residual_simplex47_official_comparison_20261006': 'lowalpha_huber_residual_comparison50_20261006',
        'passed_actual47_convex_simplex_residual_ensemble_full_official_comparisons':
            'passed_actual50_fixed_lowalpha_Huber_residual_and_ensemble_full_official_comparisons',
        '== 47': '== 50', "'expected_scored_records': 47": "'expected_scored_records': 50",
        "'existing_actual_official_records': 47": "'existing_actual_official_records': 50",
        "'scored_records': 47": "'scored_records': 50", "'original_official_pilot_records_registered': 47": "'original_official_pilot_records_registered': 50",
        'all47': 'all50', 'actual47': 'actual50', 'Register47': 'Register50',
        'the47': 'the50', 'official47': 'official50', '第106轮': '第107轮', '既有47项': '既有50项',
        'lossless_ranking_display_qa_v17_20261006': 'lossless_ranking_display_qa_v18_20261007',
        'ranking_display_qa_v17_20261006': 'ranking_display_qa_v18_20261007',
        'collect(106, 17, 47)': 'collect(107, 18, 50)',
        "namespace['snapshot'](106)": "namespace['snapshot'](107)",
        'assert number == 106': 'assert number == 107',
        'actual_complete_QA_version=17': 'actual_complete_QA_version=18',
        "'actual_full_QA_version': 17": "'actual_full_QA_version': 18",
    }
    for source_name, target_name in NAMES.items():
        original = (A / source_name).read_text(encoding='utf-8')
        text, effective = original, {}
        for before in sorted(common, key=len, reverse=True):
            if before in text:
                text = text.replace(before, common[before]); effective[before] = common[before]
        if source_name.startswith('register_'):
            start = text.index('    sources = [')
            end = text.index('    pins = ', start)
            text = text[:start] + """    sources = [Path(__file__), A / 'optimize_training_round107.py', A / 'finalize_training_round107.py',
        A / 'run_lowalpha50_round107_full_registration_20261007.py',
        A / 'publish_lowalpha50_round107_full_validation_20261007.py',
        A / 'prepare_lowalpha50_round107_20261007.py',
        A / 'lowalpha50_round107_preparation_20261007.json',
        A / 'lowalpha50_selected_candidate_reuse_confirmation_20261007.json',
        A / 'lossless_ranking_runtime_adapter_round107_20261007.py',
        A / 'build_lossless_ranking_display_round107_20261007.py',
        A / 'verify_lossless_ranking_display_round107_20261007.py',
        A / 'publish_explicit_parent_training_round_v2_20261005.py']
""" + text[end:]
            text = text.replace("pins = {**read(RELEASE / 'protocol.json')['input_sha256'],",
                "pins = {**read(RELEASE / 'protocol.json')['input_sha256'], **pilot['input_sha256'],")
            text = text.replace("selection.update(winner=winner, ranking=records,",
                "selection.update(winner=winner, ranking=records, baseline_score=winner['connected_final_score'], score_gain=0.,\n"
                "        explicit_comparison_parent_round=106, preserved_scheme_training_parent_round=100,")
            text = text.replace("'explicit_parent_round': 100", "'explicit_parent_round': 106")
            text = text.replace("'existing_actual_native_bank_fits': 40,", "'existing_actual_native_bank_fits': 60, 'actual_lowalpha_bank_fits': 20, 'existing_L2_reference_bank_fits': 40,")
            text = text.replace("'actual_ordered_integer_convex_weights': pilot['ensemble_integer_weights'],",
                "'actual_declared_model_ensembles': pilot['ensembles'],\n"
                "        'actual20_lowalpha_native_bank_source': str(A / 'lowalpha_huber_residual_bank20_20261006/verification.json'),\n"
                "        'actual_selected_candidate_reuse_confirmation': str(A / 'lowalpha50_selected_candidate_reuse_confirmation_20261007.json'),")
            text = text.replace("'actual_all_annual_mature_native_and_independent_codec_and_prefix_controls': str(A / 'conditional_residual128_256_bank40_20261006/verification.json'),",
                "'actual_all_annual_mature_native_and_independent_codec_and_prefix_controls': str(A / 'lowalpha_huber_residual_bank20_20261006/verification.json'),\n"
                "        'selected_reference40_native_and_codec_controls': str(A / 'conditional_residual128_256_bank40_20261006/verification.json'),")
        if source_name == 'optimize_training_round106.py':
            text = text.replace('PREVIOUS_NUMBER = 100', 'PREVIOUS_NUMBER = 106')
            text = text.replace("PREVIOUS = ROOT / 'analysis/optimization_20261003_r100'", "PREVIOUS = ROOT / 'analysis/optimization_20261003_r106'")
            text = text.replace("'training_parent_round': PREVIOUS_NUMBER", "'training_parent_round': 100, 'comparison_baseline_round': PREVIOUS_NUMBER")
        if source_name.startswith('publish_'):
            # All the old selected candidate evidence remains relevant. Append
            # every new native/control/score source; never substitute inference.
            anchor = '    for path in extra:'
            assert text.count(anchor) == 1
            text = text.replace(anchor, """    extra += [A / 'lowalpha50_selected_candidate_reuse_confirmation_20261007.json',
        A / 'lowalpha50_round107_preparation_20261007.json',
        A / 'prepare_lowalpha50_round107_20261007.py',
        A / 'run_lowalpha50_round107_full_registration_20261007.py',
        A / 'train_lowalpha_huber_residual_bank20_20261006.py',
        A / 'run_lowalpha_huber_residual_comparison50_v2_20261006.py',
        A / 'run_lowalpha_huber_residual_comparison50_20261006.py',
        A / 'publish_lowalpha_huber_residual50_scores_20261006.py',
        A / 'lowalpha_huber_residual_scores_github_20261006/receipt.json']
    extra += [p for p in (A / 'lowalpha_huber_residual_bank20_20261006').rglob('*.json') if not p.name.startswith('model_dump_')]
    for name in ('lowalpha_huber_residual_comparison50_v2', 'lowalpha_huber_residual_scores50_evidence_publication'):
        service = A / 'service_owned_workflows_20261006' / name
        extra += list(service.glob('*.json')) + list(service.glob('*.log'))
""" + anchor)
            text = text.replace('47项四分之一步长凸残差集成验证', '50项固定较低阈值Huber残差及集成验证')
            text = text.replace('原命名候选目录实际完成', '原命名候选目录实际完成，本次50项搜索的赢家经全验证数组及全部参数核对与该候选相同')
        if source_name.startswith(('build_lossless_', 'verify_lossless_', 'lossless_ranking_runtime_')):
            restored = text
            for before in sorted(effective, key=len, reverse=True):
                restored = restored.replace(effective[before], before)
            assert restored == original, 'Original complete QA logic must be unchanged'
        compile(text, str(A / target_name), 'exec')
        generated[target_name] = text
        routes.append({'source': source_name, 'target': target_name, 'source_sha256': sha(A / source_name),
                       'literal_identifier_routes': effective})
    publisher_tree = ast.parse(generated[NAMES['publish_simplex_residual47_round106_full_validation_20261006.py']])
    assert [[a.value for a in n.args] for n in ast.walk(publisher_tree) if isinstance(n, ast.Call)
        and isinstance(n.func, ast.Name) and n.func.id == 'collect'] == [[107, 18, 50]]
    pins = {str(A / old): sha(A / old) for old in NAMES}
    for name, text in generated.items():
        with (A / name).open('x', encoding='utf-8') as stream:
            stream.write(text)
        pins[str(A / name)] = sha(A / name)
    for p in (Path(__file__), A / 'run_lowalpha50_round107_full_registration_20261007.py',
              A / 'lowalpha50_selected_candidate_reuse_confirmation_20261007.json'):
        pins[str(p)] = sha(p)
    create(A / 'lowalpha50_round107_preparation_20261007.json', {
        'status': 'passed_actual_complete50_registry_source_preparation_and_exact_existing_candidate_confirmation',
        'at_local': time.strftime('%Y-%m-%dT%H:%M:%S'), 'input_sha256': pins, 'routes': routes,
        'scored_records': 50, 'wave': 390, 'comparison_parent_round': 106, 'original_scheme_training_parent_round': 100,
        'original_full_six_view_and45second_browser_QA_unchanged': True,
        'original_candidate_and_inference_freeze_preserved': True, 'new_inference_claimed': False,
        'actual_new_native_fits': 0, 'new_quality_score_records_by_preparation': 0, 'test_labels_read': False})


if __name__ == '__main__':
    main()
