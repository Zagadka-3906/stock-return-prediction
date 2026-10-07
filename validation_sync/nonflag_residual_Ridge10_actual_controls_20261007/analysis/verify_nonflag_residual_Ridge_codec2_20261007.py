"""Real past-only diagnostic fits before admitting ten linear residual models."""
from pathlib import Path
import os, sys, time
ROOT=Path(__file__).resolve().parents[1]; A=ROOT/'analysis'
sys.path[:0]=[str(ROOT),str(A)]
for k in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','POLARS_MAX_THREADS'): os.environ[k]='2'
from run_dependency_queue_v3_20261006 import read,sha,create

def main():
    import numpy as np, polars as pl, joblib
    from sklearn.linear_model import Ridge
    from threadpoolctl import threadpool_limits
    from run import fold_cutoff
    from nonflag_residual_HGB_preprocessing_20261007 import fit_preprocessing,prepare
    from nonflag_residual_Ridge_codec_20261007 import export,predict_native,predict_decoded
    from win32_read_handle_hash_cache_with_filename_v2_20261006 import LockedReadHashCache
    out=A/'nonflag_residual_Ridge_codec2_preflight_20261007'; assert not out.exists(); out.mkdir()
    plan_path=A/'nonflag_residual_Ridge10_plan_20261007.json'; plan=read(plan_path)
    paths=[Path(__file__),plan_path,A/'nonflag_residual_Ridge_codec_20261007.py',
           A/'nonflag_residual_HGB_preprocessing_20261007.py',A/'memory_bounded_numeric_preparation_20261007.py',
           A/'cpu_conditional_residual_mlp_codec_20261007.py',ROOT/'run.py',ROOT/'data/features.parquet',
           ROOT/'data/feature_manifest.json',ROOT/'后续选模标准.md']
    pins={str(p):sha(p) for p in paths}
    create(out/'frozen_before_actual_controls.json',{'input_sha256':pins,'actual_diagnostic_fits_expected':2,'actual_official_scores':0})
    with LockedReadHashCache(pins) as scope,threadpool_limits(limits=2):
        names=read(ROOT/'data/feature_manifest.json')['features']; assert len(names)==63
        f=pl.scan_parquet(ROOT/'data/features.parquet').filter(pl.col('is_train')&(pl.col('flag_limit_up')!=1)&(pl.col('trade_date')<fold_cutoff(2021))&pl.col('y_rank').is_finite()).sort('trade_date','ts_code').select(*names,'trade_date','y_rank').head(975).collect()
        assert len(f)==975 and f['trade_date'].max()<fold_cutoff(2021)
        x=np.column_stack([f.select(names).to_numpy(),np.zeros(len(f))]).astype(float)
        y=f['y_rank'].to_numpy().astype(float)+.5
        prep=fit_preprocessing(x[:512]); records=[]
        # These small diagnostics use an explicit zero teacher, not selection predictions.
        for name,cfg in plan['configurations'].items():
            params={**plan['fixed_parameters'],'alpha':512*cfg['alpha_per_training_row']}
            model=Ridge(**params).fit(prepare(x[:512],prep),y[:512])
            bundle={'model':model,'preprocessing':prep,'features':[*names,'zero_diagnostic_teacher']}
            native=out/(name+'.joblib'); state_path=out/(name+'.json')
            joblib.dump(bundle,native); create(state_path,export(bundle))
            actual=predict_native(bundle,x)
            for n in (0,1,79,256,511,601,975):
                cold=predict_native(joblib.load(native),x[:n]); decoded=predict_decoded(read(state_path),x[:n])
                assert np.array_equal(actual[:n].view('u8'),cold.view('u8'))
                assert np.array_equal(cold.view('u8'),decoded.view('u8'))
            records.append({'name':name,'training_rows':512,'prediction_rows':975,'parameters':params,
                'native_reload_independent_and_all_prefix_bits_exact':True,'native_sha256':sha(native),'state_sha256':sha(state_path)})
        scope.reverify()
    create(out/'verification.json',{'status':'passed_actual2_nonflag_residual_Ridge_historical_codec_controls',
        'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'input_sha256':pins,'records':records,
        'actual_diagnostic_fits':2,'actual_selection_fits':0,'actual_official_scores':0,'test_labels_read':False})
    print({'status':'passed','actual_diagnostic_fits':2},flush=True)
if __name__=='__main__': main()
