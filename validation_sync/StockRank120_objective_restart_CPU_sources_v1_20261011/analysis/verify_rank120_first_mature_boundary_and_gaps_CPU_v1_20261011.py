from pathlib import Path
import sys,math
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
def main():
 assert allowed();import polars as pl
 import recent252_rank120_mature_training_population_v2_20261011 as population
 import forward120_mature_training_labels_v2_20261011 as labels
 cfg={'target':'y_rank_120mean','label_horizon_trading_days':120,'training_calendar_window':252};records=[]
 for mode in ('complete','missing_calendar_observation','missing_label','excluded_train_observation'):
  rows=[]
  for j,stock in enumerate(('A','B','C','D')):
   for day in range(1,181):
    if mode=='missing_calendar_observation' and stock=='A' and day==30:continue
    rows.append({'ts_code':stock,'trade_date':day,'is_train':not(mode=='excluded_train_observation' and stock=='A' and day==40),'price_valid':True,'y_ret_1d':float('nan') if mode=='missing_label' and stock=='A' and day==30 else (day+j//2)/1024.})
  frame=pl.DataFrame(rows)
  for cutoff in (121,122,123):
   past=[r for r in rows if r['is_train'] and r['trade_date']<cutoff];calendar=sorted({r['trade_date'] for r in past});positions={d:i for i,d in enumerate(calendar)};raw=[]
   for stock in ('A','B','C','D'):
    own=sorted([r for r in past if r['ts_code']==stock],key=lambda r:r['trade_date'])
    for i,origin in enumerate(own):
     if i+120>=len(own):continue
     end=own[i+120]['trade_date'];values=[r['y_ret_1d'] for r in own[i:i+120]]
     if positions[end]-positions[origin['trade_date']]!=120 or not all(math.isfinite(v) for v in values):continue
     raw.append((origin['trade_date'],stock,end,math.fsum(values)/120.))
   expected=[]
   for day,stock,end,target in raw:
    values=[r[3] for r in raw if r[0]==day];rank=(sum(v<target for v in values)+(sum(v==target for v in values)+1)/2.)/len(values);expected.append((day,stock,end,target,rank))
   expected.sort();actual=population.training_frame(frame.lazy(),cutoff,cfg).select('trade_date','ts_code','label_end_120d','y_ret_120mean','y_rank_120mean').collect().rows();assert actual==expected,(mode,cutoff,actual,expected)
   poisoned=frame.with_columns(pl.when(pl.col('trade_date')>=cutoff).then(1e12).otherwise(pl.col('y_ret_1d')).alias('y_ret_1d'));assert population.training_frame(frame.lazy(),cutoff,cfg).collect().equals(population.training_frame(poisoned.lazy(),cutoff,cfg).collect())
   if cutoff==121:assert len(actual)==0
   if mode=='complete' and cutoff==122:assert len(actual)==4 and {r[0] for r in actual}=={1} and {r[2] for r in actual}=={121}
   if mode!='complete' and cutoff==122:assert len(actual)==3 and all(r[1]!='A' for r in actual)
   records.append({'case':mode,'exclusive_cutoff':cutoff,'rows':len(actual),'first_mature_boundary_and_contiguous120_observations_independent_scalar_exact':True,'future_poison_identical':True})
 proof=A/'recent252_rank120_mature_population_actual_CPU_controls_v2_20261011.json';assert len(read(proof)['records'])==7
 create(A/'rank120_first_mature_boundary_and_gaps_actual_CPU_controls_v1_20261011.json',{'status':'passed12_first_eligible122_strict121_boundary_and_calendar_missing_labels_train_gaps_scalar_oracles','records':records,'input_sha256':{str(p):sha(p) for p in [Path(__file__),Path(population.__file__),Path(labels.__file__),proof]},'new_fits':0,'new_scores':0,'test_labels_read':False})
 print({'actual_mature120_boundary_and_gap_controls':len(records)},flush=True)
if __name__=='__main__':main()
