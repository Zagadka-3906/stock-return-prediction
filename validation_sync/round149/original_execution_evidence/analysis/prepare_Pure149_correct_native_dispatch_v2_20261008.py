"""Prospectively correct two deferred149 control receivers; preserve their idle originals."""
from pathlib import Path
import sys,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from prepare_JointCrossHuber147_core_receivers_v1_20261008 import save
def main():
 from handoff_joint_goss_round97_full_execution_20261006 import suspended_idle
 import psutil
 retired=[]
 for n,driver in [('PureRFFHuber80_native_historical_calendar_controls_v1_20261008','verify_PureRFFHuber80_native_historical_calendar_v1_20261008.py'),('PureRFFHuber124_actual_full_historical_controls_v1_20261008','verify_PureRFFHuber124_full_historical_controls_v1_20261008.py')]:
  row=read(A/'service_owned_workflows_20261006'/n/'native_launch.json');assert owned(row)
  parent,worker,proof=suspended_idle(row,'    closed ('+driver+':');worker.terminate();parent.terminate()
  _,alive=psutil.wait_procs([worker,parent],timeout=10);assert not alive and not owned(row)
  retired.append({'launch':row,'idle_stack':proof,'actual_scientific_work_not_started':True})
 originals=[];products=[]
 for old,new in [('verify_PureRFFHuber80_native_historical_calendar_v1_20261008.py','verify_PureRFFHuber80_native_historical_calendar_v2_20261008.py'),('verify_PureRFFHuber124_full_historical_controls_v1_20261008.py','verify_PureRFFHuber124_full_historical_controls_v2_20261008.py')]:
  p=A/old;originals.append(p);s=p.read_text(encoding='utf8')
  for before,after in [('PureRFFHuber80_native_historical_calendar_v1_20261008','PureRFFHuber80_native_historical_calendar_v2_20261008'),('PureRFFHuber80_native_historical_calendar_controls_v1_20261008','PureRFFHuber80_native_historical_calendar_controls_v2_20261008'),('PureRFFHuber124_parent134_historical_v1_20261008','PureRFFHuber124_parent134_historical_v2_20261008'),('actual_PureRFFHuber80_native_calendar_location_v1_20261008','actual_PureRFFHuber80_native_calendar_location_v2_20261008'),('actual_PureRFFHuber124_parent134_location_v1_20261008','actual_PureRFFHuber124_parent134_location_v2_20261008')]:s=s.replace(before,after)
  if old.startswith('verify_PureRFFHuber80'):
   assert s.count("kind=row['state_kind']")==1
   s=s.replace("kind=row['state_kind']","kind=row.get('native_stage_state_kind',row['state_kind']);storage_kind=row['state_kind']").replace("info['independent_'+kind+","info['independent_'+storage_kind+")
  s=s.replace("sources=[Path(__file__),","sources=[Path(__file__),A/'prepare_Pure149_correct_native_dispatch_v2_20261008.py',A/'Pure149_correct_native_dispatch_preparation_v2_20261008.json',")
  products.append(save(new,s))
 meta=A/'Pure149_correct_native_dispatch_preparation_v2_20261008.json'
 create(meta,{'status':'prepared_correct_native_storage_kind_dispatch_before_any149_actual_native_or_full_controls','at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'input_sha256':{str(p):sha(p) for p in [Path(__file__),*originals,*products]},'retired_only_proved_idle_original_receivers':retired,'124_cases_and_372_prefixes_and25_models_unchanged':True,'original_sources_preserved':True,'new_quality_scores':0,'test_labels_read':False})
 from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start
 rows={}
 for name,p in [('PureRFFHuber80_native_historical_calendar_controls_v2_20261008',products[0]),('PureRFFHuber124_actual_full_historical_controls_v2_20261008',products[1])]:rows[name]=start(name,p.name,[],{str(p):sha(p) for p in [Path(__file__),meta,*products]})
 create(A/'Pure149_correct_native_dispatch_hidden_launch_v2_20261008.json',rows);print({n:r['owned_worker_pid'] for n,r in rows.items()},flush=True)
if __name__=='__main__':main()
