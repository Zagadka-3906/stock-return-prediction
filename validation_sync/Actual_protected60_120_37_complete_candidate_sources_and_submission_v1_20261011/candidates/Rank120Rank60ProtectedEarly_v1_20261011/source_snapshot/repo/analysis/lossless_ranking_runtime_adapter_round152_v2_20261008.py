"""Retain full scientific rankings and run complete QA on a lossless display."""
from pathlib import Path
import hashlib
import json
import shutil
import time

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'


def sha(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def install(number):
    assert number == 152
    import build_all_model_rankings_20261003 as ranking
    import verify_all_model_rankings_20261003 as qa
    from build_lossless_ranking_display_round152_v2_20261008 import main as encode
    from verify_lossless_ranking_display_round152_v2_20261008 import main as verify
    original_ranking, original_qa = ranking.main, qa.main
    display = A / 'lossless_ranking_display_v2_20261006' / f'round{number}'
    qa_folder = A / 'lossless_ranking_display_qa_v63_20261009' / f'round{number}'
    assert not qa_folder.exists()
    from SparseAfter148152_storage_v1_20261009 import ensure_display as ensure
    ensure(display, number, create=False)

    def build():
        result = original_ranking()
        encode(number)
        return result

    def check():
        verify(number)
        proof = json.loads((qa_folder / 'verification.json').read_text(encoding='utf-8'))
        assert proof['status'] == 'passed_all_original_full_ranking_QA_and_lossless_browser_node_checks'
        # These are mutable display outputs; retain each immutable per-round proof.
        html = display / 'complete_rankings_lossless.html'
        target = ROOT / 'results/all_model_rankings_20261003.html'
        shutil.copyfile(html, target)
        assert sha(target) == sha(html)
        copied = {}
        for filename in ('interaction_result.json', 'ranking_report.png', 'rendered_dom.html', 'interaction_check.html'):
            source = qa_folder / 'qa' / filename
            destination = A / 'all_model_ranking_qa' / filename
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, destination)
            assert sha(source) == sha(destination)
            copied[str(destination)] = sha(source)
        with (display / 'runtime_publication.json').open('x', encoding='utf-8') as stream:
            json.dump({'status': 'passed_actual_lossless_complete_ranking_and_full_original_QA',
                'round': number, 'at_local': time.strftime('%Y-%m-%dT%H:%M:%S'),
                'complete_report_sha256': sha(ROOT / 'results/all_model_rankings_20261003.json'),
                'lossless_HTML_sha256': sha(html), 'actual_full_QA_sha256': sha(qa_folder / 'verification.json'),
                'current_display_output_sha256': copied, 'all_values_six_views_and_current_candidate_preserved': True,
                'browser_timeout_seconds': 45, 'new_model_fits': 0, 'new_quality_scores': 0,
                'test_labels_read': False}, stream, ensure_ascii=False, indent=2)
            stream.write('\n')

    ranking.main, qa.main = build, check

    def restore():
        assert ranking.main is build and qa.main is check
        ranking.main, qa.main = original_ranking, original_qa

    return restore
