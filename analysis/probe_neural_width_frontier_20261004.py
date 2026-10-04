"""Isolated real mature-training one-step MLP capacity controls, never quality scores."""
from pathlib import Path
from datetime import datetime
import argparse
import hashlib
import json
import os
import subprocess
import sys
import time

ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT),str(ROOT/'analysis')]
OUT=ROOT/'analysis/neural_width_frontier_20261004'
WIDTHS=(16384,32768,65536)
ROWS=32768
COMMON={'kind':'mlp','target':'y_rank','batch_size':ROWS,'learning_rate':.001,
    'weight_decay':.0001,'dropout':0.,'epochs':1,'seed':20261007}

def read(path):return json.loads(path.read_text(encoding='utf-8-sig'))
def create(path,value):
    with path.open('x',encoding='utf-8') as stream:json.dump(value,stream,ensure_ascii=False,indent=2)
def sha(path):
    h=hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda:stream.read(8*1024*1024),b''):h.update(block)
    return h.hexdigest()
def gpu_observation():
    try:
        result=subprocess.run(['nvidia-smi','--query-gpu=name,memory.total,memory.used,memory.free','--format=csv,noheader,nounits'],capture_output=True,text=True,timeout=3,check=True,creationflags=subprocess.CREATE_NO_WINDOW if os.name=='nt' else 0)
        return {'nvidia_smi_all_process_memory_csv':result.stdout.strip()}
    except (OSError,subprocess.SubprocessError) as error:return {'observation_error':str(error)}

def child(width):
    import numpy as np
    import train_diverse_backbones_20261003 as engine
    import torch
    protocol=read(OUT/'protocol.json');assert width in protocol['widths']
    assert all(sha(Path(p))==d for p,d in protocol['fitter_source_sha256'].items())
    data=OUT/'mature_training_batch.npz';assert sha(data)==protocol['actual_batch_sha256']
    with np.load(data) as saved:x,y=saved['x'],saved['y']
    assert x.shape==(ROWS,63) and len(y)==ROWS
    assert torch.cuda.is_available(),'CUDA unavailable; CPU fallback is not a GPU capacity control'
    torch.cuda.init();torch.cuda.reset_peak_memory_stats()
    cfg={**COMMON,'hidden':[width,width//2,width//4]}
    before=torch.cuda.mem_get_info();started=time.perf_counter();bundle=None
    result={'width':width,'configuration':cfg,'device_name':torch.cuda.get_device_name(),
        'torch_version':torch.__version__,'cuda_version':torch.version.cuda,
        'device_free_bytes_before':before[0],'device_total_bytes':before[1],
        'actual_batch_sha256':protocol['actual_batch_sha256'],'training_rows':ROWS,
        'one_epoch_equals_one_original_AdamW_training_step':True,
        'full_annual_orfull_training_not_performed':True,'new_quality_scores':0,'test_labels_read':False}
    try:
        bundle=engine.fit_arrays(x,y,cfg);torch.cuda.synchronize()
        assert bundle['device']=='cuda' and len(bundle['training_losses'])==1
        assert np.isfinite(bundle['training_losses']).all()
        result.update(status='one_step_completed',training_losses=bundle['training_losses'],
            parameter_count=sum(v.numel() for v in bundle['state'].values()),
            all_returned_weights_finite=all(torch.isfinite(v).all().item() for v in bundle['state'].values()))
    except torch.cuda.OutOfMemoryError as error:
        result.update(status='actual_CUDA_out_of_memory',exception_type=type(error).__name__,exception_message=str(error))
    finally:
        result.update(total_fit_seconds=time.perf_counter()-started,
            peak_own_tensor_allocated_bytes=torch.cuda.max_memory_allocated(),
            peak_own_allocator_reserved_bytes=torch.cuda.max_memory_reserved(),
            allocated_bytes_after_fitter_cleanup_or_exception=torch.cuda.memory_allocated(),
            reserved_bytes_after_fitter_cleanup_or_exception=torch.cuda.memory_reserved(),
            at_local=datetime.now().isoformat(timespec='seconds'))
    create(OUT/f'width{width}_child_result.json',result)
    print(json.dumps({key:result[key] for key in ('width','status','total_fit_seconds','peak_own_tensor_allocated_bytes','peak_own_allocator_reserved_bytes')}),flush=True)

def wait_for_completed_scientific_work():
    import psutil
    gates=[ROOT/'results/optimization_20261003_r60.json',
        ROOT/'analysis/optimization_20261003_r60/provenance_scope_execution.json',
        ROOT/'analysis/portfolio_surrogate_bank_20261004/training_execution_scope.json',
        ROOT/'analysis/portfolio_surrogate_future_models_qa_20261004/verification.json',
        ROOT/'analysis/portfolio_surrogate_complete_scheme_preflight_20261004/verification.json',
        ROOT/'analysis/neural_width_bank_20261004/training_execution_scope.json',
        ROOT/'analysis/neural_width_future_models_qa_20261004/verification.json',
        ROOT/'analysis/neural_width_complete_scheme_preflight_20261004/verification.json']
    from verify_official_extended_capacity_20261004 import external_state
    while True:
        try:values=[read(path) for path in gates]
        except (FileNotFoundError,json.JSONDecodeError):time.sleep(10);continue
        assert values[0]['status']=='complete'
        assert all(v['status']=='passed' for v in values[1:])
        if psutil.virtual_memory().available>=20*2**30 and not external_state().get('actual_official_worker_pids'):
            return gates
        time.sleep(10)

def main():
    completed_gates=wait_for_completed_scientific_work()
    import numpy as np
    import polars as pl
    import psutil
    import train_diverse_backbones_20261003 as engine
    from verify_official_extended_capacity_20261004 import external_state
    OUT.mkdir(exist_ok=True);assert not (OUT/'protocol.json').exists()
    features=engine.feature_names();assert len(features)==63
    cutoff=engine.fold_cutoff(2020)
    frame=engine.training_frame(pl.scan_parquet(engine.FEATURE_FILE),cutoff,COMMON).select(engine.KEYS+features+['y_rank']).sort('trade_date','ts_code').head(ROWS).collect()
    assert len(frame)==ROWS and int(frame['trade_date'].max())<cutoff
    x=engine.to_matrix(frame,features);y=frame['y_rank'].to_numpy()
    data=OUT/'mature_training_batch.npz';np.savez(data,x=x,y=y)
    keys=OUT/'mature_training_batch_keys.parquet';frame.select(engine.KEYS).write_parquet(keys)
    sources=[Path(__file__),Path(engine.__file__),engine.FEATURE_FILE,engine.MANIFEST,
        ROOT/'run.py',ROOT/'src/features.py',ROOT/'analysis/neural_regularization_bank_20261003/protocol.json',
        ROOT/'analysis/neural_regularization_bank_20261003/rank512_drop000_e32/info_2020.json',
        ROOT/'analysis/neural_width_frontier_prepared_plan_20261004.json',
        ROOT/'analysis/neural_width_capacity_20261004/verification.json',*completed_gates]
    frozen={str(p.resolve()):sha(p) for p in sources}
    create(OUT/'protocol.json',{'status':'frozen_before_resource_controls','at_local':datetime.now().isoformat(timespec='seconds'),
        'widths':WIDTHS,'hidden_layout':'[width,width/2,width/4]','common_configuration':COMMON,
        'original_fitter_used_without_modification':True,'training_year_control':2020,
        'cutoff_exclusive':cutoff,'actual_batch_rows':ROWS,'features':features,
        'first_trade_date':int(frame['trade_date'].min()),'last_trade_date':int(frame['trade_date'].max()),
        'training_keys_sha256':sha(keys),'actual_batch_sha256':sha(data),
        'training_matrix_sha256':engine.array_hash(x),'training_target_sha256':engine.array_hash(y),
        'fitter_source_sha256':{str(Path(engine.__file__).resolve()):sha(Path(engine.__file__))},
        'input_sha256':frozen,'fresh_subprocess_per_width':True,'stop_after_first_actual_CUDA_OOM':True,
        'minimum_available_host_bytes_before_launch':20*2**30,'stop_owned_child_if_available_host_bytes_below':4*2**30,
        'maximum_seconds_per_width':180,'all_guards_are_execution_policies':True,
        'all_process_GPU_memory_separate_from_own_tensor_allocations':True,
        'full_training_resident_inputs_not_measured':True,'no_fit_orquality_extrapolation_from_single_step':True,
        'new_quality_scores':0,'test_labels_read':False,
        'primary_API_references':['https://docs.pytorch.org/docs/stable/generated/torch.cuda.memory.max_memory_allocated.html',
            'https://docs.pytorch.org/docs/stable/generated/torch.cuda.memory.max_memory_reserved.html',
            'https://docs.pytorch.org/docs/stable/generated/torch.cuda.OutOfMemoryError.html']})
    del frame,x,y
    controls=[]
    for width in WIDTHS:
        free=psutil.virtual_memory().available
        if free<20*2**30:
            control={'width':width,'status':'not_launched_for_current_memory_budget','available_host_bytes_at_launch':free,
                'physical_resource_exhaustion_proved':False,'background':external_state()}
            create(OUT/f'width{width}_result.json',control);controls.append(control);break
        stdout=OUT/f'width{width}.stdout.log';stderr=OUT/f'width{width}.stderr.log'
        with stdout.open('x',encoding='utf-8') as out,stderr.open('x',encoding='utf-8') as err:
            process=subprocess.Popen([sys.executable,'-B','-X','utf8',str(Path(__file__).resolve()),'--width',str(width)],
                cwd=ROOT,stdout=out,stderr=err,creationflags=subprocess.CREATE_NO_WINDOW if os.name=='nt' else 0)
            samples=[];started=time.perf_counter();reason=None;last_external=0;background=external_state();gpu=gpu_observation()
            while process.poll() is None:
                now=time.perf_counter();free=psutil.virtual_memory().available
                if now-last_external>=3:
                    background,gpu,last_external=external_state(),gpu_observation(),now
                try:rss=psutil.Process(process.pid).memory_info().rss
                except psutil.Error:rss=None
                samples.append({'at_local':datetime.now().isoformat(timespec='seconds'),'elapsed_seconds':now-started,
                    'available_host_bytes':free,'root_process_rss_bytes':rss,'background':background,'gpu':gpu})
                if free<4*2**30 or now-started>180:
                    reason='sampled_host_memory_floor' if free<4*2**30 else 'declared_wall_time_budget'
                    try:
                        owned=[psutil.Process(process.pid),*psutil.Process(process.pid).children(recursive=True)]
                        for p in reversed(owned):
                            if p.is_running():p.terminate()
                    except psutil.Error:pass
                    break
                time.sleep(.25)
            process.wait(timeout=15)
        sample_path=OUT/f'width{width}_samples.jsonl'
        with sample_path.open('x',encoding='utf-8') as stream:
            for sample in samples:stream.write(json.dumps(sample,ensure_ascii=False)+'\n')
        child_path=OUT/f'width{width}_child_result.json'
        control={'width':width,'root_pid':process.pid,'exit_code':process.returncode,
            'status':'stopped_at_declared_control_boundary' if reason else ('completed' if process.returncode==0 and child_path.exists() else 'failed'),
            'stop_reason':reason,'samples':len(samples),'minimum_available_host_bytes_sampled':min(s['available_host_bytes'] for s in samples),
            'resource_samples_sha256':sha(sample_path),'stdout_sha256':sha(stdout),'stderr_sha256':sha(stderr),
            'child_result_sha256':sha(child_path) if child_path.exists() else None,
            'child_result':read(child_path) if child_path.exists() else None}
        create(OUT/f'width{width}_result.json',control);controls.append(control)
        print(json.dumps({'width':width,'status':control['status'],'training_step_status':control['child_result']['status'] if control['child_result'] else None,'stop_reason':reason}),flush=True)
        if control['status']!='completed' or control['child_result']['status']=='actual_CUDA_out_of_memory':break
    assert all(sha(Path(p))==d for p,d in frozen.items())
    measured=[r['child_result'] for r in controls if r['status']=='completed']
    create(OUT/'verification.json',{'status':'passed' if all(r['status'] in ('completed','not_launched_for_current_memory_budget','stopped_at_declared_control_boundary') for r in controls) else 'failed',
        'at_local':datetime.now().isoformat(timespec='seconds'),'execution_controls':controls,
        'successful_one_step_widths':[r['width'] for r in measured if r['status']=='one_step_completed'],
        'actual_CUDA_OOM_widths':[r['width'] for r in measured if r['status']=='actual_CUDA_out_of_memory'],
        'unattempted_widths':[w for w in WIDTHS if w not in [r['width'] for r in controls]],
        'all_frozen_source_inputs_unchanged':True,'protocol_sha256':sha(OUT/'protocol.json'),
        'full_training_feasibility_orhardware_maximum_not_established':True,
        'first_completed16384_control_repeats_earlier_successful_workload':True,
        'allocation_failures_guards_andtimeouts_do_not_prove_a_global_model_space_maximum':True,
        'no_annual_training_orcandidate_score_orinference_generated':True,'new_quality_scores':0,'test_labels_read':False,
        'scope':'Actual original-fitter one32768-row AdamW step on real mature2020-training inputs. Limits andOOM apply only to these layouts, batch, allocator andobserved background; full resident training inputs andcomplete folds are unmeasured.'})

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--width',type=int,choices=WIDTHS)
    args=parser.parse_args();child(args.width) if args.width else main()
