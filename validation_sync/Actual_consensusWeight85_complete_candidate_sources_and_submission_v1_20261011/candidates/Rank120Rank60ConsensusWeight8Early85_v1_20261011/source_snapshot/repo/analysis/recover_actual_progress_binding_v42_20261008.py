"""Complete the observer handoff using each source's actual idle line."""
from pathlib import Path
import ast
import importlib.util
import sys
import time

ROOT=Path(__file__).resolve().parents[1]
A=ROOT/'analysis'
sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from handoff_joint_goss_round97_full_execution_20261006 import suspended_idle
from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start


def main():
    failed=A/'prepare_actual_progress_service_binding_v41_20261008.py'
    create(A/'actual_progress41_idle_line_failure_v1_20261008.json',{
        'status':'failed_only_old_observer_retirement_after_successful_new41_start',
        'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'source_sha256':sha(failed),
        'error':'RuntimeError: Owned helper did not reach its unchanged idle boundary',
        'expected_old_sleep_line':100,'actual_old_sleep_line':103,
        'old40_and_new41_still_owned_no_scientific_workers_stopped':True})
    old_source=A/'monitor_actual_chronological_optimization_progress_v41_20261008.py'
    new_source=A/'monitor_actual_chronological_optimization_progress_v42_20261008.py'
    source=old_source.read_text(encoding='utf8')
    before='JointCrossHuber147_complete_chronological_dispatch_v3_20261008'
    assert source.count(before)==1
    source=source.replace(before,'JointCrossHuber147_complete_chronological_dispatch_v4_20261008').replace('progress_v41_20261008','progress_v42_20261008')
    with new_source.open('x',encoding='utf8',newline='') as stream:stream.write(source)
    spec=importlib.util.spec_from_file_location('actual_progress42',new_source)
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    value=module.snapshot()
    assert value['pipeline']['146']['full_registration']['status']=='passed'
    assert value['joint147_frontier']['chronological_dispatch']['worker']==39376
    pins={str(path):sha(path) for path in (Path(__file__),failed,old_source,new_source)}
    launch=start('actual_chronological_optimization_progress_observer_v42_20261008',new_source.name,[],pins)
    retired=[]
    for version in (40,41):
        path=A/f'monitor_actual_chronological_optimization_progress_v{version}_20261008.py'
        tree=ast.parse(path.read_text(encoding='utf8'))
        lines=[node.lineno for node in ast.walk(tree) if isinstance(node,ast.Expr) and isinstance(node.value,ast.Call) and isinstance(node.value.func,ast.Attribute) and node.value.func.attr=='sleep' and len(node.value.args)==1 and isinstance(node.value.args[0],ast.Constant) and node.value.args[0].value==45]
        assert len(lines)==1
        old=read(A/f'service_owned_workflows_20261006/actual_chronological_optimization_progress_observer_v{version}_20261008/native_launch.json')
        parent,worker,proof=suspended_idle(old,f'    main ({path.name}:{lines[0]})')
        try:
            assert not worker.children() and owned(launch)
            worker.terminate();worker.wait(timeout=10)
            parent.terminate();parent.wait(timeout=10)
        finally:
            for process in (parent,worker):
                if process.is_running():process.resume()
        retired.append({'launch':old,'source_sha256':sha(path),'actual_idle_line':lines[0],'idle_stack':proof})
    create(A/'latest_actual_optimization_progress_pointer_v42_20261008.json',{
        'json':str(A/'optimization_live_progress_v42_20261008.json'),
        'markdown':str(A/'optimization_live_progress_v42_20261008.md'),
        'launch':launch,'new_quality_scores':0})
    create(A/'actual_progress146_and147_receiver_binding_v42_20261008.json',{
        'status':'corrected_actual146_successful_services_and_actual147_dispatch4_and_retired_only_idle_old40_41',
        'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'input_sha256':pins,
        'actual146':value['pipeline']['146'],'actual147':value['joint147_frontier'],
        'new_observer':launch,'retired_observers':retired,'scientific_workers_stopped':0,
        'new_quality_scores':0,'original_failed_attempts_preserved':True})
    print({'status':'progress42_running_with_truthful146_and147_status','worker':launch['owned_worker_pid']},flush=True)


if __name__=='__main__':main()
