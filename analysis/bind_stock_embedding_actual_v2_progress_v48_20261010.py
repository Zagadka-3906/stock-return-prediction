"""Current actual score attempts and stable user-facing progress pointers."""
from pathlib import Path
import sys,time
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from handoff_ready_goss_full_execution_20261006 import start_service,retire
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
from scheduled_user_pause_20261007 import write
def main():
    assert allowed();old=A/'monitor_fast_optimization_v47_20261010.py';text=old.read_text(encoding='utf8')
    for before,after in [('actual_stock_embedding_after170_fast17_screen_v1_20261010','actual_stock_embedding_after170_fast17_screen_v2_20261010'),('actual_stock_embedding_after172_high_impact17_screen_v1_20261010','actual_stock_embedding_after172_high_impact17_screen_v2_20261010'),('actual_stock_embedding_after170_fast17_completion_main_v51_20261010','actual_stock_embedding_after170_completion_main_v53_20261010'),('actual_stock_embedding17_completion_main_v49_20261010','actual_stock_embedding_after172_completion_main_v52_20261010')]:text=text.replace(before,after)
    text=text.replace('optimization_live_progress_v47','optimization_live_progress_v48').replace('actual_optimization_fast_runtime_handoff_v77','actual_optimization_fast_runtime_handoff_v79').replace('high_impact_additional_validation_rankings_v18','high_impact_additional_validation_rankings_v20')
    text=text.replace("tmp.replace(p)\n        if now", "tmp.replace(p)\n        stable=A/'optimization_live_progress_current_20261010.md';stabletmp=stable.with_suffix('.tmp');stabletmp.write_text(p.read_text(encoding='utf8'),encoding='utf8');stabletmp.replace(stable)\n        if now")
    source=A/'monitor_fast_optimization_v48_20261010.py';assert not source.exists();compile(text,str(source),'exec');source.write_text(text,encoding='utf8',newline='\n')
    row=start_service('actual_fast_optimization_progress_v48_20261010',source.name,[],{str(source):sha(source)})
    create(A/'actual_fast_optimization_progress_v48_activation_20261010.json',row)
    while not (A/'optimization_live_progress_v48_20261010.json').exists():assert allowed();time.sleep(.5)
    actual=read(A/'optimization_live_progress_v48_20261010.json');assert 'actual_stock_embedding_after170_fast17_screen_v2_20261010' in actual['services']
    prior=read(A/'service_owned_workflows_20261006/actual_fast_optimization_progress_v47_20261010/native_launch.json');retire(prior,'Observer48 bound to actual v2 scientific score attempts and publishers53/52, stable user-facing Markdown; all scientific tasks preserved.')
    create(A/'observer47_retired_after_actual48_verified_v1_20261010.json',{'status':'administratively_retired_only_childless_observer47','retired':prior,'successor':row,'scientific_tasks_terminated':0})
    handoff=read(A/'actual_optimization_fast_runtime_handoff_v76_20261010.json')
    handoff.update(status='active_stock_native42_passed_main_published_and_actual_fast17017_official_scoring_started_baseline_all8_exact',actual_live_progress=str(A/'optimization_live_progress_v48_20261010.json'),stock_fast17017_actual_service='actual_stock_embedding_after170_fast17_screen_v2_20261010',stock_fast17017_expected_main_service='actual_stock_embedding_after170_completion_main_v53_20261010',stock17217_actual_service='actual_stock_embedding_after172_high_impact17_screen_v2_20261010',stock17217_expected_main_service='actual_stock_embedding_after172_completion_main_v52_20261010',stock_native42_completion_pending=False,stock_native42_main_receipt=read(A/'stock_embedding_actual_six_state_native42_completion_main_receipt_v50_20261010.json'),stock_fast17017_all8_anchor_metrics_exact=True,actual_prototype_route_recovery=str(A/'stock_embedding_score_original_fixture169_and_actual170172_baseline_route_recovery_v2_20261010.json'),remaining_work='Complete fast stock17 and later172 stock17 comparison; prepare36-record normalized selected scheme and14 exact saved-state controls then full173 freeze/two future/cold80/QA84/main. Existing171/172 remain active and ordered; do not register173 ahead of them.')
    create(A/'actual_optimization_fast_runtime_handoff_v78_20261010.json',handoff)
    write(A/'optimization_live_progress_current_location_20261010.json',{'actual_live_progress_json':str(A/'optimization_live_progress_v48_20261010.json'),'actual_live_progress_md':str(A/'optimization_live_progress_current_20261010.md'),'actual_runtime_handoff':str(A/'actual_optimization_fast_runtime_handoff_v78_20261010.json'),'actual_scientific_attempts':{'stock17017':'actual_stock_embedding_after170_fast17_screen_v2_20261010','stock17217':'actual_stock_embedding_after172_high_impact17_screen_v2_20261010'},'deadline_local':actual['deadline_local']})
    print('Observer48 actual stockv2 bindings and stable progress pointer verified; baseline170 exact official scoring active',flush=True)
if __name__=='__main__':main()
