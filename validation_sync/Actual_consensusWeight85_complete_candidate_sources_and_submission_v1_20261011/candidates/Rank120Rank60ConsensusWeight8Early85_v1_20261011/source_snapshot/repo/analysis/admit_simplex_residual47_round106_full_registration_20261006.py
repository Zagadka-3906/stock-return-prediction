"""Wait for genuine47-case inference, main scores, full105 and original R90."""
from pathlib import Path
import runpy
import sys
import time

ROOT=Path(__file__).resolve().parents[1]
A=ROOT/'analysis'
sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from atomic_optimization_observer_writes_20261005 import write


def main():
    import psutil
    prep=A/'simplex_residual47_full_registration_preparation_20261006.json'
    pins=read(prep)['input_sha256']
    services={name:A/'service_owned_workflows_20261006'/name for name in (
        'simplex_residual47_candidate_inference','simplex_residual47_candidate_sealing',
        'robust_residual50_round105_full_registration','residual_simplex47_scores_evidence_publication')}
    identities={name:read(folder/'native_launch.json') for name,folder in services.items()}
    queue=A/'service_owned_dependency_queue_v4_20261006'
    out=A/'simplex_residual47_round106_registration_admission_20261006'
    assert not out.exists();out.mkdir()
    original90=None
    while True:
        closed={name:not owned(row) for name,row in identities.items()}
        terminal={name:read(folder/'service_execution.json') if (folder/'service_execution.json').exists() else None
            for name,folder in services.items()}
        failures={name:row for name,row in terminal.items() if row and row['status']!='passed' and closed[name]}
        assert not failures,failures
        passed=all(closed.values()) and all(row and row['status']=='passed' for row in terminal.values())
        if original90 is None:
            row=read(queue/'state.json')['activated_jobs'].get('round90')
            if row is not None:
                original90=row;create(out/'original90_writer_identity_before_wait.json',row)
        original_closed=original90 is None or not owned(original90)
        if original90 is not None and original_closed:
            assert (queue/'activated_jobs/round90/execution.json').exists()
        available=psutil.virtual_memory().available/2**30
        write(out/'waiting_status.json',{
            'status':'waiting_for_real47_candidate_seal_full105_main47_scores_and_original90_writer',
            'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),
            'preceding_services_naturally_closed':closed,'preceding_services_naturally_passed':passed,
            'original90_writer_seen':original90 is not None,'original90_writer_closed':original_closed,
            'available_RAM_GiB':available,'scientific_workers_suspended_stopped_or_restarted':0})
        if passed and original_closed and available>=8:break
        time.sleep(30)
    for path,digest in pins.items():assert sha(path)==digest,path
    create(out/'actual_admission.json',{
        'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'input_sha256':pins,
        'preceding_full105_and_actual47_main_scores_naturally_passed':True,
        'original90_writer_identity':original90,'original90_writer_naturally_terminal_if_seen':original_closed,
        'scientific_workers_suspended_stopped_or_restarted':0,'test_labels_read':False})
    runpy.run_path(str(A/'run_simplex_residual47_round106_full_registration_20261006.py'),run_name='__main__')


if __name__=='__main__':main()
