"""Publish corrected154 guard/bindings, actual151 complete receipt and independent69 Git reconciliation."""
from pathlib import Path
import sys,os,gzip,hashlib
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
OUT=Path('E:/赛题五_本机临时/drop05_156_frozen_gpu_frontier_main_v75_20261009')
def main():
    import publish_classifier_consensus_workflows_20261006 as h
    from handoff_joint_goss_round97_full_execution_20261006 import suspended_idle
    assert read(A/'two_seed154_actual_controls_main_v69_reconciled_receipt_20261009.json')['actual_independently_reverified_git_blobs']==991
    assert read(A/'optimization_20261003_r151/full_registration_execution.json')['status']=='passed'
    OUT.mkdir(exist_ok=False)
    pointer=A/'actual_BF16_medium2048_drop05_seed09_restart_location_v1_20261009.json'
    restart=Path(read(pointer)['output']);proof=read(restart/'verification.json')
    assert sha(restart/'verification.json')==read(pointer)['verification_sha256']
    assert proof['status']=='passed_actual_small32_and_wide2_BF16_micro_fresh_process_restart'
    assert len(proof['records'])==2
    assert all(r['all_training_losses_and_all_weight_bits_exact'] and r['changed_training_input_checkpoint_rejected'] for r in proof['records'])
    names=['bind_BF16Medium153_actual_receiver_dispatch_v42_20261009.py','BF16Medium153_actual_receiver_dispatch_v42_20261009.json',
        'BF16Medium153_actual_receiver_dispatch_controls_v42_20261009.json','BF16Medium153_actual_receiver_dispatch_hidden_launch_v42_20261009.json',
        'seed10_155_and_actual152_153_guard_main_v74_receipt_20261009.json',
        'qualified_submission_delivery_update_round152_v2_20261008.json',
        'monitor_actual_chronological_optimization_progress_v64_20261009.py','start_actual_recovered_progress_v64_20261009.py',
        'actual_recovered_progress_hidden_launch_v64_20261009.json','latest_actual_optimization_progress_pointer_v64_20261009.json',
        'actual_recovered_progress_handoff_v64_20261009.json','optimization_live_progress_v64_20261009.json','optimization_live_progress_v64_20261009.md',
        'BF16Drop05_81_round156_proposal_v1_20261009.json']
    sources=[Path(__file__),pointer,*(A/n for n in names)]
    for pattern in ('*drop05_seed09*20261009.py','*drop05_seed09*20261009.json','*BF16Medium*actual_v42_20261009.py'):
        sources.extend(p for p in A.glob(pattern) if p.is_file())
    sources.extend(p for p in restart.rglob('*') if p.is_file() and p.suffix in ('.json','.log'))
    for name in ('actual_BF16_medium2048_drop05_seed09_restart_control_v1_20261009','actual_BF16_medium2048_drop05_seed09_e64_bank6_v1_20261009',
        'BF16Medium153_complete_chronological_dispatch_actual_v42_20261009','BF16Medium78_round153_source_admission_v2_20261009'):
        f=A/'service_owned_workflows_20261006'/name;sources.extend(p for p in f.iterdir() if p.suffix in ('.json','.log'))
    sources=list(dict.fromkeys(sources));assert all(p.is_file() for p in sources)
    declaration=read(A/'neural_BF16_medium2048_drop05_seed09_e64_frontier_v1_20261009.json')
    for f,d in declaration['input_sha256'].items():assert sha(f)==d,f
    held=[]
    try:
        row=read(A/'service_owned_workflows_20261006/main_publisher_v10_20261009/native_launch.json');assert owned(row)
        parent,worker,idle=suspended_idle(row,'    main (watch_validations_main_v7_20261006.py:71)');held.extend((worker,parent))
        create(OUT/'actual_idle_watcher_hold.json',idle)
        sync=h.sync;previous=sync.git('rev-parse','HEAD');h.verify_main(previous);assert not sync.git('status','--porcelain')
        prefix=Path('validation_sync/drop05_156_frozen_gpu_frontier_v75_20261009');payload={};bindings={}
        for p in sources:
            raw=p.read_bytes();assert not sync.SECRET.search(raw),p
            digest=hashlib.sha256(raw).hexdigest();relative=p.relative_to(ROOT) if p.is_relative_to(ROOT) else Path('external_metadata')/(digest+'_'+p.name)
            target=(prefix/relative).as_posix();data=raw
            if len(data)>=5*1024**2:data=gzip.compress(data,mtime=0);target+='.gz';assert gzip.decompress(data)==raw
            assert len(data)<95*1024**2;payload[target]=data;bindings[str(p)]={'published_path':target,'raw_sha256':digest,'original_bytes':len(raw)}
        payload[(prefix/'.gitattributes').as_posix()]=b'* -text\n'
        payload[(prefix/'manifest.json').as_posix()]=sync.encoded({'status':'frozen_dropout_only_contrast_and_actual_bit_exact_restart_before_own_six_annual_fits',
            'at_local':sync.now(),'files':bindings,'new_dropout_configuration':declaration['configuration'],
            'scientific_training_change':'dropout0_to0.05_seed09_epochs64_all_other_config_exact',
            'actual_restart_control_cases':2,'all_losses_and_weights_and_reloaded_predictions_bits_exact':True,
            'actual_156_complete_annual_fits':0,'expected_156_complete_annual_fits':6,'expected_156_official_records':81,
            'actual156_GPU_training_waits_complete155':True,'actual156_quality_scores':0,
            'actual153_admission2_passed_and_quality_running':True,'actual152_new_delivery_fully_verified':True,
            'all_failed_original_attempts_preserved':True,'scientific_jobs_stopped_or_restarted':0,
            'test_labels_read':False,'full156_qualification_not_claimed':True})
        create(OUT/'frozen_before_main_publication.json',{'files':bindings})
        for name,data in payload.items():sync.atomic(sync.WORKTREE/name,data)
        targets=sorted(payload)
        for i in range(0,len(targets),50):sync.git('add','-f','--',*targets[i:i+50])
        assert set(sync.git('-c','core.quotepath=false','diff','--cached','--name-only').splitlines())==set(targets)
        sync.git('-c','maintenance.auto=false','-c','gc.auto=0','commit','-m','同步156单变量dropout对照冻结及实际断点恢复逐位验证与153准入恢复和152新交付',timeout=180)
        commit=sync.git('rev-parse','HEAD');hashes={p:hashlib.sha256(data).hexdigest() for p,data in payload.items()};assert h.blob_hashes(commit,hashes)==hashes
        sync.git('push','origin','HEAD:refs/heads/main',timeout=180);h.verify_main(commit);h.watcher.advance_source_index(commit)
        value={'status':'pushed_and_remote_head_verified','at_local':sync.now(),'branch':'main','commit':commit,'raw_git_blobs_verified':len(hashes),
            'url':'https://github.com/Zagadka-3906/stock-return-prediction/tree/main/'+prefix.as_posix()}
        create(OUT/'receipt.json',value);create(A/'drop05_156_frozen_gpu_frontier_main_v75_receipt_20261009.json',value);print(value,flush=True)
    finally:
        for process in reversed(held):
            if process.is_running():process.resume()
        create(OUT/'actual_idle_watcher_resumed.json',{'resumed_in_finally':True,'scientific_workers_held':0})
if __name__=='__main__':
    count=int(os.environ.get('GIT_CONFIG_COUNT','0'))
    for i,(key,value) in enumerate((('http.proxy','http://127.0.0.1:7897'),('http.version','HTTP/1.1'))):os.environ[f'GIT_CONFIG_KEY_{count+i}']=key;os.environ[f'GIT_CONFIG_VALUE_{count+i}']=value
    os.environ['GIT_CONFIG_COUNT']=str(count+2)
    from lossless_chunked_safe_main_runtime_v1_20261009 import installed as safe
    from serial_main_publication_mutex_v1_20261009 import installed as serial
    from verified_TLS_Git_retry_runtime_v2_20261008 import installed as git_io
    log=Path('E:/赛题五_本机临时/drop05_156_frozen_gpu_frontier_safe_main_v75_20261009')
    with safe(log),serial(log/'serial_mutex.json'),git_io(log/'file_backed_git'):main()
