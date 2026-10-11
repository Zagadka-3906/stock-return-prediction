from pathlib import Path
import sys,runpy
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
kind=sys.argv[1];assert kind in ('weight84','fraction88')
import prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 as gates
from run_dependency_queue_v3_20261006 import read,sha
assert gates.allowed()
aliases={'actual_rank120_rank60_after183_consensusWeight8_screen84_v1_20261011':'actual_completed_weight84_namespace_bridge90_v1_20261011','actual_rank120_rank60_after183_consensusFraction8_screen88_v1_20261011':'actual_completed_fraction88_namespace_bridge91_v1_20261011','actual_consensusWeight8_results_selection_main85_v1_20261011':'actual_completed_weight85_full_pipeline90_v1_20261011'}
oldclosed=gates.closed
gates.closed=lambda name:oldclosed(aliases.get(name,name))
driver=sys.argv[2] if len(sys.argv)>2 else ('run_consensusWeight8_results_selection_main_and_conditional85_v1_20261011.py' if kind=='weight84' else 'run_consensusFraction8_results_selection_main_and_conditional89_v1_20261011.py')
import start_fast_completed_owned_service_v1_20261011 as fast
oldstart=fast.start_service
def start(name,child,args,pins):
 if child.startswith('normalize_rank120_rank60_consensus'):
  wrapper=A/('namespace_safe90_'+child);assert not wrapper.exists();wrapper.write_text('import sys\nfrom pathlib import Path\nsys.path.insert(0,str(Path(__file__).resolve().parent))\nimport runpy\nsys.argv=['+repr(str(A/'run_completed_screen_namespace_safe_pipeline90_v1_20261011.py'))+','+repr(kind)+','+repr(child)+']\nrunpy.run_path(sys.argv[0],run_name="__main__")\n',encoding='utf8')
  return oldstart(name,wrapper.name,args,{**pins,str(wrapper):sha(wrapper),str(Path(__file__)):sha(__file__)})
 return oldstart(name,child,args,pins)
fast.start_service=start
runpy.run_path(str(A/driver),run_name='__main__')
