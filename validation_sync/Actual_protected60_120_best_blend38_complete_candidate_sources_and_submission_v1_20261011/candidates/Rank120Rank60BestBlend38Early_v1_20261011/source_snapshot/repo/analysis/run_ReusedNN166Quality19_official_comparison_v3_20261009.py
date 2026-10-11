"""Official continuous OOF scoring of the frozen flagged-neural stage after complete152."""
from pathlib import Path
from types import SimpleNamespace
import sys,os,time,gc,hashlib,json
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
OUT=Path('E:/赛题五_本机临时/ReusedNN166Quality19_official_comparison_v1_20261009')
for key in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','POLARS_MAX_THREADS'):os.environ[key]='2'
for key in ('TEMP','TMP','TMPDIR','MPLCONFIGDIR'):os.environ[key]=str(OUT/'tmp'/key)
from run_dependency_queue_v3_20261006 import read,sha,create,owned
def closed(name):
    f=A/'service_owned_workflows_20261006'/name
    while not (f/'native_launch.json').exists() or owned(read(f/'native_launch.json')):time.sleep(15)
    assert read(f/'service_execution.json')['status']=='passed',name
def write(path,value):
    temporary=path.with_name(path.name+f'.{os.getpid()}.tmp');temporary.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf8');os.replace(temporary,path)
def best_key(row):return (-row['connected_final_score'],row['expected_unique_native_models'],abs(row['configuration']['weight']),row['case'])
def main():
    closed('ReusedNN166Quality19_round166_source_admission_v1_20261009')
    closed('ReusedNN166Quality19_controls_main_publication_v1_20261009')
    closed('ReusedNN166Full17_actual_full_training_controls_v1_20261009')
    closed('ReusedNN165Quality19_round165_full_registration_v1_20261009')
    closed('ReusedNN166Stage_actual_native14_calendar_v1_20261009')
    import numpy as np,polars as pl,psutil
    import BF16Medium153_complete_parent_rank_CDF_v1_20261009 as codec
    from score_calibrated_candidates_20261003 import score
    from official_date_index_dataframe_adapter_20261007 import installed
    from all_forecast_percentile_runtime_20261007 import installed as installed_percentile
    from cached_official_spearman_runtime_20261007 import installed as installed_ic
    from win32_read_handle_hash_cache_with_filename_v2_20261006 import LockedReadHashCache
    planpath=A/'ReusedNN166Quality19_quality_preparation_v59_20261009.json';plan=read(planpath)
    for p,d in plan['input_sha256'].items():assert sha(p)==d,p
    proposalpath=A/'ReusedNN166Full17_train_only_proposal_v1_20261009.json';proposal=read(proposalpath)
    ptr=A/'actual_ReusedNN166Full17_full_training_location_v1_20261009.json';controls=Path(read(ptr)['output'])/'verification.json'
    assert sha(controls)==read(ptr)['verification_sha256'];control=read(controls)
    assert (control['actual_parent_round'],control['actual_full_cases'],control['actual_cold_cases'])==(152,17,51)
    native_pointer=A/'actual_ReusedNN166Stage_native14_calendar_location_v1_20261009.json'
    native_proof_path=Path(read(native_pointer)['output'])/'verification.json'
    assert sha(native_proof_path)==read(native_pointer)['verification_sha256']
    native_proof=read(native_proof_path)
    assert (native_proof['actual_saved_states'],native_proof['actual_historical_cases'],native_proof['actual_calendar_cases'],native_proof['actual_cold_cases'])==(6,10,4,14)
    assert len(native_proof['records'])==14 and len(native_proof['prefit_rejections'])==7

    parents={n:A/f'optimization_20261003_r{n}' for n in (152, 165)}
    baselines={n:read(p/'calibrated_csv_official.json')['metrics'] for n,p in parents.items()}
    models={n:read(ROOT/f'candidates/optimization_20261003_r{n}/verification.json')['models'] for n in parents}
    comparison=min(parents,key=lambda n:(-baselines[n]['final_score'],len({m['sha256'] for m in models[n].values()}),n))
    bank=Path(proposal['native_bank']);neural_sha=read(bank/'2025/info.json')['model_sha256']
    loc=A/'actual_BF16ReturnHuber050166_full5_independent_location_v1_20261009.json';neural_folder=Path(read(loc)['output'])
    proof=neural_folder/'verification.json';assert sha(proof)==read(loc)['verification_sha256']
    framepath=A/'connected_validation_20261002/combined_fold_frame.parquet';rawpath=neural_folder/'combined_raw.parquet'
    scoring_source=A/'optimization_20261003_r95/scoring_validation_only'
    cases=[{'anchor_round':n,'model':None,'role':None,'weight':0.,'sign':1.,'universe':None} for n in parents]
    cases += [{'anchor_round':152,'model':proposal['model_name'] if c['weight'] else 'zero_BF16_rank_identity',
        'role':c['role'],'weight':c['weight'],'sign':c['sign'],'universe':'all_current_raw_forecasts'} for c in proposal['new_cases']]
    assert len(cases)==19
    sources=[Path(__file__),planpath,proposalpath,ptr,controls,loc,proof,framepath,rawpath,Path(codec.__file__),
        A/'BF16_complete_parent_rank_CDF_v1_20261008.py',A/'score_calibrated_candidates_20261003.py',
        A/'official_date_index_dataframe_adapter_20261007.py',A/'all_forecast_percentile_runtime_20261007.py',
        A/'cached_official_spearman_runtime_20261007.py',ROOT/'evaluate.py',ROOT/'后续选模标准.md',
        *[scoring_source/n for n in ('测试集_X.csv','测试集_Y.csv')]]
    for n,p in parents.items():
        assert read(p/'full_registration_execution.json')['status']=='passed'
        sources += [p/name for name in ('selected_validation.npy','calibrated_csv_official.json','full_registration_execution.json')]
        sources += [ROOT/f'candidates/optimization_20261003_r{n}'/name for name in ('verification.json','manifest.json')]
        sources.append(A/f'github_validation_sync_main_20261005/round{n}_receipt.json')
    sources += [native_pointer,native_proof_path,A/'ReusedNN166Stage_complete_native_predictor_preparation_v58_20261009.json']
    pins={**control['input_sha256'],**native_proof['input_sha256'],**{str(p):sha(p) for p in sources}}
    from ReusedNN166Stage_storage_v1_20261009 import empty
    empty(A/'ReusedNN166Quality19_official_comparison_v1_20261009')
    create(OUT/'frozen_before_actual22_official_scores.json',{'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),
        'input_sha256':pins,'cases':cases,'fixed_stage_base':152,'comparison_parent':comparison,'baseline_metrics':baselines,
        'actual_future_X_read':False,'test_labels_read':False,'selection_bias_uncorrected':True,
        'candidate_future_freeze_full_native_replays_and_complete_ranking_still_required':True})
    while psutil.virtual_memory().available<11.5*2**30:time.sleep(15)
    with LockedReadHashCache(pins) as scope:
        frame=pl.read_parquet(framepath,columns=['ts_code','trade_date','flag_limit_up','price_valid','y_ret_1d']);rawframe=pl.read_parquet(rawpath)
        assert frame.select(['ts_code','trade_date']).equals(rawframe.select(['ts_code','trade_date']))
        assert (len(frame),frame['trade_date'].n_unique(),frame['ts_code'].n_unique())==(5635800,1212,4650)
        dates,flags,valid=[frame[k].to_numpy() for k in ('trade_date','flag_limit_up','price_valid')]
        parent=np.load(parents[152]/'selected_validation.npy',mmap_mode='r');raw=rawframe['pred_raw'].to_numpy()
        prepared={s:codec.prepare(parent,raw,dates,flags,valid,s) for s in (1.,-1.)}
        scoring=A/'ReusedNN166Stage_D_scoring_v1_20261009/comparison/scoring_validation_only';scoring.mkdir(parents=True,exist_ok=False)
        for name in ('测试集_X.csv','测试集_Y.csv'):os.link(scoring_source/name,scoring/name)
        ctx=SimpleNamespace(frame=frame,dates=dates,scoring=scoring);records=[];rank_cache={}
        for i,cfg in enumerate(cases):
            if cfg['model'] is None:value=np.asarray(np.load(parents[cfg['anchor_round']]/'selected_validation.npy',mmap_mode='r'))
            else:
                value=codec.apply_prepared(parent,flags,valid,cfg['role'],cfg['weight'],prepared[cfg['sign']])
                mask=codec.selected(flags,valid,cfg['role']);assert np.array_equal(value[~mask].view('u8'),np.asarray(parent)[~mask].view('u8'))
                assert hashlib.sha256(memoryview(np.ascontiguousarray(value)).cast('B')).hexdigest()==control['controls'][i-2]['numeric_sha256']
            write(OUT/'actual_stage.json',{'status':'actual_official22_scoring','at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'actual_completed_cases':len(records),'expected_cases':19,'case':i,'configuration':cfg})
            with installed_percentile() as percentile,installed_ic(rank_cache) as ic:
                with installed(scoring/'submission.csv') as date_index:metrics=score(ctx,value)
            if cfg['model'] is None:assert metrics==baselines[cfg['anchor_round']]
            if not cfg['weight'] and cfg['model'] is not None:assert metrics==baselines[152]
            capsule=Path(ctx.last_official_score_cache['official_metrics_source'])
            row={'case':i,'configuration':cfg,'metrics':metrics,'connected_final_score':metrics['final_score'],
                'score_gain_over_qualified_parent':metrics['final_score']-baselines[comparison]['final_score'],
                'actual_comparison_parent_round':comparison,'actual_scheme_base_round':152,
                'prediction_numeric_bytes_sha256':hashlib.sha256(memoryview(np.ascontiguousarray(value)).cast('B')).hexdigest(),
                'expected_unique_native_models':len({m['sha256'] for m in models[cfg['anchor_round']].values()}|({neural_sha} if cfg['model'] is not None and cfg['weight']>0. else set())),
                'ordered_native_components':[] if cfg['model'] is None or not cfg['weight'] else [proposal['model_name']],
                'official_score_cache':ctx.last_official_score_cache,'official_metric_capsule_sha256':sha(capsule),
                'official_date_index_runtime':dict(date_index),'all_row_percentile_runtime':percentile,'scoring_only_spearman_runtime':ic,
                'actual_return_mapping':ctx.last_candidate_return_mapping,'test_labels_read':False,
                'whole_complete152_branches_preserved_before_new_stage':True,
                'whole_complete_parent_branches_preserved_before_new_stage':cfg['model'] is not None,
                'qualified_anchor_all8_metrics_exact':cfg['model'] is None,
                'invalid_and_declared_unselected_raw_bits_preserved':cfg['model'] is not None,
                'actual_cold80_260_975_bits_exact':cfg['model'] is not None,
                'first2020_active':cfg['model'] is not None and cfg['weight']>0.,
                'native_bank_source':str(proof),
                'candidate_full_native_replays_and_sealing_and_complete_ranking_pending':True}
            create(OUT/f'case{i:02d}_official.json',row);records.append(row)
            print({'case':i,'score':metrics['final_score'],'gain':row['score_gain_over_qualified_parent']},flush=True)
            del value;gc.collect()
        scope.reverify()
    best=min(records,key=best_key)
    create(OUT/'verification.json',{'status':'passed_actual19_reusedNN166_complete_parent_rank_CDF_full_official_comparisons',
        'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'input_sha256':pins,'records':records,'best':best,'components':{proposal['model_name']:[proposal['model_name']]},
        'actual_comparison_parent_round':comparison,'actual_scheme_base_round':152,'new_quality_score_records':19,
        'existing_neural_mature_annual_states_reused':6,'new_native_fits':0,
        'candidate_freeze_inference_native_replays_seal_and_complete_registration_pending':True,'test_labels_read':False,
        'global_feasible_direction_or_resource_exhaustion_not_established':True})
    create(A/'actual_ReusedNN166Quality19_official_comparison_location_v1_20261009.json',{'output':str(OUT),'verification_sha256':sha(OUT/'verification.json')})
if __name__=='__main__':main()
