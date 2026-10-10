"""Preserve the complete103 registry and QA machinery for the actual74-case branch."""
from pathlib import Path
import ast
import sys

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path[:0] = [str(ROOT), str(A)]
from run_dependency_queue_v3_20261006 import create, sha, read


def main():
    names = {
        'register_residual_extrapolation43_round103_artifacts_20261006.py': 'register_longer_residual74_round104_artifacts_20261006.py',
        'optimize_training_round103.py': 'optimize_training_round104.py',
        'finalize_training_round103.py': 'finalize_training_round104.py',
        'run_residual_extrapolation43_round103_full_registration_20261006.py': 'run_longer_residual74_round104_full_registration_20261006.py',
        'publish_residual_extrapolation43_round103_full_validation_20261006.py': 'publish_longer_residual74_round104_full_validation_20261006.py',
        'build_lossless_ranking_display_v12_20261006.py': 'build_lossless_ranking_display_v13_20261006.py',
        'verify_lossless_ranking_display_v14_20261006.py': 'verify_lossless_ranking_display_v15_20261006.py',
        'lossless_ranking_runtime_adapter_v11_20261006.py': 'lossless_ranking_runtime_adapter_v12_20261006.py',
    }
    changes = {
        **{old.removesuffix('.py'): new.removesuffix('.py') for old, new in names.items()},
        'admit_residual_extrapolation43_round103_full_registration_20261006': 'admit_longer_residual74_round104_full_registration_20261006',
        'prepare_residual_extrapolation43_complete_workflow_20261006': 'prepare_longer_residual74_full_registration_20261006',
        'residual_extrapolation43_workflow_preparation_20261006': 'longer_residual74_full_registration_preparation_20261006',
        'residual_extrapolation43_workflow_admission_20261006': 'longer_residual74_workflow_admission_20261006',
        'residual_extrapolation43_candidate_admission_20261006': 'longer_residual74_candidate_admission_20261006',
        'admit_residual_extrapolation43_candidate_20261006': 'admit_longer_residual74_candidate_20261006',
        'wait_and_seal_residual_extrapolation43_candidate_20261006': 'wait_and_seal_longer_residual74_candidate_20261006',
        'residual_extrapolation43_candidate_inference': 'longer_residual74_candidate_inference',
        'residual_extrapolation43_candidate_sealing': 'longer_residual74_candidate_sealing',
        'residual_extrapolation43_source_freeze_20261006': 'longer_residual74_source_freeze_20261006',
        'residual_extrapolation43_release_20261006': 'longer_residual74_release_20261006',
        'residual_extrapolation43_20261006': 'longer_residual74_20261006',
        'conditional_residual_extrapolation43_official_20261006': 'conditional_residual128_256_comparison74_20261006',
        'passed_actual43_conditional_residual_extrapolation_full_official_comparisons': 'passed_actual74_matched128_256_residual_and_ensemble_full_official_comparisons',
        'conditional_flag_residual_bank_20261006': 'conditional_residual128_256_bank40_20261006',
        'lossless_ranking_display_qa_v14_20261006': 'lossless_ranking_display_qa_v15_20261006',
        'ranking_display_qa_v14_20261006': 'ranking_display_qa_v15_20261006',
        'collect(103, 14, 43)': 'collect(104, 15, 74)',
        "namespace['snapshot'](103)": "namespace['snapshot'](104)",
        'publish(103,': 'publish(104,', 'lossless(103)': 'lossless(104)',
        'assert number == 103': 'assert number == 104',
        'actual_complete_QA_version=14': 'actual_complete_QA_version=15',
        "'actual_full_QA_version': 14": "'actual_full_QA_version': 15",
        'round103': 'round104', '_r103': '_r104',
        'NUMBER = 103': 'NUMBER = 104', 'PREVIOUS_NUMBER = 102': 'PREVIOUS_NUMBER = 100',
        "PREVIOUS = ROOT / 'analysis/optimization_20261003_r102'": "PREVIOUS = ROOT / 'analysis/optimization_20261003_r100'",
        'WAVES = (386,)': 'WAVES = (387,)', 'wave=386': 'wave=387',
        'wave386_results': 'wave387_results', "'waves': [386]": "'waves': [387]",
        "'explicit_parent_round': 102": "'explicit_parent_round': 100",
        "'round': 103": "'round': 104", '== 43': '== 74',
        "'expected_scored_records': 43": "'expected_scored_records': 74",
        "'existing_actual_official_records': 43": "'existing_actual_official_records': 74",
        "'existing_official_scores_registered': 43": "'existing_official_scores_registered': 74",
        "'scored_records': 43": "'scored_records': 74",
        "'original_official_pilot_records_registered': 43": "'original_official_pilot_records_registered': 74",
        "'actual_native_bank_fits': 20": "'actual_native_bank_fits': 40",
        'actual20': 'actual40', 'all43': 'all74', 'actual43': 'actual74',
        'Register43': 'Register74', 'the43': 'the74',
        'original_actual_official37_scores': 'original_actual_official74_scores',
        'actual_residual_extrapolation103_complete': 'actual_longer_residual104_complete',
        '第103轮': '第104轮', '既有43项': '既有74项',
        '预定43项条件残差放大系数及集成官方比较': '预定74项128与256棵树条件残差及集成官方比较',
        '43项条件残差放大系数及集成验证': '74项128与256棵树条件残差及集成验证',
    }
    pins, generated, routes = {}, {}, []
    for old, new in names.items():
        original = (A / old).read_text(encoding='utf-8')
        text, effective = original, {}
        for before in sorted(changes, key=len, reverse=True):
            if before in text:
                text = text.replace(before, changes[before]); effective[before] = changes[before]
        if old.startswith('register_'):
            text = text.replace("'actual_full_parent102_source': str(A / 'optimization_20261003_r102/component_audit.json')",
                                "'actual_full_parent100_source': str(A / 'optimization_20261003_r100/component_audit.json')")
            text = text.replace("'complete_parent102_causal_checks': str(A / 'optimization_20261003_r102/conditional_flag_residual_causal_checks.json')",
                                "'complete_parent100_causal_checks': str(A / 'optimization_20261003_r100/cohort_rank_calibration_causal_checks.json')")
            before = "'actual40_native_bank_source': str(A / 'conditional_residual128_256_bank40_20261006/verification.json'),"
            assert text.count(before) == 1
            text = text.replace(before, before +
                "\n        'actual_original64_anchor_bank_source': str(A / 'conditional_flag_residual_bank_20261006/verification.json'),")
        if old.startswith('publish_'):
            before = "    extra += list((A / 'conditional_residual128_256_bank40_20261006').glob('*/info_*.json'))"
            assert text.count(before) == 1
            text = text.replace(before, before +
                "\n    extra += [A / 'conditional_flag_residual_bank_20261006/verification.json',\n"
                "        A / 'longer_residual74_candidate_workflow_preparation_20261006.json',\n"
                "        A / 'longer_residual74_workflow_admission_20261006/verification.json']\n"
                "    extra += list((A / 'conditional_residual128_256_bank40_20261006').glob('*/original64_prefix_*_verification.json'))\n")
        if old.startswith(('build_lossless_', 'verify_lossless_', 'lossless_ranking_runtime_')):
            restored = text
            for before in sorted(effective, key=len, reverse=True): restored = restored.replace(effective[before], before)
            assert restored == original, 'All original full ranking and browser QA arithmetic must remain unchanged'
        compile(text, str(A / new), 'exec')
        generated[new] = text
        pins[str(A / old)] = sha(A / old)
        routes.append({'source': old, 'target': new, 'explicit_replacements': effective})
    runner = ast.parse(generated['run_longer_residual74_round104_full_registration_20261006.py'])
    for name in ('publish', 'lossless'):
        assert [n.args[0].value for n in ast.walk(runner) if isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id == name] == [104]
    publisher = ast.parse(generated['publish_longer_residual74_round104_full_validation_20261006.py'])
    assert [[a.value for a in n.args] for n in ast.walk(publisher) if isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id == 'collect'] == [[104, 15, 74]]
    assert [n.args[0].value for n in ast.walk(publisher) if isinstance(n, ast.Call) and isinstance(n.func, ast.Subscript) and isinstance(n.func.slice, ast.Constant) and n.func.slice.value == 'snapshot'] == [104]
    optimizer = ast.parse(generated['optimize_training_round104.py'])
    constants = {target.id: node.value.value for node in optimizer.body if isinstance(node, ast.Assign) and isinstance(node.value, ast.Constant) for target in node.targets if isinstance(target, ast.Name)}
    assert constants['NUMBER'] == 104 and constants['PREVIOUS_NUMBER'] == 100
    assert "PREVIOUS = ROOT / 'analysis/optimization_20261003_r100'" in generated['optimize_training_round104.py']
    for new in generated: assert not (A / new).exists(), new
    prep = A / 'longer_residual74_candidate_workflow_preparation_20261006.json'
    pins.update(read(prep)['input_sha256']); pins[str(prep)] = sha(prep)
    pins[str(Path(__file__))] = sha(Path(__file__))
    admission = A / 'admit_longer_residual74_round104_full_registration_20261006.py'
    compile(admission.read_text(encoding='utf-8'), str(admission), 'exec')
    pins[str(admission)] = sha(admission)
    for new, text in generated.items():
        with (A / new).open('x', encoding='utf-8') as stream: stream.write(text)
        pins[str(A / new)] = sha(A / new)
    create(A / 'longer_residual74_full_registration_preparation_20261006.json', {
        'status': 'prepared_actual74_independent_parent100_branch_full104_QA15',
        'input_sha256': pins, 'routes': routes,
        'actual_AST_collect': [104, 15, 74], 'actual_AST_publish_lossless_snapshot_round': 104,
        'explicit_training_parent_round': 100, 'qualified102_anchor_retained_in_original74_comparison': True,
        'same_selected_saved_component_graph_and_exact_metric_capsules_required': True,
        'complete_six_views_browser45s_all_values_full_source_provenance_and_candidate_QA_preserved': True,
        'both_original64_reference_and_new40_matched_native_bank_evidence_preserved': True,
        'global_direction_or_resource_exhaustion_claimed': False,
        'new_native_fits': 0, 'new_quality_scores': 0, 'test_labels_read': False,
    })


if __name__ == '__main__': main()
