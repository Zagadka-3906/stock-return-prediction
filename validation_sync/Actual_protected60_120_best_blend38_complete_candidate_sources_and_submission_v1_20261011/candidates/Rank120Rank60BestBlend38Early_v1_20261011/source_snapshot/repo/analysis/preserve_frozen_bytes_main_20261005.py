"""Keep committed scientific inputs byte-identical to their frozen local files."""
from pathlib import Path
import hashlib
import json
import subprocess
import sys

import psutil

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'analysis'))
import watch_validations_main_v2_20261005 as watcher

sync = watcher.sync
PREFIX = Path('validation_sync/workspace_snapshot_20261005')
OUT = ROOT / 'analysis/workspace_main_submission_20261005'


def main():
    assert not sync.git('status', '--porcelain')
    previous = sync.git('rev-parse', 'HEAD')
    assert sync.git('ls-remote', '--heads', 'origin').splitlines() == [f'{previous}\trefs/heads/main']
    attrs = (ROOT / '.gitattributes').read_bytes()
    updated = attrs + (b'\n# Frozen scientific hashes refer to original bytes, including line endings.\n'
        b'/analysis/** -text\n/experiments/** -text\n/src/** -text\n/config/** -text\n'
        b'/*.py -text\n/results/** -text\n/README.md -text\n/active_release.json -text\n')
    paths, bindings = [], {}
    listed = subprocess.check_output(['git', 'ls-files', '-z'], cwd=ROOT)
    selected = [ROOT / name.decode('utf-8') for name in listed.split(b'\0') if name]
    selected.append(Path(__file__))
    for source in sorted(set(selected)):
        relative = source.relative_to(ROOT)
        if not source.is_file() or relative.parts[0] == 'validation_sync':
            continue
        if relative.parts[0] not in ('analysis', 'experiments', 'src', 'config', 'results') and not (
                source.suffix == '.py' or relative.as_posix() in ('README.md', 'active_release.json')):
            continue
        data = source.read_bytes()
        assert len(data) < 50 * 1024**2 and not sync.SECRET.search(data), relative
        sync.atomic(sync.WORKTREE / relative, data)
        paths.append(relative.as_posix())
        bindings[relative.as_posix()] = hashlib.sha256(data).hexdigest()
    sync.atomic(sync.WORKTREE / '.gitattributes', updated)
    paths.append('.gitattributes')
    evidence = {
        'status': 'original_bytes_captured_before_fixing_git_text_conversion', 'at_local': sync.now(),
        'previous_main': previous, 'source_sha256': bindings,
        'reason': 'Default CRLF normalization changed a frozen RUN JSON digest in the first workspace commit.',
        'original_scientific_files_unchanged': True,
        'future_commits_preserve_original_scientific_file_bytes': True,
        'branches': ['main'], 'new_quality_scores': 0}
    sync.atomic(sync.WORKTREE / PREFIX / 'frozen_bytes_correction.json', sync.encoded(evidence))
    paths.append((PREFIX / 'frozen_bytes_correction.json').as_posix())
    proof = sync.read(ROOT / 'analysis/nystrom_tuning_cost_inventory_qa_20261005/verification.json')
    for source, expected in proof['source_sha256'].items():
        relative = Path(source).relative_to(ROOT).as_posix()
        assert bindings[relative] == expected, relative

    observer = psutil.Process(sync.read(sync.OUT / 'owner.lock')['pid'])
    assert str(ROOT / 'analysis/watch_validations_main_v2_20261005.py') in observer.cmdline()
    parent = observer.parent()
    assert parent is not None and parent.cmdline()[1:] == observer.cmdline()[1:]
    suspended = []
    try:
        for process in (observer, parent):
            process.suspend()
            suspended.append(process)
        assert all(p.pid == observer.pid or p.name().lower() == 'conhost.exe' for p in parent.children(recursive=True))
        assert sync.git('rev-parse', 'HEAD') == previous
        for offset in range(0, len(paths), 50):
            sync.git('add', '--', *paths[offset:offset + 50])
        changed = set(sync.git('-c', 'core.quotepath=false', 'diff', '--cached', '--name-only').splitlines())
        assert changed and changed <= set(paths)
        sync.git('commit', '-m', '保留冻结源码和运行记录原始字节，修正Git换行转换')
        commit = sync.git('rev-parse', 'HEAD')
        for source, expected in proof['source_sha256'].items():
            relative = Path(source).relative_to(ROOT).as_posix()
            blob = subprocess.check_output(['git', 'show', f'{commit}:{relative}'], cwd=ROOT)
            assert hashlib.sha256(blob).hexdigest() == expected, relative
        assert (ROOT / '.gitattributes').read_bytes() == attrs
        sync.git('push', 'origin', 'HEAD:refs/heads/main', timeout=180)
        assert sync.git('ls-remote', '--heads', 'origin').splitlines() == [f'{commit}\trefs/heads/main']
        sync.atomic(ROOT / '.gitattributes', updated)
        watcher.advance_source_index(commit)
        receipt = {'status': 'passed_frozen_bytes_preserved_and_only_main_pushed', 'at_local': sync.now(),
            'commit': commit, 'previous_main': previous, 'files_changed': len(changed),
            'frozen_cost_inventory_source_hashes_checked_from_actual_git_blobs': len(proof['source_sha256']),
            'original_scientific_sources_not_modified': True, 'remote_branches': ['main'],
            'url': f'https://github.com/Zagadka-3906/stock-return-prediction/commit/{commit}'}
        with (OUT / 'frozen_bytes_receipt.json').open('x', encoding='utf-8') as stream:
            json.dump(receipt, stream, ensure_ascii=False, indent=2)
        print(json.dumps(receipt, ensure_ascii=False), flush=True)
    finally:
        for process in reversed(suspended):
            if process.is_running():
                process.resume()


if __name__ == '__main__':
    main()
