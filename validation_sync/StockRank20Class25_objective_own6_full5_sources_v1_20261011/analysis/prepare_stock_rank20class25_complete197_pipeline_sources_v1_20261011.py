from pathlib import Path
import sys,re
A=Path(__file__).resolve().parent;ROOT=A.parent;sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
from start_fast_completed_owned_service_v1_20261011 import start_service
if __name__=='__main__':
 assert allowed();old=A/'prepare_StockRank20Class10Embedding195_complete48_pipeline_v1_20261011.py';new=A/'prepare_StockRank20Class25Embedding197_complete48_pipeline_v1_20261011.py';assert not new.exists()
 s=old.read_text(encoding='utf8').replace('StockRank20Class10','StockRank20Class25').replace('stock_rank20class10','stock_rank20class25').replace('rank20class10','rank20class25').replace('STOCK_RANK20CLASS10','STOCK_RANK20CLASS25').replace('top10_binary','top25_binary')
 s=s.replace('17948','18015').replace('qa106','qa108').replace('QA106','QA108').replace('qa_v106','qa_v108')
 s=re.sub(r'(?<!\d)(195|194|478|106)(?!\d)',lambda m:{'195':'197','194':'196','478':'480','106':'108'}[m.group()],s)
 s=s.replace("'stock_rank20tail4_embedding196_full_execution_sources_admission_v1_20261011.json'","'stock_rank20class10_embedding196_full_execution_sources_admission_v1_20261011.json'")
 s=s.replace("'StockRank20Tail4Embedding196_complete48_family_v1_20261011'","'StockRank20Class10Embedding196_complete19_family_v1_20261011'")
 s=s.replace("closed('actual_stock_rank20class25_objective_stages_main_v2_20261011')","closed('actual_stock_rank20class25_objective_stages_main_v1_20261011')")
 # The phase waiter is embedded in a quoted generated Python string.
 s=s.replace('actual_stock_rank20class25_objective_stages_main_v2_20261011','actual_stock_rank20class25_objective_stages_main_v1_20261011')
 compile(s,str(new),'exec');new.write_text(s,encoding='utf8',newline='\n')
 oldw=A/'run_StockRank20Class10Embedding195_actual_parent34_factory_v1_20261011.py';wrapper=A/'run_StockRank20Class25Embedding197_actual_parent34_factory_v1_20261011.py';assert not wrapper.exists();t=oldw.read_text(encoding='utf8').replace('StockRank20Class10','StockRank20Class25').replace('stock_rank20class10','stock_rank20class25').replace('Embedding195','Embedding197');compile(t,str(wrapper),'exec');wrapper.write_text(t,encoding='utf8',newline='\n')
 proof=A/'stock_rank20class25_complete197_pipeline_before_scores_sources_v1_20261011.json';paths=[Path(__file__),old,new,oldw,wrapper,A/'stock_rank20class25_balanced_BCE_actual_CPU_controls_v1_20261011.json',A/'stock_rank20class25_embedding_actual_eleven_parent_callbacks_CPU_controls_v1_20261011.json',A/'stock_rank20class10_latest183_complete196_exact_routes_v3_20261011.json'];create(proof,{'status':'compiled_top25_complete197_QA10818015W480_before_training_scores_future','input_sha256':{str(p):sha(p) for p in paths},'expected_records':48,'anchor_rounds':[175,196],'new_fits':0,'new_scores':0,'test_labels_read':False})
 assert allowed();r=start_service('actual_stock_rank20class25_complete197_factory_v1_20261011',wrapper.name,[],{str(wrapper):sha(wrapper),str(proof):sha(proof)});create(A/'actual_stock_rank20class25_complete197_factory_activation_v1_20261011.json',r)
