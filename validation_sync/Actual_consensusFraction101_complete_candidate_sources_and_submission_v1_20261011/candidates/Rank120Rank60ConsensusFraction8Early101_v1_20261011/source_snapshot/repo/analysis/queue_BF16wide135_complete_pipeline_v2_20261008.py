"""Dispatch lightweight dependency waiters for the complete admitted135 workflow; no duplicate fitter."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start


def main():
    prospective=A/'BF16wide40_prospective_routes_v2_20261008.json';proof=read(prospective)
    assert proof['status']=='passed_actual24_prospective135_sources_schema_graphs_baselines_status_paths_and_cross_volume_bytes'
    for p,d in proof['input_sha256'].items():assert sha(p)==d,p
    train=A/'service_owned_workflows_20261006/actual_neural_BF16_micro8192_bank6_v2_20261008/native_launch.json'
    assert owned(read(train)) or read(train.parent/'service_execution.json')['status']=='passed'
    jobs=[('BF16wide40_round135_source_admission_v2_20261008','verify_BF16wide40_round135_sources_v2_20261008.py',[]),
        ('BF16wide40_controls_main_publication_v2_20261008','publish_BF16wide40_evidence_v2_20261008.py',['controls']),
        ('BF16wide40_official_comparison_v2_20261008','run_BF16wide40_official_comparison_v2_20261008.py',[]),
        ('BF16wide40_scores_main_publication_v2_20261008','publish_BF16wide40_evidence_v2_20261008.py',['scores']),
        ('BF16wide40_selected_candidate_preparation_v2_20261008','prepare_BF16wide40_selected_candidate_v2_20261008.py',[]),
        ('BF16wide40_selected_candidate_sealing_v2_20261008','seal_BF16wide40_selected_candidate_v2_20261008.py',[]),
        ('BF16wide40_round135_full_registration_v2_20261008','run_BF16wide40_round135_full_registration_v2_20261008.py',[])]
    sources=[Path(__file__),prospective,A/'prepare_BF16wide40_round135_sources_v2_20261008.py',
        A/'BF16wide135_receiver_preparation_v2_20261008.json',*[A/driver for _,driver,_ in jobs]]
    pins={**proof['input_sha256'],**{str(p):sha(p) for p in sources}}
    create(A/'BF16wide135_complete_dependency_plan_v2_20261008.json',{'status':'frozen_complete135_pipeline_before_quality',
        'input_sha256':pins,'jobs':jobs,'actual6_GPU37_111_3_controls_required_before_first_quality':True,
        'new_fits_by_dispatch':0,'new_quality_scores_by_dispatch':0,'test_labels_read':False})
    rows={}
    for name,driver,args in jobs:
        for p,d in pins.items():assert sha(p)==d,p
        rows[name]=start(name,driver,args,pins)
    create(A/'BF16wide135_complete_hidden_launches_v2_20261008.json',{'status':'started_complete135_ordered_lazy_admission_controls_main_scores_candidate_QA46_main_pipeline',
        'launches':rows,'input_sha256':pins,'new_fits_by_dispatch':0,'new_quality_scores_by_dispatch':0,
        'actual_future_X_not_read_by_dispatch':True,'test_labels_read':False})
    print('Complete135 pipeline dispatched as consoleless lazy waiters after actual6/5GPU/37/111/3 controls.',flush=True)


if __name__=='__main__':main()
