"""Prepare round100 registration and extend routing without changing existing sources."""
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path.insert(0, str(A))
from run_dependency_queue_v3_20261006 import sha, create


def main():
    pins, records = {}, []
    recipes = [
        ('optimize_training_round99.py', 'optimize_training_round100.py'),
        ('finalize_training_round99.py', 'finalize_training_round100.py'),
        ('register_cohort_round99_artifacts_20261006.py', 'register_extended_cohort_round100_artifacts_20261006.py'),
        ('run_cohort_round99_full_registration_20261006.py', 'run_extended_cohort_round100_full_registration_20261006.py'),
        ('publish_cohort_round99_full_validation_20261006.py', 'publish_extended_cohort_round100_full_validation_20261006.py')]
    route = {
        'cohort_rank_calibration_source_freeze_20261006': 'extended_cohort_rank_calibration_source_freeze_20261006',
        'cohort_rank_calibration_release_20261006': 'extended_cohort_rank_calibration_release_20261006',
        'cohort_rank_calibration_full_controls_20261006': 'extended_cohort_rank_calibration_full_controls_20261006',
        'cohort_rank_calibration_official_pilot_20261006': 'extended_cohort_rank_calibration_official_pilot_20261006',
        'candidates/cohort_rank_calibration_20261006': 'candidates/extended_cohort_rank_calibration_20261006',
        'cohort_rank_calibration_scheme_graph': 'extended_cohort_rank_calibration_scheme_graph',
        'register_cohort_round99_artifacts_20261006': 'register_extended_cohort_round100_artifacts_20261006',
        'run_cohort_round99_full_registration_20261006': 'run_extended_cohort_round100_full_registration_20261006',
        'publish_cohort_round99_full_validation_20261006': 'publish_extended_cohort_round100_full_validation_20261006',
        'prepare_cohort_round99_registration_sources_20261006': 'prepare_extended_cohort_round100_registration_20261006',
        'cohort_round99_ranking_source_preparation_20261006': 'extended_cohort_round100_registration_source_preparation_20261006',
        'lossless_ranking_runtime_adapter_v7_20261006': 'lossless_ranking_runtime_adapter_v8_20261006',
        'build_lossless_ranking_display_v8_20261006': 'build_lossless_ranking_display_v9_20261006',
        'verify_lossless_ranking_display_v10_20261006': 'verify_lossless_ranking_display_v11_20261006',
        'lossless_ranking_display_qa_v10_20261006': 'lossless_ranking_display_qa_v11_20261006',
        'optimize_training_round99': 'optimize_training_round100',
        'finalize_training_round99': 'finalize_training_round100',
        'round99': 'round100', '_r99': '_r100', '(99,': '(100,', '(99)': '(100)',
        "'round': 99": "'round': 100", 'NUMBER = 99': 'NUMBER = 100',
        'wave382': 'wave383', 'wave=382': 'wave=383', 'WAVES = (382,)': 'WAVES = (383,)',
        "'waves': [382]": "'waves': [383]", 'actual17_': 'actual66_', 'full17_': 'full66_',
        'all17_': 'all66_', 'official17_': 'official66_', 'existing_actual_official_records\': 17': 'existing_actual_official_records\': 66',
        "== 17": "== 66", "'expected_scored_records': 17": "'expected_scored_records': 66",
        "'scored_records'] == full['scored_records'] == 17": "'scored_records'] == full['scored_records'] == 66",
        "'scored_records': 17": "'scored_records': 66", "'existing_official_scores_registered': 17": "'existing_official_scores_registered': 66",
        'collect(100, 10, 17)': 'collect(100, 11, 66)',
        'actual_complete_QA_version=10': 'actual_complete_QA_version=11', "'actual_full_QA_version': 10": "'actual_full_QA_version': 11",
        "'original_official_pilot_records_registered': 17": "'original_official_pilot_records_registered': 66",
        "'actual_annual_cohort_pair_fits': 16": "'actual_annual_cohort_pair_fits': 68",
        '17项': '66项', '17 条': '66 条', '17条': '66条',
        'neural17384_annual': 'neural16384_annual'}
    for old, new in recipes:
        original = (A / old).read_text(encoding='utf-8')
        text = original
        changes = {}
        for before, after in route.items():
            if before in text:
                text = text.replace(before, after)
                changes[before] = after
        if old == 'finalize_training_round99.py':
            before = "    assert (spec['weight'], spec['bins'], spec['pseudocount']) == (1., 32, 0.)"
            after = "    measured = read(record['original_frozen_selection_source'])['chosen_postprocessor']\n    assert all(spec[key] == measured[key] for key in ('weight', 'bins', 'pseudocount'))"
            assert text.count(before) == 1
            text = text.replace(before, after)
            changes[before] = after
        # Prevent the old helper's path typo and accidental1599600 string edits.
        assert 'neural17384' not in text and '15100600' not in text
        compile(text, str(A / new), 'exec')
        with (A / new).open('x', encoding='utf-8') as stream:
            stream.write(text)
        pins.update({str(A / old): sha(A / old), str(A / new): sha(A / new)})
        records.append({'original': old, 'effective': new, 'explicit_changes': changes})
    routing = [
        ('build_lossless_ranking_display_v8_20261006.py', 'build_lossless_ranking_display_v9_20261006.py', {'assert number == 99': 'assert number == 100'}),
        ('verify_lossless_ranking_display_v10_20261006.py', 'verify_lossless_ranking_display_v11_20261006.py', {
            'build_lossless_ranking_display_v8_20261006': 'build_lossless_ranking_display_v9_20261006',
            'lossless_ranking_display_qa_v10_20261006': 'lossless_ranking_display_qa_v11_20261006',
            'ranking_display_qa_v10_20261006': 'ranking_display_qa_v11_20261006'}),
        ('lossless_ranking_runtime_adapter_v7_20261006.py', 'lossless_ranking_runtime_adapter_v8_20261006.py', {
            'assert number == 99': 'assert number == 100',
            'build_lossless_ranking_display_v8_20261006': 'build_lossless_ranking_display_v9_20261006',
            'verify_lossless_ranking_display_v10_20261006': 'verify_lossless_ranking_display_v11_20261006',
            'lossless_ranking_display_qa_v10_20261006': 'lossless_ranking_display_qa_v11_20261006'})]
    for old, new, changes in routing:
        original = (A / old).read_text(encoding='utf-8')
        text = original
        for before in sorted(changes, key=len, reverse=True):
            assert before in text
            text = text.replace(before, changes[before])
        restored = text
        for before in sorted(changes, key=len, reverse=True):
            restored = restored.replace(changes[before], before)
        assert restored == original
        compile(text, str(A / new), 'exec')
        with (A / new).open('x', encoding='utf-8') as stream:
            stream.write(text)
        pins.update({str(A / old): sha(A / old), str(A / new): sha(A / new)})
        records.append({'original': old, 'effective': new, 'explicit_changes': changes,
            'entire_original_scientific_six_view_and_browser_checks_exact_after_reversing_routes': True})
    create(A / 'extended_cohort_round100_registration_source_preparation_20261006.json', {
        'status': 'prepared_complete_actual66_record_round100_registration_and_all_original_QA',
        'input_sha256': pins, 'controls': records,
        'nested_candidate_manifests_covered_by_outer_manifest': True,
        'lossless_large_JSON_publication_and_full_original_report_preserved': True,
        'browser_timeout_seconds': 45, 'new_quality_scores_by_preparation': 0, 'test_labels_read': False})


if __name__ == '__main__':
    main()
