from pathlib import Path
import sys,importlib
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
from start_fast_completed_owned_service_v1_20261011 import start_service
def main():
 assert allowed();paths=[]
 for name in ['normalize_completed_stock_rank10_embedding_complete48_after191_v1_20261011.py','qualify_stock_rank10_embedding48_selected_native14_v1_20261011.py']:
  p=A/(Path(name).stem+'_canonical_terminal_wrapper_v1_20261011.py');assert not p.exists()
  text="from pathlib import Path\nimport sys,importlib\nA=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]\nfrom prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed,closed\nif __name__=='__main__':\n assert allowed();m=importlib.import_module("+repr(Path(name).stem)+");m.closed=closed;m.main()\n"
  compile(text,str(p),'exec');p.write_text(text,encoding='utf8',newline='\n');paths.append(p)
 proof=A/'rank10_192_canonical_terminal_dispatch_admission_v1_20261011.json';create(proof,{'status':'compiled_exact_original_new_rank10_math_with_actual_terminal_prerequisite_controls','input_sha256':{str(p):sha(p) for p in [Path(__file__),*paths,A/'stock_rank10_embedding192_full_execution_sources_admission_v1_20261011.json']},'new_fits':0,'new_scores':0})
 tasks=[('actual_stock_rank10_embedding48_after191_normalization_queue_v1_20261011',paths[0]),('StockRank10Embedding48_selected_native14_v1_20261011',paths[1]),('actual_stock_rank10_objective_stages_main_v1_20261011',A/'run_stock_rank10_objective_actual_stages_main_v1_20261011.py')]
 for name,p in tasks:
  assert allowed();r=start_service(name,p.name,[],{str(p):sha(p),str(proof):sha(proof)});create(A/(name+'_activation.json'),r)
 print({'actual_rank10_192_prerequisites_and_staged_main_dispatched':3},flush=True)
if __name__=='__main__':main()
