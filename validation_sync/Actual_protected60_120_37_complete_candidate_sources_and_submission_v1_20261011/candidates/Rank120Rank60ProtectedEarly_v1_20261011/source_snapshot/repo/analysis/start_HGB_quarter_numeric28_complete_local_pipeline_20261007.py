"""Start eight hidden local dependency workers for the full118 closure."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis'
sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from handoff_ready_goss_full_execution_20261006 import start_service

def main():
    out=A/'HGB_quarter_numeric28_complete_pipeline_actual_hidden_launches_20261007.json';assert not out.exists()
    jobs=[
      ('HGB_quarter_numeric28_full25_transform_preflight','run_HGB_quarter_numeric28_controls_after117_20261007.py',[]),
      ('HGB_quarter_numeric28_round118_source_admission','verify_HGB_quarter_numeric28_round118_sources_v3_20261007.py',[]),
      ('HGB_quarter_numeric28_full25_controls_main_publication','publish_HGB_quarter_numeric28_evidence_v3_20261007.py',['controls']),
      ('HGB_quarter_numeric28_official_comparison','run_HGB_quarter_numeric28_admitted_comparison_20261007.py',[]),
      ('HGB_quarter_numeric28_scores_main_publication','publish_HGB_quarter_numeric28_evidence_v3_20261007.py',['scores']),
      ('HGB_quarter_numeric28_selected_candidate_preparation','prepare_HGB_quarter_numeric28_selected_candidate_20261007.py',[]),
      ('HGB_quarter_numeric28_selected_candidate_sealing','seal_HGB_quarter_numeric28_selected_candidate_20261007.py',[]),
      ('HGB_quarter_numeric28_round118_full_registration','run_HGB_quarter_numeric28_round118_full_registration_v2_20261007.py',[])]
    import prepare_HGB_quarter_numeric28_round118_sources_v2_20261007 as generator
    sources=[Path(__file__),*[A/driver for _,driver,_ in jobs],Path(generator.__file__),Path(generator.base.__file__),
      *[A/n for n in generator.base.NAMES],A/'verify_HGB_quarter_numeric28_transform_v3_20261007.py',
      A/'run_HGB_quarter_numeric28_official_comparison_20261007.py',A/'HGB_quarter_numeric28_plan_20261007.json',
      A/'HGB_quarter_numeric28_prospective_source_paths_and_metadata_preflight_20261007.json',
      A/'HGB_quarter_numeric28_complete_scope_source_preparation_v3_20261007.json',
      A/'predict_refined_weighted_flagged_CPU_HGB_scheme_v2_20261007.py',
      A/'predict_flagged_CPU_HGB_weighted_quarters_scheme_v2_20261007.py',
      A/'predict_lower_pool_after_weighted_flagged_CPU_HGB_scheme_v2_20261007.py',
      A/'all_forecast_percentile_runtime_20261007.py',A/'exact_numpy_all_forecast_percentiles_20261007.py',
      A/'all_forecast_percentiles_full_scoring_benchmark_20261007/verification.json',ROOT/'evaluate.py',ROOT/'后续选模标准.md']
    pins={str(p):sha(p) for p in sources}
    for p in sources:
        if p.suffix=='.py':compile(p.read_text(encoding='utf8'),str(p),'exec')
    assert pins[str(ROOT/'evaluate.py')]=='72dc59987e92ba8ae6b506e114dfe8591b5608c9beccd0769d5d1f778f9189c2'
    launches={}
    for name,driver,args in jobs:
        try:r=start_service(name,driver,args,pins)
        except AssertionError:
            folder=A/'service_owned_workflows_20261006'/name;r=read(folder/'native_launch.json')
            assert not owned(r) and read(folder/'service_execution.json')['status']=='passed',name
        assert r['actual_native_console_handle']==0 and not r['independent_launch_root_in_any_job'];launches[name]=r
    create(out,{'status':'actual_eight_consoleless_local118_dependency_workers_started',
      'input_sha256':pins,'launches':launches,'actual117_closure_required_before25_controls':True,
      'actual25_controls_and24_sources_and_real117_baselines_required_before28_scoring':True,
      'remote_tasks_dispatched':0,'scientific_workers_stopped':0,'new_native_fits_by_launcher':0,'new_quality_scores_by_launcher':0,
      'actual118_official_scoring_and_future_inference_and_fullQA29_not_claimed':True,'test_labels_read':False})
    print({'status':'started_actual_local118_pipeline','jobs':len(launches)},flush=True)

if __name__=='__main__':main()
