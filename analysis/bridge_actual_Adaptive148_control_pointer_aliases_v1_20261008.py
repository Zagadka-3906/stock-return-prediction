"""Bind unused legacy metadata pointers to actual newly verified control outputs, without changing failed service statuses."""
from pathlib import Path
import sys,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
def main():
 rows=[]
 for actual,legacy in [('actual_AdaptiveJointCrossHuber80_native_calendar_location_v3_20261008.json','actual_AdaptiveJointCrossHuber80_native_calendar_location_v2_20261008.json'),('actual_AdaptiveJointCrossHuber238_parent134_location_v3_20261008.json','actual_AdaptiveJointCrossHuber238_parent134_location_v2_20261008.json')]:
  p=A/actual
  while not p.is_file():time.sleep(.5)
  value=read(p);proof=Path(value['output'])/'verification.json';assert sha(proof)==value['verification_sha256']
  q=A/legacy;assert not q.exists();create(q,value)
  rows.append({'actual_pointer':str(p),'unused_legacy_metadata_alias':str(q),'actual_output':value['output'],'verification_sha256':sha(proof),'failed_old_service_status_unchanged':True})
 create(A/'actual_Adaptive148_control_pointer_aliases_v1_20261008.json',{'status':'passed_metadata_pointer_aliases_to_actual_retry_controls','at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'input_sha256':{str(Path(__file__)):sha(__file__)},'bindings':rows,'new_quality_scores':0,'test_labels_read':False})
if __name__=='__main__':main()
