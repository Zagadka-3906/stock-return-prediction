"""Measure four inference paths with20 frozen actual HGBs; no fits or scoring."""
from pathlib import Path
import gc
import hashlib
import os
import sys
import time
for key in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','POLARS_MAX_THREADS'):
    os.environ[key]='4'
ROOT=Path(__file__).resolve().parents[1]
A=ROOT/'analysis'
sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from atomic_optimization_observer_writes_20261005 import write

def bits(x):
    import numpy as np
    return np.ascontiguousarray(x).view('u8')

def main():
    import numpy as np
    import polars as pl
    import psutil
    import joblib
    from threadpoolctl import threadpool_limits
    import quantile_HGB_cpu_codec_v2_20261007 as old
    import quantile_HGB_large_batch_codec_20261007 as new
    from direct_flag_centered_rank_CDF_transform_20261007 import prepare
    from run import fold_cutoff
    from win32_read_handle_hash_cache_with_filename_v2_20261006 import LockedReadHashCache
    out=A/'quantile_HGB_large_batch20_benchmark_20261007'
    assert not out.exists();out.mkdir()
    bank=A/'quantile_HGB_native_bank20_v2_20261007'
    proof=read(bank/'verification.json')
    assert proof['status']=='passed_actual20_CPU_quantile_HGB_native_independent_numpy_and_prefix_controls'
    assert proof['actual_native_fits']==20
    service=A/'service_owned_workflows_20261006/quantile_HGB_native_bank20_training_v2'
    assert not owned(read(service/'native_launch.json'))
    assert read(service/'service_execution.json')['status']=='passed'
    while psutil.virtual_memory().available < 9*2**30:
        write(out/'actual_stage.json',{'status':'waiting9GiB_RAM_before_diagnostic_only','new_fits':0,'new_scores':0})
        time.sleep(15)
    sources=[Path(__file__),A/'quantile_HGB_cpu_codec_v2_20261007.py',A/'cpu_conditional_residual_mlp_codec_20261007.py',A/'quantile_HGB_large_batch_codec_20261007.py',bank/'verification.json',A/'direct_flag_centered_rank_CDF_transform_20261007.py',ROOT/'run.py',ROOT/'后续选模标准.md',ROOT/'data/features.parquet',ROOT/'data/feature_manifest.json',A/'connected_validation_20261002/combined_fold_frame.parquet',A/'conditional_flag_rank_bank_v2_20261006/flagged_validation_features.parquet',A/'optimization_20261003_r106/selected_validation.npy']
    for model in proof['actual_models']:
        sources += [Path(model['native_model_path']),Path(model['independent_hist_tree_state_path']),bank/model['name']/f"info_{model['year']}.json"]
    sources += [bank/n/'flagged_oof_predictions.npy' for n in proof['configurations']]
    pins={str(p.resolve()):sha(p) for p in sources}
    create(out/'frozen_before_actual_benchmark.json',{'input_sha256':pins,'actual_existing_models':20,'orders':[['native256','native8192','decoder256','decoder8192'],['decoder8192','decoder256','native8192','native256']],'threads_each_path':4,'training_only_inputs':True,'new_fits':0,'new_quality_scores':0,'test_labels_read':False})
    started=time.perf_counter();records=[];totals={k:[] for k in ('native256','native8192','decoder256','decoder8192')}
    with LockedReadHashCache(pins) as scope, threadpool_limits(limits=4):
        features=read(ROOT/'data/feature_manifest.json')['features']
        frame=pl.read_parquet(A/'connected_validation_20261002/combined_fold_frame.parquet',columns=['ts_code','trade_date','flag_limit_up','price_valid'])
        assert len(frame)==5635800
        keyed=pl.read_parquet(A/'conditional_flag_rank_bank_v2_20261006/flagged_validation_features.parquet')
        assert len(keyed)==86968
        assert keyed.select('ts_code','trade_date').equals(frame.filter(pl.col('flag_limit_up')==1).select('ts_code','trade_date'))
        raw=np.load(A/'optimization_20261003_r106/selected_validation.npy',mmap_mode='r')
        dates,flags,valid=(frame[k].to_numpy() for k in ('trade_date','flag_limit_up','price_valid'))
        pct=np.zeros(len(frame),dtype=np.float64)
        for _,pos,percentile,_,_ in prepare(raw,dates,flags,valid,'all_current_raw_forecasts'):
            pct[pos]=percentile
        positions=keyed['oof_position'].to_numpy();kd=keyed['trade_date'].to_numpy()
        x=np.column_stack([keyed.select(features).to_numpy(),pct[positions]]).astype(np.float64)
        truth=pl.scan_parquet(ROOT/'data/features.parquet').filter(pl.col('is_train')&(pl.col('flag_limit_up')==1)).select('ts_code','trade_date','y_rank').collect()
        joined=keyed.select('ts_code','trade_date').join(truth,on=['ts_code','trade_date'],how='left',validate='1:1',maintain_order='left')
        finite=np.isfinite(joined['y_rank'].to_numpy())&valid[positions]
        del frame,raw,pct,truth,joined;gc.collect()
        for rep in range(2):
            aggregate={k:0. for k in totals}
            order=list(totals) if rep==0 else list(reversed(totals))
            for item in proof['actual_models']:
                name,year=item['name'],item['year']
                selected=kd//10000==year
                if year<2025:
                    test=x[selected]
                    original=np.load(bank/name/'flagged_oof_predictions.npy',mmap_mode='r')[positions[selected]]
                else:
                    test=x[(kd<fold_cutoff(2025))&finite][:1000]
                    original=None
                bundle=joblib.load(item['native_model_path']);state=read(item['independent_hist_tree_state_path'])
                calls={'native256':lambda:old.predict_native(bundle,test),'native8192':lambda:new.predict_native(bundle,test),'decoder256':lambda:old.predict_decoded(state,test),'decoder8192':lambda:new.predict_decoded(state,test)}
                results={};timings={}
                write(out/'actual_stage.json',{'status':'actual_alternating_saved_HGB_inference_benchmark','model':name,'year':year,'repeat':rep,'completed_model_repeats':len(records),'new_fits':0,'new_scores':0})
                for method in order:
                    t=time.perf_counter();results[method]=calls[method]();timings[method]=time.perf_counter()-t;aggregate[method]+=timings[method]
                expected=results['native256']
                if original is not None: assert np.array_equal(bits(expected),bits(original))
                assert all(np.array_equal(bits(expected),bits(v)) for v in results.values())
                counts=sorted(set([0,1,79,256,511,len(test)]))
                counts=[n for n in counts if n<=len(test)]
                if rep==0:
                    for count in counts:
                        assert np.array_equal(bits(expected[:count]),bits(new.predict_native(bundle,test[:count])))
                        assert np.array_equal(bits(expected[:count]),bits(new.predict_decoded(state,test[:count])))
                records.append({'name':name,'year':year,'repeat':rep,'rows':len(test),'order':order,'timings':timings,'all_four_paths_uint64_bits_exact':True,'original_saved_annual_OOF_bits_exact':original is not None,'actual_new_runtime_prefix_counts':counts if rep==0 else [],'prediction_numeric_sha256':hashlib.sha256(memoryview(np.ascontiguousarray(expected)).cast('B')).hexdigest()})
                del bundle,state,results,test,original;gc.collect()
            for method in totals:totals[method].append(aggregate[method])
        assert len(records)==40
        medians={k:float(np.median(v)) for k,v in totals.items()}
        scope.reverify()
        create(out/'verification.json',{'status':'passed_actual20_saved_HGB_two_alternating_inference_repeats_all_bits_and_prefix_controls','at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'input_sha256':pins,'actual_existing_native_models_tested':20,'actual_model_repeat_count':40,'records':records,'aggregate_seconds_per_repeat':totals,'median_aggregate_seconds':medians,'native_phase_speedup':medians['native256']/medians['native8192'],'independent_decoder_phase_speedup':medians['decoder256']/medians['decoder8192'],'elapsed_seconds_including_setup_and_controls':time.perf_counter()-started,'official_scores_unchanged_and_not_recomputed':True,'selected_future_wrapper_not_yet_adopted':True,'model_or_target_math_unchanged':True,'new_fits':0,'new_quality_scores':0,'full1599600_future_or_whole_goal_speedup_not_claimed':True,'test_labels_read':False})
if __name__=='__main__':main()
