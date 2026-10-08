"""Close only the administrative collector failure after original QA and automatic main publication passed."""
from pathlib import Path
import sys,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned

def main():
    import publish_classifier_consensus_workflows_20261006 as helpers
    service=A/'service_owned_workflows_20261006/ConeRidge52_round142_full_registration_v1_20261008'
    assert not owned(read(service/'native_launch.json')) and read(service/'service_execution.json')['status']=='failed'
    log=(service/'stderr.log').read_text(encoding='utf8')
    assert 'collect_full_lossless_round142_qa53_20261007.py' in log and '(136, 47, 52)' in log
    folder=A/'optimization_20261003_r142';scope=folder/'provenance_scope_execution.json';s=read(scope)
    assert s['status']=='passed' and s['final_full_rehash_after_actual_full_ranking_QA'] and s['all_original_six_view_browser_and_candidate_manifest_QA_passed']
    qa_path=A/'lossless_ranking_display_qa_v53_20261007/round142/verification.json';qa=read(qa_path)
    assert qa['status']=='passed_all_original_full_ranking_QA_and_lossless_browser_node_checks' and qa['round']==142
    assert qa['original_full_QA_result']['connected_records']==13670 and qa['original_full_QA_result']['new_round_records']==52
    assert qa['all_original_provenance_candidate_manifest_sorting_and_six_view_checks_passed']
    ready_path=A/'ConeRidge52_selected_release_v1_20261008/selected_candidate_ready_for_registration.json';ready=read(ready_path)
    assert ready['sealed_candidate_complete'] and not ready['new_inference_claimed']
    prediction=ROOT/'candidates/optimization_20261003_r142/verification.json';p=read(prediction)
    assert p['status']=='passed'
    for key in ('model_reload_bit_identical','pipeline_replay_bit_identical','csv_replay_byte_identical','cold80_day_prefix_bit_identical'):assert p[key]
    assert len(p['models'])==len({row['sha256'] for row in p['models'].values()})==18
    assert sha(ROOT/'candidates/optimization_20261003_r142/submission.csv')==p['csv_sha256']
    receipt_path=A/'github_validation_sync_main_20261005/round142_receipt.json';receipt=read(receipt_path)
    assert receipt['status']=='pushed_and_remote_head_verified' and receipt['round']==142 and receipt['branch']=='main'
    assert receipt['scored_records']==52 and receipt['connected_records']==13670 and receipt['raw_git_blobs_verified']==4010
    assert receipt['full_immutable_ranking_and_all_original_QA_preserved']
    helpers.verify_main(receipt['commit'])
    sources=[Path(__file__),scope,qa_path,ready_path,prediction,receipt_path,service/'service_execution.json',service/'stderr.log']
    from win32_read_handle_hash_cache_with_filename_v2_20261006 import LockedReadHashCache
    pins={**s['input_sha256'],**{str(path):sha(path) for path in sources}}
    with LockedReadHashCache(pins) as lock:lock.reverify()
    create(folder/'administrative_registration_reconciliation_v2_20261008.json',{
        'status':'passed_original52_scores_frozen_candidate_QA53_and_automatic_full_main_receipt_reconciled',
        'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'input_sha256':pins,'main_commit':receipt['commit'],
        'original_failed_guard':'collect signature and fixed tuple inherited136/47/52; caller also used count/QAversion order',
        'original_QA_and_native_checks_not_weakened_or_rerun':True,'new_model_fits':0,'new_quality_scores':0,'new_inference_calls':0,'test_labels_read':False})
    create(folder/'full_registration_execution.json',{'status':'passed','at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),
        'existing_official_scores_registered':52,'full_rankings_all_original_QA_and_main_publication_completed':True,
        'actual_complete_QA_version':53,'actual_remote_verified_commit':receipt['commit'],
        'administrative_collector_failure_preserved_and_reconciled_after_independent_auto_main_publication':True,
        'reconciliation_source':str(Path(__file__)),'reconciliation_proof_sha256':sha(folder/'administrative_registration_reconciliation_v2_20261008.json'),
        'scientific_workers_suspended_stopped_or_restarted':0,'new_quality_scores_by_registration':0,
        'new_inference_claimed_by_registration':False,'selected_candidate_actual_new_inference':False,
        'global_goal_or_resource_exhaustion_claimed':False,'test_labels_read':False})
    print('142 full registration reconciled from original QA53 and verified main; failed source1 preserved.',flush=True)

if __name__=='__main__':main()
