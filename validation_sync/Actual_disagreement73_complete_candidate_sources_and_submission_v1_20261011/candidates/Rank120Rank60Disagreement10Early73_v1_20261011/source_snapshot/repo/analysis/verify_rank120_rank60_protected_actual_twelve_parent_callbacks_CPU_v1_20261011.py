"""Execute the exact callbacks inserted into every supported complete-parent source; CPU stubs only."""
from pathlib import Path
import sys,ast,copy
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed

def main():
    assert allowed()
    import predict_rank120_rank60_protected_complete_qualified183_scheme_v1_20261011 as predictor
    original=A/'stock_rank20seed10_embedding_actual_eleven_parent_callbacks_CPU_controls_v1_20261011.json'
    rows=[]
    graph=read(A.parent/'candidates/optimization_20261003_r183/verification.json')['whole_scheme_graph']
    assert predictor.parent_filename(graph)=='predict_stock_rank20_embedding_complete_qualified_parent_scheme_v1_20261010.py'
    source_rows=[*read(original)['records'],{'parent':'predict_stock_rank20_embedding_complete_qualified_parent_scheme_v1_20261010.py'}]
    for row in source_rows:
        p=A/row['parent'];tree=ast.parse(predictor.prepared_parent(p.read_text(encoding='utf8')))
        nodes=[n for n in ast.walk(tree) if isinstance(n,ast.FunctionDef) and n.name in ('tail_stage','after_whole')];assert len(nodes)==1
        events=[];calls=[];context=object();ns=object();spec=object();component=object();components=[component]
        def before(a,b,c,d,e):
            assert a is ns and b is context and c==11 and d is spec and (e is component or e is components)
            events.append('whole_parent_first');return 22,{}
        def after(a,b):
            assert a is context and b==22 and len(calls)==1;events.append('two_seed_stage_last');return 33
        scope=dict(ns=ns,spec=spec,component=component,components=components,calls=calls,after_parent=before,RANK120_RANK60_PROTECTED_AFTER_WHOLE_QUALIFIED_PARENT=after)
        exec(compile(ast.fix_missing_locations(ast.Module(body=[copy.deepcopy(nodes[0])],type_ignores=[])),str(p)+'::actual_two_seed_CPU_callback','exec'),scope)
        assert scope[nodes[0].name](context,11)==33 and events==['whole_parent_first','two_seed_stage_last']
        rows.append({'parent':p.name,'sha256':sha(p),'actual_callback_order':events,'CPU_stub_only_no_native_or_future_inference_claim':True})
    assert len(rows)==12
    create(A/'rank120_rank60_protected_actual_twelve_parent_callbacks_CPU_controls_v1_20261011.json',{
        'status':'passed_actual_eleven_complete_parent_callback_expressions_for_two_seed',
        'records':rows,'input_sha256':{str(p):sha(p) for p in [Path(__file__),Path(predictor.__file__),original]},
        'new_native_fits':0,'new_quality_scores':0,'actual_future_X_read':False,'test_labels_read':False})
    print({'actual_parent_callback_CPU_checks':12,'native_and_full_future_inference_not_claimed':True},flush=True)

if __name__=='__main__':main()
