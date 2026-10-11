"""Check current selected packages and adopted roots after the authorized cleanup."""
from pathlib import Path
from datetime import datetime
import hashlib
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
OUT = A / 'rejected_artifact_cleanup_20261005'


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8-sig'))


def sha(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as stream:
        for block in iter(lambda: stream.read(4 * 1024**2), b''):
            h.update(block)
    return h.hexdigest()


def main():
    cleanup = read(OUT / 'verification.json')
    assert cleanup['status'] == 'passed_user_authorized_rejected_artifact_cleanup'
    assert cleanup['new_missing_protected_dependencies'] == 0
    checks = []
    active = read(ROOT / 'active_release.json')
    for key in ('manifest', 'submission'):
        assert sha(active[key]) == active[key + '_sha256'], active[key]
    checks.append({'kind': 'active_delivery_pointer', 'manifest_and_submission_sha256': 'passed'})
    folder = Path(active['delivery_directory'])
    manifests = [(folder, read(active['manifest'])['artifacts'])]
    for number in (65, 66):
        folder = ROOT / f'candidates/optimization_20261003_r{number}'
        manifests.append((folder, read(folder / 'manifest.json')['files']))
    for folder, entries in manifests:
        for name, record in entries.items():
            assert '测试集_Y' not in name and 'TestY' not in name, name
            path = folder / name
            assert path.resolve().is_relative_to(folder.resolve()), path
            assert path.is_file() and sha(path) == record['sha256'], path
        checks.append({'kind': 'retained_selected_package', 'folder': str(folder),
                       'verified_file_count': len(entries), 'all_files_match_frozen_manifest': True})
    retention = read(A / 'artifact_cleanup_selected_roots_retention_plan_20261005.json')
    for path, digest in retention['input_sha256'].items():
        assert sha(path) == digest, path
    checks.append({'kind': 'adopted_GRU_and_root_reconstruction_sources',
                   'verified_file_count': len(retention['input_sha256']), 'all_sha256_match': True})
    plan = read(OUT / 'plan.json')
    checked = 0
    for line in (OUT / 'deletions.jsonl').read_text(encoding='utf-8').splitlines():
        row = json.loads(line)
        assert not Path(row['path']).exists(), row['path']
        checked += 1
    assert checked == cleanup['deleted_files']
    proof = {'status': 'passed_selected_artifact_integrity_after_cleanup',
        'at_local': datetime.now().isoformat(timespec='seconds'), 'checks': checks,
        'deleted_artifacts_absent': checked, 'historical_record_files_verified_by_cleanup':
        cleanup['record_files_verified_unchanged'], 'ranking_rows_before_cleanup': plan['board_records_at_plan'],
        'official_score_unchanged_by_cleanup': True, 'test_labels_read': False,
        'new_model_fits': 0, 'new_quality_scores': 0, 'source_sha256': sha(__file__)}
    with (OUT / 'selected_artifact_integrity.json').open('x', encoding='utf-8') as stream:
        json.dump(proof, stream, ensure_ascii=False, indent=2)
        stream.write('\n')
    print(json.dumps(proof, ensure_ascii=False), flush=True)


if __name__ == '__main__':
    main()
