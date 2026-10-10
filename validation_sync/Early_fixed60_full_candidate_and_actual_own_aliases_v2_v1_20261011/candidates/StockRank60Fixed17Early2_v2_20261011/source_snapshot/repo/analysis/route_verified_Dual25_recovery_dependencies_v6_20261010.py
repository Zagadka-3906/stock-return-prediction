"""Explicit terminal-service aliases; keep original failures, scores and scientific drivers immutable."""
from pathlib import Path
import sys,importlib,runpy,os
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed,closed
from handoff_ready_goss_full_execution_20261006 import start_service,retire
PROOF=A/'Dual25_verified_recovery_exact_dependency_aliases_v6_20261010.json'
def installed():
    proof=read(PROOF)
    for p,d in proof['input_sha256'].items():assert sha(p)==d,p
    aliases=proof['service_aliases'];drivers=proof['driver_wrappers']
    import prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 as checks
    import handoff_ready_goss_full_execution_20261006 as launch
    original_closed=checks.closed;original_start=launch.start_service
    def resolve_closed(name):return original_closed(aliases.get(name,name))
    def resolved_start(name,driver,args,pins):
        extra={str(PROOF):sha(PROOF),str(Path(__file__)):sha(__file__)}
        return original_start(aliases.get(name,name),drivers.get(driver,driver),args,{**pins,**extra})
    checks.closed=resolve_closed;launch.start_service=resolved_start
    # Actual wrapper and terminal recovery evidence must be part of every newly sealed registry.
    for name in proof['source_factories']:
        module=importlib.import_module(name);original=module.source_paths
        def augmented(original=original):return list(dict.fromkeys([*original(),PROOF,Path(__file__),*[Path(p) for p in proof['input_sha256']],*[A/n for n in drivers.values()]]))
        module.source_paths=augmented
    actual_run_path=runpy.run_path
    def resolve_candidate_path(path,*args,**kwargs):
        candidate_name=Path(path).name
        if candidate_name.startswith('prepare_') and '_selected_candidate_' in candidate_name and candidate_name in drivers:
            path=str(A/drivers[candidate_name])
        return actual_run_path(path,*args,**kwargs)
    runpy.run_path=resolve_candidate_path
    return resolve_closed
def execute(driver):
    assert allowed();resolve_closed=installed();source=A/driver
    count=int(os.environ.get('GIT_CONFIG_COUNT','0'))
    for i,(key,value) in enumerate((('http.proxy','http://127.0.0.1:7897'),('http.version','HTTP/1.1'))):os.environ[f'GIT_CONFIG_KEY_{count+i}']=key;os.environ[f'GIT_CONFIG_VALUE_{count+i}']=value
    os.environ['GIT_CONFIG_COUNT']=str(count+2)
    if driver.startswith('run_') and '_full_registration_' in driver:
        runpy.run_path(str(source),run_name='__main__');return
    module=importlib.import_module(source.stem)
    # Some original selected-candidate/qualifier modules define their own closed().
    if hasattr(module,'closed'):module.closed=resolve_closed
    if hasattr(module,'start_service'):
        import handoff_ready_goss_full_execution_20261006 as launch
        module.start_service=launch.start_service
    module.main()
