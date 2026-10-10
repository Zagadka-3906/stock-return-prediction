"""Date-local convex averaging of independent raw Rank20 forecasts; no fitted state."""
def combine(first,second,second_weight):
    import numpy as np
    first=np.asarray(first,dtype=np.float64);second=np.asarray(second,dtype=np.float64)
    w=float(second_weight)
    assert first.ndim==second.ndim==1 and first.shape==second.shape
    assert 0.<w<1. and np.isfinite(first).all() and np.isfinite(second).all()
    return (1.-w)*first+w*second

def scalar_oracle(first,second,second_weight):
    import numpy as np
    assert len(first)==len(second)
    w=float(second_weight);assert 0.<w<1.
    return np.fromiter(((1.-w)*float(a)+w*float(b) for a,b in zip(first,second)),dtype=np.float64,count=len(first))

def actual_cpu_controls():
    from pathlib import Path
    import numpy as np
    from run_dependency_queue_v3_20261006 import create,sha
    from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
    assert allowed()
    rng=np.random.default_rng(202610101)
    first=rng.normal(0,.15,10017);second=rng.normal(0,.15,10017)
    first[::71]=second[::71]=-1e6;first[::37]=0.;second[::41]=0.
    rows=[]
    for w in (.25,.5,.75):
        actual=combine(first,second,w); oracle=scalar_oracle(first,second,w)
        assert np.array_equal(actual.view('u8'),oracle.view('u8'))
        for n in (1,67,4650,10017):
            assert np.array_equal(actual[:n].view('u8'),combine(first[:n],second[:n],w).view('u8'))
        poisoned=first.copy();poisoned[4650:]=12345.
        assert np.array_equal(actual[:4650].view('u8'),combine(poisoned,second,w)[:4650].view('u8'))
        rows.append({'second_seed_weight':w,'rows':len(first),'full_scalar_bits_exact':True,'prefixes':[1,67,4650,10017],'future_suffix_poison_invariant':True})
    bad=[(first,second[:-1],.5),(first,second,0.),(first,second,1.),(first[:,None],second,.5),(first*float('nan'),second,.5)]
    for args in bad:
        try:combine(*args)
        except AssertionError:pass
        else:raise AssertionError('bad signal combination accepted')
    source=Path(__file__).resolve()
    create(source.with_name('rank20_two_seed_raw_signal_actual_CPU_controls_v1_20261010.json'),{
        'status':'passed_actual3_full_scalar_oracles12_prefix_controls3_future_poison_controls5_bad_input_refusals',
        'input_sha256':{str(source):sha(source)},'records':rows,'bad_input_refusals':5,
        'new_native_fits':0,'new_quality_scores':0,'actual_future_X_read':False,'test_labels_read':False})
if __name__=='__main__':actual_cpu_controls()
