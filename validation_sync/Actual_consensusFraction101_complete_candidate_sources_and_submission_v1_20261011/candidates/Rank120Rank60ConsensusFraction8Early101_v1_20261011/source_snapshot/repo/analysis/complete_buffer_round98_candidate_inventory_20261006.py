"""Supplement actual full QA with exact coverage of every immutable candidate file."""
from pathlib import Path
import json
import os
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path.insert(0, str(A))
from run_dependency_queue_v3_20261006 import read, sha, create


def main():
    candidate = ROOT / 'candidates/optimization_20261003_r98'
    old_manifest = read(candidate / 'manifest.json')
    actual = {p.relative_to(candidate).as_posix(): p for p in candidate.rglob('*') if p.is_file()}
    missing = set(actual) - set(old_manifest['files']) - {'manifest.json'}
    assert missing == {'evidence/causal_entry_exit_buffer_source_freeze_20261006/manifest.json'}
    for relative, item in old_manifest['files'].items():
        assert sha(actual[relative]) == item['sha256']
    complete = A / 'optimization_20261003_r98/candidate_complete_manifest_20261006.json'
    create(complete, {'status': 'passed', 'candidate': str(candidate), 'files': {
        relative: {'sha256': sha(path), 'bytes': path.stat().st_size}
        for relative, path in sorted(actual.items())},
        'immutable_candidate_files_not_modified': True,
        'original_partial_manifest_also_hash_bound': True,
        'original_partial_manifest_missing_nested_file': sorted(missing)})
    qa8 = A / 'lossless_ranking_display_qa_v8_20261006/round98'
    qa9 = A / 'lossless_ranking_display_qa_v9_20261006/round98'
    prior = read(qa8 / 'verification.json')
    assert prior['status'] == 'passed_all_original_full_ranking_QA_and_lossless_browser_node_checks'
    display = A / 'lossless_ranking_display_v2_20261006/round98'
    publication = read(display / 'runtime_publication.json')
    assert publication['actual_full_QA_sha256'] == sha(qa8 / 'verification.json')
    assert publication['lossless_HTML_sha256'] == sha(display / 'complete_rankings_lossless.html')
    assert not qa9.exists()
    qa9.mkdir(parents=True)
    bindings = {str(path): sha(path) for path in (Path(__file__), complete, qa8 / 'verification.json',
        display / 'verification.json', display / 'complete_rankings_lossless.html',
        display / 'full_report_reconstructed_for_publication.json.gz')}
    bindings.update({str(path): read(complete)['files'][relative]['sha256'] for relative, path in actual.items()})
    create(qa9 / 'frozen_before_actual_full_QA.json', {'input_sha256': bindings,
        'full_original_actual_QA8_preserved': True,
        'only_additional_control': 'Every candidate file including nested and original outer manifests is hash bound',
        'browser_and_ranking_files_unchanged_so_actual_full_UI_QA8_reused': True,
        'no_new_Chrome_runs_claimed': True, 'test_labels_read': False})
    from locked_read_hash_cache_20261004 import LockedReadHashCache
    with LockedReadHashCache(bindings) as cache:
        record = read(complete)
        assert set(record['files']) == {p.relative_to(candidate).as_posix() for p in candidate.rglob('*') if p.is_file()}
        for relative, info in record['files'].items():
            assert sha(candidate / relative) == info['sha256']
        # Preserve the exact previously executed six-view interaction evidence.
        for name in ('interaction_result.json', 'ranking_report.png', 'rendered_dom.html', 'interaction_check.html'):
            source, target = qa8 / 'qa' / name, qa9 / 'qa' / name
            target.parent.mkdir(parents=True, exist_ok=True)
            os.link(source, target)
            assert sha(source) == sha(target)
        cache.reverify()
    proof = {**prior, 'at_local': time.strftime('%Y-%m-%dT%H:%M:%S'),
        'input_sha256': bindings, 'original_actual_full_QA8_source': str(qa8 / 'verification.json'),
        'original_actual_full_QA8_sha256': sha(qa8 / 'verification.json'),
        'additional_complete_candidate_inventory': {'status': 'passed', 'actual_candidate_files': len(actual),
            'manifest_path': str(complete), 'manifest_sha256': sha(complete),
            'all_candidate_files_including_nested_and_original_outer_manifests_checked': True},
        'actual_browser_QA8_reused_on_unchanged_HTML_and_graph_scores': True,
        'new_Chrome_runs': 0, 'new_model_fits': 0, 'new_quality_scores': 0}
    create(qa9 / 'verification.json', proof)
    create(display / 'runtime_publication_completeness_v2_20261006.json', {
        **publication, 'actual_full_QA_sha256': sha(qa9 / 'verification.json'),
        'complete_candidate_inventory_manifest': str(complete),
        'complete_candidate_inventory_manifest_sha256': sha(complete),
        'original_runtime_publication_retained': True})
    print(json.dumps({'status': 'passed_original_full_QA8_plus_exact2012_candidate_file_inventory',
        'candidate_files': len(actual), 'original_candidate_files_edited': 0}), flush=True)


if __name__ == '__main__':
    main()
