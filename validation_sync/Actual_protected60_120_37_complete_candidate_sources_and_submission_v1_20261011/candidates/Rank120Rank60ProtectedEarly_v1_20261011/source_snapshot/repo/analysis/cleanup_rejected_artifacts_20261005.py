"""User-authorized removal of obsolete model artifacts, preserving live evidence."""
from pathlib import Path
from collections import Counter
from datetime import datetime
import argparse
import hashlib
import json
import os
import re
import sys
import psutil

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
OUT = A / 'rejected_artifact_cleanup_20261005'
ARCHIVE = ROOT.parent / '赛题五_历史归档_20261001'
BACKUPS = [ROOT.parent / name for name in (
    '赛题五_清理备份_20261001', '赛题五_清理备份_20260926_003839')]
WEIGHTS = {'.joblib', '.ubj', '.pkl', '.pt', '.pth', '.cbm'}
CACHES = {'.npy', '.npz', '.parquet', '.csv'}
RECORDS = {'.json', '.jsonl', '.md', '.py', '.yaml', '.yml', '.toml'}


def now():
    return datetime.now().isoformat(timespec='seconds')


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8-sig'))


def sha(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as stream:
        for block in iter(lambda: stream.read(4 * 1024**2), b''):
            h.update(block)
    return h.hexdigest()


def create(path, value):
    with Path(path).open('x', encoding='utf-8') as stream:
        json.dump(value, stream, ensure_ascii=False, indent=2)
        stream.write('\n')


def files(folder):
    if not folder.exists():
        return
    for directory, dirs, names in os.walk(folder, followlinks=False):
        dirs[:] = [name for name in dirs if name not in {
            '.git', '.venv', '.tools', 'node_modules', '__pycache__'}
            and not (Path(directory) / name).is_symlink()
            and not (Path(directory) / name).is_junction()]
        for name in names:
            p = Path(directory) / name
            if p.is_file() and not p.is_symlink():
                yield p


def model_text(path):
    return path.suffix == '.txt' and (
        path.name.startswith(('model_', 'fold_', 'final_', 'xgboost_', 'nn_'))
        or 'models' in path.parts)


def project_jobs():
    jobs = []
    for process in psutil.process_iter(['pid', 'name', 'cmdline', 'create_time']):
        try:
            item = process.info
            cmd = item['cmdline'] or []
            scripts = [s for s in cmd if s.lower().endswith('.py')
                       and str(ROOT).lower() in s.lower()]
            if 'python' in (item['name'] or '').lower() and scripts:
                jobs.append({'pid': item['pid'], 'creation_time': item['create_time'],
                             'cmdline': cmd})
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    return jobs


def protected_inputs():
    """Follow actual source seals recursively; protect all current model banks too."""
    protected = set()
    queue, visited, queued, seen = [], set(), set(), set()

    def absolute_string(value):
        return len(value) > 2 and (value[1] == ':' and value[2] in '\\/'
                                  or value.startswith(('\\\\', '//')))

    def add(path):
        name = str(path)
        if name in seen:
            return
        seen.add(name)
        p = Path(path)
        if not p.is_absolute():
            p = ROOT / p
        try:
            p = p.resolve()
            if not p.is_file():
                return
        except (OSError, ValueError):
            return
        protected.add(p)
        if p.suffix == '.json' and p not in queued:
            queue.append(p)
            queued.add(p)

    def walk(value):
        if isinstance(value, dict):
            for key, item in value.items():
                if isinstance(key, str) and absolute_string(key):
                    add(key)
                if key.endswith('sha256') and isinstance(item, dict):
                    for name, digest in item.items():
                        if isinstance(name, str) and isinstance(digest, str) and re.fullmatch('[0-9a-f]{64}', digest):
                            add(name)
                walk(item)
        elif isinstance(value, list):
            for item in value:
                walk(item)
        elif isinstance(value, str):
            try:
                if absolute_string(value):
                    add(value)
            except (OSError, ValueError):
                pass

    add(ROOT / 'active_release.json')
    for path in A.glob('*.json'):
        if any(word in path.stem for word in ('plan', 'run', 'launch', 'storage', 'followup')):
            add(path)
    for number in (65, 66, *range(67, 85)):
        folder = A / f'optimization_20261003_r{number}'
        for name in ('protocol.json', 'selection.json'):
            add(folder / name)
    jobs = project_jobs()
    for job in jobs:
        for arg in job['cmdline']:
            if arg.lower().endswith(('.json', '.py')):
                add(arg)
    for name in ('data', 'models', 'deliveries', 'delivery_day_connected_20261003'):
        for path in files(ROOT / name):
            add(path)
    for number in (29, 30, 65, 66):
        for path in files(ROOT / f'candidates/optimization_20261003_r{number}'):
            add(path)
    for folder in A.iterdir():
        if folder.is_dir() and any(word in folder.name for word in ('bank', 'future', 'preflight')):
            for path in files(folder):
                add(path)
    while queue:
        p = queue.pop()
        if p in visited:
            continue
        visited.add(p)
        # JSON evidence only; never read feature matrices or test labels.
        if p.stat().st_size < 10 * 1024**2:
            walk(read(p))
    return protected, jobs, visited


def plan():
    OUT.mkdir(exist_ok=True)
    assert not (OUT / 'plan.json').exists(), 'Use the existing frozen plan; never overwrite.'
    protected, jobs, seals = protected_inputs()
    allowed = [ROOT.resolve(), ARCHIVE.resolve(), *(p.resolve() for p in BACKUPS)]
    proposed = {}
    retained = []
    evidence = set()

    def propose(path, category, record=None, score=None):
        path = path.resolve()
        assert any(path.is_relative_to(base) for base in allowed), path
        assert path.suffix in WEIGHTS | CACHES or model_text(path), path
        if path.name in {'训练集.csv', '测试集_X.csv', '测试集_Y.csv'} or (
            path.suffix in CACHES and path.name.lower().startswith(
                ('test_y', 'testy', 'y_test', 'labels', 'targets'))):
            retained.append({'path': str(path), 'reason': 'original_input_or_label_named_alias'})
            return
        if path in protected:
            retained.append({'path': str(path), 'reason': 'selected_or_live_frozen_dependency'})
            return
        if record:
            evidence.add(Path(record).resolve())
        st = path.stat()
        proposed[path] = {'path': str(path), 'bytes': st.st_size, 'identity': [st.st_dev, st.st_ino],
            'mtime_ns': st.st_mtime_ns, 'hardlinks_before': st.st_nlink, 'category': category,
            'retained_record': str(record) if record else None, 'completed_scheme_score': score,
            'artifact_kind': 'model_weight' if path.suffix in WEIGHTS or model_text(path) else 'prediction_or_derived_cache'}

    board = read(ROOT / 'results/all_model_rankings_20261003.json')
    best_score = read(A / 'optimization_20261003_r66/selection.json')['winner']['connected_final_score']
    for base in ('analysis', 'candidates'):
        for folder in (ROOT / base).glob('optimization_20261003*'):
            match = re.fullmatch(r'optimization_20261003(?:_r(\d+))?', folder.name)
            if not folder.is_dir() or not match:
                continue
            number = int(match.group(1) or 1)
            if number >= 65 or number in (29, 30):
                continue
            result = ROOT / 'results' / (folder.name + '.json')
            if not result.exists():
                continue
            completed = read(result)
            score = completed.get('winner', {}).get('connected_final_score')
            if completed.get('status') != 'complete' or score is None or score >= best_score:
                continue
            if base == 'candidates':
                proof = folder / 'verification.json'
                if not proof.exists() or read(proof).get('status') != 'passed':
                    continue
                evidence.add(proof)
            for path in files(folder):
                if path.suffix in WEIGHTS | CACHES or model_text(path):
                    propose(path, 'completed_unselected_scheme_artifact', result, score)
            evidence.update(p for p in files(folder) if p.suffix in RECORDS)

    for backup in BACKUPS:
        record = backup / 'cleanup_plan.json'
        original_plan = read(record)
        previous = {row['path'] for row in original_plan.get('removals', [])}
        # The earlier backup has a different schema; retain its whole evidence tree.
        for path in files(backup):
            relative = path.relative_to(backup)
            if relative.parts[0] not in ('analysis', 'experiments'):
                continue
            if previous and relative.as_posix() not in previous:
                continue
            if path.suffix in WEIGHTS | CACHES or model_text(path):
                propose(path, 'previously_retired_historical_backup_artifact', record)
        evidence.update(p for p in files(backup) if p.suffix in RECORDS)

    for base in (ARCHIVE / 'experiments', ARCHIVE / 'analysis/all_models_test_20260929',
                 ARCHIVE / 'analysis/slow8_monthly_validation_20260929',
                 ARCHIVE / 'analysis/top2_training_validation_20260929'):
        records = [p for p in files(base) if p.suffix in RECORDS]
        evidence.update(records)
        record = next((p for p in records if p.name in ('results.json', 'all_results.json', 'metrics.json')), None)
        if record is None:
            continue
        for path in files(base):
            if path.suffix in WEIGHTS | CACHES or model_text(path):
                propose(path, 'retired_historical_experiment_artifact', record)

    connected = A / 'connected_validation_20261002'
    record = ROOT / 'results/all_model_rankings_20261003.json'
    for path in connected.glob('connected_pred_raw*.npy'):
        propose(path, 'unused_historical_connected_prediction_cache', record)
    evidence.update(p for p in files(connected) if p.suffix in RECORDS)
    evidence.update((ROOT / 'results').glob('*.json'))
    evidence.add(ROOT / 'results/all_model_rankings_20261003.csv')
    evidence = {p.resolve() for p in evidence if p.is_file()}
    records = {str(p): {'bytes': p.stat().st_size, 'sha256': sha(p)} for p in sorted(evidence)}
    for index, (path, row) in enumerate(sorted(proposed.items())):
        row['sha256'] = sha(path)
        if index % 200 == 0:
            print(json.dumps({'stage': 'hashing_cleanup_artifacts', 'hashed': index, 'total': len(proposed)}), flush=True)
    value = {'status': 'frozen_user_authorized_rejected_artifact_cleanup', 'at_local': now(),
        'authorization': '直接删除之前验证过不采用的模型，仅保留记录和分数等信息，以免存储空间不足；历史副本与弃用缓存已获授权清理',
        'allowed_absolute_roots': list(map(str, allowed)), 'source_sha256': sha(__file__),
        'deletions': list(proposed.values()), 'logical_bytes': sum(row['bytes'] for row in proposed.values()),
        'retained_live_dependencies': retained, 'protected_paths': sorted(map(str, protected)),
        'records_preserved_sha256': records, 'recursive_live_evidence_json': sorted(map(str, seals)),
        'jobs_before': jobs, 'best_complete_score_at_plan': best_score,
        'board_records_at_plan': board['summary']['connected_exact_records'],
        'D_free_bytes_before': psutil.disk_usage('D:/').free,
        'raw_data_preserved': True, 'test_labels_read': False, 'new_model_fits': 0, 'new_quality_scores': 0}
    create(OUT / 'plan.json', value)
    print(json.dumps({'status': value['status'], 'files': len(proposed), 'logical_GiB': value['logical_bytes'] / 2**30,
        'retained_dependency_files': len(retained), 'record_files': len(records)}, ensure_ascii=False), flush=True)


def execute():
    value = read(OUT / 'plan.json')
    assert sha(__file__) == value['source_sha256']
    assert not (OUT / 'verification.json').exists()
    allowed = [Path(p).resolve() for p in value['allowed_absolute_roots']]
    protected, _, _ = protected_inputs()
    for name, record in value['records_preserved_sha256'].items():
        assert sha(name) == record['sha256'], name
    missing_before = {str(p) for p in protected if not p.exists()}
    deleted, skipped = [], []
    with (OUT / 'deletions.jsonl').open('x', encoding='utf-8') as journal:
        for row in value['deletions']:
            path = Path(row['path'])
            assert path.resolve() == path and any(path.is_relative_to(base) for base in allowed), path
            assert not path.is_symlink() and not path.is_junction(), path
            if path in protected:
                skipped.append({'path': str(path), 'reason': 'new_live_dependency_since_plan'})
                continue
            st = path.stat()
            assert [st.st_dev, st.st_ino] == row['identity'] and st.st_size == row['bytes'] and st.st_mtime_ns == row['mtime_ns'], path
            assert sha(path) == row['sha256'], path
            try:
                path.unlink()
            except PermissionError as error:
                skipped.append({'path': str(path), 'reason': 'open_read_seal_or_access_denied', 'winerror': error.winerror})
                continue
            done = {**row, 'deleted_at_local': now()}
            journal.write(json.dumps(done, ensure_ascii=False) + '\n')
            journal.flush()
            deleted.append(done)
            if len(deleted) % 200 == 0:
                print(json.dumps({'stage': 'deleted', 'files': len(deleted), 'logical_GiB': sum(r['bytes'] for r in deleted)/2**30}), flush=True)
    assert {str(p) for p in protected if not p.exists()} == missing_before
    for name, record in value['records_preserved_sha256'].items():
        assert sha(name) == record['sha256'], name
    after = psutil.disk_usage('D:/').free
    jobs = []
    for old in value['jobs_before']:
        try:
            p = psutil.Process(old['pid'])
            live = p.create_time() == old['creation_time'] and p.cmdline() == old['cmdline']
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            live = False
        jobs.append({'pid': old['pid'], 'same_owned_process_live_after': live})
    counts = Counter(row['artifact_kind'] for row in deleted)
    categories = Counter(row['category'] for row in deleted)
    result = {'status': 'passed_user_authorized_rejected_artifact_cleanup', 'at_local': now(),
        'deleted_files': len(deleted), 'deleted_logical_bytes': sum(row['bytes'] for row in deleted),
        'deleted_by_kind': dict(counts), 'deleted_by_category': dict(categories),
        'skipped': skipped, 'D_free_bytes_after': after,
        'D_free_bytes_change': after-value['D_free_bytes_before'],
        'disk_change_includes_concurrent_training_writes_and_hardlinks': True,
        'record_files_verified_unchanged': len(value['records_preserved_sha256']),
        'new_missing_protected_dependencies': 0, 'jobs_after': jobs,
        'processes_stopped_or_restarted_by_cleanup': 0, 'raw_data_preserved': True,
        'C_project_data_written': False, 'E_project_data_written': False,
        'test_labels_read': False, 'new_model_fits': 0, 'new_quality_scores': 0,
        'historical_metadata_describes_deleted_weights_not_present_weights': True,
        'live_frozen_bank_dependencies_retained_until_workflows_finish': True}
    create(OUT / 'verification.json', result)
    print(json.dumps(result, ensure_ascii=False), flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--execute', action='store_true')
    args = parser.parse_args()
    execute() if args.execute else plan()
