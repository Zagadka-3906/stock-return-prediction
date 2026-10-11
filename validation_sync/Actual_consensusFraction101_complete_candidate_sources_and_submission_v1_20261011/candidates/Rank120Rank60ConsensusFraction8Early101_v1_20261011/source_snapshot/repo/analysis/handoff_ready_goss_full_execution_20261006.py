"""Adopt the complete extra GOSS grid while preserving all scientific workers and original grids."""
from pathlib import Path
from copy import deepcopy
import ast
import json
import subprocess
import sys
import time
import psutil

ROOT=Path(__file__).resolve().parents[1]
A=ROOT/'analysis'
sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from atomic_optimization_observer_writes_20261005 import write
from launch_service_owned_workflow_with_pwsh_20261006 import launch

OUT=A/'ready_goss_reference_actual_handoff_20261006'
QUEUE=A/'service_owned_dependency_queue_v4_20261006'
PWSH=Path('C:/Users/esesl/.cache/codex-runtimes/codex-primary-runtime/dependencies/native/powershell/pwsh.exe')


def service_row(name):return read(A/f'service_owned_workflows_20261006/{name}/native_launch.json')
def pair(row):
    assert owned(row)
    parent,worker=psutil.Process(row['pid']),psutil.Process(row['owned_worker_pid'])
    assert parent.create_time()==row['owned_parent_creation_time'] and parent.cmdline()[1:]==worker.cmdline()[1:]
    return parent,worker


def start_service(name,driver,arguments,pins,previous_definition=None):
    folder=A/'service_owned_workflows_20261006'/name
    assert not folder.exists();folder.mkdir()
    definition=deepcopy(previous_definition) if previous_definition else {}
    path=folder/'job_definition.json'
    definition.update(name=name,driver=str(A/driver),arguments=arguments,scratch=str(ROOT/'tmp'/('service_owned_'+name)),input_sha256=pins,bootstrap_sha256=sha(A/'run_service_owned_windows_workflow_20261006.py'))
    definition['command_line']=subprocess.list2cmdline([str(ROOT/'.venv/Scripts/python.exe'),'-B','-X','utf8',str(A/'run_service_owned_windows_workflow_20261006.py'),str(path)])
    create(path,definition)
    result=launch(path,PWSH);create(folder/'verified_hidden_launch.json',result)
    while not (folder/'native_launch.json').exists():
        assert not (folder/'service_execution.json').exists(),read(folder/'service_execution.json')
        time.sleep(.5)
    row=read(folder/'native_launch.json');assert owned(row) and row['actual_native_console_handle']==0 and not row['independent_launch_root_in_any_job']
    return row


def retire(row,reason):
    parent,worker=pair(row)
    # Retire exact helper processes only. Never recurse into scientific children.
    assert not worker.children()
    worker.terminate();worker.wait(timeout=15)
    parent.terminate();parent.wait(timeout=15)
    create(Path(row['script_args'][0]).parent/'administrative_supersession_for_GOSS_20261006.json',{'status':'administratively_retired_helper_not_claimed_scientifically_complete','reason':reason,'identity':row,'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'new_model_fits':0,'new_quality_scores':0,'scientific_workers_terminated':0})


def main():
    assert not OUT.exists()
    proof_path=A/'ready_goss_reference_queue_preparation_20261006/verification.json'
    proof=read(proof_path);assert proof['status']=='passed_actual25_original_and_additional_routes_and_exact_dispatch_expression'
    assert read(A/'GOSS_cost_schema_observer30_preflight_20261006.json')['status']=='passed_actual_complete_monitor30_GOSS_schema_update'
    assert read(A/'service_owned_workflows_20261006/progress_monitor_v28/service_execution.json')['failure']=="KeyError: 'elapsed_seconds'"
    assert not owned(service_row('progress_monitor_v28'))
    pins=deepcopy(proof['source_sha256'])
    sources=[Path(__file__),proof_path,A/'GOSS_cost_schema_observer30_preflight_20261006.json',A/'GOSS_cost_schema_observer30_recovery_20261006.json',A/'prepare_goss_cost_schema_and_monitor30_20261006.py',A/'refresh_gradient_sampling_cost_evidence_v2_20261006.py',A/'monitor_actual_optimization_progress_v30_20261006.py',A/'ready_goss_reference_queue_preparation_github_20261006/receipt.json',A/'launch_service_owned_workflow_with_pwsh_20261006.py',A/'launch_service_owned_windows_workflow_20261006.ps1',A/'run_service_owned_windows_workflow_20261006.py',A/'goss_reference_lossless_publication_adapter_20261006.py',A/'distribution_views_lossless_publication_adapter_20261006.py',A/'collect_full_lossless_round_publication_20261006.py']
    pins.update({str(p.resolve()):sha(p) for p in sources})
    for path,digest in pins.items():assert sha(path)==digest,path
    OUT.mkdir()
    old_queue=service_row('dependency_queue_v6');old_publisher=service_row('main_publisher_v5');old_supplement=service_row('distribution_views_full_ranking_publisher')
    assert all(owned(row) for row in (old_queue,old_publisher,old_supplement))
    original_plan=read(QUEUE/'queue_plan_v6.json')
    prototype=read(A/'ready_goss_reference_queue_preparation_20261006/prospective_queue_plan_v7.json')
    assert prototype['deferred_jobs'][:-2]==original_plan['deferred_jobs']
    preserved={name:service_row(name) for name in ('neural16384_annual','quantile_tree_quality_queue_v2','quantile_distribution_views_quality_queue')}
    assert all(owned(row) for row in preserved.values())
    create(OUT/'frozen_before_actual_handoff.json',{'input_sha256':pins,'old_queue':old_queue,'old_main_publisher':old_publisher,'original_waiting_full93_94_supplement':old_supplement,'preserved_scientific_workers':preserved,'original_deferred_jobs':original_plan['deferred_jobs'],'additional_records':262,'test_labels_read':False})
    observer=start_service('progress_monitor_v30','monitor_actual_optimization_progress_v30_20261006.py',[],pins)
    while True:
        assert owned(observer)
        current=read(A/'actual_optimization_monitor_state_20261005.json')
        if current.get('actual_observer_version')==30 and current.get('pid')==observer['owned_worker_pid']:break
        time.sleep(1)
    create(OUT/'actual_observer_first_complete_update.json',{'status':'passed_actual_owned_observer30_complete_generation','identity':observer,'generation':current['complete_observer_generation'],'original_failed_observer28_retained':True,'new_quality_scores':0})
    # Install actual publication closures before retiring idle old publication helpers.
    import watch_validations_main_v6_20261006 as publisher
    tree=ast.parse(Path(publisher.__file__).read_text(encoding='utf-8'))
    body=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='main').body
    setup=[]
    for node in body:
        if isinstance(node,ast.Try):break
        setup.append(node)
    namespace=vars(publisher).copy();exec(compile(ast.fix_missing_locations(ast.Module(body=setup,type_ignores=[])),str(publisher.__file__),'exec'),namespace)
    assert namespace['sync'].snapshot.__code__.co_filename.endswith('goss_reference_lossless_publication_adapter_20261006.py')
    namespace['sync'].snapshot=namespace['old_snapshot'];namespace['sync'].complete_round_evidence=namespace['old_gate'];namespace['restore_children']()
    old_parent,old_worker=pair(old_publisher);suspended=[]
    try:
        for _ in range(300):
            for process in (old_worker,old_parent):process.suspend();suspended.append(process)
            busy=[p for p in old_parent.children(recursive=True) if p.pid!=old_worker.pid and p.name().lower()!='conhost.exe']
            if not busy:break
            for p in reversed(suspended):p.resume()
            suspended.clear();time.sleep(1)
        else:raise RuntimeError('Main5 still owns a publication command; no retirement performed')
        # The waiting supplement has not published93/94; main6 contains its same
        # complete collect(number,6,124/138) export and raw-blob verifier.
        for number in (93,94):assert not (A/f'distribution_views_full_ranking_publisher_20261006/round{number}_receipt.json').exists()
        retire(old_supplement,'Unfinished full93/94 export transferred to actual main6 identical full collector; original scores and proofs retained.')
        retire(old_publisher,'Same main-only publisher plus full immutable93/94/95/96 export adapters; no validation restarted.')
        suspended.clear()
        publisher_row=start_service('main_publisher_v6','watch_validations_main_v6_20261006.py',[],pins)
        while True:
            assert owned(publisher_row)
            path=A/'github_validation_sync_main_20261005/state_v6_20261006.json'
            if path.exists():
                published=read(path)
                if published.get('pid')==publisher_row['owned_worker_pid'] and published['status']=='monitoring_completed_validations':break
            time.sleep(1)
        assert read(A/'github_validation_sync_main_20261005/owner.lock')['pid']==publisher_row['owned_worker_pid']
        create(OUT/'actual_main6_first_update.json',{'status':'passed_actual_main6_owned_lock_and_complete_loop','identity':publisher_row,'actual_state':published,'all_original_exports_and_complete93_through96_collector_preserved':True,'new_quality_scores':0})
    finally:
        for p in reversed(suspended):
            if p.is_running():p.resume()
    queue_parent,queue_worker=pair(old_queue);retired=False;suspended=[];queue_row=None
    try:
        for p in (queue_worker,queue_parent):p.suspend();suspended.append(p)
        assert not queue_worker.children()
        snapshot=read(QUEUE/'state.json');assert snapshot['pid']==queue_worker.pid
        live_quality={name:row for name,row in snapshot['activated_jobs'].items() if name.startswith('round') and owned(row)}
        create(OUT/'original_queue_last_snapshot.json',snapshot)
        registry_path=Path(original_plan['registry']);registry_before=read(registry_path)
        assert not any(r['round'] in (95,96) for r in registry_before)
        create(OUT/'original_registry_before_additions.json',registry_before)
        registry=deepcopy(registry_before)
        for number,parent in ((95,84),(96,95)):
            registry.append({'round':number,'explicit_parent_round':parent,'name':f'round{number}','pid':0,'script':str(A/f'run_training_round{number}_v3_pipeline.py'),'script_args':[],'queued_without_heavy_imports':True,'prespecified_complete_records':124 if number==95 else 138,'prospective_official_workers':1,'at_local':time.strftime('%Y-%m-%dT%H:%M:%S')})
        plan=deepcopy(prototype)
        # Dispatch the newly ready reference branch immediately after the live
        # round; every old job retains its relative order and exact gate.
        additions=plan['deferred_jobs'][-2:];prior=plan['deferred_jobs'][:-2]
        insertion=next(i for i,j in enumerate(prior) if j['name']=='round86')
        plan['deferred_jobs']=prior[:insertion]+additions+prior[insertion:]
        assert [j for j in plan['deferred_jobs'] if j['name'] not in ('round95','round96')]==original_plan['deferred_jobs']
        plan.update(status='frozen_actual_queue7_GOSS_extension_before_dispatch',input_sha256={**prototype['input_sha256'],**pins},previously_activated_jobs=deepcopy(snapshot['activated_jobs']),activation_handoff_commit_marker=str(OUT/'handoff_commit.json'),prior_queue_plan=str(QUEUE/'queue_plan_v6.json'),addition_priority='After live R85, before original R86; original deferred order and all scientific grids retained',original_required_rounds_retained=list(range(67,95)),additional_required_rounds=[95,96])
        plan['preserved_active_jobs'].update(main_publisher_v6=publisher_row,progress_monitor_v30=observer)
        plan_path=QUEUE/'queue_plan_v7.json';create(plan_path,plan)
        write(registry_path,registry)
        queue_row=start_service('dependency_queue_v7','run_dependency_queue_v7_20261006.py',[str(plan_path)],{**plan['input_sha256'],str(plan_path):sha(plan_path)})
        while True:
            assert owned(queue_row)
            current=read(QUEUE/'state.json')
            if current['pid']==queue_row['owned_worker_pid']:
                assert current['activated_jobs']==snapshot['activated_jobs'];break
            time.sleep(1)
        assert all(owned(row) for row in preserved.values())
        for name,row in live_quality.items():
            if not owned(row):
                assert read(QUEUE/'activated_jobs'/name/'execution.json')['status']=='passed',name
        retire(old_queue,'Actual queue7 retains original23 routes and original67–94 scope, and adds full262 GOSS95/96 records.')
        retired=True;suspended.clear()
        create(OUT/'handoff_commit.json',{'status':'retired_original_controller_and_preserved_scientific_workers','old_controller':old_queue,'actual_new_controller':queue_row,'new_quality_scores':0,'test_labels_read':False})
        for path,digest in pins.items():assert sha(path)==digest,path
        create(OUT/'verification.json',{'status':'passed_actual_queue7_main6_monitor30_handoff_full_original_and_GOSS_scope','actual_queue':queue_row,'actual_main_publisher':publisher_row,'actual_observer':observer,'preserved_scientific_workers':preserved,'previous_live_quality':live_quality,'input_sha256':pins,'original23_routes_and_all_original67_through94_rounds_retained':True,'original198_quantile_and262_distribution_views_scopes_retained':True,'additional95_96_full_records':262,'original_waiting93_94_publication_transferred_to_same_complete_collector':True,'old_failed_observer28_retained':True,'scientific_workers_restarted_or_terminated':0,'new_native_fits':0,'new_quality_scores':0,'test_labels_read':False})
        print('passed_actual_queue7_main6_monitor30_handoff_full_original_and_GOSS_scope',flush=True)
    finally:
        if not retired:
            if queue_row is not None and owned(queue_row):
                assert not (OUT/'handoff_commit.json').exists()
                observed=read(QUEUE/'state.json')
                assert observed['activated_jobs']==snapshot['activated_jobs']
                retire(queue_row,'Failed held-controller adoption; no scientific activation occurred. Original queue resumes.')
            for p in reversed(suspended):
                if p.is_running():p.resume()


if __name__=='__main__':
    try:main()
    except BaseException as error:
        if OUT.exists() and not (OUT/'failure.json').exists():create(OUT/'failure.json',{'status':'failed_preserved_actual_execution_handoff','error':f'{type(error).__name__}: {error}','at_local':time.strftime('%Y-%m-%dT%H:%M:%S')})
        raise
