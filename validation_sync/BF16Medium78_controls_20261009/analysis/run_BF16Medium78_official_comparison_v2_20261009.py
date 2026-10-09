"""Score the fixed40 complete-parent neural rank-CDF schemes on continuous own-mature OOF."""
from pathlib import Path
from types import SimpleNamespace
import gc, hashlib, os, sys, time
ROOT=Path(__file__).resolve().parents[1]; A=ROOT/'analysis'
sys.path[:0]=[str(ROOT),str(A),str(A/'connected_validation_20261002')]
for key in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','POLARS_MAX_THREADS'):os.environ[key]='2'
from run_dependency_queue_v3_20261006 import read,sha,create,owned
OUT=A/'BF16Medium78_official_comparison_v1_20261009'
STATUS='passed_actual78_BF16_medium2048_seed09_complete_parent_rank_CDF_full_official_comparisons'


def closed(name):
    folder=A/'service_owned_workflows_20261006'/name
    while not (folder/'native_launch.json').exists() or owned(read(folder/'native_launch.json')):time.sleep(15)
    assert read(folder/'service_execution.json')['status']=='passed',name


def main():
    closed('BF16Medium78_round153_source_admission_v1_20261009')
    closed('BF16Medium78_controls_main_publication_v1_20261009')
    import numpy as np
    import polars as pl
    import psutil
    import BF16Medium153_complete_parent_rank_CDF_v1_20261009 as codec
    from BF16Medium153_storage_v1_20261009 import empty,installed_transfer,write_progress as write
    from score_calibrated_candidates_20261003 import score
    from official_date_index_dataframe_adapter_20261007 import installed
    from all_forecast_percentile_runtime_20261007 import installed as installed_percentile
    from cached_official_spearman_runtime_20261007 import installed as installed_ic
    from win32_read_handle_hash_cache_with_filename_v2_20261006 import LockedReadHashCache
    empty(OUT)
    plan_path=A/'BF16Medium78_round153_plan_v1_20261009.json';plan=read(plan_path)
    controls=Path(read(A/'actual_BF16Medium153_full73_training_location_v1_20261009.json')['output'])
    control=read(controls/'verification.json')
    assert control['status']=='passed_actual73_full5635800_medium153_signed_rank_mix_and219_cold_prefixes'
    neural_folder=Path(read(A/'actual_BF16Medium153_full5_independent_location_v1_20261009.json')['output'])
    neural_proof=read(neural_folder/'verification.json')
    assert neural_proof['status']=='passed_actual_full5_5635800_medium2048_BF16_native_and_independent_GPU_forecasts_and10_cold_prefixes'
    parents={n:A/f'optimization_20261003_r{n}' for n in plan['qualified_anchor_rounds']}
    baselines={n:read(p/'calibrated_csv_official.json')['metrics'] for n,p in parents.items()}
    parent_models={n:read(ROOT/f'candidates/optimization_20261003_r{n}/verification.json')['models'] for n in parents}
    comparison_parent=min(parents,key=lambda n:(-baselines[n]['final_score'],len(parent_models[n]),n))
    scheme_base=148
    assert scheme_base==control['actual_parent_round']==148
    final_info=read(Path(plan['actual_annual_bank'])/'2025/info.json');neural_sha=final_info['model_sha256']
    graph=read(ROOT/f'candidates/optimization_20261003_r{scheme_base}/verification.json')['whole_scheme_graph']
    assert 'nonflag_CPU_ReverseBayes64_residual_CDF' in graph and 'BF16_medium2048_seed09_complete_parent_rank_CDF' not in graph
    cases=[{'anchor_round':n,'model':None,'role':None,'weight':0.,'universe':None} for n in parents]
    cases += [{"anchor_round":148,"model":plan['model_name'] if c['weight'] else 'zero_BF16_rank_identity',"role":c['role'],"weight":c['weight'],"sign":c['sign'],"universe":plan['rank_universe']} for c in plan['new_cases']]
    assert len(cases)==plan['expected_scored_records']==78
    frame_path=A/'connected_validation_20261002/combined_fold_frame.parquet'
    neural_path=neural_folder/'combined_raw.parquet'
    scoring_source=A/'optimization_20261003_r95/scoring_validation_only'
    duplicate_pointer=A/'actual_BF16Medium153_prior_complete_forecast_duplicate_audit_v1_20261009.json'
    duplicate_proof=Path(read(duplicate_pointer)['output'])/'verification.json'
    assert sha(duplicate_proof)==read(duplicate_pointer)['verification_sha256']
    duplicate=read(duplicate_proof);assert duplicate['actual_current_cases']==73
    duplicate_by_sha={r['numeric_sha256']:r['prior_full_board_matches'] for r in duplicate['records']}
    sources=[Path(__file__),Path(codec.__file__),A/'BF16Medium153_storage_v1_20261009.py',plan_path,
        controls/'verification.json',neural_folder/'verification.json',frame_path,neural_path,
        A/'BF16Medium78_round153_source_admission_v1_20261009.json',A/'BF16Medium78_controls_github_v1_20261009/receipt.json',
        A/'score_calibrated_candidates_20261003.py',A/'official_date_index_dataframe_adapter_20261007.py',
        A/'all_forecast_percentile_runtime_20261007.py',A/'cached_official_spearman_runtime_20261007.py',
        A/'exact_cached_official_spearman_v2_20261007.py',A/'exact_cached_validation_spearman_20261007.py',ROOT/'evaluate.py',ROOT/'后续选模标准.md',
        *[scoring_source/n for n in ('测试集_X.csv','测试集_Y.csv')]]
    sources += [duplicate_pointer,duplicate_proof]
    for n,p in parents.items():
        assert read(p/'full_registration_execution.json')['status']=='passed'
        sources += [p/name for name in ('selection.json','protocol.json','selected_validation.npy','calibrated_csv_official.json','full_registration_execution.json')]
        sources += [ROOT/f'candidates/optimization_20261003_r{n}'/name for name in ('verification.json','manifest.json')]
        sources += [A/f'github_validation_sync_main_20261005/round{n}_receipt.json']
    pins={**control['input_sha256'],**neural_proof['input_sha256'],**{str(p):sha(p) for p in sources}}
    create(OUT/'frozen_before_actual_full_controls_and_official_scores.json',{'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),
        'input_sha256':pins,'cases':cases,'actual_comparison_parent_round':comparison_parent,'actual_scheme_base_round':scheme_base,
        'baseline_metrics':baselines,'whole_complete_parent_all_original_branches_retained':True,'first2020_active':True,
        'native_bank_fits':6,'new_native_fits_by_comparison':0,'selection_bias_uncorrected':True,
        'no_extra_Top_worst_year_or_significance_gate':True,'test_labels_read':False})
    while psutil.virtual_memory().available<8.5*2**30:time.sleep(15)
    records=[];rank_cache={}
    with LockedReadHashCache(pins) as scope,installed_transfer():
        frame=pl.read_parquet(frame_path,columns=['ts_code','trade_date','flag_limit_up','price_valid','y_ret_1d'])
        neural_frame=pl.read_parquet(neural_path)
        assert neural_frame.select(['ts_code','trade_date']).equals(frame.select(['ts_code','trade_date']))
        dates,flags,valid=[frame[k].to_numpy() for k in ('trade_date','flag_limit_up','price_valid')]
        assert (len(frame),frame['trade_date'].n_unique(),frame['ts_code'].n_unique())==(5635800,1212,4650)
        parent=np.load(parents[scheme_base]/'selected_validation.npy',mmap_mode='r')
        neural=neural_frame['pred_raw'].to_numpy();prepared={sign:codec.prepare(parent,neural,dates,flags,valid,sign) for sign in (1.,-1.)}
        scoring=A/'BF16Medium153_D_scoring_v1_20261009/comparison/scoring_validation_only';scoring.mkdir(parents=True)
        for n in ('测试集_X.csv','测试集_Y.csv'):os.link(scoring_source/n,scoring/n)
        ctx=SimpleNamespace(frame=frame,dates=dates,scoring=scoring)
        for index,cfg in enumerate(cases):
            if cfg['model'] is None:
                values=np.asarray(np.load(parents[cfg['anchor_round']]/'selected_validation.npy',mmap_mode='r'))
            else:
                values=codec.apply_prepared(parent,flags,valid,cfg['role'],cfg['weight'],prepared[cfg['sign']])
                mask=codec.selected(flags,valid,cfg['role'])
                assert np.array_equal(values[~mask].view('u8'),np.asarray(parent)[~mask].view('u8'))
                for count in (80,260,975):
                    n=count*4650
                    cold=codec.transform(parent[:n],neural[:n],dates[:n],flags[:n],valid[:n],cfg['role'],cfg['weight'],cfg['sign'])
                    assert np.array_equal(values[:n].view('u8'),cold.view('u8'))
            write(OUT/'actual_stage.json',{'status':'actual_full_official_scoring','at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),
                'case':index,'configuration':cfg,'actual_completed_cases':len(records),'expected_cases':78})
            with installed_percentile() as percentile_runtime,installed_ic(rank_cache) as ic_runtime:
                with installed(scoring/'submission.csv') as date_index:metrics=score(ctx,values)
            if cfg['model'] is None:assert metrics==baselines[cfg['anchor_round']]
            if cfg['weight']==0. and cfg['model'] is not None:
                assert metrics==baselines[scheme_base] and np.array_equal(values.view('u8'),np.asarray(parent).view('u8'))
            capsule=Path(ctx.last_official_score_cache['official_metrics_source'])
            item={'case':index,'configuration':cfg,'metrics':metrics,'connected_final_score':metrics['final_score'],
                'score_gain_over_qualified_parent':metrics['final_score']-baselines[comparison_parent]['final_score'],
                'actual_comparison_parent_round':comparison_parent,'actual_scheme_base_round':scheme_base,
                'prediction_numeric_bytes_sha256':hashlib.sha256(memoryview(np.ascontiguousarray(values)).cast('B')).hexdigest(),
                'official_date_index_runtime':dict(date_index),'all_row_percentile_runtime':percentile_runtime,'scoring_only_spearman_runtime':ic_runtime,
                'official_score_cache':ctx.last_official_score_cache,'official_metric_capsule_sha256':sha(capsule),
                'actual_return_mapping':ctx.last_candidate_return_mapping,
                'whole_complete_parent_branches_preserved_before_new_stage':True,
                'invalid_and_declared_unselected_raw_bits_preserved':cfg['model'] is not None,
                'actual_cold80_260_975_bits_exact':cfg['model'] is not None,'qualified_anchor_all8_metrics_exact':cfg['model'] is None,
                'native_bank_source':str(neural_folder/'verification.json'),
                'ordered_native_components':[] if cfg['model'] is None or cfg['weight']==0. else [plan['model_name']],
                'expected_unique_native_models':len({m['sha256'] for m in parent_models[cfg['anchor_round']].values()} | ({neural_sha} if cfg['model'] is not None and cfg['weight']>0. else set())),
                'first2020_active':cfg['model'] is not None and cfg['weight']>0.,
                'candidate_future_freeze_replays_QA64_and_main_pending':True,'test_labels_read':False}
            previous=duplicate_by_sha.get(item['prediction_numeric_bytes_sha256'],[])
            all8=0
            for observed in previous:
                assert all(metrics[k]==v for k,v in observed['metrics'].items()),observed['id']
                if observed['all8_metrics'] is not None:
                    assert metrics==observed['all8_metrics'],observed['id'];all8+=1
            item['observed_prior_complete_forecast_matches']=len(previous)
            item['observed_prior_complete_all8_metric_crosschecks']=all8
            create(OUT/f'case{index:02d}_official.json',item);records.append(item)
            print({'case':index,'score':metrics['final_score'],'gain':item['score_gain_over_qualified_parent']},flush=True)
            del values;gc.collect()
        scope.reverify()
    from prepare_BF16Medium153_core_drafts_v1_20261009 import best_key
    best=min(records,key=best_key)
    create(OUT/'verification.json',{'status':STATUS,'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),
        'input_sha256':pins,'records':records,'best':best,'components':{plan['model_name']:[plan['model_name']]},
        'actual_comparison_parent_round':comparison_parent,'actual_scheme_base_round':scheme_base,
        'existing_native_bank_fits':6,'new_native_fits_by_comparison':0,'new_quality_score_records':78,
        'all73_nonanchors_full_and_cold_controls_passed':True,'future_candidate_and_full153_qualification_pending':True,
        'global_feasible_direction_or_resource_exhaustion_not_established':True,'test_labels_read':False})


if __name__=='__main__':main()
