"""Scoring-only SciPy-compatible two-Series Spearman with byte-keyed target ranks."""
from contextlib import contextmanager
import numpy as np
from exact_cached_validation_spearman_20261007 import average_ranks

@contextmanager
def installed(target_cache=None):
    import evaluate
    import pandas as pd
    from scipy.stats._stats_py import SignificanceResult, _SimpleStudentT, _get_pvalue
    original=evaluate.spearmanr
    cache={} if target_cache is None else target_cache
    events={'fast_calls':0,'target_rank_cache_hits':0,'target_rank_cache_misses':0,'fallback_calls':0,
            'scoring_labels_never_used_as_features_or_training_inputs':True}
    def spearman(a,b=None,axis=0,nan_policy='propagate',alternative='two-sided'):
        supported=(axis==0 and nan_policy=='propagate' and alternative=='two-sided'
          and isinstance(a,pd.Series) and isinstance(b,pd.Series)
          and a.name=='pred' and b.name=='y_ret_1d' and a.index.equals(b.index)
          and a.dtype==np.dtype('float64') and b.dtype==np.dtype('float64'))
        if supported:
            x=a.to_numpy(copy=False);y=b.to_numpy(copy=False)
            supported=(len(x)>=3 and np.isfinite(x).all() and np.isfinite(y).all()
                       and np.any(x!=x[0]) and np.any(y!=y[0]))
        if not supported:
            events['fallback_calls']+=1
            return original(a,b,axis=axis,nan_policy=nan_policy,alternative=alternative)
        key=y.tobytes(order='C');ranked_y=cache.get(key)
        if ranked_y is None:
            ranked_y=average_ranks(y);cache[key]=ranked_y;events['target_rank_cache_misses']+=1
        else:events['target_rank_cache_hits']+=1
        rs=np.corrcoef(np.vstack([average_ranks(x),ranked_y]),rowvar=True)
        dof=len(x)-2
        with np.errstate(divide='ignore'):
            t=rs*np.sqrt((dof/((rs+1.0)*(1.0-rs))).clip(0))
        prob=_get_pvalue(t,_SimpleStudentT(dof),alternative,xp=np)
        result=SignificanceResult(rs[1,0],prob[1,0]);result.correlation=rs[1,0]
        events['fast_calls']+=1
        return result
    evaluate.spearmanr=spearman
    try:yield events
    finally:
        assert evaluate.spearmanr is spearman
        evaluate.spearmanr=original
        events['cached_target_vectors']=len(cache)
        events['original_official_spearman_identity_restored']=evaluate.spearmanr is original
