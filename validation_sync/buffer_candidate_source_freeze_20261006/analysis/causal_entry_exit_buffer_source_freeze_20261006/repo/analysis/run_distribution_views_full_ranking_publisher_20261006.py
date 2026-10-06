"""Publish93/94 with complete immutable rankings, coordinating the owned main publisher."""
from pathlib import Path
from contextlib import contextmanager
import json
import sys
import time
import psutil

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path[:0] = [str(ROOT), str(A)]
import publish_classifier_consensus_workflows_20261006 as helpers
from collect_full_lossless_round_publication_20261006 import collect, sha, read
from run_dependency_queue_v3_20261006 import owned
from atomic_optimization_observer_writes_20261005 import write

OUT = A / 'distribution_views_full_ranking_publisher_20261006'
sync = helpers.sync


@contextmanager
def idle_main_publisher():
    row = read(A / 'service_owned_workflows_20261006/main_publisher_v5/native_launch.json')
    assert owned(row)
    root, worker = helpers.owned_pair(row['pid'], Path(row['script']), row['script_args'])
    assert root.create_time() == row['owned_parent_creation_time']
    assert worker.pid == row['owned_worker_pid'] and worker.create_time() == row['owned_worker_creation_time']
    suspended = []
    try:
        for _ in range(50):
            for process in (worker, root):
                process.suspend()
                suspended.append(process)
            busy = [p for p in root.children(recursive=True) if p.pid != worker.pid and p.name().lower() != 'conhost.exe']
            if not busy:
                break
            for process in reversed(suspended):
                process.resume()
            suspended.clear()
            time.sleep(.2)
        else:
            raise RuntimeError('Main publisher owns an active publication child; retry later.')
        yield row
    finally:
        for process in reversed(suspended):
            if process.is_running():
                process.resume()


def state(**extra):
    write(OUT / 'state.json', {'at_local': sync.now(), 'required_rounds': [93, 94],
        'original198_and_new262_scientific_plans_preserved': True,
        'new_model_fits': 0, 'new_quality_scores': 0, 'test_labels_read': False,
        'global_goal_complete': False, **extra})


def full_publish(number, expected):
    import qualified_round_recovery_evidence_v3_20261006 as qualification
    from verified_round_main_publication_20261006 import publish
    evidence = qualification.complete_round_evidence(number)
    assert evidence is not None and evidence['scored_records'] == expected
    payload, full = collect(number, 6, expected)
    receipt_path = sync.OUT / f'round{number}_receipt.json'
    with idle_main_publisher() as actual_publisher:
        current = sync.git('rev-parse', 'HEAD')
        helpers.verify_main(current)
        if not receipt_path.exists():
            # Our installed adapter includes every full immutable display and QA file.
            receipt = publish(sync, number)
            publication_mode = 'primary_complete_round_export'
        else:
            receipt = read(receipt_path)
            assert receipt['status'] == 'pushed_and_remote_head_verified' and receipt['branch'] == 'main'
            assert receipt['scored_records'] == expected and receipt['official_score'] == evidence['score']
            relative = Path(f'validation_sync/round{number}')
            manifest_path = sync.WORKTREE / relative / 'manifest.json'
            manifest = read(manifest_path)
            assert manifest['original_full_ranking_sha256'] == full['original_full_ranking_sha256']
            assert manifest['connected_records'] == full['connected_records']
            assert manifest['scored_records'] == full['scored_records']
            attributes = (relative / '.gitattributes').as_posix()
            payload[attributes] = b'* -text\n'
            full['exported_files'][attributes] = {'bytes': 8, 'sha256': sync.sha(payload[attributes])}
            manifest['local_input_source_sha256'].update(full['local_input_source_sha256'])
            manifest['exported_files'].update(full['exported_files'])
            manifest['immutable_all_values_lossless_display_and_complete_original_QA_published'] = True
            manifest['actual_complete_QA_version'] = 6
            payload[(relative / 'manifest.json').as_posix()] = sync.encoded(manifest)
            payload[(relative / 'full_lossless_publication_supplement.json').as_posix()] = sync.encoded(full)
            selected = sorted(payload)
            staged = set(sync.git('-c', 'core.quotepath=false', 'diff', '--cached', '--name-only').splitlines())
            assert staged <= set(selected), 'Unrelated staged files; preserve them and retry.'
            for name, data in payload.items():
                sync.atomic(sync.WORKTREE / name, data)
            for offset in range(0, len(selected), 50):
                sync.git('add', '-f', '--', *selected[offset:offset + 50])
            staged = set(sync.git('-c', 'core.quotepath=false', 'diff', '--cached', '--name-only').splitlines())
            assert staged <= set(selected)
            if staged:
                sync.git('-c', 'maintenance.auto=false', '-c', 'gc.auto=0', 'commit', '-m',
                    f'补齐第{number}轮完整无损交互榜与全部原始检查证据', timeout=180)
            commit = sync.git('rev-parse', 'HEAD')
            expected_blobs = {name: sync.sha(data) for name, data in payload.items()}
            assert helpers.blob_hashes(commit, expected_blobs) == expected_blobs
            sync.git('push', 'origin', 'HEAD:refs/heads/main', timeout=180)
            helpers.verify_main(commit)
            helpers.watcher.advance_source_index(commit)
            receipt.update(full_lossless_publication_commit=commit,
                full_immutable_ranking_and_all_original_QA_preserved=True,
                full_lossless_supplement_raw_blobs_verified=len(expected_blobs))
            sync.atomic(receipt_path, sync.encoded(receipt))
            publication_mode = 'complete_lossless_supplement_to_existing_base_export'
        commit = receipt.get('full_lossless_publication_commit', receipt['commit'])
        original_files = full['exported_files']
        expected_blobs = {name: value['sha256'] for name, value in original_files.items()}
        assert helpers.blob_hashes(commit, expected_blobs) == expected_blobs
        result = {'status': 'pushed_complete_immutable_rankings_and_all_original_QA_main_only',
            'round': number, 'at_local': sync.now(), 'commit': commit, 'publication_mode': publication_mode,
            'original_main_receipt': receipt, 'actual_complete_collection': full,
            'actual_main_publisher_identity_preserved': actual_publisher,
            'raw_git_blobs_verified': len(expected_blobs), 'new_model_fits': 0,
            'new_quality_scores': 0, 'test_labels_read': False}
        write(OUT / f'round{number}_receipt.json', result)
    return result


def main():
    import qualified_round_recovery_evidence_v3_20261006 as qualification
    from distribution_views_lossless_publication_adapter_20261006 import install as lossless
    from hidden_windows_child_creation_20261006 import install as hidden
    run_path = Path(sys.argv[1]).resolve()
    run = read(run_path)
    assert run['required_rounds'] == [93, 94] and run['expected_records'] == [124, 138]
    for source, digest in run['input_sha256'].items():
        assert sha(source) == digest
    OUT.mkdir()
    old_gate = sync.complete_round_evidence
    sync.complete_round_evidence = qualification.complete_round_evidence
    old_snapshot = lossless(sync)
    restore = hidden()
    closed = []
    try:
        for number, expected in ((93, 124), (94, 138)):
            while True:
                for source, digest in run['input_sha256'].items():
                    assert sha(source) == digest
                actual = read(A / 'service_owned_workflows_20261006/main_publisher_v5/native_launch.json')
                assert owned(actual)
                result_path = ROOT / f'results/optimization_20261003_r{number}.json'
                full_qa = A / f'lossless_ranking_display_qa_v6_20261006/round{number}/verification.json'
                if result_path.exists() and full_qa.exists() and psutil.virtual_memory().available >= 6 * 1024**3:
                    try:
                        if qualification.complete_round_evidence(number) is not None:
                            full_publish(number, expected)
                            closed.append(number)
                            break
                    except Exception as error:
                        attempts = OUT / 'preserved_publication_attempts'
                        attempts.mkdir(exist_ok=True)
                        write(attempts / f'{number}_{time.time_ns()}.json', {
                            'at_local': sync.now(), 'error': f'{type(error).__name__}: {error}',
                            'scientific_scores_and_sources_unchanged': True})
                        state(stage='actual_full_publication_retry_pending', round=number, error=str(error))
                    finally:
                        qualification.close()
                state(stage='waiting_actual_qualified_complete_round_and_QA_v6', round=number,
                    complete_publication_rounds=closed, main_publisher_owned_live=True,
                    actual_host_available_bytes=psutil.virtual_memory().available)
                time.sleep(30)
        state(stage='completed_both_actual_full_lossless_round_publications', complete_publication_rounds=closed)
    finally:
        sync.snapshot, sync.complete_round_evidence = old_snapshot, old_gate
        qualification.close()
        write(OUT / 'actual_hidden_child_creations.json', {'events': restore()})


if __name__ == '__main__':
    main()
