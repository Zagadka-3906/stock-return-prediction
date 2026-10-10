"""One fixed stock-identity alpha fitted only on the preceding mature 756 trading days."""
import numpy as np
import polars as pl
CONFIG={'target':'y_ret_1d','window_days':756,'prior_zero_pseudo_days':252.,'fixed_return_clip':.1,'unseen_stock_alpha':0.}

def population(frame,cutoff):
    past=frame.filter((pl.col('trade_date')<cutoff)&pl.col('is_train'))
    days=past['trade_date'].unique().sort().to_numpy()[-CONFIG['window_days']:]
    assert len(days)>0
    return past.filter((pl.col('trade_date')>=int(days[0]))&pl.col('price_valid')&pl.col('y_ret_1d').is_finite()).sort('trade_date','ts_code')

def fit(frame,cutoff):
    past=population(frame,cutoff)
    daily=past.with_columns(pl.col('y_ret_1d').cast(pl.Float64).clip(-CONFIG['fixed_return_clip'],CONFIG['fixed_return_clip']).alias('r'))
    daily=daily.with_columns((pl.col('r')-pl.col('r').mean().over('trade_date')).alias('excess'))
    table=daily.group_by('ts_code').agg(pl.col('excess').sum().alias('sum'),pl.len().alias('count')).sort('ts_code')
    table=table.with_columns((pl.col('sum')/(pl.col('count')+CONFIG['prior_zero_pseudo_days'])).alias('alpha'))
    return {'config':dict(CONFIG),'cutoff':int(cutoff),'codes':table['ts_code'].to_list(),'alpha':table['alpha'].to_numpy(),'sum':table['sum'].to_numpy(),'count':table['count'].to_numpy(),'training_rows':len(past),'first':int(past['trade_date'].min()),'last':int(past['trade_date'].max())}

def predict(bundle,codes):
    table={k:float(v) for k,v in zip(bundle['codes'],bundle['alpha'])}
    return np.fromiter((table.get(k,0.) for k in codes),dtype=np.float64,count=len(codes))

def independent_predict(bundle,codes):
    # A separate sorted-array lookup with no native predictor or hash-table reuse.
    keys=np.asarray(bundle['codes'],dtype=str);incoming=np.asarray(codes,dtype=str)
    positions=np.searchsorted(keys,incoming);out=np.zeros(len(incoming),dtype=np.float64)
    in_range=positions<len(keys);indices=np.flatnonzero(in_range)
    matches=keys[positions[indices]]==incoming[indices];indices=indices[matches]
    out[indices]=bundle['alpha'][positions[indices]]
    return out
