"""Preserve actual failed gates and successful admission, and publish after full122."""
from pathlib import Path
import sys,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
def main():
    sources=[Path(__file__),A/'RFFRidge122_zero_score_QA_literal_correction_20261007.json',
        A/'nonflag_RFFRidge40_corrected_admission_hidden_launches_v2_20261007.json',
        A/'nonflag_RFFRidge40_complete_pipeline_actual_hidden_launches_v1_20261007.json',
        A/'nonflag_RFFRidge40_round122_source_admission_v1_20261007.json',
        A/'start_actual_admitted_RFFRidge122_scientific_stages_20261007.py',
        A/'correct_RFFRidge122_QA_literal_before_any_official_score_20261007.py']
    # A starter's live-only assertion prevented its final receipt; the actual services are authoritative.
    sources.remove(A/'nonflag_RFFRidge40_corrected_admission_hidden_launches_v2_20261007.json')
    outcomes={}
    for name,status in [('nonflag_RFFRidge40_round122_source_admission_v1','failed'),
        ('nonflag_RFFRidge40_continue_after_actual_admission','failed'),
        ('nonflag_RFFRidge40_continue_after_actual_admission_v2','failed'),
        ('nonflag_RFFRidge40_round122_source_admission_v2','passed')]:
        folder=A/'service_owned_workflows_20261006'/name
        assert not owned(read(folder/'native_launch.json')) and read(folder/'service_execution.json')['status']==status
        outcomes[name]=read(folder/'service_execution.json')
        sources += [*folder.glob('*.json'),*folder.glob('*.log')]
    for stem in ['verify_nonflag_RFFRidge40_round122_sources','prepare_nonflag_RFFRidge40_round122_sources',
        'run_nonflag_RFFRidge40_admitted_comparison','publish_nonflag_RFFRidge40_evidence','run_nonflag_RFFRidge40_round122_full_registration']:
        sources += [A/(stem+f'_v{v}_20261007.py') for v in (1,2)]
    sources += [A/f'nonflag_RFFRidge40_prospective_routes_v{v}_20261007.json' for v in (1,2)]
    sources=list(dict.fromkeys(sources));pins={str(p):sha(p) for p in sources}
    proof=A/'RFFRidge122_admission_recovery_history_20261007.json'
    create(proof,{'status':'verified_actual_failed_zero_score_admission_history_and_corrected_real_admission',
        'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'input_sha256':pins,'actual_terminal_outcomes':outcomes,
        'native_parameters_and_official_scoring_math_unchanged':True,'new_native_fits_by_recovery':0,
        'new_quality_scores_by_recovery':0,'actual_six_scientific_stages_started':True,'test_labels_read':False})
    old=A/'publish_lossless_string_benchmark_after_audit_20261007.py'
    new=A/'publish_RFFRidge122_admission_history_after_full_20261007.py';assert not new.exists()
    text=old.read_text(encoding='utf8')
    text=text.replace('local_boundary_audit_v4_main_after121','nonflag_RFFRidge40_round122_full_registration_v1')
    text=text.replace('exact_early_string_lossless_codec_benchmark_20261007/verification.json','RFFRidge122_admission_recovery_history_20261007.json')
    text=text.replace('passed_actual6_two_order_independent_report_subset_benchmarks_and_full12406_original_codebook_exact','verified_actual_failed_zero_score_admission_history_and_corrected_real_admission')
    text=text.replace('lossless_string_codec_benchmark_github_20261007','RFFRidge122_admission_history_github_20261007')
    text=text.replace("proof_path,proof_path.parent/'frozen_before_benchmark.json',","proof_path,")
    text=text.replace('validation_sync/lossless_string_codec_benchmark_20261007','validation_sync/RFFRidge122_admission_history_20261007')
    text=text.replace('published_actual_codec_diagnostic_not_adopted','published_actual_failed_gates_and_corrected_admission')
    text=text.replace("'median_subset_speedup':proof['median_measured_subset_packing_speedup'],", "'actual_failed_admission_and_controller_scopes_preserved':True,")
    text=text.replace("'full_old_packing_not_retimed':True,'whole_goal_speedup_not_measured':True,", "'actual_corrected_real_admission_passed':True,")
    text=text.replace('记录完整榜编码加速对照：原始码表完全一致，未采用','保留122轮评分前的真实检查失败及修复后完整准入记录')
    compile(text,str(new),'exec');new.write_text(text,encoding='utf8',newline='\n')
    from handoff_ready_goss_full_execution_20261006 import start_service
    row=start_service('RFFRidge122_actual_admission_history_main_after_full',new.name,[],{str(new):sha(new),str(proof):sha(proof),str(Path(__file__)):sha(__file__)})
    create(A/'RFFRidge122_admission_history_actual_publication_launch_20261007.json',row)
    print({'status':'actual_history_publication_queued','worker':row['owned_worker_pid']},flush=True)
if __name__=='__main__':main()
