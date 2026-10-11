"""Actual finite, ties, signedzero and unsupported pandas correlation behavior controls."""
from pathlib import Path
import sys
import warnings
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis'
sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import sha,create

def main():
    import numpy as np
    import pandas as pd
    from scipy.stats import rankdata
    from exact_cached_validation_spearman_20261007 import installed,average_ranks
    rng=np.random.default_rng(20261007)
    samples=[rng.normal(size=4650),rng.integers(-8,9,size=4650).astype(float),
      np.array([-0.,0.,-10.,-10.,1.,1.,2.]),np.ones(4650),np.array([])]
    for values in samples:assert np.array_equal(average_ranks(values).view('u8'),np.asarray(rankdata(values),dtype=float).view('u8'))
    pairs=[(rng.normal(size=4650),rng.normal(size=4650)),
      (rng.integers(-8,9,size=4650).astype(float),rng.integers(-4,5,size=4650).astype(float)),
      (np.array([-0.,0.,-10.,-10.,1.,1.,2.]),np.array([2.,1.,1.,-0.,0.,-10.,3.])),
      (np.array([1.,np.nan,3.,4.]),np.array([4.,5.,np.nan,1.])),
      (np.ones(10),np.arange(10,dtype=float)),
      (np.array([1.,2.,np.inf,4.]),np.array([4.,3.,2.,1.])),
      (np.array([]),np.array([])),(np.array([1.,2.]),np.array([2.,1.]))]
    original=pd.Series.corr;controls=[]
    for mode in ('spearman','pearson'):
        for x,y in pairs:
            sx=pd.Series(x,name='pred');sy=pd.Series(y,name='y_ret_1d')
            with warnings.catch_warnings():
                warnings.simplefilter('ignore');expected=original(sx,sy,method=mode)
                with installed() as events:
                    actual=sx.corr(sy,method=mode);second=sx.corr(sy,method=mode)
            if np.isnan(expected):assert np.isnan(actual) and np.isnan(second)
            else:assert np.float64(expected).view('u8')==np.float64(actual).view('u8')==np.float64(second).view('u8')
            assert pd.Series.corr is original
            controls.append({'method':mode,'rows':len(x),'result_uint64_exact_or_matching_nan':True,'events':dict(events)})
    out=A/'exact_cached_validation_spearman_edge_preflight_20261007';assert not out.exists();out.mkdir()
    create(out/'verification.json',{'status':'passed_actual5_rank_arrays16_series_correlation_edge_and_fallback_controls',
      'input_sha256':{str(p):sha(p) for p in [Path(__file__),A/'exact_cached_validation_spearman_20261007.py']},
      'controls':controls,'new_native_fits':0,'new_quality_scores':0,'full_official_equivalence_benchmark_still_required':True,'test_labels_read':False})
    print({'status':'passed','rank_arrays':5,'series_controls':len(controls)},flush=True)

if __name__=='__main__':main()
