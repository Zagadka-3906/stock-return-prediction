"""Actual nested hook tests, pending six-state controls, and compact successor observer."""
from pathlib import Path
import sys
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from handoff_ready_goss_full_execution_20261006 import start_service
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
def save(name,text):
    p=A/name;assert not p.exists();compile(text,str(p),'exec');p.write_text(text,encoding='utf8',newline='\n');return p
def main():
    assert allowed()
    original=A/'verify_frontier133_actual_nested_parent_hooks_CPU_v1_20261010.py';text=original.read_text(encoding='utf8')
    text=text.replace('import predict_frontier133_complete_qualified_parent_scheme_v1_20261010 as actual','import predict_stock_embedding_complete_qualified_parent_scheme_v1_20261010 as actual')
    text=text.replace('    rows=[];inputs=',"    from frontier133_after_complete_qualified_parent_native_stage_v1_20261010 import GRAPH_KEY as key133\n    routes.append(({key133:{}},'predict_frontier133_complete_qualified_parent_scheme_v1_20261010.py'))\n    rows=[];inputs=")
    text=text.replace('FRONTIER133_AFTER_WHOLE_QUALIFIED_PARENT','STOCK_EMBEDDING_AFTER_WHOLE_QUALIFIED_PARENT').replace('frontier133_actual_three_nested_parent_hooks_CPU_controls_v1','stock_embedding_actual_four_nested_parent_hooks_CPU_controls_v1').replace('passed_actual_three_parent_source','passed_actual_four_parent_source')
    hooks=save('verify_stock_embedding_actual_four_nested_parent_hooks_CPU_v1_20261010.py',text)
    scope={'__file__':str(hooks),'__name__':'actual_stock_hook_CPU_check'};exec(compile(text,str(hooks),'exec'),scope);scope['main']()
    old=A/'verify_stock_embedding_six_state_native42_v1_20261010.py';text=old.read_text(encoding='utf8')
    text=text.replace('                for sign in (1.,-1.):',"                for sign in (1.,-1.):\n                    assert allowed()\n                    if Path('E:/赛题五_本机临时/Dual120Consensus_after169_high_impact193_screen_v1_20261010/verification.json').exists():closed('Frontier133172_selected_candidate_sealing_v1_20261010')")
    native=save('verify_stock_embedding_six_state_native42_v2_20261010.py',text)
    old=A/'monitor_fast_optimization_v45_20261010.py';text=old.read_text(encoding='utf8')
    text=text.replace("jobs=['actual_stock_embedding_own_training_queue_v4_20261010'","jobs=['actual_stock_embedding_six_state_native42_v2_20261010','actual_stock_embedding_checkpoint_yield_training_queue_v5_20261010','actual_stock_embedding_own_training_queue_v4_20261010'")
    text=text.replace('optimization_live_progress_v45','optimization_live_progress_v46').replace('actual_optimization_fast_runtime_handoff_v73','actual_optimization_fast_runtime_handoff_v75').replace('high_impact_additional_validation_rankings_v16','high_impact_additional_validation_rankings_v17')
    observer=save('monitor_fast_optimization_v46_20261010.py',text)
    for name,driver,receipt in [('actual_stock_embedding_six_state_native42_v2_20261010',native,'actual_stock_embedding_six_state_native42_activation_v2_20261010.json'),('actual_fast_optimization_progress_v46_20261010',observer,'actual_fast_optimization_progress_v46_activation_20261010.json')]:
        assert allowed();row=start_service(name,driver.name,[],{str(driver):sha(driver)});create(A/receipt,row)
    create(A/'stock_embedding_actual_four_hooks_native42_and_observer_admission_v46_20261010.json',{'status':'actual_four_nested_CPU_hooks_passed_native42_and_observer46_started','input_sha256':{str(p):sha(p) for p in [Path(__file__),hooks,A/'stock_embedding_actual_four_nested_parent_hooks_CPU_controls_v1_20261010.json',native,observer]},'actual_six_saved_state_native42_completion_pending':True,'new_quality_scores':0})
if __name__=='__main__':main()
