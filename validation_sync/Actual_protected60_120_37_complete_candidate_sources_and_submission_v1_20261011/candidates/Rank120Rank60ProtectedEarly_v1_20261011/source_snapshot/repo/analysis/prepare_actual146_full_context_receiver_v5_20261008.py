"""Preserve protected transfer/TLS contexts around recovered full146 and publish actual5 receiver metadata."""
from pathlib import Path
import sys,time,json
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from prepare_JointCrossHuber147_core_receivers_v1_20261008 import save
META=A/'actual146_full_context_receiver_preparation_v5_20261008.json'
FILES=['verify_HuberCrossFamilyFine125_round146_sources_v5_20261008.py','publish_HuberCrossFamilyFine125_evidence_v5_20261008.py',
 'run_HuberCrossFamilyFine125_round146_full_registration_v5_20261008.py','dispatch_HuberCrossFamilyFine146_complete_pipeline_v6_20261008.py']
def execute(original,phase=None):
 import prepare_actual146_after_recovered145_report_v4_20261008 as prior
 for f,d in read(META)['input_sha256'].items():assert sha(f)==d,f
 paths=prior.actual_paths
 prior.actual_paths=lambda:list(dict.fromkeys([*paths(),Path(__file__),META,*(A/n for n in FILES)]))
 if original.startswith('run_HuberCrossFamilyFine125_round146_full'):
  from verified_TLS_Git_retry_runtime_v2_20261008 import installed
  from HuberCrossFamilyFine146_storage_v1_20261008 import installed_transfer
  with installed(A/'run_HuberCrossFamilyFine125_round146_full_registration_v5_file_IO_20261008'),installed_transfer():prior.execute(original)
 else:prior.execute(original,phase)
def main():
 assert not (A/'service_owned_workflows_20261006/HuberCrossFamilyFine125_official_comparison_v2_20261008').exists()
 originals=[];products=[]
 for old,new in [('verify_HuberCrossFamilyFine125_round146_sources_v3_20261008.py',FILES[0]),('publish_HuberCrossFamilyFine125_evidence_v3_20261008.py',FILES[1]),('run_HuberCrossFamilyFine125_round146_full_registration_v3_20261008.py',FILES[2])]:
  originals.append(A/old)
  s='''"""Protected original146 mathematical receiver; actual5 operational source closure and full contexts."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1];sys.path[:0]=[str(ROOT),str(ROOT/'analysis')]
from prepare_actual146_full_context_receiver_v5_20261008 import execute
'''
  if old.startswith('publish_'):s+=f"if __name__=='__main__':\n import argparse\n p=argparse.ArgumentParser();p.add_argument('phase',choices=('controls','scores'));execute({old!r},p.parse_args().phase)\n"
  else:s+=f"if __name__=='__main__':execute({old!r})\n"
  products.append(save(new,s))
 old=A/'dispatch_HuberCrossFamilyFine146_complete_pipeline_v5_20261008.py';originals.append(old);s=old.read_text(encoding='utf8')
 for before,after in [('verify_HuberCrossFamilyFine125_round146_sources_v4_20261008.py',FILES[0]),('publish_HuberCrossFamilyFine125_evidence_v4_20261008.py',FILES[1]),('run_HuberCrossFamilyFine125_round146_full_registration_v4_20261008.py',FILES[2])]:s=s.replace(before,after)
 s=s.replace('execution_cost_slot_handoff_v3_20261008','execution_cost_slot_handoff_v4_20261008').replace('complete_hidden_launches_v3_20261008','complete_hidden_launches_v4_20261008')
 s=s.replace(";rows={}",";pins[str(A/'actual146_full_context_receiver_preparation_v5_20261008.json')]=sha(A/'actual146_full_context_receiver_preparation_v5_20261008.json');rows={}")
 products.append(save(FILES[3],s))
 from handoff_joint_goss_round97_full_execution_20261006 import suspended_idle
 service=A/'service_owned_workflows_20261006/HuberCrossFamilyFine146_complete_chronological_dispatch_v5_20261008';row=read(service/'native_launch.json');assert owned(row)
 parent,worker,idle=suspended_idle(row,'    closed (dispatch_HuberCrossFamilyFine146_complete_pipeline_v5_20261008.py:')
 try:
  assert not (A/'service_owned_workflows_20261006/HuberCrossFamilyFine125_official_comparison_v2_20261008').exists()
  worker.terminate();parent.terminate()
  import psutil
  _,alive=psutil.wait_procs([worker,parent],timeout=10);assert not alive and not owned(row)
  create(META,{'status':'prepared_actual5_full_TLS_transfer_contexts_and_source_publication_before_any146_quality',
   'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'input_sha256':{str(p):sha(p) for p in [Path(__file__),*originals,*products]},
   'cancelled_only_proved_idle_dispatch5':{'launch':row,'idle_stack':idle},'old_benchmark3_kept_running':True,
   'original_scientific_sources_generated_routes_grid_models_scores_and_selection_rules_unchanged':True,'new_quality_scores':0,'test_labels_read':False})
  from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start
  d=start('HuberCrossFamilyFine146_complete_chronological_dispatch_v6_20261008',FILES[3],[],{str(p):sha(p) for p in [Path(__file__),META,*products]})
  create(A/'actual146_full_context_dispatch_hidden_launch_v5_20261008.json',d);print(d['owned_worker_pid'],flush=True)
 finally:
  for p in (worker,parent):
   if p.is_running():p.resume()
if __name__=='__main__':main()
