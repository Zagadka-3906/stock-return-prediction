"""Prepare complete native replay and full103 registration for the declared43 trial."""
from pathlib import Path
import ast
import sys

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path[:0] = [str(ROOT), str(A)]
from run_dependency_queue_v3_20261006 import create, sha


def main():
    common = {
        'conditional_residual_source_freeze_20261006': 'residual_extrapolation43_source_freeze_20261006',
        'conditional_residual_release_20261006': 'residual_extrapolation43_release_20261006',
        'candidates/conditional_residual_20261006': 'candidates/residual_extrapolation43_20261006',
        'conditional_flag_residual_official_comparison_20261006': 'conditional_residual_extrapolation43_official_20261006',
        'service_owned_workflows_20261006/conditional_flag_residual_official_comparison':
            'service_owned_workflows_20261006/conditional_residual_extrapolation43_official_comparison',
        'service_owned_workflows_20261006/conditional_residual_candidate_inference':
            'service_owned_workflows_20261006/residual_extrapolation43_candidate_inference',
        'passed_actual49_conditional_residual_native_and_ensemble_full_official_comparisons':
            'passed_actual43_conditional_residual_extrapolation_full_official_comparisons',
        'predict_conditional_residual_native_scheme_20261006': 'predict_residual_extrapolation43_native_scheme_20261006',
        'freeze_and_infer_conditional_residual_candidate_20261006': 'freeze_and_infer_residual_extrapolation43_candidate_20261006',
        'seal_conditional_residual_candidate_source_package_20261006': 'seal_residual_extrapolation43_candidate_source_package_20261006',
        'conditional_flag_residual_transform_20261006': 'conditional_flag_residual_extrapolation_transform_20261006',
        'full49': 'full43', "== 49": "== 43", "'scored_records': 49": "'scored_records': 43",
        "expected_scored_records=49": "expected_scored_records=43",
        'score_gain_over_parent100': 'score_gain_over_parent102',
        "'explicit_parent_round': 100": "'explicit_parent_round': 102",
        'explicit_parent_round=100': 'explicit_parent_round=102'}
    names = {
        'predict_conditional_residual_native_scheme_20261006.py': 'predict_residual_extrapolation43_native_scheme_20261006.py',
        'freeze_and_infer_conditional_residual_candidate_20261006.py': 'freeze_and_infer_residual_extrapolation43_candidate_20261006.py',
        'freeze_conditional_residual_candidate_sources_20261006.py': 'freeze_residual_extrapolation43_candidate_sources_20261006.py',
        'seal_conditional_residual_candidate_source_package_20261006.py': 'seal_residual_extrapolation43_candidate_source_package_20261006.py',
        'register_conditional_residual_round102_artifacts_20261006.py': 'register_residual_extrapolation43_round103_artifacts_20261006.py',
        'optimize_training_round102.py': 'optimize_training_round103.py',
        'finalize_training_round102.py': 'finalize_training_round103.py',
        'run_conditional_residual_round102_full_registration_20261006.py': 'run_residual_extrapolation43_round103_full_registration_20261006.py',
        'publish_conditional_residual_round102_full_validation_20261006.py': 'publish_residual_extrapolation43_round103_full_validation_20261006.py',
        'build_lossless_ranking_display_v11_20261006.py': 'build_lossless_ranking_display_v12_20261006.py',
        'verify_lossless_ranking_display_v13_20261006.py': 'verify_lossless_ranking_display_v14_20261006.py',
        'lossless_ranking_runtime_adapter_v10_20261006.py': 'lossless_ranking_runtime_adapter_v11_20261006.py'}
    registry_routes = {
        **{old.removesuffix('.py'): new.removesuffix('.py') for old, new in names.items()},
        'prepare_conditional_residual_round102_registration_20261006': 'prepare_residual_extrapolation43_complete_workflow_20261006',
        'conditional_residual_round102_registration_source_preparation_20261006': 'residual_extrapolation43_workflow_preparation_20261006',
        'admit_conditional_residual_round102_full_registration_20261006': 'admit_residual_extrapolation43_round103_full_registration_20261006',
        'conditional_residual_candidate_inference_v2': 'residual_extrapolation43_candidate_inference',
        'conditional_residual_candidate_sealing_v2': 'residual_extrapolation43_candidate_sealing',
        'conditional_residual_candidate_admission_v2_20261006': 'residual_extrapolation43_candidate_admission_20261006',
        'conditional_residual_admission_recovery_v2_20261006': 'residual_extrapolation43_workflow_admission_20261006',
        'admit_conditional_residual_candidate_inference_v2_20261006': 'admit_residual_extrapolation43_candidate_20261006',
        'wait_and_seal_conditional_residual_candidate_v2_20261006': 'wait_and_seal_residual_extrapolation43_candidate_20261006',
        'round102': 'round103', '_r102': '_r103', 'NUMBER = 102': 'NUMBER = 103',
        'PREVIOUS_NUMBER = 100': 'PREVIOUS_NUMBER = 102',
        "PREVIOUS = ROOT / 'analysis/optimization_20261003_r100'": "PREVIOUS = ROOT / 'analysis/optimization_20261003_r102'",
        'WAVES = (385,)': 'WAVES = (386,)', 'wave=385': 'wave=386', 'wave385_results': 'wave386_results',
        "'waves': [385]": "'waves': [386]", "'expected_scored_records': 49": "'expected_scored_records': 43",
        'existing_actual_official_records\': 49': 'existing_actual_official_records\': 43',
        'existing_official_scores_registered\': 49': 'existing_official_scores_registered\': 43',
        'existing_executed_validation_scope': 'existing_executed_validation_scope',
        'collect(102, 13, 49)': 'collect(103, 14, 43)', "namespace['snapshot'](102)": "namespace['snapshot'](103)",
        'publish(102,': 'publish(103,', 'lossless(102)': 'lossless(103)',
        'lossless_ranking_display_qa_v13_20261006': 'lossless_ranking_display_qa_v14_20261006',
        'ranking_display_qa_v13_20261006': 'ranking_display_qa_v14_20261006',
        'assert number == 102': 'assert number == 103', 'actual_complete_QA_version=13': 'actual_complete_QA_version=14',
        "'actual_full_QA_version': 13": "'actual_full_QA_version': 14", "'round': 102": "'round': 103",
        "'original_official_pilot_records_registered': 49": "'original_official_pilot_records_registered': 43",
        '全量49': '全量43', '预定49项完整条件残差及集成官方比较': '预定43项条件残差放大系数及集成官方比较',
        '第102轮49项实际条件残差原生模型与集成验证': '第103轮43项条件残差放大系数及集成验证',
        '既有49项官方评分': '既有43项官方评分', '第102轮目录': '第103轮目录',
        'sealed16_model': 'sealed_selected_model', 'sealed16': 'sealed_selected', 'native16': 'native_selected'}
    proofs, pins, generated = [], {}, {}
    for old, new in names.items():
        original = (A / old).read_text(encoding='utf-8')
        changes = dict(common)
        if old not in list(names)[:4]: changes.update(registry_routes)
        text, effective = original, {}
        for before in sorted(changes, key=len, reverse=True):
            if before in text and changes[before] != before:
                text = text.replace(before, changes[before]); effective[before] = changes[before]
        if old == 'freeze_and_infer_conditional_residual_candidate_20261006.py':
            before = "assert cfg['weight'] > 0 and best['score_gain_over_parent102'] > 0"
            assert text.count(before) == 1
            text = text.replace(before, "assert cfg['weight'] > 0 and best['score_gain_over_parent102'] >= 0")
        if old == 'optimize_training_round102.py':
            text = text.replace('PREVIOUS_NUMBER = 103', 'PREVIOUS_NUMBER = 102')
            text = text.replace("PREVIOUS = ROOT / 'analysis/optimization_20261003_r103'",
                                "PREVIOUS = ROOT / 'analysis/optimization_20261003_r102'")
        if old == 'register_conditional_residual_round102_artifacts_20261006.py':
            assert text.count("== 13 + len(original['native_component_names']) == 16") == 1
            text = text.replace("== 13 + len(original['native_component_names']) == 16", "== 13 + len(original['native_component_names'])")
            text = text.replace("'actual_full_parent100_source': str(A / 'optimization_20261003_r100/component_audit.json')",
                "'actual_full_parent102_source': str(A / 'optimization_20261003_r102/component_audit.json')")
            text = text.replace("'complete_parent100_causal_checks': str(A / 'optimization_20261003_r100/cohort_rank_calibration_causal_checks.json')",
                "'complete_parent102_causal_checks': str(A / 'optimization_20261003_r102/conditional_flag_residual_causal_checks.json')")
        if old.startswith('publish_conditional_residual_round102'):
            before = "    extra += [A / 'residual_extrapolation43_workflow_admission_20261006/verification.json'"
            assert before in text
            # The new workflow has no superseded inference controller. Its own
            # admission proof replaces the unrelated old administrative journal.
            text = text.replace("A / 'residual_extrapolation43_workflow_admission_20261006/verification.json'",
                "A / 'residual_extrapolation43_workflow_admission_20261006/frozen_before_launch.json'")
            text = text.replace('residual_extrapolation43_candidate_inference_v2', 'residual_extrapolation43_candidate_inference')
        for before, after in {'the49': 'the43', 'Register49': 'Register43', 'actual49': 'actual43',
            'all49_': 'all43_', 'actual_all49': 'actual_all43',
            'actual_full_future16_models': 'actual_full_selected_saved_models',
            'actual_conditional_residual102_complete': 'actual_residual_extrapolation103_complete'}.items():
            text = text.replace(before, after)
        if old.startswith(('build_lossless_', 'verify_lossless_', 'lossless_ranking_runtime_')):
            restored = text
            for before in sorted(effective, key=len, reverse=True): restored = restored.replace(effective[before], before)
            assert restored == original
        compile(text, str(A / new), 'exec')
        generated[new] = text
        pins[str(A / old)] = sha(A / old)
        proofs.append({'original': old, 'effective': new, 'explicit_routes': effective})
    runner = ast.parse(generated[names['run_conditional_residual_round102_full_registration_20261006.py']])
    for name in ('publish', 'lossless'):
        assert [n.args[0].value for n in ast.walk(runner) if isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id == name] == [103]
    pub = ast.parse(generated[names['publish_conditional_residual_round102_full_validation_20261006.py']])
    assert [[a.value for a in n.args] for n in ast.walk(pub) if isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id == 'collect'] == [[103, 14, 43]]
    assert [n.args[0].value for n in ast.walk(pub) if isinstance(n, ast.Call) and isinstance(n.func, ast.Subscript) and isinstance(n.func.slice, ast.Constant) and n.func.slice.value == 'snapshot'] == [103]
    optimizer = ast.parse(generated['optimize_training_round103.py'])
    constants = {target.id: node.value.value for node in optimizer.body if isinstance(node, ast.Assign)
        and isinstance(node.value, ast.Constant) for target in node.targets if isinstance(target, ast.Name)}
    assert constants['NUMBER'] == 103 and constants['PREVIOUS_NUMBER'] == 102
    assert "PREVIOUS = ROOT / 'analysis/optimization_20261003_r102'" in generated['optimize_training_round103.py']
    for new, text in generated.items():
        assert '15101600' not in text and 'neural17384' not in text
        with (A / new).open('x', encoding='utf-8') as stream: stream.write(text)
        pins[str(A / new)] = sha(A / new)
    for name in ('admit_residual_extrapolation43_candidate_20261006.py',
                 'wait_and_seal_residual_extrapolation43_candidate_20261006.py',
                 'admit_residual_extrapolation43_round103_full_registration_20261006.py'):
        p = A / name
        compile(p.read_text(encoding='utf-8'), str(p), 'exec'); pins[str(p)] = sha(p)
    pins[str(Path(__file__))] = sha(Path(__file__))
    create(A / 'residual_extrapolation43_workflow_preparation_20261006.json', {
        'status': 'prepared_actual43_extended_domain_saved_model_replay_and_full103_QA14',
        'input_sha256': pins, 'routes': proofs, 'actual_AST_collect': [103, 14, 43],
        'actual_AST_publish_lossless_snapshot_round': 103,
        'baseline_case_retained_even_if_all_extensions_fail_to_improve': True,
        'all_original_six_views_and_full_decoder_and_cold80_controls_retained': True,
        'new_native_fits_by_preparation': 0, 'new_quality_scores_by_preparation': 0,
        'native_candidate_count_follows_selected_frozen_components': True,
        'all_external_absolute_input_locks_and_full_rehash_retained': True, 'test_labels_read': False})


if __name__ == '__main__':
    main()
