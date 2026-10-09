"""Current-day market regimes, normalized exclusively on each fold's past."""
from pathlib import Path
import sys
import time
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT),str(ROOT/'analysis')]
from run import FEATURE_FILE,MANIFEST,fold_cutoff
from continue_optimization import read,dump,sha,log,YEARS
OUT=ROOT/'analysis/market_regime_bank_20261003'
NAMES=('abs_return','return_dispersion','relative_volume')
KEYS=['ts_code','trade_date']


def daily_statistics(frame):
    import numpy as np
    import polars as pl
    frame=frame.select(KEYS+['price_valid','RET1','RVOL20']).sort('trade_date','ts_code')
    dates=frame['trade_date'].to_numpy();valid=frame['price_valid'].to_numpy()
    returns=frame['RET1'].to_numpy().astype(np.float64);volume=frame['RVOL20'].to_numpy().astype(np.float64)
    unique,starts=np.unique(dates,return_index=True);ends=np.append(starts[1:],len(frame));values=[]
    # Fixed per-day stock order avoids parallel reduction differences after future appends.
    for date,start,end in zip(unique,starts,ends):
        r=returns[start:end];v=volume[start:end];usable=valid[start:end]
        r=r[usable&np.isfinite(r)];v=v[usable&np.isfinite(v)]
        values.append((int(date),float(np.median(np.abs(r))) if len(r) else float('nan'),
                       float(np.std(r,ddof=1)) if len(r)>1 else float('nan'),float(np.median(v)) if len(v) else float('nan')))
    return pl.DataFrame(values,schema=['trade_date',*NAMES],orient='row').with_columns(pl.col('trade_date').cast(frame.schema['trade_date']))


def fit_mapping(past,name):
    import numpy as np
    import polars as pl
    values=past[name].filter(past[name].is_finite()).to_numpy();assert len(values)>20
    lower,upper=np.quantile(values,[.25,.75]);fallback=float(np.median(values))
    assert np.isfinite(lower) and np.isfinite(upper) and np.isfinite(fallback)
    return {'name':name,'lower':float(lower),'upper':float(upper),'fallback':fallback,
            'past_days':len(values),'past_first_date':int(past['trade_date'].min()),'past_last_date':int(past['trade_date'].max())}


def apply_mapping(mapping,daily):
    import numpy as np
    values=daily[mapping['name']].to_numpy().astype(np.float64)
    values=np.where(np.isfinite(values),values,mapping['fallback'])
    scale=max(mapping['upper']-mapping['lower'],1e-12)
    return np.clip((values-mapping['lower'])/scale,0.,1.)


def verify():
    record=read(OUT/'protocol.json')
    for path,digest in record['input_sha256'].items():assert sha(path)==digest,path
    return record


def freeze():
    if (OUT/'protocol.json').exists():verify();return
    sources=[Path(__file__),FEATURE_FILE,MANIFEST,ROOT/'run.py',ROOT/'src/features.py',ROOT/'后续选模标准.md']
    dump(OUT/'protocol.json',{'frozen_at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'regimes':NAMES,'years':YEARS,
         'current_information':'Only current-date provided-derived RET1 and RVOL20 over price-valid finite stock pools; no realized next-day return or label eligibility.',
         'normalization':'For each validation year, fit 25th/75th quantiles and missing-value median using training dates below the original exclusive mature-label cutoff. Clip current-day normalized value to [0,1].',
         'feature_columns_read':['ts_code','trade_date','price_valid','RET1','RVOL20','is_train'],
         'no_labels_read':True,'test_data_read':False,'input_sha256':{str(p.resolve()):sha(p) for p in sources}},immutable=True)
    log('Three current-day market regimes and past-only normalizers frozen')


def all_oof():
    import numpy as np
    import polars as pl
    freeze();verify()
    if (OUT/'oof_audit.json').exists():
        for path,digest in read(OUT/'oof_audit.json')['output_sha256'].items():assert sha(path)==digest,path
        return
    columns=KEYS+['price_valid','RET1','RVOL20']
    frame=pl.scan_parquet(FEATURE_FILE).filter(pl.col('is_train')).select(columns).sort('trade_date','ts_code').collect()
    daily=daily_statistics(frame);daily.write_parquet(OUT/'past_daily_statistics.parquet')
    parts={name:[] for name in NAMES};proofs=[]
    for year in YEARS:
        cutoff=fold_cutoff(year);past=daily.filter(pl.col('trade_date')<cutoff)
        validation=frame.filter(pl.col('trade_date')//10000==year);current=daily.filter(pl.col('trade_date')//10000==year)
        last=int(current['trade_date'][79]);prefix=validation.filter(pl.col('trade_date')<=last)
        assert daily_statistics(prefix).equals(current.head(80))
        poisoned=validation.with_columns(pl.lit(12345.).alias('y_ret_1d'),pl.lit(float('nan')).alias('y_rank'))
        assert daily_statistics(poisoned).equals(current)
        for name in NAMES:
            mapping=fit_mapping(past,name);assert mapping['past_last_date']<cutoff<int(current['trade_date'].min())
            dump(OUT/f'mapping_{name}_{year}.json',mapping,immutable=True)
            enriched=current.select('trade_date').with_columns(pl.Series('state',apply_mapping(mapping,current)))
            values=validation.select(KEYS).join(enriched,on='trade_date',how='left',validate='m:1')['state'].to_numpy()
            assert np.isfinite(values).all() and np.all(values>=0) and np.all(values<=1);parts[name].append(values)
            prefix_values=apply_mapping(mapping,daily_statistics(prefix));assert np.array_equal(prefix_values,apply_mapping(mapping,current)[:80])
            proofs.append({'year':year,'regime':name,'past_last_date':mapping['past_last_date'],'cutoff_exclusive':cutoff,
                           'current_feature_prefix_bit_identical':True,'label_poisoning_statistics_bit_identical':True})
    for name,arrays in parts.items():np.save(OUT/f'{name}.npy',np.concatenate(arrays))
    outputs=[OUT/'past_daily_statistics.parquet',*[OUT/f'{name}.npy' for name in NAMES],*sorted(OUT.glob('mapping_*_20*.json'))]
    dump(OUT/'oof_audit.json',{'status':'passed','controls':proofs,'models_trained':0,'test_data_read':False,
         'label_columns_read':False,'output_sha256':{str(p):sha(p) for p in outputs}},immutable=True)
    log('Three market regimes, 15 past-normalizer boundaries and date-prefix controls passed')


def future_mapping():
    import polars as pl
    verify();assert read(OUT/'oof_audit.json')['status']=='passed'
    cutoff=fold_cutoff(2025);past=pl.read_parquet(OUT/'past_daily_statistics.parquet').filter(pl.col('trade_date')<cutoff)
    mappings={name:fit_mapping(past,name) for name in NAMES}
    assert all(mapping['past_last_date']<cutoff for mapping in mappings.values())
    dump(OUT/'future_mapping_2025.json',{'cutoff_exclusive':cutoff,'mappings':mappings,'test_data_read':False},immutable=True)
    return mappings


def future_values(mappings,frame):
    import numpy as np
    import polars as pl
    daily=daily_statistics(frame);result={}
    for name,mapping in mappings.items():
        enriched=daily.select('trade_date').with_columns(pl.Series('state',apply_mapping(mapping,daily)))
        values=frame.select(KEYS).join(enriched,on='trade_date',how='left',validate='m:1')['state'].to_numpy()
        assert np.isfinite(values).all();result[name]=values
    return result


if __name__=='__main__':all_oof()
