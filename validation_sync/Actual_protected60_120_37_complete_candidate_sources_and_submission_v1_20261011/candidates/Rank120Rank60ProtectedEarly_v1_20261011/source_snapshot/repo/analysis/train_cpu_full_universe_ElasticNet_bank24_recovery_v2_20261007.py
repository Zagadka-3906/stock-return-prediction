"""Full universe24 CPU ElasticNet mature-fold native fits with full exact replay controls."""
from pathlib import Path
import gc
import hashlib
import os
import sys
import time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis'
sys.path[:0]=[str(ROOT),str(A)]
for key in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','POLARS_MAX_THREADS'):os.environ[key]='2'
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from atomic_optimization_observer_writes_20261005 import write

def numeric_sha(x):
    import numpy as np
    return hashlib.sha256(memoryview(np.ascontiguousarray(x)).cast('B')).hexdigest()

def await_closed(name):
    folder=A/'service_owned_workflows_20261006'/name
    while not (folder/'native_launch.json').exists() or owned(read(folder/'native_launch.json')):time.sleep(15)
    assert read(folder/'service_execution.json')['status']=='passed',name

def main():
    import psutil
    out=A/'cpu_full_universe_ElasticNet_bank24_recovery_v2_20261007';assert not out.exists();out.mkdir()
    await_closed('CPU_FULL_HGB44_round113_full_registration_v3')
    assert read(A/'optimization_20261003_r113/full_registration_execution.json')['status']=='passed'
    assert read(A/'github_validation_sync_main_20261005/round113_receipt.json')['actual_full_QA_version']==24
    await_closed('cpu_ElasticNet63_codec_preflight')
    await_closed('ElasticNet_memory_preprocessing_preflight')
    assert read(A/'ElasticNet_memory_preprocessing_preflight_20261007/verification.json')['status']=='passed_actual_historical63_column_statistics_and_native_training_layout_controls'
    diagnostic=A/'cpu_ElasticNet63_codec_preflight_20261007/verification.json'
    assert read(diagnostic)['status']=='passed_actual_four_ElasticNet63_native_target_units_decoder_batch_boundary_and_maturity_controls'
    while psutil.virtual_memory().available<12*2**30:time.sleep(15)
    import numpy as np
    import polars as pl
    import joblib
    import sklearn
    from sklearn.linear_model import ElasticNet
    import warnings
    from threadpoolctl import threadpool_limits
    from run import fold_cutoff
    import cpu_ElasticNet_independent_linear_codec_20261007 as new
    from ElasticNet_memory_bounded_preprocessing_20261007 import fit_preprocessing,prepare_training_fortran
    from win32_read_handle_hash_cache_with_filename_v2_20261006 import LockedReadHashCache
    plan_path=A/'cpu_full_universe_ElasticNet_bank24_plan_20261007.json';plan=read(plan_path)
    features=read(ROOT/'data/feature_manifest.json')['features'];assert len(features)==63
    sources=[Path(__file__),plan_path,A/'cpu_full_universe_ElasticNet_bank24_admission_20261007.json',diagnostic,A/'verify_cpu_ElasticNet63_codec_20261007.py',A/'ElasticNet_memory_preprocessing_preflight_20261007/verification.json',A/'ElasticNet_memory_bounded_preprocessing_20261007.py',A/'cpu_ElasticNet_independent_linear_codec_20261007.py',A/'cpu_conditional_residual_mlp_codec_20261007.py',ROOT/'run.py',ROOT/'src/features.py',ROOT/'后续选模标准.md',ROOT/'data/features.parquet',ROOT/'data/feature_manifest.json',A/'connected_validation_20261002/combined_fold_frame.parquet',A/'github_validation_sync_main_20261005/round113_receipt.json',A/'optimization_20261003_r113/full_registration_execution.json']
    pins={str(p.resolve()):sha(p) for p in sources}
    create(out/'frozen_before_actual_training.json',{'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'input_sha256':pins,'plan':plan,'features':features,'no_validation_early_stopping':True,'actual_declared_native_fits':24,'selected_future_inference_not_started':True,'test_labels_read':False})
    records=[];started=time.perf_counter()
    with LockedReadHashCache(pins) as scope,threadpool_limits(limits=2):
        lazy=pl.scan_parquet(ROOT/'data/features.parquet')
        keys=pl.read_parquet(A/'connected_validation_20261002/combined_fold_frame.parquet',columns=['ts_code','trade_date']).with_row_index('oof_position')
        assert (len(keys),keys['trade_date'].n_unique(),keys['ts_code'].n_unique())==(5635800,1212,4650)
        dates=keys['trade_date'].to_numpy();oof_days=keys['trade_date'].unique().sort().to_numpy()
        all_days=lazy.filter(pl.col('is_train')).select('trade_date').unique().sort('trade_date').collect()['trade_date'].to_numpy()
        outputs={}
        for name in plan['configurations']:
            folder=out/name;folder.mkdir();outputs[name]=np.lib.format.open_memmap(folder/'raw_oof_predictions.npy',mode='w+',dtype=np.float64,shape=(len(keys),));outputs[name][:]=np.nan
        for year in plan['years']:
            cutoff=fold_cutoff(year)
            year_keys=keys.filter(pl.col('trade_date')//10000==year) if year<2025 else None
            if year<2025:
                vf=lazy.filter(pl.col('is_train')&(pl.col('trade_date')//10000==year)).select(list(dict.fromkeys(['ts_code','trade_date',*features,'price_valid']))).collect()
                vf=year_keys.join(vf,on=['ts_code','trade_date'],how='left',validate='1:1',maintain_order='left');assert len(vf)==len(year_keys)
                vx=vf.select(features).to_numpy().astype(np.float64);vd=vf['trade_date'].to_numpy();valid=vf['price_valid'].to_numpy();positions=vf['oof_position'].to_numpy();del vf;gc.collect()
            for target in ('y_rank','y_ret_1d'):
                while True:
                    state=read(A/'service_owned_dependency_queue_v4_20261006/state.json')
                    busy=any(n.startswith('round') and owned(r) for n,r in state['activated_jobs'].items())
                    if psutil.virtual_memory().available>=12*2**30 and not busy:break
                    write(out/'actual_stage.json',{'status':'waiting12GiB_RAM_and_no_original_round_writer','year':year,'target':target,'actual_verified_native_fits':len(records),'original_round_writer_live':busy,'available_RAM_GiB':psutil.virtual_memory().available/2**30,'test_labels_read':False});time.sleep(15)
                tf=lazy.filter(pl.col('is_train')&(pl.col('trade_date')<cutoff)&pl.col('price_valid')&pl.col(target).is_finite()).select(list(dict.fromkeys(['ts_code','trade_date',*features,target]))).sort('trade_date','ts_code').collect()
                tx=tf.select(features).to_numpy().astype(np.float64);ty=tf[target].to_numpy().astype(np.float64);td=tf['trade_date'].to_numpy()
                last=int(td[-1]);label_end=int(all_days[np.searchsorted(all_days,last)+1]);assert last<cutoff and label_end<=cutoff
                target_bounds=None
                if target=='y_ret_1d':target_bounds=np.quantile(ty,[.005,.995]);ty=np.clip(ty,*target_bounds)
                meta={'rows':len(tf),'target':target,'exclusive_cutoff':cutoff,'last_training_label_date':last,'last_training_label_end':label_end,'training_feature_numeric_sha256':numeric_sha(tx),'training_target_numeric_sha256':numeric_sha(ty),'training_keys_numeric_sha256':numeric_sha(tf.select('ts_code','trade_date').hash_rows(seed=20261007).to_numpy()),'return_winsor_bounds_own_past_only':target_bounds.tolist() if target_bounds is not None else None}
                del tf,td;gc.collect()
                preprocessing=fit_preprocessing(tx);bx=prepare_training_fortran(tx,preprocessing);test_final=tx[:1000].copy() if year==2025 else None
                target_scaling=new.target_scale(ty);fit_target=(ty-target_scaling['center'])/target_scaling['scale']
                del tx;gc.collect()
                for name,cfg in plan['configurations'].items():
                    if cfg['target']!=target:continue
                    params={**plan['fixed_parameters'],**{k:v for k,v in cfg.items() if k!='target'}}
                    write(out/'actual_stage.json',{'status':'actual_full_universe_CPU_ElasticNet_training','model':name,'year':year,'actual_verified_native_fits':len(records),'expected_fits':24,'training_rows':meta['rows'],'test_labels_read':False})
                    t=time.perf_counter()
                    with warnings.catch_warnings(record=True) as actual_warnings:
                        warnings.simplefilter('always');model=ElasticNet(**params).fit(bx,fit_target)
                    fit_seconds=time.perf_counter()-t
                    bundle={'model':model,'preprocessing':preprocessing,'features':features,'target':target,'target_bounds':meta['return_winsor_bounds_own_past_only'],'target_scaling':target_scaling}
                    native=out/name/f'model_{year}.joblib';joblib.dump(bundle,native)
                    independent=out/name/f'independent_linear_state_{year}.json';create(independent,new.export(bundle))
                    create(out/name/f'native_fit_completed_{year}.json',{'status':'actual_native_fit_saved_controls_pending','parameters':params,'training_metadata':meta,'fit_seconds':fit_seconds,'native_sha256':sha(native),'test_labels_read':False})
                    saved=joblib.load(native);state=read(independent);test=vx if year<2025 else test_final
                    pred=new.predict_native(bundle,test);replay=new.predict_native(saved,test);decoded=new.predict_decoded(state,test)
                    assert all(np.array_equal(pred.view('u8'),v.view('u8')) for v in (replay,decoded))
                    controls=[]
                    if year<2025:
                        for count in (80,260,975):
                            mask=vd<=oof_days[count-1]
                            cold=new.predict_native(saved,test[mask]);cold_decoded=new.predict_decoded(state,test[mask])
                            assert np.array_equal(pred[mask].view('u8'),cold.view('u8'));assert np.array_equal(cold.view('u8'),cold_decoded.view('u8'))
                            controls.append({'days':count,'actual_rows':int(mask.sum()),'native_and_independent_full_prefix_bits_exact':True})
                        pred[~valid]=-1e6;outputs[name][positions]=pred;outputs[name].flush()
                    item={'status':'passed_actual_full_native_reload_fixed8192_independent_decoder_and_prefix','name':name,'year':year,'parameters':params,'features':features,'training_metadata':meta,'fit_seconds':fit_seconds,'actual_iterations':int(model.n_iter_),'actual_dual_gap':float(model.dual_gap_),'actual_nonzero_coefficients':int(np.count_nonzero(model.coef_)),'actual_warnings':[str(w.message) for w in actual_warnings],'target_scaling_own_training_only':target_scaling,'native_model_path':str(native),'native_model_sha256':sha(native),'independent_linear_state_path':str(independent),'independent_linear_state_sha256':sha(independent),'actual_prediction_control_rows':len(test),'actual_cold_prefix_controls':controls,'native_full_reload_fixed8192_and_independent_bits_exact':True,'sklearn_version':sklearn.__version__,'CPU_threads':2,'new_native_fits':1,'test_labels_read':False}
                    create(out/name/f'info_{year}.json',item);records.append(item);print({'model':name,'year':year,'fits':len(records),'fit_seconds':fit_seconds},flush=True)
                    del model,bundle,saved,state,pred,replay,decoded;gc.collect()
                del bx,ty,fit_target,preprocessing,test_final;gc.collect()
            if year<2025:del vx,vd,valid,positions,year_keys;gc.collect()
        for name,array in outputs.items():
            assert np.isfinite(array).all();array.flush();create(out/name/'oof_verification.json',{'status':'passed_actual_full5635800_OOF_values','rows':len(array),'prediction_array_sha256':sha(out/name/'raw_oof_predictions.npy'),'all5_actual_annual_mature_models_and_final2025_saved':True,'official_quality_scoring_not_yet_executed':True,'test_labels_read':False})
        assert len(records)==24;scope.reverify();create(out/'verification.json',{'status':'passed_actual24_full_universe_CPU_ElasticNet_native_target_units_and_independent_full_prefix_controls','at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'input_sha256':pins,'actual_models':records,'actual_native_fits':24,'configurations':plan['configurations'],'features':features,'elapsed_seconds':time.perf_counter()-started,'new_official_quality_scores':0,'full_official_comparisons_selected_freeze_future_inference_and_full_board_still_required':True,'global_resource_boundary_not_claimed':True,'test_labels_read':False})
if __name__=='__main__':main()
