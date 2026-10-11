"""Recover receipts from independently rehashed committed blobs after the old watcher index incident."""
from pathlib import Path
import sys,os,time,json,hashlib,gzip,subprocess
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
OUT=Path('E:/赛题五_本机临时/actual150_and65_remote_reconciliation_v36_20261009')
def batch(commit,paths):
    import publish_classifier_consensus_workflows_20261006 as h
    names=sorted(paths);request=''.join(f'{commit}:{p}\n' for p in names).encode('utf8')
    response=OUT/(commit+'_git_blobs.bin')
    with response.open('xb') as writer:
        subprocess.run(['git','cat-file','--batch'],cwd=h.sync.WORKTREE,input=request,stdout=writer,stderr=subprocess.PIPE,
            check=True,creationflags=subprocess.CREATE_NO_WINDOW)
    with response.open('rb') as reader:
        for p in names:
            header=reader.readline().split();assert len(header)==3 and header[1]==b'blob',p
            data=reader.read(int(header[2]));assert reader.read(1)==b'\n';yield p,data
        assert not reader.read(1)
def main():
    import publish_classifier_consensus_workflows_20261006 as h
    OUT.mkdir(exist_ok=False)
    restored=read(A/'main_watcher_safe_handoff_and_index_restore_v34_20261009.json')
    assert restored['status']=='passed_exact_preexisting_index_restored_and_owned_idle_watcher_replaced'
    assert sha(ROOT/'.git/index')==restored['restored_original_index_sha256']
    receipt150=read(A/'github_validation_sync_main_20261005/round150_receipt.json');commit150=receipt150['commit']
    current=h.sync.git('rev-parse','HEAD');h.verify_main(current);h.sync.git('merge-base','--is-ancestor',commit150,current)
    prefix150='validation_sync/round150';manifest150=json.loads(h.sync.git('show',commit150+':'+prefix150+'/manifest.json'))
    expected={p:v['sha256'] for p,v in manifest150['exported_files'].items()}
    for p,data in batch(commit150,expected):assert hashlib.sha256(data).hexdigest()==expected[p],p
    assert manifest150['scored_records']==59 and manifest150['connected_records']==15144
    assert manifest150['metrics']['final_score']==.4511917507998099
    qa=A/'lossless_ranking_display_qa_v61_20261007/round150/verification.json';q=read(qa)
    assert q['status']=='passed_all_original_full_ranking_QA_and_lossless_browser_node_checks'
    assert q['all_original_provenance_candidate_manifest_sorting_and_six_view_checks_passed']
    folder=A/'optimization_20261003_r150';protocol=read(folder/'protocol.json')
    for p,d in protocol['input_sha256'].items():assert sha(p)==d,p
    prefix65='validation_sync/two_seed154_recovery_v65_20261009'
    manifest65=json.loads(h.sync.git('show',current+':'+prefix65+'/manifest.json'))
    frozen=read(Path('E:/赛题五_本机临时/two_seed154_recovery_main_v65_20261009/frozen_before_main_publication.json'))
    assert manifest65['files']==frozen['files']
    paths={v['published_path']:v for v in frozen['files'].values()}
    for p,data in batch(current,paths):
        raw=gzip.decompress(data) if p.endswith('.gz') else data
        assert hashlib.sha256(raw).hexdigest()==paths[p]['raw_sha256'] and len(raw)==paths[p]['original_bytes'],p
    create(OUT/'verification.json',{'status':'passed_independent150_and65_committed_blob_rehash_after_exact_user_index_restore',
        'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'commit150':commit150,'current_main':current,
        'actual150_git_blob_count':len(expected),'actual65_source_blob_count':len(paths),'actual150_official_cases':59,
        'actual150_connected_records':15144,'original_six_view_QA_preserved':True,'input_sha256':{str(p):sha(p) for p in (Path(__file__),qa,folder/'protocol.json',
            A/'main_watcher_safe_handoff_and_index_restore_v34_20261009.json')},'new_scores':0,'new_inference':0,'test_labels_read':False})
    create(A/'two_seed154_recovery_main_v65_receipt_20261009.json',{'status':'pushed_and_remote_head_verified','at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),
        'branch':'main','commit':current,'raw_source_blobs_independently_reverified':len(paths),'original65_service_failure_preserved':True,
        'index_incident_and_exact_restore_evidence':str(A/'main_watcher_safe_handoff_and_index_restore_v34_20261009.json'),
        'reconciliation_evidence':str(OUT/'verification.json'),'url':'https://github.com/Zagadka-3906/stock-return-prediction/tree/main/'+prefix65})
    create(folder/'full_registration_execution.json',{'status':'passed','at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),
        'existing_official_scores_registered':59,'full_rankings_all_original_QA_and_main_publication_completed':True,
        'actual_remote_commit':commit150,'actual_new_candidate_inference':False,'new_quality_scores_by_registration':0,
        'new_inference_claimed_by_registration':False,'selected_candidate_actual_new_inference':False,
        'scientific_workers_suspended_stopped_or_restarted':0,'failed_original_full_publication_preserved':True,
        'original_user_index_restored_byte_exact':True,'reconciliation_evidence':str(OUT/'verification.json'),
        'global_goal_or_resource_exhaustion_claimed':False,'test_labels_read':False})
    print({'full150_passed':True,'main150':commit150,'main65':current,'blobs150':len(expected),'blobs65':len(paths)},flush=True)
if __name__=='__main__':
    count=int(os.environ.get('GIT_CONFIG_COUNT','0'))
    for i,(k,v) in enumerate((('http.proxy','http://127.0.0.1:7897'),('http.version','HTTP/1.1'))):os.environ[f'GIT_CONFIG_KEY_{count+i}']=k;os.environ[f'GIT_CONFIG_VALUE_{count+i}']=v
    os.environ['GIT_CONFIG_COUNT']=str(count+2)
    from verified_TLS_Git_retry_runtime_v2_20261008 import installed
    with installed(Path('E:/赛题五_本机临时/actual150_and65_remote_reconciliation_file_IO_v36_20261009')):main()
