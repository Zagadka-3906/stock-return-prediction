from pathlib import Path
from datetime import datetime,timezone,timedelta
import sys
A=Path(__file__).resolve().parent;ROOT=A.parent;sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import create,read,sha,owned
def main():
    now=datetime.now(timezone(timedelta(hours=8)));control=read(A/'current_user_runtime_control_20261010.json');read(A/'current_user_runtime_control_20261009.json')
    assert now<datetime.fromisoformat(control['stop_at_local']) and control['status']=='optimization_active_after_explicit_manual_resume'
    native=read(A/'service_owned_workflows_20261006/actual_stock_pairrank_embedding_six_state_native42_admission_recovery_v2_20261010/service_execution.json');assert native['status']=='passed'
    top_restart=read(A/'service_owned_workflows_20261006/actual_stock_toppair_embedding_small512_restart_v1_20261010/service_execution.json');assert top_restart['status']=='passed'
    state=read(A/'optimization_live_progress_v82_20261010.json')
    names=['actual_stock_pairrank_embedding_after174_fast17_screen_v1_20261010','actual_stock_pairrank_embedding_after174_large_allocation29_screen_v1_20261010','actual_stock_toppair_embedding_own32_controls46_queue_v2_20261010','actual_stock_toppair_embedding_small512_bank6_v1_20261010','actual_PairTop185_native_admission_sources_main_v1_20261010','actual_StockTopPair_objective_stages_main_v1_20261010','StockTopPairEmbedding185_complete48_family_v9_20261010','actual_StockPairRank_remaining_native46_main_v8_20261010']
    actual={}
    for name in names:
        f=A/'service_owned_workflows_20261006'/name;row=read(f/'native_launch.json') if (f/'native_launch.json').exists() else None
        actual[name]={'identity':row,'owned_live':owned(row) if row else False,'terminal':read(f/'service_execution.json') if (f/'service_execution.json').exists() else None,'not_started':row is None}
    screens={k:v for k,v in state['screen_progress'].items() if 'tiny_CDF' in k or 'Pair' in k}
    proofs=['actual_PairRank_native42_admission_routes_v8_20261010.json','route_actual_PairRank_native42_admission_v8_20261010.py','PairRank184_native42_three_idle_helper_recovery_v8_20261010.json','same_day_top_ranknet_loss_actual_CPU_controls_v1_20261010.json','stock_toppair_embedding_own32_controls46_sources_admission_v1_20261010.json','prepare_StockTopPairEmbedding185_complete48_pipeline_v1_20261010.py','stock_toppair_embedding185_full_execution_sources_admission_v3_20261010.json','TopPair185_generated_child_import_recovery_v2_20261010.json','route_StockTopPair185_exact_verified_children_v1_20261010.py','route_StockTopPair185_exact_verified_children_v3_20261010.py','StockTopPair185_exact_child_sources_v3_20261010.json','PairTop185_actual_native_recipe_and_exact_admission_CPU_v1_20261010.json']
    index=sha(ROOT/'.git/index');assert index=='ed2fa41598113343f7cf84c4ff16f7685c9ed3e079c16edf869c2c32019d3406'
    create(A/'actual_pair_top185_native42_and_GPU_controls_handoff_v137_20261010.json',{'status':'actual_pair_own6_full5_and_native42_passed_official17_running_top_weighted_loss_GPU_restart_passed_annual6_and_full185_pending','at_local':now.isoformat(),'deadline_local':control['stop_at_local'],'best_fully_qualified':read(A/'latest_verified_submission_delivery_v2_20261008.json'),'actual_pair_native42':native,'actual_top_restart':top_restart,'actual_screens':screens,'actual_services':actual,'resource_snapshot':state['resources'],'top_training_wait_uses_actual_memory_guard_not_failure_or_exhaustion':True,'full185_expected_records':48,'full185_QA':96,'full185_expected_board':17354,'full185_parent_rounds':[174,184],'actual_14_parent_callback_CPU':True,'immutable_source_proofs_sha256':{str(A/n):sha(A/n) for n in proofs},'original_failed_native42_and_top_queue_and_generated_import_statuses_preserved':True,'all_model_and_temporary_storage_on_E':True,'root_git_index_untouched_sha256':index,'submission_qualification_and_feasible_direction_exhaustion_not_claimed':True})
    print({'actual_pair_native42':'passed','actual_top_restart':'passed','actual_screen_counts':{k:v.get('completed_cases') for k,v in screens.items()},'actual_training_only_best':max(v.get('best',{}).get('connected_final_score',-1) for v in screens.values()),'qualified_round':state['best_fully_qualified']['selected_round']},flush=True)
if __name__=='__main__':main()
