"""Complete only the explicit staged implementation export after ignored log files."""
from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'analysis'))
import sync_validated_rounds_github_20261005 as sync


def main():
    assert not (ROOT / 'results/optimization_20261003_r61.json').exists()
    prefix = Path('validation_sync/implementation_controls_nystrom_20261005')
    directory = sync.WORKTREE / prefix
    manifest = sync.read(directory / 'manifest.json')
    assert manifest['status'] == 'passed_implementation_controls_archived'
    sources = [Path(path) for path in manifest['source_sha256'] if Path(path).suffix == '.py']
    allowed = {p.relative_to(sync.WORKTREE).as_posix() for p in directory.rglob('*') if p.is_file()}
    allowed.update(p.relative_to(ROOT).as_posix() for p in sources)
    allowed.add('analysis/' + Path(__file__).name)
    assert set(sync.git('diff', '--cached', '--name-only').splitlines()) <= allowed
    for path, digest in manifest['source_sha256'].items():
        assert sync.sha(Path(path).read_bytes()) == digest, path
    # Proof JSON and logs keep their exact source bytes, including Windows line endings.
    attrs = directory / '.gitattributes'
    if attrs.exists():
        assert attrs.read_text(encoding='utf-8') == '* -text\n'
    else:
        with attrs.open('x', encoding='utf-8') as stream:
            stream.write('* -text\n')
    allowed.add(attrs.relative_to(sync.WORKTREE).as_posix())
    for original in sources:
        assert original.read_bytes() == (sync.WORKTREE / original.relative_to(ROOT)).read_bytes()
    original = Path(__file__)
    destination = Path('analysis') / original.name
    sync.atomic(sync.WORKTREE / destination, original.read_bytes())
    allowed.add(destination.as_posix())
    paths = sorted(allowed)
    for offset in range(0, len(paths), 50):
        sync.git('add', '-f', '--', *paths[offset:offset + 50])
        sync.git('add', '--renormalize', '--', *paths[offset:offset + 50])
    assert set(sync.git('diff', '--cached', '--name-only').splitlines()) == allowed
    for path, digest in manifest['source_sha256'].items():
        source = Path(path)
        if source.suffix == '.py':
            continue
        exported = prefix / source.relative_to(ROOT)
        blob = sync.git('rev-parse', ':' + exported.as_posix())
        data = __import__('subprocess').check_output(['git', 'cat-file', 'blob', blob], cwd=sync.WORKTREE)
        assert sync.sha(data) == digest, exported
    sync.git('commit', '-m', '归档Nyström二十次年度拟合、四完整候选核验及推理接口恢复证据')
    commit = sync.git('rev-parse', 'HEAD')
    sync.git('push', 'origin', f'HEAD:refs/heads/{sync.BRANCH}')
    assert sync.git('ls-remote', '--heads', 'origin', f'refs/heads/{sync.BRANCH}').split()[0] == commit
    assert not sync.git('status', '--porcelain', '--untracked-files=no')
    receipt = {'status': 'pushed_and_remote_head_verified', 'at_local': sync.now(), 'commit': commit,
        'files': len(paths), 'exact_json_and_log_bytes_verified_in_git_objects': True,
        'url': f'https://github.com/Zagadka-3906/stock-return-prediction/tree/{sync.BRANCH}/{prefix.as_posix()}'}
    with (sync.OUT / 'nystrom_implementation_receipt.json').open('x', encoding='utf-8') as stream:
        json.dump(receipt, stream, ensure_ascii=False, indent=2)
    print(json.dumps(receipt, ensure_ascii=False), flush=True)


if __name__ == '__main__':
    main()
