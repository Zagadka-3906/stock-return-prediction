"""Recheck removed artifacts and retained evidence without changing historical seals."""
from pathlib import Path
from datetime import datetime
import hashlib
import json
import psutil

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
PREVIOUS = A / 'rejected_artifact_cleanup_20261005'
OUT = A / 'rejected_artifact_cleanup_recheck_20261005'


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


def main():
    assert not OUT.exists(), 'Preserve the existing recheck; do not overwrite.'
    OUT.mkdir()
    seals = [PREVIOUS / name for name in ('plan.json', 'deletions.jsonl', 'verification.json')]
    seals.append(A / 'artifact_cleanup_selected_roots_retention_plan_20261005.json')
    seals.append(Path(__file__).resolve())
    source = {str(path): sha(path) for path in seals}
    create(OUT / 'frozen_before_inspection.json', {
        'status': 'frozen_before_readonly_cleanup_recheck',
        'at_local': datetime.now().isoformat(timespec='seconds'),
        'source_sha256': source,
        'existing_cleanup_only_no_new_deletion': True,
    })
    plan, completed = read(PREVIOUS / 'plan.json'), read(PREVIOUS / 'verification.json')
    assert completed['status'] == 'passed_user_authorized_rejected_artifact_cleanup'
    deleted = [json.loads(line) for line in (PREVIOUS / 'deletions.jsonl').read_text(encoding='utf-8').splitlines()]
    assert len(deleted) == completed['deleted_files']
    for row in deleted:
        assert not Path(row['path']).exists(), row['path']
    records = plan['records_preserved_sha256']
    for name, record in records.items():
        assert sha(name) == record['sha256'], name
    active = read(ROOT / 'active_release.json')
    for key in ('manifest', 'submission'):
        assert sha(active[key]) == active[key + '_sha256'], active[key]
    manifests = [(Path(active['delivery_directory']), read(active['manifest'])['artifacts'])]
    for number in (65, 66):
        folder = ROOT / f'candidates/optimization_20261003_r{number}'
        manifests.append((folder, read(folder / 'manifest.json')['files']))
    selected = []
    for folder, entries in manifests:
        for name, record in entries.items():
            assert '测试集_Y' not in name and 'TestY' not in name
            path = folder / name
            assert path.resolve().is_relative_to(folder.resolve())
            assert sha(path) == record['sha256'], path
        selected.append({'folder': str(folder), 'verified_files': len(entries)})
    retention = read(A / 'artifact_cleanup_selected_roots_retention_plan_20261005.json')
    for name, digest in retention['input_sha256'].items():
        assert sha(name) == digest, name
    for name, digest in source.items():
        assert sha(name) == digest, name
    proof = {
        'status': 'passed_deleted_artifacts_still_absent_and_all_retained_records_and_selected_packages_unchanged',
        'at_local': datetime.now().isoformat(timespec='seconds'),
        'deleted_artifacts_still_absent': len(deleted),
        'deleted_model_weights': completed['deleted_by_kind']['model_weight'],
        'deleted_prediction_or_derived_caches': completed['deleted_by_kind']['prediction_or_derived_cache'],
        'original_actual_D_free_bytes_change': completed['D_free_bytes_change'],
        'current_D_free_bytes': psutil.disk_usage('D:/').free,
        'retained_records_fresh_sha256_verified': len(records),
        'selected_packages': selected,
        'adopted_root_dependencies_fresh_sha256_verified': len(retention['input_sha256']),
        'source_sha256': source,
        'new_deletions': 0,
        'new_model_fits': 0,
        'new_quality_scores': 0,
        'scientific_processes_stopped_or_restarted': 0,
        'test_labels_read': False,
        'project_files_written_to_C': False,
    }
    create(OUT / 'verification.json', proof)
    print(json.dumps(proof, ensure_ascii=False), flush=True)


if __name__ == '__main__':
    main()
