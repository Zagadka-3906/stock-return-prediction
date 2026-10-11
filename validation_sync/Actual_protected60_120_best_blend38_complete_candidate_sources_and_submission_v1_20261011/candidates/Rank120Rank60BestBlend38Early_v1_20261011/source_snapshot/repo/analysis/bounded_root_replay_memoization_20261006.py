"""Experimental validation-only root reuse; full controls required before adoption.

Instance class replacement binds methods correctly after copy/slice. Copies
start with independent cold caches. Retained array/serialized-stat payload is
bounded; this is not a bound on total process RSS. No global classes change.
"""
from collections import OrderedDict
from copy import deepcopy
import hashlib
import json
import pickle
import time

MAXIMUM_BYTES=128*1024**2
ARRAYS=('dates','flags','valid','codes','tie_key','slow_finished','w5a','slow',
        'top_values','top_ranks','membership_values','membership_ranks')

def digest_array(value,hash_value):
    import numpy as np
    value=np.asarray(value)
    assert not value.dtype.hasobject,'Object pointer bytes are not an input identity'
    hash_value.update(str((value.dtype.str,value.shape)).encode('ascii'))
    hash_value.update(memoryview(np.ascontiguousarray(value)).cast('B'))

def input_key(context,method,args,certificate):
    hash_value=hashlib.sha256()
    hash_value.update(certificate.encode('ascii'))
    hash_value.update(json.dumps(context._whole_graph['root'],sort_keys=True,separators=(',',':')).encode('utf-8'))
    hash_value.update(method.encode('ascii'))
    seen=set();n=len(context.dates)
    for owner in (context,getattr(context,'_whole_base',None)):
        if owner is None:continue
        for name in ARRAYS:
            value=getattr(owner,name,None)
            if value is not None and id(value) not in seen:
                seen.add(id(value));hash_value.update(name.encode('ascii'));digest_array(value[:n],hash_value)
        for name in sorted(getattr(owner,'ranks',{})):
            hash_value.update(name.encode('utf-8'));digest_array(owner.ranks[name][:n],hash_value)
        frame=getattr(owner,'frame',None)
        if frame is not None:
            for name in ('aux_raw','y_ret_1d'):
                if name in frame.columns:
                    hash_value.update(name.encode('ascii'));digest_array(frame[name].to_numpy()[:n],hash_value)
    hash_value.update(json.dumps(getattr(context,'_whole_paths',{}),sort_keys=True,default=str).encode('utf-8'))
    for value in args:
        if hasattr(value,'dtype'):digest_array(value,hash_value)
        else:hash_value.update(json.dumps(value,sort_keys=True,allow_nan=False).encode('utf-8'))
    return hash_value.hexdigest()

class Memo:
    def __init__(self,owner,budget):
        self.owner=owner;self.budget=budget;self.entries=OrderedDict();self.retained=0
        self.hits=self.misses=self.evictions=0;self.hash_seconds=self.original_seconds=0.
    def stats(self):
        return {'hits':self.hits,'misses':self.misses,'evictions':self.evictions,
            'retained_payload_bytes':self.retained,'maximum_payload_bytes':self.budget,
            'hash_seconds':self.hash_seconds,'original_function_seconds':self.original_seconds}

def enable(context,certified_source_sha256,maximum_bytes=MAXIMUM_BYTES):
    assert certified_source_sha256 and 0<=maximum_bytes<=MAXIMUM_BYTES
    assert all(len(value)==64 for value in certified_source_sha256.values())
    assert context._whole_graph['root']['kind'] in ('complete_r30','standalone')
    assert not getattr(context,'_bounded_root_memoization_enabled',False)
    certificate=hashlib.sha256(json.dumps(certified_source_sha256,sort_keys=True).encode('utf-8')).hexdigest()
    original=type(context)
    def call(self,method,args):
        import numpy as np
        memo=getattr(self,'_bounded_root_memo',None)
        if memo is None or memo.owner!=id(self):
            memo=Memo(id(self),maximum_bytes);self._bounded_root_memo=memo
        started=time.perf_counter();key=input_key(self,method,args,certificate)
        memo.hash_seconds+=time.perf_counter()-started
        if key in memo.entries:
            memo.hits+=1;array,stats,size=memo.entries.pop(key);memo.entries[key]=(array,stats,size)
            return array.copy() if method=='donor' else (array.copy(),deepcopy(stats))
        memo.misses+=1;started=time.perf_counter()
        result=getattr(original,method)(self,*args)
        memo.original_seconds+=time.perf_counter()-started
        array=result if method=='donor' else result[0]
        assert isinstance(array,np.ndarray)
        stats=None if method=='donor' else result[1]
        size=array.nbytes+(0 if stats is None else len(pickle.dumps(stats,protocol=5)))
        if size<=memo.budget:
            while memo.entries and memo.retained+size>memo.budget:
                _,(_,_,removed)=memo.entries.popitem(last=False);memo.retained-=removed;memo.evictions+=1
            saved=array.copy();saved.flags.writeable=False
            memo.entries[key]=(saved,deepcopy(stats),size);memo.retained+=size
        assert memo.retained<=memo.budget
        return result
    class RootMemoized(original):
        def donor(self,promote,rerank_weight=None):return call(self,'donor',(promote,rerank_weight))
        def root_prediction(self,donor):return call(self,'root_prediction',(donor,))
    context.__class__=RootMemoized
    context._bounded_root_memoization_enabled=True
    return context

def statistics(context):
    memo=getattr(context,'_bounded_root_memo',None)
    return memo.stats() if memo is not None and memo.owner==id(context) else {'cold_owner':True}
