"""Freeze two untested mid-gamma streaming Fourier residual models and actual native controls."""
from pathlib import Path
import sys,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_upper_pool_HGB66_round115_sources_20261007 import substitute

def convert(text):
    return substitute(text,{'nonflag_residual_RFF128Hi':'nonflag_residual_RFF128StreamMid',
      'passed_actual2_RFF128Hi':'passed_actual2_RFF128StreamMid',
      'nonflag_residual_rff128hi':'nonflag_residual_rff128streammid'})

def main():
    plan=read(A/'nonflag_residual_RFF128Hi10_plan_20261007.json')
    plan.update(status='frozen_new_streamed_Gram128_mid_gamma_before_actual_controls_and_fits',
      at_local=time.strftime('%Y-%m-%dT%H:%M:%S'),configurations={
        'nonflag_residual_rff128streammid_g00625':{'gamma':.0625,'n_components':128,'random_state':20261007,'alpha_per_training_row':.01},
        'nonflag_residual_rff128streammid_g0125':{'gamma':.125,'n_components':128,'random_state':20261007,'alpha_per_training_row':.01}},
      resource_gate_available_RAM_GiB=8.5,
      training_solver_recipe='fixed8192_padded_RBF128_centered_float64_Gram_cholesky_v1',
      comparison_hypothesis='uncovered_mid_gamma0625_and125_with_explicit_memory_bounded_Gram_training',
      no_full_training_random_feature_matrix_allocated=True,
      new_floating_point_accumulation_recipe_not_claimed_identical_to_dense_fit=True)
    plan_path=A/'nonflag_residual_RFF128StreamMid10_plan_20261007.json';create(plan_path,plan)
    old=A/'train_nonflag_residual_RFF128Hi_bank10_v1_20261007.py';new=A/'train_nonflag_residual_RFF128StreamMid_bank10_v1_20261007.py'
    text=convert(old.read_text(encoding='utf8'))
    text=text.replace('    from nonflag_residual_RFF128_codec_20261007 import make_model',
      '    from nonflag_RFF128_streamed_gram_fitter_20261007 import fit_streamed,prepared_sha')
    text=text.replace('available<14*2**30','available<8.5*2**30').replace('at_least14GiB','at_least8_5GiB')
    text=text.replace('            bx=prepare(window,prep); train_y=y[train]',
      '            train_y=y[train]')
    text=text.replace("assert numeric_sha(bx)==old_info['training_matrix_numeric_sha256']",
      "assert prepared_sha(window,prep)==old_info['training_matrix_numeric_sha256']")
    text=text.replace('assert not np.shares_memory(bx,window) and not np.shares_memory(test,raw) and not np.shares_memory(test,window)',
      'assert not np.shares_memory(test,raw) and not np.shares_memory(test,window)')
    text=text.replace('            window._mmap.close();window=None;gc.collect()','            gc.collect()')
    text=text.replace("t=time.perf_counter(); model=make_model(cfg,len(indices)).fit(bx,train_y); fit_seconds=time.perf_counter()-t",
      "t=time.perf_counter(); model,fit_metadata=fit_streamed(window,prep,train_y,cfg); fit_seconds=time.perf_counter()-t")
    text=text.replace("'fit_seconds':fit_seconds,'prediction_control_rows':len(test)",
      "'fit_seconds':fit_seconds,'fit_metadata':fit_metadata,'prediction_control_rows':len(test)")
    text=text.replace('            del bx,window,train_y,test,indices; gc.collect()',
      '            window._mmap.close();window=None\n            del train_y,test,indices; gc.collect()')
    assert 'bx' not in text
    compile(text,str(new),'exec');assert not new.exists();new.write_text(text,encoding='utf8',newline='\n')
    olddiag=A/'verify_nonflag_residual_RFF128Hi_codec2_20261007.py';diag=A/'verify_nonflag_residual_RFF128StreamMid_codec2_20261007.py'
    text=convert(olddiag.read_text(encoding='utf8'))
    text=text.replace('    from nonflag_residual_RFF128_codec_20261007 import make_model',
      '    from nonflag_RFF128_streamed_gram_fitter_20261007 import fit_streamed')
    text=text.replace('model=make_model(cfg,512).fit(prepare(x[:512],prep),y[:512])',
      'model,fit_metadata=fit_streamed(x[:512],prep,y[:512],cfg)')
    text=text.replace("'native_reload_independent_and_all_prefix_bits_exact':True",
      "'native_reload_independent_and_all_prefix_bits_exact':True,'actual_streamed_fit_metadata':fit_metadata")
    compile(text,str(diag),'exec');assert not diag.exists();diag.write_text(text,encoding='utf8',newline='\n')
    sources=[Path(__file__),plan_path,old,new,olddiag,diag,A/'nonflag_RFF128_streamed_gram_fitter_20261007.py',
      A/'nonflag_residual_RFF128_codec_20261007.py',A/'nonflag_residual_HGB_preprocessing_20261007.py']
    create(A/'nonflag_residual_RFF128StreamMid_source_preparation_20261007.json',{
      'status':'compiled_explicit_new_streamed_Gram128_mid_gamma_routes',
      'input_sha256':{str(p):sha(p) for p in sources},'new_quality_scores':0,'test_labels_read':False})
    from verify_nonflag_residual_RFF128StreamMid_codec2_20261007 import main as controls
    controls()
    proof_path=A/'nonflag_residual_RFF128StreamMid_codec2_preflight_20261007/verification.json';proof=read(proof_path)
    assert proof['actual_diagnostic_fits']==2
    pins={**proof['input_sha256'],**{str(p):sha(p) for p in [*sources,proof_path]}}
    admission=A/'nonflag_residual_RFF128StreamMid10_source_admission_v1_20261007.json'
    create(admission,{'status':'passed_actual2_RFF128StreamMid_codec_controls_and10_past_only_fit_admission',
      'input_sha256':pins,'actual_diagnostic_fits':2,'new_quality_scores':0,'test_labels_read':False})
    from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start
    row=start('nonflag_residual_RFF128StreamMid_native_bank10',new.name,[],{**pins,str(admission):sha(admission)})
    create(A/'nonflag_residual_RFF128StreamMid10_actual_hidden_launch_20261007.json',{
      'status':'started_actual10_streamed128_mid_gamma_mature_native_fits_after_real_codec_controls',
      'identity':row,'input_sha256':pins,'new_quality_scores':0,'test_labels_read':False})
    print({'status':'started_new_streamed_native_bank','worker':row['owned_worker_pid']},flush=True)

if __name__=='__main__':main()
