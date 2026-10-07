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
    out=A/'protected_upper_pool_HGB66_candidate_pipeline_github_20261007';assert not out.exists();out.mkdir()
    # The bank publisher precedes us; score publication cannot start until all44 finish.
    closed('local_closed_dependency_recovery_v2_main_publication')
    closed('cpu_full_universe_ElasticNet24_bank_evidence_publication_v4')
    proof_path=A/'protected_upper_pool_HGB66_candidate_source_admission_20261007.json';proof=read(proof_path)
    assert proof['status']=='passed_actual_native_hook_and24_prospective_source_AST_hashes_schema_and_parent_baseline_controls'
    for p,digest in proof['input_sha256'].items():assert sha(p)==digest,p
    sources=[Path(__file__),proof_path,*map(Path,proof['input_sha256']),
        A/'protected_upper_pool_HGB66_candidate_actual_launch_20261007.json',
        A/'protected_upper_pool_HGB66_round115_actual_hidden_launch_20261007.json',
        A/'local_closed_dependency_recovery_v2_github_20261007/receipt.json',
        A/'github_validation_sync_main_20261005/round113_receipt.json',
        A/'cpu_full_universe_ElasticNet24_bank_recovery_v3_github_20261007/receipt.json']
    for name in ('protected_upper_pool_HGB66_selected_candidate_preparation','protected_upper_pool_HGB66_selected_candidate_sealing','protected_upper_pool_HGB66_round115_full_registration'):
        folder=A/'service_owned_workflows_20261006'/name
        sources += [folder/n for n in ('job_definition.json','native_launch.json','launch_result.json','verified_hidden_launch.json')]
    pins={str(p):sha(p) for p in dict.fromkeys(sources)}
    create(out/'frozen_before_main_publication.json',{'input_sha256':pins,'future_full115_qualification_not_claimed':True,'test_labels_read':False})
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
            prefix=Path('validation_sync/protected_upper_pool_HGB66_candidate_pipeline_20261007');payload={(prefix/'.gitattributes').as_posix():b'* -text\n'};files={}
            for p in dict.fromkeys([*sources,out/'frozen_before_main_publication.json']):
                data=p.read_bytes();assert not sync.SECRET.search(data),p
                digest=hashlib.sha256(data).hexdigest();target=(prefix/p.relative_to(ROOT)).as_posix()
                if len(data)>=5*1024**2:
                    data=gzip.compress(data,mtime=0);assert hashlib.sha256(gzip.decompress(data)).hexdigest()==digest;target+='.gz'
                payload[target]=data;files[p.relative_to(ROOT).as_posix()]={'published_path':target,'original_sha256':digest,'published_sha256':hashlib.sha256(data).hexdigest()}
            previous=sync.git('rev-parse','HEAD');helpers.verify_main(previous);assert not sync.git('status','--porcelain')
            payload[(prefix/'manifest.json').as_posix()]=sync.encoded({'status':'published_actual_native_hook_and_prospective_full115_pipeline_controls',
                'at_local':sync.now(),'files':files,'previous_main':previous,'only_branch':'main',
                'actual_historical_native_hook_cases':63,'prospective_source_compile_hash_controls':24,
                'actual_generated_baseline_gain_metadata_regressions':len(proof['baseline_gain_regression_controls']),
                'canonical115_sources_written_by_admission':0,'future1599600_or80day_qualification_not_claimed':True,
                'new_native_fits':0,'new_quality_scores':0,'future66_scores_and_full115_QA26_not_claimed_complete':True,
                'scientific_workers_stopped_suspended_or_restarted':0,'test_labels_read':False})
            payload[(prefix/'README.md').as_posix()]=('# 低分区HGB候选及第115轮完整登记流程\n\n'
                '63项原生候选钩子诊断已在603行历史特征、合成日期上通过；不代替实际完整父模型、1599600行测试X、两次重放或冷80日验证。'
                '66项评分选出方案后，新方案先冻结所有源码、原生模型、参数和收益率映射，再实际推理及封存；已有锚点则核对全验证位、8项指标、完整图及全部封存字节，保留原冻结时间，0新推理。\n\n'
                '第115轮取实际已选合格父轮次（112、113或114）作为比较基准。三种路径的24份生成源码已编译、核对评分字段及摘要；'
                '9项正、零、负增益元数据回归验证了基准与官方指标贡献一致，其中尚未完成114的路径明确使用假设指标。'
                '这些检查不新增质量分数或证明114完成。生产流程在任何规范文件写入前先检查整批8份摘要，避免旧摘要与新生成器不一致。\n\n'
                '候选封存后仍须实际运行完整榜六视图、全部参数及来源、45秒浏览器检查、全量原始字节发布与main远端核验。'
                '本次只登记已完成诊断、预检查和原生隐藏启动身份，不宣称未来66项评分、候选推理或115完整资格完成。\n').encode('utf8')
            scope.reverify()
            for name,data in payload.items():sync.atomic(sync.WORKTREE/name,data)
            names=sorted(payload)
            for offset in range(0,len(names),50):sync.git('add','-f','--',*names[offset:offset+50])
            assert set(sync.git('-c','core.quotepath=false','diff','--cached','--name-only').splitlines())<=set(payload)
            sync.git('-c','maintenance.auto=false','-c','gc.auto=0','commit','-m','登记低分区HGB候选冻结封存及完整115流程的24源码9项基准回归',timeout=180)
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
