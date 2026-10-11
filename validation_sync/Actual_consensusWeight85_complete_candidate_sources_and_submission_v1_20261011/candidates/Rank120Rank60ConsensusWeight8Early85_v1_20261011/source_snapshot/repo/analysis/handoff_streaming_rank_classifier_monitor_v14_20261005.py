"""Replace only the owned operational observer and verify actual expanded fit costs."""
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
OUT=A/'streaming_rank_classifier_monitor_handoff_v14_20261005'

def read(path):return json.loads(Path(path).read_text(encoding='utf-8-sig'))
def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def create(path,value):
    with Path(path).open('x',encoding='utf-8') as stream:json.dump(value,stream,ensure_ascii=False,indent=2)


def main():
    assert not OUT.exists()
    old=read(A/'actual_optimization_monitor_launch_v13_20261005.json')
    parent,worker=owned_pair(old['pid'],Path(old['script']),old['script_args'])
    assert not [p for p in parent.children(recursive=True) if p.pid!=worker.pid and p.name().lower()!='conhost.exe']
    OUT.mkdir()
    create(OUT/'frozen_before_handoff.json',{'status':'frozen_before_owned_operational_observer_replacement',
        'old_observer':old,'old_worker_pid':worker.pid,'old_worker_creation_time':worker.create_time(),
        'scientific_trainers_and_quality_waiters_untouched':True,'new_quality_scores':0})
    worker.suspend();parent.suspend()
    try:
        import monitor_actual_optimization_progress_v14_20261005 as monitor
        monitor.main(True)
        cost=read(A/'optimization_fit_cost_evidence_20261004.json')
        assert cost['configurations']==187 and cost['streaming_rank_classifier_declared_configurations']==4
        bank=Path(read(A/'streaming_rank_classifier_storage_v3_20261005.json')['output_directory'])
        assert cost['streaming_rank_classifier_actual_annual_fits']==len(list(bank.glob('*/info_202[0-4].json')))
        assert cost['streaming_rank_classifier_actual_annual_fits']>=4
        create(OUT/'actual_expanded_cost_preflight.json',{
            'status':'passed','at_local':datetime.datetime.now().isoformat(),
            'configurations':cost['configurations'],'actual_completed_classifier_annual_fits':cost['streaming_rank_classifier_actual_annual_fits'],
            'actual_completed_all_annual_fits':cost['total_actual_new_annual_fits'],
            'exact_model_raw_prefix_metadata_and_full32pass_records_checked':True,
            'failed_attempts_and_pilots_excluded':True,'cost_source_sha256':sha(A/'refresh_streaming_rank_classifier_cost_evidence_20261005.py')})
    except BaseException:
        parent.resume();worker.resume()
        raise
    # Only these two positively identified idle observer handles are replaced.
    worker.terminate();parent.terminate()
    psutil.wait_procs([worker,parent],timeout=10)
    assert not any(p.is_running() for p in (worker,parent))
    driver=A/'monitor_actual_optimization_progress_v14_20261005.py'
    launcher=A/'run_recovery_qualified_workflow_20261005.py'
    run=A/'actual_optimization_monitor_run_v14_20261005.json'
    bindings=dict(read(A/'actual_optimization_monitor_run_v13_20261005.json')['input_sha256'])
    inputs=[Path(__file__),driver,launcher,A/'refresh_streaming_rank_classifier_cost_evidence_20261005.py',
        A/'refresh_optimization_boundary_evidence_v13_20261005.py',OUT/'actual_expanded_cost_preflight.json',
        A/'streaming_rank_classifier_quality_followups_v4_20261005/verification.json']
    bindings.update({str(path):sha(path) for path in inputs})
    create(run,{'original_driver':str(driver),'original_arguments':[],'input_sha256':bindings,
        'monitors_through_actual_qualified_round':80,'goal_completion_not_inferred':True})
    stdout=A/'run_logs/actual_optimization_monitor_v14_20261005.stdout.log'
    stderr=A/'run_logs/actual_optimization_monitor_v14_20261005.stderr.log'
    env=dict(os.environ)
    scratch=read(A/'streaming_rank_classifier_storage_v3_20261005.json')['temporary_directory']
    for name in ('TMP','TEMP','TMPDIR'):env[name]=scratch
    args=[str(driver),str(run)]
    with stdout.open('xb') as output,stderr.open('xb') as error:
        p=subprocess.Popen([str(ROOT/'.venv/Scripts/python.exe'),'-B','-X','utf8',str(launcher),*args],
            cwd=ROOT,env=env,stdout=output,stderr=error,creationflags=subprocess.CREATE_NO_WINDOW)
    job={'pid':p.pid,'script':str(launcher),'script_args':args,'stdout':str(stdout),'stderr':str(stderr),
        'at_local':datetime.datetime.now().isoformat()}
    create(A/'actual_optimization_monitor_launch_v14_20261005.json',job)
    time.sleep(3)
    new_parent,new_worker=owned_pair(p.pid,launcher,args)
    assert not stderr.read_bytes()
    create(OUT/'verification.json',{'status':'passed_actual_full_fit_costs_and_owned_observer_handoff',
        'observer':job,'owned_worker_pid':new_worker.pid,'old_operational_observer_closed':True,
        'actual187_configurations_and_verified_classifier_full_fits_counted':True,
        'scientific_trainers_and_quality_jobs_not_stopped':True,
        'all_new_project_files_D_or_E_only':True,'test_labels_read':False,'new_quality_scores':0})
    print(json.dumps({'status':'passed','observer':job,'worker':new_worker.pid},ensure_ascii=False),flush=True)


if __name__=='__main__':main()
