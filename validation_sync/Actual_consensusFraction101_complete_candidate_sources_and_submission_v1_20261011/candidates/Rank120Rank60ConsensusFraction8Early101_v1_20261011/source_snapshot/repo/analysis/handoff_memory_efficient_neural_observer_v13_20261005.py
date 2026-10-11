"""Verify real producer ordering and E-drive inventory before replacing only the observer."""
from pathlib import Path
import importlib
import os
import sys
import time

ROOT=Path(__file__).resolve().parents[1]
A=ROOT/'analysis'
sys.path[:0]=[str(ROOT),str(A)]
from handoff_recovery_qualified_workflows_20261005 import read,sha,create
from handoff_factorization_machine_repaired_workflows_20261005 import processes,stop
from prepare_gradient_sampling_followups_20261005 import launch


def main():
    out=A/'memory_efficient_neural_observer_handoff_v13_20261005'
    assert not out.exists()
    old=read(A/'actual_optimization_monitor_launch_v12_20261005.json')
    owned=processes(old)
    for process in owned:
        assert process.cmdline()[-len(old['script_args']):]==old['script_args']
    full=read(A/'memory_efficient_neural_followups_20261005/verification.json')
    assert full['status'].startswith('passed')
    for job in (full['native'],full['future'],*full['quality_rounds']):
        processes(job)
        assert not Path(job['stderr']).read_text(encoding='utf-8')
    scripts=[A/'monitor_actual_optimization_progress_v13_20261005.py',
        A/'refresh_memory_efficient_neural_cost_evidence_20261005.py',
        A/'refresh_optimization_boundary_evidence_v12_20261005.py']
    old_guard=read(A/'actual_optimization_monitor_run_v12_20261005.json')['input_sha256']
    for source,digest in old_guard.items():
        assert sha(source)==digest,source
    out.mkdir()
    create(out/'frozen_before_owned_observer_handoff.json',{'status':'frozen_before_actual_integration_and_idle_observer_handoff',
        'previous_monitor':old,'source_sha256':{str(path):sha(path) for path in [Path(__file__),*scripts]},
        'all_native_and_quality_jobs_untouched':True,'new_quality_scores':0})
    paused=[]
    replacement=None
    try:
        for process in owned:
            process.suspend();paused.append(process)
        import qualified_round_recovery_evidence_v2_20261005 as qualification
        import refresh_optimization_boundary_evidence_20261004 as base
        original=base.complete_round_evidence
        base.complete_round_evidence=qualification.complete_round_evidence
        try:
            boundary=importlib.import_module('refresh_optimization_boundary_evidence_v12_20261005')
            assert callable(boundary.complete_round_evidence)
            boundary.main()
            cost=read(A/'optimization_fit_cost_evidence_20261004.json')
            evidence=read(A/'optimization_boundary_evidence_20261004.json')
            assert cost['configurations']==183 and cost['memory_efficient_neural_actual_annual_fits']==0
            assert cost['total_actual_new_annual_fits']==697
            assert evidence['memory_efficient_neural_coverage_evidence']['remaining_required_official_rounds']==[77,78]
            assert evidence['memory_efficient_neural_coverage_evidence']['native_bank_and_scratch_drive']=='E:'
            monitor=importlib.import_module('monitor_actual_optimization_progress_v13_20261005')
            # Run the actual observer, including its previous producers, once.
            monitor.main(True)
            after=read(A/'optimization_fit_cost_evidence_20261004.json')
            state=read(A/'actual_optimization_monitor_state_20261005.json')
            assert after['configurations']==183 and after['memory_efficient_neural_actual_annual_fits']==0
            assert state['latest_completed_round']==66 and state['active_round']==67 and state['active_root_command_owned']
        finally:
            qualification.close()
            base.complete_round_evidence=original
        proof=out/'integration_preflight.json'
        create(proof,{'status':'passed_actual_nested_producers_E_storage_and_complete_fit_observer_integration',
            'actual_declared_configurations':183,'actual_completed_annual_fits':697,
            'actual_new_memory_layout_annual_fits':0,'remaining_memory_layout_quality_rounds':[77,78],
            'actual_latest_qualified_round':66,'actual_active_owned_round':67,
            'pilot_fits_not_counted_as_complete_annual_fits':True,'native_bank_and_scratch_drive':'E:',
            'source_sha256':{str(path):sha(path) for path in [Path(__file__),*scripts]},'new_quality_scores':0})
        run_path=A/'actual_optimization_monitor_run_v13_20261005.json'
        sources=[Path(__file__),*scripts,proof,A/'memory_efficient_neural_complete_search_plan_20261005.json',
            A/'memory_efficient_neural_storage_20261005.json',A/'memory_efficient_neural_followups_20261005/verification.json',
            A/'memory_efficient_neural_workflow_preflight_20261005/verification.json']
        create(run_path,{'original_driver':str(scripts[0]),'original_arguments':[],
            'input_sha256':{**old_guard,**{str(path):sha(path) for path in sources}},
            'monitors_through_actual_qualified_round':78,'actual_E_drive_native_fit_inventory_included':True,
            'goal_completion_not_inferred':True})
        stopped=stop(old)
        paused=[]
        env=dict(os.environ)
        env['PYTHONDONTWRITEBYTECODE']='1'
        for key in ('TMP','TEMP','TMPDIR'):
            env[key]=read(A/'memory_efficient_neural_storage_20261005.json')['temporary_directory']
        launcher=A/'run_recovery_qualified_workflow_20261005.py'
        replacement=launch(launcher,[str(scripts[0]),str(run_path)],'actual_optimization_monitor_v13_20261005',env)
        create(A/'actual_optimization_monitor_launch_v13_20261005.json',replacement)
        time.sleep(6)
        processes(replacement)
        assert not Path(replacement['stderr']).read_text(encoding='utf-8')
        for job in (full['native'],full['future'],*full['quality_rounds']):
            processes(job)
        create(out/'verification.json',{'status':'passed_actual_integration_and_owned_observer_handoff_through78',
            'monitor':replacement,'stopped_only_owned_previous_monitor_processes':stopped,
            'all_native_and_quality_jobs_preserved':True,'original_frozen_sources_RUNs_and_proofs_unchanged':True,
            'actual_cost_and_boundary_integration_proof':str(proof),'only_publication_branch':'main',
            'new_model_fits':0,'new_quality_scores':0,'test_labels_read':False})
        print('Verified actual183 configurations/697 complete fits; observer handed off through78 only.',flush=True)
    finally:
        for process in reversed(paused):
            if process.is_running():process.resume()


if __name__=='__main__':
    main()
