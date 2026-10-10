"""Queue real129 source admission and complete76 stages after128main and native10/6/73/219."""
from pathlib import Path
from datetime import datetime
import sys,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start

def closed(name):
    folder=A/'service_owned_workflows_20261006'/name
    while not (folder/'native_launch.json').exists() or owned(read(folder/'native_launch.json')):
        assert time.time()<datetime.fromisoformat('2026-10-07T22:55:00+08:00').timestamp(),'new76 round deferred to respect2355 stop'
        time.sleep(10)
    assert read(folder/'service_execution.json')['status']=='passed',name

def main():
    closed('nonflag_RidgeFine52_round128_full_registration_v1')
    closed('nonflag_residual_RFF128StreamMid_native_bank10')
    closed('nonflag_RFF128StreamMid_actual_hook6_and_full73_controls')
    from verify_nonflag_RFF128StreamMid76_prospective_routes_v3_20261007 import main as prospective
    prospective()
    prospective_path=A/'nonflag_RFF128StreamMid76_prospective_routes_v3_20261007.json';prospect=read(prospective_path)
    assert prospect['status']=='passed_actual24_prospective_sources_and24_graph_controls' and not prospect['issues']
    preparation=A/'nonflag_RFF128StreamMid76_science_route_preparation_v1_20261007.json'
    pins={**read(preparation)['input_sha256'],**prospect['input_sha256'],str(Path(__file__)):sha(Path(__file__)),
      str(preparation):sha(preparation),str(prospective_path):sha(prospective_path)}
    for p,d in pins.items():assert sha(p)==d,p
    name='nonflag_RFF128StreamMid76_round129_source_admission_v1'
    row=start(name,'verify_nonflag_RFF128StreamMid76_round129_sources_v1_20261007.py',[],pins)
    create(A/'nonflag_RFF128StreamMid76_actual_admission_hidden_launch_20261007.json',{
      'status':'started_actual129_admission_after10_fits6_hooks73_full219_cold_and128main',
      'identity':row,'input_sha256':pins,'new_quality_scores':0,'test_labels_read':False})
    closed(name)
    path=A/'nonflag_RFF128StreamMid76_round129_source_admission_v1_20261007.json';proof=read(path)
    assert len(proof['baseline_gain_regressions'])==9 and len(proof['graph_metadata_controls'])==24
    pins.update({**proof['input_sha256'],str(path):sha(path)})
    jobs=[('nonflag_RFF128StreamMid76_full37_controls_main_publication_v1','publish_nonflag_RFF128StreamMid76_evidence_v1_20261007.py',['controls']),
      ('nonflag_RFF128StreamMid76_official_comparison_v1','run_nonflag_RFF128StreamMid76_admitted_comparison_v1_20261007.py',[]),
      ('nonflag_RFF128StreamMid76_scores_main_publication_v1','publish_nonflag_RFF128StreamMid76_evidence_v1_20261007.py',['scores']),
      ('nonflag_RFF128StreamMid76_selected_candidate_preparation_v1','prepare_nonflag_RFF128StreamMid76_selected_candidate_v1_20261007.py',[]),
      ('nonflag_RFF128StreamMid76_selected_candidate_sealing_v1','seal_nonflag_RFF128StreamMid76_selected_candidate_v1_20261007.py',[]),
      ('nonflag_RFF128StreamMid76_round129_full_registration_v1','run_nonflag_RFF128StreamMid76_round129_full_registration_v1_20261007.py',[])]
    assert all(not (A/'service_owned_workflows_20261006'/name).exists() for name,_,_ in jobs)
    for p,d in pins.items():assert sha(p)==d,p
    launches={name:start(name,driver,args,pins) for name,driver,args in jobs}
    create(A/'nonflag_RFF128StreamMid76_actual6_complete_pipeline_launches_20261007.json',{
      'status':'started_actual6_complete129_stages_after_source_admission_and_actual128_main',
      'launches':launches,'input_sha256':pins,'new_quality_scores_by_dispatch':0,'test_labels_read':False})

if __name__=='__main__':main()
