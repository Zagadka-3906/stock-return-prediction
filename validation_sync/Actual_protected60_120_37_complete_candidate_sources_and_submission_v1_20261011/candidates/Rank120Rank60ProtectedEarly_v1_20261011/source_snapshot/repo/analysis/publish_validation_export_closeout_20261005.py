"""Save the full raw Git-byte audit and avoid restaging an already archived ranking."""
from pathlib import Path
import hashlib
import json
import sys
import psutil

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path.insert(0, str(A))
import watch_validations_main_v2_20261005 as watcher
from publish_main_closeout_v2_20261005 import blob_hashes

sync = watcher.sync


def main():
    head = sync.git('rev-parse', 'HEAD')
    paths = sync.git('ls-tree', '-r', '--name-only', head, 'validation_sync').splitlines()
    manifests = [p for p in paths if p.endswith('/manifest.json') and p.split('/')[1].startswith('round')]
    checked = {}
    for path in manifests:
        record = json.loads(sync.subprocess.check_output(['git', 'show', f'{head}:{path}'], cwd=ROOT))
        prefix = path.rsplit('/', 1)[0] + '/'
        expected = {p: v['sha256'] for p, v in record['exported_files'].items() if p.startswith(prefix)}
        assert blob_hashes(head, expected) == expected
        checked.update(expected)
    standard = sync.subprocess.check_output(['git', 'show', f'{head}:后续选模标准.md'], cwd=ROOT)
    assert standard == (ROOT / '后续选模标准.md').read_bytes()
    proof_path = A / 'validation_export_raw_bytes_audit_20261005/post_repair.json'
    with proof_path.open('x', encoding='utf-8') as stream:
        json.dump({'status': 'passed_all_current_round_export_Git_blob_SHA256',
            'actual_commit_verified': head, 'actual_rounds': len(manifests), 'actual_artifacts': len(checked),
            'all_checked_Git_blob_sha256': checked, 'selection_standard_original_bytes_preserved': True,
            'new_quality_scores': 0, 'test_labels_read': False}, stream, ensure_ascii=False, indent=2)
    observer = psutil.Process(sync.read(sync.OUT / 'owner.lock')['pid'])
    parent = observer.parent()
    assert str(A / 'watch_validations_main_v3_20261005.py') in parent.cmdline()
    paused = []
    try:
        for p in (observer, parent):
            p.suspend()
            paused.append(p)
        assert all(p.pid == observer.pid or p.name().lower() == 'conhost.exe' for p in parent.children(recursive=True))
        assert not sync.git('status', '--porcelain')
        assert sync.git('rev-parse', 'HEAD') == head
        targets = {'.gitignore': (ROOT / '.gitignore').read_bytes(),
            Path(__file__).relative_to(ROOT).as_posix(): Path(__file__).read_bytes(),
            'validation_sync/gradient_sampling_controls_20261005/raw_export_post_repair.json': proof_path.read_bytes()}
        for path, data in targets.items():
            sync.atomic(sync.WORKTREE / path, data)
        sync.git('add', '-f', '--', *targets)
        staged = set(sync.git('-c', 'core.quotepath=false', 'diff', '--cached', '--name-only').splitlines())
        assert staged and staged <= set(targets)
        sync.git('-c', 'maintenance.auto=false', '-c', 'gc.auto=0', 'commit', '-m',
            '核验全部108个验证导出Git字节，记录已归档完整榜')
        commit = sync.git('rev-parse', 'HEAD')
        expected = {p: hashlib.sha256(d).hexdigest() for p, d in targets.items()}
        assert blob_hashes(commit, expected) == expected
        sync.git('push', 'origin', 'HEAD:refs/heads/main', timeout=180)
        assert sync.git('ls-remote', '--heads', 'origin').splitlines() == [f'{commit}\trefs/heads/main']
        watcher.advance_source_index(commit)
        receipt = {'status': 'pushed_only_main_and_all108_raw_export_blobs_verified',
            'commit': commit, 'at_local': sync.now(), 'actual_rounds': len(manifests),
            'actual_artifacts': len(checked), 'new_quality_scores': 0}
        sync.atomic(A / 'validation_export_raw_bytes_audit_20261005/receipt.json', sync.encoded(receipt))
        print(json.dumps(receipt, ensure_ascii=False), flush=True)
    finally:
        for p in reversed(paused):
            if p.is_running():
                p.resume()


if __name__ == '__main__':
    main()
