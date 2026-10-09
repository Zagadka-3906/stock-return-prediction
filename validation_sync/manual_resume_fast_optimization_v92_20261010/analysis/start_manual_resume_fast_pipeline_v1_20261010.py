"""Verify durable artifacts and resume under new immutable launches until Oct11 11:00."""
from pathlib import Path
from datetime import datetime, timezone, timedelta
import sys,json,time
A=Path(__file__).resolve().parent;ROOT=A.parent
sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from scheduled_user_pause_20261007 import write,inventory
from handoff_ready_goss_full_execution_20261006 import start_service

def main():
    now=datetime.now(timezone(timedelta(hours=8)))
    deadline='2026-10-11T11:00:00+08:00'
    assert now<datetime.fromisoformat(deadline)
    manifest_path=A/'user_requested_immediate_stop_20261009_214340/disk_recovery_manifest.json'
    manifest=read(manifest_path)
    assert not inventory(full=True), 'Existing owned jobs require reconciliation before restart'
    saved=manifest['completed_native_disk_checkpoints']
    delivery=A/'latest_verified_submission_delivery_v2_20261008.json'
    assert sha(delivery)==saved['delivery_pointer_sha256']
    bank=Path('E:/赛题五_本机临时/neural_BF16_medium2048_drop05_seed09_e64_bank6_v1_20261009')
    rows=[]
    for year in range(2020,2026):
        folder=bank/str(year);row={'year':year,'completed':(folder/'info.json').is_file()}
        if row['completed']:
            info=read(folder/'info.json');assert sha(folder/'model.joblib')==info['model_sha256']
            if year<2025:assert sha(folder/'raw.parquet')==info['prediction_sha256']
            row['model_sha256']=info['model_sha256']
        if (folder/'checkpoint.joblib').is_file():
            expected=next(s for b in saved['durable_epoch_checkpoint_inventory'] if Path(b['bank'])==bank for s in b['annual_states'] if s['year']==year)
            digest=sha(folder/'checkpoint.joblib');assert digest==expected['checkpoint']['sha256']
            row['checkpoint_sha256']=digest
        rows.append(row)
    assert [r['year'] for r in rows if r['completed']]==list(range(2020,2025))
    stop_folder=A/'user_requested_stop1100_until_manual_continue_v1_20261011';stop_folder.mkdir(exist_ok=False)
    schedule={'output_folder':str(stop_folder),'stop_at_local':deadline,'automatic_restart_enabled':False,
              'execute_Windows_shutdown':False,'actual_user_instruction':'10月11日上午11点前持续优化，最快速度，节省时间'}
    write(stop_folder/'schedule.json',schedule)
    previous=read(A/'current_user_runtime_control_20261009.json')
    write(stop_folder/'previous_runtime_control.json',previous)
    control={'status':'optimization_active_after_explicit_manual_resume','at_local':now.isoformat(),
             'actual_user_instruction':'现在继续优化模型，模型优化截止时间更改至10月11日上午11点',
             'stop_at_local':deadline,'optimization_deadline_local':deadline,
             'schedule':str(stop_folder/'schedule.json'),'activation':str(stop_folder/'actual_schedule_activation.json'),
             'guard_status':str(stop_folder/'guardian_status.json'),
             'previous_stop_guard_status':str(A/'user_requested_immediate_stop_20261009_214340/guardian_status.json'),
             'disk_recovery_manifest':str(manifest_path),'automatic_restart_enabled':False,
             'resume_only_after_actual_user_continue':True,'immediate_pause':False,
             'goal_pause_required_now':False,'expired_20261009_schedule_superseded':True}
    for name in ('current_user_runtime_control_20261008.json','current_user_runtime_control_20261009.json','current_user_runtime_control_20261010.json'):write(A/name,control)
    specs=[
      ('actual_BF16_medium2048_drop05_seed09_e64_bank6_v1_20261009',[]),
      ('BF16Drop05_156_independent_full5_GPU_controls_v1_20261009',[]),
      ('BF16Drop05_156_actual_native42_calendar_v1_20261009',[]),
      ('BF16Drop05_156_actual_full73_training_v1_20261009',[]),
      ('BF16Drop05_156_prior_complete_forecast_duplicate_audit_v1_20261009',[]),
      ('BF16Drop05_156_complete_chronological_dispatch_v3_20261009',[]),
      ('BF16FlagAfter15217_actual_full_training_controls_v1_20261009',['BF16Drop05_81_round156_full_registration_v1_20261009']),
      ('BF16FlagAfter152157_actual_native14_calendar_v1_20261009',[]),
    ]
    jobs={j['name']:j for j in manifest['jobs_before_stop']['jobs']}
    aliases={name:name+'_manual_resume_v1_20261010' for name,_ in specs}
    drivers={str(Path(jobs[name]['original_driver'])):sha(jobs[name]['original_driver']) for name,_ in specs}
    for name,_ in specs:
        definition=jobs[name]['definition']
        for p,d in definition['input_sha256'].items():assert sha(p)==d,p
    alias_path=A/'manual_resume_service_aliases_v1_20261010.json'
    create(alias_path,{'service_aliases':aliases,'original_driver_sha256':drivers,
                       'administrative_recovery_only':True,'scientific_driver_sources_unchanged':True})
    create(A/'manual_resume_saved_artifact_verification_v1_20261010.json',{
        'status':'passed_saved_five_annual_models_and_durable_epochs_match_stop_manifest',
        'at_local':now.isoformat(),'annual_bank':str(bank),'annual_records':rows,
        'saved_delivery_pointer_sha256':sha(delivery),'recovery_manifest':str(manifest_path),
        'new_fits':0,'new_quality_scores':0,'unadmitted157_quality_v2_not_restarted':True})
    guardian_script=A/'user_requested_stop1100_v1_20261011.py'
    guard=start_service('actual_user_stop1100_wait_manual_continue_v1_20261011',guardian_script.name,
                        ['run','--folder',str(stop_folder)],{str(guardian_script):sha(guardian_script)})
    write(stop_folder/'actual_schedule_activation.json',{'status':'actual_owned_deadline_guard_started','identity':guard,'stop_at_local':deadline})
    write(stop_folder/'handoff_committed.json',{'status':'new_user_deadline_activated','stop_at_local':deadline,'old_guard_not_restarted':True})
    wrapper=A/'manual_resume_service_alias_runtime_v1_20261010.py';launches={}
    for name,gates in specs:
        driver=Path(jobs[name]['original_driver'])
        args=['--driver',str(driver),'--aliases',str(alias_path)]
        for gate in gates:args+=['--wait-for',gate]
        pins={**jobs[name]['definition']['input_sha256'],str(wrapper):sha(wrapper),str(alias_path):sha(alias_path),str(driver):sha(driver)}
        row=start_service(aliases[name],wrapper.name,args,pins)
        launches[name]=row
        print(json.dumps({'resumed':name,'worker_pid':row['owned_worker_pid'],'console':row['actual_native_console_handle']},ensure_ascii=False),flush=True)
    create(A/'actual_manual_resume_fast_pipeline_hidden_launches_v1_20261010.json',{'launches':launches,'guardian':guard,'stop_at_local':deadline})

if __name__=='__main__':main()
