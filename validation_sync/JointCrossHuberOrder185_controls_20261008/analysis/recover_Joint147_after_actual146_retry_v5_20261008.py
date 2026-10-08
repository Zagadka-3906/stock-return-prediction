"""Keep frozen185 math unchanged and prospectively correct native component dispatch and failed upstream gates."""
from pathlib import Path
import sys,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_JointCrossHuber147_core_receivers_v1_20261008 import save
META=A/'Joint147_actual146_retry_receivers_v5_20261008.json'
MAP={'HuberCrossFamilyFine125_round146_full_registration_v2_20261008':'HuberCrossFamilyFine125_round146_full_registration_v4_20261008','JointCrossHuber80_native_historical_calendar_controls_v2_20261008':'JointCrossHuber80_native_historical_calendar_controls_v3_20261008','JointCrossHuber181_actual_full_historical_controls_v1_20261008':'JointCrossHuber181_actual_full_historical_controls_v2_20261008','actual_JointCrossHuber80_native_calendar_location_v2_20261008.json':'actual_JointCrossHuber80_native_calendar_location_v3_20261008.json','actual_JointCrossHuber181_parent134_location_v1_20261008.json':'actual_JointCrossHuber181_parent134_location_v2_20261008.json'}
DRIVERS={'verify_JointCrossHuberOrder185_round147_sources_v2_20261008.py':'verify_JointCrossHuberOrder185_round147_sources_v3_20261008.py','publish_JointCrossHuberOrder185_evidence_v4_20261008.py':'publish_JointCrossHuberOrder185_evidence_v5_20261008.py','prepare_JointCrossHuberOrder185_selected_candidate_v3_20261008.py':'prepare_JointCrossHuberOrder185_selected_candidate_v4_20261008.py','run_JointCrossHuberOrder185_round147_full_registration_v5_20261008.py':'run_JointCrossHuberOrder185_round147_full_registration_v6_20261008.py'}
def execute(original,phase=None):
 import prepare_JointCrossHuberOrder185_round147_sources_v4_20261008 as g
 paths=g.source_paths
 extras=[Path(__file__),META,*(A/n for n in DRIVERS.values()),A/'verify_JointCrossHuber80_native_historical_calendar_v3_20261008.py',A/'verify_JointCrossHuber181_full_historical_controls_v2_20261008.py',A/'dispatch_JointCrossHuber147_complete_pipeline_v3_20261008.py',A/'actual_JointCrossHuber80_native_calendar_location_v3_20261008.json',A/'actual_JointCrossHuber181_parent134_location_v2_20261008.json']
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
 from JointCrossHuber147_storage_v1_20261008 import installed_transfer
 from verified_TLS_Git_retry_runtime_v2_20261008 import installed
 with installed(A/'Joint147_actual146_retry_file_IO_v5_20261008'/DRIVERS[original].removesuffix('.py')),installed_transfer():
  if phase is None:ns['main']()
  else:ns['main'](phase)
def main():
 assert read(A/'service_owned_workflows_20261006/JointCrossHuber80_native_historical_calendar_controls_v2_20261008/service_execution.json')['status']=='failed'
 originals=[];products=[]
 for old,new in [('verify_JointCrossHuber80_native_historical_calendar_v2_20261008.py','verify_JointCrossHuber80_native_historical_calendar_v3_20261008.py'),('verify_JointCrossHuber181_full_historical_controls_v1_20261008.py','verify_JointCrossHuber181_full_historical_controls_v2_20261008.py')]:
  p=A/old;originals.append(p);s=p.read_text(encoding='utf8')
  for before,after in MAP.items():s=s.replace(before,after)
  s=s.replace('JointCrossHuber80_native_historical_calendar_v2_20261008','JointCrossHuber80_native_historical_calendar_v3_20261008').replace('JointCrossHuber181_parent134_historical_v1_20261008','JointCrossHuber181_parent134_historical_v2_20261008')
  if old.startswith('verify_JointCrossHuber80'):
   s=s.replace("kind=row['state_kind']","kind=row.get('native_stage_state_kind',row['state_kind']);storage_kind=row['state_kind']").replace("info['independent_'+kind+","info['independent_'+storage_kind+")
  s=s.replace("sources=[Path(__file__),","sources=[Path(__file__),A/'recover_Joint147_after_actual146_retry_v5_20261008.py',A/'Joint147_actual146_retry_receivers_v5_20261008.json',")
  products.append(save(new,s))
 for old,new in DRIVERS.items():
  originals.append(A/old)
  s="from pathlib import Path\nimport sys\nROOT=Path(__file__).resolve().parents[1];sys.path[:0]=[str(ROOT),str(ROOT/'analysis')]\nfrom recover_Joint147_after_actual146_retry_v5_20261008 import execute\n"
  if old.startswith('publish_'):s+=f"if __name__=='__main__':\n import argparse\n p=argparse.ArgumentParser();p.add_argument('phase',choices=('controls','scores'));execute({old!r},p.parse_args().phase)\n"
  else:s+=f"if __name__=='__main__':execute({old!r})\n"
  products.append(save(new,s))
 p=A/'dispatch_JointCrossHuber147_complete_pipeline_v2_20261008.py';originals.append(p);s=p.read_text(encoding='utf8')
 for before,after in {**MAP,**DRIVERS}.items():s=s.replace(before,after)
 s=s.replace('complete_hidden_launches_v2_20261008','complete_hidden_launches_v3_20261008')
 products.append(save('dispatch_JointCrossHuber147_complete_pipeline_v3_20261008.py',s))
 create(META,{'status':'prepared_actual146_completion_retry_and_native_storage_kind_dispatch_before_any185_quality','at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'input_sha256':{str(p):sha(p) for p in [Path(__file__),*originals,*products]},'original_generated_eight_canonical_routes_and185_grid_and32_prospective_hashes_unchanged':True,'old_failures_preserved':True,'new_quality_scores':0,'test_labels_read':False})
 from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start
 rows={}
 for name,p in [('JointCrossHuber80_native_historical_calendar_controls_v3_20261008',products[0]),('JointCrossHuber181_actual_full_historical_controls_v2_20261008',products[1]),('JointCrossHuber147_complete_chronological_dispatch_v3_20261008',products[-1])]:rows[name]=start(name,p.name,[],{str(p):sha(p) for p in [Path(__file__),META,*products]})
 create(A/'Joint147_actual146_retry_hidden_launches_v5_20261008.json',rows);print({n:r['owned_worker_pid'] for n,r in rows.items()},flush=True)
if __name__=='__main__':main()
