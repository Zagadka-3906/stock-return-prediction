"""Separate execution-control wall latency from a causal speed improvement claim."""
from pathlib import Path
import sys,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create

def main():
    par=A/'actual_two_process_uncached_scoring_controls_20261007/verification.json';seq=A/'actual_paired_serial_uncached_scoring_controls_20261007/verification.json'
    p,s=read(par),read(seq)
    serial_calls=[r['elapsed_seconds'] for worker in s['records'] for r in worker['records']]
    parallel_per_process=[sum(r['elapsed_seconds'] for r in worker['records']) for worker in p['records']]
    create(A/'actual_two_process_scoring_latency_interpretation_20261007.json',{
      'status':'actual_historical_equivalence_passed_but_general_or_causal_speed_factor_not_established',
      'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'input_sha256':{str(x):sha(x) for x in [Path(__file__),par,seq]},
      'serial_wall_seconds_including_resource_gate_and_process_preparation':s['serial_process_wall_seconds'],
      'parallel_wall_seconds_including_resource_gate_and_process_preparation':p['wall_seconds_under_current_local_workload'],
      'serial_sum_actual_score_call_seconds':sum(serial_calls),'parallel_sum_actual_score_call_seconds':sum(parallel_per_process),
      'parallel_process_actual_score_call_seconds':parallel_per_process,
      'serial_controller_minimum_sampled_host_available_RAM_GiB':s['minimum_sampled_serial_available_RAM_GiB'],
      'parallel_controller_minimum_sampled_host_available_RAM_GiB':p['minimum_sampled_available_RAM_GiB'],
      'background_original_GPU_and_full_board_QA_not_controlled_between_runs':True,
      'wall_ratio_cannot_be_reported_as_guaranteed_or_causally_isolated_speedup':True,
      'shared_cache_donor_concurrency_not_admitted':True,'current_serial_quality_search_kept_unchanged':True,
      'new_quality_scores':0,'new_native_fits':0,'test_labels_read':False})

if __name__=='__main__':main()
