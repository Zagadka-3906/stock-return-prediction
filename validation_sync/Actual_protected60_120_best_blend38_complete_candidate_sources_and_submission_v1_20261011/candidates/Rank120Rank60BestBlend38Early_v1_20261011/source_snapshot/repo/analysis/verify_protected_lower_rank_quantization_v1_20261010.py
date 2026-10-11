"""Own independent synthetic, cutoff-tie, signed-zero, missing-price and future-poison controls."""
from pathlib import Path
import sys,time
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A),str(A.parent)]
from run_dependency_queue_v3_20261006 import sha,create

def main():
    import numpy as np,itertools
    import protected_lower_rank_quantization_v1_20261010 as codec
    rng=np.random.default_rng(20261010);days=np.repeat([20200102,20200103,20200106],200)
    parent=np.round(rng.normal(size=600),1);parent[:4]=[0.,-0.,0.,-0.]
    flags=np.zeros(600,dtype=np.int8);flags[::7]=1;flags[::43]=2
    valid=rng.random(600)>.35;parent[~valid]=-1e6
    # Repeated near-Top values exercise quicksort-boundary ties without labels.
    parent[valid&((np.arange(600)%4)==0)]=1.5
    controls=[]
    for bins,fraction,representative in itertools.product((8,16,32,64,128,256),(.15,.25,.4),('minimum','lower_median')):
        args=(bins,fraction,representative)
        value=codec.transform(parent,days,flags,valid,*args);oracle=codec.pandas_oracle(parent,days,flags,valid,*args)
        assert np.array_equal(value.view('u8'),oracle.view('u8'));codec.assert_invariants(parent,value,days,flags,valid)
        for n in (200,400):
            prefix=codec.transform(parent[:n],days[:n],flags[:n],valid[:n],*args)
            assert np.array_equal(value[:n].view('u8'),prefix.view('u8'))
        poison=parent.copy();poison[200:]=rng.normal(300,70,400)
        changed=codec.transform(poison,days,flags,valid,*args)
        assert np.array_equal(value[:200].view('u8'),changed[:200].view('u8'))
        for constant in (0.,-1e6):
            p=np.full(600,constant);v=codec.transform(p,days,flags,valid,*args)
            assert np.array_equal(p.view('u8'),v.view('u8'))
        controls.append({'bins':bins,'protect_fraction':fraction,'representative':representative,'full_independent_bits_exact':True,'prefixes':2,'future_prediction_poison_first_day_bits_exact':True,'constant_identity_bits_exact':True,'original_official_Top_sets_exact':True})
    create(A/'protected_lower_rank_quantization_controls_v1_20261010.json',{'status':'passed36_independent_quantization_cases72_prefixes_future_poison_and_Top_ties','at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'input_sha256':{str(p):sha(p) for p in [Path(__file__),Path(codec.__file__)]},'controls':controls,'test_labels_read':False,'actual_future_X_read':False,'new_quality_scores':0})
    print('PASS 36 independent quantization controls, 72 prefixes, poison, constants, officialTop',flush=True)

if __name__=='__main__':main()
