"""Original official scoring on four qualified anchors and181 previously controlled ordered training forecasts."""
from pathlib import Path
from types import SimpleNamespace
import os,sys,time,gc,hashlib
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A),str(A/'connected_validation_20261002')]
for k in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','POLARS_MAX_THREADS'):os.environ[k]='2'
from run_dependency_queue_v3_20261006 import read,sha,create,owned
OUT=A/'PureRFFHuber128_official_comparison_v1_20261008'
STATUS='passed_actual128_PureRFFHuber_complete_parent_full_official_comparisons'
def closed(n):
 p=A/'service_owned_workflows_20261006'/n
 while not (p/'service_execution.json').exists():time.sleep(15)
 while owned(read(p/'native_launch.json')):time.sleep(1)
 assert read(p/'service_execution.json')['status']=='passed',n
def best_key(r):return (-r['connected_final_score'],r['expected_unique_native_models'],abs(r['configuration']['weight']),r['case'])
def main():
 for n in ('Pure149_prior_complete_forecast_duplicate_audit_v1_20261008','AdaptiveJointCrossHuber242_round148_full_registration_v1_20261008',
  'PureRFFHuber128_round149_source_admission_v1_20261008','PureRFFHuber128_controls_main_publication_v1_20261008'):closed(n)
 import numpy as np,polars as pl,psutil
 import PureRFFHuber_ordered_CDF_v2_20261008 as codec
 from PureRFFHuber149_storage_v1_20261008 import empty,installed_transfer,write_progress
 from score_calibrated_candidates_20261003 import score
 from official_date_index_dataframe_adapter_20261007 import installed
 from all_forecast_percentile_runtime_20261007 import installed as installed_percentile
 from cached_official_spearman_runtime_20261007 import installed as installed_ic
 from win32_read_handle_hash_cache_with_filename_v2_20261006 import LockedReadHashCache
 empty(OUT);planpath=A/'PureRFFHuber128_round149_plan_v1_20261008.json';plan=read(planpath)
 controlpath=Path(read(A/'actual_PureRFFHuber124_parent134_location_v2_20261008.json')['output'])/'verification.json';control=read(controlpath)
 assert control['actual_full_cases_including_identity']==124 and control['actual_cold_cases_including_identity']==372
 assert plan['anchor_rounds']==[145,146,147,148] and plan['fixed_scientific_stage_base_round']==134 and len(plan['new_cases'])==124
 parents={n:A/f'optimization_20261003_r{n}' for n in [134,136,*plan['anchor_rounds']]}
 baselines={n:read(p/'calibrated_csv_official.json')['metrics'] for n,p in parents.items()}
 predictions={n:read(ROOT/f'candidates/optimization_20261003_r{n}/verification.json') for n in parents}
 comparison_parent=min(plan['anchor_rounds'],key=lambda n:(-baselines[n]['final_score'],len({r['sha256'] for r in predictions[n]['models'].values()}),n))
 parent=134;graph=predictions[parent]['whole_scheme_graph'];assert codec.GRAPH_KEY not in graph
 assert 'nonflag_CPU_CrossFamily_complete_parent_CDF' not in graph and 'nonflag_CPU_HuberCrossFamily_complete_parent_CDF' not in graph
 model_sha={r['sha256'] for r in predictions[parent]['models'].values()};infos={h:read(r['infos']['2025']) for h,r in plan['heads'].items()}
 cases=[{'anchor_round':n,'model':None,'configuration':None,'role':None,'weight':0.,'universe':None} for n in plan['anchor_rounds']]
 cases.extend({'anchor_round':134,'model':'JointCrossHuber_ordered_case'+str(i),'configuration':case,'joint_control_case':i,
  'role':'nonflag_valid_2021_onward','weight':sum(abs(case[n]['amplitude']) for n in ('cross','huber')),'universe':'all_current_raw_forecasts'} for i,case in enumerate(plan['new_cases']))
 assert len(cases)==plan['expected_scored_cases']==128
 framepath=A/'connected_validation_20261002/combined_fold_frame.parquet';scoring_source=A/'optimization_20261003_r95/scoring_validation_only'
 sources=[Path(__file__),Path(codec.__file__),Path(codec.cross.__file__),Path(codec.huber.__file__),A/'PureRFFHuber149_storage_v1_20261008.py',
  planpath,controlpath,framepath,A/'PureRFFHuber128_round149_source_admission_v1_20261008.json',A/'PureRFFHuber128_controls_github_v1_20261008/receipt.json',
  A/'score_calibrated_candidates_20261003.py',A/'official_date_index_dataframe_adapter_20261007.py',A/'all_forecast_percentile_runtime_20261007.py',
  A/'cached_official_spearman_runtime_20261007.py',A/'exact_cached_official_spearman_v2_20261007.py',A/'exact_cached_validation_spearman_20261007.py',ROOT/'evaluate.py',ROOT/'后续选模标准.md',
  *[scoring_source/n for n in ('测试集_X.csv','测试集_Y.csv')],*[Path(r['oof']) for r in plan['heads'].values()],*[Path(r['infos']['2025']) for r in plan['heads'].values()]]
 for n,p in parents.items():
  assert read(p/'full_registration_execution.json')['status']=='passed'
  sources.extend(p/name for name in ('selection.json','protocol.json','selected_validation.npy','calibrated_csv_official.json','full_registration_execution.json'))
  sources.extend(ROOT/f'candidates/optimization_20261003_r{n}'/name for name in ('verification.json','manifest.json'))
  sources.append(A/f'github_validation_sync_main_20261005/round{n}_receipt.json')
 admission=read(A/'PureRFFHuber128_round149_source_admission_v1_20261008.json')
 pins={**admission['input_sha256'],**control['input_sha256'],**{str(p):sha(p) for p in sources}}
 create(OUT/'frozen_before_actual_full_controls_and_official_scores.json',{'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'input_sha256':pins,'cases':cases,
  'actual_comparison_parent_round':comparison_parent,'actual_scheme_base_round':134,'baseline_metrics':baselines,'whole_complete134_parent_preserved_before_ordered_composite':True,
  'existing_saved_native_heads':25,'new_native_fits_by_comparison':0,'selection_bias_uncorrected':True,'no_extra_Top_worst_year_or_significance_gate':True,'test_labels_read':False})
 while psutil.virtual_memory().available<8.5*2**30:time.sleep(15)
 records=[];rank_cache={};controlled={r['case']:r for r in control['records']}
 with LockedReadHashCache(pins) as scope,installed_transfer():
  frame=pl.read_parquet(framepath,columns=['ts_code','trade_date','flag_limit_up','price_valid','y_ret_1d']);assert (len(frame),frame['trade_date'].n_unique(),frame['ts_code'].n_unique())==(5635800,1212,4650)
  dates,flags,valid=[frame[n].to_numpy() for n in ('trade_date','flag_limit_up','price_valid')];assert dates.max()<20250101
  base=np.load(parents[134]/'selected_validation.npy',mmap_mode='r');arrays={h:np.load(r['oof'],mmap_mode='r') for h,r in plan['heads'].items()}
  scoring=A/'PureRFFHuber149_D_scoring_v1_20261008/comparison/scoring_validation_only';scoring.mkdir(parents=True)
  for n in ('测试集_X.csv','测试集_Y.csv'):os.link(scoring_source/n,scoring/n)
  ctx=SimpleNamespace(frame=frame,dates=dates,scoring=scoring)
  for index,cfg in enumerate(cases):
   components=[];known=None
   if cfg['model'] is None:
    values=np.asarray(np.load(parents[cfg['anchor_round']]/'selected_validation.npy',mmap_mode='r'));expected_models=len(predictions[cfg['anchor_round']]['models'])
   else:
    values=codec.transform(base,arrays,dates,flags,valid,cfg['configuration']);components=codec.required(cfg['configuration'])
    measured=controlled[cfg['joint_control_case']];assert measured['configuration']==cfg['configuration']
    numeric=hashlib.sha256(memoryview(np.ascontiguousarray(values)).cast('B')).hexdigest();assert numeric==measured['numeric_sha256']
    preserved=(dates<20210101)|(flags==1)|~valid;assert np.array_equal(values[preserved].view('u8'),np.asarray(base)[preserved].view('u8'))
    for days in (80,260,975):
     n=days*4650;cold=codec.transform(base[:n],{h:x[:n] for h,x in arrays.items()},dates[:n],flags[:n],valid[:n],cfg['configuration'])
     assert np.array_equal(values[:n].view('u8'),cold.view('u8'))
    known=measured['qualified_anchor_numeric_identity_round'];expected_models=len(model_sha|{infos[h]['native_model_sha256'] for h in components})
   write_progress(OUT/'actual_stage.json',{'status':'actual_full_official_scoring','at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'case':index,
    'configuration':cfg,'actual_completed_cases':len(records),'expected_cases':128})
   with installed_percentile() as percentile,installed_ic(rank_cache) as ic:
    with installed(scoring/'submission.csv') as adapter:metrics=score(ctx,values)
   if cfg['model'] is None:assert metrics==baselines[cfg['anchor_round']]
   if known is not None:assert metrics==baselines[known]
   capsule=Path(ctx.last_official_score_cache['official_metrics_source'])
   item={'case':index,'configuration':cfg,'metrics':metrics,'connected_final_score':metrics['final_score'],'expected_unique_native_models':expected_models,
    'score_gain_over_qualified_parent':metrics['final_score']-baselines[comparison_parent]['final_score'],'actual_comparison_parent_round':comparison_parent,'actual_scheme_base_round':134,
    'prediction_numeric_bytes_sha256':hashlib.sha256(memoryview(np.ascontiguousarray(values)).cast('B')).hexdigest(),'official_date_index_runtime':dict(adapter),
    'all_row_percentile_runtime':percentile,'scoring_only_spearman_runtime':ic,'official_score_cache':ctx.last_official_score_cache,'official_metric_capsule_sha256':sha(capsule),
    'actual_return_mapping':ctx.last_candidate_return_mapping,'whole_complete_parent_branches_preserved_before_new_stage':True,
    'invalid_and_declared_unselected_raw_bits_preserved':cfg['model'] is not None,'actual_cold80_260_975_bits_exact':cfg['model'] is not None,
    'qualified_anchor_all8_metrics_exact':cfg['model'] is None,'known_134_all8_metrics_exact':known,
    'native_bank_source':str(A/'PureRFFHuber128_actual_controls_index_v1_20261008.json'),'ordered_native_components':components,
    'first2020_identity':True,'candidate_future_freeze_replays_QA60_and_main_pending':True,'test_labels_read':False}
   create(OUT/f'case{index:03d}_official.json',item);records.append(item);print({'case':index,'score':metrics['final_score'],'gain':item['score_gain_over_qualified_parent']},flush=True)
   del values;gc.collect()
  scope.reverify()
 best=min(records,key=best_key)
 create(OUT/'verification.json',{'status':STATUS,'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'input_sha256':pins,'records':records,'best':best,
  'components':{'cross_group4':[list(m) for m,s in codec.cross.GROUPS[4]],'huber_group4':[list(m) for m,s in codec.huber.GROUPS[4]],'order_is_explicit_per_case':True},
  'actual_comparison_parent_round':comparison_parent,'actual_scheme_base_round':134,'existing_saved_native_heads':25,'new_native_fits_by_comparison':0,
  'new_quality_score_records':128,'all181_full_and543_cold_and80_native_controls_passed':True,
  'future_candidate_and_full149_qualification_pending':True,'global_feasible_direction_or_resource_exhaustion_not_established':True,'test_labels_read':False})
if __name__=='__main__':main()
