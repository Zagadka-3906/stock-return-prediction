"""Replace only seven verified idle119 waiters; no scientific fit, score or inference is interrupted."""
from pathlib import Path
import sys,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis'
sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from handoff_ready_goss_full_execution_20261006 import start_service
from handoff_joint_goss_round97_full_execution_20261006 import suspended_idle
def main():
    out=A/'quantile_HGB88_actual_idle_waiter_handoff_v3_20261007';assert not out.exists();out.mkdir()
    assert not (A/'quantile_HGB88_official_comparison_20261007').exists()
    assert not list((A/'quantile_HGB88_selected_release_20261007').glob('*'))
    assert not (A/'quantile_HGB88_round119_source_admission_20261007.json').exists()
    jobs=[
      ('quantile_HGB88_round119_source_admission','verify_quantile_HGB88_round119_sources_v3_20261007.py',[], '    closed (verify_quantile_HGB88_round119_sources_v2_20261007.py:14)'),
      ('quantile_HGB88_full85_controls_main_publication','publish_quantile_HGB88_evidence_v3_20261007.py',['controls'],'    closed (publish_quantile_HGB88_evidence_v2_20261007.py:16)'),
      ('quantile_HGB88_official_comparison','run_quantile_HGB88_admitted_comparison_v3_20261007.py',[],'    main (run_quantile_HGB88_admitted_comparison_20261007.py:10)'),
      ('quantile_HGB88_scores_main_publication','publish_quantile_HGB88_evidence_v3_20261007.py',['scores'],'    closed (publish_quantile_HGB88_evidence_v2_20261007.py:16)'),
      ('quantile_HGB88_selected_candidate_preparation','prepare_quantile_HGB88_selected_candidate_v3_20261007.py',[],'    closed (prepare_quantile_HGB88_selected_candidate_20261007.py:22)'),
      ('quantile_HGB88_selected_candidate_sealing','seal_quantile_HGB88_selected_candidate_v3_20261007.py',[],'    main (seal_quantile_HGB88_selected_candidate_20261007.py:13)'),
      ('quantile_HGB88_round119_full_registration','run_quantile_HGB88_round119_full_registration_v3_20261007.py',[],'    main (run_quantile_HGB88_round119_full_registration_v2_20261007.py:20)')]
    preserved={n:read(A/'service_owned_workflows_20261006'/n/'native_launch.json') for n in ('neural16384_annual','dependency_queue_v12_local_cache','flagged_HGB_weighted_quarters340_official_comparison')}
    assert all(owned(r) for r in preserved.values())
    files=[Path(__file__),*[A/s for n,s,args,line in jobs],A/'run_quantile_HGB88_official_comparison_v3_20261007.py',
      A/'prepare_quantile_HGB88_round119_sources_v3_20261007.py',A/'quantile_HGB88_routes_source_preparation_v3_20261007.json',
      A/'quantile_HGB88_plan_20261007.json',A/'predict_refined_quantile_HGB_scheme_v2_20261007.py']
    pins={str(p):sha(p) for p in files};create(out/'frozen_before_handoff.json',{'input_sha256':pins,'preserved_scientific_identities':preserved,'zero_original119_actual_official_scores_and_inferences':True})
    held=[];launches={};retired=set()
    try:
        for name,script,args,line in jobs:
            folder=A/'service_owned_workflows_20261006'/name;identity=read(folder/'native_launch.json')
            parent,worker,idle=suspended_idle(identity,line);held.append((name,parent,worker,identity))
            create(out/(name+'_actual_idle_before_and_after.json'),idle)
        assert all(owned(r) for r in preserved.values())
        for name,script,args,line in jobs:
            new=name+'_v3';r=start_service(new,script,args,pins)
            assert r['actual_native_console_handle']==0 and not r['independent_launch_root_in_any_job'];launches[new]=r
        for name,parent,worker,identity in held:
            assert not worker.children();worker.terminate();worker.wait(timeout=15);parent.terminate();parent.wait(timeout=15);retired.add(name)
            create(A/'service_owned_workflows_20261006'/name/'administrative_supersession_before_any119_science_v3_20261007.json',{
              'status':'administratively_retired_exact_idle_waiter_no_scientific_completion_claim','identity':identity,'successor':launches[name+'_v3'],
              'actual119_native_fits_scores_future_inferences_interrupted':0,'at_local':time.strftime('%Y-%m-%dT%H:%M:%S')})
        assert all(owned(r) for r in preserved.values()) and all(owned(r) for r in launches.values())
        create(A/'quantile_HGB88_complete_pipeline_actual_hidden_launches_v3_20261007.json',{'status':'actual_seven_hidden_corrected119_jobs_started',
          'input_sha256':pins,'launches':launches,'preserved_scientific_identities':preserved,'remote_tasks_dispatched':0,'scientific_workers_stopped':0})
        create(out/'verification.json',{'status':'passed_actual7_exact_idle_waiters_replaced_before_any119_scientific_execution',
          'input_sha256':pins,'launches':launches,'actual_retired_idle_waiters':sorted(retired),'preserved_scientific_identities':preserved,
          'old_original_sources_and_waiter_records_retained':True,'scientific_workers_stopped':0,'new_native_fits':0,'new_quality_scores':0,'test_labels_read':False})
        print({'status':'passed','idle_waiters_replaced':7,'scientific_workers_interrupted':0},flush=True)
    finally:
        for name,parent,worker,identity in held:
            if name not in retired:
                for p in (parent,worker):
                    if p.is_running():p.resume()
if __name__=='__main__':main()
