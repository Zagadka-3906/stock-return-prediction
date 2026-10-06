"""Predeclare a smaller-amplitude CDF grid and admit measured exact official acceleration."""
from pathlib import Path
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path[:0] = [str(ROOT), str(A)]
from run_dependency_queue_v3_20261006 import read, create, sha


def main():
    plan_path = A / 'single_host_direct_flag_rank_micro74_plan_20261007.json'
    script = A / 'run_direct_flag_rank_micro74_official_comparison_20261007.py'
    pub = A / 'publish_single_host_rank_micro74_evidence_20261007.py'
    admission = A / 'single_host_rank_micro74_source_admission_20261007.json'
    assert all(not p.exists() for p in (plan_path, script, pub, admission))
    prior_path = A / 'direct_flag_rank92_official_comparison_20261007/verification.json'
    prior = read(prior_path)
    assert prior['status'] == 'passed_actual92_direct_rank_CDF_full_official_comparisons'
    assert len(prior['records']) == 92 and prior['best']['case'] == 1
    benchmark_path = A / 'official_date_index_speed_benchmark_20261007/verification.json'
    benchmark = read(benchmark_path)
    assert benchmark['status'] == 'passed_actual_full_official_date_index_equivalence_and_benchmark'
    assert benchmark['all8_metrics_bit_identical_each_actual_comparison']
    assert benchmark['all1212_date_index_row_orders_exact_original_masks']
    for p, digest in benchmark['input_sha256'].items():
        assert sha(p) == digest
    plan = read(A / 'single_host_direct_flag_rank_plan_20261007.json')
    plan.update(status='frozen_local_only74_micro_amplitude_official_cases_before_execution',
        at_local=time.strftime('%Y-%m-%dT%H:%M:%S'), fixed_amplitudes=[.005, .01, .025, .05],
        prospective_native_fits=0, existing_native_bank_fits=36, prospective_official_cases=74,
        prior_completed_full_official_comparison=str(prior_path), prior_completed_full_official_comparison_sha256=sha(prior_path),
        reason='Extend the untested interval below previous minimum0.1 after all92 prior cases failed to improve. This grid is adaptive training-internal search, with multiple-selection risk disclosed.',
        fixed_74_cases_before_any_new_score=True, only_original_complete_official_S_selects=True,
        date_index_acceleration_actual_proof=str(benchmark_path), date_index_acceleration_proof_sha256=sha(benchmark_path),
        requires_round108_full_QA_main_closed_before_scoring=True,
        original_evaluate_py_bytes_and_every_sort_filter_formula_unchanged=True,
        measured_official_phase_speedup=benchmark['median_full_official_evaluation_speedup'],
        total_goal_speedup_not_claimed=True, compute_mode='single_host_CPU_original_GPU_worker_preserved')
    create(plan_path, plan)
    original_script = A / 'run_direct_flag_rank92_official_comparison_20261007.py'
    text = original_script.read_text(encoding='utf-8')
    for before, after in {
        'direct_flag_rank92_official_comparison_20261007': 'direct_flag_rank_micro74_official_comparison_20261007',
        'single_host_direct_flag_rank_plan_20261007': 'single_host_direct_flag_rank_micro74_plan_20261007',
        'Compare92': 'Compare74', 'all92': 'all74', 'len(cases) == 92': 'len(cases) == 74',
        "'expected_cases': 92": "'expected_cases': 74", "'new_quality_score_records': 92": "'new_quality_score_records': 74",
        'passed_actual92_direct_rank_CDF_full_official_comparisons': 'passed_actual74_micro_amplitude_direct_rank_CDF_full_official_comparisons',
        'all90_nonanchor_cases': 'all72_nonanchor_cases', 'actual_complete92': 'actual_complete74',
    }.items():
        text = text.replace(before, after)
    text = text.replace('    bank = read(BANK', "    completed = A / 'service_owned_workflows_20261006/direct_rank92_round108_full_registration'\n    while not (completed / 'native_launch.json').exists() or owned(read(completed / 'native_launch.json')):\n        time.sleep(15)\n    assert read(completed / 'service_execution.json')['status'] == 'passed'\n    assert read(A / 'optimization_20261003_r108/full_registration_execution.json')['status'] == 'passed'\n    assert read(A / 'github_validation_sync_main_20261005/round108_receipt.json')['actual_full_QA_version'] == 19\n    bank = read(BANK", 1)
    text = text.replace("    pins = {**bank['input_sha256']", "    sources += [A / 'official_date_index_dataframe_adapter_20261007.py', A / 'official_date_index_speed_benchmark_20261007/verification.json', A / 'single_host_rank_micro74_source_admission_20261007.json', A / 'prepare_direct_rank_micro74_20261007.py', A / 'optimization_20261003_r108/full_registration_execution.json', A / 'github_validation_sync_main_20261005/round108_receipt.json']\n    pins = {**bank['input_sha256']", 1)
    text = text.replace('            metrics = score(ctx, values)', "            from official_date_index_dataframe_adapter_20261007 import installed\n            with installed(scoring / 'submission.csv') as actual_date_index:\n                metrics = score(ctx, values)\n            assert actual_date_index['date_index_lookups'] in (0, 1212)", 1)
    text = text.replace("'official_score_cache': ctx.last_official_score_cache", "'official_date_index_runtime': dict(actual_date_index), 'official_score_cache': ctx.last_official_score_cache")
    compile(text, str(script), 'exec')
    with script.open('x', encoding='utf-8', newline='\n') as f:
        f.write(text)
    original_pub = A / 'publish_single_host_rank36_evidence_20261007.py'
    text = original_pub.read_text(encoding='utf-8')
    for before, after in {
        'direct_flag_rank92_official_comparison': 'direct_flag_rank_micro74_official_comparison',
        'passed_actual92_direct_rank_CDF_full_official_comparisons': 'passed_actual74_micro_amplitude_direct_rank_CDF_full_official_comparisons',
        '== 92': '== 74', 'else 92': 'else 74',
        "f'single_host_rank36_{phase}_github_20261007'": "f'single_host_rank_micro74_{phase}_github_20261007'",
        "f'validation_sync/single_host_rank36_{phase}_20261007'": "f'validation_sync/single_host_rank_micro74_{phase}_20261007'",
    }.items():
        text = text.replace(before, after)
    text = text.replace("    assert phase in ('bank', 'scores')", "    assert phase == 'scores'")
    text = text.replace("    if phase == 'scores':\n        sources +=", "    sources += [A / 'official_date_index_dataframe_adapter_20261007.py', A / 'benchmark_official_date_index_speed_20261007.py', A / 'single_host_direct_flag_rank_micro74_plan_20261007.json', A / 'single_host_rank_micro74_source_admission_20261007.json', A / 'prepare_direct_rank_micro74_20261007.py', *list((A / 'official_date_index_speed_benchmark_20261007').glob('*.json'))]\n    if phase == 'scores':\n        sources +=", 1)
    text = text.replace("'# 本机加速与直接排名模型\\n\\n'", "'# 本机加速与74项小幅CDF融合验证\\n\\n'\n            '本轮在先前92项验证完成后，预先固定0.005/0.01/0.025/0.05四种新权重；这属于训练内部的自适应扩展，存在反复选模偏差。'\n            '复用已完成的36个真实模型，不新增拟合。官方代码不修改；索引适配只加速同日行提取，全部8项指标逐位一致的实际基准随记录保留。\\n\\n'")
    compile(text, str(pub), 'exec')
    with pub.open('x', encoding='utf-8', newline='\n') as f:
        f.write(text)
    sources = [Path(__file__), original_script, original_pub, plan_path, script, pub, prior_path,
        benchmark_path, A / 'official_date_index_dataframe_adapter_20261007.py']
    create(admission, {'status': 'passed_actual_prespecified74_micro_grid_and_exact_official_speed_admission',
        'at_local': time.strftime('%Y-%m-%dT%H:%M:%S'), 'input_sha256': {str(p): sha(p) for p in sources},
        'actual_new_native_fits': 0, 'new_scores_by_preparation': 0, 'expected_official_cases': 74,
        'original_all_same_day_bit_identity_and_full_80_260_975_prefix_controls_retained': True,
        'all_scoring_waits_for_actual_full108_qualification_main_and_closed_service': True,
        'test_labels_read': False, 'global_exhaustion_not_claimed': True})


if __name__ == '__main__':
    main()
