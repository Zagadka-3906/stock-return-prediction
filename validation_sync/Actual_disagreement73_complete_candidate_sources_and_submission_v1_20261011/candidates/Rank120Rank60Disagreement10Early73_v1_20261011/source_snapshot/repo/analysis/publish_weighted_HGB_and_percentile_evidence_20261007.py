"""Publish prospective full115 pipeline controls, without claiming its future scientific completion."""
from pathlib import Path
import gzip
import hashlib
import sys
import time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis'
sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from handoff_joint_goss_round97_full_execution_20261006 import suspended_idle
from hidden_windows_child_creation_20261006 import install
import publish_classifier_consensus_workflows_20261006 as helpers


def closed(name):
    folder=A/'service_owned_workflows_20261006'/name
    while not (folder/'native_launch.json').exists() or owned(read(folder/'native_launch.json')):time.sleep(15)
    assert read(folder/'service_execution.json')['status']=='passed',name


def main():
    out=A/'weighted_HGB_and_percentile_controls_github_20261007';assert not out.exists();out.mkdir()
    # The bank publisher precedes us; score publication cannot start until all44 finish.
    closed('flagged_HGB88_round116_full_registration_v2')
    closed('weighted_flagged_HGB_native_hook_preflight_v2')
    closed('all_forecast_percentiles_full_scoring_benchmark')
    proof_path=A/'weighted_flagged_HGB_native_hook_preflight_v2_20261007/verification.json';proof=read(proof_path)
    assert proof['status']=='passed_actual28_historical603_weighted_HGB_unique_native_independent_and_whole_day_prefix_controls'
    for p,digest in proof['input_sha256'].items():assert sha(p)==digest,p
    benchmark=A/'all_forecast_percentiles_full_scoring_benchmark_20261007/verification.json';measured=read(benchmark)
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
    pins={str(p):sha(p) for p in dict.fromkeys(sources)}
    create(out/'frozen_before_main_publication.json',{'input_sha256':pins,'future_full117_qualification_not_claimed':True,'test_labels_read':False})
    from win32_read_handle_hash_cache_with_filename_v2_20261006 import LockedReadHashCache
    sync=helpers.sync;old_git=sync.git;held=[];retries=[];restore=install()
    def retry_git(*args,**kwargs):
        for attempt in range(3):
            try:return old_git(*args,**kwargs)
            except RuntimeError as error:
                if args[0] not in ('ls-remote','push','fetch') or not any(t in str(error).lower() for t in ('ssl','tls','connection','timed out','unable to access')):raise
                retries.append({'command':args[0],'attempt':attempt+1,'error':str(error)[:1000]})
                if attempt==2:raise
                time.sleep(2)
    sync.git=retry_git
    try:
        main7=read(A/'service_owned_workflows_20261006/main_publisher_v7/native_launch.json')
        parent,worker,idle=suspended_idle(main7,'    main (watch_validations_main_v7_20261006.py:71)');held.extend((worker,parent))
        with LockedReadHashCache(pins) as scope:
            prefix=Path('validation_sync/weighted_HGB_and_percentile_controls_20261007');payload={(prefix/'.gitattributes').as_posix():b'* -text\n'};files={}
            for p in dict.fromkeys([*sources,out/'frozen_before_main_publication.json']):
                data=p.read_bytes();assert not sync.SECRET.search(data),p
                digest=hashlib.sha256(data).hexdigest();target=(prefix/p.relative_to(ROOT)).as_posix()
                if len(data)>=5*1024**2:
                    data=gzip.compress(data,mtime=0);assert hashlib.sha256(gzip.decompress(data)).hexdigest()==digest;target+='.gz'
                payload[target]=data;files[p.relative_to(ROOT).as_posix()]={'published_path':target,'original_sha256':digest,'published_sha256':hashlib.sha256(data).hexdigest()}
            previous=sync.git('rev-parse','HEAD');helpers.verify_main(previous);assert not sync.git('status','--porcelain')
            payload[(prefix/'manifest.json').as_posix()]=sync.encoded({'status':'published_actual28_historical_native_hooks_and12_uncached_full_official_percentile_controls',
                'at_local':sync.now(),'files':files,'previous_main':previous,'only_branch':'main',
                'actual_historical_native_hook_cases':28,'historical_hook_rows':603,
                'actual_uncached_official_full_calls':12,'operator_only_speedup':read(A/'all_forecast_percentiles_benchmark_20261007/verification.json')['operator_only_speedup'],
                'actual_mapping_and_official_score_phase_speedup':measured['median_full_mapping_and_official_score_phase_speedup'],
                'new_distinct_model_selection_vectors_by_benchmark':0,'new_native_fits':0,
                'future340_scores_full337_controls_and_full117_QA28_not_claimed_complete':True,
                'original_failed_native_diagnostic_and116_source_route_failures_preserved':True,
                'scientific_workers_stopped_suspended_or_restarted':0,'test_labels_read':False})
            payload[(prefix/'README.md').as_posix()]=('# 本机非等权HGB推理诊断和完整评分提速证据\n\n'
                '28个3:1、2:1:1等有序四项均值组合在603行历史特征、合成日期上通过真实原生重载、独立数值树解码、Pandas同日CDF和完整日期前缀。'
                '同一模型只保存和核验一次；四项求和可以重复使用同一模型输出。此诊断不代替完整父图和未来1599600行验证。'
                '337项完整5635800行控制等待116完整QA27后运行；340项官方评分和117完整资格仍未完成。\n\n'
                '收益率映射的全部当日百分位保留无效价格预测哨兵，三条完整向量及九个冷前缀逐位相同。'
                '另对已评分的三个向量按两种相反顺序完成12次不读取评分胶囊缓存的真实官方评分：映射数组、CSV字节和八项指标完全一致。'
                '分别报告单算子和完整映射/评分阶段的实测加速，未测量整项任务加速。原评分脚本与本机GPU训练不改动。'
                '保留变量遮蔽和源码路径错误的真实失败记录及恢复来源，不伪造成功状态。\n').encode('utf8')
            scope.reverify()
            for name,data in payload.items():sync.atomic(sync.WORKTREE/name,data)
            names=sorted(payload)
            for offset in range(0,len(names),50):sync.git('add','-f','--',*names[offset:offset+50])
            assert set(sync.git('-c','core.quotepath=false','diff','--cached','--name-only').splitlines())<=set(payload)
            sync.git('-c','maintenance.auto=false','-c','gc.auto=0','commit','-m','登记28项非等权HGB原生诊断与12次完整官方评分提速验证',timeout=180)
            commit=sync.git('rev-parse','HEAD');hashes={n:hashlib.sha256(data).hexdigest() for n,data in payload.items()}
            assert helpers.blob_hashes(commit,hashes)==hashes
            sync.git('push','origin','HEAD:refs/heads/main',timeout=180);helpers.verify_main(commit);helpers.watcher.advance_source_index(commit);scope.reverify()
            create(out/'receipt.json',{'status':'pushed_and_remote_head_verified','commit':commit,'at_local':sync.now(),'branch':'main',
                'raw_git_blobs_verified':len(hashes),'new_quality_scores':0,'all_source_inputs_initial_and_final_read_locked_full_rehash':True,
                'url':'https://github.com/Zagadka-3906/stock-return-prediction/tree/main/'+prefix.as_posix()})
    finally:
        sync.git=old_git
        for p in reversed(held):
            if p.is_running():p.resume()
        create(out/'actual_hidden_publication_children.json',{'events':restore()})
        create(out/'transport_retries.json',{'attempts':retries,'TLS_verification_unchanged':True})


if __name__=='__main__':main()
