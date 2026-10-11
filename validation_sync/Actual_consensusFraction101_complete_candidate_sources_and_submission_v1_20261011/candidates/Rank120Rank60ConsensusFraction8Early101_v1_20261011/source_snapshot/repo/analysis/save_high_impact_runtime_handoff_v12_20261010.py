"""Save actual running work and pending qualification without implying goal completion."""
from pathlib import Path
from datetime import datetime,timezone,timedelta
import sys
A=Path(__file__).resolve().parent;ROOT=A.parent;sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned

def main():
    state=read(A/'optimization_live_progress_v15_20261010.json');control=read(A/'current_user_runtime_control_20261010.json')
    assert control['status']=='optimization_active_after_explicit_manual_resume'
    now=datetime.now(timezone(timedelta(hours=8)));assert now<datetime.fromisoformat(control['stop_at_local'])
    jobs={}
    for name in ('continuous_fast_reused_frontiers_v15_20261010','actual_fast_optimization_progress_v15_20261010','main_publisher_v11_20261010','actual_user_stop1100_wait_manual_continue_v1_20261011','actual_BF16_medium2048_huber010_seed09_e64_bank6_v1_20261009','actual_Huber010_high_impact65_screen_v1_20261010','actual_high_impact_priority_huber65_main_v7_20261010','actual_protected_official_top_screen_v2_20261010_location_reconciliation_v2_20261010','actual_reconciled_official_top37_main_v7_20261010','actual_protected_quantization37_screen_v1_20261010','actual_high_impact_priority_quant37_main_v8_20261010'):
        f=A/'service_owned_workflows_20261006'/name
        if (f/'native_launch.json').is_file():
            row=read(f/'native_launch.json');jobs[name]={'identity':row,'actual_owned_running':owned(row),'execution':read(f/'service_execution.json') if (f/'service_execution.json').is_file() else None}
    descriptor=A/'TailProtected162_full76_ready_dispatch_v1_20261010.json'
    declaration=read(descriptor)
    for p,d in declaration['input_sha256'].items():assert sha(p)==d,p
    receipts={n:read(A/n) for n in ('github_validation_sync_main_20261005/round160_receipt.json','high_impact_priority_preparation_main_receipt_v7_20261010.json','high_impact_priority_scores_main_receipt_v6_20261010.json','high_impact_priority_valid_main_receipt_v6_20261010.json')}
    for receipt in receipts.values():assert receipt['status']=='pushed_and_remote_head_verified' and receipt['branch']=='main'
    create(A/'actual_optimization_fast_runtime_handoff_v12_20261010.json',{'status':'actual_running_qualified_Huber_bank_controls_protected162_and_no_fit37_not_goal_complete','at_local':now.isoformat(),'deadline_local':control['stop_at_local'],'jobs':jobs,'best_fully_qualified':state['best_fully_qualified'],'best_completed_screen_score':0.45120245465782494,'best_screen_vs157_gain':1.017367827760296e-5,'actual_completed_additional_score_records':state['new_high_impact_verified_score_records'],'Huber_actual_saved_annual_models':state['actual_Huber_annual_training']['completed_annual_models'],'Huber_current_stage':state['actual_Huber_annual_training'].get('stage'),'protected162_actual_full_dispatch_descriptor':declaration,'protected162_new_native_candidate_still_pending':True,'Huber65_actual_hidden_queue':str(A/'Huber010_high_impact65_actual_hidden_queue_v1_20261010.json'),'all65_require_own6_full5_native42_before_any_quality':True,'actual_main_receipts':receipts,'live_progress':str(A/'optimization_live_progress_v15_20261010.json'),'fresh_protected162_candidate_source_authority_version':2,'prototype_candidate_v1_not_admitted_for_execution':True,'pointer_collisions_preserved_and_actual_completed_scores_not_rerun':True,'model_data_and_archives_on_D_or_E_only':True,'root_git_index_sha256':sha(ROOT/'.git/index'),'required_next_work':['own6 training and full5 now passed; finish native42 and prefits then real quality','formal161 19 controls, scores, freeze/inference as selected, QA72 and main','actual protected37 Top pointer reconciliation and main','actual protected162 selected native14 and14 cold plus7 prefits, freeze before futureX, entire157 plus tail two full future replays and cold80, realmodel manifests, formal76 registration QA73/main','65 own-Huber cumulative/protected official comparisons plus actual main export; qualify any winner through a new complete frozen candidate before adoption','continue chronological163+ using administrative predecessor alias with real162 contract76','stop only at explicit 11:00 deadline and then require manual continue'],'global_feasible_direction_exhaustion_proven':False,'compute_resource_boundary_proven':False,'goal_status_to_keep':'active','test_labels_read':False})
    print('Actual handoff12 saved; optimization remains active',flush=True)

if __name__=='__main__':main()
