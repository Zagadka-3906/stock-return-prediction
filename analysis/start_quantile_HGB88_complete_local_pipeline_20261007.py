"""Launch seven hidden local dependency jobs; preserve all existing scientific workers."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis'
sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from handoff_ready_goss_full_execution_20261006 import start_service
def main():
    out=A/'quantile_HGB88_complete_pipeline_actual_hidden_launches_20261007.json';assert not out.exists()
    jobs=[
      ('quantile_HGB88_round119_source_admission','verify_quantile_HGB88_round119_sources_v2_20261007.py',[]),
      ('quantile_HGB88_full85_controls_main_publication','publish_quantile_HGB88_evidence_v2_20261007.py',['controls']),
      ('quantile_HGB88_official_comparison','run_quantile_HGB88_admitted_comparison_20261007.py',[]),
      ('quantile_HGB88_scores_main_publication','publish_quantile_HGB88_evidence_v2_20261007.py',['scores']),
      ('quantile_HGB88_selected_candidate_preparation','prepare_quantile_HGB88_selected_candidate_20261007.py',[]),
      ('quantile_HGB88_selected_candidate_sealing','seal_quantile_HGB88_selected_candidate_20261007.py',[]),
      ('quantile_HGB88_round119_full_registration','run_quantile_HGB88_round119_full_registration_v2_20261007.py',[])]
    sources=[Path(__file__),*[A/s for n,s,args in jobs],
      A/'run_quantile_HGB88_official_comparison_20261007.py',A/'prepare_quantile_HGB88_round119_sources_v2_20261007.py',
      A/'quantile_HGB88_plan_20261007.json',A/'quantile_HGB88_complete_routes_source_preparation_v2_20261007.json',
      A/'quantile_HGB88_complete_pipeline_source_preparation_20261007.json',A/'quantile_HGB88_workflow_source_preparation_20261007.json',
      A/'quantile_HGB88_prospective_graph_and_paths_preflight_20261007.json',
      A/'predict_quantile_HGB_residual_CDF_scheme_v2_20261007.py',A/'predict_lower_pool_after_quantile_HGB_scheme_v2_20261007.py',
      A/'predict_refined_quantile_HGB_scheme_v2_20261007.py',A/'quantile_HGB_large_batch_codec_20261007.py',
      A/'cached_official_spearman_runtime_20261007.py',A/'exact_cached_official_spearman_v2_20261007.py',
      A/'cached_official_spearman_full_scoring_benchmark_20261007/verification.json',A/'quantile_HGB_native_hook7_preflight_20261007/verification.json',
      ROOT/'后续选模标准.md',ROOT/'evaluate.py']
    for p in sources:
        if p.suffix=='.py':compile(p.read_text(encoding='utf8'),str(p),'exec')
    pins={str(p):sha(p) for p in sources};launches={}
    for name,script,args in jobs:
        try:r=start_service(name,script,args,pins)
        except AssertionError:
            f=A/'service_owned_workflows_20261006'/name;r=read(f/'native_launch.json')
            assert not owned(r) and read(f/'service_execution.json')['status']=='passed',name
        assert r['actual_native_console_handle']==0 and not r['independent_launch_root_in_any_job'];launches[name]=r
    create(out,{'status':'actual_seven_hidden_local119_dependency_jobs_started','at_local':__import__('time').strftime('%Y-%m-%dT%H:%M:%S'),
      'input_sha256':pins,'launches':launches,'remote_tasks_dispatched':0,'scientific_workers_stopped':0,
      'new_native_fits':0,'actual119_scores_freeze_future_QA30_or_main_not_yet_claimed':True,'test_labels_read':False})
    print({'status':'started','actual_hidden_jobs':7},flush=True)
if __name__=='__main__':main()
