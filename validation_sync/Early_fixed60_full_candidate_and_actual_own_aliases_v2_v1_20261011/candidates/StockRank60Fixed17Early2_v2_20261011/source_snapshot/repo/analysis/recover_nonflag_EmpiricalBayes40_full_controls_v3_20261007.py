"""Preserve native3 success and the real inherited bank-status failure before full37 controls."""
from pathlib import Path
import sys,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start

def main():
    failed=A/'service_owned_workflows_20261006/nonflag_residual_EmpiricalBayes37_transform_preflight_v2'
    assert not owned(read(failed/'native_launch.json')) and read(failed/'service_execution.json')['status']=='failed'
    native=A/'nonflag_residual_EmpiricalBayes64_native_hook3_preflight_20261007/verification.json'
    assert len(read(native)['records'])==3
    old=A/'verify_nonflag_residual_EmpiricalBayes37_transform_20261007.py'
    new=A/'verify_nonflag_residual_EmpiricalBayes37_transform_v3_20261007.py';assert not new.exists()
    text=old.read_text(encoding='utf8').replace(
      'passed_actual10_nonflag_residual_Ridge_mature_native_reload_independent_and_prefix_controls',
      'passed_actual10_nonflag_residual_EmpiricalBayes64_mature_native_reload_independent_and_prefix_controls')
    assert text!=old.read_text(encoding='utf8')
    compile(text,str(new),'exec');new.write_text(text,encoding='utf8',newline='\n')
    paths=[Path(__file__),old,new,native,failed/'service_execution.json',failed/'stderr.log']
    for stem in ['verify_nonflag_EmpiricalBayes40_round130_sources','run_nonflag_EmpiricalBayes40_official_comparison',
      'prepare_nonflag_EmpiricalBayes40_selected_candidate','publish_nonflag_EmpiricalBayes40_evidence']:
        old=A/(stem+'_v2_20261007.py');new_receiver=A/(stem+'_v3_20261007.py');assert not new_receiver.exists()
        text=old.read_text(encoding='utf8').replace("'nonflag_residual_EmpiricalBayes37_transform_preflight_v2'",
                                                "'nonflag_residual_EmpiricalBayes37_transform_preflight_v3'")
        if stem.startswith('verify_'):
            needle='    for p in sources:';assert text.count(needle)==1
            text=text.replace(needle,"    sources += [A/'nonflag_EmpiricalBayes40_full_control_recovery_v3_20261007.json',A/'run_nonflag_EmpiricalBayes40_official_comparison_v3_20261007.py',A/'prepare_nonflag_EmpiricalBayes40_selected_candidate_v3_20261007.py',A/'publish_nonflag_EmpiricalBayes40_evidence_v3_20261007.py']\n"+needle)
        if stem.startswith('publish_'):
            needle="    if phase=='scores':\n        for row in proof['records']:";assert text.count(needle)==1
            text=text.replace(needle,"    sources += [A/'nonflag_EmpiricalBayes40_full_control_recovery_v3_20261007.json',A/'verify_nonflag_residual_EmpiricalBayes37_transform_v3_20261007.py',A/'nonflag_EmpiricalBayes40_partial_preparation_failure_20261007.json',A/'prepare_nonflag_EmpiricalBayes40_complete_routes_v2_20261007.py',A/'nonflag_residual_EmpiricalBayes6410_plan_20261007.json',A/'nonflag_residual_EmpiricalBayes6410_source_admission_v1_20261007.json',A/'train_nonflag_residual_EmpiricalBayes64_bank10_v1_20261007.py']\n"+needle)
        compile(text,str(new_receiver),'exec');new_receiver.write_text(text,encoding='utf8',newline='\n');paths.extend((old,new_receiver))
    old=A/'run_nonflag_EmpiricalBayes40_admitted_comparison_v2_20261007.py';new_admitted=A/'run_nonflag_EmpiricalBayes40_admitted_comparison_v3_20261007.py';assert not new_admitted.exists()
    text=old.read_text(encoding='utf8').replace('run_nonflag_EmpiricalBayes40_official_comparison_v2_20261007','run_nonflag_EmpiricalBayes40_official_comparison_v3_20261007')
    compile(text,str(new_admitted),'exec');new_admitted.write_text(text,encoding='utf8',newline='\n');paths.extend((old,new_admitted))
    previous=A/'nonflag_EmpiricalBayes40_control_gate_recovery_v2_20261007.json'
    pins={**read(previous)['input_sha256'],**{str(p):sha(p) for p in [*paths,previous]}}
    gate=A/'nonflag_EmpiricalBayes40_full_control_recovery_v3_20261007.json'
    create(gate,{'status':'prepared_real_full37_retry_after_actual_native3_pass_and_preserved_status_guard_failure',
      'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'input_sha256':pins,'original_native10_fits_unchanged':True,
      'actual_native3_not_rerun_or_recounted':True,'CDF_math_and_prior_recipe_unchanged':True,
      'new_quality_scores':0,'test_labels_read':False})
    row=start('nonflag_residual_EmpiricalBayes37_transform_preflight_v3',
      'verify_nonflag_residual_EmpiricalBayes37_transform_v3_20261007.py',[],{**pins,str(gate):sha(gate)})
    create(A/'nonflag_EmpiricalBayes40_full_control_retry_v3_hidden_launch_20261007.json',{
      'status':'started_actual37_full_and111_cold_transform_checks_after_real3_hooks','identity':row,
      'input_sha256':pins,'new_quality_scores':0,'test_labels_read':False})
    print({'status':'started_full37_cold111_retry','worker':row['owned_worker_pid']},flush=True)

if __name__=='__main__':main()
