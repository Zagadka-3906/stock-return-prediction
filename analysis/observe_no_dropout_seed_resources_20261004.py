"""Actual basis training andconcurrent official process trees; scoped evidence."""
from pathlib import Path
from datetime import datetime
import hashlib
import json
import time
import subprocess
import psutil
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'analysis/no_dropout_seed_resource_observations_20261004'
RUN=ROOT/'analysis/no_dropout_seed_training_run_20261004.json'


def read(path):return json.loads(path.read_text(encoding='utf-8-sig'))


def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()


def dump(path,data):
    with path.open('x',encoding='utf-8') as stream:json.dump(data,stream,ensure_ascii=False,indent=2)


def main():
    while not RUN.exists():time.sleep(1)
    run=read(RUN);OUT.mkdir(exist_ok=True);assert not (OUT/'protocol.json').exists()
    dump(OUT/'protocol.json',{'status':'sampling_started','at_local':datetime.now().isoformat(),
        'input_sha256':{str(path.resolve()):sha(path) for path in (Path(__file__),RUN)},
        'sample_interval_seconds':1.,'scope':'Samples after start only; identify actual spawned scoring workers from live process trees. Global registry may advance; retain each observed snapshot hash. Prior memory peaks are not inferred.',
        'chosen_available_reserve_GiB':8.,'global_resource_exhaustion_established':False,'test_data_read':False})
    started=time.monotonic();count=0;low=psutil.virtual_memory().available;high=0;overlap=0;snapshots={};failure=None
    gpu_tick=-10.;gpu_value=None;gpu_max=0;gpu_failures=0
    bank=ROOT/'analysis/no_dropout_seed_bank_20261004'
    with (OUT/'samples.jsonl').open('x',encoding='utf-8') as stream:
        while True:
            tick=time.monotonic();processes={};official=[]
            global_state=ROOT/'analysis/ongoing_optimization_state.json'
            try:registry=ROOT/read(global_state)['active_run_registry'];entries=read(registry)
            except (json.JSONDecodeError,FileNotFoundError):entries=[]
            else:snapshots[str(registry.resolve())]=sha(registry)
            for entry in [*entries,run]:
                try:
                    parent=psutil.Process(entry['pid']);tree=[parent,*parent.children(recursive=True)]
                except psutil.Error:continue
                worker_pids=[]
                for p in tree:
                    try:
                        if 'python' in p.name().lower():processes[p.pid]=p.memory_info().rss
                        command=' '.join(p.cmdline())
                        if 'multiprocessing.spawn' in command and '--multiprocessing-fork' in command:worker_pids.append(p.pid)
                    except psutil.Error:continue
                if worker_pids:official.append({'round':entry.get('round'),'actual_worker_pids':worker_pids})
            if tick-gpu_tick>=5:
                gpu_tick=tick
                try:
                    result=subprocess.run(['nvidia-smi','--query-gpu=memory.used,memory.total,utilization.gpu','--format=csv,noheader,nounits'],capture_output=True,text=True,creationflags=subprocess.CREATE_NO_WINDOW,timeout=10)
                    assert result.returncode==0
                    devices=[[int(v.strip()) for v in line.split(',')] for line in result.stdout.strip().splitlines()]
                    gpu_value={'memory_used_mib':sum(v[0] for v in devices),'memory_total_mib':sum(v[1] for v in devices),'maximum_device_utilization_percent':max(v[2] for v in devices),'devices':devices,'query_status':'passed'}
                    gpu_max=max(gpu_max,gpu_value['memory_used_mib'])
                except (OSError,ValueError,AssertionError,subprocess.TimeoutExpired) as error:
                    gpu_failures+=1;gpu_value={'query_status':'unavailable','error_type':type(error).__name__}
            available=psutil.virtual_memory().available;rss=sum(processes.values());low=min(low,available);high=max(high,rss)
            annual=len(list(bank.glob('*/info_202[0-4].json')));nworkers=sum(len(e['actual_worker_pids']) for e in official)
            overlap+=int(nworkers>0 and psutil.pid_exists(run['pid']))
            record={'at_local':datetime.now().isoformat(timespec='seconds'),'elapsed_seconds':tick-started,
                'available_ram_bytes':available,'tracked_python_rss_sum_bytes':rss,'actual_official_jobs':official,
                'actual_spawned_official_workers':nworkers,'actual_completed_annual_fits':annual,'gpu_last_sample':gpu_value}
            stream.write(json.dumps(record,separators=(',',':'))+'\n');stream.flush();count+=1
            if (bank/'oof_audit.json').exists():assert read(bank/'oof_audit.json')['status']=='passed';break
            if not psutil.pid_exists(run['pid']):failure='training process ended before complete20-fit OOF audit';break
            time.sleep(max(0.,1.-(time.monotonic()-tick)))
    dump(OUT/'summary.json',{'status':'passed' if failure is None else 'training_incomplete','failure':failure,
        'at_local':datetime.now().isoformat(),'samples':count,'elapsed_seconds':time.monotonic()-started,
        'minimum_available_ram_bytes_sampled':low,'maximum_tracked_python_rss_sum_bytes_sampled':high,
        'actual_official_worker_overlap_samples':overlap,'observed_registry_snapshots':snapshots,
        'maximum_all_gpu_memory_used_mib_sampled':gpu_max,'gpu_query_failures':gpu_failures,
        'gpu_memory_includes_any_background_GPU_work':True,
        'protocol_sha256':sha(OUT/'protocol.json'),'samples_sha256':sha(OUT/'samples.jsonl'),
        'physical_resource_boundary_established':False,'global_resource_exhaustion_established':False,
        'test_data_read':False})


if __name__=='__main__':main()
