"""Dispatch the frozen2 scientific receivers with accurate140 queue metadata."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start

def main():
    prospective=A/'SpectralGram52_prospective_routes_v2_20261008.json';proof=read(prospective)
    assert proof['actual_prospective_sources']==24 and proof['actual_graph_controls']==882
    for path,digest in proof['input_sha256'].items():assert sha(path)==digest,path
    retirement=A/'SpectralGram140_exact_idle_metadata_supersession_v1_20261008.json'
    assert read(retirement)['status']=='passed_exact_eight_idle140_receivers_superseded_before_quality'
    for row in read(A/'SpectralGram140_complete_hidden_launches_v1_20261008.json')['launches'].values():assert not owned(row)
    jobs=[('SpectralGram49_current_parent_controls_v2_20261008','verify_SpectralGram49_current_parent_v2_20261008.py',[]),
        ('SpectralGram52_round140_source_admission_v2_20261008','verify_SpectralGram52_round140_sources_v2_20261008.py',[]),
        ('SpectralGram52_controls_main_publication_v2_20261008','publish_SpectralGram52_evidence_v2_20261008.py',['controls']),
        ('SpectralGram52_official_comparison_v2_20261008','run_SpectralGram52_official_comparison_v2_20261008.py',[]),
        ('SpectralGram52_scores_main_publication_v2_20261008','publish_SpectralGram52_evidence_v2_20261008.py',['scores']),
        ('SpectralGram52_selected_candidate_preparation_v2_20261008','prepare_SpectralGram52_selected_candidate_v2_20261008.py',[]),
        ('SpectralGram52_selected_candidate_sealing_v2_20261008','seal_SpectralGram52_selected_candidate_v2_20261008.py',[]),
        ('SpectralGram52_round140_full_registration_v2_20261008','run_SpectralGram52_round140_full_registration_v2_20261008.py',[])]
    files=[Path(__file__),prospective,retirement,A/'SpectralGram140_receiver_preparation_v2_20261008.json',A/'prepare_SpectralGram52_round140_sources_v2_20261008.py',*[A/driver for _,driver,_ in jobs]]
    pins={**proof['input_sha256'],**{str(p):sha(p) for p in files}}
    create(A/'SpectralGram140_complete_dependency_plan_v3_20261008.json',{
        'status':'frozen_complete140_pipeline_before_quality','input_sha256':pins,'jobs':jobs,'round':140,'expected_official_cases':52,
        'complete139_QA50_main_and_exact_current_parent_required_before140_score':True,'scientific_receiver_version':2,
        'new_fits_by_dispatch':0,'new_quality_scores_by_dispatch':0,'test_labels_read':False})
    launches={}
    for name,driver,args in jobs:
        assert not (A/'service_owned_workflows_20261006'/name).exists()
        launches[name]=start(name,driver,args,pins)
    create(A/'SpectralGram140_complete_hidden_launches_v3_20261008.json',{
        'status':'started_eight_lazy140_services_for_controls_main52_scores_frozen_candidate_QA51_main',
        'launches':launches,'input_sha256':pins,'round':140,'expected_official_cases':52,'QA_version':51,'scientific_receiver_version':2,
        'new_fits_by_dispatch':0,'new_quality_scores_by_dispatch':0,'actual_future_X_not_read_by_dispatch':True,'test_labels_read':False})
    print('Eight consoleless140 frozen2 receivers started with accurate52-case metadata.',flush=True)

if __name__=='__main__':main()
