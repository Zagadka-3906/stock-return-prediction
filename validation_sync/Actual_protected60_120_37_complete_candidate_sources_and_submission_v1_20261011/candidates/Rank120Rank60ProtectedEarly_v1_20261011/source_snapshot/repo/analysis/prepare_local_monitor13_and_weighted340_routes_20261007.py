"""Prepare fresh local observation and weighted scoring routes; preserve frozen predecessors."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis'
sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import sha,create,read

def save(name,text):
    p=A/name;assert not p.exists();compile(text,str(p),'exec')
    with p.open('x',encoding='utf8',newline='\n') as s:s.write(text)
    return p

def main():
    old=A/'monitor_local_only_runtime_v12_20261007.py'
    text=old.read_text(encoding='utf8').replace('local_only_v12','local_only_v13').replace('live_status_v12','live_status_v13')
    text=text.replace("'flagged_HGB88_round116_full_registration'","'flagged_HGB88_round116_full_registration_v2'")
    needle="'flagged_HGB_small_amplitude88_selected_candidate_sealing_v4','flagged_HGB88_round116_full_registration_v2')"
    assert text.count(needle)==1
    text=text.replace(needle,"'flagged_HGB_small_amplitude88_selected_candidate_sealing_v4','flagged_HGB88_round116_full_registration_v2',\n        'weighted_flagged_HGB_native_hook_preflight_v2','weighted_flagged_HGB_full337_transform_preflight_v3',\n        'all_forecast_percentiles_full_scoring_benchmark','weighted_HGB_and_percentile_controls_main_publication')")
    needle="    value['no_full_qualification_claim_from_partial_case_counts']=True"
    insert="""    for key,relative in (
        ('weighted_native28_diagnostic','weighted_flagged_HGB_native_hook_preflight_v2_20261007/verification.json'),
        ('weighted_full337_controls','flagged_HGB_weighted_quarters340_transform_preflight_20261007/verification.json'),
        ('all_row_percentile_full_scoring_benchmark','all_forecast_percentiles_full_scoring_benchmark_20261007/verification.json'),
        ('weighted_and_speed_main_receipt','weighted_HGB_and_percentile_controls_github_20261007/receipt.json')):
        path=A/relative
        if path.exists():
            proof=read(path)
            value[key]={k:v for k,v in proof.items() if k in ('status','commit','branch','median_full_mapping_and_official_score_phase_speedup','new_native_fits','new_quality_scores')}
    value['weighted340_official_cases_completed']=len(list((A/'flagged_HGB_weighted_quarters340_official_comparison_20261007').glob('case*_official.json')))
    value['weighted340_expected_cases']=340
    value['weighted340_partial_controls_not_candidate_qualification']=True
"""
    assert text.count(needle)==1;text=text.replace(needle,insert+needle)
    monitor=save('monitor_local_only_runtime_v13_20261007.py',text)
    old_handoff=A/'handoff_local_only_monitor_v12_20261007.py'
    handoff=old_handoff.read_text(encoding='utf8').replace('v12','v13').replace('v11','v12').replace('Observer12','Observer13').replace('observer12','observer13')
    handoff=handoff.replace("A/'flagged_HGB88_complete_pipeline_actual_hidden_launches_v4_20261007.json',A/'flagged_HGB88_round116_source_admission_20261007.json'","A/'flagged_HGB88_round116_source_path_recovery_actual_launch_v2_20261007.json',A/'weighted_flagged_HGB_full337_actual_source_route_recovery_v3_20261007.json'")
    h=save('handoff_local_only_monitor_v13_20261007.py',handoff)
    scorer_old=A/'run_flagged_HGB_weighted_quarters340_official_comparison_v2_20261007.py'
    scorer=scorer_old.read_text(encoding='utf8').replace("'weighted_flagged_HGB_full337_transform_preflight_v2'","'weighted_flagged_HGB_full337_transform_preflight_v3'").replace("'flagged_HGB88_round116_full_registration'","'flagged_HGB88_round116_full_registration_v2'")
    s=save('run_flagged_HGB_weighted_quarters340_official_comparison_v3_20261007.py',scorer)
    create(A/'local_monitor13_and_weighted340_route_preparation_20261007.json',{'status':'compiled_fresh_observer_and_actual_dependency_routes_before_launch',
        'input_sha256':{str(p):sha(p) for p in [Path(__file__),old,monitor,old_handoff,h,scorer_old,s]},
        'new_native_fits':0,'new_quality_scores':0,'scientific_workers_stopped':0,'test_labels_read':False})

if __name__=='__main__':main()
