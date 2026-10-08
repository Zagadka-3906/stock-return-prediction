"""Declare100 TRAIN-only cases with a distinct new stage preserving the full qualified Cone parent."""
from pathlib import Path
import ast,hashlib,sys,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
def save(name,text):
    path=A/name;assert not path.exists();compile(text,str(path),'exec');path.write_text(text,encoding='utf8',newline='\n');return path
def main():
    import nonflag_ConeRidgeAlpha8_64_streamed_v1_20261008 as native
    heads=tuple('alpha_'+name.removeprefix('nonflag_residual_coneRidge64_') for name in native.CONFIGS)
    groups=tuple((((head,),sign),((head,),sign)) for head in heads for sign in (1.,-1.))
    assert len(heads)==8 and len(groups)==16
    original=A/'ConeRidge64_complete_parent_CDF_v1_20261008.py';text=original.read_text(encoding='utf8');tree=ast.parse(text)
    lines=text.splitlines(keepends=True)
    for node in reversed([n for n in tree.body if isinstance(n,ast.Assign) and isinstance(n.targets[0],ast.Name) and n.targets[0].id in ('HEADS','GROUPS')]):
        value=heads if node.targets[0].id=='HEADS' else groups
        lines[node.lineno-1:node.end_lineno]=[node.targets[0].id+' = '+repr(value)+'\n']
    codec=save('ConeRidgeAlpha8_64_complete_parent_CDF_v1_20261008.py',''.join(lines))
    original_stage=A/'ConeRidge64_complete_parent_native_stage_v1_20261008.py'
    stage=save('ConeRidgeAlpha8_64_complete_parent_native_stage_v1_20261008.py',original_stage.read_text(encoding='utf8').replace('ConeRidge64','ConeRidgeAlpha8_64'))
    original_wrapper=A/'predict_ConeRidge64_complete_parent_scheme_v1_20261008.py'
    wrapper_text=original_wrapper.read_text(encoding='utf8').replace('ConeRidge64','ConeRidgeAlpha8_64')
    needle='BACKENDS={';assert wrapper_text.count(needle)==1
    wrapper_text=wrapper_text.replace(needle,needle+"\n    'ConeRidge64':('predict_ConeRidge64_complete_parent_scheme_v1_20261008.py','ConeRidge64_complete_parent_native_stage_v1_20261008',True),")
    needle="    for key,name in (";assert wrapper_text.count(needle)==1
    wrapper_text=wrapper_text.replace(needle,needle+"('nonflag_CPU_ConeRidge64_complete_parent_CDF','ConeRidge64'),")
    wrapper=save('predict_ConeRidgeAlpha8_64_complete_parent_scheme_v1_20261008.py',wrapper_text)
    amps=(.0001,.00025,.0005,.001,.0015,.0025)
    cases=[{'group':group,'share':.5,'amplitude':amp} for group in range(16) for amp in amps]
    assert len(cases)==96
    sources=[Path(__file__),Path(native.__file__),original,codec,original_stage,stage,original_wrapper,wrapper,
        A/'nonflag_ConeRidgeAlpha8_64_bank40_plan_v2_20261008.json',A/'ConeRidgeAlpha8_probe_pointer_recovery_v2_20261008.json']
    create(A/'ConeRidgeAlpha100_round144_blueprint_v1_20261008.json',{
        'status':'frozen96_new_alpha_stages_three_qualified_anchors_and_exact_identity_before_any144_quality',
        'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'round':144,'expected_scored_cases':100,
        'anchors':[132,134,143],'amplitudes':list(amps),'heads':dict(zip(heads,native.CONFIGS)),
        'new_cases':cases,'expected_transform_cases':97,'expected_cold_cases':291,
        'expected_native_historical_hooks':48,'expected_calendar_controls':48,'expected_calendar_day_controls':96,
        'graph_key':'nonflag_CPU_ConeRidgeAlpha8_64_complete_parent_CDF',
        'already_present_ConeRidge64_parent_stage_preserved_as_distinct_inner_stage':True,
        'current_parent_selected_only_after_actual143_complete_candidate_QA54_and_main':True,
        'all40_own_mature_saved_models_and_independent_BVLS_and40_causal_refits_required':True,
        'new_model_fits_by_grid':0,'actual_quality_scores':0,'full100_scoring_freeze_candidate_native_independent_cold80_QA55_main_still_required':True,
        'input_sha256':{str(p):sha(p) for p in sources},'test_labels_read':False,'global_exhaustion_claimed':False})
    # Execute every inserted adapter plus strict priority preserving the existing inner Cone stage.
    from types import SimpleNamespace
    import numpy as np
    import importlib
    w=importlib.import_module(wrapper.stem);records=[];pins=list(sources)
    for backend,(filename,module,has_teacher) in w.BACKENDS.items():
        path=A/filename;pins.append(path);prepared=w.prepared_backend(path.read_text(encoding='utf8'),backend);compile(prepared,str(path),'exec')
        nodes=[n for n in ast.walk(ast.parse(prepared)) if isinstance(n,ast.FunctionDef) and n.name=='after_parent'];assert len(nodes)==1
        teacher=np.array([-.2,0.,.4]);parent=np.array([4.,5.,6.]);context=SimpleNamespace();events=[]
        def complete(*args):
            assert args[1] is context;events.append('complete_parent');return parent+2.,{'all_prior_stages_preserved':True}
        complete=w.teacher_capture(complete) if has_teacher else complete
        if not has_teacher:w.teacher_capture(lambda *args:(parent,{}))(None,context,teacher,parent,{},[])
        def appended(ctx,value,passed):
            assert ctx is context and np.array_equal(value,parent+2.) and ctx._ConeRidgeAlpha8_64_teacher106 is teacher
            assert passed is teacher if has_teacher else passed is None
            events.append('new_alpha_stage');return value+3.
        namespace={'COMPLETE_PARENT_AFTER':complete,'HUBER_CROSS_AFTER_COMPLETE_PARENT':appended}
        exec(compile(ast.fix_missing_locations(ast.Module(body=nodes,type_ignores=[])),str(path),'exec'),namespace)
        args=(None,context,teacher,parent,{},[]) if has_teacher else (None,context,parent,{}, {})
        result,report=namespace['after_parent'](*args)
        assert np.array_equal(result,parent+5.) and events==['complete_parent','new_alpha_stage'] and report=={'all_prior_stages_preserved':True}
        records.append({'backend':backend,'actual_inserted_adapter_executed':True,'all_inner_parent_stages_before_new_alpha':True,'teacher106_identity_preserved':True})
    assert len(records)==9
    graph={'nonflag_CPU_ReverseBayes64_residual_CDF':{},'nonflag_CPU_KrylovGram64_complete_parent_CDF':{},'nonflag_CPU_ConeRidge64_complete_parent_CDF':{}}
    assert w.backend_for(graph)=='ConeRidge64'
    create(A/'ConeRidgeAlpha144_native_receiver_preflight_v1_20261008.json',{
        'status':'passed9_actual_complete_parent_adapter_contracts_including_preserved_inner_Cone_stage',
        'input_sha256':{str(p):sha(p) for p in dict.fromkeys(pins)},'records':records,'actual_adapter_controls':9,
        'actual_model_or_future_inference_not_claimed':True,'new_quality_scores':0,'test_labels_read':False})
    print('Round144100-case blueprint frozen; nine actual adapter contracts passed, including the full Cone143 parent.',flush=True)
if __name__=='__main__':main()
