"""Reconcile the already committed/pushed159 without repeating science or overwriting the failure."""
from pathlib import Path
from datetime import datetime,timezone,timedelta
import sys,os,json,hashlib,time
A=Path(__file__).resolve().parent;ROOT=A.parent;sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
COMMIT='2e02e4b1970f0e916717b366106608a6735b2971'

def main():
    c=read(A/'current_user_runtime_control_20261010.json');read(A/'current_user_runtime_control_20261009.json')
    assert c['status']=='optimization_active_after_explicit_manual_resume' and datetime.now(timezone(timedelta(hours=8)))<datetime.fromisoformat(c['stop_at_local'])
    out=Path('E:/赛题五_本机临时/round159_existing_main_reconciliation_v1_20261010');out.mkdir(exist_ok=False)
    import publish_classifier_consensus_workflows_20261006 as h
    from serial_main_publication_mutex_v1_20261009 import installed as serial
    from verified_TLS_Git_retry_runtime_v2_20261008 import installed as git_io
    folder=A/'optimization_20261003_r159';qa_path=A/'lossless_ranking_display_qa_v70_20261009/round159/verification.json'
    failed=read(folder/'full_registration_failure.json');assert 'TimeoutExpired' in failed['error']
    scope=read(folder/'provenance_scope_execution.json');assert scope['status']=='passed' and scope['all_original_six_view_browser_and_candidate_manifest_QA_passed']
    qa=read(qa_path);assert qa['original_full_QA_result']['connected_records']==15614 and qa['original_full_QA_result']['new_round_records']==19
    assert read(folder/'protocol.json')['expected_scored_records']==19
    with serial(out/'serial_mutex.json') as mutex,git_io(out/'file_backed_git'):
        mutex.acquire()
        current=h.sync.git('rev-parse','HEAD');h.verify_main(current)
        h.sync.git('merge-base','--is-ancestor',COMMIT,current)
        manifest=json.loads(h.sync.git('show',COMMIT+':validation_sync/round159/manifest.json'))
        assert (manifest['scored_records'],manifest['connected_records'])==(19,15614)
        assert manifest['metrics']==read(folder/'calibrated_csv_official.json')['metrics']
        snapshot=read(A/'lossless_ranking_display_v2_20261006/round159/full_report_publication_snapshot_verification.json')
        assert manifest['original_full_ranking_sha256']==snapshot['original_report_sha256']
        expected={p:v['sha256'] for p,v in manifest['exported_files'].items()}
        assert h.blob_hashes(COMMIT,expected)==expected
        # Recheck the immutable original science, not the current mutable rankings output.
        protocol=read(folder/'protocol.json')
        for p,d in protocol['input_sha256'].items():assert sha(p)==d,p
        index_before=sha(ROOT/'.git/index');assert index_before=='ed2fa41598113343f7cf84c4ff16f7685c9ed3e079c16edf869c2c32019d3406'
        h.watcher.advance_source_index(current);assert sha(ROOT/'.git/index')==index_before
        evidence={'status':'passed_exact_already_pushed_commit_and_all_exported_blobs_original_science_QA_reverified','at_local':datetime.now().isoformat(),
            'commit':COMMIT,'remote_verified_head':current,'raw_exported_blobs_verified':len(expected),'original_failure_preserved':True,
            'new_scores':0,'new_training':0,'new_inference':0,'root_original_index_byte_exact':True,'test_labels_read':False,
            'input_sha256':{str(p):sha(p) for p in (Path(__file__),folder/'full_registration_failure.json',folder/'provenance_scope_execution.json',qa_path,folder/'protocol.json')}}
        create(out/'verification.json',evidence);create(A/'round159_existing_main_reconciliation_v1_20261010.json',evidence)
        create(A/'github_validation_sync_main_20261005/round159_receipt.json',{'status':'pushed_and_remote_head_verified','round':159,'at_local':datetime.now().isoformat(),
            'commit':COMMIT,'branch':'main','remote':h.sync.REMOTE,'official_score':manifest['metrics']['final_score'],'scored_records':19,'connected_records':15614,
            'raw_git_blobs_verified':len(expected),'actual_full_QA_version':70,'full_immutable_ranking_and_all_original_QA_preserved':True,
            'original_official_pilot_records_registered':19,'new_quality_scores_by_registration':0,'original_push_timeout_preserved':True,
            'scheme_url':'https://github.com/Zagadka-3906/stock-return-prediction/tree/main/validation_sync/round159'})
        create(folder/'full_registration_execution.json',{'status':'passed','at_local':datetime.now().isoformat(),'existing_official_scores_registered':19,
            'full_rankings_all_original_QA_and_main_publication_completed':True,'scientific_workers_suspended_stopped_or_restarted':0,
            'new_quality_scores_by_registration':0,'new_inference_claimed_by_registration':False,'selected_candidate_actual_new_inference':False,
            'original_failure_preserved':True,'reconciliation_evidence':str(A/'round159_existing_main_reconciliation_v1_20261010.json'),
            'global_goal_or_resource_exhaustion_claimed':False,'test_labels_read':False})
    print({'round159':'passed_original_QA_and_existing_main_reconciled','commit':COMMIT,'blobs':len(expected)},flush=True)

if __name__=='__main__':
    count=int(os.environ.get('GIT_CONFIG_COUNT','0'))
    for i,(k,v) in enumerate((('http.proxy','http://127.0.0.1:7897'),('http.version','HTTP/1.1'))):os.environ[f'GIT_CONFIG_KEY_{count+i}']=k;os.environ[f'GIT_CONFIG_VALUE_{count+i}']=v
    os.environ['GIT_CONFIG_COUNT']=str(count+2);main()
