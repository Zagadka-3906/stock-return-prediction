"""Wait for actual immutable proofs, audit them, refresh only mutable execution evidence."""
from pathlib import Path
import hashlib
import importlib
import json
import sys
import time
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT),str(ROOT/'analysis')]

def read(path):return json.loads(path.read_text(encoding='utf-8-sig'))
def sha(path):
    h=hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda:stream.read(8*1024*1024),b''):h.update(block)
    return h.hexdigest()
def wait_for(paths):
    while True:
        try:values=[read(path) for path in paths]
        except (FileNotFoundError,json.JSONDecodeError):time.sleep(10);continue
        for path,value in zip(paths,values):assert value['status']=='passed',path
        return
def refresh(**fields):
    path=ROOT/'analysis/neural_width_search_execution_20261004.json';value=read(path)
    value.update(fields,updated_at_local=time.strftime('%Y-%m-%dT%H:%M:%S'))
    path.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

def main():
    bank=ROOT/'analysis/neural_width_bank_20261004'
    wait_for([bank/'oof_audit.json',bank/'training_execution_scope.json',
        ROOT/'analysis/neural_width_resource_observations_20261004/summary.json'])
    importlib.import_module('audit_neural_width_resource_scope_20261004').main()
    refresh(annual_training_status='passed',actual_annual_fits=20,
        annual_resource_scope_audit='analysis/neural_width_resource_scope_audit_20261004.json')
    print('Actual20-fit width OOF and resource scope audited',flush=True)
    future=ROOT/'analysis/neural_width_future_models_qa_20261004/verification.json'
    wait_for([future]);importlib.import_module('audit_neural_width_future_resources_20261004').main()
    refresh(future_model_preflight_status='passed',future_model_preflight_sha256=sha(future),
        future_resource_scope_audit='analysis/neural_width_future_resource_scope_audit_20261004.json')
    print('Actual four mature full-model future controls and resources audited',flush=True)
    complete=ROOT/'analysis/neural_width_complete_scheme_preflight_20261004/verification.json'
    wait_for([complete]);proof=read(complete)
    for path,digest in proof['input_sha256'].items():assert sha(Path(path))==digest,path
    for case,digest in proof['candidate_verification_sha256'].items():
        path=complete.parent/case/'candidate/verification.json';assert sha(path)==digest,path
        candidate=read(path);assert candidate['status']=='passed'
        assert sha(path.parent/'submission.csv')==candidate['csv_sha256']
        assert (candidate['rows'],candidate['days'],candidate['codes'])==(1599600,344,4650)
    refresh(complete_scheme_preflight_status='passed',complete_scheme_preflight_sha256=sha(complete),
        complete_scheme_preflight_pending=False,status='implementation_gates_passed_actual_predecessor_comparisons_pending')
    print('Complete width scheme inputs and four actual full candidate CSVs audited',flush=True)

if __name__=='__main__':main()
