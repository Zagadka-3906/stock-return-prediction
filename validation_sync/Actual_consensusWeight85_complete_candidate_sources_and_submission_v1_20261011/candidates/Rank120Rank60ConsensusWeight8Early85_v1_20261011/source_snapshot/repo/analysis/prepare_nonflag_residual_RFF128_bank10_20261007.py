"""Admit 128-component random Fourier models using a memory-saving native Ridge recipe."""
from pathlib import Path
import sys,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_upper_pool_HGB66_round115_sources_20261007 import substitute
def main():
    old_codec=A/'nonflag_residual_RFFRidge_codec_20261007.py';codec=A/'nonflag_residual_RFF128_codec_20261007.py';assert not codec.exists()
    code=old_codec.read_text(encoding='utf8').replace('nonflag_residual_RFFRidge','nonflag_residual_RFF128')
    assert code.count('copy_X=True')==1;code=code.replace('copy_X=True','copy_X=False')
    compile(code,str(codec),'exec');codec.write_text(code,encoding='utf8',newline='\n')
    replacements={
      'nonflag_residual_RFFRidge10_source_admission_v2_20261007':'nonflag_residual_RFF12810_source_admission_v1_20261007',
      'nonflag_residual_RFFRidge':'nonflag_residual_RFF128',
      'passed_actual2_RFFRidge':'passed_actual2_RFF128',
      'available<12*2**30':'available<14*2**30',
      'at_least12GiB':'at_least14GiB'}
    originals=[A/'verify_nonflag_residual_RFFRidge_codec2_20261007.py',A/'train_nonflag_residual_RFFRidge_bank10_v2_20261007.py']
    generated=[A/'verify_nonflag_residual_RFF128_codec2_20261007.py',A/'train_nonflag_residual_RFF128_bank10_v1_20261007.py']
    for old,new in zip(originals,generated):
        assert not new.exists();text=substitute(old.read_text(encoding='utf8'),replacements)
        compile(text,str(new),'exec');new.write_text(text,encoding='utf8',newline='\n')
    plan=read(A/'nonflag_residual_RFFRidge10_plan_20261007.json')
    plan.update(status='frozen_RFF128_before_actual_diagnostics_and10_mature_fits',at_local=time.strftime('%Y-%m-%dT%H:%M:%S'),
      configurations={
        'nonflag_residual_rff128_g003125':{'gamma':.03125,'n_components':128,'random_state':20261007,'alpha_per_training_row':.01},
        'nonflag_residual_rff128_g025':{'gamma':.25,'n_components':128,'random_state':20261007,'alpha_per_training_row':.01}},
      fixed_parameters={'ridge_solver':'cholesky','fit_intercept':True,'copy_X':False},
      resource_gate_available_RAM_GiB=14,
      random_feature_array_owned_by_RBF_transform_no_training_feature_matrix_mutation=True,
      larger_basis_is_new_scientific_recipe_requires_actual_native_controls_and_official_comparison=True)
    plan_path=A/'nonflag_residual_RFF12810_plan_20261007.json';create(plan_path,plan)
    paths=[Path(__file__),old_codec,codec,*originals,*generated,plan_path]
    create(A/'nonflag_residual_RFF128_source_preparation_20261007.json',
      {'status':'compiled_new_RFF128_zero_copy_native_sources_before_any_fit','input_sha256':{str(p):sha(p) for p in paths}})
    from verify_nonflag_residual_RFF128_codec2_20261007 import main as diagnostic
    diagnostic()
    proof_path=A/'nonflag_residual_RFF128_codec2_preflight_20261007/verification.json';proof=read(proof_path)
    assert proof['status']=='passed_actual2_nonflag_residual_RFF128_historical_codec_controls' and proof['actual_diagnostic_fits']==2
    pins={**proof['input_sha256'],**{str(p):sha(p) for p in [*paths,proof_path]}}
    admission=A/'nonflag_residual_RFF12810_source_admission_v1_20261007.json'
    create(admission,{'status':'passed_actual2_RFF128_codec_controls_and10_past_only_fit_admission',
      'input_sha256':pins,'actual_diagnostic_fits':2,'new_quality_scores':0,'test_labels_read':False})
    from handoff_ready_goss_full_execution_20261006 import start_service
    row=start_service('nonflag_residual_RFF128_native_bank10','train_nonflag_residual_RFF128_bank10_v1_20261007.py',[],{**pins,str(admission):sha(admission)})
    create(A/'nonflag_residual_RFF12810_actual_hidden_launch_20261007.json',
      {'status':'started_actual_single_host_RFF128_native_bank_after_real2_codec_controls','identity':row,'input_sha256':pins,
       'actual_official_scores':0,'test_labels_read':False})
    print({'status':'started_actual_RFF128_bank','worker':row['owned_worker_pid']},flush=True)
if __name__=='__main__':main()
