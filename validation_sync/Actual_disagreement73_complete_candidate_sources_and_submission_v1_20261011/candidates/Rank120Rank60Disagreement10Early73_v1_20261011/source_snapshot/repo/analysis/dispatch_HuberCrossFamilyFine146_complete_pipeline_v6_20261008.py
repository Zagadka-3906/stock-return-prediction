"""Dispatch only after all complete prospective source controls and the actual preceding141 round qualify."""
from pathlib import Path
import sys,time,json
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
def closed(name):
    folder=A/'service_owned_workflows_20261006'/name
    while not (folder/'native_launch.json').exists() or owned(read(folder/'native_launch.json')):time.sleep(10)
    assert read(folder/'service_execution.json')['status']=='passed',name
def main():
    closed('HuberCrossFamilyFine146_complete_prospective_controls_v3_20261008')
    p=A/'HuberCrossFamilyFine125_prospective_routes_v3_20261008.json';proof=read(p)
    for path,d in proof['input_sha256'].items():assert sha(path)==d,path
    closed('CrossFamilyFine125_round145_full_registration_v3_20261008')
    benchmark=A/'service_owned_workflows_20261006/actual_full_board_deferred_serialization_benchmark_v3_20261008'
    while not (benchmark/'service_execution.json').exists():time.sleep(15)
    while owned(read(benchmark/'native_launch.json')):time.sleep(1)
    terminal=read(benchmark/'service_execution.json');assert terminal['status'] in ('passed','failed')
    create(A/'HuberCrossFamilyFine146_execution_cost_slot_handoff_v4_20261008.json',{'status':'original146_runtime_retained_after_actual_benchmark_process_closure','actual_benchmark_terminal':terminal,'new_execution_runtime_not_adopted':True,'new_quality_scores':0})
    from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start
    specs=[('HuberCrossFamilyFine125_round146_source_admission_v2_20261008','verify_HuberCrossFamilyFine125_round146_sources_v5_20261008.py',[]),
        ('HuberCrossFamilyFine125_controls_main_publication_v2_20261008','publish_HuberCrossFamilyFine125_evidence_v5_20261008.py',['controls']),
        ('HuberCrossFamilyFine125_official_comparison_v2_20261008','run_HuberCrossFamilyFine125_official_comparison_v3_20261008.py',[]),
        ('HuberCrossFamilyFine125_scores_main_publication_v2_20261008','publish_HuberCrossFamilyFine125_evidence_v5_20261008.py',['scores']),
        ('HuberCrossFamilyFine125_selected_candidate_preparation_v2_20261008','prepare_HuberCrossFamilyFine125_selected_candidate_v2_20261008.py',[]),
        ('HuberCrossFamilyFine125_selected_candidate_sealing_v2_20261008','seal_HuberCrossFamilyFine125_selected_candidate_v2_20261008.py',[]),
        ('HuberCrossFamilyFine125_round146_full_registration_v2_20261008','run_HuberCrossFamilyFine125_round146_full_registration_v5_20261008.py',[])]
    recovery=A/'actual146_recovered145_gate_and_report_preflight_v4_20261008.json'
    pins={str(Path(__file__)):sha(__file__),str(p):sha(p),str(recovery):sha(recovery)};pins[str(A/'actual146_full_context_receiver_preparation_v5_20261008.json')]=sha(A/'actual146_full_context_receiver_preparation_v5_20261008.json');rows={}
    for name,driver,args in specs:
        rows[name]=start(name,driver,args,{**pins,str(A/driver):sha(A/driver)})
    create(A/'HuberCrossFamilyFine146_complete_hidden_launches_v4_20261008.json',{'status':'started_seven_preflighted145_receivers_after_actual141_full_qualification','launches':rows,'input_sha256':pins,
        'stage_base_round':136,'expected_official_cases':125,'QA_version':57,'new_fits':0,'new_quality_scores_by_dispatch':0,'test_labels_read':False})
    print(json.dumps({'started':list(rows)}),flush=True)
if __name__=='__main__':main()
