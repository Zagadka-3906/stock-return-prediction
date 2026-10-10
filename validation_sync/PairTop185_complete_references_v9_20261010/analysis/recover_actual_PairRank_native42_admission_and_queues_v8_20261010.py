"""Fill omitted immutable admission references; preserve failures and own6/full5 results."""
from pathlib import Path
import sys,subprocess,re
A=Path(__file__).resolve().parent;ROOT=A.parent;sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from handoff_ready_goss_full_execution_20261006 import start_service,retire
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
def save(name,text):
    p=A/name;assert not p.exists(),p;compile(text,str(p),'exec');p.write_text(text,encoding='utf8',newline='\n');return p
def main():
    assert allowed()
    admissions=[]
    for family in ('pairrank','toppair'):
        source=A/f'stock_{family}_embedding_own32_controls46_sources_admission_v1_20261010.json'
        target=A/f'stock_{family}_embedding_native_stage_and_fast17_sources_admission_v1_20261010.json'
        assert not target.exists();target.write_bytes(source.read_bytes());assert sha(source)==sha(target)
        admissions.append({'actual_admission':str(source),'reference_copy':str(target),'sha256':sha(source),'copy_only_not_scientific_completion':True})
    actual_native='actual_stock_pairrank_embedding_six_state_native42_admission_recovery_v2_20261010'
    services={'actual_stock_pairrank_embedding_six_state_native42_v1_20261010':actual_native}
    oldhelpers=['actual_stock_pairrank_embedding48_after183_normalization_queue_v8_20261010','StockPairRankEmbedding48_selected_native14_v8_20261010','StockPairRankEmbedding184_complete48_family_v9_20261010']
    for old in oldhelpers:services[old]=old.removesuffix('_20261010')+'_after_actual_native_admission_v8_20261010'
    originals=['run_stock_pairrank_embedding_own32_controls46_queue_v2_20261010.py','run_stock_toppair_embedding_own32_controls46_queue_v2_20261010.py','publish_stock_pairrank_objective_remaining_native46_main_v2_20261010.py','normalize_completed_stock_pairrank_embedding_complete48_after183_v8_20261010.py','qualify_stock_pairrank_embedding48_selected_native14_v8_20261010.py','run_StockPairRankEmbedding184_complete_family_v9_20261010.py','run_StockPairRankEmbedding184_selected_candidate_feature_cache_v9_20261010.py','prepare_StockPairRankEmbedding184_selected_candidate_v8_20261010.py','seal_StockPairRankEmbedding184_selected_candidate_v5_20261010.py','run_StockPairRankEmbedding184_full_registration_v8_20261010.py','run_stock_pairrank_embedding_after174_fast17_screen_v1_20261010.py','run_stock_pairrank_embedding_after174_large_allocation29_screen_v1_20261010.py']
    # Native42 originally failed before producing its frozen protocol: the original exclusive output is unused.
    assert read(A/'service_owned_workflows_20261006/actual_stock_pairrank_embedding_six_state_native42_v1_20261010/service_execution.json')['status']=='failed'
    assert not Path('E:/赛题五_本机临时/stock_pairrank_embedding_six_state_native42_v1_20261010/frozen_before_native42.json').exists()
    queue=(A/'run_stock_pairrank_embedding_own32_controls46_queue_v1_20261010.py').read_text(encoding='utf8')
    start=queue.index('    for name,driver in ');end=queue.index(':\n',start)
    import ast
    tasks=ast.literal_eval(queue[start+len('    for name,driver in '):end]);assert len(tasks)==7
    queue=queue[:start]+'    for name,driver in '+repr(tasks[5:])+queue[end:]
    queue=queue.replace("closed('actual_stock_rank_wide32_embedding_after174_large_allocation29_screen_v1_20261010')","closed('actual_stock_pairrank_embedding_six_state_native42_v1_20261010')")
    save(originals[0],queue)
    top=(A/'run_stock_toppair_embedding_own32_controls46_queue_v1_20261010.py').read_text(encoding='utf8');save(originals[1],top)
    pub=(A/'publish_stock_pairrank_objective_stages_main_v1_20261010.py').read_text(encoding='utf8')
    start=pub.index('    phases=');end=pub.index('\n',start)
    pub=pub[:start]+"    phases=[('native42_official46',('actual_stock_pairrank_embedding_six_state_native42_v1_20261010','actual_stock_pairrank_embedding_after174_large_allocation29_screen_v1_20261010'))]"+pub[end:]
    pub=pub.replace("paths=[Path(__file__),template,", "paths=[Path(__file__),A/'actual_PairRank_native42_admission_routes_v8_20261010.json',A/'route_actual_PairRank_native42_admission_v8_20261010.py',template,")
    save(originals[2],pub)
    wrappers={n:Path(n).stem+'_actual_native_admission_v8.py' for n in originals}
    runtime='''from pathlib import Path
import sys,importlib,runpy
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha
PROOF=A/'actual_PairRank_native42_admission_routes_v8_20261010.json'
def installed():
    import route_verified_Dual25_recovery_dependencies_v7_20261010 as parent
    parent.installed()
    import prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 as checks
    import handoff_ready_goss_full_execution_20261006 as launch
    data=read(PROOF)
    for p,d in data['input_sha256'].items():assert sha(p)==d,p
    previous_closed=checks.closed;previous_start=launch.start_service
    def closed(name):return previous_closed(data['service_aliases'].get(name,name))
    def start(name,driver,args,pins):return previous_start(data['service_aliases'].get(name,name),data['driver_wrappers'].get(driver,driver),args,{**pins,str(PROOF):sha(PROOF),str(Path(__file__)):sha(__file__)})
    checks.closed=closed;launch.start_service=start
    module=importlib.import_module('prepare_StockPairRankEmbedding184_complete48_pipeline_v4_20261010');original=module.source_paths
    module.source_paths=lambda:list(dict.fromkeys([*original(),PROOF,Path(__file__),*[A/n for n in data['driver_wrappers'].values()]]))
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
    runtime_path=save('route_actual_PairRank_native42_admission_v8_20261010.py',runtime)
    for source,target in wrappers.items():save(target,"from pathlib import Path\nimport sys\nA=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]\nfrom route_actual_PairRank_native42_admission_v8_20261010 import execute\nif __name__=='__main__':execute("+repr(source)+")\n")
    proof=A/'actual_PairRank_native42_admission_routes_v8_20261010.json'
    paths=[Path(__file__),runtime_path,*[A/n for n in originals],*[A/n for n in wrappers.values()],*[Path(r[k]) for r in admissions for k in ('actual_admission','reference_copy')]]
    create(proof,{'status':'compiled_actual_own6_full5_preserved_exact_missing_admission_copies_and_new_service_routes','service_aliases':services,'driver_wrappers':wrappers,'admission_copies':admissions,'input_sha256':{str(p):sha(p) for p in paths},'new_fits':0,'new_scores':0,'new_future_inference':0,'original_native42_failure_preserved':True})
    records=[]
    for name in oldhelpers:
        row=read(A/'service_owned_workflows_20261006'/name/'native_launch.json')
        result=subprocess.run([str(ROOT/'tools/readonly_pyspy_diagnostics_20261006/py-spy.exe'),'dump','--pid',str(row['owned_worker_pid'])],capture_output=True,text=True)
        assert result.returncode==0 and '(idle)' in result.stdout and 'closed (' in result.stdout
        retire(row,'Resume exact completed own6/full5 via honest native42 recovery alias; no184 outputs or inference started');records.append(row)
    create(A/'PairRank184_native42_three_idle_helper_recovery_v8_20261010.json',{'status':'retired_only_three_verified_idle_helpers_for_actual_native42_alias','identities':records,'new_fits':0,'new_inference':0})
    tasks=[(actual_native,'verify_stock_pairrank_embedding_six_state_native42_v1_20261010.py'),('actual_stock_pairrank_embedding_own32_controls46_queue_v2_20261010',wrappers[originals[0]]),('actual_stock_toppair_embedding_own32_controls46_queue_v2_20261010',wrappers[originals[1]]),(services[oldhelpers[0]],wrappers[originals[3]]),(services[oldhelpers[1]],wrappers[originals[4]]),(services[oldhelpers[2]],wrappers[originals[5]])]
    # Complete an original in-flight own6 publication first; the recovery publishes only the unstarted native/score phase.
    publisher='''from pathlib import Path
import sys,time,runpy
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,owned
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
def main():
    f=A/'service_owned_workflows_20261006/actual_StockPairRank_objective_stages_main_v1_20261010'
    row=read(f/'native_launch.json')
    while owned(row):assert allowed();time.sleep(10)
    assert read(A/'StockPairRank_objective_own6_full5_main_receipt_v1_20261010.json')['status']=='pushed_and_remote_head_verified'
    runpy.run_path(str(A/'publish_stock_pairrank_objective_remaining_native46_main_v2_20261010_actual_native_admission_v8.py'),run_name='__main__')
if __name__=='__main__':main()
'''
    driver=save('finish_PairRank_own6_publication_and_actual_native46_v8_20261010.py',publisher)
    tasks.append(('actual_StockPairRank_remaining_native46_main_v8_20261010',driver.name))
    for name,n in tasks:
        assert allowed();p=A/n;row=start_service(name,n,[],{str(p):sha(p),str(proof):sha(proof)});create(A/(name+'_activation.json'),row)
    print({'exact_admission_copies':2,'own6_and_full5_not_repeated':True,'actual_native42_recovery_started':True,'fresh_queue_tasks':len(tasks)},flush=True)
if __name__=='__main__':main()
