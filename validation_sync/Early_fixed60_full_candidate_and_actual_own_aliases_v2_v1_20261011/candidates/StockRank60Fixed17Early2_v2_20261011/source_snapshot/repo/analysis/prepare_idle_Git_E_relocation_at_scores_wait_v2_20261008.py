"""The controls publisher already passed; move only while its actual scores publisher still waits for52 quality calls."""
from pathlib import Path
import sys,json
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
def main():
    previous=A/'service_owned_workflows_20261006/Git_publisher_verified_E_relocation_v1_20261008/service_execution.json'
    assert read(previous)['status']=='failed'
    assert read(A/'service_owned_workflows_20261006/Huber52_controls_main_publication_v14_20261008/service_execution.json')['status']=='passed'
    original=A/'relocate_idle_verified_Git_publisher_to_E_v1_20261008.py';text=original.read_text(encoding='utf8')
    text=text.replace('Git_publisher_E_relocation_v1_20261008','Git_publisher_E_relocation_v2_20261008')
    text=text.replace('Git_publisher_E_relocation_location_v1_20261008','Git_publisher_E_relocation_location_v2_20261008')
    text=text.replace('Huber52_controls_main_publication_v14_20261008','Huber52_scores_main_publication_v14_20261008')
    target=A/'relocate_idle_verified_Git_publisher_to_E_v2_20261008.py';assert not target.exists()
    compile(text,str(target),'exec');target.write_text(text,encoding='utf8',newline='\n')
    create(A/'Git_publisher_E_relocation_gate_recovery_v2_20261008.json',{
        'status':'frozen_current_actual_idle_scores_publication_boundary_before_first_repository_copy',
        'input_sha256':{str(p):sha(p) for p in [Path(__file__),original,target,previous]},
        'previous_failed_before_file_hash_copy_rename_or_delete':True,'original_repository_unmodified':True,
        'new_quality_scores':0,'test_labels_read':False})
    from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start
    row=start('Git_publisher_verified_E_relocation_v2_20261008',target.name,[],{str(p):sha(p) for p in [Path(__file__),target]})
    create(A/'Git_publisher_verified_E_relocation_v2_hidden_launch_20261008.json',row)
    print(json.dumps({'service':row['name'],'worker':row['owned_worker_pid']}),flush=True)
if __name__=='__main__':main()
