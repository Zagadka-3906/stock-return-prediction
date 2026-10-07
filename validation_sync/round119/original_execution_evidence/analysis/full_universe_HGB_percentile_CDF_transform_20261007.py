"""Causal full-pool forecast-percentile ensembles and same-day parent CDF."""
import numpy as np
import direct_flag_centered_rank_CDF_transform_20261007 as inherited

def centered_daily_forecast(raw, dates):
    raw,dates=map(np.asarray,(raw,dates))
    assert raw.ndim==dates.ndim==1 and len(raw)==len(dates) and np.isfinite(raw).all()
    assert np.all(np.diff(dates)>=0)
    days,starts=np.unique(dates,return_index=True);ends=np.r_[starts[1:],len(raw)]
    result=np.empty(len(raw),dtype=np.float64)
    for left,right in zip(starts,ends):
        ordered=np.sort(raw[left:right],kind='stable')
        lo=np.searchsorted(ordered,raw[left:right],side='left');hi=np.searchsorted(ordered,raw[left:right],side='right')
        result[left:right]=(lo+hi+1.)/(2.*(right-left))-.5
    return result

def prepare(raw,dates,flags,valid,universe):
    assert universe=='all_current_raw_forecasts'
    return inherited.prepare(raw,dates,np.ones(len(raw),dtype=np.int8),valid,universe)

def apply_prepared(raw,centered_forecast,weight,prepared):
    return inherited.apply_prepared(raw,centered_forecast,weight,prepared)

def transform(raw,dates,flags,valid,centered_forecast,weight,universe):
    return apply_prepared(raw,centered_forecast,weight,prepare(raw,dates,flags,valid,universe))
