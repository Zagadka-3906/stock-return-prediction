"""Exercise all181 ordered configurations, ties, identity, protected cohorts and543 day-prefix controls."""
from pathlib import Path
import sys,time,hashlib,json
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
def main():
 import numpy as np
 import JointCrossHuber_ordered_CDF_v1_20261008 as codec
 planpath=A/'JointCrossHuberOrder185_round147_proposal_v1_20261008.json';plan=read(planpath)
 assert len(plan['new_cases'])==181 and len(plan['heads'])==7
 pins={str(p):sha(p) for p in [Path(__file__),Path(codec.__file__),planpath,Path(codec.cross.__file__),Path(codec.huber.__file__)]}
 out=Path('E:/赛题五_本机临时/JointCrossHuber181_synthetic_v1_20261008');out.mkdir(exist_ok=False)
 create(out/'frozen_before_actual_controls.json',{'input_sha256':pins,'declared_cases':181,'new_quality_scores':0,'test_labels_read':False})
 def exact(x,y):
  assert x.dtype==y.dtype==np.float64 and x.shape==y.shape and np.array_equal(x.view('u8'),y.view('u8'))
 rng=np.random.default_rng(20261008);dates=np.repeat(np.array([20201230,20210104,20210105,20210106]),37)
 base=np.round(rng.normal(size=len(dates)),1);flags=(rng.random(len(base))<.2).astype(int);valid=rng.random(len(base))>.2;base[~valid]=-1e6
 raw={h:rng.normal(size=len(base)) for h in plan['heads']};preserved=(dates<20210101)|(flags==1)|~valid
 records=[];ordered_pairs={}
 for index,case in enumerate(plan['new_cases']):
  value=codec.transform(base,raw,dates,flags,valid,case);exact(value,codec.pandas_oracle(base,raw,dates,flags,valid,case));exact(value[preserved],base[preserved])
  if not any(case[n]['amplitude'] for n in ('cross','huber')):exact(value,base)
  for days in (1,2,3):
   n=days*37;cold={h:a[:n] for h,a in raw.items()}
   exact(codec.transform(base[:n],cold,dates[:n],flags[:n],valid[:n],case),value[:n])
   exact(codec.pandas_oracle(base[:n],cold,dates[:n],flags[:n],valid[:n],case),value[:n])
  heads=codec.required(case);assert len(heads)==(7 if all(case[n]['amplitude'] for n in ('cross','huber')) else (4 if case['cross']['amplitude'] else (3 if case['huber']['amplitude'] else 0)))
  digest=hashlib.sha256(memoryview(value).cast('B')).hexdigest()
  records.append({'case':index,'configuration':case,'numeric_sha256':digest,'protected_and_independent_full_bits_exact':True,'cold_days':[1,2,3],'heads':heads})
  if all(case[n]['amplitude'] for n in ('cross','huber')):
   key=json.dumps({n:case[n] for n in ('cross','huber')},sort_keys=True);ordered_pairs.setdefault(key,{})[','.join(case['order'])]=digest
 assert len(records)==181 and len(ordered_pairs)==81 and all(len(v)==2 for v in ordered_pairs.values())
 for p,d in pins.items():assert sha(p)==d,p
 create(out/'verification.json',{'status':'passed_actual181_ordered_tied_identity_and_preserved_cohort_synthetic_controls_and543_cold_controls',
  'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'input_sha256':pins,'records':records,'actual_cases':181,'actual_cold_cases':543,
  'actual_double_stage_order_pairs':81,'actual_order_pairs_with_distinct_numeric_bits':sum(len(set(v.values()))==2 for v in ordered_pairs.values()),
  'historical_full_rows_or_native_saved_model_replays_not_claimed_by_synthetic_controls':True,
  'new_model_fits':0,'new_quality_scores':0,'test_labels_read':False})
 create(A/'actual_JointCrossHuber181_synthetic_location_v1_20261008.json',{'output':str(out),'verification_sha256':sha(out/'verification.json'),'new_quality_scores':0})
 print(json.dumps({'actual_cases':181,'cold_cases':543,'order_pairs_distinct_bits':sum(len(set(v.values()))==2 for v in ordered_pairs.values())}),flush=True)
if __name__=='__main__':main()
