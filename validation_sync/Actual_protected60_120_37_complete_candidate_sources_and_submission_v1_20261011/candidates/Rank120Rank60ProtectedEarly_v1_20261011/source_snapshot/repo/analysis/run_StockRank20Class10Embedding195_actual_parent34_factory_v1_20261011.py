from pathlib import Path
import sys,importlib,runpy
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
from route_new_objectives_exact_source_recovery34_v1_20261011 import installed
if __name__=='__main__':
 assert allowed();closed,start,data=installed()
 import prepare_StockRank20Class10Embedding195_complete48_pipeline_v1_20261011 as m
 prior=m.source_paths
 m.source_paths=lambda:list(dict.fromkeys([*prior(),A/'new_objectives_exact_source_recovery34_routes_v1_20261011.json',Path(__file__)]))
 import start_fast_completed_owned_service_v1_20261011 as fast
 original=fast.start_service
 def dispatch(name,driver,args,pins):
  path=A/driver
  if 'StockRank20Class10' in driver or 'stock_rank20class10' in driver:
   q=A/(path.stem+'_actual_parent34_dispatch_wrapper.py')
   if not q.exists():
    text="from pathlib import Path\nimport sys,runpy\nA=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]\nfrom route_new_objectives_exact_source_recovery34_v1_20261011 import installed\nif __name__=='__main__':\n closed,start,data=installed()\n runpy.run_path(str(A/"+repr(driver)+"),run_name='__main__')\n"
    compile(text,str(q),'exec');q.write_text(text,encoding='utf8',newline='\n')
   return original(name,q.name,args,{**pins,str(q):sha(q)})
  return original(name,driver,args,pins)
 m.start_service=dispatch
 import handoff_ready_goss_full_execution_20261006 as launch
 launch.start_service=dispatch
 m.main()
