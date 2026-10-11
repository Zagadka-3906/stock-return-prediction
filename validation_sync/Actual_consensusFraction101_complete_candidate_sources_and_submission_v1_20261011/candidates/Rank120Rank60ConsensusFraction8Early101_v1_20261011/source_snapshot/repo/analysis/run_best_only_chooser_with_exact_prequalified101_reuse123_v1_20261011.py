from pathlib import Path
import sys,runpy
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,owned
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
assert allowed()
import start_fast_completed_owned_service_v1_20261011 as fast
original=fast.start_service
reuse={'actual_rank120_rank60_consensusFraction8_early101_normalization_v1_20261011':'normalize_rank120_rank60_consensusFraction8_early101_v1_20261011.py','actual_rank120_rank60_consensusFraction8_early101_selected_native14_v1_20261011':'qualify_rank120_rank60_consensusFraction8_early101_selected_native14_v2_20261011.py'}
def dispatch(name,driver,args,pins):
 if name in reuse:
  assert driver==reuse[name] and not args
  f=A/'service_owned_workflows_20261006'/name;definition=read(f/'job_definition.json');assert definition['driver']==str(A/driver) and definition['arguments']==args
  for p,d in pins.items():assert sha(p)==d and definition['input_sha256'][p]==d,p
  identity=read(f/'native_launch.json');terminal=read(f/'service_execution.json') if (f/'service_execution.json').exists() else None
  assert owned(identity) or terminal and terminal['status']=='passed';return identity
 return original(name,driver,args,pins)
fast.start_service=dispatch
try:runpy.run_path(str(A/'run_final_score_best_only_fraction100_or108_pipeline110_v1_20261011.py'),run_name='__main__')
finally:fast.start_service=original
