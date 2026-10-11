"""Publish each completed numeric stage and preserved failed independent control to main."""
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

def publish(phase):
    closed('prepare_nonflag_ConeRidge64_bank20_v1_20261008')
    names=['nonflag_ConeRidge64_actual200k_v2_20261008']
    pointers=['actual_nonflag_ConeRidge64_small_location_v2_20261008.json','actual_nonflag_ConeRidge64_actual200k_location_v2_20261008.json']
    if phase in ('bank','causal'):
        names.append('nonflag_ConeRidge64_bank20_v1_20261008');pointers.append('actual_nonflag_ConeRidge64_bank20_location_v1_20261008.json')
    if phase=='causal':
        names.append('ConeRidge20_causal_refit_controls_v1_20261008');pointers.append('actual_ConeRidge20_causal_refit_location_v1_20261008.json')
    sources=[Path(__file__),ROOT/'后续选模标准.md']
    for filename in ('nonflag_ConeRidge64_streamed_v1_20261008.py','verify_nonflag_ConeRidge64_small_v1_20261008.py',
        'verify_nonflag_ConeRidge64_actual200k_v1_20261008.py','verify_nonflag_ConeRidge64_small_v2_20261008.py',
        'verify_nonflag_ConeRidge64_actual200k_v2_20261008.py','prepare_ConeRidge64_BVLS_oracle_recovery_v2_20261008.py',
        'ConeRidge64_BVLS_oracle_recovery_v2_20261008.json','prepare_nonflag_ConeRidge64_bank20_v1_20261008.py',
        'train_nonflag_ConeRidge64_bank20_v1_20261008.py','nonflag_ConeRidge64_bank20_plan_v1_20261008.json',
        'prepare_ConeRidge64_causal_controls_v1_20261008.py','verify_ConeRidge20_causal_refit_v1_20261008.py',
        'actual_nonflag_ConeRidge64_actual200k_hidden_launch_v2_20261008.json','actual_nonflag_ConeRidge64_bank20_hidden_launch_v1_20261008.json',
        'actual_ConeRidge20_causal_refit_hidden_launch_v1_20261008.json','nonflag_HuberIRLS64_own_window_v1_20261008.py',
        'nonflag_SpectralGram64_streamed_v1_20261008.py','nonflag_residual_HGB_preprocessing_20261007.py',
        'memory_bounded_numeric_preparation_20261007.py','nonflag_residual_Ridge_codec_20261007.py'):
        sources.append(A/filename)
    for name in names:
        folder=closed(name);sources += list(folder.glob('*.json'))+list(folder.glob('*.log'))
    for filename in pointers:
        pointer_path=A/filename;pointer=read(pointer_path);folder=Path(pointer['output']);proof=read(folder/'verification.json')
        assert sha(folder/'verification.json')==pointer['verification_sha256']
        if 'small_location' in filename:assert proof['actual_synthetic_native_fits']==12 and proof['actual_prefix_controls']==72
        elif 'actual200k_location' in filename:assert proof['actual_probe_native_fits']==4 and proof['own_full_window_rows_rechecked']==4969483
        elif 'bank20_location' in filename:assert proof['actual_native_fits']==20 and proof['actual_full_OOF_heads']==4
        else:assert proof['actual_causal_same_configuration_refit_controls']==20 and proof['actual_maturity_windows']==5
        sources += [pointer_path,*folder.rglob('*.json')]
    rejected=A/'service_owned_workflows_20261006/nonflag_ConeRidge64_actual200k_v1_20261008'
    assert not owned(read(rejected/'native_launch.json')) and read(rejected/'service_execution.json')['status']=='failed'
    sources += list(rejected.glob('*.json'))+list(rejected.glob('*.log'))
    for label in ('nonflag_ConeRidge64_small_v1_20261008','nonflag_ConeRidge64_actual200k_v1_20261008','ConeRidge64_dense_BVLS_bound_diagnostic_v1_20261008'):
        sources += list(Path('E:/赛题五_本机临时',label).rglob('*.json'))
    sources=list(dict.fromkeys(sources));pins={str(p):sha(p) for p in sources}
    out=A/'ConeRidge64_controls_main_v1_20261008'/phase;assert not out.exists();out.mkdir(parents=True)
    counts={'synthetic_native_fits':12,'synthetic_prefixes':72,'actual200k_native_fits':4,'actual200k_prefixes':24,
        'full_own_mature_native_fits':20 if phase!='probe' else 0,'full_OOF_heads':4 if phase!='probe' else 0,
        'same_recipe_causal_refits':20 if phase=='causal' else 0,'maturity_windows':5 if phase=='causal' else 0}
    create(out/'frozen_before_main_publication.json',{'input_sha256':pins,'phase':phase,'actual_completed_controls':counts,
        'new_official_scores':0,'failed_independent_control_preserved':True,'test_labels_read':False})
    held=[]
    try:
        row=read(A/'service_owned_workflows_20261006/main_publisher_v8_20261008/native_launch.json')
        parent,worker,idle=suspended_idle(row,'    main (watch_validations_main_v7_20261006.py:71)');held.extend((worker,parent))
        create(out/'actual_idle_main_hold.json',idle)
        from win32_read_handle_hash_cache_with_filename_v2_20261006 import LockedReadHashCache
        with installed(out/'file_backed_git'),LockedReadHashCache(pins) as scope:
            sync=helpers.sync;helpers.verify_main(sync.git('rev-parse','HEAD'));assert not sync.git('status','--porcelain')
            prefix=Path('validation_sync')/f'ConeRidge64_{phase}_v1_20261008';targets={};bindings={}
            for source in sources:
                data=source.read_bytes();assert not sync.SECRET.search(data),source;digest=hashlib.sha256(data).hexdigest()
                relative=source.relative_to(ROOT) if source.is_relative_to(ROOT) else Path('external_metadata')/(digest+'_'+source.name)
                target=(prefix/relative).as_posix();targets[target]=data
                bindings[str(source)]={'published_path':target,'raw_sha256':digest,'original_bytes':len(data)}
            targets[(prefix/'.gitattributes').as_posix()]=b'* -text\n'
            targets[(prefix/'manifest.json').as_posix()]=sync.encoded({'status':'actual_constrained_ridge_controls_passed',
                'at_local':sync.now(),'phase':phase,'files':bindings,'actual_completed_controls':counts,
                'native_recipe_v1_unchanged':True,'independent_BVLS_only_boundary_roundoff_checked_and_recorded':True,
                'failed_strict_bound_control_v1_retained':True,'new_official_scores':0,'test_labels_read':False,
                'selected_candidate_not_yet_qualified':True,'global_exhaustion_not_established':True})
            for name,data in targets.items():sync.atomic(sync.WORKTREE/name,data)
            names=sorted(targets)
            for left in range(0,len(names),50):sync.git('add','-f','--',*names[left:left+50])
            assert set(sync.git('-c','core.quotepath=false','diff','--cached','--name-only').splitlines())==set(names)
            sync.git('-c','maintenance.auto=false','-c','gc.auto=0','commit','-m','同步约束岭回归真实校验及保留失败记录 '+phase,timeout=180)
            commit=sync.git('rev-parse','HEAD');hashes={name:hashlib.sha256(data).hexdigest() for name,data in targets.items()}
            assert helpers.blob_hashes(commit,hashes)==hashes
            sync.git('push','origin','HEAD:refs/heads/main',timeout=180);helpers.verify_main(commit);helpers.watcher.advance_source_index(commit);scope.reverify()
            create(out/'receipt.json',{'status':'pushed_and_remote_head_verified','at_local':sync.now(),'branch':'main','phase':phase,
                'commit':commit,'raw_git_blobs_verified':len(hashes),'actual_completed_controls':counts,'new_official_scores':0,
                'url':'https://github.com/Zagadka-3906/stock-return-prediction/tree/main/'+prefix.as_posix()})
            print('Constrained ridge '+phase+' verified on main: '+commit,flush=True)
    finally:
        for process in reversed(held):
            if process.is_running():process.resume()

if __name__=='__main__':
    for phase in ('probe','bank','causal'):publish(phase)
