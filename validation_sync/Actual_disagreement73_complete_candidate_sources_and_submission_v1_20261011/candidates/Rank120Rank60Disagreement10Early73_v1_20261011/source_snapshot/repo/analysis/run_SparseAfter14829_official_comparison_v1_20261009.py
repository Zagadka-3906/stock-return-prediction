"""Score90 declared cross-family transformations, three anchors and one identity with unchanged official math."""
from pathlib import Path
from types import SimpleNamespace
import gc,hashlib,os,sys,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A),str(A/'connected_validation_20261002')]
for key in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','POLARS_MAX_THREADS'):os.environ[key]='2'
from run_dependency_queue_v3_20261006 import read,sha,create,owned
OUT=A/'SparseAfter14829_official_comparison_v1_20261009'
STATUS='passed_actual29_SparseAfter148_complete_parent_full_official_comparisons'


def closed(name):
    folder=A/'service_owned_workflows_20261006'/name
    while not (folder/'native_launch.json').exists() or owned(read(folder/'native_launch.json')):time.sleep(10)
    assert read(folder/'service_execution.json')['status']=='passed',name


def best_key(row):
    return (-row['connected_final_score'],row['expected_unique_native_models'],abs(row['configuration']['weight']),row['case'])


def main():
    closed('RFFSparse59_round151_full_registration_v1_20261009')
    closed('SparseAfter148152_prior_complete_forecast_duplicate_audit_v1_20261009')
    closed('SparseAfter14829_round152_source_admission_v1_20261009')
    closed('SparseAfter14829_controls_main_publication_v1_20261009')
    import numpy as np,polars as pl,psutil
    import SparseAfter148_complete_parent_CDF_v1_20261009 as codec
    from SparseAfter148152_storage_v1_20261009 import empty,installed_transfer,write_progress
    from score_calibrated_candidates_20261003 import score
    from official_date_index_dataframe_adapter_20261007 import installed
    from all_forecast_percentile_runtime_20261007 import installed as installed_percentile
    from cached_official_spearman_runtime_20261007 import installed as installed_ic
    from win32_read_handle_hash_cache_with_filename_v2_20261006 import LockedReadHashCache
    duplicate_path=A/'SparseAfter148152_prior_complete_forecast_duplicate_audit_raw_v1_20261009.json';duplicate=read(duplicate_path)
    assert duplicate['actual_current_cases']==25 and duplicate['known_zero_control_count']==1
    duplicate_rows={r['control_case']:r for r in duplicate['records']}
    empty(OUT)
    plan_path=A/'SparseAfter14829_round152_plan_v1_20261009.json';plan=read(plan_path)
    control_path=Path(read(A/'actual_SparseAfter14825_parent148_location_v1_20261009.json')['output'])/'verification.json';control=read(control_path)
    assert control['status']=='passed_actual25_SparseAfter148_full_training_CDF_and75_cold_controls_with_exact148_identity' and control['actual_stage_base_round']==148
    controlled={(r['configuration']['group'],r['configuration']['share'],r['configuration']['amplitude']):r for r in control['records']}
    assert len(controlled)==25
    parents={n:A/f'optimization_20261003_r{n}' for n in [148,*plan['anchor_rounds']]}
    baselines={n:read(path/'calibrated_csv_official.json')['metrics'] for n,path in parents.items()}
    predictions={n:read(ROOT/f'candidates/optimization_20261003_r{n}/verification.json') for n in parents}
    comparison_parent=min(plan['anchor_rounds'],key=lambda n:(-baselines[n]['final_score'],len({r['sha256'] for r in predictions[n]['models'].values()}),n))
    parent=148
    assert parent==control['actual_stage_base_round']==plan['fixed_scientific_stage_base_round']
    graph=predictions[parent]['whole_scheme_graph'];assert 'nonflag_CPU_ReverseBayes64_residual_CDF' in graph
    assert 'nonflag_CPU_SparseAfter148_complete_parent_CDF' not in graph
    model_sha={c['sha256'] for c in predictions[parent]['models'].values()}
    final_infos={h:read(row['infos']['2025']) for h,row in plan['heads'].items()}
    cases=[{'anchor_round':n,'model':None,'group':None,'share':None,'role':None,'weight':0.,'universe':None} for n in plan['anchor_rounds']]
    cases += [{'anchor_round':parent,'model':f'SparseAfter148_group{case["group"]}_share{case["share"]}',
        'group':case['group'],'share':case['share'],'role':'nonflag_valid_2021_onward','weight':case['amplitude'],'universe':'all_current_raw_forecasts'} for case in plan['new_cases']]
    cases += [{'anchor_round':parent,'model':'zero_SparseAfter148_residual_identity','group':None,'share':None,'role':'nonflag_valid_2021_onward','weight':0.,'universe':'all_current_raw_forecasts'}]
    assert len(cases)==plan['expected_scored_cases']==29
    frame_path=A/'connected_validation_20261002/combined_fold_frame.parquet';scoring_source=A/'optimization_20261003_r95/scoring_validation_only'
    sources=[Path(__file__),duplicate_path,A/'SparseAfter148152_complete_receiver_refinement_v3_20261009.json',Path(codec.__file__),A/'SparseAfter148152_storage_v1_20261009.py',plan_path,control_path,frame_path,
        A/'SparseAfter14829_round152_source_admission_v1_20261009.json',A/'SparseAfter14829_controls_github_v1_20261009/receipt.json',
        A/'score_calibrated_candidates_20261003.py',A/'official_date_index_dataframe_adapter_20261007.py',A/'all_forecast_percentile_runtime_20261007.py',
        A/'cached_official_spearman_runtime_20261007.py',A/'exact_cached_official_spearman_v2_20261007.py',A/'exact_cached_validation_spearman_20261007.py',ROOT/'evaluate.py',ROOT/'后续选模标准.md',
        *[scoring_source/name for name in ('测试集_X.csv','测试集_Y.csv')],*[Path(row['oof']) for row in plan['heads'].values()],
        *[Path(row['infos']['2025']) for row in plan['heads'].values()]]
    for n,path in parents.items():
        assert read(path/'full_registration_execution.json')['status']=='passed'
        sources += [path/name for name in ('selection.json','protocol.json','selected_validation.npy','calibrated_csv_official.json','full_registration_execution.json')]
        sources += [ROOT/f'candidates/optimization_20261003_r{n}'/name for name in ('verification.json','manifest.json')]
        sources += [A/f'github_validation_sync_main_20261005/round{n}_receipt.json']
    pins={**read(A/'SparseAfter14829_round152_source_admission_v1_20261009.json')['input_sha256'],**control['input_sha256'],**{str(path):sha(path) for path in sources}}
    create(OUT/'frozen_before_actual_full_controls_and_official_scores.json',{'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),
        'input_sha256':pins,'cases':cases,'actual_comparison_parent_round':comparison_parent,'actual_scheme_base_round':parent,'baseline_metrics':baselines,
        'whole_complete_parent_all_original_branches_retained':True,'new_stage_first2020_identity':True,'existing_saved_native_heads':10,
        'new_native_fits_by_comparison':0,'selection_bias_uncorrected':True,'no_extra_Top_worst_year_or_significance_gate':True,'test_labels_read':False})
    while psutil.virtual_memory().available<8.5*2**30:time.sleep(10)
    records=[];rank_cache={};residual=None;last_pair=None
    with LockedReadHashCache(pins) as scope,installed_transfer():
        frame=pl.read_parquet(frame_path,columns=['ts_code','trade_date','flag_limit_up','price_valid','y_ret_1d'])
        dates,flags,valid=[frame[name].to_numpy() for name in ('trade_date','flag_limit_up','price_valid')]
        assert (len(frame),frame['trade_date'].n_unique(),frame['ts_code'].n_unique())==(5635800,1212,4650)
        base=np.load(parents[parent]/'selected_validation.npy',mmap_mode='r');prepared=codec.prepare(base,dates)
        arrays={h:np.load(row['oof'],mmap_mode='r') for h,row in plan['heads'].items()}
        scoring=A/'SparseAfter148152_D_scoring_v1_20261009/comparison/scoring_validation_only';scoring.mkdir(parents=True)
        for filename in ('测试集_X.csv','测试集_Y.csv'):os.link(scoring_source/filename,scoring/filename)
        ctx=SimpleNamespace(frame=frame,dates=dates,scoring=scoring)
        for index,cfg in enumerate(cases):
            components=[]
            if cfg['model'] is None:
                values=np.asarray(np.load(parents[cfg['anchor_round']]/'selected_validation.npy',mmap_mode='r'))
                expected_models=len(predictions[cfg['anchor_round']]['models'])
            else:
                if cfg['weight']==0.:
                    values=codec.apply_prepared(base,np.zeros(len(base)),dates,flags,valid,0.,prepared)
                else:
                    pair=(cfg['group'],cfg['share'])
                    if pair!=last_pair:residual=codec.mixture(arrays,*pair);last_pair=pair
                    values=codec.apply_prepared(base,residual,dates,flags,valid,cfg['weight'],prepared)
                    components=list(dict.fromkeys(h for names,sign in codec.GROUPS[cfg['group']] for h in names))
                key=(cfg['group'],cfg['share'],cfg['weight']) if cfg['weight'] else (0,.5,0.)
                measured=controlled[key];control_case=measured['case']
                numeric=hashlib.sha256(memoryview(np.ascontiguousarray(values)).cast('B')).hexdigest()
                assert numeric==measured['numeric_sha256']==duplicate_rows[control_case]['numeric_sha256']
                mask=codec.selected(dates,flags,valid)
                assert np.array_equal(values[~mask].view('u8'),np.asarray(base)[~mask].view('u8'))
                for count in (80,260,975):
                    n=count*4650
                    cold_residual=codec.mixture({h:array[:n] for h,array in arrays.items()},cfg['group'],cfg['share']) if cfg['weight'] else np.zeros(n)
                    cold=codec.transform(base[:n],cold_residual,dates[:n],flags[:n],valid[:n],cfg['weight'])
                    assert np.array_equal(values[:n].view('u8'),cold.view('u8'))
                expected_models=len(model_sha|{final_infos[h]['native_model_sha256'] for h in components})
            write_progress(OUT/'actual_stage.json',{'status':'actual_full_official_scoring','at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),
                'case':index,'configuration':cfg,'actual_completed_cases':len(records),'expected_cases':29})
            with installed_percentile() as percentile_runtime,installed_ic(rank_cache) as ic_runtime:
                with installed(scoring/'submission.csv') as date_index:metrics=score(ctx,values)
            if cfg['model'] is None:assert metrics==baselines[cfg['anchor_round']]
            if cfg['weight']==0. and cfg['model'] is not None:
                assert metrics==baselines[parent] and np.array_equal(values.view('u8'),np.asarray(base).view('u8'))
            if cfg['model'] is not None:
                for previous in duplicate_rows[control_case]['prior_full_board_matches']:
                    assert all(metrics[k]==value for k,value in previous['metrics'].items())
                    if previous['all8_metrics'] is not None:assert metrics==previous['all8_metrics']
            capsule=Path(ctx.last_official_score_cache['official_metrics_source'])
            item={'case':index,'configuration':cfg,'metrics':metrics,'connected_final_score':metrics['final_score'],
                'expected_unique_native_models':expected_models,'score_gain_over_qualified_parent':metrics['final_score']-baselines[comparison_parent]['final_score'],
                'actual_comparison_parent_round':comparison_parent,'actual_scheme_base_round':parent,
                'prediction_numeric_bytes_sha256':hashlib.sha256(memoryview(np.ascontiguousarray(values)).cast('B')).hexdigest(),
                'actual_declared55_numeric_control_exact':cfg['model'] is not None,'actual_prior_complete_forecast_duplicate_metric_guards':cfg['model'] is not None,
                'official_date_index_runtime':dict(date_index),'all_row_percentile_runtime':percentile_runtime,'scoring_only_spearman_runtime':ic_runtime,
                'official_score_cache':ctx.last_official_score_cache,'official_metric_capsule_sha256':sha(capsule),'actual_return_mapping':ctx.last_candidate_return_mapping,
                'whole_complete_parent_branches_preserved_before_new_stage':True,'invalid_and_declared_unselected_raw_bits_preserved':cfg['model'] is not None,
                'actual_cold80_260_975_bits_exact':cfg['model'] is not None,'qualified_anchor_all8_metrics_exact':cfg['model'] is None,
                'native_bank_source':str(A/'SparseAfter14829_actual_controls_index_v1_20261009.json'),'ordered_native_components':components,
                'first2020_identity':True,'candidate_future_freeze_replays_QA63_and_main_pending':True,'test_labels_read':False}
            create(OUT/f'case{index:02d}_official.json',item);records.append(item)
            print({'case':index,'score':metrics['final_score'],'gain':item['score_gain_over_qualified_parent']},flush=True)
            del values;gc.collect()
        scope.reverify()
    best=min(records,key=best_key)
    create(OUT/'verification.json',{'status':STATUS,'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'input_sha256':pins,
        'records':records,'best':best,'components':{'group4':[list(names) for names,sign in codec.GROUPS[4]]},
        'actual_comparison_parent_round':comparison_parent,'actual_scheme_base_round':parent,'existing_saved_native_heads':10,
        'new_native_fits_by_comparison':0,'new_quality_score_records':29,'all55_nonanchors_full_and165_cold_controls_passed':True,
        'future_candidate_and_full152_qualification_pending':True,'global_feasible_direction_or_resource_exhaustion_not_established':True,'test_labels_read':False})


if __name__=='__main__':main()
