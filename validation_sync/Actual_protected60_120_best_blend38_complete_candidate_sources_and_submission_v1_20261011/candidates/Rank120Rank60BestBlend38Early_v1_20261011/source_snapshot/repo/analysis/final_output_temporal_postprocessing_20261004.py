"""Causal daily-rank EMA applied after a frozen complete output pipeline."""
import numpy as np
from optimize_wave15 import daily_ranks


def transform(raw,dates,valid,codes,configuration):
    raw=np.asarray(raw,dtype=np.float64);dates=np.asarray(dates);valid=np.asarray(valid,dtype=bool);codes=np.asarray(codes,dtype=np.int64)
    assert len(raw)==len(dates)==len(valid)==len(codes) and np.isfinite(raw).all()
    assert np.all(dates[1:]>=dates[:-1]) and np.all(codes>=0)
    alpha=float(configuration['alpha']);mix=float(configuration['mix']);power=float(configuration['power'])
    assert 0.<alpha<=1. and 0.<=mix<=1. and power>0.
    if mix==0. or (alpha==1. and power==1.):return raw.copy()
    ranks=daily_ranks(raw,valid,dates);current=np.power(np.maximum(ranks,0.),power)
    state=np.zeros(int(codes.max())+1,dtype=np.float64);seen=np.zeros(len(state),dtype=bool)
    result=raw.copy();bounds=np.r_[0,np.flatnonzero(dates[1:]!=dates[:-1])+1,len(dates)]
    for start,end in zip(bounds[:-1],bounds[1:]):
        index=np.arange(start,end)[valid[start:end]];stock=codes[index]
        assert len(stock)==len(np.unique(stock))
        values=current[index];old=state[stock];known=seen[stock]
        updated=np.where(known,alpha*values+(1.-alpha)*old,values)
        result[index]=(1.-mix)*values+mix*updated
        state[stock]=updated;seen[stock]=True
    assert np.isfinite(result).all()
    return result
