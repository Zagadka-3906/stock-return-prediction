"""Preserve the12 collision and separate the already frozen current-parent driver from fresh13 receivers."""
from pathlib import Path
import sys,runpy
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
def main():
    old=A/'prepare_pending137to141_fresh_closed_dependencies_v12_20261008.py'
    helper=A/'recover_pending137to141_registration_contracts_v12_20261008.py'
    parent=A/'verify_HuberIRLS64_49_current_parent_v5_20261008.py'
    create(A/'pending12_exclusive_current_source_conflict_preserved_20261008.json',{
        'status':'failed_before_any_generated_receiver_source_write_or_quality',
        'reason':'factory included the separately written current-parent5 driver in its exclusive generated products',
        'input_sha256':{str(p):sha(p) for p in [old,helper,parent]},'new_official_scores':0})
    text=old.read_text(encoding='utf8').replace('v12','v13')
    needle="current=A/'verify_HuberIRLS64_49_current_parent_v5_20261008.py';save(current,value)";assert text.count(needle)==1
    text=text.replace(needle,"current=A/'verify_HuberIRLS64_49_current_parent_v5_20261008.py'\n    assert current.read_text(encoding='utf8')==value")
    needle='    # Candidate aliases wrap the original predictor; model bytes and numerical code remain unchanged.'
    assert text.count(needle)==1
    text=text.replace(needle,"    text=text.replace(\"if name not in MAPPING:continue\",\"if name not in MAPPING or name.startswith('HuberIRLS64_49_current_parent_controls_'):continue\")\n"+needle)
    target=A/'prepare_pending137to141_fresh_closed_dependencies_v13_20261008.py';assert not target.exists()
    compile(text,str(target),'exec');target.write_text(text,encoding='utf8',newline='\n')
    runpy.run_path(str(target),run_name='__main__')
if __name__=='__main__':main()
