"""Current exact service4 handoff, real native audit and ordered historical/new score prerequisites."""
from pathlib import Path
from datetime import datetime
import sys
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned


def main():
    state=read(A/'actual_BF16wide135_progress_v4_20261008.json')
    launch_path=A/'BF16wide135_complete_hidden_launches_v4_20261008.json';launch=read(launch_path)
    assert len(launch['launches'])==7 and all(owned(row) for row in launch['launches'].values())
    train_path=A/'service_owned_workflows_20261006/actual_neural_BF16_micro8192_bank6_v2_20261008/native_launch.json';train=read(train_path);assert owned(train)
    receipt_path=A/'actual_BF16wide135_receiver_preflight_main_v4_20261008/receipt.json';receipt=read(receipt_path)
    assert receipt['status']=='pushed_and_remote_head_verified' and receipt['branch']=='main'
    bank_receipt=A/'CrossFamily_preliminary_controls_main_v1_20261008/bank/receipt.json';native_receipt=read(bank_receipt)
    assert native_receipt['status']=='pushed_and_remote_head_verified'
    audit_path=Path(read(A/'actual_CrossFamily_bank30_synthetic_location_v1_20261008.json')['output'])/'verification.json'
    audit=read(audit_path);assert audit['actual_model_count']==30 and audit['actual_full_OOF_heads']==6 and audit['synthetic_case_count']==90
    cross_services={}
    for name in ('CrossFamily91_parent134_historical_full_controls_v1_20261008','CrossFamily15_native_historical_hooks_v1_20261008','CrossFamily_preliminary_controls_main_publication_v1_20261008'):
        folder=A/'service_owned_workflows_20261006'/name;row=read(folder/'native_launch.json')
        cross_services[name]={'identity':row,'live':owned(row),'terminal':read(folder/'service_execution.json') if (folder/'service_execution.json').exists() else None}
    full=Path('E:/赛题五_本机临时/CrossFamily91_parent134_historical_v1_20261008')
    completed=len(list(full.glob('case*.json'))) if full.exists() else 0
    source_paths=[Path(__file__),launch_path,train_path,receipt_path,bank_receipt,audit_path,
        A/'BF16wide40_prospective_routes_v4_20261008.json',A/'BF16wide135_actual_output_contract_v4_20261008.json',
        A/'actual_BF16wide135_producer_consumer_recovery_v6_20261008.json',A/'actual_BF16wide135_consistent_auxiliary_launches_v4_20261008.json',
        A/'CrossFamily94_round136_plan_v1_20261008.json',A/'predict_CrossFamily_complete_parent_scheme_v1_20261008.py',
        A/'CrossFamily_complete_parent_native_stage_v1_20261008.py',A/'github_validation_sync_main_20261005/round134_receipt.json']
    create(A/'actual_optimization_handoff_v4_20261008.json',{'status':'active_current4_matched_producer_consumer_queue_and_actual_CrossFamily30_native_audit',
        'at_local':datetime.now().isoformat(timespec='seconds'),'deadline_local':state['deadline_local'],'current_live_progress_snapshot':state,
        'current_progress_document':str(A/'actual_BF16wide135_progress_v4_20261008.md'),'actual_new_queue':launch['launches'],
        'actual_fitter_identity':train,'actual_source_preflight_main_receipt':receipt,'actual_crossfamily_native_main_receipt':native_receipt,
        'actual_crossfamily_native_audit':{'model_count':30,'full_OOF_heads':6,'synthetic_cases':90,'synthetic_cold_controls':270,'verification':str(audit_path)},
        'actual_crossfamily_services':cross_services,'actual_crossfamily_historical_cases_completed_excluding_identity':completed,
        'input_sha256':{str(p):sha(p) for p in source_paths},'retired1_2_3_waiters_not_to_be_restarted':True,
        'all_original_failures_and_sources_preserved':True,'physical_data_publication_outputs_version1_and_current_services_version4':True,
        'numeric_model_graph_and_official_scoring_math_unchanged_by_path_repair':True,
        'actual135_score_records_at_handoff':state['actual135_quality']['completed_records'],
        'still_required135':['Finish remaining2022-2025 own-mature32-epoch BF16 fits.',
            'Actual5 full GPU oracle,37 CDF/111 cold controls and3 historical native hooks.',
            'Source admission4, controls main, actual40 official comparisons, score main.',
            'Selected complete graph/source/calibration freeze and actual two future replays/cold80, or exact anchor reuse.',
            'All original six-view45-second QA46 and actual round135 main receipt.'],
        'still_required136':['Finish91 preliminary parent134 full historical CDF/273 cold controls and15 actual historical native hooks; publish main.',
            'Prepare and test all complete94-case136 receivers and native wrapper BEFORE first136 score; D scoring scope, E large outputs.',
            'After135 full qualification, freeze highest qualified112/134/135 complete parent and run91/273 full controls on that exact parent.',
            '94 original official connected comparisons, selected freeze/native independent replays or exact anchor reuse, all original QA47/fullboard/main.'],
        'CrossFamily_future_wrapper_is_unadmitted_draft_until_prospective_and_selected_actual_replay_controls':True,
        'scientific_workers_not_stopped_or_restarted_by_repair':True,'expired_20261007_shutdown_schedule_not_restarted':True,
        'goal_not_paused_or_complete':True,'global_optimization_or_resource_exhaustion_not_proven':True,'test_labels_read':False})
    print('Handoff4: real7 current services, unchanged fitter, bank30/90 controls on main, incomplete135/136 requirements explicit.',flush=True)


if __name__=='__main__':main()
