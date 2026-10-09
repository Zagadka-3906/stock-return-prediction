"""Current-day nonflag teacher-residual CDF; flags and2020 preserve complete parent bytes."""
import numpy as np
def prepare(reference,dates,flags,valid,universe):
    assert universe=='all_current_raw_forecasts'
    reference=np.asarray(reference);dates=np.asarray(dates);flags=np.asarray(flags)
    assert len(reference)==len(dates)==len(flags)==len(valid) and np.isfinite(reference).all()
    assert np.all(dates[1:]>=dates[:-1])
    boundaries=np.r_[0,np.flatnonzero(dates[1:]!=dates[:-1])+1,len(dates)];result=[]
    for left,right in zip(boundaries[:-1],boundaries[1:]):
        if dates[left]<20210101:continue
        order=np.argsort(reference[left:right],kind='stable');ordered=reference[left:right][order]
        starts=np.r_[0,np.flatnonzero(ordered[1:]!=ordered[:-1])+1];ends=np.r_[starts[1:],right-left]
        ranks=np.empty(right-left,dtype=np.float64);ranks[order]=np.repeat((starts+1+ends)/2.,ends-starts)
        positions=np.flatnonzero(flags[left:right]!=1)+left
        percentile=ranks[positions-left]/(right-left);knots=np.arange(1,right-left+1,dtype=np.float64)/(right-left)
        result.append((int(dates[left]),positions,percentile,knots,ordered))
    return result
def apply_prepared(parent,reference,flags,residual,weight,prepared):
    assert np.isfinite(weight) and weight>=0.
    assert len(parent)==len(reference)==len(flags)==len(residual)
    values=np.asarray(parent,dtype=np.float64).copy()
    for day,positions,percentile,knots,ordered in prepared:
        assert day>=20210101
        if weight==0.:values[positions]=reference[positions]
        else:
            q=percentile+float(weight)*np.asarray(residual)[positions]
            values[positions]=np.interp(np.clip(q,knots[0],knots[-1]),knots,ordered)
    return values
def transform(parent,reference,dates,flags,valid,residual,weight,universe):
    return apply_prepared(parent,reference,flags,residual,weight,prepare(reference,dates,flags,valid,universe))
