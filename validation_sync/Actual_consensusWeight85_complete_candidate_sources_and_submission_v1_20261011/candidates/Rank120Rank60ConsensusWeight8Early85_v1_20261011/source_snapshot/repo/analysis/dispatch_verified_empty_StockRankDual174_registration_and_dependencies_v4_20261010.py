"""Fresh dispatch after verified empty registry, with all current service dependencies resolved."""
from pathlib import Path
import sys
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
from handoff_ready_goss_full_execution_20261006 import start_service,retire
def save(name,text):
    p=A/name;assert not p.exists(),p;compile(text,str(p),'exec');p.write_text(text,encoding='utf8',newline='\n');return p
def main():
    assert allowed();oldpath=A/'Dual25_verified_recovery_exact_dependency_aliases_v2_20261010.json';old=read(oldpath)
    from stock_rank_dual174_storage_v1_20261010 import empty
    empty(A/'optimization_20261003_r174');empty(A.parent/'candidates/optimization_20261003_r174')
    runtime=A/'run_StockRankDual174_full_registration_v4_20261010.py';assert runtime.exists()
    assert not Path('E:/赛题五_本机临时/第174轮_20261010/frozen_external_capsule_publication_guard_registry_recovery_v4.json').exists()
    brokerold=A/'route_verified_Dual25_recovery_dependencies_v3_20261010.py';broker=save('route_verified_Dual25_recovery_dependencies_v4_20261010.py',brokerold.read_text(encoding='utf8').replace('Dual25_verified_recovery_exact_dependency_aliases_v3_20261010.json','Dual25_verified_recovery_exact_dependency_aliases_v4_20261010.json'))
    aliases=dict(old['service_aliases']);finishname='StockRankDual174_verified_candidate_registration_recovery_v3_20261010'
    for key,value in list(aliases.items()):
        if value=='StockRankDual174_verified_candidate_registration_recovery_v1_20261010':aliases[key]=finishname
    aliases['StockRankDual174_verified_candidate_registration_recovery_v1_20261010']=finishname
    inverse={v:k for p in [oldpath,A/'Dual25_verified_recovery_exact_dependency_aliases_v1_20261010.json'] for k,v in read(p)['driver_wrappers'].items()}
    existing={};selected={};root=A/'service_owned_workflows_20261006'
    # Inspect real native handles, including publishers omitted by old observers.
    for folder in root.iterdir():
        if not folder.is_dir() or not (folder/'job_definition.json').exists() or not (folder/'native_launch.json').exists():continue
        name=folder.name
        if 'progress' in name or 'main_publisher' in name or name.startswith('StockRankDual174'):continue
        row=read(folder/'native_launch.json');terminal=read(folder/'service_execution.json') if (folder/'service_execution.json').exists() else {}
        if not owned(row) and not (terminal.get('status')=='failed' and terminal.get('at_local','')>='2026-10-10T21:07:00'):continue
        definition=read(folder/'job_definition.json');driver=Path(definition['driver']).name;original=inverse.get(driver,driver)
        source=A/original
        if source.is_file():existing[name]=(original,row,source.read_text(encoding='utf8'))
    while True:
        before=len(selected)
        for name,(driver,row,text) in existing.items():
            if name not in selected and any(key in text for key in aliases):selected[name]=(driver,row)
        for name in selected:
            actual=name.removesuffix('_20261010')+'_dispatch_v4_20261010';aliases[name]=actual
            for original,value in old['service_aliases'].items():
                if value==name:aliases[original]=actual
        if len(selected)==before:break
    # Canonical dependencies must refer directly to the latest verified handle.
    for key in list(aliases):
        value=aliases[key];seen={key}
        while value in aliases and aliases[value]!=value:
            assert value not in seen;seen.add(value);value=aliases[value]
        aliases[key]=value
    inputs=[Path(__file__),oldpath,brokerold,broker,runtime,A/'StockRankDual174_partial_registry_lossless_preservation_v1_20261010.json'];drivers={};wrappers=[]
    originals=set(old['driver_wrappers'])|{driver for driver,row in selected.values()}|{runtime.name}
    for driver in sorted(originals):
        if driver.startswith('run_StockRankDual174_full_registration_') and driver!=runtime.name:continue
        p=A/driver;inputs.append(p);wrapper=p.with_name(p.stem+'_after_registry_dispatch_v4.py')
        body="from pathlib import Path\nimport sys\nA=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]\nfrom route_verified_Dual25_recovery_dependencies_v4_20261010 import execute\nif __name__=='__main__':execute("+repr(driver)+")\n"
        wrappers.append(save(wrapper.name,body));drivers[driver]=wrapper.name
    for v in (2,3):drivers[f'run_StockRankDual174_full_registration_v{v}_20261010.py']=drivers[runtime.name]
    oldfinish=A/'finish_StockRankDual174_verified_registration_recovery_v2_20261010.py';text=oldfinish.read_text(encoding='utf8').replace('route_verified_Dual25_recovery_dependencies_v3','route_verified_Dual25_recovery_dependencies_v4').replace('full_registration_recovery_v2','full_registration_recovery_v3').replace('run_StockRankDual174_full_registration_v4_20261010_after_registry_recovery_v3','run_StockRankDual174_full_registration_v4_20261010_after_registry_dispatch_v4')
    finish=save('finish_StockRankDual174_verified_registration_recovery_v3_20261010.py',text);inputs += [oldfinish,finish]
    proof=A/'Dual25_verified_recovery_exact_dependency_aliases_v4_20261010.json';create(proof,{'status':'fresh_dispatch_after_verified_empty_preserved_registry_with_fresh_guard_v4_and_explicit_actual_service_dependencies','service_aliases':aliases,'driver_wrappers':drivers,'source_factories':old['source_factories'],'selected_helpers':sorted(selected),'input_sha256':{str(p):sha(p) for p in dict.fromkeys([*inputs,*wrappers])},'new_fits':0,'new_quality_scores':0,'new_inference':False,'no_terminal_status_forged':True,'test_labels_read':False})
    for name,(driver,row) in selected.items():
        if owned(row):retire(row,'Replace verified childless wait with direct latest registration-only recovery handle; actual controls and scientific source files retained')
    tasks=[(finishname,finish.name)]+[(aliases[name],drivers[driver]) for name,(driver,row) in sorted(selected.items())]
    for name,n in tasks:
        assert allowed();row=start_service(name,n,[],{str(A/n):sha(A/n),str(proof):sha(proof)});create(A/(name+'_activation.json'),row)
    print({'registration_only_v4_dispatched':True,'sealed_candidate_not_recomputed':True,'dependency_helpers':len(selected)},flush=True)
if __name__=='__main__':main()
