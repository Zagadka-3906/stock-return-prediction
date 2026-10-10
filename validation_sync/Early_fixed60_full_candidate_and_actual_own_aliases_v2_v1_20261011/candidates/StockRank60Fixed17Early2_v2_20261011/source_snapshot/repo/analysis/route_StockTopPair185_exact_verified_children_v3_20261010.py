from pathlib import Path
import sys,importlib,runpy
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha
def execute(driver):
    import route_actual_PairRank_native42_admission_v8_20261010 as parent
    parent.installed()
    import prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 as checks
    import handoff_ready_goss_full_execution_20261006 as launch
    assert checks.allowed()
    proof=A/'StockTopPair185_exact_child_sources_v3_20261010.json';data=read(proof)
    for p,d in data['input_sha256'].items():assert sha(p)==d,p
    previous=launch.start_service
    def start(name,source,args,pins):return previous(name,data['driver_wrappers'].get(source,source),args,{**pins,str(proof):sha(proof),str(Path(__file__)):sha(__file__)})
    launch.start_service=start
    actual_run=runpy.run_path
    def routed(path,*args,**kwargs):return actual_run(str(A/data['driver_wrappers'][Path(path).name]) if Path(path).name.startswith('prepare_') and Path(path).name in data['driver_wrappers'] else path,*args,**kwargs)
    runpy.run_path=routed
    source=A/driver
    if driver.startswith('seal_') or '_full_registration_' in driver:
        runpy.run_path(str(source),run_name='__main__');return
    module=importlib.import_module(source.stem)
    if hasattr(module,'closed'):module.closed=checks.closed
    if hasattr(module,'start_service'):module.start_service=start
    module.main()
