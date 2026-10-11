"""Transfer only the idle publisher lease from an exact owned pipe-waiting helper."""
from pathlib import Path
import sys,time,psutil
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from handoff_joint_goss_round97_full_execution_20261006 import stack
from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start

def main():
    out=A/'sparse_main_API_transport_recovery_20261007';folder=A/'service_owned_workflows_20261006/main_publication_API_tree_recovery_lease'
    row=read(folder/'native_launch.json');assert owned(row);worker=psutil.Process(row['owned_worker_pid'])
    trace=stack(worker.pid);assert '_wait_for_tstate_lock (threading.py:' in trace and not worker.children(recursive=True)
    identities=[]
    for key,birth in [('owned_worker_pid','owned_worker_creation_time'),('pid','owned_parent_creation_time')]:
        p=psutil.Process(row[key]);assert abs(p.create_time()-row[birth])<.03
        identities.append({'pid':p.pid,'creation_time':p.create_time(),'cmdline':p.cmdline()})
    for p in identities:psutil.Process(p['pid']).terminate()
    for p in identities:
        try:psutil.Process(p['pid']).wait(timeout=10)
        except psutil.NoSuchProcess:pass
    assert not owned(row)
    driver=A/'finish_API_main_exact_tree_with_file_IO_v2_20261007.py'
    proof=out/'actual_pipe_waiting_holder_administrative_transfer_v2.json'
    create(proof,{'status':'transferred_exact_idle_main_publisher_lease_from_owned_pipe_waiting_helper',
      'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'previous_holder':identities,'readonly_previous_holder_stack':trace,
      'no_scientific_workers_stopped_or_restarted':True,'original_helper_not_marked_scientifically_passed':True,
      'input_sha256':{str(p):sha(p) for p in [Path(__file__),driver,out/'frozen_exact_API_tree_payload.json',out/'actual_API_ref_update_and_release.json',*folder.glob('*.json'),*folder.glob('*.log')]}})
    row=start('main_publication_API_tree_recovery_lease_v2',driver.name,[],{**read(proof)['input_sha256'],str(proof):sha(proof)})
    create(out/'actual_hidden_file_IO_lease_v2_launch.json',{'identity':row,'new_quality_scores':0})

if __name__=='__main__':main()
