"""Verify the real supplemental artifacts and repeated central inventory refresh."""
from pathlib import Path
from datetime import datetime
import hashlib
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'analysis'))
OUT = ROOT / 'analysis/nystrom_tuning_cost_inventory_qa_20261005'


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8-sig'))


def sha(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def create(path, value):
    with path.open('x', encoding='utf-8') as stream:
        json.dump(value, stream, ensure_ascii=False, indent=2)
        stream.write('\n')


def summary(cost):
    return {key: cost[key] for key in ('configurations', 'total_actual_new_annual_fits',
        'fully_completed_five_year_configurations', 'fulltraining_artifacts_ready',
        'nystrom_tuning_actual_annual_fits', 'nystrom_tuning_actual_fulltraining_artifacts')}


def main():
    import refresh_nystrom_tuning_cost_evidence_20261005 as refresh
    import refresh_nystrom_tuning_progress_20261005 as actual
    OUT.mkdir(exist_ok=True)
    sources = [Path(__file__), Path(refresh.__file__), Path(actual.__file__),
        ROOT / 'analysis/monitor_actual_optimization_progress_v4_20261005.py',
        ROOT / 'analysis/refresh_optimization_boundary_evidence_v3_20261005.py',
        ROOT / 'analysis/actual_optimization_monitor_run_v4_20261005.json']
    bindings = {str(path): sha(path) for path in sources}
    create(OUT / 'frozen_before_controls.json', {'status': 'frozen_before_actual_inventory_controls',
        'at_local': datetime.now().isoformat(), 'source_sha256': bindings,
        'new_quality_scores': 0, 'test_labels_read': False})
    actual.main()
    artifact_path = ROOT / 'analysis/nystrom_tuning_progress_20261005.json'
    artifact = read(artifact_path)
    info_hashes = {path: digest for path, digest in artifact['source_sha256'].items() if Path(path).name.startswith('info_')}
    cost_path = ROOT / 'analysis/optimization_fit_cost_evidence_20261004.json'
    refresh.main()
    first = read(cost_path)
    refresh.main()
    second = read(cost_path)
    assert summary(first) == summary(second), 'Stable completed artifacts were counted differently on repeated refresh.'
    assert second['nystrom_tuning_actual_annual_fits'] == artifact['actual_annual_fits']
    assert second['nystrom_tuning_actual_fulltraining_artifacts'] == artifact['actual_fulltraining_artifacts']
    rows = [row for row in second['models'] if row['model'].startswith(('rank_nystrom_tune_', 'return_nystrom_tune_'))]
    assert len(rows) == 10
    assert sum(row['annual_artifacts'] for row in rows) == artifact['actual_annual_fits']
    assert second['total_actual_new_annual_fits'] == sum(row['new_annual_fits'] for row in second['models'])
    assert len({row['model'] for row in second['models']}) == second['configurations']
    for path, digest in {**bindings, **info_hashes}.items():
        assert sha(path) == digest, path
    result = {'status': 'passed_actual_artifact_inventory_and_idempotent_refresh',
        'at_local': datetime.now().isoformat(), 'central_counts': summary(second),
        'actual_new_bank_annual_artifacts_and_raw_model_hashes_verified': True,
        'actual_new_bank_prefix_controls': artifact['actual_prefix_controls'],
        'source_sha256': bindings, 'actual_info_sha256': info_hashes,
        'two_real_refreshes_with_unchanged_completed_artifacts_same_counts': True,
        'new_model_fits': 0, 'new_quality_scores': 0, 'test_labels_read': False}
    create(OUT / 'verification.json', result)
    print(json.dumps({'status': result['status'], 'counts': result['central_counts']}, ensure_ascii=False), flush=True)


if __name__ == '__main__':
    main()
