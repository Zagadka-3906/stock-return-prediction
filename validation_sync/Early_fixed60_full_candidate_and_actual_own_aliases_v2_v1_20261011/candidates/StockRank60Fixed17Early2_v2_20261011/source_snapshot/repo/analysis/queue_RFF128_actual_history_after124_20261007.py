"""Record the real completed or failed native bank and publish its records after full124."""
from pathlib import Path
import sys,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
def main():
    service=A/'service_owned_workflows_20261006/nonflag_residual_RFF128_native_bank10'
    while owned(read(service/'native_launch.json')):time.sleep(10)
    execution=read(service/'service_execution.json')
    bank=A/'nonflag_residual_RFF128_bank10_20261007'
    sources=[Path(__file__),*A.glob('*nonflag_residual_RFF128*20261007.py'),*A.glob('*nonflag_residual_RFF128*20261007.json'),
      *bank.glob('*.json'),*bank.glob('*/info_*.json'),*bank.glob('*/oof_verification.json'),
      *bank.glob('*/independent_random_fourier_linear_state_*.json'),
      *(A/'nonflag_residual_RFF128_codec2_preflight_20261007').glob('*.json'),
      *service.glob('*.json'),*service.glob('*.log'),
      *(A/'nonflag_reverse_Ridge40_unadmitted_preparation_first_attempt_20261007').glob('*'),
      *A.glob('*nonflag_reverse_Ridge*20261007.py'),*A.glob('*nonflag_reverse_Ridge*20261007.json')]
    sources=list(dict.fromkeys(sources));pins={str(p):sha(p) for p in sources}
    native_fits=len(list(bank.glob('*/info_*.json')))
    if execution['status']=='passed':
        proof=read(bank/'verification.json')
        assert proof['actual_native_fits']==native_fits==10
        assert proof['status']=='passed_actual10_nonflag_residual_RFF128_mature_native_reload_independent_and_prefix_controls'
    proof_path=A/'RFF128_actual_native_bank_and124_source_history_20261007.json'
    create(proof_path,{'status':'verified_actual_RFF128_native_terminal_and_preserved_unadmitted124_preparation_history',
      'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'input_sha256':pins,'actual_native_fits':native_fits,
      'native_bank_terminal':execution,'actual_diagnostic_fits':2,
      'new_quality_scores_by_this_record':0,'complete_future_RFF128_candidate_not_claimed':True,'test_labels_read':False})
    old=A/'publish_RFFRidge122_admission_history_after_full_20261007.py'
    new=A/'publish_RFF128_actual_history_after124_20261007.py';assert not new.exists()
    text=old.read_text(encoding='utf8')
    replacements={
      'nonflag_RFFRidge40_round122_full_registration_v1':'nonflag_reverse_Ridge40_round124_full_registration_v1',
      'RFFRidge122_admission_recovery_history_20261007':'RFF128_actual_native_bank_and124_source_history_20261007',
      'verified_actual_failed_zero_score_admission_history_and_corrected_real_admission':'verified_actual_RFF128_native_terminal_and_preserved_unadmitted124_preparation_history',
      'RFFRidge122_admission_history_github_20261007':'RFF128_actual_history_github_20261007',
      'validation_sync/RFFRidge122_admission_history_20261007':'validation_sync/RFF128_actual_history_20261007',
      'published_actual_failed_gates_and_corrected_admission':'published_actual_RFF128_native_history_and_unadmitted124_source_preparation',
      "'actual_failed_admission_and_controller_scopes_preserved':True":"'actual_native_fits':proof['actual_native_fits']",
      "'actual_corrected_real_admission_passed':True":"'native_bank_terminal':proof['native_bank_terminal']",
      '保留122轮评分前的真实检查失败及修复后完整准入记录':'保存128维随机傅里叶实际训练与解码记录及124轮准备检查历史'}
    for before,after in replacements.items():text=text.replace(before,after)
    compile(text,str(new),'exec');new.write_text(text,encoding='utf8',newline='\n')
    from handoff_ready_goss_full_execution_20261006 import start_service
    row=start_service('RFF128_actual_history_main_after124',new.name,[],
      {str(new):sha(new),str(proof_path):sha(proof_path),str(Path(__file__)):sha(__file__)})
    create(A/'RFF128_actual_history_publication_launch_20261007.json',row)
if __name__=='__main__':main()
