"""Retire only a proven idle controller; preserve every scientific worker."""
from pathlib import Path
from copy import deepcopy
import sys
import time

ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis'
sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from handoff_ready_goss_full_execution_20261006 import start_service,pair
from handoff_joint_goss_round97_full_execution_20261006 import suspended_idle

OLD=A/'service_owned_dependency_queue_v4_20261006'
OUT=A/'dependency_queue_v11_bootstrap_recovery_20261006'
QUEUE=A/'service_owned_dependency_queue_v11_recovery_20261006'


def main():
    assert not OUT.exists() and not QUEUE.exists()
    OUT.mkdir();QUEUE.mkdir()
    identity=read(A/'service_owned_workflows_20261006/dependency_queue_v10/native_launch.json')
    assert owned(identity)
    original_plan=read(OLD/'queue_plan_v10.json')
    prior89=read(OLD/'activated_jobs/round89/launch.json')
    assert not owned(prior89)
    assert not (A/'optimization_20261003_r89').exists()
    stderr=OLD/'activated_jobs/round89/stderr.log'
    text=stderr.read_text(encoding='utf-8')
    assert "KeyError: 'recovery_driver_sha256'" in text
    assert 'run_reboot_recovery_attempt_20261006.py", line 20' in text
    assert not (OLD/'activated_jobs/round89/execution.json').exists()
    run=read(OLD/'activated_jobs/round89/run.json')
    assert 'name' not in run and 'recovery_driver_sha256' not in run
    assert run['original_arguments'][0]==str(A/'run_training_round89_v3_pipeline.py')
    for path,digest in run['input_sha256'].items():assert sha(path)==digest,path
    create(OUT/'original89_actual_initialization_failure.json',{
        'status':'failed_bootstrap_before_original_scientific_driver_started',
        'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),
        'identity':prior89,'strong_owned_handle_absent':True,'original_scientific_output_absent':True,
        'failure':"KeyError: 'recovery_driver_sha256'",'stderr':str(stderr),'stderr_sha256':sha(stderr),
        'original_run_sha256':sha(OLD/'activated_jobs/round89/run.json'),
        'missing_required_bootstrap_fields':['name','recovery_driver_sha256'],
        'scientific_validation_completed':False,'test_labels_read':False})
    pins={**original_plan['input_sha256']}
    sources=[Path(__file__),A/'run_dependency_queue_v11_20261006.py',
        A/'run_dependency_queue_v10_20261006.py',A/'run_dependency_queue_v3_20261006.py',
        A/'run_reboot_recovery_attempt_20261006.py',A/'handoff_ready_goss_full_execution_20261006.py',
        A/'handoff_joint_goss_round97_full_execution_20261006.py',OLD/'queue_plan_v10.json',
        OLD/'activated_jobs/round89/run.json',OLD/'activated_jobs/round89/qualified_run.json',
        OLD/'activated_jobs/round89/launch.json',stderr,OUT/'original89_actual_initialization_failure.json']
    pins.update({str(p):sha(p) for p in sources})
    preserved={}
    for name in ('neural16384_annual','quantile_tree_quality_queue_v2','quantile_distribution_views_quality_queue'):
        row=read(A/f'service_owned_workflows_20261006/{name}/native_launch.json')
        if owned(row):preserved[name]=row
    parent=worker=None;new=None;retired=False
    try:
        parent,worker,idle=suspended_idle(identity,'    main (run_dependency_queue_v3_20261006.py:141)')
        create(OUT/'old_controller_actual_idle_before_and_after.json',idle)
        snapshot=read(OLD/'state.json')
        assert snapshot['pid']==worker.pid
        assert snapshot['activated_jobs']['round89']==prior89
        assert not any(owned(row) for row in snapshot['activated_jobs'].values())
        create(OUT/'old_controller_last_actual_snapshot.json',snapshot)
        plan=deepcopy(original_plan)
        activated=deepcopy(snapshot['activated_jobs']);del activated['round89']
        plan.update(status='frozen_full_queue11_required_bootstrap_fields_recovery',
            input_sha256=pins,previously_activated_jobs=activated,
            original_controller_source_sha256=sha(A/'run_dependency_queue_v10_20261006.py'),
            shared_original_state_path=str(OLD/'state.json'),
            prior_queue_plan=str(OLD/'queue_plan_v10.json'),
            initialization_failed_job_preserved={'round89':prior89},
            activation_handoff_commit_marker=str(OUT/'handoff_commit.json'),
            complete_ranking_registration_serialization_markers=[str(A/f'optimization_20261003_r{n}/full_registration_execution.json') for n in (105,106)],
            original_scientific_grids_arguments_and_routes_preserved=True)
        plan['preserved_active_jobs'].update(preserved)
        assert plan['deferred_jobs']==original_plan['deferred_jobs']
        assert plan['registry']==original_plan['registry']
        for path,digest in pins.items():assert sha(path)==digest,path
        plan_path=QUEUE/'queue_plan_v11.json';create(plan_path,plan)
        create(OUT/'frozen_before_actual_handoff.json',{'input_sha256':pins,'old_controller':identity,
            'preserved_owned_scientific_workers':preserved,'all_original_routes':plan['deferred_jobs'],
            'actual_initialization_failure_not_a_completed_validation':True,'scientific_workers_to_stop':0})
        new=start_service('dependency_queue_v11','run_dependency_queue_v11_20261006.py',[str(plan_path)],
            {**pins,str(plan_path):sha(plan_path)})
        for _ in range(120):
            assert owned(new)
            current=read(OLD/'state.json')
            if current['pid']==new['owned_worker_pid']:
                assert current['activated_jobs']==activated;break
            time.sleep(.5)
        else:raise RuntimeError('New held controller did not preserve the complete shared state')
        assert all(owned(row) for row in preserved.values())
        old_parent,old_worker=pair(identity)
        assert not old_worker.children()
        old_worker.terminate();old_worker.wait(timeout=15)
        old_parent.terminate();old_parent.wait(timeout=15)
        retired=True
        create(A/'service_owned_workflows_20261006/dependency_queue_v10/administrative_supersession_bootstrap_recovery_v11_20261006.json',{
            'status':'administratively_retired_idle_helper_not_claimed_scientifically_complete',
            'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'old_identity':identity,'actual_new_identity':new,
            'idle_evidence':str(OUT/'old_controller_actual_idle_before_and_after.json'),
            'scientific_workers_stopped_or_restarted':0})
        create(OUT/'handoff_commit.json',{'status':'retired_original_controller_and_preserved_scientific_workers',
            'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'old_identity':identity,'actual_new_identity':new,
            'original_bootstrap_failure_preserved':True,'scientific_workers_stopped_or_restarted':0})
        create(OUT/'verification.json',{'status':'passed_actual_full_queue11_bootstrap_recovery_handoff',
            'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'input_sha256':pins,'actual_new_identity':new,
            'all_original_deferred_routes_preserved':len(plan['deferred_jobs']),
            'original_shared_state_and_registry_paths_preserved':True,
            'preserved_owned_scientific_workers':preserved,'scientific_workers_stopped_or_restarted':0,
            'new_model_fits':0,'new_quality_scores':0,'test_labels_read':False})
        print('passed_actual_full_queue11_bootstrap_recovery_handoff',flush=True)
    finally:
        if not retired:
            if new is not None and owned(new):
                assert not (OUT/'handoff_commit.json').exists()
                np,nw=pair(new);assert not nw.children();nw.terminate();nw.wait(timeout=15);np.terminate();np.wait(timeout=15)
            for process in (parent,worker):
                if process is not None and process.is_running():process.resume()


if __name__=='__main__':main()
