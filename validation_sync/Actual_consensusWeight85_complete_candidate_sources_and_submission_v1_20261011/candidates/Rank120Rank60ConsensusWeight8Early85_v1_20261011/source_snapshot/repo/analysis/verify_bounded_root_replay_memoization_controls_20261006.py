"""Check mutation, copy/prefix, key and retention-budget semantics on tiny fixtures."""
from pathlib import Path
from copy import copy,deepcopy
import json
import sys

ROOT=Path(__file__).resolve().parents[1]
A=ROOT/'analysis';sys.path.insert(0,str(A))
from run_dependency_queue_v3_20261006 import sha,create
from bounded_root_replay_memoization_20261006 import enable,statistics
OUT=A/'bounded_root_replay_memoization_semantic_controls_20261006'

def main():
    import numpy as np
    import polars as pl
    assert not OUT.exists();OUT.mkdir()
    sources=[Path(__file__),A/'bounded_root_replay_memoization_20261006.py',
        A/'live_scoring_and_GPU_shared_memory_profile_20261006/verification.json']
    pins={str(p):sha(p) for p in sources}
    create(OUT/'frozen_before_semantic_controls.json',{'input_sha256':pins,
        'tiny_fixture_is_not_full5635800_row_or_official_metric_control':True,
        'new_native_fits':0,'new_quality_scores':0,'test_labels_read':False})
    class Fixture:
        def __init__(self,n=16):
            self.dates=np.arange(n,dtype=np.int64);self.flags=np.zeros(n,dtype=np.int64)
            self.valid=np.ones(n,dtype=bool);self.codes=np.arange(n,dtype=np.int64)
            self.tie_key=np.arange(n,dtype=float);self.ranks={}
            self.frame=pl.DataFrame({'aux_raw':np.arange(n,dtype=float),'y_ret_1d':np.arange(n,dtype=float)/100})
            self._whole_graph={'root':{'kind':'complete_r30','configuration':{'factor':2.}},'layers':[]}
            self._whole_paths={};self.donor_calls=self.prediction_calls=0
        def donor(self,promote,rerank_weight=None):
            self.donor_calls+=1
            return promote*self._whole_graph['root']['configuration']['factor']+self.flags+np.asarray(0 if rerank_weight is None else rerank_weight)
        def root_prediction(self,donor):
            self.prediction_calls+=1
            return donor+np.arange(len(self.dates)),{'actual_fixture_root':True,'rows':len(donor)}
    ctx=Fixture();promote=np.arange(16,dtype=float)
    expected_donor=ctx.donor(promote);expected=ctx.root_prediction(expected_donor)
    enable(ctx,pins);first=ctx.donor(promote);one=ctx.root_prediction(first)
    assert np.array_equal(first,expected_donor) and np.array_equal(one[0],expected[0]) and one[1]==expected[1]
    d,p=ctx.donor_calls,ctx.prediction_calls
    second=ctx.donor(promote);two=ctx.root_prediction(second)
    assert ctx.donor_calls==d and ctx.prediction_calls==p and statistics(ctx)['hits']==2
    second[:]=-999.;two[0][:]=-888.;two[1]['rows']=-1
    third=ctx.donor(promote);three=ctx.root_prediction(third)
    assert np.array_equal(third,expected_donor) and np.array_equal(three[0],expected[0]) and three[1]==expected[1]
    ctx._whole_graph['layers']=[{'private_downstream_weight':.025}]
    before=ctx.donor_calls;assert np.array_equal(ctx.donor(promote),expected_donor) and ctx.donor_calls==before
    ctx._whole_graph['root']['configuration']['factor']=3.
    assert np.array_equal(ctx.donor(promote),promote*3.) and ctx.donor_calls==before+1
    ctx.flags[0]=7
    assert ctx.donor(promote)[0]==7
    labels=ctx.frame['y_ret_1d'].to_numpy().copy();labels[:]=np.nan
    ctx.frame=ctx.frame.with_columns(pl.Series('y_ret_1d',labels));before=ctx.donor_calls
    ctx.donor(promote);assert ctx.donor_calls==before+1,'Same-owner label mutation must force recomputation'
    prefix=copy(ctx);prefix.dates=ctx.dates[:8];prefix.flags=ctx.flags[:8];prefix.valid=ctx.valid[:8]
    prefix.codes=ctx.codes[:8];prefix.tie_key=ctx.tie_key[:8];prefix.frame=ctx.frame.head(8)
    parent_stats=deepcopy(statistics(ctx));before=prefix.donor_calls
    short=prefix.donor(promote[:8]);pred,stats=prefix.root_prediction(short)
    assert prefix.donor_calls==before+1 and len(pred)==8 and stats['rows']==8
    assert statistics(prefix)['misses']==2 and statistics(prefix)['hits']==0
    assert statistics(ctx)==parent_stats,'Copied prefix must not share the parent cache'
    fresh=Fixture();enable(fresh,pins,maximum_bytes=0)
    fresh.donor(promote);fresh.donor(promote)
    assert fresh.donor_calls==2 and statistics(fresh)['retained_payload_bytes']==0
    tiny=Fixture();enable(tiny,pins,maximum_bytes=promote.nbytes)
    tiny.donor(promote);tiny.donor(promote+1)
    assert statistics(tiny)['evictions']==1 and statistics(tiny)['retained_payload_bytes']<=promote.nbytes
    original=Fixture();original.donor(promote);original.donor(promote)
    assert original.donor_calls==2,'Global fixture class must remain unchanged'
    for path,digest in pins.items():assert sha(path)==digest,path
    proof={'status':'passed_tiny_root_cache_semantics_full_real_array_controls_pending','input_sha256':pins,
        'copy_and_prefix_owners_cold_and_independent':True,'returned_array_and_stats_mutations_cannot_poison_cache':True,
        'root_configuration_numeric_inputs_and_same_owner_labels_invalidate':True,
        'downstream_role_changes_reuse_only_unchanged_root':True,'zero_budget_and_bounded_evictions_passed':True,
        'global_classes_and_live_scientific_processes_not_modified':True,
        'full5635800_bit_outputs_8_metrics_and_real_cold_prefix_and_timing_and_RAM_still_required':True,
        'runtime_adopted':False,'new_native_fits':0,'new_quality_scores':0,'test_labels_read':False}
    create(OUT/'verification.json',proof);print(json.dumps(proof,ensure_ascii=False),flush=True)

if __name__=='__main__':
    try:main()
    except BaseException as exc:
        if OUT.exists() and not (OUT/'failure.json').exists():create(OUT/'failure.json',{'status':'failed_preserved_root_cache_semantic_controls','error':f'{type(exc).__name__}: {exc}'})
        raise
