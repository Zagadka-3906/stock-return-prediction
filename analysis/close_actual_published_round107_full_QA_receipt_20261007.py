"""Verify already-published full QA18 bytes and preserve/replace the earlier generic receipt."""
from pathlib import Path
import hashlib
import json
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path[:0] = [str(ROOT), str(A)]
from run_dependency_queue_v3_20261006 import read, sha, create, owned
from handoff_joint_goss_round97_full_execution_20261006 import suspended_idle
from hidden_windows_child_creation_20261006 import install
import publish_classifier_consensus_workflows_20261006 as helpers


def main():
    out = A / 'round107_full_QA_receipt_closure_20261007'
    assert not out.exists()
    out.mkdir()
    prior_service = A / 'service_owned_workflows_20261006/lowalpha50_round107_closed_QA_publication_recovery'
    assert not owned(read(prior_service / 'native_launch.json'))
    terminal = read(prior_service / 'service_execution.json')
    assert terminal['status'] == 'failed' and 'FileExistsError:' in terminal['failure']
    assert 'round107_receipt.json' in terminal['failure']
    canonical = A / 'github_validation_sync_main_20261005/round107_receipt.json'
    previous_bytes = canonical.read_bytes()
    previous = json.loads(previous_bytes)
    assert previous['round'] == 107 and previous['status'] == 'pushed_and_remote_head_verified'
    with (out / 'original_generic_receipt.raw.json').open('xb') as stream:
        stream.write(previous_bytes)
    sync = helpers.sync
    sources = [Path(__file__), canonical, prior_service / 'service_execution.json',
        *list(prior_service.glob('*.log')),
        A / 'lowalpha50_round107_closed_QA_publication_recovery_20261007/failure.json',
        A / 'collect_full_lossless_round107_qa18_20261007.py',
        A / 'optimization_20261003_r107/provenance_scope_execution.json',
        A / 'lossless_ranking_display_qa_v18_20261007/round107/verification.json']
    pins = {**read(A / 'optimization_20261003_r107/protocol.json')['input_sha256'],
            **{str(p): sha(p) for p in sources}}
    # Canonical receipt is a mutable pointer; retain its exact old bytes separately.
    pins.pop(str(canonical))
    frozen = out / 'frozen_before_actual_full_QA_receipt_closure.json'
    create(frozen, {'at_local': time.strftime('%Y-%m-%dT%H:%M:%S'), 'input_sha256': pins,
        'original_generic_receipt_sha256': hashlib.sha256(previous_bytes).hexdigest(),
        'original_generic_receipt_raw_copy': str(out / 'original_generic_receipt.raw.json'),
        'original_natural_duplicate_receipt_failure': terminal, 'test_labels_read': False})
    held, scope = [], None
    restore = install()
    try:
        row = read(A / 'service_owned_workflows_20261006/main_publisher_v7/native_launch.json')
        parent, worker, idle = suspended_idle(row, '    main (watch_validations_main_v7_20261006.py:71)')
        held.extend((worker, parent))
        create(out / 'actual_main7_idle_before_and_after_hold.json', idle)
        from win32_read_handle_hash_cache_with_filename_v2_20261006 import LockedReadHashCache
        scope = LockedReadHashCache(pins)
        scope.__enter__()
        head = sync.git('rev-parse', 'HEAD')
        helpers.verify_main(head)
        assert not sync.git('status', '--porcelain')
        manifest_path = sync.WORKTREE / 'validation_sync/round107/manifest.json'
        manifest = read(manifest_path)
        assert manifest['actual_complete_QA_version'] == 18
        assert manifest['immutable_all_values_lossless_display_and_complete_original_QA_published']
        assert (manifest['scored_records'], manifest['connected_records']) == (50, 11604)
        expected = {name: item['sha256'] for name, item in manifest['exported_files'].items()}
        expected['validation_sync/round107/manifest.json'] = hashlib.sha256(manifest_path.read_bytes()).hexdigest()
        assert helpers.blob_hashes(head, expected) == expected
        qa_paths = [name for name in expected if 'lossless_ranking_display_qa_v18_20261007/round107/' in name]
        assert len(qa_paths) == 4
        assert any(name.endswith('/verification.json') for name in qa_paths)
        assert any(name.endswith('/qa/interaction_result.json') for name in qa_paths)
        assert any(name.endswith('/qa/ranking_report.png') for name in qa_paths)
        scope.reverify()
        proof = {'status': 'passed_actual_main_full_QA18_all_committed_export_bytes_and_frozen_inputs',
            'at_local': sync.now(), 'actual_full_QA_commit': head,
            'earlier_generic_commit': previous['commit'], 'round': 107,
            'actual_full_QA_version': 18, 'scored_records': 50, 'connected_records': 11604,
            'raw_committed_full_export_blobs_verified': len(expected), 'full_export_git_blob_sha256': expected,
            'all_original_frozen_inputs_initial_and_final_rehash_and_read_only_Windows_locks_passed': True,
            'all_original_failed_publications_and_exact_generic_receipt_preserved': True,
            'original_generic_receipt_did_not_bind_actual_full_QA18_export': True,
            'new_model_fits': 0, 'new_quality_scores': 0, 'new_inference_claimed': False, 'test_labels_read': False}
        create(out / 'actual_full_QA18_main_blob_verification.json', proof)
        prefix = Path('validation_sync/round107/publication_receipt_recovery')
        files = [Path(__file__), frozen, out / 'original_generic_receipt.raw.json',
            out / 'actual_full_QA18_main_blob_verification.json', prior_service / 'service_execution.json',
            A / 'lowalpha50_round107_closed_QA_publication_recovery_20261007/failure.json']
        payload = {(prefix / 'original_records' / p.relative_to(ROOT)).as_posix(): p.read_bytes() for p in files}
        payload[(prefix / '.gitattributes').as_posix()] = b'* -text\n'
        for name, data in payload.items():
            assert not sync.SECRET.search(data)
            sync.atomic(sync.WORKTREE / name, data)
        sync.git('add', '-f', '--', *sorted(payload))
        assert set(sync.git('-c', 'core.quotepath=false', 'diff', '--cached', '--name-only').splitlines()) == set(payload)
        sync.git('-c', 'maintenance.auto=false', '-c', 'gc.auto=0', 'commit', '-m',
            '核验第107轮完整QA18主分支导出并保留原通用回执和重复写入失败', timeout=180)
        commit = sync.git('rev-parse', 'HEAD')
        repair_hashes = {name: hashlib.sha256(data).hexdigest() for name, data in payload.items()}
        assert helpers.blob_hashes(commit, {**expected, **repair_hashes}) == {**expected, **repair_hashes}
        sync.git('push', 'origin', 'HEAD:refs/heads/main', timeout=180)
        helpers.verify_main(commit)
        helpers.watcher.advance_source_index(commit)
        receipt = {**previous, 'at_local': sync.now(), 'commit': commit,
            'actual_full_QA_version': 18, 'full_QA_payload_commit': head,
            'raw_git_blobs_verified': len(expected)+len(repair_hashes),
            'full_immutable_ranking_and_all_original_QA_preserved': True,
            'earlier_generic_receipt_preserved_in_full': str(out / 'original_generic_receipt.raw.json'),
            'actual_full_QA_export_and_all_source_bytes_verified': True,
            'new_quality_scores_by_registration': 0}
        assert canonical.read_bytes() == previous_bytes
        sync.atomic(canonical, sync.encoded(receipt))
        create(out / 'verification.json', {**proof, 'status': 'passed_actual_complete_round107_receipt_recovery_and_main',
            'main_receipt': receipt, 'repair_commit': commit})
        create(A / 'optimization_20261003_r107/full_registration_execution.json', {'status': 'passed',
            'at_local': sync.now(), 'existing_official_scores_registered': 50,
            'full_rankings_all_original_QA_and_main_publication_completed': True,
            'all_original_publication_failures_and_generic_receipt_retained': True,
            'actual_full_QA18_main_receipt_closure': str(out / 'verification.json'),
            'scientific_workers_stopped_or_restarted': 0, 'new_quality_scores_by_registration': 0,
            'global_goal_or_resource_exhaustion_claimed': False, 'test_labels_read': False})
        print(json.dumps(receipt, ensure_ascii=False), flush=True)
    finally:
        if scope is not None:
            scope.close()
        for process in reversed(held):
            if process.is_running():
                process.resume()
        create(out / 'actual_hidden_publication_children.json', {'events': restore()})


if __name__ == '__main__':
    main()
