"""Execute two-order real alias fixtures, then launch the memory-bounded cached audit."""
from pathlib import Path
import os,sys,json,time
ROOT=Path(__file__).resolve().parents[1]; A=ROOT/'analysis'
sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create

def main():
    import bounded_frozen_SHA_bindings_20261007 as original
    import bounded_frozen_SHA_bindings_v2_20261007 as cached
    out=A/'cached_bounded_SHA_bindings_actual_preflight_20261007';assert not out.exists();out.mkdir()
    fixture=ROOT/'tmp/cached_bounded_SHA_bindings_fixture_20261007';assert not fixture.exists();(fixture/'analysis').mkdir(parents=True)
    target=fixture/'analysis/history/scoring_validation_only/submission.csv';digest='a'*64
    payload={'members':[{'input_sha256':{str(target):digest,target.as_posix():digest}} for _ in range(500)]}
    source=fixture/'analysis/source_plan.json';source.write_text(json.dumps(payload,ensure_ascii=False,indent=2),encoding='utf8',newline='\n')
    alias=fixture/'analysis/alias_plan.json';os.link(source,alias)
    records=[]
    for order in [(original,cached),(cached,original)]:
        results={}
        for module in order:
            started=time.perf_counter(); result=module.scan(fixture,{target});seconds=time.perf_counter()-started
            results[module.__name__]=result;records.append({'module':module.__name__,'elapsed_seconds':seconds,'blocked':result['blocked'],
                'fingerprints':result['fingerprints'],'actual_paths_cached':result.get('path_cache_hits',0),'physical_aliases_reused':result.get('identical_physical_JSON_aliases_reused',0)})
        assert results[original.__name__]['blocked']==results[cached.__name__]['blocked']==[str(target.resolve())]
        assert results[original.__name__]['fingerprints']==results[cached.__name__]['fingerprints']
        assert results[cached.__name__]['path_cache_hits']>=499 and results[cached.__name__]['identical_physical_JSON_aliases_reused']==1
    create(out/'verification.json',{'status':'passed_actual4_two_order_repeated_SHA_keys_and_physical_alias_results_exact','records':records,
        'input_sha256':{str(p):sha(p) for p in [Path(__file__),Path(original.__file__),Path(cached.__file__),source,alias]},'actual_quality_scores':0,'test_labels_read':False})
    old=A/'plan_closed_local_score_scratch_cleanup_v2_20261007.py';new=A/'plan_closed_local_score_scratch_cleanup_v3_20261007.py'
    text=old.read_text(encoding='utf8').replace("OUT=A/'closed_local_score_scratch_cleanup_v2_20261007'","OUT=A/'closed_local_score_scratch_cleanup_v3_20261007'")
    text=text.replace('from bounded_frozen_SHA_bindings_20261007 import scan','from bounded_frozen_SHA_bindings_v2_20261007 import scan')
    text=text.replace("str(A/'bounded_frozen_SHA_bindings_20261007.py'):sha(A/'bounded_frozen_SHA_bindings_20261007.py')", "str(A/'bounded_frozen_SHA_bindings_20261007.py'):sha(A/'bounded_frozen_SHA_bindings_20261007.py'),str(A/'bounded_frozen_SHA_bindings_v2_20261007.py'):sha(A/'bounded_frozen_SHA_bindings_v2_20261007.py')")
    compile(text,str(new),'exec');assert not new.exists();new.write_text(text,encoding='utf8',newline='\n')
    create(A/'cached_bounded_score_cleanup_v3_source_preparation_20261007.json',{'status':'passed_actual_two_order_alias_controls_and_compiled_cached_bounded_cleanup',
        'input_sha256':{str(p):sha(p) for p in [Path(__file__),old,new,out/'verification.json']},'actual_quality_scores':0,'test_labels_read':False})
    print({'status':'passed_actual_two_order_alias_controls'},flush=True)
if __name__=='__main__':main()
