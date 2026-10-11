"""Correct actual116 runtime provenance before registration; keep all eight frozen originals."""
from pathlib import Path
import ast
import sys
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis'
sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from handoff_ready_goss_full_execution_20261006 import start_service

def new_file(name,text):
    p=A/name;assert not p.exists();compile(text,str(p),'exec')
    with p.open('x',encoding='utf8',newline='\n') as stream:stream.write(text)
    return p

def main():
    old=A/'service_owned_workflows_20261006/flagged_HGB88_round116_full_registration'
    assert not owned(read(old/'native_launch.json')) and read(old/'service_execution.json')['status']=='failed'
    assert not (A/'optimization_20261003_r116').exists() and not (ROOT/'candidates/optimization_20261003_r116').exists()
    bad='run_protected_upper_pool_HGB66_round116_full_registration_20261007.py'
    driver_name='run_flagged_HGB88_round116_full_registration_v4_20261007.py'
    publisher_name='publish_flagged_HGB88_round116_full_validation_v2_20261007.py'
    old_registry=A/'register_flagged_HGB88_round116_artifacts_20261007.py'
    text=old_registry.read_text(encoding='utf8');assert text.count(bad)==1
    text=text.replace(bad,driver_name).replace('publish_flagged_HGB88_round116_full_validation_20261007.py',publisher_name)
    needle="    pins = {**read(RELEASE / 'protocol.json')['input_sha256']";assert text.count(needle)==1
    extra="    sources += [A/'recover_flagged_HGB88_round116_source_paths_v2_20261007.py', A/'flagged_HGB88_round116_actual_source_path_preflight_v2_20261007.json', A/'register_flagged_HGB88_round116_artifacts_20261007.py', A/'run_flagged_HGB88_round116_full_registration_v3_20261007.py', *list((A/'service_owned_workflows_20261006/flagged_HGB88_round116_full_registration').glob('*.json')), A/'service_owned_workflows_20261006/flagged_HGB88_round116_full_registration/stderr.log']\n"
    text=text.replace(needle,extra+needle)
    registry=new_file('register_flagged_HGB88_round116_artifacts_v2_20261007.py',text)
    old_publisher=A/'publish_flagged_HGB88_round116_full_validation_20261007.py';text=old_publisher.read_text(encoding='utf8')
    assert text.count(bad)==1;text=text.replace(bad,driver_name)
    needle='    for path in extra:';assert text.count(needle)==1
    text=text.replace(needle,"    extra += [A/'register_flagged_HGB88_round116_artifacts_v2_20261007.py', A/'recover_flagged_HGB88_round116_source_paths_v2_20261007.py', A/'flagged_HGB88_round116_actual_source_path_preflight_v2_20261007.json', *list((A/'service_owned_workflows_20261006/flagged_HGB88_round116_full_registration').glob('*.json')), A/'service_owned_workflows_20261006/flagged_HGB88_round116_full_registration/stderr.log']\n"+needle)
    publisher=new_file(publisher_name,text)
    old_driver=A/'run_flagged_HGB88_round116_full_registration_v3_20261007.py';text=old_driver.read_text(encoding='utf8')
    text=text.replace('flagged_HGB88_round116_actual_registration_v3_20261007','flagged_HGB88_round116_actual_registration_v4_20261007')
    text=text.replace('    prepare_sources()',"    prep=read(A/'flagged_HGB88_round116_source_preparation_v3_20261007.json')\n    assert prep['status']=='passed_actual88_sealed_candidate_registry_and_original_QA27_source_routes'\n    for p,digest in prep['input_sha256'].items():assert sha(p)==digest,p")
    text=text.replace('from register_flagged_HGB88_round116_artifacts_20261007 import main as register','from register_flagged_HGB88_round116_artifacts_v2_20261007 import main as register')
    text=text.replace('from publish_flagged_HGB88_round116_full_validation_20261007 import main as github','from publish_flagged_HGB88_round116_full_validation_v2_20261007 import main as github')
    driver=new_file(driver_name,text)
    # Execute only the concrete source-list expression, before any registration or file alias.
    import importlib.util
    spec=importlib.util.spec_from_file_location('actual116_registry_source_preflight',registry)
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    function=next(n for n in ast.parse(registry.read_text(encoding='utf8')).body if isinstance(n,ast.FunctionDef) and n.name=='main')
    assignment=next(n for n in function.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='sources' for t in n.targets))
    ns=dict(module.__dict__);exec(compile(ast.fix_missing_locations(ast.Module(body=[assignment],type_ignores=[])),str(registry),'exec'),ns)
    assert all(Path(p).is_file() for p in ns['sources']),[str(p) for p in ns['sources'] if not Path(p).is_file()]
    ready=read(A/'flagged_HGB_small_amplitude88_selected_release_v4_20261007/selected_candidate_ready_for_registration.json')
    pins={str(p):sha(p) for p in [Path(__file__),old_registry,registry,old_publisher,publisher,old_driver,driver,*ns['sources'],old/'service_execution.json',old/'stderr.log']}
    proof=A/'flagged_HGB88_round116_actual_source_path_preflight_v2_20261007.json'
    create(proof,{'status':'passed_actual_all_concrete116_registry_source_paths_before_any_alias_or_registration',
        'input_sha256':pins,'actual_registry_sources':len(ns['sources']),'all_original_eight_frozen_sources_preserved':True,
        'actual_selected_native_models':ready['actual_saved_native_models'],'original_selected_freeze_and_manifest_preserved':True,
        'old_failure_preserved':True,'new_native_fits':0,'new_quality_scores':0,'test_labels_read':False})
    pins[str(proof)]=sha(proof)
    row=start_service('flagged_HGB88_round116_full_registration_v2',driver.name,[],pins)
    create(A/'flagged_HGB88_round116_source_path_recovery_actual_launch_v2_20261007.json',{'input_sha256':pins,'actual_native_launch':row,'new_native_fits':0,'new_quality_scores':0})
    print({'status':'launched_actual116_recovery','worker_pid':row['owned_worker_pid']},flush=True)

if __name__=='__main__':main()
