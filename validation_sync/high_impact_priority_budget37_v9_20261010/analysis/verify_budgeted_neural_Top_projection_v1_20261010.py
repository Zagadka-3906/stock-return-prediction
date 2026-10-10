"""Own sequential independent, eligibility, ties, stock-slot, annual-boundary and future-poison controls."""
from pathlib import Path
import sys,itertools,time
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A),str(A.parent)]
from run_dependency_queue_v3_20261006 import sha,create

def main():
    import numpy as np
    import budgeted_neural_Top_projection_v1_20261010 as codec
    rng=np.random.default_rng(20261010);dates=np.repeat([20201229,20201230,20201231,20210104,20210105],200)
    parent=np.round(rng.normal(size=len(dates)),1);raw=np.round(rng.normal(size=len(dates)),1)
    flags=np.zeros(len(dates),dtype=np.int8);flags[::17]=1;flags[::73]=2
    valid=rng.random(len(dates))>.2;parent[~valid]=raw[~valid]=-1e6
    parent[:4]=[0.,-0.,0.,-0.];rows=[]
    for w,b,m,s in itertools.product((.125,.5,1.),(.005,.01,.02,.1),(0.,.05),(1.,-1.)):
        args=(w,b,m,s);actual,trace=codec.transform(parent,raw,dates,flags,valid,*args,return_trace=True)
        oracle,independent=codec.pandas_oracle(parent,raw,dates,flags,valid,*args,return_trace=True)
        assert np.array_equal(actual.view('u8'),oracle.view('u8')) and trace==independent
        assert np.array_equal(actual[:200].view('u8'),parent[:200].view('u8'))
        fixed=~((flags==0)&valid);assert np.array_equal(actual[fixed].view('u8'),parent[fixed].view('u8'))
        for n in (200,400,800):assert np.array_equal(actual[:n].view('u8'),codec.transform(parent[:n],raw[:n],dates[:n],flags[:n],valid[:n],*args).view('u8'))
        pp=parent.copy();rr=raw.copy();pp[400:]=rng.normal(300,70,len(parent)-400);rr[400:]=rng.normal(-300,70,len(raw)-400)
        poison=codec.transform(pp,rr,dates,flags,valid,*args);assert np.array_equal(actual[:400].view('u8'),poison[:400].view('u8'))
        for r in trace:assert r['optional_swaps']<=r['budget']
        rows.append({'weight':w,'budget_fraction':b,'margin':m,'sign':s,'full_independent_bits_and_trace_exact':True,'three_prefixes_and_two_forecast_future_poison_exact':True,'nonzero_flags_and_invalid_bits_exact':True,'initial_parent_Top_identity_exact':True,'state_continues_across_annual_boundary':True,'optional_budget_checked':True})
    try:codec.transform(parent[:900],raw[:900],dates[:900],flags[:900],valid[:900],.5,.01,0.)
    except AssertionError:pass
    else:raise AssertionError('inconsistent stock slots accepted')
    create(A/'budgeted_neural_Top_projection_controls_v1_20261010.json',{'status':'passed48_sequential_independent_cases144_prefixes_and_future_poison_and_stock_slot_rejection','at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'input_sha256':{str(p):sha(p) for p in [Path(__file__),Path(codec.__file__)]},'records':rows,'new_quality_scores':0,'actual_future_X_read':False,'test_labels_read':False})
    print('PASS independent sequential projection, annual boundaries, prefixes, poison and budgets',flush=True)

if __name__=='__main__':main()
