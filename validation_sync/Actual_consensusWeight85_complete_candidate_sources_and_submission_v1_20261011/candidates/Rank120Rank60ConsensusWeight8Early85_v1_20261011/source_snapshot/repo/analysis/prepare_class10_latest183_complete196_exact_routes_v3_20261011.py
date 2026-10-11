from pathlib import Path
import sys,importlib
A=Path(__file__).resolve().parent;ROOT=A.parent;sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
from start_fast_completed_owned_service_v1_20261011 import start_service
if __name__=='__main__':
 assert allowed();m=importlib.import_module('prepare_StockRank20Class10Embedding196_complete19_pipeline_v2_20261011');old=A/m.EXTRAS[0];new=A/'normalize_completed_stock_rank20class10_embedding_complete19_after195_exact_v3_20261011.py';assert not new.exists();s=old.read_text(encoding='utf8').replace("plan['fully_qualified_anchors']==[175,195]","plan['fully_qualified_anchors']==[183,195]").replace('StockRank20Class10Embedding195_complete19_family_v1_20261011','StockRank20Class10Embedding195_complete48_family_v1_20261011');assert "[175,195]" not in s;compile(s,str(new),'exec');new.write_text(s,encoding='utf8',newline='\n')
 oldname='actual_stock_rank20class10_embedding19_after195_normalization_queue_v1_20261011';f=A/'service_owned_workflows_20261006'/oldname;assert read(f/'service_execution.json')['status']=='failed' and not owned(read(f/'native_launch.json'))
 tasks=[(oldname,m.EXTRAS[0]),('StockRank20Class10Embedding19_selected_native14_v1_20261011',m.EXTRAS[1]),('StockRank20Class10Embedding196_complete19_family_v1_20261011',m.EXTRAS[5])];aliases={oldname:'actual_stock_rank20class10_embedding19_after195_normalization_exact_v3_20261011'};wrappers={};paths=[Path(__file__),old,new,A/'route_class10_latest183_complete196_exact_v3_20261011.py',*m.source_paths()]
 for d in [m.EXTRAS[0],m.EXTRAS[1],m.EXTRAS[5],m.EXTRAS[6],m.EXTRAS[8],m.EXTRAS[4]]:
  p=A/(Path(d).stem+'_latest183_exact_v3_wrapper.py');assert not p.exists();s="from pathlib import Path\nimport sys\nA=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]\nfrom route_class10_latest183_complete196_exact_v3_20261011 import execute\nif __name__=='__main__':execute("+repr(d)+")\n";compile(s,str(p),'exec');p.write_text(s,encoding='utf8',newline='\n');wrappers[d]=p.name;paths.append(p)
 normal=importlib.import_module(new.stem);stage=importlib.import_module(m.EXTRAS[14][:-3]);assert set(normal.RECIPES)==set(stage.BACKENDS)
 from verify_protected162_full_family_preflight_v1_20261010 import literal_assignments
 opt=literal_assignments(A/m.NAMES[2]);assert (opt['NUMBER'],opt['PREVIOUS_NUMBER'],opt['WAVES'])==(196,195,(479,))
 assert '(196, 107, 19)' in (A/m.NAMES[-1]).read_text(encoding='utf8')
 plan=read(A/m.EXTRAS[11]);assert plan['expected_records']==19 and plan['fully_qualified_anchors']==[183,195] and len(plan['families'])==1 and plan['families'][0]['records']==17 and plan['families'][0]['base_round']==183
 for p in paths:
  if p.suffix=='.py':compile(p.read_text(encoding='utf8'),str(p),'exec')
 proof=A/'stock_rank20class10_latest183_complete196_exact_routes_v3_20261011.json';create(proof,{'status':'compiled_actual19_records16_full48_prefix_anchors183195_QA10717967W479_before_scores_future','input_sha256':{str(p):sha(p) for p in dict.fromkeys(paths)},'service_aliases':aliases,'driver_wrappers':wrappers,'source_overrides':{old.name:new.name},'expected_records':19,'old_failed_normalizer_preserved':read(f/'service_execution.json'),'new_fits':0,'new_scores':0})
 for n,d in tasks:
  assert allowed();p=A/wrappers[d];r=start_service(aliases.get(n,n),p.name,[],{str(p):sha(p),str(proof):sha(proof)});create(A/(aliases.get(n,n)+'_activation_v3.json'),r)
 print({'actual_latest183_complete196_routes_v3_dispatched':3,'new_fits_or_scores':0},flush=True)
