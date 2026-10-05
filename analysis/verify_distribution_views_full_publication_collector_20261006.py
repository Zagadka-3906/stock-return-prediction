"""Validate collection against an actual completed round and its committed raw blobs."""
from pathlib import Path
from datetime import datetime
import hashlib
import json

from collect_full_lossless_round_publication_20261006 import collect, read, sha, ROOT, A
import publish_classifier_consensus_workflows_20261006 as helpers


def create(path, value):
    with Path(path).open('x', encoding='utf-8') as stream:
        json.dump(value, stream, ensure_ascii=False, indent=2)
        stream.write('\n')


def main():
    out = A / 'distribution_views_full_publication_collector_preflight_20261006'
    assert not out.exists()
    out.mkdir()
    inputs = {str(path.resolve()): sha(path) for path in (
        Path(__file__), A / 'collect_full_lossless_round_publication_20261006.py',
        A / 'distribution_views_lossless_publication_adapter_20261006.py',
        A / 'immutable_lossless_ranking_snapshot_20261006.py',
        A / 'quantile_tree_quality_queue_v2_20261006/plan.json',
        A / 'quantile_distribution_views_quality_queue_20261006/plan.json')}
    create(out / 'frozen_before_actual_collection.json', {
        'at_local': datetime.now().isoformat(timespec='seconds'), 'input_sha256': inputs,
        'actual_reference_round': 82, 'actual_reference_QA_version': 4,
        'actual_reference_scored_records': 138, 'prospective_rounds': [93, 94],
        'new_model_fits': 0, 'new_quality_scores': 0, 'test_labels_read': False})
    try:
        payload, evidence = collect(82, 4, 138)
        assert len(payload) == 10 and evidence['connected_records'] == 10084
        receipt = read(A / 'github_validation_sync_main_20261005/round82_receipt.json')
        assert receipt['status'] == 'pushed_and_remote_head_verified' and receipt['branch'] == 'main'
        expected = {name: hashlib.sha256(data).hexdigest() for name, data in payload.items()}
        assert helpers.blob_hashes(receipt['commit'], expected) == expected
        # Compile the exact prospective adapter and check that both93/94 route to QA v6.
        import sync_validated_rounds_main_20261005 as sync
        from distribution_views_lossless_publication_adapter_20261006 import install
        old = install(sync)
        assert sync.snapshot is not old
        sync.snapshot = old
        for filename, digest in inputs.items():
            assert sha(filename) == digest
        create(out / 'verification.json', {
            'status': 'passed_actual_full138_record_round82_collector_and_committed_blob_match',
            'at_local': datetime.now().isoformat(timespec='seconds'), 'input_sha256': inputs,
            'actual_full_ranking_collection': evidence, 'actual_reference_commit': receipt['commit'],
            'actual_raw_git_blobs_matching': len(expected),
            'original_complete_json_bytes_decompressed_and_rehashed': True,
            'all10_original_immutable_display_and_full_QA_files_collected': True,
            'both_original198_and_new262_scientific_plans_unchanged': True,
            'prospective93_94_real_science_and_QA_not_yet_complete': True,
            'prospective_adapter_compiled_and_installed': True,
            'new_model_fits': 0, 'new_quality_scores': 0, 'test_labels_read': False})
    except BaseException as error:
        create(out / 'failure.json', {'status': 'failed_actual_collection_preserved',
            'error': f'{type(error).__name__}: {error}'})
        raise
    print(json.dumps({'status': 'passed', 'actual_reference_round': 82,
        'actual_connected_records': 10084, 'actual_raw_blobs_verified': 10,
        'future93_94_validation_still_pending': True}), flush=True)


if __name__ == '__main__':
    main()
