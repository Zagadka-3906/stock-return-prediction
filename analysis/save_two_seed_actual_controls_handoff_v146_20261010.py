"""Save completed own6/full5 evidence and honest pending ensemble/native/official/main stages."""
from pathlib import Path
from datetime import datetime
import sys
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
def main():
    assert allowed()
    bank=Path('E:/赛题五_本机临时/stock_rank20seed10_embedding_small512_BF16_bank6_v1_20261010')
    full=Path(read(A/'actual_StockRank20Seed10EmbeddingSmall512_full5_independent_location_v1_20261009.json')['output'])
    assert read(bank/'verification.json')['actual_native_fits']==6
    assert read(full/'verification.json')['rows_days_stocks']==[5635800,1212,4650]
    weights=A/'rank20_two_seed_actual_six_population_and_weights_CPU_v1_20261010.json'
    assert read(weights)['status'].startswith('passed_actual6_')
    names=['actual_stock_rank20seed10_embedding_own64_controls46_queue_v2_20261010',
        'actual_stock_rank20seed10_embedding_small512_bank6_v1_20261010',
        'StockRank20Seed10EmbeddingSmall512_independent_full5_GPU_controls_v1_20261009',
        'actual_stock_rank20seed10_embedding_six_state_native42_v1_20261010',
        'actual_stock_rank20seed10_embedding_after175_fast17_screen_v1_20261010',
        'actual_stock_rank20seed10_embedding_after175_large_allocation29_screen_v1_20261010',
        'actual_rank20_two_seed_after175_complement49_screen_v1_20261010','actual_rank20_two_seed_native84_v1_20261010',
        'actual_Rank20_two_seed_stages_main_v1_20261010','actual_Rank20_two_seed_native84_stages_main_v2_20261010',
        'actual_StockRank20Seed10_remaining_main_v2_20261010','StockRank5Embedding177_round177_full_registration_v1_20261010']
    services={}
    for name in names:
        folder=A/'service_owned_workflows_20261006'/name
        services[name]={'execution':read(folder/'service_execution.json') if (folder/'service_execution.json').exists() else None,
            'owned_now':owned(read(folder/'native_launch.json')) if (folder/'native_launch.json').exists() else False,
            'native_launch_exists':(folder/'native_launch.json').exists()}
    scores={}
    for family in ('StockRank20Seed10EmbeddingSmall512_after175_high_impact17_screen_v1_20261010','StockRank20Seed10EmbeddingSmall512_after175_large_allocation29_screen_v1_20261010','StockRank20TwoSeed_after175_complement49_screen_v1_20261010'):
        folder=bank.parent/family
        scores[family]={'official_json_files':len(list(folder.glob('case*_official.json'))),'best_so_far':read(folder/'best_so_far.json') if (folder/'best_so_far.json').exists() else None,'verification_exists':(folder/'verification.json').exists()}
    assert sha(A.parent/'.git/index')=='ed2fa41598113343f7cf84c4ff16f7685c9ed3e079c16edf869c2c32019d3406'
    sources=[Path(__file__),weights,A/'verify_rank20_two_seed_actual_six_population_and_weights_CPU_v1_20261010.py',
        A/'rank20_two_seed_raw_signal_v1_20261010.py',A/'rank20_two_seed_raw_signal_actual_CPU_controls_v1_20261010.json',
        A/'prepare_rank20_two_seed_complement49_v1_20261010.py',A/'rank20_two_seed_complement49_predeclared_plan_v1_20261010.json',
        A/'run_rank20_two_seed_after175_complement49_screen_v1_20261010.py',A/'rank20_two_seed_after_qualified_parent_native_stage_v1_20261010.py',
        A/'verify_rank20_two_seed_six_pair_states_native84_v1_20261010.py',A/'publish_rank20_two_seed_stages_main_v1_20261010.py',
        A/'prepare_rank20_two_seed_native84_main_v2_20261010.py',A/'monitor_fast_optimization_v86_20261010.py',
        bank/'verification.json',full/'verification.json']
    create(A/'actual_two_seed_own6_full5_controls_and49_native84_handoff_v146_20261010.json',{
        'status':'actual_new_seed_own6_full5_and_six_tensor_population_controls_passed_95_scores_and_future_qualification_pending',
        'at_local':datetime.now().astimezone().isoformat(),'deadline_local':read(A/'current_user_runtime_control_20261010.json')['stop_at_local'],
        'input_sha256':{str(p):sha(p) for p in sources},'services':services,'actual_scores':scores,
        'best_fully_qualified':read(A/'latest_verified_submission_delivery_v2_20261008.json'),
        'root_git_index_untouched':True,'planned_new_two_seed_records':49,'planned_native84_and_cold84':True,
        'original_main177_QA_finished_push_live_at_last_verified_stack':True,
        'next_priorities':['Inspect exact live main177 push; preserve completed full QA and never re-run it merely for a transport retry',
            'Inspect actual seed10 native42/17+29, actual two-seed official49/native84 and stage-specific main receipts',
            'Sync six-population/distinct-tensor CPU proof and its source to main; not yet included in the earlier source snapshot',
            'Once actual scores identify the best candidate, build the next complete registry and future pipeline using exact backend APIs; no untested source clones',
            'Continue strong pending 183 candidate qualification with broker7 and actual184185 with broker9'],
        'new_ensemble_training':0,'actual_future_X_read_by_this_turn':False,'test_labels_read':False,
        'global_optimization_or_resource_exhaustion_not_proven':True})
    print({'own6_and_full5_verified':True,'six_actual_tensor_pairs_verified':True,'goal_still_active':True},flush=True)
if __name__=='__main__':main()
