"""Serialize auxiliary publication behind real130 and any already-dispatched131 controls."""
from pathlib import Path
from datetime import datetime
import sys,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start

def wait(name):
    f=A/'service_owned_workflows_20261006'/name
    while not (f/'native_launch.json').exists() or owned(read(f/'native_launch.json')):
        assert time.time()<datetime.fromisoformat('2026-10-07T23:35:00+08:00').timestamp();time.sleep(5)
    return read(f/'service_execution.json')

def main():
    assert wait('nonflag_EmpiricalBayes40_round130_full_registration_v1')['status']=='passed'
    dispatch=wait('nonflag_RidgeMicro40_actual131_after130_dependency_queue')
    controls=A/'service_owned_workflows_20261006/nonflag_RidgeMicro40_full37_controls_main_publication_v1'
    if (controls/'native_launch.json').is_file():assert wait(controls.name)['status']=='passed'
    else:assert dispatch['status']=='failed','no dispatched controls despite passing131 queue'
    proof=A/'actual_sparse_publication_context_v2_source_preparation_20261007.json';p=read(proof)
    pins={**p['input_sha256'],str(proof):sha(proof),str(Path(__file__)):sha(Path(__file__))}
    for path,digest in pins.items():assert sha(path)==digest,path
    row=start('actual_sparse_and_isolated_scoring_controls_main_publication_v2','publish_actual_sparse_and_isolated_scoring_controls_main_v2_20261007.py',[],pins)
    create(A/'actual_sparse_publication_safe_main_window_dispatch_20261007.json',{
      'status':'started_auxiliary_publication_after_real130_main_and_actual131_dispatch_state','identity':row,
      'actual131_dispatch_execution':dispatch,'input_sha256':pins,'new_quality_scores':0})

if __name__=='__main__':main()
