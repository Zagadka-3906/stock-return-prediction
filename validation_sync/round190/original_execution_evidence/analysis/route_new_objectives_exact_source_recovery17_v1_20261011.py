"""Route fresh workers to real source corrections, retaining original failures and model banks."""
from pathlib import Path
import sys,importlib,runpy
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed,closed as base_closed
from start_fast_completed_owned_service_v1_20261011 import start_service as base_start
PROOF=A/'new_objectives_exact_source_recovery17_routes_v1_20261011.json'
def installed():
 data=read(PROOF)
 for p,d in data['input_sha256'].items():assert sha(p)==d,p
 def actual(n):return data['service_aliases'].get(n,n)
 def closed(n):return base_closed(actual(n))
 def start(n,d,args,pins):return base_start(actual(n),data['driver_wrappers'].get(d,d),args,{**pins,str(PROOF):sha(PROOF),str(Path(__file__)):sha(__file__)})
 import prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 as checks
 import handoff_ready_goss_full_execution_20261006 as launch
 import start_fast_completed_owned_service_v1_20261011 as fast
 checks.closed=closed;launch.start_service=start;fast.start_service=start
 for name in data['source_factories']:
  m=importlib.import_module(name);prior=m.source_paths
  def paths(prior=prior):return list(dict.fromkeys([*prior(),PROOF,Path(__file__),*[Path(p) for p in data['input_sha256']]]))
  m.source_paths=paths
 before=runpy.run_path
 def routed(path,*args,**kwargs):
  name=Path(path).name
  if name.startswith('prepare_') and '_selected_candidate_' in name and name in data['driver_wrappers']:path=A/data['driver_wrappers'][name]
  return before(str(path),*args,**kwargs)
 runpy.run_path=routed
 return closed,start,data
def execute(driver):
 assert allowed();closed,start,data=installed();p=A/data['source_overrides'].get(driver,driver)
 if driver.startswith('seal_') or '_full_registration_' in driver or '_selected_candidate_feature_cache_' in driver:
  runpy.run_path(str(p),run_name='__main__');return
 m=importlib.import_module(p.stem)
 if hasattr(m,'closed'):m.closed=closed
 if hasattr(m,'start_service'):m.start_service=start
 m.main()
