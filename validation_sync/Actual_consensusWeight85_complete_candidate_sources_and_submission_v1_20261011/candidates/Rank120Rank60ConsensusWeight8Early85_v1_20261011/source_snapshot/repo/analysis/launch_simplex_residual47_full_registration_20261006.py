"""Admit full106 behind actual candidate seal, main47 scores and prior full105."""
from pathlib import Path
import sys
import time

ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis'
sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from handoff_ready_goss_full_execution_20261006 import start_service


def main():
    prep=A/'simplex_residual47_full_registration_preparation_20261006.json'
    pins={**read(prep)['input_sha256'],str(prep):sha(prep),str(Path(__file__)):sha(Path(__file__))}
    for path,digest in pins.items():assert sha(path)==digest,path
    assert not (A/'optimization_20261003_r106').exists()
    state=read(A/'service_owned_dependency_queue_v4_20261006/state.json')
    originals={name:row for name,row in state['activated_jobs'].items() if owned(row)}
    wide=read(A/'service_owned_workflows_20261006/neural16384_annual/native_launch.json')
    if owned(wide):originals['neural16384_annual']=wide
    row=start_service('simplex_residual47_round106_full_registration',
        'admit_simplex_residual47_round106_full_registration_20261006.py',[],pins)
    assert owned(row)
    create(A/'simplex_residual47_workflow_admission_20261006/full_registration_hidden_launch.json',{
        'status':'passed_actual_hidden_owned_full106_admission_waiting_for_genuine_dependencies',
        'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'identity':row,'input_sha256':pins,
        'original_scientific_workers_preserved_at_launch':originals,
        'actual_native_console_handle':row['actual_native_console_handle'],
        'actual_complete_ranking_and_main_publication_not_claimed_complete':True,
        'scientific_workers_suspended_stopped_or_restarted':0,'test_labels_read':False})
    print('Full106 admitted after actual47 inference/seal, main scores and preceding full105.',flush=True)


if __name__=='__main__':main()
