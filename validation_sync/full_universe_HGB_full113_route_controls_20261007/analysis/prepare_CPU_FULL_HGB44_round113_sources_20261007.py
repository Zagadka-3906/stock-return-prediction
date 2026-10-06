"""Prepare44-record registration after actual selected candidate sealing; retain full QA."""
from pathlib import Path
import hashlib
import re
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path[:0] = [str(ROOT), str(A)]
from run_dependency_queue_v3_20261006 import read, sha, create

NAMES = {
    'register_direct_rank_micro74_round109_artifacts_20261007.py': 'register_CPU_FULL_HGB44_round113_artifacts_20261007.py',
    'optimize_training_round109.py': 'optimize_training_round113.py',
    'finalize_training_round109.py': 'finalize_training_round113.py',
    'publish_direct_rank_micro74_round109_full_validation_20261007.py': 'publish_CPU_FULL_HGB44_round113_full_validation_20261007.py',
    'build_lossless_ranking_display_round109_20261007.py': 'build_lossless_ranking_display_round113_20261007.py',
    'verify_lossless_ranking_display_round109_20261007.py': 'verify_lossless_ranking_display_round113_20261007.py',
    'lossless_ranking_runtime_adapter_round109_20261007.py': 'lossless_ranking_runtime_adapter_round113_20261007.py',
    'collect_full_lossless_round109_qa20_20261007.py': 'collect_full_lossless_round113_qa24_20261007.py',
}


def substitute(text, mappings):
    pattern = '|'.join(map(re.escape, sorted(mappings, key=len, reverse=True)))
    return re.sub(pattern, lambda match: mappings[match.group()], text)


def main():
    ready_path = A / 'CPU_FULL_HGB_residual44_selected_release_20261007/selected_candidate_ready_for_registration.json'
    ready = read(ready_path)
    assert ready['status'] == 'passed_actual44_selected_candidate_full_graph_and_metrics_and_source_bytes'
    assert ready['sealed_candidate_complete']
    assert read(A / 'optimization_20261003_r112/full_registration_execution.json')['status'] == 'passed'
    assert read(A / 'cpu_full_universe_HGB24_scores_github_20261007/receipt.json')['scored_records'] == 44
    candidate = Path(ready['source_candidate'])
    assert sha(candidate / 'manifest.json') == ready['source_manifest_sha256']
    for relative, info in read(candidate / 'manifest.json')['files'].items():
        assert sha(candidate / relative) == info['sha256'], relative
    pilot = read(A / 'full_universe_HGB44_official_comparison_v2_20261007/verification.json')
    assert len(pilot['records']) == 44 and pilot['best'] == ready['best']
    assert read(candidate / 'verification.json')['whole_scheme_graph'] == read(candidate / 'selection.json')['winner']['conditional_flag_residual_scheme_graph']
    for name in [*NAMES.values(), 'CPU_FULL_HGB44_round113_source_preparation_20261007.json']:
        assert not (A / name).exists(), name
    common = {**{old.removesuffix('.py'): new.removesuffix('.py') for old, new in NAMES.items()},
        'run_direct_rank_micro74_round109_full_registration_20261007': 'run_CPU_FULL_HGB44_round113_full_registration_20261007',
        'prepare_direct_rank_micro74_round109_20261007': 'prepare_CPU_FULL_HGB44_round113_sources_20261007',
        'direct_rank_micro74_round109_preparation_20261007': 'CPU_FULL_HGB44_round113_source_preparation_20261007',
        'direct_rank_micro74_selected_candidate_reuse_confirmation_20261007.json': 'CPU_FULL_HGB_residual44_selected_release_20261007/selected_candidate_ready_for_registration.json',
        'direct_flag_rank_micro74_official_comparison_20261007': 'full_universe_HGB44_official_comparison_v2_20261007',
        'passed_actual74_micro_amplitude_direct_rank_CDF_full_official_comparisons': 'passed_actual44_full_universe_CPU_HGB_CDF_full_official_comparisons',
        'single_host_rank_micro74_scores_github_20261007': 'cpu_full_universe_HGB24_scores_github_20261007',
        'round108_receipt.json': 'round112_receipt.json', '_r108': '_r112',
        'PREVIOUS_NUMBER = 108': 'PREVIOUS_NUMBER = 112',
        'round109': 'round113', '_r109': '_r113', 'NUMBER = 109': 'NUMBER = 113',
        'assert number == 109': 'assert number == 113', "namespace['snapshot'](109)": "namespace['snapshot'](113)",
        'WAVES = (392,)': 'WAVES = (396,)', 'wave=392': 'wave=396',
        'wave392_results': 'wave396_results', "'waves': [392]": "'waves': [396]",
        'lossless_ranking_display_qa_v20_20261007': 'lossless_ranking_display_qa_v24_20261007',
        'ranking_display_qa_v20_20261007': 'ranking_display_qa_v24_20261007',
        '(109, 20, 74)': '(113, 24, 44)', 'actual_complete_QA_version=20': 'actual_complete_QA_version=24',
        "'actual_full_QA_version': 20": "'actual_full_QA_version': 24", "'round': 109": "'round': 113",
        '== 74': '== 44', "'expected_scored_records': 74": "'expected_scored_records': 44",
        "'existing_actual_official_records': 74": "'existing_actual_official_records': 44",
        "'scored_records': 74": "'scored_records': 44", "'original_official_pilot_records_registered': 74": "'original_official_pilot_records_registered': 44",
        'all74': 'all44', 'actual74': 'actual44', 'the74': 'the44', 'official74': 'official44',
        'Registry for the74': 'Registry for the44', 'Register74': 'Register44', '既有74项': '既有44项',
        '第109轮': '第113轮', '74项较小幅度直接中心秩与同日CDF融合': '44项全股票池CPU直方图梯度回归与同日CDF融合',
    }
    generated, routes = {}, []
    for old, new in NAMES.items():
        original = (A / old).read_text(encoding='utf-8')
        effective = {key: value for key, value in common.items() if key in original}
        text = substitute(original, effective)
        if old.startswith('register_'):
            text = text.replace("RELEASE = A / 'simplex_residual47_release_20261006'\nSOURCE_CANDIDATE = ROOT / 'candidates/simplex_residual47_20261006'", "READY = read(A / 'CPU_FULL_HGB_residual44_selected_release_20261007/selected_candidate_ready_for_registration.json')\nRELEASE = Path(READY['source_release'])\nSOURCE_CANDIDATE = Path(READY['source_candidate'])")
            text = text.replace("len(actual['models']) == 13 + len(original['native_component_names'])", "len(actual['models']) == READY['actual_saved_native_models']")
            start = text.index("        graph = deepcopy(actual['whole_scheme_graph'])")
            end = text.index('        row = ', start)
            text = text[:start] + """        if measured['case'] == pilot['best']['case']:
            graph = deepcopy(actual['whole_scheme_graph'])
        elif cfg['model'] is None and cfg['anchor_round'] == 100:
            graph = deepcopy(read(A / 'optimization_20261003_r100/selection.json')['winner']['extended_cohort_rank_calibration_scheme_graph'])
        else:
            graph = deepcopy(read(ROOT / 'candidates/simplex_residual47_20261006/verification.json')['whole_scheme_graph'])
            if cfg['model'] is not None:
                graph['full_universe_CPU_HGB_rank_CDF'] = {**cfg,
                    'actual_annual_native_bank': measured['native_bank_source'],
                    'ordered_equal_mean_components': measured['ensemble_components'] or [cfg['model']],
                    'prediction_targets': 'mature supplied rank or own-past winsorized return; per-head daily percentile before ordered mean',
                    'transformation': '(1-weight)*parent_percentile+weight*mean_head_percentile; same-day parent inverseCDF',
                    'actual2020_native_fold': True, 'full_pool_including_nonflag': True,
                    'future_candidate_not_inferred_for_nonselected_comparison': True}
""" + text[end:]
            text = text.replace('explicit_comparison_parent_round=108', 'explicit_comparison_parent_round=112')
            text = text.replace("'explicit_parent_round': 108", "'explicit_parent_round': 112")
            text = text.replace('preserved_scheme_training_parent_round=100', 'preserved_scheme_training_parent_round=106')
            text = text.replace("'existing_actual_native_bank_fits': 76, 'actual_direct_centered_rank_bank_fits': 36, 'selected_existing_L2_reference_bank_fits': 40,", "'actual_new_CPU_FULL_HGB_native_bank_fits': 24, 'saved_selected_parent_models': 15,")
            text = text.replace("A / 'direct_flag_centered_rank_bank36_20261007/verification.json'", "A / 'cpu_full_universe_HGB_bank24_20261007/verification.json'")
            text = text.replace('actual36_direct_rank_native_bank_source', 'actual24_CPU_FULL_HGB_native_bank_source')
            text = text.replace("A / 'publish_explicit_parent_training_round_v2_20261005.py',", "A / 'publish_explicit_parent_training_round_v2_20261005.py',\n        A / 'CPU_FULL_HGB44_selected_candidate_source_admission_20261007.json',\n        A / 'prepare_CPU_FULL_HGB_residual44_selected_candidate_20261007.py',\n        A / 'seal_CPU_FULL_HGB_residual44_selected_candidate_20261007.py',\n        A / 'predict_full_universe_CPU_HGB_rank_CDF_scheme_20261007.py',")
        elif old.startswith('optimize_'):
            text = text.replace("'actual_direct_rank_CDF_comparison_after_complete_parent106_or_explicit_anchor_graph'", "'actual_full_pool_CPU_HGB_rank_CDF_comparison_after_complete_parent106_or_explicit_anchor_graph'")
            text = text.replace("'training_parent_round': 100", "'training_parent_round': 106")
        elif old.startswith('finalize_'):
            text = text.replace("spec = record['winner'][GRAPH_FIELD]['conditional_flag_residual']", "graph = record['winner'][GRAPH_FIELD]\n    spec = graph.get('full_universe_CPU_HGB_rank_CDF', graph['conditional_flag_residual'])")
        elif old.startswith('publish_'):
            start = text.index('    extra = [')
            end = text.index('    for path in extra:', start)
            text = text[:start] + """    ready = read(A / 'CPU_FULL_HGB_residual44_selected_release_20261007/selected_candidate_ready_for_registration.json')
    extra = [Path(__file__), A / 'CPU_FULL_HGB44_round113_source_preparation_20261007.json',
        A / 'prepare_CPU_FULL_HGB44_round113_sources_20261007.py',
        A / 'run_CPU_FULL_HGB44_round113_full_registration_20261007.py',
        A / 'CPU_FULL_HGB44_selected_candidate_source_admission_20261007.json',
        A / 'prepare_CPU_FULL_HGB_residual44_selected_candidate_20261007.py',
        A / 'seal_CPU_FULL_HGB_residual44_selected_candidate_20261007.py',
        A / 'predict_full_universe_CPU_HGB_rank_CDF_scheme_20261007.py',
        A / 'full_universe_HGB_percentile_CDF_transform_20261007.py', A / 'cpu_numerical_HGB_large_batch_codec_v2_20261007.py',
        A / 'cpu_full_universe_HGB24_bank_github_20261007/receipt.json',
        A / 'cpu_full_universe_HGB24_scores_github_20261007/receipt.json',
        ROOT / 'candidates/optimization_20261003_r113/registry_alias_verification.json',
        Path(ready['source_candidate']) / 'manifest.json']
    for folder in (A / 'CPU_FULL_HGB_residual44_selected_release_20261007', Path(ready['source_release']),
        A / 'full_universe_HGB44_official_comparison_v2_20261007',
        A / 'full_universe_HGB_selected_hook_preflight_20261007'):
        extra += list(folder.glob('*.json'))
    extra += [p for p in (A / 'cpu_full_universe_HGB_bank24_20261007').rglob('*.json') if not p.name.startswith('independent_hist_tree_state_')]
    for name in ('cpu_full_universe_HGB_native_bank24', 'full_universe_HGB44_official_comparison_v2',
        'cpu_full_universe_HGB24_bank_evidence_publication', 'cpu_full_universe_HGB24_scores_evidence_publication',
        'CPU_FULL_HGB44_selected_candidate_preparation', 'CPU_FULL_HGB44_selected_candidate_sealing'):
        service = A / 'service_owned_workflows_20261006' / name
        extra += list(service.glob('*.json')) + list(service.glob('*.log'))
""" + text[end:]
            text = text.replace("actual_inference_source_candidate='candidates/simplex_residual47_20261006'", "actual_inference_source_candidate=ready['source_candidate']")
            start = text.index("    payload[(prefix / 'README.md').as_posix()] += (")
            end = text.index("    previous = sync.git", start)
            text = text[:start] + """    payload[(prefix / 'README.md').as_posix()] += (
        '\\n本轮登记44项全股票池CPU直方图梯度回归、固定均值集成及CDF幅度的完整官方比较。'
        '仅按原始完整连接总分选优，不设单项、最差年份或显著性额外淘汰门槛。'
        '训练期24个模型均保存重载并以独立NumPy数值树解码与日期前缀实际核验。'
        '获胜模型已按冻结方案执行完整1599600行两次重载与80日前缀；'
        '若获胜的是相同106锚点，则通过全部预测位、8项指标、图与封存文件核对后复用，0新增推理。'
        '具体采用哪种情况由随附selected_candidate_ready_for_registration.json记录，不把复用冒充新推理。'
        '完整榜六视图及45秒浏览器检查均保留。只main，未读真实测试标签。\\n').encode('utf-8')
""" + text[end:]
        else:
            restored = substitute(text, {value: key for key, value in effective.items()})
            assert restored == original, old
        compile(text, str(A / new), 'exec')
        generated[new] = text
        routes.append({'source': old, 'target': new, 'source_sha256': sha(A / old), 'literal_routes': effective})
    preflight = read(A / 'CPU_FULL_HGB44_round113_source_route_preflight_20261007.json')
    assert preflight['status'] == 'passed_prospective_eight_source_AST_and_original_QA_reverse_routes_only'
    for name, text in generated.items():
        assert hashlib.sha256(text.encode('utf-8')).hexdigest() == preflight['generated_source_sha256'][name], name
        with (A / name).open('x', encoding='utf-8', newline='\n') as stream:
            stream.write(text)
    pins = {str(A / name): sha(A / name) for name in [*NAMES, *NAMES.values(), Path(__file__).name,
        'run_CPU_FULL_HGB44_round113_full_registration_20261007.py']}
    pins[str(ready_path)] = sha(ready_path)
    create(A / 'CPU_FULL_HGB44_round113_source_preparation_20261007.json', {'status': 'passed_actual44_selected_candidate_registry_and_unchanged_QA21_source_routes',
        'input_sha256': pins, 'routes': routes, 'scored_records': 44, 'wave': 396, 'round': 113,
        'new_native_fits_by_preparation': 0, 'new_quality_scores': 0,
        'all_original_six_views_full_parameters_sources_and45second_browser_checks_preserved': True,
        'test_labels_read': False})


if __name__ == '__main__':
    main()
