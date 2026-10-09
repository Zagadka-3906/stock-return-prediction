"""Audit existing35 native states without claiming new replays; freeze both original kernels in fresh native80 receiver."""
from pathlib import Path
import sys,time,json
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
def main():
 planpath=A/'JointCrossHuberOrder185_round147_proposal_v1_20261008.json';plan=read(planpath)
 originals=[Path(__file__),planpath];audits=[]
 for pointer in ('actual_CrossFamily_bank30_synthetic_location_v1_20261008.json','actual_HuberCrossFamilyFine_bank15_location_v1_20261008.json'):
  p=A/pointer;v=Path(read(p)['output'])/'verification.json';originals.extend([p,v]);audits.append(read(v))
 records=[];sources=list(originals)
 for head,row in plan['heads'].items():
  sources.extend([Path(row['oof']),Path(row['folder'])/'oof_verification.json'])
  for year in range(2021,2026):
   matched=[r for audit in audits for r in audit['actual_native_replay_records'] if r['head']==head and r['year']==year]
   assert matched and all(r['full_saved_reloaded_independent_bits_exact'] for r in matched)
   infoPath=Path(row['infos'][str(year)]);info=read(infoPath);kind=row['state_kind']
   assert info['year']==year and info['last_training_label_date']<info['exclusive_cutoff']<=year*10000+101
   assert info['last_training_label_end']<=info['exclusive_cutoff']
   model=Path(info['native_model_path']);state=Path(info['independent_'+kind+'_state_path'])
   assert sha(model)==info['native_model_sha256'] and sha(state)==info['independent_'+kind+'_state_sha256']
   sources.extend([infoPath,model,state]);records.append({'head':head,'year':year,'actual_original_replay_records':matched,
    'native_model_sha256':sha(model),'independent_state_sha256':sha(state),'new_replay_claimed':False})
 assert len(records)==35 and len(plan['heads'])==7
 out=Path('E:/赛题五_本机临时/JointCrossHuber35_existing_native_evidence_v1_20261008');out.mkdir(exist_ok=False)
 proof={'status':'passed_rehashed_existing35_own_mature_saved_states_and_preserved_actual_original_replay_records',
  'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'input_sha256':{str(p):sha(p) for p in dict.fromkeys(sources)},'records':records,
  'actual_saved_model_count':35,'actual_full_OOF_heads':7,'new_native_replay_claimed':False,
  '2025_records_retain_their_original_training_sample_scope_and_never_claim_actual_future_replay':True,
  'new_native_fits':0,'new_quality_scores':0,'test_labels_read':False}
 create(out/'verification.json',proof)
 pointer=A/'actual_JointCrossHuber35_existing_native_location_v1_20261008.json';create(pointer,{'output':str(out),'verification_sha256':sha(out/'verification.json'),'new_quality_scores':0})
 old=A/'verify_JointCrossHuber80_native_historical_calendar_v1_20261008.py';s=old.read_text(encoding='utf8')
 s=s.replace('JointCrossHuber80_native_historical_calendar_v1_20261008','JointCrossHuber80_native_historical_calendar_v2_20261008').replace('actual_JointCrossHuber80_native_calendar_location_v1_20261008','actual_JointCrossHuber80_native_calendar_location_v2_20261008')
 needle='    for r in plan[\'heads\'].values():\n';assert s.count(needle)==1
 extra="""    existingPointer=A/'actual_JointCrossHuber35_existing_native_location_v1_20261008.json'
    existingPath=Path(read(existingPointer)['output'])/'verification.json';existing=read(existingPath)
    assert existing['actual_saved_model_count']==35 and existing['actual_full_OOF_heads']==7 and not existing['new_native_replay_claimed']
    for p,d in existing['input_sha256'].items():assert sha(p)==d,p
    sources.extend([existingPointer,existingPath,A/'CrossFamilyFine_complete_parent_native_stage_v1_20261008.py',
        A/'HuberCrossFamilyFine_complete_parent_native_stage_v1_20261008.py',A/'CrossFamilyFine_complete_parent_CDF_v1_20261008.py',
        A/'HuberCrossFamilyFine_complete_parent_CDF_v1_20261008.py',Path(__file__).parent/'prepare_JointCrossHuber35_reused_evidence_and_native80_v2_20261008.py'])
"""
 s=s.replace(needle,extra+needle)
 target=A/'verify_JointCrossHuber80_native_historical_calendar_v2_20261008.py';compile(s,str(target),'exec')
 with target.open('x',encoding='utf8',newline='') as f:f.write(s)
 from handoff_joint_goss_round97_full_execution_20261006 import suspended_idle
 row=read(A/'service_owned_workflows_20261006/JointCrossHuber80_native_historical_calendar_controls_v1_20261008/native_launch.json');assert owned(row)
 parent,worker,idle=suspended_idle(row,'    closed (verify_JointCrossHuber80_native_historical_calendar_v1_20261008.py:')
 try:
  worker.terminate();parent.terminate()
  import psutil
  _,alive=psutil.wait_procs([worker,parent],timeout=10);assert not alive and not owned(row)
 finally:
  for p in (worker,parent):
   if p.is_running():p.resume()
 recovery=A/'JointCrossHuber80_native_source_scope_recovery_v2_20261008.json'
 pins={str(p):sha(p) for p in [Path(__file__),old,target,pointer,out/'verification.json']}
 create(recovery,{'status':'replaced_only_proved_idle_unstarted_native80_receiver_with_both_original_kernel_sources_explicitly_frozen',
  'input_sha256':pins,'old_launch':row,'actual_idle_stack':idle,'old_native_controls_executed':0,'old_sources_preserved':True,
  'new_quality_scores':0,'test_labels_read':False})
 pins[str(recovery)]=sha(recovery)
 from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start
 r=start('JointCrossHuber80_native_historical_calendar_controls_v2_20261008',target.name,[],pins)
 create(A/'JointCrossHuber80_native_calendar_hidden_launch_v2_20261008.json',r)
 print(json.dumps({'native35_existing_evidence':'passed','new_native_replays':0,'queued_native80_worker':r['owned_worker_pid']}),flush=True)
if __name__=='__main__':main()
