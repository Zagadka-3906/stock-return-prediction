"""Observe the actual reverse-residual round without altering scientific workers."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import sha,create
from prepare_protected_upper_pool_HGB66_round115_sources_20261007 import substitute
def main():
    old=A/'monitor_local_only_runtime_v22_20261007.py';new=A/'monitor_local_only_runtime_v23_20261007.py'
    text=substitute(old.read_text(encoding='utf8'),{
      'local_only_v22':'local_only_v23','single_host_optimization_live_status_v22_20261007':'single_host_optimization_live_status_v23_20261007'})
    needle="'lossless_string_codec_benchmark_main_after_audit')";assert text.count(needle)==1
    services=['nonflag_RFFRidge40_round122_source_admission_v2','RFFRidge122_actual_admission_history_main_after_full',
      'nonflag_reverse_RFF_actual_hook3_and_full37_controls','nonflag_reverse_RFF40_round123_source_admission_v1',
      'nonflag_reverse_RFF40_continue_after_actual_admission','nonflag_reverse_RFF40_full37_controls_main_publication_v1',
      'nonflag_reverse_RFF40_official_comparison_v1','nonflag_reverse_RFF40_scores_main_publication_v1',
      'nonflag_reverse_RFF40_selected_candidate_preparation_v1','nonflag_reverse_RFF40_selected_candidate_sealing_v1',
      'nonflag_reverse_RFF40_round123_full_registration_v1']
    text=text.replace(needle,"'lossless_string_codec_benchmark_main_after_audit',\n        "+','.join(repr(n) for n in services)+')')
    text=text.replace('(121, 32), (122, 33))','(121, 32), (122, 33), (123, 34))')
    text=text.replace("122:'nonflag_RFFRidge40_round122_full_registration_v1'}[n]",
      "122:'nonflag_RFFRidge40_round122_full_registration_v1',123:'nonflag_reverse_RFF40_round123_full_registration_v1'}[n]")
    needle="    value['no_full_qualification_claim_from_partial_case_counts']=True";assert text.count(needle)==1
    text=text.replace(needle,"""    reverse=A/'nonflag_reverse_RFF40_official_comparison_v1_20261007'
    value['reverse_RFF40_actual_official_cases_completed']=len(list(reverse.glob('case*_official.json')))
    value['reverse_RFF40_expected_official_cases']=40
    if (reverse/'actual_stage.json').exists():value['reverse_RFF40_actual_official_stage']=read(reverse/'actual_stage.json')
    value['reverse_RFF123_fully_qualified']=123 in qualified
    value['reverse_RFF_new_native_fits']=0
"""+needle)
    assert not new.exists();compile(text,str(new),'exec');new.write_text(text,encoding='utf8',newline='\n')
    old_h=A/'handoff_local_only_monitor_v22_20261007.py';new_h=A/'handoff_local_only_monitor_v23_20261007.py'
    h=substitute(old_h.read_text(encoding='utf8'),{
      'local_only_monitor_v22_actual_handoff_20261007':'local_only_monitor_v23_actual_handoff_20261007',
      'local_only_progress_monitor_v21':'local_only_progress_monitor_v22','local_only_progress_monitor_v22':'local_only_progress_monitor_v23',
      'monitor_local_only_runtime_v21_20261007.py':'monitor_local_only_runtime_v22_20261007.py',
      'monitor_local_only_runtime_v22_20261007.py':'monitor_local_only_runtime_v23_20261007.py',
      'local_only_v22':'local_only_v23','administrative_supersession_local_v22_20261007':'administrative_supersession_local_v23_20261007',
      'passed_actual_idle_observer21_RFF122_real_native_controls_and_qualified_only_routes':'passed_actual_idle_observer22_reverse_RFF123_real_controls_and_qualified_only_routes'})
    needle="        assert all(owned(r) for r in preserved.values())";assert h.count(needle)==1
    h=h.replace(needle,"        assert live['RFFRidge122_fully_qualified'] and live['reverse_RFF40_expected_official_cases']==40\n"+needle)
    assert not new_h.exists();compile(h,str(new_h),'exec');new_h.write_text(h,encoding='utf8',newline='\n')
    create(A/'local_only_monitor_v23_source_preparation_20261007.json',
      {'status':'compiled_reverse_RFF123_actual_progress_and_qualified_only_monitor',
       'input_sha256':{str(p):sha(p) for p in [Path(__file__),old,new,old_h,new_h]},'scientific_workers_stopped':0})
if __name__=='__main__':main()
