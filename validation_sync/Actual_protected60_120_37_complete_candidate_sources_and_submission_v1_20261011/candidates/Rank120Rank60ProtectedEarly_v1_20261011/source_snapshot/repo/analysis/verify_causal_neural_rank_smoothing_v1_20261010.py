"""Independent bits, cross-year continuity, poison, unchanged cohorts and slot rejection."""
from pathlib import Path
import sys,itertools
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A),str(A.parent)]
from run_dependency_queue_v3_20261006 import create,sha
def main():
    import numpy as np
    import causal_neural_rank_smoothing_v1_20261010 as codec
    rng=np.random.default_rng(20261010);slots=200;n=slots*5
    dates=np.repeat([20201229,20201230,20201231,20210104,20210105],slots)
    parent=rng.normal(size=n).astype('f8');raw=rng.normal(size=n).astype('f8');raw[::9]=0.;raw[::17]=-0.
    flags=rng.integers(0,3,size=n);valid=rng.random(n)>.1;parent[~valid]=-1e6;raw[~valid]=-1e6
    exact=lambda x,y:np.array_equal(x.view('u8'),y.view('u8'))
    count=prefixes=0
    for decay,role,weight,sign in itertools.product((0.,.8,.95,.99),('nonflag_valid','all_valid'),(.016,.5),(-1.,1.)):
        args=(role,weight,sign,decay);full=codec.transform(parent,raw,dates,flags,valid,*args)
        assert exact(full,codec.pandas_oracle(parent,raw,dates,flags,valid,*args))
        mask=codec.selected(flags,valid,role);assert exact(full[~mask],parent[~mask])
        for days in (1,3,4):
            m=days*slots;short=codec.transform(parent[:m],raw[:m],dates[:m],flags[:m],valid[:m],*args)
            assert exact(full[:m],short) and exact(short,codec.pandas_oracle(parent[:m],raw[:m],dates[:m],flags[:m],valid[:m],*args))
            poisoned=raw.copy();poisoned[m:]=rng.normal(size=n-m)*1e4
            assert exact(full[:m],codec.transform(parent,poisoned,dates,flags,valid,*args)[:m]);prefixes+=1
        count+=1
    carried=codec.smooth(raw,dates,valid,.95)
    reset=codec.smooth(raw[3*slots:],dates[3*slots:],valid[3*slots:],.95)
    assert not exact(carried[3*slots:],reset),'Cross-year history must actually be active'
    try:codec.smooth(raw[:-1],dates[:-1],valid[:-1],.95)
    except AssertionError:pass
    else:raise AssertionError('Unequal stock-slot grid accepted')
    create(A/'causal_neural_rank_smoothing_controls_v1_20261010.json',{'status':'passed64_independent_synthetic_and192_prefix_poison_cross_year_controls','cases':count,'prefix_cases':prefixes,'cross_year_state_actually_carried':True,'unequal_slot_count_rejected':True,'input_sha256':{str(p):sha(p) for p in [Path(__file__),Path(codec.__file__)]},'new_quality_scores':0,'test_labels_read':False})
    print({'cases':count,'prefixes':prefixes,'status':'passed'},flush=True)
if __name__=='__main__':main()
