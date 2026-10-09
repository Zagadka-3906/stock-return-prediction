from pathlib import Path
import sys,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
def main():
    from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start
    script=A/'monitor_actual_chronological_optimization_progress_v69_20261009.py'
    row=start('actual_chronological_optimization_progress_observer_v69_20261009',script.name,[],{str(script):sha(script)})
    assert owned(row)
    create(A/'actual_recovered_progress_hidden_launch_v69_20261009.json',row)
    time.sleep(2)
    p=A/'optimization_live_progress_v69_20261009.json';assert p.exists() and 'drop05_156_frontier' in read(p)
    create(A/'latest_actual_optimization_progress_pointer_v69_20261009.json',{'status':'actual_current_progress','json':str(p),'markdown':str(p.with_suffix('.md')),'actual_observer':row})
    from handoff_joint_goss_round97_full_execution_20261006 import stack,suspended_idle,retire_suspended
    old=read(A/'service_owned_workflows_20261006/actual_chronological_optimization_progress_observer_v68_20261009/native_launch.json')
    if owned(old):
        line=next(line for line in stack(old['owned_worker_pid']).splitlines() if '    main (' in line)
        parent,worker,idle=suspended_idle(old,line)
        try:retire_suspended(old,row)
        except BaseException:
            if parent.is_running():parent.resume()
            if worker.is_running():worker.resume()
            raise
        create(A/'actual_recovered_progress_handoff_v69_20261009.json',{'old':old,'new':row,'old_idle_stack':idle,'scientific_jobs_retired':0})
    print(row['owned_worker_pid'],flush=True)
if __name__=='__main__':main()
