"""Independent67-column ranks, uniform first-year output and learned solver checks."""
from pathlib import Path
import sys
import time
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT),str(ROOT/'analysis')]
import train_nonlinear_stacking_bank_20261004 as bank


def main():
    import numpy as np
    import polars as pl
    from scipy.stats import rankdata
    from sklearn.linear_model import Ridge
    if bank.PREFLIGHT.exists():
        proof=bank.read(bank.PREFLIGHT);assert proof['status']=='passed'
        for path,digest in proof['source_sha256'].items():assert bank.sha(path)==digest,path
        return
    rng=np.random.default_rng(20261004);codes=37
    dates=np.repeat(np.array([20201229,20201230,20201231,20210104,20210105]),codes);valid=rng.random(len(dates))>.1;valid[0]=False
    arrays=[rng.integers(-7,8,size=len(dates)).astype(float) for _ in bank.MEMBERS]
    matrix=bank.rank_features(arrays,dates,valid);expected=np.full_like(matrix,np.nan)
    for index,values in enumerate(arrays):
        for date in np.unique(dates):
            mask=(dates==date)&valid;expected[mask,index]=(rankdata(values[mask],method='average')/mask.sum()-.5).astype(np.float32)
    assert np.array_equal(matrix,expected,equal_nan=True)
    prefix=dates<=20201231;assert np.array_equal(bank.rank_features([a[prefix] for a in arrays],dates[prefix],valid[prefix]),matrix[prefix],equal_nan=True)
    uniform=bank.uniform_rank_mean(matrix,valid)
    independent=np.full(len(dates),-1e6)
    for row in np.flatnonzero(valid):
        value=0.
        for column in range(len(bank.MEMBERS)):value+=float(expected[row,column])*(1./len(bank.MEMBERS))
        independent[row]=value
    uniform_error=float(np.max(np.abs(uniform-independent)))
    assert uniform_error<1e-15
    assert np.array_equal(uniform[prefix],bank.uniform_rank_mean(matrix[prefix],valid[prefix]))
    frame=pl.DataFrame({'ts_code':[f'{i%codes:06d}' for i in range(len(dates))],'trade_date':dates,'price_valid':valid,
                        'y_rank':rng.uniform(-.5,.5,len(dates)),'y_ret_1d':rng.normal(0,.03,len(dates))})
    frame=frame.with_columns(pl.when(pl.int_range(pl.len())==4).then(float('nan')).otherwise(pl.col('y_rank')).alias('y_rank'))
    cutoff=bank.engine.fold_cutoff(2021);poisoned=frame.with_columns([pl.when(pl.col('trade_date')>=cutoff).then(12345.).otherwise(pl.col(c)).alias(c) for c in ('y_rank','y_ret_1d')])
    controls=[]
    for name in bank.BASE_CONFIGS:
        cfg=bank.CONFIGS[name];mask=bank.training_mask(frame,2021,cfg['target']);changed=bank.training_mask(poisoned,2021,cfg['target'])
        assert np.array_equal(mask,changed) and not mask[dates>=cutoff].any()
        a=bank.linear.fit_arrays(matrix[mask],frame[cfg['target']].to_numpy()[mask],cfg)
        b=bank.linear.fit_arrays(matrix[changed],poisoned[cfg['target']].to_numpy()[changed],cfg)
        assert all(np.array_equal(a[k],b[k]) for k in ('mean','scale','coefficients')) and a['intercept']==b['intercept']
        labels=frame[cfg['target']].to_numpy()[mask]
        if a['target_bounds'] is not None:labels=np.clip(labels,*a['target_bounds'])
        x=bank.linear.transform(matrix[mask],a['mean'],a['scale'],cfg['clip_z'])
        reference=Ridge(alpha=cfg['ridge_lambda']*len(labels),solver='cholesky').fit(x,labels)
        assert np.max(np.abs(reference.coef_-a['coefficients']))<1e-12 and abs(reference.intercept_-a['intercept'])<1e-12
        pred=bank.linear.predict_arrays(a,matrix);assert np.array_equal(pred[:codes*3],bank.linear.predict_arrays(a,matrix[:codes*3]))
        controls.append({'model':name,'future_label_poisoned_fit_bit_identical':True,'independent_sklearn_tolerance':1e-12,'prefix_bit_identical':True})
    paths=[Path(__file__),Path(bank.__file__),bank.SOURCE,Path(bank.linear.__file__),ROOT/'analysis/nonlinear_stacking_model_sources_20261004.py']
    bank.dump(bank.PREFLIGHT,{'status':'passed','verified_at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'members':67,
          'scheme_configurations':12,'distinct_later_year_fits_per_fold':6,'independent_scipy_rank_reference_bit_identical':True,
          'independent_uniform_scalar_reference_max_abs_error':uniform_error,'uniform_reference_tolerance':1e-15,
          'first_year_fallback_not_fitted_to_validation_targets':True,
          'price_valid_pool_independent_of_target_availability':True,'controls':controls,'test_data_read':False,'new_official_scores':0,
          'source_sha256':{str(p.resolve()):bank.sha(p) for p in paths}},immutable=True)
    bank.log('Expanded67-parent stacking preflight passed: independent ranks, uniform sum and six solver/cutoff controls')


if __name__=='__main__':main()
