"""Start real hidden local dependency jobs; heavy phases remain sequential."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis'
sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from handoff_ready_goss_full_execution_20261006 import start_service

def main():
    out=A/'weighted_HGB340_complete_pipeline_actual_hidden_launches_20261007.json';assert not out.exists()
    controls=read(A/'service_owned_workflows_20261006/weighted_flagged_HGB_full337_transform_preflight_v3/native_launch.json')
    assert owned(controls) or read(A/'service_owned_workflows_20261006/weighted_flagged_HGB_full337_transform_preflight_v3/service_execution.json')['status']=='passed'
    jobs=[
      ('weighted_HGB340_round117_source_admission','verify_weighted_HGB340_round117_sources_20261007.py',[]),
      ('weighted_HGB340_full337_controls_main_publication','publish_weighted_HGB340_evidence_20261007.py',['controls']),
      ('flagged_HGB_weighted_quarters340_official_comparison','run_weighted_HGB340_admitted_official_comparison_20261007.py',[]),
      ('flagged_HGB_weighted_quarters340_scores_main_publication','publish_weighted_HGB340_evidence_20261007.py',['scores']),
      ('flagged_HGB_weighted_quarters340_selected_candidate_preparation','prepare_flagged_HGB_weighted_quarters340_selected_candidate_v3_20261007.py',[]),
      ('flagged_HGB_weighted_quarters340_selected_candidate_sealing','seal_flagged_HGB_weighted_quarters340_selected_candidate_v3_20261007.py',[]),
      ('weighted_HGB340_round117_full_registration','run_weighted_HGB340_round117_full_registration_20261007.py',[])]
    sources=[Path(__file__),*[A/name for _,name,_ in jobs],
      A/'run_flagged_HGB_weighted_quarters340_official_comparison_v3_20261007.py',
      A/'prepare_weighted_HGB340_round117_sources_20261007.py',
      A/'weighted_HGB340_actual_prospective_source_paths_and_metadata_preflight_20261007.json',
      A/'predict_refined_weighted_flagged_CPU_HGB_scheme_v2_20261007.py',
      A/'predict_flagged_CPU_HGB_weighted_quarters_scheme_v2_20261007.py',
      A/'predict_lower_pool_after_weighted_flagged_CPU_HGB_scheme_v2_20261007.py',
      A/'flagged_HGB_weighted_quarters340_plan_20261007.json',
      A/'all_forecast_percentile_runtime_20261007.py',A/'exact_numpy_all_forecast_percentiles_20261007.py',
      A/'all_forecast_percentiles_full_scoring_benchmark_20261007/verification.json',
      ROOT/'evaluate.py',ROOT/'后续选模标准.md']
    pins={str(p):sha(p) for p in sources}
    for p in sources:
        if p.suffix=='.py':compile(p.read_text(encoding='utf8'),str(p),'exec')
    assert pins[str(ROOT/'evaluate.py')]=='72dc59987e92ba8ae6b506e114dfe8591b5608c9beccd0769d5d1f778f9189c2'
    launches={}
    for name,driver,args in jobs:
        try:row=start_service(name,driver,args,pins)
        except AssertionError:
            folder=A/'service_owned_workflows_20261006'/name
            row=read(folder/'native_launch.json')
            assert not owned(row) and read(folder/'service_execution.json')['status']=='passed',name
        assert row['actual_native_console_handle']==0 and not row['independent_launch_root_in_any_job']
        launches[name]=row
    create(out,{'status':'actual_seven_local_consoleless_dependency_jobs_started',
      'input_sha256':pins,'launches':launches,'preserved_full337_controls_identity':controls,
      'remote_tasks_dispatched':0,'new_native_fits_by_launcher':0,'new_quality_scores_by_launcher':0,
      'actual340_scoring_and_full117_not_yet_claimed':True,'scientific_workers_stopped':0,'test_labels_read':False})
    print({'status':'started_actual_local_pipeline','jobs':len(launches)},flush=True)

if __name__=='__main__':main()
