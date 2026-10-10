"""Current-day-only tail permutation; upper nonflag forecasts and whole-day value multiset stay exact."""
import numpy as np
import BF16Medium153_complete_parent_rank_CDF_v1_20261009 as codec
prepare=codec.prepare

def apply_prepared(parent,flags,valid,weight,protect_fraction,prepared):
    assert 0.<=weight<=1. and .1<=protect_fraction<=.5
    result=np.asarray(parent,dtype=np.float64).copy()
    if weight==0.:return result
    eligible=np.asarray(valid,dtype=bool)&(np.asarray(flags)!=1)
    for left,right,pp,npct,knots,ordered in prepared:
        pool=np.flatnonzero(eligible[left:right])
        if not len(pool):continue
        values=np.asarray(parent)[left+pool]
        keep=max(1,int(np.ceil(float(protect_fraction)*len(pool))))
        cutoff=np.sort(values,kind='stable')[-keep]
        lower=pool[values<cutoff]
        if len(lower)<2:continue
        blended=(1.-float(weight))*pp[lower]+float(weight)*npct[lower]
        target=lower[np.argsort(blended,kind='stable')]
        result[left+target]=np.sort(np.asarray(parent)[left+lower],kind='stable')
    return result

def transform(parent,raw,dates,flags,valid,weight,protect_fraction,sign=1.):
    return apply_prepared(parent,flags,valid,weight,protect_fraction,prepare(parent,raw,dates,flags,valid,sign))

def pandas_oracle(parent,raw,dates,flags,valid,weight,protect_fraction,sign=1.):
    import pandas as pd
    assert 0.<=weight<=1. and .1<=protect_fraction<=.5 and sign in (-1.,1.)
    result=np.asarray(parent,dtype=np.float64).copy()
    if weight==0.:return result
    neural=np.asarray(raw).copy();neural[np.asarray(valid,dtype=bool)]*=float(sign)
    pp=pd.Series(parent).groupby(dates,sort=False).rank(method='average',pct=True)
    npct=pd.Series(neural).groupby(dates,sort=False).rank(method='average',pct=True)
    eligible=np.asarray(valid,dtype=bool)&(np.asarray(flags)!=1)
    for indices in pd.Series(np.arange(len(dates))).groupby(dates,sort=False).indices.values():
        pool=indices[eligible[indices]]
        if not len(pool):continue
        values=pd.Series(np.asarray(parent)[pool],index=pool)
        keep=max(1,int(np.ceil(float(protect_fraction)*len(pool))))
        cutoff=values.sort_values(ascending=False,kind='mergesort').iloc[keep-1]
        lower=values[values<cutoff].index.to_numpy()
        if len(lower)<2:continue
        blended=(1.-float(weight))*pp.iloc[lower]+float(weight)*npct.iloc[lower]
        target=blended.sort_values(kind='mergesort').index.to_numpy()
        result[target]=values.loc[lower].sort_values(kind='mergesort').to_numpy()
    return result

def assert_invariants(parent,value,dates,flags,valid,protect_fraction):
    assert np.array_equal(value[~(np.asarray(valid,dtype=bool)&(np.asarray(flags)!=1))].view('u8'),np.asarray(parent)[~(np.asarray(valid,dtype=bool)&(np.asarray(flags)!=1))].view('u8'))
    boundaries=np.r_[0,np.flatnonzero(np.asarray(dates)[1:]!=np.asarray(dates)[:-1])+1,len(dates)]
    for left,right in zip(boundaries[:-1],boundaries[1:]):
        a=np.asarray(parent)[left:right];b=value[left:right]
        # Sort bit patterns to compare multisets; -0.0/+0.0 have equal numeric sort keys.
        assert np.array_equal(np.sort(a.view('u8')),np.sort(b.view('u8')))
        pool=np.flatnonzero(np.asarray(valid[left:right],dtype=bool)&(np.asarray(flags[left:right])!=1))
        if len(pool):
            keep=max(1,int(np.ceil(float(protect_fraction)*len(pool))))
            cutoff=np.sort(a[pool],kind='stable')[-keep];chosen=pool[a[pool]>=cutoff]
            assert np.array_equal(a[chosen].view('u8'),b[chosen].view('u8'))
