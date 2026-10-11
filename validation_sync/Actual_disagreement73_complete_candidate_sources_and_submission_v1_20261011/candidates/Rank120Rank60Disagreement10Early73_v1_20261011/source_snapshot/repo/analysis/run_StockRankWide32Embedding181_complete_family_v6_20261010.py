"""Finish133 qualification, freeze selected scheme, infer, seal, registry, QA92 and main."""
from pathlib import Path
import sys,time
A=Path(__file__).resolve().parent;ROOT=A.parent;sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed,closed
from handoff_ready_goss_full_execution_20261006 import start_service
from run_protected167_complete_family_v1_20261010 import junction

def main():
    assert allowed();closed('StockRankWide32Embedding48_selected_native14_v5_20261010')
    # Selected full-parent inference must not compete with an active new GPU fit.
    closed('actual_stock_rank_wide32_embedding1024_ID32_own64_controls46_queue_v1_20261010')
    closed('actual_stock_rank_wide32_embedding_six_state_native42_v1_20261010')
    from verify_StockRankWide32Embedding181_full48_preflight_v5_20261010 import main as preflight
    preflight()
    from stock_rank_wide32_embedding181_storage_v2_20261010 import OUTPUTS,empty
    for logical,physical in OUTPUTS.items():
        assert logical.is_relative_to(ROOT) and physical.is_relative_to(Path('E:/赛题五_本机临时/第181轮_20261010'))
        assert not logical.exists() and not physical.exists(),logical
        physical.mkdir(parents=True);logical.parent.mkdir(parents=True,exist_ok=True);junction(logical,physical);empty(logical)
    from prepare_StockRankWide32Embedding181_complete48_pipeline_v1_20261010 import source_paths
    extra=[Path(__file__),A/'run_StockRankWide32Embedding181_full_registration_v5_20261010.py',A/'verify_StockRankWide32Embedding181_full48_preflight_v5_20261010.py',A/'stock_rank_wide32_embedding181_full_family_preflight_v2_20261010.json']
    pins={str(p):sha(p) for p in dict.fromkeys([*source_paths(),*extra])}
    out=A/'StockRankWide32Embedding181_complete_family_v1_20261010';out.mkdir(exist_ok=False)
    create(out/'frozen_before_selected_future_dispatch.json',{'input_sha256':pins,'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'quality_cases':48,'actual_future_X_read':False,'new_native_fits':0,'test_labels_read':False})
    for name,driver in [('StockRankWide32Embedding181_selected_candidate_preparation_v1_20261010','run_StockRankWide32Embedding181_selected_candidate_feature_cache_v6_20261010.py'),('StockRankWide32Embedding181_selected_candidate_sealing_v1_20261010','seal_StockRankWide32Embedding181_selected_candidate_v2_20261010.py'),('StockRankWide32Embedding181_round181_full_registration_v1_20261010','run_StockRankWide32Embedding181_full_registration_v5_20261010.py')]:
        assert allowed();row=start_service(name,driver,[],pins);create(out/(name+'_launch.json'),row);closed(name)
    receipt=read(A/'github_validation_sync_main_20261005/round181_receipt.json')
    assert receipt['status']=='pushed_and_remote_head_verified' and receipt['scored_records']==48
    assert read(A/'optimization_20261003_r181/full_registration_execution.json')['status']=='passed'
    assert allowed()
    from maintain_best_fully_qualified_submission_delivery_v3_20261010 import update
    update()
    create(out/'passed.json',{'status':'passed_actual48_selected_stage_full_native_candidate_or_exact_anchor_QA92_main_and_delivery','at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'receipt':receipt,'actual_scored_records':48,'new_quality_scores_by_registration':0,'test_labels_read':False})

if __name__=='__main__':main()
