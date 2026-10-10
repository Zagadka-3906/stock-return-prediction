"""Carry each fixed stock's neural percentile forward without future observations or annual resets."""
import numpy as np
import BF16_complete_parent_rank_CDF_v1_20261008 as base
selected=base.selected
apply_prepared=base.apply_prepared

def smooth(raw,dates,valid,decay,oracle=False):
    raw=np.asarray(raw);dates=np.asarray(dates);valid=np.asarray(valid,dtype=bool)
    assert raw.dtype==np.float64 and raw.ndim==dates.ndim==valid.ndim==1 and raw.shape==dates.shape==valid.shape
    assert len(raw) and np.isfinite(raw).all() and np.all(dates[1:]>=dates[:-1]) and 0.<=decay<1.
    edges=np.r_[0,np.flatnonzero(dates[1:]!=dates[:-1])+1,len(raw)]
    widths=np.diff(edges);assert np.all(widths==widths[0]),'Fixed stock-slot grid required'
    if oracle:
        import pandas as pd
        percentiles=pd.Series(raw).groupby(dates,sort=False).rank(method='average',pct=True).to_numpy()
    result=np.empty_like(raw);state=None
    for left,right in zip(edges[:-1],edges[1:]):
        if oracle:pct=percentiles[left:right]
        else:
            values=raw[left:right];order=np.argsort(values,kind='stable');ordered=values[order]
            start=np.r_[0,np.flatnonzero(ordered[1:]!=ordered[:-1])+1];end=np.r_[start[1:],right-left]
            ranks=np.empty(right-left);ranks[order]=np.repeat((start+1+end)/2.,end-start);pct=ranks/(right-left)
        mask=valid[left:right]
        if state is None:state=pct.copy()
        else:
            previous=state[mask].copy();state[mask]=float(decay)*previous+(1.-float(decay))*pct[mask]
        result[left:right]=state
        result[left:right][~mask]=-1e6
    return result

def prepare(parent,raw,dates,flags,valid,sign,decay):
    assert sign in (-1.,1.)
    neural=smooth(raw,dates,valid,decay);neural[np.asarray(valid,dtype=bool)]*=sign
    return base.prepare(parent,neural,dates,flags,valid)

def transform(parent,raw,dates,flags,valid,role,weight,sign,decay):
    return apply_prepared(parent,flags,valid,role,weight,prepare(parent,raw,dates,flags,valid,sign,decay))

def pandas_oracle(parent,raw,dates,flags,valid,role,weight,sign,decay):
    assert sign in (-1.,1.)
    neural=smooth(raw,dates,valid,decay,oracle=True);neural[np.asarray(valid,dtype=bool)]*=sign
    return base.pandas_oracle(parent,neural,dates,flags,valid,role,weight)
