"""Verify exact committed export bytes before pushing each full round to main."""
import hashlib


def publish(sync, number):
    from finalize_main_branch_consolidation_20261005 import verify_main
    from publish_main_closeout_v2_20261005 import blob_hashes
    from watch_validations_main_v2_20261005 import advance_source_index
    existing = sync.WORKTREE / f'validation_sync/round{number}/manifest.json'
    if not existing.exists():
        assert not sync.git('status', '--porcelain')
        verify_main(sync.git('rev-parse', 'HEAD'))
        manifest, payload = sync.snapshot(number)
        for name, data in payload.items():
            sync.atomic(sync.WORKTREE / name, data)
        selected = sorted(payload)
        for offset in range(0, len(selected), 50):
            sync.git('add', '-f', '--', *selected[offset:offset + 50])
        staged = set(sync.git('-c', 'core.quotepath=false', 'diff', '--cached', '--name-only').splitlines())
        assert staged and staged <= set(selected)
        sync.git('-c', 'maintenance.auto=false', '-c', 'gc.auto=0', 'commit', '-m',
            f'完成第{number}轮完整验证及无损榜单，逐文件核验后同步main', timeout=180)
        expected = {name: hashlib.sha256(data).hexdigest() for name, data in payload.items()}
    else:
        manifest = sync.read(existing)
        assert manifest['round'] == number
        allowed = set(manifest['exported_files']) | {
            f'validation_sync/round{number}/manifest.json', f'validation_sync/round{number}/README.md',
            'validation_sync/latest.json', 'validation_sync/README.md', 'README.md'}
        staged = set(sync.git('-c', 'core.quotepath=false', 'diff', '--cached', '--name-only').splitlines())
        assert staged <= allowed
        if staged:
            sync.git('commit', '-m', f'完成第{number}轮完整验证及无损榜单', timeout=180)
        assert not sync.git('status', '--porcelain', '--untracked-files=no')
        expected = {name: entry['sha256'] for name, entry in manifest['exported_files'].items()}
    commit = sync.git('rev-parse', 'HEAD')
    assert blob_hashes(commit, expected) == expected
    sync.git('push', 'origin', 'HEAD:refs/heads/main', timeout=180)
    verify_main(commit)
    advance_source_index(commit)
    receipt = {'status': 'pushed_and_remote_head_verified', 'round': number,
        'at_local': sync.now(), 'commit': commit, 'branch': 'main', 'remote': sync.REMOTE,
        'official_score': manifest['metrics']['final_score'], 'scored_records': manifest['scored_records'],
        'connected_records': manifest['connected_records'], 'raw_git_blobs_verified': len(expected),
        'full_immutable_ranking_and_all_original_QA_preserved': True,
        'all_publication_child_creation_explicitly_hidden': True,
        'scheme_url': f'https://github.com/Zagadka-3906/stock-return-prediction/tree/main/validation_sync/round{number}'}
    sync.atomic(sync.OUT / f'round{number}_receipt.json', sync.encoded(receipt))
    return receipt
