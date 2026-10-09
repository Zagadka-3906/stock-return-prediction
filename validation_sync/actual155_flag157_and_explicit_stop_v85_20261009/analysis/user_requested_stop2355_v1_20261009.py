"""Use the verified stop mechanism with current rounds and durable epoch inventories."""
from pathlib import Path
from datetime import datetime
import sys
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
import user_requested_stop2355_v2_20261008 as core
from scheduled_user_pause_20261007 import read,write
old_inventory=core.checkpoint_inventory
old_stop=core.stop_verified

def checkpoint_inventory():
    result=old_inventory();records=[]
    comparisons=[(152,'SparseAfter14829',29),(153,'BF16Medium78',78),
        (154,'BF16TwoSeed79',79),(155,'BF16Seed10_80',80),(156,'BF16Drop05_81',81)]
    for number,family,expected in comparisons:
        folder=A/f'{family}_official_comparison_v1_20261009'
        saved=sorted(folder.glob('case*_official.json'))
        records.append({'round':number,'expected_cases':expected,'saved_score_records':len(saved),
            'complete_scoring_verification_exists':(folder/'verification.json').is_file(),
            'full_registration_passed':(read(A/f'optimization_20261003_r{number}/full_registration_execution.json')['status']=='passed'
                if (A/f'optimization_20261003_r{number}/full_registration_execution.json').is_file() else False),
            'saved_records':{str(p):core.sha(p) for p in saved}})
    banks=[]
    for bank in sorted(Path('E:/赛题五_本机临时').glob('neural_BF16_medium2048*bank6_v1_20261009')):
        states=[]
        for year in range(2020,2026):
            d=bank/str(year);info=d/'info.json';checkpoint=d/'checkpoint.joblib'
            row={'year':year,'completed_annual_info_exists':info.is_file(),'durable_checkpoint_exists':checkpoint.is_file()}
            if info.is_file():row['saved_info']={'path':str(info),'sha256':core.sha(info),'metadata':read(info)}
            if checkpoint.is_file():row['checkpoint']={'path':str(checkpoint),'bytes':checkpoint.stat().st_size,'sha256':core.sha(checkpoint),'must_verify_training_identity_and_rng_before_resume':True,'incomplete_annual_fit_not_claimed_complete':True}
            states.append(row)
        banks.append({'bank':str(bank),'annual_states':states,'automatic_restart':False})
    result.update(current_round_saved_score_records=records,durable_epoch_checkpoint_inventory=banks,
        recorded_at_local=datetime.now().astimezone().isoformat(),restart_only_after_actual_user_continue=True)
    return result

def stop_verified(folder,config,journal):
    old_stop(folder,config,journal)
    if not config.get('isolated_preflight_target'):
        control={'status':'project_workers_stopped_until_actual_user_manual_continue',
            'at_local':datetime.now().astimezone().isoformat(),'actual_user_instruction':'23:55停止工作',
            'stop_at_local':config['stop_at_local'],'schedule':str(folder/'schedule.json'),
            'activation':str(folder/'actual_schedule_activation.json'),'guard_status':str(folder/'guardian_status.json'),
            'previous_stop_guard_status':str(A/'user_requested_stop2355_until_manual_continue_v2_20261008/guardian_status.json'),
            'disk_recovery_manifest':str(folder/'disk_recovery_manifest.json'),
            'automatic_restart_enabled':False,'resume_only_after_actual_user_continue':True,
            'goal_pause_required_after_actual_deadline':True,'Windows_shutdown_executed':False}
        write(A/'current_user_runtime_control_20261009.json',control)
        write(A/'current_user_runtime_control_20261008.json',control)

if __name__=='__main__':
    core.checkpoint_inventory=checkpoint_inventory;core.stop_verified=stop_verified;core.main()
