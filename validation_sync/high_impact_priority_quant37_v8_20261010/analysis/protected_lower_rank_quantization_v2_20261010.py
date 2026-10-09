"""Current-day lower-pool rank compression with independent Top-boundary tie enforcement."""
import numpy as np

def transform(parent,dates,flags,valid,bins,protect_fraction,representative):
    assert bins in (8,16,32,64,128,256) and protect_fraction in (.15,.25,.4)
    assert representative in ('minimum','lower_median')
    p=np.asarray(parent,dtype=np.float64);result=p.copy()
    boundaries=np.r_[0,np.flatnonzero(np.asarray(dates)[1:]!=np.asarray(dates)[:-1])+1,len(dates)]
    for left,right in zip(boundaries[:-1],boundaries[1:]):
        pool=np.flatnonzero(np.asarray(flags[left:right])==0)
        if not len(pool):continue
        before=p[left:right];keep=max(1,int(np.ceil(protect_fraction*len(pool))))
        cutoff=np.sort(before[pool],kind='stable')[-keep]
        lower=pool[(before[pool]<cutoff)&np.asarray(valid[left:right],dtype=bool)[pool]]
        if len(lower)<2:continue
        order=lower[np.argsort(before[lower],kind='stable')];values=before[order]
        assert np.isfinite(values).all()
        # Average ranks preserve equal predictions as a single group, including signed zero.
        changes=np.r_[0,np.flatnonzero(values[1:]!=values[:-1])+1,len(values)]
        rank=np.repeat((changes[:-1]+1.+changes[1:])/2.,changes[1:]-changes[:-1])
        bucket=np.minimum(np.floor(rank/len(values)*bins).astype(np.int64),bins-1)
        cuts=np.r_[0,np.flatnonzero(bucket[1:]!=bucket[:-1])+1,len(bucket)]
        representative_indices=cuts[:-1] if representative=='minimum' else cuts[:-1]+(cuts[1:]-cuts[:-1]-1)//2
        result[left+order]=np.repeat(values[representative_indices],cuts[1:]-cuts[:-1])
        # The official Pandas default quicksort can otherwise change tied Top members.
        import pandas as pd
        original=pd.Series(before[pool],index=pool).sort_values(ascending=False).index.to_numpy()[:max(len(pool)//10,1)]
        other=pool[~np.isin(pool,original)]
        if len(other):
            boundary=np.max(result[left+other]);lift=original[result[left+original]<=boundary]
            if len(lift):
                assert np.asarray(valid[left:right],dtype=bool)[lift].all()
                result[left+lift]=np.nextafter(boundary,np.inf)
    return result

def pandas_oracle(parent,dates,flags,valid,bins,protect_fraction,representative):
    import pandas as pd,math
    assert bins in (8,16,32,64,128,256) and protect_fraction in (.15,.25,.4)
    assert representative in ('minimum','lower_median')
    p=np.asarray(parent,dtype=np.float64);result=p.copy()
    for indices in pd.Series(np.arange(len(p))).groupby(dates,sort=False).indices.values():
        pool=indices[np.asarray(flags)[indices]==0]
        if not len(pool):continue
        values=pd.Series(p[pool],index=pool);keep=max(1,int(math.ceil(protect_fraction*len(pool))))
        cutoff=values.sort_values(ascending=False,kind='mergesort').iloc[keep-1]
        lower=values[(values<cutoff)&np.asarray(valid,dtype=bool)[pool]]
        if len(lower)<2:continue
        ranks=lower.rank(method='average',pct=True)
        buckets=ranks.map(lambda r:min(int(math.floor(r*bins)),bins-1))
        grouped=lower.groupby(buckets,sort=False)
        representatives=grouped.min() if representative=='minimum' else grouped.quantile(.5,interpolation='lower')
        result[lower.index.to_numpy()]=buckets.map(representatives).to_numpy()
        original=values.sort_values(ascending=False).index.to_numpy()[:max(len(pool)//10,1)]
        other=values.index.difference(original).to_numpy()
        if len(other):
            boundary=max(result[other]);lift=[i for i in original if result[i]<=boundary]
            if lift:
                assert all(np.asarray(valid,dtype=bool)[i] for i in lift)
                result[lift]=math.nextafter(float(boundary),math.inf)
    return result

def assert_invariants(parent,value,dates,flags,valid):
    import pandas as pd
    p=np.asarray(parent,dtype=np.float64);value=np.asarray(value,dtype=np.float64)
    unchanged=~(np.asarray(valid,dtype=bool)&(np.asarray(flags)==0))
    assert np.array_equal(p[unchanged].view('u8'),value[unchanged].view('u8'))
    for indices in pd.Series(np.arange(len(p))).groupby(dates,sort=False).indices.values():
        pool=indices[np.asarray(flags)[indices]==0]
        if len(pool):
            n=max(len(pool)//10,1)
            top=lambda x:set(pd.Series(x[pool],index=pool).sort_values(ascending=False).index.to_numpy()[:n])
            assert top(p)==top(value)
