"""Launch the first actual Ridge comparison only when full admission has genuinely passed."""
from pathlib import Path
import sys,time
ROOT=Path(__file__).resolve().parents[1]; A=ROOT/'analysis'
sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned

def main():
    folder=A/'service_owned_workflows_20261006/nonflag_RFFRidge40_round122_source_admission_v1'
    while owned(read(folder/'native_launch.json')):time.sleep(10)
    assert read(folder/'service_execution.json')['status']=='passed'
    admission=A/'nonflag_RFFRidge40_round122_source_admission_v1_20261007.json'; proof=read(admission)
    assert proof['status']=='passed_actual37_controls_and24_prospective122_complete_source_schema_paths_and_graph_routes'
    assert proof['declared_prospective_sources']==24 and len(proof['baseline_gain_regressions'])==9 and len(proof['graph_metadata_controls'])==12
    pins={**proof['input_sha256'],str(admission):sha(admission),str(Path(__file__)):sha(__file__)}
    jobs=[('nonflag_RFFRidge40_full37_controls_main_publication_v1','publish_nonflag_RFFRidge40_evidence_v2_20261007.py',['controls']),
        ('nonflag_RFFRidge40_official_comparison_v1','run_nonflag_RFFRidge40_admitted_comparison_v2_20261007.py',[]),
        ('nonflag_RFFRidge40_scores_main_publication_v1','publish_nonflag_RFFRidge40_evidence_v2_20261007.py',['scores']),
        ('nonflag_RFFRidge40_selected_candidate_preparation_v1','prepare_nonflag_RFFRidge40_selected_candidate_v1_20261007.py',[]),
        ('nonflag_RFFRidge40_selected_candidate_sealing_v1','seal_nonflag_RFFRidge40_selected_candidate_v1_20261007.py',[]),
        ('nonflag_RFFRidge40_round122_full_registration_v1','run_nonflag_RFFRidge40_round122_full_registration_v2_20261007.py',[])]
    pins.update({str(A/driver):sha(A/driver) for name,driver,args in jobs})
    for p,d in pins.items(): assert sha(p)==d,p
    from handoff_ready_goss_full_execution_20261006 import start_service
    launches={}
    for name,driver,args in jobs:launches[name]=start_service(name,driver,args,pins)
    create(A/'nonflag_RFFRidge40_complete_pipeline_actual_hidden_launches_v1_20261007.json',{
        'status':'started_actual6_Ridge_stages_after_genuine_complete121_source_admission','launches':launches,'input_sha256':pins,
        'new_quality_scores_by_launcher':0,'test_labels_read':False})
    print({'status':'actual_full_source_admission_passed_and6_stages_started'},flush=True)
if __name__=='__main__':main()
