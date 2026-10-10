"""Compact actual score/qualification monitor for the recovered chronological pipeline."""
from pathlib import Path
import argparse,json,os,sys,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,owned
COMPARISONS={136:('CrossFamily94',94,5),137:('Huber52',52,14),138:('BF16reverse40',40,14),139:('HuberCrossFamily112',112,18),140:('SpectralGram52',52,18),141:('KrylovGram52',52,18),145:('CrossFamilyFine125',125,1),146:('HuberCrossFamilyFine125',125,2),147:('JointCrossHuberOrder185',185,1),148:('AdaptiveJointCrossHuber242',242,1),149:('PureRFFHuber128',128,1),150:('HuberSparse59',59,1),151:('RFFSparse59',59,1),152:('SparseAfter14829',29,2),153:('BF16Medium78',78,1),154:('BF16TwoSeed79',79,1),155:('BF16Seed10_80',80,1)}
def status(name):
    folder=A/'service_owned_workflows_20261006'/name
    if (folder/'service_execution.json').exists():return read(folder/'service_execution.json')
    if (folder/'native_launch.json').exists():
        launch=read(folder/'native_launch.json');return {'status':'running' if owned(launch) else 'ownership_not_yet_reconciled','worker':launch['owned_worker_pid']}
    return {'status':'not_started'}
def write(path,data):
    path=Path(path);temporary=path.with_name(path.name+f'.{os.getpid()}.tmp');temporary.write_text(data,encoding='utf8');os.replace(temporary,path)
def snapshot():
    import psutil
    qualified=[]
    for directory in A.glob('optimization_20261003_r*'):
        suffix=directory.name.removeprefix('optimization_20261003_r')
        if not suffix.isdecimal():continue
        number=int(suffix);full=directory/'full_registration_execution.json';receipt=A/f'github_validation_sync_main_20261005/round{number}_receipt.json'
        candidate=ROOT/f'candidates/optimization_20261003_r{number}'
        if not all(p.is_file() for p in (full,receipt,directory/'calibrated_csv_official.json',candidate/'verification.json')):continue
        if read(full)['status']!='passed' or read(receipt)['status']!='pushed_and_remote_head_verified' or read(candidate/'verification.json')['status']!='passed':continue
        metrics=read(directory/'calibrated_csv_official.json')['metrics'];models=read(candidate/'verification.json')['models']
        qualified.append({'round':number,'score':metrics['final_score'],'unique_models':len({row['sha256'] for row in models.values()}),'main_commit':read(receipt)['commit']})
    assert qualified
    best=min(qualified,key=lambda row:(-row['score'],row['unique_models'],row['round']))
    pipeline={}
    for number,(prefix,count,version) in COMPARISONS.items():
        date='20261009' if number>=151 else '20261008'
        folder=A/f'{prefix}_official_comparison_v1_{date}'
        row={'expected_cases':count,'quality':status(f'{prefix}_official_comparison_v{version}_{date}'),
            'controls_main':status(f'{prefix}_controls_main_publication_v{version}_{date}'),
            'scores_main':status(f'{prefix}_scores_main_publication_v{version}_{date}'),
            'selected_candidate':status(f'{prefix}_selected_candidate_preparation_v{version}_{date}'),
            'candidate_sealing':status(f'{prefix}_selected_candidate_sealing_v{version}_{date}'),
            'full_registration':status(f'{prefix}_round{number}_full_registration_v{6 if number==136 else version}_{date}')}
        if number==138:
            row.update(scores_main=status('exact138_connected_API_publication_reconciliation_v2_20261008'),selected_candidate=status('BF16reverse40_selected_candidate_preparation_v17_20261008'),candidate_sealing=status('BF16reverse40_selected_candidate_sealing_v17_20261008'),full_registration=status('BF16reverse40_round138_full_registration_v17_20261008'))
        if number==140:row['full_registration']=status('SpectralGram52_round140_full_registration_v19_20261008')
        if number==145:
            row['full_registration']=status('CrossFamilyFine125_round145_full_registration_v3_20261008')
        if number==146:
            row['selected_candidate']=status('HuberCrossFamilyFine125_selected_candidate_preparation_v4_20261008')
            row['candidate_sealing']=status('HuberCrossFamilyFine125_selected_candidate_sealing_v4_20261008')
            row['full_registration']=status('HuberCrossFamilyFine125_round146_full_registration_v4_20261008')
        if number==147:
            row['scores_main']=status('JointCrossHuberOrder185_scores_main_publication_v2_20261008')
            row['selected_candidate']=status('JointCrossHuberOrder185_selected_candidate_preparation_v2_20261009')
            row['candidate_sealing']=status('JointCrossHuberOrder185_selected_candidate_sealing_v2_20261009')
            row['full_registration']=status('JointCrossHuberOrder185_round147_full_registration_v2_20261009')
        if number==148:
            row['selected_candidate']=status('AdaptiveJointCrossHuber242_selected_candidate_preparation_v2_20261009')
            row['candidate_sealing']=status('AdaptiveJointCrossHuber242_selected_candidate_sealing_v2_20261009')
            row['full_registration']=status('AdaptiveJointCrossHuber242_round148_full_registration_v8_20261009')
            row['original_failed_entry_preserved']=status('AdaptiveJointCrossHuber242_selected_candidate_preparation_v1_20261008')
        if (folder/'verification.json').exists():
            proof=read(folder/'verification.json');row.update(completed_cases=len(proof['records']),scoring_winner={'case':proof['best']['case'],'score':proof['best']['connected_final_score'],'configuration':proof['best']['configuration']},scoring_winner_is_not_a_full_qualification=True)
        elif (folder/'actual_stage.json').exists():
            progress=read(folder/'actual_stage.json');row['actual_scoring_stage']=progress;row['completed_cases']=progress.get('actual_completed_cases',0)
        else:row['completed_cases']=0
        pipeline[str(number)]=row
    state={'status':'actual_chronological_optimization_active','at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),
        'deadline_local':'2026-10-10T23:59:00+08:00','best_fully_qualified':best,'pipeline':pipeline,
        'fresh18_three_round_full_prospective_controls':status('pending139to141_complete_prospective_controls_v18_20261008'),
        'fresh18_chronological_dispatch':status('pending139to141_chronological_dispatch_v18_20261008'),
        'available_memory_GiB':psutil.virtual_memory().available/2**30,
        'free_storage_GiB':{d:psutil.disk_usage(d+':/').free/2**30 for d in ('D','E')},
        'optimization_exhaustion_proven':False,'new_official_scores_by_observer':0,'test_labels_read':False}
    fine=Path('E:/赛题五_本机临时/CrossFamilyFine121_parent134_historical_v1_20261008')
    state['fine145_frontier']={'native30_controls':status('CrossFamilyFine30_actual_native_historical_controls_v1_20261008'),'full121_controls':status('CrossFamilyFine121_actual_full_historical_controls_v1_20261008'),'actual_full_control_records':len(list(fine.glob('case*.json'))),'expected_full_control_records_including_identity':121,'synthetic120_controls_completed':(fine/'synthetic120_controls.json').is_file(),'quality_case_count_planned':125,'quality_source_admission':status('CrossFamilyFine125_round145_source_admission_v1_20261008'),'quality_scoring':status('CrossFamilyFine125_official_comparison_v1_20261008'),'actual_official_score_records':pipeline['145']['completed_cases'],'new_native_fits':0,'complete_prospective_controls':status('CrossFamilyFine145_complete_prospective_controls_v1_20261008'),'chronological_dispatch':status('CrossFamilyFine145_complete_chronological_dispatch_v1_20261008'),'prospective_main_publication':status('actual145_complete_prospective_main_publication_v27_20261008')}
    state['actual138_fine145_controls_main_publication']=status('actual138_fine145_historical_controls_main_publication_v25_20261008')
    fine146=Path('E:/赛题五_本机临时/HuberCrossFamilyFine121_parent136_historical_v1_20261008')
    state['fine146_frontier']={'expected_quality_cases':125,'actual_native30':status('HuberCrossFamilyFine30_actual_native_historical_controls_v1_20261008'),'actual_full121':status('HuberCrossFamilyFine121_actual_full_historical_controls_v1_20261008'),'actual_full_control_records':len(list(fine146.glob('case*.json'))),'complete_quality_receivers_preflighted':status('HuberCrossFamilyFine146_complete_prospective_controls_v3_20261008'),'actual_new_official_scores':0,'new_future_inference':0,'historical_main_publication':status('actual_fine146_historical_controls_main_publication_v30_20261008')}
    state['fine146_frontier'].update(actual_new_official_scores=pipeline['146']['completed_cases'],quality_source_admission=status('HuberCrossFamilyFine125_round146_source_admission_v2_20261008'),chronological_dispatch=status('HuberCrossFamilyFine146_complete_chronological_dispatch_v6_20261008'),actual_calendar=status('HuberCrossFamilyFine30_multiyear_calendar_controls_v1_20261008'))
    state['fresh141_closure']=status('KrylovGram141_actual_preflight_metadata_closure_v20_20261008')
    state['fresh141_dispatch']=status('KrylovGram141_remaining_chronological_dispatch_v20_20261008')
    state['publisher_storage_relocation']=status('Git_publisher_exact_nine_index_refresh_verified_E_relocation_v10_20261008')
    state['expired_20261007_shutdown_schedule_not_restarted']=True
    state['isolated_serialization_benchmark']={'actual_service':status('actual_full_board_deferred_serialization_benchmark_v3_20261008'),'gate':'actual145_full_completion_then24GiB_available_RAM','original139_to145_runtime_retained':True,'full_measurement_not_yet_adopted':True,'preparation_main':status('actual_full_board_deferred_preparation_main_publication_v32_20261008')}
    joint=Path('E:/赛题五_本机临时/JointCrossHuber181_parent134_historical_v2_20261008')
    state['joint147_frontier']={'expected_quality_cases':185,'complete_quality_receivers_not_yet_admitted':status('JointCrossHuberOrder185_round147_source_admission_v1_20261008')['status']!='passed',
        'synthetic181':status('JointCrossHuber181_actual_synthetic_controls_v1_20261008'),
        'native80':status('JointCrossHuber80_native_historical_calendar_controls_v3_20261008'),
        'full181':status('JointCrossHuber181_actual_full_historical_controls_v2_20261008'),
        'actual_full_control_records':len(list(joint.glob('case*.json'))),'actual147_official_scores':pipeline['147']['completed_cases'],
        'existing35_evidence_is_rehash_not_new_native_replay':True,'actual_future_inference':0,'native_and_full_jobs_wait_for_actual146_full_completion':True,'core_candidate_sealer_full_and_scoring_prototypes_prepared':True,'complete_prospective_routes':status('JointCrossHuber147_complete_prospective_controls_v2_20261008'),'chronological_dispatch':status('JointCrossHuber147_complete_chronological_dispatch_v4_20261008'),'all_quality_receivers_preflighted':True}
    state['isolated_serialization_benchmark']['memory_wait_budget_seconds']=300
    state['isolated_serialization_benchmark']['original24GiB_start_threshold_preserved']=True
    adaptive=Path('E:/赛题五_本机临时/AdaptiveJointCrossHuber238_parent134_historical_v3_20261008')
    state['adaptive148_frontier']={'expected_quality_cases':242,'new_configuration_cases':238,
        'synthetic238':status('AdaptiveJointCrossHuber238_actual_synthetic_controls_v2_20261008'),
        'native80':status('AdaptiveJointCrossHuber80_native_historical_calendar_controls_v4_20261009'),
        'full238':status('AdaptiveJointCrossHuber238_actual_full_historical_controls_v4_20261009'),
        'native_and_full_wait_for_actual147_full':True,'actual_full_control_records':len(list(adaptive.glob('case*.json'))),
        'actual148_official_scores':pipeline['148']['completed_cases'],'complete_quality_receivers_preflighted':status('AdaptiveJointCrossHuber148_complete_prospective_controls_v2_20261008'),'chronological_dispatch':status('AdaptiveJointCrossHuber148_complete_chronological_dispatch_v6_20261009'),'new_model_fits':0,'actual_future_inference':0}
    state['pure149_frontier']={'expected_quality_cases':128,'synthetic124':status('PureRFFHuber124_actual_synthetic_controls_v2_20261008'),'actual_native80_and_full124_receivers_prepared':True,'native80':status('PureRFFHuber80_native_historical_calendar_controls_v6_20261009'),'full124':status('PureRFFHuber124_actual_full_historical_controls_v5_20261009'),'complete_quality_receivers_preflighted':status('PureRFFHuber149_complete_prospective_controls_v2_20261008'),'duplicate_audit':status('Pure149_prior_complete_forecast_duplicate_audit_v4_20261009'),'chronological_dispatch':status('PureRFFHuber149_complete_chronological_dispatch_publication_v15_20261009'),'actual_saved_state_count':25,'actual_official_scores':pipeline['149']['completed_cases'],'actual_future_inference':0,'reduced_required_heads_cross_huber_both':[2,3,5],'own25_saved_state_audit':status('PureRFFHuber25_existing_native_evidence_audit_v1_20261008')}
    state['actual_user_runtime_control']=read(A/'current_user_runtime_control_20261008.json')
    state['previous_user2355_stop_guardian']=read(Path(state['actual_user_runtime_control']['previous_stop_guard_status']))
    state['expired20261008_stop_guard_not_restarted']=True
    sparse150=Path('E:/赛题五_本机临时/HuberSparse55_parent134_historical_v1_20261008')
    state['huber_sparse150_frontier']={'expected_quality_cases':59,'existing_annual_states':20,
        'synthetic55_and_metadata20_passed':True,
        'native72':status('HuberSparse72_native_historical_calendar_controls_v1_20261008'),
        'full55':status('HuberSparse55_full_historical_controls_v1_20261008'),
        'actual_full_control_records':len(list(sparse150.glob('case*.json'))),
        'expected_full_control_records':55,'actual_official_scores':pipeline['150']['completed_cases'],'actual_future_inference':0,
        'complete_quality_receivers_not_yet_prepared':False,'duplicate_audit_still_required':status('HuberSparse150_prior_complete_forecast_duplicate_audit_v1_20261009')['status']!='passed',
        'complete_prospective_controls':status('HuberSparse150_complete_prospective_controls_v1_20261009'),
        'duplicate_audit':status('HuberSparse150_prior_complete_forecast_duplicate_audit_v1_20261009'),
        'chronological_dispatch':status('HuberSparse150_complete_chronological_dispatch_publication_v16_20261009'),
        'prospective_main_publication':status('HuberSparse150_prospective_main_publication_v2_20261009'),
        'historical_controls_do_not_use_futureX_or_labels':True,'full_control_start_memory_threshold_GiB':12,
        'new_native_fits':0,'new_unadopted_candidates_not_claimed_qualified':True}
    state['joint147_frontier']['original_failed_dispatcher_preserved']=state['joint147_frontier']['chronological_dispatch']
    state['joint147_frontier']['chronological_dispatch']={'status':'recovered_remaining_receivers_started',
        'scores_publication':pipeline['147']['scores_main'],'selected_candidate':pipeline['147']['selected_candidate'],
        'candidate_sealing':pipeline['147']['candidate_sealing'],'full_registration':pipeline['147']['full_registration']}
    state['joint147_frontier']['phase_collision_recovery']=str(A/'Joint147_publisher_phase_scratch_recovery_v7_20261008.json')
    state['pending148_149_phase_collision_prevented_before_quality']=True
    rff151=Path('E:/赛题五_本机临时/RFFSparse55_parent134_historical_v1_20261009')
    state['rff_sparse151_frontier']={'expected_quality_cases':59,'existing_saved_annual_states':20,
        'native72':status('RFFSparse72_native_historical_calendar_controls_v1_20261009'),
        'full55':status('RFFSparse55_full_historical_controls_v1_20261009'),
        'actual_full_control_records':len(list(rff151.glob('case*.json'))),
        'historical_main':status('RFFSparse151_historical_main_publication_v1_20261009'),
        'draft_bindings55_and_six_empty_E_outputs_passed':(A/'RFFSparse151_draft_control_bindings_v1_20261009.json').is_file(),
        'complete_quality_receivers_and_duplicate_audit_still_required':True,'inherited_full150_status_labels_require_normalization_before_admission':True,
        'actual151_official_scores':0,'actual151_future_inference':0,'new_native_fits':0,'actual150_full_required_before_quality':True}
    coverage=read(A/'sparse150151_all20_annual_native_coverage_v1_20261009.json')
    for row in coverage['records']:
        frontier=state['huber_sparse150_frontier' if row['round']==150 else 'rff_sparse151_frontier']
        frontier.update(actual_annual_native_states_replayed=row['actual_head_year_states'],actual_native_stage_cases=row['actual_native_cases'],actual_cold_native_cases=row['actual_cold_cases'],all5_model_years_replayed=True)
    state['rff_sparse151_frontier'].update(complete_quality_receivers_and_duplicate_audit_still_required=status('RFFSparse151_prior_complete_forecast_duplicate_audit_v1_20261009')['status']!='passed',
        inherited_full150_status_labels_require_normalization_before_admission=False,
        complete_prospective_controls=status('RFFSparse151_complete_prospective_controls_v1_20261009'),
        duplicate_audit=status('RFFSparse151_prior_complete_forecast_duplicate_audit_v1_20261009'),
        chronological_dispatch=status('RFFSparse151_complete_chronological_dispatch_publication_v16_20261009'),
        actual_project_import_sources=read(A/'RFFSparse151_project_source_closure_v1_20261009.json')['project_source_count'],
        actual151_official_scores=pipeline['151']['completed_cases'],source_admission=status('RFFSparse59_round151_source_admission_v1_20261009'))
    state['all5_annual150151_complete_prospective_main_publication']=status('sparse150151_full_prospective_main_publication_v50_20261009')
    state['adaptive148_frontier']['actual_future_inference']=int(pipeline['148']['selected_candidate']['status']=='passed')
    state['adaptive148_frontier']['actual_selected_two_full_native_replays_and_sealing_completed']=pipeline['148']['candidate_sealing']['status']=='passed'
    annual=A/'Pure149_all25_annual_native_coverage_v1_20261009.json'
    state['pure149_frontier'].update(additional2023_native=status('PureRFFHuber20_year2023_native_supplement_v2_20261009'),all5_annual_coverage=status('PureRFFHuber25_all5_annual_native_coverage_v2_20261009'))
    if annual.exists():
        actual=read(annual)
        state['pure149_frontier'].update(actual_all5_annual_states=actual['actual_head_year_states'],actual_native_controls=actual['actual_native_cases'],actual_cold_native_controls=actual['actual_cold_cases'])
    native152=Path('E:/赛题五_本机临时/SparseAfter14860_native_historical_calendar_v1_20261009')
    full152=Path('E:/赛题五_本机临时/SparseAfter14825_parent148_historical_v1_20261009')
    state['sparse_after148_152_frontier']={'stage_base_round':148,'expected_quality_cases':29,'actual_official_scores':0,
        'synthetic25_and75_prefixes_and10_saved_state_metadata_passed':True,
        'native60':status('SparseAfter14860_native_historical_calendar_controls_v2_20261009'),
        'actual_native_control_records':len(list(native152.glob('control*.json'))),'expected_native_controls':60,
        'full25':status('SparseAfter14825_full_historical_controls_v2_20261009'),
        'actual_full_control_records':len(list(full152.glob('case*.json'))),'expected_full_control_records':25,
        'actual_complete148_predictor_adapter_ABI_passed':(A/'SparseAfter148152_complete_native_predictor_preparation_v1_20261009.json').is_file(),
        'complete_quality_receivers_and_prior_duplicate_audit_still_required':True,
        'historical_main':status('actual149_all5_and152_historical_main_publication_v56_20261009'),
        'new_native_fits':0,'actual_future_X_read':False,'test_labels_read':False}
    frontier=state['sparse_after148_152_frontier']
    frontier.update(complete_quality_receivers_and_prior_duplicate_audit_still_required=status('SparseAfter148152_prior_complete_forecast_duplicate_audit_v1_20261009')['status']!='passed',
        complete_prospective_controls=status('SparseAfter148152_complete_prospective_controls_v1_20261009'),
        duplicate_audit=status('SparseAfter148152_prior_complete_forecast_duplicate_audit_v1_20261009'),
        chronological_dispatch=status('SparseAfter148152_complete_chronological_dispatch_publication_v16_20261009'),
        source_admission=status('SparseAfter14829_round152_source_admission_v1_20261009'),
        official_scoring=status('SparseAfter14829_official_comparison_v1_20261009'),
        prospective_source_routes=32,prospective_graph_controls=200,actual_future_X_read=False)
    q=A/'SparseAfter14829_official_comparison_v1_20261009'
    if (q/'verification.json').exists():frontier['actual_official_scores']=len(read(q/'verification.json')['records'])
    elif (q/'actual_stage.json').exists():frontier['actual_official_scores']=read(q/'actual_stage.json').get('actual_completed_cases',0)
    state['verified_publication_only_large_report_and_research_index_guards']=str(A/'lossless_chunked_safe_main_runtime_v1_20261009.json')
    bank=Path('E:/赛题五_本机临时/neural_BF16_medium2048_seed09_e64_bank6_v1_20261009')
    completed=[int(p.parent.name) for p in bank.glob('*/info.json') if p.parent.name.isdecimal()]
    stage=read(bank/'actual_stage.json') if (bank/'actual_stage.json').exists() else None
    state['neural_medium_new_recipe_frontier']={'configuration':read(A/'neural_BF16_medium2048_seed09_e64_frontier_v1_20261009.json')['configuration'],
      'actual_restart_control':status('actual_BF16_medium2048_seed09_restart_control_v1_20261009'),
      'actual_annual_training':status('actual_BF16_medium2048_seed09_e64_bank6_v1_20261009'),
      'completed_mature_annual_model_years':sorted(completed),'completed_annual_models':len(completed),'expected_annual_models':6,
      'actual_training_stage':stage,'restart_controls_main_publication':status('neural_medium_restart_main_publication_v58_20261009'),
      'actual_new_quality_scores':0,'actual_future_X_read':False,'fully_qualified_not_claimed':True}
    medium_full=Path('E:/赛题五_本机临时/BF16Medium153_full73_training_v1_20261009')
    medium_native=Path('E:/赛题五_本机临时/BF16Medium153_native42_calendar_v1_20261009')
    state['medium153_frontier']={'actual_stage_base_round':148,'quality_anchor_rounds':[148,149,150,151,152],
      'expected_quality_cases':78,'synthetic_cases':73,'synthetic_cold_cases':219,
      'actual_small_independent':status('BF16Medium153_independent_small_CPU_v1_20261009'),
      'actual_full5_independent':status('BF16Medium153_independent_full5_GPU_controls_v1_20261009'),
      'actual_full73':status('BF16Medium153_actual_full73_training_v1_20261009'),
      'actual_native42':status('BF16Medium153_actual_native42_calendar_v1_20261009'),
      'actual_full_case_records':len(list(medium_full.glob('case*.json'))),'actual_native_case_records':len(list(medium_native.glob('case*.json'))),
      'official_scores':0,'actual_future_X_read':False,'test_labels_read':False,
      'complete_quality_receivers_and_prospective_and_duplicate_checks_still_required':True}
    for number in (150,151):
        prefix='HuberSparse59' if number==150 else 'RFFSparse59';version=3
        row=pipeline[str(number)]
        for field,stem in (('quality','official_comparison'),('scores_main','scores_main_publication'),('selected_candidate','selected_candidate_preparation'),('candidate_sealing','selected_candidate_sealing'),('full_registration',f'round{number}_full_registration')):
            row[field]=status(f'{prefix}_{stem}_v{version}_20261009')
        row['controls_main']=status(f'{prefix}_controls_main_publication_v{2 if number==150 else 3}_20261009')
        row['failed_original_services_retained']=True
    state['huber_sparse150_frontier'].update(duplicate_audit=status('HuberSparse150_prior_complete_forecast_duplicate_audit_v1_20261009'),actual_official_scores=pipeline['150']['completed_cases'],serial_recovery=status('HuberSparse59_official_comparison_v3_20261009'))
    state['rff_sparse151_frontier'].update(duplicate_audit=status('RFFSparse151_prior_complete_forecast_duplicate_audit_v9_20261009'),chronological_dispatch=status('RFFSparse151_complete_chronological_dispatch_serial_v38_20261009'))
    state['sparse_after148_152_frontier'].update(duplicate_audit=status('SparseAfter148152_prior_complete_forecast_duplicate_audit_v10_20261009'),chronological_dispatch=status('SparseAfter148152_complete_chronological_dispatch_serial_v38_20261009'),source_admission=status('SparseAfter14829_round152_source_admission_v2_20261009'),official_scoring=status('SparseAfter14829_official_comparison_v2_20261009'))
    state['medium153_frontier'].update(complete_prospective=status('BF16Medium153_complete_prospective_controls_v1_20261009'),prospective_sources=40,prospective_graph_controls=1500,duplicate_audit=status('BF16Medium153_prior_complete_forecast_duplicate_audit_v10_20261009'),chronological_dispatch=status('BF16Medium153_complete_chronological_dispatch_actual_v42_20261009'),source_admission=status('BF16Medium78_round153_source_admission_v2_20261009'),official_scoring=status('BF16Medium78_official_comparison_v1_20261009'),historical_full_controls_main=status('medium153_fulltraining_main_publication_v63_20261009'))
    state['serial_publication_main_lock_actual_two_process_proof']=str(A/'serial_main_publication_mutex_v1_20261009.json')
    q=A/'BF16Medium78_official_comparison_v1_20261009'
    if (q/'verification.json').exists():state['medium153_frontier']['official_scores']=len(read(q/'verification.json')['records'])
    elif (q/'actual_stage.json').exists():state['medium153_frontier']['official_scores']=read(q/'actual_stage.json').get('actual_completed_cases',0)
    pipeline['150'].update(selected_candidate=status('HuberSparse59_selected_candidate_preparation_v4_20261009'),candidate_sealing=status('HuberSparse59_selected_candidate_sealing_v5_20261009'),full_registration=status('HuberSparse59_round150_full_registration_v11_20261009'))
    state['huber_sparse150_frontier']['chronological_dispatch']=pipeline['150']['full_registration']
    bank10=Path('E:/赛题五_本机临时/neural_BF16_medium2048_seed10_e64_bank6_v1_20261009')
    years10=sorted(int(p.parent.name) for p in bank10.glob('*/info.json') if p.parent.name.isdecimal())
    state['two_seed154_frontier']={'proposal':str(A/'BF16TwoSeed79_round154_proposal_v1_20261009.json'),'seed10_configuration':read(A/'neural_BF16_medium2048_seed10_e64_frontier_v1_20261009.json')['configuration'],'actual_restart_control':status('actual_BF16_medium2048_seed10_restart_control_v1_20261009'),'actual_annual_training':status('actual_BF16_medium2048_seed10_e64_bank6_v1_20261009'),'completed_mature_annual_model_years':years10,'completed_annual_models':len(years10),'expected_annual_models':6,'actual_stage':read(bank10/'actual_stage.json') if (bank10/'actual_stage.json').exists() else None,'expected_quality_cases':79,'official_scores':0,'future_X_read':False,'test_labels_read':False,'global_search_exhaustion_not_claimed':True}
    state['future_registry13_and_import24_controls']={'registry_paths':str(A/'external_registry_source_paths_runtime_v1_20261009.json'),'service_and_import_names':str(A/'future_import_namespaces_v31_20261009.json'),'historical_failures_preserved':True}
    state['safe_main_watcher']=status('main_publisher_v10_20261009')
    state['actual_original_user_index_restore']=str(A/'main_watcher_safe_handoff_and_index_restore_v34_20261009.json')
    state['actual150_and65_committed_blob_reconciliation']=status('HuberSparse59_round150_full_registration_v11_20261009')
    state['two_seed154_frontier'].update(actual_synthetic_cases=73,actual_synthetic_cold_cases=219,independent_small=status('BF16TwoSeed154_seed10_independent_small_CPU_v1_20261009'),independent_full5=status('BF16TwoSeed154_seed10_independent_full5_GPU_controls_v1_20261009'),equal_mean_full5=status('BF16TwoSeed154_equal_mean_full5_controls_v1_20261009'),full73=status('BF16TwoSeed154_actual_full73_training_v1_20261009'),current_evidence_main=status('two_seed154_guard_verified_controls_main_publication_v70_20261009'))
    full154=Path('E:/赛题五_本机临时/BF16TwoSeed154_full73_training_v1_20261009')
    state['two_seed154_frontier'].update(native42=status('BF16TwoSeed154_actual_native42_calendar_v1_20261009'),
        actual_full_control_records=len(list(full154.glob('case*.json'))),
        complete_prospective=status('BF16TwoSeed154_complete_prospective_controls_v1_20261009'),prospective_sources=48,prospective_graph_controls=1800,
        duplicate_audit=status('BF16TwoSeed154_prior_complete_forecast_duplicate_audit_v1_20261009'),
        chronological_dispatch=status('BF16TwoSeed154_complete_chronological_dispatch_v2_20261009'),
        source_admission=status('BF16TwoSeed79_round154_source_admission_v1_20261009'),
        official_scores=pipeline['154']['completed_cases'],full_registration=pipeline['154']['full_registration'])
    state['future_registry13_and_import24_controls']['service_and_import_names']=str(A/'future_import_namespaces_v38_20261009.json')
    state['two_seed154_frontier']['actual_comparison_parent_guard16_controls']=str(A/'BF16TwoSeed154_actual_parent_guard_controls_v2_20261009.json')
    state['actual_all_file_literal_namespace24_controls']=str(A/'future_all_file_literal_namespaces_v39_20261009.json')
    state['sparse_after148_152_frontier'].update(actual_future_X_read=pipeline['152']['selected_candidate']['status']=='passed',legacy55_service_name_is_only_alias_for_actual25=True,actual25_gate_bridge=str(A/'SparseAfter148152_legacy55_wait_gate_actual25_bridge_v40_20261009.json'))
    state['medium153_frontier']['actual_future_X_read']=pipeline['153']['selected_candidate']['status']=='passed'
    state['seed10_155_frontier']={'fixed_stage_base_round':148,'comparison_anchor_rounds':list(range(148,155)),'expected_quality_cases':80,'actual_reused_annual_models':6,'new_native_fits':0,
        'native42':status('BF16Seed10_155_actual_native42_calendar_v1_20261009'),'full73':status('BF16Seed10_155_actual_full73_training_v2_20261009'),
        'failed_original_full1_preserved':status('BF16Seed10_155_actual_full73_training_v1_20261009'),
        'complete_prospective':status('BF16Seed10_155_complete_prospective_controls_v1_20261009'),'prospective_sources':56,'prospective_graph_controls':2100,
        'duplicate_audit':status('BF16Seed10_155_prior_complete_forecast_duplicate_audit_v1_20261009'),
        'chronological_dispatch':status('BF16Seed10_155_complete_chronological_dispatch_v1_20261009'),
        'source_admission':status('BF16Seed10_80_round155_source_admission_v1_20261009'),
        'official_scores':pipeline['155']['completed_cases'],'actual_future_X_read':pipeline['155']['selected_candidate']['status']=='passed','test_labels_read':False}
    state['current_turn_evidence_main']=status('seed10_155_and_actual152_153_guard_main_publication_v74_20261009')
    state['tonight_stop_not_inferred_from_expired_yesterday_schedule']=True
    bank156=Path('E:/赛题五_本机临时/neural_BF16_medium2048_drop05_seed09_e64_bank6_v1_20261009')
    years156=sorted(int(p.parent.name) for p in bank156.glob('*/info.json') if p.parent.name.isdecimal())
    state['drop05_156_frontier']={'proposal':str(A/'BF16Drop05_81_round156_proposal_v1_20261009.json'),'expected_quality_cases':81,
        'only_training_change':'dropout0_to0.05','seed_unchanged':20261009,'epochs_unchanged':64,
        'restart_control':status('actual_BF16_medium2048_drop05_seed09_restart_control_v1_20261009'),
        'annual_training':status('actual_BF16_medium2048_drop05_seed09_e64_bank6_v1_20261009'),
        'mature_annual_years_completed':years156,'completed_own_fits':len(years156),'required_own_fits':6,
        'GPU_training_waits_complete155':True,'official_scores':0,'future_X_read':False,'test_labels_read':False}
    write(A/'optimization_live_progress_v64_20261009.json',json.dumps(state,ensure_ascii=False,indent=2)+'\n')
    text=f"# 赛题五实际优化进度\n\n更新时间：{state['at_local']}。截止：10月10日23:59。\n\n完全通过评分、候选检查、完整榜和 main 同步的最佳为第{best['round']}轮，S={best['score']:.12f}，{best['unique_models']}个物理模型。\n\n"
    text+='\n'.join(f"- 第{n}轮：官方评分{r['completed_cases']}/{r['expected_cases']}，评分任务{r['quality']['status']}，候选准备{r['selected_candidate']['status']}，完整验证{r['full_registration']['status']}。" for n,r in pipeline.items())
    text+=f"\n\n可用内存{state['available_memory_GiB']:.2f} GiB；D/E可用{state['free_storage_GiB']['D']:.2f}/{state['free_storage_GiB']['E']:.2f} GiB。试验最高分需完成全部候选检查才可采用。未证明可行优化方向或计算资源穷尽。\n"
    text+=f"\n细权重第145轮：原生30项控制{state['fine145_frontier']['native30_controls']['status']}，完整控制{state['fine145_frontier']['actual_full_control_records']}/121，125项官方评分准入{state['fine145_frontier']['quality_source_admission']['status']}，评分任务{state['fine145_frontier']['quality_scoring']['status']}。\n"
    text+=f"\n第146轮新方向：完整历史控制{state['fine146_frontier']['actual_full_control_records']}/121，原生复现{state['fine146_frontier']['actual_native30']['status']}；完整评分与候选接收流程已预检，实际官方评分见上表。\n"
    text+=f"\n完整榜重复编码隔离基准：{state['isolated_serialization_benchmark']['actual_service']['status']}，排在145轮完成之后；尚未采用新运行方式。\n"
    text+=f"\n第147轮联合两阶段与顺序：185项比较提案，合成181项/543截断{state['joint147_frontier']['synthetic181']['status']}；原生80项任务（等待146轮完整结束后执行）{state['joint147_frontier']['native80']['status']}，完整训练控制{state['joint147_frontier']['actual_full_control_records']}/181。实际官方评分见上表；预检查通过后还需等待原生和完整控制。\n"
    text+='\n第148轮扩展低比例联合方案：238项合成及714冷检查已通过，80原生和238完整历史控制排在147完成之后；242项正式评分接收流程已通过32条程序检查，等待原生及完整历史控制。\n'
    text+='\n第149轮少模型方向：两个RFF均值与Huber组合，124合成/372冷检查及零Ridge权重参考预测相等已通过；25个年度状态已完成子集核验；真实历史80项原生回放与124项完整控制已排队；128项评分、推理、完整榜接收流程已通过32程序与992图检查；既有预测去重及同预测分数交叉核验已排队，尚无质量分。\n'
    text+='\n2026-10-08 23:55已实际停工；2026-10-09收到用户“继续”后重新核对冻结记录并恢复。旧停工安排未重新启用。\n'
    text+=f"\n第150轮Huber与稀疏残差混合：复用20个年度状态，55合成/165截断已通过；72项真实原生、重载、解码与日历控制{state['huber_sparse150_frontier']['native72']['status']}，完整历史控制{state['huber_sparse150_frontier']['actual_full_control_records']}/55；59项正式评分接收流程32代码/440图检查已通过；历史预测去重{state['huber_sparse150_frontier']['duplicate_audit']['status']}，连续派发{state['huber_sparse150_frontier']['chronological_dispatch']['status']}，实际质量评分见上表。\n"
    text+=f"\n第151轮RFF与稀疏残差混合：55合成/165截断及20状态元数据已通过，原生72项{state['rff_sparse151_frontier']['native72']['status']}，完整55项{state['rff_sparse151_frontier']['full55']['status']}，历史证据main同步{state['rff_sparse151_frontier']['historical_main']['status']}；完整32代码/440图及五个年度全部20状态90原生/90冷检查已通过，已接入连续派发；去重{state['rff_sparse151_frontier']['duplicate_audit']['status']}，等待150轮完整合格后准入，实际评分见上表。\n"
    frontier=state['sparse_after148_152_frontier']
    text+=f"\n第152轮在完整148后叠加单独稀疏修正：25合成/75前缀及10年度状态元数据已通过；真实原生回放{frontier['actual_native_control_records']}/60（{frontier['native60']['status']}），完整历史控制{frontier['actual_full_control_records']}/25（{frontier['full25']['status']}）；完整148预测器接口检查已通过。仍需完整评分接收预检查及训练期官方29项评分，尚无质量分。\n"
    neural=state['neural_medium_new_recipe_frontier']
    text+=f"\n新中型神经网络：2048/1024/512、BF16、seed20261009、64轮固定训练；重启与权重/预测逐位核验{neural['actual_restart_control']['status']}，年度模型{neural['completed_annual_models']}/6，训练{neural['actual_annual_training']['status']}，尚无正式质量分。\n"
    medium=state['medium153_frontier']
    text+=f"\n第153轮：新中型神经网络叠加完整148方案，正负信号、3种群体、12种权重与零权重，共73个训练组合、5个父方案锚点；73合成/219前缀通过。完整历史控制{medium['actual_full_case_records']}/73，六状态原生控制{medium['actual_native_case_records']}/42。尚无正式质量分；完整接收流程、去重与前置轮次准入仍须完成。\n"
    text=f"# 赛题五实际优化进度\n\n更新时间：{state['at_local']}；截止：2026-10-10 23:59。\n\n完全验证最佳：第{best['round']}轮，S={best['score']:.12f}，{best['unique_models']}个物理模型。\n\n"
    text+='\n'.join(f"- 第{n}轮：评分{r['completed_cases']}/{r['expected_cases']}，候选准备{r['selected_candidate']['status']}，封存{r['candidate_sealing']['status']}，完整验证{r['full_registration']['status']}。" for n,r in pipeline.items() if int(n)>=148)
    seed=state['two_seed154_frontier'];text+=f"\n\n第154轮：两种子等权集成已完成73完整/219截断、12状态42原生/42冷、48流程/1800方案图检查，后续完整验证已排队；seed10恢复检查{seed['actual_restart_control']['status']}，年度拟合{seed['completed_annual_models']}/6，官方评分{seed['official_scores']}/79。\n"
    text+=f"\n第152轮已有60原生和25完整历史控制；第153轮已有42原生、73完整历史、40程序及1500图检查。后续轮次仍须按先后顺序完成正式评分、候选检查、完整榜与main同步。\n\n可用内存{state['available_memory_GiB']:.2f} GiB；D/E可用{state['free_storage_GiB']['D']:.2f}/{state['free_storage_GiB']['E']:.2f} GiB。未证明资源或优化方向穷尽。\n"
    text+=f"\n第155轮单独seed10：复用6个成熟年度模型；73完整/219截断和42原生已通过，56程序/2100图已通过。80项正式评分排在154轮完整通过之后。当前评分{pipeline['155']['completed_cases']}/80。\n"
    text+=f"\n第156轮 dropout 对照：固定seed09/64轮，dropout从0改为0.05。重启控制{state['drop05_156_frontier']['restart_control']['status']}，自有年度模型{len(years156)}/6；GPU训练排在155轮完整结束之后。81项评分尚未开始。\n"
    write(A/'optimization_live_progress_v64_20261009.md',text)
    return state
def main(once):
    while True:
        state=snapshot()
        if once:print(json.dumps({'at_local':state['at_local'],'best':state['best_fully_qualified'],'pipeline':{n:{'completed':r['completed_cases'],'quality':r['quality']['status'],'full':r['full_registration']['status']} for n,r in state['pipeline'].items()}},ensure_ascii=False),flush=True);return
        time.sleep(45)
if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--once',action='store_true');main(parser.parse_args().once)
