from pathlib import Path
import sys,time
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
def main():
    assert allowed()
    from route_reboot_complete_candidate_v11_20261011 import installed,PROOF
    closed,start=installed();data=read(PROOF)
    closed('StockRank20Embedding180_selected_candidate_preparation_actual_native_gate_v10_20261011')
    ready=read(A/'StockRank20Embedding180_selected_release_v1_20261010/inference_ready.json')
    assert ready['status']=='passed_exact_selected_anchor48_candidate_reuse' and not ready['new_inference_claimed']
    candidate=Path(ready['source_candidate']);assert sha(candidate/'manifest.json')==ready['manifest_sha256']
    for relative,row in read(candidate/'manifest.json')['files'].items():assert sha(candidate/relative)==row['sha256']
    out=A/'StockRank20Embedding180_reboot_continuation_v11_20261011';out.mkdir(exist_ok=False)
    pins=data['input_sha256'];create(out/'frozen_remaining_dispatch.json',{'input_sha256':pins,'new_model_fits':0,'new_quality_scores':0,'reuse_completed_candidate':True})
    for name,driver in [('StockRank20Embedding180_selected_candidate_sealing_v1_20261010','seal_StockRank20Embedding180_selected_candidate_v2_20261010.py'),('StockRank20Embedding180_round180_full_registration_v1_20261010','run_StockRank20Embedding180_full_registration_v5_20261010.py')]:
        assert allowed();row=start(name,driver,[],pins);create(out/(name+'_launch.json'),row);closed(name)
    receipt=read(A/'github_validation_sync_main_20261005/round180_receipt.json')
    assert receipt['status']=='pushed_and_remote_head_verified' and receipt['actual_full_QA_version']==91 and receipt['scored_records']==48
    from maintain_best_fully_qualified_submission_delivery_v3_20261010 import update
    assert allowed();update();create(out/'passed.json',{'status':'passed_completed_candidate_reused_full48_QA91_main','receipt':receipt,'new_model_fits':0,'new_quality_scores':0})
if __name__=='__main__':main()
