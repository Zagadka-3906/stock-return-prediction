"""Fresh identities after the actual183 cardinality failure; preserve frozen source1 and all completed scores."""
from pathlib import Path
import sys,importlib,runpy,builtins
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import closed as base_closed,allowed
from start_fast_completed_owned_service_v1_20261011 import start_service as base_start
PROOF=A/'unified_completed_parent_shared_publication36_routes_v1_20261011.json'

def installed():
    import route_complete_registered180_v13_20261011 as old
    old.installed();data=read(PROOF)
    for p,d in data['input_sha256'].items():assert sha(p)==d,p
    import prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 as checks
    import handoff_ready_goss_full_execution_20261006 as launch
    import start_fast_completed_owned_service_v1_20261011 as fast
    def actual(name):
        seen=set()
        while name in data['service_aliases'] and data['service_aliases'][name]!=name:
            assert name not in seen;seen.add(name);name=data['service_aliases'][name]
        return name
    def closed(name):return base_closed(actual(name))
    def start(name,driver,args,pins):
        return base_start(actual(name),data['driver_wrappers'].get(driver,driver),args,
                          {**pins,str(PROOF):sha(PROOF),str(Path(__file__)):sha(__file__)})
    checks.closed=closed;launch.start_service=start;fast.start_service=start
    legacy=importlib.import_module('qualify_stock_rank20_embedding85_selected_native14_v5_20261010')
    fixed=importlib.import_module('qualify_stock_rank20_embedding85_selected_native14_v6_20261011')
    legacy.OUT=fixed.OUT
    for name in data['source_factories']:
        module=importlib.import_module(name);previous=module.source_paths
        def paths(previous=previous):return list(dict.fromkeys([*previous(),PROOF,Path(__file__),*[Path(p) for p in data['input_sha256']]]))
        module.source_paths=paths
    before=runpy.run_path
    def routed(path,*args,**kwargs):
        name=Path(path).name
        if name.startswith('prepare_') and '_selected_candidate_' in name and name in data['driver_wrappers']:
            path=str(A/data['driver_wrappers'][name])
        return before(path,*args,**kwargs)
    runpy.run_path=routed
    previous_import=builtins.__import__
    def importing(name,globals=None,locals=None,fromlist=(),level=0):
        if level==0 and name in data['module_aliases']:
            return previous_import(data['module_aliases'][name],globals,locals,fromlist,level)
        if level==0 and name=='normalize_completed_stock_toppair_embedding_complete48_after184_v6_20261010':
            return previous_import('normalize_completed_stock_toppair_embedding_complete48_after184_v8_20261010',globals,locals,fromlist,level)
        if level==0 and name=='register_StockRank20Embedding183_round183_artifacts_v3_20261010':
            return previous_import('register_StockRank20Embedding183_round183_artifacts_v4_20261011',globals,locals,fromlist,level)
        return previous_import(name,globals,locals,fromlist,level)
    builtins.__import__=importing
    return closed,start,data

def execute(driver):
    assert allowed();closed,start,data=installed()
    source=A/data['actual_source_overrides'].get(driver,driver)
    if driver.startswith('seal_') or '_full_registration_' in driver:
        runpy.run_path(str(source),run_name='__main__');return
    module=importlib.import_module(source.stem)
    if hasattr(module,'closed'):module.closed=closed
    if hasattr(module,'start_service'):module.start_service=start
    module.main()
