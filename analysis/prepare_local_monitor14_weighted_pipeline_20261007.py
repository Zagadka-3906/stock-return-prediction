"""Route the observer to actual full337 proof and the complete117 qualification gate."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis'
sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import sha,create

def save(name,text):
    p=A/name;assert not p.exists();compile(text,str(p),'exec');p.write_text(text,encoding='utf8',newline='\n');return p

def main():
    old=A/'monitor_local_only_runtime_v13_20261007.py';text=old.read_text(encoding='utf8')
    text=text.replace('local_only_v13','local_only_v14').replace('live_status_v13','live_status_v14')
    needle="'all_forecast_percentiles_full_scoring_benchmark','weighted_HGB_and_percentile_controls_main_publication')"
    assert text.count(needle)==1
    text=text.replace(needle,"'all_forecast_percentiles_full_scoring_benchmark','weighted_HGB_and_percentile_controls_main_publication',\n        'weighted_HGB340_round117_source_admission','weighted_HGB340_full337_controls_main_publication',\n        'flagged_HGB_weighted_quarters340_official_comparison','flagged_HGB_weighted_quarters340_scores_main_publication',\n        'flagged_HGB_weighted_quarters340_selected_candidate_preparation','flagged_HGB_weighted_quarters340_selected_candidate_sealing',\n        'weighted_HGB340_round117_full_registration')")
    text=text.replace('(115, 26), (116, 27))','(115, 26), (116, 27), (117, 28))')
    needle="116:'flagged_HGB88_round116_full_registration_v2'}[n]";assert text.count(needle)==1
    text=text.replace(needle,"116:'flagged_HGB88_round116_full_registration_v2',117:'weighted_HGB340_round117_full_registration'}[n]")
    needle="    value['weighted340_expected_cases']=340";assert text.count(needle)==1
    text=text.replace(needle,needle+"\n    stage=A/'flagged_HGB_weighted_quarters340_official_comparison_20261007/actual_stage.json'\n    if stage.exists():value['weighted340_actual_stage']=read(stage)")
    text=text.replace("value['weighted340_partial_controls_not_candidate_qualification']=True","value['weighted340_partial_controls_not_candidate_qualification']=117 not in qualified")
    monitor=save('monitor_local_only_runtime_v14_20261007.py',text)
    original=A/'handoff_local_only_monitor_v13_recovery_v2_20261007.py';h=original.read_text(encoding='utf8')
    routes={
      'local_only_monitor_v13_actual_handoff_recovery_v2_20261007':'local_only_monitor_v14_actual_handoff_20261007',
      'local_only_progress_monitor_v12':'local_only_progress_monitor_v13',
      'monitor_local_only_runtime_v12_20261007':'monitor_local_only_runtime_v13_20261007',
      'monitor_local_only_runtime_v13_20261007':'monitor_local_only_runtime_v14_20261007',
      'local_only_progress_monitor_v13':'local_only_progress_monitor_v14','local_only_v13':'local_only_v14',
      'administrative_supersession_local_v13_20261007':'administrative_supersession_local_v14_20261007'}
    from prepare_protected_upper_pool_HGB66_round115_sources_20261007 import substitute
    h=substitute(h,routes)
    h=h.replace("f'    <module> (monitor_local_only_runtime_v12_20261007.py:{sleep_line})'","f'    <module> (monitor_local_only_runtime_v13_20261007.py:{sleep_line})'")
    h=h.replace("A/'flagged_HGB88_round116_source_path_recovery_actual_launch_v2_20261007.json',A/'weighted_flagged_HGB_full337_actual_source_route_recovery_v3_20261007.json'","A/'weighted_HGB340_complete_pipeline_actual_hidden_launches_20261007.json',A/'weighted_HGB340_round117_source_admission_20261007.json'")
    handoff=save('handoff_local_only_monitor_v14_20261007.py',h)
    create(A/'local_monitor14_weighted_pipeline_source_preparation_20261007.json',{'status':'compiled_actual117_full_qualification_and_local340_monitor_routes',
      'input_sha256':{str(p):sha(p) for p in [Path(__file__),old,monitor,original,handoff]},'new_quality_scores':0,'new_native_fits':0,'scientific_workers_stopped':0})

if __name__=='__main__':main()
