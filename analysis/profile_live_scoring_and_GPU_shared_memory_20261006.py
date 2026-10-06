"""Sample exact-owned scientific processes without changing any computation."""
from pathlib import Path
from datetime import datetime
import json
import os
import shutil
import subprocess
import sys
import time

import psutil

ROOT=Path(__file__).resolve().parents[1]
A=ROOT/'analysis'
sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
OUT=A/'live_scoring_and_GPU_shared_memory_profile_20261006'
PWSH=Path('C:/Users/esesl/.cache/codex-runtimes/codex-primary-runtime/dependencies/native/powershell/pwsh.exe')

def command(args,timeout=12):
    return subprocess.run(args,capture_output=True,text=True,encoding='utf-8',errors='replace',
        timeout=timeout,creationflags=subprocess.CREATE_NO_WINDOW,stdin=subprocess.DEVNULL)

def dump(pid):
    result=command([str(ROOT/'tools/readonly_pyspy_diagnostics_20261006/py-spy.exe'),'dump','--pid',str(pid)])
    assert result.returncode==0,result.stderr
    return result.stdout

def gpu(pid):
    code=(f"Get-CimInstance -ClassName Win32_PerfRawData_GPUPerformanceCounters_GPUProcessMemory | "
        f"Where-Object {{ $_.Name -like 'pid_{pid}_*' }} | "
        "Select-Object Name,SharedUsage,DedicatedUsage,TotalCommitted | ConvertTo-Json -Compress")
    result=command([str(PWSH),'-NoLogo','-NoProfile','-NonInteractive','-Command',code],timeout=20)
    assert result.returncode==0,result.stderr
    rows=json.loads(result.stdout)
    if isinstance(rows,dict):rows=[rows]
    assert rows and all(row['Name'].startswith(f'pid_{pid}_') for row in rows)
    nvidia=command([shutil.which('nvidia-smi'),
        '--query-gpu=name,memory.total,memory.used,utilization.gpu,utilization.memory','--format=csv,noheader,nounits'])
    assert nvidia.returncode==0,nvidia.stderr
    return {'at_local':datetime.now().isoformat(timespec='seconds'),'WDDM_process_memory':rows,
        'nvidia_device_aggregate_not_per_process':nvidia.stdout.strip()}

def category(text):
    if 'donor (whole_scheme_replay_runtime_20261004.py:' in text:return 'root_donor'
    if 'root_prediction (whole_scheme_replay_runtime_20261004.py:' in text:return 'root_prediction'
    if 'finished (whole_scheme_replay_runtime_20261004.py:' in text:return 'root_finished'
    if 'replay_layers (role_layer_replay_20261004.py:' in text:return 'downstream_role_layers'
    if 'score (score_calibrated_candidates_20261003.py:' in text:return 'causal_mapping_or_official_score'
    if 'recv' in text or '_recv' in text:return 'worker_idle_or_IPC'
    return 'other_sampled_frame'

def main():
    assert not OUT.exists();OUT.mkdir()
    scratch=ROOT/'tmp/readonly_live_scoring_gpu_profile_20261006';scratch.mkdir(exist_ok=True)
    for variable in ('TMP','TEMP','TMPDIR'):os.environ[variable]=str(scratch)
    annual=read(A/'service_owned_workflows_20261006/neural16384_annual/native_launch.json')
    round_launch=read(A/'service_owned_dependency_queue_v4_20261006/activated_jobs/round95/launch.json')
    assert owned(annual) and owned(round_launch)
    scientific=psutil.Process(round_launch['owned_worker_pid'])
    workers=[p for p in scientific.children(recursive=True) if 'multiprocessing.spawn' in ' '.join(p.cmdline())]
    assert len(workers)==1
    worker=workers[0];identity={'pid':worker.pid,'creation_time':worker.create_time(),'command':worker.cmdline()}
    paths=[Path(__file__),A/'whole_scheme_replay_runtime_20261004.py',A/'replay_complete_scheme_20261003.py',
        A/'role_layer_replay_20261004.py',A/'optimization_20261003_r95/protocol.json',
        A/'ready_goss_reference_search_engine_v2_20261006.py',A/'train_diverse_backbones_20261003.py',
        A/'train_neural16384_full_bank_20261005.py',A/'memory_efficient_neural_complete_search_plan_20261005.json']
    pins={str(p):sha(p) for p in paths}
    create(OUT/'frozen_before_readonly_samples.json',{'input_sha256':pins,'actual_scoring_worker_identity':identity,
        'actual_round95_identity':round_launch,'actual_wide_neural_identity':annual,
        'stack_samples':10,'interval_seconds':5,'stack_fraction_is_not_exact_elapsed_time_or_speedup':True,
        'no_original_model_epoch_batch_or_dtype_changes':True,'new_native_fits':0,'new_quality_scores':0,'test_labels_read':False})
    gpu_samples=[gpu(annual['owned_worker_pid'])]
    neural_stack=dump(annual['owned_worker_pid']);(OUT/'actual_neural_backward_stack.txt').write_text(neural_stack,encoding='utf-8')
    assert '_engine_run_backward' in neural_stack
    samples=[];start=time.monotonic();before_cpu=sum(worker.cpu_times()[:2])
    for index in range(10):
        assert owned(annual) and owned(round_launch)
        current=psutil.Process(identity['pid'])
        assert current.create_time()==identity['creation_time'] and current.cmdline()==identity['command']
        text=dump(current.pid)
        path=OUT/f'actual_scoring_worker_stack_{index:02d}.txt';path.write_text(text,encoding='utf-8')
        samples.append({'at_local':datetime.now().isoformat(timespec='seconds'),'category':category(text),
            'source':str(path),'sha256':sha(path),'cpu_seconds':sum(current.cpu_times()[:2]),
            'RSS_bytes':current.memory_info().rss,'host_available_bytes':psutil.virtual_memory().available})
        if index!=9:time.sleep(max(0,start+5*(index+1)-time.monotonic()))
    after_cpu=sum(worker.cpu_times()[:2]);elapsed=time.monotonic()-start
    gpu_samples.append(gpu(annual['owned_worker_pid']))
    counts={name:sum(row['category']==name for row in samples) for name in set(row['category'] for row in samples)}
    for p,digest in pins.items():assert sha(p)==digest,p
    assert owned(annual) and owned(round_launch)
    profile={'status':'passed_actual_owned10_stack_samples_and_process_WDDM_GPU_memory',
        'at_local':datetime.now().isoformat(timespec='seconds'),'input_sha256':pins,
        'actual_scoring_worker_identity':identity,'stack_samples':samples,'sample_categories':counts,
        'observed_window_seconds':elapsed,'worker_CPU_seconds_over_observed_window':after_cpu-before_cpu,
        'actual_wide_neural_GPU_samples':gpu_samples,
        'actual_neural_backward_stack_sha256':sha(OUT/'actual_neural_backward_stack.txt'),
        'existing_accumulate_checkpoint_combined_models_already_declared_no_duplicate_direction_added':True,
        'sampled_root_replay_counts_do_not_prove_memoization_speedup':True,
        'shared_GPU_bytes_do_not_prove_global_resource_exhaustion_or_OOM':True,
        'new_native_fits':0,'new_quality_scores':0,'scientific_processes_stopped_or_restarted':0,
        'training_batch_epochs_dtype_and_original_scoring_unchanged':True,'test_labels_read':False,
        'global_resource_exhaustion_established':False}
    create(OUT/'verification.json',profile)
    print(json.dumps({'status':profile['status'],'sample_categories':counts,
        'worker_CPU_seconds':after_cpu-before_cpu,'observed_window_seconds':elapsed,
        'actual_WDDM_GPU_memory_samples':gpu_samples},ensure_ascii=False),flush=True)

if __name__=='__main__':
    try:main()
    except BaseException as exc:
        if OUT.exists() and not (OUT/'failure.json').exists():create(OUT/'failure.json',{'status':'failed_preserved_readonly_live_profile','error':f'{type(exc).__name__}: {exc}'})
        raise
