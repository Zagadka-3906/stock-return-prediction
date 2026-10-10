"""Vectorize rank filling and bucket assignment; retain an independent Pandas grouping oracle."""
from pathlib import Path
import sys,itertools,time
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A),str(A.parent)]
from run_dependency_queue_v3_20261006 import create,sha

def main():
    source=A/'protected_lower_rank_quantization_v1_20261010.py';s=source.read_text(encoding='utf8')
    old="""        rank=np.empty(len(values),dtype=np.float64)
        for start,end in zip(changes[:-1],changes[1:]):rank[start:end]=(start+1.+end)/2."""
    new="        rank=np.repeat((changes[:-1]+1.+changes[1:])/2.,changes[1:]-changes[:-1])"
    assert s.count(old)==1;s=s.replace(old,new)
    old="""        for start,end in zip(cuts[:-1],cuts[1:]):
            representative_index=start if representative=='minimum' else start+(end-start-1)//2
            result[left+order[start:end]]=values[representative_index]"""
    new="""        representative_indices=cuts[:-1] if representative=='minimum' else cuts[:-1]+(cuts[1:]-cuts[:-1]-1)//2
        result[left+order]=np.repeat(values[representative_indices],cuts[1:]-cuts[:-1])"""
    assert s.count(old)==1;s=s.replace(old,new)
    old="""        for group in buckets.unique():
            members=lower[buckets==group].sort_values(kind='mergesort')
            value=members.iloc[0 if representative=='minimum' else (len(members)-1)//2]
            result[members.index.to_numpy()]=value"""
    new="""        grouped=lower.groupby(buckets,sort=False)
        representatives=grouped.min() if representative=='minimum' else grouped.quantile(.5,interpolation='lower')
        result[lower.index.to_numpy()]=buckets.map(representatives).to_numpy()"""
    assert s.count(old)==1;s=s.replace(old,new)
    target=A/'protected_lower_rank_quantization_v2_20261010.py';assert not target.exists();compile(s,str(target),'exec');target.write_text(s,encoding='utf8',newline='\n')
    import protected_lower_rank_quantization_v1_20261010 as previous
    import protected_lower_rank_quantization_v2_20261010 as actual
    import numpy as np
    rng=np.random.default_rng(20261010);dates=np.repeat([20200102,20200103,20200106],4650)
    parent=np.round(rng.normal(size=len(dates)),1);parent[:4]=[0.,-0.,0.,-0.]
    flags=np.zeros(len(parent),dtype=np.int8);flags[::7]=1;flags[::43]=2;valid=rng.random(len(parent))>.35;parent[~valid]=-1e6
    parent[valid&((np.arange(len(parent))%4)==0)]=1.5;rows=[]
    for bins,fraction,representative in itertools.product((8,16,32,64,128,256),(.15,.25,.4),('minimum','lower_median')):
        args=(bins,fraction,representative);value=actual.transform(parent,dates,flags,valid,*args)
        oracle=actual.pandas_oracle(parent,dates,flags,valid,*args);oldvalue=previous.transform(parent,dates,flags,valid,*args)
        assert np.array_equal(value.view('u8'),oracle.view('u8')) and np.array_equal(value.view('u8'),oldvalue.view('u8'))
        actual.assert_invariants(parent,value,dates,flags,valid)
        for n in (4650,9300):assert np.array_equal(value[:n].view('u8'),actual.transform(parent[:n],dates[:n],flags[:n],valid[:n],*args).view('u8'))
        poison=parent.copy();poison[4650:]=rng.normal(300,70,len(poison)-4650)
        assert np.array_equal(value[:4650].view('u8'),actual.transform(poison,dates,flags,valid,*args)[:4650].view('u8'))
        rows.append({'bins':bins,'protect_fraction':fraction,'representative':representative,'full13950_rows_old_new_and_independent_bits_exact':True,'two_prefixes_and_future_poison_exact':True,'official_Top_and_invalid_bits_exact':True})
    create(A/'protected_lower_rank_quantization_controls_v2_20261010.json',{'status':'passed36_vectorized_and_original_and_independent13950_rows72_prefixes_and_future_poison','at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'input_sha256':{str(p):sha(p) for p in [Path(__file__),source,target,A/'protected_lower_rank_quantization_controls_v1_20261010.json']},'records':rows,'new_quality_scores':0,'test_labels_read':False,'actual_future_X_read':False})
    print('PASS 36 actual13950-row independent and original-bit controls,72 prefixes,poison',flush=True)

if __name__=='__main__':main()
