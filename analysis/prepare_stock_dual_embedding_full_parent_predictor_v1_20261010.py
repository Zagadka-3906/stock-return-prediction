"""Preserve actual complete-parent replay and physical leaf reuse for the two-bank stage."""
from pathlib import Path
import sys,ast
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import create,sha
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
def main():
    assert allowed()
    source=A/'predict_frontier233_complete_parent_scheme_v1_20261010.py'
    rank=A/'predict_stock_rank_embedding_complete_qualified_parent_scheme_v1_20261010.py'
    template=rank.read_text(encoding='utf8');functions=template[template.index('def parent_filename'):template.index('\ndef predict(')]
    functions=functions.replace('STOCK_RANK_EMBEDDING_AFTER_WHOLE_QUALIFIED_PARENT','STOCK_DUAL_EMBEDDING_AFTER_WHOLE_QUALIFIED_PARENT')
    text=source.read_text(encoding='utf8');begin=text.index('def parent_filename');end=text.index('\ndef predict(',begin)
    text=text[:begin]+functions+text[end:]
    text=text.replace('frontier233_after_complete_parent_native_stage_v1_20261010','stock_dual_embedding_after_complete_parent_native_stage_v1_20261010').replace("in (169,170)","in (169,170,171,172,173)").replace('dual120_rank_consensus','stock_return_rank_embedding_consensus').replace('FRONTIER233_AFTER_WHOLE_QUALIFIED_PARENT','STOCK_DUAL_EMBEDDING_AFTER_WHOLE_QUALIFIED_PARENT')
    text=text.replace('frontier233_stage_calls','stock_dual_embedding_stage_calls').replace('frontier233_physical_leaf_reuse','stock_dual_embedding_physical_leaf_reuse').replace('frontier233_complete_parent_native_replay_verification.json','stock_dual_embedding_complete_parent_native_replay_verification.json')
    dest=A/'predict_stock_dual_embedding_complete_parent_scheme_v1_20261010.py';assert not dest.exists();compile(text,str(dest),'exec');dest.write_text(text,encoding='utf8',newline='\n')
    actual=__import__(dest.stem);checked=[];paths=[Path(__file__),source,rank,dest,A/'stock_dual_embedding_after_complete_parent_native_stage_v1_20261010.py']
    for filename in ('predict_fast_neural_frontier169_complete_scheme_v2_20261010.py','predict_cross120170_complete169_scheme_v1_20261010.py','predict_frontier233_complete_parent_scheme_v1_20261010.py','predict_frontier133_complete_qualified_parent_scheme_v1_20261010.py','predict_stock_embedding_complete_qualified_parent_scheme_v1_20261010.py'):
        path=A/filename;prepared=actual.prepared_parent(path.read_text(encoding='utf8'))
        nodes=[n for n in ast.walk(ast.parse(prepared)) if isinstance(n,ast.FunctionDef) and n.name in ('tail_stage','after_whole') and any(isinstance(c,ast.Name) and c.id=='STOCK_DUAL_EMBEDDING_AFTER_WHOLE_QUALIFIED_PARENT' for c in ast.walk(n))];assert len(nodes)==1
        events=[];calls=[]
        def parent(ns,ctx,value,spec,components):events.append('parent');return value+3,{'CPU_only':True}
        def after(ctx,value):events.append('dual');assert value==5;return value+100
        scope={'after_parent':parent,'ns':None,'spec':{},'component':{},'components':[{},{}],'calls':calls,'STOCK_DUAL_EMBEDDING_AFTER_WHOLE_QUALIFIED_PARENT':after}
        exec(compile(ast.fix_missing_locations(ast.Module(body=nodes,type_ignores=[])),str(path)+'::nested_hook','exec'),scope)
        assert scope[nodes[0].name](None,2)==105 and events==['parent','dual'] and len(calls)==1
        try:actual.prepared_parent(prepared)
        except AssertionError:pass
        else:raise AssertionError('Duplicate dual hook accepted')
        checked.append({'source':str(path),'actual_nested_hook_order_exact':True});paths.append(path)
    create(A/'stock_dual_embedding_five_parent_hooks_CPU_controls_v1_20261010.json',{'status':'passed_actual_five_complete_parent_nested_hooks_two_bank_stage_GPU_and_full_future_pending','records':checked,'input_sha256':{str(p):sha(p) for p in paths},'new_fits':0,'new_scores':0,'future_X_read':False,'test_labels_read':False})
    print({'dual_parent_nested_hooks_passed':5,'actual_dual_GPU_stage_pending':True},flush=True)
if __name__=='__main__':main()
