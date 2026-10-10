"""Refresh finite completed scopes and live open directions without altering science."""
from pathlib import Path
import re,sys,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis'
sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned

def main():
    import psutil
    out=A/'local_optimization_boundary_audit_v1_20261007';assert not out.exists();out.mkdir()
    inputs={}
    def evidence(path):
        path=Path(path);digest=sha(path);value=read(path);assert sha(path)==digest
        inputs[str(path.resolve())]=digest;return value
    completed=[]
    names={107:'round107_full_QA_receipt_closure_v2',108:'direct_rank92_round108_full_registration',109:'direct_rank_micro74_round109_full_registration',110:'CPU_MLP44_round110_full_registration'}
    for number,qa in [(107,18),(108,19),(109,20),(110,21)]:
        receipt=evidence(A/f'github_validation_sync_main_20261005/round{number}_receipt.json')
        closure=evidence(A/f'optimization_20261003_r{number}/full_registration_execution.json')
        scope=evidence(A/f'optimization_20261003_r{number}/provenance_scope_execution.json')
        browser=evidence(A/f'lossless_ranking_display_qa_v{qa}_20261007/round{number}/verification.json')
        service=A/'service_owned_workflows_20261006'/names[number]
        row=evidence(service/'native_launch.json');terminal=evidence(service/'service_execution.json')
        official=evidence(A/f'optimization_20261003_r{number}/calibrated_csv_official.json')
        assert not owned(row) and terminal['status']=='passed'
        assert closure['status']==scope['status']==official['status']=='passed'
        assert receipt['status']=='pushed_and_remote_head_verified' and receipt['branch']=='main'
        assert receipt['round']==number and receipt['actual_full_QA_version']==qa
        assert browser['status']=='passed_all_original_full_ranking_QA_and_lossless_browser_node_checks'
        assert browser['original_full_QA_result']['new_round_records']==receipt['scored_records']
        assert receipt['official_score']==official['metrics']['final_score']
        completed.append({'round':number,'scored_records':receipt['scored_records'],'selected_complete_score':receipt['official_score'],'main_commit':receipt['commit'],'actual_full_QA_version':qa,'closed_worker_pid':row['owned_worker_pid'],'finite_declared_grid_only':True})
    ready=evidence(A/'CPU_MLP_residual44_selected_release_20261007/selected_candidate_ready_for_registration.json')
    assert ready['all5635800_validation_raw_bits_and_all8_metrics_exact'] and ready['sealed_candidate_complete']
    assert ready['actual_rehashed_candidate_files']==2237 and ready['actual_saved_native_models']==15
    assert ready['new_inference_claimed'] is False
    best_candidate=Path(ready['source_candidate']);manifest=evidence(best_candidate/'manifest.json')
    assert sha(best_candidate/'manifest.json')==ready['manifest_sha256']
    native=evidence(best_candidate/'verification.json')
    assert native['status']=='passed' and (native['rows'],native['days'],native['codes'])==(1599600,344,4650)
    for k in ('model_reload_bit_identical','pipeline_replay_bit_identical','csv_replay_byte_identical','csv_ranks_unchanged','cold80_day_prefix_bit_identical'):
        assert native[k] is True,k
    mlp=evidence(A/'cpu_conditional_residual_mlp_bank20_20261007/verification.json')
    comparison=evidence(A/'conditional_residual_mlp44_official_comparison_20261007/verification.json')
    assert mlp['actual_native_fits']==20 and comparison['new_quality_score_records']==44
    assert comparison['all42_nonanchor_cases_have_actual_three_cold_prefix_controls']
    assert comparison['best']['connected_final_score']==ready['best']['connected_final_score']
    science={}
    service_names=('neural16384_annual','classifier_consensus_R90_root_resolution_recovery_v3','parent_rank_cache_alternating_benchmark','cpu_compact_conditional_residual_mlp_native_bank20','compact_conditional_residual_mlp44_official_comparison','CPU_COMPACT_MLP44_round111_full_registration','conditional_residual_hgb44_official_comparison','CPU_HGB44_round112_full_registration','cpu_full_universe_HGB_native_bank24','full_universe_HGB44_official_comparison_v2','CPU_FULL_HGB44_round113_full_registration_v2','cpu_full_universe_ElasticNet_native_bank24','full_universe_ElasticNet44_official_comparison','CPU_ELASTIC44_round114_full_registration')
    for name in service_names:
        folder=A/'service_owned_workflows_20261006'/name;row=evidence(folder/'native_launch.json')
        live=owned(row);terminal=evidence(folder/'service_execution.json') if (folder/'service_execution.json').exists() else None
        science[name]={'worker_pid':row['owned_worker_pid'],'owned_worker_creation_time':row['owned_worker_creation_time'],'strong_identity_owned_live_at_observation':live,'terminal_status':terminal['status'] if terminal else None,'console_handle':row['actual_native_console_handle']}
    partial90=[]
    for path in sorted((A/'optimization_20261003_r90').glob('wave*_results.json')):
        row=read(path);partial90.append({'file':path.name,'status':row['status'],'written_official_records':len(row['results'])})
    # Growing operational files are observations, not sealed static inputs.
    queue=read(A/'service_owned_dependency_queue_v4_20261006/state.json')
    families=[]
    for family,bank_name,score_name,declared in [('compact_MLP','cpu_compact_conditional_residual_mlp_bank20_20261007','compact_conditional_residual_mlp44_official_comparison_20261007',20),('conditional_HGB','cpu_conditional_residual_hgb_bank20_20261007','conditional_residual_hgb44_official_comparison_20261007',20),('full_pool_HGB','cpu_full_universe_HGB_bank24_20261007','full_universe_HGB44_official_comparison_v2_20261007',24),('ElasticNet','cpu_full_universe_ElasticNet_bank24_20261007','full_universe_ElasticNet44_official_comparison_20261007',24)]:
        bank=A/bank_name;proof=bank/'verification.json';verified=evidence(proof)['actual_native_fits'] if proof.exists() else len(list(bank.glob('*/info_*.json')))
        families.append({'family':family,'actual_verified_native_fits':verified,'declared_native_fits':declared,'actual_saved_native_fits_controls_pending':len(list(bank.glob('*/native_fit_completed_*.json'))),'actual_official_records':len(list((A/score_name).glob('case*_official.json'))),'declared_official_records':44,'full_future_candidate_and_QA_and_main_still_required':True})
    gpu=evidence(A/'neural16384_actual_shared_GPU_memory_boundary_evidence_20261006.json')
    assert gpu['global_resource_boundary_not_established'] is True
    log=A/'service_owned_workflows_20261006/neural16384_annual/stdout.log'
    with log.open('rb') as stream:
        stream.seek(max(0,log.stat().st_size-65536));tail=stream.read().decode('utf-8')
    epochs=re.findall(r'\[([^]]+)\] MLP y_rank epoch(\d+)/(\d+) mature-training loss=([^\s]+)',tail)
    resource={'available_RAM_GiB_at_observation':psutil.virtual_memory().available/2**30,'free_D_GiB_at_observation':psutil.disk_usage('D:/').free/2**30,'free_E_GiB_at_observation':psutil.disk_usage('E:/').free/2**30,'previous_actual_specific_GPU_evidence_at_local':gpu['at_local'],'previous_actual_specific_shared_GPU_memory_GiB':gpu['shared_system_memory_for_GPU_GiB'],'previous_actual_specific_dedicated_GPU_memory_GiB':gpu['dedicated_GPU_memory_GiB'],'GPU_specific_measurement_not_remeasured_this_audit':True,'last_observed_GPU_epoch':{'time_of_day':epochs[-1][0],'epoch':int(epochs[-1][1]),'required':int(epochs[-1][2])} if epochs else None}
    inputs[str(Path(__file__).resolve())]=sha(Path(__file__))
    for path,digest in inputs.items():assert sha(path)==digest,path
    report={'status':'verified_completed_recent_scopes_with_live_open_directions_not_global_exhaustion','at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'execution_mode':'single_host','remote_tasks_dispatched':0,'latest_complete_round':110,'selected_best_origin_round':106,'selected_complete_score':ready['best']['connected_final_score'],'full_board_last_verified_connected_records':11938,'completed_recent_declared_scopes':completed,'qualified_best_candidate':{'path':str(best_candidate),'manifest_sha256':ready['manifest_sha256'],'original_inference_freeze_timestamp':ready['original_inference_freeze_timestamp'],'rows':native['rows'],'days':native['days'],'codes':native['codes'],'native_models':ready['actual_saved_native_models'],'exact_reuse_candidate_files':2237,'no_new_inference_for_same_candidate':True},'MLP_declared_scope':{'actual_native_fits':20,'actual_official_records':44,'gain_over_best106':comparison['best']['score_gain_over_best106'],'actual_native_training_and_controls_seconds':mlp['elapsed_seconds'],'only_declared_four_configs_and_seven_heads_six_weights_not_all_MLPs':True},'actual_live_services':science,'R90_partial_written_waves_not_full_qualification':partial90,'R90_expected_records':138,'open_CPU_directions':families,'original_uncompleted_queue_names':queue['deferred_jobs_remaining'],'specific_resource_observation':resource,'global_resource_exhaustion_established':False,'all_feasible_optimization_directions_exhausted':False,'incomplete_work_remains':True,'scientific_processes_stopped_or_restarted':0,'test_labels_read':False,'input_sha256':inputs,'audit_rechecks_summary_and_closure_evidence_not_all2237_model_bytes_or_full5635800_again':True}
    create(out/'verification.json',report)
    text=(f"# 本机优化范围与资源证据\n\n截至 {report['at_local']}，最近完整闭合验证为第110轮，最佳方案来自第106轮，官方连接验证分数 {report['selected_complete_score']:.17g}。完整榜最近通过的记录数为11938。\n\n第110轮实际训练20个CPU条件残差MLP、评分44项方案；所声明范围没有超过第106轮。相同方案通过完整预测位值、八项评分、图和2237个封存文件核验后复用原推理，未重新定义冻结时间。\n\n当前仍有第90轮未闭合验证、小型MLP、条件HGB、全股票池HGB、ElasticNet，以及原大型神经网络和后续队列。已检查实际进程身份；这些工作尚未全部完成，不能据此宣布方法或计算资源已穷尽。\n\n既有GPU证据只表明16384宽度配置使用共享系统内存，本次未重测显存；D/E盘余量和当前RAM是现场观测，并非全局资源边界。测试标签未读取。\n\n本报告核对已保存的闭合与质量证据，没有再次重跑历史推理和全部模型文件核验。细节和来源SHA见同目录 verification.json。\n")
    (out/'运行范围说明.md').write_text(text,encoding='utf-8',newline='\n')
    print({'status':report['status'],'latest_complete_round':110,'R90_written_records':sum(v['written_official_records'] for v in partial90),'open_directions':len(families)})

if __name__=='__main__':main()
