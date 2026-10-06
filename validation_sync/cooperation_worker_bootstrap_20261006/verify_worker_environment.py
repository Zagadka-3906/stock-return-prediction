"""Inventory the worker and perform a small CUDA forward/backward compatibility check."""
from pathlib import Path
import argparse
import importlib.metadata
import json
import platform
import socket
import sys
import time


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--worker-id',required=True,choices=['worker1','worker2'])
    parser.add_argument('--output',required=True)
    args=parser.parse_args()
    target=Path(args.output).resolve()
    if target.drive.upper() not in ('D:','E:'):
        raise ValueError('Write worker reports on D: or E:.')
    if target.exists():
        raise FileExistsError(target)
    report={'status':'worker_environment_check_started','worker_id':args.worker_id,
        'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'hostname':socket.gethostname(),
        'python':platform.python_version(),'python_executable':sys.executable,
        'platform':platform.platform(),'dependencies':{},'training_performed':False,
        'data_or_test_labels_read':False,'GPU_training_throughput_not_benchmarked':True}
    error=None
    try:
        expected={line.split('==')[0]:line.split('==')[1] for line in
            (Path(__file__).parent/'requirements-worker-core.txt').read_text(encoding='utf-8').splitlines() if line.strip()}
        for name,version in expected.items():
            actual=importlib.metadata.version(name)
            report['dependencies'][name]=actual
            if actual!=version:raise RuntimeError(f'{name}: expected {version}, got {actual}')
        import psutil
        report['RAM_GiB']=round(psutil.virtual_memory().total/2**30,2)
        report['available_RAM_GiB']=round(psutil.virtual_memory().available/2**30,2)
        report['logical_CPUs']=psutil.cpu_count()
        import torch
        report['dependencies']['torch']=torch.__version__
        report['torch_cuda']=torch.version.cuda
        report['cuda_available']=torch.cuda.is_available()
        if torch.__version__!='2.11.0+cu128' or torch.version.cuda!='12.8':
            raise RuntimeError('Expected the canonical torch2.11.0+cu128 / CUDA12.8 build.')
        if not torch.cuda.is_available():raise RuntimeError('CUDA is unavailable; check NVIDIA driver and GPU package installation.')
        gpu=torch.cuda.get_device_properties(0)
        report['GPU']={'name':gpu.name,'VRAM_GiB':round(gpu.total_memory/2**30,2),
            'compute_capability':[gpu.major,gpu.minor]}
        torch.manual_seed(20261006)
        with torch.enable_grad():
            x=torch.randn(512,512,device='cuda',requires_grad=True)
            w=torch.randn(512,128,device='cuda',requires_grad=True)
            loss=(x@w).square().mean()
            loss.backward()
            torch.cuda.synchronize()
            if not torch.isfinite(loss).item() or not torch.isfinite(x.grad).all().item():
                raise RuntimeError('CUDA forward/backward check produced non-finite values.')
        report['actual_small_CUDA_forward_backward_passed']=True
        report['status']='passed_matching_worker_dependencies_and_actual_small_CUDA_forward_backward'
    except Exception as exc:
        error=exc
        report['status']='failed_worker_environment_check_preserved'
        report['error']=f'{type(exc).__name__}: {exc}'
    target.parent.mkdir(parents=True,exist_ok=True)
    with target.open('x',encoding='utf-8') as stream:
        json.dump(report,stream,ensure_ascii=False,indent=2,allow_nan=False)
        stream.write('\n')
    print(json.dumps(report,ensure_ascii=False))
    if error is not None:raise SystemExit(2)


if __name__=='__main__':main()
