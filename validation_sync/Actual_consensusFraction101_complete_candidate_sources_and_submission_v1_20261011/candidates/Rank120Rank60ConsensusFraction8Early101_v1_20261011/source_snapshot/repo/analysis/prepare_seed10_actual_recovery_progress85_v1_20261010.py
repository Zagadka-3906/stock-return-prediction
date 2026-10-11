"""Show exact restart recovery separately from the administratively retired original helper."""
from pathlib import Path
import sys
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
from handoff_ready_goss_full_execution_20261006 import start_service,retire
def main():
    assert allowed();source=A/'monitor_fast_optimization_v84_20261010.py';text=source.read_text(encoding='utf8')
    aliases={'actual_stock_rank20seed10_embedding_small512_restart_v1_20261010':'actual_stock_rank20seed10_embedding_small512_restart_actual_fixture_v2_20261010',
        'actual_stock_rank20seed10_embedding_own64_controls46_queue_v1_20261010':'actual_stock_rank20seed10_embedding_own64_controls46_queue_v2_20261010'}
    text=text.replace('    while True:','    jobs += '+repr([*aliases.values(),'actual_StockRank20Seed10_remaining_main_v2_20261010'])+'\n    while True:',1)
    marker="        state={'at_local'";assert text.count(marker)==1
    prefix='        for original,actual in '+repr(aliases)+".items():\n            services[original]={**services.get(actual,{'status':'not_started'}),'actual_service_alias':actual,'original_service_status':original_services.get(original,{}).get('status'),'explicit_recovery_routing_not_original_terminal_status':True}\n"
    text=text.replace(marker,prefix+marker).replace('optimization_live_progress_v84','optimization_live_progress_v85').replace('actual_optimization_fast_runtime_handoff_v142','actual_optimization_fast_runtime_handoff_v143').replace('high_impact_additional_validation_rankings_v56','high_impact_additional_validation_rankings_v57')
    driver=A/'monitor_fast_optimization_v85_20261010.py';assert not driver.exists();compile(text,str(driver),'exec');driver.write_text(text,encoding='utf8',newline='\n')
    retire(read(A/'service_owned_workflows_20261006/actual_fast_optimization_progress_v84_20261010/native_launch.json'),'Verified idle observer replaced with truthful exact seed10 recovery2 states; no scientific worker terminated')
    assert allowed();row=start_service('actual_fast_optimization_progress_v85_20261010',driver.name,[],{str(driver):sha(driver)})
    create(A/'actual_fast_optimization_progress_v85_20261010_activation.json',row)
    print({'observer85':'started','new_scientific_completions_claimed':0},flush=True)
if __name__=='__main__':main()
