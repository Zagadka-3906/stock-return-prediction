"""Publish causal optional-swap methodology and all completed actual37 records to main."""
from pathlib import Path
import sys
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A),str(A.parent)]
from prepare_protected162_candidate_sources_v2_20261010 import change
from run_dependency_queue_v3_20261006 import sha,create,read,owned
from handoff_ready_goss_full_execution_20261006 import start_service
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed

def main():
    assert allowed();s=(A/'publish_high_impact_priority_v8_20261010.py').read_text(encoding='utf8')
    s=s.replace('main_v8_20261010','main_v9_20261010').replace('receipt_v8_20261010','receipt_v9_20261010').replace("'_v8_20261010'","'_v9_20261010'")
    s=change(s,"'quant37':'protected_quantization37_screen_v1_20261010'","'quant37':'protected_quantization37_screen_v1_20261010','budget37':'budgeted_neural_Top37_screen_v1_20261010'")
    s=change(s,"'quant37':'actual_protected_quantization37_screen_v1_20261010'","'quant37':'actual_protected_quantization37_screen_v1_20261010','budget37':'actual_budgeted_neural_Top37_screen_v1_20261010'")
    s=change(s,"    if phase in ('scores','protected','valid','huber65','quant37'):","    sources.extend(A/n for n in ('budgeted_neural_Top_projection37_proposal_v1_20261010.json','budgeted_neural_Top_projection_v1_20261010.py','verify_budgeted_neural_Top_projection_v1_20261010.py','budgeted_neural_Top_projection_controls_v1_20261010.json','run_budgeted_neural_Top37_screen_v1_20261010.py','budgeted_neural_Top37_actual_hidden_launch_v1_20261010.json','monitor_fast_optimization_v15_20261010.py','prepare_progress_observer15_quantization37_v1_20261010.py','save_high_impact_runtime_handoff_v12_20261010.py','actual_optimization_fast_runtime_handoff_v12_20261010.json'))\n    sources.extend((A/'quantization37_progress_observer_handoff_v15_20261010').glob('*.json'))\n    if phase in ('scores','protected','valid','huber65','quant37','budget37'):")
    s=change(s,"phase in ('protected','valid','quant37')","phase in ('protected','valid','quant37','budget37')")
    s=change(s,"'actual_protected_quantization37_screen_location_v1_20261010.json' if phase=='quant37'","'actual_budgeted_neural_Top37_screen_location_v1_20261010.json' if phase=='budget37' else 'actual_protected_quantization37_screen_location_v1_20261010.json' if phase=='quant37'")
    s=s.replace("choices=['preparation','scores','protected','valid','huber65','quant37']","choices=['preparation','scores','protected','valid','huber65','quant37','budget37']")
    target=A/'publish_high_impact_priority_v9_20261010.py';assert not target.exists();compile(s,str(target),'exec');target.write_text(s,encoding='utf8',newline='\n')
    for phase in ('preparation','budget37'):
        name='actual_high_impact_priority_'+phase+'_main_v9_20261010'
        try:row=start_service(name,target.name,[phase],{str(target):sha(target)})
        except AssertionError:
            folder=A/'service_owned_workflows_20261006'/name;row=read(folder/'native_launch.json');assert not owned(row) and read(folder/'service_execution.json')['status']=='passed'
        create(A/('high_impact_priority_'+phase+'_main_hidden_launch_v9_20261010.json'),row);print(phase,row['owned_worker_pid'],flush=True)

if __name__=='__main__':main()
