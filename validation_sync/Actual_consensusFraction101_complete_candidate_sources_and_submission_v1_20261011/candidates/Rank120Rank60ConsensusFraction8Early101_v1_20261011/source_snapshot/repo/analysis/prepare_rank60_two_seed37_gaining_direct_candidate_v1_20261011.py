"""Admit a complete37-model two-seed candidate only on an actual higher official TRAIN S."""
from pathlib import Path
import sys,ast,re,importlib
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
from handoff_ready_goss_full_execution_20261006 import start_service
PROOF='rank60_two_seed_protected37_early_sources_admission_v2_20261011.json'
RAW='recovery59_actual_rank60_two_seed_after183_protected37_screen_v1_20261011'

def changed(s):
 s=s.replace('rank60_two_capacity_protected109','rank60_two_seed_protected37').replace('Rank60TwoCapacityProtected109Early','Rank60TwoSeedProtected37Early')
 s=s.replace('rank60_two_capacity_protected','rank60_two_seed_protected').replace('medium_weight','second_seed_weight')
 s=s.replace('stock_rank60medium_embedding_medium2048','stock_rank60seed10_embedding_small512').replace('StockRank60MediumEmbeddingMedium2048','StockRank60Seed10EmbeddingSmall512')
 s=s.replace('60日大小网络protected109项提前完整候选','60日双随机种子37项提前完整候选').replace('60日大小网络protected109项','60日双随机种子37项')
 s=s.replace('capacity_protected109','rank60_two_seed_protected37')
 s=re.sub(r'(?<![A-Za-z0-9_])(109|108|324)(?![A-Za-z0-9_])',lambda m:{'109':'37','108':'36','324':'108'}[m.group()],s)
 for old,new in [('pilot109','pilot37'),('actual109','actual37'),('all109','all37'),('normalized109','normalized37')]:s=s.replace(old,new)
 return s

def save(p,s):
 ast.parse(s);assert not p.exists(),p;p.write_text(s,encoding='utf-8',newline='\n');return p

def main():
 assert allowed();original_cpu=A/'rank60_two_seed_protected_actual_twelve_parent_callbacks_CPU_controls_v1_20261011.json'
 cpu=read(original_cpu);assert len(cpu['records'])==12
 for p,d in cpu['input_sha256'].items():assert sha(p)==d,p
 bridge=save(A/'verify_rank60_two_seed_actual_completed_CPU12_gate_bridge_v1_20261011.py','''from pathlib import Path
import sys
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
assert allowed();p=A/'rank60_two_seed_protected_actual_twelve_parent_callbacks_CPU_controls_v1_20261011.json';v=read(p);assert len(v['records'])==12
for source,digest in v['input_sha256'].items():assert sha(source)==digest,source
for row in v['records']:assert sha(A/row['parent'])==row['sha256']
create(A/'rank60_two_seed_actual_completed_CPU12_gate_bridge_admission_v1_20261011.json',{'status':'passed_actual_completed12_CPU_controls_gate_bridge_no_new_tests_claimed','actual_existing_records':12,'new_CPU_tests':0,'input_sha256':{str(p):sha(p)},'new_native_fits':0,'new_scores':0,'test_labels_read':False})
''')
 templates=['normalize_rank60_two_capacity_protected109_early_v1_20261011.py','qualify_rank60_two_capacity_protected109_early_selected_native14_v2_20261011.py','prepare_Rank60TwoCapacityProtected109Early_selected_candidate_v2_20261011.py','run_Rank60TwoCapacityProtected109Early_selected_candidate_feature_cache_v2_20261011.py','seal_Rank60TwoCapacityProtected109Early_selected_candidate_v2_20261011.py','rank60_two_capacity_protected109_early_storage_v1_20261011.py','run_rank60_two_capacity_protected109_early_gaining_candidate_queue_v1_20261011.py','publish_actual_capacity_protected109_complete_candidate_main_v1_20261011.py','prepare_verified_capacity_protected109_alternate_submission_delivery_v1_20261011.py']
 outputs=[]
 for name in templates:
  text=changed((A/name).read_text(encoding='utf-8'))
  if name.startswith('normalize_'):
   text=text.replace('actual_rank60_two_capacity_after183_protected109_screen_v3_20261011',RAW).replace('StockRank60TwoCapacity_after183_protected109_screen_v1_20261011','StockRank60TwoSeed_after183_protected37_screen_v1_20261011')
   begin=text.index(' for width,bankname in ');end=text.index('\n records=[]',begin)
   text=text[:begin]+''' for seed,bankname in [(20261009,'stock_rank60_embedding_small512_BF16_bank6_v1_20261011'),(20261010,'stock_rank60seed10_embedding_small512_BF16_bank6_v1_20261011')]:
  bank=Path('E:/赛题五_本机临时')/bankname;info=read(bank/'2025/info.json')
  assert read(bank/'verification.json')['actual_native_fits']==6 and info['configuration']['seed']==seed
  assert info['configuration']['label_horizon_trading_days']==60 and info['configuration']['training_calendar_window']==252 and info['configuration']['hidden']==[512,256,128]
  leaves.append({'name':f'rank_MLP512_StockEmbedding16_Cross120Recent252Rank60Mean_seed{seed}_e64','bank':str(bank),'sha256':info['model_sha256'],'label_horizon_trading_days':60,'training_calendar_window':252})
  for year in range(2020,2026):
   for n in ('info.json','model.joblib'):p=bank/str(year)/n;pins[str(p)]=sha(p)
'''+text[end:]
  if name.startswith('run_rank60_'):
   text=text.replace('actual_rank60_two_capacity_after183_protected109_screen_v3_20261011',RAW)
   text=text.replace(" assert allowed();closed("," closed('actual_rank60medium2048_gain_selected_full_candidate_queue_v1_20261011')\n assert allowed();closed(",1)
   begin=text.index(" for n in ['alternate_verified_best_blend38");end=text.index(' assert references;',begin)
   text=text[:begin]+''' for p in sorted(A.glob('alternate_verified_*submission_delivery_v1_20261011.json')):
  v=read(p)
  if v.get('all_full_native_independent_reload_csv_and_cold80_checks_passed') and v.get('actual_main_commit'):
   references.append({'pointer':str(p),'sha256':sha(p),'S':v['official_TRAIN_internal_score']})
'''+text[end:]
  # Titles, recipes, codecs, model counts and all native/independent replay checks stay unchanged.
  outputs.append(save(A/changed(name),text))
 sourcepaths=[Path(__file__),bridge,original_cpu,*[A/n for n in templates],*outputs,A/'rank60_two_seed_protected_after_qualified183_native_stage_v1_20261011.py',A/'predict_rank60_two_seed_protected_complete_qualified183_scheme_v1_20261011.py']
 for p in outputs[:6]:importlib.import_module(p.stem)
 qualifier=outputs[1].read_text(encoding='utf-8');assert "closed('actual_rank60_two_seed_protected_twelve_parent_callbacks_CPU_v1_20261011')" in qualifier
 prep=outputs[2].read_text(encoding='utf-8');assert 'stock_rank60seed10_embedding_small512_BF16_bank6_v1_20261011' in prep and 'second_seed_weight' in prep
 assert '(36, 108)' in outputs[0].read_text(encoding='utf-8')
 create(A/PROOF,{'status':'predeclared_actual_all37_two_seed_official_scores_vs_highest_completed_candidate_S_only_before_complete37_model_candidate_execution','input_sha256':{str(p):sha(p) for p in sourcepaths},'actual_runtime_imported_modules':6,'actual_existing_parent_CPU_records':12,'new_native_fits':0,'new_quality_scores':0,'expected_records':37,'expected_nonidentity_full_controls':36,'expected_prefix_controls':108,'expected_physical_models':37,'native14_cold14_prefit7_full_two_independent_replays_reload_CSV_and_cold80_required':True,'source_scores_and_main_independent_of_adoption':True,'actual_future_X_read':False,'test_labels_read':False})
 jobs=[('actual_rank60_two_seed_protected_twelve_parent_callbacks_CPU_v1_20261011',bridge),('actual_rank60_two_seed_protected37_early_gaining_candidate_queue_v1_20261011',outputs[6]),('actual_rank60_two_seed_protected37_complete_candidate_main_v1_20261011',outputs[7]),('actual_verified_rank60_two_seed_protected37_alternate_delivery_v1_20261011',outputs[8])]
 for name,p in jobs:
  assert allowed();i=start_service(name,p.name,[],{str(p):sha(p),str(A/PROOF):sha(A/PROOF)});create(A/(name+'_activation.json'),i)
 print({'actual_modules_imported':6,'two_seed_gain_only_complete37_candidate_pipeline_queued':True,'new_fits_or_scores':0},flush=True)

if __name__=='__main__':main()
