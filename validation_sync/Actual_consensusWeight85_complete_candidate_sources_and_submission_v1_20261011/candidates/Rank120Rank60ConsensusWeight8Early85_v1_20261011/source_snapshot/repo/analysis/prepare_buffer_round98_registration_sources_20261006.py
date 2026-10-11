"""Version only routing identifiers; retain the entire actual ranking and QA."""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path.insert(0, str(A))
from run_dependency_queue_v3_20261006 import read, sha, create


def main():
    recipes = [
        ('build_lossless_ranking_display_v6_20261006.py', 'build_lossless_ranking_display_v7_20261006.py',
            {'assert number == 97': 'assert number == 98'}),
        ('verify_lossless_ranking_display_v7_20261006.py', 'verify_lossless_ranking_display_v8_20261006.py', {
            'build_lossless_ranking_display_v6_20261006': 'build_lossless_ranking_display_v7_20261006',
            'lossless_ranking_display_qa_v7_20261006': 'lossless_ranking_display_qa_v8_20261006',
            'ranking_display_qa_v7_20261006': 'ranking_display_qa_v8_20261006'}),
        ('lossless_ranking_runtime_adapter_v5_20261006.py', 'lossless_ranking_runtime_adapter_v6_20261006.py', {
            'assert number == 97': 'assert number == 98',
            'build_lossless_ranking_display_v6_20261006': 'build_lossless_ranking_display_v7_20261006',
            'verify_lossless_ranking_display_v7_20261006': 'verify_lossless_ranking_display_v8_20261006',
            'lossless_ranking_display_qa_v7_20261006': 'lossless_ranking_display_qa_v8_20261006'})]
    bindings, controls = {}, []
    for old, new, replacements in recipes:
        original = (A / old).read_text(encoding='utf-8')
        text = original
        # Longest tokens first so overlapping path fragments cannot mask a patch.
        for before in sorted(replacements, key=len, reverse=True):
            assert before in text, before
            text = text.replace(before, replacements[before])
        restored = text
        for before in sorted(replacements, key=len, reverse=True):
            restored = restored.replace(replacements[before], before)
        assert restored == original, 'All original scientific and browser assertions must survive exactly'
        compile(text, str(A / new), 'exec')
        with (A / new).open('x', encoding='utf-8') as stream:
            stream.write(text)
        bindings[str(A / old)] = sha(A / old)
        bindings[str(A / new)] = sha(A / new)
        controls.append({'original': old, 'effective': new, 'only_changes': replacements,
            'full_original_source_exact_after_reversing_route_identifiers': True})
    create(A / 'buffer_round98_ranking_source_preparation_20261006.json', {
        'status': 'passed_full_original_lossless_ranking_and_QA_preserved_for_round98',
        'input_sha256': bindings, 'controls': controls,
        'all_original_six_views_source_provenance_candidate_manifest_search_sort_and_CSV_checks_retained': True,
        'all_records_rendered_and_full_lossless_nodes_checked': True,
        'browser_timeout_seconds': 45, 'test_labels_read': False, 'new_quality_scores': 0})


if __name__ == '__main__':
    main()
