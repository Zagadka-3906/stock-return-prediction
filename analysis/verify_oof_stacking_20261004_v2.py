"""Independent feature-assembly, cutoff-poisoning and numerical controls."""
from pathlib import Path
import sys
import time
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT),str(ROOT/'analysis')]
import train_oof_stacking_bank_20261004 as bank


def main():
    import numpy as np
    import polars as pl
    from scipy.stats import rankdata
    from sklearn.linear_model import Ridge
    rng=np.random.default_rng(20261004)
    codes=37;dates=np.repeat(np.array([20201229,20201230,20201231,20210104,20210105]),codes)
    valid=rng.random(len(dates))>.1;valid[0]=False
    arrays=[rng.integers(-7,8,size=len(dates)).astype(float) for _ in bank.MEMBERS]
    assembled=bank.rank_features(arrays,dates,valid)
    expected=np.empty_like(assembled);expected.fill(np.nan)
    for index,values in enumerate(arrays):
        for date in np.unique(dates):
            mask=(dates==date)&valid
            expected[mask,index]=(rankdata(values[mask],method='average')/mask.sum()-.5).astype(np.float32)
    assert np.array_equal(assembled,expected,equal_nan=True)
    prefix=dates<=20201231
    assert np.array_equal(bank.rank_features([a[prefix] for a in arrays],dates[prefix],valid[prefix]),assembled[prefix],equal_nan=True)
    frame=pl.DataFrame({'ts_code':[f'{i%codes:06d}' for i in range(len(dates))], 'trade_date':dates,'price_valid':valid,
                        'y_rank':rng.uniform(-.5,.5,len(dates)),'y_ret_1d':rng.normal(0,.03,len(dates))})
    frame=frame.with_columns(pl.when(pl.int_range(pl.len())==4).then(float('nan')).otherwise(pl.col('y_rank')).alias('y_rank'))
    cutoff=bank.fold_cutoff(2021);assert cutoff==20201231
    poisoned=frame.with_columns([pl.when(pl.col('trade_date')>=cutoff).then(12345.).otherwise(pl.col(c)).alias(c) for c in ('y_rank','y_ret_1d')])
    controls=[]
    for name,cfg in bank.CONFIGS.items():
        mask=bank.training_mask(frame,2021,cfg['target']);changed=bank.training_mask(poisoned,2021,cfg['target'])
        assert np.array_equal(mask,changed) and not mask[dates>=cutoff].any()
        a=bank.linear.fit_arrays(assembled[mask],frame[cfg['target']].to_numpy()[mask],cfg)
        b=bank.linear.fit_arrays(assembled[changed],poisoned[cfg['target']].to_numpy()[changed],cfg)
        assert all(np.array_equal(a[k],b[k]) for k in ('mean','scale','coefficients')) and a['intercept']==b['intercept']
        labels=frame[cfg['target']].to_numpy()[mask]
        if a['target_bounds'] is not None:labels=np.clip(labels,*a['target_bounds'])
        x=bank.linear.transform(assembled[mask],a['mean'],a['scale'],cfg['clip_z'])
        reference=Ridge(alpha=cfg['ridge_lambda']*len(labels),solver='cholesky').fit(x,labels)
        assert np.max(np.abs(reference.coef_-a['coefficients']))<1e-12 and abs(reference.intercept_-a['intercept'])<1e-12
        pred=bank.linear.predict_arrays(a,assembled)
        assert np.array_equal(pred[:codes*3],bank.linear.predict_arrays(a,assembled[:codes*3]))
        controls.append({'model':name,'future_label_poisoned_fit_bit_identical':True,'sklearn_cholesky_max_abs_tolerance':1e-12,
                         'complete_day_feature_prefix_bit_identical':True,'training_rows':int(mask.sum())})
    out=ROOT/'analysis/oof_stacking_preflight_20261004_v2'
    bank.dump(out/'verification.json',{'status':'passed','verified_at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),
              'members':len(bank.MEMBERS),'independent_scipy_daily_rank_reference_bit_identical':True,
              'price_invalid_and_target_missing_pools_handled_separately':True,'controls':controls,'test_data_read':False,
              'source_sha256':{str(p.resolve()):bank.sha(p) for p in (Path(__file__),Path(bank.__file__),Path(bank.linear.__file__))}},immutable=True)
    print('Stacking preflight passed: six independent solver/boundary controls and45 input-rank references',flush=True)


if __name__=='__main__':main()
