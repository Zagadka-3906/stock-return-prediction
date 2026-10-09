"""Full37 causal sequential forecasts; only complete officialS selects and no new fits are needed."""
from pathlib import Path
from types import SimpleNamespace
from datetime import datetime
import sys,os,time,gc,hashlib,json
A=Path(__file__).resolve().parent;ROOT=A.parent;sys.path[:0]=[str(ROOT),str(A),str(A/'connected_validation_20261002')]
OUT=Path('E:/赛题五_本机临时/budgeted_neural_Top37_screen_v1_20261010')
for key in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','POLARS_MAX_THREADS'):os.environ[key]='2'
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed,closed

def write(path,value):
    t=path.with_name(path.name+f'.{os.getpid()}.tmp');t.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf8');os.replace(t,path)

def main():
    assert allowed()
    closed('BF16Huber010161_independent_full5_GPU_controls_v1_20261009');closed('BF16Huber010161_actual_native42_calendar_v1_20261009')
    import numpy as np,polars as pl,psutil
    import budgeted_neural_Top_projection_v1_20261010 as codec
    from score_calibrated_candidates_20261003 import score
    from official_date_index_dataframe_adapter_20261007 import installed
    from all_forecast_percentile_runtime_20261007 import installed as percentiles
    from cached_official_spearman_runtime_20261007 import installed as spearman
    proposalpath=A/'budgeted_neural_Top_projection37_proposal_v1_20261010.json';proposal=read(proposalpath);cases=proposal['cases'];assert len(cases)==37
    proofpath=A/'budgeted_neural_Top_projection_controls_v1_20261010.json';proof=read(proofpath);assert len(proof['records'])==48
    for p,d in proof['input_sha256'].items():assert sha(p)==d,p
    pointers={'seed09':A/'actual_BF16Medium153_full5_independent_location_v1_20261009.json','huber010':A/'actual_BF16Huber010161_full5_independent_location_v1_20261009.json'}
    sources=[Path(__file__),Path(codec.__file__),proposalpath,proofpath,ROOT/'后续选模标准.md',A/'BF16Medium153_complete_parent_rank_CDF_v1_20261009.py',A/'BF16_complete_parent_rank_CDF_v1_20261008.py',A/'optimization_20261003_r157/selected_validation.npy',A/'optimization_20261003_r157/calibrated_csv_official.json',A/'connected_validation_20261002/combined_fold_frame.parquet',A/'score_calibrated_candidates_20261003.py']
    for pointer in pointers.values():
        folder=Path(read(pointer)['output']);assert sha(folder/'verification.json')==read(pointer)['verification_sha256'];sources.extend([pointer,folder/'verification.json',folder/'combined_raw.parquet'])
    pins={str(p):sha(p) for p in sources};OUT.mkdir(exist_ok=False)
    create(OUT/'frozen_before_all_actual_full_controls_and_scores.json',{'status':'frozen37_mature_neural_bounded_optional_Top_swaps_after_complete157','at_local':datetime.now().isoformat(),'input_sha256':pins,'cases':cases,'scheme_base':157,'empty_initial_state_first_day_original_parent_Top':True,'stock_identity':'verified_fixed_sorted_stock_row_positions','annual_boundaries_do_not_reset_state':True,'mapped_csv_actual_turnover_not_assumed_to_equal_optional_swap_budget':True,'new_native_fits':0,'future_X_read':False,'test_labels_read':False})
    scoring=A/'budgeted_neural_Top37_D_scoring_v1_20261010/scoring_validation_only';scoring.mkdir(parents=True,exist_ok=False)
    for name in ('测试集_X.csv','测试集_Y.csv'):os.link(A/'optimization_20261003_r95/scoring_validation_only'/name,scoring/name)
    scratch=OUT/'tmp';scratch.mkdir()
    for key in ('TMP','TEMP','TMPDIR','MPLCONFIGDIR'):os.environ[key]=str(scratch)
    import tempfile;tempfile.tempdir=str(scratch)
    while psutil.virtual_memory().available<11.5*2**30:assert allowed();time.sleep(15)
    frame=pl.read_parquet(A/'connected_validation_20261002/combined_fold_frame.parquet',columns=['ts_code','trade_date','flag_limit_up','price_valid','y_ret_1d'])
    assert (len(frame),frame['trade_date'].n_unique(),frame['ts_code'].n_unique())==(5635800,1212,4650)
    stock_codes=frame['ts_code'].to_numpy().reshape(1212,4650);assert np.all(stock_codes==stock_codes[0]) and len(set(stock_codes[0]))==4650
    dates,flags,valid=[frame[k].to_numpy() for k in ('trade_date','flag_limit_up','price_valid')]
    parent=np.load(A/'optimization_20261003_r157/selected_validation.npy',mmap_mode='r');baseline=read(A/'optimization_20261003_r157/calibrated_csv_official.json')['metrics']
    ctx=SimpleNamespace(frame=frame,dates=dates,scoring=scoring);rank_cache={};records=[];raw=None;prepared=None;recipe=None
    for i,c in enumerate(cases):
        assert allowed();controls=[];started=time.perf_counter()
        if c['recipe'] is None:value=np.asarray(parent);trace=[]
        else:
            if recipe!=c['recipe']:
                raw=None;prepared=None;gc.collect();rf=pl.read_parquet(Path(read(pointers[c['recipe']])['output'])/'combined_raw.parquet')
                assert rf.select(['ts_code','trade_date']).equals(frame.select(['ts_code','trade_date']))
                raw=rf['pred_raw'].to_numpy();prepared=codec.ranks.prepare(parent,raw,dates,flags,valid,c['sign']);recipe=c['recipe'];del rf
            args=(c['weight'],c['budget_fraction'],c['margin'])
            value,trace=codec.apply_prepared(parent,flags,valid,*args,prepared,return_trace=True)
            oracle,othertrace=codec.pandas_oracle(parent,raw,dates,flags,valid,*args,c['sign'],return_trace=True)
            assert np.array_equal(value.view('u8'),oracle.view('u8')) and trace==othertrace;del oracle,othertrace
            unchanged=~((flags==0)&valid);assert np.array_equal(value[unchanged].view('u8'),np.asarray(parent)[unchanged].view('u8'))
            assert all(t['optional_swaps']<=t['budget'] for t in trace) and np.array_equal(value[:4650].view('u8'),np.asarray(parent)[:4650].view('u8'))
            for days in (80,260,975):
                n=days*4650;prefix=codec.transform(parent[:n],raw[:n],dates[:n],flags[:n],valid[:n],*args,c['sign']);oracle=codec.pandas_oracle(parent[:n],raw[:n],dates[:n],flags[:n],valid[:n],*args,c['sign'])
                assert np.array_equal(value[:n].view('u8'),prefix.view('u8')) and np.array_equal(value[:n].view('u8'),oracle.view('u8'))
                controls.append({'days':days,'rows':n,'sequential_and_independent_bits_exact':True});del prefix,oracle
        control={'case':i,'configuration':c,'rows':len(value),'full_independent_Pandas_exact':bool(i),'prefix_controls':controls,'numeric_sha256':hashlib.sha256(memoryview(np.ascontiguousarray(value)).cast('B')).hexdigest(),'sequential_optional_budget_checks':trace,'stock_identity_grid_verified':True,'control_elapsed_seconds':time.perf_counter()-started,'state_not_reset_at_annual_boundaries':True,'actual_future_X_read':False}
        create(OUT/f'case{i:03d}_controls.json',control);write(OUT/'actual_stage.json',{'status':'actual_budgeted_neural_Top_projection_training_only_official_scoring','at_local':datetime.now().isoformat(),'case':i,'completed_cases':len(records),'expected_cases':37,'configuration':c})
        assert allowed()
        with percentiles(),spearman(rank_cache),installed(scoring/'submission.csv'):metrics=score(ctx,value)
        if not i:assert metrics==baseline
        capsule=Path(ctx.last_official_score_cache['official_metrics_source']);row={'case':i,'configuration':c,'metrics':metrics,'connected_final_score':metrics['final_score'],'score_gain_over_qualified_parent':metrics['final_score']-baseline['final_score'],'control_sha256':sha(OUT/f'case{i:03d}_controls.json'),'prediction_numeric_sha256':control['numeric_sha256'],'official_metric_capsule_sha256':sha(capsule),'official_score_cache':ctx.last_official_score_cache,'actual_return_mapping':ctx.last_candidate_return_mapping,'submission_qualified':False,'future_X_read':False,'test_labels_read':False,'new_native_fits':0,'first2020_active_after_declared_first_day_initialization':bool(i),'selection_bias_uncorrected':True,'new_complete_native_scheme_freeze_inference_and_registration_required_before_adoption':True}
        create(OUT/f'case{i:03d}_official.json',row);records.append(row);write(OUT/'best_so_far.json',{'completed_cases':len(records),'expected_cases':37,'best':max(records,key=lambda r:r['connected_final_score']),'submission_qualified':False})
        print({'case':i,'configuration':c,'S':metrics['final_score'],'gain':row['score_gain_over_qualified_parent'],'controls_seconds':control['control_elapsed_seconds']},flush=True);del value;gc.collect()
    for p,d in pins.items():assert sha(p)==d,p
    create(OUT/'verification.json',{'status':'passed37_actual_causal_budgeted_neural_Top_projection_connected_official_comparisons','at_local':datetime.now().isoformat(),'input_sha256':pins,'records':records,'best':max(records,key=lambda r:r['connected_final_score']),'new_quality_score_records':37,'actual_nonidentity_full_controls':36,'actual_nonidentity_prefix_controls':108,'new_native_fits':0,'submission_qualified':False,'future_X_read':False,'test_labels_read':False,'global_feasible_direction_exhaustion_not_proven':True})
    create(A/'actual_budgeted_neural_Top37_screen_location_v1_20261010.json',{'output':str(OUT),'verification_sha256':sha(OUT/'verification.json')})

if __name__=='__main__':main()
