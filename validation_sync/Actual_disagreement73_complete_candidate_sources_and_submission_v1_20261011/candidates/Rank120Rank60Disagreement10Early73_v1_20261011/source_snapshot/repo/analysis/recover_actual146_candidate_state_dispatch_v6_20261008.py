"""Retry the unchanged125 winner with the declared native Huber decoder, fresh frozen outputs and preserved failures."""
from pathlib import Path
import sys,time,hashlib,subprocess
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_JointCrossHuber147_core_receivers_v1_20261008 import save
META=A/'actual146_candidate_state_dispatch_recovery_v6_20261008.json'
EXTRAS=[Path(__file__),META,A/'prepare_HuberCrossFamilyFine125_selected_candidate_v3_20261008.py',A/'seal_HuberCrossFamilyFine125_selected_candidate_v3_20261008.py',A/'run_HuberCrossFamilyFine125_round146_full_registration_v6_20261008.py',A/'run_HuberCrossFamilyFine125_round146_full_registration_original_v6_20261008.py']

def full():
 import prepare_actual146_after_recovered145_report_v4_20261008 as prior
 from verified_TLS_Git_retry_runtime_v2_20261008 import installed
 from HuberCrossFamilyFine146_storage_v1_20261008 import installed_transfer
 original=prior.actual_paths
 prior.actual_paths=lambda:list(dict.fromkeys([*original(),*EXTRAS]))
 with installed(A/'run_HuberCrossFamilyFine125_round146_full_registration_v6_file_IO_20261008'),installed_transfer():
  prior.execute('run_HuberCrossFamilyFine125_round146_full_registration_original_v6_20261008.py')

def main():
 failed=A/'service_owned_workflows_20261006/HuberCrossFamilyFine125_selected_candidate_preparation_v2_20261008/service_execution.json'
 assert read(failed)['status']=='failed'
 plan=read(A/'HuberCrossFamilyFine125_round146_plan_v2_20261008.json')
 assert all(plan['heads'][h]['state_kind']=='linear' and plan['heads'][h]['native_stage_state_kind']=='HuberIRLS64_linear' for h in ('huber_d010','huber_d025'))
 pilot=read(A/'HuberCrossFamilyFine125_official_comparison_v1_20261008/verification.json')
 assert len(pilot['records'])==125 and pilot['best']['configuration']['weight']==.00325
 old=A/'prepare_HuberCrossFamilyFine125_selected_candidate_v2_20261008.py';s=old.read_text(encoding='utf8')
 s=s.replace("OUT=A/'HuberCrossFamilyFine125_selected_release_v1_20261008'","OUT=A/'HuberCrossFamilyFine125_selected_release_v3_20261008'")
 s=s.replace("CANDIDATE=ROOT/'candidates/HuberCrossFamilyFine125_v1_20261008'","CANDIDATE=ROOT/'candidates/HuberCrossFamilyFine125_v3_20261008'")
 s=s.replace('pre_inference_source_freeze_v1','pre_inference_source_freeze_v3')
 s=s.replace("kind=row['state_kind']","kind=row.get('native_stage_state_kind',row['state_kind']); storage_kind=row['state_kind']")
 s=s.replace("info['independent_'+kind+'_state_path']","info['independent_'+storage_kind+'_state_path']").replace("info['independent_'+kind+'_state_sha256']","info['independent_'+storage_kind+'_state_sha256']")
 # Pin all retry sources before reading future X; no scoring or numerical/model parameter changes.
 s=s.replace("pins={**protocol_pins,", "sources += [A/'recover_actual146_candidate_state_dispatch_v6_20261008.py',A/'actual146_candidate_state_dispatch_recovery_v6_20261008.json',A/'seal_HuberCrossFamilyFine125_selected_candidate_v3_20261008.py']\n    pins={**protocol_pins,")
 products=[save('prepare_HuberCrossFamilyFine125_selected_candidate_v3_20261008.py',s)]
 oldseal=A/'seal_HuberCrossFamilyFine125_selected_candidate_v2_20261008.py';s=oldseal.read_text(encoding='utf8').replace('selected_candidate_preparation_v2_20261008','selected_candidate_preparation_v3_20261008').replace('selected_release_v1_20261008','selected_release_v3_20261008')
 # Append the canonical readiness pointer only after the new full candidate has sealed successfully.
 s=s.replace("\n\nif __name__", "\n    create(A/'HuberCrossFamilyFine125_selected_release_v1_20261008/selected_candidate_ready_for_registration.json',read(release/'selected_candidate_ready_for_registration.json'))\n\nif __name__")
 products.append(save('seal_HuberCrossFamilyFine125_selected_candidate_v3_20261008.py',s))
 originalfull=A/'run_HuberCrossFamilyFine125_round146_full_registration_v3_20261008.py';s=originalfull.read_text(encoding='utf8').replace('actual_registration_v3_20261008','actual_registration_v6_20261008').replace('selected_candidate_sealing_v2_20261008','selected_candidate_sealing_v3_20261008').replace('full_registration_v3_file_IO','full_registration_v6_file_IO')
 products.append(save('run_HuberCrossFamilyFine125_round146_full_registration_original_v6_20261008.py',s))
 products.append(save('run_HuberCrossFamilyFine125_round146_full_registration_v6_20261008.py',"from pathlib import Path\nimport sys\nROOT=Path(__file__).resolve().parents[1];sys.path[:0]=[str(ROOT),str(ROOT/'analysis')]\nfrom recover_actual146_candidate_state_dispatch_v6_20261008 import full\nif __name__=='__main__':full()\n"))
 from HuberCrossFamilyFine146_storage_v1_20261008 import OUTPUTS
 destinations=[]
 for access,target in [(A/'HuberCrossFamilyFine125_selected_release_v3_20261008',Path('E:/赛题五_本机临时/第146轮_20261008/selected_release_v3')),(ROOT/'candidates/HuberCrossFamilyFine125_v3_20261008',Path('E:/赛题五_本机临时/第146轮_20261008/candidate_v3'))]:
  assert not access.exists() and not target.exists() and target.is_relative_to(Path('E:/赛题五_本机临时/第146轮_20261008'))
  target.mkdir(parents=True);q=lambda p:"'"+str(p).replace("'","''")+"'"
  subprocess.run(['pwsh','-NoProfile','-NonInteractive','-Command','New-Item -ItemType Junction -Path '+q(access)+' -Target '+q(target)+' | Out-Null'],check=True,creationflags=subprocess.CREATE_NO_WINDOW)
  destinations.append({'access':str(access),'target':str(target)})
 # Each worker independently admits its exact fresh E-backed output through the unchanged storage guard.
 p=products[0];s=p.read_text(encoding='utf8');s=s.replace('empty(OUT);empty(CANDIDATE)',"from HuberCrossFamilyFine146_storage_v1_20261008 import OUTPUTS\n    OUTPUTS[OUT]=Path('E:/赛题五_本机临时/第146轮_20261008/selected_release_v3');OUTPUTS[CANDIDATE]=Path('E:/赛题五_本机临时/第146轮_20261008/candidate_v3')\n    empty(OUT);empty(CANDIDATE)")
 # This fresh file has not been admitted, launched or frozen yet.
 p.write_text(s,encoding='utf8',newline='\n');compile(s,str(p),'exec')
 create(META,{'status':'prepared_retry_of_same_selected125_scheme_with_native_stage_state_kind_and_fresh_full_inference','at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'input_sha256':{str(p):sha(p) for p in [Path(__file__),failed,old,oldseal,originalfull,*products]},'original_failed_selection_and_source_freeze_and_partial_candidate_preserved':True,'official125_scores_and_selected_parameters_and_native_model_SHA_unchanged':True,'decoder_dispatch_uses_already_declared_native_stage_state_kind':True,'fresh_E_outputs':destinations,'new_quality_scores':0,'new_model_fits':0,'test_labels_read':False})
 from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start
 launches={}
 for name,driver in [('HuberCrossFamilyFine125_selected_candidate_preparation_v3_20261008',products[0].name),('HuberCrossFamilyFine125_selected_candidate_sealing_v3_20261008',products[1].name),('HuberCrossFamilyFine125_round146_full_registration_v3_20261008',products[-1].name)]:
  launches[name]=start(name,driver,[],{str(p):sha(p) for p in [Path(__file__),META,*products]})
 create(A/'actual146_candidate_state_dispatch_hidden_launches_v6_20261008.json',launches)
 print({n:r['owned_worker_pid'] for n,r in launches.items()},flush=True)
if __name__=='__main__':main()
