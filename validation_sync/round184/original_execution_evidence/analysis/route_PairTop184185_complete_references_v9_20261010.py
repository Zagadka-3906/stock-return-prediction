from pathlib import Path
import sys,importlib,runpy
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha
PROOF=A/'PairTop184185_complete_reference_routes_v9_20261010.json'
def installed():
    import route_actual_PairRank_native42_admission_v8_20261010 as parent
    parent.installed()
    import prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 as checks
    import handoff_ready_goss_full_execution_20261006 as launch
    data=read(PROOF)
    for p,d in data['input_sha256'].items():assert sha(p)==d,p
    previous_closed=checks.closed;previous_start=launch.start_service
    def closed(name):return previous_closed(data['service_aliases'].get(name,name))
    def start(name,driver,args,pins):return previous_start(data['service_aliases'].get(name,name),data['driver_wrappers'].get(driver,driver),args,{**pins,str(PROOF):sha(PROOF),str(Path(__file__)):sha(__file__)})
    checks.closed=closed;launch.start_service=start
    # Every original version that the preserved184 callers might import gains the actual complete supplement.
    for name in data['source_factories']:
        module=importlib.import_module(name);original=module.source_paths
        def augmented(original=original):return list(dict.fromkeys([*original(),PROOF,Path(__file__),*[Path(p) for p in data['input_sha256']],*[A/n for n in data['driver_wrappers'].values()]]))
        module.source_paths=augmented
    previous_run=runpy.run_path
    def routed(path,*args,**kwargs):return previous_run(str(A/data['driver_wrappers'][Path(path).name]) if Path(path).name.startswith('prepare_') and Path(path).name in data['driver_wrappers'] else path,*args,**kwargs)
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
