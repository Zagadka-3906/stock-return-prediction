"""Route every unstarted future child, including cache wrappers and own closed() candidates."""
from pathlib import Path
import sys
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
from handoff_ready_goss_full_execution_20261006 import start_service,retire
def save(name,text):
    p=A/name;assert not p.exists();compile(text,str(p),'exec');p.write_text(text,encoding='utf8',newline='\n');return p
def main():
    assert allowed();oldpath=A/'Dual25_verified_recovery_exact_dependency_aliases_v4_20261010.json';old=read(oldpath);aliases=dict(old['service_aliases'])
    inverse={v:k for ver in (1,2,4) for k,v in read(A/f'Dual25_verified_recovery_exact_dependency_aliases_v{ver}_20261010.json')['driver_wrappers'].items()}
    jobs={};root=A/'service_owned_workflows_20261006'
    for folder in root.iterdir():
        if not folder.is_dir() or not (folder/'native_launch.json').exists() or not (folder/'job_definition.json').exists():continue
        name=folder.name
        if 'progress' in name or name.startswith('StockRankDual174') or 'native42_and_after174_fast17_queue' in name:continue
        row=read(folder/'native_launch.json')
        if not owned(row):continue
        driver=Path(read(folder/'job_definition.json')['driver']).name;original=inverse.get(driver,driver);p=A/original
        if p.is_file():jobs[name]=(original,row,p.read_text(encoding='utf8'))
    selected={}
    while True:
        before=len(selected)
        for name,(driver,row,text) in jobs.items():
            if name not in selected and any(key in text for key in aliases):selected[name]=(driver,row)
        for name in selected:aliases[name]=name.removesuffix('_20261010')+'_future_children_v5_20261010'
        if len(selected)==before:break
    for key in list(aliases):
        value=aliases[key];seen={key}
        while value in aliases and aliases[value]!=value:
            assert value not in seen;seen.add(value);value=aliases[value]
        aliases[key]=value
    original=A/'route_verified_Dual25_recovery_dependencies_v4_20261010.py';text=original.read_text(encoding='utf8').replace('Dual25_verified_recovery_exact_dependency_aliases_v4_20261010.json','Dual25_verified_recovery_exact_dependency_aliases_v5_20261010.json')
    needle='    return resolve_closed\n';assert text.count(needle)==1
    patch="    actual_run_path=runpy.run_path\n    def resolve_candidate_path(path,*args,**kwargs):\n        candidate_name=Path(path).name\n        if candidate_name.startswith('prepare_') and '_selected_candidate_' in candidate_name and candidate_name in drivers:\n            path=str(A/drivers[candidate_name])\n        return actual_run_path(path,*args,**kwargs)\n    runpy.run_path=resolve_candidate_path\n"
    text=text.replace(needle,patch+needle);broker=save('route_verified_Dual25_recovery_dependencies_v5_20261010.py',text)
    # Native/model outputs are exclusive and remain untouched. Future registration, sealing and cache entry points are all pinned now.
    extra=['run_StockTop10Embedding175_full_registration_v3_20261010.py','seal_StockTop10Embedding175_selected_candidate_v1_20261010.py','run_StockTop10Embedding176_full_registration_v3_20261010.py','seal_StockTop10Embedding176_selected_candidate_v1_20261010.py','run_StockRank5Embedding177_full_registration_v4_20261010.py','seal_StockRank5Embedding177_selected_candidate_v1_20261010.py','run_StockForward5Embedding178_full_registration_v4_20261010.py','run_StockForward5Embedding178_selected_candidate_feature_cache_v5_20261010.py','seal_StockForward5Embedding178_selected_candidate_v1_20261010.py','run_StockForward20Embedding179_full_registration_v5_20261010.py','run_StockForward20Embedding179_selected_candidate_feature_cache_v6_20261010.py','seal_StockForward20Embedding179_selected_candidate_v2_20261010.py','run_StockRank20Embedding180_full_registration_v5_20261010.py','run_StockRank20Embedding180_selected_candidate_feature_cache_v6_20261010.py','seal_StockRank20Embedding180_selected_candidate_v2_20261010.py']
    drivers={};wrappers=[];inputs=[Path(__file__),oldpath,original,broker]
    for driver in sorted(set(old['driver_wrappers'])|set(extra)|{v[0] for v in selected.values()}):
        if driver.startswith('run_StockRankDual174_full_registration_'):continue
        p=A/driver;assert p.is_file(),p;inputs.append(p);wrapper=p.with_name(p.stem+'_after_future_children_v5.py')
        body="from pathlib import Path\nimport sys\nA=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]\nfrom route_verified_Dual25_recovery_dependencies_v5_20261010 import execute\nif __name__=='__main__':execute("+repr(driver)+")\n"
        wrappers.append(save(wrapper.name,body));drivers[driver]=wrapper.name
    # The running174 registry is a distinct verified handle and is never redirected or restarted.
    proof=A/'Dual25_verified_recovery_exact_dependency_aliases_v5_20261010.json';create(proof,{'status':'compiled_all_actual_future_child_entry_points_and_own_closed_candidate_cache_routing_before_future_dispatch','service_aliases':aliases,'driver_wrappers':drivers,'source_factories':old['source_factories'],'selected_helpers':sorted(selected),'input_sha256':{str(p):sha(p) for p in dict.fromkeys([*inputs,*wrappers])},'running174_registry_preserved':True,'new_fits':0,'new_quality_scores':0,'new_inference':False,'test_labels_read':False})
    for name,(driver,row) in selected.items():retire(row,'Replace verified childless still-unstarted dependency helper with complete future-child routing; completed native42 and active registry174 preserved')
    tasks={}
    for name,(driver,row) in selected.items():
        actual=aliases[name];wrapper=drivers[driver];assert actual not in tasks or tasks[actual]==wrapper;tasks[actual]=wrapper
    for name,n in tasks.items():
        assert allowed();row=start_service(name,n,[],{str(A/n):sha(A/n),str(proof):sha(proof)});create(A/(name+'_activation.json'),row)
    print({'all_future_child_types_predeclared':len(extra),'pending_helpers_routed':len(tasks),'active174_registration_not_restarted':True},flush=True)
if __name__=='__main__':main()
