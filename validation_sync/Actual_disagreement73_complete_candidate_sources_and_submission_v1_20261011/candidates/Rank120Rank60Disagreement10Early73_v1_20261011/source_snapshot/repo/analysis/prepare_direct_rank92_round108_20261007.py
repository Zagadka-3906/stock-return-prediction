"""Register92 actual direct-rank comparisons and preserve their unchanged selected candidate."""
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
    'register_lowalpha50_round107_artifacts_20261007.py': 'register_direct_rank92_round108_artifacts_20261007.py',
    'optimize_training_round107.py': 'optimize_training_round108.py',
    'finalize_training_round107.py': 'finalize_training_round108.py',
    'publish_lowalpha50_round107_full_validation_20261007.py': 'publish_direct_rank92_round108_full_validation_20261007.py',
    'build_lossless_ranking_display_round107_20261007.py': 'build_lossless_ranking_display_round108_20261007.py',
    'verify_lossless_ranking_display_round107_20261007.py': 'verify_lossless_ranking_display_round108_20261007.py',
    'lossless_ranking_runtime_adapter_round107_20261007.py': 'lossless_ranking_runtime_adapter_round108_20261007.py',
    'collect_full_lossless_round107_qa18_20261007.py': 'collect_full_lossless_round108_qa19_20261007.py',
}


def confirm():
    import numpy as np
    c = ROOT / 'candidates/simplex_residual47_20261006'
    release = A / 'simplex_residual47_release_20261006'
    pilot = read(A / 'direct_flag_rank92_official_comparison_20261007/verification.json')
    assert pilot['status'] == 'passed_actual92_direct_rank_CDF_full_official_comparisons'
    assert len(pilot['records']) == 92 and pilot['best']['case'] == 1
    assert pilot['best']['configuration'] == {'anchor_round': 106, 'model': None, 'weight': 0., 'universe': None}
    original, actual, manifest = (read(c / f'{n}.json') for n in ('selection', 'verification', 'manifest'))
    assert pilot['best']['metrics'] == original['winner']['metrics']
    assert pilot['best']['metrics'] == read(A / 'optimization_20261003_r107/calibrated_csv_official.json')['metrics']
    raw = np.load(release / 'selected_validation.npy', mmap_mode='r')
    baseline_raw = np.load(A / 'optimization_20261003_r106/selected_validation.npy', mmap_mode='r')
    assert raw.shape == baseline_raw.shape == (5635800,)
    assert np.array_equal(raw.view(np.uint64), baseline_raw.view(np.uint64))
    numeric = hashlib.sha256(memoryview(np.ascontiguousarray(raw)).cast('B')).hexdigest()
    assert numeric == pilot['best']['prediction_numeric_bytes_sha256']
    assert actual['whole_scheme_graph'] == original['winner']['conditional_flag_residual_scheme_graph']
    assert actual['status'] == 'passed' and (actual['rows'], actual['days'], actual['codes']) == (1599600, 344, 4650)
    for k in ('model_reload_bit_identical', 'pipeline_replay_bit_identical', 'csv_replay_byte_identical', 'csv_ranks_unchanged', 'cold80_day_prefix_bit_identical'):
        assert actual[k], k
    assert sha(c / 'submission.csv') == actual['csv_sha256']
    for relative, item in manifest['files'].items():
        assert sha(c / relative) == item['sha256'], relative
    assert sha(c / 'manifest.json') == read(release / 'source_package_verification.json')['manifest_sha256']
    create(A / 'direct_rank92_selected_candidate_reuse_confirmation_20261007.json', {
        'status': 'passed_actual92_selected_scheme_full_validation_bits_all_metrics_graph_and_all_sealed_candidate_files_unchanged',
        'at_local': time.strftime('%Y-%m-%dT%H:%M:%S'), 'actual_selected_full_validation_rows': len(raw),
        'selected_numeric_sha256': numeric, 'all8_original_official_metrics_exact': True,
        'chosen_postprocessor': original['chosen_postprocessor'], 'actual_selected_anchor_configuration': pilot['best']['configuration'],
        'original_case1_source': str(A / 'direct_flag_rank92_official_comparison_20261007/case01_official.json'),
        'actual_candidate_source': str(c), 'actual_candidate_files_rehashed': len(manifest['files']),
        'source_manifest_sha256': sha(c / 'manifest.json'), 'actual_submission_sha256': actual['csv_sha256'],
        'original_pre_inference_freeze_time': original['frozen_at_local'], 'actual_native_models': len(actual['models']),
        'previously_completed_full_model_reload_pipeline_csv_and_cold80_proofs_preserved': True,
        'new_inference_or_training_claimed_by_reuse': False, 'actual_new_native_fits_by_this_confirmation': 0, 'test_labels_read': False})


def main():
    for p in [*(A / n for n in NAMES.values()), A / 'direct_rank92_round108_preparation_20261007.json', A / 'direct_rank92_selected_candidate_reuse_confirmation_20261007.json']:
        assert not p.exists(), p
    assert read(A / 'optimization_20261003_r107/full_registration_execution.json')['status'] == 'passed'
    assert read(A / 'github_validation_sync_main_20261005/round107_receipt.json')['actual_full_QA_version'] == 18
    assert read(A / 'single_host_rank36_scores_github_20261007/receipt.json')['scored_records'] == 92
    confirm()
    common = {**{k.removesuffix('.py'): v.removesuffix('.py') for k, v in NAMES.items()},
        'run_lowalpha50_round107_full_registration_20261007': 'run_direct_rank92_round108_full_registration_20261007',
        'prepare_lowalpha50_round107_20261007': 'prepare_direct_rank92_round108_20261007',
        'lowalpha50_round107_preparation_20261007': 'direct_rank92_round108_preparation_20261007',
        'lowalpha50_selected_candidate_reuse_confirmation_20261007': 'direct_rank92_selected_candidate_reuse_confirmation_20261007',
        'round107': 'round108', '_r107': '_r108', 'NUMBER = 107': 'NUMBER = 108',
        'WAVES = (390,)': 'WAVES = (391,)', 'wave=390': 'wave=391', 'wave390_results': 'wave391_results', "'waves': [390]": "'waves': [391]",
        'lowalpha_huber_residual_comparison50_20261006': 'direct_flag_rank92_official_comparison_20261007',
        'passed_actual50_fixed_lowalpha_Huber_residual_and_ensemble_full_official_comparisons': 'passed_actual92_direct_rank_CDF_full_official_comparisons',
        '== 50': '== 92', "'expected_scored_records': 50": "'expected_scored_records': 92", "'existing_actual_official_records': 50": "'existing_actual_official_records': 92",
        "'scored_records': 50": "'scored_records': 92", "'original_official_pilot_records_registered': 50": "'original_official_pilot_records_registered': 92",
        'all50': 'all92', 'actual50': 'actual92', 'Register50': 'Register92', 'the50': 'the92', 'official50': 'official92',
        '第107轮': '第108轮', '既有50项': '既有92项',
        'lossless_ranking_display_qa_v18_20261007': 'lossless_ranking_display_qa_v19_20261007',
        'ranking_display_qa_v18_20261007': 'ranking_display_qa_v19_20261007',
        'collect(107, 18, 50)': 'collect(108, 19, 92)', '(107, 18, 50)': '(108, 19, 92)',
        "namespace['snapshot'](107)": "namespace['snapshot'](108)", 'assert number == 107': 'assert number == 108',
        'actual_complete_QA_version=18': 'actual_complete_QA_version=19', "'actual_full_QA_version': 18": "'actual_full_QA_version': 19",
    }
    generated, routes = {}, []
    for old, new in NAMES.items():
        original = (A / old).read_text(encoding='utf-8')
        text, effective = original, {}
        for before in sorted(common, key=len, reverse=True):
            if before in text:
                text = text.replace(before, common[before]); effective[before] = common[before]
        if old.startswith('register_'):
            text = text.replace("A / 'publish_explicit_parent_training_round_v2_20261005.py']", "A / 'publish_explicit_parent_training_round_v2_20261005.py',\n        A / 'collect_full_lossless_round108_qa19_20261007.py',\n        A / 'github_validation_sync_main_20261005/round107_receipt.json',\n        A / 'single_host_rank36_scores_github_20261007/receipt.json']")
            start = text.index('        assert measured[')
            end = text.index('        capsule = ', start)
            text = text[:start] + """        cfg = measured['configuration']
        if cfg['model'] is None:
            assert measured['qualified_anchor_all_metrics_exact']
            assert measured['metrics'] == read(A / f"optimization_20261003_r{cfg['anchor_round']}/calibrated_csv_official.json")['metrics']
        else:
            assert measured['all1212_nonflag_raw_bits_exact_implies_same_orders_and_ties']
            assert measured['actual_cold80_260_975_bits_exact']
""" + text[end:]
            start = text.index('        if measured[\'case\'] != pilot[')
            end = text.index('        row = ', start)
            text = text[:start] + """        if cfg['model'] is None and cfg['anchor_round'] == 100:
            graph = deepcopy(read(A / 'optimization_20261003_r100/selection.json')['winner']['extended_cohort_rank_calibration_scheme_graph'])
        elif cfg['model'] is not None:
            graph['conditional_flag_direct_centered_rank_CDF'] = {**cfg,
                'actual_annual_native_bank': measured['native_bank_source'],
                'ensemble_components': measured['ensemble_components'],
                'ordered_equal_mean_arithmetic': True, 'direct_model_quantile': 'centered_pred_plus_0.5',
                'current_day_CDF_pool': cfg['universe'], 'current_price_valid_uses_t_features_only': True,
                'outside_pool_CDF': 'insertion_index/N', 'inverse_knots': '1/N..1',
                'only_flag1_modified_nonflag_raw_bits_exact': True, 'first2020_actual_mature_direct_model': True,
                'future_candidate_not_inferred_for_nonselected_comparison': True,
                'position': 'after_complete_qualified_parent106_graph_including_saved_cohort_curve_and_residual'}
""" + text[end:]
            text = text.replace("actual_full_conditional_residual_control=deepcopy(measured)", "actual_full_conditional_residual_control=deepcopy(measured), direct_rank_comparison_configuration=deepcopy(cfg), original_comparison_case=measured['case']")
            text = text.replace("records.sort(key=lambda r: (-r['connected_final_score'], r[GRAPH_FIELD]['conditional_flag_residual']['weight'], r['arm']))", "records.sort(key=lambda r: (-r['connected_final_score'], r['direct_rank_comparison_configuration']['weight'], r['original_comparison_case']))")
            text = text.replace('explicit_comparison_parent_round=106', 'explicit_comparison_parent_round=107')
            text = text.replace("'explicit_parent_round': 106", "'explicit_parent_round': 107")
            text = text.replace("'existing_actual_native_bank_fits': 60, 'actual_lowalpha_bank_fits': 20, 'existing_L2_reference_bank_fits': 40,", "'existing_actual_native_bank_fits': 76, 'actual_direct_centered_rank_bank_fits': 36, 'selected_existing_L2_reference_bank_fits': 40,")
            text = text.replace("'actual20_lowalpha_native_bank_source': str(A / 'lowalpha_huber_residual_bank20_20261006/verification.json')", "'actual36_direct_rank_native_bank_source': str(A / 'direct_flag_centered_rank_bank36_20261007/verification.json')")
            text = text.replace("'actual_all_annual_mature_native_and_independent_codec_and_prefix_controls': str(A / 'lowalpha_huber_residual_bank20_20261006/verification.json')", "'actual_all_annual_mature_native_and_independent_codec_and_prefix_controls': str(A / 'direct_flag_centered_rank_bank36_20261007/verification.json')")
        if old.startswith('optimize_'):
            text = text.replace('PREVIOUS_NUMBER = 106', 'PREVIOUS_NUMBER = 107').replace("PREVIOUS = ROOT / 'analysis/optimization_20261003_r106'", "PREVIOUS = ROOT / 'analysis/optimization_20261003_r107'")
            text = text.replace("'native_conditional_residual_ensemble_after_complete_parent100_graph'", "'actual_direct_rank_CDF_comparison_after_complete_parent106_or_explicit_anchor_graph'")
        if old.startswith('publish_'):
            text = text.replace('from collect_full_lossless_round_publication_20261006 import collect', 'from collect_full_lossless_round108_qa19_20261007 import collect')
            text = text.replace("'round': 106", "'round': 108")
            text = text.replace('50项固定较低阈值Huber残差及集成验证', '92项直接中心秩与同日CDF融合验证')
            anchor = '    for path in extra:'
            assert text.count(anchor) == 1
            text = text.replace(anchor, """    extra += [A / 'single_host_rank36_scores_github_20261007/receipt.json',
        A / 'single_host_rank36_bank_github_20261007/receipt.json',
        A / 'train_direct_flag_centered_rank_bank36_20261007.py',
        A / 'run_direct_flag_rank92_official_comparison_20261007.py',
        A / 'direct_flag_centered_rank_CDF_transform_20261007.py',
        A / 'single_host_direct_flag_rank_plan_20261007.json',
        A / 'single_host_rank92_source_admission_20261007.json',
        A / 'collect_full_lossless_round108_qa19_20261007.py']
    extra += [p for p in (A / 'direct_flag_centered_rank_bank36_20261007').rglob('*.json') if not p.name.startswith('model_dump_')]
    for name in ('direct_flag_centered_rank_native_bank36', 'direct_flag_rank92_official_comparison', 'single_host_rank92_scores_after_full107_receipt_closure_v2'):
        service = A / 'service_owned_workflows_20261006' / name
        extra += list(service.glob('*.json')) + list(service.glob('*.log'))
""" + anchor)
        if old.startswith(('build_lossless_', 'verify_lossless_', 'lossless_ranking_runtime_', 'collect_full_lossless_')):
            restored = text
            for before in sorted(effective, key=len, reverse=True):
                restored = restored.replace(effective[before], before)
            assert restored == original, old
        compile(text, str(A / new), 'exec')
        generated[new] = text
        routes.append({'source': old, 'target': new, 'source_sha256': sha(A / old), 'literal_routes': effective})
    for name, text in generated.items():
        with (A / name).open('x', encoding='utf-8', newline='\n') as f:
            f.write(text)
    pins = {str(A / n): sha(A / n) for n in [*NAMES, *NAMES.values(), Path(__file__).name, 'run_direct_rank92_round108_full_registration_20261007.py', 'direct_rank92_selected_candidate_reuse_confirmation_20261007.json']}
    create(A / 'direct_rank92_round108_preparation_20261007.json', {'status': 'passed_actual_complete92_registry_source_preparation_and_exact_existing_candidate_confirmation',
        'at_local': time.strftime('%Y-%m-%dT%H:%M:%S'), 'input_sha256': pins, 'routes': routes,
        'scored_records': 92, 'wave': 391, 'comparison_parent_round': 107, 'selected_original_scheme_training_parent_round': 100,
        'original_full_six_view_and45second_browser_QA_unchanged': True,
        'QA19_actual_date_path_collector_and_round108_receipt_routed_before_execution': True,
        'original_candidate_and_inference_freeze_preserved': True, 'new_inference_claimed': False,
        'actual_new_native_fits': 0, 'new_quality_score_records_by_preparation': 0, 'test_labels_read': False})


if __name__ == '__main__':
    main()
