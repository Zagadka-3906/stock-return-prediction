"""Launch actual source admission and six hidden complete127 stages after fixed controls."""
from pathlib import Path
import sys,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start

def main():
    preparation=A/'nonflag_RFF128Hi76_science_route_preparation_v2_20261007.json'
    proof=read(preparation)
    prospective=A/'nonflag_RFF128Hi76_prospective_routes_v2_20261007.json'
    assert not read(prospective)['issues']
    pins={**proof['input_sha256'],str(preparation):sha(preparation),str(Path(__file__)):sha(Path(__file__))}
    for p,d in pins.items():assert sha(p)==d,p
    name='nonflag_RFF128Hi76_round127_source_admission_v1'
    row=start(name,'verify_nonflag_RFF128Hi76_round127_sources_v1_20261007.py',[],pins)
    create(A/'nonflag_RFF128Hi76_actual_admission_hidden_launch_20261007.json',{
        'status':'started_actual127_source_admission_after_native10_hooks6_full73_cold219',
        'identity':row,'input_sha256':pins,'new_quality_scores':0,'test_labels_read':False})
    while owned(row):time.sleep(2)
    assert read(A/'service_owned_workflows_20261006'/name/'service_execution.json')['status']=='passed'
    admission=A/'nonflag_RFF128Hi76_round127_source_admission_v1_20261007.json';admitted=read(admission)
    assert len(admitted['baseline_gain_regressions'])==9 and len(admitted['graph_metadata_controls'])==24
    jobs=[('nonflag_RFF128Hi76_full37_controls_main_publication_v1','publish_nonflag_RFF128Hi76_evidence_v1_20261007.py',['controls']),
          ('nonflag_RFF128Hi76_official_comparison_v1','run_nonflag_RFF128Hi76_admitted_comparison_v1_20261007.py',[]),
          ('nonflag_RFF128Hi76_scores_main_publication_v1','publish_nonflag_RFF128Hi76_evidence_v1_20261007.py',['scores']),
          ('nonflag_RFF128Hi76_selected_candidate_preparation_v1','prepare_nonflag_RFF128Hi76_selected_candidate_v1_20261007.py',[]),
          ('nonflag_RFF128Hi76_selected_candidate_sealing_v1','seal_nonflag_RFF128Hi76_selected_candidate_v1_20261007.py',[]),
          ('nonflag_RFF128Hi76_round127_full_registration_v1','run_nonflag_RFF128Hi76_round127_full_registration_v1_20261007.py',[])]
    assert all(not (A/'service_owned_workflows_20261006'/name).exists() for name,_,_ in jobs)
    pins.update({**admitted['input_sha256'],str(admission):sha(admission)})
    for p,d in pins.items():assert sha(p)==d,p
    launches={name:start(name,driver,args,pins) for name,driver,args in jobs}
    create(A/'nonflag_RFF128Hi76_complete_pipeline_actual_hidden_launches_20261007.json',{
        'status':'started_actual6_complete127_stages_after_real_source_admission',
        'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'launches':launches,'input_sha256':pins,
        'new_quality_scores_by_launcher':0,'test_labels_read':False})
    print({'status':'started_actual6_complete127_stages'},flush=True)

if __name__=='__main__':main()
