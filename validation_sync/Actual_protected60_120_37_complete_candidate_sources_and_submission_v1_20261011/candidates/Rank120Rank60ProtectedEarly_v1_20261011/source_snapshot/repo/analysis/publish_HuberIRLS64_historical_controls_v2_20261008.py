"""Publish actual49/147 CDF and18/18 native historical controls after the full-bank publication closes."""
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
    folders=[closed(name) for name in ('HuberIRLS64_18_native_historical_hooks_v2_20261008','HuberIRLS64_49_parent134_historical_controls_v2_20261008',
        'nonflag_HuberIRLS64_controls_main_publication_v1_20261008')]
    sources=[Path(__file__),A/'freeze_HuberIRLS64_52_round137_plan_v2_20261008.py',A/'HuberIRLS64_52_round137_plan_v2_20261008.json',
        A/'HuberIRLS64_complete_parent_CDF_v1_20261008.py',A/'HuberIRLS64_complete_parent_native_stage_v2_20261008.py',
        A/'predict_HuberIRLS64_complete_parent_scheme_v2_20261008.py',A/'verify_HuberIRLS64_49_parent134_historical_v2_20261008.py',
        A/'verify_HuberIRLS64_18_native_historical_hooks_v2_20261008.py',A/'verify_HuberIRLS64_49_current_parent_v2_20261008.py',
        A/'queue_HuberIRLS64_historical_controls_v1_20261008.py',A/'actual_HuberIRLS64_bounded_pipeline_hidden_launches_v2_20261008.json',
        A/'nonflag_HuberIRLS64_controls_main_v1_20261008/probe/receipt.json',A/'nonflag_HuberIRLS64_controls_main_v1_20261008/bank/receipt.json']
    for folder in folders:sources += list(folder.glob('*.json'))+list(folder.glob('*.log'))
    counts=[]
    for filename in ('actual_HuberIRLS64_49_parent134_location_v2_20261008.json','actual_HuberIRLS64_18_native_hooks_location_v2_20261008.json'):
        path=A/filename;pointer=read(path);folder=Path(pointer['output']);proof=read(folder/'verification.json')
        assert sha(folder/'verification.json')==pointer['verification_sha256'] and proof['actual_quality_scores' if 'actual_quality_scores' in proof else 'actual_official_scores']==0
        counts.append((proof.get('actual_full_cases',proof.get('actual_hooks')),proof.get('actual_cold_cases',proof.get('actual_cold_hooks'))))
        sources += [path,*folder.glob('*.json'),*folder.glob('*.py')]
    assert counts==[(49,147),(18,18)]
    recovery=A/'HuberIRLS64_amplitude_cap_receiver_recovery_v2_20261008.json'
    sources += [recovery,A/'recover_HuberIRLS64_amplitude_cap_receivers_v2_20261008.py']
    sources += [Path(path) for path in read(recovery)['preserved_failed_source_and_log_sha256']]
    sources=list(dict.fromkeys(sources));pins={str(p):sha(p) for p in sources}
    out=A/'HuberIRLS64_historical_controls_main_v2_20261008';assert not out.exists();out.mkdir()
    create(out/'frozen_before_main_publication.json',{'input_sha256':pins,'actual_full_CDF_controls':49,'actual_cold_CDF_controls':147,
        'actual_native_hooks':18,'actual_cold_native_hooks':18,'actual_quality_scores':0,'exact137_parent52_receivers_scores_and_candidate_not_yet_qualified':True})
    held=[]
    try:
        row=read(A/'service_owned_workflows_20261006/main_publisher_v8_20261008/native_launch.json')
        parent,worker,idle=suspended_idle(row,'    main (watch_validations_main_v7_20261006.py:71)');held.extend((worker,parent));create(out/'actual_idle_main_hold.json',idle)
        from win32_read_handle_hash_cache_with_filename_v2_20261006 import LockedReadHashCache
        with installed(out/'file_backed_git'),LockedReadHashCache(pins) as scope:
            sync=helpers.sync;helpers.verify_main(sync.git('rev-parse','HEAD'));assert not sync.git('status','--porcelain')
            prefix=Path('validation_sync/HuberIRLS64_historical_v2_20261008');targets={};bindings={}
            for source in sources:
                data=source.read_bytes();assert not sync.SECRET.search(data),source;digest=hashlib.sha256(data).hexdigest()
                relative=source.relative_to(ROOT) if source.is_relative_to(ROOT) else Path('external_metadata')/(digest+'_'+source.name)
                target=(prefix/relative).as_posix();targets[target]=data;bindings[str(source)]={'published_path':target,'raw_sha256':digest}
            targets[(prefix/'.gitattributes').as_posix()]=b'* -text\n';targets[(prefix/'manifest.json').as_posix()]=sync.encoded({
                'status':'passed_actual49_full147cold18native18cold_Huber_preliminary_historical_controls','at_local':sync.now(),
                'files':bindings,'actual_full_rows_per_CDF_case':5635800,'actual_full_CDF_cases':49,'actual_cold_CDF_cases':147,
                'actual_native_historical_hooks':18,'actual_cold_native_hooks':18,'historical_parent_round':134,'actual_new_quality_scores':0,
                'prospective_backend_compilations':3,'actual_future_candidate_replay_not_claimed':True,
                'complete52_receiver_preflight_and_exact_current_parent_still_required':True,'test_labels_read':False})
            for name,data in targets.items():sync.atomic(sync.WORKTREE/name,data)
            names=sorted(targets)
            for left in range(0,len(names),50):sync.git('add','-f','--',*names[left:left+50])
            assert set(sync.git('-c','core.quotepath=false','diff','--cached','--name-only').splitlines())==set(names)
            sync.git('-c','maintenance.auto=false','-c','gc.auto=0','commit','-m','同步Huber鲁棒残差49项完整历史CDF与18项原生模型接入检查',timeout=180)
            commit=sync.git('rev-parse','HEAD');hashes={n:hashlib.sha256(d).hexdigest() for n,d in targets.items()};assert helpers.blob_hashes(commit,hashes)==hashes
            sync.git('push','origin','HEAD:refs/heads/main',timeout=180);helpers.verify_main(commit);helpers.watcher.advance_source_index(commit);scope.reverify()
            create(out/'receipt.json',{'status':'pushed_and_remote_head_verified','at_local':sync.now(),'branch':'main','commit':commit,
                'raw_git_blobs_verified':len(hashes),'actual_quality_scores':0,
                'url':'https://github.com/Zagadka-3906/stock-return-prediction/tree/main/'+prefix.as_posix()})
            print('Actual Huber49/147 and18/18 historical controls published to main: '+commit,flush=True)
    finally:
        for process in reversed(held):
            if process.is_running():process.resume()


if __name__=='__main__':main()
