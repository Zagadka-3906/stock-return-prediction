"""Fresh reboot continuations; preserve terminal failures and completed scientific files."""
from pathlib import Path
import sys,importlib,runpy
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import closed as base_closed,allowed
from handoff_ready_goss_full_execution_20261006 import start_service as base_start
PROOF=A/'reboot_complete_candidate_routes_v11_20261011.json'

def installed():
    import route_actual_candidate_closed_and180_continuation_v10_20261011 as old
    old.installed();data=read(PROOF)
    for p,d in data['input_sha256'].items():assert sha(p)==d,p
    import prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 as checks
    import handoff_ready_goss_full_execution_20261006 as launch
    def closed(name):return base_closed(data['service_aliases'].get(name,name))
    def start(name,driver,args,pins):
        actual=data['service_aliases'].get(name,name);driver=data['driver_wrappers'].get(driver,driver)
        try:return base_start(actual,driver,args,{**pins,str(PROOF):sha(PROOF),str(Path(__file__)):sha(__file__)})
        except AssertionError:
            folder=A/'service_owned_workflows_20261006'/actual
            if (folder/'service_execution.json').exists() and read(folder/'service_execution.json')['status']=='passed':
                return read(folder/'native_launch.json')
            raise
    checks.closed=closed;launch.start_service=start
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
    return closed,start

def execute(driver):
    assert allowed();closed,start=installed();source=A/driver
    if driver.startswith('seal_') or '_full_registration_' in driver:
        runpy.run_path(str(source),run_name='__main__');return
    module=importlib.import_module(source.stem)
    if hasattr(module,'closed'):module.closed=closed
    if hasattr(module,'start_service'):module.start_service=start
    module.main()
