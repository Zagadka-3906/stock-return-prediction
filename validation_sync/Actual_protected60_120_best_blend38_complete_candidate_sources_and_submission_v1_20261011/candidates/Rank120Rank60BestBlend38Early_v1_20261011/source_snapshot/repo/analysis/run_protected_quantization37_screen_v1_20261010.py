"""No-fit rank compression after complete157; same connected officialS and real prefix checks."""
from pathlib import Path
from types import SimpleNamespace
from datetime import datetime
import sys,os,time,gc,json,hashlib,itertools
A=Path(__file__).resolve().parent;ROOT=A.parent;sys.path[:0]=[str(ROOT),str(A),str(A/'connected_validation_20261002')]
OUT=Path('E:/赛题五_本机临时/protected_quantization37_screen_v1_20261010')
for key in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','POLARS_MAX_THREADS'):os.environ[key]='2'
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed

def write(path,value):
    t=path.with_name(path.name+f'.{os.getpid()}.tmp');t.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf8');os.replace(t,path)

def cases():
    return [{'bins':None,'protect_fraction':None,'representative':None}]+[{'bins':b,'protect_fraction':f,'representative':r} for b,f,r in itertools.product((8,16,32,64,128,256),(.15,.25,.4),('minimum','lower_median'))]

def main():
    assert allowed()
    import numpy as np,polars as pl,psutil
    import protected_lower_rank_quantization_v3_20261010 as codec
    from score_calibrated_candidates_20261003 import score
    from official_date_index_dataframe_adapter_20261007 import installed
    from all_forecast_percentile_runtime_20261007 import installed as percentiles
    from cached_official_spearman_runtime_20261007 import installed as spearman
    proofpath=A/'protected_lower_rank_quantization_controls_v3_20261010.json';proof=read(proofpath)
    assert len(proof['records'])==36
    for p,d in proof['input_sha256'].items():assert sha(p)==d,p
    sources=[Path(__file__),Path(codec.__file__),proofpath,A/'protected_lower_rank_quantization_controls_v1_20261010.json',ROOT/'后续选模标准.md',A/'optimization_20261003_r157/selected_validation.npy',A/'optimization_20261003_r157/calibrated_csv_official.json',A/'connected_validation_20261002/combined_fold_frame.parquet',A/'score_calibrated_candidates_20261003.py']
    pins={str(p):sha(p) for p in sources};plan=cases();assert len(plan)==37
    OUT.mkdir(exist_ok=False)
    create(OUT/'frozen_before_any_actual_full_controls_or_official_scores.json',{'status':'frozen37_model_free_protected_lower_rank_compression_hypotheses','at_local':datetime.now().isoformat(),'input_sha256':pins,'cases':plan,'parent_round':157,'new_native_fits':0,'new_physical_models':0,'actual_future_X_read':False,'test_labels_read':False,'v2_failed_signed_zero_oracle_not_adopted':True,'v3_original_and_independent_and_poison_proven':True})
    scoring=A/'protected_quantization37_D_scoring_v1_20261010/scoring_validation_only';scoring.mkdir(parents=True,exist_ok=False)
    for n in ('测试集_X.csv','测试集_Y.csv'):os.link(A/'optimization_20261003_r95/scoring_validation_only'/n,scoring/n)
    scratch=OUT/'tmp';scratch.mkdir()
    for n in ('TEMP','TMP','TMPDIR','MPLCONFIGDIR'):os.environ[n]=str(scratch)
    import tempfile;tempfile.tempdir=str(scratch)
    while psutil.virtual_memory().available<11.5*2**30:assert allowed();time.sleep(15)
    frame=pl.read_parquet(A/'connected_validation_20261002/combined_fold_frame.parquet',columns=['ts_code','trade_date','flag_limit_up','price_valid','y_ret_1d'])
    assert (len(frame),frame['trade_date'].n_unique(),frame['ts_code'].n_unique())==(5635800,1212,4650)
    dates,flags,valid=[frame[k].to_numpy() for k in ('trade_date','flag_limit_up','price_valid')]
    parent=np.load(A/'optimization_20261003_r157/selected_validation.npy',mmap_mode='r');baseline=read(A/'optimization_20261003_r157/calibrated_csv_official.json')['metrics']
    ctx=SimpleNamespace(frame=frame,dates=dates,scoring=scoring);rank_cache={};records=[]
    for i,c in enumerate(plan):
        assert allowed();controls=[];started=time.perf_counter()
        if not i:value=np.asarray(parent)
        else:
            args=(c['bins'],c['protect_fraction'],c['representative'])
            value=codec.transform(parent,dates,flags,valid,*args);oracle=codec.pandas_oracle(parent,dates,flags,valid,*args)
            assert np.array_equal(value.view('u8'),oracle.view('u8'));del oracle
            codec.assert_invariants(parent,value,dates,flags,valid)
            for days in (80,260,975):
                n=days*4650;prefix=codec.transform(parent[:n],dates[:n],flags[:n],valid[:n],*args);oracle=codec.pandas_oracle(parent[:n],dates[:n],flags[:n],valid[:n],*args)
                assert np.array_equal(value[:n].view('u8'),prefix.view('u8')) and np.array_equal(value[:n].view('u8'),oracle.view('u8'))
                controls.append({'days':days,'rows':n,'vectorized_and_independent_bits_exact':True});del prefix,oracle
        control={'case':i,'configuration':c,'full_independent_Pandas_exact':bool(i),'prefix_controls':controls,'rows':len(value),'numeric_sha256':hashlib.sha256(memoryview(np.ascontiguousarray(value)).cast('B')).hexdigest(),'control_elapsed_seconds':time.perf_counter()-started,'original_official_raw_Top_set_preserved':bool(i),'mapped_csv_official_turnover_invariance_not_assumed':True,'new_models':0,'future_X_read':False}
        create(OUT/f'case{i:03d}_controls.json',control)
        write(OUT/'actual_stage.json',{'status':'actual_model_free_quantization_train_only_official_scoring','at_local':datetime.now().isoformat(),'case':i,'completed_cases':len(records),'expected_cases':37,'configuration':c})
        assert allowed()
        with percentiles(),spearman(rank_cache),installed(scoring/'submission.csv'):metrics=score(ctx,value)
        if not i:assert metrics==baseline
        capsule=Path(ctx.last_official_score_cache['official_metrics_source']);row={'case':i,'configuration':c,'metrics':metrics,'connected_final_score':metrics['final_score'],'score_gain_over_qualified_parent':metrics['final_score']-baseline['final_score'],'control_sha256':sha(OUT/f'case{i:03d}_controls.json'),'prediction_numeric_sha256':control['numeric_sha256'],'official_metric_capsule_sha256':sha(capsule),'official_score_cache':ctx.last_official_score_cache,'actual_return_mapping':ctx.last_candidate_return_mapping,'submission_qualified':False,'future_X_read':False,'test_labels_read':False,'new_native_fits':0,'new_physical_models':0,'annual_excess_exactly_matches_parent':metrics['annual_excess']==baseline['annual_excess'],'turnover_exactly_matches_parent':metrics['mean_turnover']==baseline['mean_turnover'],'selection_bias_uncorrected':True,'new_full_scheme_freeze_native_inference_and_registration_required_before_adoption':True}
        create(OUT/f'case{i:03d}_official.json',row);records.append(row);write(OUT/'best_so_far.json',{'completed_cases':len(records),'expected_cases':37,'best':max(records,key=lambda r:r['connected_final_score']),'submission_qualified':False})
        print({'case':i,'configuration':c,'S':metrics['final_score'],'gain':row['score_gain_over_qualified_parent'],'controls_seconds':control['control_elapsed_seconds']},flush=True);del value;gc.collect()
    for p,d in pins.items():assert sha(p)==d,p
    create(OUT/'verification.json',{'status':'passed37_no_fit_protected_rank_quantization_connected_official_comparisons','at_local':datetime.now().isoformat(),'input_sha256':pins,'records':records,'best':max(records,key=lambda r:r['connected_final_score']),'new_quality_score_records':37,'actual_nonidentity_full_controls':36,'actual_nonidentity_prefix_controls':108,'new_native_fits':0,'new_physical_models':0,'submission_qualified':False,'future_X_read':False,'test_labels_read':False,'global_feasible_direction_exhaustion_not_proven':True})
    create(A/'actual_protected_quantization37_screen_location_v1_20261010.json',{'output':str(OUT),'verification_sha256':sha(OUT/'verification.json')})

if __name__=='__main__':main()
