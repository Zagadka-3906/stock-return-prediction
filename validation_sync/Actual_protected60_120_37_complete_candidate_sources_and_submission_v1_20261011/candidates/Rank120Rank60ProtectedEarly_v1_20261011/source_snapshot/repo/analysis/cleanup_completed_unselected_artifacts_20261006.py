"""Delete completed, unused artifacts; retain scores and pending dependencies."""
from pathlib import Path
from collections import Counter
from datetime import datetime
import argparse
import hashlib
import json
import subprocess
import time

import psutil
import cleanup_rejected_artifacts_20261005 as previous

ROOT = previous.ROOT
A = ROOT / 'analysis'
OUT = A / 'completed_unselected_artifact_cleanup_20261006'
OLD = A / 'rejected_artifact_cleanup_20261005'
QA_ROOTS = (
    'official_extended_capacity_qa_20261004',
    'official_native_thread_capacity_qa_20261004',
    'official_worker_frontier_forward_qa_20261004',
    'official_worker_frontier_reverse_qa_20261004',
    'official_parallel_capacity_qa_20261004',
    'parallel_candidate_scoring_qa_20261004',
    'parallel_candidate_scoring_four_qa_20261004',
    'late_context_initialization_recovery_v2_20261004',
    'cross_round_official_reuse_qa_20261003',
    'mapped_cross_round_reuse_qa_20261003',
    'validation_parse_cache_qa_20261003',
    'validation_parse_cache_full_oof_qa_20261003',
    'official_score_cache_qa_20261003',
)


def now():
    return datetime.now().isoformat(timespec='seconds')


def sha(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def read(path):
    return previous.read(path)


def create(path, value):
    previous.create(path, value)


def identity(path):
    st = path.stat()
    return {'bytes': st.st_size, 'device': st.st_dev, 'inode': st.st_ino,
            'mtime_ns': st.st_mtime_ns, 'hardlinks': st.st_nlink}


def unchanged(path, row):
    current = identity(path)
    assert all(current[k] == row[k] for k in ('bytes', 'device', 'inode', 'mtime_ns')), path


def protect():
    protected, jobs, seals = previous.protected_inputs()
    # A missing process does not make its incomplete experiment rejected.
    for number in range(67, 89):
        for parent in ('analysis', 'candidates'):
            for path in previous.files(ROOT / parent / f'optimization_20261003_r{number}'):
                protected.add(path.resolve())
    # Retain all current champion artifacts except disposable scoring-worker CSVs.
    for number in (65, 66):
        for path in previous.files(A / f'optimization_20261003_r{number}'):
            disposable = path.suffix == '.csv' and 'parallel_official_workers' in path.parts
            if not disposable:
                protected.add(path.resolve())
    return protected, jobs, seals


def verify_selected():
    active = read(ROOT / 'active_release.json')
    for key in ('manifest', 'submission'):
        assert sha(active[key]) == active[key + '_sha256'], active[key]
    packages = [(Path(active['delivery_directory']), read(active['manifest'])['artifacts'])]
    for number in (65, 66):
        folder = ROOT / f'candidates/optimization_20261003_r{number}'
        packages.append((folder, read(folder / 'manifest.json')['files']))
    checks = []
    for folder, entries in packages:
        for name, record in entries.items():
            path = folder / name
            assert path.resolve().is_relative_to(folder.resolve()), path
            assert '测试集_Y' not in name and 'TestY' not in name, name
            assert sha(path) == record['sha256'], path
        checks.append({'folder': str(folder), 'verified_files': len(entries)})
    roots = read(A / 'artifact_cleanup_selected_roots_retention_plan_20261005.json')
    for name, digest in roots['input_sha256'].items():
        assert sha(name) == digest, name
    return checks


def plan():
    assert not OUT.exists(), 'Keep each completed cleanup immutable; use a new version.'
    OUT.mkdir()
    protected, jobs, seals = protect()
    tracked = set(subprocess.check_output(['git', 'ls-files', '-z'], cwd=ROOT).split(b'\0'))
    best = read(ROOT / 'results/optimization_20261003_r66.json')['winner']['connected_final_score']
    proposed, retained = {}, []

    def propose(path, category, record, score=None):
        path = path.resolve()
        assert path.is_relative_to(ROOT.resolve()) and path != ROOT.resolve(), path
        assert not path.is_symlink() and not path.is_junction(), path
        if path.suffix not in previous.WEIGHTS | previous.CACHES and not previous.model_text(path):
            return
        if path.name in {'训练集.csv', '测试集_X.csv', '测试集_Y.csv'} or path.name.lower().startswith(
                ('test_y', 'testy', 'y_test', 'labels', 'targets')):
            retained.append({'path': str(path), 'reason': 'input_or_label_named_file'})
            return
        if path in protected or path.relative_to(ROOT).as_posix().encode('utf-8') in tracked:
            retained.append({'path': str(path), 'reason': 'adopted_pending_frozen_or_tracked_dependency'})
            return
        proposed[path] = {'path': str(path), **identity(path), 'category': category,
            'retained_evidence': str(record), 'completed_scheme_score': score,
            'kind': 'model_weight' if path.suffix in previous.WEIGHTS or previous.model_text(path)
                    else 'prediction_or_derived_cache'}

    for number in range(1, 65):
        if number in (29, 30):
            continue
        name = 'optimization_20261003' + (f'_r{number}' if number > 1 else '')
        record = ROOT / 'results' / (name + '.json')
        if not record.exists():
            continue
        result = read(record)
        score = result.get('winner', {}).get('connected_final_score')
        if result.get('status') != 'complete' or score is None or score >= best:
            continue
        for parent in ('analysis', 'candidates'):
            folder = ROOT / parent / name
            if parent == 'candidates':
                proof = folder / 'verification.json'
                if not proof.exists() or read(proof).get('status') != 'passed':
                    continue
            for path in previous.files(folder):
                propose(path, 'completed_unselected_scheme_artifact', record, score)
    for name in QA_ROOTS:
        folder = A / name
        record = folder / 'verification.json'
        if not record.exists() or read(record).get('status') != 'passed':
            continue
        for path in previous.files(folder):
            propose(path, 'completed_diagnostic_prediction_copy', record)
    for number in (65, 66):
        folder = A / f'optimization_20261003_r{number}'
        record = ROOT / 'results' / (folder.name + '.json')
        assert read(record)['status'] == 'complete'
        for path in previous.files(folder / 'parallel_official_workers'):
            if path.suffix == '.csv':
                propose(path, 'completed_champion_round_worker_scratch_copy', record)

    old_plan = read(OLD / 'plan.json')
    records = dict(old_plan['records_preserved_sha256'])
    for path in previous.files(ROOT):
        if path.is_relative_to(OUT):
            continue
        is_record = path.suffix in previous.RECORDS | {'.log', '.html'}
        is_text_record = path.suffix == '.txt' and not previous.model_text(path)
        is_score_table = path.suffix in {'.csv', '.tsv'} and path.is_relative_to(ROOT / 'results')
        if is_record or is_text_record or is_score_table:
            records[str(path.resolve())] = {'bytes': path.stat().st_size, 'sha256': sha(path)}
    for name, row in old_plan['records_preserved_sha256'].items():
        assert sha(name) == row['sha256'], name
    selected = verify_selected()
    artifact_protection = {}
    for path in sorted(protected):
        if path.suffix in previous.WEIGHTS | previous.CACHES or previous.model_text(path):
            row = identity(path)
            if path.suffix in previous.WEIGHTS or previous.model_text(path):
                row['sha256'] = sha(path)
            artifact_protection[str(path)] = row
    cache = {}
    for i, row in enumerate(proposed.values(), 1):
        key = (row['device'], row['inode'], row['bytes'], row['mtime_ns'])
        if key not in cache:
            cache[key] = sha(row['path'])
        row['sha256'] = cache[key]
        if i % 100 == 0:
            print(json.dumps({'stage': 'hashing_proposed_cleanup', 'files': i,
                              'total': len(proposed)}), flush=True)
    groups = Counter((row['device'], row['inode']) for row in proposed.values())
    unique = {(row['device'], row['inode']): row for row in proposed.values()}
    reclaimable = sum(row['bytes'] for key, row in unique.items() if groups[key] == row['hardlinks'])
    value = {'status': 'frozen_additional_user_authorized_completed_artifact_cleanup', 'at_local': now(),
        'authorization': '直接删除之前验证过不采用的模型，仅保留记录和分数等信息，以免存储空间不足',
        'source_sha256': {str(Path(__file__).resolve()): sha(__file__),
                         str(Path(previous.__file__).resolve()): sha(previous.__file__)},
        'allowed_absolute_root': str(ROOT.resolve()), 'deletions': list(proposed.values()),
        'logical_bytes': sum(row['bytes'] for row in proposed.values()),
        'unique_reclaimable_bytes_estimated_from_hardlinks': reclaimable,
        'retained_records_sha256': records, 'retained_artifacts': artifact_protection,
        'skipped_dependencies': retained, 'selected_packages_before': selected,
        'jobs_before': jobs, 'required_incomplete_rounds_retained': list(range(67, 89)),
        'prior_cleanup': read(OLD / 'verification.json'), 'best_complete_score': best,
        'D_free_bytes_before': psutil.disk_usage('D:/').free,
        'test_labels_read': False, 'new_model_fits': 0, 'new_quality_scores': 0}
    create(OUT / 'plan.json', value)
    print(json.dumps({'status': value['status'], 'files': len(proposed),
        'kinds': dict(Counter(row['kind'] for row in proposed.values())),
        'logical_GiB': value['logical_bytes']/2**30, 'estimated_reclaimable_GiB': reclaimable/2**30,
        'retained_records': len(records), 'retained_artifacts': len(artifact_protection)}, ensure_ascii=False), flush=True)


def execute():
    value = read(OUT / 'plan.json')
    assert not (OUT / 'deletions.jsonl').exists() and not (OUT / 'verification.json').exists()
    for name, digest in value['source_sha256'].items():
        assert sha(name) == digest, name
    protected, _, _ = protect()
    for name, row in value['retained_records_sha256'].items():
        assert sha(name) == row['sha256'], name
    for name, row in value['retained_artifacts'].items():
        unchanged(Path(name), row)
    verify_selected()
    deleted, skipped, digest_cache = [], [], {}
    before = psutil.disk_usage('D:/').free
    with (OUT / 'deletions.jsonl').open('x', encoding='utf-8') as journal:
        for row in value['deletions']:
            path = Path(row['path'])
            assert path.resolve() == path and path.is_relative_to(Path(value['allowed_absolute_root'])), path
            assert all(not parent.is_symlink() and not parent.is_junction()
                       for parent in (path, *path.parents) if parent.is_relative_to(ROOT)), path
            if path in protected:
                skipped.append({'path': str(path), 'reason': 'new_frozen_dependency'})
                continue
            unchanged(path, row)
            key = (row['device'], row['inode'], row['bytes'], row['mtime_ns'])
            if key not in digest_cache:
                digest_cache[key] = sha(path)
            assert digest_cache[key] == row['sha256'], path
            try:
                path.unlink()
            except PermissionError as error:
                skipped.append({'path': str(path), 'reason': 'locked_or_access_denied', 'winerror': error.winerror})
                continue
            done = {**row, 'deleted_at_local': now()}
            journal.write(json.dumps(done, ensure_ascii=False) + '\n')
            journal.flush()
            deleted.append(done)
            if len(deleted) % 100 == 0:
                print(json.dumps({'stage': 'deleted', 'files': len(deleted)}), flush=True)
    after = psutil.disk_usage('D:/').free
    for row in deleted:
        assert not Path(row['path']).exists(), row['path']
    for name, row in value['retained_records_sha256'].items():
        assert sha(name) == row['sha256'], name
    protected_weights = 0
    for name, row in value['retained_artifacts'].items():
        unchanged(Path(name), row)
        if 'sha256' in row:
            assert sha(name) == row['sha256'], name
            protected_weights += 1
    selected = verify_selected()
    old = value['prior_cleanup']
    old_absent = 0
    for line in (OLD / 'deletions.jsonl').read_text(encoding='utf-8').splitlines():
        row = json.loads(line)
        assert not Path(row['path']).exists(), row['path']
        old_absent += 1
    assert old_absent == old['deleted_files']
    kinds = Counter(row['kind'] for row in deleted)
    proof = {'status': 'passed_additional_completed_unselected_artifact_cleanup', 'at_local': now(),
        'deleted_files': len(deleted), 'deleted_by_kind': dict(kinds),
        'deleted_by_category': dict(Counter(row['category'] for row in deleted)),
        'deleted_logical_bytes': sum(row['bytes'] for row in deleted),
        'actual_D_free_bytes_change_during_deletion': after-before, 'D_free_bytes_after': after,
        'hardlinks_accounted_for_logical_size_is_not_released_space': True,
        'retained_records_SHA256_unchanged': len(value['retained_records_sha256']),
        'retained_artifact_identities_unchanged': len(value['retained_artifacts']),
        'retained_model_weight_SHA256_verified': protected_weights,
        'selected_packages': selected, 'skipped': skipped,
        'prior_deleted_files_still_absent': old_absent,
        'cumulative_deleted_files': old_absent+len(deleted),
        'cumulative_deleted_model_weights': old['deleted_by_kind']['model_weight']+kinds['model_weight'],
        'cumulative_deleted_prediction_or_derived_caches': old['deleted_by_kind']['prediction_or_derived_cache']+kinds['prediction_or_derived_cache'],
        'source_sha256': value['source_sha256'], 'new_missing_protected_dependencies': 0,
        'incomplete_experiments_not_classified_as_rejected': True,
        'scientific_processes_stopped_or_restarted': 0,
        'C_project_data_written': False, 'E_project_data_written': False,
        'new_backup_copies_created': 0, 'test_labels_read': False,
        'new_model_fits': 0, 'new_quality_scores': 0}
    create(OUT / 'verification.json', proof)
    print(json.dumps(proof, ensure_ascii=False), flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--execute', action='store_true')
    args = parser.parse_args()
    execute() if args.execute else plan()
