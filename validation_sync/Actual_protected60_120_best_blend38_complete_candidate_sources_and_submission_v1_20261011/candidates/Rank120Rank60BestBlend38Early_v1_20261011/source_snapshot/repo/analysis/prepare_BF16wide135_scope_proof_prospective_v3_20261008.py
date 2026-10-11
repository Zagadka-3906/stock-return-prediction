"""Preserve the premature prospective2 receiver; verify an already completed D-scope prerequisite honestly."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import sha,create,read


def main():
    scope=A/'BF16wide135_D_scoring_scope_v2_20261008.json'
    assert read(scope)['status']=='passed_actual3_original_scope_guards_reject_E_and_accept_both_D_scoring_directories'
    original=A/'verify_BF16wide40_prospective_routes_v2_20261008.py';text=original.read_text(encoding='utf8')
    before='    scope_checks()'
    after="    actual_scope=read(A/'BF16wide135_D_scoring_scope_v2_20261008.json')\n    assert actual_scope['status']=='passed_actual3_original_scope_guards_reject_E_and_accept_both_D_scoring_directories'\n    for p,d in actual_scope['input_sha256'].items():assert sha(p)==d,p"
    assert text.count(before)==1;text=text.replace(before,after)
    target=A/'verify_BF16wide40_prospective_routes_v3_20261008.py';assert not target.exists();compile(text,str(target),'exec')
    assert not (A/'BF16wide40_prospective_routes_v2_20261008.json').exists()
    target.write_text(text,encoding='utf8',newline='\n')
    create(A/'BF16wide135_scope_proof_prospective_preparation_v3_20261008.json',{'status':'prepared_fresh_prospective3_after_actual_D_scope_proof_keeping_original2_failure_source',
        'input_sha256':{str(p):sha(p) for p in (Path(__file__),scope,original,target)},'original2_proof_not_created':True,'new_quality_scores':0,'test_labels_read':False})


if __name__=='__main__':main()
