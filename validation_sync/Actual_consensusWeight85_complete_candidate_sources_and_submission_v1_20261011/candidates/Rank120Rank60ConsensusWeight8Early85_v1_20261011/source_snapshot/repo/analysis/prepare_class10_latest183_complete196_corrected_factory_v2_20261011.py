from pathlib import Path
import sys
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
from start_fast_completed_owned_service_v1_20261011 import start_service
if __name__=='__main__':
 assert allowed();f=A/'service_owned_workflows_20261006/actual_stock_rank20class10_latest183_complete196_factory_v1_20261011';assert read(f/'service_execution.json')['status']=='failed' and not owned(read(f/'native_launch.json'))
 old=A/'prepare_StockRank20Class10Embedding196_complete19_pipeline_v1_20261011.py';new=A/'prepare_StockRank20Class10Embedding196_complete19_pipeline_v2_20261011.py';assert not new.exists();s=old.read_text(encoding='utf8').replace('prepare_StockRank10Embedding192_complete19_pipeline_v2_20261011','prepare_StockRank10Embedding192_complete48_pipeline_v2_20261011');compile(s,str(new),'exec');new.write_text(s,encoding='utf8',newline='\n')
 oldw=A/'run_StockRank20Class10Embedding196_actual_parent34_factory_v1_20261011.py';neww=A/'run_StockRank20Class10Embedding196_actual_parent34_factory_v2_20261011.py';assert not neww.exists();s=oldw.read_text(encoding='utf8').replace('Embedding196_complete19_pipeline_v1','Embedding196_complete19_pipeline_v2');compile(s,str(neww),'exec');neww.write_text(s,encoding='utf8',newline='\n')
 proof=A/'stock_rank20class10_latest183_complete196_corrected_factory_sources_v2_20261011.json';create(proof,{'status':'compiled_actual_existing192_complete48_template_for_new196_complete19_before_any_future','input_sha256':{str(p):sha(p) for p in [Path(__file__),old,new,oldw,neww]},'old_failure_preserved':read(f/'service_execution.json'),'new_fits':0,'new_scores':0})
 assert allowed();r=start_service('actual_stock_rank20class10_latest183_complete196_factory_v2_20261011',neww.name,[],{str(neww):sha(neww),str(proof):sha(proof)});create(A/'actual_stock_rank20class10_latest183_complete196_factory_activation_v2_20261011.json',r)
