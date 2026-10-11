"""Include the actual fast170 screen without duplicating observers or missing handoff paths."""
from pathlib import Path
import sys,time
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from handoff_ready_goss_full_execution_20261006 import start_service,retire
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
def main():
    assert allowed();old=A/'monitor_fast_optimization_v46_20261010.py';text=old.read_text(encoding='utf8')
    text=text.replace("jobs=['actual_stock_embedding_six_state_native42_v2_20261010'","jobs=['actual_stock_embedding_after170_fast17_screen_v1_20261010','actual_stock_embedding_after170_fast17_completion_main_v51_20261010','actual_stock_embedding_six_state_native42_completion_main_v50_20261010','actual_stock_embedding_GPU_restart_and_checkpoint_yield_main_v34_20261010','actual_stock_embedding_six_state_native42_v2_20261010'")
    text=text.replace("families=['StockEmbeddingSmall512_after172", "families=['StockEmbeddingSmall512_after170_high_impact17_screen_v1_20261010','StockEmbeddingSmall512_after172")
    text=text.replace("('StockEmbeddingSmall512_after172_high_impact17_screen_v1_20261010',17)","('StockEmbeddingSmall512_after172_high_impact17_screen_v1_20261010',17),('StockEmbeddingSmall512_after170_high_impact17_screen_v1_20261010',17)")
    text=text.replace('optimization_live_progress_v46','optimization_live_progress_v47').replace('actual_optimization_fast_runtime_handoff_v75','actual_optimization_fast_runtime_handoff_v77').replace('high_impact_additional_validation_rankings_v17','high_impact_additional_validation_rankings_v18')
    source=A/'monitor_fast_optimization_v47_20261010.py';assert not source.exists();compile(text,str(source),'exec');source.write_text(text,encoding='utf8',newline='\n')
    row=start_service('actual_fast_optimization_progress_v47_20261010',source.name,[],{str(source):sha(source)})
    create(A/'actual_fast_optimization_progress_v47_activation_20261010.json',row)
    while not (A/'optimization_live_progress_v47_20261010.json').exists():assert allowed();time.sleep(.5)
    current=read(A/'optimization_live_progress_v47_20261010.json');assert 'actual_stock_embedding_after170_fast17_screen_v1_20261010' in current['services']
    retired=read(A/'service_owned_workflows_20261006/actual_fast_optimization_progress_v46_20261010/native_launch.json');retire(retired,'Observer47 includes actual fast17017 and pending17217; actual current output verified, preserving all scientific jobs.')
    create(A/'observer46_retired_after_actual47_verified_v1_20261010.json',{'status':'administratively_retired_childless_observer46_only','successor':row,'retired':retired,'scientific_jobs_terminated':0})
    handoff=read(A/'actual_optimization_fast_runtime_handoff_v74_20261010.json')
    handoff.update(status='active_own_six_stock_embedding_fits_and_full5_complete_native42_actual_then_fast17017_plus_existing171172',actual_live_progress=str(A/'optimization_live_progress_v47_20261010.json'),stock_fast17017_actual_service='actual_stock_embedding_after170_fast17_screen_v1_20261010',stock_fast17017_expected_main_service='actual_stock_embedding_after170_fast17_completion_main_v51_20261010',stock_own_six_fits_completed=True,stock_own_full5_independent_completed=True,stock_six_fit_bank_location=str(A/'actual_stock_embedding_small512_bank6_location_v1_20261010.json'),stock_own_full5_pointer=str(A/'actual_StockEmbeddingSmall512_full5_independent_location_v1_20261009.json'),stock_native42_completion_pending=True,stock_fast17017_scoring_pending=True,stock_actual_GPU_main_receipt=read(A/'stock_embedding_actual_GPU_restart_and_checkpoint_yield_preparation_main_receipt_v34_20261010.json'),latest_training_only_return81_score=.45134504575777823,latest_training_only_return81_submission_qualification_pending=True,stock_full_candidate173_flow='not_created_pending_selected_comparison_and_full173_sources')
    create(A/'actual_optimization_fast_runtime_handoff_v76_20261010.json',handoff)
    print({'actual_observer':row['owned_worker_pid'],'stock_six_fit_and_independent_full5':'passed','native42_and_fast17':'running_or_queued'},flush=True)
if __name__=='__main__':main()
