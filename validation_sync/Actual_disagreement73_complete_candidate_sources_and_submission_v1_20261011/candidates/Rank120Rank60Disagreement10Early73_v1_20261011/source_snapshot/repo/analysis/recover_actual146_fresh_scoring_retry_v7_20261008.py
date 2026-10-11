"""Preserve the failed retries; allocate a fresh scoring/candidate scope for the same frozen winner."""
from pathlib import Path
import sys,time,subprocess
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_JointCrossHuber147_core_receivers_v1_20261008 import save
META=A/'actual146_fresh_scoring_retry_v7_20261008.json'
def full():
 import prepare_actual146_after_recovered145_report_v4_20261008 as prior
 from verified_TLS_Git_retry_runtime_v2_20261008 import installed
 from HuberCrossFamilyFine146_storage_v1_20261008 import installed_transfer
 original=prior.actual_paths
 prior.actual_paths=lambda:list(dict.fromkeys([*original(),Path(__file__),META,A/'prepare_HuberCrossFamilyFine125_selected_candidate_v4_20261008.py',A/'seal_HuberCrossFamilyFine125_selected_candidate_v4_20261008.py',A/'run_HuberCrossFamilyFine125_round146_full_registration_v7_20261008.py',A/'run_HuberCrossFamilyFine125_round146_full_registration_original_v7_20261008.py',A/'recover_actual146_candidate_state_dispatch_v6_20261008.py',A/'actual146_candidate_state_dispatch_recovery_v6_20261008.json']))
 with installed(A/'run_HuberCrossFamilyFine125_round146_full_registration_v7_file_IO_20261008'),installed_transfer():prior.execute('run_HuberCrossFamilyFine125_round146_full_registration_original_v7_20261008.py')
def main():
 failed=A/'service_owned_workflows_20261006/HuberCrossFamilyFine125_selected_candidate_preparation_v3_20261008/service_execution.json';assert read(failed)['status']=='failed'
 originals=[];products=[]
 for old,new in [('prepare_HuberCrossFamilyFine125_selected_candidate_v3_20261008.py','prepare_HuberCrossFamilyFine125_selected_candidate_v4_20261008.py'),('seal_HuberCrossFamilyFine125_selected_candidate_v3_20261008.py','seal_HuberCrossFamilyFine125_selected_candidate_v4_20261008.py'),('run_HuberCrossFamilyFine125_round146_full_registration_original_v6_20261008.py','run_HuberCrossFamilyFine125_round146_full_registration_original_v7_20261008.py')]:
  p=A/old;originals.append(p);s=p.read_text(encoding='utf8')
  for before,after in [('selected_candidate_v3_20261008.py','selected_candidate_v4_20261008.py'),('selected_candidate_preparation_v3_20261008','selected_candidate_preparation_v4_20261008'),('selected_candidate_sealing_v3_20261008','selected_candidate_sealing_v4_20261008'),('selected_release_v3','selected_release_v4'),('HuberCrossFamilyFine125_v3','HuberCrossFamilyFine125_v4'),('candidate_v3','candidate_v4'),('pre_inference_source_freeze_v3','pre_inference_source_freeze_v4'),('actual_registration_v6','actual_registration_v7'),('full_registration_v6_file_IO','full_registration_v7_file_IO')]:s=s.replace(before,after)
  s=s.replace('HuberCrossFamilyFine146_D_scoring_v1_20261008/selected/scoring_validation_only','HuberCrossFamilyFine146_D_scoring_v1_20261008/selected_retry4/scoring_validation_only')
  if old.startswith('prepare_'):s=s.replace('sources += [',"sources += [A/'recover_actual146_fresh_scoring_retry_v7_20261008.py',A/'actual146_fresh_scoring_retry_v7_20261008.json',")
  products.append(save(new,s))
 products.append(save('run_HuberCrossFamilyFine125_round146_full_registration_v7_20261008.py',"from pathlib import Path\nimport sys\nROOT=Path(__file__).resolve().parents[1];sys.path[:0]=[str(ROOT),str(ROOT/'analysis')]\nfrom recover_actual146_fresh_scoring_retry_v7_20261008 import full\nif __name__=='__main__':full()\n"))
 for access,target in [(A/'HuberCrossFamilyFine125_selected_release_v4_20261008',Path('E:/赛题五_本机临时/第146轮_20261008/selected_release_v4')),(ROOT/'candidates/HuberCrossFamilyFine125_v4_20261008',Path('E:/赛题五_本机临时/第146轮_20261008/candidate_v4'))]:
  assert not access.exists() and not target.exists();target.mkdir(parents=True);q=lambda p:"'"+str(p).replace("'","''")+"'"
  subprocess.run(['pwsh','-NoProfile','-NonInteractive','-Command','New-Item -ItemType Junction -Path '+q(access)+' -Target '+q(target)+' | Out-Null'],check=True,creationflags=subprocess.CREATE_NO_WINDOW)
 create(META,{'status':'prepared_fresh_scoring_directory_and_preserved_all_failed_outputs','at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'input_sha256':{str(p):sha(p) for p in [Path(__file__),failed,*originals,*products]},'selected125_parameters_and_scores_unchanged':True,'new_quality_scores':0,'test_labels_read':False})
 from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start
 rows={}
 for name,p in [('HuberCrossFamilyFine125_selected_candidate_preparation_v4_20261008',products[0]),('HuberCrossFamilyFine125_selected_candidate_sealing_v4_20261008',products[1]),('HuberCrossFamilyFine125_round146_full_registration_v4_20261008',products[-1])]:rows[name]=start(name,p.name,[],{str(p):sha(p) for p in [Path(__file__),META,*products]})
 create(A/'actual146_fresh_scoring_retry_hidden_launch_v7_20261008.json',rows);print({n:r['owned_worker_pid'] for n,r in rows.items()},flush=True)
if __name__=='__main__':main()
