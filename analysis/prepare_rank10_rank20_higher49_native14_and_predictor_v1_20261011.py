from pathlib import Path
import sys,re,ast,importlib
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
from start_fast_completed_owned_service_v1_20261011 import start_service
def main():
 assert allowed();inputs=[];outputs=[]
 def transform(text):
  mapping={'rank5_rank20':'rank10_rank20','StockRank5Rank20':'StockRank10Rank20','RANK5_RANK20':'RANK10_RANK20','rank5_weight':'rank10_weight','stock_rank5_embedding_small512_BF16_native_v1_20261010':'stock_rank10_embedding_small512_BF16_native_v1_20261011','stock_rank5_embedding_saved_tensor_decoder_v1_20261010':'stock_rank10_embedding_saved_tensor_decoder_v1_20261011','y_rank_5mean':'y_rank_10mean','stock_rank5_embedding':'stock_rank10_embedding'}
  pat=re.compile('|'.join(re.escape(k) for k in sorted(mapping,key=len,reverse=True)))
  text=pat.sub(lambda m:mapping[m.group()],text).replace('(20,5)','(20,10)').replace('five-day','ten-day')
  text=text.replace('actual_rank10_rank20_after175_mixed_horizon49_screen_v2_20261011','actual_rank10_rank20_after175_higher_allocation49_screen_v1_20261011')
  text=text.replace('rank10_rank20_mixed_horizon49_predeclared_plan_v1_20261011.json','rank10_rank20_higher_allocation49_predeclared_sources_admission_v1_20261011.json')
  return text
 def save(name,text):
  p=A/name;assert not p.exists(),p;compile(text,str(p),'exec');p.write_text(text,encoding='utf8',newline='\n');outputs.append(p);return p
 for name in ['rank5_rank20_mixed_after_qualified_parent_native_stage_v1_20261011.py','predict_rank5_rank20_mixed_complete_qualified_parent_scheme_v1_20261011.py','verify_rank5_rank20_mixed_selected_native14_v1_20261011.py','verify_rank5_rank20_mixed_actual_eleven_parent_callbacks_CPU_v1_20261011.py']:
  p=A/name;inputs.append(p);text=transform(p.read_text(encoding='utf8'))
  if name.startswith('verify_rank5_rank20_mixed_selected'):
   text=text.replace("closed('registered13_StockRank20Embedding183_complete85_family_v6_20261010')","closed('recovery15_StockRank20Embedding183_selected_candidate_sealing_v1_20261010')")
   needle="banks=[Path(f'E:/赛题五_本机临时/{name}_small512_BF16_bank6_v1_20261010') for name in ('stock_rank20_embedding','stock_rank10_embedding')]"
   assert needle in text;text=text.replace(needle,"banks=[Path('E:/赛题五_本机临时/stock_rank20_embedding_small512_BF16_bank6_v1_20261010'),Path('E:/赛题五_本机临时/stock_rank10_embedding_small512_BF16_bank6_v1_20261011')]")
  save(transform(name),text)
 import rank10_rank20_mixed_after_qualified_parent_native_stage_v1_20261011 as stage
 n20=importlib.import_module(stage.BACKENDS[stage.RECIPE][0]);n10=importlib.import_module(stage.BACKENDS[stage.RECIPE][2])
 assert (n20.CONFIG['label_horizon_trading_days'],n10.CONFIG['label_horizon_trading_days'])==(20,10)
 assert (n20.CONFIG['target'],n10.CONFIG['target'])==('y_rank_20mean','y_rank_10mean')
 assert all((Path(A)/(m+'.py')).is_file() for m in stage.BACKENDS[stage.RECIPE])
 text=outputs[0].read_text(encoding='utf8');assert '(20,10)[i]' in text and "'y_rank_10mean'" in text and 'rank5_weight' not in text
 proof=A/'rank10_rank20_higher49_actual_native14_and_predictor_sources_admission_v1_20261011.json'
 create(proof,{'status':'compiled_distinct_horizon20_and10_native_replays_and_complete_parent175_callback_sources_before49_selection','input_sha256':{str(p):sha(p) for p in [Path(__file__),*inputs,*outputs,A/'rank10_rank20_higher_allocation49_predeclared_sources_admission_v1_20261011.json',*[A/(m+'.py') for m in stage.BACKENDS[stage.RECIPE]]]},'expected_native':14,'expected_cold':14,'expected_prefit_refusals':7,'independent_own_saved_annual_states':12,'own_population_equality_not_assumed':True,'new_fits':0,'new_scores':0,'future_X_read':False,'test_labels_read':False})
 for name,p in [('actual_rank10_rank20_mixed_actual_eleven_parent_callbacks_CPU_v1_20261011',A/'verify_rank10_rank20_mixed_actual_eleven_parent_callbacks_CPU_v1_20261011.py'),('actual_rank10_rank20_mixed_selected_native14_v1_20261011',A/'verify_rank10_rank20_mixed_selected_native14_v1_20261011.py')]:
  assert allowed();r=start_service(name,p.name,[],{str(p):sha(p),str(proof):sha(proof)});create(A/(name+'_activation.json'),r)
 print({'new_horizon10_20_native14_and_CPU11_queued':True},flush=True)
if __name__=='__main__':main()
