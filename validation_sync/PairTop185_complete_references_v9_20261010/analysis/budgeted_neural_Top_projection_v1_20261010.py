"""Causal bounded optional Top swaps; eligibility corrections are explicit, not a promised turnover cap."""
import numpy as np
import BF16Medium153_complete_parent_rank_CDF_v1_20261009 as ranks

def original_top(parent,pool):
    import pandas as pd
    return pd.Series(parent[pool],index=pool).sort_values(ascending=False).index.to_numpy()[:max(len(pool)//10,1)]

def apply_prepared(parent,flags,valid,weight,budget_fraction,margin,prepared,return_trace=False):
    assert 0.<weight<=1. and 0.<=budget_fraction<=.1 and 0.<=margin<=1.
    p=np.asarray(parent,dtype=np.float64);out=p.copy();previous=None;slots=None;trace=[]
    for left,right,pp,npct,knots,ordered in prepared:
        if slots is None:slots=right-left
        assert right-left==slots,'Stock identity is fixed sorted row position in an independently verified panel.'
        before=p[left:right];pool=np.flatnonzero(np.asarray(flags[left:right])==0)
        if not len(pool):previous=set();trace.append({'optional_swaps':0,'budget':0,'empty_pool':True});continue
        original=original_top(before,pool);quota=len(original)
        eligible=pool[np.asarray(valid[left:right],dtype=bool)[pool]]
        if previous is None or len(eligible)<quota or not np.asarray(valid[left:right],dtype=bool)[original].all():
            previous=set(map(int,original));trace.append({'optional_swaps':0,'budget':int(np.floor(budget_fraction*quota)),'declared_parent_initialization_or_price_fallback':True});continue
        q=(1.-float(weight))*pp+float(weight)*npct
        present=np.array(sorted(previous.intersection(map(int,eligible))),dtype=np.int64)
        order=lambda indices,descending:indices[np.lexsort((indices,-q[indices] if descending else q[indices]))]
        if len(present)>quota:present=order(present,True)[:quota]
        if len(present)<quota:
            candidates=eligible[~np.isin(eligible,present)];present=np.r_[present,order(candidates,True)[:quota-len(present)]]
        desired=set(map(int,present));budget=int(np.floor(budget_fraction*quota));swaps=0
        for _ in range(budget):
            challengers=eligible[~np.isin(eligible,np.array(sorted(desired),dtype=np.int64))]
            if not len(challengers):break
            entrant=int(order(challengers,True)[0]);incumbent=int(order(np.array(sorted(desired),dtype=np.int64),False)[0])
            if not q[entrant]-q[incumbent]>margin:break
            desired.remove(incumbent);desired.add(entrant);swaps+=1
        original_set=set(map(int,original));extras=np.array(sorted(desired-original_set),dtype=np.int64);exits=np.array(sorted(original_set-desired),dtype=np.int64)
        assert len(extras)==len(exits)
        if len(extras):
            extras=order(extras,True);exits=exits[np.lexsort((exits,-before[exits]))]
            out[left+extras]=before[exits];out[left+exits]=before[extras]
            selected=np.array(sorted(desired),dtype=np.int64);other=pool[~np.isin(pool,selected)]
            if len(other):
                boundary=np.max(out[left+other]);lift=selected[out[left+selected]<=boundary]
                if len(lift):out[left+lift]=np.nextafter(boundary,np.inf)
        assert set(map(int,original_top(out[left:right],pool)))==desired
        assert swaps<=budget
        trace.append({'optional_swaps':swaps,'budget':budget,'quota':quota,'price_and_flag_forced_corrections_may_exceed_optional_budget':True})
        previous=desired
    return (out,trace) if return_trace else out

def transform(parent,raw,dates,flags,valid,weight,budget_fraction,margin,sign=1.,return_trace=False):
    return apply_prepared(parent,flags,valid,weight,budget_fraction,margin,ranks.prepare(parent,raw,dates,flags,valid,sign),return_trace)

def pandas_oracle(parent,raw,dates,flags,valid,weight,budget_fraction,margin,sign=1.,return_trace=False):
    import pandas as pd,math
    assert 0.<weight<=1. and 0.<=budget_fraction<=.1 and 0.<=margin<=1. and sign in (-1.,1.)
    p=np.asarray(parent,dtype=np.float64);neural=np.asarray(raw,dtype=np.float64).copy();neural[np.asarray(valid,dtype=bool)]*=float(sign)
    pr=pd.Series(p).groupby(dates,sort=False).rank(method='average',pct=True)
    nr=pd.Series(neural).groupby(dates,sort=False).rank(method='average',pct=True)
    out=p.copy();previous=None;slots=None;trace=[]
    for global_indices in pd.Series(np.arange(len(p))).groupby(dates,sort=False).indices.values():
        if slots is None:slots=len(global_indices)
        assert len(global_indices)==slots
        local=np.arange(slots);day=p[global_indices];pool=local[np.asarray(flags)[global_indices]==0]
        if not len(pool):previous=set();trace.append({'optional_swaps':0,'budget':0,'empty_pool':True});continue
        values=pd.Series(day[pool],index=pool);original=values.sort_values(ascending=False).index.to_numpy()[:max(len(pool)//10,1)]
        quota=len(original);eligible=pool[np.asarray(valid,dtype=bool)[global_indices][pool]]
        if previous is None or len(eligible)<quota or not all(np.asarray(valid,dtype=bool)[global_indices][original]):
            previous=set(map(int,original));trace.append({'optional_swaps':0,'budget':int(math.floor(budget_fraction*quota)),'declared_parent_initialization_or_price_fallback':True});continue
        q=pd.Series((1.-float(weight))*pr.iloc[global_indices].to_numpy()+float(weight)*nr.iloc[global_indices].to_numpy(),index=local)
        present=q.loc[sorted(previous.intersection(map(int,eligible)))].sort_values(ascending=False,kind='mergesort').iloc[:quota]
        if len(present)<quota:
            candidates=q.loc[sorted(set(map(int,eligible))-set(present.index))].sort_values(ascending=False,kind='mergesort')
            present=pd.concat([present,candidates.iloc[:quota-len(present)]])
        desired=set(map(int,present.index));budget=int(math.floor(budget_fraction*quota));swaps=0
        for _ in range(budget):
            challengers=q.loc[sorted(set(map(int,eligible))-desired)].sort_values(ascending=False,kind='mergesort')
            if not len(challengers):break
            weakest=q.loc[sorted(desired)].sort_values(kind='mergesort');entrant=int(challengers.index[0]);incumbent=int(weakest.index[0])
            if not float(challengers.iloc[0])-float(weakest.iloc[0])>margin:break
            desired.remove(incumbent);desired.add(entrant);swaps+=1
        original_set=set(map(int,original))
        extras=q.loc[sorted(desired-original_set)].sort_values(ascending=False,kind='mergesort').index.to_numpy()
        exits=pd.Series(day,index=local).loc[sorted(original_set-desired)].sort_values(ascending=False,kind='mergesort').index.to_numpy()
        assert len(extras)==len(exits)
        if len(extras):
            out[global_indices[extras]]=day[exits];out[global_indices[exits]]=day[extras]
            other=sorted(set(map(int,pool))-desired)
            if other:
                boundary=max(out[global_indices[other]])
                lift=[i for i in desired if out[global_indices[i]]<=boundary]
                if lift:out[global_indices[lift]]=math.nextafter(float(boundary),math.inf)
        actual=pd.Series(out[global_indices[pool]],index=pool).sort_values(ascending=False).index.to_numpy()[:quota]
        assert set(map(int,actual))==desired and swaps<=budget
        trace.append({'optional_swaps':swaps,'budget':budget,'quota':quota,'price_and_flag_forced_corrections_may_exceed_optional_budget':True});previous=desired
    return (out,trace) if return_trace else out
