"""Run same four historical official calls serially, compare real process wall time."""
from pathlib import Path
from datetime import datetime
import sys,time,psutil
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start

def main():
    cutoff=datetime.fromisoformat('2026-10-07T23:05:00+08:00').timestamp()
    out=A/'actual_paired_serial_uncached_scoring_controls_20261007';assert not out.exists();out.mkdir()
    source=A/'actual_paired_serial_official_controls_source_preparation_20261007.json';p=read(source)
    pins={**p['input_sha256'],str(source):sha(source)}
    for path,digest in pins.items():assert sha(path)==digest,path
    start_time=time.perf_counter();samples=[];results=[]
    for slot in (0,1):
        while psutil.virtual_memory().available<8.5*2**30:
            assert time.time()<cutoff;time.sleep(10)
        assert time.time()<cutoff
        row=start(f'actual_paired_serial_official_worker2_slot{slot}','verify_actual_paired_serial_official_worker2_20261007.py',[str(slot)],pins)
        while owned(row):
            samples.append({'seconds':time.perf_counter()-start_time,'available_RAM_GiB':psutil.virtual_memory().available/2**30});time.sleep(.2)
        f=A/f'service_owned_workflows_20261006/actual_paired_serial_official_worker2_slot{slot}'
        assert read(f/'service_execution.json')['status']=='passed',read(f/'service_execution.json')
        result=read(out/f'worker{slot}/verification.json');assert result['actual_uncached_official_calls']==2;results.append(result)
    serial=time.perf_counter()-start_time
    parallel=read(A/'actual_two_process_uncached_scoring_controls_20261007/verification.json')
    assert parallel['actual_uncached_official_calls']==4 and parallel['actual_processes']==2
    for actual,expected in zip(results,parallel['records']):
        for ar,er in zip(actual['records'],expected['records']):
            assert ar['metrics']==er['metrics'] and ar['csv_sha256']==er['csv_sha256'] and ar['mapped_numeric_sha256']==er['mapped_numeric_sha256']
    create(out/'verification.json',{'status':'passed_actual_matching_serial4_and_isolated_parallel4_full_official_calls_all8_CSV_and_input_bits_exact',
      'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'input_sha256':{**pins,**{str(out/f'worker{slot}/verification.json'):sha(out/f'worker{slot}/verification.json') for slot in (0,1)}},
      'actual_serial_uncached_official_calls':4,'actual_parallel_uncached_official_calls':4,'serial_process_wall_seconds':serial,
      'parallel_process_wall_seconds':parallel['wall_seconds_under_current_local_workload'],
      'local_measured_serial_over_parallel_ratio':serial/parallel['wall_seconds_under_current_local_workload'],
      'minimum_sampled_serial_available_RAM_GiB':min(s['available_RAM_GiB'] for s in samples),
      'background_workload_can_change_and_measurement_is_not_general_speed_guarantee':True,
      'current_cached_serial_search_not_modified_by_control':True,'new_quality_scores':0,'new_native_fits':0,'test_labels_read':False,'records':results})

if __name__=='__main__':main()
