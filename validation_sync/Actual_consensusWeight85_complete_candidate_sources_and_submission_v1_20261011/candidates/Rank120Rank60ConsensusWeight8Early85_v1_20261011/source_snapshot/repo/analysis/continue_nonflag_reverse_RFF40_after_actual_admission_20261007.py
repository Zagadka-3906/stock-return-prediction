"""Launch six complete round123 stages only after the genuine actual source admission."""
from pathlib import Path
import sys,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from start_nonflag_reverse_RFF40_actual_admission_20261007 import start
def main():
    folder=A/'service_owned_workflows_20261006/nonflag_reverse_RFF40_round123_source_admission_v1'
    while owned(read(folder/'native_launch.json')):time.sleep(10)
    assert read(folder/'service_execution.json')['status']=='passed'
    admission=A/'nonflag_reverse_RFF40_round123_source_admission_v1_20261007.json';proof=read(admission)
    assert proof['status']=='passed_actual37_controls_and24_prospective123_complete_source_schema_paths_and_graph_routes'
    assert proof['declared_prospective_sources']==24 and len(proof['baseline_gain_regressions'])==9 and len(proof['graph_metadata_controls'])==12
    jobs=[('nonflag_reverse_RFF40_full37_controls_main_publication_v1','publish_nonflag_reverse_RFF40_evidence_v1_20261007.py',['controls']),
      ('nonflag_reverse_RFF40_official_comparison_v1','run_nonflag_reverse_RFF40_admitted_comparison_v1_20261007.py',[]),
      ('nonflag_reverse_RFF40_scores_main_publication_v1','publish_nonflag_reverse_RFF40_evidence_v1_20261007.py',['scores']),
      ('nonflag_reverse_RFF40_selected_candidate_preparation_v1','prepare_nonflag_reverse_RFF40_selected_candidate_v1_20261007.py',[]),
      ('nonflag_reverse_RFF40_selected_candidate_sealing_v1','seal_nonflag_reverse_RFF40_selected_candidate_v1_20261007.py',[]),
      ('nonflag_reverse_RFF40_round123_full_registration_v1','run_nonflag_reverse_RFF40_round123_full_registration_v1_20261007.py',[])]
    assert all(not (A/'service_owned_workflows_20261006'/name).exists() for name,_,_ in jobs)
    previous=read(A/'nonflag_reverse_RFF40_actual_admission_hidden_launch_20261007.json')['input_sha256']
    pins={**previous,**proof['input_sha256'],**{str(p):sha(p) for p in [Path(__file__),admission,*[A/d for _,d,_ in jobs]]}}
    for p,d in pins.items():assert sha(p)==d,p
    launches={name:start(name,driver,args,pins) for name,driver,args in jobs}
    create(A/'nonflag_reverse_RFF40_complete_pipeline_actual_hidden_launches_v1_20261007.json',
      {'status':'started_actual6_reverse_RFF_stages_after_genuine_complete123_source_admission',
       'launches':launches,'input_sha256':pins,'new_quality_scores_by_launcher':0,'test_labels_read':False})
    print({'status':'started6_actual_admitted_stages'},flush=True)
if __name__=='__main__':main()
