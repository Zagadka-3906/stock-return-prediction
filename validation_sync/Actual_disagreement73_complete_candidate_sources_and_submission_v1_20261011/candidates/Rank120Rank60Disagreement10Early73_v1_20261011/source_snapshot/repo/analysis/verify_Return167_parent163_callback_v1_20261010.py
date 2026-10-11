"""Check actual163 source preservation and execute the extracted new callback order on CPU."""
from pathlib import Path
import sys,ast,copy
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import sha,create
def main():
    import predict_protected_Return_after163_complete_scheme_v3_20261010 as new
    original=A/new.PARENT_FILENAME;s=original.read_text(encoding='utf8');prepared=new.prepared_parent163(s)
    assert new.PARENT_FILENAME=='predict_protected_tail_after157_complete_scheme_v2_20261010.py'
    old_ast=ast.parse(s);new_ast=ast.parse(prepared)
    changed=[]
    for old,node in zip(ast.walk(old_ast),ast.walk(new_ast)):
        if isinstance(old,ast.Return) and isinstance(node,ast.Return) and ast.dump(old)!=ast.dump(node):changed.append((old,node))
    assert len(changed)==1
    old,node=changed[0]
    assert isinstance(old.value,ast.Name) and old.value.id=='value'
    assert isinstance(node.value,ast.Call) and node.value.func.id=='PROTECTED_RETURN_AFTER_COMPLETE163'
    restored=copy.deepcopy(new_ast)
    class Restore(ast.NodeTransformer):
        def visit_Return(self,node):
            if isinstance(node.value,ast.Call) and isinstance(node.value.func,ast.Name) and node.value.func.id=='PROTECTED_RETURN_AFTER_COMPLETE163':node.value=ast.Name(id='value',ctx=ast.Load())
            return node
    restored=Restore().visit(restored)
    assert ast.dump(restored)==ast.dump(old_ast),'All original163 AST except one appended callback must stay identical'
    fn=next(n for n in ast.walk(new_ast) if isinstance(n,ast.FunctionDef) and n.name=='tail_stage')
    module=ast.fix_missing_locations(ast.Module(body=[fn],type_ignores=[]));rows=[]
    for parent in (-3.,0.,7.):
        events=[];calls=[]
        def old_stage(ns,context,value,spec,component):events.append(('original163_tail',value));return value+2.,{'parent':value}
        def appended(context,value):events.append(('new_Return_after_entire163',value));return value*7.
        scope={'after_parent':old_stage,'ns':None,'spec':{'old_parent':157},'component':{'recipe':'huber010'},'calls':calls,'PROTECTED_RETURN_AFTER_COMPLETE163':appended}
        exec(compile(module,str(original),'exec'),scope)
        out=scope['tail_stage'](None,parent)
        assert out==(parent+2.)*7. and events==[('original163_tail',parent),('new_Return_after_entire163',parent+2.)] and calls==[{'parent':parent}]
        rows.append({'parent':parent,'output':out,'actual_extracted_parent163_callback_order_exact':True})
    create(A/'Return167_actual_parent163_source_and_callback_controls_v1_20261010.json',{'status':'passed_exact_original163_AST_preservation_and3_extracted_callback_CPU_order_cases','records':rows,'input_sha256':{str(p):sha(p) for p in [Path(__file__),original,Path(new.__file__)]},'actual_full_graph_inference_not_claimed':True,'GPU_used':False,'new_quality_scores':0,'test_labels_read':False})
    print('PASS original163 AST preserved and actual appended callback ordering3 cases; full inference pending',flush=True)
if __name__=='__main__':main()
