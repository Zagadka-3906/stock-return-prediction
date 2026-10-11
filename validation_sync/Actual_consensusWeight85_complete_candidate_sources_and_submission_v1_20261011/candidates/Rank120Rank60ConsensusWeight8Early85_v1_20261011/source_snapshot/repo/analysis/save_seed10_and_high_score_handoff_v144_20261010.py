"""Record actual progress and next priorities; no pending fit or validation is marked complete."""
from pathlib import Path
from datetime import datetime
import sys
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
def main():
    assert allowed()
    names=['actual_stock_rank20seed10_embedding_own64_controls46_queue_v1_20261010',
        'actual_stock_rank20seed10_embedding_small512_restart_v1_20261010',
        'actual_stock_rank20seed10_embedding_own64_controls46_queue_v2_20261010',
        'actual_stock_rank20seed10_embedding_small512_restart_actual_fixture_v2_20261010',
        'actual_StockRank20Seed10_objective_stages_main_v1_20261010',
        'actual_StockRank20Seed10_remaining_main_v2_20261010','actual_fast_optimization_progress_v85_20261010']
    services={}
    for n in names:
        f=A/'service_owned_workflows_20261006'/n
        services[n]={'execution':read(f/'service_execution.json') if (f/'service_execution.json').exists() else None,
            'owned':owned(read(f/'native_launch.json')),
            'administrative_record':read(f/'administrative_supersession_for_GOSS_20261006.json') if (f/'administrative_supersession_for_GOSS_20261006.json').exists() else None}
    pins=read(A/'stock_rank20seed10_embedding_own64_controls46_sources_admission_v1_20261010.json')['input_sha256']
    for p,d in pins.items():assert sha(p)==d,p
    assert sha(A.parent/'.git/index')=='ed2fa41598113343f7cf84c4ff16f7685c9ed3e079c16edf869c2c32019d3406'
    scores={}
    for parent in (174,175):
        p=Path(f'E:/赛题五_本机临时/StockRank20EmbeddingSmall512_after{parent}_tiny_CDF41_screen_v1_20261010/verification.json')
        data=read(p);assert data['new_quality_score_records']==41
        scores[str(parent)]={'verification_sha256':sha(p),'best':data['best'],'scored_cases':41,'submission_qualified':False}
    bank=Path('E:/赛题五_本机临时/stock_rank20seed10_embedding_small512_BF16_bank6_v1_20261010')
    data={'status':'actual_seed10_recovery2_queued_full_high_score_qualification_active_not_global_completion',
        'at_local':datetime.now().astimezone().isoformat(),'deadline_local':read(A/'current_user_runtime_control_20261010.json')['stop_at_local'],
        'best_fully_qualified':read(A/'latest_verified_submission_delivery_v2_20261008.json'),
        'actual_high_score_82':scores,'actual_main176':read(A/'github_validation_sync_main_20261005/round176_receipt.json'),
        'new_seed':20261010,'planned_own_fits':6,'completed_seed10_annual_models':sum((bank/str(y)/'info.json').exists() for y in range(2020,2026)),
        'services':services,'source_freeze_unchanged':True,'root_git_index_untouched':True,
        'actual_restart_waiting_memory_guard_at_last_stack':True,'no_GPU_training_completed_claimed':True,
        'publication_remaining_actual_recovery_service':'actual_StockRank20Seed10_remaining_main_v2_20261010',
        'observer':'monitor_fast_optimization_v85_20261010.py','test_labels_read':False,
        'next_priorities':['Finish strong 183 candidate qualification with broker7; do not rerun completed official82 scores',
            'Check actual seed10 restart2 and six annual fits, then full5/native42/17+29 and staged main receipts',
            'After seed10 full5, predeclare seed09/seed10 convex raw-signal ensemble comparisons with independent full and causal-prefix oracles; do not claim these unimplemented comparisons complete',
            'Freeze a complete pipeline for any improved seed10 or seed ensemble before actualfutureX, using exact native backend schemas and original failure records',
            'A 504-session Rank20 bank remains an unimplemented alternative; no fit/score/efficiency gain is claimed']}
    create(A/'actual_seed10_and_high_score_handoff_v144_20261010.json',data)
    print({'actual82_completed':True,'seed10_completed_models':data['completed_seed10_annual_models'],'goal_still_active':True},flush=True)
if __name__=='__main__':main()
