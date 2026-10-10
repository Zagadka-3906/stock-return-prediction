"""Preserve partial registry; resume only registration of the already sealed actual candidate."""
from pathlib import Path
import sys,os,importlib
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed,closed
from handoff_ready_goss_full_execution_20261006 import start_service,retire
def save(name,text):
    p=A/name;assert not p.exists(),p;compile(text,str(p),'exec');p.write_text(text,encoding='utf8',newline='\n');return p
def main():
    assert allowed();oldproof=A/'Dual25_verified_recovery_exact_dependency_aliases_v1_20261010.json';previous=read(oldproof)
    runtime_job=A/'service_owned_workflows_20261006/StockRankDual174_round174_full_registration_v1_20261010'
    failure=read(runtime_job/'service_execution.json');assert failure['status']=='failed' and failure['failure']=="KeyError: 'name'" and not owned(read(runtime_job/'native_launch.json'))
    ready=A/'StockRankDual174_selected_release_v1_20261010/selected_candidate_ready_for_registration.json';assert read(ready)['sealed_candidate_complete'] and read(ready)['new_inference_claimed']
    source_candidate=Path(read(ready)['source_candidate']);manifest=source_candidate/'manifest.json';sealed_sha=sha(manifest)
    original=A/'register_StockRankDual174_round174_artifacts_v2_20261010.py';text=original.read_text(encoding='utf8');needle="(f['name']+'_screen_v1_20261010')";assert text.count(needle)==1
    text=text.replace(needle,"f['folder']")
    registration=save('register_StockRankDual174_round174_artifacts_v3_20261010.py',text)
    runtime_original=A/'run_StockRankDual174_full_registration_v2_20261010.py'
    runtime=save('run_StockRankDual174_full_registration_v3_20261010.py',runtime_original.read_text(encoding='utf8').replace(original.stem,registration.stem))
    # Verify exact known physical E targets before moving any partial output. Sealed candidate stays intact.
    base=Path('E:/赛题五_本机临时/第174轮_20261010').resolve();backup=base/'failed_registry_before_protocol_v1';assert not backup.exists();backup.mkdir()
    moved=[]
    from stock_rank_dual174_storage_v1_20261010 import OUTPUTS
    for logical in [A.parent/'analysis/optimization_20261003_r174',A.parent/'candidates/optimization_20261003_r174']:
        physical=OUTPUTS[logical].resolve();assert logical.resolve()==physical and physical.is_relative_to(base) and physical.parent==base
        destination=backup/physical.name;assert destination.resolve().is_relative_to(backup.resolve()) and not destination.exists()
        before={p.relative_to(physical).as_posix():{'sha256':sha(p),'bytes':p.stat().st_size} for p in physical.rglob('*') if p.is_file()}
        os.rename(physical,destination);physical.mkdir()
        for relative,row in before.items():assert sha(destination/relative)==row['sha256'] and (destination/relative).stat().st_size==row['bytes']
        assert not any(logical.iterdir());moved.append({'physical':str(physical),'preserved_backup':str(destination),'files':before})
    assert sha(manifest)==sealed_sha
    archive=A/'StockRankDual174_partial_registry_lossless_preservation_v1_20261010.json';create(archive,{'status':'preserved_failed_partial_registry_all_file_bytes_and_sealed_candidate_unchanged','original_failure':failure,'moved':moved,'sealed_manifest_sha256':sealed_sha,'source_candidate':str(source_candidate),'new_fits':0,'new_quality_scores':0,'new_inference':False})
    # New runtime broker retains the first recovery proof and replaces only exact dependency entry points.
    broker_original=A/'route_verified_Dual25_recovery_dependencies_v1_20261010.py';broker=save('route_verified_Dual25_recovery_dependencies_v2_20261010.py',broker_original.read_text(encoding='utf8').replace('Dual25_verified_recovery_exact_dependency_aliases_v1_20261010.json','Dual25_verified_recovery_exact_dependency_aliases_v2_20261010.json'))
    newproof=A/'Dual25_verified_recovery_exact_dependency_aliases_v2_20261010.json';aliases=dict(previous['service_aliases']);drivers={};wrappers=[];inputs=[Path(__file__),oldproof,archive,original,registration,runtime_original,runtime,broker,ready,manifest,runtime_job/'service_execution.json']
    original174='StockRankDual174_complete44_family_v2_20261010';old174=aliases[original174];finishname='StockRankDual174_verified_candidate_registration_recovery_v1_20261010'
    aliases[original174]=aliases[old174]=finishname
    state=read(A/'optimization_live_progress_v73_20261010.json');jobs={};launches={};inverse={v:k for k,v in previous['driver_wrappers'].items()}
    excluded={original174,old174,'StockRankDual174_round174_full_registration_v1_20261010'}
    for name in set(state['services'])|set(previous['service_aliases'].values()):
        folder=A/'service_owned_workflows_20261006'/name
        if name in excluded or 'progress' in name or not (folder/'job_definition.json').exists():continue
        definition=read(folder/'job_definition.json');launch=read(folder/'native_launch.json');terminal=read(folder/'service_execution.json') if (folder/'service_execution.json').exists() else {}
        if owned(launch) or (terminal.get('status')=='failed' and terminal.get('at_local','')>='2026-10-10T21:09:00'):
            driver=Path(definition['driver']).name;raw_driver=inverse.get(driver,driver);jobs[name]=(raw_driver,definition);launches[name]=launch
    selected=set()
    while True:
        before=len(selected)
        for name,(driver,_) in jobs.items():
            if name in selected:continue
            raw=(A/driver).read_text(encoding='utf8')
            if any(key in raw for key in aliases):selected.add(name)
        for name in selected:
            new=name.removesuffix('_20261010')+'_registry_recovery_v2_20261010';aliases[name]=new
            for original_name,actual in previous['service_aliases'].items():
                if actual==name:aliases[original_name]=new
        if len(selected)==before:break
    all_drivers=set(previous['driver_wrappers'])|{jobs[n][0] for n in selected}|{runtime.name}
    for driver in sorted(all_drivers):
        if driver==runtime_original.name:continue
        p=A/driver;assert p.is_file();inputs.append(p);wrapper=p.with_name(p.stem+'_after_registry_recovery_v2.py')
        body="from pathlib import Path\nimport sys\nA=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]\nfrom route_verified_Dual25_recovery_dependencies_v2_20261010 import execute\nif __name__=='__main__':execute("+repr(driver)+")\n"
        wrappers.append(save(wrapper.name,body));drivers[driver]=wrapper.name
    # Preserve old runtime sources; only the new registration-only driver can be launched.
    drivers[runtime_original.name]=drivers[runtime.name]
    finish=save('finish_StockRankDual174_verified_registration_recovery_v1_20261010.py',"""from pathlib import Path
import sys
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from route_verified_Dual25_recovery_dependencies_v2_20261010 import installed
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
def main():
    assert allowed();closed=installed()
    from handoff_ready_goss_full_execution_20261006 import start_service
    name='StockRankDual174_full_registration_recovery_v1_20261010';p=A/'run_StockRankDual174_full_registration_v3_20261010_after_registry_recovery_v2.py'
    row=start_service(name,p.name,[],{str(p):sha(p)});create(A/(name+'_activation.json'),row);closed(name)
    receipt=read(A/'github_validation_sync_main_20261005/round174_receipt.json');assert receipt['status']=='pushed_and_remote_head_verified' and receipt['scored_records']==44
    assert read(A/'optimization_20261003_r174/full_registration_execution.json')['status']=='passed'
    assert allowed()
    from maintain_best_fully_qualified_submission_delivery_v3_20261010 import update
    update()
    create(A/'StockRankDual174_registry_recovery_complete_v1_20261010.json',{'status':'passed_actual44_QA85_main_and_delivery_after_exact_partial_registry_preservation','receipt':receipt,'new_fits':0,'new_quality_scores':0,'new_inference':False})
if __name__=='__main__':main()
""")
    inputs.append(finish)
    factories=list(dict.fromkeys([*previous['source_factories'],'prepare_stock_rank_dual174_full_registry_sources_v2_20261010','prepare_StockRank20Embedding180_complete48_pipeline_v1_20261010']))
    create(newproof,{'status':'explicit_verified_candidate_registration_only_recovery_original_failures_and_partial_bytes_retained','service_aliases':aliases,'driver_wrappers':drivers,'source_factories':factories,'selected_helpers':sorted(selected),'input_sha256':{str(p):sha(p) for p in dict.fromkeys([*inputs,*wrappers])},'original_recovery_proof_sha256':sha(oldproof),'sealed_candidate_manifest_unchanged':sealed_sha,'new_fits':0,'new_quality_scores':0,'no_terminal_status_forged':True,'test_labels_read':False})
    for name in selected:
        row=launches[name]
        if owned(row):retire(row,'Replace verified childless dependency wait with exact registration-only recovery; retain original scientific drivers and all completed native controls')
    tasks=[(finishname,finish.name)]+[(aliases[name],drivers[jobs[name][0]]) for name in sorted(selected)]
    for name,n in tasks:
        assert allowed();row=start_service(name,n,[],{str(A/n):sha(A/n),str(newproof):sha(newproof)});create(A/(name+'_activation.json'),row)
    print({'sealed_candidate_not_recomputed':True,'partial_registry_preserved':True,'routed_helpers':len(selected),'actual44_registration_recovery_started':True},flush=True)
if __name__=='__main__':main()
