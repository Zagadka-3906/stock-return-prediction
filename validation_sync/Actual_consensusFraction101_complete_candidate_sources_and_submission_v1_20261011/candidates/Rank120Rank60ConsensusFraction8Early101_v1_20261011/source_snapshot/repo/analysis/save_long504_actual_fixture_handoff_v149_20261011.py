"""Preserve actual long504 controls and exact live queues without claiming pending scores or training."""
from pathlib import Path
from datetime import datetime
import sys
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
def main():
    assert allowed()
    pointer=A/'actual_stock_rank20long_embedding_mature_fixture_location_v1_20261010.json'
    fixture=Path(read(pointer)['output']);proof=read(fixture/'verification.json')
    assert proof['rows']==49153 and proof['full_mature_days']==466 and proof['configuration']['training_calendar_window']==504
    seed17=Path('E:/赛题五_本机临时/StockRank20Seed10EmbeddingSmall512_after175_high_impact17_screen_v1_20261010/verification.json')
    assert read(seed17)['new_quality_score_records']==17
    sources=[Path(__file__),pointer,fixture/'verification.json',A/'prepare_recent504_rank20_population_CPU_v1_20261011.py',
        A/'recent504_rank20_mature_training_population_v1_20261011.py',A/'recent504_rank20_mature_population_actual_CPU_controls_v1_20261011.json',
        A/'prepare_stock_rank20long_504_own64_controls46_v1_20261011.py',A/'stock_rank20long_embedding_own64_native_sources_preparation_v1_20261010.json',
        A/'verify_stock_rank20long_embedding_actual_mature_fixture_v1_20261010.py',A/'run_stock_rank20long_embedding_504_own64_controls46_queue_v1_20261011.py',
        A/'prepare_rank20long_504_staged_main_v1_20261011.py',A/'publish_stock_rank20long_objective_stages_main_v1_20261011.py',
        A/'monitor_fast_optimization_v87_20261011.py',seed17]
    states={}
    for name in ['StockRank20LongEmbedding_actual_mature_fixture_CPU_v1_20261010','actual_stock_rank20long_embedding_504_own64_controls46_queue_v1_20261011',
        'actual_stock_rank20seed10_embedding_after175_large_allocation29_screen_v1_20261010','actual_rank20_two_seed_after175_complement49_screen_v1_20261010',
        'actual_rank20_two_seed_native84_v1_20261010','actual_StockRank20Long_504_objective_stages_main_v1_20261011']:
        folder=A/'service_owned_workflows_20261006'/name
        states[name]={'execution':read(folder/'service_execution.json') if (folder/'service_execution.json').exists() else None,
            'owned_now':owned(read(folder/'native_launch.json')) if (folder/'native_launch.json').exists() else False}
    proposal=A/'recover_long504_fixture_bounded_RAM_v2_20261011.py'
    assert not (A/'long504_fixture_bounded_RAM_actual_source_and_idle_controls_v2_20261011.json').exists()
    assert not (A/'verify_stock_rank20long_embedding_actual_mature_fixture_bounded_RAM_v2_20261011.py').exists()
    assert sha(A.parent/'.git/index')=='ed2fa41598113343f7cf84c4ff16f7685c9ed3e079c16edf869c2c32019d3406'
    create(A/'actual_long504_fixture_CPU7_and_pending46_handoff_v149_20261011.json',{
        'status':'actual_long504_CPU7_and_real49153_fixture_passed_own_training_pending',
        'at_local':datetime.now().astimezone().isoformat(),'deadline_local':read(A/'current_user_runtime_control_20261010.json')['stop_at_local'],
        'input_sha256':{str(p):sha(p) for p in sources},'actual_new_fixture':{'rows':49153,'mature_days':466,'training_calendar_window':504},
        'actual_seed10_17_best':read(seed17)['best'],'services':states,
        'tensor_CPU_actual_main_receipt':read(A/'Rank20_two_seed_actual_weights_CPU_main_receipt_v3_20261010.json'),
        'best_fully_qualified':read(A/'latest_verified_submission_delivery_v2_20261008.json'),
        'unused_memory_guard_proposal':{'path':str(proposal),'sha256':sha(proposal),'not_applied':True,'reason':'Original fixture completed successfully before idle verification; proposal safely stopped on NoSuchProcess before any mutation or retirement','do_not_execute_again':True},
        'new_long504_fits_completed':0,'new_long504_quality_scores':0,'observer':'monitor_fast_optimization_v87_20261011.py',
        'root_git_index_untouched':True,'actual_future_X_read':False,'test_labels_read':False,
        'next_priorities':['Follow exact live seed10 remaining29, two-seed49/native84; do not rerun completed seed17/own6/full5',
            'Follow original long504 queue1 after actual native84; genuine new restart/own6/full5/native42/46 remain pending',
            'Continue full178-185 with existing broker7/broker9; strongest183 qualified candidate remains priority',
            'Register new seed46, two-seed49 and long50446 in new complete rankings with highest-S qualification; build exact backend schemas before future dispatch',
            'Do not apply unused RAM recovery proposal: original source fixture already passed'],
        'global_optimization_or_resource_exhaustion_not_proven':True})
    print({'actual_long504_real_fixture_passed':True,'unused_guard_proposal_not_applied':True,'goal_still_active':True},flush=True)
if __name__=='__main__':main()
