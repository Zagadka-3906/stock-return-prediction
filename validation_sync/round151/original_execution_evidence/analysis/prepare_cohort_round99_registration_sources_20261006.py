"""Extend routing while preserving every original lossless board and browser check."""
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path.insert(0, str(A))
from run_dependency_queue_v3_20261006 import sha, create


def main():
    recipes = [
        ('build_lossless_ranking_display_v7_20261006.py', 'build_lossless_ranking_display_v8_20261006.py',
         {'assert number == 98': 'assert number == 99'}),
        ('verify_lossless_ranking_display_v8_20261006.py', 'verify_lossless_ranking_display_v10_20261006.py', {
            'build_lossless_ranking_display_v7_20261006': 'build_lossless_ranking_display_v8_20261006',
            'lossless_ranking_display_qa_v8_20261006': 'lossless_ranking_display_qa_v10_20261006',
            'ranking_display_qa_v8_20261006': 'ranking_display_qa_v10_20261006'}),
        ('lossless_ranking_runtime_adapter_v6_20261006.py', 'lossless_ranking_runtime_adapter_v7_20261006.py', {
            'assert number == 98': 'assert number == 99',
            'build_lossless_ranking_display_v7_20261006': 'build_lossless_ranking_display_v8_20261006',
            'verify_lossless_ranking_display_v8_20261006': 'verify_lossless_ranking_display_v10_20261006',
            'lossless_ranking_display_qa_v8_20261006': 'lossless_ranking_display_qa_v10_20261006'})]
    pins, controls = {}, []
    for old, new, replacements in recipes:
        original = (A / old).read_text(encoding='utf-8')
        text = original
        for before in sorted(replacements, key=len, reverse=True):
            assert before in text
            text = text.replace(before, replacements[before])
        restored = text
        for before in sorted(replacements, key=len, reverse=True):
            restored = restored.replace(replacements[before], before)
        assert restored == original
        compile(text, str(A / new), 'exec')
        with (A / new).open('x', encoding='utf-8') as stream:
            stream.write(text)
        pins.update({str(A / old): sha(A / old), str(A / new): sha(A / new)})
        controls.append({'original': old, 'effective': new, 'only_changes': replacements,
                         'original_source_exact_after_reversing_route_identifiers': True})
    create(A / 'cohort_round99_ranking_source_preparation_20261006.json', {
        'status': 'passed_full_original_lossless_ranking_and_QA_preserved_for_round99',
        'input_sha256': pins, 'controls': controls,
        'all_original_six_views_provenance_candidate_manifest_search_sort_CSV_and_all_nodes_checks_retained': True,
        'browser_timeout_seconds': 45, 'new_quality_scores': 0, 'test_labels_read': False})


if __name__ == '__main__':
    main()
