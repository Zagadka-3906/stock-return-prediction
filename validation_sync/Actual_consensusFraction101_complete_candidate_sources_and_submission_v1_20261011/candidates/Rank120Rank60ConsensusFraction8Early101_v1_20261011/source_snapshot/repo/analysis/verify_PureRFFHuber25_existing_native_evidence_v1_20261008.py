"""Rehash the own25 mature saved states and original replay records; never claim a new native replay."""
from pathlib import Path
import sys,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
def main():
 proposal=A/'PureRFFHuber128_round149_proposal_v1_20261008.json';plan=read(proposal);assert len(plan['heads'])==5
 pointer=A/'actual_JointCrossHuber35_existing_native_location_v1_20261008.json';original=Path(read(pointer)['output'])/'verification.json';bank=read(original)
 assert bank['actual_saved_model_count']==35 and not bank['new_native_replay_claimed']
 for p,d in bank['input_sha256'].items():assert sha(p)==d,p
 relevant=[r for r in bank['records'] if r['head'] in plan['heads']]
 assert len(relevant)==25 and {(r['head'],r['year']) for r in relevant}=={(h,y) for h in plan['heads'] for y in range(2021,2026)}
 inputs=[Path(__file__),proposal,pointer,original];records=[]
 for head,row in plan['heads'].items():
  inputs.extend([Path(row['oof']),Path(row['folder'])/'oof_verification.json'])
  for year in range(2021,2026):
   p=Path(row['infos'][str(year)]);info=read(p);kind=row['state_kind']
   assert info['year']==year and info['last_training_label_date']<info['exclusive_cutoff']<=year*10000+101
   assert info['last_training_label_end']<=info['exclusive_cutoff']
   state=Path(info['native_model_path']);decoded=Path(info['independent_'+kind+'_state_path'])
   assert sha(state)==info['native_model_sha256'] and sha(decoded)==info['independent_'+kind+'_state_sha256']
   old=next(r for r in relevant if r['head']==head and r['year']==year)
   records.append({'head':head,'year':year,'info_sha256':sha(p),'native_model_sha256':info['native_model_sha256'],
    'independent_state_sha256':info['independent_'+kind+'_state_sha256'],'original_actual_replay_record_preserved':old,
    'own_mature_saved_state_rehashed':True,'new_native_replay_claimed':False})
   inputs.extend([p,state,decoded])
 pins={str(p):sha(p) for p in dict.fromkeys(inputs)};out=Path('E:/赛题五_本机临时/PureRFFHuber25_existing_native_evidence_v1_20261008');out.mkdir(exist_ok=False)
 create(out/'verification.json',{'status':'passed_rehashed_own25_mature_saved_states_and_original_replay_records_not_new_native_replays',
  'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'input_sha256':pins,'records':records,'actual_saved_model_count':25,'actual_full_OOF_heads':5,
  'original_2025_training_sample_scope_retained_not_actual_future_replay':True,'new_native_replay_claimed':False,'new_native_fits':0,
  'new_quality_scores':0,'test_labels_read':False})
 create(A/'actual_PureRFFHuber25_existing_native_location_v1_20261008.json',{'output':str(out),'verification_sha256':sha(out/'verification.json'),'new_quality_scores':0})
 print('Own25 mature saved states and original records rehashed; no new native replay claimed.',flush=True)
if __name__=='__main__':main()
