"""Prepare whole152 prediction composition and14 actual saved-state calendar controls."""
from pathlib import Path
import sys,ast,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
def replace(s,before,after,count=1):
    assert s.count(before)==count,(before,s.count(before),count);return s.replace(before,after)
def write(name,text):
    ast.parse(text);p=A/name
    with p.open('x',encoding='utf8',newline='\n') as f:f.write(text)
    return p
def main():
    native_source=A/'BF16Medium153_complete_parent_native_stage_v1_20261009.py'
    s=native_source.read_text(encoding='utf8').replace('BF16_medium2048_seed09_complete_parent_rank_CDF','BF16_flag_after152157_complete_parent_rank_CDF')
    s=s.replace('BF16_medium2048_seed09_full_','BF16_flag_after152157_full_')
    native=write('BF16FlagAfter152157_complete_parent_native_stage_v1_20261009.py',s)
    predictor_source=A/'predict_BF16Medium153_complete_parent_scheme_v1_20261009.py';s=predictor_source.read_text(encoding='utf8')
    s=replace(s,'predict_AdaptiveJointCrossHuber_complete_parent_scheme_v1_20261008.py','predict_SparseAfter148_complete_parent_scheme_v1_20261009.py')
    s=replace(s,"    needle='        value,report=after_parent(ns,context,teacher,parent,spec,components);calls.append(report);return value'","    needle='  calls.append(report);return value'")
    s=replace(s,"'        value,report=after_parent(ns,context,teacher,parent,spec,components);calls.append(report);return MEDIUM_AFTER_COMPLETE148(context,value)'","'  calls.append(report);return FLAG_AFTER_COMPLETE152(context,value)'")
    s=replace(s,'BF16Medium153_complete_parent_native_stage_v1_20261009','BF16FlagAfter152157_complete_parent_native_stage_v1_20261009')
    s=replace(s,"spec['original_complete_parent_round']==148","spec['original_complete_parent_round']==152")
    s=replace(s,"'MEDIUM_AFTER_COMPLETE148':medium_stage","'FLAG_AFTER_COMPLETE152':medium_stage")
    s=s.replace('BF16_medium2048_seed09_full_','BF16_flag_after152157_full_').replace('BF16Medium153','BF16FlagAfter152157')
    s=s.replace('complete148_before_','complete152_before_').replace('actual_complete148_then_medium153','actual_complete152_then_flag157')
    s=s.replace('actual_entire148_then_','actual_entire152_then_').replace('complete148_all_original_branches','complete152_all_original_branches')
    s=s.replace('passed_actual_complete148_and_','passed_actual_complete152_and_')
    predictor=write('predict_BF16FlagAfter152157_complete_parent_scheme_v1_20261009.py',s)
    import predict_BF16FlagAfter152157_complete_parent_scheme_v1_20261009 as module
    parent=A/module.PARENT_FILENAME;before=parent.read_text(encoding='utf8');after=module.prepared_parent148(before);ast.parse(after)
    defs=lambda text:{n.name:n for n in ast.walk(ast.parse(text)) if isinstance(n,ast.FunctionDef)}
    left,right=defs(before),defs(after);assert left.keys()==right.keys()
    for name in left:
        if name not in ('predict','sparse_stage'):assert ast.dump(left[name],include_attributes=False)==ast.dump(right[name],include_attributes=False),name
    returns=[n for n in ast.walk(right['sparse_stage']) if isinstance(n,ast.Return)]
    assert len(returns)==1 and ast.unparse(returns[0].value)=='FLAG_AFTER_COMPLETE152(context, value)'
    import predict_AdaptiveJointCrossHuber_complete_parent_scheme_v1_20261008 as original148
    backends=[];files=[Path(__file__),native_source,native,predictor_source,predictor,parent]
    for backend,(filename,_,_) in original148.BACKENDS.items():
        p=A/filename;ast.parse(original148.prepared_backend(p.read_text(encoding='utf8'),backend));files.append(p);backends.append({'backend':backend,'original_parent_ABI_compiles':True})
    control_source=A/'verify_BF16Medium153_native42_calendar_v1_20261009.py';s=control_source.read_text(encoding='utf8')
    s=replace(s,"    service=A/'service_owned_workflows_20261006/BF16Medium153_independent_full5_GPU_controls_v1_20261009'","    service=A/'service_owned_workflows_20261006/BF16Drop05_81_round156_full_registration_v1_20261009'")
    s=s.replace('BF16Medium153_native42_calendar_v1_20261009','BF16FlagAfter152157_native14_calendar_v1_20261009')
    s=replace(s,'import BF16Medium153_complete_parent_native_stage_v1_20261009 as stage','import BF16FlagAfter152157_complete_parent_native_stage_v1_20261009 as stage')
    s=s.replace("parentpath=A/'optimization_20261003_r148/selected_validation.npy'","parentpath=A/'optimization_20261003_r152/selected_validation.npy'")
    s=s.replace("A/'BF16Medium153_complete_parent_rank_CDF_v1_20261009.py'","A/'BF16Medium153_complete_parent_rank_CDF_v1_20261009.py',A/'optimization_20261003_r152/full_registration_execution.json'")
    s=replace(s,"for role,weight in zip(ROLES,(.004,.064,.25)):","for role,weight in [('flag_valid',.008)]:")
    s=replace(s,'assert len(records)==42 and len(prefit)==7','assert len(records)==14 and len(prefit)==7')
    s=s.replace("'historical_cases':30,'calendar_remapped_training_cases':12,'cold_cases':42","'historical_cases':10,'calendar_remapped_training_cases':4,'cold_cases':14")
    s=s.replace("'actual_historical_cases':30,'actual_calendar_cases':12,'actual_cold_cases':42","'actual_historical_cases':10,'actual_calendar_cases':4,'actual_cold_cases':14")
    s=s.replace('states42_native_reload_independent_calendar_and42_cold_controls','states14_native_reload_independent_calendar_and14_cold_controls')
    s=s.replace('six_state_native42_cold42','six_state_native14_cold14').replace('native42_cold42_on_E','native14_cold14_on_E')
    s=s.replace('actual_BF16Medium153_native42_calendar_location_v1_20261009.json','actual_BF16FlagAfter152157_native14_calendar_location_v1_20261009.json')
    s=s.replace('/42, state','/14, state').replace('medium153 native','flag_after152157 native')
    native_control=write('verify_BF16FlagAfter152157_native14_calendar_v1_20261009.py',s);files.extend((control_source,native_control))
    proof=A/'BF16FlagAfter152157_complete_native_predictor_preparation_v58_20261009.json'
    create(proof,{'status':'passed_only_final152_sparse_stage_return_gets_new_neural_hook_and5_original_parent_ABI_controls',
        'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'input_sha256':{str(p):sha(p) for p in files},
        'original5_parent_backends':backends,'original_sparse152_code_and_all_earlier148_branches_unchanged':True,
        'future_end_to_end_candidate_replays_still_required':True,'actual_future_X_read':False,'new_quality_scores':0,
        'expected_actual_saved_state_native_controls':14,'expected_native_cold_controls':14,'prefit_rejections_expected':7})
    from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start
    row=start('BF16FlagAfter152157_actual_native14_calendar_v1_20261009',native_control.name,[],{str(proof):sha(proof),str(native_control):sha(native_control)})
    create(A/'BF16FlagAfter152157_native14_calendar_launch_v58_20261009.json',{'launch':row,'waits_actual156_full_before_using_GPU':True})
    print({'original_ABI_controls':5,'native_controls_queued':14,'owned_worker':row['owned_worker_pid']},flush=True)
if __name__=='__main__':main()
