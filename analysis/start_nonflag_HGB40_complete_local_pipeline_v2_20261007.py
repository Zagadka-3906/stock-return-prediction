"""Start seven real local stages, with qualified119 and source admission gates."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis'
sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from handoff_ready_goss_full_execution_20261006 import start_service

def main():
    jobs=[
      ('nonflag_HGB40_round120_source_admission','verify_nonflag_HGB40_round120_sources_v2_20261007.py',[]),
      ('nonflag_HGB40_full37_controls_main_publication','publish_nonflag_HGB40_evidence_v2_20261007.py',['controls']),
      ('nonflag_HGB40_official_comparison','run_nonflag_HGB40_admitted_comparison_v2_20261007.py',[]),
      ('nonflag_HGB40_scores_main_publication','publish_nonflag_HGB40_evidence_v2_20261007.py',['scores']),
      ('nonflag_HGB40_selected_candidate_preparation','prepare_nonflag_HGB40_selected_candidate_v2_20261007.py',[]),
      ('nonflag_HGB40_selected_candidate_sealing','seal_nonflag_HGB40_selected_candidate_v2_20261007.py',[]),
      ('nonflag_HGB40_round120_full_registration','run_nonflag_HGB40_round120_full_registration_v2_20261007.py',[])]
    sources=[Path(__file__),*[A/driver for _,driver,_ in jobs],
      A/'run_nonflag_HGB40_official_comparison_v2_20261007.py',A/'prepare_nonflag_HGB40_round120_sources_v2_20261007.py',
      A/'nonflag_HGB40_plan_20261007.json',A/'nonflag_HGB40_prospective24_source_and12_graph_preflight_v2_20261007.json',
      A/'nonflag_HGB40_complete_routes_source_preparation_v2_20261007.json',A/'resolve_sealed_scientific_protocol_20261007.py',
      A/'predict_nonflag_residual_HGB_complete_scheme_20261007.py',A/'nonflag_residual_HGB_native_stage_20261007.py',
      A/'nonflag_residual_HGB_CDF_transform_20261007.py',A/'nonflag_residual_HGB_preprocessing_20261007.py',
      A/'nonflag_residual_HGB_bank10_20261007/verification.json',A/'nonflag_residual_HGB37_transform_preflight_20261007/verification.json',
      A/'nonflag_residual_HGB_native_hook3_preflight_20261007/verification.json',ROOT/'evaluate.py',ROOT/'后续选模标准.md']
    for p in sources:
        assert p.is_file(),p
        if p.suffix=='.py':compile(p.read_text(encoding='utf8'),str(p),'exec')
    pins={str(p):sha(p) for p in sources}
    assert pins[str(ROOT/'evaluate.py')]=='72dc59987e92ba8ae6b506e114dfe8591b5608c9beccd0769d5d1f778f9189c2'
    launches={}
    for name,driver,args in jobs:
        try:r=start_service(name,driver,args,pins)
        except AssertionError:
            folder=A/'service_owned_workflows_20261006'/name;r=read(folder/'native_launch.json')
            assert not owned(r) and read(folder/'service_execution.json')['status']=='passed',name
        launches[name]=r
    create(A/'nonflag_HGB40_complete_pipeline_actual_hidden_launches_20261007.json',{
      'status':'started_actual_seven_consoleless_local120_dependency_stages','input_sha256':pins,'launches':launches,
      'actual10_native_fits37_full111_cold_and3_historical_hooks_preserved':True,
      'actual_qualified119_and24_source_admission_required_before40_scoring':True,
      'remote_tasks_dispatched':0,'scientific_workers_stopped':0,'new_quality_scores_by_launcher':0,
      'full120_qualification_not_claimed':True,'test_labels_read':False})
    print({'status':'started','actual_hidden_local_stages':len(launches)},flush=True)

if __name__=='__main__':main()
