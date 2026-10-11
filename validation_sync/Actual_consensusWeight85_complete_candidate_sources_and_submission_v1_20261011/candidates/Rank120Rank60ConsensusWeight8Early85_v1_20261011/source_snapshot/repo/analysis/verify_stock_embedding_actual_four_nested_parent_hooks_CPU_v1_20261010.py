"""Execute the actual prepared nested hooks of all three qualified-parent predictor routes."""
from pathlib import Path
import ast,sys
A=Path(__file__).resolve().parent;ROOT=A.parent;sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import create,sha

def main():
    from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
    assert allowed()
    import predict_stock_embedding_complete_qualified_parent_scheme_v1_20261010 as actual
    from frontier233_after_complete_parent_native_stage_v1_20261010 import GRAPH_KEY as key233
    from cross120_after_complete169_native_stage_v2_20261010 import GRAPH_KEY as key120
    routes=[({},'predict_fast_neural_frontier169_complete_scheme_v2_20261010.py'),({key120:{}},'predict_cross120170_complete169_scheme_v1_20261010.py'),({key120:{},key233:{}},'predict_frontier233_complete_parent_scheme_v1_20261010.py')]
    from frontier133_after_complete_qualified_parent_native_stage_v1_20261010 import GRAPH_KEY as key133
    routes.append(({key133:{}},'predict_frontier133_complete_qualified_parent_scheme_v1_20261010.py'))
    rows=[];inputs=[Path(__file__),Path(actual.__file__)]
    for graph,filename in routes:
        assert actual.parent_filename(graph)==filename
        source=A/filename;text=source.read_text(encoding='utf8');prepared=actual.prepared_parent(text)
        functions=[node for node in ast.walk(ast.parse(prepared)) if isinstance(node,ast.FunctionDef) and node.name in ('tail_stage','after_whole') and any(isinstance(call,ast.Name) and call.id=='STOCK_EMBEDDING_AFTER_WHOLE_QUALIFIED_PARENT' for call in ast.walk(node))]
        assert len(functions)==1
        events=[];calls=[]
        def parent(ns,context,value,spec,component):events.append('actual_parent_stage');return value+3,{'actual_mock_parent_stage':True}
        def after(context,value):events.append('new_stage_after_whole_parent');assert value==5;return value+100
        scope={'after_parent':parent,'ns':object(),'spec':{},'component':{},'components':[{},{}],'calls':calls,'STOCK_EMBEDDING_AFTER_WHOLE_QUALIFIED_PARENT':after}
        module=ast.Module(body=functions,type_ignores=[]);exec(compile(ast.fix_missing_locations(module),str(source)+'::actual_nested_hook','exec'),scope)
        assert scope[functions[0].name](object(),2)==105 and events==['actual_parent_stage','new_stage_after_whole_parent'] and len(calls)==1
        try:actual.prepared_parent(prepared)
        except AssertionError:pass
        else:raise AssertionError('Nested callback applied twice')
        inputs.append(source);rows.append({'actual_parent_source':filename,'actual_source_sha256':sha(source),'actual_nested_function_execution_order_passed':True,'repeated_hook_patch_refused':True})
    assert actual.parent_filename({key233:{}})=='predict_frontier233_complete_parent_scheme_v1_20261010.py'
    create(A/'stock_embedding_actual_four_nested_parent_hooks_CPU_controls_v1_20261010.json',{'status':'passed_actual_four_parent_source_nested_callbacks_and_route_priority','input_sha256':{str(p):sha(p) for p in inputs},'records':rows,'does_not_claim_actual_full_future_pipeline_execution':True,'new_native_fits':0,'new_quality_scores':0,'actual_future_X_read':False,'test_labels_read':False})
    print({'actual_nested_parent_sources_checked':len(rows),'new_quality_scores':0},flush=True)

if __name__=='__main__':main()
