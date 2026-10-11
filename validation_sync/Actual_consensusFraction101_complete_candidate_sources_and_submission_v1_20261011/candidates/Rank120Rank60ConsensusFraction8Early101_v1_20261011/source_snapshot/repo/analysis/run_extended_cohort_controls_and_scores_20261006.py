"""Run wider controls and official scoring without changing any frozen source."""
from pathlib import Path
import os
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path[:0] = [str(ROOT), str(A)]
from run_dependency_queue_v3_20261006 import read, create, sha, owned
from hidden_windows_child_creation_20261006 import install
OUT = A / 'extended_cohort_search_execution_20261006'


def replace_once(text, before, after):
    assert text.count(before) == 1, before
    return text.replace(before, after)


def main():
    import psutil
    assert not OUT.exists()
    OUT.mkdir()
    definition = read(A / 'extended_cohort_search_preparation_20261006.json')
    pins = dict(definition['input_sha256'])
    controls_source = A / 'run_cohort_rank_calibration_controls_20261006.py'
    pilot_source = A / 'score_cohort_rank_calibration_pilot_20261006.py'
    sources = [Path(__file__), controls_source, pilot_source,
               A / 'extended_cohort_search_preparation_20261006.json',
               A / 'cohort_rank_calibration_release_20261006/verification.json',
               A / 'cohort_rank_calibration_release_20261006/selection.json',
               A / 'publish_extended_cohort_search_20261006.py']
    pins.update({str(p): sha(p) for p in sources})
    create(OUT / 'frozen_before_admission.json', {'input_sha256': pins, 'expected_scored_records': 66,
        'wait_for_original_round99_qualification_and_available_memory': True,
        'all_original_workers_preserved': True, 'test_labels_read': False})
    while True:
        for path, digest in pins.items():
            assert sha(path) == digest, path
        receipt = A / 'github_validation_sync_main_20261005/round99_receipt.json'
        qualified = A / 'optimization_20261003_r99/full_registration_execution.json'
        if receipt.exists() and qualified.exists() and read(qualified)['status'] == 'passed' and psutil.virtual_memory().available >= 9 * 2**30:
            break
        time.sleep(30)
    assert read(receipt)['status'] == 'pushed_and_remote_head_verified'
    assert read(receipt)['actual_full_QA_version'] == 10
    assert read(receipt)['scored_records'] == 17
    pins.update({str(receipt): sha(receipt), str(qualified): sha(qualified)})
    create(OUT / 'admitted.json', {'at_local': time.strftime('%Y-%m-%dT%H:%M:%S'),
        'actual_round99_receipt_sha256': sha(receipt), 'actual_round99_full_execution_sha256': sha(qualified),
        'available_RAM_GiB': psutil.virtual_memory().available / 2**30, 'test_labels_read': False})
    text = controls_source.read_text(encoding='utf-8')
    text = text.replace('cohort_rank_calibration_full_controls_20261006', 'extended_cohort_rank_calibration_full_controls_20261006')
    text = text.replace('cohort_rank_calibration_20261006 as method', 'cohort_rank_calibration_v2_20261006 as method')
    before = "for bins in (32, 128) for pseudo in (0., 200.) for weight in (.1, .25, .5, 1.)]"
    after = "for bins in (8, 16, 64, 256) for pseudo in (0., 50., 200., 1000.) for weight in (.25, .5, .75, 1.)]\n    cases.insert(1, {'weight': 1., 'bins': 32, 'pseudocount': 0.})"
    text = replace_once(text, before, after)
    text = replace_once(text, 'for bins in (32, 128):', 'for bins in (8, 16, 32, 64, 256):')
    text = replace_once(text, 'for pseudo in (0., 200.):', "for pseudo in (0., 50., 200., 1000.):\n                if bins == 32 and pseudo != 0.:\n                    continue")
    text = text.replace('all17_', 'all66_').replace('passed_full17_', 'passed_full66_').replace("'expected_cases': 17", "'expected_cases': 66")
    text = replace_once(text, "'actual_annual_cohort_curve_fits': 16", "'actual_annual_cohort_curve_fits': 68")
    text = replace_once(text, 'pins = {str(p): sha(p) for p in sources}', 'pins = {**EXTRA_SOURCE_PINS, **{str(p): sha(p) for p in sources}}')
    control_namespace = {'__name__': 'extended_cohort_controls', '__file__': __file__, 'EXTRA_SOURCE_PINS': pins}
    exec(compile(text, str(controls_source), 'exec'), control_namespace)
    restore = install()
    try:
        control_namespace['main']()
        from publish_extended_cohort_search_20261006 import main as publish
        try:
            publish('controls')
        except Exception as exc:
            create(OUT / 'controls_publication_pending.json', {'error': f'{type(exc).__name__}: {exc}',
                'actual_controls_completed_and_preserved': True, 'official_scoring_continues': True})
        text = pilot_source.read_text(encoding='utf-8')
        text = text.replace('cohort_rank_calibration_official_pilot_20261006', 'extended_cohort_rank_calibration_official_pilot_20261006')
        text = text.replace('cohort_rank_calibration_full_controls_20261006', 'extended_cohort_rank_calibration_full_controls_20261006')
        text = text.replace('cohort_rank_calibration_20261006 as method', 'cohort_rank_calibration_v2_20261006 as method')
        # Controls execute synchronously in this owned workflow; no separate
        # completed service is invented for them.
        start = "    service = A / 'service_owned_workflows_20261006/cohort_rank_calibration_controls'"
        end = '    assert not OUT.exists()'
        left, right = text.index(start), text.index(end)
        text = text[:left] + text[right:]
        text = text.replace('full17_', 'full66_').replace('actual17_', 'actual66_').replace('all17_', 'all66_')
        text = text.replace('len(cases) == 17', 'len(cases) == 66')
        text = text.replace("'expected_records': 17", "'expected_records': 66")
        text = text.replace("'actual_annual_cohort_calibration_fits_reused': 16", "'actual_annual_cohort_calibration_fits_reused': 68")
        text = text.replace("'actual_annual_cohort_calibration_fits': 16", "'actual_annual_cohort_calibration_fits': 68")
        text = text.replace("'new_quality_score_records': 17", "'new_quality_score_records': 66")
        text = replace_once(text, '            for field in', "            if i == 1:\n                assert metrics == read(A / 'cohort_rank_calibration_release_20261006/calibrated_csv_official.json')['metrics']\n            for field in")
        namespace = {'__name__': 'extended_cohort_official_scores', '__file__': __file__}
        exec(compile(text, str(pilot_source), 'exec'), namespace)
        namespace['main']()
        result = read(A / 'extended_cohort_rank_calibration_official_pilot_20261006/verification.json')
        create(OUT / 'verification.json', {'status': 'passed_actual66_extended_cohort_controls_and_official_scores',
            'actual_official_pilot_source': str(A / 'extended_cohort_rank_calibration_official_pilot_20261006/verification.json'),
            'score_gain_over_qualified_round99': result['best']['connected_final_score'] - read(A / 'cohort_rank_calibration_release_20261006/verification.json')['selected_official_score'],
            'new_native_base_model_fits': 0, 'actual_annual_pair_fits': 68,
            'frozen_candidate_inference_and_full_ranking_still_required': True, 'test_labels_read': False})
        try:
            publish('pilot')
        except Exception as exc:
            create(OUT / 'pilot_publication_pending.json', {'error': f'{type(exc).__name__}: {exc}',
                'actual_scores_completed_and_preserved': True, 'publication_still_required': True})
    finally:
        create(OUT / 'actual_hidden_children.json', {'events': restore()})


if __name__ == '__main__':
    try:
        main()
    except BaseException as exc:
        if OUT.exists() and not (OUT / 'failure.json').exists():
            create(OUT / 'failure.json', {'status': 'failed_preserved_extended_cohort_search',
                'error': f'{type(exc).__name__}: {exc}', 'test_labels_read': False})
        raise
