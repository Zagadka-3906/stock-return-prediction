"""Observe real RFF122 controls and qualification; change only the idle monitor."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import sha,create
from prepare_protected_upper_pool_HGB66_round115_sources_20261007 import substitute
def main():
    old=A/'monitor_local_only_runtime_v21_20261007.py';new=A/'monitor_local_only_runtime_v22_20261007.py'
    text=substitute(old.read_text(encoding='utf8'),{'local_only_v21':'local_only_v22','single_host_optimization_live_status_v21_20261007':'single_host_optimization_live_status_v22_20261007'})
    needle="'nonflag_Ridge40_round121_full_registration_v1')";assert text.count(needle)==1
    text=text.replace(needle,"""'nonflag_Ridge40_round121_full_registration_v1',
        'nonflag_residual_RFFRidge_native_bank10','nonflag_residual_RFFRidge_native_bank10_v2',
        'nonflag_RFFRidge_actual_hook3_and_full37_controls','nonflag_RFFRidge_actual_controls_main_after121',
        'nonflag_RFFRidge40_round122_source_admission_v1','nonflag_RFFRidge40_continue_after_actual_admission',
        'nonflag_RFFRidge40_full37_controls_main_publication_v1','nonflag_RFFRidge40_official_comparison_v1',
        'nonflag_RFFRidge40_scores_main_publication_v1','nonflag_RFFRidge40_selected_candidate_preparation_v1',
        'nonflag_RFFRidge40_selected_candidate_sealing_v1','nonflag_RFFRidge40_round122_full_registration_v1',
        'local_boundary_audit_v4_main_after121','lossless_string_codec_benchmark_main_after_audit')""")
    text=text.replace('(120, 31), (121, 32))','(120, 31), (121, 32), (122, 33))')
    text=text.replace("121:'nonflag_Ridge40_round121_full_registration_v1'}[n]","121:'nonflag_Ridge40_round121_full_registration_v1',122:'nonflag_RFFRidge40_round122_full_registration_v1'}[n]")
    needle="    value['no_full_qualification_claim_from_partial_case_counts']=True";assert text.count(needle)==1
    extra="""    rff_bank=A/'nonflag_residual_RFFRidge_bank10_20261007/verification.json'
    rff_controls=A/'nonflag_residual_RFFRidge37_transform_preflight_20261007/verification.json'
    rff_hooks=A/'nonflag_residual_RFFRidge_native_hook3_preflight_20261007/verification.json'
    value['RFFRidge_actual_native_fit_count']=read(rff_bank)['actual_native_fits'] if rff_bank.exists() else 0
    value['RFFRidge_training_and_native_controls_seconds']=read(rff_bank)['elapsed_seconds'] if rff_bank.exists() else None
    value['RFFRidge_actual_full_transform_controls']=read(rff_controls)['actual_full_cases'] if rff_controls.exists() else 0
    value['RFFRidge_actual_cold_prefix_controls']=read(rff_controls)['actual_cold_cases'] if rff_controls.exists() else 0
    value['RFFRidge_actual_historical_native_hook_controls']=len(read(rff_hooks)['records']) if rff_hooks.exists() else 0
    rff_score=A/'nonflag_RFFRidge40_official_comparison_v1_20261007'
    value['RFFRidge40_actual_official_cases_completed']=len(list(rff_score.glob('case*_official.json')))
    value['RFFRidge40_expected_official_cases']=40
    if (rff_score/'actual_stage.json').exists():value['RFFRidge40_actual_official_stage']=read(rff_score/'actual_stage.json')
    value['RFFRidge122_fully_qualified']=122 in qualified
    value['RFFRidge_native_controls_are_not_official_selection_or_full_candidate_qualification']=True
    refusal=A/'closed_local_score_scratch_cleanup_v3_20261007/deletion_not_executed_policy_rejection.json'
    if refusal.exists():value['historical_scratch_cleanup_actual_refusal']=read(refusal)
"""
    text=text.replace(needle,extra+needle);compile(text,str(new),'exec');assert not new.exists();new.write_text(text,encoding='utf8',newline='\n')
    old_h=A/'handoff_local_only_monitor_v21_20261007.py';new_h=A/'handoff_local_only_monitor_v22_20261007.py'
    h=substitute(old_h.read_text(encoding='utf8'),{
        'local_only_monitor_v21_actual_handoff_20261007':'local_only_monitor_v22_actual_handoff_20261007',
        'local_only_progress_monitor_v20':'local_only_progress_monitor_v21','local_only_progress_monitor_v21':'local_only_progress_monitor_v22',
        'monitor_local_only_runtime_v20_20261007.py':'monitor_local_only_runtime_v21_20261007.py','monitor_local_only_runtime_v21_20261007.py':'monitor_local_only_runtime_v22_20261007.py',
        'local_only_v21':'local_only_v22','administrative_supersession_local_v21_20261007':'administrative_supersession_local_v22_20261007',
        'passed_actual_idle_observer20_Ridge121_real_native_controls_and_qualified_only_routes':'passed_actual_idle_observer21_RFF122_real_native_controls_and_qualified_only_routes'})
    needle="        assert all(owned(r) for r in preserved.values())";assert h.count(needle)==1
    h=h.replace(needle,"        assert live['RFFRidge_actual_native_fit_count']==10 and live['RFFRidge_actual_full_transform_controls']==37 and live['RFFRidge_actual_cold_prefix_controls']==111\n"+needle)
    compile(h,str(new_h),'exec');assert not new_h.exists();new_h.write_text(h,encoding='utf8',newline='\n')
    create(A/'local_only_monitor_v22_source_preparation_20261007.json',{'status':'compiled_RFF122_real_stage_and_qualified_only_monitor','input_sha256':{str(p):sha(p) for p in [Path(__file__),old,new,old_h,new_h]},'scientific_workers_stopped':0})
if __name__=='__main__':main()
