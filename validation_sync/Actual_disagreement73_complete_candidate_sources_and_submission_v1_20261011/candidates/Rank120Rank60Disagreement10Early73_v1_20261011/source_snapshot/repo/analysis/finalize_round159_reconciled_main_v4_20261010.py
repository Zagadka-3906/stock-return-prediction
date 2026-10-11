"""Consume the actual completed rehash and concurrently created valid watcher receipt idempotently."""
from pathlib import Path
import sys,os
A=Path(__file__).resolve().parent;ROOT=A.parent;sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from datetime import datetime,timezone,timedelta
def main():
    c=read(A/'current_user_runtime_control_20261010.json');read(A/'current_user_runtime_control_20261009.json')
    assert c['status']=='optimization_active_after_explicit_manual_resume' and datetime.now(timezone(timedelta(hours=8)))<datetime.fromisoformat(c['stop_at_local'])
    proof=read(A/'round159_existing_main_reconciliation_v3_20261010.json')
    assert proof['status']=='passed_exact_already_pushed_commit_and_all_exported_blobs_original_science_QA_reverified' and proof['raw_exported_blobs_verified']==6202
    for p,d in proof['input_sha256'].items():assert sha(p)==d,p
    receipt=read(A/'github_validation_sync_main_20261005/round159_receipt.json')
    assert receipt['status']=='pushed_and_remote_head_verified' and receipt['commit']==proof['commit'] and receipt['branch']=='main'
    assert (receipt['scored_records'],receipt['connected_records'],receipt['raw_git_blobs_verified'])==(19,15614,6202)
    assert sha(ROOT/'.git/index')=='ed2fa41598113343f7cf84c4ff16f7685c9ed3e079c16edf869c2c32019d3406'
    folder=A/'optimization_20261003_r159'
    assert receipt['official_score']==read(folder/'calibrated_csv_official.json')['metrics']['final_score']
    value={'status':'passed','at_local':datetime.now().isoformat(),'existing_official_scores_registered':19,
        'full_rankings_all_original_QA_and_main_publication_completed':True,'scientific_workers_suspended_stopped_or_restarted':0,
        'new_quality_scores_by_registration':0,'new_inference_claimed_by_registration':False,'selected_candidate_actual_new_inference':False,
        'original_failure_preserved':True,'reconciliation_evidence':str(A/'round159_existing_main_reconciliation_v3_20261010.json'),
        'original_user_index_restored_byte_exact':True,'actual_watcher_receipt_accepted_after_exact_rehash':True,
        'global_goal_or_resource_exhaustion_claimed':False,'test_labels_read':False}
    target=folder/'full_registration_execution.json'
    if target.exists():assert read(target)['status']=='passed'
    else:create(target,value)
    create(A/'round159_actual_reconciliation_completion_v4_20261010.json',{'status':'passed','at_local':datetime.now().isoformat(),
        'source_sha256':sha(Path(__file__)),'receipt_sha256':sha(A/'github_validation_sync_main_20261005/round159_receipt.json'),
        'full_registration_execution_sha256':sha(target),'existing_rehash_proof_sha256':sha(A/'round159_existing_main_reconciliation_v3_20261010.json'),
        'new_scores':0,'new_inference':0,'all_original_failed_services_and_index_incident_preserved':True})
    print('round159 fully qualified; original science and full main rehash retained',flush=True)
if __name__=='__main__':main()
