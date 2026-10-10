"""Replace only the positively owned observer; keep every live scientific attempt."""
from pathlib import Path
import datetime
import hashlib
import json
import os
import subprocess
import sys
import time
import psutil

ROOT=Path(__file__).resolve().parents[1]
A=ROOT/'analysis'
sys.path.insert(0,str(A))
from finalize_main_branch_consolidation_20261005 import owned_pair
OUT=A/'gap_aware_optimization_monitor_handoff_v16_20261005'


def read(path):return json.loads(Path(path).read_text(encoding='utf-8-sig'))
def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def create(path,value):
    with Path(path).open('x',encoding='utf-8') as stream:json.dump(value,stream,ensure_ascii=False,indent=2)


def main():
    assert not OUT.exists()
    assert read(A/'ready_fm_reference_execution_preflight_20261005/verification.json')['status']=='passed'
    old=read(A/'actual_optimization_monitor_launch_v15_20261005.json')
    parent,worker=owned_pair(old['pid'],Path(old['script']),old['script_args'])
    assert not [p for p in parent.children(recursive=True) if p.pid!=worker.pid and p.name().lower()!='conhost.exe']
    OUT.mkdir()
    create(OUT/'frozen_before_handoff.json',{'status':'frozen_before_owned_observer_replacement','old_observer':old,
        'old_worker_pid':worker.pid,'old_worker_creation_time':worker.create_time(),
        'scientific_training_and_quality_processes_untouched':True,'new_quality_scores':0})
    worker.suspend();parent.suspend()
    try:
        import qualified_round_recovery_evidence_v2_20261005 as qualification
        import refresh_optimization_boundary_evidence_20261004 as base
        original=base.complete_round_evidence
        base.complete_round_evidence=qualification.complete_round_evidence
        try:
            import monitor_actual_optimization_progress_v16_20261005 as monitor
            monitor.main(True)
        finally:
            base.complete_round_evidence=original
            qualification.close()
        observed=read(A/'actual_optimization_monitor_state_20261005.json')
        assert observed['active_round']==67 and observed['last_contiguous_registered_completed_round']==66
        assert {83,84}<=set(observed['pending_required_rounds'])
        assert observed['latest_completed_round']==66 and observed['active_root_command_owned']
        create(OUT/'actual_progress_inventory_preflight.json',{'status':'passed',
            'active_round':observed['active_round'],'latest_completed_round':observed['latest_completed_round'],
            'qualified_rounds':observed['qualified_rounds'],'pending_required_rounds':observed['pending_required_rounds'],
            'last_contiguous_registered_completed_round':observed['last_contiguous_registered_completed_round'],
            'best_completed_round':observed['best_completed_round'],'all_old_and_new_rounds_remain_required':True})
    except BaseException:
        parent.resume();worker.resume()
        raise
    worker.terminate();parent.terminate()
    psutil.wait_procs([worker,parent],timeout=10)
    assert not any(p.is_running() for p in (worker,parent))
    driver=A/'monitor_actual_optimization_progress_v16_20261005.py'
    launcher=A/'run_recovery_qualified_workflow_20261005.py'
    run=A/'actual_optimization_monitor_run_v16_20261005.json'
    bindings=dict(read(A/'actual_optimization_monitor_run_v15_20261005.json')['input_sha256'])
    sources=[Path(__file__),driver,launcher,A/'refresh_continuous_progress_v2_20261005.py',
        A/'qualified_round_inventory_20261005.py',A/'refresh_optimization_boundary_evidence_v15_20261005.py',
        OUT/'actual_progress_inventory_preflight.json',A/'ready_fm_reference_execution_preflight_20261005/verification.json',
        A/'ready_fm_reference_quality_followups_20261005/verification.json']
    bindings.update({str(path):sha(path) for path in sources})
    create(run,{'original_driver':str(driver),'original_arguments':[],'input_sha256':bindings,
        'all_registered_rounds_require_actual_scoped_completion':True,'goal_completion_not_inferred':True})
    stdout=A/'run_logs/actual_optimization_monitor_v16_20261005.stdout.log'
    stderr=A/'run_logs/actual_optimization_monitor_v16_20261005.stderr.log'
    env=dict(os.environ)
    for variable in ('TMP','TEMP','TMPDIR'):env[variable]=str(ROOT/'tmp')
    args=[str(driver),str(run)]
    with stdout.open('xb') as output,stderr.open('xb') as error:
        process=subprocess.Popen([str(ROOT/'.venv/Scripts/python.exe'),'-B','-X','utf8',str(launcher),*args],
            cwd=ROOT,env=env,stdout=output,stderr=error,creationflags=subprocess.CREATE_NO_WINDOW)
    job={'pid':process.pid,'script':str(launcher),'script_args':args,'stdout':str(stdout),'stderr':str(stderr),
        'at_local':datetime.datetime.now().isoformat()}
    create(A/'actual_optimization_monitor_launch_v16_20261005.json',job)
    time.sleep(3)
    new_parent,new_worker=owned_pair(process.pid,launcher,args)
    assert not stderr.read_bytes()
    create(OUT/'verification.json',{'status':'passed_owned_gap_aware_observer_handoff',
        'observer':job,'owned_worker_pid':new_worker.pid,'old_operational_observer_closed':True,
        'all67_through84_required_actual_scopes_retained':True,'scientific_training_and_quality_processes_untouched':True,
        'all_new_project_files_D_or_E_only':True,'test_labels_read':False,'new_quality_scores':0})
    print(json.dumps({'status':'passed_gap_aware_monitor_handoff','observer':job,'worker':new_worker.pid},ensure_ascii=False),flush=True)


if __name__=='__main__':main()
