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
    out=A/'HGB88_complete_pipeline_github_20261007';assert not out.exists();out.mkdir()
    # The bank publisher precedes us; score publication cannot start until all44 finish.
    closed('protected_upper_pool_HGB66_round115_full_registration_v5')
    closed('local_only_progress_monitor_v12_handoff')
    proof_path=A/'flagged_HGB88_round116_source_admission_20261007.json';proof=read(proof_path)
    assert proof['status']=='passed_actual85_full_controls_and24_prospective116_source_schema_baseline_and_ablation_routes'
    for p,digest in proof['input_sha256'].items():assert sha(p)==digest,p
    prepared=read(A/'flagged_HGB88_complete_pipeline_preparation_v4_20261007.json')
    sources=[Path(__file__),A/'prepare_HGB88_complete_pipeline_main_publication_20261007.py',proof_path,*map(Path,proof['input_sha256']),*map(Path,prepared['input_sha256']),
        A/'flagged_HGB88_complete_pipeline_preparation_v4_20261007.json',A/'flagged_HGB88_complete_pipeline_actual_hidden_launches_v4_20261007.json',
        A/'prepare_flagged_HGB88_pipeline_complete_v4_20261007.py',A/'prepare_local_monitor12_and_HGB88_launch_20261007.py',
        A/'monitor_local_only_runtime_v12_20261007.py',A/'handoff_local_only_monitor_v12_20261007.py',
        *list((A/'local_only_monitor_v12_actual_handoff_20261007').glob('*.json')),
        A/'flagged_HGB_small_amplitude88_controls_github_20261007/receipt.json',
        A/'CPU_full_bank_resource_observer_ElasticNet_v4_github_20261007/receipt.json',
        A/'github_validation_sync_main_20261005/round115_receipt.json',
        A/'optimization_20261003_r115/full_registration_execution.json',A/'optimization_20261003_r115/provenance_scope_execution.json',
        *list(A.glob('protected_upper_pool_HGB66_round115*recovery*20261007.json')),
        A/'protected_upper_pool_HGB66_round115_inherited_registry_alias_relocation_20261007.json',
        A/'local115_alias_and116_dependency_recovery_admission_20261007.json',A/'local115_alias_and116_dependency_recovery_actual_hidden_launches_20261007.json',
        A/'flagged_HGB88_dependency_routes_v3_admission_20261007.json',
        A/'flagged_HGB88_round116_pipeline_preparation_prototype_failure_20261007.json']
    names=[job['name'] for job in prepared['jobs']]+['protected_upper_pool_HGB66_round115_full_registration',
        'protected_upper_pool_HGB66_round115_full_registration_v2','protected_upper_pool_HGB66_round115_full_registration_v3',
        'protected_upper_pool_HGB66_round115_full_registration_v4','protected_upper_pool_HGB66_round115_full_registration_v5',
        'flagged_HGB_small_amplitude88_official_comparison','flagged_HGB_small_amplitude88_official_comparison_v2','flagged_HGB_small_amplitude88_official_comparison_v3',
        'flagged_HGB_small_amplitude88_selected_candidate_preparation','flagged_HGB_small_amplitude88_selected_candidate_sealing',
        'flagged_HGB_small_amplitude88_scores_main_publication']
    for name in names:
        folder=A/'service_owned_workflows_20261006'/name
        sources += [folder/n for n in ('job_definition.json','native_launch.json')]
        if not owned(read(folder/'native_launch.json')):sources += list(folder.glob('*.json'))+list(folder.glob('*.log'))
    pins={str(p):sha(p) for p in dict.fromkeys(sources)}
    create(out/'frozen_before_main_publication.json',{'input_sha256':pins,'future_full116_qualification_not_claimed':True,'test_labels_read':False})
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
            prefix=Path('validation_sync/HGB88_complete_pipeline_20261007');payload={(prefix/'.gitattributes').as_posix():b'* -text\n'};files={}
            for p in dict.fromkeys([*sources,out/'frozen_before_main_publication.json']):
                data=p.read_bytes();assert not sync.SECRET.search(data),p
                digest=hashlib.sha256(data).hexdigest();target=(prefix/p.relative_to(ROOT)).as_posix()
                if len(data)>=5*1024**2:
                    data=gzip.compress(data,mtime=0);assert hashlib.sha256(gzip.decompress(data)).hexdigest()==digest;target+='.gz'
                payload[target]=data;files[p.relative_to(ROOT).as_posix()]={'published_path':target,'original_sha256':digest,'published_sha256':hashlib.sha256(data).hexdigest()}
            previous=sync.git('rev-parse','HEAD');helpers.verify_main(previous);assert not sync.git('status','--porcelain')
            payload[(prefix/'manifest.json').as_posix()]=sync.encoded({'status':'published_actual85_full_controls_and_prospective_full116_pipeline_with_failed_dependency_history',
                'at_local':sync.now(),'files':files,'previous_main':previous,'only_branch':'main',
                'actual_full5635800_transform_controls':85,'prospective_source_compile_hash_controls':24,
                'actual_generated_baseline_gain_metadata_regressions':len(proof['baseline_gain_regression_controls']),
                'canonical116_sources_written_by_admission':0,'future1599600_or80day_qualification_not_claimed':True,
                'new_native_fits':0,'new_quality_scores':0,'future88_scores_and_full116_QA27_not_claimed_complete':True,
                'scientific_workers_stopped_suspended_or_restarted':0,'test_labels_read':False})
            payload[(prefix/'README.md').as_posix()]=('# 本机HGB小权重完整流程和实际故障恢复记录\n\n'
                '85项方案已通过完整5635800行独立变换与255个冷前缀控制；下一轮88项官方评分等待115完整QA26及main完成后运行。'
                '本目录保存24份未来登记源码的编译与摘要、9项比较基准增益元数据控制、移除涨停分支及保留非涨停分支图结构控制。'
                '复用已有20模型，比较基准和兼容方案基底分别记录，不新增训练。'
                '同时保留历史登记路径冲突、依赖退出的真实状态及隐藏启动身份，115原始66项分数及原冻结不重写。'
                '未来选中方案仍须封存、完整推理或精确锚点复用、完整QA27及main上传；本次不宣称这些已完成。\n').encode('utf8')
            scope.reverify()
            for name,data in payload.items():sync.atomic(sync.WORKTREE/name,data)
            names=sorted(payload)
            for offset in range(0,len(names),50):sync.git('add','-f','--',*names[offset:offset+50])
            assert set(sync.git('-c','core.quotepath=false','diff','--cached','--name-only').splitlines())<=set(payload)
            sync.git('-c','maintenance.auto=false','-c','gc.auto=0','commit','-m','登记本机HGB小权重完整116流程与真实依赖恢复记录',timeout=180)
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
