from pathlib import Path
import sys,re
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed,closed
from start_fast_completed_owned_service_v1_20261011 import start_service
def main():
 assert allowed();closed('actual_stock_rank20tail4_weighted_Huber_CPU_v1_20261011')
 inputs=[];outputs=[]
 def renamed(text):
  fixture='actual_stock_rank20_embedding_mature_fixture_location_v1_20261010.json';text=text.replace(fixture,'__ORIGINAL_RANK20_MATURE_FIXTURE__')
  text=text.replace('stock_rank20_embedding','stock_rank20tail4_embedding').replace('StockRank20Embedding','StockRank20Tail4Embedding')
  text=re.sub(r'[A-Za-z0-9_]*(?:stock_rank20tail4|StockRank20Tail4)[A-Za-z0-9_]*',lambda m:m.group().replace('20261010','20261011').replace('20261009','20261011'),text)
  return text.replace('__ORIGINAL_RANK20_MATURE_FIXTURE__',fixture)
 for name in ['verify_stock_rank20_embedding_small512_restart_v1_20261010.py','verify_stock_rank20_embedding_small512_small_CPU_v1_20261010.py','train_stock_rank20_embedding_small512_BF16_bank6_own64_v1_20261010.py','verify_stock_rank20_embedding_small512_full5_independent_v1_20261010.py']:
  p=A/name;inputs.append(p);text=renamed(p.read_text(encoding='utf8'));q=A/renamed(name);assert not q.exists()
  if name.startswith('train_'):
   assert "label_end <= cutoff" in text;text=text.replace('label_end <= cutoff','label_end < cutoff')
  compile(text,str(q),'exec');q.write_text(text,encoding='utf8',newline='\n');outputs.append(q)
 proof=A/'stock_rank20tail4_restart_and_own6_sources_admission_v1_20261011.json'
 create(proof,{'status':'compiled_fresh_restart_and_own6_full5_for_new_label_upper15_weighted_Huber_loss_CPU6_passed','input_sha256':{str(p):sha(p) for p in [Path(__file__),*inputs,*outputs,A/'stock_rank20tail4_weighted_Huber_actual_CPU_controls_v1_20261011.json',A/'stock_rank20tail4_own64_native_sources_preparation_v1_20261011.json']},'new_annual_fits':0,'new_scores':0,'mature_rank20_features_labels_reused_not_original_bank_weights':True,'forecast_pipeline_independent_decoder_and80_160_prefixes_required':True,'test_labels_read':False})
 queue=A/'run_stock_rank20tail4_own_training_and_full5_queue_v1_20261011.py';assert not queue.exists()
 text='''from pathlib import Path
import sys
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed,closed
from start_fast_completed_owned_service_v1_20261011 import start_service
def main():
 assert allowed();closed('actual_stock_rank20tail4_weighted_Huber_CPU_v1_20261011')
 closed('actual_stock_rank10_embedding_six_state_native42_v1_20261011')
 closed('recovery15_StockRank20Embedding183_selected_candidate_sealing_v1_20261010')
 for name,driver in [('actual_stock_rank20tail4_embedding_small512_restart_v1_20261011','verify_stock_rank20tail4_embedding_small512_restart_v1_20261011.py'),('StockRank20Tail4EmbeddingSmall512_independent_small_CPU_v1_20261011','verify_stock_rank20tail4_embedding_small512_small_CPU_v1_20261011.py'),('actual_stock_rank20tail4_embedding_small512_bank6_v1_20261011','train_stock_rank20tail4_embedding_small512_BF16_bank6_own64_v1_20261011.py'),('StockRank20Tail4EmbeddingSmall512_independent_full5_GPU_controls_v1_20261011','verify_stock_rank20tail4_embedding_small512_full5_independent_v1_20261011.py')]:
  assert allowed();p=A/driver;r=start_service(name,driver,[],{str(p):sha(p)});create(A/(name+'_activation.json'),r);closed(name)
if __name__=='__main__':main()
''';compile(text,str(queue),'exec');queue.write_text(text,encoding='utf8',newline='\n')
 r=start_service('actual_stock_rank20tail4_own_training_and_full5_queue_v1_20261011',queue.name,[],{str(queue):sha(queue),str(proof):sha(proof)});create(A/'actual_stock_rank20tail4_own_training_and_full5_queue_activation_v1_20261011.json',r)
 print({'weighted_rank20_tail4_restart_and_own6_full5_actual_queue_dispatched':True},flush=True)
if __name__=='__main__':main()
