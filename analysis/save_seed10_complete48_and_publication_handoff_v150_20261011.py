"""Record partial48 admission, actual11 callback checks and publication-only recovery without fake completion."""
from pathlib import Path
from datetime import datetime
import sys
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
def main():
    assert allowed()
    admission=A/'seed10_complete48_normalization_native14_sources_admission_v1_20261011.json'
    data=read(admission);assert data['complete186_future_pipeline_pending']
    for p,d in data['input_sha256'].items():assert sha(p)==d,p
    names=['actual_stock_rank20seed10_embedding48_after185_normalization_queue_v1_20261011','StockRank20Seed10Embedding48_selected_native14_v1_20261011',
        'actual_Seed10_complete48_sources_main_v1_20261011','actual_Seed10_complete48_source_capsules_main_v2_20261011',
        'actual_stock_rank20seed10_embedding_after175_large_allocation29_screen_v1_20261010','actual_rank20_two_seed_native84_v1_20261010',
        'actual_rank20_two_seed_after175_complement49_screen_v1_20261010','actual_stock_rank20long_embedding_504_own64_controls46_queue_v1_20261011',
        'actual_fast_optimization_progress_v88_20261011']
    states={}
    for name in names:
        f=A/'service_owned_workflows_20261006'/name
        states[name]={'execution':read(f/'service_execution.json') if (f/'service_execution.json').exists() else None,
            'owned_now':owned(read(f/'native_launch.json')) if (f/'native_launch.json').exists() else False}
    assert states['actual_Seed10_complete48_sources_main_v1_20261011']['execution']['status']=='failed'
    assert sha(A.parent/'.git/index')=='ed2fa41598113343f7cf84c4ff16f7685c9ed3e079c16edf869c2c32019d3406'
    source_receipt=A/'Seed10_complete48_sources_main_receipt_v1_20261011.json'
    large=Path('E:/赛题五_本机临时/StockRank20Seed10EmbeddingSmall512_after175_large_allocation29_screen_v1_20261010')
    create(A/'actual_seed10_complete48_callback11_and_publication_recovery_handoff_v150_20261011.json',{
        'status':'compiled48_normalization_native14_and_actual11_callbacks_passed_complete186_pipeline_pending',
        'at_local':datetime.now().astimezone().isoformat(),'deadline_local':read(A/'current_user_runtime_control_20261010.json')['stop_at_local'],
        'input_sha256':{str(p):sha(p) for p in [Path(__file__),admission,A/'prepare_seed10_complete48_normalization_and_native14_v1_20261011.py',
            A/'stock_rank20seed10_embedding_actual_eleven_parent_callbacks_CPU_controls_v1_20261011.json',
            A/'seed10_source_capsules_case_collision_recovery_v2_20261011.json',A/'recover_seed10_source_capsules_case_collision_v2_20261011.py',
            A/'publish_seed10_complete48_source_capsules_main_v2_20261011.py',A/'monitor_fast_optimization_v88_20261011.py']},
        'services':states,'source_main_receipt':read(source_receipt) if source_receipt.exists() else None,
        'actual_seed10_large29_best':read(large/'best_so_far.json') if (large/'best_so_far.json').exists() else None,
        'best_fully_qualified':read(A/'latest_verified_submission_delivery_v2_20261008.json'),
        'root_git_index_untouched':True,'scientific_workers_restarted_for_publication_collision':0,
        'observer87_initial_active_snapshot_safely_refused_then_exact_idle_adoption':True,
        'complete186_candidate_storage_sealing_cache_registry_QA97_main_pipeline_not_created':True,
        'actual_future_X_read':False,'test_labels_read':False,'new_quality_scores_by_source_admission':0,
        'next_priorities':['Finish actual seed10 large29, actual two-seed49/native84 and long504 own6/full5/native42/46 without replaying completed science',
            'Construct complete186 future/storage/seal/cache/registry/QA97/main pipeline from verified current templates; existing48 normalizer and native14 qualifier already exist and must not be overwritten',
            'Use anchors175/185 and keep new-stage base175; predictor supports complete175 callbacks,185 is whole anchor reuse only',
            'Use exact namespace stems and independently check backend recipes/configurations before future dispatch; avoid Windows filename pairs differing only by case',
            'Publish and register seed46/two-seed49/long50446 with actual controls and complete ranking updates',
            'Continue strongest183 qualification through original178-185 broker7/broker9; do not rerun raw failures or idle recovered helpers'],
        'global_optimization_or_resource_exhaustion_not_proven':True})
    print({'actual_callback_CPU_checks':11,'full186_pipeline_still_pending':True,'goal_active':True},flush=True)
if __name__=='__main__':main()
