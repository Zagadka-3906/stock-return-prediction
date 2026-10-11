"""Remove verified historical copies and unused caches, preserving live dependencies."""
from pathlib import Path
import argparse
import hashlib
import json
import os
import psutil
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'analysis'))
import sync_validated_rounds_github_20261005 as sync
OUT = ROOT / 'analysis/authorized_history_cache_cleanup_20261005'


def sha(path):
    digest = hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            digest.update(block)
    return digest.hexdigest()


def create(path, value):
    with path.open('x', encoding='utf-8') as stream:
        json.dump(value, stream, ensure_ascii=False, indent=2)
        stream.write('\n')


def protected_inputs():
    protected, digests = set(), {}
    sources = [
        'analysis/optimization_20261003_r60/protocol.json',
        'analysis/optimization_20261003_r60/selection.json',
        'analysis/nystrom_ridge_bank_20261004/protocol.json',
        'analysis/nystrom_ridge_bank_20261004/training_execution_scope.json',
        'analysis/nystrom_ridge_future_models_qa_20261004/verification.json',
        'analysis/nystrom_ridge_complete_scheme_preflight_20261004/frozen_before_controls.json',
        'analysis/latest_graph_joint_round63_source_preflight_20261005/verification.json',
        'analysis/latest_joint_zero_axis_policy_preflight_20261005/verification.json',
        'analysis/nystrom_evidence_audit_resume_20261005/plan.json',
        'analysis/nystrom_count_resume_20261005/plan.json',
        'analysis/official_worker_frontier_execution_20261004/verification.json',
        'analysis/official_worker_frontier_scope_audit_20261004.json',
        'analysis/neural_width_frontier_scope_audit_20261004.json',
    ]
    def walk(value):
        if isinstance(value, dict):
            for key in ('input_sha256', 'frozen_sha256', 'source_sha256'):
                fields = value.get(key)
                if isinstance(fields, dict):
                    for name, digest in fields.items():
                        if isinstance(name, str) and isinstance(digest, str) and len(digest) == 64:
                            path = Path(name)
                            path = path if path.is_absolute() else ROOT / path
                            protected.add(path.resolve())
                            digests[path.resolve()] = digest
            for item in value.values():
                walk(item)
        elif isinstance(value, list):
            for item in value:
                walk(item)
        elif isinstance(value, str):
            try:
                path = Path(value)
                if path.is_absolute() and path.exists() and path.is_file():
                    protected.add(path.resolve())
            except (OSError, ValueError):
                pass
    for name in sources:
        path = ROOT / name
        if path.exists():
            protected.add(path.resolve())
            walk(sync.read(path))
    for entry in sync.read(ROOT / 'results/all_model_rankings_20261003.json')['source_manifest']:
        path = Path(entry['path'])
        path = path if path.is_absolute() else ROOT / path
        protected.add(path.resolve())
        digests[path.resolve()] = entry['sha256']
    # Keep current best, current replay source, pending family and formal deliverables.
    keep = ['candidates/optimization_20261003_r29', 'candidates/optimization_20261003_r55',
            'candidates/optimization_20261003_r60', 'analysis/optimization_20261003_r55',
            'analysis/optimization_20261003_r60', 'analysis/nystrom_ridge_bank_20261004',
            'analysis/nystrom_ridge_future_models_qa_20261004',
            'analysis/nystrom_ridge_complete_scheme_preflight_20261004', 'deliveries']
    for name in keep:
        for path in (ROOT / name).rglob('*'):
            if path.is_file():
                protected.add(path.resolve())
    for number in (61, 62, 63):
        for path in (ROOT / f'analysis/optimization_20261003_r{number}').rglob('*'):
            if path.is_file():
                protected.add(path.resolve())
    protected.add((ROOT / 'active_release.json').resolve())
    protected.add((ROOT / 'analysis/optimization_20261003_r30/calibrated_validation.csv').resolve())
    return protected, digests


def plan():
    OUT.mkdir(exist_ok=True)
    protected, digests = protected_inputs()
    remote = sync.git('ls-remote', '--heads', 'origin', f'refs/heads/{sync.BRANCH}').split()[0]
    assert remote == sync.git('rev-parse', 'HEAD')
    assert not sync.git('status', '--porcelain', '--untracked-files=no')
    assert sync.git('show', 'HEAD:validation_sync/history/files.json').encode('utf-8') == (sync.WORKTREE / 'validation_sync/history/files.json').read_text(encoding='utf-8').strip().encode('utf-8')
    deletions = []
    for folder in (ROOT / 'analysis').glob('optimization_20261003*'):
        if not folder.is_dir():
            continue
        number = 1 if folder.name == 'optimization_20261003' else int(folder.name.rsplit('_r', 1)[1])
        if number > 60 or number in (55, 60):
            continue
        published = ROOT / f'results/{folder.name}.json'
        if not published.exists() or sync.read(published)['status'] != 'complete':
            continue
        for path in folder.rglob('*.csv'):
            if path.name not in ('submission.csv', 'calibrated_validation.csv'):
                continue
            if path.resolve() in protected or path.is_symlink() or path.stat().st_size < 10 * 1024**2:
                continue
            deletions.append({'path': str(path), 'bytes': path.stat().st_size,
                              'category': 'unused_completed_round_prediction_cache', 'round': number})
    retained_by_hash = {}
    for path, digest in digests.items():
        if path.suffix in ('.joblib', '.ubj', '.pth', '.pt', '.pkl', '.txt') and path.exists():
            retained_by_hash.setdefault(digest, path)
    verified_retained = set()
    for folder in (ROOT / 'candidates').glob('optimization_20261003*'):
        if not folder.is_dir():
            continue
        number = 1 if folder.name == 'optimization_20261003' else int(folder.name.rsplit('_r', 1)[1])
        if number in (29, 55, 60) or number > 60:
            continue
        verification = folder / 'verification.json'
        if not verification.exists() or sync.read(verification)['status'] != 'passed':
            continue
        for path in folder.rglob('*'):
            if not path.is_file() or path.suffix not in ('.joblib', '.ubj', '.pth', '.pt', '.pkl', '.txt'):
                continue
            if path.resolve() in protected or path.is_symlink():
                continue
            digest = sha(path)
            retained = retained_by_hash.get(digest)
            if retained is None:
                continue
            if retained not in verified_retained:
                assert sha(retained) == digest
                verified_retained.add(retained)
            deletions.append({'path': str(path), 'bytes': path.stat().st_size,
                              'category': 'unused_duplicate_tested_model_copy', 'round': number,
                              'sha256': digest, 'retained_identical_model': str(retained)})
    # Remote-confirmed historical export copies are independent of scientific execution.
    tracked = sync.git('ls-files', 'validation_sync').splitlines()
    for relative in tracked:
        parts = Path(relative).parts
        historical = len(parts) > 1 and (parts[1] == 'history' or
                     parts[1].startswith('round') and parts[1][5:].isdigit() and int(parts[1][5:]) < 60)
        path = sync.WORKTREE / relative
        if not historical or not path.exists() or not path.is_file():
            continue
        # Compare the committed representation, including the repository's LF policy.
        # The separate SHA-256 below protects the exact local bytes before deletion.
        blob = subprocess.check_output(['git', 'hash-object', '--path=' + relative, str(path)], cwd=sync.WORKTREE, text=True).strip()
        assert sync.git('rev-parse', 'HEAD:' + relative) == blob
        deletions.append({'path': str(path), 'bytes': path.stat().st_size,
                          'category': 'remote_verified_history_export_copy', 'git_path': relative,
                          'git_blob': blob, 'sha256': sha(path)})
    result = {'status': 'frozen_authorized_cleanup_plan', 'at_local': sync.now(),
              'authorization': '用户确认清理历史副本与弃用缓存，保留当前方案及继续验证依赖；不使用C盘，不足时可用E盘',
              'remote_verified_commit': remote, 'protected_paths': sorted(map(str, protected)),
              'deletions': deletions, 'logical_bytes': sum(item['bytes'] for item in deletions),
              'D_free_bytes_before': psutil.disk_usage('D:/').free,
              'source_sha256': sha(Path(__file__)), 'raw_data_andoriginal_model_banks_preserved': True}
    create(OUT / 'plan.json', result)
    print(json.dumps({'status': result['status'], 'files': len(deletions),
                      'logical_bytes': result['logical_bytes'], 'protected_paths': len(protected)}, ensure_ascii=False), flush=True)
    return result


def execute(value):
    assert sha(Path(__file__)) == value['source_sha256']
    protected = set(map(Path, value['protected_paths']))
    remote = sync.git('ls-remote', '--heads', 'origin', f'refs/heads/{sync.BRANCH}').split()[0]
    assert remote == value['remote_verified_commit']
    exports = [item['git_path'] for item in value['deletions'] if 'git_path' in item]
    for offset in range(0, len(exports), 50):
        sync.git('update-index', '--skip-worktree', '--', *exports[offset:offset + 50])
    deleted, missing_protected_before = [], [str(path) for path in protected if not path.exists()]
    journal = OUT / 'deletions.jsonl'
    with journal.open('x', encoding='utf-8') as stream:
        for item in value['deletions']:
            path = Path(item['path'])
            allowed = ROOT if item['category'] != 'remote_verified_history_export_copy' else sync.WORKTREE
            assert path.resolve().is_relative_to(allowed.resolve())
            assert path.resolve() not in protected and not path.is_symlink()
            assert path.stat().st_size == item['bytes']
            if 'sha256' in item:
                assert sha(path) == item['sha256']
            path.unlink()
            stream.write(json.dumps(item, ensure_ascii=False) + '\n')
            stream.flush()
            deleted.append(item)
    assert [str(path) for path in protected if not path.exists()] == missing_protected_before
    assert not sync.git('status', '--porcelain', '--untracked-files=no')
    after = psutil.disk_usage('D:/').free
    result = {'status': 'passed_authorized_history_andunused_cache_cleanup', 'at_local': sync.now(),
              'deleted_files': len(deleted), 'deleted_logical_bytes': sum(item['bytes'] for item in deleted),
              'D_free_bytes_after': after, 'D_free_bytes_change': after - value['D_free_bytes_before'],
              'protected_paths': len(protected), 'no_new_missing_protected_dependencies': True,
              'C_project_scratch_absent': not Path('C:/Users/esesl/.codex/contest5_compute_scratch_20261005').exists(),
              'remote_history_retained': True, 'original_model_banks_preserved_for_frozen_validation_dependencies': True,
              'new_model_fits': 0, 'new_quality_scores': 0, 'test_labels_read': False}
    create(OUT / 'verification.json', result)
    print(json.dumps(result, ensure_ascii=False), flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--execute', action='store_true')
    args = parser.parse_args()
    value = plan()
    if args.execute:
        execute(value)
