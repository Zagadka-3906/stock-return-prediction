"""Dispatch eight exact141 receivers after the complete prospective source/graph admission."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start

def main():
    prospective=A/'KrylovGram52_prospective_routes_v3_20261008.json';proof=read(prospective)
    assert proof['status']=='passed_actual24_prospective141_sources_schema_graphs_baselines_status_paths_model_counts_and_cross_volume_bytes'
    assert proof['actual_prospective_sources']==24 and proof['actual_graph_controls']==1029
    for path,digest in proof['input_sha256'].items():assert sha(path)==digest,path
    jobs=[('KrylovGram49_current_parent_controls_v3_20261008','verify_KrylovGram49_current_parent_v3_20261008.py',[]),
        ('KrylovGram52_round141_source_admission_v3_20261008','verify_KrylovGram52_round141_sources_v3_20261008.py',[]),
        ('KrylovGram52_controls_main_publication_v3_20261008','publish_KrylovGram52_evidence_v3_20261008.py',['controls']),
        ('KrylovGram52_official_comparison_v3_20261008','run_KrylovGram52_official_comparison_v3_20261008.py',[]),
        ('KrylovGram52_scores_main_publication_v3_20261008','publish_KrylovGram52_evidence_v3_20261008.py',['scores']),
        ('KrylovGram52_selected_candidate_preparation_v3_20261008','prepare_KrylovGram52_selected_candidate_v3_20261008.py',[]),
        ('KrylovGram52_selected_candidate_sealing_v3_20261008','seal_KrylovGram52_selected_candidate_v3_20261008.py',[]),
        ('KrylovGram52_round141_full_registration_v3_20261008','run_KrylovGram52_round141_full_registration_v3_20261008.py',[])]
    files=[Path(__file__),prospective,A/'prepare_KrylovGram52_round141_sources_v3_20261008.py',
        A/'KrylovGram141_receiver_preparation_v3_20261008.json',*[A/driver for _,driver,_ in jobs]]
    pins={**proof['input_sha256'],**{str(p):sha(p) for p in files}}
    create(A/'KrylovGram141_complete_dependency_plan_v3_20261008.json',{
        'status':'frozen_complete141_pipeline_before_quality','input_sha256':pins,'jobs':jobs,'expected_official_cases':52,'QA_version':52,
        'complete140_registration3_QA51_main_and_exact_current_parent_required_before141_score':True,
        'new_fits_by_dispatch':0,'new_quality_scores_by_dispatch':0,'test_labels_read':False})
    launches={}
    for name,driver,args in jobs:
        assert not (A/'service_owned_workflows_20261006'/name).exists();launches[name]=start(name,driver,args,pins)
    create(A/'KrylovGram141_complete_hidden_launches_v3_20261008.json',{
        'status':'started_eight_lazy141_services_for_controls_main52_scores_frozen_candidate_QA52_main',
        'launches':launches,'input_sha256':pins,'expected_official_cases':52,'QA_version':52,'new_fits_by_dispatch':0,
        'new_quality_scores_by_dispatch':0,'actual_future_X_not_read_by_dispatch':True,'test_labels_read':False})
    print('Eight consoleless141 science2 receivers started after24 sources and1029 full graph controls.',flush=True)

if __name__=='__main__':main()
