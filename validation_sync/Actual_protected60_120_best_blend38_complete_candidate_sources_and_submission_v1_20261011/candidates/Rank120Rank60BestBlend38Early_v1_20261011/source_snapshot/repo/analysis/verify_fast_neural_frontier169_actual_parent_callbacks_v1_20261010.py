"""Extract the real two parent callbacks and verify source preservation and stage order on CPU."""
from pathlib import Path
import sys,ast
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import create,sha
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed

def main():
    assert allowed()
    import predict_fast_neural_frontier169_complete_scheme_v1_20261010 as predictor
    import fast_neural_frontier169_native_stage_v1_20261010 as stage
    import importlib
    assert predictor.PARENT_FILENAMES=={167:'predict_protected_Return_after163_complete_scheme_v4_20261010.py',168:'predict_protected_RecentReturn252_after167_complete_scheme_v2_20261010.py'}
    records=[];paths=[Path(__file__),Path(predictor.__file__),Path(stage.__file__)]
    needle='\n        value,report=after_parent(ns,context,parent,spec,component);calls.append(report);return value'
    inserted=needle.replace('return value','return FRONTIER169_AFTER_WHOLE_SELECTED_PARENT(context,value)')
    for number,name in predictor.PARENT_FILENAMES.items():
        source=A/name;original=source.read_text(encoding='utf8');changed=predictor.prepared_parent167(original)
        assert original.count(needle)==1 and changed.count(inserted)==1
        assert changed.replace(inserted,needle)==original
        assert ast.dump(ast.parse(changed.replace(inserted,needle)))==ast.dump(ast.parse(original))
        tree=ast.parse(changed)
        callbacks=[node for node in ast.walk(tree) if isinstance(node,ast.FunctionDef) and any(isinstance(x,ast.Name) and x.id=='FRONTIER169_AFTER_WHOLE_SELECTED_PARENT' for statement in node.body for x in ast.walk(statement)) and not any(isinstance(statement,ast.FunctionDef) for statement in node.body)]
        assert len(callbacks)==1,(name,[x.name for x in callbacks])
        fn=callbacks[0];assert [arg.arg for arg in fn.args.args]==['context','parent']
        for parent in ([0.,1.,-1.],[3.,8.,12.]):
            calls=[];order=[]
            def original_stage(ns,context,values,spec,component):
                assert context=='probe';order.append('complete_parent_stage_returned');return [v*2 for v in values],{'base':number}
            def new_stage(context,values):
                assert context=='probe';order.append('frontier_after_whole_parent');return [v+5 for v in values]
            namespace={'ns':None,'spec':None,'component':None,'after_parent':original_stage,'calls':calls,'FRONTIER169_AFTER_WHOLE_SELECTED_PARENT':new_stage}
            module=ast.Module(body=[fn],type_ignores=[]);ast.fix_missing_locations(module);exec(compile(module,str(source),'exec'),namespace)
            assert namespace[fn.name]('probe',parent)==[v*2+5 for v in parent]
            assert order==['complete_parent_stage_returned','frontier_after_whole_parent'] and calls==[{'base':number}]
        records.append({'actual_parent_round':number,'real_source':str(source),'source_sha256':sha(source),'real_callback_name':fn.name,'source_and_AST_restored_exact':True,'actual_CPU_callback_orders_checked':2})
        paths.append(source)
    expected={'recent252returnhuber050':('y_ret_1d',1,20.),'recent252forward20huber050':('y_ret_20mean',20,100.),'recent252forward5huber050':('y_ret_5mean',5,100.),'recent252rank5huber050':('y_rank_5mean',5,1.)}
    for name,(target,horizon,scale) in expected.items():
        native=importlib.import_module(stage.BACKENDS[name][0]);decoder=importlib.import_module(stage.BACKENDS[name][1])
        assert (native.CONFIG['target'],native.CONFIG['label_horizon_trading_days'],native.CONFIG['return_target_scale'])==(target,horizon,scale)
        assert native.CONFIG['training_calendar_window']==252
        paths.extend([Path(native.__file__),Path(decoder.__file__)])
    create(A/'fast_neural_frontier169_actual_parent_callback_CPU_controls_v1_20261010.json',{'status':'passed2_real_parent_callbacks4_actual_CPU_order_probes_exact_AST_restore_and4_own_recipe_source_routes',
        'records':records,'backend_configuration_cases':4,'input_sha256':{str(p):sha(p) for p in paths},'new_native_fits':0,'new_quality_scores':0,'future_X_read':False,'test_labels_read':False,
        'full_selected_pipeline_equivalence_not_claimed_before_actual_inference':True,
        'legacy_schema_status_names_retained_actual_parent_defined_by_configuration_anchor_round_and_stage_report':True})
    print({'actual_parent_sources':2,'actual_CPU_orders':4,'admitted_recipe_configs':4,'full_future_inference_not_claimed':True},flush=True)
if __name__=='__main__':main()
