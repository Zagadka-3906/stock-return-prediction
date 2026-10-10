"""Keep frozen242 math unchanged and prospectively correct native component dispatch and failed upstream gates."""
from pathlib import Path
import sys,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_JointCrossHuber147_core_receivers_v1_20261008 import save
META=A/'Adaptive148_native_dispatch_receivers_v3_20261008.json'
MAP={'JointCrossHuberOrder185_round147_full_registration_v1_20261008':'JointCrossHuberOrder185_round147_full_registration_v1_20261008','AdaptiveJointCrossHuber80_native_historical_calendar_controls_v2_20261008':'AdaptiveJointCrossHuber80_native_historical_calendar_controls_v3_20261008','AdaptiveJointCrossHuber238_actual_full_historical_controls_v2_20261008':'AdaptiveJointCrossHuber238_actual_full_historical_controls_v3_20261008','actual_AdaptiveJointCrossHuber80_native_calendar_location_v2_20261008.json':'actual_AdaptiveJointCrossHuber80_native_calendar_location_v3_20261008.json','actual_AdaptiveJointCrossHuber238_parent134_location_v2_20261008.json':'actual_AdaptiveJointCrossHuber238_parent134_location_v3_20261008.json'}
DRIVERS={'verify_AdaptiveJointCrossHuber242_round148_sources_v2_20261008.py':'verify_AdaptiveJointCrossHuber242_round148_sources_v3_20261008.py','publish_AdaptiveJointCrossHuber242_evidence_v2_20261008.py':'publish_AdaptiveJointCrossHuber242_evidence_v3_20261008.py','prepare_AdaptiveJointCrossHuber242_selected_candidate_v1_20261008.py':'prepare_AdaptiveJointCrossHuber242_selected_candidate_v2_20261008.py','run_AdaptiveJointCrossHuber242_round148_full_registration_v2_20261008.py':'run_AdaptiveJointCrossHuber242_round148_full_registration_v3_20261008.py'}
def execute(original,phase=None):
 import prepare_AdaptiveJointCrossHuber242_round148_sources_v2_20261008 as g
 paths=g.source_paths
 extras=[Path(__file__),META,*(A/n for n in DRIVERS.values()),A/'verify_AdaptiveJointCrossHuber80_native_historical_calendar_v3_20261008.py',A/'verify_AdaptiveJointCrossHuber238_full_historical_controls_v3_20261008.py',A/'dispatch_AdaptiveJointCrossHuber148_complete_pipeline_v3_20261008.py',A/'actual_AdaptiveJointCrossHuber80_native_calendar_location_v3_20261008.json',A/'actual_AdaptiveJointCrossHuber238_parent134_location_v3_20261008.json']
 g.source_paths=lambda:list(dict.fromkeys([*paths(),*[p for p in extras if p.exists()]]))
 for p,d in read(META)['input_sha256'].items():assert sha(p)==d,p
 p=A/original;s=p.read_text(encoding='utf8')
 for before,after in MAP.items():s=s.replace(before,after)
 if original.startswith('prepare_'):
  assert s.count("kind=row['state_kind']")==1
  s=s.replace("kind=row['state_kind']","kind=row.get('native_stage_state_kind',row['state_kind']);storage_kind=row['state_kind']")
  s=s.replace("info['independent_'+kind+", "info['independent_'+storage_kind+")
 ns={'__file__':str(A/DRIVERS[original]),'__name__':'actual_joint147_protected_receiver_after_failed_upstream_recovery'}
 exec(compile(s,str(p),'exec'),ns)
 from AdaptiveJointCrossHuber148_storage_v1_20261008 import installed_transfer
 from verified_TLS_Git_retry_runtime_v2_20261008 import installed
 with installed(A/'Adaptive148_native_dispatch_file_IO_v3_20261008'/DRIVERS[original].removesuffix('.py')),installed_transfer():
  if phase is None:ns['main']()
  else:ns['main'](phase)
def main():
 from handoff_joint_goss_round97_full_execution_20261006 import suspended_idle
 from run_dependency_queue_v3_20261006 import owned
 retired=[]
 for n,driver in [('AdaptiveJointCrossHuber80_native_historical_calendar_controls_v2_20261008','verify_AdaptiveJointCrossHuber80_native_historical_calendar_v2_20261008.py'),('AdaptiveJointCrossHuber238_actual_full_historical_controls_v2_20261008','verify_AdaptiveJointCrossHuber238_full_historical_controls_v2_20261008.py'),('AdaptiveJointCrossHuber148_complete_chronological_dispatch_v2_20261008','dispatch_AdaptiveJointCrossHuber148_complete_pipeline_v2_20261008.py')]:
  row=read(A/'service_owned_workflows_20261006'/n/'native_launch.json');assert owned(row)
  parent,worker,proof=suspended_idle(row,'    closed ('+driver+':')
  worker.terminate();parent.terminate()
  import psutil
  _,alive=psutil.wait_procs([worker,parent],timeout=10);assert not alive and not owned(row)
  retired.append({'launch':row,'idle_stack':proof,'no_scientific_work_started':True})
 create(A/'Adaptive148_proved_idle_old_receivers_retired_v3_20261008.json',retired)
 originals=[];products=[]
 for old,new in [('verify_AdaptiveJointCrossHuber80_native_historical_calendar_v2_20261008.py','verify_AdaptiveJointCrossHuber80_native_historical_calendar_v3_20261008.py'),('verify_AdaptiveJointCrossHuber238_full_historical_controls_v2_20261008.py','verify_AdaptiveJointCrossHuber238_full_historical_controls_v3_20261008.py')]:
  p=A/old;originals.append(p);s=p.read_text(encoding='utf8')
  for before,after in MAP.items():s=s.replace(before,after)
  s=s.replace('AdaptiveJointCrossHuber80_native_historical_calendar_v2_20261008','AdaptiveJointCrossHuber80_native_historical_calendar_v3_20261008').replace('AdaptiveJointCrossHuber238_parent134_historical_v2_20261008','AdaptiveJointCrossHuber238_parent134_historical_v3_20261008')
  if old.startswith('verify_AdaptiveJointCrossHuber80'):
   s=s.replace("kind=row['state_kind']","kind=row.get('native_stage_state_kind',row['state_kind']);storage_kind=row['state_kind']").replace("info['independent_'+kind+","info['independent_'+storage_kind+")
  s=s.replace("sources=[Path(__file__),","sources=[Path(__file__),A/'recover_Adaptive148_native_dispatch_v3_20261008.py',A/'Adaptive148_native_dispatch_receivers_v3_20261008.json',")
  products.append(save(new,s))
 for old,new in DRIVERS.items():
  originals.append(A/old)
  s="from pathlib import Path\nimport sys\nROOT=Path(__file__).resolve().parents[1];sys.path[:0]=[str(ROOT),str(ROOT/'analysis')]\nfrom recover_Adaptive148_native_dispatch_v3_20261008 import execute\n"
  if old.startswith('publish_'):s+=f"if __name__=='__main__':\n import argparse\n p=argparse.ArgumentParser();p.add_argument('phase',choices=('controls','scores'));execute({old!r},p.parse_args().phase)\n"
  else:s+=f"if __name__=='__main__':execute({old!r})\n"
  products.append(save(new,s))
 p=A/'dispatch_AdaptiveJointCrossHuber148_complete_pipeline_v2_20261008.py';originals.append(p);s=p.read_text(encoding='utf8')
 for before,after in {**MAP,**DRIVERS}.items():s=s.replace(before,after)
 s=s.replace('complete_hidden_launches_v2_20261008','complete_hidden_launches_v3_20261008')
 products.append(save('dispatch_AdaptiveJointCrossHuber148_complete_pipeline_v3_20261008.py',s))
 create(META,{'status':'prepared_actual147_completion_retry_and_native_storage_kind_dispatch_before_any242_quality','at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'input_sha256':{str(p):sha(p) for p in [Path(__file__),*originals,*products]},'original_generated_eight_canonical_routes_and242_grid_and32_prospective_hashes_unchanged':True,'old_failures_preserved':True,'new_quality_scores':0,'test_labels_read':False})
 from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start
 rows={}
 for name,p in [('AdaptiveJointCrossHuber80_native_historical_calendar_controls_v3_20261008',products[0]),('AdaptiveJointCrossHuber238_actual_full_historical_controls_v3_20261008',products[1]),('AdaptiveJointCrossHuber148_complete_chronological_dispatch_v3_20261008',products[-1])]:rows[name]=start(name,p.name,[],{str(p):sha(p) for p in [Path(__file__),META,*products]})
 create(A/'Adaptive148_native_dispatch_hidden_launches_v3_20261008.json',rows);print({n:r['owned_worker_pid'] for n,r in rows.items()},flush=True)
if __name__=='__main__':main()
