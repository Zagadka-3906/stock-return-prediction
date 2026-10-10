"""Record the user's actual Oct10 23:59 deadline without pausing the active goal."""
from pathlib import Path
from datetime import datetime, timezone, timedelta
import sys
ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path[:0] = [str(ROOT), str(A)]
from run_dependency_queue_v3_20261006 import read, sha, create


def main():
    local = timezone(timedelta(hours=8))
    now = datetime.now(local)
    deadline = datetime(2026, 10, 10, 23, 59, tzinfo=local)
    assert now < deadline
    full = A / 'optimization_20261003_r132/full_registration_execution.json'
    receipt = A / 'github_validation_sync_main_20261005/round132_receipt.json'
    assert read(full)['status'] == 'passed' and read(receipt)['status'] == 'pushed_and_remote_head_verified'
    controls = A / 'actual_GPU_resource_controls_main_v1_20261008/receipt.json'
    assert read(controls)['status'] == 'pushed_and_remote_head_verified'
    paths = [Path(__file__), full, receipt, controls,
             A / 'actual_SparseGram133_complete_dependency_plan_v1_20261008.json',
             A / 'actual_neural_BF16_micro8192_bank6_v2_20261008_hidden_launch.json']
    create(A / 'actual_user_submission_deadline_and_priority_20261008.json', {
        'status': 'actual_user_deadline_recorded_active_optimization_continues',
        'user_answer': '10号晚上11:59', 'deadline_local': deadline.isoformat(),
        'timezone': 'UTC+08:00', 'recorded_at_local': now.isoformat(timespec='seconds'),
        'remaining_hours_at_record': (deadline - now).total_seconds() / 3600,
        'input_sha256': {str(p): sha(p) for p in paths},
        'current_fully_qualified_round': 132, 'current_fully_qualified_score': read(receipt)['official_score'],
        'priority': ['finish_active_BF16_own_full_annual_bank_and_complete_quality_validation',
                     'finish_admitted_sparse_Gram133_full40_round',
                     'refine_promising_negative_Bayes_weights_using_training_only',
                     'admit_extra_long_training_only_if_measured_runtime_fits_remaining_budget',
                     'reserve_final_candidate_integrity_inference_scoring_and_main_delivery_time'],
        'goal_not_marked_paused_or_complete': True,
        'new_model_or_submission_quality_not_inferred_from_training_speed': True,
        'old_20261007_shutdown_schedule_not_restarted': True,
        'real_test_labels_never_used': True, 'no_new_quality_scores_by_this_record': True,
        'final_external_competition_submission_not_claimed': True})
    print('Actual user deadline recorded, remaining hours:', (deadline - now).total_seconds() / 3600)


if __name__ == '__main__': main()
