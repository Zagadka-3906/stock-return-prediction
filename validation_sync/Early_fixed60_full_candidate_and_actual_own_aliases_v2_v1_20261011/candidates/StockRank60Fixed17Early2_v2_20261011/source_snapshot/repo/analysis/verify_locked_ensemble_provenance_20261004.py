"""Measure actual recursive ensemble provenance with scoped hash reuse."""
from pathlib import Path
import json
import sys
import time
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT),str(ROOT/'analysis')]
from locked_read_hash_cache_20261004 import LockedReadHashCache,fresh_sha,REFERENCES
OUT=ROOT/'analysis/locked_ensemble_provenance_preflight_20261004'

def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def write(p,v):
    with p.open('x',encoding='utf-8') as f:json.dump(v,f,ensure_ascii=False,indent=2)

def main():
    OUT.mkdir(exist_ok=True)
    if (OUT/'verification.json').exists():
        for p,d in read(OUT/'verification.json')['input_sha256'].items():assert fresh_sha(p)==d,p
        print('Frozen ensemble provenance controls verified');return
    import train_no_dropout_seed_ensembles_20261004 as virtual
    first=ROOT/'analysis/locked_read_hash_cache_preflight_20261004/verification.json'
    assert read(first)['status']=='passed'
    modules=[]
    for name,module in sorted(sys.modules.copy().items()):
        file=getattr(module,'__file__',None)
        if file and Path(file).resolve().parent==ROOT/'analysis' and callable(getattr(module,'sha',None)):
            modules.append((name,module,module.sha))
    assert modules
    sources=[Path(__file__),first,ROOT/'analysis/locked_read_hash_cache_20261004.py',
        virtual.OUT/'protocol.json',virtual.OUT/'assembly_inputs.json',virtual.OUT/'oof_audit.json',
        *dict.fromkeys(Path(m.__file__) for _,m,_ in modules)]
    hashes={str(p.resolve()):fresh_sha(p) for p in sources}
    write(OUT/'frozen_before_controls.json',{'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),
        'input_sha256':hashes,'actual_assembly_freeze_calls_per_arm':3,
        'algorithm':'Record each actual original validated SHA call, acquire read-only-sharing handles for precisely those files, replay identical actual assembly_freeze, rehash on scope exit.',
        'primary_references':REFERENCES,'live_queued_sources_changed':False,'new_quality_scores':0,'test_labels_read':False})
    expected={};baseline=[];events=[]
    def traced(original):
        def sha(path):
            key=str(Path(path).resolve());digest=original(path)
            if key in expected:assert expected[key]==digest,key
            expected[key]=digest;events.append(key);return digest
        return sha
    start=time.perf_counter()
    try:
        for _,module,original in modules:module.sha=traced(original)
        for _ in range(3):
            t=time.perf_counter();virtual.assembly_freeze();baseline.append(time.perf_counter()-t)
            print('Original ensemble provenance replay passed',flush=True)
    finally:
        for _,module,original in modules:module.sha=original
    baseline_total=time.perf_counter()-start
    write(OUT/'actual_validated_hash_inputs.json',{'input_sha256':expected,'actual_hash_call_count':len(events)})
    start=time.perf_counter();cached=[]
    with LockedReadHashCache(expected) as cache:
        acquired=time.perf_counter()
        try:
            for _,module,_ in modules:module.sha=cache.sha
            for _ in range(3):
                t=time.perf_counter();virtual.assembly_freeze();cached.append(time.perf_counter()-t)
        finally:
            for _,module,original in modules:module.sha=original
        assert cache.hits==len(events) and cache.fresh_calls==0
        hits=cache.hits;before_close=time.perf_counter()
    complete=time.perf_counter()
    assert all(module.sha is original for _,module,original in modules)
    for p,d in hashes.items():assert fresh_sha(p)==d,p
    hashes[str((OUT/'actual_validated_hash_inputs.json').resolve())]=fresh_sha(OUT/'actual_validated_hash_inputs.json')
    value={'status':'passed','at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),
        'actual_original_recursive_provenance_andassembly_calls_passed':True,
        'actual_locked_recursive_provenance_andassembly_calls_passed':True,
        'actual_assembly_freeze_calls_per_arm':3,'original_namespace_restored':True,
        'unique_immutable_inputs':len(expected),'unique_input_bytes':sum(Path(p).stat().st_size for p in expected),
        'actual_hash_calls_per_arm':len(events),'baseline_seconds':baseline,
        'baseline_complete_seconds':baseline_total,'cached_seconds':cached,
        'cached_setup_full_hash_seconds':acquired-start,'cached_final_full_hash_seconds':complete-before_close,
        'cached_complete_seconds':complete-start,'cache_hits':hits,
        'background_andfilesystem_cache_not_matched':True,'adopted_in_live_queued_rounds':False,
        'new_quality_scores':0,'test_labels_read':False,'hardware_boundary_established':False,
        'scope':'Actual read-only recursive assembly_freeze with existing actual native/virtual models. First arm includes digest recording overhead; second includes acquiring every handle andfinal full rehash. Timing is specific to order andbackground.',
        'primary_references':REFERENCES,'input_sha256':hashes}
    write(OUT/'verification.json',value);print(json.dumps(value,ensure_ascii=False),flush=True)

if __name__=='__main__':main()
