"""Include composed generator dependencies and correct25-control reporting before launch."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis'
sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import sha,create

def save(name,text):
    p=A/name;assert not p.exists();compile(text,str(p),'exec');p.write_text(text,encoding='utf8',newline='\n');return p

def main():
    paths=[Path(__file__)]
    old=A/'verify_HGB_quarter_numeric28_transform_v2_20261007.py';text=old.read_text(encoding='utf8')
    text=text.replace("'full5635800_cases':337","'full5635800_cases':25").replace("'cold_prefix_cases':1011","'cold_prefix_cases':75")
    p=save('verify_HGB_quarter_numeric28_transform_v3_20261007.py',text);paths += [old,p]
    old=A/'verify_HGB_quarter_numeric28_round118_sources_v2_20261007.py';text=old.read_text(encoding='utf8')
    text=text.replace("A/'publish_HGB_quarter_numeric28_evidence_v2_20261007.py'","A/'publish_HGB_quarter_numeric28_evidence_v3_20261007.py'")
    needle="    for p in sources:";assert text.count(needle)==1
    text=text.replace(needle,"    sources += [Path(generator.base.__file__),*[A/n for n in generator.base.NAMES],\n        A/'verify_HGB_quarter_numeric28_transform_v3_20261007.py',A/'HGB_quarter_numeric28_complete_scope_source_preparation_v3_20261007.json']\n"+needle)
    p=save('verify_HGB_quarter_numeric28_round118_sources_v3_20261007.py',text);paths += [old,p]
    old=A/'publish_HGB_quarter_numeric28_evidence_v2_20261007.py';text=old.read_text(encoding='utf8')
    text=text.replace('verify_HGB_quarter_numeric28_transform_v2_20261007.py','verify_HGB_quarter_numeric28_transform_v3_20261007.py')
    text=text.replace('verify_HGB_quarter_numeric28_round118_sources_v2_20261007.py','verify_HGB_quarter_numeric28_round118_sources_v3_20261007.py')
    needle="    if phase=='scores':\n        for row in proof['records']:";assert text.count(needle)==1
    text=text.replace(needle,"    sources += [A/'prepare_HGB_quarter_numeric28_complete_scope_v3_20261007.py',A/'HGB_quarter_numeric28_complete_scope_source_preparation_v3_20261007.json',A/'prepare_weighted_HGB340_round117_sources_20261007.py']\n"+needle)
    p=save('publish_HGB_quarter_numeric28_evidence_v3_20261007.py',text);paths += [old,p]
    create(A/'HGB_quarter_numeric28_complete_scope_source_preparation_v3_20261007.json',{'status':'compiled_all_actual25_control_counts_and_transitive117_generator_inputs',
      'input_sha256':{str(p):sha(p) for p in paths},'new_native_fits':0,'new_quality_scores':0})

if __name__=='__main__':main()
