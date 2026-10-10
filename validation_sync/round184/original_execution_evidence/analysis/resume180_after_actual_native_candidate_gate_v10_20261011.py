"""Continue failed180 from verified empty junction outputs; never replay bootstrap, models or scores."""
from pathlib import Path
import sys,time
A=Path(__file__).resolve().parent;ROOT=A.parent;sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed

def main():
    assert allowed()
    from route_actual_candidate_closed_and180_continuation_v10_20261011 import installed
    closed,start=installed()
    closed('StockRank20Embedding48_selected_native14_v5_20261010')
    original=A/'StockRank20Embedding180_complete_family_v1_20261010/frozen_before_selected_future_dispatch.json'
    freeze=read(original)
    for p,d in freeze['input_sha256'].items():assert sha(p)==d,p
    from stock_rank20_embedding180_storage_v2_20261010 import OUTPUTS,empty
    for logical,physical in OUTPUTS.items():assert logical.resolve()==physical.resolve();empty(logical)
    from prepare_StockRank20Embedding180_complete48_pipeline_v1_20261010 import source_paths
    sources=[*source_paths(),Path(__file__),original]
    pins={str(p):sha(p) for p in sources}
    out=A/'StockRank20Embedding180_actual_resume_v10_20261011';out.mkdir(exist_ok=False)
    create(out/'frozen_before_actual_remaining_dispatch.json',{'input_sha256':pins,'original_freeze_sha256':sha(original),
        'original_failed_services_preserved':True,'all_six_existing_junction_outputs_verified_empty':True,
        'new_quality_scores':0,'new_model_fits':0,'actual_future_X_read':False,'test_labels_read':False})
    for name,driver in [('StockRank20Embedding180_selected_candidate_preparation_v1_20261010','run_StockRank20Embedding180_selected_candidate_feature_cache_actual_gate_v10_20261011.py'),
        ('StockRank20Embedding180_selected_candidate_sealing_v1_20261010','seal_StockRank20Embedding180_selected_candidate_v2_20261010.py'),
        ('StockRank20Embedding180_round180_full_registration_v1_20261010','run_StockRank20Embedding180_full_registration_v5_20261010.py')]:
        assert allowed();row=start(name,driver,[],pins);create(out/(name+'_launch.json'),row);closed(name)
    receipt=read(A/'github_validation_sync_main_20261005/round180_receipt.json')
    assert receipt['status']=='pushed_and_remote_head_verified' and receipt['scored_records']==48 and receipt['actual_full_QA_version']==91
    assert read(A/'optimization_20261003_r180/full_registration_execution.json')['status']=='passed'
    assert allowed()
    from maintain_best_fully_qualified_submission_delivery_v3_20261010 import update
    update()
    create(out/'passed.json',{'status':'passed_actual180_remaining_candidate_seal_full48_QA91_main_and_delivery',
        'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'receipt':receipt,'original_failed_services_preserved':True,
        'new_quality_scores_by_continuation':0,'new_model_fits':0,'test_labels_read':False})

if __name__=='__main__':main()
