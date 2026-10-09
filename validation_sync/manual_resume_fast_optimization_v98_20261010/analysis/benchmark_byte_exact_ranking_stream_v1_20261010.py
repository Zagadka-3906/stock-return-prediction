"""Measure the existing byte-exact encoder on the entire sealed155 board."""
from pathlib import Path
import sys,time,json,re,hashlib,os
A=Path(__file__).resolve().parent;ROOT=A.parent
sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create

def main():
    import psutil
    from datetime import datetime,timezone,timedelta
    control=read(A/'current_user_runtime_control_20261010.json')
    assert datetime.now(timezone(timedelta(hours=8)))<datetime.fromisoformat(control['stop_at_local'])
    while psutil.virtual_memory().available<8*2**30:time.sleep(10)
    from exact_native_pretty_JSON_archive_20261007 import pieces
    from build_lossless_ranking_display_v2_20261006 import unpack_report
    source=A/'lossless_ranking_display_v2_20261006/round155'
    expected=read(source/'full_report_publication_snapshot_verification.json')
    paths=[Path(__file__),source/'complete_rankings_lossless.html',source/'verification.json',source/'full_report_publication_snapshot_verification.json',A/'exact_native_pretty_JSON_archive_20261007.py',A/'build_all_model_rankings_20261003.py']
    pins={str(p):sha(p) for p in paths}
    text=(source/'complete_rankings_lossless.html').read_text(encoding='utf8')
    payload=re.search(r'<script\s+id="data"\s+type="application/json">(.*?)</script>',text,re.S)
    assert payload
    report=unpack_report(json.loads(payload.group(1)))
    del text,payload
    # Both orders on the same actual record sample, including every top-level field.
    sample={key:(value[:40] if isinstance(value,list) else value) for key,value in report.items()}
    records=[]
    for order in [('original','stream'),('stream','original')]:
        timings={};digests={};sizes={}
        for method in order:
            started=time.perf_counter();digest=hashlib.sha256();count=0
            if method=='original':
                blobs=[(json.dumps(sample,ensure_ascii=False,indent=2,allow_nan=False)+'\n').replace('\n',os.linesep).encode('utf8')]
            else:blobs=pieces(sample)
            for raw in blobs:digest.update(raw);count+=len(raw)
            timings[method]=time.perf_counter()-started;digests[method]=digest.hexdigest();sizes[method]=count
            del blobs
        assert len(set(digests.values()))==len(set(sizes.values()))==1
        records.append({'order':order,'seconds':timings,'speedup':timings['original']/timings['stream'],'bytes':sizes['stream'],'sha256':digests['stream']})
        print(records[-1],flush=True)
    started=time.perf_counter();digest=hashlib.sha256();count=0
    for raw in pieces(report):digest.update(raw);count+=len(raw)
    assert digest.hexdigest()==expected['original_report_sha256'] and count==expected['full_original_bytes']
    for p,d in pins.items():assert sha(p)==d,p
    proof={'status':'passed_actual_full155_original_report_bytes_and_two_order_timing',
        'input_sha256':pins,'records':records,'full_original_bytes':count,'full_original_sha256':digest.hexdigest(),
        'full_stream_seconds':time.perf_counter()-started,'connected_records':expected['connected_records'],
        'adopt':min(r['speedup'] for r in records)>1.05,
        'all_original_values_order_whitespace_and_float_spellings_exact':True,'new_quality_scores':0,'new_native_fits':0,'test_labels_read':False}
    create(A/'byte_exact_ranking_stream_benchmark_v1_20261010.json',proof)
    print({k:v for k,v in proof.items() if k not in ('input_sha256','records')},flush=True)
if __name__=='__main__':main()
