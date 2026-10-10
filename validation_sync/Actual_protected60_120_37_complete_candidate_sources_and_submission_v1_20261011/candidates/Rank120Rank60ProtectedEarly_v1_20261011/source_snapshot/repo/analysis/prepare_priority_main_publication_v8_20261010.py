"""Publish the model-free compression frontier and every actual completed comparison to main."""
from pathlib import Path
import sys
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A),str(A.parent)]
from prepare_protected162_candidate_sources_v2_20261010 import change
from run_dependency_queue_v3_20261006 import sha,create,read,owned
from handoff_ready_goss_full_execution_20261006 import start_service
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed

def main():
    assert allowed();s=(A/'publish_high_impact_priority_v7_20261010.py').read_text(encoding='utf8')
    s=s.replace('main_v7_20261010','main_v8_20261010').replace('receipt_v7_20261010','receipt_v8_20261010').replace("'_v7_20261010'","'_v8_20261010'")
    s=change(s,"'huber65':'Huber010_high_impact65_screen_v1_20261010'","'huber65':'Huber010_high_impact65_screen_v1_20261010','quant37':'protected_quantization37_screen_v1_20261010'")
    s=change(s,"'huber65':'actual_Huber010_high_impact65_screen_v1_20261010'","'huber65':'actual_Huber010_high_impact65_screen_v1_20261010','quant37':'actual_protected_quantization37_screen_v1_20261010'")
    s=change(s,"    if phase in ('scores','protected','valid','huber65'):","    sources.extend(A/n for n in ('protected_lower_rank_quantization_v1_20261010.py','protected_lower_rank_quantization_v2_20261010.py','protected_lower_rank_quantization_v3_20261010.py','verify_protected_lower_rank_quantization_v1_20261010.py','protected_lower_rank_quantization_controls_v1_20261010.json','prepare_fast_quantization_controls_v2_20261010.py','prepare_fast_quantization_controls_v3_20261010.py','run_fast_quantization_controls_v3_20261010.py','protected_lower_rank_quantization_controls_v3_20261010.json','run_protected_quantization37_screen_v1_20261010.py','protected_quantization37_actual_hidden_launch_v1_20261010.json','monitor_fast_optimization_v14_20261010.py','prepare_progress_observer14_Huber65_v1_20261010.py','save_high_impact_runtime_handoff_v11_20261010.py','actual_optimization_fast_runtime_handoff_v11_20261010.json','high_impact_priority_protected_main_receipt_v7_20261010.json','protected_official_top_screen_v2_20261010_location_reconciliation_v2_20261010.json'))\n    sources.extend((A/'Huber65_progress_observer_handoff_v14_20261010').glob('*.json'))\n    if phase in ('scores','protected','valid','huber65','quant37'):")
    s=change(s,"expected=65 if phase=='huber65' else 37 if phase in ('protected','valid') else 97","expected=65 if phase=='huber65' else 37 if phase in ('protected','valid','quant37') else 97")
    s=change(s,"'actual_Huber010_high_impact65_screen_location_v1_20261010.json' if phase=='huber65'","'actual_protected_quantization37_screen_location_v1_20261010.json' if phase=='quant37' else 'actual_Huber010_high_impact65_screen_location_v1_20261010.json' if phase=='huber65'")
    s=s.replace("choices=['preparation','scores','protected','valid','huber65']","choices=['preparation','scores','protected','valid','huber65','quant37']")
    target=A/'publish_high_impact_priority_v8_20261010.py';assert not target.exists();compile(s,str(target),'exec');target.write_text(s,encoding='utf8',newline='\n')
    for phase in ('preparation','quant37'):
        name='actual_high_impact_priority_'+phase+'_main_v8_20261010'
        try:row=start_service(name,target.name,[phase],{str(target):sha(target)})
        except AssertionError:
            folder=A/'service_owned_workflows_20261006'/name;row=read(folder/'native_launch.json');assert not owned(row) and read(folder/'service_execution.json')['status']=='passed'
        create(A/('high_impact_priority_'+phase+'_main_hidden_launch_v8_20261010.json'),row);print(phase,row['owned_worker_pid'],flush=True)

if __name__=='__main__':main()
