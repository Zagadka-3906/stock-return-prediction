"""Test real streaming path encodings, then create a bounded replacement cleanup script."""
from pathlib import Path
import sys,json
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis'
sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create

def main():
    import bounded_frozen_SHA_bindings_20261007 as bounded
    out=A/'bounded_frozen_SHA_bindings_preflight_20261007';assert not out.exists();out.mkdir()
    digest='a'*64; cases=[]
    for ascii_only in (True,False):
        for path in [str(A/'conditional_residual_hgb44_official_comparison_20261007/scoring_validation_only/submission.csv'),
            (A/'conditional_residual_hgb44_official_comparison_20261007/scoring_validation_only/submission.csv').as_posix(),
            'analysis/conditional_residual_hgb44_official_comparison_20261007/scoring_validation_only/submission.csv']:
            p=out/f'case{len(cases)}.json'
            # Place the encoded path across a one-MiB streaming boundary.
            text=json.dumps({'padding':'x'*(bounded.CHUNK-37),'nested':{'input_sha256':{path:digest}}},ensure_ascii=ascii_only)
            p.write_text(text,encoding='utf8',newline='\n')
            actual=list(bounded.entries(p));assert (path,digest) in actual and len(actual)==1
            cases.append({'ensure_ascii':ascii_only,'key':path,'chunk_boundary_exact':True,'bytes':p.stat().st_size,'sha256':sha(p)})
    create(out/'verification.json',{'status':'passed_actual6_UTF8_ASCII_Windows_POSIX_relative_SHA_keys_cross_chunk_controls','cases':cases,
        'source_sha256':sha(bounded.__file__),'new_quality_scores':0,'test_labels_read':False})
    old=A/'plan_closed_local_score_scratch_cleanup_20261007.py';new=A/'plan_closed_local_score_scratch_cleanup_v2_20261007.py'
    text=old.read_text(encoding='utf8').replace("OUT=A/'closed_local_score_scratch_cleanup_20261007'","OUT=A/'closed_local_score_scratch_cleanup_v2_20261007'")
    text=text.replace('from cleanup_closed_round_worker_submissions_20261006 import scan_bindings,identities','from cleanup_closed_round_worker_submissions_20261006 import identities\nfrom bounded_frozen_SHA_bindings_20261007 import scan as bounded_scan\ndef scan_bindings(targets):\n    proof=bounded_scan(ROOT,targets)\n    if proof[\'blocked\']:raise AssertionError(\'Frozen input: \'+proof[\'blocked\'][0])\n    return proof[\'fingerprints\']')
    start=text.index('    while True:\n        try:bindings=scan_bindings(remaining);break');end=text.index('    deletions=',start)
    text=text[:start]+"    binding_proof=bounded_scan(ROOT,remaining)\n    bindings=binding_proof['fingerprints']\n    for item in binding_proof['blocked']:\n        remaining.remove(Path(item));skipped.append({'path':item,'reason':'conservative_existing_SHA_map_binding'})\n"+text[end:]
    text=text.replace("'live_jobs_at_observation':services,'source_sha256':{str(Path(__file__)):sha(__file__)},", "'live_jobs_at_observation':services,'source_sha256':{str(Path(__file__)):sha(__file__),str(A/'bounded_frozen_SHA_bindings_20261007.py'):sha(A/'bounded_frozen_SHA_bindings_20261007.py')},'bounded_scan':{k:v for k,v in binding_proof.items() if k!='fingerprints'},")
    compile(text,str(new),'exec');assert not new.exists();new.write_text(text,encoding='utf8',newline='\n')
    create(A/'bounded_closed_score_cleanup_v2_source_preparation_20261007.json',{'status':'passed_actual6_chunk_encodings_and_compiled_bounded_cleanup','input_sha256':{str(p):sha(p) for p in [Path(__file__),old,new,A/'bounded_frozen_SHA_bindings_20261007.py',out/'verification.json']},'model_files_deleted':0,'test_labels_read':False})
    print({'status':'passed_actual6_stream_controls_and_compiled'},flush=True)
if __name__=='__main__':main()
