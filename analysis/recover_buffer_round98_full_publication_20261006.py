"""Complete full publication after retaining the actual large-JSON export failure."""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path[:0] = [str(ROOT), str(A)]
from run_dependency_queue_v3_20261006 import read, sha, create, owned
from hidden_windows_child_creation_20261006 import install
from handoff_joint_goss_round97_full_execution_20261006 import suspended_idle


def main():
    folder = A / 'optimization_20261003_r98'
    failure = read(folder / 'full_registration_failure.json')
    assert failure['error'].startswith('AssertionError: ') and failure['error'].endswith('selection.json')
    execution = read(A / 'service_owned_workflows_20261006/causal_entry_exit_buffer_round98_full_registration/service_execution.json')
    assert execution['status'] == 'failed'
    assert read(folder / 'provenance_scope_execution.json')['status'] == 'passed'
    qa = A / 'lossless_ranking_display_qa_v8_20261006/round98/verification.json'
    assert read(qa)['status'] == 'passed_all_original_full_ranking_QA_and_lossless_browser_node_checks'
    original_receipt = A / 'github_validation_sync_main_20261005/round98_receipt.json'
    assert read(original_receipt)['status'] == 'pushed_and_remote_head_verified'
    paths = [Path(__file__), A / 'publish_buffer_round98_full_validation_v2_20261006.py',
        folder / 'protocol.json', folder / 'selection.json', folder / 'provenance_scope_execution.json',
        folder / 'full_registration_failure.json', qa, original_receipt,
        ROOT / 'candidates/optimization_20261003_r98/manifest.json']
    pins = {str(p): sha(p) for p in paths}
    create(folder / 'frozen_before_full_publication_recovery_20261006.json', {
        'input_sha256': pins, 'original_scientific_inputs_scores_and_candidate_not_modified': True,
        'only_recovery_change': 'Losslessly gzip original JSON over review blob size cap; publish all full QA',
        'test_labels_read': False})
    publisher = read(A / 'service_owned_workflows_20261006/main_publisher_v7/native_launch.json')
    assert owned(publisher)
    suspended = []
    restore = install()
    try:
        parent, worker, idle = suspended_idle(publisher, '    main (watch_validations_main_v7_20261006.py:71)')
        suspended.extend((worker, parent))
        create(folder / 'actual_idle_publisher_full_recovery_20261006.json', idle)
        from publish_buffer_round98_full_validation_v2_20261006 import main as publish
        publish()
        for path, digest in pins.items():
            assert sha(path) == digest, path
        create(folder / 'publication_recovery_execution_v2_20261006.json', {
            'status': 'passed_full_immutable_board_QA8_and_all_original_execution_evidence_published',
            'input_sha256': pins, 'initial_registration_and_service_failure_preserved': True,
            'official16_metrics_frozen_selection_and_actual_candidate_byte_unchanged': True,
            'full_QA8_actual_already_passed_and_now_published': True,
            'compressed_large_selection_preserves_every_original_byte': True,
            'main_receipt': str(A / 'github_validation_sync_main_20261005/round98_complete_recovery_receipt_20261006.json'),
            'new_model_fits': 0, 'new_quality_scores': 0,
            'scientific_processes_suspended_or_restarted': 0, 'test_labels_read': False})
    finally:
        for process in reversed(suspended):
            if process.is_running():
                process.resume()
        create(folder / 'actual_hidden_full_publication_recovery_children_20261006.json', {'events': restore()})


if __name__ == '__main__':
    main()
