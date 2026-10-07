"""Compare actual full weighted vectors and original all-row percentiles in two orders."""
from pathlib import Path
import hashlib
import os
import sys
import time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis'
sys.path[:0]=[str(ROOT),str(A),str(A/'connected_validation_20261002')]
for key in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','POLARS_MAX_THREADS'):os.environ[key]='2'
from run_dependency_queue_v3_20261006 import read,sha,create

def main():
    import numpy as np
    import pandas as pd
    import polars as pl
    from return_mapping import daily_percentile as original
    from exact_numpy_all_forecast_percentiles_20261007 import AllForecastPercentiles
    from refine_flagged_HGB_compatible_parent_transform_20261007 import prepare,apply_prepared
    from win32_read_handle_hash_cache_with_filename_v2_20261006 import LockedReadHashCache
    out=A/'all_forecast_percentiles_benchmark_20261007';assert not out.exists();out.mkdir()
    plan_path=A/'flagged_HGB_weighted_quarters340_plan_20261007.json';plan=read(plan_path)
    bank=A/plan['existing_native_bank'];frame_path=A/'connected_validation_20261002/combined_fold_frame.parquet'
    source=ROOT/'analysis/connected_validation_20261002/return_mapping.py'
    reference_path=A/'optimization_20261003_r106/selected_validation.npy';parent_path=A/'optimization_20261003_r112/selected_validation.npy'
    sources=[Path(__file__),A/'exact_numpy_all_forecast_percentiles_20261007.py',source,plan_path,frame_path,reference_path,parent_path,*[bank/n/'flagged_oof_predictions.npy' for n in plan['single_native_heads']]]
    pins={str(p):sha(p) for p in sources};create(out/'frozen_before_actual_controls.json',{'input_sha256':pins,'new_native_fits':0,'no_labels_or_future_features_read':True})
    records=[];cold_records=[];edge_records=[];operator=AllForecastPercentiles(original)
    with LockedReadHashCache(pins) as scope:
        frame=pl.read_parquet(frame_path,columns=['trade_date','flag_limit_up','price_valid'])
        dates,flags,valid=[frame[n].to_numpy() for n in ('trade_date','flag_limit_up','price_valid')]
        assert len(frame)==5635800 and frame['trade_date'].n_unique()==1212
        reference=np.load(reference_path,mmap_mode='r');parent=np.load(parent_path,mmap_mode='r');pandas_frame=frame.select('trade_date').to_pandas()
        heads={n:np.load(bank/n/'flagged_oof_predictions.npy',mmap_mode='r') for n in plan['single_native_heads']}
        prepared=prepare(reference,dates,flags,valid,plan['universe'])
        chosen=[list(plan['ensembles'])[i] for i in (0,13,27)]
        _,starts=np.unique(dates,return_index=True);ends=np.r_[starts[1:],len(dates)]
        for name in chosen:
            residual=np.zeros(len(reference),dtype=np.float64)
            for head in plan['ensembles'][name]:residual+=heads[head]
            residual/=4.
            values=apply_prepared(parent,reference,flags,residual,.0125,prepared)
            checksums=[];timings={'original':[],'numpy':[]}
            for order in (('original','numpy'),('numpy','original')):
                for method in order:
                    started=time.perf_counter();result=(original if method=='original' else operator)(pandas_frame,values)
                    elapsed=time.perf_counter()-started;timings[method].append(elapsed)
                    checksums.append(hashlib.sha256(memoryview(np.ascontiguousarray(result)).cast('B')).hexdigest())
            assert len(set(checksums))==1
            full=operator(pandas_frame,values)
            for count in (80,260,975):
                n=int(ends[count-1]);before=original(pandas_frame.iloc[:n],values[:n]);after=operator(pandas_frame.iloc[:n],values[:n])
                assert np.array_equal(before.view('u8'),after.view('u8')) and np.array_equal(full[:n].view('u8'),after.view('u8'))
                cold_records.append({'mixture':name,'days':count,'rows':n,'original_numpy_and_whole_day_prefix_bits_exact':True})
            records.append({'mixture':name,'weight':.0125,'rows':len(values),'days':1212,'all_full_raw_bits_exact':True,'percentile_sha256':checksums[0],'elapsed_seconds':timings})
        for case,values,dates_edge in [
            ('sentinels_ties_signed_zero_infinity',np.array([-10.,-1e6,-0.,0.,1.,1.,np.inf,-np.inf]),np.repeat(np.array([20240102]),8)),
            ('all_sentinels',np.array([-10.,-10.,-10.]),np.array([1,1,1])),
            ('float32',np.array([1.,1.,-10.,-0.],dtype=np.float32),np.array([1,1,2,2])),
            ('unsorted_fallback',np.array([1.,2.,3.]),np.array([2,1,2])),
            ('noninteger_dates_fallback',np.array([1.,1.,2.]),np.array(['a','a','b'])),
            ('integer_values_fallback',np.array([1,1,3]),np.array([1,1,1]))]:
            edge=pd.DataFrame({'trade_date':dates_edge});before=original(edge,values);after=operator(edge,values)
            assert np.array_equal(before.view('u8'),after.view('u8')),case
            edge_records.append({'case':case,'original_bits_exact':True,'all_rows_including_sentinels_retained':True})
        for case,values in [('empty',np.array([],dtype=float)),('NaN',np.array([1.,np.nan]))]:
            edge=pd.DataFrame({'trade_date':np.ones(len(values),dtype=np.int64)});errors=[]
            for method in (original,operator):
                try:method(edge,values)
                except Exception as error:errors.append((type(error).__name__,str(error)))
            assert len(errors)==2 and errors[0]==errors[1];edge_records.append({'case':case,'original_error_preserved':errors[0]})
        scope.reverify()
    old=np.median([v for row in records for v in row['elapsed_seconds']['original']]);new=np.median([v for row in records for v in row['elapsed_seconds']['numpy']])
    create(out/'verification.json',{'status':'passed_actual_three_full5635800_all_row_percentile_two_orders_and_nine_cold_prefix_controls',
        'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'input_sha256':pins,'records':records,'cold_records':cold_records,'edge_records':edge_records,
        'operator_statistics':operator.statistics(),'median_original_operator_seconds':float(old),'median_numpy_operator_seconds':float(new),'operator_only_speedup':float(old/new),
        'native_model_or_whole_official_score_or_whole_goal_speedup_not_claimed':True,'actual_full_official8_metric_equivalence_still_to_be_tested':True,
        'new_native_fits':0,'new_quality_scores':0,'test_labels_read':False})
    print({'status':'passed','full_vectors':3,'cold_prefixes':9,'operator_only_speedup':float(old/new)},flush=True)

if __name__=='__main__':main()
