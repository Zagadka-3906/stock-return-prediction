"""Correct two stale canonical aliases, audit every terminal endpoint, preserve all scientific workers."""
from pathlib import Path
import sys,ast,re,subprocess,importlib,copy
A=Path(__file__).resolve().parent;ROOT=A.parent;sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
from handoff_ready_goss_full_execution_20261006 import retire,start_service

def main():
    assert allowed();oldpath=A/'Dual25_verified_recovery_exact_dependency_aliases_v5_20261010.json';old=read(oldpath)
    for p,d in old['input_sha256'].items():assert sha(p)==d,p
    aliases=dict(old['service_aliases'])
    screen='actual_stock_top10_embedding_after174_large_allocation29_screen_v2_after_Dual25_recovery_v1_dispatch_v4_future_children_v5_20261010'
    screenfolder=A/'service_owned_workflows_20261006'/screen
    assert read(screenfolder/'service_execution.json')['status']=='passed' and not owned(read(screenfolder/'native_launch.json'))
    livepub='actual_stock_top10_embedding_after174_large_allocation29_completion_main_v72_after_Dual25_recovery_v1_dispatch_v4_future_children_v5_20261010'
    # Canonical v2 and its older registry aliases must all point to the passed
    # physical screen, rather than a retired registry-v2 waiting helper.
    for key in ['actual_stock_top10_embedding_after174_large_allocation29_screen_v2_20261010','actual_stock_top10_embedding_after174_large_allocation29_screen_v2_after_Dual25_recovery_v1_registry_recovery_v2_20261010']:aliases[key]=screen
    for key in ['actual_stock_top10_embedding_after174_large_allocation29_completion_main_v72_20261010','actual_stock_top10_embedding_after174_large_allocation29_completion_main_v72_after_Dual25_recovery_v1_registry_recovery_v2_20261010']:aliases[key]=livepub
    helpers={}
    for actual in sorted(set(aliases.values())):
        folder=A/'service_owned_workflows_20261006'/actual
        if (folder/'native_launch.json').exists():
            row=read(folder/'native_launch.json')
            if owned(row):helpers[actual]={'row':row,'definition':read(folder/'job_definition.json')}
    for actual in ['actual_stock_rank_wide32_embedding48_after180_normalization_queue_v6_20261010','StockRankWide32Embedding48_selected_native14_v6_20261010','StockRankWide32Embedding181_complete48_family_v7_20261010']:
        folder=A/'service_owned_workflows_20261006'/actual;row=read(folder/'native_launch.json');assert owned(row)
        helpers[actual]={'row':row,'definition':read(folder/'job_definition.json')}
    # Every replacement is independently verified idle at closed(); completed
    # scores/native42/actual six fits and all other workers are never restarted.
    for actual,item in helpers.items():
        dump=subprocess.run([str(ROOT/'tools/readonly_pyspy_diagnostics_20261006/py-spy.exe'),'dump','--pid',str(item['row']['owned_worker_pid'])],capture_output=True,text=True,check=True).stdout
        assert '(idle)' in dump and '    closed (' in dump,actual
        item['idle_stack']=dump
        item['new']=actual.removesuffix('_20261010')+'_resolved_terminal_routes_v6_20261010'
        aliases[actual]=item['new']
    def resolve(name):
        seen=set()
        while name in aliases and aliases[name]!=name:
            assert name not in seen,('alias_cycle',name);seen.add(name);name=aliases[name]
        return name
    aliases={key:resolve(value) for key,value in aliases.items()}
    assert aliases['actual_stock_top10_embedding_after174_large_allocation29_screen_v2_20261010']==screen
    assert aliases['actual_stock_top10_embedding_after174_large_allocation29_completion_main_v72_20261010']==helpers[livepub]['new']
    drivers={};originals=set()
    for name in old['driver_wrappers'].values():
        tree=ast.parse((A/name).read_text(encoding='utf8'));calls=[n for n in ast.walk(tree) if isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.func.id=='execute']
        assert len(calls)==1;originals.add(ast.literal_eval(calls[0].args[0]))
    fresh181=['normalize_completed_stock_rank_wide32_embedding_complete48_after180_v6_20261010.py','qualify_stock_rank_wide32_embedding48_selected_native14_v6_20261010.py','run_StockRankWide32Embedding181_complete_family_v7_20261010.py','prepare_StockRankWide32Embedding181_selected_candidate_v6_20261010.py','seal_StockRankWide32Embedding181_selected_candidate_v3_20261010.py','run_StockRankWide32Embedding181_full_registration_v6_20261010.py','run_StockRankWide32Embedding181_selected_candidate_feature_cache_v7_20261010.py']
    originals.update(fresh181)
    proofpath=A/'Dual25_verified_recovery_exact_dependency_aliases_v6_20261010.json'
    broker=A/'route_verified_Dual25_recovery_dependencies_v6_20261010.py';assert not broker.exists()
    text=(A/'route_verified_Dual25_recovery_dependencies_v5_20261010.py').read_text(encoding='utf8');text=text[:text.index('\ndef main():')]+ '\n'
    text=text.replace('Dual25_verified_recovery_exact_dependency_aliases_v5','Dual25_verified_recovery_exact_dependency_aliases_v6')
    assert not broker.exists();compile(text,str(broker),'exec');broker.write_text(text,encoding='utf8',newline='\n')
    wrappers=[]
    for original in sorted(originals):
        name=Path(original).stem+'_after_terminal_routes_v6.py';path=A/name;assert not path.exists()
        source="from pathlib import Path\nimport sys\nA=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]\nfrom route_verified_Dual25_recovery_dependencies_v6_20261010 import execute\nif __name__=='__main__':execute("+repr(original)+")\n"
        compile(source,str(path),'exec');path.write_text(source,encoding='utf8',newline='\n');wrappers.append(path);drivers[original]=name
    for previousname,wrapper in old['driver_wrappers'].items():
        tree=ast.parse((A/wrapper).read_text(encoding='utf8'));call=next(n for n in ast.walk(tree) if isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.func.id=='execute');original=ast.literal_eval(call.args[0]);drivers[previousname]=drivers[original];drivers[wrapper]=drivers[original]
    factories=[*old['source_factories'],'prepare_StockRankWide32Embedding181_complete48_pipeline_v2_20261010']
    paths=[Path(__file__),oldpath,broker,*wrappers,*[A/n for n in originals],screenfolder/'service_execution.json']
    create(proofpath,{'status':'compiled_actual_passed_Top29_canonical_terminal_and_every_live_idle_helper_flattened_alias_before_future_dispatch','service_aliases':aliases,'driver_wrappers':drivers,'source_factories':factories,'selected_helpers':[{'old':name,'new':item['new'],'idle_stack':item['idle_stack'],'identity':item['row']} for name,item in helpers.items()],'input_sha256':{str(p):sha(p) for p in paths},'scientific_workers_restarted':0,'new_fits':0,'new_quality_scores':0,'new_inference':0,'test_labels_read':False})
    # Audit all endpoint evidence now. Fresh exclusive replacements are planned;
    # every preserved endpoint has a real terminal/owned handle, including the
    # unrelated failed native42 dispatcher, which is never claimed passed.
    endpoints=[]
    planned={item['new'] for item in helpers.values()}
    for name in sorted(set(aliases.values())):
        folder=A/'service_owned_workflows_20261006'/name
        if name in planned:
            assert not folder.exists();status='exclusive_fresh_idle_helper_replacement'
        else:
            assert (folder/'native_launch.json').exists(),name
            terminal=read(folder/'service_execution.json') if (folder/'service_execution.json').exists() else None
            assert terminal is not None or owned(read(folder/'native_launch.json')),name
            status=terminal['status'] if terminal else 'verified_owned_live'
        endpoints.append({'actual_service':name,'status':status})
    create(A/'all_actual_terminal_dependency_routes_endpoint_audit_v6_20261010.json',{'status':'passed_every_alias_endpoint_exists_or_is_exclusive_fresh_dispatch_before_replacements','records':endpoints,'input_sha256':{str(proofpath):sha(proofpath)},'failed_unused_dispatcher_preserved_not_qualified':True,'new_quality_scores':0})
    for item in helpers.values():retire(item['row'],'Replace only verified idle childless dependency helper: canonical Top29 points to the passed physical screen; all aliases flattened to live actual route6.')
    for actual,item in helpers.items():
        assert allowed();definition=item['definition'];old_driver=Path(definition['driver']).name;driver=drivers.get(old_driver,old_driver)
        assert driver!=old_driver,(actual,old_driver)
        row=start_service(item['new'],driver,definition['arguments'],{str(A/driver):sha(A/driver),str(proofpath):sha(proofpath)})
        create(A/(item['new']+'_activation.json'),row)
    print({'actual_idle_helpers_routed':len(helpers),'all_endpoint_audits':len(endpoints),'passed_Top29_preserved':screen,'new_wrappers':len(wrappers),'scientific_workers_restarted':0},flush=True)
if __name__=='__main__':main()
