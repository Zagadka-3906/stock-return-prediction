from pathlib import Path
import sys,ast,copy
A=Path(__file__).resolve().parent;ROOT=A.parent;sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import create,sha
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed

def main():
    assert allowed()
    stageold=A/'protected_Return_after163_native_stage_v3_20261010.py'
    predold=A/'predict_protected_Return_after163_complete_scheme_v4_20261010.py'
    pilotold=A/'prepare_Return_protected_pilot67_and_selected_native14_v1_20261010.py'
    stagename='protected_RecentReturn252_after167_native_stage_v1_20261010.py'
    predname='predict_protected_RecentReturn252_after167_complete_scheme_v2_20261010.py'
    pilotname='qualify_RecentReturn252_after167_selected_native14_v2_20261010.py'
    original=A/'predict_protected_RecentReturn252_after167_complete_scheme_v1_20261010.py'
    pred=original.read_text(encoding='utf8')
    before="needle='        value,report="
    after="needle='\\n        value,report="
    assert pred.count(before)==1
    pred=pred.replace(before,after)
    pilot=(A/'qualify_RecentReturn252_after167_selected_native14_v1_20261010.py').read_text(encoding='utf8').replace(original.name,predname)
    outputs={predname:pred,pilotname:pilot}
    for n,text in outputs.items():assert not (A/n).exists();compile(text,str(A/n),'exec')
    for n,text in outputs.items():(A/n).write_text(text,encoding='utf8',newline='\n')
    create(A/'RecentReturn252_after167_callback_prototype_correction_v2_20261010.json',{'status':'preserved_unadopted_v1_literal_match_failure_corrected_only_new_v2','failure':'AssertionError: actual parent167 contains both literal needle and callback; require real leading newline','previous_generator_sha256':sha(A/'prepare_RecentReturn252_selected_native14_after167_v1_20261010.py'),'new_native_fits':0,'new_quality_scores':0,'future_X_read':False})
    # Execute the actual extracted parent167 callback; restore its AST to prove every other statement survives.
    namespace={'__file__':str(A/predname),'__name__':'checked_new_recent252_wrapper'}
    exec(compile(pred,str(A/predname),'exec'),namespace)
    oldtext=predold.read_text(encoding='utf8');prepared=namespace['prepared_parent167'](oldtext)
    oldtree=ast.parse(oldtext);newtree=ast.parse(prepared)
    callbacks=[n for n in ast.walk(newtree) if isinstance(n,ast.Return) and isinstance(n.value,ast.Call) and isinstance(n.value.func,ast.Name) and n.value.func.id=='PROTECTED_RECENT252_AFTER_COMPLETE167']
    assert len(callbacks)==1
    class Restore(ast.NodeTransformer):
        def visit_Return(self,n):
            if isinstance(n.value,ast.Call) and isinstance(n.value.func,ast.Name) and n.value.func.id=='PROTECTED_RECENT252_AFTER_COMPLETE167':n.value=ast.Name(id='value',ctx=ast.Load())
            return n
    assert ast.dump(Restore().visit(copy.deepcopy(newtree)))==ast.dump(oldtree)
    fn=next(n for n in ast.walk(newtree) if isinstance(n,ast.FunctionDef) and n.name=='tail_stage')
    module=ast.fix_missing_locations(ast.Module(body=[fn],type_ignores=[]));rows=[]
    for value in (-3.,0.,7.):
        events=[];calls=[]
        def old_stage(ns,context,parent,spec,component):events.append(('complete167_last_stage',parent));return parent+2.,{'parent':parent}
        def recent_stage(context,parent):events.append(('new_recent252_after167',parent));return parent*7.
        scope={'after_parent':old_stage,'ns':None,'spec':None,'component':None,'calls':calls,'PROTECTED_RECENT252_AFTER_COMPLETE167':recent_stage}
        exec(compile(module,str(predold),'exec'),scope);result=scope['tail_stage'](None,value)
        assert result==(value+2.)*7. and events==[('complete167_last_stage',value),('new_recent252_after167',value+2.)] and calls==[{'parent':value}]
        rows.append({'parent':value,'result':result,'actual_extracted_parent167_callback_order_exact':True})
    create(A/'RecentReturn252_after167_selected_native14_source_admission_v1_20261010.json',{'status':'compiled_native14_routes_and_passed_complete_parent167_AST_preservation_and3_CPU_callback_order_cases','records':rows,'input_sha256':{str(p):sha(p) for p in [Path(__file__),stageold,predold,pilotold,*[A/n for n in outputs]]},'actual_scheme_base_round':167,'selected_native14_future_X_and_full_candidate_qualification_pending':True,'new_quality_scores':0,'new_native_fits':0,'test_X_read':False,'test_labels_read':False})
    from handoff_ready_goss_full_execution_20261006 import start_service
    assert allowed()
    row=start_service('RecentReturn252_after167_selected_native14_v1_20261010',pilotname,[],{str(A/pilotname):sha(A/pilotname),str(A/stagename):sha(A/stagename),str(A/predname):sha(A/predname)})
    create(A/'RecentReturn252_after167_selected_native14_activation_v1_20261010.json',row)
    print({'selected_native14_worker':row['owned_worker_pid'],'CPU_callback_controls':3,'full_candidate_round_assignment_pending':True},flush=True)
if __name__=='__main__':main()
