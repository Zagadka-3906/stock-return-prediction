"""Keep measured search/resource scope distinct from untested boundary claims."""
from pathlib import Path
from datetime import datetime
import hashlib
import json
import psutil
ROOT=Path(__file__).resolve().parents[1]


def read(path):return json.loads(path.read_text(encoding='utf-8-sig'))
def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()


def complete_round_evidence(number):
    result=ROOT/f'results/optimization_20261003_r{number}.json'
    if not result.exists():return None
    value=read(result)
    if value['status']!='complete':return None
    for key in ('component_audit','calibrated_written_csv','method_causal_checks','prediction'):
        if value.get(key,{}).get('status')!='passed':return None
    candidate=Path(value['candidate_submission']).parent/'verification.json'
    official=ROOT/f'analysis/optimization_20261003_r{number}/calibrated_csv_official.json'
    if not candidate.exists() or not official.exists():return None
    pred,scoring=read(candidate),read(official)
    if pred['status']!='passed' or scoring['status']!='passed':return None
    if (pred['rows'],pred['days'],pred['codes'])!=(1599600,344,4650):return None
    if scoring['metrics']!=value['winner']['metrics']:return None
    recovery=None;recovery_snapshot=None
    if number>=50:
        scoped=ROOT/f'analysis/optimization_20261003_r{number}/provenance_scope_execution.json'
        if not scoped.exists():return None
        original_scope=read(scoped)
        if original_scope['status']!='passed':
            if number!=54:return None
            recovery=scoped.parent/'publication_recovery_execution_20261005.json'
            if not recovery.exists():return None
            restored=read(recovery)
            required=('all_original_frozen_inputs_fully_rehashed_andmatched',
                'all_selected_scientific_artifacts_andcandidate_bytes_rehashed_andmatched',
                'Windows_read_share_only_locks_held_during_actual_ranking_andQA',
                'final_full_rehash_before_read_lock_release_passed','all_read_handles_closed',
                'actual_ranking_QA_passed','original_failed_scope_retained')
            if restored['status']!='passed' or not all(restored.get(key) is True for key in required):return None
            if restored.get('original_failure')!="NameError: name 'provenance_ref' is not defined":return None
            if original_scope.get('failure')!=restored['original_failure']:return None
            if restored.get('new_model_fits')!=0 or restored.get('new_quality_scores')!=0 or restored.get('test_labels_read') is not False:return None
            protocol=scoped.parent/'protocol.json';frozen=read(protocol)['input_sha256']
            if restored['original_protocol_frozen_input_files']!=len(frozen):return None
            if any(restored['input_sha256'].get(path)!=expected for path,expected in frozen.items()):return None
            bound={result:'published_result_sha256',protocol:'protocol_sha256',
                scoped:'original_failed_scope_sha256',candidate:'candidate_verification_sha256',
                official:'official_written_CSV_verification_sha256'}
            if any(digest(path)!=restored[key] for path,key in bound.items()):return None
            recovery_snapshot=Path(restored['ranking_qa_snapshot'])
            if digest(recovery_snapshot)!=restored['ranking_qa_snapshot_sha256'] or read(recovery_snapshot)['status']!='passed':return None
    else:scoped=None
    paths=[result,candidate,official]+([scoped] if scoped else [])+([recovery,recovery_snapshot] if recovery else [])
    return {'round':number,'status':'complete_declared_round',
        'score':scoring['metrics']['final_score'],
        'scored_records':value['scored_records'],'candidate_csv_sha256':pred['csv_sha256'],
        'source_sha256':{str(p.relative_to(ROOT)):digest(p) for p in paths}}


def main():
    state=read(ROOT/'analysis/ongoing_optimization_state.json')
    capacity=ROOT/'analysis/official_parallel_capacity_qa_20261004/verification.json'
    controls=read(capacity);assert controls['status']=='passed'
    layer_qa=ROOT/'analysis/role_layer_replay_preflight_20261004/verification.json'
    layer_status=read(layer_qa)['status'] if layer_qa.exists() else 'implementation_controls_running'
    published=[(int(p.stem.rsplit('_r',1)[1]),p,read(p)) for p in (ROOT/'results').glob('optimization_20261003_r*.json')]
    eligible=[row for row in published if row[0]<50 or complete_round_evidence(row[0]) is not None]
    latest,path,result=max(eligible,key=lambda r:r[0])
    closed=[]
    for n,p,value in published:
        if n<22:continue
        if complete_round_evidence(n) is None:continue
        closed.append({'round':n,'score':value['winner']['connected_final_score'],'gain':value['score_gain'],
            'evidence':str(p.relative_to(ROOT)),'sha256':digest(p),
            'scope':'Completed declared grid only; no claim about all variants of this method.'})
    resources=[]
    for label in ('expanded_future','expanded_future_recovery','additive_ridge','fourier_ridge','nonlinear_stacking','nonlinear_stacking_recovery','fourier_tuning','additive_basis','no_dropout_seed','neural_interaction'):
        folder_name=f'{label.removesuffix("_recovery")}_resource_observations_recovery_20261004' if label.endswith('_recovery') else f'{label}_resource_observations_20261004'
        folder=ROOT/'analysis'/folder_name
        summary=folder/'summary.json'
        if not summary.exists():
            if (folder/'protocol.json').exists():resources.append({'scope':str(folder.relative_to(ROOT)),'status':'sampling_in_progress'})
            continue
        value=read(summary)
        resources.append({'scope':str(folder.relative_to(ROOT)),'status':value['status'],'summary_sha256':digest(summary),
            'minimum_available_ram_GiB_sampled':value['minimum_available_ram_bytes_sampled']/2**30,
            'maximum_tracked_rss_GiB_sampled':value['maximum_tracked_python_rss_sum_bytes_sampled']/2**30,
            'physical_exhaustion_proved':False})
    future_audit=ROOT/'analysis/additive_basis_future_resource_scope_audit_20261004.json'
    if future_audit.exists():
        value=read(future_audit);assert value['status']=='passed'
        resources.append({'scope':'analysis/additive_basis_future_models_qa_20261004','status':value['status'],
            'scope_audit':str(future_audit.relative_to(ROOT)),'scope_audit_sha256':digest(future_audit),
            'minimum_available_ram_GiB_sampled':value['minimum_available_ram_GiB_sampled'],
            'maximum_single_qa_python_rss_GiB_sampled':value['maximum_qa_python_rss_GiB_sampled'],
            'samples':value['samples'],'actual_official_worker_count_samples':value['actual_official_worker_count_samples'],
            'physical_exhaustion_proved':False})
    basis_complete=ROOT/'analysis/additive_basis_complete_scheme_preflight_20261004/verification.json'
    basis_status=read(basis_complete)['status'] if basis_complete.exists() else 'pending'
    no_dropout_future=ROOT/'analysis/no_dropout_seed_future_models_qa_20261004/verification.json'
    no_dropout_complete=ROOT/'analysis/no_dropout_seed_complete_scheme_preflight_20261004/verification.json'
    no_dropout_resources=ROOT/'analysis/no_dropout_seed_future_resource_scope_audit_20261004.json'
    if no_dropout_resources.exists():
        value=read(no_dropout_resources);assert value['status']=='passed'
        resources.append({'scope':'analysis/no_dropout_seed_future_models_qa_20261004','status':value['status'],
            'scope_audit':str(no_dropout_resources.relative_to(ROOT)),'scope_audit_sha256':digest(no_dropout_resources),
            'minimum_available_ram_GiB_sampled':value['minimum_available_ram_GiB_sampled'],
            'maximum_single_qa_python_rss_GiB_sampled':value['maximum_qa_python_rss_GiB_sampled'],
            'samples':value['samples'],'actual_official_worker_count_samples':value['actual_official_worker_count_samples'],
            'physical_exhaustion_proved':False})
    width_future=ROOT/'analysis/neural_width_future_resource_scope_audit_20261004.json'
    if width_future.exists():
        value=read(width_future)
        assert value['status']=='passed' and value['actual_completed_fulltraining_models']==4
        resources.append({'scope':'analysis/neural_width_future_models_qa_20261004',
            'status':value['status'],'scope_audit':str(width_future.relative_to(ROOT)),
            'scope_audit_sha256':digest(width_future),
            'actual_completed_fulltraining_models':value['actual_completed_fulltraining_models'],
            'actual_future_rows':value['actual_future_rows'],'samples':value['samples'],
            'minimum_available_ram_GiB_sampled':value['minimum_available_ram_GiB_sampled'],
            'maximum_single_qa_python_rss_GiB_sampled':value['maximum_qa_python_rss_GiB_sampled'],
            'samples_with_actual_official_workers':value['samples_with_actual_official_workers'],
            'start_reserve_is_not_a_guarantee_of_peak_free_memory':True,
            'not_an_isolated_per_width_memory_or_throughput_benchmark':True,
            'physical_exhaustion_proved':False})
    interaction_resources=ROOT/'analysis/neural_interaction_future_resource_scope_audit_20261004.json'
    portfolio_future_resources=ROOT/'analysis/portfolio_surrogate_future_resource_scope_audit_20261004.json'
    if portfolio_future_resources.exists():
        value=read(portfolio_future_resources)
        assert value['status']=='passed' and value['actual_completed_fulltraining_models']==4
        resources.append({'scope':'analysis/portfolio_surrogate_future_models_qa_20261004',
            'status':value['status'],'scope_audit':str(portfolio_future_resources.relative_to(ROOT)),
            'scope_audit_sha256':digest(portfolio_future_resources),
            'actual_completed_fulltraining_models':value['actual_completed_fulltraining_models'],
            'actual_future_rows':value['actual_future_rows'],'samples':value['samples'],
            'minimum_available_ram_GiB_sampled':value['minimum_available_ram_GiB_sampled'],
            'maximum_single_qa_python_rss_GiB_sampled':value['maximum_qa_python_rss_GiB_sampled'],
            'samples_with_actual_official_workers':value['samples_with_actual_official_workers'],
            'startup_memory_reserves_do_not_guarantee_peak_free_memory':True,
            'not_an_isolated_per_configuration_memory_or_throughput_benchmark':True,
            'physical_exhaustion_proved':False})
    portfolio_resources=ROOT/'analysis/portfolio_surrogate_resource_scope_audit_20261004.json'
    if portfolio_resources.exists():
        value=read(portfolio_resources)
        assert value['status']=='passed' and value['actual_completed_annual_fits']==20
        resources.append({'scope':'analysis/portfolio_surrogate_resource_observations_20261004',
            'status':value['status'],'scope_audit':str(portfolio_resources.relative_to(ROOT)),
            'scope_audit_sha256':digest(portfolio_resources),
            'actual_completed_annual_fits':value['actual_completed_annual_fits'],
            'five_year_native_configurations':value['five_year_native_configurations'],
            'samples':value['samples'],
            'minimum_available_ram_GiB_sampled':value['minimum_available_ram_GiB_sampled'],
            'maximum_tracked_python_rss_GiB_sampled':value['maximum_tracked_python_rss_GiB_sampled'],
            'actual_spawned_official_worker_count_samples':value['actual_spawned_official_worker_count_samples'],
            'sampler_includes_serialized_admission_wait_before_actual_training':value['sampler_includes_serialized_admission_wait_before_actual_training'],
            'sum_RSS_may_count_shared_pages_more_than_once':True,
            'future_fulltraining_andinference_peak_not_in_this_sampler_window':True,
            'not_an_isolated_per_configuration_memory_or_throughput_benchmark':True,
            'physical_exhaustion_proved':False})
    if interaction_resources.exists():
        value=read(interaction_resources);assert value['status']=='passed'
        resources.append({'scope':'analysis/neural_interaction_future_models_qa_20261004','status':value['status'],
            'scope_audit':str(interaction_resources.relative_to(ROOT)),'scope_audit_sha256':digest(interaction_resources),
            'minimum_available_ram_GiB_sampled':value['minimum_available_ram_GiB_sampled'],
            'maximum_single_qa_python_rss_GiB_sampled':value['maximum_qa_python_rss_GiB_sampled'],
            'samples':value['samples'],'actual_official_worker_count_samples':value['actual_official_worker_count_samples'],
            'physical_exhaustion_proved':False})
    extended=ROOT/'analysis/official_extended_capacity_qa_20261004/verification.json'
    extended_payload=read(extended) if extended.exists() else None
    provenance=ROOT/'analysis/locked_ensemble_provenance_preflight_20261004/verification.json'
    model_reuse=ROOT/'analysis/locked_no_dropout_model_reuse_preflight_20261004/verification.json'
    memory=psutil.virtual_memory();disk=psutil.disk_usage(str(ROOT.anchor))
    output={'status':'search_and_resource_boundaries_not_yet_established','updated_at_local':datetime.now().isoformat(timespec='seconds'),
        'selection_standard':'后续选模标准.md','completed_best':result['winner']['connected_final_score'],'latest_completed_round':latest,
        'completed_declared_searches':sorted(closed,key=lambda r:r['round']),
        'current_machine_snapshot':{'total_ram_GiB':memory.total/2**30,'available_ram_GiB':memory.available/2**30,
            'cpu_physical_cores':psutil.cpu_count(logical=False),'cpu_logical_cores':psutil.cpu_count(),
            'workspace_volume_total_GiB':disk.total/2**30,'workspace_volume_free_GiB':disk.free/2**30,
            'snapshot_is_observation_not_a_limit_or_completed_capacity_test':True},
        'active_round':state['round'],'active_stage':state['stage'],'pending_rounds':state['queued_rounds'],
        'measured_official_scoring_capacity':[{'workers':r['workers'],'jobs':r['jobs'],'records_per_minute':r['records_per_minute'],
            'minimum_available_ram_GiB_sampled':r['minimum_available_bytes_sampled']/2**30,
            'all_eight_metrics_bit_identical':r['all_eight_metrics_bit_identical']} for r in controls['execution_controls']],
        'capacity_experiment_evidence':str(capacity.relative_to(ROOT)),'capacity_experiment_sha256':digest(capacity),
        'capacity_scope':controls['scope'],'resource_observations':resources,
        'extended_scorer_capacity_evidence':str(extended.relative_to(ROOT)),
        'extended_scorer_capacity_scope_audit':'analysis/official_extended_capacity_scope_audit_20261004.json',
        'extended_scorer_capacity_status':extended_payload['status'] if extended_payload else ('running' if (extended.parent/'diagnostic_frozen_before_scoring.json').exists() else 'pending'),
        'extended_scorer_capacity_controls':extended_payload['execution_controls'] if extended_payload else [],
        'extended_scorer_capacity_scope':extended_payload['scope'] if extended_payload else 'Four, five, six andeight scorer controls on an already selected training-only CSV; no hardware maximum inferred while controls are pending.',
        'native_thread_capacity_evidence':'analysis/official_native_thread_capacity_qa_20261004/verification.json',
        'native_thread_capacity_scope_audit':'analysis/official_native_thread_capacity_scope_audit_20261004.json',
        'native_thread_capacity_production_adopted':False,
        'neural_width_single_step_capacity_evidence':'analysis/neural_width_capacity_20261004/verification.json',
        'neural_width_single_step_capacity_scope_audit':'analysis/neural_width_capacity_scope_audit_20261004.json',
        'neural_width_single_step_does_not_establish_complete_fit_feasibility':True,
        'resource_interpretation_evidence':'analysis/nonlinear_ridge_resource_scope_audit_20261004.json',
        'fourier_tuning_resource_interpretation_evidence':'analysis/fourier_tuning_resource_scope_audit_20261004.json',
        'open_feasible_directions':[
            {'method':'Complete official evaluation of all prepared models and output schemes','evidence':state['active_run_registry'],'reason':'Prepared rounds remain active or gated; training andimplementation checks alone do not establish comparative quality.'},
            {'method':'Jointly refine earlier and later selected augmentation layers','evidence':'analysis/role_layer_replay_20261004.py',
             'layer_kernel_preflight_status':layer_status,
             'preflight_evidence':str(layer_qa.relative_to(ROOT)),
             'future_kernel_evidence':'analysis/role_layer_future_replay_qa_20261004/verification.json',
             'recipe_graph_compiler_evidence':'analysis/selected_scheme_graph_preflight_v2_20261004/verification.json',
             'actual_selected_graph_assembler':'analysis/assemble_selected_scheme_graph_20261004.py',
             'whole_validation_runtime_evidence':'analysis/whole_scheme_runtime_preflight_20261004/verification.json',
             'whole_future_runtime_evidence':'analysis/whole_scheme_future_runtime_qa_20261004/verification.json',
             'joint_official_round':50,
             'reason':'Whole runtimes pass actual complete historical validation andfuture CSV controls; the actual selected R30–49 provenance graph, R50 joint quality comparison andcandidate remain pending.'},
            {'method':'Complete matched Fourier feature-count, seed and penalty sensitivity','evidence':'analysis/fourier_tuning_training_run_20261004.json','reason':'All50 annual fits, OOF replay andcopied future-model controls passed; complete official output comparisons in R47–48 remain pending.'},
            {'method':'Alternative fixed additive basis layouts','evidence':'analysis/additive_basis_bank_20261004/protocol.json',
             'numerical_preflight_evidence':'analysis/additive_basis_preflight_20261004/verification.json',
             'actual_annual_fits_completed':state.get('additive_basis_annual_fits_completed',0),
             'resource_scope_audit':'analysis/additive_basis_resource_scope_audit_20261004.json',
             'fulltraining_future_resource_scope_audit':str(future_audit.relative_to(ROOT)),
             'generator_evidence':'analysis/additive_basis_search_generator_preflight_20261004/verification.json',
             'actual_complete_scheme_control_evidence':str(basis_complete.relative_to(ROOT)),
             'actual_complete_scheme_control_status':basis_status,
             'queued_official_rounds':[51,52],
             'reason':f'All60 narrow252-column andwide378-column annual fits pass actual replay andmaturity controls. All12 mature full-trained models pass future model replay. Actual generators emit196 role and258 standalone records; complete scheme implementation controls:{basis_status}. Official quality comparison andselected candidates still require actual R50/R51 predecessors.'},
            {'method':'Matched no-dropout neural seeds, epochs andequal-weight ensembles',
             'evidence':'analysis/no_dropout_seed_complete_output_search_plan_20261004.json',
             'actual_native_annual_fits':state.get('no_dropout_seed_annual_artifacts_completed',0),
             'actual_virtual_annual_artifacts':state.get('no_dropout_ensemble_annual_artifacts_completed',0),
             'future_model_qa_status':read(no_dropout_future)['status'] if no_dropout_future.exists() else 'pending',
             'complete_scheme_qa_status':read(no_dropout_complete)['status'] if no_dropout_complete.exists() else 'pending',
             'resource_scope_audit':'analysis/no_dropout_seed_resource_scope_audit_20261004.json',
             'queued_official_rounds':[53,54],
             'reason':'All20 new native annual fits,20 virtual annual forecasts, eight full-training future controls andcomplete scheme checks pass actual replay. The326 official output comparisons after actual R52/R53 predecessors remain pending.'},
            {'method':'Reduce repeated immutable provenance hashing with scoped read locks',
             'evidence':str(provenance.relative_to(ROOT)),
             'actual_recursive_control_status':read(provenance)['status'] if provenance.exists() else 'pending',
             'actual_model_reuse_control_status':read(model_reuse)['status'] if model_reuse.exists() else 'pending',
             'adopted_in_live_queued_rounds':(ROOT/'analysis/neural_interaction_locked_waiter_replacement_20261004.json').exists() and read(ROOT/'analysis/neural_interaction_locked_waiter_replacement_20261004.json')['status']=='passed',
             'adoption_evidence':'analysis/neural_interaction_locked_waiter_replacement_20261004.json',
             'seed_ensemble_adoption_evidence':'analysis/no_dropout_locked_waiter_replacement_20261004.json',
             'queued_effective_driver':'analysis/run_neural_interaction_locked_pipeline_20261004.py',
             'reason':'Actual integrity, recursive assembly, complete scheme CSV parity andseparate frozen wrapper controls passed. Verified idle53–56 waiters were replaced with versioned wrappers; actual production execution after their real selected predecessors is still pending. No hardware maximum orquality improvement inferred.'},
            {'method':'Matched no-dropout optimizer interactions','evidence':'analysis/neural_interaction_complete_output_search_plan_20261004.json',
             'actual_annual_fits_completed':state.get('neural_interaction_annual_artifacts_completed',0),
             'queued_official_rounds':[55,56],'expected_official_records':198,
             'reason':'Four previously uncovered original-seed dropout/learning-rate/epoch/weight-decay combinations pass all20 annual fits, all4 mature full-training future controls, complete scheme causal checks andgenerator controls. The198 actual official comparisons after R54/R55 remain pending.'}],
        'wider_neural_complete_training_pending_evidence':'analysis/neural_width_training_run_20261004.json',
        'mature_portfolio_loss_fine_tuning_pending_evidence':'analysis/portfolio_surrogate_search_execution_20261004.json',
        'portfolio_original_preflight_admission_guard_failure_evidence':'analysis/portfolio_surrogate_preflight_memory_gate_20261004.json',
        'portfolio_original_guard_failure_does_not_establish_physical_exhaustion':True,
        'chosen8GiB_reserve_is_scheduling_rule':True,'global_resource_exhaustion_established':False,
        'unlimited_model_space_exhaustion_not_inferred_from_finite_grids':True,'test_labels_read':False}
    portfolio=ROOT/'analysis/portfolio_surrogate_search_execution_20261004.json'
    measured=list((ROOT/'analysis').glob('neural_width_measured_prefix*/verification.json'))
    if measured:
        proof=max(measured,key=lambda p:read(p)['completed_models_inspected'])
        output['actual_wide_model_internal_andmeasured_prefix_cost_evidence']=str(proof.relative_to(ROOT))
        output['actual_wide_models_inspected']=read(proof)['completed_models_inspected']
        output['actual_past_normalizer_target_andraw_source_controls_passed']=read(proof)['status']=='passed'
        output['measured_timing_environment_not_matched_andno_optimal_width_inferred']=True
    frontier=ROOT/'analysis/neural_width_frontier_prepared_plan_20261004.json'
    if frontier.exists():
        output['serialized_width_frontier_prepared_plan']=str(frontier.relative_to(ROOT))
        output['serialized_width_frontier_evidence']='analysis/neural_width_frontier_20261004/verification.json'
        output['serialized_width_frontier_status']=state.get('neural_width_frontier_status','pending')
        output['serialized_width_frontier_scope_audit_status']=state.get('neural_width_frontier_scope_audit_status','pending_actual_controls')
        output['serialized_width_frontier_scope_audit_execution_record']='analysis/neural_width_frontier_audit_run_20261004.json'
        output['resource_guard_ortimeout_never_substitutes_for_actual_physical_exhaustion']=True
    worker_frontier=ROOT/'analysis/official_worker_frontier_prepared_plan_20261004.json'
    if worker_frontier.exists():
        output['serialized_official_worker_frontier_prepared_plan']=str(worker_frontier.relative_to(ROOT))
        output['serialized_official_worker_frontier_evidence']='analysis/official_worker_frontier_execution_20261004/verification.json'
        output['serialized_official_worker_frontier_status']=state.get('official_worker_frontier_status','pending')
        output['serialized_official_worker_frontier_actual_completed_control_jobs']=state.get('official_worker_frontier_actual_completed_control_jobs',0)
        output['serialized_official_worker_frontier_scope_audit_status']=state.get('official_worker_frontier_scope_audit_status','pending_actual_controls')
        output['official_worker_frontier_resource_controls_are_not_new_model_quality_records']=True
    if portfolio.exists() and not complete_round_evidence(60):
        output['open_feasible_directions'].append({'method':'Mature checkpoint fine tuning with rank, soft top-group return andholdings overlap losses',
            'evidence':str(portfolio.relative_to(ROOT)),
            'implementation_evidence':'analysis/portfolio_bank_implementation_preflight_20261004/verification.json',
            'frozen_complete_output_plan':'analysis/portfolio_surrogate_complete_output_search_plan_20261004.json',
            'queued_official_rounds':[59,60],'expected_official_records':198,
            'actual_annual_fine_tuning_fits_completed':state.get('portfolio_surrogate_annual_artifacts_completed',0),
            'reason':'Actual implicit-gradient, warm checkpoint, complete original-supervision hash, mature-label boundary andcold-prefix controls pass. Four configurations and20 fine-tuning annual fits are serialized after wide-model QA; future replay andcomplete official quality comparison remain required.'})
    nystrom=ROOT/'analysis/nystrom_ridge_complete_output_search_plan_20261004.json'
    if nystrom.exists() and not complete_round_evidence(62):
        output['open_feasible_directions'].append({'method':'Training-sampled Nyström RBF kernel basis plus raw63 one-day ridge',
            'evidence':str(nystrom.relative_to(ROOT)),
            'numerical_preflight':'analysis/nystrom_ridge_preflight_20261004/verification.json',
            'queue_adoption':'analysis/nystrom_ridge_queue_adoption_20261004.json',
            'queued_official_rounds':[61,62],'expected_official_records':198,
            'actual_annual_fits_completed':state.get('nystrom_ridge_annual_artifacts_completed',0),
            'reason':'Four configurations pass independent sklearn basis/solver, reload/prefix, actual past-data poisoning andseparate dispatch/generator controls. Twenty full annual fits, four mature full-training future controls andactual complete official output comparisons remain required; queued after prior scientific andresource audits.'})
    if (ROOT/'analysis/neural_width_complete_output_search_plan_20261004.json').exists() and not complete_round_evidence(58):
        output['open_feasible_directions'].append({'method':'Matched wider neural models withcomplete annual andfuture output checks',
            'evidence':'analysis/neural_width_complete_output_search_plan_20261004.json',
            'queued_official_rounds':[57,58],'expected_official_records':198,
            'actual_annual_fits_completed':state.get('neural_width_annual_artifacts_completed',0),
            'all_twenty_model_internal_inspection_evidence':'analysis/neural_width_complete_model_inspection_execution_20261004/verification.json',
            'reason':'Full annual training, mature full-training future checks andactual complete official role/standalone comparisons are required; completed partial annual fits do not establish all-fold orquality completion.'})
    requirements={
        'Complete official evaluation of all prepared models and output schemes':list(range(48,max([48,*state['queued_rounds']])+1)),
        'Jointly refine earlier and later selected augmentation layers':[50],
        'Complete matched Fourier feature-count, seed and penalty sensitivity':[47,48],
        'Alternative fixed additive basis layouts':[51,52],
        'Matched no-dropout neural seeds, epochs andequal-weight ensembles':[53,54],
        'Reduce repeated immutable provenance hashing with scoped read locks':list(range(50,63)),
        'Matched no-dropout optimizer interactions':[55,56],
        'Mature checkpoint fine tuning with rank, soft top-group return andholdings overlap losses':[59,60],
        'Training-sampled Nyström RBF kernel basis plus raw63 one-day ridge':[61,62],
        'Matched wider neural models withcomplete annual andfuture output checks':[57,58]}
    closed_scopes=[];current=[];evidence_cache={}
    for direction in output['open_feasible_directions']:
        required=requirements[direction['method']]
        for number in required:
            if number not in evidence_cache:evidence_cache[number]=complete_round_evidence(number)
        complete=[n for n in required if evidence_cache[n] is not None]
        remaining=[n for n in required if evidence_cache[n] is None]
        direction.update(required_official_rounds=required,actual_completed_official_rounds=complete,
            remaining_required_official_rounds=remaining,
            actual_complete_round_evidence=[evidence_cache[n] for n in complete])
        if remaining:
            direction['current_required_work']=f'Actual complete official output, candidate andexecution evidence remains required for rounds{remaining}.'
            current.append(direction)
        else:
            direction.update(status='completed_declared_scope_only',
                reason='All specified complete official output rounds, selected candidate coverage andrequired scoped executions have actual published evidence. This closes the declared comparisons only; broader variants andhardware maxima are not inferred.')
            closed_scopes.append(direction)
    output['open_feasible_directions']=current
    output['completed_declared_method_scopes']=closed_scopes
    output['actual_scientific_scope_completion_excludes_published_before_scoped_execution_closes']=True
    inspection=ROOT/'analysis/neural_width_complete_model_inspection_execution_20261004/verification.json'
    output['all_twenty_width_model_internal_inspection_status']=read(inspection)['status'] if inspection.exists() else 'queued_actual_twenty_fit_checks'
    output['actual_wide_fulltraining_artifacts_completed']=state.get('neural_width_fulltraining_artifacts_completed',0)
    output['actual_wide_native_future_controls_recorded']=state.get('neural_width_native_fullfuture_controls_recorded',0)
    output['wide_future_actual_owned_root_live']=state.get('neural_width_future_owned_root_live',False)
    output['wide_future_last_complete_resource_observation']=state.get('neural_width_future_last_sample')
    output['wide_future_admission_reserve_GiB']=12.
    output['wide_future_reserve_is_scheduling_rule_andnot_physical_exhaustion']=True
    target=ROOT/'analysis/optimization_boundary_evidence_20261004.json'
    target.write_text(json.dumps(output,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
    print(json.dumps({'status':output['status'],'latest_completed_round':latest,'active_round':state['round'],'completed_declared_searches':len(closed),'open_feasible_directions':len(output['open_feasible_directions'])}))


if __name__=='__main__':main()
