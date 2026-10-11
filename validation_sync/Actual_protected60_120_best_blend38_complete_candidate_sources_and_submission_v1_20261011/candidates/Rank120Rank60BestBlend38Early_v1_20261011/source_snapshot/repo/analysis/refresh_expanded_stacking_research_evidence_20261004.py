"""Inventory forecast schemes, real fits and reused coefficients separately."""
from pathlib import Path
import json
from datetime import datetime
ROOT=Path(__file__).resolve().parents[1]


def read(path):return json.loads(path.read_text(encoding='utf-8-sig'))
def write(path,value):path.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')


def main():
    bank=ROOT/'analysis/expanded_stacking_bank_20261004';protocol=read(bank/'protocol.json');configs=protocol['configurations']
    complete=(bank/'oof_audit.json').exists();now=datetime.now().isoformat(timespec='seconds');models=[];artifacts=0;actual=0;aliases=0
    for name,cfg in configs.items():
        details=[]
        for year in (2020,2021,2022,2023,2024):
            path=bank/name/f'info_{year}.json'
            if not path.exists():continue
            info=read(path);assert info['status']=='passed';new=info['new_model_fits'];artifacts+=1;actual+=new
            aliases+=int(year>2020 and info.get('paired_fit_reused_from') is not None)
            details.append({'year':year,'mature_training_rows':info['training_meta']['rows'],'fit_seconds':info['fit_seconds'],
                 'artifact_elapsed_seconds':info['elapsed_seconds'],'actual_new_fits':new,'source':str(path.resolve()),
                 'paired_fit_reused_from':info.get('paired_fit_reused_from'),'fixed_first_year':year==2020})
        model={'model':name,'kind':'past_oof_ridge','target':cfg['target'],'annual_artifacts':len(details),
               'new_annual_fits':sum(r['actual_new_fits'] for r in details),'fit_seconds_total':sum(r['fit_seconds'] for r in details),
               'annual_details':details,'all_five_annual_outputs_complete':len(details)==5,'first_fold_policy':cfg['first_fold_policy']}
        full=bank/name/'info_2025.json'
        if full.exists():
            info=read(full);model['fulltraining']={'status':info['status'],'mature_training_rows':info['training_meta']['rows'],
                 'fit_seconds':info['fit_seconds'],'elapsed_seconds':info['elapsed_seconds'],'actual_new_fits':info['new_model_fits'],
                 'source':str(full.resolve()),'test_prediction_not_generated_during_fit':info['fulltraining_only_test_prediction_not_generated']}
        models.append(model)
    assert not complete or (artifacts,actual,aliases)==(60,24,24)
    cost_path=ROOT/'analysis/optimization_fit_cost_evidence_20261004.json';cost=read(cost_path)
    cost['models']=[model for model in cost['models'] if model['model'] not in configs]+models
    additive=ROOT/'analysis/additive_ridge_bank_20261004'
    for native_bank,basis_columns in ((additive,252),(ROOT/'analysis/fourier_ridge_bank_20261004',191),(ROOT/'analysis/fourier_tuning_bank_20261004',None),(ROOT/'analysis/additive_basis_bank_20261004',None)):
        if not (native_bank/'protocol.json').exists():continue
        additive_configs=read(native_bank/'protocol.json')['configurations']
        cost['models']=[model for model in cost['models'] if model['model'] not in additive_configs]
        for name,cfg in additive_configs.items():
            details=[]
            for year in range(2020,2025):
                path=native_bank/name/f'info_{year}.json'
                if not path.exists():continue
                info=read(path);assert info['status']=='passed'
                details.append({'year':year,'mature_training_rows':info['training_meta']['rows'],
                    'fit_seconds':info['fit_seconds'],'artifact_elapsed_seconds':info['elapsed_seconds'],
                    'actual_new_fits':1,'source':str(path.resolve())})
            cost['models'].append({'model':name,'kind':cfg['kind'],'target':cfg['target'],
                'annual_artifacts':len(details),'new_annual_fits':len(details),
                'fit_seconds_total':sum(r['fit_seconds'] for r in details),'annual_details':details,
                'all_five_annual_outputs_complete':len(details)==5,'expanded_basis_columns':basis_columns if basis_columns is not None else (63*(1+len(cfg['hinge_knots'])) if cfg['kind']=='ridge_additive' else 63+cfg['random_components'])})
    for label in ('no_dropout_seed','no_dropout_ensemble','neural_interaction','neural_width','portfolio_surrogate','nystrom_ridge'):
        fresh_bank=ROOT/f'analysis/{label}_bank_20261004'
        if (fresh_bank/'protocol.json').exists():configs=read(fresh_bank/'protocol.json')['configurations']
        elif label in ('portfolio_surrogate','nystrom_ridge'):
            plan=ROOT/f'analysis/{label}_complete_output_search_plan_20261004.json'
            if not plan.exists():continue
            configs=read(plan)['model_configurations']
        else:continue
        cost['models']=[model for model in cost['models'] if model['model'] not in configs]
        for name,cfg in configs.items():
            details=[]
            for year in range(2020,2025):
                info_path=fresh_bank/name/f'info_{year}.json'
                if not info_path.exists():continue
                info=read(info_path);assert info['status']=='passed'
                details.append({'year':year,'mature_training_rows':info['training_meta']['rows'],
                    'fit_seconds':info.get('fit_seconds',0.),'artifact_elapsed_seconds':info['elapsed_seconds'],
                    'actual_new_fits':info.get('new_model_fits',1),'source':str(info_path.resolve())})
            cost['models'].append({'model':name,'kind':cfg['kind'],'target':cfg['target'],
                'annual_artifacts':len(details),'new_annual_fits':sum(r['actual_new_fits'] for r in details),
                'fit_seconds_total':sum(r['fit_seconds'] for r in details),'annual_details':details,
                'all_five_annual_outputs_complete':len(details)==5,'source_bank':str(fresh_bank.relative_to(ROOT)),
                'training_objective':cfg.get('training_objective','original supervised target'),
                'warm_pretraining_reused_not_counted_as_new':label=='portfolio_surrogate'})
    # Update cached child full fits without counting them as new annual OOF fits.
    nonlinear=ROOT/'analysis/nonlinear_stacking_bank_20261004'
    if (nonlinear/'protocol.json').exists():
        new_configs=read(nonlinear/'protocol.json')['configurations']
        cost['models']=[m for m in cost['models'] if m['model'] not in new_configs]
        for name,cfg in new_configs.items():
            details=[]
            for year in range(2020,2025):
                path=nonlinear/name/f'info_{year}.json'
                if not path.exists():continue
                info=read(path);assert info['status']=='passed'
                details.append({'year':year,'mature_training_rows':info['training_meta']['rows'],
                    'fit_seconds':info['fit_seconds'],'artifact_elapsed_seconds':info['elapsed_seconds'],
                    'actual_new_fits':info['new_model_fits'],'source':str(path.resolve()),
                    'paired_fit_reused_from':info.get('paired_fit_reused_from'),'fixed_first_year':year==2020})
            cost['models'].append({'model':name,'kind':'past_oof_ridge','target':cfg['target'],
                'annual_artifacts':len(details),'new_annual_fits':sum(r['actual_new_fits'] for r in details),
                'fit_seconds_total':sum(r['fit_seconds'] for r in details),'annual_details':details,
                'all_five_annual_outputs_complete':len(details)==5,'first_fold_policy':cfg['first_fold_policy'],'parent_count':67})
    for model in cost['models']:
        if not model['annual_details']:continue
        full=Path(model['annual_details'][0]['source']).with_name('info_2025.json')
        if not full.exists():continue
        info=read(full);model['fulltraining']={'status':info['status'],'mature_training_rows':info['training_meta']['rows'],
             'fit_seconds':info.get('fit_seconds',0.),'elapsed_seconds':info.get('elapsed_seconds',0.),'source':str(full.resolve()),
             'test_prediction_not_generated_during_fit':info.get('fulltraining_only_test_prediction_not_generated',False)}
    families={}
    for model in cost['models']:
        family=families.setdefault(model['kind'],{'configurations':0,'new_annual_fits':0,'fit_seconds_total':0.})
        family['configurations']+=1;family['new_annual_fits']+=model['new_annual_fits'];family['fit_seconds_total']+=model['fit_seconds_total']
    completed=[(int(p.stem.rsplit('_r',1)[1]),read(p)) for p in (ROOT/'results').glob('optimization_20261003_r*.json')]
    latest,last_result=max(completed,key=lambda r:r[0]);active=latest+1
    registry=read(ROOT/'analysis/ongoing_optimization_state.json')['active_run_registry']
    last_queued=max(r['round'] for r in read(ROOT/registry))
    cost.update({'generated_at_local':now,'configurations':len(cost['models']),'families':families,
        'native_child_annual_fits':sum(m['new_annual_fits'] for m in cost['models'] if m['kind'] not in ('past_oof_ridge','neural_ensemble')),
        'learned_meta_annual_fits':sum(m['new_annual_fits'] for m in cost['models'] if m['kind']=='past_oof_ridge'),
        'total_actual_new_annual_fits':sum(m['new_annual_fits'] for m in cost['models']),
        'expanded_stacking_completed_annual_artifacts':artifacts,'expanded_stacking_distinct_annual_fits':actual,
        'expanded_stacking_paired_later_fold_reuses':aliases,'expanded_stacking_all_annual_controls_complete':complete,
        'fixed_first_fold_meta_fallbacks':sum(r['year']==2020 and r['actual_new_fits']==0 for m in cost['models'] if m['kind']=='past_oof_ridge' for r in m['annual_details']),
        'fully_completed_five_year_configurations':sum(m['annual_artifacts']==5 for m in cost['models']),
        'fulltraining_artifacts_ready':sum('fulltraining' in m for m in cost['models']),
        'native_backbone_configurations_fully_trained':sum(m['annual_artifacts']==5 and m['kind'] not in ('past_oof_ridge','neural_ensemble') for m in cost['models']),
        'active_validation_round':active,'queued_rounds':list(range(active+1,last_queued+1)),
        'active_run_registry':registry,
        'expanded_full_fit_inference_resource_scope':'analysis/expanded_future_resource_observations_20261004/protocol.json',
        'global_resource_exhaustion_established':False,
        'additive_ridge_annual_fits_completed':len(list(additive.glob('*/info_202[0-4].json'))),
        'additive_basis_annual_fits_completed':len(list((ROOT/'analysis/additive_basis_bank_20261004').glob('*/info_202[0-4].json'))),
        'fourier_ridge_annual_fits_completed':len(list((ROOT/'analysis/fourier_ridge_bank_20261004').glob('*/info_202[0-4].json'))),
        'fourier_tuning_annual_fits_completed':len(list((ROOT/'analysis/fourier_tuning_bank_20261004').glob('*/info_202[0-4].json')))})
    resource_audit=ROOT/'analysis/nonlinear_ridge_resource_scope_audit_20261004.json'
    if resource_audit.exists():
        assert read(resource_audit)['status']=='passed'
        cost['nonlinear_ridge_resource_scope_audit']=str(resource_audit.relative_to(ROOT))
        cost['fourier_sampling_does_not_establish_four_worker_training_capacity']=True
    write(cost_path,cost)
    directions_path=ROOT/'analysis/next_experiment_directions_20261003.json';directions=read(directions_path)
    if not any(r.get('priority')==19 for r in directions['directions']):
        directions['directions'].append({'priority':19,'method':'Matched fixed additive hinge-layout sensitivity',
            'reason':'Original252-column family uses only knots[-1,0,1]. Compare fixed narrow[-.5,0,.5] andwide5[-2,-1,0,1,2] using the same two one-day targets, three penalties, mature samples andfull continuous output score.',
            'configurations':12,'expected_annual_fits':60,'expanded_columns':{'narrow':252,'wide5':378},
            'preflight':'analysis/additive_basis_preflight_20261004/verification.json',
            'bank_protocol':'analysis/additive_basis_bank_20261004/protocol.json',
            'resource_observations':'analysis/additive_basis_resource_observations_20261004/protocol.json',
            'quality_status':'pending_actual_complete_output_comparison','test_labels_read':False})
    native_no_dropout=ROOT/'analysis/no_dropout_seed_bank_20261004'
    virtual_no_dropout=ROOT/'analysis/no_dropout_ensemble_bank_20261004'
    if (native_no_dropout/'protocol.json').exists() and not any(r.get('priority')==20 for r in directions['directions']):
        directions['directions'].append({'priority':20,'method':'Matched no-dropout seed/epoch models andequal-weight ensembles',
            'reason':'Actual selectedR31 uses2.5% rank512_drop000_e32. Earlier neural seed ensembles retain dropout0.05; compare three new no-dropout seeds, matched seed18 epoch32/64 andfour fixed raw/rank equal-weight ensembles.',
            'new_native_configs':4,'new_virtual_configs':4,'expected_new_annual_fits':20,
            'expected_annual_forecast_artifacts':40,'proposed_official_rounds':[53,54],
            'expected_official_records':{'53':148,'54':178},
            'native_protocol':str((native_no_dropout/'protocol.json').relative_to(ROOT)),
            'ensemble_protocol':str((virtual_no_dropout/'protocol.json').relative_to(ROOT)),
            'quality_status':'pending_actual_complete_output_comparison','test_labels_read':False})
    if not any(r.get('priority')==21 for r in directions['directions']):
        directions['directions'].append({'priority':21,'method':'Scoped immutable-input read locks andSHA reuse',
            'reason':'Actual recursive ensemble assembly repeats hashes of identical frozen inputs; reduce provenance overhead while preserving full hash checks anddenying writes for the cache lifetime.',
            'preflight':'analysis/locked_read_hash_cache_preflight_20261004/verification.json',
            'actual_recursive_control':'analysis/locked_ensemble_provenance_preflight_20261004/verification.json',
            'actual_model_reuse_control':'analysis/locked_no_dropout_model_reuse_preflight_20261004/verification.json',
            'new_quality_scores':0,'adopted_in_live_queued_rounds':False})
    if not any(r.get('priority')==22 for r in directions['directions']):
        directions['directions'].append({'priority':22,'method':'Matched no-dropout learning-rate, epoch andweight-decay interactions',
            'reason':'R31 selected a no-dropout signal andR35 a lower-learning-rate signal. Four original-seed combinations are absent from all existing configurations after target-offset normalization.',
            'configurations':4,'expected_annual_fits':20,
            'bank_protocol':'analysis/neural_interaction_bank_20261004/protocol.json',
            'preflight':'analysis/neural_interaction_preflight_20261004/verification.json',
            'execution_evidence':'analysis/neural_interaction_search_execution_20261004.json'})
    if not any(r.get('priority')==23 for r in directions['directions']):
        directions['directions'].append({'priority':23,'method':'Matched wider no-dropout neural models',
            'reason':'Actual fixed-batch width controls through16384 completed; full-fold feasibility andquality remain unmeasured. Compare1024/2048/4096/8192 against the reused512-width selected control with all optimizer settings fixed.',
            'configurations':4,'expected_annual_fits':20,'proposed_official_rounds':[57,58],
            'bank_protocol':'analysis/neural_width_bank_20261004/protocol.json',
            'preflight':'analysis/neural_width_preflight_20261004/verification.json',
            'resource_control_evidence':'analysis/neural_width_capacity_20261004/verification.json',
            'training_execution_evidence':'analysis/neural_width_training_run_20261004.json',
            'new_quality_scores':0,'test_labels_read':False})
    if not any(r.get('priority')==24 for r in directions['directions']):
        directions['directions'].append({'priority':24,'method':'Mature checkpoint fine tuning onrank, soft top-group return andholdings overlap losses',
            'reason':'Existing neural banks optimize supervised pointwise targets. Compare rank/return loss against rank/return/overlap loss, two fixed smoothing temperatures and4/8 epochs using corresponding frozen past512-width checkpoints.',
            'configurations':4,'expected_new_annual_fits':20,'warm_pretraining_reused_not_counted_as_new':True,
            'implementation_preflight':'analysis/portfolio_bank_implementation_preflight_20261004/verification.json',
            'training_loss_preflight':'analysis/portfolio_surrogate_preflight_v2_20261004/verification.json',
            'frozen_search_plan':'analysis/portfolio_surrogate_complete_output_search_plan_20261004.json',
            'execution_evidence':'analysis/portfolio_surrogate_search_execution_20261004.json',
            'queued_rounds':[59,60],'expected_official_records':{'59':100,'60':98},
            'surrogate_losses_not_official_quality_scores':True,'test_labels_read':False})
    frontier=ROOT/'analysis/neural_width_frontier_prepared_plan_20261004.json'
    if frontier.exists() and not any(r.get('priority')==25 for r in directions['directions']):
        directions['directions'].append({'priority':25,'method':'Serialized bounded neural fixed-batch allocation frontier',
            'reason':'All earlier512–16384 single-step controls succeeded. Repeat16384 andtest32768/65536 only after all actualR60 scientific work andscoped execution finish, using protected host reserve andowned child controls.',
            'frozen_plan':str(frontier.relative_to(ROOT)),'execution_record':'analysis/neural_width_frontier_run_20261004.json',
            'actual_quality_model_fits':0,'new_quality_scores':0,'test_labels_read':False,
            'does_not_claim_global_model_space_exhaustion':True})
    worker_frontier=ROOT/'analysis/official_worker_frontier_prepared_plan_20261004.json'
    if worker_frontier.exists() and not any(r.get('priority')==26 for r in directions['directions']):
        directions['directions'].append({'priority':26,'method':'Serialized unchanged official scorer at8/10/12/16 workers inforward andreverse order',
            'reason':'Existing actual capacity controls cover atmost8 workers. Run identical frozen training CSV scoring jobs after all scientific work andGPU diagnostics; distinguish completed, guarded andunattempted counts.',
            'frozen_plan':str(worker_frontier.relative_to(ROOT)),
            'execution_record':'analysis/official_worker_frontier_run_20261004.json',
            'scope_audit':'analysis/official_worker_frontier_scope_audit_20261004.json',
            'actual_quality_model_fits':0,'new_quality_scores':0,'test_labels_read':False,
            'not_a_randomized_isolated_throughput_benchmark':True})
    nystrom=ROOT/'analysis/nystrom_ridge_complete_output_search_plan_20261004.json'
    if nystrom.exists() and not any(r.get('priority')==27 for r in directions['directions']):
        directions['directions'].append({'priority':27,'method':'Past-fold sampled Nyström RBF landmarks plus raw63 ridge',
            'reason':'Existing kernel models use fixed data-independent Fourier features. Test64/128 landmarks sampled only from each mature past training fold, with the same one-day rank/return targets, fixed kernel mass128 andlambda.1.',
            'frozen_plan':str(nystrom.relative_to(ROOT)),
            'numerical_preflight':'analysis/nystrom_ridge_preflight_20261004/verification.json',
            'generator_preflight':'analysis/nystrom_ridge_search_generator_preflight_20261004/verification.json',
            'dispatch_preflight':'analysis/nystrom_ridge_frozen_provenance_preflight_20261004/verification.json',
            'queue_adoption':'analysis/nystrom_ridge_queue_adoption_20261004.json',
            'complete_scheme_source_correction':'analysis/nystrom_ridge_complete_scheme_source_correction_audit_20261004.json',
            'queued_rounds':[61,62],'expected_official_records':{'61':100,'62':98},
            'new_quality_scores':0,'test_labels_read':False})
    directions['directions']=[r for r in directions['directions'] if r.get('priority')!=12]+[{
        'priority':12,'method':'55-parent mature past-OOF ridge with paired first-year cold-start policies',
        'reason':'The original45-parent learned bank excludes the newly trained neural/CatBoost variants and fixes2020 to a raw-feature ridge. Test expanded55-member inputs and a prespecified equal-weight first-year rank ensemble under the same complete five-year score.',
        'scheme_configurations':12,'distinct_target_penalty_fits_per_later_year':6,'parents':55,
        'annual_forecast_artifacts':artifacts,'distinct_new_annual_fits':actual,'paired_later_fold_reuses':aliases,
        'first_year_policies':['frozen matching raw63 one-day ridge','fixed equal-weight55-child daily-rank mean'],
        'first_year_uniform_meta_weights_not_fitted':True,'later_raw_predictions_identical_within_each_policy_pair':True,
        'full_postprocessing_may_propagate_different_first_year_states_across_year_boundaries':True,
        'status':'All60 forecast artifacts,24 learned fits, five55-child actual replays and36 role/12 standalone preflights passed',
        'queued_rounds':[39,40],'expected_official_records':{'39':176,'40':258},
        'preflight':'analysis/expanded_stacking_preflight_20261004/verification.json',
        'oof_audit':'analysis/expanded_stacking_bank_20261004/oof_audit.json',
        'resource_scope':'analysis/expanded_future_resource_observations_20261004/protocol.json',
        'future_qa_status':read(ROOT/'analysis/expanded_stacking_future_pipelines_qa_20261004/verification.json')['status'] if (ROOT/'analysis/expanded_stacking_future_pipelines_qa_20261004/verification.json').exists() else 'pending',
        'test_labels_read':False}]
    for direction in directions['directions']:
        if direction['priority']==27:
            fresh=ROOT/'analysis/nystrom_ridge_bank_20261004';audit=fresh/'oof_audit.json'
            future=ROOT/'analysis/nystrom_ridge_future_models_qa_20261004/verification.json'
            complete=ROOT/'analysis/nystrom_ridge_complete_scheme_preflight_20261004/verification.json'
            direction.update(completed_actual_annual_fits=len(list(fresh.glob('*/info_202[0-4].json'))),
                annual_training_status=read(audit)['status'] if audit.exists() else 'queued_after_actual_scientific_GPU_andCPU_scope_audits',
                actual_fulltraining_artifacts=len(list(fresh.glob('*/info_2025.json'))),
                future_model_preflight_status=read(future)['status'] if future.exists() else 'pending_actual_annual_fits',
                complete_scheme_preflight_status=read(complete)['status'] if complete.exists() else 'pending_actual_annual_andfuture_controls',
                minimum_available_host_GiB_before_fit_policy=14.,
                actual_generator_preflight_status=read(ROOT/'analysis/nystrom_ridge_search_generator_preflight_20261004/verification.json')['status'],
                resource_sampler='analysis/nystrom_ridge_resource_observations_20261004/protocol.json',
                original_registry_preserved=True,production_completed_rounds=[n for n in (61,62) if (ROOT/f'results/optimization_20261003_r{n}.json').exists()])
        if direction['priority']==26:
            proof=ROOT/'analysis/official_worker_frontier_execution_20261004/verification.json'
            audit=ROOT/'analysis/official_worker_frontier_scope_audit_20261004.json'
            direction.update(execution_status=read(proof)['status'] if proof.exists() else ('controls_started' if (proof.parent/'frozen_before_controls.json').exists() else 'queued_after_scientific_andGPU_completion'),
                actual_completed_control_jobs=sum(read(p).get('jobs_completed',0) for label in ('forward','reverse') for p in (ROOT/f'analysis/official_worker_frontier_{label}_qa_20261004').glob('workers*_result.json')),
                scope_audit_status=read(audit)['status'] if audit.exists() else 'pending_actual_controls',
                evidence=str(proof.relative_to(ROOT)),physical_maximum_not_inferred_from_guard_ortimeout=True)
        if direction['priority']==25:
            proof=ROOT/'analysis/neural_width_frontier_20261004/verification.json'
            audit=ROOT/'analysis/neural_width_frontier_scope_audit_20261004.json'
            direction.update(execution_status=read(proof)['status'] if proof.exists() else 'queued_after_actual_scientific_completion',
                actual_step_results_completed=len(list((ROOT/'analysis/neural_width_frontier_20261004').glob('width*_result.json'))),
                scope_audit_status=read(audit)['status'] if audit.exists() else 'pending_actual_GPU_andCPU_controls',
                scope_audit=str(audit.relative_to(ROOT)),scope_audit_execution_record='analysis/neural_width_frontier_audit_run_20261004.json',
                evidence=str(proof.relative_to(ROOT)),physical_maximum_not_inferred_from_guard_ortimeout=True)
        if direction['priority']==24:
            fresh=ROOT/'analysis/portfolio_surrogate_bank_20261004';audit=fresh/'oof_audit.json'
            future=ROOT/'analysis/portfolio_surrogate_future_models_qa_20261004/verification.json'
            complete=ROOT/'analysis/portfolio_surrogate_complete_scheme_preflight_20261004/verification.json'
            execution=read(ROOT/'analysis/portfolio_surrogate_search_execution_20261004.json')
            direction.update(completed_actual_annual_fits=len(list(fresh.glob('*/info_202[0-4].json'))),
                annual_training_status=read(audit)['status'] if audit.exists() else execution['annual_training_status'],
                execution_status='queued_with_serialized_training_andcomplete_QA_gates',
                queued_rounds=[r['round'] for r in read(ROOT/registry) if r['round'] in (59,60)],
                minimum_available_host_GiB_before_fit_policy=14.,
                resource_sampler='analysis/portfolio_surrogate_resource_observations_20261004/protocol.json',
                resource_scope_audit='analysis/portfolio_surrogate_resource_scope_audit_20261004.json',
                future_resource_scope_audit='analysis/portfolio_surrogate_future_resource_scope_audit_20261004.json',
                implementation_preflight_status=read(ROOT/'analysis/portfolio_bank_implementation_preflight_20261004/verification.json')['status'],
                actual_generator_preflight_status=read(ROOT/'analysis/portfolio_surrogate_search_generator_preflight_20261004/verification.json')['status'],
                complete_scheme_qa_status=read(complete)['status'] if complete.exists() else 'pending',
                future_model_qa_status=read(future)['status'] if future.exists() else 'pending')
        if direction['priority']==8:
            direction['queued_rounds']=[31,32]
        if direction['priority']==23:
            fresh=ROOT/'analysis/neural_width_bank_20261004';audit=fresh/'oof_audit.json'
            future=ROOT/'analysis/neural_width_future_models_qa_20261004/verification.json'
            complete=ROOT/'analysis/neural_width_complete_scheme_preflight_20261004/verification.json'
            queued=[r['round'] for r in read(ROOT/registry) if r['round'] in (57,58)]
            direction.update(completed_actual_annual_fits=len(list(fresh.glob('*/info_202[0-4].json'))),
                annual_training_status=read(audit)['status'] if audit.exists() else 'running',
                execution_status='queued_with_actual_predecessor_and_annual_training_and_QA_gates' if queued else 'annual_training_and_complete_scheme_preparation',
                queued_rounds=queued,expected_official_records={'57':100,'58':98},
                official_rounds_not_yet_queued=not bool(queued),
                resource_sampler='analysis/neural_width_resource_observations_20261004/protocol.json',
                resource_control_scope_audit='analysis/neural_width_capacity_scope_audit_20261004.json',
                actual_generator_preflight_status=read(ROOT/'analysis/neural_width_search_generator_preflight_20261004/verification.json')['status'],
                complete_scheme_qa_status=read(complete)['status'] if complete.exists() else 'waiting_for_completed_future_models',
                future_model_qa_status=read(future)['status'] if future.exists() else 'waiting_for_completed_annual_models')
        if direction['priority']==3:
            if latest>=26:
                result26=read(ROOT/'results/optimization_20261003_r26.json')
                direction.update(execution_status='completed',completed_round=26,
                    validation_gain=result26['score_gain'],
                    status='R26 completed:267 official continuous-OOF records; selected candidate and causal/ranking checks passed')
            elif active==26:
                state=read(ROOT/'analysis/ongoing_optimization_r26_state.json')
                direction.update(execution_status='validation_running',
                    status=f"R26 active stage:{state['stage']}; candidate scoring andcompletion tracked separately")
        if direction['priority']==5 and latest>=25:
            r25=read(ROOT/'results/optimization_20261003_r25.json')
            direction.update(execution_status='completed',completed_round=25,validation_gain=r25['score_gain'],
                status='R25 completed:452 official continuous-OOF records; selected candidate and causal/ranking checks passed')
        if direction['priority']==13:
            direction.update(completed_actual_annual_fits=cost['additive_ridge_annual_fits_completed'],
                annual_training_status='running' if not (additive/'oof_audit.json').exists() else 'passed')
        if direction['priority']==14:
            direction.update(completed_actual_annual_fits=cost['fourier_ridge_annual_fits_completed'],
                annual_training_status='running' if not (ROOT/'analysis/fourier_ridge_bank_20261004/oof_audit.json').exists() else 'passed')
        if direction['priority'] in (13,14):
            label='additive' if direction['priority']==13 else 'fourier'
            proof=ROOT/f'analysis/{label}_ridge_future_pipelines_qa_20261004/verification.json'
            if proof.exists():
                assert read(proof)['status']=='passed'
                direction.update(future_qa_status='passed',execution_status='queued_for_validation',
                    future_qa=str(proof.relative_to(ROOT)),resource_scope_audit=str(resource_audit.relative_to(ROOT)))
        if direction['priority']==15:
            rows=[m for m in cost['models'] if m.get('parent_count')==67]
            direction.update(completed_annual_forecast_artifacts=sum(m['annual_artifacts'] for m in rows),
                completed_actual_annual_fits=sum(m['new_annual_fits'] for m in rows),
                annual_training_status='passed' if (nonlinear/'oof_audit.json').exists() else 'running')
        if direction['priority']==16:
            bank=ROOT/'analysis/fourier_tuning_bank_20261004'
            training_status='passed' if (bank/'oof_audit.json').exists() else ('running' if (bank/'protocol.json').exists() else 'waiting_for_prior_future_checks')
            future=ROOT/'analysis/fourier_tuning_future_pipelines_qa_20261004/verification.json'
            future_status=read(future)['status'] if future.exists() else 'pending'
            direction.update(completed_actual_annual_fits=cost['fourier_tuning_annual_fits_completed'],
                annual_training_status=training_status,future_qa_status=future_status,
                resource_scope_audit='analysis/fourier_tuning_resource_scope_audit_20261004.json',
                execution_status='queued_for_validation' if future_status=='passed' else ('implementation_checks_running' if training_status=='passed' else training_status),
                status=f"Actual annual fits:{cost['fourier_tuning_annual_fits_completed']}/50; OOF audit:{training_status}; future implementation controls:{future_status}")
        if direction['priority']==18:
            proofs={label:ROOT/f'analysis/{folder}/verification.json' for label,folder in
                (('kernel','role_layer_replay_preflight_20261004'),
                 ('future','role_layer_future_replay_qa_20261004'),
                 ('graph_compiler','selected_scheme_graph_preflight_v2_20261004'),
                 ('validation_runtime','whole_scheme_runtime_preflight_20261004'),
                 ('future_runtime','whole_scheme_future_runtime_qa_20261004'),
                 ('official_scoring','whole_scheme_score_preflight_20261004'),
                 ('parameter_arms','whole_scheme_round50_proposal_preflight_20261004'),
                 ('complete_release','whole_scheme_round50_release_preflight_20261004'))}
            statuses={label:read(path)['status'] if path.exists() else 'pending' for label,path in proofs.items()}
            direction.update(implementation_control_statuses=statuses,
                execution_status='recipe_graph_prepared_awaiting_selected_rounds' if all(v=='passed' for v in statuses.values()) else 'implementation_checks_running',
                graph_compiler='analysis/selected_scheme_graph_20261004.py',
                actual_selected_graph_assembler='analysis/assemble_selected_scheme_graph_20261004.py',
                graph_preflight='analysis/selected_scheme_graph_preflight_v2_20261004/verification.json',
                future_preflight='analysis/role_layer_future_replay_qa_20261004/verification.json',
                queued_rounds=[50],joint_optimizer='analysis/optimize_training_round50.py',
                complete_validation_runtime='analysis/whole_scheme_replay_runtime_20261004.py',
                complete_future_runtime='analysis/whole_scheme_future_runtime_20261004.py',
                checker_correction_evidence='analysis/selected_scheme_graph_preflight_recovery_20261004.json',
                status='Whole validation andfuture runtimes reproduce actual complete historical schemes andchanged earlier weights; R50 actual release, calibration andfuture helper controls tracked separately. Joint official quality comparison awaits actual selected R30–49 graph.')
        if direction['priority']==19:
            audit=ROOT/'analysis/additive_basis_bank_20261004/oof_audit.json'
            future=ROOT/'analysis/additive_basis_future_models_qa_20261004/verification.json'
            complete=ROOT/'analysis/additive_basis_complete_scheme_preflight_20261004/verification.json'
            direction.update(completed_actual_annual_fits=cost['additive_basis_annual_fits_completed'],
                annual_training_status=read(audit)['status'] if audit.exists() else 'running',
                numerical_preflight_status=read(ROOT/'analysis/additive_basis_preflight_20261004/verification.json')['status'],
                native_future_model_qa_status=read(future)['status'] if future.exists() else 'pending',
                complete_scheme_preflight_status=read(complete)['status'] if complete.exists() else 'pending',
                actual_generator_preflight_status=read(ROOT/'analysis/additive_basis_search_generator_preflight_20261004/verification.json')['status'],
                queued_rounds=[51,52],expected_official_records={'51':196,'52':258},
                execution_evidence='analysis/additive_basis_search_execution_20261004.json',
                resource_scope_audit='analysis/additive_basis_resource_scope_audit_20261004.json',
                fulltraining_future_resource_scope_audit='analysis/additive_basis_future_resource_scope_audit_20261004.json',
                execution_status='queued_for_official_full_output_validation' if complete.exists() else ('awaiting_actual_future_andofficial_output_checks' if audit.exists() else 'annual_training_running'))
        if direction['priority']==7:direction['queued_rounds']=[30]
        if direction['priority']==20:
            native_audit=native_no_dropout/'oof_audit.json';virtual_audit=virtual_no_dropout/'oof_audit.json'
            future=ROOT/'analysis/no_dropout_seed_future_models_qa_20261004/verification.json'
            complete=ROOT/'analysis/no_dropout_seed_complete_scheme_preflight_20261004/verification.json'
            actual_queued=[r['round'] for r in read(ROOT/registry) if r['round'] in (53,54)]
            direction.update(completed_actual_annual_fits=len(list(native_no_dropout.glob('*/info_202[0-4].json'))),
                completed_virtual_annual_artifacts=len(list(virtual_no_dropout.glob('*/info_202[0-4].json'))),
                annual_training_status=read(native_audit)['status'] if native_audit.exists() else 'running',
                virtual_assembly_status=read(virtual_audit)['status'] if virtual_audit.exists() else 'waiting_for_actual_native_OOF',
                execution_status='queued_with_actual_predecessor_and_implementation_gates' if actual_queued else ('future_and_complete_scheme_checks_running' if virtual_audit.exists() else 'model_assembly_running'),
                resource_sampler='analysis/no_dropout_seed_resource_observations_20261004/protocol.json',
                resource_scope_audit='analysis/no_dropout_seed_resource_scope_audit_20261004.json',
                future_model_qa_status=read(future)['status'] if future.exists() else 'pending',
                complete_scheme_qa_status=read(complete)['status'] if complete.exists() else 'pending',
                actual_generator_preflight_status=read(ROOT/'analysis/no_dropout_seed_search_generator_preflight_20261004/verification.json')['status'],
                queued_rounds=actual_queued,expected_official_records={'53':148,'54':178},
                execution_evidence='analysis/no_dropout_seed_search_execution_20261004.json',
                official_rounds_not_yet_queued=not bool(actual_queued))
        if direction['priority']==21:
            recursive=ROOT/'analysis/locked_ensemble_provenance_preflight_20261004/verification.json'
            reuse=ROOT/'analysis/locked_no_dropout_model_reuse_preflight_20261004/verification.json'
            direction.update(recursive_control_status=read(recursive)['status'] if recursive.exists() else 'pending',
                actual_model_reuse_status=read(reuse)['status'] if reuse.exists() else 'pending',
                execution_status='isolated_integrity_andartifact_reuse_controls',
                official_quality_comparison_not_claimed=True)
            whole=ROOT/'analysis/locked_no_dropout_complete_scheme_preflight_20261004/verification.json'
            direction['actual_complete_scheme_reuse_status']=read(whole)['status'] if whole.exists() else 'pending'
            direction['actual_complete_scheme_reuse_evidence']=str(whole.relative_to(ROOT))
            wrapper=ROOT/'analysis/frozen_provenance_execution_preflight_20261004/verification.json'
            direction['effective_execution_wrapper_status']=read(wrapper)['status'] if wrapper.exists() else 'pending'
            direction['effective_execution_wrapper_evidence']=str(wrapper.relative_to(ROOT))
            adoption=ROOT/'analysis/neural_interaction_locked_waiter_replacement_20261004.json'
            adopted=adoption.exists() and read(adoption)['status']=='passed'
            direction['adopted_in_live_queued_rounds']=adopted
            seed_adoption=ROOT/'analysis/no_dropout_locked_waiter_replacement_20261004.json'
            seed_adopted=seed_adoption.exists() and read(seed_adoption)['status']=='passed'
            direction['execution_status']='frozen_wrappers_queued_for_actual_rounds53_56' if adopted and seed_adopted else ('frozen_wrapper_queued_for_actual_rounds55_56' if adopted else 'isolated_integrity_andartifact_reuse_controls')
            direction['adoption_evidence']=str(adoption.relative_to(ROOT))
            direction['queued_effective_driver']='analysis/run_neural_interaction_locked_pipeline_20261004.py' if adopted else None
            direction['seed_ensemble_adoption_evidence']=str(seed_adoption.relative_to(ROOT))
            direction['seed_ensemble_wrapper_status']=read(ROOT/'analysis/no_dropout_frozen_provenance_execution_preflight_20261004/verification.json')['status'] if seed_adopted else 'pending'
            direction['queued_effective_rounds']=[n for n in (53,54,55,56) if n in ([53,54] if seed_adopted else [])+([55,56] if adopted else [])]
            direction['production_execution_completed_rounds']=[n for n in (53,54,55,56) if (ROOT/f'analysis/optimization_20261003_r{n}/provenance_scope_execution.json').exists() and read(ROOT/f'analysis/optimization_20261003_r{n}/provenance_scope_execution.json')['status']=='passed']
            family_adoption=ROOT/'analysis/new_neural_families_locked_waiter_replacement_20261004.json'
            if family_adoption.exists() and read(family_adoption)['status']=='passed':
                direction['additional_neural_family_wrapper_evidence']=str(family_adoption.relative_to(ROOT))
                direction['additional_neural_family_wrapper_rounds']=[57,58,59,60]
                direction['execution_status']='frozen_wrappers_queued_for_actual_rounds53_60'
                direction['additional_production_execution_completed_rounds']=[n for n in (57,58,59,60) if (ROOT/f'analysis/optimization_20261003_r{n}/provenance_scope_execution.json').exists() and read(ROOT/f'analysis/optimization_20261003_r{n}/provenance_scope_execution.json')['status']=='passed']
            joint_adoption=ROOT/'analysis/joint_and_basis_locked_waiter_replacement_20261004.json'
            if joint_adoption.exists() and read(joint_adoption)['status']=='passed':
                direction['joint_and_basis_wrapper_evidence']=str(joint_adoption.relative_to(ROOT))
                direction['joint_and_basis_wrapper_rounds']=[50,51,52]
                direction['execution_status']='frozen_wrappers_queued_for_actual_rounds50_60'
                direction['joint_and_basis_production_execution_completed_rounds']=[n for n in (50,51,52) if (ROOT/f'analysis/optimization_20261003_r{n}/provenance_scope_execution.json').exists() and read(ROOT/f'analysis/optimization_20261003_r{n}/provenance_scope_execution.json')['status']=='passed']
            direction['complete_scheme_timing_is_not_matched_speedup_evidence']=True
            if recursive.exists():
                value=read(recursive)
                direction.update(actual_baseline_three_checks_seconds=value['baseline_complete_seconds'],
                    actual_cached_three_checks_seconds_including_setup_andexit=value['cached_complete_seconds'],
                    actual_unique_immutable_inputs=value['unique_immutable_inputs'],
                    actual_hash_calls_per_arm=value['actual_hash_calls_per_arm'],
                    background_andfilesystem_cache_not_matched=True)
        if direction['priority']==22:
            bank=ROOT/'analysis/neural_interaction_bank_20261004';audit=bank/'oof_audit.json'
            future=ROOT/'analysis/neural_interaction_future_models_qa_20261004/verification.json'
            complete=ROOT/'analysis/neural_interaction_complete_scheme_preflight_20261004/verification.json'
            direction.update(completed_actual_annual_fits=len(list(bank.glob('*/info_202[0-4].json'))),
                annual_training_status=read(audit)['status'] if audit.exists() else 'running',
                future_model_qa_status=read(future)['status'] if future.exists() else 'pending',
                complete_scheme_qa_status=read(complete)['status'] if complete.exists() else 'pending',
                queued_rounds=[r['round'] for r in read(ROOT/registry) if r['round'] in (55,56)],
                expected_official_records={'55':100,'56':98},
                actual_generator_preflight_status=read(ROOT/'analysis/neural_interaction_search_generator_preflight_20261004/verification.json')['status'],
                execution_status='queued_with_actual_predecessor_annual_training_andimplementation_gates',
                resource_sampler='analysis/neural_interaction_resource_observations_20261004/protocol.json')
            direction['resource_scope_audit']='analysis/neural_interaction_resource_scope_audit_20261004.json'
            direction['fulltraining_future_resource_scope_audit']='analysis/neural_interaction_future_resource_scope_audit_20261004.json'
        declared=direction.get('queued_rounds',[])
        completed=[n for n in declared if (ROOT/f'results/optimization_20261003_r{n}.json').exists()]
        if declared:
            direction['completed_official_rounds']=completed
            direction['pending_official_rounds']=[n for n in declared if n not in completed]
            publications=[read(ROOT/f'results/optimization_20261003_r{n}.json') for n in completed]
            assert all(r['status']=='complete' for r in publications)
            direction['completed_official_records']=sum(stage['scored_records'] for r in publications for stage in r['sequential_stage_results'])
        if declared and len(completed)==len(declared):
            publications=[read(ROOT/f'results/optimization_20261003_r{n}.json') for n in completed]
            assert all(r['status']=='complete' for r in publications)
            records=sum(stage['scored_records'] for r in publications for stage in r['sequential_stage_results'])
            direction.update(execution_status='completed',completed_round=max(completed),
                completed_official_records=records,
                validation_gain=sum(r['score_gain'] for r in publications),
                status=f"Rounds{completed} completed:{records} continuous official records; selected complete candidates andcausal/ranking QA passed. Only the declared search scopes are closed.")
        elif active in declared:direction['execution_status']='official_validation_running'
    directions.update({'updated_at_local':now,'last_completed_round':latest,'validation_best_completed':last_result['winner']['connected_final_score'],
        'active_run_registry':registry,'active_validation_round':active,
        'new_annual_oof_fits_completed':cost['total_actual_new_annual_fits'],'native_child_annual_oof_fits_completed':cost['native_child_annual_fits'],
        'new_meta_annual_oof_fits_completed':cost['learned_meta_annual_fits'],'total_new_individual_and_virtual_configurations':cost['configurations'],
        'fully_completed_five_year_configurations':cost['fully_completed_five_year_configurations'],
        'new_backbone_configurations_fully_trained':cost['native_backbone_configurations_fully_trained'],
        'new_backbone_configurations_trained':cost['native_backbone_configurations_fully_trained'],
        'global_resource_exhaustion_established':False})
    measured=list((ROOT/'analysis').glob('neural_width_measured_prefix*/verification.json'))
    if measured:
        proof=max(measured,key=lambda p:read(p)['completed_models_inspected'])
        directions['actual_neural_width_internal_andmeasured_cost_prefix_evidence']=str(proof.relative_to(ROOT))
        directions['actual_neural_width_completed_models_inspected']=read(proof)['completed_models_inspected']
    if resource_audit.exists():directions['nonlinear_ridge_resource_scope_audit']=str(resource_audit.relative_to(ROOT))
    directions['prospective_parallel_official_scoring_four']['additional_prospective_rounds']=list(range(35,last_queued+1))
    write(directions_path,directions)
    print(json.dumps({'annual_artifacts':artifacts,'distinct_expanded_annual_fits':actual,'paired_reuses':aliases,
                      'total_actual_new_annual_fits':cost['total_actual_new_annual_fits'],'five_year_output_configurations':cost['fully_completed_five_year_configurations']}))


if __name__=='__main__':main()
