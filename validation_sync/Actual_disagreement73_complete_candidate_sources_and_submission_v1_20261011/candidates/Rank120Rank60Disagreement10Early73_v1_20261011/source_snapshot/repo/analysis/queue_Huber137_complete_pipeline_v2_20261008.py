"""Reuse the live exact-parent control worker and queue all seven complete137 stages after preflight."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start


def main():
    prospective=A/'Huber52_prospective_routes_v2_20261008.json';proof=read(prospective)
    assert proof['status']=='passed_actual24_prospective137_sources_schema_complete_graphs_baselines_status_paths_model_counts_and_cross_volume_bytes'
    for path,digest in proof['input_sha256'].items():assert sha(path)==digest,path
    existing_name='HuberIRLS64_49_current_parent_controls_v3_20261008';folder=A/'service_owned_workflows_20261006'/existing_name
    existing=read(folder/'native_launch.json')
    assert existing['actual_native_console_handle']==0
    assert owned(existing) or read(folder/'service_execution.json')['status']=='passed'
    jobs=[('Huber52_round137_source_admission_v2_20261008','verify_Huber52_round137_sources_v2_20261008.py',[]),
        ('Huber52_controls_main_publication_v2_20261008','publish_Huber52_evidence_v2_20261008.py',['controls']),
        ('Huber52_official_comparison_v2_20261008','run_Huber52_official_comparison_v2_20261008.py',[]),
        ('Huber52_scores_main_publication_v2_20261008','publish_Huber52_evidence_v2_20261008.py',['scores']),
        ('Huber52_selected_candidate_preparation_v2_20261008','prepare_Huber52_selected_candidate_v2_20261008.py',[]),
        ('Huber52_selected_candidate_sealing_v2_20261008','seal_Huber52_selected_candidate_v2_20261008.py',[]),
        ('Huber52_round137_full_registration_v2_20261008','run_Huber52_round137_full_registration_v2_20261008.py',[])]
    sources=[Path(__file__),prospective,A/'prepare_Huber52_round137_sources_v2_20261008.py',A/'Huber137_receiver_preparation_v2_20261008.json',
        folder/'native_launch.json',*[A/driver for _,driver,_ in jobs]]
    pins={**proof['input_sha256'],**{str(path):sha(path) for path in sources}}
    create(A/'Huber137_complete_dependency_plan_v2_20261008.json',{'status':'frozen_complete137_pipeline_before_quality','input_sha256':pins,
        'jobs':jobs,'reused_existing_current_parent_worker':existing,'complete136_QA47_main_and_current_parent_controls_required':True,
        'new_fits_by_dispatch':0,'new_quality_scores_by_dispatch':0,'test_labels_read':False})
    launches={existing_name:existing}
    for name,driver,args in jobs:
        for path,digest in pins.items():assert sha(path)==digest,path
        launches[name]=start(name,driver,args,pins)
    create(A/'Huber137_complete_hidden_launches_v2_20261008.json',{'status':'started_reused_parent_then_complete137_lazy_controls_main52_scores_candidate_QA48_main',
        'launches':launches,'input_sha256':pins,'new_service_count':7,'reused_service_count':1,
        'new_fits_by_dispatch':0,'new_quality_scores_by_dispatch':0,'actual_future_X_not_read_by_dispatch':True,'test_labels_read':False})


if __name__=='__main__':main()
