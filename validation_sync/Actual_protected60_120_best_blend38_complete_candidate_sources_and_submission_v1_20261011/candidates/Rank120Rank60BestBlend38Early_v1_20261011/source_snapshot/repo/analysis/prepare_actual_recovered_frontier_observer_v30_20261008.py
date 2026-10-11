"""Observe actual140 closure19,141 closure20 and146 qualified prospective3; distinguish scores from qualification."""
from pathlib import Path
import sys,json
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import sha,create
def main():
 old=A/'monitor_actual_chronological_optimization_progress_v29_20261008.py';s=old.read_text(encoding='utf8').replace('_v29_20261008','_v30_20261008')
 needle="145:('CrossFamilyFine125',125,1)}";assert needle in s;s=s.replace(needle,"145:('CrossFamilyFine125',125,1),146:('HuberCrossFamilyFine125',125,2)}")
 needle='        if number==145:\n';assert s.count(needle)==1
 s=s.replace(needle,"        if number==140:row['full_registration']=status('SpectralGram52_round140_full_registration_v19_20261008')\n"+needle)
 s=s.replace("'complete_quality_receivers_not_yet_prepared':True", "'complete_quality_receivers_preflighted':status('HuberCrossFamilyFine146_complete_prospective_controls_v3_20261008')")
 needle="    state['isolated_serialization_benchmark']=";assert s.count(needle)==1
 extra="""    state['fine146_frontier'].update(actual_new_official_scores=pipeline['146']['completed_cases'],quality_source_admission=status('HuberCrossFamilyFine125_round146_source_admission_v2_20261008'),chronological_dispatch=status('HuberCrossFamilyFine146_complete_chronological_dispatch_v3_20261008'),actual_calendar=status('HuberCrossFamilyFine30_multiyear_calendar_controls_v1_20261008'))
    state['fresh141_closure']=status('KrylovGram141_actual_preflight_metadata_closure_v20_20261008')
    state['fresh141_dispatch']=status('KrylovGram141_remaining_chronological_dispatch_v20_20261008')
    state['publisher_storage_relocation']=status('Git_publisher_refreshed_current_main_and_E_relocation_v7_20261008')
    state['expired_20261007_shutdown_schedule_not_restarted']=True
"""
 s=s.replace(needle,extra+needle)
 s=s.replace('125项评分与候选流程仍需准备。', '完整评分与候选接收流程已预检，实际官方评分见上表。')
 target=A/'monitor_actual_chronological_optimization_progress_v30_20261008.py';compile(s,str(target),'exec')
 with target.open('x',encoding='utf8',newline='') as f:f.write(s)
 pins={str(p):sha(p) for p in [Path(__file__),old,target]}
 from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start
 row=start('actual_chronological_optimization_progress_observer_v30_20261008',target.name,[],pins)
 create(A/'actual_recovered_frontier_observer_hidden_launch_v30_20261008.json',{'launch':row,'input_sha256':pins})
 create(A/'latest_actual_optimization_progress_pointer_v30_20261008.json',{'json':str(A/'optimization_live_progress_v30_20261008.json'),'markdown':str(A/'optimization_live_progress_v30_20261008.md'),'observer_worker':row['owned_worker_pid'],'actual_states_only':True})
 print(json.dumps({'worker':row['owned_worker_pid']}),flush=True)
if __name__=='__main__':main()
