"""Publish the admitted complete162 chain now, and all65 new-Huber scores when actually complete."""
from pathlib import Path
import sys
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A),str(A.parent)]
from prepare_protected162_candidate_sources_v2_20261010 import change
from run_dependency_queue_v3_20261006 import sha,create,read,owned
from handoff_ready_goss_full_execution_20261006 import start_service
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed

def main():
    assert allowed()
    s=(A/'publish_high_impact_priority_v6_20261010.py').read_text(encoding='utf8')
    s=s.replace('main_v6_20261010','main_v7_20261010').replace('receipt_v6_20261010','receipt_v7_20261010')
    s=s.replace("'_v6_20261010'","'_v7_20261010'")
    s=change(s,"'valid':'protected_upper_tail_screen_v1_20261010'","'valid':'protected_upper_tail_screen_v1_20261010','huber65':'Huber010_high_impact65_screen_v1_20261010'")
    s=change(s,"'valid':'actual_protected_upper_tail_screen_v1_20261010'","'valid':'actual_protected_upper_tail_screen_v1_20261010','huber65':'actual_Huber010_high_impact65_screen_v1_20261010'")
    s=change(s,"    if phase in ('scores','protected','valid'):","    sources.extend(A/n for n in ('verify_protected162_full_family_preflight_v1_20261010.py','protected162_full_family_preflight_v1_20261010.json','TailProtected162_full76_ready_dispatch_v1_20261010.json','run_Huber010_high_impact65_screen_v1_20261010.py','Huber010_high_impact65_actual_hidden_queue_v1_20261010.json','high_impact_priority_preparation_main_receipt_v6_20261010.json','high_impact_priority_scores_main_receipt_v6_20261010.json','high_impact_priority_valid_main_receipt_v6_20261010.json'))\n    if phase in ('scores','protected','valid','huber65'):")
    s=change(s,"expected=37 if phase in ('protected','valid') else 97","expected=65 if phase=='huber65' else 37 if phase in ('protected','valid') else 97")
    s=change(s,"        if phase!='valid':sources.append(A/('actual_protected_official_top_screen_location_v2_20261010.json' if phase=='protected' else 'actual_high_impact_cumulative_screen_location_v2_20261010.json'))","        if phase!='valid':sources.append(A/('actual_Huber010_high_impact65_screen_location_v1_20261010.json' if phase=='huber65' else 'actual_protected_official_top_screen_location_v2_20261010.json' if phase=='protected' else 'actual_high_impact_cumulative_screen_location_v2_20261010.json'))")
    s=s.replace("choices=['preparation','scores','protected','valid']","choices=['preparation','scores','protected','valid','huber65']")
    target=A/'publish_high_impact_priority_v7_20261010.py';assert not target.exists();compile(s,str(target),'exec');target.write_text(s,encoding='utf8',newline='\n')
    for phase in ('preparation','huber65'):
        name='actual_high_impact_priority_'+phase+'_main_v7_20261010'
        try:row=start_service(name,target.name,[phase],{str(target):sha(target)})
        except AssertionError:
            folder=A/'service_owned_workflows_20261006'/name;row=read(folder/'native_launch.json');assert not owned(row) and read(folder/'service_execution.json')['status']=='passed'
        create(A/('high_impact_priority_'+phase+'_main_hidden_launch_v7_20261010.json'),row);print(phase,row['owned_worker_pid'],flush=True)

if __name__=='__main__':main()
