"""Finish the unchanged50/47 pilots with full QA, provenance and main publication."""
from pathlib import Path
import importlib
import os
import sys
import time

ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis'
sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from atomic_optimization_observer_writes_20261005 import write
from hidden_windows_child_creation_20261006 import install
from handoff_joint_goss_round97_full_execution_20261006 import suspended_idle

LABELS={105:'robust_residual50',106:'simplex_residual47'}
CASES={105:50,106:47}


def main():
    import psutil
    number=int(sys.argv[1]);assert number in LABELS
    label=LABELS[number]
    out=A/f'{label}_round{number}_complete_registration_v5_20261006'
    assert not out.exists();out.mkdir()
    required=[f'{label}_candidate_inference',f'{label}_candidate_sealing']
    required+=['longer_residual74_round104_full_registration_v2'] if number==105 else [
        'robust_residual50_round105_full_registration_v5','residual_simplex47_scores_evidence_publication']
    identities={};terminal={}
    while True:
        for name in required:
            folder=A/'service_owned_workflows_20261006'/name
            if name not in identities and (folder/'native_launch.json').exists():identities[name]=read(folder/'native_launch.json')
            terminal[name]=read(folder/'service_execution.json') if (folder/'service_execution.json').exists() else None
            if name in identities and not owned(identities[name]) and terminal[name]:assert terminal[name]['status']=='passed',(name,terminal[name])
        state=read(A/'service_owned_dependency_queue_v4_20261006/state.json')
        live={name:row for name,row in state['activated_jobs'].items() if name.startswith('round') and owned(row)}
        writer=state['activated_jobs']['round89']
        execution=Path(writer['script_args'][0]).parent/'execution.json'
        writer_closed=not owned(writer) and execution.exists()
        all_closed=len(identities)==len(required) and all(not owned(r) for r in identities.values())
        passed=all_closed and all(row and row['status']=='passed' for row in terminal.values())
        available=psutil.virtual_memory().available/2**30
        write(out/'waiting_status.json',{'status':'waiting_for_actual_sealed_pilot_preceding_complete_registration_and_terminal_original_writer',
            'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'preceding_terminal_status':terminal,
            'original89_identity':writer,'original89_has_terminal_evidence_and_no_owned_handle':writer_closed,
            'actual_live_original_rounds':live,'available_RAM_GiB':available})
        if passed and not live and writer_closed and available>=9:break
        time.sleep(15)
    plan_path=A/'service_owned_dependency_queue_bootstrap_fields_recovery_v2_20261006/queue_plan.json'
    plan=read(plan_path)
    assert plan['complete_ranking_registration_serialization_markers']==[str(A/f'optimization_20261003_r{n}/full_registration_execution.json') for n in (105,106)]
    prep=A/f'{label}_full_registration_preparation_20261006.json'
    evidence=[Path(__file__),prep,plan_path,execution,Path(writer['stderr']),Path(writer['script_args'][0]),
        A/'optimization_20261003_r89/provenance_scope_execution.json',
        A/'frozen_controller_name_collision_restoration_20261006/source_restoration_verification.json',
        A/'frozen_controller_name_collision_restoration_20261006/verification.json',
        A/'run_dependency_queue_bootstrap_fields_recovery_v1_20261006.py',
        A/'win32_read_handle_hash_cache_with_filename_v2_20261006.py',
        A/'win32_read_handle_hash_cache_20261006.py',A/'win32_read_handle_hash_cache_full104_preflight_20261006.json',
        A/'full105_read_handle_denied_paths_actual_probe_20261006.json']
    for version in ('', '_v2', '_v3', '_v4'):
        for stem in LABELS.values():
            n=105 if stem=='robust_residual50' else 106
            folder=A/'service_owned_workflows_20261006'/f'{stem}_round{n}_full_registration{version}'
            if folder.exists():
                assert (folder/'service_execution.json').exists()
                assert not owned(read(folder/'native_launch.json'))
                evidence+=list(folder.glob('*.json'))+list(folder.glob('*.log'))
    for name in required:
        folder=A/'service_owned_workflows_20261006'/name
        evidence.extend([folder/'native_launch.json',folder/'service_execution.json'])
    for n in (105,106):
        evidence+=list((A/f'optimization_20261003_r{n}').glob('full_registration_failure*.json'))
    evidence+=list((A/'dependency_queue_v11_bootstrap_recovery_20261006').glob('*.json'))
    evidence=list(dict.fromkeys(evidence))
    recovery_pins={**read(prep)['input_sha256'],**{str(p):sha(p) for p in evidence}}
    for path,digest in recovery_pins.items():assert sha(path)==digest,path
    create(out/'actual_admission.json',{'status':'passed_actual_serialized_registration_of_completed_sealed_pilot',
        'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'round':number,'input_sha256':recovery_pins,
        'original89_terminal':read(execution),'scientific_workers_stopped_or_restarted':0,
        'current_running_service_logs_excluded_from_immutable_input_set_and_retained_after_completion':True,
        'test_labels_read':False})
    evidence.append(out/'actual_admission.json')
    recovery_pins[str(out/'actual_admission.json')]=sha(out/'actual_admission.json')
    folder=A/f'optimization_20261003_r{number}'
    if number==105:
        assert read(folder/'actual_registration_preparation.json')['status']=='passed_actual50_scores_controls_and_sealed_selected_model_candidate_registered'
        protocol=read(folder/'protocol.json')
    else:
        assert not (folder/'protocol.json').exists()
        prepare=importlib.import_module(f'register_{label}_round{number}_artifacts_20261006')
        protocol=prepare.main()
    assert not (ROOT/f'results/optimization_20261003_r{number}.json').exists()
    assert not (folder/'provenance_scope_execution.json').exists()
    assert not (A/f'github_validation_sync_main_20261005/round{number}_receipt.json').exists()
    pins={**protocol['input_sha256'],**recovery_pins}
    create(folder/'frozen_before_actual_full_registration_v5.json',{'input_sha256':pins,
        'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'original_scientific_round_handles_all_terminal':True,
        'actual_completed_pilot_scores_and_candidate_seal_unchanged':True,'new_training_or_scoring':False})
    evidence.append(folder/'frozen_before_actual_full_registration_v5.json')
    scratch=ROOT/f'tmp/full_registration{number}_v5_20261006';scratch.mkdir(parents=True,exist_ok=True)
    for key in ('TEMP','TMP','TMPDIR','MPLCONFIGDIR'):os.environ[key]=str(scratch)
    import tempfile
    tempfile.tempdir=str(scratch)
    publisher=read(A/'service_owned_workflows_20261006/main_publisher_v7/native_launch.json')
    held=[];restore_children=install();restore_ranking=None;scope=None;transport=[]
    import publish_classifier_consensus_workflows_20261006 as helpers
    old_git=helpers.sync.git
    def retry_git(*args,**kwargs):
        for attempt in range(3):
            try:return old_git(*args,**kwargs)
            except RuntimeError as error:
                if args[0] not in ('ls-remote','push','fetch') or not any(w in str(error).lower() for w in ('tls','ssl','unable to access','connection','timed out')):raise
                transport.append({'command':args[0],'attempt':attempt+1,'error':str(error)[:1200]})
                if attempt==2:raise
                time.sleep(2)
    try:
        parent,worker,idle=suspended_idle(publisher,'    main (watch_validations_main_v7_20261006.py:71)')
        held.extend((worker,parent))
        create(folder/'actual_main7_idle_before_and_after_hold_v5.json',idle)
        evidence.append(folder/'actual_main7_idle_before_and_after_hold_v5.json')
        from win32_read_handle_hash_cache_with_filename_v2_20261006 import LockedReadHashCache
        scope=LockedReadHashCache(pins);scope.__enter__()
        from publish_explicit_parent_training_round_v2_20261005 import publish
        publish(number,'成熟历史标签的涨停条件残差原生模型与集成','conditional_flag_residual_causal_checks.json',
            [f'预定{CASES[number]}项条件残差及集成官方比较'])
        adapter=importlib.import_module(f'lossless_ranking_runtime_adapter_v{13 if number==105 else 14}_20261006')
        restore_ranking=adapter.install(number)
        import build_all_model_rankings_20261003 as ranking
        import verify_all_model_rankings_20261003 as qa
        ranking.main();qa.main();scope.reverify()
        create(folder/'provenance_scope_execution.json',{'status':'passed','at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),
            'input_sha256':pins,'initial_full_hash_and_Windows_read_share_only_locks':True,
            'final_full_rehash_after_actual_full_ranking_QA':True,'sealed_input_files':len(pins),
            'cache_hits':scope.hits,'nonsealed_paths_rehashed':scope.fresh_calls,
            'actual1599600_row_model_reload_and_cold80_candidate_proofs_preserved':True,
            'all_original_six_view_browser_and_candidate_manifest_QA_passed':True,
            'registered_previously_executed_scope_not_a_new_scientific_freeze':True,
            'new_model_fits':0,'new_quality_scores_by_registration':0,'test_labels_read':False})
        scope.close();scope=None
        publication=A/f'publish_{label}_round{number}_full_validation_20261006.py'
        text=publication.read_text(encoding='utf-8');before='    for path in extra:'
        assert text.count(before)==1
        text=text.replace(before,'    extra += RECOVERY_EVIDENCE\n'+before)
        ns={'__file__':str(publication),'__name__':f'actual_complete_round{number}_registration_recovery_v5',
            'RECOVERY_EVIDENCE':evidence}
        exec(compile(text,str(publication),'exec'),ns)
        helpers.sync.git=retry_git;ns['main']()
        create(folder/'full_registration_execution.json',{'status':'passed','at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),
            'existing_official_scores_registered':CASES[number],
            'full_rankings_and_all_original_QA_and_main_publication_completed':True,
            'scientific_processes_suspended_or_restarted':0,'new_quality_scores_by_registration':0,
            'global_goal_or_resource_exhaustion_claimed':False,'test_labels_read':False})
    except BaseException as error:
        create(folder/'full_registration_failure_v5.json',{'status':'failed_preserved_complete_registration_v5',
            'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'error':f'{type(error).__name__}: {error}'})
        raise
    finally:
        helpers.sync.git=old_git
        if scope is not None:scope.close()
        if restore_ranking is not None:restore_ranking()
        for process in reversed(held):
            if process.is_running():process.resume()
        create(folder/'actual_hidden_registration_children_v5.json',{'events':restore_children(),
            'scientific_workers_not_suspended_stopped_or_restarted':True})
        create(out/'actual_transport_retries.json',{'attempts':transport,'TLS_verification_unchanged':True})


if __name__=='__main__':main()
