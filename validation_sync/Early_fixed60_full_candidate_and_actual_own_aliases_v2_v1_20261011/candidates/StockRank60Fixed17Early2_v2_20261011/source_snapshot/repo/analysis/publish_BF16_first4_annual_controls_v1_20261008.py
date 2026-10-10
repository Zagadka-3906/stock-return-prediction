"""Publish four genuinely completed annual saved-model controls while the remaining fits continue."""
from pathlib import Path
import hashlib,sys
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from file_backed_hidden_git_runtime_20261007 import installed
from handoff_joint_goss_round97_full_execution_20261006 import suspended_idle
import publish_classifier_consensus_workflows_20261006 as helpers


def main():
    bank=Path('E:/赛题五_本机临时/neural_BF16_micro8192_bank6_v2_20261008');records=[]
    sources=[Path(__file__),A/'neural_BF16_micro8192_native_v1_20261008.py',A/'train_neural_BF16_micro8192_bank6_v2_20261008.py',bank/'protocol.json']
    for year in (2020,2021,2022,2023):
        folder=bank/str(year);path=folder/'info.json';info=read(path)
        assert info['status']=='passed_actual_complete_mature_BF16_micro_annual_model' and info['year']==year
        assert info['actual_full_annual_reload_prediction_bits_exact'] and info['actual_cold80_prefix_bits_exact']
        assert not info['test_labels_read'] and info['training_meta']['actual_future_training_label_poisoning_population_exact']
        assert sha(folder/'model.joblib')==info['model_sha256']
        assert sha(folder/'raw.parquet')==info['prediction_sha256']
        meta=info['training_meta'];assert meta['last']<meta['cutoff_exclusive'] and meta['last_label_end']<=meta['cutoff_exclusive']
        sources += [path,folder/'frozen_training_inputs.json'];records.append(info)
    original=A/'service_owned_workflows_20261006/actual_neural_BF16_micro8192_bank6_v2_20261008/native_launch.json';assert owned(read(original));sources.append(original)
    sources=list(dict.fromkeys(sources));pins={str(p):sha(p) for p in sources}
    out=A/'BF16_first4_annual_controls_main_v1_20261008';assert not out.exists();out.mkdir()
    create(out/'frozen_before_main_publication.json',{'input_sha256':pins,'actual_completed_annual_models':4,
        'actual_years':[2020,2021,2022,2023],'records':records,'new_official_scores':0,
        'actual2024_2025_fits_and_full5_independent_GPU_controls_and_candidate_qualification_pending':True,'test_labels_read':False})
    held=[]
    try:
        row=read(A/'service_owned_workflows_20261006/main_publisher_v8_20261008/native_launch.json')
        parent,worker,idle=suspended_idle(row,'    main (watch_validations_main_v7_20261006.py:71)');held.extend((worker,parent));create(out/'actual_idle_main_hold.json',idle)
        from win32_read_handle_hash_cache_with_filename_v2_20261006 import LockedReadHashCache
        with installed(out/'file_backed_git'),LockedReadHashCache(pins) as scope:
            sync=helpers.sync;helpers.verify_main(sync.git('rev-parse','HEAD'));assert not sync.git('status','--porcelain')
            prefix=Path('validation_sync/BF16_first4_annual_controls_v1_20261008');targets={};bindings={}
            for source in sources:
                data=source.read_bytes();assert not sync.SECRET.search(data),source
                relative=source.relative_to(ROOT) if source.is_relative_to(ROOT) else Path('external_E_metadata')/source.relative_to(bank)
                target=(prefix/relative).as_posix();targets[target]=data
                bindings[str(source)]={'published_path':target,'raw_sha256':hashlib.sha256(data).hexdigest()}
            targets[(prefix/'.gitattributes').as_posix()]=b'* -text\n'
            targets[(prefix/'manifest.json').as_posix()]=sync.encoded({'status':'passed_actual4_completed_mature_annual_models_full_reload_and_cold80_controls',
                'at_local':sync.now(),'files':bindings,'actual_years':[2020,2021,2022,2023],'actual_native_models':records,
                'all_native_model_and_stored_prediction_payload_sha_rechecked':True,'new_official_scores':0,
                'actual2024_2025_fits_and_full5_independent_GPU_oracles_not_yet_claimed':True,
                'remaining_original_GPU_fitter_owned_live_unchanged':True,'new_future_X_and_Y_read':False,'main_only':True})
            for name,data in targets.items():sync.atomic(sync.WORKTREE/name,data)
            names=sorted(targets)
            for left in range(0,len(names),50):sync.git('add','-f','--',*names[left:left+50])
            assert set(sync.git('-c','core.quotepath=false','diff','--cached','--name-only').splitlines())==set(names)
            sync.git('-c','maintenance.auto=false','-c','gc.auto=0','commit','-m','同步已完成四个成熟年度神经模型的完整重载、冷80及源数据复核记录',timeout=180)
            commit=sync.git('rev-parse','HEAD');hashes={name:hashlib.sha256(data).hexdigest() for name,data in targets.items()};assert helpers.blob_hashes(commit,hashes)==hashes
            sync.git('push','origin','HEAD:refs/heads/main',timeout=180);helpers.verify_main(commit);helpers.watcher.advance_source_index(commit);scope.reverify()
            create(out/'receipt.json',{'status':'pushed_and_remote_head_verified','at_local':sync.now(),'branch':'main','commit':commit,
                'raw_git_blobs_verified':len(hashes),'actual_completed_annual_models':4,'new_official_scores':0,
                'url':'https://github.com/Zagadka-3906/stock-return-prediction/tree/main/'+prefix.as_posix()})
            assert owned(read(original));print('Actual four completed annual model controls published while remaining GPU fit continues: '+commit,flush=True)
    finally:
        for process in reversed(held):
            if process.is_running():process.resume()


if __name__=='__main__':main()
