"""Prepare37-score registration without changing prior frozen inference sources."""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path.insert(0, str(A))
from run_dependency_queue_v3_20261006 import create, sha


def main():
    routes = [
        ('optimize_training_round100.py', 'optimize_training_round101.py', {
            '_r100': '_r101', 'NUMBER = 100': 'NUMBER = 101', 'PREVIOUS_NUMBER = 95': 'PREVIOUS_NUMBER = 99',
            "PREVIOUS = ROOT / 'analysis/optimization_20261003_r95'": "PREVIOUS = ROOT / 'analysis/optimization_20261003_r99'",
            'WAVES = (383,)': 'WAVES = (384,)', 'extended_cohort_rank_calibration_scheme_graph': 'conditional_flag_rank_scheme_graph',
            'mature_cohort_rank_calibration_after_complete_parent95_graph': 'native_conditional_flag_rank_after_complete_parent99_graph',
            "MEMBERS = ('mature_cohort_rank_calibration',)": "MEMBERS = ('native_conditional_flag_rank',)",
            '== 66': '== 37', 'the 66 actually scored mature cohort calibration schemes': 'the37 actually scored conditional native flag schemes'}),
        ('finalize_training_round100.py', 'finalize_training_round101.py', {
            'optimize_training_round100': 'optimize_training_round101', '== 66': '== 37',
            "['cohort_rank_calibration']": "['conditional_flag_rank']",
            "('weight', 'bins', 'pseudocount')": "('model', 'weight', 'first_year_slope')"}),
        ('run_extended_cohort_round100_full_registration_20261006.py', 'run_conditional_flag_round101_full_registration_20261006.py', {
            'register_extended_cohort_round100_artifacts_20261006': 'register_conditional_flag_round101_artifacts_20261006',
            'publish_extended_cohort_round100_full_validation_20261006': 'publish_conditional_flag_round101_full_validation_20261006',
            'lossless_ranking_runtime_adapter_v8_20261006': 'lossless_ranking_runtime_adapter_v9_20261006',
            'round100': 'round101', '_r100': '_r101', '(100,': '(101,',
            'official66_': 'official37_', "'existing_official_scores_registered': 66": "'existing_official_scores_registered': 37",
            '成熟标签的涨停分组单调排名校准': '成熟标签的原生涨停条件排名模型',
            'cohort_rank_calibration_causal_checks.json': 'conditional_flag_rank_causal_checks.json',
            '预定66项完整后处理官方比较': '预定37项完整条件模型官方比较'}),
        ('publish_extended_cohort_round100_full_validation_20261006.py', 'publish_conditional_flag_round101_full_validation_20261006.py', {
            'round100': 'round101', '_r100': '_r101', 'collect(100, 11, 66)': 'collect(101, 12, 37)',
            "'round': 100": "'round': 101",
            '== 66': '== 37', "'scored_records': 66": "'scored_records': 37",
            "'original_official_pilot_records_registered': 66": "'original_official_pilot_records_registered': 37",
            'lossless_ranking_display_qa_v11_20261006': 'lossless_ranking_display_qa_v12_20261006',
            'actual_complete_QA_version=11': 'actual_complete_QA_version=12', "'actual_full_QA_version': 11": "'actual_full_QA_version': 12",
            'actual_cohort100': 'actual_conditional101',
            'extended_cohort_rank_calibration_release_20261006': 'conditional_flag_rank_release_20261006',
            'extended_cohort_rank_calibration_official_pilot_20261006': 'conditional_flag_rank_official_comparison_v2_20261006',
            'frozen_before_actual_official_scores.json': 'frozen_before_actual_controls_and_official_scores.json',
            'extended_cohort_round100_registration_source_preparation_20261006': 'conditional_flag_round101_registration_source_preparation_20261006',
            'extended_cohort_rank_calibration_source_freeze_20261006': 'conditional_flag_rank_source_freeze_20261006',
            'extended_cohort_rank_calibration_full_controls_20261006': 'conditional_flag_rank_bank_v2_20261006',
            'extended_cohort_rank_calibration_20261006': 'conditional_flag_rank_20261006',
            'service_owned_workflows_20261006/extended_cohort_candidate_inference': 'service_owned_workflows_20261006/conditional_flag_rank_candidate_inference',
            '第100轮66项实际后处理验证': '第101轮37项实际原生条件模型验证',
            '既有66项官方评分': '既有37项官方评分', '第100轮目录': '第101轮目录'}),
        ('build_lossless_ranking_display_v9_20261006.py', 'build_lossless_ranking_display_v10_20261006.py', {'assert number == 100': 'assert number == 101'}),
        ('verify_lossless_ranking_display_v11_20261006.py', 'verify_lossless_ranking_display_v12_20261006.py', {
            'build_lossless_ranking_display_v9_20261006': 'build_lossless_ranking_display_v10_20261006',
            'lossless_ranking_display_qa_v11_20261006': 'lossless_ranking_display_qa_v12_20261006',
            'ranking_display_qa_v11_20261006': 'ranking_display_qa_v12_20261006'}),
        ('lossless_ranking_runtime_adapter_v8_20261006.py', 'lossless_ranking_runtime_adapter_v9_20261006.py', {
            'assert number == 100': 'assert number == 101',
            'build_lossless_ranking_display_v9_20261006': 'build_lossless_ranking_display_v10_20261006',
            'verify_lossless_ranking_display_v11_20261006': 'verify_lossless_ranking_display_v12_20261006',
            'lossless_ranking_display_qa_v11_20261006': 'lossless_ranking_display_qa_v12_20261006'})]
    pins, proofs = {}, []
    for old, new, changes in routes:
        source = A / old
        original = source.read_text(encoding='utf-8')
        text = original
        effective = {}
        for before in sorted(changes, key=len, reverse=True):
            if before in text:
                text = text.replace(before, changes[before])
                effective[before] = changes[before]
        if new == 'publish_conditional_flag_round101_full_validation_20261006.py':
            marker = '    for path in extra:\n'
            assert text.count(marker) == 1
            text = text.replace(marker,
                "    extra += list((A / 'conditional_flag_rank_bank_v2_20261006').glob('*/info_*.json'))\n"
                "    extra += [ROOT / 'candidates/conditional_flag_rank_20261006/conditional_native_replay_verification.json',\n"
                "        ROOT / 'candidates/conditional_flag_rank_20261006/cohort_curve_replay_verification.json']\n" + marker)
        if new.startswith(('build_lossless_', 'verify_lossless_', 'lossless_ranking_runtime_')):
            restored = text
            for before in sorted(effective, key=len, reverse=True):
                restored = restored.replace(effective[before], before)
            assert restored == original
        assert '15101600' not in text and 'neural17384' not in text
        compile(text, str(A / new), 'exec')
        with (A / new).open('x', encoding='utf-8') as stream:
            stream.write(text)
        pins.update({str(source): sha(source), str(A / new): sha(A / new)})
        proofs.append({'original': old, 'effective': new, 'explicit_changes': effective})
    registrar = A / 'register_conditional_flag_round101_artifacts_20261006.py'
    pins[str(registrar)] = sha(registrar)
    create(A / 'conditional_flag_round101_registration_source_preparation_20261006.json', {
        'status': 'prepared_complete_actual37_record_native14_round101_registration_and_full_QA',
        'input_sha256': pins, 'controls': proofs, 'all_original_six_views_and_browser_checks_preserved': True,
        'browser_timeout_seconds': 45, 'native_training_or_quality_scores_by_preparation': 0,
        'nested_manifests_covered_and_large_JSON_lossless_publication': True, 'test_labels_read': False})


if __name__ == '__main__':
    main()
