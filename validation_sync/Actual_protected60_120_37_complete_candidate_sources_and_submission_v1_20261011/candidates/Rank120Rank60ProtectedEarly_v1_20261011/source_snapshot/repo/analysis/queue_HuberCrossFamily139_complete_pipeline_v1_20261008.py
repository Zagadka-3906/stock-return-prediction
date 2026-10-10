"""Start eight lazy139 workers; all prior scientific jobs keep their original ownership."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start


def main():
    prospective=A/'HuberCrossFamily112_prospective_routes_v1_20261008.json';proof=read(prospective)
    assert proof['status']=='passed_actual24_prospective139_sources_schema_graphs_baselines_status_paths_model_counts_and_cross_volume_bytes'
    for path,digest in proof['input_sha256'].items():assert sha(path)==digest,path
    jobs=[('HuberCrossFamily109_current_parent_controls_v1_20261008','verify_HuberCrossFamily109_current_parent_v1_20261008.py',[]),
        ('HuberCrossFamily112_round139_source_admission_v1_20261008','verify_HuberCrossFamily112_round139_sources_v1_20261008.py',[]),
        ('HuberCrossFamily112_controls_main_publication_v1_20261008','publish_HuberCrossFamily112_evidence_v1_20261008.py',['controls']),
        ('HuberCrossFamily112_official_comparison_v1_20261008','run_HuberCrossFamily112_official_comparison_v1_20261008.py',[]),
        ('HuberCrossFamily112_scores_main_publication_v1_20261008','publish_HuberCrossFamily112_evidence_v1_20261008.py',['scores']),
        ('HuberCrossFamily112_selected_candidate_preparation_v1_20261008','prepare_HuberCrossFamily112_selected_candidate_v1_20261008.py',[]),
        ('HuberCrossFamily112_selected_candidate_sealing_v1_20261008','seal_HuberCrossFamily112_selected_candidate_v1_20261008.py',[]),
        ('HuberCrossFamily112_round139_full_registration_v1_20261008','run_HuberCrossFamily112_round139_full_registration_v1_20261008.py',[])]
    sources=[Path(__file__),prospective,A/'prepare_HuberCrossFamily112_round139_sources_v1_20261008.py',
        A/'HuberCrossFamily139_receiver_preparation_v1_20261008.json',*[A/driver for _,driver,_ in jobs]]
    pins={**proof['input_sha256'],**{str(p):sha(p) for p in sources}}
    create(A/'HuberCrossFamily139_complete_dependency_plan_v1_20261008.json',{
        'status':'frozen_complete139_pipeline_before_quality','input_sha256':pins,'jobs':jobs,
        'complete138_QA49_main_and_exact_current_parent_required_before139_score':True,'new_fits_by_dispatch':0,'new_quality_scores_by_dispatch':0,'test_labels_read':False})
    launches={}
    for name,driver,args in jobs:
        assert not (A/'service_owned_workflows_20261006'/name).exists()
        launches[name]=start(name,driver,args,pins)
    create(A/'HuberCrossFamily139_complete_hidden_launches_v1_20261008.json',{
        'status':'started_eight_lazy139_services_for_controls_main112_scores_frozen_candidate_QA50_main',
        'launches':launches,'input_sha256':pins,'new_fits_by_dispatch':0,'new_quality_scores_by_dispatch':0,
        'actual_future_X_not_read_by_dispatch':True,'test_labels_read':False})
    print('Eight consoleless139 workers started; no GPU refit or scientific worker restart.',flush=True)


if __name__=='__main__':main()
