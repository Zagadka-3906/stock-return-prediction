"""Remove only the published pilot's final rejected private prediction CSV."""
from pathlib import Path
import os
import sys

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path[:0] = [str(ROOT), str(A)]
from run_dependency_queue_v3_20261006 import read, sha, create, owned


def main():
    pilot = (A / 'causal_entry_exit_buffer_official_pilot_20261006').resolve()
    path = (pilot / 'scoring_validation_only/submission.csv').resolve()
    record_path = A / 'rejected_buffer_pilot_csv_cleanup_20261006.json'
    assert not record_path.exists()
    assert path.is_relative_to(pilot) and path.drive.upper() == 'D:'
    assert path.name == 'submission.csv' and path.is_file()
    assert path.stat().st_nlink == 1, 'A shared/canonical CSV must never be removed'
    assert not owned(read(A / 'service_owned_workflows_20261006/causal_entry_exit_buffer_official_pilot/native_launch.json'))
    proof = read(pilot / 'verification.json')
    receipt = read(A / 'causal_entry_exit_buffer_official_pilot_github_20261006/receipt.json')
    assert receipt['status'] == 'pushed_actual16_official_buffer_pilot_records_main_only'
    last = proof['records'][-1]
    assert last['margin'] == 1. and last['connected_final_score'] < proof['best']['connected_final_score']
    capsule = Path(last['official_score_cache']['official_metrics_source'])
    assert sha(capsule) == last['official_metric_capsule_sha256']
    assert sha(path) == read(capsule)['scope']['submission_csv_sha256']
    assert str(path) not in proof['input_sha256']
    inputs = {str(value): sha(value) for value in (Path(__file__), pilot / 'verification.json',
        A / 'causal_entry_exit_buffer_official_pilot_github_20261006/receipt.json', capsule)}
    size = path.stat().st_size
    fingerprint = sha(path)
    path.unlink()
    assert not path.exists()
    for value, digest in inputs.items(): assert sha(value) == digest
    create(record_path, {'status': 'passed_removed_only_published_rejected_private_buffer_prediction_csv',
        'removed_path': str(path), 'removed_bytes': size, 'removed_sha256': fingerprint,
        'input_sha256': inputs, 'actual_published_main_commit': receipt['commit'],
        'retained_all16_scores_source_capsules_and_input_fingerprints': True,
        'canonical_parent_predictions_models_training_aliases_and_live_R96_untouched': True,
        'not_a_recursive_cleanup': True, 'new_quality_scores': 0, 'test_labels_read': False})
    print(f'removed {size} bytes of rejected private prediction CSV; all sixteen score records retained', flush=True)


if __name__ == '__main__': main()
