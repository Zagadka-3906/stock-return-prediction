"""Adopt one additive round while preserving all live scientific identities."""
from pathlib import Path
from copy import deepcopy
import subprocess
import sys
import time

import psutil

ROOT=Path(__file__).resolve().parents[1]
A=ROOT/'analysis'
sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from atomic_optimization_observer_writes_20261005 import write
from handoff_ready_goss_full_execution_20261006 import start_service,pair

OUT=A/'joint_goss_round97_actual_handoff_recovery_v2_20261006'
QUEUE=A/'service_owned_dependency_queue_v4_20261006'
PUBLIC=('ongoing_optimization_state.json','resume_optimization_20261004.json','actual_optimization_monitor_state_20261005.json')

def row(name):return read(A/f'service_owned_workflows_20261006/{name}/native_launch.json')

def stack(pid):
    p=subprocess.run([str(ROOT/'tools/readonly_pyspy_diagnostics_20261006/py-spy.exe'),'dump','--pid',str(pid)],
        capture_output=True,text=True,encoding='utf-8',errors='replace',timeout=10,creationflags=subprocess.CREATE_NO_WINDOW)
    assert p.returncode==0,p.stderr
    return p.stdout

def suspended_idle(identity,needle):
    parent,worker=pair(identity)
    for _ in range(180):
        before=stack(worker.pid)
        if needle in before:
            worker.suspend();parent.suspend()
            after=stack(worker.pid)
            if needle in after and not worker.children():return parent,worker,{'before':before,'after':after}
            parent.resume();worker.resume()
        time.sleep(1)
    raise RuntimeError('Owned helper did not reach its unchanged idle boundary')

def retire_suspended(identity,successor):
    parent,worker=pair(identity)
    assert not worker.children()
    worker.terminate();worker.wait(timeout=15)
    parent.terminate();parent.wait(timeout=15)
    create(Path(identity['script_args'][0]).parent/'administrative_supersession_for_joint97_20261006.json',{
        'status':'administratively_retired_idle_helper_not_claimed_scientifically_complete',
        'identity':identity,'successor':successor,'scientific_workers_stopped_or_restarted':0,
        'at_local':time.strftime('%Y-%m-%dT%H:%M:%S')})

def main():
    assert not OUT.exists();OUT.mkdir()
    preparation=A/'joint_goss_round97_queue_preparation_20261006/verification.json'
    prep=read(preparation)
    assert prep['status']=='passed_all_original25_routes_preserved_and_additive151_record_dispatch_and_owner_controls'
    pins=deepcopy(prep['input_sha256'])
    pins.update({str(p):sha(p) for p in (Path(__file__),preparation,A/'joint_goss_round97_prospective_github_20261006/receipt.json',
        A/'handoff_ready_goss_full_execution_20261006.py',A/'launch_service_owned_workflow_with_pwsh_20261006.py',
        A/'launch_service_owned_windows_workflow_20261006.ps1',A/'run_service_owned_windows_workflow_20261006.py',
        A/'recover_joint97_handoff_sources_v2_20261006.py',
        A/'interrupted_round95_lossless_snapshot_recovery_20261006/verification.json')})
    for p,digest in pins.items():assert sha(p)==digest,p
    old_queue,old_monitor,old_publisher=row('dependency_queue_v7'),row('progress_monitor_v31'),row('main_publisher_v7')
    preserved={name:row(name) for name in ('neural16384_annual','quantile_tree_quality_queue_v2','quantile_distribution_views_quality_queue')}
    snapshot=read(QUEUE/'state.json')
    preserved.update({name:value for name,value in snapshot['activated_jobs'].items() if name.startswith('round') and owned(value)})
    assert all(owned(value) for value in preserved.values())
    create(OUT/'frozen_before_handoff.json',{'input_sha256':pins,'old_queue':old_queue,'old_monitor':old_monitor,
        'old_publisher':old_publisher,'preserved_scientific_workers':preserved,
        'scientific_grid_for_existing67_through96_unchanged':True,'additional_records':151,'test_labels_read':False})
    suspended=[];new_queue=new_monitor=None;queue_retired=False;monitor_retired=False
    registry_path=Path(read(QUEUE/'queue_plan_v7.json')['registry']);registry_before=read(registry_path)
    try:
        parent,worker,proof=suspended_idle(old_monitor,'    main (monitor_actual_optimization_progress_v18_20261005.py:146)')
        suspended.extend((worker,parent));create(OUT/'old_observer_idle_boundary.json',proof)
        parent,worker,proof=suspended_idle(old_queue,'    main (run_dependency_queue_v3_20261006.py:141)')
        suspended.extend((worker,parent));create(OUT/'old_queue_idle_boundary.json',proof)
        snapshot=read(QUEUE/'state.json');assert snapshot['pid']==old_queue['owned_worker_pid']
        create(OUT/'original_queue_last_snapshot.json',snapshot)
        create(OUT/'registry_before_addition.json',registry_before)
        # main7 already implements all original and new97 exports. Reuse its
        # actual owned process and lock; never retire an in-process serializer.
        publisher=old_publisher
        pair(publisher)
        for _ in range(180):
            assert owned(publisher)
            path=A/'github_validation_sync_main_20261005/state_v7_20261006.json'
            if path.exists() and read(path).get('pid')==publisher['owned_worker_pid'] and read(path)['status']=='monitoring_completed_validations':break
            time.sleep(1)
        else:raise RuntimeError('New main7 did not reach its verified publication loop')
        assert read(A/'github_validation_sync_main_20261005/owner.lock')['pid']==publisher['owned_worker_pid']
        create(OUT/'actual_main7_first_update.json',{'identity':publisher,'state':read(path)})
        plan=read(A/'joint_goss_round97_queue_preparation_20261006/prospective_queue_plan_v10.json')
        plan.update(status='frozen_actual_queue10_additive_joint97_before_dispatch',input_sha256={**plan['input_sha256'],**pins},
            previously_activated_jobs=deepcopy(snapshot['activated_jobs']),
            activation_handoff_commit_marker=str(OUT/'handoff_commit.json'))
        plan['preserved_active_jobs'].update(main_publisher_v7=publisher)
        assert not any(r['round']==97 for r in registry_before)
        registry=deepcopy(registry_before)+[{'round':97,'explicit_parent_round':95,'name':'round97','pid':0,
            'script':str(A/'run_training_round97_v3_pipeline.py'),'script_args':[],'queued_without_heavy_imports':True,
            'prespecified_complete_records':151,'prospective_official_workers':1,'at_local':time.strftime('%Y-%m-%dT%H:%M:%S')}]
        plan_path=QUEUE/'queue_plan_v10.json';create(plan_path,plan);write(registry_path,registry)
        new_queue=start_service('dependency_queue_v10','run_dependency_queue_v10_20261006.py',[str(plan_path)],{**plan['input_sha256'],str(plan_path):sha(plan_path)})
        for _ in range(180):
            assert owned(new_queue)
            current=read(QUEUE/'state.json')
            if current['pid']==new_queue['owned_worker_pid']:
                assert current['activated_jobs']==snapshot['activated_jobs'];break
            time.sleep(1)
        else:raise RuntimeError('New queue10 did not preserve the original activated jobs')
        new_monitor=start_service('progress_monitor_v34','monitor_actual_optimization_progress_v34_20261006.py',[],pins)
        for _ in range(180):
            assert owned(new_monitor)
            docs={name:read(A/name) for name in PUBLIC}
            generations={v.get('complete_observer_generation') for v in docs.values()}
            if (len(generations)==1 and all(v.get('actual_observer_version')==34 and 97 in v['pending_required_rounds']
                    and v.get('dependency_queue_registry')==str((A/'service_owned_workflows_20261006/dependency_queue_v10/native_launch.json').relative_to(ROOT)).replace('\\','/') for v in docs.values())):break
            time.sleep(1)
        else:raise RuntimeError('New monitor34 did not publish one complete generation for actual queue10')
        assert docs[PUBLIC[2]]['pid']==new_monitor['owned_worker_pid']
        for v in docs.values():
            assert v['gradient_sampling_actual_annual_fits']==30 and v['gradient_sampling_actual_final_fits']==6
            assert v['joint_membership_retention_expected_official_records']==151
        create(OUT/'actual_first_complete_observer34_generation.json',{'identity':new_monitor,'documents':docs,'generation':next(iter(generations))})
        assert all(owned(value) for value in preserved.values())
        retire_suspended(old_queue,new_queue);queue_retired=True
        retire_suspended(old_monitor,new_monitor);monitor_retired=True
        suspended.clear()
        create(OUT/'handoff_commit.json',{'status':'retired_original_controller_and_preserved_scientific_workers',
            'actual_queue':new_queue,'actual_publisher':publisher,'actual_observer':new_monitor,
            'new_quality_scores':0,'scientific_workers_stopped_or_restarted':0,'test_labels_read':False})
        for p,digest in pins.items():assert sha(p)==digest,p
        assert all(owned(value) for value in preserved.values())
        create(OUT/'verification.json',{'status':'passed_actual_queue10_main7_observer34_additive_joint97_handoff',
            'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'input_sha256':pins,'actual_queue':new_queue,
            'actual_main_publisher':publisher,'actual_observer':new_monitor,'preserved_scientific_workers':preserved,
            'all_original25_routes_and67_through96_scientific_scope_preserved':True,'additional97_records':151,
            'actual_original_scientific_workers_stopped_or_restarted':0,'new_quality_scores':0,'new_native_fits':0,
            'all_children_hidden_and_project_storage_D_E':True,'test_labels_read':False})
        # Compatibility locations remain the immutable prototype's declared
        # adoption locations. Fill them only after this actual recovery passes.
        compatibility=A/'joint_goss_round97_actual_handoff_20261006'
        recovered=read(OUT/'verification.json')
        recovered.update(recovered_previous_failed_handoff=True,
            actual_recovery_verification=str(OUT/'verification.json'),
            already_owned_main7_reused_without_retirement=True,
            original_failed_handoff_record_preserved=str(compatibility/'failure.json'))
        create(compatibility/'handoff_commit.json',read(OUT/'handoff_commit.json'))
        create(compatibility/'verification.json',recovered)
        print('passed_actual_queue10_main7_observer34_additive_joint97_handoff',flush=True)
    finally:
        if not queue_retired:
            if new_monitor is not None and owned(new_monitor):
                parent,worker=pair(new_monitor);worker.suspend();parent.suspend();retire_suspended(new_monitor,{'reason':'held handoff failed'})
            if new_queue is not None and owned(new_queue):
                assert not (OUT/'handoff_commit.json').exists()
                parent,worker=pair(new_queue);worker.suspend();parent.suspend();retire_suspended(new_queue,{'reason':'held handoff failed before scientific dispatch'})
            if 'snapshot' in locals():write(QUEUE/'state.json',snapshot)
            write(registry_path,registry_before)
        for p in reversed(suspended):
            if p.is_running():p.resume()

if __name__=='__main__':
    try:main()
    except BaseException as exc:
        if OUT.exists() and not (OUT/'failure.json').exists():create(OUT/'failure.json',{'status':'failed_preserved_joint97_actual_handoff','error':f'{type(exc).__name__}: {exc}'})
        raise
