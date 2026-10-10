"""Publish the already completed153 ranking/QA and finish qualification; no scientific rerun."""
from pathlib import Path
import sys,os,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
OUT=Path('E:/赛题五_本机临时/BF16Medium153_completed_QA_main_recovery_v43_20261009')

def main():
    import publish_classifier_consensus_workflows_20261006 as helpers
    from handoff_joint_goss_round97_full_execution_20261006 import suspended_idle
    folder=A/'optimization_20261003_r153';failure=read(folder/'full_registration_failure.json')
    assert 'lossless_ranking_display_qa_v64_20261007' in failure['error']
    previous=read(folder/'provenance_scope_execution.json');assert previous['status']=='passed'
    assert previous['all_original_six_view_browser_and_candidate_manifest_QA_passed']
    qa=A/'lossless_ranking_display_qa_v64_20261009/round153/verification.json'
    controls=A/'actual_QA_collector_path_controls_v43_20261009.json'
    for f,d in read(controls)['input_sha256'].items():assert sha(f)==d,f
    assert read(qa)['original_full_QA_result']['new_round_records']==78
    assert not (folder/'full_registration_execution.json').exists()
    OUT.mkdir(exist_ok=False);held=[]
    try:
        row=read(A/'service_owned_workflows_20261006/main_publisher_v10_20261009/native_launch.json');assert owned(row)
        parent,worker,idle=suspended_idle(row,'    main (watch_validations_main_v7_20261006.py:71)');held.extend((worker,parent))
        create(OUT/'actual_idle_watcher_hold.json',idle)
        from win32_read_handle_hash_cache_with_filename_v2_20261006 import LockedReadHashCache
        with LockedReadHashCache(previous['input_sha256']) as scope:
            scope.reverify()
            from publish_BF16Medium78_round153_full_validation_20261009 import main as publish
            publish();scope.reverify()
        receipt=read(A/'github_validation_sync_main_20261005/round153_receipt.json')
        assert receipt['status']=='pushed_and_remote_head_verified' and receipt['scored_records']==78 and receipt['connected_records']==15310
        result={'status':'passed','at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),
            'existing_official_scores_registered':78,'full_rankings_all_original_QA_and_main_publication_completed':True,
            'recovery_from_existing_passed_original_six_view_QA_only':True,'actual_QA_path':str(qa),'actual_QA_sha256':sha(qa),
            'original_failed_full1_preserved':True,'scientific_workers_suspended_stopped_or_restarted':0,
            'new_quality_scores_by_registration':0,'new_inference_claimed_by_registration':False,
            'global_goal_or_resource_exhaustion_claimed':False,'test_labels_read':False,'main_receipt':receipt}
        create(folder/'full_registration_execution.json',result);create(OUT/'verification.json',result)
        print({'status':'passed_actual153_completed_QA_main_recovery','commit':receipt['commit'],'new_scientific_scores':0},flush=True)
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
    from actual_QA_collector_path_runtime_v43_20261009 import installed as qa_paths
    from external_publication_source_paths_runtime_v1_20261009 import installed as publication_paths
    log=Path('E:/赛题五_本机临时/BF16Medium153_completed_QA_main_safe_v43_20261009')
    with safe(log),serial(log/'serial_mutex.json'),git_io(log/'file_backed_git'),qa_paths(),publication_paths():main()
