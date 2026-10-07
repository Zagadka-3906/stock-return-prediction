"""Correct the stale service identities without changing actual training or observation."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis'
sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from handoff_ready_goss_full_execution_20261006 import start_service

def main():
    old=A/'service_owned_workflows_20261006/CPU_full_bank_resource_observer_ElasticNet_main_publication_v3'
    assert not owned(read(old/'native_launch.json'))
    assert read(old/'service_execution.json')['status']=='failed'
    proof_path=A/'CPU_ElasticNet_full_bank_resource_observation_v3_20261007/verification.json'
    proof=read(proof_path)
    actual=A/'service_owned_workflows_20261006/cpu_full_universe_ElasticNet_native_bank24_v3'
    assert proof['actual_terminal']==read(actual/'service_execution.json') and proof['actual_native_fits']==24
    source=A/'publish_CPU_full_bank_resource_observers_v4_20261007.py'
    target=A/'publish_CPU_full_bank_resource_observers_v5_20261007.py';assert not target.exists()
    text=source.read_text(encoding='utf8')
    edits={
        "observer_name = f'CPU_{kind}_full_bank_resource_observer_v2'":"observer_name = f'CPU_{kind}_full_bank_resource_observer_' + ('v3' if kind == 'ElasticNet' else 'v2')",
        "bank_name = f'cpu_full_universe_{kind}_native_bank24_v2'":"bank_name = f'cpu_full_universe_{kind}_native_bank24_' + ('v3' if kind == 'ElasticNet' else 'v2')",
        "('_v3' if kind == 'ElasticNet' else '_v2')":"('_v4' if kind == 'ElasticNet' else '_v2')",
        "out = A / f'CPU_full_bank_resource_observer_{phase}_v3_github_20261007'":"out = A / f'CPU_full_bank_resource_observer_{phase}_v4_github_20261007'",
        "validation_sync/CPU_full_bank_resource_observer_{phase}_v2_20261007":"validation_sync/CPU_full_bank_resource_observer_{phase}_v4_20261007",
        "sources = [Path(__file__), A / 'observe_CPU_full_bank_resources_v4_20261007.py']":"sources = [Path(__file__), A / 'observe_CPU_full_bank_resources_v4_20261007.py', A / 'prepare_ElasticNet_resource_publication_v5_20261007.py', *list((A / 'service_owned_workflows_20261006/CPU_full_bank_resource_observer_ElasticNet_main_publication_v3').glob('*.json')), *list((A / 'service_owned_workflows_20261006/CPU_full_bank_resource_observer_ElasticNet_main_publication_v3').glob('*.log'))]"
    }
    for before,after in edits.items():
        assert text.count(before)==1,before
        text=text.replace(before,after)
    compile(text,str(target),'exec')
    with target.open('x',encoding='utf8',newline='\n') as f:f.write(text)
    pins={str(p):sha(p) for p in (Path(__file__),source,target,proof_path,old/'stderr.log',old/'service_execution.json')}
    row=start_service('CPU_full_bank_resource_observer_ElasticNet_main_publication_v4',target.name,['ElasticNet'],pins)
    create(A/'ElasticNet_resource_publication_v5_actual_hidden_launch_20261007.json',{'input_sha256':pins,'actual_native_launch':row,'actual_fits_repeated':0,'new_quality_scores':0,'scientific_workers_stopped':0,'old_failure_preserved':True})
    print({'status':'launched','owned_worker_pid':row['owned_worker_pid']},flush=True)

if __name__=='__main__':main()
