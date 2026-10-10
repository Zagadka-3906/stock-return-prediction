"""Record the actual consistent3 live queue, current main receipt and unchanged fitter after the D-scope repair."""
from pathlib import Path
from datetime import datetime
import sys
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned


def main():
    state=read(A/'actual_BF16wide135_progress_v3_20261008.json')
    launch_path=A/'BF16wide135_complete_hidden_launches_v3_20261008.json';launch=read(launch_path)
    assert len(launch['launches'])==7 and all(owned(row) for row in launch['launches'].values())
    train_path=A/'service_owned_workflows_20261006/actual_neural_BF16_micro8192_bank6_v2_20261008/native_launch.json';train=read(train_path);assert owned(train)
    receipt_path=A/'actual_BF16wide135_receiver_preflight_main_v3_20261008/receipt.json';receipt=read(receipt_path)
    assert receipt['status']=='pushed_and_remote_head_verified' and receipt['branch']=='main'
    source_paths=[Path(__file__),launch_path,train_path,receipt_path,A/'BF16wide40_prospective_routes_v3_20261008.json',
        A/'BF16wide135_D_scoring_scope_v2_20261008.json',A/'actual_BF16wide135_complete_dependency_recovery_v5_20261008.json',
        A/'actual_BF16wide135_consistent_auxiliary_launches_v3_20261008.json',A/'github_validation_sync_main_20261005/round134_receipt.json']
    create(A/'actual_optimization_handoff_v3_20261008.json',{'status':'active_live_unchanged_BF16_fitter_and_complete_consistent3_round135_queue',
        'at_local':datetime.now().isoformat(timespec='seconds'),'deadline_local':state['deadline_local'],'current_live_progress_snapshot':state,
        'current_progress_document':str(A/'actual_BF16wide135_progress_v3_20261008.md'),
        'actual_new_queue':launch['launches'],'actual_fitter_identity':train,'actual_source_preflight_main_receipt':receipt,
        'input_sha256':{str(p):sha(p) for p in source_paths},
        'retired1_and_partial2_waiters_not_to_be_restarted':True,'all_original_failures_and_sources_preserved':True,
        'numeric_model_graph_and_official_scoring_math_unchanged_by_D_path_repair':True,
        'actual135_score_records_at_handoff':state['actual135_quality']['completed_records'],
        'still_required':['Finish remaining2022-2025 own-mature32-epoch BF16 fits.',
            'Finish actual5 full GPU oracle,37 CDF/111 cold controls and3 historical native hooks.',
            'Source admission3, controls main, actual40 official comparisons, score main.',
            'Selected graph/source/calibration freeze and two actual future replays/cold80, or honest exact anchor reuse.',
            'Complete all original six-view45-second QA46 and actual round135 main receipt.'],
        'next_uncovered_direction':'Cross-family Ridge/RFF128/Bayes residual ensembles; freeze new parent after135 result; no new score/future inference for this direction yet.',
        'scientific_workers_not_stopped_or_restarted_by_repair':True,'old_20261007_shutdown_schedule_not_restarted':True,
        'goal_not_paused_or_complete':True,'global_optimization_or_resource_exhaustion_not_proven':True,'test_labels_read':False})
    print('Current handoff3 recorded: real seven-service3 queue, unchanged fitter, qualified134 and main-confirmed receiver repair.',flush=True)


if __name__=='__main__':main()
