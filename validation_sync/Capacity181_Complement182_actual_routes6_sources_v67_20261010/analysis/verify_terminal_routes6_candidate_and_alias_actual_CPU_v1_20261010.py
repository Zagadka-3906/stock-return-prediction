"""Execute actual closure/child-routing functions independently, without forecasts or fake terminal states."""
from pathlib import Path
import sys,ast,copy
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
def function(tree,name):
    nodes=[n for n in ast.walk(tree) if isinstance(n,ast.FunctionDef) and n.name==name];assert len(nodes)==1
    return ast.fix_missing_locations(ast.Module(body=[copy.deepcopy(nodes[0])],type_ignores=[]))
def main():
    broker=A/'route_verified_Dual25_recovery_dependencies_v6_20261010.py';proofpath=A/'Dual25_verified_recovery_exact_dependency_aliases_v6_20261010.json';proof=read(proofpath)
    for p,d in proof['input_sha256'].items():assert sha(p)==d,p
    aliases=proof['service_aliases'];drivers=proof['driver_wrappers'];tree=ast.parse(broker.read_text(encoding='utf8'));events=[]
    def original_closed(name):events.append(name);return name
    scope={'aliases':aliases,'original_closed':original_closed}
    exec(compile(function(tree,'resolve_closed'),str(broker)+'::actual_resolve_closed','exec'),scope)
    rows=[]
    for original,actual in aliases.items():
        assert scope['resolve_closed'](original)==actual and events[-1]==actual
        assert aliases.get(actual,actual)==actual
        rows.append({'original':original,'actual_endpoint':actual,'exact_single_flattened_closed_call':True})
    routed=[]
    def actual_run_path(path,*args,**kwargs):routed.append((str(path),args,kwargs));return str(path)
    scope={'Path':Path,'A':A,'drivers':drivers,'actual_run_path':actual_run_path}
    exec(compile(function(tree,'resolve_candidate_path'),str(broker)+'::actual_nested_candidate_redirect','exec'),scope)
    candidates=sorted(n for n in drivers if n.startswith('prepare_') and '_selected_candidate_' in n and n.endswith('_20261010.py'))
    assert any('181' in n and 'v6' in n for n in candidates)
    childrows=[]
    for name in [*candidates,'run_StockRankWide32Embedding181_full_registration_v6_20261010.py','unmapped_actual_control.py']:
        result=scope['resolve_candidate_path'](str(A/name),run_name='__main__')
        expected=str(A/drivers[name]) if name in candidates else str(A/name)
        assert result==expected and routed[-1][2]=={'run_name':'__main__'}
        childrows.append({'source':name,'actual_routed_path':result,'noncandidate_runtime_not_redirected_again':name not in candidates})
    import normalize_completed_stock_rank_wide32_embedding_complete48_after180_v6_20261010 as normalized
    import stock_rank_wide32_embedding_after_complete_qualified_parent_native_stage_v1_20261010 as stage
    import stock_rank_wide32_embedding_wide1024_BF16_native_v1_20261010 as native
    assert set(normalized.RECIPES)==set(stage.BACKENDS) and native.CONFIG['stock_embedding_dim']==32 and native.CONFIG['hidden']==[1024,512,256] and native.CONFIG['epochs']==64
    paths=[Path(__file__),broker,proofpath,Path(normalized.__file__),Path(stage.__file__),Path(native.__file__),A/'stock_rank_wide32_embedding_actual_twelve_parent_callbacks_CPU_controls_v2_20261010.json']
    create(A/'terminal_routes6_candidate_aliases_and_recipe32_actual_CPU_v1_20261010.json',{'status':'passed_actual_flattened_closed_functions_nested_candidate_redirect_and_recipe32_backend_contract','alias_records':rows,'child_records':childrows,'actual_alias_cases':len(rows),'actual_nested_child_cases':len(childrows),'actual_capacity_parent_callbacks_CPU':12,'input_sha256':{str(p):sha(p) for p in paths},'new_fits':0,'new_quality_scores':0,'actual_future_X_read':False,'saved_model_inference_not_claimed':True})
    print({'actual_alias_cases':len(rows),'actual_child_cases':len(childrows),'recipe32_contract':True},flush=True)
if __name__=='__main__':main()
