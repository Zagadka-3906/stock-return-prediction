"""Protect the official X-only Top set, including missing-label rows; resolve boundary ties explicitly."""
import numpy as np
import pandas as pd
import math
import BF16Medium153_complete_parent_rank_CDF_v1_20261009 as codec
prepare=codec.prepare

def top(pool,values):
    n=max(len(pool)//10,1)
    return pd.Series(values[pool],index=pool).sort_values(ascending=False).index.to_numpy()[:n]

def apply_prepared(parent,flags,valid,weight,protect_fraction,prepared):
    assert 0.<=weight<=1. and .1<=protect_fraction<=.5
    result=np.asarray(parent,dtype=np.float64).copy()
    if weight==0.:return result
    for left,right,pp,npct,knots,ordered in prepared:
        base=np.asarray(parent)[left:right];pool=np.flatnonzero(np.asarray(flags[left:right])==0)
        if not len(pool):continue
        # Official turnover does not filter label-missing or price-invalid rows.
        protected=max(1,int(np.ceil(float(protect_fraction)*len(pool))))
        cutoff=np.sort(base[pool],kind='stable')[-protected]
        lower=pool[(base[pool]<cutoff)&np.asarray(valid[left:right],dtype=bool)[pool]]
        if len(lower)<2:continue
        q=(1.-float(weight))*pp[lower]+float(weight)*npct[lower]
        result[left+lower[np.argsort(q,kind='stable')]]=np.sort(base[lower],kind='stable')
        # Quicksort may choose different members of a cutoff tie after lower-row
        # changes. Lift only the original chosen boundary members by one ULP.
        selected=top(pool,base);others=np.setdiff1d(pool,selected)
        if len(others):
            boundary=np.max(result[left+others]);chosen=selected[result[left+selected]<=boundary]
            if len(chosen):
                assert np.all(np.asarray(valid[left:right],dtype=bool)[chosen])
                result[left+chosen]=np.nextafter(boundary,np.inf)
        assert set(top(pool,result[left:right]))==set(selected)
    return result

def transform(parent,raw,dates,flags,valid,weight,protect_fraction,sign=1.):
    return apply_prepared(parent,flags,valid,weight,protect_fraction,prepare(parent,raw,dates,flags,valid,sign))

def pandas_oracle(parent,raw,dates,flags,valid,weight,protect_fraction,sign=1.):
    assert 0.<=weight<=1. and .1<=protect_fraction<=.5 and sign in (-1.,1.)
    result=np.asarray(parent,dtype=np.float64).copy()
    if weight==0.:return result
    neural=np.asarray(raw).copy();neural[np.asarray(valid,dtype=bool)]*=float(sign)
    pp=pd.Series(parent).groupby(dates,sort=False).rank(method='average',pct=True)
    npct=pd.Series(neural).groupby(dates,sort=False).rank(method='average',pct=True)
    for indices in pd.Series(np.arange(len(dates))).groupby(dates,sort=False).indices.values():
        pool=indices[np.asarray(flags)[indices]==0]
        if not len(pool):continue
        values=pd.Series(np.asarray(parent)[pool],index=pool)
        keep=max(1,int(np.ceil(float(protect_fraction)*len(pool))))
        cutoff=values.sort_values(ascending=False,kind='mergesort').iloc[keep-1]
        lower=pool[(np.asarray(parent)[pool]<cutoff)&np.asarray(valid,dtype=bool)[pool]]
        if len(lower)<2:continue
        q=(1.-float(weight))*pp.iloc[lower]+float(weight)*npct.iloc[lower]
        target=q.sort_values(kind='mergesort').index.to_numpy()
        result[target]=values.loc[lower].sort_values(kind='mergesort').to_numpy()
        selected=values.sort_values(ascending=False).index.to_numpy()[:max(len(pool)//10,1)]
        other=values.index.difference(selected).to_numpy()
        if len(other):
            boundary=max(result[other]);chosen=[i for i in selected if result[i]<=boundary]
            if chosen:
                assert all(np.asarray(valid,dtype=bool)[i] for i in chosen)
                result[chosen]=math.nextafter(float(boundary),math.inf)
    return result

def assert_invariants(parent,value,dates,flags,valid,protect_fraction):
    unchanged=~(np.asarray(valid,dtype=bool)&(np.asarray(flags)==0))
    assert np.array_equal(value[unchanged].view('u8'),np.asarray(parent)[unchanged].view('u8'))
    boundaries=np.r_[0,np.flatnonzero(np.asarray(dates)[1:]!=np.asarray(dates)[:-1])+1,len(dates)]
    for left,right in zip(boundaries[:-1],boundaries[1:]):
        pool=np.flatnonzero(np.asarray(flags[left:right])==0)
        if len(pool):assert set(top(pool,np.asarray(parent)[left:right]))==set(top(pool,value[left:right]))
