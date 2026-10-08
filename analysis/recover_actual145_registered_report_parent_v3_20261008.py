"""Resume after completed125 registration and genuine inference; repair only reporting baseline binding."""
from pathlib import Path
import sys,time,hashlib
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
def verify_existing():
 import prepare_CrossFamilyFine125_round145_sources_v2_20261008 as g
 prep=A/'CrossFamilyFine125_round145_source_preparation_v1_20261008.json';p=read(prep)
 for f,d in p['input_sha256'].items():assert sha(f)==d,f
 for n,s in g.generate(p['actual_comparison_parent_round']).items():assert sha(A/n)==hashlib.sha256(s.encode()).hexdigest(),n
 folder=A/'optimization_20261003_r145';protocol=read(folder/'protocol.json');selection=read(folder/'selection.json')
 pilot=read(A/'CrossFamilyFine125_official_comparison_v1_20261008/verification.json')
 assert protocol['expected_scored_records']==len(selection['ranking'])==len(pilot['records'])==125
 assert selection['winner']['metrics']==pilot['best']['metrics']
 assert read(folder/'actual_registration_preparation.json')['status']=='passed_actual125_scores_controls_and_sealed_selected_model_candidate_registered'
 original=g.source_paths
 extras=[Path(__file__),A/'actual_explicit_comparison_parent_binding_v1_20261008.py',A/'run_CrossFamilyFine125_round145_full_registration_v3_20261008.py',
  A/'actual145_report_parent_recovery_preparation_v3_20261008.json',A/'actual145_report_parent_binding_v3_20261008.json',
  folder/'full_registration_failure.json',A/'service_owned_workflows_20261006/CrossFamilyFine125_round145_full_registration_v2_20261008/service_execution.json']
 g.source_paths=lambda:list(dict.fromkeys([*original(),*extras]))
 return protocol
def main():
 failed=A/'service_owned_workflows_20261006/CrossFamilyFine125_round145_full_registration_v2_20261008/service_execution.json';assert read(failed)['status']=='failed'
 old=A/'run_CrossFamilyFine125_round145_full_registration_v2_20261008.py';target=A/'run_CrossFamilyFine125_round145_full_registration_v3_20261008.py'
 s=old.read_text(encoding='utf8').replace('actual_registration_v2_20261008','actual_registration_v3_20261008').replace('full_registration_v2_file_IO_20261008','full_registration_v3_file_IO_20261008')
 begin=s.index('    from prepare_CrossFamilyFine125_round145_sources_v2_20261008 import main as prepare_sources');end=s.index('    scratch=',begin)
 s=s[:begin]+'''    from recover_actual145_registered_report_parent_v3_20261008 import verify_existing
    protocol=verify_existing();folder=A/'optimization_20261003_r145';pins=dict(protocol['input_sha256'])
    from actual_explicit_comparison_parent_binding_v1_20261008 import bind
    bind(145,A/'actual145_report_parent_binding_v3_20261008.json')
    for p in (A/'actual145_report_parent_binding_v3_20261008.json',A/'actual145_report_parent_recovery_preparation_v3_20261008.json',Path(__file__),A/'actual_explicit_comparison_parent_binding_v1_20261008.py',A/'recover_actual145_registered_report_parent_v3_20261008.py'):pins[str(p)]=sha(p)
    ready=read(A/'CrossFamilyFine125_selected_release_v1_20261008/selected_candidate_ready_for_registration.json')
'''+s[end:]
 s=s.replace('actual_main7_idle_before_and_after_hold.json','actual_main7_idle_report_recovery_v3.json').replace('full_registration_failure.json','full_registration_recovery_failure_v3.json').replace('actual_hidden_registration_children.json','actual_hidden_registration_children_recovery_v3.json')
 compile(s,str(target),'exec')
 with target.open('x',encoding='utf8',newline='') as f:f.write(s)
 proof=A/'actual145_report_parent_recovery_preparation_v3_20261008.json'
 create(proof,{'status':'prepared_recovery_after_actual125_scoring_two_full_native_replays_and_completed_registration_before_report',
  'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'input_sha256':{str(p):sha(p) for p in [Path(__file__),failed,old,target,A/'actual_explicit_comparison_parent_binding_v1_20261008.py']},
  'all_original_failures_and_canonical_sources_preserved':True,'original_parameters_models_scores_and_freeze_unchanged':True,'no_repeated_registration_or_inference':True,'test_labels_read':False})
 from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start
 row=start('CrossFamilyFine125_round145_full_registration_v3_20261008',target.name,[],{str(p):sha(p) for p in [Path(__file__),target,proof]})
 create(A/'actual145_report_parent_recovery_hidden_launch_v3_20261008.json',row)
 print(row['owned_worker_pid'],flush=True)
if __name__=='__main__':main()
