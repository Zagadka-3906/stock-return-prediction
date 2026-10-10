"""Check actual SciPy statistic, p-value and fallback behavior before full scoring."""
from pathlib import Path
import sys,warnings
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis'
sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import create,sha
def main():
    import numpy as np,pandas as pd,evaluate
    from exact_cached_official_spearman_v2_20261007 import installed
    rng=np.random.default_rng(20261007)
    pairs=[(rng.normal(size=4650),rng.normal(size=4650)),
      (rng.integers(-8,9,size=4650).astype(float),rng.integers(-4,5,size=4650).astype(float)),
      (np.array([-0.,0.,-10.,-10.,1.,1.,2.]),np.array([2.,1.,1.,-0.,0.,-10.,3.])),
      (np.array([1.,np.nan,3.,4.]),np.array([4.,5.,np.nan,1.])),
      (np.ones(10),np.arange(10,dtype=float)),
      (np.array([1.,2.,np.inf,4.]),np.array([4.,3.,2.,1.])),
      (np.array([]),np.array([])),(np.array([1.,2.]),np.array([2.,1.]))]
    controls=[];original=evaluate.spearmanr;cache={}
    for alternative in ('two-sided','greater','less'):
        for x,y in pairs:
            sx=pd.Series(x,name='pred');sy=pd.Series(y,name='y_ret_1d')
            with warnings.catch_warnings():
                warnings.simplefilter('ignore');expected=original(sx,sy,alternative=alternative)
                with installed(cache) as events:
                    actual=evaluate.spearmanr(sx,sy,alternative=alternative)
                    second=evaluate.spearmanr(sx,sy,alternative=alternative)
            for exp,got,again in zip(expected,actual,second):
                if np.isnan(exp):assert np.isnan(got) and np.isnan(again)
                else:assert np.float64(exp).view('u8')==np.float64(got).view('u8')==np.float64(again).view('u8')
            assert evaluate.spearmanr is original
            controls.append({'alternative':alternative,'rows':len(x),'statistic_and_pvalue_bits_exact_or_matching_nan':True,'events':dict(events)})
    out=A/'exact_cached_official_spearman_v2_edge_preflight_20261007';assert not out.exists();out.mkdir()
    create(out/'verification.json',{'status':'passed_actual24_SciPy_statistic_pvalue_edge_and_fallback_controls',
      'input_sha256':{str(p):sha(p) for p in [Path(__file__),A/'exact_cached_official_spearman_v2_20261007.py',A/'exact_cached_validation_spearman_20261007.py',ROOT/'evaluate.py']},
      'controls':controls,'full_official_equivalence_not_claimed':True,'new_native_fits':0,'new_quality_scores':0,'test_labels_read':False})
    print({'status':'passed','controls':len(controls)},flush=True)
if __name__=='__main__':main()
