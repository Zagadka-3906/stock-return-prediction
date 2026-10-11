"""Benchmark fixed-panel preparation reuse against native and Pandas on all5635800 TRAIN rows."""
from pathlib import Path
import sys,os,time,hashlib,gc
A=Path(__file__).resolve().parent;ROOT=A.parent;sys.path[:0]=[str(ROOT),str(A)]
for key in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','POLARS_MAX_THREADS'):os.environ[key]='2'
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed

def main():
    assert allowed()
    import numpy as np,polars as pl
    import immutable_prepared_rank_panel_cache_v1_20261010 as cache
    bank=Path(read(A/'actual_BF16Recent252Rank5Huber050172_full5_independent_location_v1_20261009.json')['output'])
    assert read(bank/'verification.json')['rows_days_stocks']==[5635800,1212,4650]
    paths=[Path(__file__),Path(cache.__file__),Path(cache.cdf.__file__),Path(cache.valid_tail.__file__),Path(cache.top_tail.__file__),
           A/'optimization_20261003_r168/selected_validation.npy',bank/'combined_raw.parquet',bank/'verification.json',A/'connected_validation_20261002/combined_fold_frame.parquet']
    pins={str(p):sha(p) for p in paths}
    out=Path('E:/赛题五_本机临时/immutable_prepared_rank_panel_cache_full_TRAIN_benchmark_v1_20261010');out.mkdir(exist_ok=False)
    create(out/'frozen_before_benchmark.json',{'input_sha256':pins,'actual_future_X_read':False,'test_labels_read':False,'new_quality_scores':0,'performance_only_no_live_pipeline_adoption':True})
    frame=pl.read_parquet(paths[-1],columns=['ts_code','trade_date','flag_limit_up','price_valid'])
    rawframe=pl.read_parquet(bank/'combined_raw.parquet');assert frame.select(['ts_code','trade_date']).equals(rawframe.select(['ts_code','trade_date']))
    parent=np.load(paths[-4],mmap_mode='r');raw=rawframe['pred_raw'].to_numpy()
    dates,flags,valid=[frame[k].to_numpy() for k in ('trade_date','flag_limit_up','price_valid')]
    assert len(parent)==len(raw)==5635800
    cases=[]
    for role in ('all_valid','nonflag_valid'):
        for sign in (1.,-1.):
            for weight in (.004,.064):cases.append({'kind':'CDF','role':role,'weight':weight,'sign':sign,'protect_fraction':None})
    for kind in ('valid_pool_protection_v1','official_Top_protection_v2'):
        for fraction in (.15,.25):cases.append({'kind':kind,'role':'nonflag_valid','weight':.064,'sign':1.,'protect_fraction':fraction})
    started=time.perf_counter();panel=cache.Panel(parent,raw,dates,flags,valid);cached_seconds=time.perf_counter()-started
    original_seconds=0.;records=[];exact=lambda a,b:np.array_equal(a.view('u8'),b.view('u8'))
    for i,c in enumerate(cases):
        assert allowed()
        codec={'CDF':cache.cdf,'valid_pool_protection_v1':cache.valid_tail,'official_Top_protection_v2':cache.top_tail}[c['kind']]
        args=(c['role'],c['weight'],c['sign']) if c['kind']=='CDF' else (c['weight'],c['protect_fraction'],c['sign'])
        started=time.perf_counter();baseline=codec.transform(parent,raw,dates,flags,valid,*args);original_seconds+=time.perf_counter()-started
        started=time.perf_counter();value=panel.transform(c);cached_seconds+=time.perf_counter()-started
        assert exact(value,baseline);oracle=codec.pandas_oracle(parent,raw,dates,flags,valid,*args);assert exact(value,oracle);del baseline,oracle
        prefixes=[]
        for days in (80,260,975):
            n=days*4650;prefix=panel.transform(c,n)
            original=codec.transform(parent[:n],raw[:n],dates[:n],flags[:n],valid[:n],*args)
            oracle=codec.pandas_oracle(parent[:n],raw[:n],dates[:n],flags[:n],valid[:n],*args)
            assert exact(prefix,value[:n]) and exact(prefix,original) and exact(prefix,oracle)
            prefixes.append(days);del prefix,original,oracle
        records.append({'case':i,'configuration':c,'full_native_and_Pandas_bits_exact':True,'cold_independent_prefix_days':prefixes,
                        'numeric_sha256':hashlib.sha256(memoryview(np.ascontiguousarray(value)).cast('B')).hexdigest()})
        del value;gc.collect();print(f'Actual fixed TRAIN panel cache {i+1}/12 full native/Pandas and3 cold prefixes',flush=True)
    # Mutation of caller input cannot change the panel's owned snapshots.
    small=cache.Panel(parent[:4650],raw[:4650],dates[:4650],flags[:4650],valid[:4650]);copied=raw[:4650].copy()
    assert not np.shares_memory(small.raw,raw) and np.array_equal(small.raw.view('u8'),copied.view('u8'))
    try:panel.transform(cases[0],4650-1)
    except AssertionError:pass
    else:raise AssertionError('Partial-date prefix accepted')
    for p,d in pins.items():assert sha(p)==d,p
    result={'status':'passed_actual5635800_TRAIN_rows12_native_and_Pandas_bit_controls36_independent_cold_prefixes_owned_immutable_snapshots_and_partial_date_refusal',
            'input_sha256':pins,'records':records,'rows_days_stocks':[5635800,1212,4650],
            'native_full_12_case_seconds':original_seconds,'cached_full_12_case_seconds_including_owned_copy_and_first_preparations':cached_seconds,
            'native_transform_speedup':original_seconds/cached_seconds,'does_not_measure_or_claim_whole_scoring_or_training_speedup':True,
            'live_pipeline_adoption':False,'new_quality_scores':0,'new_native_fits':0,'test_labels_read':False}
    create(out/'verification.json',result);create(A/'immutable_prepared_rank_panel_cache_actual_full_TRAIN_benchmark_v1_20261010.json',result)
    print({'speedup_native_transform_only':original_seconds/cached_seconds,'official_score_or_live_adoption_not_changed':True},flush=True)

if __name__=='__main__':main()
