"""Replace only the exact idle observer, preserving original scientific identities."""
from pathlib import Path
import sys
import time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis'
sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from handoff_ready_goss_full_execution_20261006 import start_service
from handoff_joint_goss_round97_full_execution_20261006 import suspended_idle

def main():
    out=A/'local_only_monitor_v15_actual_handoff_20261007';assert not out.exists();out.mkdir()
    old_folder=A/'service_owned_workflows_20261006/local_only_progress_monitor_v14';old=read(old_folder/'native_launch.json')
    old_source=A/'monitor_local_only_runtime_v14_20261007.py'
    sleep_line=next(i+1 for i,line in enumerate(old_source.read_text(encoding='utf8').splitlines()) if line.strip()=='time.sleep(30)')
    sources=[Path(__file__),old_source,A/'monitor_local_only_runtime_v15_20261007.py',A/'weighted_HGB340_complete_pipeline_actual_hidden_launches_20261007.json',A/'weighted_HGB340_round117_source_admission_20261007.json']
    preserved={name:read(A/'service_owned_workflows_20261006'/name/'native_launch.json') for name in ('neural16384_annual','dependency_queue_v12_local_cache')}
    assert all(owned(r) for r in preserved.values())
    pins={str(p):sha(p) for p in sources};create(out/'frozen_before_handoff.json',{'input_sha256':pins,'preserved_actual_workers':preserved})
    parent,worker,idle=suspended_idle(old,f'    <module> (monitor_local_only_runtime_v14_20261007.py:{sleep_line})')
    retired=False
    try:
        assert not worker.children();create(out/'old_observer_exact_idle_before_and_after.json',idle)
        new=start_service('local_only_progress_monitor_v15','monitor_local_only_runtime_v15_20261007.py',[],pins)
        for _ in range(50):
            assert owned(new)
            current=read(A/'actual_optimization_monitor_state_20261005.json')
            if current.get('actual_observer_version')=='local_only_v15' and current['local_only_live_status']['monitor_pid']==new['owned_worker_pid']:break
            time.sleep(1)
        else:raise RuntimeError('Observer15 has not published a complete generation')
        live=current['local_only_live_status'];assert live['R90_actual_full_scope_and_main_qualified'] is True
        assert all(owned(r) for r in preserved.values())
        create(out/'actual_first_complete_public_generation.json',current)
        worker.terminate();worker.wait(timeout=15);parent.terminate();parent.wait(timeout=15);retired=True
        create(old_folder/'administrative_supersession_local_v15_20261007.json',{'status':'administratively_retired_exact_idle_observer_not_scientific_completion','identity':old,'successor':new,'scientific_workers_stopped':0})
        create(out/'verification.json',{'status':'passed_actual_idle_observer14_complete118_119_and_nonflag_training_routes_and_R90_gate',
            'input_sha256':pins,'new_identity':new,'generation':current['complete_observer_generation'],'preserved_actual_workers':preserved,
            'new_native_fits':0,'new_quality_scores':0,'scientific_workers_stopped':0,'test_labels_read':False})
    finally:
        if not retired:
            for process in (parent,worker):
                if process.is_running():process.resume()

if __name__=='__main__':main()
