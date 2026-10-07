"""Dispatch the fine signed Bayesian round after real parent closure and ordered main handoff."""
from pathlib import Path
import sys
import time
ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path[:0] = [str(ROOT), str(A)]
from run_dependency_queue_v3_20261006 import read, sha, create, owned
from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start


def closed(name):
    folder = A / 'service_owned_workflows_20261006' / name
    while not (folder / 'native_launch.json').exists() or owned(read(folder / 'native_launch.json')): time.sleep(15)
    assert read(folder / 'service_execution.json')['status'] == 'passed', name


def main():
    jobs = [('nonflag_ReverseBayesFine40_round134_source_admission_v1', 'verify_nonflag_ReverseBayesFine40_round134_sources_v1_20261007.py', []),
            ('nonflag_ReverseBayesFine40_full37_controls_main_publication_v1', 'publish_nonflag_ReverseBayesFine40_evidence_v1_20261007.py', ['controls']),
            ('nonflag_ReverseBayesFine40_official_comparison_v1', 'run_nonflag_ReverseBayesFine40_admitted_comparison_v1_20261007.py', []),
            ('nonflag_ReverseBayesFine40_scores_main_publication_v1', 'publish_nonflag_ReverseBayesFine40_evidence_v1_20261007.py', ['scores']),
            ('nonflag_ReverseBayesFine40_selected_candidate_preparation_v1', 'prepare_nonflag_ReverseBayesFine40_selected_candidate_v1_20261007.py', []),
            ('nonflag_ReverseBayesFine40_selected_candidate_sealing_v1', 'seal_nonflag_ReverseBayesFine40_selected_candidate_v1_20261007.py', []),
            ('nonflag_ReverseBayesFine40_round134_full_registration_v1', 'run_nonflag_ReverseBayesFine40_round134_full_registration_v1_20261007.py', [])]
    paths = [Path(__file__), *[A / driver for _, driver, _ in jobs],
             A / 'nonflag_ReverseBayesFine40_science_route_preparation_v1_20261007.json',
             A / 'nonflag_ReverseBayesFine40_prospective_routes_v2_20261007.json',
             A / 'actual_user_submission_deadline_and_priority_20261008.json']
    pins = {str(p): sha(p) for p in paths}
    create(A / 'actual_ReverseBayesFine134_complete_dependency_plan_v1_20261008.json', {
            'status': 'frozen_complete134_negative_amplitude_refinement_queue_before_quality_scores',
            'jobs': jobs, 'input_sha256': pins, 'new_quality_scores': 0, 'test_labels_read': False})
    closed('nonflag_ReverseBayesFine40_actual_full37_controls_v1_20261008')
    closed('nonflag_SparseGram40_round133_full_registration_v1')
    closed('actual_deadline_and_full_training_handoff_main_publication_v1_20261008')
    assert read(A / 'optimization_20261003_r133/full_registration_execution.json')['status'] == 'passed'
    assert read(A / 'github_validation_sync_main_20261005/round133_receipt.json')['actual_full_QA_version'] == 44
    assert read(A / 'actual_deadline_and_full_training_handoff_main_v1_20261008/receipt.json')['status'] == 'pushed_and_remote_head_verified'
    rows = {}
    for name, driver, args in jobs:
        for p, d in pins.items(): assert sha(p) == d, p
        rows[name] = start(name, driver, args, pins)
        if name.endswith('source_admission_v1'): closed(name)
    create(A / 'actual_ReverseBayesFine134_complete_hidden_launches_v1_20261008.json', {
            'status': 'started_actual_full134_negative_amplitude_controls_scores_candidate_QA45_main_pipeline',
            'launches': rows, 'input_sha256': pins, 'new_quality_scores_by_launch': 0, 'test_labels_read': False})
    print('Complete negative Bayes refinement134 pipeline started', flush=True)


if __name__ == '__main__': main()
