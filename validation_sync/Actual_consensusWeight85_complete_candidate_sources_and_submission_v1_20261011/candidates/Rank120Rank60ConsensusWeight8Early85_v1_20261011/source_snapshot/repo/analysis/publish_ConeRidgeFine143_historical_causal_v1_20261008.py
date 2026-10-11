"""Publish completed49/147,24/24,24/48 and twenty actual causal refits to main."""
from pathlib import Path
import gzip,hashlib,sys,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from file_backed_hidden_git_runtime_20261007 import installed
from handoff_joint_goss_round97_full_execution_20261006 import suspended_idle
import publish_classifier_consensus_workflows_20261006 as helpers


def main():
    prior=A/'service_owned_workflows_20261006/ConeRidge64_controls_main_publication_v1_20261008'
    while owned(read(prior/'native_launch.json')):time.sleep(10)
    assert read(prior/'service_execution.json')['status']=='passed'
    names=['ConeRidgeFine65_parent134_historical_controls_v1_20261008','ConeRidgeFine24_native_historical_hooks_v1_20261008',
        'ConeRidgeFine_multiyear_native_calendar_v1_20261008','ConeRidge20_causal_refit_controls_v1_20261008']
    pointers=['actual_ConeRidgeFine65_parent134_location_v1_20261008.json','actual_ConeRidgeFine24_native_hooks_location_v1_20261008.json',
        'actual_ConeRidgeFine_multiyear_calendar_location_v1_20261008.json','actual_ConeRidge20_causal_refit_location_v1_20261008.json']
    sources=[Path(__file__),*[A/name for name in ('prepare_ConeRidgeFine68_round143_plan_controls_v1_20261008.py',
        'ConeRidgeFine68_round143_plan_v1_20261008.json','ConeRidge64_complete_parent_CDF_v1_20261008.py',
        'ConeRidge64_complete_parent_native_stage_v1_20261008.py','predict_ConeRidge64_complete_parent_scheme_v1_20261008.py',
        'verify_ConeRidgeFine65_parent134_historical_v1_20261008.py','verify_ConeRidgeFine24_native_historical_hooks_v1_20261008.py','prepare_ConeRidgeFine143_native_preflight_v1_20261008.py','ConeRidgeFine143_native_receiver_preflight_v1_20261008.json',
        'verify_ConeRidgeFine_multiyear_native_calendar_v1_20261008.py','verify_ConeRidge20_causal_refit_v1_20261008.py',
        'actual_ConeRidge20_causal_refit_hidden_launch_v1_20261008.json',
        'actual_ConeRidgeFine68_plan_historical_hidden_launches_v1_20261008.json',
        'ConeRidgeFine143_plan_controls_preparation_hidden_launch_v1_20261008.json',
        'ConeRidge64_controls_main_v1_20261008/probe/receipt.json',
        'ConeRidge64_controls_main_v1_20261008/bank/receipt.json')]]
    controls={};proofs={}
    for index,(name,pointer) in enumerate(zip(names,pointers)):
        folder=A/'service_owned_workflows_20261006'/name
        while owned(read(folder/'native_launch.json')):time.sleep(10)
        assert read(folder/'service_execution.json')['status']=='passed',name
        sources += [p for p in folder.iterdir() if p.suffix in ('.json','.log')]
        pointer=A/pointer;out=Path(read(pointer)['output']);proof=read(out/'verification.json');proofs[name]=proof
        for path,digest in proof['input_sha256'].items():assert sha(path)==digest,path
        sources += [pointer,*out.glob('*.json')]
        if index==0:assert proof['actual_full_cases']==65 and proof['actual_cold_cases']==195
        elif index==1:assert proof['actual_hooks']==proof['actual_cold_hooks']==24
        elif index==2:assert proof['actual_calendar_cases']==24 and proof['actual_whole_day_controls']==64
        else:assert proof['actual_causal_same_configuration_refit_controls']==20 and proof['actual_maturity_windows']==5
    native=read(A/'ConeRidgeFine143_native_receiver_preflight_v1_20261008.json');assert len(native['adapter_controls'])==8 and native['backend_priority_cases']==8
    controls={'actual_native_bank_models':20,'actual_full5635800_CDF':65,'actual_cold_CDF':195,
        'actual_historical_native_hooks':24,'actual_historical_cold_hooks':24,'actual_calendar_controls':24,
        'actual_day_controls':64,'actual_adapter_contracts':8,'actual_own_maturity_windows':5,'actual_same_configuration_causal_refits':20}
    sources=list(dict.fromkeys(sources));pins={str(p):sha(p) for p in sources}
    output=A/'ConeRidgeFine143_historical_causal_main_v1_20261008';assert not output.exists();output.mkdir()
    create(output/'frozen_before_main_publication.json',{'input_sha256':pins,'actual_completed_controls':controls,
        'new_unique_native_candidates_by_controls':0,'new_official_scores':0,'full143_official_candidate_QA54_and_main_pending':True,'test_labels_read':False})
    held=[]
    try:
        row=read(A/'service_owned_workflows_20261006/main_publisher_v8_20261008/native_launch.json')
        parent,worker,idle=suspended_idle(row,'    main (watch_validations_main_v7_20261006.py:71)');held.extend((worker,parent));create(output/'actual_idle_main_hold.json',idle)
        from win32_read_handle_hash_cache_with_filename_v2_20261006 import LockedReadHashCache
        with installed(output/'file_backed_git'),LockedReadHashCache(pins) as scope:
            sync=helpers.sync;helpers.verify_main(sync.git('rev-parse','HEAD'));assert not sync.git('status','--porcelain')
            prefix=Path('validation_sync/ConeRidgeFine143_historical_causal_v1_20261008');targets={};bindings={}
            for source in sources:
                data=source.read_bytes();assert not sync.SECRET.search(data),source;digest=hashlib.sha256(data).hexdigest()
                relative=source.relative_to(ROOT) if source.is_relative_to(ROOT) else Path('external_metadata')/(digest+'_'+source.name)
                target=(prefix/relative).as_posix();raw_size=len(data)
                if len(data)>=5*1024**2:data=gzip.compress(data,mtime=0);target+='.gz';assert hashlib.sha256(gzip.decompress(data)).hexdigest()==digest
                targets[target]=data;bindings[str(source)]={'published_path':target,'raw_sha256':digest,'original_bytes':raw_size}
            targets[(prefix/'.gitattributes').as_posix()]=b'* -text\n'
            targets[(prefix/'manifest.json').as_posix()]=sync.encoded({'status':'passed_actual_spectral_full_historical_native_calendar_and_causal_refit_controls',
                'at_local':sync.now(),'planned_round':143,'files':bindings,'actual_completed_controls':controls,'planned_official_cases':68,
                'original_numerical_probe_and_bank_path_failures_preserved_in_prior_main_receipts':True,'actual_eight_adapter_contracts':True,
                'new_official_scores':0,'no_actual_future_X_and_Y_read':True,'full143_quality_candidate_QA54_main_still_required':True,
                'main_only':True,'global_resource_or_feasible_direction_exhaustion_not_claimed':True})
            for name,data in targets.items():sync.atomic(sync.WORKTREE/name,data)
            names=sorted(targets)
            for left in range(0,len(names),50):sync.git('add','-f','--',*names[left:left+50])
            assert set(sync.git('-c','core.quotepath=false','diff','--cached','--name-only').splitlines())==set(names)
            sync.git('-c','maintenance.auto=false','-c','gc.auto=0','commit','-m','同步第143轮65完整195冷、24原生24跨年及20标签扰动原生重新拟合检查',timeout=180)
            commit=sync.git('rev-parse','HEAD');hashes={name:hashlib.sha256(data).hexdigest() for name,data in targets.items()}
            assert helpers.blob_hashes(commit,hashes)==hashes
            sync.git('push','origin','HEAD:refs/heads/main',timeout=180);helpers.verify_main(commit);helpers.watcher.advance_source_index(commit);scope.reverify()
            create(output/'receipt.json',{'status':'pushed_and_remote_head_verified','at_local':sync.now(),'branch':'main','commit':commit,
                'raw_git_blobs_verified':len(hashes),'actual_completed_controls':controls,'new_official_scores':0,
                'url':'https://github.com/Zagadka-3906/stock-return-prediction/tree/main/'+prefix.as_posix()})
            print('Completed spectral historical and causal native evidence published: '+commit,flush=True)
    finally:
        for process in reversed(held):
            if process.is_running():process.resume()


if __name__=='__main__':main()
