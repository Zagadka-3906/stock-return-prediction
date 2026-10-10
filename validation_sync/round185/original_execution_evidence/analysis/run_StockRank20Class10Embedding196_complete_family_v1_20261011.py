"""Finish133 qualification, freeze selected scheme, infer, seal, registry, QA107 and main."""
from pathlib import Path
import sys,time
A=Path(__file__).resolve().parent;ROOT=A.parent;sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed,closed
from handoff_ready_goss_full_execution_20261006 import start_service
from run_protected167_complete_family_v1_20261010 import junction

def main():
    assert allowed();closed('StockRank20Class10Embedding19_selected_native14_v1_20261011')
    closed('StockRank20Class10EmbeddingSmall512_independent_full5_GPU_controls_v1_20261011')
    # Selected full-parent inference must not compete with an active new GPU fit.
    closed('actual_stock_rank20class10_BCE_own6_full5_queue_v1_20261011')
    closed('actual_stock_rank20class10_embedding_six_state_native42_v1_20261011')
    from verify_StockRank20Class10Embedding196_full19_preflight_v1_20261011 import main as preflight
    preflight()
    from stock_rank20class10_embedding196_storage_v1_20261011 import OUTPUTS,empty
    for logical,physical in OUTPUTS.items():
        assert logical.is_relative_to(ROOT) and physical.is_relative_to(Path('E:/赛题五_本机临时/第196轮_20261010'))
        assert not logical.exists() and not physical.exists(),logical
        physical.mkdir(parents=True);logical.parent.mkdir(parents=True,exist_ok=True);junction(logical,physical);empty(logical)
    from prepare_StockRank20Class10Embedding196_complete19_pipeline_v2_20261011 import source_paths
    extra=[Path(__file__),A/'run_StockRank20Class10Embedding196_full_registration_v1_20261011.py',A/'verify_StockRank20Class10Embedding196_full19_preflight_v1_20261011.py',A/'stock_rank20class10_embedding196_full_family_preflight_v1_20261011.json']
    pins={str(p):sha(p) for p in dict.fromkeys([*source_paths(),*extra])}
    out=A/'StockRank20Class10Embedding196_complete_family_v1_20261011';out.mkdir(exist_ok=False)
    create(out/'frozen_before_selected_future_dispatch.json',{'input_sha256':pins,'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'quality_cases':19,'actual_future_X_read':False,'new_native_fits':0,'test_labels_read':False})
    for name,driver in [('StockRank20Class10Embedding196_selected_candidate_preparation_v1_20261011','run_StockRank20Class10Embedding196_selected_candidate_feature_cache_v1_20261011.py'),('StockRank20Class10Embedding196_selected_candidate_sealing_v1_20261011','seal_StockRank20Class10Embedding196_selected_candidate_v1_20261011.py'),('StockRank20Class10Embedding196_round196_full_registration_v1_20261011','run_StockRank20Class10Embedding196_full_registration_v1_20261011.py')]:
        assert allowed();row=start_service(name,driver,[],pins);create(out/(name+'_launch.json'),row);closed(name)
    receipt=read(A/'github_validation_sync_main_20261005/round196_receipt.json')
    assert receipt['status']=='pushed_and_remote_head_verified' and receipt['scored_records']==19
    assert read(A/'optimization_20261003_r196/full_registration_execution.json')['status']=='passed'
    assert allowed()
    from maintain_best_fully_qualified_submission_delivery_v3_20261010 import update
    update()
    create(out/'passed.json',{'status':'passed_actual19_selected_stage_full_native_candidate_or_exact_anchor_QA107_main_and_delivery','at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'receipt':receipt,'actual_scored_records':19,'new_quality_scores_by_registration':0,'test_labels_read':False})

if __name__=='__main__':main()
