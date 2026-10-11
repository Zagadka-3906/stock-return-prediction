"""Publish actual24/8/40/40 controls and failed bank1 after143 publication releases main."""
from pathlib import Path
import gzip,hashlib,sys,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from file_backed_hidden_git_runtime_20261007 import installed
from handoff_joint_goss_round97_full_execution_20261006 import suspended_idle
import publish_classifier_consensus_workflows_20261006 as helpers
def closed(name):
    folder=A/'service_owned_workflows_20261006'/name
    while owned(read(folder/'native_launch.json')):time.sleep(10)
    assert read(folder/'service_execution.json')['status']=='passed',name
    return folder
def main():
    for name in ('nonflag_ConeRidgeAlpha8_64_bank40_v2_20261008','ConeRidgeAlpha40_causal_refit_v2_20261008','ConeRidgeFine68_round143_full_registration_v2_20261008'):closed(name)
    counts={};sources=[Path(__file__),ROOT/'后续选模标准.md']
    for pointer_name in ('actual_nonflag_ConeRidgeAlpha8_64_small_location_v1_20261008.json',
        'actual_nonflag_ConeRidgeAlpha8_64_actual200k_location_v1_20261008.json',
        'actual_nonflag_ConeRidgeAlpha8_64_bank40_location_v2_20261008.json','actual_ConeRidgeAlpha40_causal_refit_location_v2_20261008.json'):
        pointer=A/pointer_name;folder=Path(read(pointer)['output']);proof=read(folder/'verification.json')
        assert sha(folder/'verification.json')==read(pointer)['verification_sha256']
        if 'small_location' in pointer_name:
            assert proof['actual_synthetic_native_fits']==24 and proof['actual_prefix_controls']==144
            counts.update(synthetic_fits=24,synthetic_prefix_controls=144)
        elif 'actual200k_location' in pointer_name:
            assert proof['actual_probe_native_fits']==8 and proof['own_full_window_rows_rechecked']==4969483
            counts.update(actual200003_fits=8,actual200003_prefix_controls=48)
        elif 'bank40_location' in pointer_name:
            assert proof['actual_native_fits']==40 and proof['actual_full_OOF_heads']==8
            assert {r['year'] for r in proof['actual_models']}==set(range(2021,2026))
            counts.update(own_mature_annual_fits=40,full5635800_OOF_heads=8)
        else:
            assert proof['actual_causal_same_configuration_refit_controls']==40 and proof['actual_maturity_windows']==5
            counts.update(same_configuration_causal_refits=40,maturity_windows=5)
        for path,digest in proof['input_sha256'].items():assert sha(path)==digest,path
        sources.extend([pointer,*folder.rglob('*.json')])
    for pattern in ('*ConeRidgeAlpha*20261008.py','*ConeRidgeAlpha*20261008.json'):
        sources.extend(A.glob(pattern))
    sources += [A/'monitor_actual_optimization135_to144_v14_20261008.py',A/'actual_optimization135_to144_progress_hidden_launch_v14_20261008.json',
        A/'recover_ConeRidgeFine143_E_snapshot_sealing_v2_20261008.py',A/'ConeRidgeFine143_E_snapshot_sealing_recovery_v2_20261008.json',
        A/'ConeRidgeFine143_E_snapshot_sealing_hidden_launches_v2_20261008.json',A/'seal_ConeRidgeFine68_selected_candidate_v2_20261008.py',
        A/'run_ConeRidgeFine68_round143_full_registration_v2_20261008.py']
    for name in ('nonflag_ConeRidgeAlpha8_64_bank40_v1_20261008','ConeRidgeAlpha40_causal_refit_v1_20261008',
        'nonflag_ConeRidgeAlpha8_64_bank40_v2_20261008','ConeRidgeAlpha40_causal_refit_v2_20261008',
        'ConeRidgeFine68_selected_candidate_sealing_v1_20261008','ConeRidgeFine68_round143_full_registration_v1_20261008',
        'ConeRidgeFine68_selected_candidate_sealing_v2_20261008','ConeRidgeFine68_round143_full_registration_v2_20261008'):
        folder=A/'service_owned_workflows_20261006'/name;assert not owned(read(folder/'native_launch.json'))
        sources.extend(folder.glob('*.json'));sources.extend(folder.glob('*.log'))
    sources=list(dict.fromkeys(sources));pins={str(p):sha(p) for p in sources}
    out=A/'ConeRidgeAlpha8_completed_controls_main_v1_20261008';assert not out.exists();out.mkdir()
    create(out/'frozen_before_main_publication.json',{'input_sha256':pins,'actual_completed_controls':counts,
        'actual144_quality_scores':0,'all_failed_sources_retained':True,'test_labels_read':False})
    held=[]
    try:
        row=read(A/'service_owned_workflows_20261006/main_publisher_v8_20261008/native_launch.json')
        parent,worker,idle=suspended_idle(row,'    main (watch_validations_main_v7_20261006.py:71)');held.extend((worker,parent));create(out/'actual_idle_main_hold.json',idle)
        from win32_read_handle_hash_cache_with_filename_v2_20261006 import LockedReadHashCache
        with installed(out/'file_backed_git'),LockedReadHashCache(pins) as scope:
            sync=helpers.sync;previous=sync.git('rev-parse','HEAD');helpers.verify_main(previous);assert not sync.git('status','--porcelain')
            prefix=Path('validation_sync/ConeRidgeAlpha8_completed_controls_v1_20261008');payload={};bindings={}
            for source in sources:
                data=source.read_bytes();assert not sync.SECRET.search(data),source;digest=hashlib.sha256(data).hexdigest()
                relative=source.relative_to(ROOT) if source.is_relative_to(ROOT) else Path('external_metadata')/(digest+'_'+source.name)
                target=(prefix/relative).as_posix();size=len(data)
                if size>=5*1024**2:data=gzip.compress(data,mtime=0);target+='.gz';assert hashlib.sha256(gzip.decompress(data)).hexdigest()==digest
                payload[target]=data;bindings[str(source)]={'published_path':target,'raw_sha256':digest,'original_bytes':size}
            payload[(prefix/'.gitattributes').as_posix()]=b'* -text\n'
            payload[(prefix/'manifest.json').as_posix()]=sync.encoded({'status':'actual_eight_alpha_numeric_bank_and_causal_controls_passed',
                'at_local':sync.now(),'files':bindings,'actual_completed_controls':counts,'actual144_official_scores':0,
                'native_solver_AST_changed_only_declared_alpha_tuple':True,'new_alpha_values':[.001,.003,.03,.3],
                'bank1_pointer_failure_and_seal1_E_path_failure_preserved':True,
                'diagnostic_only_bank_field_actual4025_is_boolean_for_actual_info_year2025':True,
                'actual144_blueprint100_and9_adapter_contracts_frozen':True,'actual_full144_quality_and_candidate_still_required':True,
                'main_only':True,'test_labels_read':False,'global_exhaustion_claimed':False})
            for target,data in payload.items():sync.atomic(sync.WORKTREE/target,data)
            names=sorted(payload)
            for start in range(0,len(names),50):sync.git('add','-f','--',*names[start:start+50])
            assert set(sync.git('-c','core.quotepath=false','diff','--cached','--name-only').splitlines())==set(names)
            sync.git('-c','maintenance.auto=false','-c','gc.auto=0','commit','-m','同步8个新增正则参数头的40成熟年度模型、40因果检查与真实探针及失败修复证据',timeout=180)
            commit=sync.git('rev-parse','HEAD');expected={n:hashlib.sha256(data).hexdigest() for n,data in payload.items()};assert helpers.blob_hashes(commit,expected)==expected
            sync.git('push','origin','HEAD:refs/heads/main',timeout=180);helpers.verify_main(commit);helpers.watcher.advance_source_index(commit);scope.reverify()
            create(out/'receipt.json',{'status':'pushed_and_remote_head_verified','at_local':sync.now(),'branch':'main','commit':commit,
                'raw_git_blobs_verified':len(expected),'actual_completed_controls':counts,'actual144_official_scores':0,
                'url':'https://github.com/Zagadka-3906/stock-return-prediction/tree/main/'+prefix.as_posix()})
            print('All eight alpha real40 bank40 causal proofs published: '+commit,flush=True)
    finally:
        for process in reversed(held):
            if process.is_running():process.resume()
if __name__=='__main__':main()
