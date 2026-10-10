"""Scoped continuation preserving the exact complete183 graph and frozen sources."""
from pathlib import Path
import sys,importlib,runpy,builtins
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
from start_fast_completed_owned_service_v1_20261011 import start_service as original_start
PROOF=A/'actual_latest183_parent196198_routes37_v1_20261011.json'

def installed():
 import route_unified_completed_parent_shared_publication36_v1_20261011 as previous
 prior_closed,_,_=previous.installed();data=read(PROOF)
 for p,d in data['input_sha256'].items():assert sha(p)==d,p
 def actual(n):
  seen=set()
  while n in data['service_aliases'] and data['service_aliases'][n]!=n:
   assert n not in seen;seen.add(n);n=data['service_aliases'][n]
  return n
 def closed(n):return prior_closed(actual(n))
 def start(n,d,args,pins):return original_start(actual(n),data['driver_wrappers'].get(d,d),args,{**pins,str(PROOF):sha(PROOF),str(Path(__file__)):sha(__file__)})
 import prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 as checks
 import handoff_ready_goss_full_execution_20261006 as launch
 import start_fast_completed_owned_service_v1_20261011 as fast
 checks.closed=closed;launch.start_service=start;fast.start_service=start
 for name in data['source_factories']:
  m=importlib.import_module(name);prior=m.source_paths
  m.source_paths=lambda prior=prior:list(dict.fromkeys([*prior(),PROOF,Path(__file__),*[Path(p) for p in data['input_sha256']]]))
 prior_import=builtins.__import__
 def importing(name,globals=None,locals=None,fromlist=(),level=0):
  if level==0:name=data['module_aliases'].get(name,name)
  return prior_import(name,globals,locals,fromlist,level)
 builtins.__import__=importing
 prior_run=runpy.run_path
 def routed(path,*args,**kwargs):
  name=Path(path).name
  if name.startswith('prepare_') and '_selected_candidate_' in name:path=str(A/data['actual_source_overrides'].get(name,name))
  return prior_run(path,*args,**kwargs)
 runpy.run_path=routed
 return closed,start,data

def execute(driver):
 assert allowed();closed,start,data=installed();source=A/data['actual_source_overrides'].get(driver,driver)
 if driver.startswith('seal_') or '_full_registration_' in driver:runpy.run_path(str(source),run_name='__main__');return
 m=importlib.import_module(source.stem)
 if hasattr(m,'closed'):m.closed=closed
 if hasattr(m,'start_service'):m.start_service=start
 m.main()
