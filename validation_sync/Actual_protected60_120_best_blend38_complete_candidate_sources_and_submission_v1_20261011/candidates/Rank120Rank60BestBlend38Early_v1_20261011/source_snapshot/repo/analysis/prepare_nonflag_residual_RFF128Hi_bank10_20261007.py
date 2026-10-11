"""Fourfold stronger L2; close unused read-only feature mappings without changing training bits."""
from pathlib import Path
import sys,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_upper_pool_HGB66_round115_sources_20261007 import substitute

def replace_once(text,before,after):
    assert text.count(before)==1,(before,text.count(before))
    return text.replace(before,after)

def main():
    mapping={'nonflag_residual_RFF128_codec_20261007':'nonflag_residual_RFF128_codec_20261007',
        'nonflag_residual_RFF128':'nonflag_residual_RFF128Hi','passed_actual2_RFF128_codec':'passed_actual2_RFF128Hi_codec'}
    olddiag=A/'verify_nonflag_residual_RFF128_codec2_20261007.py'
    diag=A/'verify_nonflag_residual_RFF128Hi_codec2_20261007.py';assert not diag.exists()
    text=substitute(olddiag.read_text(encoding='utf8'),mapping)
    compile(text,str(diag),'exec');diag.write_text(text,encoding='utf8',newline='\n')
    oldtrainer=A/'train_nonflag_residual_RFF128_bank10_v1_20261007.py'
    trainer=A/'train_nonflag_residual_RFF128Hi_bank10_v1_20261007.py';assert not trainer.exists()
    text=substitute(oldtrainer.read_text(encoding='utf8'),mapping)
    text=replace_once(text,'        eligible=np.isfinite(y)&valid; del labels; gc.collect()',
        '        eligible=np.isfinite(y)&valid; del labels; gc.collect()\n        raw._mmap.close();raw=None;gc.collect()')
    text=replace_once(text,"            window=np.load(cache/f'mature_training_features64_{year}.npy',mmap_mode='r')",
        "            assert raw is None\n            raw=np.load(raw_path,mmap_mode='r')\n            window=np.load(cache/f'mature_training_features64_{year}.npy',mmap_mode='r')")
    text=replace_once(text,'            else: test=np.asarray(window[:1000]).copy()',
        '            else: test=np.asarray(window[:1000]).copy()\n            assert not np.shares_memory(bx,window) and not np.shares_memory(test,raw) and not np.shares_memory(test,window)\n            raw._mmap.close();raw=None\n            window._mmap.close();window=None;gc.collect()')
    text=text.replace("'actual_nonflag_Ridge_training'","'actual_nonflag_RFF128Hi_training'")
    compile(text,str(trainer),'exec');trainer.write_text(text,encoding='utf8',newline='\n')
    original_plan=A/'nonflag_residual_RFF12810_plan_20261007.json';plan=read(original_plan)
    cfg=plan['configurations'];plan.update(status='frozen_RFF128_stronger_L2_before_actual_diagnostics_and10_mature_fits',
        at_local=time.strftime('%Y-%m-%dT%H:%M:%S'),configurations={
            'nonflag_residual_rff128hi_g003125':{**cfg['nonflag_residual_rff128_g003125'],'alpha_per_training_row':.04},
            'nonflag_residual_rff128hi_g025':{**cfg['nonflag_residual_rff128_g025'],'alpha_per_training_row':.04}},
        comparison_hypothesis='fourfold_stronger_L2_than_original128_basis; same_gamma_seed_dimensions_and_past_only_windows',
        unused_raw_and_training_window_mappings_closed_only_after_own_preprocessing_and_numeric_hash_verification=True)
    planpath=A/'nonflag_residual_RFF128Hi10_plan_20261007.json';create(planpath,plan)
    paths=[Path(__file__),olddiag,diag,oldtrainer,trainer,original_plan,planpath,A/'nonflag_residual_RFF128_codec_20261007.py',
        A/'RFF128Low_checkpoint_memory_release_actual_handoff_20261007/verification.json']
    create(A/'nonflag_residual_RFF128Hi_source_preparation_20261007.json',
        {'status':'compiled_stronger_L2_memory_release_before_actual_fit','input_sha256':{str(p):sha(p) for p in paths}})
    from verify_nonflag_residual_RFF128Hi_codec2_20261007 import main as diagnostic
    diagnostic()
    proofpath=A/'nonflag_residual_RFF128Hi_codec2_preflight_20261007/verification.json';proof=read(proofpath)
    assert proof['status']=='passed_actual2_nonflag_residual_RFF128Hi_historical_codec_controls' and proof['actual_diagnostic_fits']==2
    pins={**proof['input_sha256'],**{str(p):sha(p) for p in [*paths,proofpath]}}
    admission=A/'nonflag_residual_RFF128Hi10_source_admission_v1_20261007.json'
    create(admission,{'status':'passed_actual2_RFF128Hi_codec_controls_and10_past_only_fit_admission',
        'input_sha256':pins,'actual_diagnostic_fits':2,'new_quality_scores':0,'test_labels_read':False})
    from handoff_ready_goss_full_execution_20261006 import start_service
    row=start_service('nonflag_residual_RFF128Hi_native_bank10',trainer.name,[],{**pins,str(admission):sha(admission)})
    create(A/'nonflag_residual_RFF128Hi10_actual_hidden_launch_20261007.json',
        {'status':'started_actual_single_host_stronger_L2_bank_after_real2_codec_controls',
         'identity':row,'input_sha256':pins,'new_quality_scores':0,'test_labels_read':False})
if __name__=='__main__':main()
