"""Record actual simultaneous job stages and resource samples for67-child fits."""
from pathlib import Path
from datetime import datetime
import hashlib
import json
import subprocess
import time
import psutil
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'analysis/nonlinear_stacking_resource_observations_20261004'


def read(path):return json.loads(path.read_text(encoding='utf-8-sig'))
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def write(path,value):path.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')


def main():
    run_path=ROOT/'analysis/nonlinear_stacking_training_run_20261004.json';run=read(run_path)
    registry=ROOT/run['active_run_registry'];entries=read(registry)
    OUT.mkdir(exist_ok=True);assert not (OUT/'protocol.json').exists()
    protocol=OUT/'protocol.json'
    write(protocol,{'status':'sampling_started','started_at_local':datetime.now().isoformat(timespec='seconds'),
        'sampler_sha256':sha(Path(__file__)),'training_run_sha256':sha(run_path),'registry_sha256':sha(registry),
        'scope':'67-parent OOF training after sampler start; record live official pipeline stages on each sample. Stage labels are observations, not assumed worker utilization or physical capacity.',
        'sample_interval_seconds':1.,'chosen_free_ram_reserve_GiB':8,'global_resource_exhaustion_established':False,'test_data_read':False})
    started=time.monotonic();records=0;minimum_free=psutil.virtual_memory().available;maximum_rss=0;maximum_gpu=0
    gpu_value=None;gpu_at=-10.;failure=None;phase_counts={};progress=[];last_count=None
    with (OUT/'samples.jsonl').open('x',encoding='utf-8',newline='\n') as stream:
        while True:
            tick=time.monotonic();processes={};live_stages=[]
            for entry in [*entries,run]:
                try:
                    root=psutil.Process(entry['pid'])
                    for process in [root,*root.children(recursive=True)]:
                        try:
                            if 'python' in process.name().lower():processes[process.pid]=process.memory_info().rss
                        except (psutil.NoSuchProcess,psutil.AccessDenied):pass
                    if 'round' in entry:
                        state=ROOT/f"analysis/ongoing_optimization_r{entry['round']}_state.json"
                        if state.exists():
                            value=read(state)
                            if not value['stage'].startswith('waiting'):
                                live_stages.append({'round':entry['round'],'stage':value['stage'],'status':value['status']})
                except (psutil.NoSuchProcess,psutil.AccessDenied):pass
            if tick-gpu_at>=5.:
                gpu_at=tick
                result=subprocess.run(['nvidia-smi','--query-gpu=memory.used,memory.total,utilization.gpu','--format=csv,noheader,nounits'],capture_output=True,text=True,creationflags=subprocess.CREATE_NO_WINDOW,timeout=10)
                if result.returncode==0:
                    values=[int(v.strip()) for v in result.stdout.strip().split(',')]
                    gpu_value=dict(zip(('memory_used_mib','memory_total_mib','utilization_percent'),values));maximum_gpu=max(maximum_gpu,values[0])
            memory=psutil.virtual_memory();rss=sum(processes.values());minimum_free=min(minimum_free,memory.available);maximum_rss=max(maximum_rss,rss)
            infos=list((ROOT/'analysis/nonlinear_stacking_bank_20261004').glob('*/info_202[0-4].json'))
            count=len(infos);fits=sum(read(p)['new_model_fits'] for p in infos)
            record={'at_local':datetime.now().isoformat(timespec='seconds'),'elapsed_seconds':tick-started,
                'available_ram_bytes':memory.available,'tracked_python_rss_sum_bytes':rss,'python_processes':len(processes),
                'completed_annual_artifacts':count,'completed_distinct_annual_fits':fits,'live_official_pipeline_stages':live_stages,'gpu_last_sample':gpu_value}
            stream.write(json.dumps(record,separators=(',',':'))+'\n');stream.flush();records+=1
            for stage in live_stages:
                key=f"r{stage['round']}:{stage['stage']}";phase_counts[key]=phase_counts.get(key,0)+1
            if count!=last_count:progress.append(record);last_count=count
            audit=ROOT/'analysis/nonlinear_stacking_bank_20261004/oof_audit.json'
            if audit.exists():assert read(audit)['status']=='passed';break
            if not psutil.pid_exists(run['pid']):failure='training ended before OOF audit';break
            time.sleep(max(0.,1.-(time.monotonic()-tick)))
    write(OUT/'summary.json',{'status':'passed' if failure is None else 'training_incomplete','failure':failure,
        'finished_at_local':datetime.now().isoformat(timespec='seconds'),'samples':records,'elapsed_seconds':time.monotonic()-started,
        'minimum_available_ram_bytes_sampled':minimum_free,'maximum_tracked_python_rss_sum_bytes_sampled':maximum_rss,
        'maximum_gpu_memory_mib_sampled':maximum_gpu,'pipeline_stage_sample_counts':phase_counts,'progress_points':progress,
        'physical_resource_boundary_established':False,'global_resource_exhaustion_established':False,'test_data_read':False,
        'protocol_sha256':sha(protocol),'samples_sha256':sha(OUT/'samples.jsonl')})
    print('67-child resource observation finished: '+('passed' if failure is None else failure),flush=True)


if __name__=='__main__':main()
