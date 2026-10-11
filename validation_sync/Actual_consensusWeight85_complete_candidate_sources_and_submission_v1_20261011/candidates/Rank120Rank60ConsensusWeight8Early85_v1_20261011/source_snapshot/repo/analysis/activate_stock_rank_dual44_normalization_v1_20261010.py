"""Declare complete44 comparison without dropping qualified173 or adding selection barriers."""
from pathlib import Path
import sys
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import create,sha
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
from handoff_ready_goss_full_execution_20261006 import start_service
def main():
    assert allowed()
    rank='stock_rank_embedding16_cross120_rank1d_recent252_small512_BF16_e24';ret='stock_embedding16_cross120_return1d_recent252_small512_BF16_e24'
    families=[{'folder':'StockRankEmbeddingSmall512_after170_high_impact17_screen_v1_20261010','base_round':170,'records':17,'stage_kind':'stock_rank_embedding_rank1d_direct','recipes':[rank],'recipe':rank,'actual_service':'actual_stock_rank_embedding_after170_fast17_screen_v1_20261010','publisher':'actual_stock_rank_embedding_after170_completion_main_v55_20261010','main_receipt':'stock_rank_embedding17_after170_completion_main_receipt_v55_20261010.json'},{'folder':'StockDualEmbedding_after173_high_impact25_screen_v1_20261010','base_round':173,'records':25,'stage_kind':'stock_return_rank_embedding_consensus','recipes':[ret,rank],'recipe':'stock_return1d_rank1d_embedding_daily_rank_consensus','actual_service':'actual_stock_dual_embedding_after173_high_impact25_screen_v1_20261010','publisher':'actual_stock_dual_embedding_after173_completion_main_v56_20261010','main_receipt':'stock_dual_embedding25_after173_completion_main_receipt_v56_20261010.json'}]
    plan=A/'stock_rank_dual44_after173_selection_plan_v1_20261010.json'
    create(plan,{'status':'declared44_existing_frozen_cases_and_qualified170_173_anchors_before_dual25_scores','expected_records':44,'fully_qualified_anchors':[170,173],'families':families,'actual_nonidentity_full_controls_required':40,'actual_nonidentity_prefix_controls_required':120,'selection':'highest_connected_official_S_then_unique_physical_models_then_absolute_weight_then_case','partial_rank17_TRAIN_scores_already_seen_without_changing_cases':True,'new_quality_scores':0,'future_X_read':False,'test_labels_read':False,'full174_pipeline_not_yet_built':True})
    p=A/'normalize_stock_rank_and_dual44_after173_v1_20261010.py'
    row=start_service('actual_stock_rank_dual44_after173_normalization_v1_20261010',p.name,[],{str(p):sha(p),str(plan):sha(plan)})
    create(A/'actual_stock_rank_dual44_after173_normalization_activation_v1_20261010.json',row)
    print({'complete44_comparison':'queued','selected14_and_full174_pipeline_pending':True},flush=True)
if __name__=='__main__':main()
