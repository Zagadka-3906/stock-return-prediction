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
    from sklearn.ensemble import HistGradientBoostingRegressor
    from threadpoolctl import threadpool_limits
    from run import fold_cutoff
    import cpu_conditional_residual_hgb_codec_20261007 as old
    import cpu_numerical_HGB_large_batch_codec_v2_20261007 as new
    from win32_read_handle_hash_cache_with_filename_v2_20261006 import LockedReadHashCache
    out=A/'cpu_full_universe_HGB63_codec_preflight_20261007';assert not out.exists();out.mkdir()
    sources=[Path(__file__),A/'cpu_full_universe_HGB_bank24_plan_20261007.json',A/'cpu_conditional_residual_hgb_codec_20261007.py',A/'cpu_numerical_HGB_large_batch_codec_v2_20261007.py',A/'cpu_conditional_residual_mlp_codec_20261007.py',ROOT/'run.py',ROOT/'data/features.parquet',ROOT/'data/feature_manifest.json',ROOT/'后续选模标准.md',A/'cpu_HGB_large_batch20_benchmark_20261007/verification.json']
    pins={str(p.resolve()):sha(p) for p in sources};create(out/'frozen_before_actual_controls.json',{'input_sha256':pins,'diagnostic_only':True,'actual_declared_diagnostic_fits':4,'official_scores':0,'test_labels_read':False})
    with LockedReadHashCache(pins) as scope,threadpool_limits(limits=4):
        features=read(ROOT/'data/feature_manifest.json')['features'];assert len(features)==63
        plan=read(A/'cpu_full_universe_HGB_bank24_plan_20261007.json');cut=fold_cutoff(2020)
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
            params={**plan['fixed_parameters'],**{k:v for k,v in cfg.items() if k!='target'},'max_iter':4,'min_samples_leaf':16}
            model=HistGradientBoostingRegressor(**params).fit(new.prepare(x[:512],prep),fit_y)
            native=out/(name+'.joblib');joblib.dump({'model':model,'preprocessing':prep,'features':features},native)
            state=out/(name+'.json');create(state,new.export(model,prep,features))
            saved=joblib.load(native);decoded=read(state);test=x[512:];actual=old.predict_native(saved,test)
            for values in (new.predict_native(saved,test),old.predict_decoded(decoded,test),new.predict_decoded(decoded,test)):
                assert np.array_equal(actual.view('u8'),values.view('u8'))
            for count in (0,1,79,256,511,601):
                assert np.array_equal(actual[:count].view('u8'),new.predict_native(saved,test[:count]).view('u8'))
                assert np.array_equal(actual[:count].view('u8'),new.predict_decoded(decoded,test[:count]).view('u8'))
            records.append({'name':name,'target':target,'features':features,'training_rows':512,'actual_prediction_rows':601,'diagnostic_iterations':4,'planned_actual_iterations':96,'return_bounds_own_training_only':bounds.tolist() if bounds is not None else None,'exclusive_cutoff':cut,'last_training_label_date':int(frame['trade_date'][:512].max()),'future_label_poisoning_mask_identical_and_past_negative_control_detected':True,'original256_new8192_native_and_two_independent_decoders_bits_exact':True,'prefix_counts':[0,1,79,256,511,601],'native_sha256':sha(native),'independent_state_sha256':sha(state),'test_labels_read':False})
        scope.reverify();create(out/'verification.json',{'status':'passed_actual_four_full_universe63_feature_HGB_native_codec_prefix_and_maturity_controls','at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'input_sha256':pins,'records':records,'actual_diagnostic_fits':4,'actual_selection_fits':0,'actual_official_scores':0,'test_labels_read':False})
if __name__=='__main__':main()
