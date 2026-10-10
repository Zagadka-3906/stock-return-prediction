"""Retain successful137 and failed138 preflight14; resume with the actual D1 metadata, then untouched139-141."""
from pathlib import Path
import runpy,sys,json
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
def save(path,value):
    assert not path.exists();compile(value,str(path),'exec');path.write_text(value,encoding='utf8',newline='\n')
def main():
    original=A/'resume_pending11_complete_preflights_v12_20261008.py'
    text=original.read_text(encoding='utf8').replace('v11','v14').replace('v12','v15').replace('h.version11','h.version12')
    text=text.replace("'transfer_probe_v14':'transfer_probe_v15','cross_volume_byte_probe_v14':'cross_volume_byte_probe_v15'", "'transfer_probe_v14':'transfer_probe_v15','cross_volume_byte_probe_v14':'cross_volume_byte_probe_v15'")
    target=A/'resume_pending14_complete_preflights_v15_20261008.py';save(target,text)
    dispatch_old=A/'dispatch_pending137to141_verified_fresh14_20261008.py'
    value=dispatch_old.read_text(encoding='utf8').replace('pending137to141_complete_prospective_controls_v14_20261008','pending137to141_complete_prospective_controls_actual_D1_v15_20261008')
    dispatch=A/'dispatch_pending137to141_verified_fresh14_after_actual15_controls_20261008.py';save(dispatch,value)
    create(A/'pending14_reverse_preflight_actual_input_recovery_v15_20261008.json',{
        'status':'prepared_fresh15_preflight_resume_without_modifying_frozen14_sources_or_passed137_proof',
        'reason':'broad gate5_to6_mapping_also_changed_a_missing_metadata_removal_literal',
        'input_sha256':{str(p):sha(p) for p in [Path(__file__),original,target,dispatch_old,dispatch]},
        'old_failed14_not_marked_passed':True,'new_official_scores':0,'test_labels_read':False})
    from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start
    row=start('pending137to141_complete_prospective_controls_actual_D1_v15_20261008',target.name,[],{str(p):sha(p) for p in [Path(__file__),target,dispatch]})
    create(A/'pending137to141_actual15_controls_hidden_launch_20261008.json',row)
    print(json.dumps({'service':row['name'],'worker':row['owned_worker_pid']}),flush=True)
if __name__=='__main__':main()
