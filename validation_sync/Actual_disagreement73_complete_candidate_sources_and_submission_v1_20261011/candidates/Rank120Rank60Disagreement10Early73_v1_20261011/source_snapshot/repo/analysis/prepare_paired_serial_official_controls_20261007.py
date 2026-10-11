"""Prepare matching serial control before claiming speed benefit from isolated concurrency."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start

def main():
    old=A/'verify_actual_isolated_official_worker2_20261007.py';new=A/'verify_actual_paired_serial_official_worker2_20261007.py'
    text=old.read_text(encoding='utf8').replace("actual_two_process_uncached_scoring_controls_20261007/worker{slot}","actual_paired_serial_uncached_scoring_controls_20261007/worker{slot}")
    compile(text,str(new),'exec');assert not new.exists();new.write_text(text,encoding='utf8',newline='\n')
    controller=A/'verify_actual_paired_serial_official_controls_20261007.py';assert controller.is_file()
    proof=A/'actual_paired_serial_official_controls_source_preparation_20261007.json'
    create(proof,{'status':'compiled_matching_historical_serial_workers_for_actual_local_latency_comparison',
      'input_sha256':{str(p):sha(p) for p in [Path(__file__),old,new,controller,A/'actual_two_process_uncached_scoring_controls_20261007/verification.json']},
      'new_quality_scores':0,'new_native_fits':0,'operational_speed_improvement_not_yet_claimed':True})
    row=start('actual_paired_serial_official_controls_queue',controller.name,[],{**read(proof)['input_sha256'],str(proof):sha(proof)})
    create(A/'actual_paired_serial_official_controls_hidden_launch_20261007.json',{'status':'started_hidden_matching_serial_execution_control_queue','identity':row})

if __name__=='__main__':main()
