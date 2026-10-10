"""Close only the failed publication; preserve already passed full101 scientific QA."""
from pathlib import Path
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path[:0] = [str(ROOT), str(A)]
from run_dependency_queue_v3_20261006 import read, create, sha, owned


def main():
    failed = A / 'service_owned_workflows_20261006/conditional_flag_round101_full_registration_v3'
    assert not owned(read(failed / 'native_launch.json'))
    assert read(failed / 'service_execution.json')['status'] == 'failed'
    preceding = A / 'service_owned_workflows_20261006/conditional_residual_scores_evidence_publication_v2'
    identity = read(preceding / 'native_launch.json')
    while owned(identity):
        time.sleep(30)
    assert read(preceding / 'service_execution.json')['status'] == 'passed'
    folder = A / 'optimization_20261003_r101'
    assert read(folder / 'provenance_scope_execution.json')['status'] == 'passed'
    assert read(A / 'lossless_ranking_display_qa_v12_20261006/round101/verification.json')['status'] == 'passed_original_full_ranking_QA_on_lossless_page'
    assert not (A / 'github_validation_sync_main_20261005/round101_receipt.json').exists()
    pins = {str(p): sha(p) for p in (Path(__file__), A / 'publish_conditional_flag_round101_full_validation_v4_20261006.py',
        folder / 'provenance_scope_execution.json', folder / 'full_registration_failure_v3.json',
        A / 'lossless_ranking_display_qa_v12_20261006/round101/verification.json')}
    create(folder / 'frozen_before_actual_main_publication_v4.json', {
        'input_sha256': pins, 'at_local': time.strftime('%Y-%m-%dT%H:%M:%S'),
        'actual37_scientific_registry_and_all_full_QA_already_passed': True,
        'only_snapshot_number_corrected100_to101': True,
        'three_original_failed_registry_or_publication_attempts_preserved': True,
        'new_training_scoring_inference_or_QA_claimed': False, 'test_labels_read': False})
    from hidden_windows_child_creation_20261006 import install
    from handoff_joint_goss_round97_full_execution_20261006 import suspended_idle
    restore = install()
    held = []
    try:
        publisher = read(A / 'service_owned_workflows_20261006/main_publisher_v7/native_launch.json')
        parent, worker, idle = suspended_idle(publisher, '    main (watch_validations_main_v7_20261006.py:71)')
        held.extend((worker, parent))
        create(folder / 'actual_main7_idle_before_and_after_publication_v4_hold.json', idle)
        for path, digest in pins.items():
            assert sha(path) == digest
        from publish_conditional_flag_round101_full_validation_v4_20261006 import main as publish
        publish()
        create(folder / 'full_registration_execution.json', {'status': 'passed',
            'at_local': time.strftime('%Y-%m-%dT%H:%M:%S'), 'existing_official_scores_registered': 37,
            'full_rankings_all_original_QA_and_main_publication_completed': True,
            'scientific_processes_suspended_or_restarted': 0, 'new_quality_scores_by_registration': 0,
            'original_three_registry_and_publication_failures_preserved': True,
            'global_goal_or_resource_exhaustion_claimed': False, 'test_labels_read': False})
    except BaseException as error:
        create(folder / 'publication_failure_v4.json', {'status': 'failed_preserved_round101_main_closure',
            'error': f'{type(error).__name__}: {error}'})
        raise
    finally:
        for process in reversed(held):
            if process.is_running():
                process.resume()
        create(folder / 'actual_hidden_publication_v4_children.json', {'events': restore()})


if __name__ == '__main__':
    main()
