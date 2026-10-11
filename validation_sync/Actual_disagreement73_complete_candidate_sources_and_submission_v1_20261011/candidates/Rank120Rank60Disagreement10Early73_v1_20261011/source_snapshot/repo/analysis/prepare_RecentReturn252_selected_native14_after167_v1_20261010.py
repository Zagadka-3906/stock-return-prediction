"""Prepare native qualification of current strongest recent-window screen; no future X or round assignment."""
from pathlib import Path
import sys,ast,copy
A=Path(__file__).resolve().parent;ROOT=A.parent;sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import create,sha
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed

def main():
    assert allowed()
    stageold=A/'protected_Return_after163_native_stage_v3_20261010.py'
    stagename='protected_RecentReturn252_after167_native_stage_v1_20261010.py'
    stage=stageold.read_text(encoding='utf8').replace('163','167').replace('protected_Return_after_complete167_native_v3_20261010','protected_RecentReturn252_after_complete167_native_v1_20261010').replace('returnhuber050','recent252returnhuber050')
    needle="    assert meta['features']==context._BF16_feature_names"
    assert stage.count(needle)==1
    stage=stage.replace(needle,"    assert meta['training_calendar_window']==252 and meta['days']<=252\n"+needle)
    predold=A/'predict_protected_Return_after163_complete_scheme_v4_20261010.py'
    predname='predict_protected_RecentReturn252_after167_complete_scheme_v1_20261010.py'
    pred=predold.read_text(encoding='utf8').replace('163','167').replace('protected_Return_after167_native_stage_v3_20261010','protected_RecentReturn252_after167_native_stage_v1_20261010').replace('PROTECTED_RETURN_AFTER_COMPLETE167','PROTECTED_RECENT252_AFTER_COMPLETE167')
    pred=pred.replace("PARENT_FILENAME='predict_protected_tail_after157_complete_scheme_v2_20261010.py'","PARENT_FILENAME='predict_protected_Return_after163_complete_scheme_v4_20261010.py'")
    assert pred.count("PARENT_FILENAME='predict_protected_Return_after163_complete_scheme_v4_20261010.py'")==1
    pilotold=A/'prepare_Return_protected_pilot67_and_selected_native14_v1_20261010.py'
    pilotname='qualify_RecentReturn252_after167_selected_native14_v1_20261010.py'
    pilot=pilotold.read_text(encoding='utf8')
    substitutions={
      'protected_Return_selected_native14_v1_20261010':'protected_RecentReturn252_selected_native14_v1_20261010',
      'actual_Return_after163_high_impact65_screen_v1_20261010':'actual_RecentReturn252_after167_high_impact65_screen_v1_20261010',
      'ReusedNN166Quality19_round166_full_registration_v1_20261009':'actual_RecentReturn252_after167_65_completion_main_v19_20261010',
      'protected_Return_after163_native_stage_v3_20261010':'protected_RecentReturn252_after167_native_stage_v1_20261010',
      'Return_after163_high_impact65_screen_v1_20261010':'RecentReturn252_after167_high_impact65_screen_v1_20261010',
      'protected_Return_after163_native_predictor_preparation_v1_20261010.json':'RecentReturn252_after167_selected_native14_source_admission_v1_20261010.json',
      'predict_protected_Return_after163_complete_scheme_v3_20261010.py':predname,
      'returnhuber050':'recent252returnhuber050',
      'ReturnHuber050':'RecentReturn252Huber050',
      'actual_protected_Return_selected_native14_location_v1_20261010':'actual_protected_RecentReturn252_selected_native14_location_v1_20261010',
      'r163':'r167',
    }
    for old,new in substitutions.items():pilot=pilot.replace(old,new)
    pilot=pilot.replace('for n in (163,165,166)','for n in (166,167)').replace('for n in (165,166)','for n in (166,167)')
    pilot=pilot.replace('anchor_round=163','anchor_round=167').replace('models[163]','models[167]').replace("'actual_scheme_base_round':163,'actual_comparison_parent_round':166","'actual_scheme_base_round':167,'actual_comparison_parent_round':167").replace("'original_complete_parent_round':163","'original_complete_parent_round':167")
    pilot=pilot.replace("closed('actual_forward20_own_controls_and_training_queue_v1_20261010')","closed('actual_recent252_return_own_controls_and_training_queue_v2_20261010')")
    outputs={stagename:stage,predname:pred,pilotname:pilot}
    for name,source in outputs.items():assert not (A/name).exists();compile(source,str(A/name),'exec')
    for name,source in outputs.items():(A/name).write_text(source,encoding='utf8',newline='\n')
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
