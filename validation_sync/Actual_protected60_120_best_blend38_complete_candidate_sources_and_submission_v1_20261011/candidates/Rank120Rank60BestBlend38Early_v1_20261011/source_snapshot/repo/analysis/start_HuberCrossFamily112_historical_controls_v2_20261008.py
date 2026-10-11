"""Start the already frozen scientific receivers after preserving a dispatcher variable-shadow failure."""
from pathlib import Path
import sys,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start as start_worker


def main():
    plan_path=A/'HuberCrossFamily112_round139_plan_v1_20261008.json';plan=read(plan_path)
    assert len(plan['new_cases'])==108 and plan['expected_scored_cases']==112
    for p,d in plan['input_sha256'].items():assert sha(p)==d,p
    paths=[Path(__file__),plan_path,A/'prepare_HuberCrossFamily112_plan_and_historical_controls_v1_20261008.py',
        A/'HuberCrossFamily_complete_parent_CDF_v1_20261008.py',A/'HuberCrossFamily_complete_parent_native_stage_v1_20261008.py',
        A/'verify_HuberCrossFamily109_parent134_historical_v1_20261008.py',A/'verify_HuberCrossFamily18_native_historical_hooks_v1_20261008.py']
    pins={str(p):sha(p) for p in paths}
    failure=A/'HuberCrossFamily112_initial_dispatch_failure_v1_20261008.json'
    create(failure,{'status':'preserved_before_any_model_fit_or_score','at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),
        'failed_source_sha256':sha(paths[2]),'reason':'Local start offset variable shadowed imported start function after preparation; no service launch occurred.',
        'prepared_plan_and_scientific_sources_unchanged':True,'new_native_fits':0,'new_official_scores':0,'test_labels_read':False})
    pins[str(failure)]=sha(failure);launches={}
    jobs=[('HuberCrossFamily109_parent134_historical_controls_v1_20261008',paths[5].name),
        ('HuberCrossFamily18_native_historical_hooks_v1_20261008',paths[6].name)]
    for name,driver in jobs:
        assert not (A/'service_owned_workflows_20261006'/name).exists()
        launches[name]=start_worker(name,driver,[],pins)
    create(A/'actual_HuberCrossFamily112_plan_and_historical_hidden_launches_v2_20261008.json',{
        'status':'started_actual109_full327_cold_then18_native18_cold_for_frozen112_cases',
        'input_sha256':pins,'launches':launches,'new_fits':0,'new_official_scores':0,
        'original_GPU_fitter_not_stopped_or_restarted':True,'complete139_source_admission_scoring_candidate_QA50_main_still_required':True,
        'test_labels_read':False})
    print('Frozen112 grid and unchanged scientific receivers dispatched; previous launcher failure retained.',flush=True)


if __name__=='__main__':main()
