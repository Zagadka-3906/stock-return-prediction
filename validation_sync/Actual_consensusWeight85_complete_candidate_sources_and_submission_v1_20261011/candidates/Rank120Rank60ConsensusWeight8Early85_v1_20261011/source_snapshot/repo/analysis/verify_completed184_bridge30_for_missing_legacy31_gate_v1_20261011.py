"""Validate actual completed184 evidence for an unused legacy dependency name.

This is an administrative receipt validator, not rerunning the old family driver.
"""
from pathlib import Path
import sys
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed,closed

def main():
 assert allowed();closed('actual184_registered_QA_main_complete_parent_bridge30_v1_20261011')
 paths=[A/'service_owned_workflows_20261006/actual184_registered_QA_main_complete_parent_bridge30_v1_20261011/service_execution.json',A/'github_validation_sync_main_20261005/round184_receipt.json',A/'optimization_20261003_r184/full_registration_execution.json',A/'optimization_20261003_r184/selection.json',A/'optimization_20261003_r184/calibrated_csv_official.json',A.parent/'candidates/optimization_20261003_r184/verification.json']
 receipt=read(paths[1]);assert receipt['status']=='pushed_and_remote_head_verified' and receipt['branch']=='main' and receipt['scored_records']==48
 assert read(paths[2])['status']=='passed'
 assert read(paths[3])['winner']['metrics']==read(paths[4])['metrics']
 candidate=read(paths[5]);assert candidate['status']=='passed' and len(candidate['models'])==35
 models={}
 for name,row in candidate['models'].items():
  p=Path(row['path']);assert sha(p)==row['sha256'];models[name]={'path':str(p),'sha256':row['sha256']}
 create(A/'actual184_completed_bridge30_legacy31_dependency_admission_v1_20261011.json',{'status':'passed_actual_completed184_receipt_candidate_all8_metrics_and35_models_for_legacy_dependency_gate','actual_complete_parent_service':'actual184_registered_QA_main_complete_parent_bridge30_v1_20261011','legacy_wait_name':'recovery31_StockPairRankEmbedding184_complete48_family_v9_20261010','this_service_is_receipt_validation_only':True,'original_family_driver_not_executed':True,'input_sha256':{str(p):sha(p) for p in [Path(__file__),*paths]},'verified_models':models,'main_receipt':receipt,'new_fits':0,'new_scores':0,'new_future_inference':False})
 print({'actual184_completed_receipt_validator_passed':True,'legacy_gate_unblocked':True},flush=True)
if __name__=='__main__':main()
