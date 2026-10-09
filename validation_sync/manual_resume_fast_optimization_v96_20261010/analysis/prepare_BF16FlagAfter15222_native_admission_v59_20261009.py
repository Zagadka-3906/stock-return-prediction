"""Require actual six-state14 native/calendar replay before the22 official scores."""
from pathlib import Path
import sys,ast,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
def main():
    original=A/'run_BF16FlagAfter15222_official_comparison_v1_20261009.py'
    oldmeta=A/'BF16FlagAfter15222_quality_preparation_v56_20261009.json';meta=A/'BF16FlagAfter15222_quality_preparation_v59_20261009.json'
    s=original.read_text(encoding='utf8').replace(oldmeta.name,meta.name)
    marker="    closed('BF16Drop05_81_round156_full_registration_v1_20261009')";assert s.count(marker)==1
    s=s.replace(marker,marker+"\n    closed('BF16FlagAfter152157_actual_native14_calendar_v1_20261009')")
    marker="    assert (control['actual_parent_round'],control['actual_full_cases'],control['actual_cold_cases'])==(152,17,51)";assert s.count(marker)==1
    extra="""
    native_pointer=A/'actual_BF16FlagAfter152157_native14_calendar_location_v1_20261009.json'
    native_proof_path=Path(read(native_pointer)['output'])/'verification.json'
    assert sha(native_proof_path)==read(native_pointer)['verification_sha256']
    native_proof=read(native_proof_path)
    assert (native_proof['actual_saved_states'],native_proof['actual_historical_cases'],native_proof['actual_calendar_cases'],native_proof['actual_cold_cases'])==(6,10,4,14)
    assert len(native_proof['records'])==14 and len(native_proof['prefit_rejections'])==7
"""
    s=s.replace(marker,marker+extra)
    marker="    pins={**control['input_sha256'],**{str(p):sha(p) for p in sources}}";assert s.count(marker)==1
    s=s.replace(marker,"    sources += [native_pointer,native_proof_path,A/'BF16FlagAfter152157_complete_native_predictor_preparation_v58_20261009.json']\n    pins={**control['input_sha256'],**native_proof['input_sha256'],**{str(p):sha(p) for p in sources}}")
    driver=A/'run_BF16FlagAfter15222_official_comparison_v2_20261009.py';ast.parse(s)
    with driver.open('x',encoding='utf8',newline='\n') as f:f.write(s)
    for name in ('closed','write','best_key'):
        functions=lambda text:{n.name:n for n in ast.parse(text).body if isinstance(n,ast.FunctionDef)}
        assert ast.dump(functions(s)[name],include_attributes=False)==ast.dump(functions(original.read_text(encoding='utf8'))[name],include_attributes=False)
    proof=A/'BF16FlagAfter152157_complete_native_predictor_preparation_v58_20261009.json'
    create(meta,{'status':'prepared22_native14_and_full17_source_admission_before_quality',
        'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'fixed_scientific_stage_base_round':152,
        'comparison_anchor_rounds':list(range(152,157)),'expected_quality_cases':22,
        'native_controls_required':14,'native_cold_required':14,'native_prefit_rejections_required':7,
        'input_sha256':{str(p):sha(p) for p in (Path(__file__),oldmeta,original,driver,proof)},
        'actual_future_X_read':False,'test_labels_read':False,'new_quality_scores':0})
    assert not Path('E:/赛题五_本机临时/BF16FlagAfter15222_official_comparison_v1_20261009').exists()
    from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start
    row=start('BF16FlagAfter15222_official_comparison_v2_20261009',driver.name,[],{str(meta):sha(meta),str(driver):sha(driver)})
    from handoff_joint_goss_round97_full_execution_20261006 import stack,suspended_idle,retire_suspended
    old=read(A/'service_owned_workflows_20261006/BF16FlagAfter15222_official_comparison_v1_20261009/native_launch.json');assert owned(old)
    line=next(line for line in stack(old['owned_worker_pid']).splitlines() if '    closed (' in line)
    parent,worker,idle=suspended_idle(old,line)
    try:retire_suspended(old,row)
    except BaseException:
        if parent.is_running():parent.resume()
        if worker.is_running():worker.resume()
        raise
    create(A/'BF16FlagAfter15222_native_gate_handoff_v59_20261009.json',{'old_launch':old,'new_launch':row,'old_idle_stack':idle,
        'retired_only_child_free_unstarted_quality_controller':True,'official_scores_restarted':0,
        'native_inference_or_GPU_training_workers_stopped':0,'source_admission_enforced_before_new_quality':True})
    print({'actual_quality_version':2,'native_controls_required':14,'owned_worker':row['owned_worker_pid']},flush=True)
if __name__=='__main__':main()
