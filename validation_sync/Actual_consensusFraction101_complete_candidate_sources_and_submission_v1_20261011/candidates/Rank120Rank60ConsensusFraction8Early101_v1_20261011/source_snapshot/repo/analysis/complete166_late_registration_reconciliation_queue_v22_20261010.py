"""Finish actual166 recovery, retain the early failure, then expose a truthful predecessor alias."""
from pathlib import Path
from datetime import datetime,timezone,timedelta
import sys,time,shutil
A=Path(__file__).resolve().parent;ROOT=A.parent;sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from scheduled_user_pause_20261007 import write
OUT=A/'continuous_fast_reused_frontiers_v22_20261010'

def allowed():
    now=datetime.now(timezone(timedelta(hours=8)))
    return all(c['status']=='optimization_active_after_explicit_manual_resume' and now<datetime.fromisoformat(c['stop_at_local']) for c in (read(A/n) for n in ('current_user_runtime_control_20261009.json','current_user_runtime_control_20261010.json')))

def main():
    assert allowed();OUT.mkdir(exist_ok=False)
    name='ReusedNN166Quality19_round166_full_registration_late_dynamic_v2_20261010';folder=A/'service_owned_workflows_20261006'/name
    launch=read(folder/'native_launch.json')
    while allowed() and (owned(launch) or not (folder/'service_execution.json').exists()):
        write(OUT/'state.json',{'status':'actual_return166_complete_registration_recovery_running','round':166,'quality_cases':19,'QA':77,'full_service':name,'at_local':time.strftime('%Y-%m-%dT%H:%M:%S')});time.sleep(10)
    if not allowed():return
    assert read(folder/'service_execution.json')['status']=='passed'
    final=read(A/'optimization_20261003_r166/full_registration_execution.json');assert final['status']=='passed' and final['existing_official_scores_registered']==19
    receipt=read(A/'github_validation_sync_main_20261005/round166_receipt.json');assert receipt['status']=='pushed_and_remote_head_verified' and receipt['scored_records']==19
    canonical=A/'service_owned_workflows_20261006/ReusedNN166Quality19_round166_full_registration_v1_20261009'
    archive=canonical.with_name(canonical.name+'_original_early_import_failure_v1_20261010')
    assert not owned(read(canonical/'native_launch.json')) and read(canonical/'service_execution.json')['status']=='failed'
    assert 'ModuleNotFoundError' in read(canonical/'service_execution.json')['failure']
    assert canonical.resolve().is_relative_to((A/'service_owned_workflows_20261006').resolve()) and archive.resolve().is_relative_to((A/'service_owned_workflows_20261006').resolve()) and not archive.exists()
    # Neither this failed workflow folder nor its files may be part of a scientific input lock.
    for path in A.glob('optimization_20261003_r*/protocol.json'):
        assert not any(Path(p).is_relative_to(canonical) for p in read(path).get('input_sha256',{})),path
    records={p.name:sha(p) for p in canonical.iterdir() if p.is_file()}
    canonical.rename(archive);canonical.mkdir()
    for filename in ('native_launch.json','job_definition.json'):
        shutil.copyfile(folder/filename,canonical/filename)
    create(canonical/'service_execution.json',{'status':'passed','at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'actual_service':name,'actual_execution':read(folder/'service_execution.json'),'administrative_alias_only_not_new_computation':True,'original_failed_evidence':str(archive)})
    assert all(sha(archive/n)==d for n,d in records.items())
    create(OUT/'round166_fully_qualified_reconciliation.json',{'status':'passed_actual_full166_original_QA77_main_and_precise_finished_service_alias','receipt':receipt,'original_failure_archive':str(archive),'original_file_sha256':records,'actual_finished_service':name,'new_model_training_scores_or_inference_by_reconciliation':0})
    write(OUT/'state.json',{'status':'actual166_complete_ready_for_next_training_only_direction','round':166,'quality_cases':19,'QA':77,'full_service':name,'receipt':receipt,'at_local':time.strftime('%Y-%m-%dT%H:%M:%S')})
    print({'status':'passed','actual166_main':receipt['commit'],'next':'new prospective forward20 bank after its own CPU and GPU controls'},flush=True)
if __name__=='__main__':main()
