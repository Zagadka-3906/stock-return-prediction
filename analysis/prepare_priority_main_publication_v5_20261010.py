"""Publish all completed screens and the complete162 source foundation with truthful pointers."""
from pathlib import Path
import sys
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A),str(A.parent)]
from prepare_protected162_candidate_sources_v2_20261010 import change
from run_dependency_queue_v3_20261006 import create,sha,read,owned
from handoff_ready_goss_full_execution_20261006 import start_service

def main():
    s=(A/'publish_high_impact_priority_v4_20261010.py').read_text(encoding='utf8').replace('main_v4_20261010','main_v5_20261010').replace('_v4_20261010\')','_v5_20261010\')').replace('receipt_v4_20261010','receipt_v5_20261010')
    s=change(s,"screen=Path('E:/赛题五_本机临时')/('protected_official_top_screen_v2_20261010' if phase=='protected' else 'high_impact_cumulative_screen_v2_20261010')","screen=Path('E:/赛题五_本机临时')/({'protected':'protected_official_top_screen_v2_20261010','valid':'protected_upper_tail_screen_v1_20261010'}.get(phase,'high_impact_cumulative_screen_v2_20261010'))")
    s=change(s,"    if phase in ('scores','protected'):","    from prepare_protected162_full_registry_sources_v1_20261010 import source_paths\n    sources.extend(source_paths())\n    sources.extend(A/n for n in ('monitor_fast_optimization_v13_20261010.py','run_continuous_fast_reused_frontiers_v15_20261010.py','prepare_priority_screen_location_recovery_v2_20261010.py','reconcile_completed_priority_screen_pointer_v1_20261010.py','reconcile_completed_priority_screen_pointer_v2_20261010.py'))\n    sources.extend((A/'high_impact_protected162_priority_controller_handoff_v15_20261010').glob('*.json'))\n    sources.extend((A/'protected162_progress_observer_handoff_v13_20261010').glob('*.json'))\n    sources.extend((A/'service_owned_workflows_20261006/actual_high_impact_priority_protected_main_v2_20261010').glob('*.json'))\n    sources.extend((A/'service_owned_workflows_20261006/actual_high_impact_cumulative_screen_v2_20261010_original_pointer_collision_evidence_v1_20261010').glob('*.json'))\n    sources.extend((A/'service_owned_workflows_20261006/actual_high_impact_cumulative_screen_v2_20261010_location_reconciliation_v1_20261010').glob('*.json'))\n    if phase in ('scores','protected','valid'):")
    s=change(s,"('actual_protected_official_top_screen_v2_20261010' if phase=='protected' else 'actual_high_impact_cumulative_screen_v2_20261010')","({'protected':'actual_protected_official_top_screen_v2_20261010','valid':'actual_protected_upper_tail_screen_v1_20261010'}.get(phase,'actual_high_impact_cumulative_screen_v2_20261010'))")
    s=s.replace("expected=37 if phase=='protected' else 97","expected=37 if phase in ('protected','valid') else 97")
    s=change(s,"        sources.append(A/('actual_protected_official_top_screen_location_v2_20261010.json' if phase=='protected' else 'actual_high_impact_cumulative_screen_location_v2_20261010.json'))","        if phase!='valid':sources.append(A/('actual_protected_official_top_screen_location_v2_20261010.json' if phase=='protected' else 'actual_high_impact_cumulative_screen_location_v2_20261010.json'))")
    s=s.replace("choices=['preparation','scores','protected']","choices=['preparation','scores','protected','valid']").replace("choices=('preparation','scores','protected')","choices=('preparation','scores','protected','valid')")
    target=A/'publish_high_impact_priority_v5_20261010.py';assert not target.exists();compile(s,str(target),'exec');target.write_text(s,encoding='utf8',newline='\n')
    for phase in ('preparation','scores','valid','protected'):
        name='actual_high_impact_priority_'+phase+'_main_v5_20261010'
        row=start_service(name,target.name,[phase],{str(target):sha(target)})
        create(A/('high_impact_priority_'+phase+'_main_hidden_launch_v5_20261010.json'),row);print(phase,row['owned_worker_pid'],flush=True)

if __name__=='__main__':main()
