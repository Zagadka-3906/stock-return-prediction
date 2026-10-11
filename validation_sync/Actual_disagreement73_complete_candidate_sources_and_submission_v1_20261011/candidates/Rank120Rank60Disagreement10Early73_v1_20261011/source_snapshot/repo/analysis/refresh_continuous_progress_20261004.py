"""Refresh mutable progress only from actual published results and stage proofs."""
from pathlib import Path
from datetime import datetime
import json
import psutil
from refresh_optimization_boundary_evidence_20261004 import complete_round_evidence
ROOT=Path(__file__).resolve().parents[1]


def read(path):return json.loads(path.read_text(encoding='utf-8-sig'))
def write(path,value):path.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')


def main():
    files=[ROOT/'analysis/ongoing_optimization_state.json',ROOT/'analysis/resume_optimization_20261004.json']
    registry=read(files[0])['active_run_registry'];entries=read(ROOT/registry)
    completed=[(int(p.stem.rsplit('_r',1)[1]),read(p)) for p in (ROOT/'results').glob('optimization_20261003_r*.json')]
    latest_published=max(number for number,_ in completed)
    completed=[(number,result) for number,result in completed if number<50 or complete_round_evidence(number) is not None]
    latest,result=max(completed,key=lambda item:item[0]);active=latest+1
    stage_file=ROOT/f'analysis/ongoing_optimization_r{active}_state.json'
    stage=read(stage_file) if stage_file.exists() else {'stage':'not_started','status':'pending'}
    folder=ROOT/f'analysis/optimization_20261003_r{active}'
    waves={p.stem:len(read(p)['results']) for p in folder.glob('wave*_results.json')}
    scores=[r['connected_final_score'] for p in folder.glob('wave*_results.json') for r in read(p)['results'].values()]
    cost=read(ROOT/'analysis/optimization_fit_cost_evidence_20261004.json')
    qa=read(ROOT/'analysis/all_model_ranking_qa/interaction_result.json')
    payload={'round':active,'active_round':active,'stage':stage['stage'],'status':stage['status'],
        'updated_at_local':datetime.now().isoformat(timespec='seconds'),'last_completed_round':latest,'latest_completed_round':latest,
        'latest_published_round':latest_published,'published_rounds_pending_scoped_completion':list(range(latest+1,latest_published+1)),
        'completed_validation_best':result['winner']['connected_final_score'],'queued_rounds':[r['round'] for r in entries if r['round']>active],
        'active_wave_records':waves,'active_partial_score':max(scores,default=None),'partial_scores_not_added_to_completed_board':True,
        'actual_new_annual_fits_completed':cost['total_actual_new_annual_fits'],'five_year_configuration_count':cost['fully_completed_five_year_configurations'],
        'fulltraining_artifacts_ready':cost['fulltraining_artifacts_ready'],'completed_board_records':qa['connected_records'],
        'ranking_qa_status':f"passed_{qa['connected_records']}_records_{qa['source_hashes']}_sources",
        'nonlinear_ridge_resource_scope_audit':'analysis/nonlinear_ridge_resource_scope_audit_20261004.json',
        'global_resource_exhaustion_established':False,'test_labels_read':False}
    entry=next((r for r in entries if r['round']==active),None)
    payload['active_root_pid_live']=bool(entry and psutil.pid_exists(entry['pid']))
    workers=[]
    if payload['active_root_pid_live']:
        try:
            for process in psutil.Process(entry['pid']).children(recursive=True):
                try:
                    command=' '.join(process.cmdline())
                    if 'multiprocessing.spawn' in command and '--multiprocessing-fork' in command:
                        workers.append(process.pid)
                except psutil.Error:
                    continue
        except psutil.Error:
            pass
    payload['active_official_worker_pids']=workers
    payload['active_official_workers']=len(workers)
    payload['official_workers_observed_from_actual_process_tree']=True
    for label in ('additive','fourier'):
        bank=ROOT/f'analysis/{label}_ridge_bank_20261004'
        count=len(list(bank.glob('*/info_202[0-4].json')))
        payload[f'{label}_ridge_annual_fits_completed']=count
        payload[f'{label}_ridge_oof_status']=read(bank/'oof_audit.json')['status'] if (bank/'oof_audit.json').exists() else 'pending'
        payload[f'{label}_ridge_training_status']='passed' if payload[f'{label}_ridge_oof_status']=='passed' else 'running'
        proof=ROOT/f'analysis/{label}_ridge_future_pipelines_qa_20261004/verification.json'
        payload[f'{label}_ridge_future_qa_status']=read(proof)['status'] if proof.exists() else 'pending'
    nonlinear=ROOT/'analysis/nonlinear_stacking_bank_20261004'
    infos=[read(p) for p in nonlinear.glob('*/info_202[0-4].json')]
    payload.update(nonlinear_stacking_annual_artifacts_completed=len(infos),
        nonlinear_stacking_distinct_annual_fits_completed=sum(r['new_model_fits'] for r in infos),
        nonlinear_stacking_oof_status=read(nonlinear/'oof_audit.json')['status'] if (nonlinear/'oof_audit.json').exists() else 'pending_actual_child_replays')
    future=ROOT/'analysis/nonlinear_stacking_future_pipelines_qa_20261004/verification.json'
    payload['nonlinear_stacking_future_qa_status']=read(future)['status'] if future.exists() else 'pending'
    tuning=ROOT/'analysis/fourier_tuning_bank_20261004'
    payload['fourier_tuning_annual_fits_completed']=len(list(tuning.glob('*/info_202[0-4].json')))
    payload['fourier_tuning_oof_status']=read(tuning/'oof_audit.json')['status'] if (tuning/'oof_audit.json').exists() else 'pending'
    payload['fourier_tuning_preflight_status']='passed' if (ROOT/'analysis/fourier_tuning_preflight_20261004/verification.json').exists() else 'pending'
    future=ROOT/'analysis/fourier_tuning_future_pipelines_qa_20261004/verification.json'
    payload['fourier_tuning_future_qa_status']=read(future)['status'] if future.exists() else 'pending'
    payload['fourier_tuning_resource_scope_audit']='analysis/fourier_tuning_resource_scope_audit_20261004.json'
    payload['joint_layer_replay_preflight_status']=read(ROOT/'analysis/role_layer_replay_preflight_20261004/verification.json')['status']
    payload['joint_layer_future_preflight_status']=read(ROOT/'analysis/role_layer_future_replay_qa_20261004/verification.json')['status']
    payload['selected_scheme_graph_compiler_status']=read(ROOT/'analysis/selected_scheme_graph_preflight_v2_20261004/verification.json')['status']
    graph=ROOT/'analysis/whole_selected_scheme_graph_20261004/graph.json'
    payload['whole_selected_graph_status']=read(graph)['status'] if graph.exists() else 'awaiting_completed_rounds_30_through_49'
    for label,folder in (
            ('whole_scheme_validation_runtime','whole_scheme_runtime_preflight_20261004'),
            ('whole_scheme_future_runtime','whole_scheme_future_runtime_qa_20261004'),
            ('whole_scheme_score_preflight','whole_scheme_score_preflight_20261004'),
            ('whole_scheme_proposal_preflight','whole_scheme_round50_proposal_preflight_20261004'),
            ('whole_scheme_release_preflight','whole_scheme_round50_release_preflight_20261004'),
            ('late_context_initialization_recovery','late_context_initialization_recovery_v2_20261004')):
        proof=ROOT/f'analysis/{folder}/verification.json'
        payload[label+'_status']=read(proof)['status'] if proof.exists() else 'pending'
    payload['whole_scheme_joint_round']=50
    joint_scope=ROOT/'analysis/optimization_20261003_r50/provenance_scope_execution.json'
    joint_complete=(ROOT/'results/optimization_20261003_r50.json').exists() and joint_scope.exists() and read(joint_scope)['status']=='passed'
    payload['whole_scheme_joint_quality_status']='completed' if joint_complete else ('running' if active==50 else 'pending_actual_selected_predecessors_orclosed_execution')
    basis=ROOT/'analysis/additive_basis_bank_20261004'
    payload['additive_basis_annual_fits_completed']=len(list(basis.glob('*/info_202[0-4].json')))
    payload['additive_basis_oof_status']=read(basis/'oof_audit.json')['status'] if (basis/'oof_audit.json').exists() else 'running'
    for label,folder in (('additive_basis_native_future','additive_basis_future_models_qa_20261004'),
            ('additive_basis_complete_scheme','additive_basis_complete_scheme_preflight_20261004'),
            ('additive_basis_search_generator','additive_basis_search_generator_preflight_20261004')):
        proof=ROOT/f'analysis/{folder}/verification.json'
        payload[label+'_status']=read(proof)['status'] if proof.exists() else 'pending'
    payload['additive_basis_fulltraining_artifacts_completed']=len(list(basis.glob('*/info_2025.json')))
    payload['additive_basis_actual_native_future_controls_completed']=len(list((ROOT/'analysis/additive_basis_future_models_qa_20261004').glob('*_raw.parquet')))
    payload['additive_basis_resource_scope_audit']='analysis/additive_basis_resource_scope_audit_20261004.json'
    payload['additive_basis_fulltraining_future_resource_scope_audit']='analysis/additive_basis_future_resource_scope_audit_20261004.json'
    capacity=ROOT/'analysis/official_extended_capacity_qa_20261004/verification.json'
    payload['extended_official_capacity_status']=read(capacity)['status'] if capacity.exists() else ('running' if (capacity.parent/'diagnostic_frozen_before_scoring.json').exists() else 'pending')
    payload['extended_official_capacity_evidence']=str(capacity.relative_to(ROOT))
    payload['extended_official_capacity_scope_audit']='analysis/official_extended_capacity_scope_audit_20261004.json'
    payload['lightweight_queue_handoff_status']=read(ROOT/'analysis/late_context_lazy_queue_v2_preflight_20261004/verification.json')['status']
    for label in ('no_dropout_seed','no_dropout_ensemble','neural_interaction','neural_width','portfolio_surrogate','nystrom_ridge'):
        bank=ROOT/f'analysis/{label}_bank_20261004'
        payload[label+'_annual_artifacts_completed']=len(list(bank.glob('*/info_202[0-4].json')))
        payload[label+'_fulltraining_artifacts_completed']=len(list(bank.glob('*/info_2025.json')))
        audit=bank/'oof_audit.json'
        payload[label+'_oof_status']=read(audit)['status'] if audit.exists() else 'pending'
    for label,folder in (('no_dropout_future','no_dropout_seed_future_models_qa_20261004'),
            ('no_dropout_complete_scheme','no_dropout_seed_complete_scheme_preflight_20261004'),
            ('no_dropout_generators','no_dropout_seed_search_generator_preflight_20261004')):
        proof=ROOT/f'analysis/{folder}/verification.json'
        payload[label+'_status']=read(proof)['status'] if proof.exists() else 'pending'
    payload['no_dropout_actual_future_controls_completed']=len(list((ROOT/'analysis/no_dropout_seed_future_models_qa_20261004').glob('*_raw.parquet')))
    payload['no_dropout_seed_resource_scope_audit']='analysis/no_dropout_seed_resource_scope_audit_20261004.json'
    payload['no_dropout_future_resource_scope_audit']='analysis/no_dropout_seed_future_resource_scope_audit_20261004.json'
    payload['no_dropout_expected_official_records']={'53':148,'54':178}
    for label,folder in (('neural_interaction_future','neural_interaction_future_models_qa_20261004'),
            ('neural_interaction_complete_scheme','neural_interaction_complete_scheme_preflight_20261004'),
            ('neural_interaction_generators','neural_interaction_search_generator_preflight_20261004'),
            ('locked_provenance','locked_ensemble_provenance_preflight_20261004'),
            ('locked_model_reuse','locked_no_dropout_model_reuse_preflight_20261004'),
            ('locked_complete_scheme','locked_no_dropout_complete_scheme_preflight_20261004')):
        proof=ROOT/f'analysis/{folder}/verification.json'
        payload[label+'_status']=read(proof)['status'] if proof.exists() else 'pending'
    payload['neural_interaction_expected_official_records']={'55':100,'56':98}
    payload['neural_interaction_resource_scope_audit']='analysis/neural_interaction_resource_scope_audit_20261004.json'
    payload['neural_interaction_future_resource_scope_audit']='analysis/neural_interaction_future_resource_scope_audit_20261004.json'
    payload['neural_interaction_future_controls_completed']=len(list((ROOT/'analysis/neural_interaction_future_models_qa_20261004').glob('*_raw.parquet')))
    wrapper=ROOT/'analysis/frozen_provenance_execution_preflight_20261004/verification.json'
    payload['frozen_provenance_wrapper_status']=read(wrapper)['status'] if wrapper.exists() else 'pending'
    seed_wrapper=ROOT/'analysis/no_dropout_frozen_provenance_execution_preflight_20261004/verification.json'
    payload['seed_ensemble_frozen_provenance_wrapper_status']=read(seed_wrapper)['status'] if seed_wrapper.exists() else 'pending'
    native_capacity=ROOT/'analysis/official_native_thread_capacity_qa_20261004/verification.json'
    payload['native_thread_capacity_status']=read(native_capacity)['status'] if native_capacity.exists() else 'control_running' if (ROOT/'analysis/official_native_thread_capacity_qa_20261004/diagnostic_frozen_before_scoring.json').exists() else 'not_started'
    payload['native_thread_capacity_evidence']=str(native_capacity.relative_to(ROOT))
    gpu_width=ROOT/'analysis/neural_width_capacity_20261004/verification.json'
    payload['neural_width_single_step_resource_status']=read(gpu_width)['status'] if gpu_width.exists() else 'pending'
    payload['neural_width_single_step_resource_evidence']=str(gpu_width.relative_to(ROOT))
    payload['neural_width_complete_training_feasibility_pending']=not (ROOT/'analysis/neural_width_bank_20261004/oof_audit.json').exists()
    for label,folder in (('portfolio_loss','portfolio_surrogate_preflight_v2_20261004'),
            ('portfolio_bank_implementation','portfolio_bank_implementation_preflight_20261004'),
            ('portfolio_generators','portfolio_surrogate_search_generator_preflight_20261004'),
            ('portfolio_future','portfolio_surrogate_future_models_qa_20261004'),
            ('portfolio_complete_scheme','portfolio_surrogate_complete_scheme_preflight_20261004')):
        proof=ROOT/f'analysis/{folder}/verification.json'
        payload[label+'_status']=read(proof)['status'] if proof.exists() else 'pending'
    payload['portfolio_expected_official_records']={'59':100,'60':98}
    execution=ROOT/'analysis/portfolio_surrogate_search_execution_20261004.json'
    if execution.exists():payload['portfolio_training_status']=read(execution)['annual_training_status']
    portfolio_bank=ROOT/'analysis/portfolio_surrogate_bank_20261004'
    payload['portfolio_surrogate_annual_artifacts_completed']=len(list(portfolio_bank.glob('*/info_202[0-4].json')))
    if (portfolio_bank/'protocol.json').exists():
        portfolio_protocol=read(portfolio_bank/'protocol.json')
        minimum_available=float(portfolio_protocol['minimum_available_host_GiB_before_fit_policy'])
        observed_available=psutil.virtual_memory().available
        payload['portfolio_fit_start_memory_policy_GiB']=minimum_available
        payload['portfolio_observed_available_memory_bytes']=observed_available
        payload['portfolio_memory_observation_at_local']=datetime.now().isoformat(timespec='seconds')
        payload['portfolio_fit_start_memory_policy_currently_satisfied']=observed_available>=minimum_available*2**30
        payload['portfolio_memory_observation_does_not_identify_active_training_phase']=True
        payload['portfolio_memory_policy_is_scheduling_not_hardware_limit']=portfolio_protocol['guard_is_scheduling_not_hardware_limit']
        audit=portfolio_bank/'oof_audit.json'
        scope=portfolio_bank/'training_execution_scope.json'
        run=ROOT/'analysis/portfolio_surrogate_training_run_20261004.json'
        job=read(run)
        try:owned=job['script'] in psutil.Process(job['pid']).cmdline()
        except psutil.Error:owned=False
        payload['portfolio_training_owned_root_live']=owned
        if scope.exists() and read(scope)['status']=='failed':payload['portfolio_training_status']='failed_actual_training_execution'
        elif audit.exists() and read(audit)['status']=='passed':payload['portfolio_training_status']='annual_fine_tuning_passed'
        else:payload['portfolio_training_status']='annual_fine_tuning_in_progress' if owned else 'owned_training_process_missing_audit_required'
    payload['portfolio_training_proxy_losses_not_official_quality']=True
    recovery_run=ROOT/'analysis/portfolio_surrogate_scheme_recovery_run_20261005.json'
    if recovery_run.exists():
        job=read(recovery_run)
        try:owned=job['script'] in psutil.Process(job['pid']).cmdline()
        except psutil.Error:owned=False
        recovery=ROOT/'analysis/portfolio_surrogate_complete_scheme_recovery_20261005/verification.json'
        payload['portfolio_complete_scheme_recovery_owned_root_live']=owned
        payload['portfolio_complete_scheme_recovery_status']=read(recovery)['status'] if recovery.exists() else ('pending_actual_corrected_future_controls' if owned else 'terminated_recovery_requires_audit')
        payload['portfolio_complete_scheme_recovery_evidence']=str(recovery.relative_to(ROOT))
    adoption=ROOT/'analysis/new_neural_families_locked_waiter_replacement_20261004.json'
    if adoption.exists():
        payload['new_neural_family_scoped_hash_wrapper_adoption_status']=read(adoption)['status']
        payload['new_neural_family_scoped_hash_wrapper_production_completed_rounds']=[n for n in (57,58,59,60) if (ROOT/f'analysis/optimization_20261003_r{n}/provenance_scope_execution.json').exists() and read(ROOT/f'analysis/optimization_20261003_r{n}/provenance_scope_execution.json')['status']=='passed']
    joint=ROOT/'analysis/joint_and_basis_locked_waiter_replacement_20261004.json'
    if joint.exists():
        payload['joint_and_basis_scoped_hash_wrapper_adoption_status']=read(joint)['status']
        payload['joint_and_basis_scoped_hash_wrapper_production_completed_rounds']=[n for n in (50,51,52) if (ROOT/f'analysis/optimization_20261003_r{n}/provenance_scope_execution.json').exists() and read(ROOT/f'analysis/optimization_20261003_r{n}/provenance_scope_execution.json')['status']=='passed']
    width=ROOT/'analysis/neural_width_bank_20261004'
    payload['neural_width_annual_artifacts_completed']=len(list(width.glob('*/info_202[0-4].json')))
    payload['neural_width_fulltraining_artifacts_completed']=len(list(width.glob('*/info_2025.json')))
    for label,path in (
            ('neural_width_oof',width/'oof_audit.json'),
            ('neural_width_future_qa',ROOT/'analysis/neural_width_future_models_qa_20261004/verification.json'),
            ('neural_width_complete_scheme',ROOT/'analysis/neural_width_complete_scheme_preflight_20261004/verification.json')):
        payload[label+'_status']=read(path)['status'] if path.exists() else 'pending_actual_controls'
    width_future=ROOT/'analysis/neural_width_future_models_qa_20261004'
    payload['neural_width_native_fullfuture_controls_recorded']=len(list(width_future.glob('*_raw.parquet')))
    width_samples=width_future/'resource_samples.jsonl'
    if width_samples.exists():
        # A concurrent sampler can leave an incomplete last line; use its last complete observation.
        for line in reversed(width_samples.read_text(encoding='utf-8').splitlines()):
            try:observation=json.loads(line)
            except json.JSONDecodeError:continue
            payload['neural_width_future_last_sample']=observation
            payload['neural_width_future_last_sample_is_current_process_liveness_proof']=False
            break
        width_job=ROOT/'analysis/neural_width_future_qa_run_20261004.json'
        if width_job.exists():
            job=read(width_job)
            try:payload['neural_width_future_owned_root_live']=job['script'] in psutil.Process(job['pid']).cmdline()
            except psutil.Error:payload['neural_width_future_owned_root_live']=False
    measured=list((ROOT/'analysis').glob('neural_width_measured_prefix*/verification.json'))
    if measured:
        proof=max(measured,key=lambda p:read(p)['completed_models_inspected'])
        payload['actual_neural_width_internal_andmeasured_cost_prefix_evidence']=str(proof.relative_to(ROOT))
        payload['actual_neural_width_completed_models_inspected']=read(proof)['completed_models_inspected']
    inspection=ROOT/'analysis/neural_width_complete_model_inspection_run_20261004.json'
    if inspection.exists():
        job=read(inspection)
        try:payload['all_twenty_width_model_inspection_owned_root_live']=job['script'] in psutil.Process(job['pid']).cmdline()
        except psutil.Error:payload['all_twenty_width_model_inspection_owned_root_live']=False
        proof=ROOT/'analysis/neural_width_complete_model_inspection_execution_20261004/verification.json'
        payload['all_twenty_width_model_inspection_status']=read(proof)['status'] if proof.exists() else 'queued_actual_twenty_fit_checks'
        payload['all_twenty_width_model_inspection_evidence']=str(proof.relative_to(ROOT))
    frontier=ROOT/'analysis/neural_width_frontier_run_20261004.json'
    if frontier.exists():
        job=read(frontier);proof=ROOT/'analysis/neural_width_frontier_20261004/verification.json'
        payload['neural_width_frontier_root_pid_live']=psutil.pid_exists(job['pid'])
        payload['neural_width_frontier_status']=read(proof)['status'] if proof.exists() else 'queued_after_actual_round60_scientific_completion'
        payload['neural_width_frontier_resource_steps_completed']=len(list(proof.parent.glob('width*_result.json')))
        audit=ROOT/'analysis/neural_width_frontier_scope_audit_20261004.json'
        payload['neural_width_frontier_scope_audit_status']=read(audit)['status'] if audit.exists() else 'pending_actual_GPU_andCPU_controls'
        payload['neural_width_frontier_scope_audit_execution_record']='analysis/neural_width_frontier_audit_run_20261004.json'
    worker_frontier=ROOT/'analysis/official_worker_frontier_run_20261004.json'
    if worker_frontier.exists():
        job=read(worker_frontier)
        proof=ROOT/'analysis/official_worker_frontier_execution_20261004/verification.json'
        frozen=proof.parent/'frozen_before_controls.json'
        try:
            payload['official_worker_frontier_owned_root_live']=job['script'] in psutil.Process(job['pid']).cmdline()
        except psutil.Error:
            payload['official_worker_frontier_owned_root_live']=False
        payload['official_worker_frontier_status']=read(proof)['status'] if proof.exists() else ('controls_started' if frozen.exists() else 'queued_after_scientific_andGPU_completion')
        payload['official_worker_frontier_actual_completed_control_jobs']=sum(read(p).get('jobs_completed',0) for label in ('forward','reverse') for p in (ROOT/f'analysis/official_worker_frontier_{label}_qa_20261004').glob('workers*_result.json'))
        audit=ROOT/'analysis/official_worker_frontier_scope_audit_20261004.json'
        payload['official_worker_frontier_scope_audit_status']=read(audit)['status'] if audit.exists() else 'pending_actual_controls'
        payload['official_worker_frontier_evidence']=str(proof.relative_to(ROOT))
        payload['official_worker_frontier_is_resource_only']=True
    nystrom=ROOT/'analysis/nystrom_ridge_training_run_20261004.json'
    if nystrom.exists():
        job=read(nystrom)
        try:payload['nystrom_ridge_owned_training_root_live']=job['script'] in psutil.Process(job['pid']).cmdline()
        except psutil.Error:payload['nystrom_ridge_owned_training_root_live']=False
        for label,folder in (('nystrom_numerical','nystrom_ridge_preflight_20261004'),
                ('nystrom_generators','nystrom_ridge_search_generator_preflight_20261004'),
                ('nystrom_scoped_dispatch','nystrom_ridge_frozen_provenance_preflight_20261004'),
                ('nystrom_future','nystrom_ridge_future_models_qa_20261004'),
                ('nystrom_complete_scheme','nystrom_ridge_complete_scheme_preflight_20261004')):
            proof=ROOT/f'analysis/{folder}/verification.json'
            payload[label+'_status']=read(proof)['status'] if proof.exists() else 'pending_actual_controls'
        payload['nystrom_expected_official_records']={'61':100,'62':98}
        payload['nystrom_queued_after_actual_scientific_GPU_andCPU_scope_audits']=True
    for family in ('neural_width','portfolio_surrogate','nystrom_ridge'):
        run=ROOT/f'analysis/{family}_scheme_count_audit_run_20261004.json'
        if not run.exists():continue
        job=read(run)
        try:
            command=psutil.Process(job['pid']).cmdline()
            owned=job['script'] in command and command[-1]==family
        except psutil.Error:owned=False
        proof=ROOT/f'analysis/{family}_scheme_count_metadata_audit_20261004/verification.json'
        payload[family+'_scheme_count_audit_owned_root_live']=owned
        payload[family+'_scheme_count_audit_status']=read(proof)['status'] if proof.exists() else 'waiting_actual_completed_scheme_proofs'
        payload[family+'_scheme_count_audit_evidence']=str(proof.relative_to(ROOT))
    platform_observation=ROOT/'analysis/platform_goal_status_current_20261004.json'
    if platform_observation.exists():
        observed=read(platform_observation)
        payload['platform_goal_status_last_observed']=observed['last_observed_status']
        payload['platform_goal_status_observed_at_utc']=observed['observed_at_utc']
        payload['platform_goal_status_observation_source']=observed['immutable_observation']
        payload['platform_goal_status_andbackground_execution_are_separate']=True
    for path in files:
        old=read(path)
        old.pop('continuous_goal_status',None)
        old.pop('active_goal_status',None)
        old.update(payload);write(path,old)
    summary_keys=('round','stage','status','last_completed_round','completed_validation_best',
        'active_wave_records','active_official_workers','completed_board_records',
        'actual_new_annual_fits_completed','all_twenty_width_model_inspection_status',
        'portfolio_training_status','nystrom_future_status')
    print(json.dumps({key:payload.get(key) for key in summary_keys},ensure_ascii=False))


if __name__=='__main__':main()
