from pathlib import Path
import sys,runpy,importlib
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha
from route_new_objectives_exact_source_recovery34_v1_20261011 import installed as prior_installed
PROOF=A/'stock_rank20class10_latest183_complete196_exact_routes_v3_20261011.json'
def installed():
 closed0,start0,_=prior_installed();data=read(PROOF)
 for p,d in data['input_sha256'].items():assert sha(p)==d,p
 def closed(n):return closed0(data['service_aliases'].get(n,n))
 def start(n,d,args,pins):
  if d in data['driver_wrappers']:d=data['driver_wrappers'][d]
  return start0(data['service_aliases'].get(n,n),d,args,{**pins,str(PROOF):sha(PROOF),str(Path(__file__)):sha(__file__)})
 import prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 as checks
 import handoff_ready_goss_full_execution_20261006 as launch
 checks.closed=closed;launch.start_service=start
 m=importlib.import_module('prepare_StockRank20Class10Embedding196_complete19_pipeline_v2_20261011');prior=m.source_paths
 m.source_paths=lambda:list(dict.fromkeys([*prior(),PROOF,Path(__file__),*[Path(p) for p in data['input_sha256']]]))
 return closed,start,data
def execute(driver):
 closed,start,data=installed();p=A/data['source_overrides'].get(driver,driver)
 if driver.startswith('seal_') or '_full_registration_' in driver or '_selected_candidate_feature_cache_' in driver:
  runpy.run_path(str(p),run_name='__main__');return
 m=importlib.import_module(p.stem)
 if hasattr(m,'closed'):m.closed=closed
 if hasattr(m,'start_service'):m.start_service=start
 m.main()
