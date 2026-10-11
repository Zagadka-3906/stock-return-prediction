"""Predeclare both capacity ensembles' complete inference gates; train-only gain selection."""
from pathlib import Path
import sys,ast
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
from start_fast_completed_owned_service_v1_20261011 import start_service
TEMPLATES=['normalize_rank120_rank60_best_blend_fraction38_early_v1_20261011.py',
 'qualify_rank120_rank60_best_blend_fraction38_early_selected_native14_v2_20261011.py',
 'prepare_Rank120Rank60BestBlend38Early_selected_candidate_v2_20261011.py',
 'run_Rank120Rank60BestBlend38Early_selected_candidate_feature_cache_v2_20261011.py',
 'seal_Rank120Rank60BestBlend38Early_selected_candidate_v2_20261011.py',
 'rank120_rank60_best_blend_fraction38_early_storage_v1_20261011.py']
def transform(s,mode,count):
 low='rank60_two_capacity_'+mode+str(count)+'_early'
 title='Rank60TwoCapacity'+mode.title()+str(count)+'Early'
 s=s.replace('rank120_rank60_best_blend_fraction38_early',low).replace('Rank120Rank60BestBlend38Early',title)
 s=s.replace('60与120日最佳组合38项提前完整候选','60日大小网络'+mode+str(count)+'项提前完整候选')
 s=s.replace('rank120_rank60_protected','rank60_two_capacity_'+mode)
 s=s.replace('rank120_weight','medium_weight')
 for old,new in [('pilot38.json','pilot'+str(count)+'.json'),('normalized38_actual','normalized'+str(count)+'_actual'),('actual38_capsules','actual'+str(count)+'_capsules'),('selected_by_all38','selected_by_all'+str(count)),('actual_all38','actual_all'+str(count))]:s=s.replace(old,new)
 s=s.replace("len(pilot['records'])==38","len(pilot['records'])=="+str(count))
 s=s.replace("len(proof['records'])==proof['new_quality_score_records']==38","len(proof['records'])==proof['new_quality_score_records']=="+str(count))
 s=s.replace('(37,111)',repr((count-1,3*(count-1))))
 s=s.replace("'expected_scored_records':38","'expected_scored_records':"+str(count)).replace('expected_scored_records=38','expected_scored_records='+str(count)).replace("'scored_records':38","'scored_records':"+str(count))
 s=s.replace("'actual_nonidentity_full_controls':37","'actual_nonidentity_full_controls':"+str(count-1)).replace("'actual_nonidentity_prefix_controls':111","'actual_nonidentity_prefix_controls':"+str(3*(count-1)))
 s=s.replace('stock_rank120_embedding_small512_BF16_bank6_v1_20261011','stock_rank60medium_embedding_medium2048_BF16_bank6_v1_20261011')
 s=s.replace('actual_StockRank120EmbeddingSmall512_full5_independent_location_v1_20261011.json','actual_StockRank60MediumEmbeddingMedium2048_full5_independent_location_v1_20261011.json')
 return s
def save(p,s):
 ast.parse(s);assert not p.exists(),p;p.write_text(s,encoding='utf8');return p
def main():
 assert allowed()
 for mode,count,producer in [('protected',109,'actual_rank60_two_capacity_after183_protected109_screen_v3_20261011'),('CDF',49,'actual_rank60_two_capacity_after183_CDF49_screen_v1_20261011')]:
  low='rank60_two_capacity_'+mode+str(count)+'_early';title='Rank60TwoCapacity'+mode.title()+str(count)+'Early'
  proofname=low+'_sources_admission_v2_20261011.json';outputs=[]
  for name in TEMPLATES:
   s=transform((A/name).read_text(encoding='utf8'),mode,count)
   if name.startswith('normalize_'):
    s=s.replace('actual_rank120_rank60_after183_best_blend_fraction38_screen_v1_20261011',producer)
    s=s.replace('StockRank120Rank60_after183_best_blend_fraction38_screen_v1_20261011','StockRank60TwoCapacity_after183_'+mode+str(count)+'_screen_v1_20261011')
    begin=s.index(' for horizon in (60,120):');end=s.index('\n records=[]',begin)
    s=s[:begin]+''' for width,bankname in [(512,'stock_rank60_embedding_small512_BF16_bank6_v1_20261011'),(2048,'stock_rank60medium_embedding_medium2048_BF16_bank6_v1_20261011')]:
  bank=Path('E:/赛题五_本机临时')/bankname;info=read(bank/'2025/info.json')
  assert read(bank/'verification.json')['actual_native_fits']==6 and info['configuration']['seed']==20261009
  assert info['configuration']['label_horizon_trading_days']==60 and info['configuration']['training_calendar_window']==252
  assert info['configuration']['hidden']==([512,256,128] if width==512 else [2048,1024,512])
  leaves.append({'name':f'rank_MLP{width}_StockEmbedding16_Cross120Recent252Rank60Mean_seed09_e64','bank':str(bank),'sha256':info['model_sha256'],'label_horizon_trading_days':60,'training_calendar_window':252})
  for year in range(2020,2026):
   for n in ('info.json','model.joblib'):p=bank/str(year)/n;pins[str(p)]=sha(p)
'''+s[end:]
   if name.startswith('qualify_'):
    s=s.replace('actual_rank60_two_capacity_'+mode+'_twelve_callbacks_CPU_v1_20261011','actual_rank60_two_capacity_'+mode+'_twelve_parent_callbacks_CPU_v1_20261011')
   if name.startswith('run_'):
    s=s.replace('    assert allowed();closed(',"    closed('actual_rank60medium2048_gain_selected_full_candidate_queue_v1_20261011')\n    assert allowed();closed(",1)
   if mode=='CDF':
    s=s.replace("'kind']=='valid_pool_protection_v1'","'kind']=='CDF'")
   outputs.append(save(A/transform(name,mode,count),s))
  proof=A/proofname
  create(proof,{'status':'predeclared_gaining_capacity_ensemble_complete37_physical_model_candidate_all_official_TRAIN_records_required',
   'input_sha256':{str(p):sha(p) for p in [Path(__file__),*[A/n for n in TEMPLATES],*outputs,
    A/('rank60_two_capacity_'+mode+'_after_qualified183_native_stage_v1_20261011.py'),
    A/('predict_rank60_two_capacity_'+mode+'_complete_qualified183_scheme_v1_20261011.py')]},
   'expected_source_quality_records':count,'full_controls':count-1,'prefix_controls':3*(count-1),'physical_models_if_selected':37,
   'actual_native14_and_full_candidate_execution_pending':True,'new_fits':0,'new_scores':0,'test_labels_read':False})
  jobs=[('actual_'+low+'_normalization_v1_20261011',outputs[0].name),('actual_'+low+'_selected_native14_v1_20261011',outputs[1].name),
    (title+'_selected_candidate_preparation_v1_20261011',outputs[3].name),(title+'_selected_candidate_sealing_v1_20261011',outputs[4].name)]
  queue=A/('run_'+low+'_gaining_candidate_queue_v1_20261011.py')
  script='''from pathlib import Path
import sys,importlib
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed,closed
from start_fast_completed_owned_service_v1_20261011 import start_service
from run_protected167_complete_family_v1_20261010 import junction
def dispatch(name,driver):
 assert allowed();p=A/driver;r=start_service(name,driver,[],{str(p):sha(p),str(A/PROOF):sha(A/PROOF)})
 create(A/(name+'_activation.json'),r);closed(name)
def main():
 assert allowed();closed(PRODUCER)
 jobs=JOBS;dispatch(*jobs[0]);pilot=read(Path(read(A/POINTER)['output'])/PILOT)
 best=pilot['best'];references=[]
 for n in ['alternate_verified_best_blend38_submission_delivery_v1_20261011.json','alternate_verified_rank60medium2048_best33_submission_delivery_v1_20261011.json']:
  p=A/n
  if p.exists():
   v=read(p);assert v['all_full_native_independent_reload_csv_and_cold80_checks_passed'];references.append({'pointer':str(p),'sha256':sha(p),'S':v['official_TRAIN_internal_score']})
 assert references;incumbent=max(r['S'] for r in references);adopt=best['connected_final_score']>incumbent
 create(A/DECISION,{'status':'actual_all_source_TRAIN_scores_vs_current_completed_candidate_S_only','adopt':adopt,'best':best,'incumbent_S':incumbent,'references':references,'test_labels_read':False})
 if not adopt:
  print('All official records retained; selected S below completed candidate, no full inference.',flush=True);return
 storage=importlib.import_module(STORAGE)
 for logical,physical in storage.OUTPUTS.items():
  assert not logical.exists() and not physical.exists();physical.mkdir(parents=True);logical.parent.mkdir(parents=True,exist_ok=True);junction(logical,physical)
 for job in jobs[1:]:dispatch(*job)
 print('Actual gaining ensemble full37-model candidate sealed; main/delivery still required.',flush=True)
if __name__=='__main__':main()
'''
  for token,value in [('PROOF',proofname),('PRODUCER',producer),('POINTER','actual_'+low+'_normalized_location_v1_20261011.json'),('PILOT','pilot'+str(count)+'.json'),('DECISION',low+'_gain_decision_v1_20261011.json'),('STORAGE',outputs[5].stem)]:script=script.replace(token,repr(value))
  script=script.replace('JOBS',repr(jobs));save(queue,script)
  name='actual_'+low+'_gaining_candidate_queue_v1_20261011'
  r=start_service(name,queue.name,[],{str(queue):sha(queue),str(proof):sha(proof)})
  create(A/(name+'_activation.json'),r)
 print({'109_and49_gaining_full_candidate_queues':2,'actual_new_candidate_inference_claimed':False},flush=True)
if __name__=='__main__':main()
