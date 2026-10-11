"""Track actual saved/resumed native fits and126 full qualification without partial claims."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import sha,create
from prepare_protected_upper_pool_HGB66_round115_sources_20261007 import substitute

def main():
    old=A/'monitor_local_only_runtime_v24_20261007.py';new=A/'monitor_local_only_runtime_v25_20261007.py';assert not new.exists()
    text=substitute(old.read_text(encoding='utf8'),{
        'local_only_v24':'local_only_v25','single_host_optimization_live_status_v24_20261007':'single_host_optimization_live_status_v25_20261007'})
    services=['RFF128Low_checkpoint_memory_release_exact_idle_handoff','nonflag_residual_RFF128Low_native_bank10',
        'nonflag_residual_RFF128Low_native_bank10_v2','nonflag_RFF128Low_actual_hook6_and_full73_controls',
        'nonflag_RFF128Low_actual_hook6_and_full73_controls_v2','RFF128Low_actual_history_main_after125',
        'RFF128Low_actual_history_main_after125_v2','RFF128Low_actual_history_main_after125_v3',
        'nonflag_RFF128Low76_actual_admission_dependency_queue','nonflag_RFF128Low76_actual_admission_dependency_queue_v2',
        'nonflag_RFF128Low76_actual_admission_dependency_queue_v3','nonflag_RFF128Low76_round126_source_admission_v1',
        'nonflag_RFF128Low76_full37_controls_main_publication_v1','nonflag_RFF128Low76_official_comparison_v1',
        'nonflag_RFF128Low76_scores_main_publication_v1','nonflag_RFF128Low76_selected_candidate_preparation_v1',
        'nonflag_RFF128Low76_selected_candidate_sealing_v1','nonflag_RFF128Low76_round126_full_registration_v1']
    needle="'nonflag_RFF12876_round125_full_registration_v1')";assert text.count(needle)==1
    text=text.replace(needle,"'nonflag_RFF12876_round125_full_registration_v1',"+','.join(map(repr,services))+')')
    text=text.replace('(124, 35), (125, 36))','(124, 35), (125, 36), (126, 37))')
    text=text.replace("125:'nonflag_RFF12876_round125_full_registration_v1'}[n]",
        "125:'nonflag_RFF12876_round125_full_registration_v1',126:'nonflag_RFF128Low76_round126_full_registration_v1'}[n]")
    needle="    value['no_full_qualification_claim_from_partial_case_counts']=True";assert text.count(needle)==1
    extra="""    low=A/'nonflag_residual_RFF128Low_bank10_20261007'
    low_proof=low/'verification.json'
    value['RFF128Low_actual_native_fits']=read(low_proof)['actual_native_fits'] if low_proof.exists() else len(list(low.glob('*/info_*.json')))
    if low_proof.exists():
        evidence=read(low_proof)
        value['RFF128Low_saved_native_fits_reused']=evidence['reused_saved_native_fits']
        value['RFF128Low_actual_new_native_fits_by_resume']=evidence['actual_new_native_fits_by_resume']
        value['RFF128Low_remaining_training_and_controls_seconds']=evidence['elapsed_seconds']
        value['RFF128Low_elapsed_scope']=evidence['elapsed_seconds_scope']
    c=A/'nonflag_residual_RFF128Low73_transform_preflight_20261007/verification.json'
    h=A/'nonflag_residual_RFF128Low_native_hook6_preflight_20261007/verification.json'
    value['RFF128Low_actual_full_controls']=read(c)['actual_full_cases'] if c.exists() else 0
    value['RFF128Low_actual_cold_controls']=read(c)['actual_cold_cases'] if c.exists() else 0
    value['RFF128Low_actual_native_hooks']=len(read(h)['records']) if h.exists() else 0
    low_cases=A/'nonflag_RFF128Low76_official_comparison_v1_20261007'
    value['RFF128Low76_actual_official_cases_completed']=len(list(low_cases.glob('case*_official.json')))
    value['RFF128Low76_expected_official_cases']=76
    if (low_cases/'actual_stage.json').exists():value['RFF128Low76_actual_official_stage']=read(low_cases/'actual_stage.json')
    value['RFF128Low126_fully_qualified']=126 in qualified
    value['RFF128Low_partial_controls_do_not_prove_candidate_qualification']=True
    p=A/'RFF128Low_actual_history_github_20261007/receipt.json'
    if p.exists():value['RFF128Low_actual_history_main_receipt']=read(p)
"""
    text=text.replace(needle,extra+needle)
    compile(text,str(new),'exec');new.write_text(text,encoding='utf8',newline='\n')
    oldh=A/'handoff_local_only_monitor_v24_20261007.py';newh=A/'handoff_local_only_monitor_v25_20261007.py';assert not newh.exists()
    h=substitute(oldh.read_text(encoding='utf8'),{
        'local_only_monitor_v24_actual_handoff_20261007':'local_only_monitor_v25_actual_handoff_20261007',
        'local_only_progress_monitor_v23':'local_only_progress_monitor_v24','local_only_progress_monitor_v24':'local_only_progress_monitor_v25',
        'monitor_local_only_runtime_v23_20261007.py':'monitor_local_only_runtime_v24_20261007.py',
        'monitor_local_only_runtime_v24_20261007.py':'monitor_local_only_runtime_v25_20261007.py',
        'local_only_v24':'local_only_v25','administrative_supersession_local_v24_20261007':'administrative_supersession_local_v25_20261007',
        'passed_actual_idle_observer23_RFF128125_real_native_and_qualified_only_routes':'passed_actual_idle_observer24_checkpointed_LOW_native_and126_qualified_only_routes'})
    needle="        assert all(owned(r) for r in preserved.values())";assert h.count(needle)==1
    h=h.replace(needle,"        assert live['RFF128125_fully_qualified'] and live['RFF128Low_actual_native_fits']==10\n        assert live['RFF128Low_actual_full_controls']==73 and live['RFF128Low_actual_cold_controls']==219\n"+needle)
    compile(h,str(newh),'exec');newh.write_text(h,encoding='utf8',newline='\n')
    pins={str(p):sha(p) for p in [Path(__file__),old,new,oldh,newh]}
    create(A/'local_only_monitor_v25_source_preparation_20261007.json',
        {'status':'compiled_actual_checkpoint_resume_and126_qualified_only_local_monitor','input_sha256':pins,'scientific_workers_stopped':0})
    from handoff_ready_goss_full_execution_20261006 import start_service
    row=start_service('local_only_monitor_v25_exact_idle_handoff',newh.name,[],pins)
    create(A/'local_only_monitor_v25_actual_handoff_hidden_launch_20261007.json',row)
if __name__=='__main__':main()
