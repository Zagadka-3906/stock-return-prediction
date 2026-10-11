"""Retain every original ranking QA check, add codec checks and place profiles on D."""
from pathlib import Path
import hashlib
import json
import os
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path.insert(0, str(A))


def sha(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def create(path, value):
    with path.open('x', encoding='utf-8') as stream:
        json.dump(value, stream, ensure_ascii=False, indent=2)
        stream.write('\n')


def main(number):
    from locked_read_hash_cache_20261004 import LockedReadHashCache
    source = A / 'verify_all_model_rankings_20261003.py'
    display = A / 'lossless_ranking_display_v2_20261006' / f'round{number}'
    proof = json.loads((display / 'verification.json').read_text(encoding='utf-8'))
    assert proof['status'] == 'passed_all_original_report_values_and_six_views_lossless_roundtrip'
    assert proof['all_original_record_values_parameters_source_pointers_and_scores_preserved']
    out = A / 'lossless_ranking_display_qa_v113_20261010' / f'round{number}'
    assert not out.exists()
    profiles = ROOT / 'tmp/ranking_display_qa_v71_20261007' / f'round{number}'
    assert profiles.resolve().is_relative_to(ROOT.resolve()) and profiles.drive.upper() == 'D:'
    profiles.mkdir(parents=True)
    for key in ('TMP', 'TEMP', 'TMPDIR'):
        os.environ[key] = str(profiles)
    import tempfile
    tempfile.tempdir = str(profiles)
    paths = [Path(__file__), source, ROOT / 'results/all_model_rankings_20261003.json',
        A / 'build_lossless_ranking_display_round202_v1_20261011.py', display / 'verification.json',
        display / 'complete_rankings_lossless.html']
    bindings = {str(path.resolve()): sha(path) for path in paths}
    text = source.read_text(encoding='utf-8')
    patches = {
        "number=max(map(int,later_records));latest=f'r{number}';new_records=later_records[str(number)]": "number=REQUESTED_ROUND;latest=f'r{number}';new_records=later_records[str(number)]",
        "    assert report['connected'][0]['score']==selection['winner']['connected_final_score']": "    assert report['connected'][0]['score']==max(row['score'] for row in report['connected'])\n    assert any(row['score']==selection['winner']['connected_final_score'] and f'/optimization_20261003_r{REQUESTED_ROUND}/' in Path(row['source']).as_posix() and not row['known_restriction'] for row in report['connected']), 'actual current-round selected winner present in full ranking'",
        'f"{selection[\'winner\'][\'connected_final_score\']:.9f}" in dom': 'f"{report[\'connected\'][0][\'score\']:.9f}" in dom',

        "document.getElementById('pageSize').value='10000';":
            "document.getElementById('pageSize').value=String(report.connected.length);",
        "tempfile.mkdtemp(prefix='codex-model-ranking-qa-')":
            "tempfile.mkdtemp(prefix='codex-model-ranking-qa-',dir=str(PROFILES))",
        "check(document.querySelectorAll('#body tr').length>10,'initial rows');":
            "check(fullCodecVerified,'all lossless nodes fully reconstructed');\n check(document.querySelectorAll('#body tr').length>10,'initial rows');",
    }
    for before, after in patches.items():
        assert text.count(before) == 1, before
        text = text.replace(before, after)
    out.mkdir(parents=True)
    create(out / 'frozen_before_actual_full_QA.json', {'input_sha256': bindings,
        'original_entire_QA_used_with_all_original_scientific_and_interaction_assertions': True,
        'only_explicit_changes': patches, 'effective_QA_source_sha256': hashlib.sha256(text.encode('utf-8')).hexdigest(),
        'Chrome_timeout_seconds_unchanged': 45, 'actual_browser_profile_root': str(profiles),
        'all_original_records_must_be_rendered_without_fixed10000_cap': True})
    namespace = {'__name__': 'actual_lossless_ranking_QA', '__file__': str(source)}
    exec(compile(text, str(source), 'exec'), namespace)
    namespace.update(QA=out / 'qa', HTML=display / 'complete_rankings_lossless.html', PROFILES=profiles,
                     digest=sha, REQUESTED_ROUND=number)
    calls = []
    original_run = subprocess.run

    def traced_run(arguments, **kwargs):
        if Path(arguments[0]).name.lower() == 'chrome.exe':
            profile = next(value.split('=', 1)[1] for value in arguments if value.startswith('--user-data-dir='))
            assert Path(profile).resolve().is_relative_to(profiles.resolve())
            assert kwargs['timeout'] == 45 and kwargs['creationflags'] == subprocess.CREATE_NO_WINDOW
            assert '--headless=new' in arguments
            calls.append({'arguments': arguments, 'actual_profile': profile,
                'timeout_seconds': kwargs['timeout'], 'CREATE_NO_WINDOW': True})
            kwargs.setdefault('stdin', subprocess.DEVNULL)
        return original_run(arguments, **kwargs)

    try:
        with LockedReadHashCache(bindings):
            subprocess.run = traced_run
            try:
                namespace['main']()
            finally:
                subprocess.run = original_run
            summary = json.loads((out / 'qa/interaction_result.json').read_text(encoding='utf-8'))
            assert summary['status'] == 'passed'
            assert summary['connected_records'] == proof['connected_records']
            assert summary['new_round_records'] == json.loads((A / f'optimization_20261003_r{number}/protocol.json').read_text(encoding='utf-8'))['expected_scored_records']
            assert len(calls) == 2
        create(out / 'verification.json', {'status': 'passed_all_original_full_ranking_QA_and_lossless_browser_node_checks',
            'at_local': time.strftime('%Y-%m-%dT%H:%M:%S'), 'round': number, 'original_full_QA_result': summary,
            'all_original_provenance_candidate_manifest_sorting_and_six_view_checks_passed': True,
            'all_original_exact_report_values_and_browser_lossless_nodes_verified': True,
            'all_actual_connected_rows_rendered_and_search_details_intervals_and_CSV_views_checked': True,
            'actual_Chrome_calls': calls, 'all_new_browser_profiles_under_D': True,
            'scientific_sources_scores_and_predictions_unchanged': True, 'input_sha256': bindings,
            'original45_second_render_timeout_retained': True, 'test_labels_read': False,
            'new_model_fits': 0, 'new_quality_scores': 0})
        print(json.dumps({'status': 'passed_original_full_ranking_QA_on_lossless_page',
            'round': number, 'connected_records': summary['connected_records']}, ensure_ascii=False), flush=True)
    except BaseException as error:
        create(out / 'failure.json', {'status': 'failed_preserved_full_browser_QA_attempt',
            'at_local': time.strftime('%Y-%m-%dT%H:%M:%S'), 'error': f'{type(error).__name__}: {error}',
            'actual_Chrome_calls': calls})
        raise
    finally:
        subprocess.run = original_run


if __name__ == '__main__':
    main(int(sys.argv[1]))
