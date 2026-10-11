"""Dispatch current-parent controls and the seven complete136 services without duplicate fitting."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start


def main():
    prospective=A/'CrossFamily94_prospective_routes_v2_20261008.json';proof=read(prospective)
    assert proof['status']=='passed_actual24_prospective136_sources_schema_graphs_baselines_status_paths_model_counts_and_cross_volume_bytes'
    for path,digest in proof['input_sha256'].items():assert sha(path)==digest,path
    jobs=[('CrossFamily91_current_parent_controls_v1_20261008','verify_CrossFamily91_current_parent_v1_20261008.py',[]),
        ('CrossFamily94_round136_source_admission_v2_20261008','verify_CrossFamily94_round136_sources_v2_20261008.py',[]),
        ('CrossFamily94_controls_main_publication_v2_20261008','publish_CrossFamily94_evidence_v2_20261008.py',['controls']),
        ('CrossFamily94_official_comparison_v2_20261008','run_CrossFamily94_official_comparison_v2_20261008.py',[]),
        ('CrossFamily94_scores_main_publication_v2_20261008','publish_CrossFamily94_evidence_v2_20261008.py',['scores']),
        ('CrossFamily94_selected_candidate_preparation_v2_20261008','prepare_CrossFamily94_selected_candidate_v2_20261008.py',[]),
        ('CrossFamily94_selected_candidate_sealing_v2_20261008','seal_CrossFamily94_selected_candidate_v2_20261008.py',[]),
        ('CrossFamily94_round136_full_registration_v2_20261008','run_CrossFamily94_round136_full_registration_v2_20261008.py',[])]
    sources=[Path(__file__),prospective,A/'prepare_CrossFamily94_round136_sources_v2_20261008.py',A/'CrossFamily136_receiver_preparation_v2_20261008.json',*[A/driver for _,driver,_ in jobs]]
    pins={**proof['input_sha256'],**{str(path):sha(path) for path in sources}}
    create(A/'CrossFamily136_complete_dependency_plan_v2_20261008.json',{'status':'frozen_complete136_pipeline_before_quality','input_sha256':pins,
        'jobs':jobs,'actual_complete135_QA_main_and_current_parent_controls_required_before_first136_score':True,'new_fits_by_dispatch':0,'new_quality_scores_by_dispatch':0,'test_labels_read':False})
    launches={}
    for name,driver,args in jobs:
        for path,digest in pins.items():assert sha(path)==digest,path
        launches[name]=start(name,driver,args,pins)
    create(A/'CrossFamily136_complete_hidden_launches_v2_20261008.json',{'status':'started_current_parent_then_complete136_lazy_controls_main94_scores_candidate_QA47_main',
        'launches':launches,'input_sha256':pins,'new_fits_by_dispatch':0,'new_quality_scores_by_dispatch':0,'actual_future_X_not_read_by_dispatch':True,'test_labels_read':False})
    print('Complete136 eight-service chain dispatched; current135 scientific workers are unchanged.',flush=True)


if __name__=='__main__':main()
