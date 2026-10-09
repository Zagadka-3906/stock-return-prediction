"""Screen a genuinely new loss bank cumulatively, including tail-preserving interactions."""
from pathlib import Path
from types import SimpleNamespace
from datetime import datetime
import sys,os,time,hashlib,gc,json
A=Path(__file__).resolve().parent;ROOT=A.parent;sys.path[:0]=[str(ROOT),str(A),str(A/'connected_validation_20261002')]
OUT=Path('E:/赛题五_本机临时/Huber010_high_impact65_screen_v1_20261010')
for key in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','POLARS_MAX_THREADS'):os.environ[key]='2'
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed,closed

def write(path,value):
    t=path.with_name(path.name+f'.{os.getpid()}.tmp');t.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf8');os.replace(t,path)

def cases():
    rows=[{'kind':'anchor157','role':None,'weight':0.,'sign':1.,'protect_fraction':None}]
    for role in ('nonflag_valid','all_valid'):
        for sign in (1.,-1.):
            for weight in (.004,.016,.064,.125,.25,.5,.75,1.):rows.append({'kind':'CDF','role':role,'weight':weight,'sign':sign,'protect_fraction':None})
    for kind in ('valid_pool_protection_v1','official_Top_protection_v2'):
        for fraction in (.15,.25,.35,.5):
            for weight in (.004,.016,.064,.25):rows.append({'kind':kind,'role':'nonflag_valid','weight':weight,'sign':1.,'protect_fraction':fraction})
    assert len(rows)==65;return rows

def main():
    assert allowed()
    for name in ('actual_BF16_medium2048_huber010_seed09_e64_bank6_v1_20261009','BF16Huber010161_independent_full5_GPU_controls_v1_20261009','BF16Huber010161_actual_native42_calendar_v1_20261009'):closed(name)
    import numpy as np,polars as pl,psutil
    import BF16Medium153_complete_parent_rank_CDF_v1_20261009 as cdf
    import protected_upper_tail_rank_permutation_v1_20261010 as valid_tail
    import protected_official_top_rank_permutation_v2_20261010 as top_tail
    from score_calibrated_candidates_20261003 import score
    from official_date_index_dataframe_adapter_20261007 import installed
    from all_forecast_percentile_runtime_20261007 import installed as percentiles
    from cached_official_spearman_runtime_20261007 import installed as spearman
    bank=Path('E:/赛题五_本机临时/neural_BF16_medium2048_huber010_seed09_e64_bank6_v1_20261009')
    fullpointer=A/'actual_BF16Huber010161_full5_independent_location_v1_20261009.json';nativepointer=A/'actual_BF16Huber010161_native42_calendar_location_v1_20261009.json'
    full=Path(read(fullpointer)['output']);native=Path(read(nativepointer)['output'])
    assert read(bank/'verification.json')['actual_native_fits']==6
    assert read(full/'verification.json')['rows_days_stocks']==[5635800,1212,4650]
    assert read(native/'verification.json')['actual_saved_states']==6 and read(native/'verification.json')['actual_cold_cases']==42
    paths=[Path(__file__),A/'后续选模标准.md' if (A/'后续选模标准.md').exists() else ROOT/'后续选模标准.md',fullpointer,nativepointer,
        bank/'verification.json',full/'verification.json',native/'verification.json',full/'combined_raw.parquet',
        A/'optimization_20261003_r157/selected_validation.npy',A/'optimization_20261003_r157/calibrated_csv_official.json',A/'connected_validation_20261002/combined_fold_frame.parquet',
        Path(cdf.__file__),Path(valid_tail.__file__),Path(top_tail.__file__),A/'protected_upper_tail_rank_permutation_controls_v1_20261010.json',A/'protected_official_top_rank_permutation_controls_v2_20261010.json']
    pins={str(p):sha(p) for p in paths};plan=cases()
    OUT.mkdir(exist_ok=False)
    create(OUT/'frozen_before_any_new_controls_or_scores.json',{'status':'frozen_new_Huber65_cumulative157_hypotheses_after_own6_full5_native42_qualification','at_local':datetime.now().isoformat(),'input_sha256':pins,'cases':plan,'parent_round':157,'own_new_loss_bank_training_complete':True,'future_X_read':False,'test_labels_read':False,'new_native_fits_by_screen':0})
    scoring=A/'Huber010_high_impact65_D_scoring_v1_20261010/scoring_validation_only';scoring.mkdir(parents=True,exist_ok=False)
    for name in ('测试集_X.csv','测试集_Y.csv'):os.link(A/'optimization_20261003_r95/scoring_validation_only'/name,scoring/name)
    scratch=OUT/'tmp';scratch.mkdir()
    for key in ('TMP','TEMP','TMPDIR','MPLCONFIGDIR'):os.environ[key]=str(scratch)
    import tempfile;tempfile.tempdir=str(scratch)
    while psutil.virtual_memory().available<11.5*2**30:assert allowed();time.sleep(15)
    frame=pl.read_parquet(A/'connected_validation_20261002/combined_fold_frame.parquet',columns=['ts_code','trade_date','flag_limit_up','price_valid','y_ret_1d'])
    assert (len(frame),frame['trade_date'].n_unique(),frame['ts_code'].n_unique())==(5635800,1212,4650)
    rf=pl.read_parquet(full/'combined_raw.parquet');assert rf.select(['ts_code','trade_date']).equals(frame.select(['ts_code','trade_date']))
    dates,flags,valid=[frame[k].to_numpy() for k in ('trade_date','flag_limit_up','price_valid')]
    parent=np.load(A/'optimization_20261003_r157/selected_validation.npy',mmap_mode='r');raw=rf['pred_raw'].to_numpy()
    baseline=read(A/'optimization_20261003_r157/calibrated_csv_official.json')['metrics'];ctx=SimpleNamespace(frame=frame,dates=dates,scoring=scoring)
    ranks={};records=[];prepared={}
    exact=lambda x,y:np.array_equal(np.asarray(x,dtype=np.float64).view('u8'),np.asarray(y,dtype=np.float64).view('u8'))
    def transformed(c,n=None,oracle=False):
        n=len(parent) if n is None else n
        if c['kind']=='anchor157':return np.asarray(parent[:n])
        codec=cdf if c['kind']=='CDF' else valid_tail if c['kind']=='valid_pool_protection_v1' else top_tail
        args=(c['role'],c['weight'],c['sign']) if c['kind']=='CDF' else (c['weight'],c['protect_fraction'],c['sign'])
        fn=codec.pandas_oracle if oracle else codec.transform
        return fn(parent[:n],raw[:n],dates[:n],flags[:n],valid[:n],*args)
    for i,c in enumerate(plan):
        assert allowed()
        value=transformed(c)
        checks=[]
        if i:
            oracle=transformed(c,oracle=True);assert exact(value,oracle);del oracle
            if c['kind']=='CDF':assert exact(value[~cdf.selected(flags,valid,c['role'])],parent[~cdf.selected(flags,valid,c['role'])])
            else:(valid_tail if c['kind']=='valid_pool_protection_v1' else top_tail).assert_invariants(parent,value,dates,flags,valid,c['protect_fraction'])
            for days in (80,260,975):
                n=days*4650;prefix=transformed(c,n);oracle=transformed(c,n,True)
                assert exact(value[:n],prefix) and exact(value[:n],oracle);checks.append({'days':days,'rows':n,'native_and_independent_bits_exact':True});del prefix,oracle
        numeric=hashlib.sha256(memoryview(np.ascontiguousarray(value)).cast('B')).hexdigest()
        create(OUT/f'case{i:03d}_controls.json',{'case':i,'configuration':c,'numeric_sha256':numeric,'full_independent_Pandas_exact':bool(i),'prefix_controls':checks,'rows':len(value),'complete_parent157_preserved_before_stage':True,'future_X_read':False})
        write(OUT/'actual_stage.json',{'status':'actual_new_Huber65_training_only_official_scoring','case':i,'completed_cases':len(records),'expected_cases':65,'at_local':datetime.now().isoformat()})
        assert allowed()
        with percentiles(),spearman(ranks),installed(scoring/'submission.csv'):metrics=score(ctx,value)
        if not i:assert metrics==baseline
        capsule=Path(ctx.last_official_score_cache['official_metrics_source'])
        row={'case':i,'configuration':c,'recipe':'huber010','metrics':metrics,'connected_final_score':metrics['final_score'],'score_gain_over_qualified_parent':metrics['final_score']-baseline['final_score'],'control_sha256':sha(OUT/f'case{i:03d}_controls.json'),'prediction_numeric_sha256':numeric,'official_metric_capsule_sha256':sha(capsule),'official_score_cache':ctx.last_official_score_cache,'actual_return_mapping':ctx.last_candidate_return_mapping,'submission_qualified':False,'future_X_read':False,'test_labels_read':False,'selection_bias_uncorrected':True}
        create(OUT/f'case{i:03d}_official.json',row);records.append(row)
        write(OUT/'best_so_far.json',{'completed_cases':len(records),'expected_cases':65,'best':max(records,key=lambda r:r['connected_final_score']),'submission_qualified':False})
        print({'case':i,'configuration':c,'S':metrics['final_score'],'gain':row['score_gain_over_qualified_parent']},flush=True);del value;gc.collect()
    for p,d in pins.items():assert sha(p)==d,p
    create(OUT/'verification.json',{'status':'passed65_actual_qualified_new_Huber_cumulative157_and_protected_tail_training_only_official_comparisons','at_local':datetime.now().isoformat(),'input_sha256':pins,'records':records,'best':max(records,key=lambda r:r['connected_final_score']),'new_quality_score_records':65,'actual_nonidentity_full_controls':64,'actual_nonidentity_prefix_controls':192,'submission_qualified':False,'future_X_read':False,'test_labels_read':False,'global_feasible_direction_exhaustion_not_proven':True})
    create(A/'actual_Huber010_high_impact65_screen_location_v1_20261010.json',{'output':str(OUT),'verification_sha256':sha(OUT/'verification.json')})

if __name__=='__main__':main()
