"""Actual immutable-manifest replay and cross-process sharing controls."""
from pathlib import Path
import json
import os
import subprocess
import sys
import time
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT),str(ROOT/'analysis')]
from locked_read_hash_cache_20261004 import LockedReadHashCache,fresh_sha,REFERENCES
OUT=ROOT/'analysis/locked_read_hash_cache_preflight_20261004'

def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def write(p,v):
    with p.open('x',encoding='utf-8') as f:json.dump(v,f,ensure_ascii=False,indent=2)

def main():
    OUT.mkdir(exist_ok=True)
    if (OUT/'verification.json').exists():
        for p,d in read(OUT/'verification.json')['input_sha256'].items():assert fresh_sha(p)==d,p
        print('Frozen locked-read hash scope verified');return
    import train_no_dropout_seed_bank_20261004 as bank
    protocol=read(bank.OUT/'protocol.json')
    sources=[Path(__file__),ROOT/'analysis/locked_read_hash_cache_20261004.py',bank.OUT/'protocol.json']
    hashes={str(p.resolve()):fresh_sha(p) for p in sources}
    write(OUT/'frozen_before_controls.json',{'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),
        'input_sha256':hashes,'manifest_input_sha256':protocol['input_sha256'],'repeated_actual_verify_calls':3,
        'primary_references':REFERENCES,'new_quality_scores':0,'live_queued_sources_changed':False,
        'scope':'Isolated-process file integrity andwall-time controls only; no forecasts, labels or model selection.'})
    locked=OUT/'sharing_fixture.bin';mutable=OUT/'mutable_fixture.bin';renamed=OUT/'renamed_fixture.bin'
    locked.write_bytes(b'0123456789');mutable.write_bytes(b'abcdefghij')
    expected=fresh_sha(locked)
    code="import pathlib,sys; p=pathlib.Path(sys.argv[1]);\ntry:\n p.open('r+b').close()\nexcept PermissionError:\n sys.exit(0)\nsys.exit(2)"
    with LockedReadHashCache({str(locked):expected}) as cache:
        child=subprocess.run([sys.executable,'-B','-X','utf8','-c',code,str(locked)],capture_output=True,text=True)
        assert child.returncode==0,(child.returncode,child.stderr)
        denied=[]
        for operation in (lambda:locked.open('r+b'),lambda:locked.rename(renamed),lambda:locked.unlink()):
            try:operation()
            except PermissionError:denied.append(True)
            else:raise AssertionError('Locked write/delete/rename unexpectedly allowed')
        assert cache.sha(locked)==expected==fresh_sha(locked)
        first=cache.sha(mutable);stamp=mutable.stat()
        mutable.write_bytes(b'ABCDEFGHIJ');os.utime(mutable,ns=(stamp.st_atime_ns,stamp.st_mtime_ns))
        assert cache.sha(mutable)!=first and cache.fresh_calls==2
    with locked.open('r+b') as f:f.write(b'9')
    assert fresh_sha(locked)!=expected
    print('Sharing andmutable-file controls passed',flush=True)
    start=time.perf_counter();baseline=[]
    for _ in range(3):
        t=time.perf_counter();value=bank.verify();assert value==protocol
        baseline.append(time.perf_counter()-t)
    baseline_total=time.perf_counter()-start
    original=bank.engine.sha;cached=[];start=time.perf_counter()
    with LockedReadHashCache(protocol['input_sha256']) as cache:
        acquired=time.perf_counter();setup=acquired-start
        try:
            bank.engine.sha=cache.sha
            for _ in range(3):
                t=time.perf_counter();value=bank.verify();assert value==protocol
                cached.append(time.perf_counter()-t)
        finally:bank.engine.sha=original
        assert bank.engine.sha is original
        hits=cache.hits;fresh=cache.fresh_calls;before_close=time.perf_counter()
    complete=time.perf_counter();cached_total=complete-start
    assert fresh==0 and hits==3*len(protocol['input_sha256'])
    assert bank.engine.sha is original
    for p,d in hashes.items():assert fresh_sha(p)==d,p
    report={'status':'passed','at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),
        'cross_process_write_denied':True,'same_process_write_rename_delete_denied':all(denied),
        'nonsealed_same_size_same_mtime_change_rehashed':True,'handles_released_after_scope':True,
        'actual_frozen_protocol_replays_bit_identical':True,'actual_verify_calls_per_arm':3,
        'baseline_verify_seconds':baseline,'baseline_complete_seconds':baseline_total,
        'cached_verify_seconds':cached,'cached_setup_full_hash_seconds':setup,
        'cached_final_full_hash_seconds':complete-before_close,'cached_complete_seconds':cached_total,
        'manifest_files':len(protocol['input_sha256']),
        'manifest_input_bytes':sum(Path(p).stat().st_size for p in protocol['input_sha256']),
        'cache_hits':hits,'original_namespace_restored':True,
        'background_andfilesystem_cache_not_matched':True,'new_quality_scores':0,'test_labels_read':False,
        'adopted_in_live_queued_rounds':False,'hardware_boundary_established':False,
        'scope':'Three actual no-dropout frozen-manifest verification calls per arm in one process. Setup andfinal full rehash included; independent sharing controls. Timing is specific to this order andbackground.',
        'primary_references':REFERENCES,'input_sha256':hashes}
    write(OUT/'verification.json',report)
    print(json.dumps(report,ensure_ascii=False),flush=True)

if __name__=='__main__':main()
