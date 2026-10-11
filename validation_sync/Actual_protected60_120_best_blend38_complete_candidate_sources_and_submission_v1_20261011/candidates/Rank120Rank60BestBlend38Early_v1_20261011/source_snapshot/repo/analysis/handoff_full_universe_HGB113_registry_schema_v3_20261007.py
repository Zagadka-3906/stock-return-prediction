"""Transfer only an exactly idle, unexecuted registration helper to schema-correct V2."""
from pathlib import Path
import sys,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from handoff_ready_goss_full_execution_20261006 import start_service
from handoff_joint_goss_round97_full_execution_20261006 import suspended_idle

def main():
    prior_guard=A/'service_owned_workflows_20261006/full_universe_HGB113_schema_v2_actual_handoff'
    while owned(read(prior_guard/'native_launch.json')):time.sleep(15)
    assert read(prior_guard/'service_execution.json')['status']=='failed'
    assert not (A/'service_owned_workflows_20261006/CPU_FULL_HGB44_round113_full_registration_v2').exists()
    out=A/'full_universe_HGB113_registry_schema_v3_actual_handoff_20261007';assert not out.exists();out.mkdir()
    proof=A/'CPU_FULL_HGB44_round113_source_route_preflight_v2_20261007.json';assert read(proof)['status']=='passed_prospective_eight_source_AST_and_original_QA_reverse_routes_only'
    prior=A/'service_owned_workflows_20261006/CPU_FULL_HGB44_round113_full_registration';old=read(prior/'native_launch.json')
    pub=A/'service_owned_workflows_20261006/full_universe_HGB_full113_route_controls_main_publication';assert not owned(read(pub/'native_launch.json')) and read(pub/'service_execution.json')['status']=='passed'
    assert not (A/'optimization_20261003_r113').exists()
    assert not list((A/'CPU_FULL_HGB44_round113_actual_registration_20261007').iterdir())
    names=('neural16384_annual','dependency_queue_v12_local_cache','cpu_full_universe_HGB_native_bank24','full_universe_HGB44_official_comparison_v2','CPU_FULL_HGB44_selected_candidate_preparation','CPU_FULL_HGB44_selected_candidate_sealing','main_publisher_v7')
    preserved={n:read(A/'service_owned_workflows_20261006'/n/'native_launch.json') for n in names};assert all(owned(r) for r in preserved.values())
    sources=[Path(__file__),proof,*[A/n for n in ('prepare_CPU_FULL_HGB44_round113_sources_v2_20261007.py','run_CPU_FULL_HGB44_round113_full_registration_v2_20261007.py','verify_FULL_HGB44_round113_sources_v2_20261007.py','CPU_FULL_HGB44_round113_full_registration_admission_v2_20261007.json','CPU_FULL_HGB44_selected_candidate_source_admission_v2_20261007.json')]]
    pins={str(p.resolve()):sha(p) for p in sources};create(out/'frozen_before_handoff.json',{'input_sha256':pins,'preserved_actual_workers':preserved,'old_helper_expected_scientific_records':0,'missing_old_nonflag_field_detected_in_full_pool_actual_schema':True})
    parent,worker,idle=suspended_idle(old,'    main (run_CPU_FULL_HGB44_round113_full_registration_20261007.py:25)');retired=False
    try:
        assert not worker.children();assert not (A/'optimization_20261003_r113').exists()
        new=start_service('CPU_FULL_HGB44_round113_full_registration_v2','run_CPU_FULL_HGB44_round113_full_registration_v2_20261007.py',[],pins)
        assert all(owned(r) for r in preserved.values()) and owned(new)
        worker.terminate();worker.wait(timeout=15);parent.terminate();parent.wait(timeout=15);retired=True
        create(prior/'administrative_supersession_full_HGB113_schema_v2_20261007.json',{'status':'administratively_retired_exact_idle_unexecuted_registration_helper','identity':old,'successor':new,'idle_before_and_after':idle,'scientific_workers_stopped_or_restarted':0,'actual_official_records_by_old_helper':0})
        create(out/'verification.json',{'status':'passed_actual_idle_fullHGB113_helper_schema_correct_v2_handoff','at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'input_sha256':pins,'old_identity':old,'new_identity':new,'preserved_actual_workers':preserved,'idle_before_and_after':idle,'new_native_fits':0,'new_quality_scores':0,'scientific_workers_stopped_or_restarted':0,'test_labels_read':False})
    finally:
        if not retired:
            for process in (parent,worker):
                if process.is_running():process.resume()
if __name__=='__main__':main()
