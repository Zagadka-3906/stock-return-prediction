"""Resume preserved empty registration outputs with fresh exclusive sidecar paths."""
from pathlib import Path
import sys
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
from handoff_ready_goss_full_execution_20261006 import start_service
def save(name,text):
    p=A/name;assert not p.exists(),p;compile(text,str(p),'exec');p.write_text(text,encoding='utf8',newline='\n');return p
def main():
    assert allowed();prior=A/'Dual25_verified_recovery_exact_dependency_aliases_v2_20261010.json';old=read(prior)
    failure_folder=A/'service_owned_workflows_20261006/StockRankDual174_full_registration_recovery_v1_20261010'
    failure=read(failure_folder/'service_execution.json');assert failure['status']=='failed' and failure['failure'].startswith('FileExistsError:') and 'frozen_external_capsule_publication_guard_v3' in failure['failure'] and not owned(read(failure_folder/'native_launch.json'))
    from stock_rank_dual174_storage_v1_20261010 import empty
    empty(A/'optimization_20261003_r174');empty(A.parent/'candidates/optimization_20261003_r174')
    original=A/'run_StockRankDual174_full_registration_v3_20261010.py';text=original.read_text(encoding='utf8').replace('frozen_external_capsule_publication_guard_v3.json','frozen_external_capsule_publication_guard_registry_recovery_v4.json').replace('late_snapshot_encoder_import.json','late_snapshot_encoder_import_registry_recovery_v4.json')
    runtime=save('run_StockRankDual174_full_registration_v4_20261010.py',text)
    broker_old=A/'route_verified_Dual25_recovery_dependencies_v2_20261010.py';broker=save('route_verified_Dual25_recovery_dependencies_v3_20261010.py',broker_old.read_text(encoding='utf8').replace('Dual25_verified_recovery_exact_dependency_aliases_v2_20261010.json','Dual25_verified_recovery_exact_dependency_aliases_v3_20261010.json'))
    aliases=dict(old['service_aliases']);oldfinish='StockRankDual174_verified_candidate_registration_recovery_v1_20261010';newfinish='StockRankDual174_verified_candidate_registration_recovery_v2_20261010'
    for key,value in list(aliases.items()):
        if value==oldfinish:aliases[key]=newfinish
    aliases[oldfinish]=newfinish
    drivers={};wrappers=[];inputs=[Path(__file__),prior,broker_old,broker,original,runtime,failure_folder/'service_execution.json',A/'StockRankDual174_partial_registry_lossless_preservation_v1_20261010.json']
    for driver in sorted(set(old['driver_wrappers'])|{runtime.name}):
        if driver.startswith('run_StockRankDual174_full_registration_'):continue
        p=A/driver;inputs.append(p);wrapper=p.with_name(p.stem+'_after_registry_recovery_v3.py')
        body="from pathlib import Path\nimport sys\nA=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]\nfrom route_verified_Dual25_recovery_dependencies_v3_20261010 import execute\nif __name__=='__main__':execute("+repr(driver)+")\n"
        wrappers.append(save(wrapper.name,body));drivers[driver]=wrapper.name
    wrapper=save(runtime.stem+'_after_registry_recovery_v3.py',"from pathlib import Path\nimport sys\nA=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]\nfrom route_verified_Dual25_recovery_dependencies_v3_20261010 import execute\nif __name__=='__main__':execute('"+runtime.name+"')\n")
    wrappers.append(wrapper)
    for v in (2,3,4):drivers[f'run_StockRankDual174_full_registration_v{v}_20261010.py']=wrapper.name
    finishold=A/'finish_StockRankDual174_verified_registration_recovery_v1_20261010.py';text=finishold.read_text(encoding='utf8').replace('route_verified_Dual25_recovery_dependencies_v2','route_verified_Dual25_recovery_dependencies_v3').replace('full_registration_recovery_v1','full_registration_recovery_v2').replace('run_StockRankDual174_full_registration_v3_20261010_after_registry_recovery_v2','run_StockRankDual174_full_registration_v4_20261010_after_registry_recovery_v3')
    finish=save('finish_StockRankDual174_verified_registration_recovery_v2_20261010.py',text);inputs += [finishold,finish]
    proof=A/'Dual25_verified_recovery_exact_dependency_aliases_v3_20261010.json'
    create(proof,{'status':'explicit_registration_only_resume_with_fresh_sidecars_preserved_partial_outputs_and_sealed_candidate','service_aliases':aliases,'driver_wrappers':drivers,'source_factories':old['source_factories'],'selected_helpers':old['selected_helpers'],'input_sha256':{str(p):sha(p) for p in dict.fromkeys([*inputs,*wrappers])},'original_recovery_proof_sha256':sha(prior),'new_fits':0,'new_quality_scores':0,'new_inference':False,'no_terminal_status_forged':True,'test_labels_read':False})
    tasks=[(newfinish,finish.name)]
    for old_service in old['selected_helpers']:
        name=old['service_aliases'][old_service];folder=A/'service_owned_workflows_20261006'/name
        assert not folder.exists(),name
        original_folder=A/'service_owned_workflows_20261006'/old_service;driver=Path(read(original_folder/'job_definition.json')['driver']).name
        inverse={v:k for k,v in read(A/'Dual25_verified_recovery_exact_dependency_aliases_v1_20261010.json')['driver_wrappers'].items()};driver=inverse.get(driver,driver)
        tasks.append((name,drivers[driver]))
    for name,n in tasks:
        assert allowed();row=start_service(name,n,[],{str(A/n):sha(A/n),str(proof):sha(proof)});create(A/(name+'_activation.json'),row)
    print({'registration_only_v4_started':True,'sealed_candidate_and_actual_scores_unchanged':True,'dependencies_dispatched':len(tasks)-1},flush=True)
if __name__=='__main__':main()
