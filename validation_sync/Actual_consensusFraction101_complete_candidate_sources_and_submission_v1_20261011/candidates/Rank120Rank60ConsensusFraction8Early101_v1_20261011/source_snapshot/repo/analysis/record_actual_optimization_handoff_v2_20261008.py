"""Record actual full135 dispatch and completed two-year training; preserve all original earlier handoffs."""
from pathlib import Path
from datetime import datetime
import sys
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned


def main():
    from monitor_BF16wide135_progress_v1_20261008 import update
    update();state=read(A/'actual_BF16wide135_progress_20261008.json')
    paths=[Path(__file__),A/'monitor_BF16wide135_progress_v1_20261008.py',
        A/'BF16wide40_prospective_routes_v1_20261008.json',A/'BF16wide135_complete_dependency_plan_v1_20261008.json',
        A/'BF16wide135_complete_hidden_launches_v1_20261008.json',A/'actual_BF16wide135_live_progress_monitor_launch_v1_20261008.json',
        A/'actual_BF16wide135_receiver_preflight_main_v1_20261008/receipt.json',
        A/'github_validation_sync_main_20261005/round134_receipt.json',A/'actual_user_submission_deadline_and_priority_20261008.json']
    train=read(A/'service_owned_workflows_20261006/actual_neural_BF16_micro8192_bank6_v2_20261008/native_launch.json')
    assert owned(train)
    launch=read(paths[4]);assert len(launch['launches'])==7
    services={name:{'identity':row,'actually_owned_live':owned(row)} for name,row in launch['launches'].items()}
    best=state['best_fully_qualified'];assert best['round']==134 and best['official_score']==.45114695864085175
    bank=Path('E:/赛题五_本机临时/neural_BF16_micro8192_bank6_v2_20261008')
    annual={str(y):read(bank/str(y)/'info.json') for y in (2020,2021)}
    for info in annual.values():assert info['status']=='passed_actual_complete_mature_BF16_micro_annual_model'
    create(A/'actual_optimization_handoff_v2_20261008.json',{'status':'active_optimization_actual135_entire_pipeline_dispatched_after24_prospective_checks',
        'at_local':datetime.now().isoformat(timespec='seconds'),'deadline_local':state['deadline_local'],'actual_live_progress_snapshot':state,
        'owned_training_identity':train,'actual135_ordered_services':services,'completed_annual_training_evidence':annual,
        'input_sha256':{str(p):sha(p) for p in paths},'round135_entire_quality_pipeline_dispatched':True,
        'actual135_quality_scores_at_handoff':state['actual135_quality']['completed_records'],
        'new_best134_full_QA45_and_remote_main_confirmed':True,'new24_prospective_checks_and_dispatch_published_to_main':True,
        'still_required135':[
            'Remaining own-mature2022-2025 fixed32 BF16 fits, without duplicate workers or old-recipe weight reuse.',
            'Actual full5 GPU independent forecasts,37 full CDF/111 cold controls and3 historical native hooks.',
            'Actual source admission, controls main publication and all40 continuous official comparisons.',
            'Selected complete graph/return mapping/source freeze; two native/independent full future replays and cold80 or exact anchor reuse.',
            'Full six-view45-second QA46, original source/manifest checks and actual round135 main receipt.'
        ],'next_uncovered_direction':{
            'method':'cross_family_Ridge_RFF128_empirical_Bayes_signed_residual_ensembles',
            'additional_bank_fits_expected':0,'bank_bytes_and_full_receivers_must_be_admitted_before_scores':True,
            'current_135_result_needed_before_choosing_new_complete_parent':True,
            'no_new_grid_quality_or_future_inference_dispatched_for_this_direction':True},
        'old_20261007_stop_guard_not_restarted':True,'goal_not_paused_or_complete':True,
        'global_feasible_direction_and_compute_boundary_not_established':True,'test_labels_read':False})
    print('Actual handoff updated: qualified134, two completed years, seven lazy135 steps; goal remains active.',flush=True)


if __name__=='__main__':main()
