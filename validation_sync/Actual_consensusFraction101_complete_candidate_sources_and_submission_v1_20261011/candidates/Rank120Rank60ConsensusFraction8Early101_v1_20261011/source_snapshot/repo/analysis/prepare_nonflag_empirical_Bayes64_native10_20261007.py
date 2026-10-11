"""Prepare two additional past-only adaptive-shrinkage linear model families."""
from pathlib import Path
import sys,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_upper_pool_HGB66_round115_sources_20261007 import substitute

def convert(text):
    return substitute(text,{'nonflag_residual_RFF128StreamMid':'nonflag_residual_EmpiricalBayes64',
      'passed_actual2_RFF128StreamMid':'passed_actual2_EmpiricalBayes64',
      'nonflag_RFF128_streamed_gram_fitter_20261007':'nonflag_empirical_Bayes64_codec_20261007',
      'nonflag_residual_RFF128_codec_20261007':'nonflag_empirical_Bayes64_codec_20261007',
      'independent_random_fourier_linear_state':'independent_linear_state',
      'nonflag_residual_rff128streammid':'nonflag_residual_empirical_bayes64'})

def main():
    oldplan=A/'nonflag_residual_RFF128StreamMid10_plan_20261007.json';plan=read(oldplan)
    plan.update(status='frozen_new_empirical_Bayes64_scalar_and_diagonal_priors_before_actual_fits',
      at_local=time.strftime('%Y-%m-%dT%H:%M:%S'),configurations={
        'nonflag_residual_empirical_bayes64_scalar':{'mode':'scalar','max_iter':128,'tol':1e-8,'alpha_per_training_row':.01,'solver':'empirical_bayes_centered_Gram64'},
        'nonflag_residual_empirical_bayes64_diagonal':{'mode':'diagonal','max_iter':128,'tol':1e-8,'alpha_per_training_row':.01,'solver':'empirical_bayes_centered_Gram64'}},
      training_solver_recipe='fixed8192_centered_Gram64_empirical_Bayes_scalar_or_diagonal_v1',
      comparison_hypothesis='uncovered_scalar_and_feature_specific_empirical_Bayes_shrinkage_learned_only_on_past_rows',
      inference_recipe='fixed8192 padded rows; native saved custom linear model and independent64 coefficient JSON',
      no_full_training_random_feature_matrix_allocated=True)
    path=A/'nonflag_residual_EmpiricalBayes6410_plan_20261007.json';create(path,plan)
    old=A/'train_nonflag_residual_RFF128StreamMid_bank10_v1_20261007.py';trainer=A/'train_nonflag_residual_EmpiricalBayes64_bank10_v1_20261007.py'
    text=convert(old.read_text(encoding='utf8')).replace('actual_nonflag_RFF128Hi_training','actual_nonflag_EmpiricalBayes64_training')
    compile(text,str(trainer),'exec');assert not trainer.exists();trainer.write_text(text,encoding='utf8',newline='\n')
    olddiag=A/'verify_nonflag_residual_RFF128StreamMid_codec2_20261007.py';diag=A/'verify_nonflag_residual_EmpiricalBayes64_codec2_20261007.py'
    text=convert(olddiag.read_text(encoding='utf8'))
    compile(text,str(diag),'exec');assert not diag.exists();diag.write_text(text,encoding='utf8',newline='\n')
    sources=[Path(__file__),oldplan,path,old,trainer,olddiag,diag,A/'nonflag_empirical_Bayes64_codec_20261007.py',
      A/'nonflag_residual_Ridge_codec_20261007.py',A/'nonflag_residual_HGB_preprocessing_20261007.py',
      A/'nonflag_RFF128_streamed_gram_fitter_20261007.py']
    create(A/'nonflag_residual_EmpiricalBayes64_source_preparation_20261007.json',{
      'status':'compiled_new_empirical_Bayes64_past_only_native_and_independent_decoder_routes',
      'input_sha256':{str(p):sha(p) for p in sources},'new_quality_scores':0,'test_labels_read':False})
    from verify_nonflag_residual_EmpiricalBayes64_codec2_20261007 import main as controls
    controls()
    proof_path=A/'nonflag_residual_EmpiricalBayes64_codec2_preflight_20261007/verification.json';proof=read(proof_path)
    assert proof['actual_diagnostic_fits']==2
    pins={**proof['input_sha256'],**{str(p):sha(p) for p in [*sources,proof_path]}}
    admission=A/'nonflag_residual_EmpiricalBayes6410_source_admission_v1_20261007.json'
    create(admission,{'status':'passed_actual2_EmpiricalBayes64_codec_controls_and10_past_only_fit_admission',
      'input_sha256':pins,'actual_diagnostic_fits':2,'new_quality_scores':0,'test_labels_read':False})
    from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start
    row=start('nonflag_residual_EmpiricalBayes64_native_bank10',trainer.name,[],{**pins,str(admission):sha(admission)})
    create(A/'nonflag_residual_EmpiricalBayes6410_actual_hidden_launch_20261007.json',{
      'status':'started_actual10_new_empirical_Bayes64_mature_fits_after_real2_codec_controls',
      'identity':row,'input_sha256':pins,'new_quality_scores':0,'test_labels_read':False})
    print({'status':'started_empirical_Bayes64_native_bank','worker':row['owned_worker_pid']},flush=True)

if __name__=='__main__':main()
