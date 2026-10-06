"""Collect immutable full rankings and complete QA without changing round science."""
from pathlib import Path
import gzip
import hashlib
import json

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8-sig'))


def sha(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def collect(number, qa_version, expected_records):
    from locked_read_hash_cache_20261004 import LockedReadHashCache
    from immutable_lossless_ranking_snapshot_20261006 import prepare
    import sync_validated_rounds_main_20261005 as sync
    display = A / 'lossless_ranking_display_v2_20261006' / f'round{number}'
    qa = A / f'lossless_ranking_display_qa_v{qa_version}_20261006' / f'round{number}'
    proof = read(display / 'verification.json')
    qa_proof = read(qa / 'verification.json')
    publication = read(display / 'runtime_publication.json')
    assert proof['status'] == 'passed_all_original_report_values_and_six_views_lossless_roundtrip'
    assert proof['all_original_record_values_parameters_source_pointers_and_scores_preserved']
    assert qa_proof['status'] == 'passed_all_original_full_ranking_QA_and_lossless_browser_node_checks'
    assert qa_proof['original_full_QA_result']['new_round_records'] == expected_records
    assert qa_proof['original_full_QA_result']['connected_records'] == proof['connected_records']
    assert qa_proof['original45_second_render_timeout_retained'] and qa_proof['all_new_browser_profiles_under_D']
    assert qa_proof['all_original_provenance_candidate_manifest_sorting_and_six_view_checks_passed']
    assert qa_proof['all_original_exact_report_values_and_browser_lossless_nodes_verified']
    assert qa_proof['test_labels_read'] is False
    assert publication['status'] == 'passed_actual_lossless_complete_ranking_and_full_original_QA'
    assert publication['complete_report_sha256'] == proof['original_report_sha256']
    assert publication['lossless_HTML_sha256'] == proof['lossless_HTML_sha256']
    assert publication['actual_full_QA_sha256'] == sha(qa / 'verification.json')
    assert publication['all_values_six_views_and_current_candidate_preserved']
    report = prepare(display)
    files = [display / name for name in ('frozen_before_encoding.json', 'verification.json',
        'complete_rankings_lossless.html', 'runtime_publication.json',
        'full_report_reconstructed_for_publication.json.gz', 'full_report_publication_snapshot_verification.json')]
    files += [qa / name for name in ('frozen_before_actual_full_QA.json', 'verification.json',
        'qa/interaction_result.json', 'qa/ranking_report.png')]
    bindings = {str(path.resolve()): sha(path) for path in files}
    assert bindings[str((display / 'complete_rankings_lossless.html').resolve())] == proof['lossless_HTML_sha256']
    payload, metadata = {}, {}
    with LockedReadHashCache(bindings) as cache:
        with gzip.open(report, 'rb') as stream:
            assert hashlib.file_digest(stream, 'sha256').hexdigest() == proof['original_report_sha256']
        for path in files:
            assert cache.sha(path) == bindings[str(path.resolve())]
            data = path.read_bytes()
            assert hashlib.sha256(data).hexdigest() == bindings[str(path.resolve())]
            assert not sync.SECRET.search(data)
            destination = (Path(f'validation_sync/round{number}/complete_ranking_display') / path.relative_to(A)).as_posix()
            payload[destination] = data
            metadata[destination] = {'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}
        cache.reverify()
    return payload, {'round': number, 'qa_version': qa_version,
        'scored_records': expected_records, 'connected_records': proof['connected_records'],
        'original_full_ranking_sha256': proof['original_report_sha256'],
        'local_input_source_sha256': {str(path.relative_to(ROOT)): bindings[str(path.resolve())] for path in files},
        'exported_files': metadata, 'actual_full_lossless_ranking_and_original_QA_collected': True,
        'new_model_fits': 0, 'new_quality_scores': 0, 'test_labels_read': False}
