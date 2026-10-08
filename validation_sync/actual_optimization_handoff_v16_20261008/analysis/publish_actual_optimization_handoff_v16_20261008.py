"""Publish actual142 reconciliation, Fine143 preflight, corrected queues and every failed source to main."""
from pathlib import Path
import gzip,hashlib,sys
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from file_backed_hidden_git_runtime_20261007 import installed
from handoff_joint_goss_round97_full_execution_20261006 import suspended_idle
import publish_classifier_consensus_workflows_20261006 as helpers
def main():
    handoff=A/'actual_optimization_handoff_v16_20261008.json';state=read(handoff)
    assert state['goal_active_not_paused_complete_or_blocked'] and state['actual142_scored_records']==52
    for path,digest in state['input_sha256'].items():assert sha(path)==digest,path
    sources=[Path(__file__),handoff,A/'actual_optimization_handoff_v16_20261008.md',
        A/'record_actual_optimization_handoff_v16_20261008.py',A/'monitor_actual_optimization135_to143_v13_20261008.py',
        A/'reconcile_ConeRidge142_completed_registration_v2_20261008.py']
    for pattern in ('*ConeRidgeFine*20261008.py','*ConeRidgeFine*20261008.json','*pending137to141*20261008.py',
      '*pending137to141*20261008.json','*pending11*20261008.py','*pending11*20261008.json',
      '*future_registration*20261008.py','*future_registration*20261008.json'):
        sources.extend(A.glob(pattern))
    for version in (10,11):
        prep=A/f'pending137to141_receiver_preparation_v{version}_20261008.json'
        sources.extend(Path(path) for path in read(prep)['input_sha256'])
    sources.extend(Path(path) for path in state['input_sha256'])
    for cfg in read(A/'pending137to141_receiver_dispatch_v11_20261008.json')['launches'].values():
        for name,row in cfg.items():
            assert owned(row) and row['actual_native_console_handle']==0,name
            sources += [Path(row['original_driver']),A/'service_owned_workflows_20261006'/name/'native_launch.json',A/'service_owned_workflows_20261006'/name/'job_definition.json']
    old_rows=read(A/'pending137to141_exact_idle_audit_v11_20261008.json')['audits']
    closed_names=list(old_rows)+[
        'ConeRidgeFine143_plan_controls_preparation_v1_20261008','ConeRidgeFine143_plan_controls_preparation_v2_20261008',
        'ConeRidgeFine143_plan_controls_preparation_v3_20261008','ConeRidgeFine143_plan_controls_preparation_v4_20261008',
        'ConeRidge52_round142_full_registration_v1_20261008','ConeRidge142_registration_receipt_reconciliation_v2_20261008',
        'KrylovGram141_completed_scoring_CSV_archivist_v1_20261008','KrylovGram141_completed_scoring_CSV_archivist_v2_20261008']
    for name in closed_names:
        folder=A/'service_owned_workflows_20261006'/name
        if (folder/'native_launch.json').exists():assert not owned(read(folder/'native_launch.json')),name
        sources.extend(folder.glob('*.json'));sources.extend(folder.glob('*.log'))
    for p in A.glob('*completed_scoring_CSV_v11_20261008.py'):sources.append(p)
    for path,digest in read(A/'pending137to141_collector_controls_v11_20261008.json')['input_sha256'].items():assert sha(path)==digest,path;sources.append(Path(path))
    sources=list(dict.fromkeys(sources));assert all(p.is_file() and p.resolve().is_relative_to(ROOT) for p in sources)
    pins={str(p):sha(p) for p in sources};out=A/'actual_optimization_handoff_main_v16_20261008';assert not out.exists();out.mkdir()
    create(out/'frozen_before_main_publication.json',{'input_sha256':pins,'actual142_full_main_verified':True,
        'actual143_partial_quality_at_checkpoint':state['actual_progress_at_checkpoint']['actual143_quality'],
        'all_failed_sources_and_partial_proofs_preserved':True,'new_quality_scores_by_publication':0,'test_labels_read':False})
    held=[]
    try:
        row=read(A/'service_owned_workflows_20261006/main_publisher_v8_20261008/native_launch.json')
        parent,worker,idle=suspended_idle(row,'    main (watch_validations_main_v7_20261006.py:71)');held.extend((worker,parent));create(out/'actual_idle_main_hold.json',idle)
        from win32_read_handle_hash_cache_with_filename_v2_20261006 import LockedReadHashCache
        with installed(out/'file_backed_git'),LockedReadHashCache(pins) as scope:
            sync=helpers.sync;previous=sync.git('rev-parse','HEAD');helpers.verify_main(previous);assert not sync.git('status','--porcelain')
            prefix=Path('validation_sync/actual_optimization_handoff_v16_20261008');payload={};bindings={}
            for source in sources:
                data=source.read_bytes();assert not sync.SECRET.search(data),source
                digest=hashlib.sha256(data).hexdigest();assert digest==pins[str(source)]
                target=(prefix/source.relative_to(ROOT)).as_posix();size=len(data)
                if size>=5*1024**2:data=gzip.compress(data,mtime=0);target+='.gz';assert hashlib.sha256(gzip.decompress(data)).hexdigest()==digest
                payload[target]=data;bindings[str(source)]={'published_path':target,'raw_sha256':digest,'original_bytes':size}
            payload[(prefix/'.gitattributes').as_posix()]=b'* -text\n'
            payload[(prefix/'manifest.json').as_posix()]=sync.encoded({'status':'actual142_complete_main_and143_partial_quality_with_five_corrected_future_queues',
                'at_local':sync.now(),'previous_main':previous,'files':bindings,'main_only':True,'actual142_records':52,
                'actual142_connected_records':13670,'actual142_main_commit':state['actual142_main_commit'],
                'actual143_expected_records':68,'actual143_partial_quality':state['actual_progress_at_checkpoint']['actual143_quality'],
                'actual15_collector_contracts_and_five_full_preflights_passed':True,'actual41_owned_future_steps':True,
                'original_neural_GPU_and135136_unchanged':True,'all_failed_sources_and_records_preserved':True,
                'new_official_scores_by_publication':0,'global_goal_exhaustion_not_claimed':True,'test_labels_read':False})
            payload[(prefix/'README.md').as_posix()]=('第142轮52项官方验证、完整榜13,670条、原候选和QA53已合格并同步main。登记失败已依原QA与远端回执如实核对，原失败来源保留。第143轮68项尚在评分，65完整/195冷、24原生/24跨年及24脚本1,560父图已通过。第137至141登记参数已在新来源11修正；实际15合同及五轮完整预演通过，40个精确识别空闲接收器替换，保留137原current，41步存活。旧失败、缺失引用、完整冻结来源均保留；当前神经训练继续；目标active，未证明优化穷尽。\n').encode('utf8')
            for target,data in payload.items():sync.atomic(sync.WORKTREE/target,data)
            names=sorted(payload)
            for left in range(0,len(names),50):sync.git('add','-f','--',*names[left:left+50])
            assert set(sync.git('-c','core.quotepath=false','diff','--cached','--name-only').splitlines())==set(names)
            sync.git('-c','maintenance.auto=false','-c','gc.auto=0','commit','-m','同步第142轮完整验收、第143轮68项验证与五轮登记修复、失败证据和交接16',timeout=180)
            commit=sync.git('rev-parse','HEAD');expected={n:hashlib.sha256(d).hexdigest() for n,d in payload.items()};assert helpers.blob_hashes(commit,expected)==expected
            sync.git('push','origin','HEAD:refs/heads/main',timeout=180);helpers.verify_main(commit);helpers.watcher.advance_source_index(commit);scope.reverify()
            create(out/'receipt.json',{'status':'pushed_and_remote_head_verified','at_local':sync.now(),'branch':'main','commit':commit,
                'raw_git_blobs_verified':len(expected),'new_official_scores_by_publication':0,
                'url':'https://github.com/Zagadka-3906/stock-return-prediction/tree/main/'+prefix.as_posix()})
            print('Handoff16 complete evidence and failures published to main: '+commit,flush=True)
    finally:
        for process in reversed(held):
            if process.is_running():process.resume()
if __name__=='__main__':main()
