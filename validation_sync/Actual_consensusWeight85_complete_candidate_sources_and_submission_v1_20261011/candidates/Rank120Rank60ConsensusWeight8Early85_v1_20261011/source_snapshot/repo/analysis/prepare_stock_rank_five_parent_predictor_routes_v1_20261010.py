"""Prepare rank replay after the fully qualified stock173 lineage and execute nested CPU hooks."""
from pathlib import Path
import sys,ast
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import create,sha
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
def main():
    assert allowed()
    source=A/'predict_stock_embedding_complete_qualified_parent_scheme_v1_20261010.py'
    text=source.read_text(encoding='utf8').replace('stock_embedding','stock_rank_embedding').replace('STOCK_EMBEDDING_AFTER_WHOLE_QUALIFIED_PARENT','STOCK_RANK_EMBEDDING_AFTER_WHOLE_QUALIFIED_PARENT')
    text=text.replace('def parent_filename(graph):','def parent_filename(graph):\n    from stock_embedding_after_complete_qualified_parent_native_stage_v1_20261010 import GRAPH_KEY as stock_key\n    if stock_key in graph:return \'predict_stock_embedding_complete_qualified_parent_scheme_v1_20261010.py\'')
    text=text.replace('in (169,170,171,172)','in (169,170,171,172,173)')
    dest=A/'predict_stock_rank_embedding_complete_qualified_parent_scheme_v1_20261010.py';assert not dest.exists();compile(text,str(dest),'exec');dest.write_text(text,encoding='utf8',newline='\n')
    actual=__import__(dest.stem)
    from frontier233_after_complete_parent_native_stage_v1_20261010 import GRAPH_KEY as key233
    from cross120_after_complete169_native_stage_v2_20261010 import GRAPH_KEY as key120
    from frontier133_after_complete_qualified_parent_native_stage_v1_20261010 import GRAPH_KEY as key133
    from stock_embedding_after_complete_qualified_parent_native_stage_v1_20261010 import GRAPH_KEY as key_stock
    routes=[({},'predict_fast_neural_frontier169_complete_scheme_v2_20261010.py'),({key120:{}},'predict_cross120170_complete169_scheme_v1_20261010.py'),({key120:{},key233:{}},'predict_frontier233_complete_parent_scheme_v1_20261010.py'),({key133:{}},'predict_frontier133_complete_qualified_parent_scheme_v1_20261010.py'),({key_stock:{},key133:{},key233:{},key120:{}},'predict_stock_embedding_complete_qualified_parent_scheme_v1_20261010.py')]
    rows=[];paths=[Path(__file__),source,dest]
    for graph,filename in routes:
        assert actual.parent_filename(graph)==filename
        p=A/filename;prepared=actual.prepared_parent(p.read_text(encoding='utf8'))
        funcs=[n for n in ast.walk(ast.parse(prepared)) if isinstance(n,ast.FunctionDef) and n.name in ('tail_stage','after_whole') and any(isinstance(c,ast.Name) and c.id=='STOCK_RANK_EMBEDDING_AFTER_WHOLE_QUALIFIED_PARENT' for c in ast.walk(n))];assert len(funcs)==1
        events=[];calls=[]
        def parent(ns,context,value,spec,component):events.append('complete_parent');return value+3,{'CPU_hook_only':True}
        def new_stage(context,value):events.append('new_rank_stage');assert value==5;return value+100
        scope={'after_parent':parent,'ns':object(),'spec':{},'component':{},'components':[{},{}],'calls':calls,'STOCK_RANK_EMBEDDING_AFTER_WHOLE_QUALIFIED_PARENT':new_stage}
        exec(compile(ast.fix_missing_locations(ast.Module(body=funcs,type_ignores=[])),str(p)+'::actual_nested_hook','exec'),scope)
        assert scope[funcs[0].name](object(),2)==105 and events==['complete_parent','new_rank_stage'] and len(calls)==1
        try:actual.prepared_parent(prepared)
        except AssertionError:pass
        else:raise AssertionError('Duplicate rank hook accepted')
        paths.append(p);rows.append({'source':str(p),'nested_hook_order_exact':True,'duplicate_patch_refused':True})
    create(A/'stock_rank_embedding_actual_five_parent_hooks_CPU_controls_v1_20261010.json',{'status':'passed_actual_five_parent_source_nested_callbacks_and_stock173_route_priority','records':rows,'input_sha256':{str(p):sha(p) for p in paths},'actual_full_future_inference_claimed':False,'new_quality_scores':0,'future_X_read':False,'test_labels_read':False})
    print({'actual_nested_hooks_passed':5,'stock173_lineage_supported':True},flush=True)
if __name__=='__main__':main()
