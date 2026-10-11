"""Upload all new actual passed/failed receivers, deadline and ready-delivery metadata; preserve running136 as running."""
from pathlib import Path
import sys,time,hashlib,gzip,json,datetime
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
def main():
    assert read(A/'optimization_20261003_r144/full_registration_execution.json')['status']=='passed'
    assert read(A/'github_validation_sync_main_20261005/round144_receipt.json')['status']=='pushed_and_remote_head_verified'
    assert read(A/'service_owned_workflows_20261006/CrossFamily94_controls_main_publication_v5_20261008/service_execution.json')['status']=='passed'
    from monitor_actual135_144_connected_API_progress_v20_20261008 import snapshot
    progress=snapshot();assert progress['best_fully_qualified_round']==144
    since=datetime.datetime(2026,10,8,14,50).timestamp();sources=[]
    for p in A.iterdir():
        if p.is_file() and p.suffix in ('.py','.json','.md') and p.stat().st_mtime>=since:sources.append(p)
    for folder in (A/'service_owned_workflows_20261006').iterdir():
        if not folder.is_dir() or not (folder/'native_launch.json').exists():continue
        launch=folder/'native_launch.json'
        if launch.stat().st_mtime>=since:sources.extend(p for p in folder.iterdir() if p.is_file() and p.suffix in ('.json','.log'))
    sources.extend([A/'github_validation_sync_main_20261005/round135_receipt.json',A/'github_validation_sync_main_20261005/round144_receipt.json',A/'latest_verified_submission_delivery_v1_20261008.json',A/'current_ranking_HTML_E_relocation_verification_v1_20261008.json'])
    delivery=Path(read(A/'latest_verified_submission_delivery_v1_20261008.json')['output']);sources.extend([delivery/'submission_manifest.json',delivery/'提交说明.md'])
    bases=[Path('E:/赛题五_本机临时/exact135_144_scores_connected_API_v1_20261008')]+[Path(f'E:/赛题五_本机临时/round{n}_connected_API_main_v1_20261008') for n in (135,144)]
    for base in bases:
        for name in ('actual_connected_API_responses.json','main_only_API_verification.json','reconciliation_verification.json','verified_main_publication_receipt.json','actual_44MiB_API_blob_limit_failure_v1.json','actual_local_prepared_push_commit.json','actual_local_prepared_HTTP2_push_commit_v3.json'):
            if (base/name).is_file():sources.append(base/name)
        for directory in ('actual_proxy_Git_push_v1','adaptive_verified_TLS_push_v2','actual_verified_HTTP2_Git_push_v3'):
            folder=base/directory
            if folder.is_dir():sources.extend(p for p in folder.iterdir() if p.is_file() and p.suffix in ('.json','.stdout','.stderr'))
    import publish_classifier_consensus_workflows_20261006 as helpers
    sync=helpers.sync;out=A/'completed144_and_full_recovery_lineage_main_v21_20261008';out.mkdir(exist_ok=False)
    prefix=Path('validation_sync/completed144_and_full_recovery_lineage_v21_20261008');payload={};bindings={}
    for source in dict.fromkeys(sources):
        data=source.read_bytes();assert not sync.SECRET.search(data),source
        if source.suffix=='.json':json.loads(data.decode('utf-8-sig'))
        raw_sha=hashlib.sha256(data).hexdigest();relative=source.relative_to(ROOT) if source.is_relative_to(ROOT) else Path('external_frozen_metadata')/(raw_sha+'_'+source.name)
        target=(prefix/relative).as_posix();size=len(data)
        if size>=5*1024**2:data=gzip.compress(data,mtime=0);target+='.gz';assert hashlib.sha256(gzip.decompress(data)).hexdigest()==raw_sha
        payload[target]=data;bindings[str(source)]={'published_path':target,'sha256':raw_sha,'original_bytes':size}
    payload[(prefix/'.gitattributes').as_posix()]=b'* -text\n'
    payload[(prefix/'manifest.json').as_posix()]=sync.encoded({'status':'actual140_completed_scores_two_full_qualified_rounds_new_best144_ready_E_delivery_and_all_recovery_lineage_snapshot','at_local':sync.now(),'best_fully_qualified_round':144,'best_fully_qualified_score':progress['best_fully_qualified_score'],'files':bindings,'passed_and_failed_and_running_stages_kept_distinct':True,'deadline_local':'2026-10-10T23:59:00+08:00','goal_active_and_optimization_exhaustion_not_proven':True,'actual13694_quality_running_not_claimed_complete':True,'large_weights_predictions_and_raw_data_not_uploaded':True,'new_quality_scores_by_publication':0,'test_labels_read':False})
    payload[(prefix/'README.md').as_posix()]='''# 第135及144轮完成与实际恢复记录

第135轮40项官方评分、原有六视图完整榜QA46及main同步均已完成；选中已有134轮，未冒充新的神经网络候选推理。第144轮100项评分、20个物理模型的两次完整1599600行推理、独立解码、保存重载、冷80天、源码和参数冻结、六视图QA55及main同步均完成。完整榜13878项，当前最佳S=0.4511512965609873。

本记录保留本次所有新接收程序的通过、失败及运行中状态和错误日志，包括TLS上传失败、时区和分离HEAD协调、过长原生模型文件名、独占输出路径及状态字符串修复。旧失败没有覆盖为通过；已通过的实际预测未因封存文字修复重复计算。连接器实际拒绝44.25MiB blob的原始错误保留；原始完整归档最终通过验证TLS的HTTP2代理Git上传，远端commit/ref及每个原始Git blob均逐字节核验。

截止时间由用户确认：10月10日23:59。E盘已生成完全合格144轮提交CSV及校验清单。未向比赛平台执行提交，未读取实际测试标签。新一轮94项跨模型评分继续，运行中状态不能当作完成。优化方向或计算资源穷尽尚未证明。
'''.encode('utf8')
    create(out/'frozen_snapshot_before_main_publication.json',{'at_local':sync.now(),'files':bindings,'captured_live_state_is_a_timestamped_snapshot':True,'new_quality_scores':0})
    from handoff_joint_goss_round97_full_execution_20261006 import suspended_idle
    from file_backed_hidden_git_runtime_20261007 import installed
    held=[]
    try:
        row=read(A/'service_owned_workflows_20261006/main_publisher_v8_20261008/native_launch.json');parent,worker,idle=suspended_idle(row,'    main (watch_validations_main_v7_20261006.py:71)');held.extend((worker,parent));create(out/'actual_idle_main_hold.json',idle)
        with installed(out/'file_backed_git'):
            previous=sync.git('rev-parse','HEAD');helpers.verify_main(previous);assert not sync.git('status','--porcelain')
            for name,data in payload.items():sync.atomic(sync.WORKTREE/name,data)
            names=sorted(payload)
            for offset in range(0,len(names),50):sync.git('add','-f','--',*names[offset:offset+50])
            assert set(sync.git('-c','core.quotepath=false','diff','--cached','--name-only').splitlines())==set(names)
            sync.git('-c','maintenance.auto=false','-c','gc.auto=0','commit','-m','同步135与144轮完整验证、全部恢复失败记录、最佳提交清单和10月10日截止优先级',timeout=180)
            commit=sync.git('rev-parse','HEAD');expected={n:hashlib.sha256(d).hexdigest() for n,d in payload.items()};assert helpers.blob_hashes(commit,expected)==expected
            sync.git('push','origin','HEAD:refs/heads/main',timeout=180);helpers.verify_main(commit);helpers.watcher.advance_source_index(commit)
            create(out/'receipt.json',{'status':'pushed_and_remote_head_verified','branch':'main','commit':commit,'at_local':sync.now(),'raw_git_blobs_verified':len(expected),'best_fully_qualified_round':144,'official_score':progress['best_fully_qualified_score'],'new_quality_scores':0,'url':'https://github.com/Zagadka-3906/stock-return-prediction/tree/main/'+prefix.as_posix()})
            print(json.dumps(read(out/'receipt.json'),ensure_ascii=False),flush=True)
    finally:
        for p in reversed(held):
            if p.is_running():p.resume()
if __name__=='__main__':main()
