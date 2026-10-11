"""Prepare calendar controls and execute five adapter contracts without future X or labels."""
from pathlib import Path
from types import SimpleNamespace
import sys
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create


def main():
    import numpy as np
    import predict_HuberCrossFamily_complete_parent_scheme_v1_20261008 as wrapper
    plan=A/'HuberCrossFamily112_round139_plan_v1_20261008.json'
    assert read(plan)['expected_scored_cases']==112
    sources=[Path(__file__),plan,Path(wrapper.__file__)];records=[]
    for backend,(filename,module,has_teacher) in wrapper.BACKENDS.items():
        original=A/filename;text=wrapper.prepared_backend(original.read_text(encoding='utf8'),backend)
        compile(text,str(original),'exec');sources.append(original)
        # Execute the adapter's actual inserted function against an isolated pure sentinel.
        import ast
        tree=ast.parse(text)
        inserted=[node for node in ast.walk(tree) if isinstance(node,ast.FunctionDef) and node.name=='after_parent']
        assert len(inserted)==1
        teacher=np.array([-.2,0.,.4],dtype=np.float64);parent=np.array([4.,5.,6.],dtype=np.float64)
        ctx=SimpleNamespace();events=[]
        def complete(*args):
            assert args[1] is ctx;events.append('complete_parent');return parent+2.,{'original_parent_report':True}
        complete=wrapper.teacher_capture(complete) if has_teacher else complete
        if not has_teacher:
            capture=wrapper.teacher_capture(lambda *args:(parent,{}))
            capture(None,ctx,teacher,parent,{},[])
        def appended(context,value,passed_teacher):
            assert context is ctx and np.array_equal(value,parent+2.)
            assert context._HuberCrossFamily_teacher106 is teacher
            assert passed_teacher is teacher if has_teacher else passed_teacher is None
            events.append('new_stage');return value+3.
        namespace={'COMPLETE_PARENT_AFTER':complete,'HUBER_CROSS_AFTER_COMPLETE_PARENT':appended}
        exec(compile(ast.fix_missing_locations(ast.Module(body=inserted,type_ignores=[])),str(original),'exec'),namespace)
        args=(None,ctx,teacher,parent,{},[]) if has_teacher else (None,ctx,parent,{}, {})
        result,report=namespace['after_parent'](*args)
        assert events==['complete_parent','new_stage'] and np.array_equal(result,parent+5.) and report=={'original_parent_report':True}
        records.append({'backend':backend,'actual_inserted_adapter_executed':True,'teacher106_identity_preserved':True,
            'complete_parent_before_new_stage':True,'full_inference_not_claimed':True})
    stages=[('nonflag_CPU_ReverseBayes64_residual_CDF','ReverseBayes'),('BF16_complete_parent_rank_CDF','BF16'),
        ('nonflag_CPU_CrossFamily_complete_parent_CDF','CrossFamily'),('nonflag_CPU_HuberIRLS64_complete_parent_CDF','Huber'),
        ('BF16_reverse_complete_parent_rank_CDF','ReverseBF16')]
    graph={}
    for key,expected in stages:
        graph[key]={'prospective_only':True};assert wrapper.backend_for(graph)==expected
    source=A/'verify_multiyear_residual_native_calendar_v1_20261008.py';sources.append(source)
    text=source.read_text(encoding='utf8')
    first=text.index('    import CrossFamily_complete_parent_native_stage');last=text.index('    feature_names_=',first)
    text=text[:first]+"    import HuberCrossFamily_complete_parent_native_stage_v1_20261008 as cross\n    from HuberCrossFamily_complete_parent_CDF_v1_20261008 import GROUPS\n    plan=read(A/'HuberCrossFamily112_round139_plan_v1_20261008.json')\n"+text[last:]
    first=text.index('    sources=[');last=text.index('    pins=',first)
    text=text[:first]+'''    sources=[Path(__file__),FEATURE_FILE,frame_path,teacher_path,parent_path,authoritative,authoritative_proof,
        A/'HuberCrossFamily112_round139_plan_v1_20261008.json',
        A/'HuberCrossFamily_complete_parent_native_stage_v1_20261008.py',A/'HuberCrossFamily_complete_parent_CDF_v1_20261008.py']
    all_components={'CrossFamily':{}}
    for head,row in plan['heads'].items():
        info_path=Path(row['infos']['2025']);info=read(info_path);kind=row['state_kind']
        item={'head':head,'name':info['name'],'state_kind':row['native_stage_state_kind'],
            'path':info['native_model_path'],'sha256':info['native_model_sha256'],
            'independent_state_path':info['independent_'+kind+'_state_path'],
            'independent_state_sha256':info['independent_'+kind+'_state_sha256'],'training_info':info}
        all_components['CrossFamily'][head]=item;sources += [info_path,Path(item['path']),Path(item['independent_state_path'])]
''' +text[last:]
    text=text.replace("(('CrossFamily',cross),('Huber',huber))","(('CrossFamily',cross),)")
    text=text.replace("range(5 if family=='CrossFamily' else 6)","range(6)")
    text=text.replace('multiyear_residual_native_calendar_v1_20261008','HuberCrossFamily_multiyear_native_calendar_v1_20261008')
    text=text.replace('actual_multiyear_residual_calendar_location_v1_20261008','actual_HuberCrossFamily_multiyear_calendar_location_v1_20261008')
    text=text.replace('passed_actual33_saved2025_multiyear_native_calendar_controls_and66_day_controls','passed_actual18_Huber_crossfamily_saved2025_calendar_controls_and36_day_controls')
    text=text.replace('passed_actual33_multiyear_calendar_controls_on_E','passed_actual18_Huber_crossfamily_multiyear_calendar_controls_on_E')
    text=text.replace("'actual_calendar_cases':33,'actual_whole_day_controls':66","'actual_calendar_cases':18,'actual_whole_day_controls':36")
    target=A/'verify_HuberCrossFamily_multiyear_native_calendar_v1_20261008.py'
    assert not target.exists();compile(text,str(target),'exec');target.write_text(text,encoding='utf8',newline='\n');sources.append(target)
    create(A/'HuberCrossFamily139_native_receiver_preflight_v1_20261008.json',{
        'status':'passed_five_actual_inserted_adapter_contracts_and_compiled_historical_calendar_receiver',
        'input_sha256':{str(p):sha(p) for p in sources},'adapter_controls':records,'backend_priority_cases':5,
        'new_fits':0,'new_official_scores':0,'new_actual_future_inference_claimed':False,'test_labels_read':False})
    from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start
    launch=start('HuberCrossFamily_multiyear_native_calendar_v1_20261008',target,[])
    create(A/'actual_HuberCrossFamily139_calendar_hidden_launch_v1_20261008.json',launch)
    print('Five adapter contracts passed; actual18/36 historical calendar controls started.',flush=True)


if __name__=='__main__':main()
