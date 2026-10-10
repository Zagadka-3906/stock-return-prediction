"""Restart only proven failed dependencies; retain all original scientific jobs."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis'
sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from handoff_ready_goss_full_execution_20261006 import start_service
from prepare_local_118_119_protocol_recovery_v4_20261007 import FILES

def main():
    proof_path=A/'local_118_119_protocol_recovery_source_preparation_v4_20261007.json'
    proof=read(proof_path); pins=dict(proof['input_sha256'])
    pins.update({str(p):sha(p) for p in [Path(__file__),proof_path,
      A/'local_118_119_recovery_prospective_v4_20261007.json',
      A/'resolve_sealed_scientific_protocol_20261007.py']})
    launches={}
    for old in proof['replaced_failed_services']:
        folder=A/'service_owned_workflows_20261006'/old
        assert not owned(read(folder/'native_launch.json'))
        assert read(folder/'service_execution.json')['status']=='failed'
        definition=read(folder/'job_definition.json')
        driver=FILES[Path(definition['driver']).name]
        name=proof['service_mapping'][old]
        try:row=start_service(name,driver,definition['arguments'],pins)
        except AssertionError:
            folder=A/'service_owned_workflows_20261006'/name
            row=read(folder/'native_launch.json')
            assert not owned(row) and read(folder/'service_execution.json')['status']=='passed'
        launches[name]=row
    create(A/'local_118_119_protocol_recovery_actual_hidden_launches_v4_20261007.json',{
      'status':'started_actual17_consoleless_local_dependency_services',
      'input_sha256':pins,'launches':launches,'original_scientific_workers_stopped':0,
      'new_native_fits_by_launcher':0,'new_quality_scores_by_launcher':0,'test_labels_read':False})
    print({'status':'started','actual_hidden_local_services':len(launches)},flush=True)

if __name__=='__main__':main()
