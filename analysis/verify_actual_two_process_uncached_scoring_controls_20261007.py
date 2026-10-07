"""Measure actual overlapping isolated official processes on two already-scored vectors."""
from pathlib import Path
from datetime import datetime
import sys,time,psutil
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start

def main():
    cutoff=datetime.fromisoformat('2026-10-07T23:05:00+08:00').timestamp()
    while psutil.virtual_memory().available<15*2**30:
        if time.time()>=cutoff:
            create(A/'actual_two_process_uncached_scoring_deferred_20261007.json',{'status':'not_dispatched_before2305_resource_cutoff','new_quality_scores':0,'parallel_qualification_not_claimed':True});return
        time.sleep(10)
    assert time.time()<cutoff
    out=A/'actual_two_process_uncached_scoring_controls_20261007';assert not out.exists();out.mkdir()
    source=A/'actual_two_process_uncached_scoring_source_preparation_20261007.json';proof=read(source)
    pins={**proof['input_sha256'],str(source):sha(source)}
    for p,d in pins.items():assert sha(p)==d,p
    before=time.perf_counter();initial_ram=psutil.virtual_memory().available/2**30
    workers=[start(f'actual_isolated_official_worker2_slot{slot}','verify_actual_isolated_official_worker2_20261007.py',[str(slot)],pins) for slot in (0,1)]
    samples=[]
    while any(owned(row) for row in workers):
        live=[row for row in workers if owned(row)]
        samples.append({'seconds':time.perf_counter()-before,'available_RAM_GiB':psutil.virtual_memory().available/2**30,
          'actual_live_owned_workers':[row['owned_worker_pid'] for row in live],
          'own_worker_RSS_GiB':{str(row['owned_worker_pid']):psutil.Process(row['owned_worker_pid']).memory_info().rss/2**30 for row in live}})
        time.sleep(.2)
    results=[]
    for slot in (0,1):
        service=A/f'service_owned_workflows_20261006/actual_isolated_official_worker2_slot{slot}'
        assert read(service/'service_execution.json')['status']=='passed',read(service/'service_execution.json')
        result=read(out/f'worker{slot}/verification.json');assert result['actual_uncached_official_calls']==2
        assert result['all_shared_cache_donor_reads_bypassed'] and all(r['all8_historical_metrics_and_full_CSV_bytes_exact'] for r in result['records'])
        results.append(result)
    overlap=[s for s in samples if len(s['actual_live_owned_workers'])==2]
    assert overlap,'actual overlap not observed'
    create(out/'verification.json',{'status':'passed_actual4_uncached_full_official_calls_in2_overlapping_isolated_processes_all8_CSV_and_input_bits_exact',
      'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'input_sha256':{**pins,**{str(out/f'worker{slot}/verification.json'):sha(out/f'worker{slot}/verification.json') for slot in (0,1)}},
      'actual_uncached_official_calls':4,'actual_processes':2,'workers':workers,'records':results,'resource_samples':samples,
      'initial_available_RAM_GiB':initial_ram,'minimum_sampled_available_RAM_GiB':min(s['available_RAM_GiB'] for s in samples),
      'wall_seconds_under_current_local_workload':time.perf_counter()-before,
      'actual_overlapping_owned_worker_samples':len(overlap),'all_shared_cache_donor_reads_bypassed':True,
      'concurrent_cached_score_pipeline_not_qualified':True,'this_is_historical_execution_control_not_new_quality_scores':True,
      'new_quality_scores':0,'new_native_fits':0,'test_labels_read':False})

if __name__=='__main__':main()
