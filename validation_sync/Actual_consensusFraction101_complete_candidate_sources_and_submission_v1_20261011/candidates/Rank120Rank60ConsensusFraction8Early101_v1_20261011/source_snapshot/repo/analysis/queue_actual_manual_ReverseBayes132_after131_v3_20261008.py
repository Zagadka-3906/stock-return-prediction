"""Manual new-day dispatch of the unexecuted signed grid after actual131 closure."""
from pathlib import Path
import sys
import time
ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path[:0] = [str(ROOT), str(A)]
from run_dependency_queue_v3_20261006 import read, sha, create, owned
from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start


def closed(name):
    f = A / 'service_owned_workflows_20261006' / name
    while not (f / 'native_launch.json').exists() or owned(read(f / 'native_launch.json')):
        time.sleep(5)
    assert read(f / 'service_execution.json')['status'] == 'passed', name


def main():
    closed('round131_preserved_QA42_main_publication_recovery_v3_20261008')
    assert read(A / 'optimization_20261003_r131/full_registration_execution.json')['status'] == 'passed'
    assert read(A / 'github_validation_sync_main_20261005/round131_receipt.json')['actual_full_QA_version'] == 42
    proof_path = A / 'actual_ReverseBayes132_manual_routes_v3_20261008.json'
    proof = read(proof_path)
    pins = {**proof['input_sha256'], str(proof_path): sha(proof_path), str(Path(__file__)): sha(Path(__file__))}
    for p, d in pins.items(): assert sha(p) == d, p
    main8 = A / 'service_owned_workflows_20261006/main_publisher_v8_20261008'
    assert not main8.exists()
    publisher = start('main_publisher_v8_20261008', 'watch_validations_main_v7_20261006.py', [],
        {str(A / 'watch_validations_main_v7_20261006.py'): sha(A / 'watch_validations_main_v7_20261006.py')})
    create(A / 'actual_new_day_main_publisher_v8_20261008.json', {
        'status': 'restarted_main_only_publisher_after_actual_user_continue_and131_closure',
        'identity': publisher, 'automatic_morning_restart': False})
    admission_name = 'nonflag_ReverseBayes40_round132_source_admission_v2'
    admission = start(admission_name, 'verify_nonflag_ReverseBayes40_round132_sources_v3_20261008.py', [], pins)
    create(A / 'actual_ReverseBayes132_manual_admission_launch_20261008.json', {
        'status': 'started_original24_routes_and37_full_controls_actual131_baselines',
        'identity': admission, 'input_sha256': pins, 'official_scores_added_by_dispatch': 0})
    closed(admission_name)
    actual = A / 'nonflag_ReverseBayes40_round132_source_admission_v1_20261007.json'
    admitted = read(actual)
    assert len(admitted['baseline_gain_regressions']) == 9 and len(admitted['graph_metadata_controls']) == 12
    pins.update({**admitted['input_sha256'], str(actual): sha(actual)})
    jobs = [
        ('nonflag_ReverseBayes40_full37_controls_main_publication_v1', 'publish_nonflag_ReverseBayes40_evidence_v3_20261008.py', ['controls']),
        ('nonflag_ReverseBayes40_official_comparison_v1', 'run_nonflag_ReverseBayes40_admitted_comparison_v3_20261008.py', []),
        ('nonflag_ReverseBayes40_scores_main_publication_v1', 'publish_nonflag_ReverseBayes40_evidence_v3_20261008.py', ['scores']),
        ('nonflag_ReverseBayes40_selected_candidate_preparation_v1', 'prepare_nonflag_ReverseBayes40_selected_candidate_v1_20261007.py', []),
        ('nonflag_ReverseBayes40_selected_candidate_sealing_v1', 'seal_nonflag_ReverseBayes40_selected_candidate_v1_20261007.py', []),
        ('nonflag_ReverseBayes40_round132_full_registration_v1', 'run_nonflag_ReverseBayes40_round132_full_registration_v2_20261008.py', [])]
    assert all(not (A / 'service_owned_workflows_20261006' / n).exists() for n, _, _ in jobs)
    launches = {n: start(n, d, args, pins) for n, d, args in jobs}
    create(A / 'actual_ReverseBayes132_manual6_pipeline_launches_20261008.json', {
        'status': 'actual_manual_dispatch_after_new_day131_source_and_main_closure', 'launches': launches,
        'input_sha256': pins, 'new_native_fits': 0, 'new_quality_scores_by_dispatch': 0,
        'old_expired2312_queue_not_restarted': True, 'test_labels_read': False})


if __name__ == '__main__':
    main()
