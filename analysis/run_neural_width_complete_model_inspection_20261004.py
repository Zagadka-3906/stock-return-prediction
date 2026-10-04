"""Inspect all twenty actual saved annual models after completed training proofs."""
from pathlib import Path
import hashlib
import importlib
import json
import sys
import time
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT),str(ROOT/'analysis')]
BANK=ROOT/'analysis/neural_width_bank_20261004'
OUT=ROOT/'analysis/neural_width_complete_model_inspection_execution_20261004'

def read(path):return json.loads(path.read_text(encoding='utf-8-sig'))
def sha(path):
    h=hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda:stream.read(8*1024*1024),b''):h.update(block)
    return h.hexdigest()
def create(path,value):
    with path.open('x',encoding='utf-8') as stream:json.dump(value,stream,ensure_ascii=False,indent=2)

def main():
    import psutil
    gates=[BANK/'oof_audit.json',BANK/'training_execution_scope.json',
        ROOT/'analysis/neural_width_resource_observations_20261004/summary.json']
    while True:
        try:values=[read(p) for p in gates]
        except (FileNotFoundError,json.JSONDecodeError):time.sleep(10);continue
        assert all(v['status']=='passed' for v in values)
        assert len(list(BANK.glob('*/info_202[0-4].json')))==20
        if psutil.virtual_memory().available>=6*2**30:break
        time.sleep(10)
    OUT.mkdir(exist_ok=True);assert not (OUT/'verification.json').exists()
    source=ROOT/'analysis/audit_neural_width_measured_prefix_20261004.py'
    run=ROOT/'analysis/neural_width_complete_model_inspection_run_20261004.json'
    inputs={str(p.resolve()):sha(p) for p in [Path(__file__),source,run,*gates]}
    create(OUT/'frozen_before_inspection.json',{'status':'frozen_before_actual_twenty_model_inspection',
        'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'input_sha256':inputs,
        'available_host_GiB_admission_policy':6.,'new_model_fits':0,'new_quality_scores':0,
        'test_labels_read':False,'scope':'CPU inspection only, no new fit orGPU work. Admission reserve is a scheduling rule.'})
    proof=ROOT/'analysis/neural_width_measured_prefix20_20261004/verification.json'
    if not proof.exists():importlib.import_module('audit_neural_width_measured_prefix_20261004').main()
    actual=read(proof)
    assert actual['status']=='passed' and actual['completed_models_inspected']==20
    assert actual['all20_width_annual_fits_proven_complete'] and actual['inspection_performed_no_GPU_work']
    for path,digest in actual['input_sha256'].items():assert sha(Path(path))==digest,path
    for path,digest in inputs.items():assert sha(Path(path))==digest,path
    create(OUT/'verification.json',{'status':'passed','at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),
        'actual_saved_models_inspected':20,'model_internal_proof':str(proof.resolve()),
        'model_internal_proof_sha256':sha(proof),'input_sha256':inputs,
        'new_model_fits':0,'new_quality_scores':0,'test_labels_read':False,
        'scope':'Actual annual model internals, matched past training controls andfull sampled annual resource window. Full-training future model resources andofficial quality remain separate evidence.'})
    print('Actual twenty saved annual model internals and immutable proof inputs checked',flush=True)

if __name__=='__main__':main()
