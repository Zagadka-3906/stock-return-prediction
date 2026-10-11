"""Publish completed139 source preflight, eight owned queues and immutable handoff10 to main."""
from pathlib import Path
import gzip,hashlib,sys
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from file_backed_hidden_git_runtime_20261007 import installed
from handoff_joint_goss_round97_full_execution_20261006 import suspended_idle
import publish_classifier_consensus_workflows_20261006 as helpers


def main():
    import prepare_HuberCrossFamily112_round139_sources_v1_20261008 as generator
    routes=A/'HuberCrossFamily112_prospective_routes_v1_20261008.json';proof=read(routes)
    assert proof['actual_prospective_sources']==24 and proof['actual_graph_controls']==1635 and proof['actual_physical_model_count_controls']==8
    handoff=A/'actual_optimization_handoff_v10_20261008.json';assert read(handoff)['goal_active_not_paused_complete_or_blocked']
    sources=[Path(__file__),routes,handoff,A/'actual_optimization_handoff_v10_20261008.md',A/'record_actual_optimization_handoff_v10_20261008.py',
        A/'HuberCrossFamily139_complete_dependency_plan_v1_20261008.json',A/'HuberCrossFamily139_complete_hidden_launches_v1_20261008.json',
        A/'HuberCrossFamily139_junction_requests_v1_20261008.json',A/'archive_HuberCrossFamily139_completed_scoring_CSV_v1_20261008.py',
        A/'actual_HuberCrossFamily139_completed_CSV_archivist_hidden_launch_v1_20261008.json',
        A/'monitor_neural135_CrossFamily136_Huber137_BF16reverse138_HuberCross139_v7_20261008.py',
        A/'actual_optimization135136137138139_progress_hidden_launch_v7_20261008.json',
        A/'HuberCrossFamily139_cross_volume_byte_probe_v1.bin',*[p for p in generator.source_paths() if p.is_file()]]
    for path,digest in proof['input_sha256'].items():assert sha(path)==digest,path
    for name,row in read(A/'HuberCrossFamily139_complete_hidden_launches_v1_20261008.json')['launches'].items():
        assert owned(row) and row['actual_native_console_handle']==0,name
        folder=A/'service_owned_workflows_20261006'/name;sources += [folder/'native_launch.json',folder/'job_definition.json']
    sources=list(dict.fromkeys(sources));pins={str(p):sha(p) for p in sources}
    output=A/'HuberCrossFamily139_receiver_preflight_main_v1_20261008';assert not output.exists();output.mkdir()
    create(output/'frozen_before_main_publication.json',{'input_sha256':pins,'actual_prospective_sources':24,
        'actual_complete_graph_controls':1635,'actual_physical_SHA_count_controls':8,'new_official_scores':0,'test_labels_read':False})
    held=[]
    try:
        row=read(A/'service_owned_workflows_20261006/main_publisher_v8_20261008/native_launch.json')
        parent,worker,idle=suspended_idle(row,'    main (watch_validations_main_v7_20261006.py:71)');held.extend((worker,parent))
        create(output/'actual_idle_main_hold.json',idle)
        from win32_read_handle_hash_cache_with_filename_v2_20261006 import LockedReadHashCache
        with installed(output/'file_backed_git'),LockedReadHashCache(pins) as scope:
            sync=helpers.sync;helpers.verify_main(sync.git('rev-parse','HEAD'));assert not sync.git('status','--porcelain')
            prefix=Path('validation_sync/HuberCrossFamily139_receiver_preflight_v1_20261008');targets={};bindings={}
            for source in sources:
                data=source.read_bytes();assert not sync.SECRET.search(data),source
                digest=hashlib.sha256(data).hexdigest();target=(prefix/source.relative_to(ROOT)).as_posix();raw_size=len(data)
                if len(data)>=5*1024**2:data=gzip.compress(data,mtime=0);target+='.gz';assert hashlib.sha256(gzip.decompress(data)).hexdigest()==digest
                targets[target]=data;bindings[str(source)]={'published_path':target,'raw_sha256':digest,'original_bytes':raw_size}
            targets[(prefix/'.gitattributes').as_posix()]=b'* -text\n'
            targets[(prefix/'manifest.json').as_posix()]=sync.encoded({'status':'passed_actual24_sources1635_graphs_and_eight_owned139_queue_handoff10',
                'at_local':sync.now(),'round':139,'files':bindings,'expected_official_cases':112,'actual_prospective_sources':24,
                'actual_complete_graph_controls':1635,'actual_baseline_controls':9,'actual_same_S_controls':6,'actual_physical_model_SHA_count_controls':8,
                'completed_preliminary_native_and_full_historical_controls_main_receipt':read(A/'HuberCrossFamily139_preliminary_historical_main_v1_20261008/receipt.json'),
                'current139_complete_quality_pipeline_queued':True,'full112_quality_candidate_QA50_main_still_required':True,
                'new_official_scores':0,'new_fits':0,'test_labels_read':False,'global_exhaustion_not_claimed':True,'main_only':True})
            for name,data in targets.items():sync.atomic(sync.WORKTREE/name,data)
            names=sorted(targets)
            for left in range(0,len(names),50):sync.git('add','-f','--',*names[left:left+50])
            assert set(sync.git('-c','core.quotepath=false','diff','--cached','--name-only').splitlines())==set(names)
            sync.git('-c','maintenance.auto=false','-c','gc.auto=0','commit','-m','同步第139轮24接收器1635父图与8模型去重检查、完整八服务队列及交接10',timeout=180)
            commit=sync.git('rev-parse','HEAD');hashes={name:hashlib.sha256(data).hexdigest() for name,data in targets.items()}
            assert helpers.blob_hashes(commit,hashes)==hashes
            sync.git('push','origin','HEAD:refs/heads/main',timeout=180);helpers.verify_main(commit);helpers.watcher.advance_source_index(commit);scope.reverify()
            create(output/'receipt.json',{'status':'pushed_and_remote_head_verified','at_local':sync.now(),'branch':'main','commit':commit,
                'raw_git_blobs_verified':len(hashes),'new_official_scores':0,
                'url':'https://github.com/Zagadka-3906/stock-return-prediction/tree/main/'+prefix.as_posix()})
            print('Actual139 receiver checks and full queue handoff published: '+commit,flush=True)
    finally:
        for process in reversed(held):
            if process.is_running():process.resume()


if __name__=='__main__':main()
