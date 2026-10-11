"""Add real Ridge121 native/control/admission stages without restarting scientific workers."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]; A=ROOT/'analysis'
sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import sha,create
from prepare_protected_upper_pool_HGB66_round115_sources_20261007 import substitute

def main():
    old=A/'monitor_local_only_runtime_v20_20261007.py'; target=A/'monitor_local_only_runtime_v21_20261007.py'
    text=substitute(old.read_text(encoding='utf8'),{'local_only_v20':'local_only_v21','single_host_optimization_live_status_v20_20261007':'single_host_optimization_live_status_v21_20261007'})
    needle="'nonflag_HGB40_round120_full_registration_v4')";assert text.count(needle)==1
    text=text.replace(needle,"'nonflag_HGB40_round120_full_registration_v4',\n        'nonflag_residual_Ridge_native_bank10','nonflag_residual_Ridge_actual_hooks_and_main_after120','nonflag_residual_Ridge37_transform_preflight',\n        'nonflag_Ridge40_round121_source_admission_v1','nonflag_Ridge40_continue_after_actual_admission',\n        'nonflag_Ridge40_full37_controls_main_publication_v1','nonflag_Ridge40_official_comparison_v1','nonflag_Ridge40_scores_main_publication_v1',\n        'nonflag_Ridge40_selected_candidate_preparation_v1','nonflag_Ridge40_selected_candidate_sealing_v1','nonflag_Ridge40_round121_full_registration_v1')")
    text=text.replace('(119, 30), (120, 31))','(119, 30), (120, 31), (121, 32))')
    text=text.replace("120:'nonflag_HGB40_round120_full_registration_v4'}[n]","120:'nonflag_HGB40_round120_full_registration_v4',121:'nonflag_Ridge40_round121_full_registration_v1'}[n]")
    needle="    value['no_full_qualification_claim_from_partial_case_counts']=True"; assert text.count(needle)==1
    extra="""    ridge_bank=A/'nonflag_residual_Ridge_bank10_20261007/verification.json'
    ridge_controls=A/'nonflag_residual_Ridge37_transform_preflight_20261007/verification.json'
    ridge_hooks=A/'nonflag_residual_Ridge_native_hook3_preflight_20261007/verification.json'
    value['Ridge_actual_native_fit_count']=read(ridge_bank)['actual_native_fits'] if ridge_bank.exists() else len(list((A/'nonflag_residual_Ridge_bank10_20261007').glob('*/info_*.json')))
    value['Ridge_actual_full_transform_controls']=read(ridge_controls)['actual_full_cases'] if ridge_controls.exists() else 0
    value['Ridge_actual_cold_prefix_controls']=read(ridge_controls)['actual_cold_cases'] if ridge_controls.exists() else 0
    value['Ridge_actual_historical_native_hook_controls']=len(read(ridge_hooks)['records']) if ridge_hooks.exists() else 0
    ridge_score=A/'nonflag_Ridge40_official_comparison_v1_20261007'
    value['Ridge40_actual_official_cases_completed']=len(list(ridge_score.glob('case*_official.json')))
    value['Ridge40_expected_official_cases']=40
    if (ridge_score/'actual_stage.json').exists():value['Ridge40_actual_official_stage']=read(ridge_score/'actual_stage.json')
    value['Ridge121_fully_qualified']=121 in qualified
    value['Ridge_native_controls_are_not_official_selection_or_full_candidate_qualification']=True
    ridge_receipt=A/'nonflag_residual_Ridge10_actual_controls_github_20261007/receipt.json'
    if ridge_receipt.exists():value['Ridge_actual_native_controls_main_receipt']=read(ridge_receipt)
"""
    text=text.replace(needle,extra+needle); compile(text,str(target),'exec'); assert not target.exists(); target.write_text(text,encoding='utf8',newline='\n')
    old_h=A/'handoff_local_only_monitor_v20_20261007.py'; new_h=A/'handoff_local_only_monitor_v21_20261007.py'
    h=substitute(old_h.read_text(encoding='utf8'),{
        'local_only_monitor_v20_actual_handoff_20261007':'local_only_monitor_v21_actual_handoff_20261007',
        'local_only_progress_monitor_v19':'local_only_progress_monitor_v20','local_only_progress_monitor_v20':'local_only_progress_monitor_v21',
        'monitor_local_only_runtime_v19_20261007.py':'monitor_local_only_runtime_v20_20261007.py','monitor_local_only_runtime_v20_20261007.py':'monitor_local_only_runtime_v21_20261007.py',
        'local_only_v20':'local_only_v21','administrative_supersession_local_v20_20261007':'administrative_supersession_local_v21_20261007',
        'passed_actual_idle_observer19_correct119v6_120v4_closures_and_original_science_preserved':'passed_actual_idle_observer20_Ridge121_real_native_controls_and_qualified_only_routes'})
    needle="        assert all(owned(r) for r in preserved.values())"; assert h.count(needle)==1
    h=h.replace(needle,"        assert live['Ridge_actual_native_fit_count']==10 and live['Ridge_actual_full_transform_controls']==37 and live['Ridge_actual_cold_prefix_controls']==111\n"+needle)
    compile(h,str(new_h),'exec'); assert not new_h.exists(); new_h.write_text(h,encoding='utf8',newline='\n')
    create(A/'local_only_monitor_v21_source_preparation_20261007.json',{'status':'compiled_Ridge121_owned_stage_and_strict_full_qualification_monitor',
        'input_sha256':{str(p):sha(p) for p in (Path(__file__),old,target,old_h,new_h)},'scientific_workers_stopped':0})
if __name__=='__main__':main()
