"""Ten expanding mature nonflag residual HGB fits with bounded feature and replay memory."""
from pathlib import Path
import sys,os,time,gc,hashlib
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis'
sys.path[:0]=[str(ROOT),str(A)]
for k in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','POLARS_MAX_THREADS'):os.environ[k]='4'
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from atomic_optimization_observer_writes_20261005 import write
def numeric_sha(x):
    import numpy as np
    return hashlib.sha256(memoryview(np.ascontiguousarray(x)).cast('B')).hexdigest()
def main():
    import numpy as np,polars as pl,psutil,joblib
    from sklearn.ensemble import HistGradientBoostingRegressor
    from threadpoolctl import threadpool_limits
    from run import fold_cutoff
    import cpu_numerical_HGB_large_batch_codec_v2_20261007 as codec
    from cpu_conditional_residual_hgb_codec_20261007 import predict_native as native256
    from nonflag_residual_HGB_preprocessing_20261007 import fit_preprocessing,prepare
    from exact_numpy_all_forecast_percentiles_20261007 import AllForecastPercentiles
    from win32_read_handle_hash_cache_with_filename_v2_20261006 import LockedReadHashCache
    codec.prepare=prepare
    f=A/'service_owned_workflows_20261006/nonflag_residual_HGB_codec2_preflight'
    while owned(read(f/'native_launch.json')):time.sleep(10)
    assert read(f/'service_execution.json')['status']=='passed'
    diagnostic=A/'nonflag_residual_HGB_codec2_preflight_20261007/verification.json'
    assert read(diagnostic)['status']=='passed_actual2_nonflag_residual_HGB_historical_codec_controls'
    admitted=A/'nonflag_residual_HGB10_source_admission_20261007.json';proof=read(admitted)
    assert proof['status']=='passed_actual2_codec_controls_and10_mature_nonflag_fit_source_admission'
    for p,d in proof['input_sha256'].items():assert sha(p)==d,p
    plan_path=A/'nonflag_residual_HGB10_plan_20261007.json';plan=read(plan_path)
    out=A/'nonflag_residual_HGB_bank10_20261007';assert not out.exists();out.mkdir()
    cache=Path('E:/赛题五_本机临时/nonflag_residual_HGB10_20261007').resolve()
    assert cache.is_relative_to(Path('E:/赛题五_本机临时').resolve()) and not cache.exists();cache.mkdir(parents=True)
    while psutil.virtual_memory().available<10*2**30:time.sleep(10)
    frame_path=A/'connected_validation_20261002/combined_fold_frame.parquet';reference_path=A/'optimization_20261003_r106/selected_validation.npy'
    paths=[Path(__file__),plan_path,diagnostic,admitted,A/'nonflag_residual_HGB_preprocessing_20261007.py',
      A/'cpu_numerical_HGB_large_batch_codec_v2_20261007.py',A/'cpu_conditional_residual_hgb_codec_20261007.py',
      A/'memory_bounded_numeric_preparation_20261007.py',A/'exact_numpy_all_forecast_percentiles_20261007.py',
      A/'all_forecast_percentiles_full_scoring_benchmark_20261007/verification.json',ROOT/'run.py',ROOT/'src/features.py',
      ROOT/'data/features.parquet',ROOT/'data/feature_manifest.json',ROOT/'后续选模标准.md',frame_path,reference_path,
      A/'optimization_20261003_r106/selection.json',A/'github_validation_sync_main_20261005/round106_receipt.json']
    pins={str(p):sha(p) for p in paths};create(out/'frozen_before_actual_training.json',{'input_sha256':pins,'plan':plan,'actual_declared_native_fits':10,'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'test_labels_read':False})
    records=[];started=time.perf_counter()
    with LockedReadHashCache(pins) as scope,threadpool_limits(limits=4):
        features=read(ROOT/'data/feature_manifest.json')['features'];assert len(features)==63
        full=pl.read_parquet(frame_path,columns=['ts_code','trade_date','flag_limit_up','price_valid']).with_row_index('oof_position')
        assert (len(full),full['trade_date'].n_unique(),full['ts_code'].n_unique())==(5635800,1212,4650)
        reference=np.load(reference_path,mmap_mode='r')
        def unsupported(*args):raise AssertionError('Current teacher percentile fast path unexpectedly unsupported')
        teacher=AllForecastPercentiles(unsupported)(full,reference)
        keys=full.filter(pl.col('flag_limit_up')!=1).select('ts_code','trade_date','oof_position','price_valid')
        positions=keys['oof_position'].to_numpy();kd=keys['trade_date'].to_numpy();valid=keys['price_valid'].to_numpy()
        raw_path=cache/'all_nonflag_features64.npy';raw=np.lib.format.open_memmap(raw_path,mode='w+',dtype=np.float64,shape=(len(keys),64))
        lazy=pl.scan_parquet(ROOT/'data/features.parquet').filter(pl.col('is_train')&(pl.col('trade_date')>=20200101))
        key_only=keys.select('ts_code','trade_date')
        for left in range(0,63,8):
            block_names=features[left:left+8]
            block=lazy.select('ts_code','trade_date',*block_names).collect()
            joined=key_only.join(block,on=['ts_code','trade_date'],how='left',validate='1:1',maintain_order='left');assert len(joined)==len(keys)
            raw[:,left:left+len(block_names)]=joined.select(block_names).to_numpy();raw.flush()
            del block,joined;gc.collect()
            write(out/'actual_stage.json',{'status':'bounded_nonflag_feature_cache','completed_feature_columns':left+len(block_names),'expected':64,'native_fits':0})
        raw[:,63]=teacher[positions];raw.flush()
        labels=key_only.join(lazy.select('ts_code','trade_date','y_rank').collect(),on=['ts_code','trade_date'],how='left',validate='1:1',maintain_order='left')
        y=labels['y_rank'].to_numpy().astype(np.float64)+.5-teacher[positions]
        eligible=np.isfinite(y)&valid;del labels,teacher,key_only;gc.collect()
        all_days=pl.scan_parquet(ROOT/'data/features.parquet').filter(pl.col('is_train')).select('trade_date').unique().sort('trade_date').collect()['trade_date'].to_numpy()
        oof_days=full['trade_date'].unique().sort().to_numpy()
        create(out/'actual_teacher_target_and_key_alignment.json',{'status':'passed_actual_nonflag_keys_and_mature_residual_target','nonflag_rows':len(keys),
          'target_numeric_sha256':numeric_sha(y),'teacher_feature_numeric_sha256':numeric_sha(np.asarray(raw[:,63])),
          'feature_cache':str(raw_path),'feature_cache_sha256':sha(raw_path),'only_current_X_teacher_and_train_label_target':True,'test_labels_read':False})
        feature_names=[*features,'qualified106_current_forecast_average_rank_over_N']
        outputs={}
        for name in plan['configurations']:
            (out/name).mkdir();outputs[name]=np.lib.format.open_memmap(out/name/'nonflag_oof_predictions.npy',mode='w+',dtype=np.float64,shape=(len(full),));outputs[name][:]=0.;outputs[name].flush()
        for year in plan['native_fit_years']:
            cutoff=fold_cutoff(year);train=(kd<cutoff)&eligible;indices=np.flatnonzero(train)
            assert len(indices)>300 and kd[indices].min()>=20200101
            last=int(kd[indices].max());label_end=int(all_days[np.searchsorted(all_days,last)+1]);assert last<cutoff and label_end<=cutoff
            while psutil.virtual_memory().available<9*2**30:time.sleep(10)
            window_path=cache/f'mature_training_features64_{year}.npy'
            window=np.lib.format.open_memmap(window_path,mode='w+',dtype=np.float64,shape=(len(indices),64))
            for left in range(0,len(indices),8192):window[left:left+8192]=raw[indices[left:left+8192]]
            window.flush();prep=fit_preprocessing(window);bx=prepare(window,prep);train_y=y[train]
            training_matrix_hash=numeric_sha(bx);target_hash=numeric_sha(train_y)
            selected=kd//10000==year;test=np.asarray(raw[selected]) if year<2025 else np.asarray(window[:1000]).copy()
            for name,cfg in plan['configurations'].items():
                write(out/'actual_stage.json',{'status':'actual_nonflag_HGB_training','model':name,'year':year,'training_rows':len(indices),'actual_completed_native_fits':len(records),'expected_fits':10,'available_RAM_GiB':psutil.virtual_memory().available/2**30})
                params={**plan['fixed_parameters'],**cfg};t=time.perf_counter();model=HistGradientBoostingRegressor(**params).fit(bx,train_y);fit_seconds=time.perf_counter()-t
                assert model.n_iter_==96
                native=out/name/f'model_{year}.joblib';state_path=out/name/f'independent_hist_tree_state_{year}.json'
                bundle={'model':model,'preprocessing':prep,'features':feature_names};joblib.dump(bundle,native);create(state_path,codec.export(model,prep,feature_names))
                saved=joblib.load(native);state=read(state_path);actual=np.empty(len(test),dtype=np.float64)
                for left in range(0,len(test),65536):
                    block=test[left:left+65536];value=codec.predict_native(bundle,block)
                    replay=codec.predict_native(saved,block);original=native256(saved,block);decoded=codec.predict_decoded(state,block)
                    assert all(np.array_equal(value.view('u8'),v.view('u8')) for v in (replay,original,decoded));actual[left:left+len(block)]=value
                controls=[]
                if year<2025:
                    outputs[name][positions[selected]]=actual;outputs[name].flush()
                    for count in (80,260,975):
                        n=int(np.count_nonzero(kd[selected]<=oof_days[count-1]))
                        for left in range(0,n,65536):
                            right=min(n,left+65536);cold=codec.predict_native(saved,test[left:right]);dec=codec.predict_decoded(state,test[left:right])
                            assert np.array_equal(cold.view('u8'),actual[left:right].view('u8')) and np.array_equal(cold.view('u8'),dec.view('u8'))
                        controls.append({'days':count,'actual_nonflag_rows':n,'native_and_independent_prefix_bits_exact':True})
                item={'name':name,'year':year,'parameters':params,'features':feature_names,'training_rows':len(indices),'last_training_label_date':last,'last_training_label_end':label_end,
                  'exclusive_cutoff':cutoff,'training_matrix_numeric_sha256':training_matrix_hash,'training_target_numeric_sha256':target_hash,
                  'actual_iterations':model.n_iter_,'fit_seconds':fit_seconds,'native_model_path':str(native),'native_model_sha256':sha(native),
                  'independent_hist_tree_state_path':str(state_path),'independent_hist_tree_state_sha256':sha(state_path),'prediction_control_rows':len(test),
                  'outer_control_batch65536_multiple_of_native256_and8192':True,'native256_8192_reload_independent_all_prediction_bits_exact':True,'actual_cold_prefix_controls':controls,
                  'training_population_nonflag_past_OOF_only':True,'new_native_fits':1,'test_labels_read':False}
                create(out/name/f'info_{year}.json',item);records.append(item);print({'model':name,'year':year,'fits':len(records),'fit_seconds':fit_seconds},flush=True)
                del model,bundle,saved,state,actual;gc.collect()
            del bx,window,train_y,test,indices;gc.collect()
        for name,array in outputs.items():
            assert np.all(array[full['flag_limit_up'].to_numpy()==1]==0.) and np.all(array[full['trade_date'].to_numpy()<20210101]==0.) and np.isfinite(array).all()
            array.flush();create(out/name/'oof_verification.json',{'status':'passed_actual5635800_nonflag_residual_OOF','rows':len(array),'prediction_array_sha256':sha(out/name/'nonflag_oof_predictions.npy'),'flagged_and2020_identity_zero_residual':True,'test_labels_read':False})
        assert len(records)==10;scope.reverify()
        create(out/'verification.json',{'status':'passed_actual10_nonflag_residual_HGB_mature_native_reload_independent_and_prefix_controls','at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),
          'input_sha256':pins,'configurations':plan['configurations'],'actual_models':records,'actual_native_fits':10,'elapsed_seconds':time.perf_counter()-started,
          'feature_cache_and_mature_window_cache_root':str(cache),'actual_official_scores':0,'future_candidate_and_round120_full_qualification_not_claimed':True,'test_labels_read':False})
if __name__=='__main__':main()
