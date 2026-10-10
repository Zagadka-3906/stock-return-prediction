"""Freeze completed143/Alpha40/40/40, exact144 dispatch and six neural models; upload actual records and retained failures."""
from pathlib import Path
import sys,time,gzip,hashlib
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
def main():
    state=read(A/'actual_optimization135_to144_progress_v17_20261008.json')
    full=A/'optimization_20261003_r143/full_registration_execution.json';receipt=A/'github_validation_sync_main_20261005/round143_receipt.json'
    assert read(full)['status']=='passed' and read(receipt)['status']=='pushed_and_remote_head_verified'
    assert read(receipt)['scored_records']==68 and read(receipt)['connected_records']==13738
    sources=[Path(__file__),full,receipt,A/'ConeRidgeAlpha8_completed_controls_main_v1_20261008/receipt.json',
        A/'monitor_actual_optimization135_to144_v17_20261008.py',A/'actual144_score5_observer_archive_hidden_launches_v17_20261008.json',
        A/'ConeRidgeFine143_E_snapshot_sealing_recovery_v2_20261008.json',
        A/'recover_ConeRidgeFine143_E_snapshot_sealing_v2_20261008.py',
        A/'seal_ConeRidgeFine68_selected_candidate_v2_20261008.py',
        A/'run_ConeRidgeFine68_round143_full_registration_v2_20261008.py']
    for pattern in ('*ConeRidgeAlpha*20261008.py','*ConeRidgeAlpha*20261008.json'):
        sources.extend(A.glob(pattern))
    # Only immutable launch/definition metadata from live workers; complete terminal outputs for closed jobs.
    for folder in (A/'service_owned_workflows_20261006').iterdir():
        if not folder.is_dir() or not any(s in folder.name for s in ('ConeRidgeAlpha','ConeRidgeFine68','actual_neural_BF16_micro8192_bank6_v2')):continue
        row_path=folder/'native_launch.json'
        if not row_path.exists():continue
        row=read(row_path);sources.extend((row_path,folder/'job_definition.json'))
        if not owned(row):sources.extend(folder.glob('*.json'));sources.extend(folder.glob('*.log'))
    for pointer in ('actual_nonflag_ConeRidgeAlpha8_64_bank40_location_v2_20261008.json',
                    'actual_ConeRidgeAlpha40_causal_refit_location_v2_20261008.json',
                    'actual_ConeRidgeAlpha97_parent134_location_v1_20261008.json',
                    'actual_ConeRidgeAlpha48_native_hooks_location_v1_20261008.json',
                    'actual_ConeRidgeAlpha_multiyear_calendar_location_v1_20261008.json'):
        path=A/pointer
        if not path.exists():continue
        output=Path(read(path)['output']);assert (output/'verification.json').exists()
        sources.extend(p for p in output.rglob('*.json') if p.name!='actual_stage.json')
    neural=Path('E:/赛题五_本机临时/neural_BF16_micro8192_bank6_v2_20261008')
    sources.extend(p for p in neural.glob('*.json') if p.name!='actual_stage.json')
    # Exact six annual info files are final records; saved state/weights remain local on E.
    sources.extend(neural.glob('*/info_*.json'))
    sources += [A/'reconcile_actual_handoff18_remote_and_long_paths_v2_20261008.py',A/'actual_handoff18_long_paths_reconciliation_v2_20261008.json',A/'actual_optimization_handoff_main_v17_20261008/receipt.json',A/'start_actual144_score5_observer_and_archive_v17_20261008.py',Path(__file__)]
    sources=list(dict.fromkeys(sources));assert all(p.is_file() and p.suffix in ('.py','.json','.log') for p in sources)
    pins={str(p):sha(p) for p in sources}
    handoff=A/'actual_optimization_handoff_v18_20261008.json'
    create(handoff,{'status':'actual143_full_main_and_alpha40_annual40_causal_and_corrected100_pipeline',
        'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'deadline_local':'2026-10-10T23:59:00+08:00',
        'goal_active_not_paused_complete_or_blocked':True,'actual_progress_at_checkpoint':state,
        'actual143_fully_qualified_receipt':read(receipt),'actual_new_alpha_controls_receipt':read(sources[3]),
        'actual144_source_version':4,'actual144_scoring_version':5,'actual144_registration_version':6,'input_sha256':pins,
        'old_failures_and_exact_idle_supersessions_preserved':True,'new_quality_scores_by_handoff':0,
        'native_weights_and_large_arrays_retained_only_on_E':True,'global_exhaustion_claimed':False,'test_labels_read':False})
    md=A/'actual_optimization_handoff_v18_20261008.md'
    md.write_text('# 实际优化交接18\n\n截止10月10日23:59；目标active。\n\n第143轮68项评分、两次完整推理及冷80、19个唯一原生模型、完整榜13,738条和QA54全部通过并同步main，S=0.4511472020051003。\n\n新增八个参数头已完成40个年度模型、八份完整OOF及40次因果重训，并同步main。144轮24来源、2,619个完整父图、9接入合同、48原生/48冷及48跨年/96整日检查通过；当前143父方案97完整/291冷仍按实际进度记录。\n\n原生数学保持不变；评分输出路径与进度写入的旧配置失败保留。新来源4的24脚本/2619完整图、新D评分路径5及E进度写入实际验证后，评分5、候选5和登记6已启动；按实时快照记载实际已完成评分数量，尚不能宣称100评分、候选及QA55完成。原等待接收器在精确PID、创建时间和源码睡眠行审计后替换；旧版本、失败和局部证明全部保留。\n\n神经6个年度模型、32轮训练、5个完整年度独立复核、37完整/111冷及3原生/3冷均已通过；第135轮实际控制已同步main并开始40项评分。136至141继续队列。只使用TRAIN和原评分，不读取实际测试标签。未证明可行方向及计算边界穷尽。\n',encoding='utf8',newline='\n')
    sources.extend((handoff,md));pins={str(p):sha(p) for p in sources}
    out=A/'actual_optimization_handoff_main_v18_20261008';assert not out.exists();out.mkdir()
    create(out/'frozen_before_main_publication.json',{'input_sha256':pins,'main_only':True,'new_quality_scores':0})
    from handoff_joint_goss_round97_full_execution_20261006 import suspended_idle
    from file_backed_hidden_git_runtime_20261007 import installed
    import publish_classifier_consensus_workflows_20261006 as helpers
    held=[]
    try:
        row=read(A/'service_owned_workflows_20261006/main_publisher_v8_20261008/native_launch.json')
        parent,worker,idle=suspended_idle(row,'    main (watch_validations_main_v7_20261006.py:71)');held.extend((worker,parent))
        create(out/'actual_main_idle_hold.json',idle)
        from win32_read_handle_hash_cache_with_filename_v2_20261006 import LockedReadHashCache
        with installed(out/'file_backed_git'),LockedReadHashCache(pins) as scope:
            sync=helpers.sync;previous=sync.git('rev-parse','HEAD');helpers.verify_main(previous);assert not sync.git('status','--porcelain')
            prefix=Path('validation_sync/actual_optimization_handoff_v18_20261008');payload={};bindings={}
            for source in sources:
                data=source.read_bytes();assert not sync.SECRET.search(data),source;digest=hashlib.sha256(data).hexdigest();assert digest==pins[str(source)]
                relative=source.relative_to(ROOT) if source.is_relative_to(ROOT) else Path('external_metadata')/(digest+'_'+source.name)
                target=(prefix/relative).as_posix();size=len(data)
                if size>=5*1024**2:data=gzip.compress(data,mtime=0);target+='.gz';assert hashlib.sha256(gzip.decompress(data)).hexdigest()==digest
                payload[target]=data;bindings[str(source)]={'published_path':target,'raw_sha256':digest,'original_bytes':size}
            payload[(prefix/'.gitattributes').as_posix()]=b'* -text\n'
            payload[(prefix/'manifest.json').as_posix()]=sync.encoded({'status':'passed_actual143_complete_and_alpha_actual_controls_and_144_pending_handoff',
                'at_local':sync.now(),'files':bindings,'main_only':True,'new_quality_scores_by_publication':0,'test_labels_read':False})
            for name,data in payload.items():sync.atomic(sync.WORKTREE/name,data)
            names=sorted(payload)
            for left in range(0,len(names),50):sync.git('add','-f','--',*names[left:left+50])
            assert set(sync.git('-c','core.quotepath=false','diff','--cached','--name-only').splitlines())==set(names)
            sync.git('-c','maintenance.auto=false','-c','gc.auto=0','commit','-m','同步第143轮完整验收、40年度40因果验证及144轮完整队列、失败记录和交接18',timeout=180)
            commit=sync.git('rev-parse','HEAD');expected={n:hashlib.sha256(d).hexdigest() for n,d in payload.items()}
            assert helpers.blob_hashes(commit,expected)==expected
            sync.git('push','origin','HEAD:refs/heads/main',timeout=180);helpers.verify_main(commit);helpers.watcher.advance_source_index(commit);scope.reverify()
            create(out/'receipt.json',{'status':'pushed_and_remote_head_verified','at_local':sync.now(),'branch':'main','commit':commit,
                'raw_git_blobs_verified':len(expected),'new_quality_scores_by_publication':0,
                'url':'https://github.com/Zagadka-3906/stock-return-prediction/tree/main/'+prefix.as_posix()})
            print('Complete actual handoff18 and retained failures published: '+commit,flush=True)
    finally:
        for process in reversed(held):
            if process.is_running():process.resume()
if __name__=='__main__':main()
