"""Report the real recovered publisher and live replacement stop guard; preserve previous failure snapshots."""
from pathlib import Path
import ast
import importlib.util
import sys
import time

ROOT=Path(__file__).resolve().parents[1]
A=ROOT/'analysis'
sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from prepare_JointCrossHuber147_core_receivers_v1_20261008 import save
from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start
from handoff_joint_goss_round97_full_execution_20261006 import suspended_idle


def main():
    original=A/'monitor_actual_chronological_optimization_progress_v43_20261008.py'
    source=original.read_text(encoding='utf8').replace('progress_v43_20261008','progress_v44_20261008')
    marker="        if (folder/'verification.json').exists():"
    assert source.count(marker)==1
    source=source.replace(marker,"        if number==147:row['scores_main']=status('JointCrossHuberOrder185_scores_main_publication_v2_20261008')\n"+marker)
    source=source.replace('AdaptiveJointCrossHuber148_complete_chronological_dispatch_v4_20261008','AdaptiveJointCrossHuber148_complete_chronological_dispatch_v5_20261008')
    source=source.replace('PureRFFHuber149_complete_chronological_dispatch_v3_20261008','PureRFFHuber149_complete_chronological_dispatch_v4_20261008')
    before="read(A/'user_requested_stop2355_until_manual_continue_20261008/guardian_status.json')"
    assert source.count(before)==1
    source=source.replace(before,"read(Path(state['actual_user_runtime_control']['guard_status']))")
    marker="    write(A/'optimization_live_progress_v44_20261008.json'"
    assert source.count(marker)==1
    source=source.replace(marker,"""    state['joint147_frontier']['original_failed_dispatcher_preserved']=state['joint147_frontier']['chronological_dispatch']
    state['joint147_frontier']['chronological_dispatch']={'status':'recovered_remaining_receivers_started',
        'scores_publication':pipeline['147']['scores_main'],'selected_candidate':pipeline['147']['selected_candidate'],
        'candidate_sealing':pipeline['147']['candidate_sealing'],'full_registration':pipeline['147']['full_registration']}
    state['joint147_frontier']['phase_collision_recovery']=str(A/'Joint147_publisher_phase_scratch_recovery_v7_20261008.json')
    state['pending148_149_phase_collision_prevented_before_quality']=True
"""+marker)
    driver=save('monitor_actual_chronological_optimization_progress_v44_20261008.py',source)
    specification=importlib.util.spec_from_file_location('actual_phase_progress44',driver)
    module=importlib.util.module_from_spec(specification);specification.loader.exec_module(module)
    actual=module.snapshot()
    assert actual['pipeline']['147']['scores_main']['status']=='running'
    assert actual['actual_user2355_stop_guardian']['guardian']['pid']==45768
    assert actual['actual_user2355_stop_guardian']['suspended_entries']==0
    pins={str(path):sha(path) for path in (Path(__file__),original,driver)}
    launch=start('actual_chronological_optimization_progress_observer_v44_20261008',driver.name,[],pins)
    old=read(A/'service_owned_workflows_20261006/actual_chronological_optimization_progress_observer_v43_20261008/native_launch.json')
    tree=ast.parse(original.read_text(encoding='utf8'))
    lines=[node.lineno for node in ast.walk(tree) if isinstance(node,ast.Expr) and isinstance(node.value,ast.Call) and isinstance(node.value.func,ast.Attribute) and node.value.func.attr=='sleep' and len(node.value.args)==1 and isinstance(node.value.args[0],ast.Constant) and node.value.args[0].value==45]
    assert len(lines)==1
    parent,worker,idle=suspended_idle(old,f'    main ({original.name}:{lines[0]})')
    try:
        assert owned(launch) and not worker.children()
        worker.terminate();worker.wait(timeout=10)
        parent.terminate();parent.wait(timeout=10)
    finally:
        for process in (parent,worker):
            if process.is_running():process.resume()
    create(A/'latest_actual_optimization_progress_pointer_v44_20261008.json',{
        'json':str(A/'optimization_live_progress_v44_20261008.json'),'markdown':str(A/'optimization_live_progress_v44_20261008.md'),
        'launch':launch,'new_quality_scores':0})
    create(A/'actual_old_progress43_retired_after44_v1_20261008.json',{
        'status':'retired_only_proved_idle_old_observer','launch':old,'idle_stack':idle,
        'new_observer':launch,'scientific_workers_stopped':0})
    create(A/'actual_optimization_checkpoint_v45_20261008.json',{
        'status':'actual147_live_scoring_preserved_scores_publisher_retry_and_pending148_149_phase_safety_proven',
        'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'best_fully_qualified':actual['best_fully_qualified'],
        'actual147':actual['pipeline']['147'],'actual150':actual['huber_sparse150_frontier'],
        'pending148':actual['adaptive148_frontier'],'pending149':actual['pure149_frontier'],
        'current_user_stop_control':actual['actual_user_runtime_control'],'live_guardian':actual['actual_user2355_stop_guardian'],
        'stop_at_local_preserved':'2026-10-08T23:55:00+08:00','quiet_publishers_quiesce_at_local':'2026-10-08T23:53:00+08:00',
        'new_quality_scores_by_checkpoint':0,'no_early_goal_pause':True,'global_search_or_resource_exhaustion_proven':False})
    print({'new_observer_worker':launch['owned_worker_pid'],'actual_scoring_worker_preserved':41084,'actual_stop_guard':45768},flush=True)


if __name__=='__main__':main()
