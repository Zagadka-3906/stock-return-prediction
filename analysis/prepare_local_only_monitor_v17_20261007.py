"""Observe actual recovery identities while preserving qualified-only ranking gates."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis'
sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_upper_pool_HGB66_round115_sources_20261007 import substitute
from prepare_local_118_119_protocol_recovery_v4_20261007 import maps

def main():
    mapping=maps();mapping.update(read(A/'local_118_119_protocol_recovery_source_preparation_v4_20261007.json')['service_mapping'])
    mapping.update({
      'flagged_HGB_weighted_quarters340_selected_candidate_preparation':'flagged_HGB_weighted_quarters340_selected_candidate_preparation_v4',
      'flagged_HGB_weighted_quarters340_selected_candidate_sealing':'flagged_HGB_weighted_quarters340_selected_candidate_sealing_v4',
      'local_only_v16':'local_only_v17','single_host_optimization_live_status_v16_20261007':'single_host_optimization_live_status_v17_20261007'})
    old=A/'monitor_local_only_runtime_v16_20261007.py';text=substitute(old.read_text(encoding='utf8'),mapping)
    needle="        'nonflag_residual_HGB10_training')"
    assert text.count(needle)==1
    text=text.replace(needle,"        'nonflag_residual_HGB10_training','nonflag_residual_HGB37_transform_preflight','nonflag_residual_HGB_native_hook3_preflight','nonflag_HGB10_actual_controls_main_publication')")
    needle="    value['no_full_qualification_claim_from_partial_case_counts']=True"
    assert text.count(needle)==1
    text=text.replace(needle,"""    for key,relative in (
        ('actual_nonflag37_full_controls','nonflag_residual_HGB37_transform_preflight_20261007/verification.json'),
        ('actual_nonflag3_historical_native_hooks','nonflag_residual_HGB_native_hook3_preflight_20261007/verification.json'),
        ('actual_nonflag10_controls_main_receipt','nonflag_HGB10_actual_controls_github_20261007/receipt.json')):
        path=A/relative
        if path.exists():
            proof=read(path);value[key]={k:v for k,v in proof.items() if k in ('status','commit','branch','actual_native_fits','elapsed_seconds')}
"""+needle)
    target=A/'monitor_local_only_runtime_v17_20261007.py';assert not target.exists();compile(text,str(target),'exec');target.write_text(text,encoding='utf8')
    old_h=A/'handoff_local_only_monitor_v16_20261007.py'
    h=substitute(old_h.read_text(encoding='utf8'),{
      'local_only_monitor_v16_actual_handoff_20261007':'local_only_monitor_v17_actual_handoff_20261007',
      'local_only_progress_monitor_v15':'local_only_progress_monitor_v16','local_only_progress_monitor_v16':'local_only_progress_monitor_v17',
      'monitor_local_only_runtime_v15_20261007.py':'monitor_local_only_runtime_v16_20261007.py','monitor_local_only_runtime_v16_20261007.py':'monitor_local_only_runtime_v17_20261007.py',
      'local_only_v16':'local_only_v17','administrative_supersession_local_v16_20261007':'administrative_supersession_local_v17_20261007',
      'passed_actual_idle_observer15_correct119v3_qualification_and_all_existing_science_preserved':'passed_actual_idle_observer16_correct117_118_119_recovery_qualification_and_all_science_preserved'})
    target_h=A/'handoff_local_only_monitor_v17_20261007.py';assert not target_h.exists();compile(h,str(target_h),'exec');target_h.write_text(h,encoding='utf8')
    create(A/'local_only_monitor_v17_source_preparation_20261007.json',{'status':'compiled_actual_recovery_routes_and_nonflag_controls_qualified_only_observer',
      'input_sha256':{str(p):sha(p) for p in [Path(__file__),old,target,old_h,target_h]},'scientific_workers_stopped':0})

if __name__=='__main__':main()
