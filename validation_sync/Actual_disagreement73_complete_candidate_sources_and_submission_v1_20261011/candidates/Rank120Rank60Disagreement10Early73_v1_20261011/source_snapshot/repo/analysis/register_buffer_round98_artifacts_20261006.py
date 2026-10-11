"""Register actual completed pilot evidence without new scores or a new scientific freeze."""
from pathlib import Path
from copy import deepcopy
import os
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path[:0] = [str(ROOT), str(A)]
from run_dependency_queue_v3_20261006 import read, sha, create

OUT = A / 'optimization_20261003_r98'
SOURCE_CANDIDATE = ROOT / 'candidates/causal_entry_exit_buffer_20261006'
CANDIDATE = ROOT / 'candidates/optimization_20261003_r98'
GRAPH_FIELD = 'entry_exit_buffer_complete_scheme_graph'


def main():
    assert not OUT.exists() and not CANDIDATE.exists()
    pilot_path = A / 'causal_entry_exit_buffer_official_pilot_20261006/verification.json'
    controls_path = A / 'causal_entry_exit_buffer_full_controls_v3_20261006/verification.json'
    pilot, controls = read(pilot_path), read(controls_path)
    actual = read(SOURCE_CANDIDATE / 'verification.json')
    original_selection = read(SOURCE_CANDIDATE / 'selection.json')
    seal_path = A / 'causal_entry_exit_buffer_release_20261006/source_package_verification.json'
    seal = read(seal_path)
    manifest_path = SOURCE_CANDIDATE / 'manifest.json'
    manifest = read(manifest_path)
    assert pilot['status'] == 'completed_actual16_training_official_scores_full_submission_release_pending'
    assert controls['status'] == 'passed_full5635800_row_entry_exit_buffer_causal_and_zero_identity_controls'
    assert seal['status'] == 'passed_sealed_actual_buffer_candidate'
    assert sha(manifest_path) == seal['manifest_sha256'] and manifest['status'] == 'passed'
    assert actual['status'] == 'passed' and actual['model_reload_bit_identical'] and actual['cold80_day_prefix_bit_identical']
    assert actual['rows'] == 1599600 and not actual['test_labels_read']
    assert original_selection['chosen_postprocessor']['margin'] == 0.
    assert len(pilot['records']) == len(controls['actual_all16_margin_controls']) == 16
    for relative, item in manifest['files'].items():
        assert sha(SOURCE_CANDIDATE / relative) == item['sha256'], relative
    for path, digest in pilot['input_sha256'].items():
        assert sha(path) == digest, path
    records = []
    authority = actual['current_parameter_authority']
    pins = {**pilot['input_sha256'], str(pilot_path): sha(pilot_path),
        str(controls_path): sha(controls_path), str(manifest_path): sha(manifest_path),
        str(seal_path): sha(seal_path)}
    registration_sources = [Path(__file__), A / 'optimize_training_round98.py',
        A / 'finalize_training_round98.py', A / 'run_buffer_round98_full_registration_20261006.py',
        A / 'publish_buffer_round98_full_validation_20261006.py',
        A / 'prepare_buffer_round98_registration_sources_20261006.py',
        A / 'buffer_round98_ranking_source_preparation_20261006.json',
        A / 'lossless_ranking_runtime_adapter_v6_20261006.py',
        A / 'build_lossless_ranking_display_v7_20261006.py',
        A / 'verify_lossless_ranking_display_v8_20261006.py',
        A / 'publish_explicit_parent_training_round_v2_20261005.py']
    for source in registration_sources:
        pins[str(source)] = sha(source)
    for relative, info in manifest['files'].items():
        pins[str(SOURCE_CANDIDATE / relative)] = info['sha256']
    for index, (measured, case) in enumerate(zip(pilot['records'], controls['actual_all16_margin_controls'])):
        assert measured['margin'] == case['margin']
        assert measured['prediction_numeric_bytes_sha256'] == case['full_prediction_numeric_bytes_sha256']
        capsule_path = Path(measured['official_score_cache']['official_metrics_source'])
        capsule = read(capsule_path)
        assert sha(capsule_path) == measured['official_metric_capsule_sha256']
        assert capsule['metrics'] == measured['metrics']
        pins[str(capsule_path)] = sha(capsule_path)
        row = deepcopy(original_selection['winner'])
        graph = deepcopy(actual['whole_scheme_graph'])
        graph['entry_exit_buffer']['margin'] = measured['margin']
        row.update(wave=381, arm=f'buffer_margin_{measured["margin"]:g}',
            connected_final_score=measured['connected_final_score'], metrics=deepcopy(measured['metrics']),
            official_score_cache=deepcopy(measured['official_score_cache']),
            causal_return_mapping=deepcopy(measured['actual_return_mapping']),
            original_official_pilot_record=str(A / f'causal_entry_exit_buffer_official_pilot_20261006/case{index:02d}_official.json'),
            original_numeric_prediction_sha256=measured['prediction_numeric_bytes_sha256'],
            original_official_metric_capsule_sha256=measured['official_metric_capsule_sha256'],
            actual_full_buffer_causal_control=deepcopy(case))
        # Keep old fields as history; both current graph aliases describe the
        # same complete authoritative graph, including this candidate's margin.
        row[authority] = deepcopy(graph)
        row[GRAPH_FIELD] = graph
        records.append(row)
    records.sort(key=lambda r: (-r['connected_final_score'], r[GRAPH_FIELD]['entry_exit_buffer']['margin']))
    winner = records[0]
    assert winner[GRAPH_FIELD] == actual['whole_scheme_graph']
    assert winner['metrics'] == original_selection['winner']['metrics']
    assert winner['metrics'] == read(A / 'optimization_20261003_r85/calibrated_csv_official.json')['metrics']
    OUT.mkdir()
    CANDIDATE.mkdir()
    # Alias immutable byte-verified outputs and models. Actual inference was
    # performed in SOURCE_CANDIDATE; do not claim these aliases were re-inferred.
    for relative in manifest['files']:
        target_relative = 'original_inference_selection.json' if relative == 'selection.json' else relative
        source = SOURCE_CANDIDATE / relative
        target = CANDIDATE / target_relative
        assert target.resolve().is_relative_to(CANDIDATE.resolve())
        target.parent.mkdir(parents=True, exist_ok=True)
        os.link(source, target)
        assert os.path.samefile(source, target)
    for source in registration_sources:
        target = CANDIDATE / 'registration_sources' / source.name
        target.parent.mkdir(parents=True, exist_ok=True)
        os.link(source, target)
        assert sha(target) == pins[str(source)]
    selection = deepcopy(original_selection)
    selection.update(winner=winner, ranking=records, baseline_score=pilot['records'][0]['connected_final_score'],
        score_gain=0., original_frozen_selection_source=str(SOURCE_CANDIDATE / 'selection.json'),
        original_frozen_selection_sha256=sha(SOURCE_CANDIDATE / 'selection.json'),
        registry_created_at_local=time.strftime('%Y-%m-%dT%H:%M:%S'),
        registration_only_of_existing_executed_validation=True,
        original_inference_parameter_authority=authority, registered_parameter_authority=GRAPH_FIELD)
    selection['frozen_sha256'].update({Path(p).relative_to(ROOT).as_posix(): digest for p, digest in pins.items()})
    create(OUT / 'selection.json', selection)
    create(CANDIDATE / 'selection.json', selection)
    create(CANDIDATE / 'registry_alias_verification.json', {
        'status': 'passed_exact_file_aliases_of_actually_inferred_sealed_candidate',
        'source_candidate': str(SOURCE_CANDIDATE), 'source_manifest_sha256': sha(manifest_path),
        'registered_graph_equals_original_actually_inferred_graph': True,
        'original_selection_freeze_timestamp_preserved': original_selection['frozen_at_local'],
        'no_new_inference_claimed_for_file_aliases': True, 'new_model_fits': 0,
        'new_quality_scores': 0, 'test_labels_read': False})
    create(OUT / 'protocol.json', {
        'status': 'registered_previously_executed_training_validation_scope',
        'registration_only_of_existing_executed_validation': True, 'expected_scored_records': 16,
        'waves': [381], 'explicit_parent_round': 85, 'new_model_training': False,
        'original_pre_scoring_protocol': str(A / 'causal_entry_exit_buffer_official_pilot_20261006/frozen_before_actual_official_scores.json'),
        'original_pre_inference_selection': str(SOURCE_CANDIDATE / 'selection.json'),
        'original_selection_frozen_at_local': original_selection['frozen_at_local'],
        'registry_created_at_local': selection['registry_created_at_local'],
        'input_sha256': pins, 'actual_rows_days_stocks': [5635800, 1212, 4650],
        'test_labels_read': False, 'global_feasible_direction_or_resource_exhaustion_claimed': False})
    create(OUT / 'wave381_results.json', {'status': 'complete', 'results': {r['arm']: r for r in records},
        'original_official_pilot_source': str(pilot_path), 'new_scores_by_registration': 0})
    create(OUT / 'component_audit.json', {'status': 'passed', 'actual_full_parent85_source':
        str(A / 'optimization_20261003_r85/component_audit.json'), 'actual_kernel_controls': str(controls_path),
        'all16_controlled_numeric_hashes_equal_actually_scored_hashes': True,
        'all8_selected_official_metrics_exact': True, 'new_model_fits': 0, 'test_labels_read': False})
    create(OUT / 'entry_exit_buffer_causal_checks.json', {'status': 'passed',
        'actual_source': str(controls_path), 'actual_all16_margin_controls': controls['actual_all16_margin_controls'],
        'actual5635800_rows_80_260_975_cold_prefixes_and_future_poison_controls': True,
        'complete_parent85_causal_checks': str(A / 'optimization_20261003_r85/streaming_rank_classifier_causal_checks.json'),
        'test_labels_read': False})
    create(OUT / 'causal_validation.json', {'status': 'passed', 'actual_full_buffer_controls': str(controls_path),
        'actual_parent_full_validation': str(A / 'optimization_20261003_r85/causal_validation.json'),
        'selected_zero_buffer_complete_numeric_identity': True,
        'raw_numeric_prediction_sha256': pilot['records'][0]['prediction_numeric_bytes_sha256'],
        'test_labels_read': False})
    selected_capsule = read(Path(winner['official_score_cache']['official_metrics_source']))
    prior = read(A / 'optimization_20261003_r85/calibrated_csv_official.json')
    assert selected_capsule['scope']['submission_csv_sha256'] == prior['csv_sha256']
    create(OUT / 'calibrated_csv_official.json', {**prior,
        'actual_original_scored_csv_capsule': winner['official_score_cache']['official_metrics_source'],
        'original_selected_official_pilot': winner['original_official_pilot_record'],
        'registration_not_a_new_official_evaluation': True})
    os.link(A / 'optimization_20261003_r85/selected_validation.npy', OUT / 'selected_validation.npy')
    create(OUT / 'actual_registration_preparation.json', {'status': 'passed_actual16_scores_causal_controls_and_sealed_future_candidate_registered',
        'original_pre_scoring_freeze_preserved': True, 'original_pre_inference_freeze_preserved': True,
        'existing_actual_official_records': 16, 'new_quality_scores_by_registration': 0,
        'candidate': str(CANDIDATE), 'full_ranking_QA_and_provenance_scope_pending': True,
        'test_labels_read': False})
    return read(OUT / 'protocol.json')


if __name__ == '__main__':
    main()
