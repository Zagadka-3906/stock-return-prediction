"""Sample actual joint annual training/scoring resources without altering jobs."""
from pathlib import Path
import hashlib
import json
import subprocess
import sys
import time
from datetime import datetime
import psutil
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'analysis/expanded_future_resource_observations_recovery_20261004'


def write(path,value):
    path.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')


def main():
    OUT.mkdir(exist_ok=True)
    assert not (OUT/'protocol.json').exists()
    run=json.loads((ROOT/'analysis/expanded_future_resource_recovery_input_20261004.json').read_text(encoding='utf-8-sig'))
    queue=json.loads((ROOT/'analysis/expanded_future_resource_recovery_queue_20261004.json').read_text(encoding='utf-8-sig'))
    registry=ROOT/queue['active_run_registry']
    entries=json.loads(registry.read_text(encoding='utf-8-sig'))
    source=Path(__file__).resolve();started=time.monotonic()
    write(OUT/'protocol.json',{'status':'sampling_started','started_at_local':datetime.now().isoformat(timespec='seconds'),
          'sampler_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'registry_sha256':hashlib.sha256(registry.read_bytes()).hexdigest(),
          'expanded_training_root_pid':run['pid'],'sample_interval_seconds':1.,'gpu_sample_interval_seconds':5.,
          'scope':'Observed recovered standalone55-child future inference and concurrent official scoring from this sampler start. Prior fit/role-branch peaks are only covered by the earlier separate sampler, which ended after an inference path/assertion error. No global resource-exhaustion claim.',
          'test_data_read':False})
    records=0;minimum_free=psutil.virtual_memory().available;maximum_rss=0;maximum_gpu=0;gpu_value=None;gpu_sample=-10.
    progress=[];last_count=None;failure=None
    with (OUT/'samples.jsonl').open('x',encoding='utf-8',newline='\n') as stream:
        while True:
            tick=time.monotonic();memory=psutil.virtual_memory();processes={}
            for entry in entries+[run,{'pid':run['qa_pid']}]:
                try:
                    root=psutil.Process(entry['pid'])
                    for process in [root,*root.children(recursive=True)]:
                        try:
                            if 'python' in process.name().lower():processes[process.pid]=process.memory_info().rss
                        except (psutil.NoSuchProcess,psutil.AccessDenied):pass
                except (psutil.NoSuchProcess,psutil.AccessDenied):pass
            if tick-gpu_sample>=5:
                result=subprocess.run(['nvidia-smi','--query-gpu=memory.used,memory.total,utilization.gpu','--format=csv,noheader,nounits'],capture_output=True,text=True,creationflags=subprocess.CREATE_NO_WINDOW,timeout=10)
                gpu_sample=tick
                if result.returncode==0:
                    values=[int(v.strip()) for v in result.stdout.strip().split(',')];gpu_value={'memory_used_mib':values[0],'memory_total_mib':values[1],'utilization_percent':values[2]};maximum_gpu=max(maximum_gpu,values[0])
            rss=sum(processes.values());minimum_free=min(minimum_free,memory.available);maximum_rss=max(maximum_rss,rss)
            count=len(list((ROOT/'analysis/expanded_stacking_bank_20261004').glob('*/info_202[0-4].json')))
            record={'at_local':datetime.now().isoformat(timespec='seconds'),'elapsed_seconds':tick-started,
                    'available_ram_bytes':memory.available,'tracked_python_rss_sum_bytes':rss,'python_processes':len(processes),
                    'completed_expanded_annual_artifacts':count,'gpu_last_sample':gpu_value}
            stream.write(json.dumps(record,separators=(',',':'))+'\n');stream.flush();records+=1
            if count!=last_count:progress.append(record);last_count=count
            audit=ROOT/'analysis/expanded_stacking_future_pipelines_qa_20261004/verification.json'
            if audit.exists():assert json.loads(audit.read_text(encoding='utf-8-sig'))['status']=='passed';break
            if not any(psutil.pid_exists(pid) for pid in (run['pid'],run['qa_pid'])):failure='both full-fit/inference jobs ended before future verification';break
            time.sleep(max(0.,1.-(time.monotonic()-tick)))
    write(OUT/'summary.json',{'status':'passed' if failure is None else 'training_incomplete','failure':failure,
          'finished_at_local':datetime.now().isoformat(timespec='seconds'),'elapsed_seconds':time.monotonic()-started,'samples':records,
          'minimum_available_ram_bytes_sampled':minimum_free,'maximum_tracked_python_rss_sum_bytes_sampled':maximum_rss,
          'maximum_gpu_memory_mib_sampled':maximum_gpu,'progress_points':progress,
          'observed_full_pipeline_scoring_coexistence':True,'global_resource_exhaustion_established':False,
          'test_data_read':False,'protocol_sha256':hashlib.sha256((OUT/'protocol.json').read_bytes()).hexdigest(),
          'samples_sha256':hashlib.sha256((OUT/'samples.jsonl').read_bytes()).hexdigest()})
    print('Resource sampling finished: '+('passed' if failure is None else failure),flush=True)


if __name__=='__main__':main()
