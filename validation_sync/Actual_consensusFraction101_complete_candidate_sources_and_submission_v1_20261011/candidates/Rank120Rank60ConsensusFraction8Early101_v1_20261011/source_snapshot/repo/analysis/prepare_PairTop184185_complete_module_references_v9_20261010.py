"""Complete versioned185 imports and freeze explicit184/185 recovery dispatch before futureX."""
from pathlib import Path
import sys,re,ast,subprocess
A=Path(__file__).resolve().parent;ROOT=A.parent;sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import create,sha,read
from handoff_ready_goss_full_execution_20261006 import start_service,retire
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
def save(name,text):
    p=A/name;assert not p.exists(),p;compile(text,str(p),'exec');p.write_text(text,encoding='utf8',newline='\n');return p
def key(name):return re.sub(r'_v\d+(?=[_.])','_vVERSION',name)
def main():
    assert allowed()
    import prepare_StockTopPairEmbedding185_complete48_pipeline_v1_20261010 as top
    authority={key(n):A/n for n in top.NAMES+top.EXTRAS[:9]}
    aliases={};examined=set();todo=[A/n for n in top.NAMES+top.EXTRAS[:9]]
    while todo:
        p=todo.pop()
        if p in examined:continue
        examined.add(p);tree=ast.parse(p.read_text(encoding='utf8'));references=set()
        for n in ast.walk(tree):
            mods=([x.name for x in n.names] if isinstance(n,ast.Import) else [n.module] if isinstance(n,ast.ImportFrom) else [])
            references.update(m+'.py' for m in mods if m and '185' in m)
            if isinstance(n,ast.Constant) and isinstance(n.value,str):references.update(re.findall(r'[A-Za-z_][A-Za-z_0-9]*185[A-Za-z_0-9]*\.py',n.value))
        for name in references:
            target=A/name
            if target.exists():continue
            source=authority.get(key(name));assert source and source.is_file(),('Unresolved185localreference',name)
            # Add only nonexistent names; each is an exact byte copy of the authoritative new implementation.
            target.write_bytes(source.read_bytes());assert sha(target)==sha(source)
            aliases[str(target)]={'authoritative_source':str(source),'sha256':sha(source)};todo.append(target)
    # Recheck every collected import/file reference without loading future-dependent registration modules.
    checked=0
    for p in examined:
        for n in ast.walk(ast.parse(p.read_text(encoding='utf8'))):
            mods=([x.name for x in n.names] if isinstance(n,ast.Import) else [n.module] if isinstance(n,ast.ImportFrom) else [])
            for m in mods:
                if m and '185' in m:assert (A/(m+'.py')).is_file(),m;checked+=1
    proof=A/'PairTop184185_exact_reference_copies_CPU_v9_20261010.json'
    create(proof,{'status':'passed_recursive_local185_import_and_literal_file_completeness_and_exact_source_byte_copies_CPU','copies':aliases,'actual_import_references_checked':checked,'actual_sources_examined':len(examined),'original_sources_not_modified':True,'new_fits':0,'new_scores':0,'new_future_inference':0})
    older=read(A/'actual_PairRank_native42_admission_routes_v8_20261010.json')
    canonical=['actual_stock_pairrank_embedding48_after183_normalization_queue_v8_20261010','StockPairRankEmbedding48_selected_native14_v8_20261010','StockPairRankEmbedding184_complete48_family_v9_20261010','actual_stock_toppair_embedding48_after184_normalization_queue_v8_20261010','StockTopPairEmbedding48_selected_native14_v8_20261010','StockTopPairEmbedding185_complete48_family_v9_20261010']
    actual_old=[older['service_aliases'][n] for n in canonical[:3]]+['actual_stock_toppair_embedding48_after184_normalization_import_recovery_v2_20261010',*canonical[4:]]
    fresh=[n.removesuffix('_20261010')+'_complete_references_v9_20261010' for n in canonical]
    service_aliases={n:v for c,o,v in zip(canonical,actual_old,fresh) for n in (c,o)}
    source_drivers=['normalize_completed_stock_pairrank_embedding_complete48_after183_v8_20261010.py','qualify_stock_pairrank_embedding48_selected_native14_v8_20261010.py','run_StockPairRankEmbedding184_complete_family_v9_20261010.py','normalize_completed_stock_toppair_embedding_complete48_after184_v8_20261010.py','qualify_stock_toppair_embedding48_selected_native14_v8_20261010.py','run_StockTopPairEmbedding185_complete_family_v9_20261010.py']
    for family,number in (('StockPairRank',184),('StockTopPair',185)):
        source_drivers += [f'prepare_{family}Embedding{number}_selected_candidate_v8_20261010.py',f'seal_{family}Embedding{number}_selected_candidate_v5_20261010.py',f'run_{family}Embedding{number}_selected_candidate_feature_cache_v9_20261010.py',f'run_{family}Embedding{number}_full_registration_v8_20261010.py']
    wrappers={n:Path(n).stem+'_complete_references_v9.py' for n in source_drivers}
    runtime='''from pathlib import Path
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
'''
    runtime_path=save('route_PairTop184185_complete_references_v9_20261010.py',runtime)
    for source,target in wrappers.items():save(target,"from pathlib import Path\nimport sys\nA=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]\nfrom route_PairTop184185_complete_references_v9_20261010 import execute\nif __name__=='__main__':execute("+repr(source)+")\n")
    paths=[Path(__file__),proof,runtime_path,*[Path(p) for p in aliases],*[A/n for n in wrappers.values()],*[A/n for n in source_drivers]]
    route_proof=A/'PairTop184185_complete_reference_routes_v9_20261010.json'
    create(route_proof,{'status':'compiled_exact_complete_reference_supplement_and_original_main_context_preserving_dispatch','service_aliases':service_aliases,'driver_wrappers':wrappers,'source_factories':[f'prepare_StockPairRankEmbedding184_complete48_pipeline_v{v}_20261010' for v in range(1,5)]+['prepare_StockTopPairEmbedding185_complete48_pipeline_v1_20261010'],'input_sha256':{str(p):sha(p) for p in paths},'local_reference_CPU_proof':str(proof),'new_fits':0,'new_scores':0,'new_inference':0})
    retirements=[]
    for name in actual_old:
        row=read(A/'service_owned_workflows_20261006'/name/'native_launch.json')
        result=subprocess.run([str(ROOT/'tools/readonly_pyspy_diagnostics_20261006/py-spy.exe'),'dump','--pid',str(row['owned_worker_pid'])],capture_output=True,text=True)
        assert result.returncode==0 and '(idle)' in result.stdout and 'closed (' in result.stdout
        retire(row,'Add recursive verified185 reference copies and source supplements before any184/185 future output; scientific controls unchanged');retirements.append(row)
    create(A/'PairTop184185_six_verified_idle_helpers_reference_recovery_v9_20261010.json',{'status':'retired_only_six_actual_idle_dependency_helpers_before_future','identities':retirements,'new_fits':0,'new_inference':0})
    for name,source in zip(fresh,source_drivers[:6]):
        assert allowed();driver=wrappers[source];p=A/driver;row=start_service(name,driver,[],{str(p):sha(p),str(route_proof):sha(route_proof)});create(A/(name+'_activation.json'),row)
    print({'exact_new185_reference_copies':len(aliases),'actual_local_imports_checked':checked,'fresh_idle_dependency_helpers':6,'new_fits_or_scores':0},flush=True)
if __name__=='__main__':main()
