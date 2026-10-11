"""Execute fine52 only after the actual complete127 main closure and real49/147 controls."""
from pathlib import Path
from datetime import datetime
import sys,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start

def closed(name):
    folder=A/'service_owned_workflows_20261006'/name
    while not (folder/'native_launch.json').exists() or owned(read(folder/'native_launch.json')):
        assert time.time()<datetime.fromisoformat('2026-10-07T23:00:00+08:00').timestamp(),'defer fine52 rather than miss fixed stop'
        time.sleep(10)
    assert read(folder/'service_execution.json')['status']=='passed',name

def main():
    closed('nonflag_RFF128Hi76_round127_full_registration_v1')
    closed('nonflag_residual_RidgeFine49_transform_preflight')
    preparation=A/'nonflag_RidgeFine52_science_route_preparation_v3_20261007.json'
    pins={**read(preparation)['input_sha256'],str(preparation):sha(preparation),str(Path(__file__)):sha(Path(__file__))}
    prospective=read(A/'nonflag_RidgeFine52_prospective_routes_v2_20261007.json')
    assert not prospective['issues'] and len(prospective['graph_controls'])==12
    for p,d in pins.items():assert sha(p)==d,p
    admission_name='nonflag_RidgeFine52_round128_source_admission_v1'
    row=start(admission_name,'verify_nonflag_RidgeFine52_round128_sources_v1_20261007.py',[],pins)
    create(A/'nonflag_RidgeFine52_actual_admission_hidden_launch_20261007.json',{
        'status':'started_actual128_admission_after_complete127_main_and49_full_controls',
        'identity':row,'input_sha256':pins,'new_native_fits':0,'new_quality_scores':0,'test_labels_read':False})
    closed(admission_name)
    admission=A/'nonflag_RidgeFine52_round128_source_admission_v1_20261007.json';proof=read(admission)
    assert len(proof['baseline_gain_regressions'])==9 and len(proof['graph_metadata_controls'])==12
    pins.update({**proof['input_sha256'],str(admission):sha(admission)})
    jobs=[('nonflag_RidgeFine52_full37_controls_main_publication_v1','publish_nonflag_RidgeFine52_evidence_v1_20261007.py',['controls']),
          ('nonflag_RidgeFine52_official_comparison_v1','run_nonflag_RidgeFine52_admitted_comparison_v1_20261007.py',[]),
          ('nonflag_RidgeFine52_scores_main_publication_v1','publish_nonflag_RidgeFine52_evidence_v1_20261007.py',['scores']),
          ('nonflag_RidgeFine52_selected_candidate_preparation_v1','prepare_nonflag_RidgeFine52_selected_candidate_v1_20261007.py',[]),
          ('nonflag_RidgeFine52_selected_candidate_sealing_v1','seal_nonflag_RidgeFine52_selected_candidate_v1_20261007.py',[]),
          ('nonflag_RidgeFine52_round128_full_registration_v1','run_nonflag_RidgeFine52_round128_full_registration_v1_20261007.py',[])]
    assert all(not (A/'service_owned_workflows_20261006'/name).exists() for name,_,_ in jobs)
    for p,d in pins.items():assert sha(p)==d,p
    launches={name:start(name,driver,args,pins) for name,driver,args in jobs}
    create(A/'nonflag_RidgeFine52_actual6_complete_pipeline_launches_20261007.json',{
      'status':'started_actual6_fine52_complete128_stages_after_source_admission','launches':launches,
      'input_sha256':pins,'new_native_fits_by_dispatch':0,'new_quality_scores_by_dispatch':0,'test_labels_read':False})

if __name__=='__main__':main()
