"""Publish preserved actual40/QA42 after manual resume, without repeating science."""
from pathlib import Path
import sys
import time
ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path[:0] = [str(ROOT), str(A)]
from run_dependency_queue_v3_20261006 import read, sha, create
from file_backed_hidden_git_runtime_20261007 import installed
from hidden_windows_child_creation_20261006 import install


def main():
    folder = A / 'optimization_20261003_r131'
    out = A / 'round131_preserved_QA42_main_recovery_v3_20261008'
    assert not out.exists()
    assert not (folder / 'full_registration_execution.json').exists()
    assert not (A / 'github_validation_sync_main_20261005/round131_receipt.json').exists()
    assert read(folder / 'provenance_scope_execution.json')['status'] == 'passed'
    qa = A / 'lossless_ranking_display_qa_v42_20261007/round131/verification.json'
    q = read(qa)
    assert q['status'] == 'passed_all_original_full_ranking_QA_and_lossless_browser_node_checks'
    assert q['original_full_QA_result']['connected_records'] == 13498
    assert q['original_full_QA_result']['new_round_records'] == 40
    frozen = read(folder / 'frozen_before_actual_full_registration.json')
    extra = [Path(__file__), A / 'publish_nonflag_RidgeMicro40_round131_full_validation_v3_20261008.py',
        A / 'prepare_actual_manual_resume_and_round131_publication_v3_20261008.py',
        A / 'actual_manual_resume_after_shutdown_20261008.json', qa,
        folder / 'provenance_scope_execution.json', folder / 'full_registration_failure.json']
    pins = {**frozen['input_sha256'], **{str(p): sha(p) for p in extra}}
    out.mkdir()
    create(out / 'frozen_before_actual_publication_recovery.json', {
        'status': 'frozen_administrative_receiver_for_original_QA42_and_scientific_freeze',
        'input_sha256': pins, 'prior_failure_preserved': str(folder / 'full_registration_failure.json'),
        'new_quality_scores': 0, 'new_candidate_inference': 0, 'test_labels_read': False})
    restore = install()
    lock = None
    try:
        import publish_classifier_consensus_workflows_20261006 as helpers
        with installed(out / 'file_backed_git'):
            helpers.verify_main(helpers.sync.git('rev-parse', 'HEAD'))
            assert not helpers.sync.git('status', '--porcelain')
            assert not helpers.sync.git('diff', '--cached', '--name-only', cwd=ROOT)
            lock = helpers.sync.initialize()
            from win32_read_handle_hash_cache_with_filename_v2_20261006 import LockedReadHashCache
            with LockedReadHashCache(pins) as scope:
                from publish_nonflag_RidgeMicro40_round131_full_validation_v3_20261008 import main as publish
                publish()
                scope.reverify()
                receipt = read(A / 'github_validation_sync_main_20261005/round131_receipt.json')
                assert receipt['status'] == 'pushed_and_remote_head_verified'
                assert receipt['scored_records'] == 40 and receipt['actual_full_QA_version'] == 42
                create(out / 'actual_preserved_source_reverification.json', {
                    'status': 'passed_original_all10532_source_pins_and_fresh_recovery_bytes',
                    'input_sha256': pins, 'source_count': len(pins), 'initial_and_final_full_hashes': True,
                    'read_only_shared_handles_held_through_publication': True,
                    'original_scoring_candidate_and_QA_sources_not_rewritten': True,
                    'new_native_fits': 0, 'new_quality_scores': 0, 'new_candidate_inference': 0})
            create(folder / 'full_registration_execution.json', {
                'status': 'passed', 'at_local': time.strftime('%Y-%m-%dT%H:%M:%S'),
                'existing_official_scores_registered': 40,
                'full_rankings_all_original_QA_and_main_publication_completed': True,
                'actual_preserved_QA42_result': str(qa),
                'administrative_main_publication_recovered_after_preserved_V2_failure': True,
                'source_reverification': str(out / 'actual_preserved_source_reverification.json'),
                'new_quality_scores_by_registration': 0, 'new_inference_claimed_by_registration': False,
                'selected_candidate_actual_new_inference': True,
                'global_goal_or_resource_exhaustion_claimed': False, 'test_labels_read': False})
            print('PASS actual40/QA42/main round131 closeout; new quality scores=0', flush=True)
    finally:
        if lock is not None and lock.exists() and read(lock).get('pid') == __import__('os').getpid():
            lock.unlink()
        create(out / 'actual_hidden_children.json', {'events': restore()})


if __name__ == '__main__':
    main()
