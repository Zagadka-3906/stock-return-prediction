"""Upload all new actual passed/failed receivers, deadline and ready-delivery metadata; preserve running136 as running."""
from pathlib import Path
import sys,time,hashlib,gzip,json,datetime
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
def publish_once():
    assert read(A/'optimization_20261003_r144/full_registration_execution.json')['status']=='passed'
    assert read(A/'github_validation_sync_main_20261005/round144_receipt.json')['status']=='pushed_and_remote_head_verified'
    assert read(A/'service_owned_workflows_20261006/CrossFamily94_controls_main_publication_v5_20261008/service_execution.json')['status']=='passed'
    from monitor_actual_chronological_optimization_progress_v22_20261008 import snapshot
    progress=snapshot();progress['best_fully_qualified_round']=progress['best_fully_qualified']['round'];progress['best_fully_qualified_score']=progress['best_fully_qualified']['score'];assert progress['best_fully_qualified_round']==136
    since=datetime.datetime(2026,10,8,16,0).timestamp();sources=[]
    for p in A.iterdir():
        if p.is_file() and p.suffix in ('.py','.json','.md') and p.stat().st_mtime>=since:sources.append(p)
    for folder in (A/'service_owned_workflows_20261006').iterdir():
        if not folder.is_dir() or not (folder/'native_launch.json').exists():continue
        launch=folder/'native_launch.json'
        if launch.stat().st_mtime>=since:sources.extend(p for p in folder.iterdir() if p.is_file() and p.suffix in ('.json','.log'))
    sources.extend([A/'github_validation_sync_main_20261005/round135_receipt.json',A/'github_validation_sync_main_20261005/round144_receipt.json',A/'latest_verified_submission_delivery_v2_20261008.json',A/'current_ranking_HTML_E_relocation_verification_v1_20261008.json'])
    delivery=Path(read(A/'latest_verified_submission_delivery_v2_20261008.json')['output']);sources.extend([delivery/'submission_manifest.json',delivery/'提交说明.md'])
    sources.extend([A/'github_validation_sync_main_20261005/round136_receipt.json',A/'optimization_20261003_r136/full_registration_execution.json',A/'pending137to141_collector_controls_v14_20261008.json',A/'pending137to141_receiver_dispatch_v14_20261008.json',A/'pending14_idle_publication_hold_for_handoff22_20261008.json'])
    bases=[Path('E:/赛题五_本机临时/exact135_144_scores_connected_API_v1_20261008')]+[Path(f'E:/赛题五_本机临时/round{n}_connected_API_main_v1_20261008') for n in (135,144)]
    for base in bases:
        for name in ('actual_connected_API_responses.json','main_only_API_verification.json','reconciliation_verification.json','verified_main_publication_receipt.json','actual_44MiB_API_blob_limit_failure_v1.json','actual_local_prepared_push_commit.json','actual_local_prepared_HTTP2_push_commit_v3.json'):
            if (base/name).is_file():sources.append(base/name)
        for directory in ('actual_proxy_Git_push_v1','adaptive_verified_TLS_push_v2','actual_verified_HTTP2_Git_push_v3'):
            folder=base/directory
            if folder.is_dir():sources.extend(p for p in folder.iterdir() if p.is_file() and p.suffix in ('.json','.stdout','.stderr'))
    import publish_classifier_consensus_workflows_20261006 as helpers
    sync=helpers.sync;out=A/'completed144_and_full_recovery_lineage_main_v22_20261008';out.mkdir(exist_ok=False)
    prefix=Path('validation_sync/completed144_and_full_recovery_lineage_v22_20261008');payload={};bindings={}
    for source in dict.fromkeys(sources):
        data=source.read_bytes();assert not sync.SECRET.search(data),source
        if source.suffix=='.json':json.loads(data.decode('utf-8-sig'))
        raw_sha=hashlib.sha256(data).hexdigest();relative=source.relative_to(ROOT) if source.is_relative_to(ROOT) else Path('external_frozen_metadata')/(raw_sha+'_'+source.name)
        target=(prefix/relative).as_posix();size=len(data)
        if size>=5*1024**2:data=gzip.compress(data,mtime=0);target+='.gz';assert hashlib.sha256(gzip.decompress(data)).hexdigest()==raw_sha
        payload[target]=data;bindings[str(source)]={'published_path':target,'sha256':raw_sha,'original_bytes':size}
    payload[(prefix/'.gitattributes').as_posix()]=b'* -text\n'
    payload[(prefix/'manifest.json').as_posix()]=sync.encoded({'status':'actual234_completed_scores_new_best136_fully_qualified_and_pending14_all_recovery_lineage_snapshot','at_local':sync.now(),'best_fully_qualified_round':136,'best_fully_qualified_score':progress['best_fully_qualified_score'],'files':bindings,'passed_and_failed_and_running_stages_kept_distinct':True,'deadline_local':'2026-10-10T23:59:00+08:00','goal_active_and_optimization_exhaustion_not_proven':True,'actual13694_quality_and_full_native_QA47_main_completed':True,'pending137_to141_308_cases_remain':True,'large_weights_predictions_and_raw_data_not_uploaded':True,'new_quality_scores_by_publication':0,'test_labels_read':False})
    payload[(prefix/'README.md').as_posix()]='''# 第136轮完成及后续五轮实际恢复

第136轮94项原始官方连续前向评分已完成，最高S=0.4511623376562006。22个物理模型的两次完整1599600行原生推理、独立解码、保存重载、CSV逐字节复现及冷80天均已通过。源码、方案、参数及TRAIN成熟收益映射在未来特征读取之前冻结。完整榜13972项，原始六视图45秒QA47及main同步已完成。

后续137至141轮的120份预生成程序及全部方案图、字段、排序、模型去重、D/E文件检查通过。旧13接收流程因136旧登记路径错误失败，原始错误及文件均保留。新14流程在实际136完整main证明后启动，使用实际D1元数据的15版前检，不把失败14前检改记为成功。五轮预定308项评分仍待实际执行。

另准备了125项较小幅度及较细混合比例的可行方案草案，复用四个既有残差模型头；草案尚未获准评分，也未执行新推理。现有最优落在原网格最小正幅度，因此尚不能宣称方向或资源穷尽。

截止：10月10日23:59。E盘最新完全合格提交CSV及校验清单已经准备；旧144轮文件保留。未向比赛平台执行提交，未读取实际测试标签。同步时只临时挂起仍在等待依赖的Git发布接收程序，不停止模型验证进程；全部通过、失败和运行中状态分别保留。
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
            create(out/'receipt.json',{'status':'pushed_and_remote_head_verified','branch':'main','commit':commit,'at_local':sync.now(),'raw_git_blobs_verified':len(expected),'best_fully_qualified_round':136,'official_score':progress['best_fully_qualified_score'],'new_quality_scores':0,'url':'https://github.com/Zagadka-3906/stock-return-prediction/tree/main/'+prefix.as_posix()})
            print(json.dumps(read(out/'receipt.json'),ensure_ascii=False),flush=True)
    finally:
        for p in reversed(held):
            if p.is_running():p.resume()
def main():
    gate=A/'service_owned_workflows_20261006/CrossFamily94_round136_full_registration_v6_20261008'
    while not (gate/'native_launch.json').exists() or owned(read(gate/'native_launch.json')):time.sleep(10)
    assert read(gate/'service_execution.json')['status']=='passed'
    dispatch=A/'pending137to141_receiver_dispatch_v14_20261008.json'
    while not dispatch.exists():time.sleep(2)
    assert read(dispatch)['status']=='passed_all41_fresh_chronological_receivers_dispatched_after120_prospective_sources'
    from maintain_best_fully_qualified_submission_delivery_v2_20261008 import update
    pointer=A/'latest_verified_submission_delivery_v2_20261008.json'
    while not pointer.exists() or read(pointer)['selected_round']!=136:time.sleep(2)
    from handoff_joint_goss_round97_full_execution_20261006 import suspended_idle
    row=read(A/'service_owned_workflows_20261006/Huber52_controls_main_publication_v14_20261008/native_launch.json');held=[]
    try:
        assert owned(row)
        parent,worker,proof=suspended_idle(row,'    closed (publish_Huber52_evidence_v14_20261008.py:')
        held.extend((worker,parent))
        create(A/'pending14_idle_publication_hold_for_handoff22_20261008.json',{
            'status':'held_only_owned_waiting_publication_receiver_before_any_Git_mutation',
            'identity':row,'actual_idle_stack_before_and_after':proof,'scientific_workers_stopped':0,
            'resume_required_in_finally':True})
        publish_once()
    finally:
        for process in reversed(held):
            if process.is_running():process.resume()

if __name__=='__main__':main()
