"""Correct an unexecuted dispatcher service identity; retain frozen242 scientific routes and idle original."""
from pathlib import Path
import sys,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from prepare_JointCrossHuber147_core_receivers_v1_20261008 import save
META=A/'Adaptive148_own_full_service_identity_recovery_v4_20261008.json'
DRIVERS={'verify_AdaptiveJointCrossHuber242_round148_sources_v2_20261008.py':'verify_AdaptiveJointCrossHuber242_round148_sources_v4_20261008.py','publish_AdaptiveJointCrossHuber242_evidence_v2_20261008.py':'publish_AdaptiveJointCrossHuber242_evidence_v4_20261008.py','run_AdaptiveJointCrossHuber242_round148_full_registration_v2_20261008.py':'run_AdaptiveJointCrossHuber242_round148_full_registration_v4_20261008.py'}
def execute(original,phase=None):
 import prepare_AdaptiveJointCrossHuber242_round148_sources_v2_20261008 as g
 import recover_Adaptive148_native_dispatch_v3_20261008 as prior
 paths=g.source_paths;extras=[Path(__file__),META,*(A/n for n in DRIVERS.values()),A/'dispatch_AdaptiveJointCrossHuber148_complete_pipeline_v4_20261008.py']
 g.source_paths=lambda:list(dict.fromkeys([*paths(),*extras]))
 for p,d in read(META)['input_sha256'].items():assert sha(p)==d,p
 prior.execute(original,phase)
def main():
 p=A/'dispatch_AdaptiveJointCrossHuber148_complete_pipeline_v3_20261008.py';originals=[p];products=[]
 s=p.read_text(encoding='utf8')
 needle="('JointCrossHuberOrder185_round147_full_registration_v1_20261008','run_AdaptiveJointCrossHuber242_round148_full_registration_v3_20261008.py'";assert s.count(needle)==1
 s=s.replace(needle,"('AdaptiveJointCrossHuber242_round148_full_registration_v1_20261008','run_AdaptiveJointCrossHuber242_round148_full_registration_v4_20261008.py'")
 for before,after in [('verify_AdaptiveJointCrossHuber242_round148_sources_v3_20261008.py',DRIVERS['verify_AdaptiveJointCrossHuber242_round148_sources_v2_20261008.py']),('publish_AdaptiveJointCrossHuber242_evidence_v3_20261008.py',DRIVERS['publish_AdaptiveJointCrossHuber242_evidence_v2_20261008.py'])]:s=s.replace(before,after)
 s=s.replace('complete_hidden_launches_v3','complete_hidden_launches_v4');products.append(save('dispatch_AdaptiveJointCrossHuber148_complete_pipeline_v4_20261008.py',s))
 for old,new in DRIVERS.items():
  originals.append(A/old);s="from pathlib import Path\nimport sys\nROOT=Path(__file__).resolve().parents[1];sys.path[:0]=[str(ROOT),str(ROOT/'analysis')]\nfrom recover_Adaptive148_own_full_service_identity_v4_20261008 import execute\n"
  if old.startswith('publish_'):s+=f"if __name__=='__main__':\n import argparse\n p=argparse.ArgumentParser();p.add_argument('phase',choices=('controls','scores'));execute({old!r},p.parse_args().phase)\n"
  else:s+=f"if __name__=='__main__':execute({old!r})\n"
  products.append(save(new,s))
 from handoff_joint_goss_round97_full_execution_20261006 import suspended_idle
 row=read(A/'service_owned_workflows_20261006/AdaptiveJointCrossHuber148_complete_chronological_dispatch_v3_20261008/native_launch.json');assert owned(row)
 parent,worker,idle=suspended_idle(row,'    closed (dispatch_AdaptiveJointCrossHuber148_complete_pipeline_v3_20261008.py:');worker.terminate();parent.terminate()
 import psutil
 _,alive=psutil.wait_procs([worker,parent],timeout=10);assert not alive and not owned(row)
 create(META,{'status':'prepared_fresh_dispatcher_with_own148_full_service_before_any242_quality','at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'input_sha256':{str(p):sha(p) for p in [Path(__file__),*originals,*products]},'cancelled_only_proved_idle_dispatcher':{'launch':row,'idle_stack':idle},'native80_and_full238_workers_kept_running':True,'frozen242_parameters_and32_routes_unchanged':True,'new_quality_scores':0,'test_labels_read':False})
 from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start
 p=products[0];new=start('AdaptiveJointCrossHuber148_complete_chronological_dispatch_v4_20261008',p.name,[],{str(p):sha(p),str(META):sha(META),str(Path(__file__)):sha(__file__)})
 create(A/'Adaptive148_own_full_service_identity_hidden_launch_v4_20261008.json',new);print(new['owned_worker_pid'],flush=True)
if __name__=='__main__':main()
