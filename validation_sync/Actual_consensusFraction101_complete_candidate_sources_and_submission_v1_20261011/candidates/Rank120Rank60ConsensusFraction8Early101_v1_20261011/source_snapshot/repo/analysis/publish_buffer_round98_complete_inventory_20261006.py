"""Publish the complete candidate inventory and all actual unchanged full QA evidence."""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path.insert(0, str(A))
from run_dependency_queue_v3_20261006 import read, sha, create
from hidden_windows_child_creation_20261006 import install
from handoff_joint_goss_round97_full_execution_20261006 import suspended_idle


def main():
    qa = A / 'lossless_ranking_display_qa_v9_20261006/round98/verification.json'
    assert read(qa)['additional_complete_candidate_inventory']['status'] == 'passed'
    assert read(qa)['additional_complete_candidate_inventory']['actual_candidate_files'] == 2012
    original = read(A / 'optimization_20261003_r98/publication_recovery_execution_v2_20261006.json')
    assert original['status'] == 'passed_full_immutable_board_QA8_and_all_original_execution_evidence_published'
    publisher = read(A / 'service_owned_workflows_20261006/main_publisher_v7/native_launch.json')
    suspended = []
    restore = install()
    try:
        parent, worker, idle = suspended_idle(publisher, '    main (watch_validations_main_v7_20261006.py:71)')
        suspended.extend((worker, parent))
        from publish_buffer_round98_full_validation_v3_20261006 import main as publish
        publish()
        create(A / 'optimization_20261003_r98/complete_inventory_publication_execution_20261006.json', {
            'status': 'passed_full16_official_candidate_causal_provenance_ranking_and_complete_inventory_publication',
            'full_candidate_files': 2012, 'actual_full_UI_QA8_source_sha256': read(qa)['original_actual_full_QA8_sha256'],
            'complete_inventory_QA9_sha256': sha(qa),
            'candidate_files_not_modified': True, 'all_prior_failures_and_manifests_retained': True,
            'main_receipt': str(A / 'github_validation_sync_main_20261005/round98_complete_inventory_receipt_20261006.json'),
            'idle_publisher_before_and_after_hold': idle,
            'new_model_fits': 0, 'new_quality_scores': 0,
            'scientific_processes_suspended_or_restarted': 0, 'test_labels_read': False})
    finally:
        for process in reversed(suspended):
            if process.is_running():
                process.resume()
        create(A / 'optimization_20261003_r98/complete_inventory_hidden_publication_children_20261006.json', {'events': restore()})


if __name__ == '__main__':
    main()
