"""Verify completed deletions separately from an actively refreshed shared ranking."""
from pathlib import Path
import json
import sys
import time

import psutil

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path[:0] = [str(ROOT), str(A)]
from run_dependency_queue_v3_20261006 import read, sha, create, owned
from refresh_optimization_boundary_evidence_20261004 import complete_round_evidence

OUT = A / 'closed_round_worker_submission_cleanup_recovery_20261006'
ORIGINAL = A / 'closed_round_worker_submission_cleanup_20261006'


def main():
    assert not OUT.exists(); OUT.mkdir()
    sources = [Path(__file__), A / 'cleanup_closed_round_worker_submissions_20261006.py',
               ORIGINAL / 'plan.json', ORIGINAL / 'failure.json', ORIGINAL / 'deletions.jsonl']
    inputs = {str(p.resolve()): sha(p) for p in sources}
    live_board = (ROOT / 'results/all_model_rankings_20261003.json').resolve()
    create(OUT / 'frozen_before_verification.json', {
        'status': 'frozen_before_independent_post_deletion_verification',
        'input_sha256': inputs, 'single_mutable_observer_output_excluded': str(live_board),
        'reason': 'Original R85 pipeline actively updates the shared complete ranking; historical frozen snapshots stay retained.',
        'no_additional_deletions': True, 'original_failure_retained': True})
    try:
        plan, failure = read(ORIGINAL / 'plan.json'), read(ORIGINAL / 'failure.json')
        assert failure['status'] == 'failed_preserved_cleanup'
        assert failure['error'] == 'AssertionError: ' + str(live_board)
        assert sha(A / 'cleanup_closed_round_worker_submissions_20261006.py') == plan['source_sha256']
        deletions = [json.loads(line) for line in (ORIGINAL / 'deletions.jsonl').read_text(encoding='utf-8').splitlines()]
        assert len(deletions) == 3
        assert [{k: row[k] for k in plan['deletions'][i]} for i, row in enumerate(deletions)] == plan['deletions']
        for row in deletions:
            path = Path(row['path'])
            assert path.resolve() == path and path.is_relative_to(ROOT.resolve()) and not path.exists()
        for name, digest in plan['retained_records_sha256'].items(): assert sha(name) == digest, name
        unchanged = 0
        assert str(live_board) in plan['frozen_documents_sha256']
        for name, digest in plan['frozen_documents_sha256'].items():
            if Path(name).resolve() == live_board: continue
            assert sha(name) == digest, name
            unchanged += 1
        after = [complete_round_evidence(n) for n in (82,83,84)]
        assert after == [row['qualification'] for row in plan['qualification']]
        queue = read(A / 'service_owned_dependency_queue_v4_20261006/state.json')
        assert all(not owned(queue['activated_jobs'][f'round{n}']) for n in (82,83,84))
        for name, digest in inputs.items(): assert sha(name) == digest, name
        proof = {'status': 'passed_closed_published_round_worker_scratch_cleanup',
            'at_local': time.strftime('%Y-%m-%dT%H:%M:%S'), 'verification_kind': 'independent_recovery_after_recorded_post_deletion_observer_check_failure',
            'original_cleanup_execution_status': 'failed_preserved_cleanup', 'original_failure_retained': True,
            'deleted_files': len(deletions), 'deleted_logical_bytes': sum(row['bytes'] for row in deletions),
            'all_deleted_files_single_hardlink': all(row['hardlinks'] == 1 for row in deletions),
            'actual_D_free_bytes_now': psutil.disk_usage('D:/').free,
            'physical_free_bytes_before_deletion_not_recorded_no_exact_reclamation_claim': True,
            'records_verified_unchanged': len(plan['retained_records_sha256']),
            'frozen_and_source_documents_verified_unchanged': unchanged,
            'single_mutable_observer_output_excluded': str(live_board),
            'mutable_observer_different_before_and_after_is_expected_during_R85_publication': True,
            'original_qualification_before_and_after_identical': True, 'after_qualification': after,
            'input_sha256': inputs, 'model_weights_deleted': 0, 'candidate_submissions_deleted': 0,
            'new_deletions_by_recovery': 0, 'new_model_fits': 0, 'new_quality_scores': 0, 'test_labels_read': False,
            'scientific_processes_stopped_or_restarted': 0, 'C_project_data_written': False}
        create(OUT / 'verification.json', proof); print(json.dumps(proof, ensure_ascii=False), flush=True)
    except BaseException as error:
        create(OUT / 'failure.json', {'status': 'failed_preserved_independent_cleanup_recovery', 'error': f'{type(error).__name__}: {error}'})
        raise


if __name__ == '__main__': main()
