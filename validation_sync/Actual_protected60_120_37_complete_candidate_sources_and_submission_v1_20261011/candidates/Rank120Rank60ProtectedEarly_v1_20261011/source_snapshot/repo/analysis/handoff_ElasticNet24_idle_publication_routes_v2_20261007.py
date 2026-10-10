"""Correct one unexecuted prospective source filename; preserve all scientific jobs."""
from pathlib import Path
import sys,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from handoff_ready_goss_full_execution_20261006 import start_service
from handoff_joint_goss_round97_full_execution_20261006 import suspended_idle

def main():
    out=A/'ElasticNet24_idle_publication_routes_v2_actual_handoff_20261007';assert not out.exists();out.mkdir()
    source=A/'publish_cpu_full_universe_ElasticNet24_evidence_v2_20261007.py';assert (A/'verify_cpu_ElasticNet63_codec_20261007.py').exists()
    pins={str(p.resolve()):sha(p) for p in [Path(__file__),source,A/'publish_cpu_full_universe_ElasticNet24_evidence_20261007.py']}
    names=('neural16384_annual','dependency_queue_v12_local_cache','cpu_full_universe_ElasticNet_native_bank24','full_universe_ElasticNet44_official_comparison','main_publisher_v7')
    preserved={n:read(A/'service_owned_workflows_20261006'/n/'native_launch.json') for n in names};assert all(owned(r) for r in preserved.values())
    create(out/'frozen_before_actual_handoff.json',{'input_sha256':pins,'preserved_scientific_workers':preserved,'new_scientific_records':0})
    controls=[]
    for phase in ('bank','scores'):
        assert not (A/f'cpu_full_universe_ElasticNet24_{phase}_github_20261007').exists()
        old_name=f'cpu_full_universe_ElasticNet24_{phase}_evidence_publication';old_dir=A/'service_owned_workflows_20261006'/old_name;old=read(old_dir/'native_launch.json')
        parent,worker,idle=suspended_idle(old,'    wait_closed (publish_cpu_full_universe_ElasticNet24_evidence_20261007.py:24)');retired=False
        try:
            assert not worker.children()
            new=start_service(old_name+'_v2',source.name,[phase],pins)
            assert owned(new) and all(owned(r) for r in preserved.values())
            worker.terminate();worker.wait(timeout=15);parent.terminate();parent.wait(timeout=15);retired=True
            event={'status':'administratively_retired_exact_idle_unexecuted_publication_helper','phase':phase,'identity':old,'successor':new,'idle_before_and_after':idle,'new_scientific_records':0,'scientific_workers_stopped_or_restarted':0}
            create(old_dir/'administrative_supersession_ElasticNet24_routes_v2_20261007.json',event);controls.append(event)
        finally:
            if not retired:
                for process in (parent,worker):
                    if process.is_running():process.resume()
    create(out/'verification.json',{'status':'passed_actual_two_idle_ElasticNet_bank_score_publishers_source_route_v2_handoff','at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'input_sha256':pins,'controls':controls,'preserved_scientific_workers':preserved,'new_fits':0,'new_official_scores':0,'test_labels_read':False})
if __name__=='__main__':main()
