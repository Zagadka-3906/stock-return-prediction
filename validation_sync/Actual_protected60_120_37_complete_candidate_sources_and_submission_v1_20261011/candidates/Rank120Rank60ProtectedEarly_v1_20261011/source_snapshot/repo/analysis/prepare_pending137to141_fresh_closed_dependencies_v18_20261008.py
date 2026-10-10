"""Prepare only unscored139–141; gate actual136/137/138 qualified services and preserve all failures."""
from pathlib import Path
import sys,json
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
def main():
    old=A/'recover_pending137to141_registration_contracts_v14_20261008.py'
    s=old.read_text(encoding='utf8').replace('v14','v18')
    needle='MAPPING={};CONFIG=[]';assert s.count(needle)==1;s=s.replace(needle,'SPECS=SPECS[2:]\n'+needle)
    boundary='\ndef remap(text):';assert s.count(boundary)==1
    s=s.replace(boundary,"\n    MAPPING.update({'Huber52_round137_full_registration_v3_20261008':'Huber52_round137_full_registration_v14_20261008','BF16reverse40_round138_full_registration_v1_20261008':'BF16reverse40_round138_full_registration_v17_20261008'})\n"+boundary)
    needle="            products.append((A/(MAPPING[old.stem]+'.py'),value))";assert s.count(needle)==1
    s=s.replace(needle,"            value=value.replace('from file_backed_hidden_git_runtime_20261007 import installed','from verified_TLS_Git_retry_runtime_v2_20261008 import installed')\n"+needle)
    target=A/'recover_pending137to141_registration_contracts_v18_20261008.py';assert not target.exists();compile(s,str(target),'exec');target.write_text(s,encoding='utf8',newline='\n')
    import recover_pending137to141_registration_contracts_v18_20261008 as helper
    helper.prepare()
    pins={str(p):sha(p) for p in [Path(__file__),old,target,A/'pending137to141_receiver_preparation_v18_20261008.json',A/'verified_TLS_Git_retry_runtime_v2_20261008.py']}
    create(A/'pending139to141_closed_dependency_recovery_v18_20261008.json',{'status':'prepared_three_unscored_rounds_with_actual_qualified_parent_gates_before_prospective_controls','input_sha256':pins,
        'rounds':[139,140,141],'actual_parent_full_services':{'136':6,'137':14,'138':17},'original_declared_cases':216,
        'new_quality_scores':0,'test_labels_read':False,'old_terminal_failures_preserved':True})
    from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start
    row=start('pending139to141_complete_prospective_controls_v18_20261008',target.name,['controls'],pins)
    create(A/'pending139to141_prospective_hidden_launch_v18_20261008.json',{'launch':row,'input_sha256':pins})
    print(json.dumps({'prepared':[139,140,141],'controls_worker':row['owned_worker_pid']}),flush=True)
if __name__=='__main__':main()
