"""Preserve prototype import failure and bind only the intended Cross modules in fresh2 receivers."""
from pathlib import Path
import sys,time,json
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_JointCrossHuber147_core_receivers_v1_20261008 import save
def main():
 failed=A/'service_owned_workflows_20261006/AdaptiveJointCrossHuber238_actual_synthetic_controls_v1_20261008/service_execution.json'
 assert read(failed)['status']=='failed' and 'HuberAdaptiveCrossFamily' in read(failed)['failure']
 originals=[];products=[]
 for stem in ('AdaptiveJointCrossHuber_ordered_CDF','AdaptiveJointCrossHuber_ordered_native_stage'):
  p=A/(stem+'_v1_20261008.py');originals.append(p)
  s=p.read_text(encoding='utf8').replace('HuberAdaptiveCrossFamily','HuberCrossFamilyFine')
  s=s.replace('AdaptiveJointCrossHuber_ordered_CDF_v1_20261008','AdaptiveJointCrossHuber_ordered_CDF_v2_20261008')
  products.append(save(stem+'_v2_20261008.py',s))
 for stem in ('verify_AdaptiveJointCrossHuber238_synthetic_controls','verify_AdaptiveJointCrossHuber80_native_historical_calendar','verify_AdaptiveJointCrossHuber238_full_historical_controls'):
  p=A/(stem+'_v1_20261008.py');originals.append(p);s=p.read_text(encoding='utf8').replace('HuberAdaptiveCrossFamily','HuberCrossFamilyFine')
  for token in ('AdaptiveJointCrossHuber_ordered_CDF','AdaptiveJointCrossHuber_ordered_native_stage','AdaptiveJointCrossHuber238_synthetic',
   'AdaptiveJointCrossHuber80_native_historical_calendar','AdaptiveJointCrossHuber238_parent134_historical',
   'actual_AdaptiveJointCrossHuber238_synthetic_location','actual_AdaptiveJointCrossHuber80_native_calendar_location','actual_AdaptiveJointCrossHuber238_parent134_location',
   'AdaptiveJointCrossHuber238_actual_synthetic_controls','AdaptiveJointCrossHuber80_native_historical_calendar_controls'):
   s=s.replace(token+'_v1_20261008',token+'_v2_20261008')
  if 'native_historical_calendar' in stem:
   s=s.replace("sources=[Path(__file__),", "sources=[A/'recover_AdaptiveJointCrossHuber148_import_boundaries_v2_20261008.py',A/'AdaptiveJointCrossHuber148_import_boundary_recovery_v2_20261008.json',Path(__file__),")
  products.append(save(stem+'_v2_20261008.py',s))
 meta=A/'AdaptiveJointCrossHuber148_import_boundary_recovery_v2_20261008.json'
 create(meta,{'status':'prepared_fresh2_actual_Huber_imports_and_Cross0_125_native_controls_after_failed_unscored_prototype',
  'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'input_sha256':{str(p):sha(p) for p in [Path(__file__),failed,*originals,*products]},
  'original148_proposal_parameters_preserved':True,'all_original_failed_files_preserved':True,'new_quality_scores':0,'new_future_inference':0,'test_labels_read':False})
 from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start
 proposal=A/'AdaptiveJointCrossHuber242_round148_proposal_v1_20261008.json';pins={str(p):sha(p) for p in [Path(__file__),meta,proposal,*products,A/'AdaptiveCrossFamily_complete_parent_CDF_v1_20261008.py',A/'AdaptiveCrossFamily_complete_parent_native_stage_v1_20261008.py']}
 specs=[('AdaptiveJointCrossHuber238_actual_synthetic_controls_v2_20261008','verify_AdaptiveJointCrossHuber238_synthetic_controls_v2_20261008.py'),
  ('AdaptiveJointCrossHuber80_native_historical_calendar_controls_v2_20261008','verify_AdaptiveJointCrossHuber80_native_historical_calendar_v2_20261008.py'),
  ('AdaptiveJointCrossHuber238_actual_full_historical_controls_v2_20261008','verify_AdaptiveJointCrossHuber238_full_historical_controls_v2_20261008.py')]
 rows={n:start(n,d,[],pins) for n,d in specs}
 create(A/'AdaptiveJointCrossHuber148_historical_hidden_launches_v2_20261008.json',{'launches':rows,'input_sha256':pins,'native_and_full_wait_for_actual147_closure':True,'new_quality_scores':0})
 print(json.dumps({n:r['owned_worker_pid'] for n,r in rows.items()}),flush=True)
if __name__=='__main__':main()
