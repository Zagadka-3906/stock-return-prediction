"""Preserve both actual sign-control suites and the local observer, then publish after full123."""
from pathlib import Path
import sys,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
def main():
    services=['nonflag_reverse_RFF_actual_hook3_and_full37_controls','nonflag_reverse_Ridge_actual_hook3_and_full37_controls',
      'nonflag_reverse_RFF40_round123_source_admission_v1','nonflag_reverse_RFF40_continue_after_actual_admission',
      'local_only_monitor_v23_exact_idle_handoff']
    sources=[Path(__file__)]
    outcomes={}
    for name in services:
        folder=A/'service_owned_workflows_20261006'/name
        while owned(read(folder/'native_launch.json')):time.sleep(10)
        execution=read(folder/'service_execution.json');assert execution['status']=='passed',name
        outcomes[name]=execution;sources += [*folder.glob('*.json'),*folder.glob('*.log')]
    stems=['prepare_nonflag_reverse_RFF40_controls','prepare_nonflag_reverse_RFF40_complete_routes',
      'nonflag_reverse_RFF123_route_mapping','nonflag_reverse_RFF_CDF_transform','nonflag_reverse_RFF_native_stage',
      'run_nonflag_reverse_RFF_hook3_after_bank','verify_nonflag_reverse_RFF37_transform','run_nonflag_reverse_RFF_actual_controls',
      'start_nonflag_reverse_RFF40_actual_admission','continue_nonflag_reverse_RFF40_after_actual_admission',
      'prepare_nonflag_reverse_Ridge40_controls','nonflag_reverse_Ridge_native_stage',
      'run_nonflag_reverse_Ridge_hook3_after_bank','verify_nonflag_reverse_Ridge37_transform','run_nonflag_reverse_Ridge_actual_controls',
      'prepare_local_only_monitor_v23','monitor_local_only_runtime_v23','handoff_local_only_monitor_v23']
    sources += [A/(stem+'_20261007.py') for stem in stems]
    sources += list(A.glob('*nonflag_reverse*20261007.json'))
    sources += [A/'local_only_monitor_v23_source_preparation_20261007.json',A/'local_only_monitor_v23_hidden_launch_20261007.json',
      A/'nonflag_residual_HGB_CDF_transform_20261007.py']
    for folder in ['nonflag_reverse_RFF_native_hook3_preflight_20261007','nonflag_reverse_RFF37_transform_preflight_20261007',
      'nonflag_reverse_Ridge_native_hook3_preflight_20261007','nonflag_reverse_Ridge37_transform_preflight_20261007',
      'local_only_monitor_v23_actual_handoff_20261007']:
        sources += list((A/folder).glob('*.json'))
    sources=list(dict.fromkeys(sources));pins={str(p):sha(p) for p in sources}
    proof_path=A/'reverse_residual_actual_controls_and_local_observer_history_20261007.json'
    create(proof_path,{'status':'verified_actual_two_signed_native3_full37_cold111_controls_and_real123_admission',
      'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'input_sha256':pins,'actual_terminal_outcomes':outcomes,
      'new_native_fits':0,'new_quality_scores_by_this_record':0,
      'round124_official_scores_or_complete_source_admission_not_claimed':True,'test_labels_read':False})
    old=A/'publish_RFFRidge122_admission_history_after_full_20261007.py'
    new=A/'publish_reverse_residual_controls_history_after123_20261007.py';assert not new.exists()
    text=old.read_text(encoding='utf8')
    replacements={
      'nonflag_RFFRidge40_round122_full_registration_v1':'nonflag_reverse_RFF40_round123_full_registration_v1',
      'RFFRidge122_admission_recovery_history_20261007':'reverse_residual_actual_controls_and_local_observer_history_20261007',
      'verified_actual_failed_zero_score_admission_history_and_corrected_real_admission':'verified_actual_two_signed_native3_full37_cold111_controls_and_real123_admission',
      'RFFRidge122_admission_history_github_20261007':'reverse_residual_controls_history_github_20261007',
      'validation_sync/RFFRidge122_admission_history_20261007':'validation_sync/reverse_residual_controls_history_20261007',
      'published_actual_failed_gates_and_corrected_admission':'published_actual_two_signed_controls_and_local_observer',
      "'actual_failed_admission_and_controller_scopes_preserved':True":"'actual_two_signed_native3_full37_cold111_scopes_preserved':True",
      '保留122轮评分前的真实检查失败及修复后完整准入记录':'保存两组反向残差的全量与冷启动检查及本机监控记录'}
    for before,after in replacements.items():text=text.replace(before,after)
    compile(text,str(new),'exec');new.write_text(text,encoding='utf8',newline='\n')
    from handoff_ready_goss_full_execution_20261006 import start_service
    row=start_service('reverse_residual_controls_history_main_after123',new.name,[],
      {str(new):sha(new),str(proof_path):sha(proof_path),str(Path(__file__)):sha(__file__)})
    create(A/'reverse_residual_controls_history_actual_publication_launch_20261007.json',row)
    print({'status':'queued_actual_controls_history_after_full123','worker':row['owned_worker_pid']},flush=True)
if __name__=='__main__':main()
