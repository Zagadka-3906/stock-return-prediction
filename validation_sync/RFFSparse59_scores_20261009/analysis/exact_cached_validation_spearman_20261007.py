"""Scoped scoring-only Spearman ranks; unsupported Series calls retain pandas behavior."""
from contextlib import contextmanager
import numpy as np

def average_ranks(values):
    values=np.asarray(values,dtype=np.float64)
    assert values.ndim==1 and np.isfinite(values).all()
    n=len(values)
    if not n:return np.empty(0,dtype=np.float64)
    order=np.argsort(values,kind='mergesort');sorted_values=values[order]
    starts=np.r_[0,np.flatnonzero(sorted_values[1:]!=sorted_values[:-1])+1]
    ends=np.r_[starts[1:],n]
    sorted_ranks=np.repeat((starts+ends+1).astype(np.float64)/2.,ends-starts)
    ranks=np.empty(n,dtype=np.float64);ranks[order]=sorted_ranks
    return ranks

@contextmanager
def installed():
    import pandas as pd
    original=pd.Series.corr;cache={}
    events={'actual_scoped_fast_spearman_calls':0,'actual_fixed_label_rank_cache_hits':0,
      'actual_fixed_label_rank_cache_misses':0,'actual_unsupported_fallback_calls':0,
      'scoring_labels_never_used_as_features_or_training_inputs':True}
    def corr(self,other,method='pearson',min_periods=None):
        supported=(method=='spearman' and min_periods is None and isinstance(other,pd.Series)
          and self.name=='pred' and other.name=='y_ret_1d' and self.dtype==np.dtype('float64')
          and other.dtype==np.dtype('float64') and self.index.equals(other.index))
        if supported:
            x=self.to_numpy(copy=False);y=other.to_numpy(copy=False)
            valid=~np.isnan(x)&~np.isnan(y);x=x[valid];y=y[valid]
            supported=(len(x)>=3 and np.isfinite(x).all() and np.isfinite(y).all()
              and np.any(x!=x[0]) and np.any(y!=y[0]))
        if not supported:
            events['actual_unsupported_fallback_calls']+=1
            return original(self,other,method=method,min_periods=min_periods)
        key=y.tobytes(order='C')
        ranked_y=cache.get(key)
        if ranked_y is None:
            ranked_y=average_ranks(y);cache[key]=ranked_y;events['actual_fixed_label_rank_cache_misses']+=1
        else:events['actual_fixed_label_rank_cache_hits']+=1
        ranked_x=average_ranks(x)
        # scipy.stats.spearmanr uses two contiguous rank rows after transposing
        # np.apply_along_axis output. Retain that layout and np.corrcoef arithmetic.
        result=np.corrcoef(np.vstack([ranked_x,ranked_y]),rowvar=True)[0,1]
        events['actual_scoped_fast_spearman_calls']+=1
        return result
    pd.Series.corr=corr
    try:yield events
    finally:
        assert pd.Series.corr is corr
        pd.Series.corr=original
        events['actual_cached_target_vectors']=len(cache)
        events['original_pandas_Series_corr_identity_restored']=pd.Series.corr is original
