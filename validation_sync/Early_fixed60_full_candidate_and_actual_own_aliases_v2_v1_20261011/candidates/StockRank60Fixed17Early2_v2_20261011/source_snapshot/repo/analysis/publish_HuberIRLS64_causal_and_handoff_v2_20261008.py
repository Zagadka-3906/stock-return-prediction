"""Publish actual maturity/poison controls and an honest unfinished-goal handoff after historical publication."""
from pathlib import Path
import hashlib,sys,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from file_backed_hidden_git_runtime_20261007 import installed
from handoff_joint_goss_round97_full_execution_20261006 import suspended_idle
import publish_classifier_consensus_workflows_20261006 as helpers


def closed(name):
    folder=A/'service_owned_workflows_20261006'/name
    while not (folder/'native_launch.json').exists() or owned(read(folder/'native_launch.json')):time.sleep(10)
    assert read(folder/'service_execution.json')['status']=='passed',name
    return folder


def main():
    folders=[closed(name) for name in ('HuberIRLS64_10_causal_input_controls_v1_20261008','HuberIRLS64_historical_controls_main_publication_v2_20261008')]
    from record_actual_optimization_handoff_v6_20261008 import main as record
    record()
    pointer_path=A/'actual_HuberIRLS64_10_causal_inputs_location_v1_20261008.json';pointer=read(pointer_path);folder=Path(pointer['output'])
    proof=read(folder/'verification.json');assert sha(folder/'verification.json')==pointer['verification_sha256']
    assert proof['actual_future_training_label_poison_controls']==10 and proof['actual_native_models_audited']==10
    sources=[Path(__file__),A/'record_actual_optimization_handoff_v6_20261008.py',A/'actual_optimization_handoff_v6_20261008.json',
        A/'actual_optimization_handoff_v6_20261008.md',A/'verify_HuberIRLS64_10_causal_inputs_v1_20261008.py',
        A/'start_HuberIRLS64_causal_inputs_v1_20261008.py',A/'actual_HuberIRLS64_causal_inputs_hidden_launch_v1_20261008.json',
        A/'actual_HuberIRLS64_bounded_pipeline_hidden_launches_v2_20261008.json',
        A/'queue_HuberIRLS64_historical_publication_and_current_parent_v1_20261008.py',pointer_path,*folder.glob('*.json'),
        A/'HuberIRLS64_historical_controls_main_v2_20261008/receipt.json',A/'prepare_combined_progress_monitor_v3_20261008.py',
        A/'monitor_neural135_and_CrossFamily136_v3_20261008.py',A/'actual_neural135_CrossFamily136_Huber_progress_hidden_launch_v3_20261008.json']
    for service in folders:sources += list(service.glob('*.json'))+list(service.glob('*.log'))
    sources=list(dict.fromkeys(sources));pins={str(p):sha(p) for p in sources};out=A/'HuberIRLS64_causal_handoff_main_v2_20261008'
    assert not out.exists();out.mkdir();create(out/'frozen_before_main_publication.json',{'input_sha256':pins,'actual_quality_scores':0,
        'actual_independent_maturity_controls':5,'actual_later_training_label_poison_controls':10,'goal_remains_active':True})
    held=[]
    try:
        row=read(A/'service_owned_workflows_20261006/main_publisher_v8_20261008/native_launch.json')
        parent,worker,idle=suspended_idle(row,'    main (watch_validations_main_v7_20261006.py:71)');held.extend((worker,parent));create(out/'actual_idle_main_hold.json',idle)
        from win32_read_handle_hash_cache_with_filename_v2_20261006 import LockedReadHashCache
        with installed(out/'file_backed_git'),LockedReadHashCache(pins) as scope:
            sync=helpers.sync;helpers.verify_main(sync.git('rev-parse','HEAD'));assert not sync.git('status','--porcelain')
            prefix=Path('validation_sync/HuberIRLS64_causal_handoff_v2_20261008');targets={};bindings={}
            for source in sources:
                data=source.read_bytes();assert not sync.SECRET.search(data),source;digest=hashlib.sha256(data).hexdigest()
                relative=source.relative_to(ROOT) if source.is_relative_to(ROOT) else Path('external_metadata')/(digest+'_'+source.name)
                target=(prefix/relative).as_posix();targets[target]=data;bindings[str(source)]={'published_path':target,'raw_sha256':digest}
            targets[(prefix/'.gitattributes').as_posix()]=b'* -text\n';targets[(prefix/'manifest.json').as_posix()]=sync.encoded({
                'status':'actual5_maturity10_later_training_label_poison10_native_controls_and_active_goal_handoff',
                'at_local':sync.now(),'files':bindings,'actual_quality_scores':0,'actual_future_candidate_inferences':0,
                'goal_active':True,'complete135136_and137_receiver_scoring_freeze_candidate_QA48_main_work_remains':True,
                'new_Huber_negative_and_mean_directions_predeclared':True,'global_optimization_exhaustion_not_claimed':True,'test_labels_read':False})
            for name,data in targets.items():sync.atomic(sync.WORKTREE/name,data)
            names=sorted(targets)
            for left in range(0,len(names),50):sync.git('add','-f','--',*names[left:left+50])
            assert set(sync.git('-c','core.quotepath=false','diff','--cached','--name-only').splitlines())==set(names)
            sync.git('-c','maintenance.auto=false','-c','gc.auto=0','commit','-m','同步Huber十项后续标签扰动和独立成熟检查及持续优化交接',timeout=180)
            commit=sync.git('rev-parse','HEAD');hashes={n:hashlib.sha256(d).hexdigest() for n,d in targets.items()};assert helpers.blob_hashes(commit,hashes)==hashes
            sync.git('push','origin','HEAD:refs/heads/main',timeout=180);helpers.verify_main(commit);helpers.watcher.advance_source_index(commit);scope.reverify()
            create(out/'receipt.json',{'status':'pushed_and_remote_head_verified','at_local':sync.now(),'branch':'main','commit':commit,
                'raw_git_blobs_verified':len(hashes),'actual_quality_scores':0,'goal_remains_active':True,
                'url':'https://github.com/Zagadka-3906/stock-return-prediction/tree/main/'+prefix.as_posix()})
            print('Actual Huber causal controls and active-goal handoff published to main: '+commit,flush=True)
    finally:
        for process in reversed(held):
            if process.is_running():process.resume()


if __name__=='__main__':main()
