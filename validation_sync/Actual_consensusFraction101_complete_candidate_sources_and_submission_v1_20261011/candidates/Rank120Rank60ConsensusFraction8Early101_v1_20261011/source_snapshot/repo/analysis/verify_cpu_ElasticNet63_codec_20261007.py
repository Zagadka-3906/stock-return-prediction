"""Four actual63-feature historical HGB controls, no selection scores."""
from pathlib import Path
import os
import sys
import time
for key in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','POLARS_MAX_THREADS'):os.environ[key]='4'
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis'
sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create

def main():
    import numpy as np
    import polars as pl
    import joblib
    from sklearn.linear_model import ElasticNet
    import warnings
    from threadpoolctl import threadpool_limits
    from run import fold_cutoff
    import cpu_ElasticNet_independent_linear_codec_20261007 as new
    from win32_read_handle_hash_cache_with_filename_v2_20261006 import LockedReadHashCache
    out=A/'cpu_ElasticNet63_codec_preflight_20261007';assert not out.exists();out.mkdir()
    sources=[Path(__file__),A/'cpu_full_universe_ElasticNet_bank24_plan_20261007.json',A/'cpu_ElasticNet_independent_linear_codec_20261007.py',A/'cpu_conditional_residual_mlp_codec_20261007.py',ROOT/'run.py',ROOT/'data/features.parquet',ROOT/'data/feature_manifest.json',ROOT/'后续选模标准.md']
    pins={str(p.resolve()):sha(p) for p in sources};create(out/'frozen_before_actual_controls.json',{'input_sha256':pins,'diagnostic_only':True,'actual_declared_diagnostic_fits':4,'official_scores':0,'test_labels_read':False})
    with LockedReadHashCache(pins) as scope,threadpool_limits(limits=4):
        features=read(ROOT/'data/feature_manifest.json')['features'];assert len(features)==63
        plan=read(A/'cpu_full_universe_ElasticNet_bank24_plan_20261007.json');cut=fold_cutoff(2020)
        lazy=pl.scan_parquet(ROOT/'data/features.parquet')
        records=[]
        for name,cfg in plan['configurations'].items():
            target=cfg['target'];columns=list(dict.fromkeys(['trade_date','ts_code',*features,target,'is_train','price_valid']))
            frame=lazy.filter(pl.col('is_train')&(pl.col('trade_date')<cut)&pl.col('price_valid')&pl.col(target).is_finite()).select(columns).sort('trade_date','ts_code').head(1113).collect()
            assert len(frame)==1113 and frame['trade_date'].max()<cut
            following=lazy.filter(pl.col('is_train')&(pl.col('trade_date')>=cut)).select(columns).head(10).collect()
            sample=pl.concat([frame,following]);poison=sample.with_columns(pl.when(pl.col('trade_date')>=cut).then(pl.lit(12345.)).otherwise(pl.col(target)).cast(sample.schema[target]).alias(target))
            mask=pl.col('is_train')&(pl.col('trade_date')<cut)&pl.col('price_valid')&pl.col(target).is_finite()
            assert sample.filter(mask).equals(poison.filter(mask))
            negative=sample.with_columns(pl.when(pl.col('trade_date')<cut).then(pl.col(target)+1.).otherwise(pl.col(target)).cast(sample.schema[target]).alias(target))
            assert not sample.filter(mask).select(target).equals(negative.filter(mask).select(target))
            x=frame.select(features).to_numpy().astype(np.float64);y=frame[target].to_numpy().astype(np.float64)
            prep=new.fit_preprocessing(x[:512]);bounds=None;fit_y=y[:512]
            if target=='y_ret_1d':
                bounds=np.quantile(fit_y,[.005,.995]);fit_y=np.clip(fit_y,*bounds)
            scaling=new.target_scale(fit_y)
            params={**plan['fixed_parameters'],'alpha':cfg['alpha']}
            with warnings.catch_warnings(record=True) as actual_warnings:
                warnings.simplefilter('always');model=ElasticNet(**params).fit(np.asfortranarray(new.prepare(x[:512],prep)),(fit_y-scaling['center'])/scaling['scale'])
            bundle={'model':model,'preprocessing':prep,'features':features,'target_scaling':scaling}
            native=out/(name+'.joblib');joblib.dump(bundle,native)
            state=out/(name+'.json');create(state,new.export(bundle))
            saved=joblib.load(native);decoded=read(state);test=x[512:];actual=new.predict_native(bundle,test)
            assert np.array_equal(actual.view('u8'),new.predict_native(saved,test).view('u8'))
            assert np.array_equal(actual.view('u8'),new.predict_decoded(decoded,test).view('u8'))
            for count in (0,1,79,256,511,601):
                assert np.array_equal(actual[:count].view('u8'),new.predict_native(saved,test[:count]).view('u8'))
                assert np.array_equal(actual[:count].view('u8'),new.predict_decoded(decoded,test[:count]).view('u8'))
            repeated=np.tile(test,(28,1))[:16389];full=new.predict_native(saved,repeated)
            assert np.array_equal(full.view('u8'),new.predict_decoded(decoded,repeated).view('u8'))
            for count in (8191,8192,8193,16389):
                assert np.array_equal(full[:count].view('u8'),new.predict_native(saved,repeated[:count]).view('u8'))
                assert np.array_equal(full[:count].view('u8'),new.predict_decoded(decoded,repeated[:count]).view('u8'))
            records.append({'name':name,'target':target,'features':features,'training_rows':512,'actual_historical_prediction_rows':601,'additional_repeated_historical_matrix_prediction_rows':16389,'native_parameters':params,'native_iterations':int(model.n_iter_),'native_dual_gap':float(model.dual_gap_),'actual_nonzero_coefficients':int(np.count_nonzero(model.coef_)),'actual_warnings':[str(w.message) for w in actual_warnings],'target_scaling_own_training_only':scaling,'return_bounds_own_training_only':bounds.tolist() if bounds is not None else None,'exclusive_cutoff':cut,'last_training_label_date':int(frame['trade_date'][:512].max()),'future_label_poisoning_mask_identical_and_past_negative_control_detected':True,'native_reload_independent_dense_decoder_bits_exact':True,'prefix_counts':[0,1,79,256,511,601,8191,8192,8193,16389],'native_sha256':sha(native),'independent_state_sha256':sha(state),'test_labels_read':False})
        scope.reverify();create(out/'verification.json',{'status':'passed_actual_four_ElasticNet63_native_target_units_decoder_batch_boundary_and_maturity_controls','at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'input_sha256':pins,'records':records,'actual_diagnostic_fits':4,'actual_selection_fits':0,'actual_official_scores':0,'test_labels_read':False})
if __name__=='__main__':main()
