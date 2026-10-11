"""Upgrade the actual automatic101 receipt with complete immutable QA and failures."""
from pathlib import Path
import json
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path[:0] = [str(ROOT), str(A)]
from run_dependency_queue_v3_20261006 import read, sha, create, owned
from atomic_optimization_observer_writes_20261005 import write

OUT = A / 'conditional_flag_round101_publication_recovery_v6_20261006'


def main():
    assert not OUT.exists()
    OUT.mkdir()
    receipt = A / 'github_validation_sync_main_20261005/round101_receipt.json'
    original_bytes = receipt.read_bytes()
    previous = read(receipt)
    assert previous['status'] == 'pushed_and_remote_head_verified' and previous['round'] == 101
    assert previous['branch'] == 'main' and previous['scored_records'] == 37
    (OUT / 'previous_automatic_round101_receipt.json').write_bytes(original_bytes)
    folder = A / 'optimization_20261003_r101'
    qa = A / 'lossless_ranking_display_qa_v12_20261006/round101/verification.json'
    proof = read(qa)
    assert proof['status'] == 'passed_all_original_full_ranking_QA_and_lossless_browser_node_checks'
    assert proof['round'] == 101 and proof['original_full_QA_result']['status'] == 'passed'
    assert read(folder / 'provenance_scope_execution.json')['status'] == 'passed'
    preceding = A / 'service_owned_workflows_20261006/conditional_residual_scores_evidence_publication_v2'
    assert not owned(read(preceding / 'native_launch.json'))
    assert read(preceding / 'service_execution.json')['status'] == 'passed'
    sources = [Path(__file__), qa, folder / 'provenance_scope_execution.json',
               OUT / 'previous_automatic_round101_receipt.json',
               A / 'publish_conditional_flag_round101_full_validation_20261006.py']
    pins = {str(p): sha(p) for p in sources}
    create(OUT / 'frozen_before_actual_publication.json', {
        'input_sha256': pins, 'at_local': time.strftime('%Y-%m-%dT%H:%M:%S'),
        'actual37_scores_candidate14_and_complete_QA12_already_passed': True,
        'existing_automatic_receipt_preserved_verbatim': True,
        'new_training_scoring_inference_or_QA_claimed': False, 'test_labels_read': False})
    from hidden_windows_child_creation_20261006 import install
    from handoff_joint_goss_round97_full_execution_20261006 import suspended_idle
    import publish_classifier_consensus_workflows_20261006 as helpers
    restore = install()
    held = []
    try:
        identity = read(A / 'service_owned_workflows_20261006/main_publisher_v7/native_launch.json')
        parent, worker, idle = suspended_idle(identity, '    main (watch_validations_main_v7_20261006.py:71)')
        held.extend((worker, parent))
        create(OUT / 'actual_main7_idle_before_and_after_hold.json', idle)
        assert receipt.read_bytes() == original_bytes
        for path, digest in pins.items():
            assert sha(path) == digest
        source = A / 'publish_conditional_flag_round101_full_validation_20261006.py'
        text = source.read_text(encoding='utf-8')
        patches = {
            "namespace['snapshot'](100)": "namespace['snapshot'](101)",
            "github_validation_sync_main_20261005/round101_receipt.json":
                "github_validation_sync_main_20261005/round101_full_recovery_receipt_v6.json",
            "'actual_full_QA_version': 12,":
                "'actual_full_QA_version': 12, 'full_immutable_ranking_and_all_original_QA_preserved': True, 'original_automatic_receipt_preserved': True,"}
        for before, after in patches.items():
            assert text.count(before) == 1, before
            text = text.replace(before, after)
        before = '    for path in extra:\n'
        assert text.count(before) == 1
        text = text.replace(before,
            "    extra += list(PUBLICATION_RECOVERY_OUT.glob('*.json')) + [Path(__file__)]\n"
            "    for version in ('', '_v2', '_v3', '_v4', '_v5'):\n"
            "        p = A / ('publish_conditional_flag_round101_full_validation' + version + '_20261006.py')\n"
            "        if p.exists(): extra.append(p)\n"
            "    for name in ('register_conditional_flag_round101_artifacts_v2_20261006.py', 'run_conditional_flag_round101_full_registration_v2_20261006.py', 'run_conditional_flag_round101_full_registration_v3_20261006.py', 'close_conditional_flag_round101_main_v4_20261006.py', 'close_conditional_flag_round101_main_v5_20261006.py'):\n"
            "        extra.append(A / name)\n"
            "    extra += list((A / 'optimization_20261003_r101').glob('*failure*.json'))\n"
            "    for service_name in ('conditional_flag_round101_full_registration', 'conditional_flag_round101_full_registration_v2', 'conditional_flag_round101_full_registration_v3', 'conditional_flag_round101_main_closure_v4', 'conditional_flag_round101_main_closure_v5', 'conditional_flag_round101_full_publication_v6'):\n"
            "        failed_service = A / 'service_owned_workflows_20261006' / service_name\n"
            "        extra += list(failed_service.glob('*.json')) + list(failed_service.glob('*.log'))\n" + before)
        namespace = {'__file__': __file__, '__name__': 'actual_complete101_publication_v6',
                     'PUBLICATION_RECOVERY_OUT': OUT}
        exec(compile(text, str(source), 'exec'), namespace)
        namespace['main']()
        upgraded = read(A / 'github_validation_sync_main_20261005/round101_full_recovery_receipt_v6.json')
        assert upgraded['actual_full_QA_version'] == 12 and upgraded['scored_records'] == 37
        helpers.verify_main(upgraded['commit'])
        assert receipt.read_bytes() == original_bytes
        write(receipt, upgraded)
        create(OUT / 'verification.json', {
            'status': 'passed_actual_full101_immutable_QA12_main_publication_recovery',
            'receipt_sha256': sha(receipt), 'commit': upgraded['commit'],
            'previous_receipt_sha256': sha(OUT / 'previous_automatic_round101_receipt.json'),
            'existing_scientific_scores_and_candidate_and_QA_reused': True,
            'all_actual_failed_registration_and_publication_attempts_preserved': True,
            'scientific_workers_stopped_or_restarted': 0, 'test_labels_read': False})
        create(folder / 'full_registration_execution.json', {
            'status': 'passed', 'at_local': time.strftime('%Y-%m-%dT%H:%M:%S'),
            'existing_official_scores_registered': 37, 'full_QA_version': 12,
            'full_rankings_all_original_QA_and_main_publication_completed': True,
            'publication_recovery_verification': str(OUT / 'verification.json'),
            'scientific_workers_stopped_or_restarted': 0, 'new_quality_scores_by_registration': 0,
            'test_labels_read': False})
        print(json.dumps(upgraded, ensure_ascii=False), flush=True)
    except BaseException as error:
        create(OUT / 'failure.json', {'status': 'failed_preserved_complete101_publication_upgrade',
                                    'error': f'{type(error).__name__}: {error}'})
        raise
    finally:
        for process in reversed(held):
            if process.is_running(): process.resume()
        create(OUT / 'actual_hidden_children.json', {'events': restore()})


if __name__ == '__main__':
    main()
