"""A new capacity-diverse ensemble using own independently verified H60 annual banks."""
from pathlib import Path
import sys,ast,re,importlib
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
from start_fast_completed_owned_service_v1_20261011 import start_service
PROOF='rank60_two_capacity_after183_protected109_predeclared_sources_admission_v1_20261011.json'
def changed(s):
 s=s.replace('rank60_two_seed','rank60_two_capacity').replace('Rank60TwoSeed','Rank60TwoCapacity')
 s=s.replace('RANK60_TWO_SEED','RANK60_TWO_CAPACITY').replace('second_seed_weight','medium_weight')
 s=s.replace('stock_rank60seed10_embedding_small512','stock_rank60medium_embedding_medium2048')
 s=s.replace('stock_rank60seed10_embedding_saved_tensor_decoder','stock_rank60medium_embedding_saved_tensor_decoder')
 s=s.replace('StockRank60Seed10EmbeddingSmall512','StockRank60MediumEmbeddingMedium2048')
 s=s.replace('protected37','protected109')
 s=s.replace('(20261009,20261010)','(20261009,20261009)')
 s=s.replace("right['configuration']['seed']==20261010","right['configuration']['seed']==20261009")
 return s
def main():
 assert allowed()
 originals=['run_rank60_two_seed_after183_protected37_screen_v1_20261011.py',
  'rank60_two_seed_protected_after_qualified183_native_stage_v1_20261011.py',
  'predict_rank60_two_seed_protected_complete_qualified183_scheme_v1_20261011.py',
  'verify_rank60_two_seed_protected_actual_twelve_parent_callbacks_CPU_v1_20261011.py']
 outputs=[]
 for name in originals:
  s=changed((A/name).read_text(encoding='utf8'))
  if name.startswith('run_'):
   start=s.index('def cases():');end=s.index('\ndef main():',start)
   s=s[:start]+'''def cases():
    rows=[{'kind':'anchor183','role':None,'weight':0.,'sign':1.,'protect_fraction':None,'medium_weight':None}]
    for blend in (.125,.5,.875):
        for fraction in (.125,.2,.35):
            for sign in (-1.,1.):
                for weight in (.004,.016,.064,.25,.5,1.):
                    rows.append({'kind':'valid_pool_protection_v1','role':'nonflag_valid','weight':weight,'sign':sign,'protect_fraction':fraction,'medium_weight':blend})
    assert len(rows)==109;return rows

'''+s[end:]
   s=re.sub(r'(?<![A-Za-z0-9_])(37|36|108)(?![A-Za-z0-9_])',lambda m:{'37':'109','36':'108','108':'324'}[m.group()],s)
   s=s.replace("closed('actual_stock_rank60_after183_protected_fraction38_screen_v1_20261011')","closed('actual_fraction38_completed_namespace_bridge_v1_20261011')")
   s=s.replace("closed('actual_stock_rank60seed10_embedding_after183_direct_allocation33_v1_20261011')","closed('actual_rank60medium2048_gain_selected_full_candidate_queue_v1_20261011')")
   s=s.replace("        assert left['model_sha256']!=right['model_sha256']","        assert left['configuration']['hidden']==[512,256,128] and right['configuration']['hidden']==[2048,1024,512]\n        assert left['model_sha256']!=right['model_sha256']")
  if name.startswith('rank60_'):
   s=s.replace("assert native.CONFIG['seed']==(20261009,20261009)[i] and native.CONFIG['epochs']==64", "assert native.CONFIG['seed']==20261009 and native.CONFIG['epochs']==64\n        assert native.CONFIG['hidden']==([512,256,128],[2048,1024,512])[i]")
  p=A/changed(name);ast.parse(s);assert not p.exists();p.write_text(s,encoding='utf8');outputs.append(p)
 raw=importlib.import_module(outputs[0].stem);assert len(raw.cases())==109
 assert {x['protect_fraction'] for x in raw.cases()[1:]}=={.125,.2,.35}
 stage=importlib.import_module(outputs[1].stem)
 assert stage.BACKENDS[stage.RECIPE][0].startswith('stock_rank60_embedding_small512')
 assert stage.BACKENDS[stage.RECIPE][2].startswith('stock_rank60medium_embedding_medium2048')
 create(A/PROOF,{'status':'predeclared109_capacity_diverse_H60_protected_ensemble_before_actual_scores',
  'input_sha256':{str(p):sha(p) for p in [Path(__file__),*[A/n for n in originals],*outputs,A/'stock_rank60medium2048_own6_full5_native42_direct33_predeclared_sources_v1_20261011.json']},
  'cases':raw.cases(),'expected_records':109,'expected_nonidentity_full_controls':108,'expected_prefix_controls':324,
  'same_seed':20261009,'capacity_pairs':[[512,256,128],[2048,1024,512]],'label_horizons':[60,60],
  'training_calendar_origins':[252,252],'new_fits':0,'new_scores':0,'test_labels_read':False,'actual_future_X_read':False,
  'GPU_and_memory_serialization_after':'actual_rank60medium2048_gain_selected_full_candidate_queue_v1_20261011'})
 for name,p in [('actual_rank60_two_capacity_twelve_parent_callbacks_CPU_v1_20261011',outputs[3]),
                ('actual_rank60_two_capacity_after183_protected109_screen_v1_20261011',outputs[0])]:
  assert allowed();row=start_service(name,p.name,[],{str(p):sha(p),str(A/PROOF):sha(A/PROOF)})
  create(A/(name+'_activation.json'),row)
 print({'new_predeclared_comparisons':109,'new_training_fits':0,'same_target_different_capacity':True},flush=True)
if __name__=='__main__':main()
