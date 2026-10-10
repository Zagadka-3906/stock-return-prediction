"""Measure real344-day TRAIN feature caching and full/cold/mutation isolation."""
from pathlib import Path
import sys,os,time,hashlib,gc
A=Path(__file__).resolve().parent;ROOT=A.parent;sys.path[:0]=[str(ROOT),str(A)]
OUT=Path('E:/赛题五_本机临时/actual_feature120_verified_memoization_TRAIN344_v1_20261010')
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
def numeric(a):return hashlib.sha256(memoryview(a).cast('B')).hexdigest()
def main():
    assert allowed();import psutil
    while psutil.virtual_memory().available<12*2**30:assert allowed();time.sleep(10)
    for k in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','POLARS_MAX_THREADS'):os.environ[k]='2'
    import numpy as np,polars as pl
    import daily_cross_sectional_feature_encoder120_v1_20261010 as encoder
    import exact_verified_feature120_memoization_runtime_v1_20261010 as cache
    from run import FEATURE_FILE,feature_names,to_matrix
    paths=[Path(__file__),Path(cache.__file__),Path(encoder.__file__),FEATURE_FILE];pins={str(p):sha(p) for p in paths}
    OUT.mkdir(exist_ok=False);create(OUT/'frozen_before_actual_benchmark.json',{'input_sha256':pins,'actual_future_X_read':False,'test_labels_read':False})
    names=feature_names();keys=['ts_code','trade_date']
    lazy=pl.scan_parquet(FEATURE_FILE).filter(pl.col('is_train'))
    days=lazy.select('trade_date').unique().sort('trade_date').tail(344).collect()['trade_date'].to_list()
    frame=lazy.filter(pl.col('trade_date').is_in(days)).select(keys+names).sort('trade_date','ts_code').collect()
    x=np.ascontiguousarray(to_matrix(frame,names),dtype=np.float32);dates=frame['trade_date'].to_numpy();del frame
    assert len(x)==1599600 and len(days)==344 and np.all(np.unique(dates,return_counts=True)[1]==4650)
    started=time.perf_counter();primary=encoder.encode(x,dates,names);independent=encoder.pandas_oracle(x,dates,names)
    assert np.array_equal(primary.view('u4'),independent.view('u4'));uncached_seconds=time.perf_counter()-started;digest=numeric(primary);del primary,independent;gc.collect()
    print({'actual_uncached_full_pair_seconds':uncached_seconds,'rows':len(x)},flush=True)
    cached_seconds=[];isolation=[]
    with cache.installed() as stats:
        for repeat in range(3):
            assert allowed();started=time.perf_counter();a=encoder.encode(x,dates,names);b=encoder.pandas_oracle(x,dates,names)
            assert np.array_equal(a.view('u4'),b.view('u4')) and numeric(a)==digest;cached_seconds.append(time.perf_counter()-started)
            if repeat==0:a[0,0]=12345.;assert b[0,0]!=12345.
            del a,b;gc.collect();print({'actual_cached_full_pair':repeat,'seconds':cached_seconds[-1]},flush=True)
        n=80*4650;started=stats['misses'];a=encoder.encode(x[:n],dates[:n],names);b=encoder.pandas_oracle(x[:n],dates[:n],names)
        original=encoder.encode(x,dates,names)
        assert np.array_equal(a.view('u4'),b.view('u4')) and np.array_equal(a.view('u4'),original[:n].view('u4')) and stats['misses']==started+1
        isolation.append({'kind':'cold80_separate_key','native_Pandas_and_full_prefix_bits_exact':True});del a,b,original
        small=x[:4650].copy();small_dates=dates[:4650].copy();native=cache.installed
        # Independent native/oracle originals are captured outside the patched module by a fresh source execution.
        namespace={'__file__':str(Path(encoder.__file__)),'__name__':'actual_independent_unpatched_feature_encoder'}
        exec(compile(Path(encoder.__file__).read_text(encoding='utf8'),str(Path(encoder.__file__)),'exec'),namespace)
        for kind in ('changed_raw_peer','changed_date_group','row_order'):
            xx=small.copy();dd=small_dates.copy()
            if kind=='changed_raw_peer':xx[0,0]+=1.
            elif kind=='changed_date_group':dd[0]+=1
            else:xx=xx[::-1].copy();dd=dd[::-1].copy()
            prior=stats['misses'];a=encoder.encode(xx,dd,names);b=namespace['pandas_oracle'](xx,dd,names)
            assert stats['misses']==prior+1 and np.array_equal(a.view('u4'),b.view('u4'));isolation.append({'kind':kind,'fresh_key_and_independent_oracle_bits_exact':True});del a,b
        assert stats['max_retained_bytes']<=stats['configured_max_bytes']
    assert not encoder._exact_verified_cache_active
    for p,d in pins.items():assert sha(p)==d,p
    adopt=min(cached_seconds[1:])<uncached_seconds
    create(OUT/'verification.json',{'status':'passed_actual1599600_TRAIN_rows344_days_native_and_independent_full_bits_cold80_and_three_input_change_controls','input_sha256':pins,'rows':1599600,'days':344,'uncached_pair_seconds':uncached_seconds,'cached_pair_seconds':cached_seconds,'steady_state_speedup':uncached_seconds/min(cached_seconds[1:]),'actual_controls':isolation,'stats':stats,'adopt':adopt,'model_reload_and_independent_saved_tensor_predictions_not_cached':True,'no_training_or_scoring_changed':True,'new_fits':0,'new_quality_scores':0,'actual_future_X_read':False,'test_labels_read':False})
    create(A/'actual_feature120_verified_memoization_TRAIN344_location_v1_20261010.json',{'output':str(OUT),'verification_sha256':sha(OUT/'verification.json')})
    print({'actual_feature120_runtime_benchmark_passed':True,'adopt':adopt},flush=True)
if __name__=='__main__':main()
