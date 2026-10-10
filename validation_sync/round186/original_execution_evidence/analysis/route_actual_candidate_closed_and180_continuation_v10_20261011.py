"""Extend verified routes with the omitted180 candidate callback and explicit failed-helper continuations."""
from pathlib import Path
import sys,importlib,runpy
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha
PROOF=A/'actual_candidate_closed180_continuation_routes_v10_20261011.json'

def installed():
    import route_PairTop184185_complete_references_v9_20261010 as parent
    parent.installed()
    import prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 as checks
    import handoff_ready_goss_full_execution_20261006 as launch
    data=read(PROOF)
    for p,d in data['input_sha256'].items():assert sha(p)==d,p
    before_closed=checks.closed;before_start=launch.start_service
    def closed(name):return before_closed(data['service_aliases'].get(name,name))
    def start(name,driver,args,pins):
        return before_start(data['service_aliases'].get(name,name),data['driver_wrappers'].get(driver,driver),args,
            {**pins,str(PROOF):sha(PROOF),str(Path(__file__)):sha(__file__)})
    checks.closed=closed;launch.start_service=start
    for name in data['source_factories']:
        module=importlib.import_module(name);original=module.source_paths
        def augmented(original=original):return list(dict.fromkeys([*original(),PROOF,Path(__file__),*[Path(p) for p in data['input_sha256']],*[A/n for n in data['driver_wrappers'].values()]]))
        module.source_paths=augmented
    before_run=runpy.run_path
    def routed(path,*args,**kwargs):
        name=Path(path).name
        if name.startswith('prepare_') and '_selected_candidate_' in name and name in data['driver_wrappers']:path=str(A/data['driver_wrappers'][name])
        return before_run(path,*args,**kwargs)
    runpy.run_path=routed
    return closed,start

def execute(driver):
    closed,start=installed()
    from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
    assert allowed();source=A/driver
    if driver.startswith('seal_') or '_full_registration_' in driver:
        runpy.run_path(str(source),run_name='__main__');return
    module=importlib.import_module(source.stem)
    if hasattr(module,'closed'):module.closed=closed
    if hasattr(module,'start_service'):module.start_service=start
    module.main()
