"""Finish133 qualification, freeze selected scheme, infer, seal, registry, QA87 and main."""
from pathlib import Path
import sys,time
A=Path(__file__).resolve().parent;ROOT=A.parent;sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed,closed
from handoff_ready_goss_full_execution_20261006 import start_service
from run_protected167_complete_family_v1_20261010 import junction

def main():
    assert allowed();closed('StockTop10Embedding31_selected_native14_v3_20261010')
    # Selected full-parent inference must not compete with an active new GPU fit.
    closed('actual_stock_top10_embedding_own_training_queue_v3_20261010')
    closed('actual_stock_top10_embedding_early171_six_state_native42_v3_20261010')
    from verify_StockTop10Embedding176_full31_preflight_v3_20261010 import main as preflight
    preflight()
    from stock_top10_embedding176_storage_v1_20261010 import OUTPUTS,empty
    for logical,physical in OUTPUTS.items():
        assert logical.is_relative_to(ROOT) and physical.is_relative_to(Path('E:/赛题五_本机临时/第176轮_20261010'))
        assert not logical.exists() and not physical.exists(),logical
        physical.mkdir(parents=True);logical.parent.mkdir(parents=True,exist_ok=True);junction(logical,physical);empty(logical)
    from prepare_stock_top10_embedding176_full_registry_sources_v2_20261010 import source_paths
    extra=[Path(__file__),A/'run_StockTop10Embedding176_full_registration_v3_20261010.py',A/'verify_StockTop10Embedding176_full31_preflight_v3_20261010.py',A/'stock_top10_embedding176_full_family_preflight_v2_20261010.json']
    extra += [A/n for n in ['prevent_Top10_large29_pointer_collision_and_cascade_routes_v5_20261010.py', 'normalize_completed_stock_top10_embedding_followup31_after175_v3_20261010.py', 'qualify_stock_top10_embedding31_selected_native14_v3_20261010.py', 'prepare_StockTop10Embedding176_selected_candidate_v3_20261010.py', 'stock_top10_embedding176_candidate_sources_preparation_v3_20261010.json', 'run_stock_top10_embedding_after174_large_allocation29_screen_v2_20261010.py', 'publish_stock_top10_embedding_after174_large_allocation29_completion_v72_20261010.py']]
    pins={str(p):sha(p) for p in dict.fromkeys([*source_paths(),*extra])}
    out=A/'StockTop10Embedding176_complete_family_v1_20261010';out.mkdir(exist_ok=False)
    create(out/'frozen_before_selected_future_dispatch.json',{'input_sha256':pins,'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'quality_cases':31,'actual_future_X_read':False,'new_native_fits':0,'test_labels_read':False})
    for name,driver in [('StockTop10Embedding176_selected_candidate_preparation_v1_20261010','prepare_StockTop10Embedding176_selected_candidate_v3_20261010.py'),('StockTop10Embedding176_selected_candidate_sealing_v1_20261010','seal_StockTop10Embedding176_selected_candidate_v1_20261010.py'),('StockTop10Embedding176_round176_full_registration_v1_20261010','run_StockTop10Embedding176_full_registration_v3_20261010.py')]:
        assert allowed();row=start_service(name,driver,[],pins);create(out/(name+'_launch.json'),row);closed(name)
    receipt=read(A/'github_validation_sync_main_20261005/round176_receipt.json')
    assert receipt['status']=='pushed_and_remote_head_verified' and receipt['scored_records']==31
    assert read(A/'optimization_20261003_r176/full_registration_execution.json')['status']=='passed'
    assert allowed()
    from maintain_best_fully_qualified_submission_delivery_v3_20261010 import update
    update()
    create(out/'passed.json',{'status':'passed_actual31_selected_stage_full_native_candidate_or_exact_anchor_QA87_main_and_delivery','at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'receipt':receipt,'actual_scored_records':31,'new_quality_scores_by_registration':0,'test_labels_read':False})

if __name__=='__main__':main()
