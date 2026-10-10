"""Admit micro40 only after actual130 closes, with enough time before tonight's stop."""
from pathlib import Path
from datetime import datetime
import sys,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start

def closed(name):
    folder=A/'service_owned_workflows_20261006'/name
    while not (folder/'native_launch.json').exists() or owned(read(folder/'native_launch.json')):
        assert time.time()<datetime.fromisoformat('2026-10-07T23:05:00+08:00').timestamp(),'new micro40 scoring deferred to preserve shutdown deadline'
        time.sleep(10)
    assert read(folder/'service_execution.json')['status']=='passed',name

def main():
    closed('nonflag_EmpiricalBayes40_round130_full_registration_v1')
    closed('nonflag_residual_RidgeMicro37_transform_preflight')
    preparation=A/'nonflag_RidgeMicro40_science_route_preparation_v1_20261007.json';prospective=A/'nonflag_RidgeMicro40_prospective_routes_v2_20261007.json'
    assert not read(prospective)['issues'] and len(read(prospective)['graph_controls'])==12
    pins={**read(preparation)['input_sha256'],**read(prospective)['input_sha256'],**{str(p):sha(p) for p in [Path(__file__),preparation,prospective]}}
    for p,d in pins.items():assert sha(p)==d,p
    name='nonflag_RidgeMicro40_round131_source_admission_v1'
    row=start(name,'verify_nonflag_RidgeMicro40_round131_sources_v1_20261007.py',[],pins)
    create(A/'nonflag_RidgeMicro40_actual_admission_hidden_launch_v1_20261007.json',{'status':'started_actual131_admission_after130_main_and_micro37_controls','identity':row,'input_sha256':pins,'new_quality_scores':0})
    closed(name)
    admission=A/'nonflag_RidgeMicro40_round131_source_admission_v1_20261007.json';proof=read(admission)
    assert len(proof['baseline_gain_regressions'])==9 and len(proof['graph_metadata_controls'])==12
    pins.update({**proof['input_sha256'],str(admission):sha(admission)})
    jobs=[('nonflag_RidgeMicro40_full37_controls_main_publication_v1','publish_nonflag_RidgeMicro40_evidence_v1_20261007.py',['controls']),
      ('nonflag_RidgeMicro40_official_comparison_v1','run_nonflag_RidgeMicro40_admitted_comparison_v1_20261007.py',[]),
      ('nonflag_RidgeMicro40_scores_main_publication_v1','publish_nonflag_RidgeMicro40_evidence_v1_20261007.py',['scores']),
      ('nonflag_RidgeMicro40_selected_candidate_preparation_v1','prepare_nonflag_RidgeMicro40_selected_candidate_v1_20261007.py',[]),
      ('nonflag_RidgeMicro40_selected_candidate_sealing_v1','seal_nonflag_RidgeMicro40_selected_candidate_v1_20261007.py',[]),
      ('nonflag_RidgeMicro40_round131_full_registration_v1','run_nonflag_RidgeMicro40_round131_full_registration_v1_20261007.py',[])]
    assert all(not (A/'service_owned_workflows_20261006'/name).exists() for name,_,_ in jobs)
    for p,d in pins.items():assert sha(p)==d,p
    launches={name:start(name,driver,args,pins) for name,driver,args in jobs}
    create(A/'nonflag_RidgeMicro40_actual6_complete_pipeline_launches_v1_20261007.json',{
      'status':'started_actual6_micro40_complete131_stages_after_actual_source_admission','launches':launches,'input_sha256':pins,'new_native_fits':0,'new_quality_scores_by_dispatch':0})

if __name__=='__main__':main()
