"""Verify recent finite scopes, selected sealed files, and actual remaining local work."""
from pathlib import Path
import sys,time,hashlib,re
ROOT=Path(__file__).resolve().parents[1]; A=ROOT/'analysis'
sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned

def main():
    import psutil
    out=A/'local_optimization_boundary_audit_v2_20261007';assert not out.exists();out.mkdir()
    inputs={};started=time.strftime('%Y-%m-%dT%H:%M:%S')
    def evidence(path):
        path=Path(path).resolve();digest=sha(path);value=read(path);assert sha(path)==digest
        inputs[str(path)]=digest;return value
    names={107:'round107_full_QA_receipt_closure_v2',108:'direct_rank92_round108_full_registration',109:'direct_rank_micro74_round109_full_registration',
        110:'CPU_MLP44_round110_full_registration',111:'CPU_COMPACT_MLP44_round111_full_registration',112:'CPU_HGB44_round112_full_registration_v2',
        113:'CPU_FULL_HGB44_round113_full_registration_v4',114:'CPU_ELASTIC44_round114_full_registration_v3',115:'protected_upper_pool_HGB66_round115_full_registration_v5',
        116:'flagged_HGB88_round116_full_registration_v2',117:'weighted_HGB340_round117_full_registration_v2',118:'HGB_quarter_numeric28_round118_full_registration_v5',
        119:'quantile_HGB88_round119_full_registration_v6',120:'nonflag_HGB40_round120_full_registration_v4',121:'nonflag_Ridge40_round121_full_registration_v1'}
    completed=[]; observations={}
    for number,name in names.items():
        service=A/'service_owned_workflows_20261006'/name
        if not (service/'native_launch.json').exists():observations[name]={'status':'not_launched'};continue
        identity=evidence(service/'native_launch.json'); live=owned(identity)
        terminal=evidence(service/'service_execution.json') if (service/'service_execution.json').exists() else None
        observations[name]={'strong_identity_owned_live_at_observation':live,'pid':identity['owned_worker_pid'],'birth':identity['owned_worker_creation_time'],'terminal':terminal}
        folder=A/f'optimization_20261003_r{number}'; receipt_path=A/f'github_validation_sync_main_20261005/round{number}_receipt.json'
        if live or not terminal or terminal['status']!='passed' or not receipt_path.exists() or not (folder/'full_registration_execution.json').exists():continue
        qa=number-89; receipt=evidence(receipt_path); closure=evidence(folder/'full_registration_execution.json'); scope=evidence(folder/'provenance_scope_execution.json')
        official=evidence(folder/'calibrated_csv_official.json'); browser=evidence(A/f'lossless_ranking_display_qa_v{qa}_20261007/round{number}/verification.json')
        assert closure['status']==scope['status']==official['status']=='passed'
        assert receipt['status']=='pushed_and_remote_head_verified' and receipt['branch']=='main' and receipt['round']==number and receipt['actual_full_QA_version']==qa
        assert browser['status']=='passed_all_original_full_ranking_QA_and_lossless_browser_node_checks'
        assert browser['original_full_QA_result']['new_round_records']==receipt['scored_records']
        assert receipt['official_score']==official['metrics']['final_score']
        selection=evidence(folder/'selection.json')
        completed.append({'round':number,'scored_records':receipt['scored_records'],'selected_complete_score':receipt['official_score'],
            'main_commit':receipt['commit'],'actual_full_QA_version':qa,'continuous_board_records':receipt['connected_records'],
            'original_frozen_at_local':selection['frozen_at_local'],'finite_declared_grid_only':True})
    assert {r['round'] for r in completed}>=set(range(107,119))
    best=min(completed,key=lambda r:(-r['selected_complete_score'],r['round']));latest=max(completed,key=lambda r:r['round'])
    candidate=ROOT/f"candidates/optimization_20261003_r{best['round']}"
    manifest=evidence(candidate/'manifest.json'); prediction=evidence(candidate/'verification.json'); selection=evidence(candidate/'selection.json')
    assert prediction['status']=='passed' and (prediction['rows'],prediction['days'],prediction['codes'])==(1599600,344,4650)
    assert prediction['whole_scheme_graph']==selection['winner']['conditional_flag_residual_scheme_graph']
    for k in ('model_reload_bit_identical','pipeline_replay_bit_identical','csv_replay_byte_identical','cold80_day_prefix_bit_identical'):assert prediction[k]
    hashes={};checked=0;total_bytes=0
    for relative,info in manifest['files'].items():
        path=(candidate/relative).resolve();assert path.is_relative_to(candidate.resolve()) and path.is_file()
        st=path.stat();key=(st.st_dev,st.st_ino,st.st_size,st.st_mtime_ns)
        if key not in hashes:hashes[key]=sha(path)
        assert hashes[key]==info['sha256'],relative
        checked+=1;total_bytes+=st.st_size
    assert sha(candidate/'submission.csv')==prediction['csv_sha256']
    families=[]
    configs=[('CPU_MLP',110,'cpu_conditional_residual_mlp_bank20_20261007','conditional_residual_mlp44_official_comparison_20261007',20,44),
        ('compact_CPU_MLP',111,'cpu_compact_conditional_residual_mlp_bank20_20261007','compact_conditional_residual_mlp44_official_comparison_20261007',20,44),
        ('flag_HGB',112,'cpu_conditional_residual_hgb_bank20_20261007','conditional_residual_hgb44_official_comparison_20261007',20,44),
        ('full_pool_HGB',113,'cpu_full_universe_HGB_bank24_recovery_v2_20261007','full_universe_HGB44_official_comparison_v3_20261007',24,44),
        ('full_pool_ElasticNet',114,'cpu_full_universe_ElasticNet_bank24_recovery_v3_20261007','full_universe_ElasticNet44_official_comparison_v3_20261007',24,44),
        ('flag_quantile_HGB',119,'quantile_HGB_native_bank20_v2_20261007','quantile_HGB88_official_comparison_v6_20261007',20,88),
        ('nonflag_HGB',120,'nonflag_residual_HGB_bank10_20261007','nonflag_HGB40_official_comparison_v4_20261007',10,40),
        ('nonflag_Ridge',121,'nonflag_residual_Ridge_bank10_20261007','nonflag_Ridge40_official_comparison_v1_20261007',10,40)]
    closed_numbers={r['round'] for r in completed}
    for family,number,bank_name,score_name,fits,expected in configs:
        bank=evidence(A/bank_name/'verification.json');assert bank['actual_native_fits']==fits
        score=A/score_name/'verification.json';count=len(list((A/score_name).glob('case*_official.json')))
        item={'family':family,'round':number,'declared_native_fits':fits,'actual_verified_native_fits':fits,'expected_official_cases':expected,
            'actual_written_official_cases_at_observation':count,'full_round_qualified':number in closed_numbers,'finite_scope_only':True}
        if score.exists():
            scored=evidence(score);assert len(scored['records'])==expected
            item.update(actual_finished_official_cases=expected,actual_best_score=scored['best']['connected_final_score'],actual_best_configuration=scored['best']['configuration'])
        families.append(item)
    for name in ('neural16384_annual','dependency_queue_v12_local_cache','nonflag_residual_Ridge_actual_hooks_and_main_after120','nonflag_Ridge40_round121_source_admission_v1','nonflag_Ridge40_continue_after_actual_admission'):
        folder=A/'service_owned_workflows_20261006'/name;identity=evidence(folder/'native_launch.json'); terminal=evidence(folder/'service_execution.json') if (folder/'service_execution.json').exists() else None
        observations[name]={'strong_identity_owned_live_at_observation':owned(identity),'pid':identity['owned_worker_pid'],'birth':identity['owned_worker_creation_time'],'terminal':terminal}
    queue=read(A/'service_owned_dependency_queue_v4_20261006/state.json')
    gpu=evidence(A/'neural16384_actual_shared_GPU_memory_boundary_evidence_20261006.json'); assert gpu['global_resource_boundary_not_established']
    log=A/'service_owned_workflows_20261006/neural16384_annual/stdout.log'
    with log.open('rb') as stream:stream.seek(max(0,log.stat().st_size-65536));tail=stream.read().decode('utf8')
    epochs=re.findall(r'\[([^]]+)\] MLP y_rank epoch(\d+)/(\d+) mature-training loss=([^\s]+)',tail)
    resource={'available_RAM_GiB_at_observation':psutil.virtual_memory().available/2**30,'free_D_GiB_at_observation':psutil.disk_usage('D:/').free/2**30,
        'free_E_GiB_at_observation':psutil.disk_usage('E:/').free/2**30,'previous_GPU_shared_GiB':gpu['shared_system_memory_for_GPU_GiB'],
        'previous_GPU_dedicated_GiB':gpu['dedicated_GPU_memory_GiB'],'previous_GPU_observation_at_local':gpu['at_local'],
        'GPU_memory_not_remeasured_this_audit':True,'last_logged_original_GPU_epoch':{'time_of_day':epochs[-1][0],'epoch':int(epochs[-1][1]),'required':int(epochs[-1][2])} if epochs else None}
    inputs[str(Path(__file__).resolve())]=sha(__file__)
    for path,digest in inputs.items():assert sha(path)==digest,path
    report={'status':'verified_recent_closed_scopes_selected_sealed_files_and_live_open_directions_not_global_exhaustion',
        'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'started_at_local':started,'execution_mode':'single_host','remote_tasks_dispatched':0,
        'latest_complete_round':latest['round'],'selected_best_origin_round':best['round'],'selected_complete_score':best['selected_complete_score'],
        'full_board_last_verified_connected_records':latest['continuous_board_records'],'completed_recent_declared_scopes':completed,
        'qualified_best_candidate':{'path':str(candidate),'manifest_sha256':sha(candidate/'manifest.json'),'original_freeze_at_local':selection['frozen_at_local'],
            'native_models':len(prediction['models']),'actual_rehashed_sealed_files':checked,'actual_unique_file_objects_hashed':len(hashes),'sealed_logical_bytes':total_bytes,
            'all_actual_source_model_submission_and_proof_bytes_match_manifest':True,'previous_complete_replays_and_cold80_rechecked_not_rerun':True},
        'native_and_complete_scheme_families':families,'actual_services_at_observation':observations,'original_uncompleted_queue_names_at_observation':queue['deferred_jobs_remaining'],
        'specific_resource_observation':resource,'global_resource_exhaustion_established':False,'all_feasible_optimization_directions_exhausted':False,
        'incomplete_work_remains':True,'scientific_processes_stopped_or_restarted':0,'new_native_fits':0,'new_quality_scores':0,'test_labels_read':False,'input_sha256':inputs}
    create(out/'verification.json',report)
    text=(f"# 本机优化范围与资源证据\n\n截至 {report['at_local']}，最近完整闭合为第{latest['round']}轮，最佳合格方案来自第{best['round']}轮，连接验证官方分 {best['selected_complete_score']:.17g}。完整榜已核对 {latest['continuous_board_records']} 条记录。\n\n"
        f"本次实际重哈希最佳候选 {checked} 个封存文件，模型、提交、源码和已有完整重放证明一致。所有107轮以后已闭合轮次均核对原生服务结束、来源锁定、六视图完整QA和main回执。\n\n"
        "8个近期模型族的实际年度拟合与官方比较见 verification.json。已完成有限网格只能证明对应范围的结果；原大型网络、后续原队列、119—121完整候选与新比较仍须按实际状态推进。\n\n"
        "GPU显存数据引用先前实测，本次没有重测显存。RAM和D/E余量是当前观测；尚无全局资源或优化穷尽证据。真实测试标签未读取，当前冻结提交未替换。\n")
    (out/'运行范围说明.md').write_text(text,encoding='utf8',newline='\n')
    print({'status':report['status'],'latest':latest['round'],'best':best['round'],'sealed_files_rehashed':checked,'recent_closed_scopes':len(completed)},flush=True)
if __name__=='__main__':main()
