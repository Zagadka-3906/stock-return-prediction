"""Correct three actually detected import/path errors before launching the first Ridge scorer."""
from pathlib import Path
import ast,sys
ROOT=Path(__file__).resolve().parents[1]; A=ROOT/'analysis'
sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_upper_pool_HGB66_round115_sources_20261007 import substitute

def main():
    proof=read(A/'nonflag_Ridge40_prospective_routes_20261007.json'); assert len(proof['issues'])==3
    assert not (A/'nonflag_Ridge40_round121_source_admission_v1_20261007.json').exists()
    assert not (A/'nonflag_Ridge40_official_comparison_v1_20261007').exists()
    files=['run_nonflag_Ridge40_round121_full_registration','verify_nonflag_Ridge40_round121_sources',
        'publish_nonflag_Ridge40_evidence','prepare_nonflag_Ridge40_round121_sources']
    m={n+'_v1_20261007':n+'_v2_20261007' for n in files}; generated={}
    for stem in files:
        old=stem+'_v1_20261007'; new=m[old]
        if stem.startswith('prepare_'):
            text=(A/(old+'.py')).read_text(encoding='utf8'); node=next(n for n in ast.parse(text).body if isinstance(n,ast.FunctionDef) and n.name=='main')
            main_text='\n'.join(text.splitlines()[node.lineno-1:node.end_lineno])
            text=f'''from pathlib import Path
import hashlib,sys,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis'
sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_upper_pool_HGB66_round115_sources_20261007 import substitute
import {old} as original_generator
NAMES=original_generator.NAMES
CORRECTION_MAP={m!r}
def generate(parent):
    return {{n:substitute(t,CORRECTION_MAP) for n,t in original_generator.generate(parent).items()}}
'''+substitute(main_text,m)+"\nif __name__=='__main__':main()\n"
        else:
            text=substitute((A/(old+'.py')).read_text(encoding='utf8'),m)
            text=text.replace('register_nonflag_HGB40_round121','register_nonflag_Ridge40_round121').replace('publish_nonflag_HGB40_round121','publish_nonflag_Ridge40_round121')
        compile(text,str(A/(new+'.py')),'exec'); generated[new+'.py']=text
    old='verify_nonflag_Ridge40_prospective_routes_20261007.py'; new='verify_nonflag_Ridge40_prospective_routes_v2_20261007.py'
    text=substitute((A/old).read_text(encoding='utf8'),m).replace('nonflag_Ridge40_prospective_routes_20261007.json','nonflag_Ridge40_prospective_routes_v2_20261007.json')
    compile(text,str(A/new),'exec');generated[new]=text
    for n in generated:assert not (A/n).exists(),n
    for n,t in generated.items():
        with (A/n).open('x',encoding='utf8',newline='\n') as f:f.write(t)
    create(A/'nonflag_Ridge40_unlaunched_correction_v2_20261007.json',{'status':'corrected_three_actual_prospective_import_errors_before_any_Ridge_official_score',
        'actual_prior_audit':str(A/'nonflag_Ridge40_prospective_routes_20261007.json'),
        'input_sha256':{str(p):sha(p) for p in [Path(__file__),A/'nonflag_Ridge40_prospective_routes_20261007.json',*[A/n for n in generated]]},
        'old_sources_retained':True,'actual_quality_scores':0,'test_labels_read':False})
if __name__=='__main__':main()
