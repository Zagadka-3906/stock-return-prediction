"""All181 actual complete training OOF transforms and372 day-prefix controls; never score or infer future rows."""
from pathlib import Path
import sys,os,time,gc,json,hashlib
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
for k in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','POLARS_MAX_THREADS'):os.environ[k]='2'
from run_dependency_queue_v3_20261006 import read,sha,create,owned
OUT=Path('E:/赛题五_本机临时/PureRFFHuber124_parent134_historical_v2_20261008')
def closed(n):
 p=A/'service_owned_workflows_20261006'/n
 while not (p/'service_execution.json').exists():time.sleep(15)
 while owned(read(p/'native_launch.json')):time.sleep(1)
 assert read(p/'service_execution.json')['status']=='passed',n
def main():
 closed('PureRFFHuber80_native_historical_calendar_controls_v2_20261008')
 import numpy as np,polars as pl,psutil
 from threadpoolctl import threadpool_limits
 import PureRFFHuber_ordered_CDF_v2_20261008 as codec
 import CrossFamilyFine_complete_parent_CDF_v1_20261008 as zero_ridge_reference
 from win32_read_handle_hash_cache_with_filename_v2_20261006 import LockedReadHashCache
 def exact(x,y):assert x.dtype==y.dtype==np.float64 and x.shape==y.shape and np.array_equal(x.view('u8'),y.view('u8'))
 planpath=A/'PureRFFHuber128_round149_proposal_v1_20261008.json';plan=read(planpath);assert len(plan['new_cases'])==124
 framepath=A/'connected_validation_20261002/combined_fold_frame.parquet';basepath=A/'optimization_20261003_r134/selected_validation.npy'
 metadata=[]
 for pointer in ('actual_PureRFFHuber25_existing_native_location_v1_20261008.json','actual_PureRFFHuber124_synthetic_location_v2_20261008.json','actual_PureRFFHuber80_native_calendar_location_v2_20261008.json'):
  p=A/pointer;metadata.extend([p,Path(read(p)['output'])/'verification.json'])
 native=read(metadata[-1]);assert native['actual_historical_cases']==60 and native['actual_calendar_cases']==20 and native['actual_cold_cases']==80
 existing=read(metadata[1]);assert existing['actual_saved_model_count']==25 and not existing['new_native_replay_claimed']
 sources=[Path(__file__),A/'prepare_Pure149_correct_native_dispatch_v2_20261008.py',A/'Pure149_correct_native_dispatch_preparation_v2_20261008.json',Path(codec.__file__),Path(codec.cross.__file__),Path(codec.huber.__file__),planpath,framepath,basepath,*metadata,*[Path(r['oof']) for r in plan['heads'].values()]]
 for number in (134,):
  p=A/f'optimization_20261003_r{number}';receipt=A/f'github_validation_sync_main_20261005/round{number}_receipt.json'
  assert read(p/'full_registration_execution.json')['status']=='passed' and read(receipt)['status']=='pushed_and_remote_head_verified'
  sources.extend([p/'selected_validation.npy',p/'full_registration_execution.json',p/'calibrated_csv_official.json',receipt])
 reference_plan=read(A/'AdaptiveJointCrossHuber242_round148_proposal_v1_20261008.json');reference_paths={h:Path(reference_plan['heads'][h]['oof']) for h in ('ridge_l001','ridge_l025')}
 sources += [Path(zero_ridge_reference.__file__),A/'AdaptiveJointCrossHuber242_round148_proposal_v1_20261008.json',*reference_paths.values()]
 pins={str(p):sha(p) for p in dict.fromkeys(sources)};OUT.mkdir(exist_ok=False)
 execution=sorted(range(124),key=lambda i:(tuple(plan['new_cases'][i]['order']),json.dumps(plan['new_cases'][i][plan['new_cases'][i]['order'][0]],sort_keys=True),i))
 create(OUT/'frozen_before_actual124_full_controls.json',{'input_sha256':pins,'actual_stage_base_round':134,'execution_case_indices':execution,
  'identical_first_stage_cache_changes_neither_case_parameters_nor_case_numbers':True,'expected_full_controls':124,'expected_cold_controls':372,
  'new_native_fits':0,'new_quality_scores':0,'actual_future_X_and_labels_read':False})
 while psutil.virtual_memory().available<8*2**30:time.sleep(15)
 records=[];known=[];tick=time.perf_counter()
 with LockedReadHashCache(pins) as scope,threadpool_limits(limits=2):
  frame=pl.read_parquet(framepath,columns=['ts_code','trade_date','flag_limit_up','price_valid']);assert (len(frame),frame['trade_date'].n_unique(),frame['ts_code'].n_unique())==(5635800,1212,4650)
  dates,flags,valid=[frame[k].to_numpy() for k in ('trade_date','flag_limit_up','price_valid')];assert dates.max()<20250101
  base=np.load(basepath,mmap_mode='r');assert base.dtype==np.float64 and base.shape==(5635800,)
  raw={h:np.load(r['oof'],mmap_mode='r') for h,r in plan['heads'].items()};assert all(x.dtype==np.float64 and x.shape==base.shape for x in raw.values())
  reference_raw={**raw,**{h:np.load(p,mmap_mode='r') for h,p in reference_paths.items()}}
  reference_residual=zero_ridge_reference.independent_mixture(reference_raw,4,0.)
  residuals={(name,share):codec.CODECS[name].mixture(raw,4,share) for name in ('cross','huber') for share in sorted({case[name]['share'] for case in plan['new_cases'] if case[name]['amplitude']})}
  independent={(name,share):codec.CODECS[name].independent_mixture(raw,4,share) for name in ('cross','huber') for share in sorted({case[name]['share'] for case in plan['new_cases'] if case[name]['amplitude']})}
  for key,r in residuals.items():exact(r,independent[key])
  preserved=(dates<20210101)|(flags==1)|~valid;current_key=None;first=oracle_first=prepared=None
  for index in execution:
   case=plan['new_cases'][index];name1,name2=case['order'];c1,c2=case[name1],case[name2];key=(name1,c1['share'],c1['amplitude'])
   if key!=current_key:
    if c1['amplitude']:
     first=codec.CODECS[name1].transform(base,residuals[(name1,c1['share'])],dates,flags,valid,c1['amplitude'])
     oracle_first=codec.CODECS[name1].pandas_oracle(base,independent[(name1,c1['share'])],dates,flags,valid,c1['amplitude'])
     exact(first,oracle_first)
    else:first=oracle_first=np.asarray(base)
    prepared=codec.CODECS[name2].prepare(first,dates);current_key=key
   if c2['amplitude']:
    value=codec.CODECS[name2].apply_prepared(first,residuals[(name2,c2['share'])],dates,flags,valid,c2['amplitude'],prepared)
    oracle=codec.CODECS[name2].pandas_oracle(oracle_first,independent[(name2,c2['share'])],dates,flags,valid,c2['amplitude']);exact(value,oracle);del oracle
   else:value=np.array(first,dtype=np.float64,copy=True)
   exact(value[preserved],np.asarray(base)[preserved])
   reference=np.array(base,dtype=np.float64,copy=True)
   for stage in case['order']:
    cfg=case[stage]
    if not cfg['amplitude']:continue
    module=zero_ridge_reference if stage=='cross' else codec.huber
    residual=reference_residual if stage=='cross' else independent[('huber',cfg['share'])]
    reference=module.pandas_oracle(reference,residual,dates,flags,valid,cfg['amplitude'])
   exact(value,reference);del reference
   cold=[]
   for days in (80,260,975):
    n=days*4650;assert dates[n]!=dates[n-1];r={h:x[:n] for h,x in raw.items()}
    exact(codec.transform(base[:n],r,dates[:n],flags[:n],valid[:n],case),value[:n])
    exact(codec.pandas_oracle(base[:n],r,dates[:n],flags[:n],valid[:n],case),value[:n])
    cold.append({'days':days,'rows':n,'two_stage_native_arithmetic_and_independent_Pandas_bits_exact':True})
   anchor=None
   fixed={'group':4,'share':.5,'amplitude':.0025}
   if not c1['amplitude'] and not c2['amplitude']:anchor=134
   elif case['order']==['cross','huber'] and case['cross']==fixed and not case['huber']['amplitude']:anchor=136
   elif case['order']==['cross','huber'] and case['cross']==case['huber']==fixed:anchor=139
   if anchor is not None:
    original=np.load(A/f'optimization_20261003_r{anchor}/selected_validation.npy',mmap_mode='r');exact(value,np.asarray(original));known.append({'case':index,'actual_qualified_round':anchor,'full5635800_numeric_bits_exact':True})
   row={'case':index,'configuration':case,'rows':len(value),'primary_full_independent_bits_exact':True,
    'preserved2020_limit_up_invalid_bits_exact':True,'numeric_sha256':hashlib.sha256(memoryview(np.ascontiguousarray(value)).cast('B')).hexdigest(),
    'cold_controls':cold,'qualified_anchor_numeric_identity_round':anchor,'ordered_native_heads':codec.required(case)}
   create(OUT/f'case{index:03d}.json',row);records.append(row);del value;gc.collect();print(json.dumps({'actual_full_controls':len(records),'expected':124,'case':index}),flush=True)
  scope.reverify()
 records.sort(key=lambda r:r['case']);assert len(records)==124 and sum(len(r['cold_controls']) for r in records)==372
 assert {r['actual_qualified_round'] for r in known}=={134}
 create(OUT/'verification.json',{'status':'passed_actual124_full_ordered_joint_CDF_and372_cold_controls_with_exact134_136_139_numeric_identities',
  'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'input_sha256':pins,'records':records,'actual_stage_base_round':134,
  'actual_full_cases_including_identity':124,'actual_cold_cases_including_identity':372,'known_qualified_numeric_identities':known,
  'actual124_full_zero_Ridge_reference_forecast_bits_equal':True,'existing25_saved_native_models_reused_not_new_fits':True,'elapsed_seconds':time.perf_counter()-tick,
  'new_native_fits':0,'new_quality_scores':0,'actual_future_X_and_labels_read':False,'all128_quality_and149_freeze_inference_complete_board_main_still_required':True})
 create(A/'actual_PureRFFHuber124_parent134_location_v2_20261008.json',{'output':str(OUT),'verification_sha256':sha(OUT/'verification.json'),'new_quality_scores':0})
if __name__=='__main__':main()
