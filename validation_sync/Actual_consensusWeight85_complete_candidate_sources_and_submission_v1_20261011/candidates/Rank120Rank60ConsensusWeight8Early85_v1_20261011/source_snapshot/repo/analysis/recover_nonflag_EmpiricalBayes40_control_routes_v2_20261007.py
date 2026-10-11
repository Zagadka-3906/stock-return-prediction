"""Preserve the real failed old-head wiring; correct service gates before first official score."""
from pathlib import Path
import sys,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start

def main():
    oldservice=A/'service_owned_workflows_20261006/nonflag_residual_EmpiricalBayes37_transform_preflight'
    assert not owned(read(oldservice/'native_launch.json'))
    assert read(oldservice/'service_execution.json')['status']=='failed'
    assert 'nonflag_residual_ridge_l001' in read(oldservice/'service_execution.json')['failure']
    oldhook=A/'run_nonflag_residual_EmpiricalBayes64_hook3_after_bank_20261007.py'
    hook=A/'run_nonflag_residual_EmpiricalBayes64_hook3_after_bank_v2_20261007.py';assert not hook.exists()
    text=oldhook.read_text(encoding='utf8').replace('nonflag_residual_Ridge10_plan_20261007.json','nonflag_residual_EmpiricalBayes6410_plan_20261007.json')
    out=A/'nonflag_residual_EmpiricalBayes64_native_hook3_preflight_20261007';assert out.is_dir() and not list(out.iterdir())
    text=text.replace('assert not out.exists(); out.mkdir()',"assert not out.exists() or not list(out.iterdir()); out.mkdir(exist_ok=True)")
    compile(text,str(hook),'exec');hook.write_text(text,encoding='utf8',newline='\n')
    oldwrapper=A/'run_nonflag_EmpiricalBayes40_actual_controls_20261007.py'
    wrapper=A/'run_nonflag_EmpiricalBayes40_actual_controls_v2_20261007.py';assert not wrapper.exists()
    text=oldwrapper.read_text(encoding='utf8').replace('run_nonflag_residual_EmpiricalBayes64_hook3_after_bank_20261007',
                                                   'run_nonflag_residual_EmpiricalBayes64_hook3_after_bank_v2_20261007')
    compile(text,str(wrapper),'exec');wrapper.write_text(text,encoding='utf8',newline='\n')
    modules=['verify_nonflag_EmpiricalBayes40_round130_sources_v1_20261007.py',
      'run_nonflag_EmpiricalBayes40_official_comparison_v1_20261007.py',
      'prepare_nonflag_EmpiricalBayes40_selected_candidate_v1_20261007.py',
      'publish_nonflag_EmpiricalBayes40_evidence_v1_20261007.py']
    receiver_sources=[]
    for name in modules:
        old=A/name;new=A/name.replace('_v1_','_v2_');assert not new.exists()
        original=old.read_text(encoding='utf8')
        text=original.replace("'nonflag_residual_EmpiricalBayes37_transform_preflight'","'nonflag_residual_EmpiricalBayes37_transform_preflight_v2'")
        assert text!=original,name
        if name.startswith('publish_'):
            needle="    if phase=='scores':\n        for row in proof['records']:";assert text.count(needle)==1
            text=text.replace(needle,"    sources += [A/'nonflag_EmpiricalBayes40_control_gate_recovery_v2_20261007.json',A/'run_nonflag_residual_EmpiricalBayes64_hook3_after_bank_v2_20261007.py',A/'run_nonflag_EmpiricalBayes40_actual_controls_v2_20261007.py',A/'nonflag_EmpiricalBayes40_prospective_routes_v3_20261007.json']\n"+needle)
            text=text.replace('完整128候选','完整130候选').replace('各16个新幅度','各12幅度').replace('共52项','共40项')
        if name.startswith('verify_'):
            needle='    for p in sources:';assert text.count(needle)==1
            extra="    sources += [A/'nonflag_EmpiricalBayes40_control_gate_recovery_v2_20261007.json',A/'nonflag_EmpiricalBayes40_prospective_routes_v3_20261007.json',A/'run_nonflag_EmpiricalBayes40_official_comparison_v2_20261007.py',A/'prepare_nonflag_EmpiricalBayes40_selected_candidate_v2_20261007.py',A/'publish_nonflag_EmpiricalBayes40_evidence_v2_20261007.py']\n"
            text=text.replace(needle,extra+needle)
        compile(text,str(new),'exec');new.write_text(text,encoding='utf8',newline='\n');receiver_sources.extend((old,new))
    oldadmitted=A/'run_nonflag_EmpiricalBayes40_admitted_comparison_v1_20261007.py'
    admitted=A/'run_nonflag_EmpiricalBayes40_admitted_comparison_v2_20261007.py';assert not admitted.exists()
    text=oldadmitted.read_text(encoding='utf8').replace('run_nonflag_EmpiricalBayes40_official_comparison_v1_20261007',
                                                     'run_nonflag_EmpiricalBayes40_official_comparison_v2_20261007')
    compile(text,str(admitted),'exec');admitted.write_text(text,encoding='utf8',newline='\n')
    paths=[Path(__file__),oldservice/'service_execution.json',oldservice/'stderr.log',oldhook,hook,oldwrapper,wrapper,
      *receiver_sources,oldadmitted,admitted,A/'nonflag_EmpiricalBayes40_prospective_routes_v3_20261007.json',
      A/'nonflag_EmpiricalBayes40_science_route_preparation_v1_20261007.json']
    pins={**read(paths[-1])['input_sha256'],**{str(p):sha(p) for p in paths}}
    for p,d in pins.items():assert sha(p)==d,p
    gate=A/'nonflag_EmpiricalBayes40_control_gate_recovery_v2_20261007.json'
    create(gate,{'status':'passed_pre_score_recovery_of_Bayes_native_head_plan_and_actual_service_gate_only',
      'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'input_sha256':pins,
      'actual_original_native10_fit_source_and_models_unchanged':True,'original_prediction_codec_and_future_stage_unchanged':True,
      'actual_original_failed_empty_hook_output_preserved':True,'official_score_count_before_recovery':0,
      'new_native_fits':0,'new_quality_scores':0,'test_labels_read':False})
    row=start('nonflag_residual_EmpiricalBayes37_transform_preflight_v2',wrapper.name,[],{**pins,str(gate):sha(gate)})
    create(A/'nonflag_EmpiricalBayes40_actual_recovered_controls_hidden_launch_v2_20261007.json',{
      'status':'started_actual3_hooks37_full111_cold_checks_with_real_Bayes_heads','identity':row,
      'input_sha256':pins,'new_quality_scores':0,'test_labels_read':False})
    print({'status':'started_actual_recovered_Bayes_controls','worker':row['owned_worker_pid']},flush=True)

if __name__=='__main__':main()
