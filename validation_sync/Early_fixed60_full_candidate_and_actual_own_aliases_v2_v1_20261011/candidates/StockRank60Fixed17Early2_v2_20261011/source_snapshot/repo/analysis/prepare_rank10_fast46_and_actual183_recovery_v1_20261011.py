from pathlib import Path
import sys,re,ast
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
from start_fast_completed_owned_service_v1_20261011 import start_service

def save(name,text):
 p=A/name;assert not p.exists(),p;compile(text,str(p),'exec');p.write_text(text,encoding='utf8',newline='\n');return p

def main():
 assert allowed();outputs=[];inputs=[]
 def clone(name,mapping):
  p=A/name;inputs.append(p);text=p.read_text(encoding='utf8')
  pat=re.compile('|'.join(re.escape(k) for k in sorted(mapping,key=len,reverse=True)))
  out=save(pat.sub(lambda m:mapping[m.group()],name),pat.sub(lambda m:mapping[m.group()],text));outputs.append(out);return out
 basic={'stock_rank5':'stock_rank10','StockRank5':'StockRank10','rank5mean':'rank10mean','Rank5Embedding':'Rank10Embedding','_v1_20261010':'_v1_20261011'}
 # Only rename the new native modules; keep all shared feature/network/codec imports unchanged.
 for name in ['stock_rank5_embedding_after_complete_qualified_parent_native_stage_v1_20261010.py','verify_stock_rank5_embedding_six_state_native42_v1_20261010.py']:
  text=(A/name).read_text(encoding='utf8');inputs.append(A/name)
  mapping={'stock_rank5':'stock_rank10','StockRank5':'StockRank10','rank5mean':'rank10mean','StockRank5Embedding16':'StockRank10Embedding16','RankHuber010_seed09_e24':'Rank10Mean_seed09_e64'}
  for stem in ['stock_rank5_embedding_after_complete_qualified_parent_native_stage','stock_rank5_embedding_small512_BF16_native','stock_rank5_embedding_saved_tensor_decoder','stock_rank5_embedding_native_stage_and_fast17_sources_admission','actual_stock_rank5_embedding_small512_bank6_location','actual_stock_rank5_embedding_six_state_native42_location','stock_rank5_embedding_six_state_native42']:
   mapping[stem+'_v1_20261010']=stem.replace('rank5','rank10')+'_v1_20261011'
  mapping['StockRank5EmbeddingSmall512_independent_full5_GPU_controls_v1_20261009']='StockRank10EmbeddingSmall512_independent_full5_GPU_controls_v1_20261011'
  mapping['stock_rank5_embedding_after_complete_qualified_parent_v1_20261010']='stock_rank10_embedding_after_complete_qualified_parent_v1_20261011'
  pat=re.compile('|'.join(re.escape(k) for k in sorted(mapping,key=len,reverse=True)))
  target=name.replace('rank5','rank10').replace('_20261010','_20261011');outputs.append(save(target,pat.sub(lambda m:mapping[m.group()],text)))
 for name in ['run_stock_rank20long_embedding_after175_fast17_screen_v1_20261010.py','run_stock_rank20long_embedding_after175_large_allocation29_screen_v1_20261010.py']:
  mapping={'stock_rank20long':'stock_rank10','StockRank20Long':'StockRank10','rank20mean':'rank10mean','recent504':'recent252'}
  text=(A/name).read_text(encoding='utf8');inputs.append(A/name)
  # All new bank, screen and stage controls use their own fresh dates; shared guards remain frozen.
  for token in set(re.findall(r'[A-Za-z0-9_]*(?:rank20long|StockRank20Long)[A-Za-z0-9_]*',text)):
   if '202610' in token:mapping[token]=token.replace('rank20long','rank10').replace('StockRank20Long','StockRank10').replace('20261010','20261011').replace('20261009','20261011')
  pat=re.compile('|'.join(re.escape(k) for k in sorted(mapping,key=len,reverse=True)))
  target=name.replace('rank20long','rank10').replace('20261010','20261011');outputs.append(save(target,pat.sub(lambda m:mapping[m.group()],text)))
 clone('predict_stock_rank20_embedding_complete_qualified_parent_scheme_v1_20261010.py',{
  'stock_rank20_embedding':'stock_rank10_embedding','STOCK_RANK20_EMBEDDING':'STOCK_RANK10_EMBEDDING',
  'stock_rank20_embedding_after_complete_qualified_parent_native_stage_v1_20261010':'stock_rank10_embedding_after_complete_qualified_parent_native_stage_v1_20261011',
  'predict_stock_rank20_embedding_complete_qualified_parent_scheme_v1_20261010':'predict_stock_rank10_embedding_complete_qualified_parent_scheme_v1_20261011'})
 clone('verify_rank5_rank20_mixed_actual_eleven_parent_callbacks_CPU_v1_20261011.py',{
  'verify_rank5_rank20_mixed_actual_eleven_parent_callbacks_CPU':'verify_stock_rank10_embedding_actual_eleven_parent_callbacks_CPU',
  'predict_rank5_rank20_mixed_complete_qualified_parent_scheme':'predict_stock_rank10_embedding_complete_qualified_parent_scheme',
  'RANK5_RANK20_MIXED_AFTER_WHOLE_QUALIFIED_PARENT':'STOCK_RANK10_EMBEDDING_AFTER_WHOLE_QUALIFIED_PARENT',
  'rank5_rank20_mixed_actual_eleven_parent_callbacks_CPU_controls':'stock_rank10_embedding_actual_eleven_parent_callbacks_CPU_controls'})
 proof=A/'stock_rank10_embedding_native_stage_and_fast17_sources_admission_v1_20261011.json'
 create(proof,{'status':'compiled_own_rank10_stage_independent42_callbacks_and46_training_only_cases_before_training',
 'input_sha256':{str(p):sha(p) for p in [Path(__file__),*inputs,*outputs,A/'stock_rank10_embedding_actual_restart_and_own6_sources_admission_v1_20261011.json']},
 'expected_native':42,'expected_cold':42,'expected_prefit':7,'expected_screen_cases':[17,29],'mean_horizon':10,'new_fits':0,'new_scores':0,'test_labels_read':False})
 recover=save('verify_actual183_completed_inner_inference_after_cache_postcondition_failure_v1_20261011.py', '''from pathlib import Path
import sys
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
def main():
 assert allowed()
 release=A/'StockRank20Embedding183_selected_release_v1_20261010';ready=read(release/'inference_ready.json');v=read(release/'verification.json')
 assert ready['status']=='passed_actual_selected_new_StockRank20Embedding183_candidate_inference'
 assert v['status']=='passed_frozen_StockRank20Embedding183_complete_parent_native_independent_and_cold80'
 for p,d in v['input_sha256'].items():assert sha(p)==d,p
 folder=Path(ready['source_candidate']);pred=read(folder/'verification.json')
 assert pred['status']=='passed' and (pred['rows'],pred['days'],pred['codes'])==(1599600,344,4650)
 for k in ('model_reload_bit_identical','pipeline_replay_bit_identical','csv_replay_byte_identical','cold80_day_prefix_bit_identical'):assert pred[k],k
 assert sha(folder/'submission.csv')==pred['csv_sha256']==v['csv_sha256']
 assert len(pred['models'])==v['actual_saved_model_count']==35
 for m in pred['models'].values():assert sha(m['path'])==m['sha256']
 create(A/'actual183_completed_inner_inference_rehashed_recovery_v1_20261011.json',{'status':'passed_rehashed_actual_inner_full_candidate_inference_after_outer_4660_cache_postcondition_failure','input_sha256':{str(p):sha(p) for p in [Path(__file__),release/'inference_ready.json',release/'verification.json',folder/'verification.json',folder/'submission.csv']},'actual_saved_models':35,'rows_days_stocks':[1599600,344,4650],'new_inference_performed':False,'outer_cache_statistics_not_recovered_or_claimed':True,'original_failed_service_preserved':True,'test_labels_read':False})
if __name__=='__main__':main()
''')
 outputs.append(recover)
 old=A/'run_stock_rank10_embedding_own_training_and_full5_queue_v1_20261011.py';inputs.append(old)
 text=old.read_text(encoding='utf8')
 text=text.replace("closed('recovery14_StockRank20Embedding183_selected_candidate_preparation_v1_20261010')","closed('actual183_completed_inner_inference_rehashed_recovery_v1_20261011')")
 text=text.replace("    closed('recovery14_StockRank20Embedding183_selected_candidate_sealing_v1_20261010')\n",'')
 queue=save('run_stock_rank10_embedding_own_training_and_full5_queue_v2_20261011.py',text);outputs.append(queue)
 screen=save('run_stock_rank10_native42_and_fast46_queue_v1_20261011.py', '''from pathlib import Path
import sys
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed,closed
from start_fast_completed_owned_service_v1_20261011 import start_service
def main():
 assert allowed();closed('StockRank10EmbeddingSmall512_independent_full5_GPU_controls_v1_20261011')
 for name,driver in [('actual_stock_rank10_embedding_six_state_native42_v1_20261011','verify_stock_rank10_embedding_six_state_native42_v1_20261011.py'),('actual_stock_rank10_embedding_after175_fast17_screen_v1_20261011','run_stock_rank10_embedding_after175_fast17_screen_v1_20261011.py'),('actual_stock_rank10_embedding_after175_large_allocation29_screen_v1_20261011','run_stock_rank10_embedding_after175_large_allocation29_screen_v1_20261011.py')]:
  assert allowed();p=A/driver;r=start_service(name,driver,[],{str(p):sha(p)});create(A/(name+'_activation.json'),r);closed(name)
if __name__=='__main__':main()
''');outputs.append(screen)
 create(A/'rank10_fast46_and_actual183_inner_recovery_dispatch_v1_20261011.json',{'status':'sources_compiled_before_actual_dispatch','input_sha256':{str(p):sha(p) for p in [Path(__file__),*outputs,proof]},'new_fits':0,'new_scores':0,'outer_cache_failure_preserved':True})
 for name,p in [('actual183_completed_inner_inference_rehashed_recovery_v1_20261011',recover),('actual_stock_rank10_embedding_eleven_parent_callbacks_CPU_v1_20261011',A/'verify_stock_rank10_embedding_actual_eleven_parent_callbacks_CPU_v1_20261011.py'),('actual_stock_rank10_embedding_own_training_and_full5_queue_v2_20261011',queue),('actual_stock_rank10_native42_and_fast46_queue_v1_20261011',screen)]:
  assert allowed();row=start_service(name,p.name,[],{str(p):sha(p)});create(A/(name+'_activation.json'),row)
 print({'new_actual_tasks':4,'own_rank10_annual_fits_not_yet_claimed':True},flush=True)
if __name__=='__main__':main()
