"""Publish actual Huber probes and, separately, the completed ten-model bank to main."""
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
    names=['nonflag_SpectralGram64_actual200k_v1_20261008']
    pointers=['actual_nonflag_SpectralGram64_small_location_v1_20261008.json','actual_nonflag_SpectralGram64_actual200k_location_v1_20261008.json']
    if phase=='bank':
        names.append('nonflag_SpectralGram64_bank20_v1_20261008');pointers.append('actual_nonflag_SpectralGram64_bank20_location_v1_20261008.json')
    sources=[Path(__file__),A/'nonflag_SpectralGram64_streamed_v1_20261008.py',A/'nonflag_HuberIRLS64_own_window_v1_20261008.py',
        A/'verify_nonflag_SpectralGram64_small_v1_20261008.py',A/'verify_nonflag_SpectralGram64_actual200k_v1_20261008.py',
        A/'train_nonflag_SpectralGram64_bank20_v1_20261008.py',A/'prepare_nonflag_SpectralGram64_bank20_v1_20261008.py',
        A/'nonflag_SpectralGram64_bank20_plan_v1_20261008.json',A/'actual_nonflag_SpectralGram64_actual200k_hidden_launch_v1_20261008.json',
        A/'actual_nonflag_SpectralGram64_bank20_hidden_launch_v1_20261008.json',A/'nonflag_residual_HGB_preprocessing_20261007.py',
        A/'memory_bounded_numeric_preparation_20261007.py',A/'nonflag_residual_Ridge_codec_20261007.py',ROOT/'后续选模标准.md']
    for name in names:
        folder=closed(name);sources += list(folder.glob('*.json'))+list(folder.glob('*.log'))
    actual_full_fits=0
    for filename in pointers:
        path=A/filename;pointer=read(path);folder=Path(pointer['output']);proof=read(folder/'verification.json')
        assert sha(folder/'verification.json')==pointer['verification_sha256'] and proof['actual_official_scores']==0
        if filename==pointers[0]:assert proof['actual_synthetic_native_fits']==8
        elif filename==pointers[1]:assert proof['actual_probe_native_fits']==4 and proof['own_full_window_rows_rechecked']==4969483
        else:
            assert proof['actual_native_fits']==20 and proof['actual_full_OOF_heads']==4
            actual_full_fits=20
        sources += [path,*folder.rglob('*.json')]
    sources=list(dict.fromkeys(sources));assert all(path.suffix in ('.py','.json','.log','.md') for path in sources)
    pins={str(p):sha(p) for p in sources};out=A/'nonflag_SpectralGram64_controls_main_v1_20261008'/phase
    assert not out.exists();out.mkdir(parents=True)
    create(out/'frozen_before_main_publication.json',{'input_sha256':pins,'phase':phase,'actual_official_scores':0,
        'actual_synthetic_fits':8,'actual200k_probe_fits':4,'actual_full_own_mature_fits':actual_full_fits,
        'selected_future_candidate_complete_round_not_yet_qualified':True,'test_labels_read':False})
    held=[]
    try:
        row=read(A/'service_owned_workflows_20261006/main_publisher_v8_20261008/native_launch.json')
        parent,worker,idle=suspended_idle(row,'    main (watch_validations_main_v7_20261006.py:71)');held.extend((worker,parent))
        create(out/'actual_idle_main_hold.json',idle)
        from win32_read_handle_hash_cache_with_filename_v2_20261006 import LockedReadHashCache
        with installed(out/'file_backed_git'),LockedReadHashCache(pins) as scope:
            sync=helpers.sync;helpers.verify_main(sync.git('rev-parse','HEAD'));assert not sync.git('status','--porcelain')
            prefix=Path('validation_sync')/f'nonflag_SpectralGram64_{phase}_20261008';targets={};bindings={}
            for source in sources:
                data=source.read_bytes();assert not sync.SECRET.search(data),source
                digest=hashlib.sha256(data).hexdigest()
                relative=source.relative_to(ROOT) if source.is_relative_to(ROOT) else Path('external_metadata')/(digest+'_'+source.name)
                target=(prefix/relative).as_posix();targets[target]=data
                bindings[str(source)]={'published_path':target,'raw_sha256':digest,'original_bytes':len(data)}
            targets[(prefix/'.gitattributes').as_posix()]=b'* -text\n'
            targets[(prefix/'manifest.json').as_posix()]=sync.encoded({'status':'actual_SpectralGram64_numeric_native_controls_passed',
                'at_local':sync.now(),'phase':phase,'files':bindings,'actual_synthetic_native_fits':8,'actual200k_probe_native_fits':4,
                'actual_own_mature_full_native_fits':actual_full_fits,'actual_full_OOF_heads':4 if actual_full_fits else 0,
                'actual_official_scores':0,'selected_candidate_and_complete_parent_pipeline_not_yet_qualified':True,
                'full_bank_dispatched_on_E':True,'actual_spectral_native_and_probe_sources_preserved':True,
                'test_labels_read':False,'global_optimization_and_resource_exhaustion_not_claimed':True})
            for name,data in targets.items():sync.atomic(sync.WORKTREE/name,data)
            names=sorted(targets)
            for left in range(0,len(names),50):sync.git('add','-f','--',*names[left:left+50])
            assert set(sync.git('-c','core.quotepath=false','diff','--cached','--name-only').splitlines())==set(names)
            sync.git('-c','maintenance.auto=false','-c','gc.auto=0','commit','-m','同步Spectral64真实SVD数值与原生重载检查 '+phase,timeout=180)
            commit=sync.git('rev-parse','HEAD');hashes={n:hashlib.sha256(d).hexdigest() for n,d in targets.items()}
            assert helpers.blob_hashes(commit,hashes)==hashes
            sync.git('push','origin','HEAD:refs/heads/main',timeout=180);helpers.verify_main(commit);helpers.watcher.advance_source_index(commit);scope.reverify()
            create(out/'receipt.json',{'status':'pushed_and_remote_head_verified','at_local':sync.now(),'phase':phase,'branch':'main','commit':commit,
                'raw_git_blobs_verified':len(hashes),'actual_full_own_mature_fits':actual_full_fits,'actual_official_scores':0,
                'url':'https://github.com/Zagadka-3906/stock-return-prediction/tree/main/'+prefix.as_posix()})
            print('Actual Spectral64 '+phase+' controls published to main: '+commit,flush=True)
    finally:
        for process in reversed(held):
            if process.is_running():process.resume()


if __name__=='__main__':publish('probe');publish('bank')
