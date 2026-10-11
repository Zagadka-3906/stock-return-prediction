"""Prepare isolated historical official-call workers; no quality search or live-cache adoption."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start

def main():
    original=A/'verify_actual4_official_scoring_under_8_5GiB_gate_20261007.py';worker=A/'verify_actual_isolated_official_worker2_20261007.py'
    text=original.read_text(encoding='utf8')
    text=text.replace("out=A/'actual4_official_scoring_8_5GiB_gate_preflight_20261007'","slot=int(sys.argv[1]);assert slot in (0,1)\n    out=A/f'actual_two_process_uncached_scoring_controls_20261007/worker{slot}'")
    text=text.replace("for repeat,order in enumerate(((0,1),(1,0))):","for repeat,order in enumerate(((slot,),(slot,))):")
    text=text.replace('actual_uncached_calls_expected\':4','actual_uncached_calls_expected\':2').replace('assert len(records)==4','assert len(records)==2').replace("'actual_uncached_official_calls':4","'actual_uncached_official_calls':2")
    text=text.replace('passed_actual4_uncached_full_official_calls_at_8_5GiB_start_gate_all8_and_CSV_and_input_bits_exact','passed_actual2_uncached_full_official_calls_in_isolated_process_all8_CSV_and_input_bits_exact')
    text=text.replace("'test_labels_read':False})\nif __name__", "'test_labels_read':False,'worker_pid':psutil.Process().pid,'worker_slot':slot,'all_shared_cache_donor_reads_bypassed':True})\nif __name__")
    compile(text,str(worker),'exec');assert not worker.exists();worker.write_text(text,encoding='utf8',newline='\n')
    controller=A/'verify_actual_two_process_uncached_scoring_controls_20261007.py';assert controller.is_file()
    proof=A/'actual_two_process_uncached_scoring_source_preparation_20261007.json'
    create(proof,{'status':'compiled_actual_two_isolated_historical_official_workers_no_shared_cache_donor_reads',
      'input_sha256':{str(p):sha(p) for p in [Path(__file__),original,worker,controller]},
      'new_quality_scores':0,'new_native_fits':0,'current_official_search_keeps_serial_recipe':True})
    row=start('actual_two_process_uncached_scoring_controls_queue',controller.name,[],{**read(proof)['input_sha256'],str(proof):sha(proof)})
    create(A/'actual_two_process_uncached_scoring_controls_hidden_launch_20261007.json',{'status':'started_hidden_execution_control_queue_with_RAM15GiB_and2305_cutoff','identity':row})

if __name__=='__main__':main()
