"""Publish actual28 native diagnostics and12 fresh scoring controls after full116, on main only."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis'
sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from handoff_ready_goss_full_execution_20261006 import start_service

def main():
    source=A/'publish_protected_upper_pool_HGB66_candidate_pipeline_20261007.py';target=A/'publish_weighted_HGB_and_percentile_evidence_20261007.py';assert not target.exists()
    text=source.read_text(encoding='utf8')
    text=text.replace('protected_upper_pool_HGB66_candidate_pipeline_github_20261007','weighted_HGB_and_percentile_controls_github_20261007')
    text=text.replace("closed('local_closed_dependency_recovery_v2_main_publication')","closed('flagged_HGB88_round116_full_registration_v2')")
    text=text.replace("closed('cpu_full_universe_ElasticNet24_bank_evidence_publication_v4')","closed('weighted_flagged_HGB_native_hook_preflight_v2')\n    closed('all_forecast_percentiles_full_scoring_benchmark')")
    text=text.replace('protected_upper_pool_HGB66_candidate_source_admission_20261007.json','weighted_flagged_HGB_native_hook_preflight_v2_20261007/verification.json')
    text=text.replace('passed_actual_native_hook_and24_prospective_source_AST_hashes_schema_and_parent_baseline_controls','passed_actual28_historical603_weighted_HGB_unique_native_independent_and_whole_day_prefix_controls')
    start=text.index('    sources=[Path(__file__),proof_path');end=text.index('    pins={str(p):sha(p)',start)
    replacement="""    benchmark=A/'all_forecast_percentiles_full_scoring_benchmark_20261007/verification.json';measured=read(benchmark)
    assert measured['status']=='passed_actual12_uncached_full_official_calls_all_mapped_bits_CSV_bytes_eight_metrics_and_two_orders'
    assert len(proof['records'])==28 and measured['actual_uncached_official_evaluation_calls']==12
    sources=[Path(__file__),A/'prepare_weighted_HGB_and_percentile_evidence_publication_20261007.py',proof_path,benchmark,
        A/'prepare_flagged_HGB_weighted_quarters340_plan_20261007.py',A/'flagged_HGB_weighted_quarters340_plan_20261007.json',
        A/'prepare_weighted_flagged_HGB_native_hook_20261007.py',A/'weighted_flagged_HGB_native_hook_source_preparation_20261007.json',
        A/'verify_weighted_flagged_HGB_native_hook_20261007.py',A/'verify_weighted_flagged_HGB_native_hook_v2_20261007.py',
        A/'predict_flagged_CPU_HGB_weighted_quarters_scheme_20261007.py',A/'predict_flagged_CPU_HGB_weighted_quarters_scheme_v2_20261007.py',
        A/'predict_lower_pool_after_weighted_flagged_CPU_HGB_scheme_20261007.py',A/'predict_lower_pool_after_weighted_flagged_CPU_HGB_scheme_v2_20261007.py',
        A/'recover_weighted_flagged_HGB_native_hook_v2_20261007.py',A/'weighted_flagged_HGB_native_hook_recovery_v2_actual_launch_20261007.json',
        A/'prepare_weighted_flagged_HGB_full337_controls_20261007.py',A/'verify_flagged_HGB_weighted_quarters340_transform_20261007.py',
        A/'run_weighted_flagged_HGB_controls_after116_20261007.py',A/'run_weighted_flagged_HGB_controls_after116_v2_20261007.py',A/'run_weighted_flagged_HGB_controls_after116_v3_20261007.py',
        A/'weighted_flagged_HGB_controls_actual_hidden_launches_20261007.json',A/'weighted_flagged_HGB_full337_actual_source_route_recovery_v3_20261007.json',
        A/'exact_numpy_all_forecast_percentiles_20261007.py',A/'benchmark_all_forecast_percentiles_20261007.py',
        A/'benchmark_all_forecast_percentiles_full_scoring_20261007.py',A/'all_forecast_percentile_runtime_20261007.py',
        *list((A/'all_forecast_percentiles_benchmark_20261007').glob('*.json')),*list((A/'all_forecast_percentiles_full_scoring_benchmark_20261007').glob('*.json')),
        A/'prepare_weighted_flagged_HGB340_workflows_20261007.py',A/'prepare_weighted_flagged_HGB340_workflows_v2_20261007.py',
        A/'weighted_flagged_HGB340_workflow_source_preparation_20261007.json',A/'weighted_flagged_HGB340_workflow_source_preparation_v2_20261007.json',
        *map(Path,read(A/'weighted_flagged_HGB340_workflow_source_preparation_v2_20261007.json')['input_sha256']),
        A/'github_validation_sync_main_20261005/round116_receipt.json',A/'optimization_20261003_r116/full_registration_execution.json',
        A/'flagged_HGB88_round116_actual_source_path_preflight_v2_20261007.json',A/'recover_flagged_HGB88_round116_source_paths_v2_20261007.py',
        A/'flagged_HGB88_round116_source_path_recovery_actual_launch_v2_20261007.json']
    for name in ('weighted_flagged_HGB_native_hook_preflight','weighted_flagged_HGB_native_hook_preflight_v2',
        'all_forecast_percentiles_full_benchmark','all_forecast_percentiles_full_scoring_benchmark',
        'flagged_HGB88_round116_full_registration','flagged_HGB88_round116_full_registration_v2',
        'weighted_flagged_HGB_full337_transform_preflight','weighted_flagged_HGB_full337_transform_preflight_v2','weighted_flagged_HGB_full337_transform_preflight_v3'):
        folder=A/'service_owned_workflows_20261006'/name
        sources += [folder/n for n in ('job_definition.json','native_launch.json')]
        if not owned(read(folder/'native_launch.json')):sources += list(folder.glob('*.json'))+list(folder.glob('*.log'))
"""
    text=text[:start]+replacement+text[end:]
    text=text.replace('validation_sync/protected_upper_pool_HGB66_candidate_pipeline_20261007','validation_sync/weighted_HGB_and_percentile_controls_20261007')
    start=text.index("            payload[(prefix/'manifest.json').as_posix()]=sync.encoded(");end=text.index('            scope.reverify()',start)
    replacement="""            payload[(prefix/'manifest.json').as_posix()]=sync.encoded({'status':'published_actual28_historical_native_hooks_and12_uncached_full_official_percentile_controls',
                'at_local':sync.now(),'files':files,'previous_main':previous,'only_branch':'main',
                'actual_historical_native_hook_cases':28,'historical_hook_rows':603,
                'actual_uncached_official_full_calls':12,'operator_only_speedup':read(A/'all_forecast_percentiles_benchmark_20261007/verification.json')['operator_only_speedup'],
                'actual_mapping_and_official_score_phase_speedup':measured['median_full_mapping_and_official_score_phase_speedup'],
                'new_distinct_model_selection_vectors_by_benchmark':0,'new_native_fits':0,
                'future340_scores_full337_controls_and_full117_QA28_not_claimed_complete':True,
                'original_failed_native_diagnostic_and116_source_route_failures_preserved':True,
                'scientific_workers_stopped_suspended_or_restarted':0,'test_labels_read':False})
            payload[(prefix/'README.md').as_posix()]=('# 本机非等权HGB推理诊断和完整评分提速证据\\n\\n'
                '28个3:1、2:1:1等有序四项均值组合在603行历史特征、合成日期上通过真实原生重载、独立数值树解码、Pandas同日CDF和完整日期前缀。'
                '同一模型只保存和核验一次；四项求和可以重复使用同一模型输出。此诊断不代替完整父图和未来1599600行验证。'
                '337项完整5635800行控制等待116完整QA27后运行；340项官方评分和117完整资格仍未完成。\\n\\n'
                '收益率映射的全部当日百分位保留无效价格预测哨兵，三条完整向量及九个冷前缀逐位相同。'
                '另对已评分的三个向量按两种相反顺序完成12次不读取评分胶囊缓存的真实官方评分：映射数组、CSV字节和八项指标完全一致。'
                '分别报告单算子和完整映射/评分阶段的实测加速，未测量整项任务加速。原评分脚本与本机GPU训练不改动。'
                '保留变量遮蔽和源码路径错误的真实失败记录及恢复来源，不伪造成功状态。\\n').encode('utf8')
"""
    text=text[:start]+replacement+text[end:]
    text=text.replace('登记低分区HGB候选冻结封存及完整115流程的24源码9项基准回归','登记28项非等权HGB原生诊断与12次完整官方评分提速验证')
    text=text.replace('future_full115_qualification_not_claimed','future_full117_qualification_not_claimed')
    compile(text,str(target),'exec')
    with target.open('x',encoding='utf8',newline='\n') as stream:stream.write(text)
    pins={str(p):sha(p) for p in (Path(__file__),source,target,A/'all_forecast_percentiles_full_scoring_benchmark_20261007/verification.json')}
    row=start_service('weighted_HGB_and_percentile_controls_main_publication',target.name,[],pins)
    create(A/'weighted_HGB_and_percentile_controls_publication_actual_launch_20261007.json',{'input_sha256':pins,'actual_native_launch':row,'new_quality_scores':0})
    print({'status':'launched_control_publication','pid':row['owned_worker_pid']},flush=True)

if __name__=='__main__':main()
