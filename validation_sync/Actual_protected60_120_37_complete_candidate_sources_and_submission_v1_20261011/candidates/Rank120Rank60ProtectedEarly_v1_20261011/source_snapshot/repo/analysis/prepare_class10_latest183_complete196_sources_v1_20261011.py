from pathlib import Path
import sys,re
A=Path(__file__).resolve().parent;ROOT=A.parent;sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
from start_fast_completed_owned_service_v1_20261011 import start_service

def main():
 assert allowed();old=A/'prepare_StockRank20Class10Embedding195_complete48_pipeline_v1_20261011.py';new=A/'prepare_StockRank20Class10Embedding196_complete19_pipeline_v1_20261011.py';assert not new.exists()
 s=old.read_text(encoding='utf8').replace('17948','17967').replace('qa106','qa107').replace('QA106','QA107').replace('qa_v106','qa_v107')
 s=re.sub(r'(?<!\d)(195|194|478|106)(?!\d)',lambda m:{'195':'196','194':'195','478':'479','106':'107'}[m.group()],s)
 s=s.replace("'stock_rank20tail4_embedding195_full_execution_sources_admission_v1_20261011.json'","'stock_rank20class10_embedding195_full_execution_sources_admission_v1_20261011.json'")
 s=s.replace("'StockRank20Tail4Embedding195_complete48_family_v1_20261011'","'StockRank20Class10Embedding195_complete48_family_v1_20261011'")
 # Transform record19 identifiers without changing historical2048 widths or batch counts.
 s=re.sub(r'(?<!\d)48(?!\d)','19',s)
 # Parent195 remains the actual complete48 family.
 s=s.replace("'StockRank20Class10Embedding195_complete19_family_v1_20261011'","'StockRank20Class10Embedding195_complete48_family_v1_20261011'")
 needle=" return re.sub(r'(?<!\\d)(192|191|475|103)(?!\\d)',lambda m:"
 assert needle in s
 s=s.replace(needle," s=re.sub(r'(?<!\\d)48(?!\\d)','19',s)\n s=s.replace('(19,44,132)','(19,16,48)').replace('(44,132)','(16,48)').replace(\"'actual_nonidentity_full_controls':44\",\"'actual_nonidentity_full_controls':16\").replace(\"'actual_nonidentity_prefix_controls':132\",\"'actual_nonidentity_prefix_controls':48\").replace(\"anchor_round'] in (175,\",\"anchor_round'] in (183,\")\n"+needle)
 s=s.replace('fully_qualified_anchors=[175,195]','fully_qualified_anchors=[183,195]')
 needle=" plan['families']=[{k:basic(v) if isinstance(v,str) else v for k,v in f.items()} for f in plan['families']]"
 assert needle in s
 planfamily={'name':'StockRank20Class10EmbeddingSmall512_after183_high_impact17','actual_service':'actual_stock_rank20class10_embedding_after183_exact_latest_anchor17_v1_20261011','records':17,'base_round':183,'stage_kind':'stock_rank20class10_embedding_rank20mean_direct','main_receipt':'Class10_after183_actual17_sources_main_receipt_v1_20261011.json'}
 s=s.replace(needle," plan.update(status='predeclared19_actual_latest183_Top10_BCE17_and183195_complete_anchors_before_scores',expected_records=19,fully_qualified_anchors=[183,195],families=["+repr(planfamily)+"])")
 s=s.replace("'expected_full_controls':44,'expected_prefix_controls':132","'expected_full_controls':16,'expected_prefix_controls':48")
 # This scheme reuses the already registered Class10 phases; no duplicate exclusive receipt alias.
 start=s.index(" p=save(A/'alias_actual_rank20class10_official46_completed_main_receipt_v1_20261011.py'")
 end=s.index(" print({'",start)
 s=s[:start]+" name='StockRank20Class10Embedding196_complete19_family_v1_20261011';driver=EXTRAS[5]\n assert allowed();row=start_service(name,driver,[],{str(A/driver):sha(A/driver),str(A/PROOF):sha(A/PROOF)});create(A/(name+'_activation.json'),row)\n"+s[end:]
 compile(s,str(new),'exec');new.write_text(s,encoding='utf8',newline='\n')
 oldwrapper=A/'run_StockRank20Class10Embedding195_actual_parent34_factory_v1_20261011.py';wrapper=A/'run_StockRank20Class10Embedding196_actual_parent34_factory_v1_20261011.py';assert not wrapper.exists();t=oldwrapper.read_text(encoding='utf8').replace('Embedding195','Embedding196').replace('Embedding196_complete48_pipeline','Embedding196_complete19_pipeline');compile(t,str(wrapper),'exec');wrapper.write_text(t,encoding='utf8',newline='\n')
 proof=A/'stock_rank20class10_latest183_complete196_sources_admission_v1_20261011.json';paths=[Path(__file__),old,new,oldwrapper,wrapper,A/'stock_rank20class10_latest_qualified183_predeclared17_sources_v1_20261011.json'];create(proof,{'status':'compiled_actual_latest183_17_complete19_QA107_17967_W479_before_scores_or_future','input_sha256':{str(p):sha(p) for p in paths},'expected_records':19,'anchor_rounds':[183,195],'new_fits':0,'new_scores':0,'test_labels_read':False})
 assert allowed();r=start_service('actual_stock_rank20class10_latest183_complete196_factory_v1_20261011',wrapper.name,[],{str(wrapper):sha(wrapper),str(proof):sha(proof)});create(A/'actual_stock_rank20class10_latest183_complete196_factory_activation_v1_20261011.json',r)
 print({'class10_latest183_complete19_factory196_queued':True},flush=True)
if __name__=='__main__':main()
