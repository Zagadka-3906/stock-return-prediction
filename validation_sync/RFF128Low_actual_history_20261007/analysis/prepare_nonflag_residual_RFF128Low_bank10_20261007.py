"""Test weaker L2 with the same 128-feature kernel, own mature windows, and exact decoder."""
from pathlib import Path
import sys,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_upper_pool_HGB66_round115_sources_20261007 import substitute
def main():
    mapping={
      'nonflag_residual_RFF128_codec_20261007':'nonflag_residual_RFF128_codec_20261007',
      'nonflag_residual_RFF128':'nonflag_residual_RFF128Low',
      'passed_actual2_RFF128_codec':'passed_actual2_RFF128Low_codec'}
    pairs=[('verify_nonflag_residual_RFF128_codec2_20261007.py','verify_nonflag_residual_RFF128Low_codec2_20261007.py'),
      ('train_nonflag_residual_RFF128_bank10_v1_20261007.py','train_nonflag_residual_RFF128Low_bank10_v1_20261007.py')]
    generated=[];originals=[]
    for before,after in pairs:
        old=A/before;originals.append(old);new=A/after;assert not new.exists()
        text=substitute(old.read_text(encoding='utf8'),mapping)
        compile(text,str(new),'exec');new.write_text(text,encoding='utf8',newline='\n');generated.append(new)
    original_plan=A/'nonflag_residual_RFF12810_plan_20261007.json';plan=read(original_plan)
    old_cfg=plan['configurations']
    plan.update(status='frozen_RFF128_weaker_L2_before_actual_diagnostics_and10_mature_fits',at_local=time.strftime('%Y-%m-%dT%H:%M:%S'),
      configurations={
        'nonflag_residual_rff128low_g003125':{**old_cfg['nonflag_residual_rff128_g003125'],'alpha_per_training_row':.0025},
        'nonflag_residual_rff128low_g025':{**old_cfg['nonflag_residual_rff128_g025'],'alpha_per_training_row':.0025}},
      comparison_hypothesis='fourfold_weaker_L2_than_existing128_basis; same_gamma_seed_dimensions_and_own_training_windows',
      existing128_validation_not_used_as_test_period_answers=True)
    plan_path=A/'nonflag_residual_RFF128Low10_plan_20261007.json';create(plan_path,plan)
    paths=[Path(__file__),*originals,*generated,original_plan,plan_path,A/'nonflag_residual_RFF128_codec_20261007.py']
    create(A/'nonflag_residual_RFF128Low_source_preparation_20261007.json',
      {'status':'compiled_weaker_L2_mature_fit_sources_before_any_actual_fit','input_sha256':{str(p):sha(p) for p in paths}})
    from verify_nonflag_residual_RFF128Low_codec2_20261007 import main as diagnostic
    diagnostic()
    proof_path=A/'nonflag_residual_RFF128Low_codec2_preflight_20261007/verification.json';proof=read(proof_path)
    assert proof['status']=='passed_actual2_nonflag_residual_RFF128Low_historical_codec_controls' and proof['actual_diagnostic_fits']==2
    pins={**proof['input_sha256'],**{str(p):sha(p) for p in [*paths,proof_path]}}
    admission=A/'nonflag_residual_RFF128Low10_source_admission_v1_20261007.json'
    create(admission,{'status':'passed_actual2_RFF128Low_codec_controls_and10_past_only_fit_admission',
      'input_sha256':pins,'actual_diagnostic_fits':2,'new_quality_scores':0,'test_labels_read':False})
    from handoff_ready_goss_full_execution_20261006 import start_service
    row=start_service('nonflag_residual_RFF128Low_native_bank10','train_nonflag_residual_RFF128Low_bank10_v1_20261007.py',[],{**pins,str(admission):sha(admission)})
    create(A/'nonflag_residual_RFF128Low10_actual_hidden_launch_20261007.json',
      {'status':'started_actual_single_host_RFF128Low_bank_after_real2_codec_controls','identity':row,'input_sha256':pins,
       'actual_official_scores':0,'test_labels_read':False})
    print({'status':'started_actual_lower_L2_RFF128_bank','worker':row['owned_worker_pid']},flush=True)
if __name__=='__main__':main()
