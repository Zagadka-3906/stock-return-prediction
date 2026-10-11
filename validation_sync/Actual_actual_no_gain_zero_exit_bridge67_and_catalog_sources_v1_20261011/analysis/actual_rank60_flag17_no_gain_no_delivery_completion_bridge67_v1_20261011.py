from pathlib import Path
import sys
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed,closed
def main():
 assert allowed()
 decision=A/'rank60_flag17_best17_gain_decision_v1_20261011.json';d=read(decision);assert not d['adopt']
 closed('recovery65_actual_rank60_flag17_gain_selected_full_candidate_queue_v1_20261011')
 closed('recovery65_actual_rank60_flag17_best17_complete_candidate_main_v1_20261011')
 f=A/'service_owned_workflows_20261006'/'recovery65_actual_verified_rank60_flag17_best17_alternate_delivery_v1_20261011';t=read(f/'service_execution.json');assert t['status']=='failed' and t['failure']=='SystemExit: 0'
 assert 'No higher TRAIN S: no new candidate delivery.' in (f/'stdout.log').read_text(encoding='utf8')
 create(A/'actual_rank60_flag17_no_gain_no_delivery_completion_bridge67_v1_20261011_verification.json',{'status':'passed_actual_no_gain_no_delivery_required_original_zero_SystemExit_preserved_not_new_candidate_qualification','decision_sha256':sha(decision),'original_zero_exit_execution_sha256':sha(f/'service_execution.json'),'candidate_inference_not_claimed':True,'new_scores':0,'new_inference':0})
 print('No gain: delivery intentionally unnecessary; actual zero-exit metadata bridged without candidate claim',flush=True)
if __name__=='__main__':main()
