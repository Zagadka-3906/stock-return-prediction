"""Prepare exact102/49 routes, preserving all original full ranking and browser QA."""
from pathlib import Path
import ast
import sys

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path[:0] = [str(ROOT), str(A)]
from run_dependency_queue_v3_20261006 import create, sha


def main():
    routes = [
        ('optimize_training_round101.py', 'optimize_training_round102.py', {
            '_r101': '_r102', 'NUMBER = 101': 'NUMBER = 102', 'PREVIOUS_NUMBER = 99': 'PREVIOUS_NUMBER = 100',
            "PREVIOUS = ROOT / 'analysis/optimization_20261003_r99'": "PREVIOUS = ROOT / 'analysis/optimization_20261003_r100'",
            'WAVES = (384,)': 'WAVES = (385,)', 'conditional_flag_rank_scheme_graph': 'conditional_flag_residual_scheme_graph',
            'native_conditional_flag_rank_after_complete_parent99_graph': 'native_conditional_residual_ensemble_after_complete_parent100_graph',
            "MEMBERS = ('native_conditional_flag_rank',)": "MEMBERS = ('native_conditional_residual_ensemble',)",
            '== 37': '== 49', 'the37 actually scored conditional native flag schemes': 'the49 actually scored conditional residual schemes'}),
        ('finalize_training_round101.py', 'finalize_training_round102.py', {
            'optimize_training_round101': 'optimize_training_round102', '== 37': '== 49',
            "['conditional_flag_rank']": "['conditional_flag_residual']",
            "('model', 'weight', 'first_year_slope')": "('model', 'weight')"}),
        ('run_conditional_flag_round101_full_registration_20261006.py', 'run_conditional_residual_round102_full_registration_20261006.py', {
            'register_conditional_flag_round101_artifacts_20261006': 'register_conditional_residual_round102_artifacts_20261006',
            'publish_conditional_flag_round101_full_validation_20261006': 'publish_conditional_residual_round102_full_validation_20261006',
            'lossless_ranking_runtime_adapter_v9_20261006': 'lossless_ranking_runtime_adapter_v10_20261006',
            'round101': 'round102', '_r101': '_r102', 'publish(101,': 'publish(102,',
            'lossless(100)': 'lossless(102)', "'existing_official_scores_registered': 37": "'existing_official_scores_registered': 49",
            'conditional_flag_rank_causal_checks.json': 'conditional_flag_residual_causal_checks.json',
            '成熟历史标签的涨停分组单调排名校准': '成熟历史标签的涨停条件残差原生模型与等权集成',
            '预定37项完整条件模型官方比较': '预定49项完整条件残差及集成官方比较'}),
        ('publish_conditional_flag_round101_full_validation_20261006.py', 'publish_conditional_residual_round102_full_validation_20261006.py', {
            'round101': 'round102', '_r101': '_r102', 'collect(101, 12, 37)': 'collect(102, 13, 49)',
            "namespace['snapshot'](100)": "namespace['snapshot'](102)", "'round': 101": "'round': 102",
            '== 37': '== 49', "'scored_records': 37": "'scored_records': 49",
            "'original_official_pilot_records_registered': 37": "'original_official_pilot_records_registered': 49",
            'lossless_ranking_display_qa_v12_20261006': 'lossless_ranking_display_qa_v13_20261006',
            'actual_complete_QA_version=12': 'actual_complete_QA_version=13', "'actual_full_QA_version': 12": "'actual_full_QA_version': 13",
            'actual_conditional101': 'actual_conditional_residual102',
            'conditional_flag_rank_release_20261006': 'conditional_residual_release_20261006',
            'conditional_flag_rank_official_comparison_v2_20261006': 'conditional_flag_residual_official_comparison_20261006',
            'conditional_flag_round101_registration_source_preparation_20261006': 'conditional_residual_round102_registration_source_preparation_20261006',
            'conditional_flag_rank_source_freeze_20261006': 'conditional_residual_source_freeze_20261006',
            'conditional_flag_rank_bank_v2_20261006': 'conditional_flag_residual_bank_20261006',
            'conditional_flag_rank_20261006': 'conditional_residual_20261006',
            'service_owned_workflows_20261006/conditional_flag_rank_candidate_inference': 'service_owned_workflows_20261006/conditional_residual_candidate_inference_v2',
            'conditional_native_replay_verification.json': 'conditional_residual_native_replay_verification.json',
            '第101轮37项实际原生条件模型验证': '第102轮49项实际条件残差原生模型与集成验证',
            '既有37项官方评分': '既有49项官方评分', '第101轮目录': '第102轮目录'}),
        ('build_lossless_ranking_display_v10_20261006.py', 'build_lossless_ranking_display_v11_20261006.py', {'assert number == 101': 'assert number == 102'}),
        ('verify_lossless_ranking_display_v12_20261006.py', 'verify_lossless_ranking_display_v13_20261006.py', {
            'build_lossless_ranking_display_v10_20261006': 'build_lossless_ranking_display_v11_20261006',
            'lossless_ranking_display_qa_v12_20261006': 'lossless_ranking_display_qa_v13_20261006',
            'ranking_display_qa_v12_20261006': 'ranking_display_qa_v13_20261006'}),
        ('lossless_ranking_runtime_adapter_v9_20261006.py', 'lossless_ranking_runtime_adapter_v10_20261006.py', {
            'assert number == 101': 'assert number == 102',
            'build_lossless_ranking_display_v10_20261006': 'build_lossless_ranking_display_v11_20261006',
            'verify_lossless_ranking_display_v12_20261006': 'verify_lossless_ranking_display_v13_20261006',
            'lossless_ranking_display_qa_v12_20261006': 'lossless_ranking_display_qa_v13_20261006'})]
    pins, proofs, generated = {}, [], {}
    for old, new, changes in routes:
        source = A / old
        original = source.read_text(encoding='utf-8')
        text = original
        effective = {}
        for before in sorted(changes, key=len, reverse=True):
            if before not in text:
                assert changes[before] in text, (old, before)
                continue
            text = text.replace(before, changes[before])
            effective[before] = changes[before]
        if new.startswith(('build_lossless_', 'verify_lossless_', 'lossless_ranking_runtime_')):
            restored = text
            for before in sorted(effective, key=len, reverse=True):
                restored = restored.replace(effective[before], before)
            assert restored == original
        if new.startswith('publish_conditional_residual_'):
            marker = '    for path in extra:\n'
            assert text.count(marker) == 1
            text = text.replace(marker,
                "    extra += [A / 'conditional_residual_admission_recovery_v2_20261006/verification.json', A / 'conditional_residual_candidate_admission_v2_20261006/actual_admission.json', A / 'admit_conditional_residual_candidate_inference_v2_20261006.py', A / 'wait_and_seal_conditional_residual_candidate_v2_20261006.py']\n"
                "    extra += list((A / 'service_owned_workflows_20261006/conditional_residual_candidate_sealing_v2').glob('*.json'))\n"
                "    extra += list((A / 'conditional_residual_admission_recovery_v2_20261006').glob('*.json'))\n" + marker)
            text = text.replace("'actual_full_QA_version': 13,", "'actual_full_QA_version': 13, 'full_immutable_ranking_and_all_original_QA_preserved': True,")
        compile(text, str(A / new), 'exec')
        generated[new] = text
        pins[str(source)] = sha(source)
        proofs.append({'original': old, 'effective': new, 'explicit_changes': effective})
    # Inspect actual AST call arguments, rather than trusting substitutions.
    runner = ast.parse(generated['run_conditional_residual_round102_full_registration_20261006.py'])
    assert [n.args[0].value for n in ast.walk(runner) if isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id == 'lossless'] == [102]
    assert [n.args[0].value for n in ast.walk(runner) if isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id == 'publish'] == [102]
    publisher = ast.parse(generated['publish_conditional_residual_round102_full_validation_20261006.py'])
    assert [[a.value for a in n.args] for n in ast.walk(publisher) if isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id == 'collect'] == [[102, 13, 49]]
    assert [n.args[0].value for n in ast.walk(publisher) if isinstance(n, ast.Call) and isinstance(n.func, ast.Subscript) and isinstance(n.func.slice, ast.Constant) and n.func.slice.value == 'snapshot'] == [102]
    for new, text in generated.items():
        assert '15101600' not in text and 'neural17384' not in text
        with (A / new).open('x', encoding='utf-8') as stream:
            stream.write(text)
        pins[str(A / new)] = sha(A / new)
    registrar = A / 'register_conditional_residual_round102_artifacts_20261006.py'
    pins[str(registrar)] = sha(registrar)
    create(A / 'conditional_residual_round102_registration_source_preparation_20261006.json', {
        'status': 'prepared_complete_actual49_record_native16_round102_and_full_QA13',
        'input_sha256': pins, 'controls': proofs, 'all_original_six_views_and_browser_checks_preserved': True,
        'actual_AST_lossless_publish_and_snapshot_round': 102, 'actual_AST_collect': [102, 13, 49],
        'all_absolute_external_input_pins_preserved': True, 'browser_timeout_seconds': 45,
        'native_training_or_quality_scores_by_preparation': 0,
        'nested_manifests_covered_and_large_JSON_lossless_publication': True, 'test_labels_read': False})


if __name__ == '__main__':
    main()
