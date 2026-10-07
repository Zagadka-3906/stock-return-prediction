"""Observe the actual 128-component bank and require real124/125 full closures."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import sha,create
from prepare_protected_upper_pool_HGB66_round115_sources_20261007 import substitute
def main():
    old=A/'monitor_local_only_runtime_v23_20261007.py';new=A/'monitor_local_only_runtime_v24_20261007.py'
    text=substitute(old.read_text(encoding='utf8'),{
      'local_only_v23':'local_only_v24','single_host_optimization_live_status_v23_20261007':'single_host_optimization_live_status_v24_20261007'})
    needle="'nonflag_reverse_RFF40_round123_full_registration_v1')";assert text.count(needle)==1
    services=['nonflag_reverse_Ridge_actual_hook3_and_full37_controls','nonflag_reverse_Ridge40_round124_source_admission_v1',
      'nonflag_reverse_Ridge40_continue_after_actual_admission','nonflag_reverse_Ridge40_full37_controls_main_publication_v1',
      'nonflag_reverse_Ridge40_official_comparison_v1','nonflag_reverse_Ridge40_scores_main_publication_v1',
      'nonflag_reverse_Ridge40_selected_candidate_preparation_v1','nonflag_reverse_Ridge40_selected_candidate_sealing_v1',
      'nonflag_reverse_Ridge40_round124_full_registration_v1','nonflag_residual_RFF128_native_bank10',
      'nonflag_RFF128_actual_hook6_and_full73_controls','RFF128_actual_history_main_after124',
      'nonflag_RFF12876_round125_source_admission_v1','nonflag_RFF12876_continue_after_actual_admission_v2',
      'nonflag_RFF12876_full37_controls_main_publication_v1','nonflag_RFF12876_official_comparison_v1',
      'nonflag_RFF12876_scores_main_publication_v1','nonflag_RFF12876_selected_candidate_preparation_v1',
      'nonflag_RFF12876_selected_candidate_sealing_v1','nonflag_RFF12876_round125_full_registration_v1']
    text=text.replace(needle,"'nonflag_reverse_RFF40_round123_full_registration_v1',\n        "+','.join(repr(n) for n in services)+')')
    text=text.replace('(122, 33), (123, 34))','(122, 33), (123, 34), (124, 35), (125, 36))')
    text=text.replace("123:'nonflag_reverse_RFF40_round123_full_registration_v1'}[n]",
      "123:'nonflag_reverse_RFF40_round123_full_registration_v1',124:'nonflag_reverse_Ridge40_round124_full_registration_v1',125:'nonflag_RFF12876_round125_full_registration_v1'}[n]")
    needle="    value['no_full_qualification_claim_from_partial_case_counts']=True";assert text.count(needle)==1
    text=text.replace(needle,"""    linear_reverse=A/'nonflag_reverse_Ridge40_official_comparison_v1_20261007'
    value['reverse_Ridge40_actual_official_cases_completed']=len(list(linear_reverse.glob('case*_official.json')))
    value['reverse_Ridge124_fully_qualified']=124 in qualified
    rff128=A/'nonflag_residual_RFF128_bank10_20261007'
    proof_path=rff128/'verification.json'
    value['RFF128_actual_native_fits']=read(proof_path)['actual_native_fits'] if proof_path.exists() else len(list(rff128.glob('*/info_*.json')))
    if proof_path.exists():
        proof=read(proof_path)
        value['RFF128_training_and_native_controls_elapsed_seconds_including_RAM_wait']=proof['elapsed_seconds']
        value['RFF128_sum_native_fit_seconds']=sum(r['fit_seconds'] for r in proof['actual_models'])
    if (rff128/'actual_stage.json').exists():value['RFF128_actual_bank_stage']=read(rff128/'actual_stage.json')
    controls=A/'nonflag_residual_RFF12873_transform_preflight_20261007/verification.json'
    hooks=A/'nonflag_residual_RFF128_native_hook6_preflight_20261007/verification.json'
    value['RFF128_actual_full_controls']=read(controls)['actual_full_cases'] if controls.exists() else 0
    value['RFF128_actual_cold_controls']=read(controls)['actual_cold_cases'] if controls.exists() else 0
    value['RFF128_actual_native_hooks']=len(read(hooks)['records']) if hooks.exists() else 0
    comparison=A/'nonflag_RFF12876_official_comparison_v1_20261007'
    value['RFF12876_actual_official_cases_completed']=len(list(comparison.glob('case*_official.json')))
    value['RFF12876_expected_official_cases']=76
    if (comparison/'actual_stage.json').exists():value['RFF12876_actual_official_stage']=read(comparison/'actual_stage.json')
    value['RFF128125_fully_qualified']=125 in qualified
    value['RFF128_native_controls_not_complete_candidate_qualification']=True
"""+needle)
    assert not new.exists();compile(text,str(new),'exec');new.write_text(text,encoding='utf8',newline='\n')
    old_h=A/'handoff_local_only_monitor_v23_20261007.py';new_h=A/'handoff_local_only_monitor_v24_20261007.py'
    h=substitute(old_h.read_text(encoding='utf8'),{
      'local_only_monitor_v23_actual_handoff_20261007':'local_only_monitor_v24_actual_handoff_20261007',
      'local_only_progress_monitor_v22':'local_only_progress_monitor_v23','local_only_progress_monitor_v23':'local_only_progress_monitor_v24',
      'monitor_local_only_runtime_v22_20261007.py':'monitor_local_only_runtime_v23_20261007.py',
      'monitor_local_only_runtime_v23_20261007.py':'monitor_local_only_runtime_v24_20261007.py',
      'local_only_v23':'local_only_v24','administrative_supersession_local_v23_20261007':'administrative_supersession_local_v24_20261007',
      'passed_actual_idle_observer22_reverse_RFF123_real_controls_and_qualified_only_routes':'passed_actual_idle_observer23_RFF128125_real_native_and_qualified_only_routes'})
    needle="        assert all(owned(r) for r in preserved.values())";assert h.count(needle)==1
    h=h.replace(needle,"        assert live['RFF128_actual_native_fits']==10 and live['RFF128_actual_full_controls']==73 and live['RFF128_actual_cold_controls']==219\n"+needle)
    assert not new_h.exists();compile(h,str(new_h),'exec');new_h.write_text(h,encoding='utf8',newline='\n')
    create(A/'local_only_monitor_v24_source_preparation_20261007.json',
      {'status':'compiled_actual128_native_controls_and_124_125_qualified_only_monitor',
       'input_sha256':{str(p):sha(p) for p in [Path(__file__),old,new,old_h,new_h]},'scientific_workers_stopped':0})
if __name__=='__main__':main()
