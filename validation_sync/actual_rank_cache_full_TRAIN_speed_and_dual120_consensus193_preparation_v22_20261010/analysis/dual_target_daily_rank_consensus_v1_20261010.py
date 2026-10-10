"""Combine two supplied same-date forecasts before any eligibility filtering."""
import numpy as np

def percentiles(values,dates):
    values=np.asarray(values,dtype=np.float64);dates=np.asarray(dates)
    assert values.ndim==dates.ndim==1 and len(values)==len(dates)>0
    assert np.isfinite(values).all() and np.all(dates[1:]>=dates[:-1])
    edges=np.r_[0,np.flatnonzero(dates[1:]!=dates[:-1])+1,len(dates)]
    result=np.empty(len(values),dtype=np.float64)
    for left,right in zip(edges[:-1],edges[1:]):
        row=values[left:right];order=np.argsort(row,kind='stable');ordered=row[order]
        starts=np.r_[0,np.flatnonzero(ordered[1:]!=ordered[:-1])+1]
        ends=np.r_[starts[1:],len(row)]
        ranked=np.empty(len(row),dtype=np.float64)
        ranked[order]=np.repeat((starts+1+ends)/2.,ends-starts)/len(row)
        result[left:right]=ranked
    return result

def transform(mean_raw,rank_raw,dates,mean_weight):
    assert float(mean_weight) in (.25,.5,.75)
    return float(mean_weight)*percentiles(mean_raw,dates)+(1.-float(mean_weight))*percentiles(rank_raw,dates)

def pandas_oracle(mean_raw,rank_raw,dates,mean_weight):
    import pandas as pd
    assert float(mean_weight) in (.25,.5,.75)
    a=pd.Series(mean_raw).groupby(dates,sort=False).rank(method='average',pct=True).to_numpy()
    b=pd.Series(rank_raw).groupby(dates,sort=False).rank(method='average',pct=True).to_numpy()
    return float(mean_weight)*a+(1.-float(mean_weight))*b
