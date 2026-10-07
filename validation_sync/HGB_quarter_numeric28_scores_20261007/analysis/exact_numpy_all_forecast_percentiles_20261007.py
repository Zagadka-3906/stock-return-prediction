"""All-row daily percentiles for causal return mapping; every sentinel remains in the pool."""
import numpy as np

class AllForecastPercentiles:
    def __init__(self,original):
        self.original=original;self.fast_calls=0;self.fallback_calls=0

    def __call__(self,frame,values):
        values=np.asarray(values);dates=frame['trade_date'].to_numpy()
        supported=(values.ndim==dates.ndim==1 and len(values)==len(dates) and len(values)>0
            and values.dtype.kind=='f' and values.dtype.itemsize in (4,8) and dates.dtype.kind in 'iu'
            and not np.isnan(values).any() and np.all(dates[1:]>=dates[:-1]))
        if not supported:
            self.fallback_calls+=1;return self.original(frame,values)
        self.fast_calls+=1
        result=np.empty(len(values),dtype=np.float64)
        boundaries=np.r_[0,np.flatnonzero(dates[1:]!=dates[:-1])+1,len(dates)]
        for left,right in zip(boundaries[:-1],boundaries[1:]):
            order=np.argsort(values[left:right],kind='stable');ordered=values[left:right][order]
            starts=np.r_[0,np.flatnonzero(ordered[1:]!=ordered[:-1])+1];ends=np.r_[starts[1:],right-left]
            average=(starts+1+ends)/2.
            ranks=np.empty(right-left,dtype=np.float64);ranks[order]=np.repeat(average,ends-starts)
            result[left:right]=ranks/(right-left)
        assert np.isfinite(result).all() and result.min()>0 and result.max()<=1.+1e-12
        return result

    def statistics(self):
        return {'fast_calls':self.fast_calls,'fallback_calls':self.fallback_calls,
            'all_current_rows_including_invalid_forecast_sentinels':True,
            'no_price_valid_or_minus9_subset_filter':True,'average_ties_divided_by_all_day_rows':True,
            'retained_full_prediction_arrays':0}

def install():
    import return_mapping
    original=return_mapping.daily_percentile;operator=AllForecastPercentiles(original)
    return_mapping.daily_percentile=operator
    def restore():
        assert return_mapping.daily_percentile is operator
        return_mapping.daily_percentile=original
        return operator.statistics()
    return operator,restore
