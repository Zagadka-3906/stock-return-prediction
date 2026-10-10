"""Two real historical diagnostic fits for the nonflag model recipe and codecs."""
from pathlib import Path
import sys,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis'
sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
def main():
    import numpy as np,polars as pl,joblib
    from sklearn.ensemble import HistGradientBoostingRegressor
    from threadpoolctl import threadpool_limits
    from run import fold_cutoff
    import cpu_numerical_HGB_large_batch_codec_v2_20261007 as codec
    from cpu_conditional_residual_hgb_codec_20261007 import predict_native as native256
    from nonflag_residual_HGB_preprocessing_20261007 import fit_preprocessing,prepare
    from win32_read_handle_hash_cache_with_filename_v2_20261006 import LockedReadHashCache
    codec.prepare=prepare
    out=A/'nonflag_residual_HGB_codec2_preflight_20261007';assert not out.exists();out.mkdir()
    plan_path=A/'nonflag_residual_HGB10_plan_20261007.json';plan=read(plan_path)
    paths=[Path(__file__),plan_path,A/'nonflag_residual_HGB_preprocessing_20261007.py',A/'cpu_numerical_HGB_large_batch_codec_v2_20261007.py',
      A/'cpu_conditional_residual_hgb_codec_20261007.py',A/'memory_bounded_numeric_preparation_20261007.py',ROOT/'data/features.parquet',ROOT/'data/feature_manifest.json',ROOT/'run.py']
    pins={str(p):sha(p) for p in paths};create(out/'frozen_before_actual_controls.json',{'input_sha256':pins,'actual_diagnostic_fits_expected':2,'actual_selection_fits':0})
    with LockedReadHashCache(pins) as scope,threadpool_limits(limits=4):
        names=read(ROOT/'data/feature_manifest.json')['features'];assert len(names)==63
        f=pl.scan_parquet(ROOT/'data/features.parquet').filter(pl.col('is_train')&(pl.col('flag_limit_up')!=1)&(pl.col('trade_date')<fold_cutoff(2021))&pl.col('y_rank').is_finite()).sort('trade_date','ts_code').select(*names,'trade_date','y_rank').head(601).collect()
        assert len(f)==601 and f['trade_date'].max()<fold_cutoff(2021)
        x=np.column_stack([f.select(names).to_numpy(),np.zeros(len(f))]).astype(float);y=f['y_rank'].to_numpy().astype(float)
        prep=fit_preprocessing(x[:512]);records=[]
        for name,cfg in plan['configurations'].items():
            params={**plan['fixed_parameters'],**cfg,'max_iter':3,'min_samples_leaf':16}
            model=HistGradientBoostingRegressor(**params).fit(prepare(x[:512],prep),y[:512]);assert model.n_iter_==3
            bundle={'model':model,'preprocessing':prep,'features':[*names,'zero_diagnostic_teacher']}
            native=out/(name+'.joblib');joblib.dump(bundle,native);state=out/(name+'.json');create(state,codec.export(model,prep,bundle['features']))
            expected=native256(bundle,x);actual=codec.predict_native(joblib.load(native),x);decoded=codec.predict_decoded(read(state),x)
            assert np.array_equal(expected.view('u8'),actual.view('u8')) and np.array_equal(expected.view('u8'),decoded.view('u8'))
            for n in (0,1,79,256,511,601):
                assert np.array_equal(actual[:n].view('u8'),codec.predict_native(bundle,x[:n]).view('u8'))
                assert np.array_equal(actual[:n].view('u8'),codec.predict_decoded(read(state),x[:n]).view('u8'))
            records.append({'name':name,'training_rows':512,'prediction_rows':601,'actual_iterations':3,'native256_8192_reload_independent_and_all_prefix_bits_exact':True,'native_sha256':sha(native),'state_sha256':sha(state)})
        scope.reverify()
    create(out/'verification.json',{'status':'passed_actual2_nonflag_residual_HGB_historical_codec_controls','at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),
      'input_sha256':pins,'records':records,'actual_diagnostic_fits':2,'actual_selection_fits':0,'actual_official_scores':0,'test_labels_read':False})
    print({'status':'passed','actual_diagnostic_fits':2},flush=True)
if __name__=='__main__':main()
