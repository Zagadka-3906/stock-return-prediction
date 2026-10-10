from pathlib import Path
import sys,re,importlib
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
def main():
 assert allowed();outputs=[];inputs=[]
 def renamed(text):
  text=text.replace('stock_rank20long','stock_rank10').replace('StockRank20Long','StockRank10').replace('STOCK_RANK20LONG','STOCK_RANK10').replace('rank20mean','rank10mean').replace('Rank20Mean','Rank10Mean').replace('recent504','recent252').replace('Recent504','Recent252')
  text=re.sub(r'[A-Za-z0-9_]*(?:stock_rank10|StockRank10)[A-Za-z0-9_]*',lambda m:m.group().replace('20261010','20261011').replace('20261009','20261011'),text)
  text=re.sub(r'(?<!\d)(188|187|471|17538)(?!\d)',lambda m:{'188':'192','187':'191','471':'475','17538':'17801'}[m.group()],text)
  text=text.replace('qa99','qa103').replace('QA99','QA103').replace('qa_v99','qa_v103')
  text=text.replace('Rank20TwoSeed191_complete88_family_v2_20261011','recovery16_MixedRefined191_complete27_family_v1_20261011')
  return text
 def save(name,text):
  p=A/name;assert not p.exists(),p;compile(text,str(p),'exec');p.write_text(text,encoding='utf8',newline='\n');outputs.append(p);return p
 for name in ['normalize_completed_stock_rank20long_embedding_complete48_after187_v1_20261011.py','qualify_stock_rank20long_embedding48_selected_native14_v1_20261011.py']:
  inputs.append(A/name);save(renamed(name),renamed((A/name).read_text(encoding='utf8')))
 plan=read(A/'stock_rank20long_embedding_complete48_after187_selection_plan_v1_20261011.json')
 plan['status']='predeclared48_new_rank10_mean_horizon10_recent252_records_and175191_anchors_before_scoring'
 plan['fully_qualified_anchors']=[175,191];plan['training_calendar_window']=252;plan['label_horizon_trading_days']=10
 for family in plan['families']:
  for key in ('name','actual_service','stage_kind','main_receipt'):family[key]=renamed(family[key])
 create(A/'stock_rank10_embedding_complete48_after191_selection_plan_v1_20261011.json',plan)
 proof=A/'rank10_complete48_normalization_native14_sources_admission_v1_20261011.json'
 create(proof,{'status':'compiled_own_new_rank10_complete48_normalizer_and_selected_native14_before_scoring','input_sha256':{str(p):sha(p) for p in [Path(__file__),*inputs,*outputs,A/'stock_rank10_embedding_complete48_after191_selection_plan_v1_20261011.json',A/'stock_rank10_embedding_actual_eleven_parent_callbacks_CPU_controls_v1_20261011.json']},'new_fits':0,'new_scores':0,'future_X_read':False})
 name='prepare_StockRank20LongEmbedding188_complete48_pipeline_v1_20261011.py';inputs.append(A/name)
 text=renamed((A/name).read_text(encoding='utf8'))
 text=text.replace("'stock_rank20_embedding':'stock_rank10_embedding',","'stock_rank20_embedding':'stock_rank10_embedding','rank20mean':'rank10mean','Rank20Mean':'Rank10Mean',")
 text=text.replace("    text=basic(text)\n","    text=basic(text)\n    text=re.sub(r'[A-Za-z0-9_]*(?:stock_rank10|StockRank10)[A-Za-z0-9_]*',lambda m:m.group().replace('20261010','20261011').replace('20261009','20261011'),text)\n")
 text=text.replace("'actual_run_stock_rank10_embedding_504_own64_controls46_queue_v1_20261011'","'actual_stock_rank10_embedding_own_training_and_full5_queue_v2_20261011'")
 text=text.replace('StockForward20Embedding191_complete48_family_v6_after_Dual25_recovery_v1_20261010','StockForward20Embedding191_complete48_family_v6_after_Dual25_recovery_v1_20261010')
 # The previous factory expects an explicit predecessor service; it is the fully qualified191 family.
 text=text.replace("'Rank20TwoSeed191_complete88_family_v2_20261011'","'recovery16_MixedRefined191_complete27_family_v1_20261011'")
 text=text.replace('rank20_two_seed191_full_execution_sources_admission_v2_20261011.json','mixed_refined191_full_execution_sources_admission_v1_20261011.json')
 text=text.replace('rank20long_complete48_normalization_native14_sources_admission','rank10_complete48_normalization_native14_sources_admission')
 text=text.replace("native.CONFIG['training_calendar_window']==504","native.CONFIG['training_calendar_window']==252")
 factory=save('prepare_StockRank10Embedding192_complete48_pipeline_v1_20261011.py',text)
 import normalize_completed_stock_rank10_embedding_complete48_after191_v1_20261011 as normal
 import stock_rank10_embedding_after_complete_qualified_parent_native_stage_v1_20261011 as stage
 assert set(normal.RECIPES)==set(stage.BACKENDS)
 import prepare_StockRank10Embedding192_complete48_pipeline_v1_20261011 as module
 for n in module.EXTRAS[14:]:assert (A/n).is_file(),n
 create(A/'StockRank10Embedding192_factory_preparation_sources_v1_20261011.json',{'status':'compiled_192_complete48_QA103_17801_W475_factory_before_actual_materialization','input_sha256':{str(p):sha(p) for p in [Path(__file__),*inputs,*outputs,proof]},'new_quality_scores':0,'new_fits':0,'future_X_read':False})
 print({'normalization_and192_factory_compiled':True},flush=True)
if __name__=='__main__':main()
