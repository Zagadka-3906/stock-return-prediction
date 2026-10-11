"""Fresh route recovery, fixing nested generated prose and selection alias collisions."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis'
sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_upper_pool_HGB66_round115_sources_20261007 import substitute

def write_new(name,text):
    p=A/name;assert not p.exists();compile(text,str(p),'exec')
    with p.open('x',encoding='utf8',newline='\n') as f:f.write(text)
    return p

def main():
    routes=read(A/'local115_alias_and116_dependency_recovery_admission_20261007.json')['routes']
    more={
        'prepare_flagged_HGB88_round116_sources_20261007':'prepare_flagged_HGB88_round116_sources_v2_20261007',
        'run_flagged_HGB88_round116_full_registration_20261007':'run_flagged_HGB88_round116_full_registration_v2_20261007',
        'flagged_HGB88_round116_actual_registration_20261007':'flagged_HGB88_round116_actual_registration_v2_20261007',
        'flagged_HGB88_round116_source_preparation_20261007':'flagged_HGB88_round116_source_preparation_v2_20261007'}
    changes={**routes,**more}
    old=A/'prepare_flagged_HGB88_round116_sources_20261007.py'
    text=substitute(old.read_text(encoding='utf8'),changes)
    for before,after in [("'\\n本轮登记88","'\\\\n本轮登记88"),("标签。\\n').encode","标签。\\\\n').encode")]:
        assert text.count(before)==1,before
        text=text.replace(before,after)
    # Both inherited inference selection and the source registration selection are retained.
    needle="        if name.startswith('register_'):\n";assert text.count(needle)==1
    text=text.replace(needle,needle+"            text=text.replace(\"'original_inference_selection.json' if relative == 'selection.json' else relative\", \"'original_inference_selection_round116.json' if relative == 'selection.json' else relative\")\n")
    gen=write_new('prepare_flagged_HGB88_round116_sources_v2_20261007.py',text)
    olddriver=A/'run_flagged_HGB88_round116_full_registration_20261007.py'
    driver=write_new('run_flagged_HGB88_round116_full_registration_v2_20261007.py',substitute(olddriver.read_text(encoding='utf8'),changes))
    oldverify=A/'verify_flagged_HGB88_round116_sources_20261007.py'
    text=substitute(oldverify.read_text(encoding='utf8'),changes)
    text=text.replace("assert hook['actual_full5635800_controls']==85","assert len(hook['controls'])==85")
    text=text.replace("A/'prepare_flagged_HGB88_round116_pipeline_20261007.py'", "A/'prepare_flagged_HGB88_round116_pipeline_20261007.py', A/'prepare_flagged_HGB88_round116_pipeline_v2_20261007.py', A/'prepare_flagged_HGB88_round116_pipeline_recovery_v3_20261007.py', A/'local115_alias_and116_dependency_recovery_admission_20261007.json'")
    verify=write_new('verify_flagged_HGB88_round116_sources_v3_20261007.py',text)
    create(A/'flagged_HGB88_round116_pipeline_preparation_recovery_v3_20261007.json',{'status':'compiled_three_fresh_prospective_pipeline_sources_before_admission',
        'input_sha256':{str(p):sha(p) for p in (Path(__file__),old,gen,olddriver,driver,oldverify,verify)},
        'canonical116_sources_written':0,'new_quality_scores':0,'old_prototypes_preserved':True})
    print({'status':'compiled_three_fresh_sources'},flush=True)

if __name__=='__main__':main()
