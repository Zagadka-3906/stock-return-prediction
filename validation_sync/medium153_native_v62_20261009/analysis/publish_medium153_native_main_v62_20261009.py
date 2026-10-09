"""Synchronize actual149 missing-year closure and actual152 historical controls to main."""
from pathlib import Path
import sys,time,hashlib,gzip
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
def closed(n):
 f=A/'service_owned_workflows_20261006'/n
 while not (f/'service_execution.json').exists():time.sleep(10)
 while owned(read(f/'native_launch.json')):time.sleep(1)
 assert read(f/'service_execution.json')['status']=='passed',n
def main():
 jobs=['AdaptiveJointCrossHuber242_round148_full_registration_v8_20261009',
  'PureRFFHuber80_native_historical_calendar_controls_v6_20261009',
  'PureRFFHuber20_year2023_native_supplement_v2_20261009','PureRFFHuber25_all5_annual_native_coverage_v2_20261009',
  'SparseAfter14860_native_historical_calendar_controls_v2_20261009','SparseAfter14825_full_historical_controls_v2_20261009']
 for n in jobs:closed(n)
 pointers=[A/n for n in ['actual_PureRFFHuber80_native_calendar_location_v2_20261008.json',
  'actual_PureRFFHuber20_year2023_native_supplement_location_v1_20261009.json',
  'actual_SparseAfter14860_native_calendar_location_v1_20261009.json','actual_SparseAfter14825_parent148_location_v1_20261009.json']]
 proofs=[A/'Pure149_all25_annual_native_coverage_v1_20261009.json',
  A/'SparseAfter14829_synthetic25_and_state10_metadata_v1_20261009.json',
  A/'SparseAfter148152_historical_receiver_preparation_v1_20261009.json',
  A/'Pure149_all5_annual_native_receiver_binding_v8_20261009.json']
 sources=[Path(__file__),A/'lossless_chunked_safe_main_runtime_v1_20261009.py',A/'lossless_chunked_safe_main_runtime_v1_20261009.json',A/'Pure149_chunked_publication_receiver_runtime_v15_20261009.py',A/'Pure149_chunked_publication_receiver_runtime_v15_20261009.json',A/'recover_actual149152_after_chunked148_v14_20261009.py',A/'actual149152_after_chunked148_recovery_v14_20261009.json',A/'recover_actual149152_after_chunked148_v9_20261009.py',A/'actual149152_after_chunked148_recovery_v9_20261009.json',*pointers,*proofs,A/'Pure149_all5_annual_native_hidden_launches_v8_20261009.json',
  A/'Pure149_all5_annual_native_old_dispatch6_retired_v8_20261009.json',A/'SparseAfter148152_historical_hidden_launches_v1_20261009.json',
  A/'github_validation_sync_main_20261005/round148_receipt.json',A/'optimization_20261003_r148/full_registration_execution.json']
 for p in pointers:
  out=Path(read(p)['output']);v=out/'verification.json';assert sha(v)==read(p)['verification_sha256']
  proofs.append(v);sources.extend(out.glob('*.json'))
 for p in proofs:
  for f,d in read(p)['input_sha256'].items():
   assert sha(f)==d,f
   if Path(f).suffix in ('.py','.json','.md'):sources.append(Path(f))
 for pattern in ('*SparseAfter148*','*Pure149_all5*','*Pure149_all25*','*bind_Pure149_all5*'):
  sources.extend(p for p in A.glob(pattern) if p.is_file() and p.suffix in ('.py','.json'))
 for pattern in ('*publication_safe*20261009.py','*publication_safe*20261009.json','*safe_pipeline*20261009.py','*safe_pipeline*20261009.json'):
  sources.extend(p for p in A.glob(pattern) if p.is_file())
 for name in ('actual_optimization_checkpoint_v53_20261009.json','audit_actual_optimization_resources_v53_20261009.py',
  'latest_actual_optimization_progress_pointer_v54_20261009.json','SparseAfter148152_actual_prospective_scope_v3_20261009.json'):
  sources.append(A/name)
 for row in read(A/'actual_sparse150152_publication_safe_hidden_launches_v16_20261009.json').values():
  f=Path(row['script_args'][0]).parent
  sources.extend(f/p for p in ('job_definition.json','native_launch.json','verified_hidden_launch.json'))
  if (f/'service_execution.json').exists():sources.extend(f/p for p in ('service_execution.json','stdout.log','stderr.log'))
 delivery=read(A/'actual_optimization_checkpoint_v53_20261009.json')['delivered_submission']
 sources.append(Path(delivery['output'])/'submission_manifest.json')
 closed('actual_BF16_medium2048_seed09_restart_control_v1_20261009')
 neural_pointer=A/'actual_BF16_medium2048_seed09_restart_location_v1_20261009.json'
 neural_out=Path(read(neural_pointer)['output']);neural_proof=neural_out/'verification.json'
 assert sha(neural_proof)==read(neural_pointer)['verification_sha256']
 neural=read(neural_proof);assert len(neural['records'])==2
 assert all(r['all_training_losses_and_all_weight_bits_exact'] and r['preprocessing_and_native_prediction_bits_exact'] and r['actual_fixed8192_cold_prefix_bits_exact'] and r['changed_training_input_checkpoint_rejected'] for r in neural['records'])
 sources.extend([neural_pointer,neural_proof,A/'neural_BF16_medium2048_seed09_e64_frontier_v1_20261009.json',A/'neural_BF16_medium2048_seed09_e64_hidden_launches_v1_20261009.json'])
 for p,d in read(A/'neural_BF16_medium2048_seed09_e64_frontier_v1_20261009.json')['input_sha256'].items():
  assert sha(p)==d,p
  if Path(p).suffix=='.py':sources.append(Path(p))
 for p,d in neural['input_sha256'].items():
  assert sha(p)==d,p
  if Path(p).suffix in ('.py','.json'):sources.append(Path(p))
 sources.extend(p for p in neural_out.rglob('*') if p.is_file() and p.suffix in ('.json','.log'))
 for n in ('actual_BF16_medium2048_seed09_restart_control_v1_20261009','actual_BF16_medium2048_seed09_e64_bank6_v1_20261009'):
  f=A/'service_owned_workflows_20261006'/n
  sources.extend(f/p for p in ('job_definition.json','native_launch.json','verified_hidden_launch.json'))
  if n.endswith('restart_control_v1_20261009'):sources.extend(f/p for p in ('service_execution.json','stdout.log','stderr.log'))
 bank=Path('E:/赛题五_本机临时/neural_BF16_medium2048_seed09_e64_bank6_v1_20261009')
 closed('actual_BF16_medium2048_seed09_e64_bank6_v1_20261009')
 assert read(bank/'verification.json')['actual_native_fits']==6
 assert len(read(bank/'verification.json')['actual_models'])==6
 sources.append(bank/'verification.json')
 for f,d in read(bank/'verification.json')['input_sha256'].items():
  assert sha(f)==d,f
  if Path(f).suffix in ('.py','.json','.md'):sources.append(Path(f))
 sources.extend(A/n for n in ('prepare_medium153_controls_main_v60_20261009.py','medium153_controls_main_v60_receipt_20261009.json',
  'BF16Medium153_complete_native_predictor_preparation_v1_20261009.json','BF16Medium153_core_draft_preparation_v1_20261009.json'))
 sources.extend(p for p in A.glob('*BF16Medium*20261009.py') if p.is_file())
 sources.extend(p for p in A.glob('*BF16Medium*20261009.json') if p.is_file())
 for n in ('BF16Medium153_independent_full5_GPU_controls_v1_20261009','BF16Medium153_actual_native42_calendar_v1_20261009'):closed(n)
 for pointer in ('actual_BF16Medium153_full5_independent_location_v1_20261009.json','actual_BF16Medium153_native42_calendar_location_v1_20261009.json'):
  p=A/pointer;out=Path(read(p)['output']);v=out/'verification.json';assert sha(v)==read(p)['verification_sha256']
  sources.extend([p,*out.glob('*.json')])
  proof=read(v)
  if 'actual_saved_states' in proof:
   assert (proof['actual_saved_states'],proof['actual_historical_cases'],proof['actual_calendar_cases'],proof['actual_cold_cases'])==(6,30,12,42)
   assert len(proof['records'])==42 and len(proof['prefit_rejections'])==7
  else:
   assert proof['rows_days_stocks']==[5635800,1212,4650] and len(proof['records'])==5
   assert all(r['full_original_native_reload_and_independent_bits_exact'] and len(r['cold_controls'])==2 for r in proof['records'])
  for f,d in proof['input_sha256'].items():
   assert sha(f)==d,f
   if Path(f).suffix in ('.py','.json','.md'):sources.append(Path(f))
 sources.extend(A/n for n in ('prepare_medium153_sixfits_main_v61_20261009.py','medium153_sixfits_main_v61_receipt_20261009.json',
  'prepare_medium153_native_main_v62_20261009.py'))
 if (bank/'protocol.json').exists():sources.append(bank/'protocol.json')
 for info in sorted(bank.glob('*/info.json')):
  row=read(info);assert row['status']=='passed_actual_complete_mature_BF16_micro_annual_model'
  assert sha(info.parent/'model.joblib')==row['model_sha256']
  assert row['training_meta']['last_label_end']<=row['training_meta']['cutoff_exclusive']
  if int(row['year'])<2025:
   assert sha(info.parent/'raw.parquet')==row['prediction_sha256']
   assert row['actual_full_annual_reload_prediction_bits_exact'] and row['actual_cold80_prefix_bits_exact']
  sources.extend([info,info.parent/'frozen_training_inputs.json'])
 sources.extend(A/n for n in ('SparseAfter148152_static_entry_consistency_v1_20261009.json',
  'verify_SparseAfter148152_static_entry_consistency_v1_20261009.py','monitor_actual_chronological_optimization_progress_v55_20261009.py',
  'prepare_actual_neural_and_quality_progress_v55_20261009.py','actual_neural_and_quality_progress_hidden_launch_v55_20261009.json',
  'latest_actual_optimization_progress_pointer_v55_20261009.json'))

 closed('PureRFFHuber128_scores_main_publication_v1_20261008')
 closed('BF16Medium153_independent_small_CPU_v1_20261009')
 small=Path('E:/赛题五_本机临时/BF16Medium153_independent_small_CPU_v1_20261009/verification.json')
 actualsmall=read(small);assert len(actualsmall['controls'])==4
 sources.extend([small,*small.parent.glob('*.json'),Path(__file__)])
 for f,d in actualsmall['input_sha256'].items():
  assert sha(f)==d,f
  if Path(f).suffix in ('.py','.json'):sources.append(Path(f))
 for pattern in ('*BF16Medium153*20261009.py','*BF16Medium153*20261009.json','BF16Medium78*20261009.json','*actual_medium153*20261009.py','*actual_medium153*20261009.json'):
  sources.extend(p for p in A.glob(pattern) if p.is_file())
 sources.extend(A/n for n in ('monitor_actual_chronological_optimization_progress_v56_20261009.py',
  'latest_actual_optimization_progress_pointer_v56_20261009.json','neural_BF16_medium2048_seed09_independent_forward_v1_20261009.py'))
 for n in ('BF16Medium153_independent_small_CPU_v1_20261009','BF16Medium153_independent_full5_GPU_controls_v1_20261009',
  'BF16Medium153_actual_full73_training_v1_20261009','BF16Medium153_actual_native42_calendar_v1_20261009'):
  f=A/'service_owned_workflows_20261006'/n
  sources.extend(f/p for p in ('job_definition.json','native_launch.json','verified_hidden_launch.json'))
  if (f/'service_execution.json').exists():sources.extend(f/p for p in ('service_execution.json','stdout.log','stderr.log'))
 synth=read(A/'BF16Medium78_synthetic73_cold219_v1_20261009.json')
 assert (synth['actual_cases'],synth['actual_cold_cases'])==(73,219)
 for f,d in synth['input_sha256'].items():
  assert sha(f)==d,f
  if Path(f).suffix in ('.py','.json','.md'):sources.append(Path(f))
 for p in A.glob('*round148*20261009.py'):sources.append(p)
 for p in A.glob('*round148*20261009.json'):sources.append(p)
 for p in A.glob('*actual149152*20261009.py'):sources.append(p)
 for p in A.glob('*actual149152*20261009.json'):sources.append(p)
 for version in range(2,9):
  f=A/'service_owned_workflows_20261006'/f'AdaptiveJointCrossHuber242_round148_full_registration_v{version}_20261009'
  if f.is_dir():sources.extend(p for p in f.iterdir() if p.suffix in ('.json','.log'))
 for n in jobs:
  f=A/'service_owned_workflows_20261006'/n;sources.extend(p for p in f.iterdir() if p.suffix in ('.json','.log'))
 sources=list(dict.fromkeys(sources));assert all(p.is_file() for p in sources)
 coverage=read(A/'Pure149_all25_annual_native_coverage_v1_20261009.json')
 assert coverage['actual_head_year_states']==25 and coverage['actual_native_cases']==coverage['actual_cold_cases']==100
 native=read(Path(read(pointers[2])['output'])/'verification.json')
 full=read(Path(read(pointers[3])['output'])/'verification.json')
 assert (native['actual_historical_cases'],native['actual_calendar_cases'],native['actual_cold_cases'])==(48,12,60)
 assert (full['actual_stage_base_round'],full['actual_full_cases_including_identity'],full['actual_cold_cases_including_identity'])==(148,25,75)
 from handoff_joint_goss_round97_full_execution_20261006 import suspended_idle
 from verified_TLS_Git_retry_runtime_v2_20261008 import installed
 import publish_classifier_consensus_workflows_20261006 as helpers
 out=Path('E:/赛题五_本机临时/medium153_native_main_v62_20261009');out.mkdir(exist_ok=False);held=[]
 try:
  row=read(A/'service_owned_workflows_20261006/main_publisher_v9_20261009/native_launch.json');assert owned(row)
  parent,worker,idle=suspended_idle(row,'    main (watch_validations_main_v7_20261006.py:71)');held.extend((worker,parent))
  create(out/'main_watcher_idle_hold.json',{'identity':row,'stack':idle,'scientific_workers_held':0})
  sync=helpers.sync;prefix=Path('validation_sync/medium153_native_v62_20261009');payload={};bindings={}
  for source in sources:
   data=source.read_bytes();assert not sync.SECRET.search(data),source
   digest=hashlib.sha256(data).hexdigest();relative=source.relative_to(ROOT) if source.is_relative_to(ROOT) else Path('external_metadata')/(digest+'_'+source.name)
   target=(prefix/relative).as_posix();size=len(data)
   if size>=5*1024**2:data=gzip.compress(data,mtime=0);target+='.gz';assert hashlib.sha256(gzip.decompress(data)).hexdigest()==digest
   payload[target]=data;bindings[str(source)]={'published_path':target,'raw_sha256':digest,'original_bytes':size}
  payload[(prefix/'.gitattributes').as_posix()]=b'* -text\n'
  payload[(prefix/'manifest.json').as_posix()]=sync.encoded({'status':'actual_medium153_5635800_full5_independent_forecasts_10_cold_and_six_states42_native42_cold',
   'at_local':sync.now(),'files':bindings,'actual149_all5_annual_states':25,'actual149_native_controls':100,'actual149_cold_native_controls':100,
   'actual152_stage_base_round':148,'actual152_all5_annual_states':10,'actual152_native_controls':60,'actual152_cold_native_controls':60,
   'actual152_full_historical_cases':25,'actual152_full_prefix_cases':75,'actual152_official_scores':0,'actual152_future_X_read':False,'actual152_prospective_sources':32,'actual152_prospective_graph_controls':200,'actual148_delivered_submission_verified':True,'new_neural_medium_restart_controls_passed':True,'new_neural_annual_fits_not_yet_qualified':True,
   'actual_medium153_full5_independent_rows':5635800,'actual_medium153_full5_independent_cold_controls':10,'actual_medium153_saved_states':6,'actual_medium153_native_cases':42,'actual_medium153_native_cold_cases':42,'actual_medium153_prefit_calendar_rejections':7,'actual_new_medium_annual_fits_completed':6,'actual_medium153_parent_ABI_routes':5,'actual153_core_drafts_admitted':False,'actual153_synthetic_cases':73,'actual153_synthetic_cold_cases':219,'actual153_small_CPU_rows':10017,'actual153_small_CPU_prefixes':4,'actual153_complete_six_state_native_and_full_training_controls_not_yet_claimed':True,'actual153_official_scores':0,'actual153_future_X_read':False,'new_native_fits_by_publication':0,'test_labels_read':False,'primary_workspace_dirty_index_preserved':True,'search_exhaustion_claimed':False})
  create(out/'frozen_before_main_publication.json',{'files':bindings,'actual152_official_scores':0})
  with installed(out/'file_backed_git'):
   previous=sync.git('rev-parse','HEAD');helpers.verify_main(previous);assert not sync.git('status','--porcelain')
   for n,d in payload.items():sync.atomic(sync.WORKTREE/n,d)
   names=sorted(payload)
   for left in range(0,len(names),50):sync.git('add','-f','--',*names[left:left+50])
   assert set(sync.git('-c','core.quotepath=false','diff','--cached','--name-only').splitlines())==set(names)
   sync.git('-c','maintenance.auto=false','-c','gc.auto=0','commit','-m','同步153全训练期5635800独立预测及六状态42原生42冷验证',timeout=180)
   commit=sync.git('rev-parse','HEAD');hashes={n:hashlib.sha256(d).hexdigest() for n,d in payload.items()};assert helpers.blob_hashes(commit,hashes)==hashes
   sync.git('push','origin','HEAD:refs/heads/main',timeout=180);helpers.verify_main(commit);helpers.watcher.advance_source_index(commit)
   value={'status':'pushed_and_remote_head_verified','at_local':sync.now(),'branch':'main','commit':commit,'raw_git_blobs_verified':len(hashes),
    'actual149_all25_annual_states100_native100_cold':True,'actual152_native60_full25_prefix75':True,'actual152_official_scores':0,
    'url':'https://github.com/Zagadka-3906/stock-return-prediction/tree/main/'+prefix.as_posix()}
   create(out/'receipt.json',value);create(A/'medium153_native_main_v62_receipt_20261009.json',value);print(value,flush=True)
 finally:
  for p in reversed(held):
   if p.is_running():p.resume()
  create(out/'idle_publisher_resumed.json',{'held_processes':len(held),'resumed_in_finally':True,'scientific_workers_held':0})
if __name__=='__main__':
 import os
 count=int(os.environ.get('GIT_CONFIG_COUNT','0'))
 for offset,(key,value) in enumerate((('http.proxy','http://127.0.0.1:7897'),('http.version','HTTP/1.1'))):
  os.environ[f'GIT_CONFIG_KEY_{count+offset}']=key;os.environ[f'GIT_CONFIG_VALUE_{count+offset}']=value
 os.environ['GIT_CONFIG_COUNT']=str(count+2)
 from lossless_chunked_safe_main_runtime_v1_20261009 import installed as safe
 with safe(Path('E:/赛题五_本机临时/medium153_native_safe_publication_v62_20261009')):main()

