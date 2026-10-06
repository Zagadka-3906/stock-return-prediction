"""Preserve all actual R81 scores without claiming its release scope complete."""
from pathlib import Path
import gzip
import hashlib
import json

import publish_classifier_consensus_workflows_20261006 as previous

sync, ROOT, A = previous.sync, previous.ROOT, previous.A
PREFIX = Path('validation_sync/round81_score_checkpoint_20261006')


def main():
    out = A / 'round81_score_checkpoint_github_20261006'
    assert not out.exists()
    folder = A / 'optimization_20261003_r81'
    paths = [folder / 'protocol.json', folder / 'component_audit.json', folder / 'selection.json',
             *sorted(folder.glob('wave*_results.json'))]
    assert len(paths) == 7
    waves = [sync.read(path) for path in paths if path.name.startswith('wave')]
    assert all(row['status'] == 'complete' for row in waves)
    assert sum(len(row['results']) for row in waves) == 124
    assert sync.read(folder / 'selection.json')['scored_records'] == 124
    plan = sync.read(previous.HANDOFF / 'queue_plan.json')
    pairs = [previous.owned_pair(plan['preserved_active_jobs'][name]['pid'],
             Path(plan['preserved_active_jobs'][name]['script']), plan['preserved_active_jobs'][name]['script_args'])
             for name in ('main_publisher', 'progress_monitor')]
    suspended = []
    out.mkdir()
    try:
        for parent, worker in pairs:
            assert not [p for p in parent.children(recursive=True)
                        if p.pid != worker.pid and p.name().lower() != 'conhost.exe']
            for process in (worker, parent):
                process.suspend()
                suspended.append(process)
        old = sync.git('rev-parse', 'HEAD')
        previous.verify_main(old)
        assert not sync.git('status', '--porcelain')
        targets = {'analysis/' + Path(__file__).name: Path(__file__).read_bytes(),
                   (PREFIX / '.gitattributes').as_posix(): b'* -text\n'}
        bindings = {}
        for path in paths:
            data = path.read_bytes()
            json.loads(data.decode('utf-8-sig'))
            assert not sync.SECRET.search(data)
            digest = hashlib.sha256(data).hexdigest()
            destination = (PREFIX / path.name).as_posix()
            if len(data) > 5 * 1024**2:
                data = gzip.compress(data, mtime=0)
                destination += '.gz'
                assert hashlib.sha256(gzip.decompress(data)).hexdigest() == digest
            targets[destination] = data
            bindings[path.name] = {'published_path': destination, 'raw_sha256': digest,
                                   'published_sha256': hashlib.sha256(data).hexdigest()}
        targets[(PREFIX / 'manifest.json').as_posix()] = sync.encoded({
            'status': 'all124_actual_official_scores_and_frozen_selection_saved_release_pending',
            'at_local': sync.now(), 'previous_main': old, 'files': bindings,
            'selected_score': sync.read(folder / 'selection.json')['winner']['connected_final_score'],
            'round': 81, 'explicit_parent_round': 66, 'actual_scored_records': 124,
            'release_calibration_causality_fullfuture_candidates_ranking_and_scope_still_required': True,
            'partial_checkpoint_not_completed_board_promotion': True,
            'only_publication_branch': 'main', 'test_labels_read': False,
            'new_quality_scores_by_publication': 0})
        for name, data in targets.items():
            sync.atomic(sync.WORKTREE / name, data)
        sync.git('add', '-f', '--', *targets)
        sync.git('-c', 'maintenance.auto=false', '-c', 'gc.auto=0', 'commit', '-m',
                 '保存第81轮全部124条官方评分与冻结选择，完整发布检查继续', timeout=180)
        commit = sync.git('rev-parse', 'HEAD')
        expected = {name: hashlib.sha256(data).hexdigest() for name, data in targets.items()}
        assert previous.blob_hashes(commit, expected) == expected
        sync.git('push', 'origin', 'HEAD:refs/heads/main', timeout=180)
        previous.verify_main(commit)
        previous.watcher.advance_source_index(commit)
        receipt = {'status': 'pushed_verified_all124_R81_scores_checkpoint_main_only',
            'commit': commit, 'at_local': sync.now(), 'raw_git_blob_sha256_verified': len(expected),
            'url': f'https://github.com/Zagadka-3906/stock-return-prediction/tree/main/{PREFIX.as_posix()}'}
        with (out / 'receipt.json').open('x', encoding='utf-8') as stream:
            json.dump(receipt, stream, ensure_ascii=False, indent=2)
        print(json.dumps(receipt, ensure_ascii=False), flush=True)
    finally:
        for process in reversed(suspended):
            if process.is_running():
                process.resume()


if __name__ == '__main__':
    main()
