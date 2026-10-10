from pathlib import Path
from datetime import datetime,timezone,timedelta
import sys,hashlib
A=Path(__file__).resolve().parent;ROOT=A.parent;sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
def main():
    now=datetime.now(timezone(timedelta(hours=8)));control=read(A/'current_user_runtime_control_20261010.json')
    assert now<datetime.fromisoformat(control['stop_at_local']) and control['status']=='optimization_active_after_explicit_manual_resume'
    bank=Path('E:/赛题五_本机临时/stock_pairrank_embedding_small512_BF16_bank6_v1_20261010')
    scientific=read(bank/'verification.json');assert scientific['actual_native_fits']==6
    best=read(A/'latest_verified_submission_delivery_v2_20261008.json');assert best['selected_round']>=175
    receipt=read(A/'github_validation_sync_main_20261005/round175_receipt.json');assert receipt['status']=='pushed_and_remote_head_verified' and receipt['scored_records']==47 and receipt['connected_records']==16839
    tight=read(Path('E:/赛题五_本机临时/StockRank20EmbeddingSmall512_after174_tiny_CDF41_screen_v1_20261010')/'verification.json');assert tight['new_quality_score_records']==41
    inventory={}
    for name in ['actual_stock_pairrank_embedding_own32_controls46_queue_v1_20261010','actual_stock_pairrank_embedding_small512_bank6_v1_20261010','StockPairRankEmbeddingSmall512_independent_full5_GPU_controls_v1_20261009','actual_stock_pairrank_embedding_six_state_native42_v1_20261010','actual_stock_pairrank_embedding_after174_fast17_screen_v1_20261010','actual_stock_pairrank_embedding_after174_large_allocation29_screen_v1_20261010','StockPairRankEmbedding184_complete48_family_v9_20261010','actual_PairRank184_frozen_sources_main_v2_20261010']:
        folder=A/'service_owned_workflows_20261006'/name
        row=read(folder/'native_launch.json') if (folder/'native_launch.json').exists() else None
        terminal=read(folder/'service_execution.json') if (folder/'service_execution.json').exists() else None
        inventory[name]={'actual_identity':row,'owned_live':owned(row) if row else False,'terminal':terminal,'not_started':row is None}
    index=sha(ROOT/'.git/index');assert index=='ed2fa41598113343f7cf84c4ff16f7685c9ed3e079c16edf869c2c32019d3406'
    sources=[A/'prepare_StockPairRankEmbedding184_complete48_pipeline_v4_20261010.py',A/'stock_pairrank_embedding184_full_execution_sources_admission_v3_20261010.json',A/'route_StockPairRank184_exact_verified_children_v3_20261010.py',A/'StockPairRank184_exact_child_sources_v3_20261010.json',A/'PairRank184_actual_recipe_backend_schema_CPU_v2_20261010.json',A/'same_day_ranknet_loss_actual_CPU_controls_v1_20261010.json',A/'PairRank184_recipe_metadata_recovery_v2_20261010.json']
    create(A/'actual_pairrank184_own6_and_qualified175_handoff_v135_20261010.json',{'status':'actual175_full47_QA86_main_qualified_delivery_and_new_pairrank_own6_passed_full5_native42_official46_full184_pending','at_local':now.isoformat(),'deadline_local':control['stop_at_local'],'best_fully_qualified':best,'actual175_main':receipt,'tight_after174_41':{'actual_records':41,'best':tight['best'],'submission_qualified':False},'new_pairrank_actual_annual_fits':6,'new_pairrank_configuration':scientific['actual_models'][0]['configuration'],'new_pairrank_loss_CPU':read(A/'same_day_ranknet_loss_actual_CPU_controls_v1_20261010.json'),'full184_expected_records':48,'full184_QA':95,'full184_expected_board':17306,'full184_parent_rounds':[174,183],'actual_services':inventory,'immutable_sources_sha256':{str(p):sha(p) for p in sources},'root_git_index_untouched_sha256':index,'original184_metadata_and_failed_prepare_attempts_preserved':True,'full184_new_future_inference_claimed':False,'new_pairrank_official_scores_claimed':False,'resource_or_feasible_direction_exhaustion_not_proven':True})
    print({'pairrank_own6':'passed','qualified_round':best['selected_round'],'tight41_best':tight['best']['connected_final_score'],'handoff':str(A/'actual_pairrank184_own6_and_qualified175_handoff_v135_20261010.json')},flush=True)
if __name__=='__main__':main()
