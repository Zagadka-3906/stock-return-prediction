"""Serialize unchanged official scorer capacity blocks after scientific andGPU work."""
from pathlib import Path
import hashlib
import json
import os
import subprocess
import sys
import time
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT),str(ROOT/'analysis')]
OUT=ROOT/'analysis/official_worker_frontier_execution_20261004'

def read(path):return json.loads(path.read_text(encoding='utf-8-sig'))
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def create(path,value):
    with path.open('x',encoding='utf-8') as stream:json.dump(value,stream,ensure_ascii=False,indent=2)

def main():
    import psutil
    from verify_official_extended_capacity_20261004 import external_state
    final=ROOT/'results/optimization_20261003_r60.json'
    execution=ROOT/'analysis/optimization_20261003_r60/provenance_scope_execution.json'
    gpu=ROOT/'analysis/neural_width_frontier_20261004/verification.json'
    while True:
        try:values=[read(path) for path in (final,execution,gpu)]
        except (FileNotFoundError,json.JSONDecodeError):time.sleep(10);continue
        assert values[0]['status']=='complete' and values[1]['status']=='passed'
        assert values[2]['status'] in ('passed','failed')
        run=read(ROOT/'analysis/neural_width_frontier_run_20261004.json')
        try:
            proc=psutil.Process(run['pid'])
            still_our_gpu_probe='analysis/probe_neural_width_frontier_20261004.py' in proc.cmdline()
        except psutil.Error:still_our_gpu_probe=False
        if not still_our_gpu_probe and not external_state().get('actual_official_worker_pids'):break
        time.sleep(10)
    OUT.mkdir(exist_ok=True);assert not (OUT/'verification.json').exists()
    plan=ROOT/'analysis/official_worker_frontier_prepared_plan_20261004.json';protocol=read(plan)
    for path,digest in protocol['input_sha256'].items():assert sha(Path(path))==digest,path
    sources=[Path(__file__),plan,final,execution,gpu,
        *[ROOT/f'analysis/verify_official_worker_frontier_{label}_20261004.py' for label in ('forward','reverse')]]
    inputs={str(p.resolve()):sha(p) for p in sources}
    create(OUT/'frozen_before_controls.json',{'status':'frozen_serialized_actual_execution','input_sha256':inputs,
        'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'new_quality_scores':0,'test_labels_read':False})
    blocks=[]
    for label in ('forward','reverse'):
        script=ROOT/f'analysis/verify_official_worker_frontier_{label}_20261004.py'
        stdout=OUT/f'{label}.stdout.log';stderr=OUT/f'{label}.stderr.log'
        with stdout.open('x',encoding='utf-8') as out,stderr.open('x',encoding='utf-8') as err:
            proc=subprocess.Popen([sys.executable,'-B','-X','utf8',str(script)],cwd=ROOT,
                stdout=out,stderr=err,creationflags=subprocess.CREATE_NO_WINDOW if os.name=='nt' else 0)
            while proc.poll() is None:time.sleep(1)
        assert proc.returncode==0,(label,proc.returncode,str(stderr))
        proof=ROOT/f'analysis/official_worker_frontier_{label}_qa_20261004/verification.json'
        value=read(proof);assert value['status']=='passed'
        blocks.append({'block':label,'verification_sha256':sha(proof),'source':str(proof),
            'stdout_sha256':sha(stdout),'stderr_sha256':sha(stderr)})
        print('Actual official worker capacity block completed: '+label,flush=True)
    for path,digest in inputs.items():assert sha(Path(path))==digest,path
    create(OUT/'verification.json',{'status':'passed','at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),
        'input_sha256':inputs,'actual_control_blocks':blocks,'new_quality_scores':0,'test_labels_read':False,
        'scope':'Actual unchanged official scorer at8/10/12/16 workers in separate forward/reverse blocks. Available-memory admission, owned-worker guards andtimeouts retain distinct statuses. Not aglobal capacity orcausal throughput optimum proof.'})

if __name__=='__main__':main()
