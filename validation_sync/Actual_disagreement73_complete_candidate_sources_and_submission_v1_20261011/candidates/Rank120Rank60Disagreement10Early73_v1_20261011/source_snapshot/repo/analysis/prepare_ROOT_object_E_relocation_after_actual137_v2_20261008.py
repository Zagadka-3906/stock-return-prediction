"""The first safe report phase already ended; relocate objects after137 completes and138 publishing is still idle."""
from pathlib import Path
import sys,json
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
def main():
    old=A/'relocate_verified_ROOT_Git_objects_to_E_v1_20261008.py';text=old.read_text(encoding='utf8')
    text=text.replace('ROOT_Git_objects_E_relocation_v1_20261008','ROOT_Git_objects_E_relocation_v2_20261008').replace('ROOT_Git_objects_E_relocation_location_v1_20261008','ROOT_Git_objects_E_relocation_location_v2_20261008')
    needle='def main():\n    import psutil';assert text.count(needle)==1
    text=text.replace(needle,"""def main():
    gate=A/'service_owned_workflows_20261006/Huber52_round137_full_registration_v14_20261008'
    while not (gate/'native_launch.json').exists() or owned(read(gate/'native_launch.json')):time.sleep(5)
    assert read(gate/'service_execution.json')['status']=='passed'
    assert read(A/'optimization_20261003_r137/full_registration_execution.json')['status']=='passed'
    import psutil""")
    start=text.index("        row=read(A/'service_owned_workflows_20261006/Huber52_round137_full_registration_v14_20261008/native_launch.json')")
    end=text.index('        original_head=git(',start)
    text=text[:start]+"""        row=read(A/'service_owned_workflows_20261006/BF16reverse40_controls_main_publication_v14_20261008/native_launch.json');assert owned(row)
        parent,worker,proof=suspended_idle(row,'    closed (publish_BF16reverse40_evidence_v14_20261008.py:')
        held.extend((worker,parent));create(OUT/'actual_idle138_publication_hold.json',{'identity':row,'actual_idle_stack':proof,
            'model_fit_scoring_or_candidate_inference_workers_held':0})
"""+text[end:]
    text=text.replace("'temporarily_held_report_bookkeeping_workers':1", "'temporarily_held_report_bookkeeping_workers':0")
    target=A/'relocate_verified_ROOT_Git_objects_to_E_v2_20261008.py';assert not target.exists();compile(text,str(target),'exec');target.write_text(text,encoding='utf8',newline='\n')
    create(A/'ROOT_Git_object_relocation_actual_idle138_gate_v2_20261008.json',{
        'status':'frozen_new_object_only_relocation_after_actual137_full_main_before138_quality_publication',
        'input_sha256':{str(p):sha(p) for p in [Path(__file__),old,target]},
        'failed1_source_check_before_any_object_copy_switch_or_delete_preserved':True,'private_Git_working_cache_not_moved':True,
        'new_scores':0,'test_labels_read':False})
    from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start
    row=start('ROOT_Git_objects_verified_E_relocation_v2_20261008',target.name,[],{str(p):sha(p) for p in [Path(__file__),target]})
    create(A/'ROOT_Git_objects_verified_E_relocation_v2_hidden_launch_20261008.json',row)
    print(json.dumps({'service':row['name'],'worker':row['owned_worker_pid']}),flush=True)
if __name__=='__main__':main()
