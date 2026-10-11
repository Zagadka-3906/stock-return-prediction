"""Publish the already-passed full150 QA without repeating scoring, candidate inference, or browser QA."""
from pathlib import Path
import sys,os,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
OUT=Path('E:/赛题五_本机临时/HuberSparse150_publication_only_v32_20261009')
def main():
    from external_publication_source_paths_runtime_v1_20261009 import corrected
    from handoff_joint_goss_round97_full_execution_20261006 import suspended_idle
    from verified_TLS_Git_retry_runtime_v2_20261008 import installed
    import prepare_HuberSparse59_round150_sources_v2_20261009 as g
    folder=A/'optimization_20261003_r150';protocol=read(folder/'protocol.json')
    qa=A/'lossless_ranking_display_qa_v61_20261007/round150/verification.json'
    assert read(qa)['status']=='passed_original_full_ranking_QA_on_lossless_page'
    interaction=read(qa.parent/'qa/interaction_result.json');assert interaction['status']=='passed' and interaction['connected_records']==15144
    assert read(folder/'provenance_scope_execution.json')['status']=='passed'
    assert read(folder/'full_registration_failure.json')['status']=='failed_preserved_HuberSparse59_full150_registration'
    for p,d in protocol['input_sha256'].items():assert sha(p)==d,p
    for p,d in read(qa).get('input_sha256',{}).items():assert sha(p)==d,p
    OUT.mkdir(exist_ok=False)
    inputs=[Path(__file__),A/'external_publication_source_paths_runtime_v1_20261009.py',A/'external_publication_source_paths_runtime_v1_20261009.json',qa,qa.parent/'qa/interaction_result.json',
        folder/'protocol.json',folder/'provenance_scope_execution.json',folder/'full_registration_failure.json',A/'HuberSparse59_actual_source_paths_before_registration_retry30_20261009.json',
        A/'publish_HuberSparse59_round150_full_validation_20261008.py']
    create(OUT/'frozen_before_retry.json',{'status':'actual_completed150_QA_and_protocol_revalidated_before_publication_only_retry',
        'input_sha256':{str(p):sha(p) for p in inputs},'new_quality_scores':0,'new_inference':0,'browser_QA_repeated':False,'test_labels_read':False})
    original_paths=g.source_paths
    paths=list(read(A/'HuberSparse59_actual_source_paths_before_registration_retry30_20261009.json')['input_sha256'])
    g.source_paths=lambda:list(dict.fromkeys([*original_paths(),*(Path(p) for p in paths),*inputs,OUT/'frozen_before_retry.json']))
    source=A/'publish_HuberSparse59_round150_full_validation_20261008.py'
    ns={'__file__':str(source),'__name__':'actual150_publication_only_retry32'}
    exec(compile(corrected(source.read_text(encoding='utf8')),str(Path(__file__)),'exec'),ns)
    held=[]
    try:
        row=read(A/'service_owned_workflows_20261006/main_publisher_v9_20261009/native_launch.json');assert owned(row)
        parent,worker,idle=suspended_idle(row,'    main (watch_validations_main_v7_20261006.py:71)');held.extend((worker,parent))
        create(OUT/'actual_idle_main_hold.json',{'identity':row,'stack':idle,'scientific_workers_held':0})
        from win32_read_handle_hash_cache_with_filename_v2_20261006 import LockedReadHashCache
        with LockedReadHashCache(protocol['input_sha256']) as scope,installed(OUT/'file_backed_git'):
            ns['main']();scope.reverify()
        receipt=read(A/'github_validation_sync_main_20261005/round150_receipt.json');assert receipt['status']=='pushed_and_remote_head_verified'
        create(folder/'full_registration_execution.json',{'status':'passed','at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),
            'existing_official_scores_registered':59,'full_rankings_all_original_QA_and_main_publication_completed':True,
            'scientific_workers_suspended_stopped_or_restarted':0,'new_quality_scores_by_registration':0,'new_inference_claimed_by_registration':False,
            'selected_candidate_actual_new_inference':False,'publication_only_recovery':True,'passed_browser_QA_repeated':False,
            'actual_recovery_evidence':str(OUT/'frozen_before_retry.json'),'global_goal_or_resource_exhaustion_claimed':False,'test_labels_read':False})
        create(OUT/'verification.json',{'status':'passed_actual150_previously_completed_science_QA_and_new_verified_main_publication',
            'commit':receipt['commit'],'input_sha256':{str(p):sha(p) for p in inputs},'new_quality_scores':0,'new_inference':0,'test_labels_read':False})
    finally:
        g.source_paths=original_paths
        for p in reversed(held):
            if p.is_running():p.resume()
        create(OUT/'held_idle_main_resumed.json',{'scientific_workers_held':0,'held_processes':len(held),'resumed_in_finally':True})
if __name__=='__main__':
    count=int(os.environ.get('GIT_CONFIG_COUNT','0'))
    for i,(k,v) in enumerate((('http.proxy','http://127.0.0.1:7897'),('http.version','HTTP/1.1'))):os.environ[f'GIT_CONFIG_KEY_{count+i}']=k;os.environ[f'GIT_CONFIG_VALUE_{count+i}']=v
    os.environ['GIT_CONFIG_COUNT']=str(count+2)
    from lossless_chunked_safe_main_runtime_v1_20261009 import installed as safe
    from serial_main_publication_mutex_v1_20261009 import installed as serial
    with safe(OUT/'safe_publication'),serial(OUT/'serial_publication_mutex.json'):main()
