"""Run actual130 with recovered control gates after129main; retain every original failure."""
from pathlib import Path
from datetime import datetime
import sys,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start

def closed(name):
    folder=A/'service_owned_workflows_20261006'/name
    while not (folder/'native_launch.json').exists() or owned(read(folder/'native_launch.json')):
        assert time.time()<datetime.fromisoformat('2026-10-07T22:55:00+08:00').timestamp(),'new40 round deferred to respect fixed stop'
        time.sleep(10)
    assert read(folder/'service_execution.json')['status']=='passed',name

def main():
    closed('nonflag_RFF128StreamMid76_round129_full_registration_v1')
    closed('nonflag_residual_EmpiricalBayes37_transform_preflight_v2')
    preparation=A/'nonflag_EmpiricalBayes40_science_route_preparation_v1_20261007.json'
    recovery=A/'nonflag_EmpiricalBayes40_control_gate_recovery_v2_20261007.json'
    prospective=A/'nonflag_EmpiricalBayes40_prospective_routes_v3_20261007.json'
    assert not read(prospective)['issues'] and len(read(prospective)['graph_controls'])==12
    pins={**read(preparation)['input_sha256'],**read(recovery)['input_sha256'],**read(prospective)['input_sha256'],
      **{str(p):sha(p) for p in [Path(__file__),preparation,recovery,prospective]}}
    for p,d in pins.items():assert sha(p)==d,p
    name='nonflag_EmpiricalBayes40_round130_source_admission_v1'
    row=start(name,'verify_nonflag_EmpiricalBayes40_round130_sources_v2_20261007.py',[],pins)
    create(A/'nonflag_EmpiricalBayes40_actual_admission_hidden_launch_20261007.json',{
      'status':'started_actual130_admission_after_recovered3_37_111_controls_and129main',
      'identity':row,'input_sha256':pins,'new_quality_scores':0,'test_labels_read':False})
    closed(name)
    admission=A/'nonflag_EmpiricalBayes40_round130_source_admission_v1_20261007.json';proof=read(admission)
    assert len(proof['baseline_gain_regressions'])==9 and len(proof['graph_metadata_controls'])==12
    pins.update({**proof['input_sha256'],str(admission):sha(admission)})
    jobs=[('nonflag_EmpiricalBayes40_full37_controls_main_publication_v1','publish_nonflag_EmpiricalBayes40_evidence_v2_20261007.py',['controls']),
      ('nonflag_EmpiricalBayes40_official_comparison_v1','run_nonflag_EmpiricalBayes40_admitted_comparison_v2_20261007.py',[]),
      ('nonflag_EmpiricalBayes40_scores_main_publication_v1','publish_nonflag_EmpiricalBayes40_evidence_v2_20261007.py',['scores']),
      ('nonflag_EmpiricalBayes40_selected_candidate_preparation_v1','prepare_nonflag_EmpiricalBayes40_selected_candidate_v2_20261007.py',[]),
      ('nonflag_EmpiricalBayes40_selected_candidate_sealing_v1','seal_nonflag_EmpiricalBayes40_selected_candidate_v1_20261007.py',[]),
      ('nonflag_EmpiricalBayes40_round130_full_registration_v1','run_nonflag_EmpiricalBayes40_round130_full_registration_v1_20261007.py',[])]
    assert all(not (A/'service_owned_workflows_20261006'/name).exists() for name,_,_ in jobs)
    for p,d in pins.items():assert sha(p)==d,p
    launches={name:start(name,driver,args,pins) for name,driver,args in jobs}
    create(A/'nonflag_EmpiricalBayes40_actual6_complete_pipeline_launches_20261007.json',{
      'status':'started_actual6_empirical_Bayes40_complete130_stages_after_actual_source_admission',
      'launches':launches,'input_sha256':pins,'new_quality_scores_by_dispatch':0,'test_labels_read':False})

if __name__=='__main__':main()
