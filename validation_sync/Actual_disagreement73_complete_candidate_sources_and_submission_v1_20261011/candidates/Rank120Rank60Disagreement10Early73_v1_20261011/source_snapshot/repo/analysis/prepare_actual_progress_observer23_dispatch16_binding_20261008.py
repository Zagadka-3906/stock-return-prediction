"""Point the primary observer at the actual successful16 dispatcher and14 science receivers."""
from pathlib import Path
import json,sys
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
def main():
    source=A/'monitor_actual_chronological_optimization_progress_v22_20261008.py'
    text=source.read_text(encoding='utf8').replace('v22','v23')
    text=text.replace('pending137to141_dispatch_verified_fresh14_after_actual15_controls_20261008','pending137to141_dispatch_verified_fresh14_after_actual15_controls_v16_20261008')
    text=text.replace('fresh13_full_prospective_controls','fresh14_full_prospective_controls_actual15').replace('fresh13_dispatch','fresh14_dispatch_actual16')
    target=A/'monitor_actual_chronological_optimization_progress_v23_20261008.py';assert not target.exists()
    compile(text,str(target),'exec');target.write_text(text,encoding='utf8',newline='\n')
    from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start
    row=start('actual_chronological_optimization_progress_observer_v23_20261008',target.name,[],{str(target):sha(target)})
    create(A/'actual_chronological_optimization_progress_observer_v23_hidden_launch_20261008.json',row)
    create(A/'latest_actual_optimization_progress_pointer_v23_20261008.json',{
        'status':'primary_actual_progress_observer_with14_science_15_controls_16_dispatch_1366_qualification',
        'source':str(target),'source_sha256':sha(target),'output':str(A/'optimization_live_progress_v23_20261008.md'),
        'hidden_launch':row,'new_official_scores':0})
    print(json.dumps({'service':row['name'],'worker':row['owned_worker_pid']}),flush=True)
if __name__=='__main__':main()
