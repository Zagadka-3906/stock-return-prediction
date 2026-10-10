"""Keep63 raw channels and append57 same-date finite-only peer percentiles; no fitting."""
import numpy as np

def names(raw_names):
    raw_names=list(raw_names)
    assert len(raw_names)==63 and len(set(raw_names))==63 and not any(n.startswith('y_') for n in raw_names)
    indices=[i for i,n in enumerate(raw_names) if not n.startswith('CS_')]
    assert len(indices)==57
    result=raw_names+['AUG_CS_'+raw_names[i] for i in indices]
    assert len(result)==len(set(result))==120
    return result,indices

def encode(raw,dates,raw_names):
    raw=np.asarray(raw);dates=np.asarray(dates);encoded_names,indices=names(raw_names)
    assert raw.ndim==2 and raw.shape[1]==63 and raw.dtype==np.float32
    assert dates.ndim==1 and len(dates)==len(raw) and dates.dtype.kind in 'iu'
    output=np.empty((len(raw),120),dtype=np.float32);output[:,:63]=raw
    if not len(raw):return output
    order=np.arange(len(dates)) if np.all(dates[1:]>=dates[:-1]) else np.argsort(dates,kind='stable')
    ordered_dates=dates[order];boundaries=np.r_[0,np.flatnonzero(ordered_dates[1:]!=ordered_dates[:-1])+1,len(raw)]
    for first,last in zip(boundaries[:-1],boundaries[1:]):
        rows=order[first:last]
        for column,index in enumerate(indices):
            values=raw[rows,index];finite=np.isfinite(values);count=int(finite.sum())
            percentile=np.full(len(rows),.5,dtype=np.float32)
            if count:
                valid=values[finite];sort=np.argsort(valid,kind='stable');ordered=valid[sort]
                begin=np.r_[0,np.flatnonzero(ordered[1:]!=ordered[:-1])+1];end=np.r_[begin[1:],count]
                average=((begin+1).astype(np.float64)+end)/2.
                ranked=np.repeat(average,end-begin)/count
                restored=np.empty(count,dtype=np.float64);restored[sort]=ranked
                percentile[finite]=restored.astype(np.float32)
            output[rows,63+column]=percentile
    return output

def pandas_oracle(raw,dates,raw_names):
    import pandas as pd
    raw=np.asarray(raw,dtype=np.float32);dates=np.asarray(dates)
    # Independent Pandas date-group ranks, not the production sorting implementation.
    assert raw.ndim==2 and raw.shape[1]==63 and len(raw_names)==63
    peers=[]
    for index,name in enumerate(raw_names):
        if name.startswith('CS_'):continue
        series=pd.Series(raw[:,index].astype(np.float64))
        series=series.where(np.isfinite(series))
        peers.append(series.groupby(dates,sort=False).rank(method='average',pct=True).fillna(.5).to_numpy(dtype=np.float32))
    assert len(peers)==57
    return np.column_stack([raw,*peers]).astype(np.float32,copy=False)
