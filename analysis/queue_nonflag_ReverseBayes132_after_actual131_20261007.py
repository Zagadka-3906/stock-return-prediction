"""Dispatch signed132 only after real131 main closure and enough time before fixed stop."""
from pathlib import Path
from datetime import datetime
import sys,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start
CUTOFF=datetime.fromisoformat('2026-10-07T23:12:00+08:00').timestamp()

def closed_before_dispatch_cutoff(name):
    folder=A/'service_owned_workflows_20261006'/name
    while not (folder/'native_launch.json').exists() or owned(read(folder/'native_launch.json')):
        if time.time()>=CUTOFF:return False
        time.sleep(10)
    assert read(folder/'service_execution.json')['status']=='passed',name
    return time.time()<CUTOFF

def main():
    if not closed_before_dispatch_cutoff('nonflag_RidgeMicro40_round131_full_registration_v1'):
        create(A/'nonflag_ReverseBayes40_round132_dispatch_deferred_until_manual_continue_20261007.json',{
          'status':'not_dispatched_to_preserve2355_stop_and2345_publication_quiesce','at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),
          'actual_negative_native3_full37_cold111_controls_passed':True,'official_scores_added':0,'automatic_morning_restart_enabled':False,
          'requires_actual_user_continue_for_later_new_dispatch':True,'full132_qualification_not_claimed':True})
        return
    assert closed_before_dispatch_cutoff('nonflag_ReverseBayes40_actual_native3_full37_controls')
    preparation=A/'nonflag_ReverseBayes40_science_route_preparation_v1_20261007.json';prospective=A/'nonflag_ReverseBayes40_prospective_routes_v1_20261007.json'
    assert not read(prospective)['issues'] and len(read(prospective)['graph_controls'])==12
    pins={**read(preparation)['input_sha256'],**read(prospective)['input_sha256'],**{str(p):sha(p) for p in [Path(__file__),preparation,prospective]}}
    for p,d in pins.items():assert sha(p)==d,p
    name='nonflag_ReverseBayes40_round132_source_admission_v1'
    row=start(name,'verify_nonflag_ReverseBayes40_round132_sources_v1_20261007.py',[],pins)
    create(A/'nonflag_ReverseBayes40_actual_admission_hidden_launch_20261007.json',{'status':'started_actual_signed132_admission_after131_main_and_native3_full37_cold111','identity':row,'input_sha256':pins,'new_quality_scores':0})
    folder=A/'service_owned_workflows_20261006'/name
    while owned(read(folder/'native_launch.json')):time.sleep(5)
    assert read(folder/'service_execution.json')['status']=='passed'
    admission=A/'nonflag_ReverseBayes40_round132_source_admission_v1_20261007.json';proof=read(admission)
    assert len(proof['baseline_gain_regressions'])==9 and len(proof['graph_metadata_controls'])==12
    pins.update({**proof['input_sha256'],str(admission):sha(admission)})
    assert time.time()<CUTOFF,'late dispatch cannot use elapsed waiting as permission'
    jobs=[('nonflag_ReverseBayes40_full37_controls_main_publication_v1','publish_nonflag_ReverseBayes40_evidence_v1_20261007.py',['controls']),
      ('nonflag_ReverseBayes40_official_comparison_v1','run_nonflag_ReverseBayes40_admitted_comparison_v1_20261007.py',[]),
      ('nonflag_ReverseBayes40_scores_main_publication_v1','publish_nonflag_ReverseBayes40_evidence_v1_20261007.py',['scores']),
      ('nonflag_ReverseBayes40_selected_candidate_preparation_v1','prepare_nonflag_ReverseBayes40_selected_candidate_v1_20261007.py',[]),
      ('nonflag_ReverseBayes40_selected_candidate_sealing_v1','seal_nonflag_ReverseBayes40_selected_candidate_v1_20261007.py',[]),
      ('nonflag_ReverseBayes40_round132_full_registration_v1','run_nonflag_ReverseBayes40_round132_full_registration_v1_20261007.py',[])]
    assert all(not (A/'service_owned_workflows_20261006'/n).exists() for n,_,_ in jobs)
    launches={n:start(n,d,args,pins) for n,d,args in jobs}
    create(A/'nonflag_ReverseBayes40_actual6_complete132_pipeline_launches_20261007.json',{
      'status':'started_actual6_negative40_complete132_stages_before2312_dispatch_cutoff','launches':launches,'input_sha256':pins,
      'new_native_fits':0,'new_quality_scores_by_dispatch':0,'test_labels_read':False})

if __name__=='__main__':main()
