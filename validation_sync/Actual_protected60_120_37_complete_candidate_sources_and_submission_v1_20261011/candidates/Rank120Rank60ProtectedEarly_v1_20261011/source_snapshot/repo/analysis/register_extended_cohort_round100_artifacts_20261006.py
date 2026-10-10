"""Register actual pilot scores and sealed inference without new fits or scoring."""
from pathlib import Path
from copy import deepcopy
import os
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path[:0] = [str(ROOT), str(A)]
from run_dependency_queue_v3_20261006 import read, sha, create
OUT = A / 'optimization_20261003_r100'
RELEASE = A / 'extended_cohort_rank_calibration_release_20261006'
SOURCE_CANDIDATE = ROOT / 'candidates/extended_cohort_rank_calibration_20261006'
CANDIDATE = ROOT / 'candidates/optimization_20261003_r100'
GRAPH_FIELD = 'extended_cohort_rank_calibration_scheme_graph'


def main():
    assert not OUT.exists() and not CANDIDATE.exists()
    pilot_path = A / 'extended_cohort_rank_calibration_official_pilot_20261006/verification.json'
    controls_path = A / 'extended_cohort_rank_calibration_full_controls_20261006/verification.json'
    pilot, controls = read(pilot_path), read(controls_path)
    actual = read(SOURCE_CANDIDATE / 'verification.json')
    original_selection = read(SOURCE_CANDIDATE / 'selection.json')
    seal_path = RELEASE / 'source_package_verification.json'
    manifest_path = SOURCE_CANDIDATE / 'manifest.json'
    manifest, seal = read(manifest_path), read(seal_path)
    assert pilot['status'] == 'completed_actual66_cohort_original_official_scores_full_qualification_pending'
    assert controls['status'] == 'passed_full66_cohort_causal_prefix_and_nonflagged_order_controls'
    assert seal['status'] == 'passed_sealed_actual_cohort_candidate'
    assert sha(manifest_path) == seal['manifest_sha256'] and manifest['status'] == 'passed'
    assert actual['status'] == 'passed' and actual['model_reload_bit_identical'] and actual['cold80_day_prefix_bit_identical']
    assert actual['rows'] == 1599600 and not actual['test_labels_read']
    assert len(pilot['records']) == len(controls['actual_cases']) == 66
    pins = {**pilot['input_sha256'], str(pilot_path): sha(pilot_path),
            str(controls_path): sha(controls_path), str(manifest_path): sha(manifest_path), str(seal_path): sha(seal_path)}
    registration_sources = [Path(__file__), A / 'optimize_training_round100.py', A / 'finalize_training_round100.py',
        A / 'run_extended_cohort_round100_full_registration_20261006.py', A / 'publish_extended_cohort_round100_full_validation_20261006.py',
        A / 'prepare_extended_cohort_round100_registration_20261006.py', A / 'extended_cohort_round100_registration_source_preparation_20261006.json',
        A / 'lossless_ranking_runtime_adapter_v8_20261006.py', A / 'build_lossless_ranking_display_v9_20261006.py',
        A / 'verify_lossless_ranking_display_v11_20261006.py', A / 'publish_explicit_parent_training_round_v2_20261005.py']
    pins.update({str(p): sha(p) for p in registration_sources})
    for relative, info in manifest['files'].items():
        assert sha(SOURCE_CANDIDATE / relative) == info['sha256'], relative
        pins[str(SOURCE_CANDIDATE / relative)] = info['sha256']
    records = []
    for measured, case in zip(pilot['records'], controls['actual_cases']):
        cfg = measured['configuration']
        assert all(cfg[k] == case[k] for k in ('weight', 'bins', 'pseudocount'))
        assert measured['prediction_numeric_bytes_sha256'] == case['full_prediction_numeric_bytes_sha256']
        capsule_path = Path(measured['official_score_cache']['official_metrics_source'])
        assert sha(capsule_path) == measured['official_metric_capsule_sha256']
        assert read(capsule_path)['metrics'] == measured['metrics']
        pins[str(capsule_path)] = sha(capsule_path)
        row = deepcopy(original_selection['winner'])
        graph = deepcopy(actual['whole_scheme_graph'])
        if measured['case'] != pilot['best']['case']:
            graph['cohort_rank_calibration'] = {**cfg,
                'annual_models_source': measured['annual_model_source'], 'future_curve_model': None,
                'future_curve_not_fitted_for_nonselected_comparison': True,
                'position': 'after_complete_parent95_graph_including_temporal_transform'}
        row[GRAPH_FIELD] = graph
        row.update(wave=383, arm=f'cohort_case_{measured["case"]:02d}',
            connected_final_score=measured['connected_final_score'], metrics=deepcopy(measured['metrics']),
            official_score_cache=deepcopy(measured['official_score_cache']),
            causal_return_mapping=deepcopy(measured['actual_return_mapping']),
            original_official_pilot_record=str(A / f'extended_cohort_rank_calibration_official_pilot_20261006/case{measured["case"]:02d}_official.json'),
            original_numeric_prediction_sha256=measured['prediction_numeric_bytes_sha256'],
            original_official_metric_capsule_sha256=measured['official_metric_capsule_sha256'],
            actual_full_cohort_causal_control=deepcopy(case))
        records.append(row)
    records.sort(key=lambda r: (-r['connected_final_score'], r[GRAPH_FIELD]['cohort_rank_calibration']['weight']))
    winner = records[0]
    assert winner[GRAPH_FIELD] == actual['whole_scheme_graph']
    assert winner['metrics'] == original_selection['winner']['metrics'] == pilot['best']['metrics']
    for path, digest in pins.items():
        assert sha(path) == digest, path
    OUT.mkdir()
    CANDIDATE.mkdir()
    for relative in manifest['files']:
        target_relative = 'original_inference_selection.json' if relative == 'selection.json' else relative
        source, target = SOURCE_CANDIDATE / relative, CANDIDATE / target_relative
        assert target.resolve().is_relative_to(CANDIDATE.resolve())
        target.parent.mkdir(parents=True, exist_ok=True)
        os.link(source, target)
    for source in registration_sources:
        target = CANDIDATE / 'registration_sources' / source.name
        target.parent.mkdir(parents=True, exist_ok=True)
        os.link(source, target)
    selection = deepcopy(original_selection)
    selection.update(winner=winner, ranking=records,
        original_frozen_selection_source=str(SOURCE_CANDIDATE / 'selection.json'),
        original_frozen_selection_sha256=sha(SOURCE_CANDIDATE / 'selection.json'),
        registry_created_at_local=time.strftime('%Y-%m-%dT%H:%M:%S'),
        registration_only_of_existing_executed_validation=True,
        original_inference_parameter_authority=GRAPH_FIELD, registered_parameter_authority=GRAPH_FIELD)
    selection['frozen_sha256'].update({Path(p).relative_to(ROOT).as_posix(): digest for p, digest in pins.items()})
    create(OUT / 'selection.json', selection)
    create(CANDIDATE / 'selection.json', selection)
    create(CANDIDATE / 'registry_alias_verification.json', {
        'status': 'passed_exact_file_aliases_of_actually_inferred_sealed_candidate',
        'source_candidate': str(SOURCE_CANDIDATE), 'source_manifest_sha256': sha(manifest_path),
        'registered_graph_equals_original_actually_inferred_graph': True,
        'original_selection_freeze_timestamp_preserved': original_selection['frozen_at_local'],
        'no_new_inference_claimed_for_file_aliases': True, 'new_quality_scores': 0, 'test_labels_read': False})
    create(OUT / 'protocol.json', {
        'status': 'registered_previously_executed_training_validation_scope',
        'registration_only_of_existing_executed_validation': True, 'expected_scored_records': 66,
        'waves': [383], 'explicit_parent_round': 95, 'new_model_training': False,
        'actual_annual_cohort_pair_fits': 68, 'actual_final_cohort_pair_fits': 1, 'new_native_base_model_fits': 0,
        'original_pre_scoring_protocol': str(A / 'extended_cohort_rank_calibration_official_pilot_20261006/frozen_before_actual_official_scores.json'),
        'original_pre_inference_selection': str(SOURCE_CANDIDATE / 'selection.json'),
        'original_selection_frozen_at_local': original_selection['frozen_at_local'],
        'registry_created_at_local': selection['registry_created_at_local'],
        'input_sha256': pins, 'actual_rows_days_stocks': [5635800, 1212, 4650],
        'test_labels_read': False, 'global_feasible_direction_or_resource_exhaustion_claimed': False})
    create(OUT / 'wave383_results.json', {'status': 'complete', 'results': {r['arm']: r for r in records},
        'original_official_pilot_source': str(pilot_path), 'new_scores_by_registration': 0})
    create(OUT / 'component_audit.json', {'status': 'passed', 'actual_full_parent95_source':
        str(A / 'optimization_20261003_r95/component_audit.json'), 'actual_kernel_controls': str(controls_path),
        'all66_controlled_numeric_hashes_equal_actual_scored_hashes': True,
        'all8_baseline_official_metrics_exact': True, 'test_labels_read': False})
    create(OUT / 'cohort_rank_calibration_causal_checks.json', {'status': 'passed',
        'actual_source': str(controls_path), 'actual_all66_controls': controls['actual_cases'],
        'current2024_label_poisoning_all_annual_curves_exact': True,
        'actual_future_curve_reload_and_independent_decoder': str(SOURCE_CANDIDATE / 'cohort_curve_replay_verification.json'),
        'complete_parent95_causal_checks': str(A / 'optimization_20261003_r95/gradient_sampling_reference_causal_checks.json'),
        'test_labels_read': False})
    create(OUT / 'causal_validation.json', read(RELEASE / 'causal_validation.json'))
    create(OUT / 'calibrated_csv_official.json', {**read(RELEASE / 'calibrated_csv_official.json'),
        'original_selected_official_pilot': winner['original_official_pilot_record'],
        'registration_not_a_new_official_evaluation': True})
    os.link(RELEASE / 'selected_validation.npy', OUT / 'selected_validation.npy')
    create(OUT / 'actual_registration_preparation.json', {
        'status': 'passed_actual66_scores_causal_controls_and_sealed_future_candidate_registered',
        'original_pre_scoring_and_pre_inference_freezes_preserved': True,
        'existing_actual_official_records': 66, 'new_quality_scores_by_registration': 0,
        'candidate': str(CANDIDATE), 'full_ranking_QA_and_provenance_scope_pending': True, 'test_labels_read': False})
    return read(OUT / 'protocol.json')


if __name__ == '__main__':
    main()
