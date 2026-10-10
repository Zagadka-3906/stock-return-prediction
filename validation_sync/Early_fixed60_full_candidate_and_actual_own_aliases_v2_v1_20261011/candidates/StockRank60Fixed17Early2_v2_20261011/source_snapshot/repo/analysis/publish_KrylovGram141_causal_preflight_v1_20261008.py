"""Publish completed20 causal refits, seven adapter controls, frozen141 plan and handoff12 to main."""
from pathlib import Path
import gzip,hashlib,sys
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from file_backed_hidden_git_runtime_20261007 import installed
from handoff_joint_goss_round97_full_execution_20261006 import suspended_idle
import publish_classifier_consensus_workflows_20261006 as helpers

def main():
    handoff=A/'actual_optimization_handoff_v12_20261008.json';h=read(handoff);assert h['goal_active_not_paused_complete_or_blocked']
    pointer=A/'actual_KrylovGram20_causal_refit_location_v2_20261008.json';folder=Path(read(pointer)['output']);proof=read(folder/'verification.json')
    assert sha(folder/'verification.json')==read(pointer)['verification_sha256']
    assert proof['actual_causal_same_configuration_refit_controls']==20 and proof['actual_maturity_windows']==5
    native=A/'KrylovGram141_native_receiver_preflight_v1_20261008.json';assert len(read(native)['adapter_controls'])==7
    sources=[Path(__file__),handoff,A/'actual_optimization_handoff_v12_20261008.md',A/'record_actual_optimization_handoff_v12_20261008.py',
        pointer,*folder.rglob('*.json'),native,A/'KrylovGram52_round141_plan_v1_20261008.json',
        A/'prepare_KrylovGram52_round141_plan_controls_v1_20261008.py',A/'prepare_KrylovGram141_native_preflight_v1_20261008.py',
        A/'prepare_KrylovGram141_native_preflight_actual_v1_20261008.py',A/'KrylovGram141_native_preflight_lineage_v1_20261008.json',
        A/'KrylovGram64_complete_parent_CDF_v1_20261008.py',A/'KrylovGram64_complete_parent_native_stage_v1_20261008.py',
        A/'predict_KrylovGram64_complete_parent_scheme_v1_20261008.py',A/'verify_KrylovGram49_parent134_historical_v1_20261008.py',
        A/'verify_KrylovGram24_native_historical_hooks_v1_20261008.py',A/'verify_KrylovGram_multiyear_native_calendar_v1_20261008.py',
        A/'actual_KrylovGram52_plan_preparation_hidden_launch_v1_20261008.json',A/'actual_KrylovGram52_plan_historical_hidden_launches_v1_20261008.json',
        A/'actual_KrylovGram141_calendar_hidden_launch_v1_20261008.json',A/'actual_KrylovGram20_causal_refit_hidden_launch_v2_20261008.json',
        A/'nonflag_KrylovGram64_controls_main_v2_20261008/probe/receipt.json',A/'nonflag_KrylovGram64_controls_main_v2_20261008/bank/receipt.json']
    causal_service=A/'service_owned_workflows_20261006/KrylovGram20_causal_refit_controls_v2_20261008'
    assert not owned(read(causal_service/'native_launch.json')) and read(causal_service/'service_execution.json')['status']=='passed'
    sources += list(causal_service.glob('*.json'))+list(causal_service.glob('*.log'))
    for row in read(A/'actual_KrylovGram52_plan_historical_hidden_launches_v1_20261008.json')['launches'].values():
        sf=Path(row['script_args'][0]).parent;sources += [sf/'native_launch.json',sf/'job_definition.json']
    row=read(A/'actual_KrylovGram141_calendar_hidden_launch_v1_20261008.json');sf=Path(row['script_args'][0]).parent;sources += [sf/'native_launch.json',sf/'job_definition.json']
    sources=list(dict.fromkeys(sources));assert all(p.is_file() for p in sources)
    pins={str(p):sha(p) for p in sources};out=A/'KrylovGram141_causal_preflight_main_v1_20261008';assert not out.exists();out.mkdir()
    create(out/'frozen_before_main_publication.json',{'input_sha256':pins,'actual_causal_refits':20,'actual_adapter_contracts':7,
        'new_quality_scores':0,'actual141_complete_pipeline_not_yet_prepared':True,'test_labels_read':False})
    held=[]
    try:
        row=read(A/'service_owned_workflows_20261006/main_publisher_v8_20261008/native_launch.json')
        parent,worker,idle=suspended_idle(row,'    main (watch_validations_main_v7_20261006.py:71)');held.extend((worker,parent))
        create(out/'actual_idle_main_hold.json',idle)
        from win32_read_handle_hash_cache_with_filename_v2_20261006 import LockedReadHashCache
        with installed(out/'file_backed_git'),LockedReadHashCache(pins) as scope:
            sync=helpers.sync;helpers.verify_main(sync.git('rev-parse','HEAD'));assert not sync.git('status','--porcelain')
            prefix=Path('validation_sync/KrylovGram141_causal_preflight_v1_20261008');targets={};bindings={}
            for source in sources:
                data=source.read_bytes();assert not sync.SECRET.search(data),source
                digest=hashlib.sha256(data).hexdigest();relative=source.relative_to(ROOT) if source.is_relative_to(ROOT) else Path('external_metadata')/(digest+'_'+source.name)
                target=(prefix/relative).as_posix();raw_size=len(data)
                if len(data)>=5*1024**2:data=gzip.compress(data,mtime=0);target+='.gz'
                targets[target]=data;bindings[str(source)]={'published_path':target,'raw_sha256':digest,'original_bytes':raw_size}
            targets[(prefix/'.gitattributes').as_posix()]=b'* -text\n'
            targets[(prefix/'manifest.json').as_posix()]=sync.encoded({'status':'passed_actual20_causal_refits7_adapter_contracts_and_frozen141_plan_handoff12',
                'at_local':sync.now(),'files':bindings,'actual_own_maturity_windows':5,'actual_same_recipe_causal_refits':20,'actual_adapter_contracts':7,
                'planned_round':141,'planned_official_cases':52,'historical49_147_and24_24_andcalendar24_48_still_not_claimed_by_this_publication':True,
                'full141_quality_and_candidate_and_QA52_main_still_required':True,'new_official_scores':0,'new_unique_model_fits_by_causal_check':0,
                'test_labels_read':False,'main_only':True,'global_exhaustion_not_claimed':True})
            for name,data in targets.items():sync.atomic(sync.WORKTREE/name,data)
            names=sorted(targets)
            for left in range(0,len(names),50):sync.git('add','-f','--',*names[left:left+50])
            assert set(sync.git('-c','core.quotepath=false','diff','--cached','--name-only').splitlines())==set(names)
            sync.git('-c','maintenance.auto=false','-c','gc.auto=0','commit','-m','同步重正交CG20次因果重训练与7接入检查、冻结141方案及交接12',timeout=180)
            commit=sync.git('rev-parse','HEAD');hashes={n:hashlib.sha256(d).hexdigest() for n,d in targets.items()};assert helpers.blob_hashes(commit,hashes)==hashes
            sync.git('push','origin','HEAD:refs/heads/main',timeout=180);helpers.verify_main(commit);helpers.watcher.advance_source_index(commit);scope.reverify()
            create(out/'receipt.json',{'status':'pushed_and_remote_head_verified','at_local':sync.now(),'branch':'main','commit':commit,
                'raw_git_blobs_verified':len(hashes),'new_official_scores':0,'url':'https://github.com/Zagadka-3906/stock-return-prediction/tree/main/'+prefix.as_posix()})
            print('Actual CG20 causal refits, seven native adapters and handoff12 published: '+commit,flush=True)
    finally:
        for process in reversed(held):
            if process.is_running():process.resume()

if __name__=='__main__':main()
