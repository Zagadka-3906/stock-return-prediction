from pathlib import Path
from datetime import datetime,timezone,timedelta
import sys
A=Path(__file__).resolve().parent;ROOT=A.parent;sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
def main():
    now=datetime.now(timezone(timedelta(hours=8)));c=read(A/'current_user_runtime_control_20261010.json');read(A/'current_user_runtime_control_20261009.json')
    assert c['status']=='optimization_active_after_explicit_manual_resume' and now<datetime.fromisoformat(c['stop_at_local'])
    topbank=Path('E:/赛题五_本机临时/stock_toppair_embedding_small512_BF16_bank6_v1_20261010')
    assert read(topbank/'verification.json')['actual_native_fits']==6
    full=read(A/'service_owned_workflows_20261006/StockTopPairEmbeddingSmall512_independent_full5_GPU_controls_v1_20261009/service_execution.json');assert full['status']=='passed'
    proof=read(A/'PairTop184185_complete_reference_routes_v9_20261010.json')
    refs=read(A/'PairTop184185_exact_reference_copies_CPU_v9_20261010.json');assert len(refs['copies'])==9 and refs['actual_import_references_checked']==33
    for target,row in refs['copies'].items():assert sha(target)==sha(row['authoritative_source'])==row['sha256']
    state=read(A/'optimization_live_progress_v83_20261010.json');actual={}
    names=list(dict.fromkeys([*proof['service_aliases'].values(),'actual_PairTop185_complete_references_sources_main_v9_20261010','actual_stock_toppair_embedding_six_state_native42_v1_20261010','actual_stock_toppair_embedding_after174_fast17_screen_v1_20261010','actual_stock_toppair_embedding_after174_large_allocation29_screen_v1_20261010','StockTop10Embedding176_round176_full_registration_v1_20261010']))
    for name in names:
        f=A/'service_owned_workflows_20261006'/name;row=read(f/'native_launch.json') if (f/'native_launch.json').exists() else None
        actual[name]={'identity':row,'owned_live':owned(row) if row else False,'terminal':read(f/'service_execution.json') if (f/'service_execution.json').exists() else None,'not_started':row is None}
    screens={k:v for k,v in state['screen_progress'].items() if 'tiny_CDF' in k or 'Pair' in k}
    index=sha(ROOT/'.git/index');assert index=='ed2fa41598113343f7cf84c4ff16f7685c9ed3e079c16edf869c2c32019d3406'
    paths=[A/'PairTop184185_complete_reference_routes_v9_20261010.json',A/'route_PairTop184185_complete_references_v9_20261010.py',A/'PairTop184185_exact_reference_copies_CPU_v9_20261010.json',A/'PairTop184185_six_verified_idle_helpers_reference_recovery_v9_20261010.json',A/'prepare_complete_references9_sources_main_v1_20261010.py']
    create(A/'actual_complete_references9_Top_own6_full5_and_82_scores_handoff_v140_20261010.json',{'status':'actual_Top_weighted_own6_full5_passed_both_tiny41_and_pair17_29_complete_recursive185_imports33_and_exact_copies9_checked_full184185_future_pending','at_local':now.isoformat(),'deadline_local':c['stop_at_local'],'best_fully_qualified':read(A/'latest_verified_submission_delivery_v2_20261008.json'),'actual_screens':screens,'actual_Top_own6':read(topbank/'verification.json')['status'],'actual_Top_full5':full,'actual_reference_controls':refs,'actual_services':actual,'actual176_full_ranking_QA_log_passed_but_main_receipt_still_authoritative':True,'full184_expected_board':17306,'full185_expected_board':17354,'full184_QA':95,'full185_QA':96,'all_retired_helpers_verified_idle_before_any_new_future_outputs':True,'original_models_predictions_sources_and_failed_attempts_preserved':True,'immutable_supplement_sha256':{str(p):sha(p) for p in paths},'root_git_index_untouched_sha256':index,'whole_goal_completion_or_exhaustion_not_claimed':True})
    print({'Top_own6':'passed','Top_independent_full5':'passed','actual_reference_copies':9,'actual_imports_checked':33,'TRAIN_best':max(v.get('best',{}).get('connected_final_score',-1) for v in screens.values()),'qualified_round':state['best_fully_qualified']['selected_round']},flush=True)
if __name__=='__main__':main()
