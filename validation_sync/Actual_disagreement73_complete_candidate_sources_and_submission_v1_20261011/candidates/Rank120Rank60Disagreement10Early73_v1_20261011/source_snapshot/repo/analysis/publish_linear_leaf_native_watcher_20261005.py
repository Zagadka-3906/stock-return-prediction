"""Publish and verify the closed-native-scope synchronization controller."""
from pathlib import Path
import hashlib
import json
import sys

import psutil

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'analysis'))
import watch_validations_main_v2_20261005 as watcher

sync = watcher.sync
PREFIX = Path('validation_sync/linear_leaf_native_sync_20261005')


def sha(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def main():
    receipt = sync.OUT / 'linear_leaf_native_sync_receipt.json'
    assert not receipt.exists()
    run_path = ROOT / 'analysis/linear_leaf_native_github_run_20261005.json'
    run = sync.read(run_path)
    for source, expected in run['input_sha256'].items():
        assert sha(source) == expected, source
    native_root = psutil.Process(run['pid'])
    command = native_root.cmdline()
    assert run['script'] in command
    interpreters = [p for p in native_root.children(recursive=True) if p.cmdline()[1:] == command[1:]]
    assert len(interpreters) == 1
    observer = psutil.Process(sync.read(sync.OUT / 'owner.lock')['pid'])
    assert str(ROOT / 'analysis/watch_validations_main_v2_20261005.py') in observer.cmdline()
    parent = observer.parent()
    assert parent is not None and parent.cmdline()[1:] == observer.cmdline()[1:]
    suspended = []
    try:
        for process in (observer, parent, interpreters[0], native_root):
            process.suspend()
            suspended.append(process)
        for root, child in ((parent, observer), (native_root, interpreters[0])):
            assert all(p.pid == child.pid or p.name().lower() == 'conhost.exe' for p in root.children(recursive=True))
        assert not sync.git('status', '--porcelain')
        head = sync.git('rev-parse', 'HEAD')
        assert sync.git('ls-remote', '--heads', 'origin').splitlines() == [f'{head}\trefs/heads/main']
        sources = {Path(__file__), ROOT / 'analysis/prepare_linear_leaf_native_github_20261005.py',
                   ROOT / 'analysis/publish_linear_leaf_completed_native_20261005.py'}
        evidence = {run_path, ROOT / 'analysis/linear_leaf_publication_blob_qa_20261005/verification.json'}
        assert sync.read(ROOT / 'analysis/linear_leaf_publication_blob_qa_20261005/verification.json')['status'] == 'passed_all_published_original_file_blob_sha256'
        paths, bindings = [], {}
        sync.atomic(sync.WORKTREE / PREFIX / '.gitattributes', b'* -text\n')
        paths.append((PREFIX / '.gitattributes').as_posix())
        for source in sorted(sources | evidence):
            data = source.read_bytes()
            assert len(data) < 5 * 1024**2 and not sync.SECRET.search(data)
            relative = source.relative_to(ROOT)
            destination = relative if source in sources else PREFIX / relative
            sync.atomic(sync.WORKTREE / destination, data)
            paths.append(destination.as_posix())
            bindings[str(source)] = sha(source)
        sync.atomic(sync.WORKTREE / PREFIX / 'manifest.json', sync.encoded({
            'status': 'passed_frozen_native_scope_publication_controller_source_checks',
            'at_local': sync.now(), 'source_sha256': bindings, 'live_native_sync_root_pid': native_root.pid,
            'requires_actual30_annual_fits_and_closed_training_scope_and_resources_before_annual_publish': True,
            'requires_actual6_final_fits_and_full1599600_row_reload_prefix_controls_before_future_publish': True,
            'user_authorized_upload_each_completed_validation': True, 'only_branch': 'main',
            'scientific_controllers_untouched': True, 'new_quality_scores': 0, 'test_labels_read': False}))
        paths.append((PREFIX / 'manifest.json').as_posix())
        for offset in range(0, len(paths), 50):
            sync.git('add', '--', *paths[offset:offset + 50])
        changed = set(sync.git('-c', 'core.quotepath=false', 'diff', '--cached', '--name-only').splitlines())
        assert changed and changed <= set(paths)
        sync.git('-c', 'maintenance.auto=false', '-c', 'gc.auto=0', 'commit', '-m',
            '自动同步线性树30折训练和6个最终模型的完整证据至main', timeout=180)
        commit = sync.git('rev-parse', 'HEAD')
        sync.git('push', 'origin', 'HEAD:refs/heads/main', timeout=180)
        assert sync.git('ls-remote', '--heads', 'origin').splitlines() == [f'{commit}\trefs/heads/main']
        watcher.advance_source_index(commit)
        result = {'status': 'pushed_verified_only_main', 'at_local': sync.now(), 'commit': commit,
            'files': len(paths), 'url': f'https://github.com/Zagadka-3906/stock-return-prediction/tree/main/{PREFIX.as_posix()}'}
        sync.atomic(receipt, sync.encoded(result))
        print(json.dumps(result, ensure_ascii=False), flush=True)
    finally:
        for process in reversed(suspended):
            if process.is_running():
                process.resume()


if __name__ == '__main__':
    main()
