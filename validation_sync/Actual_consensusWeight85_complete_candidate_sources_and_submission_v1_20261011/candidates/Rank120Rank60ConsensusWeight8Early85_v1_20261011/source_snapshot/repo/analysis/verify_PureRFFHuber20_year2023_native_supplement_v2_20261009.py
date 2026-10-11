"""Sixty joint historical saved-model controls plus twenty final-model multiyear calendar controls."""
from pathlib import Path
from types import SimpleNamespace
import sys,os,time,itertools,json
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
for k in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','POLARS_MAX_THREADS'):os.environ[k]='2'
from run_dependency_queue_v3_20261006 import read,sha,create,owned
OUT=Path('E:/赛题五_本机临时/PureRFFHuber20_year2023_native_supplement_v1_20261009')
def closed(n):
 p=A/'service_owned_workflows_20261006'/n
 while not (p/'service_execution.json').exists():time.sleep(15)
 while owned(read(p/'native_launch.json')):time.sleep(1)
 assert read(p/'service_execution.json')['status']=='passed',n
def main():
 closed('AdaptiveJointCrossHuber242_round148_full_registration_v4_20261009')
 closed('PureRFFHuber80_native_historical_calendar_controls_v5_20261009')
 closed('PureRFFHuber124_actual_synthetic_controls_v2_20261008')
 import numpy as np,polars as pl,psutil
 from run import FEATURE_FILE,feature_names
 import PureRFFHuber_ordered_CDF_v2_20261008 as codec
 from PureRFFHuber_ordered_native_stage_v2_20261008 import after_parent,GRAPH_KEY,exact
 while psutil.virtual_memory().available<8*2**30:time.sleep(15)
 planpath=A/'PureRFFHuber128_round149_proposal_v1_20261008.json';plan=read(planpath)
 framepath=A/'connected_validation_20261002/combined_fold_frame.parquet'
 teacherpath=A/'optimization_20261003_r106/selected_validation.npy';parentpath=A/'optimization_20261003_r134/selected_validation.npy'
 sources=[A/'prepare_PureRFFHuber149_native80_and_full124_v1_20261008.py',A/'PureRFFHuber149_real_control_preparation_v1_20261008.json',A/'PureRFFMean_complete_parent_CDF_v1_20261008.py',A/'PureRFFMean_complete_parent_native_stage_v1_20261008.py',Path(__file__),Path(codec.__file__),A/'PureRFFHuber_ordered_native_stage_v2_20261008.py',planpath,framepath,FEATURE_FILE,teacherpath,parentpath]
 existingPointer=A/'actual_PureRFFHuber25_existing_native_location_v1_20261008.json'
 existingPath=Path(read(existingPointer)['output'])/'verification.json';existing=read(existingPath)
 assert existing['actual_saved_model_count']==25 and existing['actual_full_OOF_heads']==5 and not existing['new_native_replay_claimed']
 for p,d in existing['input_sha256'].items():assert sha(p)==d,p
 sources.extend([existingPointer,existingPath,A/'CrossFamilyFine_complete_parent_native_stage_v1_20261008.py',
     A/'HuberCrossFamilyFine_complete_parent_native_stage_v1_20261008.py',A/'CrossFamilyFine_complete_parent_CDF_v1_20261008.py',
     A/'HuberCrossFamilyFine_complete_parent_CDF_v1_20261008.py',Path(__file__).parent/'prepare_JointCrossHuber35_reused_evidence_and_native80_v2_20261008.py'])
 for r in plan['heads'].values():
  sources.append(Path(r['oof']))
  for year in (2023,):
   p=Path(r['infos'][str(year)]);info=read(p);sources.extend([p,Path(info['native_model_path']),Path(info['independent_'+r['state_kind']+'_state_path'])])
 pins={str(p):sha(p) for p in dict.fromkeys(sources)};OUT.mkdir(exist_ok=False)
 create(OUT/'frozen_before_actual20_year2023_controls.json',{'input_sha256':pins,'historical_years':[2023],
  'actual_remapped_final_model_calendar_years':[],'historical_cases':20,'calendar_cases':0,
  'each_case_full3days_or_multiyear2days_and_cold1day':True,'actual_future_X_or_labels_read':False,'new_native_fits':0,'new_quality_scores':0})
 names=feature_names();keys=['ts_code','trade_date'];frame=pl.read_parquet(framepath,columns=keys+['flag_limit_up','price_valid']);dates=frame['trade_date'].to_numpy()
 teacher=np.load(teacherpath,mmap_mode='r');base=np.load(parentpath,mmap_mode='r');oof={h:np.load(r['oof'],mmap_mode='r') for h,r in plan['heads'].items()}
 zc={'group':4,'share':0.,'amplitude':0.};zh={'group':4,'share':.5,'amplitude':0.}
 settings=[({'group':4,'share':0.,'amplitude':cw},{'group':4,'share':hs,'amplitude':hw}) for hs in (.375,.5,.625) for cw,hw in ((.001,.00325),(.00325,.001))]
 settings += [({'group':4,'share':0.,'amplitude':w},zh) for w in (.001,.00325)]
 settings += [(zc,{'group':4,'share':.5,'amplitude':w}) for w in (.001,.00325)]
 cases=[{'order':order,'cross':c,'huber':h} for order in (['cross','huber'],['huber','cross']) for c,h in settings]
 assert len({json.dumps(c,sort_keys=True) for c in cases})==20
 assert len(cases)==20
 def components(case,year):
  result=[]
  for h in codec.required(case):
   row=plan['heads'][h];info=read(row['infos'][str(year)]);kind=row.get('native_stage_state_kind',row['state_kind']);storage_kind=row['state_kind']
   result.append({'head':h,'name':info['name'],'state_kind':kind,'path':info['native_model_path'],'sha256':info['native_model_sha256'],
    'independent_state_path':info['independent_'+storage_kind+'_state_path'],'independent_state_sha256':info['independent_'+storage_kind+'_state_sha256'],'training_info':info})
  return result
 def spec(case):return {'configuration':case,'original_complete_parent_round':134,'universe':'all_current_raw_forecasts',
  'position':'ordered_composite_after_complete_qualified134_parent','teacher_feature':'qualified106_current_forecast_average_rank_over_N'}
 records=[]
 for year in (2023,):
  days=np.unique(dates[dates//10000==year])[:3];pos=np.flatnonzero(np.isin(dates,days));panel=frame[pos]
  test=pl.scan_parquet(FEATURE_FILE).filter(pl.col('is_train')&pl.col('trade_date').is_in(days)).select(keys+names).sort('trade_date','ts_code').collect()
  assert test.select(keys).equals(panel.select(keys)) and len(pos)==13950 and not {'y_rank','y_ret_1d'}&set(test.columns)
  t=np.asarray(teacher[pos],dtype=np.float64);p=np.asarray(base[pos],dtype=np.float64);raw={h:x[pos] for h,x in oof.items()}
  for case in cases:
   s=spec(case);ctx=SimpleNamespace(dates=panel['trade_date'].to_numpy(),flags=panel['flag_limit_up'].to_numpy(),valid=panel['price_valid'].to_numpy(),
    _nonflag_raw_features=test.select(names).to_numpy().astype(np.float64),_nonflag_raw_feature_names=names,_whole_graph={GRAPH_KEY:s})
   value,report=after_parent(SimpleNamespace(sha=sha,read=read),ctx,t,p,s,components(case,year))
   exact(value,codec.transform(p,raw,ctx.dates,ctx.flags,ctx.valid,case));exact(value,codec.pandas_oracle(p,raw,ctx.dates,ctx.flags,ctx.valid,case))
   cold=SimpleNamespace(**vars(ctx))
   for field in ('dates','flags','valid','_nonflag_raw_features'):setattr(cold,field,getattr(ctx,field)[:4650])
   prefix,coldreport=after_parent(SimpleNamespace(sha=sha,read=read),cold,t[:4650],p[:4650],s,components(case,year));exact(prefix,value[:4650])
   row={'mode':'own_historical_model','year':year,'configuration':case,'full':report,'cold':coldreport,'saved_OOF_and_native_bits_exact':True}
   create(OUT/f'control{len(records):03d}.json',row);records.append(row);print(json.dumps({'controls':len(records),'expected':20,'year':year}),flush=True)
 assert len(records)==20
 for f,d in pins.items():assert sha(f)==d,f
 create(OUT/'verification.json',{'status':'passed_actual20_own2023_native_reload_independent_OOF_and20_cold_supplement',
  'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'input_sha256':pins,'records':records,'actual_historical_cases':20,'actual_calendar_cases':0,'actual_cold_cases':20,
  'actual_prefit_final_model_date_rejections':0,'new_native_fits':0,'new_quality_scores':0,'actual_future_X_and_labels_read':False})
 create(A/'actual_PureRFFHuber20_year2023_native_supplement_location_v1_20261009.json',{'output':str(OUT),'verification_sha256':sha(OUT/'verification.json'),'new_quality_scores':0})
if __name__=='__main__':main()
